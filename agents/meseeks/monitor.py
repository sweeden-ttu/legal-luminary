"""Background monitor: the ModelDependencyFree orchestrator run on a schedule from a witness machine.

One cycle = git pull --ff-only  ->  python -m meseeks.run --adk  ->  commit + push whatever changed
(_data/meseeks.json, _data/meseeks_review.json, logs/meseeks). Mail is read over IMAPS from the
mailbox host (MESEEKS_IMAP_HOST, 192.168.0.15) in every folder in MESEEKS_IMAP_FOLDERS
(default INBOX; add Sent to watch outgoing mail too).

  python -m meseeks.monitor                 # one cycle
  python -m meseeks.monitor --loop 7200     # every two hours, until stopped
  python -m meseeks.monitor --install       # print the launchd (macOS) / systemd (Linux) unit to install

Every step is bounded: git and the orchestrator each get a timeout, a failed cycle is logged and the
next one runs on schedule, and nothing is pushed unless the Meseeks tests pass locally.
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOG = ROOT / "logs" / "meseeks" / "monitor.jsonl"
GIT_TIMEOUT = float(os.environ.get("MESEEKS_GIT_TIMEOUT", "120"))
RUN_TIMEOUT = float(os.environ.get("MESEEKS_RUN_TIMEOUT", "1500"))
TRACKED = ["_data/meseeks.json", "_data/meseeks_review.json", "logs/meseeks"]


def _sh(argv: list[str], timeout: float, cwd: Path = ROOT, env: dict | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(argv, cwd=cwd, capture_output=True, text=True, timeout=timeout,
                          env={**os.environ, **(env or {}), "GIT_TERMINAL_PROMPT": "0"})


def _log(entry: dict) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a") as fh:
        fh.write(json.dumps(entry) + "\n")


def cycle(branch: str | None = None, push: bool = True, dry_run: bool = False) -> dict:
    started = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    out: dict = {"started": started, "steps": {}}
    try:
        if branch:
            _sh(["git", "checkout", "-q", branch], GIT_TIMEOUT)
        pull = _sh(["git", "pull", "--ff-only", "-q"], GIT_TIMEOUT)
        out["steps"]["pull"] = pull.returncode == 0 or pull.stderr[-300:]

        folders = [f.strip() for f in os.environ.get("MESEEKS_IMAP_FOLDERS", os.environ.get("MESEEKS_IMAP_FOLDER", "INBOX")).split(",") if f.strip()]
        runs = []
        for folder in folders:
            args = [sys.executable, "-m", "meseeks.run", "--adk"] + (["--dry-run"] if dry_run else [])
            r = _sh(args, RUN_TIMEOUT, cwd=ROOT / "agents", env={"MESEEKS_IMAP_FOLDER": folder})
            try:
                summary = json.loads(r.stdout[r.stdout.find("{"):]) if r.returncode == 0 and "{" in r.stdout else {}
            except json.JSONDecodeError:
                summary = {}
            runs.append({"folder": folder, "rc": r.returncode,
                         "published": summary.get("published"), "held": summary.get("held"),
                         "for_review": summary.get("for_review"), "backend": summary.get("backend"),
                         "error": r.stderr[-300:] if r.returncode else None})
        out["steps"]["runs"] = runs

        if dry_run or not push:
            out["steps"]["push"] = "skipped"
        else:
            tests = _sh([sys.executable, "-m", "pytest", "tests/meseeks", "-q", "-p", "no:cacheprovider", "-W", "ignore"], RUN_TIMEOUT)
            out["steps"]["tests"] = "passed" if tests.returncode == 0 else tests.stdout[-300:]
            if tests.returncode == 0:
                _sh(["git", "add", "--", *[p for p in TRACKED if (ROOT / p).exists()]], GIT_TIMEOUT)
                diff = _sh(["git", "diff", "--cached", "--quiet"], GIT_TIMEOUT)
                if diff.returncode == 1:
                    n = sum((r.get("published") or 0) for r in runs)
                    h = sum((r.get("held") or 0) for r in runs)
                    _sh(["git", "commit", "-q", "-m", f"Meseeks: {n} posted, {h} held ({started[:10]})"], GIT_TIMEOUT)
                    pushed = _sh(["git", "push", "-q"], GIT_TIMEOUT)
                    out["steps"]["push"] = "pushed" if pushed.returncode == 0 else pushed.stderr[-300:]
                else:
                    out["steps"]["push"] = "nothing to commit"
            else:
                out["steps"]["push"] = "withheld: tests failed"
    except subprocess.TimeoutExpired as e:
        out["error"] = f"timeout: {e.cmd[:3]}"
    except Exception as e:  # noqa: BLE001 - a failed cycle must not stop the schedule
        out["error"] = f"{type(e).__name__}: {e}"[:300]
    out["finished"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    _log(out)
    return out


LAUNCHD = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>com.legalluminary.meseeks.monitor</string>
  <key>ProgramArguments</key><array>
    <string>{python}</string><string>-m</string><string>meseeks.monitor</string>
  </array>
  <key>WorkingDirectory</key><string>{agents}</string>
  <key>EnvironmentVariables</key><dict>
    <key>PATH</key><string>/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin</string>
    <key>MESEEKS_WITNESS</key><string>{witness}</string>
  </dict>
  <key>StartInterval</key><integer>{interval}</integer>
  <key>RunAtLoad</key><true/>
  <key>StandardOutPath</key><string>{root}/logs/meseeks/monitor.out</string>
  <key>StandardErrorPath</key><string>{root}/logs/meseeks/monitor.err</string>
</dict></plist>
# install:  cp this to ~/Library/LaunchAgents/com.legalluminary.meseeks.monitor.plist
#           launchctl load -w ~/Library/LaunchAgents/com.legalluminary.meseeks.monitor.plist
# the MESEEKS_IMAP_* variables come from ~/.zshrc (see ~/ll/meseeks_setup_secrets.sh) or add them above
"""

