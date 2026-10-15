"""Process the Meseeks inbox into _data/meseeks.json.

  python -m meseeks.run --dry-run --eml tests/meseeks/fixtures   # no mail server, no writes
  python -m meseeks.run --eml tests/meseeks/fixtures              # write from fixtures
  python -m meseeks.run                                           # IMAP (env vars in mailbox.py)
  python -m meseeks.run --adk [--dry-run] [--eml DIR]             # same, through the ADK agent (agent.yaml)

Run from the agents/ directory, or with agents/ on PYTHONPATH."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml

from . import mailbox
from .classifier import classify
from .guardrails import Inbound, enforce, to_post

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "_data" / "meseeks.json"
FIRMS = ROOT / "_data" / "meseeks_firm_domains.yml"
LOG = ROOT / "logs" / "meseeks"


def load_firm_domains(path: Path = FIRMS) -> set[str]:
    if not path.exists():
        return set()
    doc = yaml.safe_load(path.read_text()) or {}
    return {f["domain"].lower() for f in doc.get("firms") or [] if f.get("domain")}


def load_data(path: Path = DATA) -> dict:
    if path.exists():
        return json.loads(path.read_text())
    return {"generated_utc": "", "inbox": "meseeks@legalluminary.com", "retention_days": 60, "posts": []}


def order_posts(posts: list[dict]) -> list[dict]:
    """Pinned threads first (by thread number, e.g. -1), then everything else, most recently updated first.

    Every post carries ``updated`` (defaults to ``received``); an answer bumps the question it
    answers, so a question thread rises when a firm replies to it.
    """
    for p in posts:
        p["updated"] = max(p.get("updated") or p["received"], p["received"])
    by_id = {p["id"]: p for p in posts}
    for p in posts:
        q = by_id.get(p.get("in_reply_to") or "")
        if q is not None and p["category"] == "answer":
            q["updated"] = max(q["updated"], p["received"])
    pinned = sorted((p for p in posts if p.get("pinned")), key=lambda p: (p.get("thread", 0), p["received"]))
    rest = sorted((p for p in posts if not p.get("pinned")), key=lambda p: (p["updated"], p["received"], p["id"]), reverse=True)
    return pinned + rest


def expire(data: dict, now: datetime) -> int:
    """Drop posts older than retention_days; a pinned post stays until it is unpinned or removed by hand."""
    keep_after = now - timedelta(days=int(data.get("retention_days", 60)))
    before = len(data["posts"])
    data["posts"] = [p for p in data["posts"]
                     if p.get("pinned") or datetime.strptime(p["received"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc) >= keep_after]
    return before - len(data["posts"])


def process(messages: list[Inbound], data: dict, firm_domains: set[str], now: datetime) -> list[dict]:
    existing_ids = {p["id"] for p in data["posts"]}
    existing_hashes = {p.get("hash") for p in data["posts"]}
    question_ids = {p["id"] for p in data["posts"] if p["category"] == "question"}
    audit = []
    for msg in messages:
        category, confidence = classify(msg)
        d = enforce(msg, category, confidence, firm_domains, question_ids)
        entry = {"message_id": msg.message_id, "sender_domain": msg.sender.split("@")[-1].strip(">").lower(),
                 "category": d.category, "publish": d.publish, "reason": d.reason, "confidence": d.confidence}
        if d.publish:
            post = to_post(msg, d.category, firm_domains)
            if post["id"] in existing_ids or post["hash"] in existing_hashes:
                entry.update(publish=False, reason="duplicate")
            else:
                data["posts"].append(post)
                existing_ids.add(post["id"])
                existing_hashes.add(post["hash"])
                if post["category"] == "question":
                    question_ids.add(post["id"])
                entry["post_id"] = post["id"]
        audit.append(entry)
    data["posts"] = order_posts(data["posts"])
    data["generated_utc"] = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    return audit


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--eml", help="directory of .eml files instead of IMAP")
    ap.add_argument("--dry-run", action="store_true", help="classify and report; write nothing")
    ap.add_argument("--data", default=str(DATA))
    ap.add_argument("--adk", action="store_true", help="run through agents/meseeks/agent.yaml (local model -> coders -> API -> rules)")
    args = ap.parse_args(argv)

    if args.adk:
        import os

        from .adk_agent import run_adk

        os.environ["MESEEKS_DATA"] = args.data
        if args.eml:
            os.environ["MESEEKS_EML_DIR"] = args.eml
        if args.dry_run:
            os.environ["MESEEKS_DRY_RUN"] = "1"
        print(json.dumps(run_adk(), indent=2))
        return 0

    now = datetime.now(timezone.utc)
    data = load_data(Path(args.data))
    firm_domains = load_firm_domains()

    imap = None
    if args.eml:
        messages = mailbox.from_directory(args.eml)
    else:
        imap = mailbox.Imap()
        messages = imap.unseen()

    expired = expire(data, now)
    audit = process(messages, data, firm_domains, now)
    published = [a for a in audit if a["publish"]]

    print(json.dumps({"messages": len(messages), "published": len(published), "expired": expired,
                      "audit": audit}, indent=2))

    if args.dry_run:
        return 0

    Path(args.data).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    LOG.mkdir(parents=True, exist_ok=True)
    (LOG / f"{now:%Y-%m-%d}.jsonl").open("a").write(
        "\n".join(json.dumps({"run": data["generated_utc"], **a}) for a in audit) + ("\n" if audit else ""))
    if imap:
        for a in audit:
            imap.mark_processed(a["message_id"])
        imap.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