SYSTEMD = """# ~/.config/systemd/user/meseeks-monitor.service
[Unit]
Description=Meseeks inbox monitor (ModelDependencyFree orchestrator)
[Service]
Type=oneshot
WorkingDirectory={agents}
EnvironmentFile=%h/.config/meseeks/env
ExecStart={python} -m meseeks.monitor

# ~/.config/systemd/user/meseeks-monitor.timer
[Unit]
Description=Run the Meseeks inbox monitor every two hours
[Timer]
OnBootSec=5min
OnUnitActiveSec={interval}s
Persistent=true
[Install]
WantedBy=timers.target

# install:  put MESEEKS_IMAP_HOST/USER/PASSWORD (and MESEEKS_WITNESS, MESEEKS_IMAP_CA) in ~/.config/meseeks/env
#           systemctl --user daemon-reload && systemctl --user enable --now meseeks-monitor.timer
"""


def unit(interval: int) -> str:
    ctx = {"python": sys.executable, "agents": str(ROOT / "agents"), "root": str(ROOT),
           "interval": interval, "witness": os.environ.get("MESEEKS_WITNESS", "sweeden@legalluminary.com")}
    return (LAUNCHD if platform.system() == "Darwin" else SYSTEMD).format(**ctx)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--loop", type=int, default=0, help="seconds between cycles; 0 = run once")
    ap.add_argument("--branch", default=None)
    ap.add_argument("--no-push", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--install", action="store_true", help="print the launchd / systemd unit for a 2-hour schedule")
    args = ap.parse_args(argv)
    if args.install:
        print(unit(args.loop or 7200))  # noqa: T201
        return 0
    while True:
        out = cycle(args.branch, push=not args.no_push, dry_run=args.dry_run)
        print(json.dumps(out))  # noqa: T201
        if not args.loop:
            return 0 if "error" not in out else 1
        time.sleep(args.loop)


if __name__ == "__main__":
    sys.exit(main())
