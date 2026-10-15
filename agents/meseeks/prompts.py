"""Prompt registry: every prompt the Meseeks agents use is pulled from one Evidently project.

Host:     MESEEKS_EVIDENTLY_URL        (default http://192.168.0.15:8000)
Project:  MESEEKS_EVIDENTLY_PROJECT_ID (or `project_id` in agents/meseeks/prompts.yml)
Prompts are looked up by name (GET /api/prompts/by-name/<name>?project_id=...) and the latest
version is used. The lookup has a short timeout; when the host is down or the prompt is missing
the committed fallback in agents/meseeks/prompts/<name>.md is used, so a run never hangs on it.

  python -m meseeks.prompts init     # create the project if needed, seed every fallback, print ids
  python -m meseeks.prompts pull     # show which prompt versions a run would use right now
  python -m meseeks.prompts push NAME  # bump NAME to the committed fallback text
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
CONFIG = HERE / "prompts.yml"
FALLBACKS = HERE / "prompts"
TIMEOUT = float(os.environ.get("MESEEKS_EVIDENTLY_TIMEOUT", "3"))
UA = "LegalLuminaryMeseeks/1.0 (+https://legalluminary.com/meseeks/)"

#: Prompt names, as registered in Evidently. One registry entry per model-facing text.
NAMES = ("meseeks.instruction", "meseeks.coder_wrapper", "meseeks.classifier")


@dataclass
class Resolved:
    name: str
    text: str
    source: str  # "evidently:<version id>" | "fallback"
    version: int | None = None


def config() -> dict:
    doc = yaml.safe_load(CONFIG.read_text()) if CONFIG.exists() else {}
    doc = doc or {}
    doc["url"] = os.environ.get("MESEEKS_EVIDENTLY_URL") or doc.get("url") or "http://192.168.0.15:8000"
    doc["project_id"] = os.environ.get("MESEEKS_EVIDENTLY_PROJECT_ID") or doc.get("project_id") or ""
    doc["project_name"] = doc.get("project_name") or "Meseeks"
    doc["url"] = doc["url"].rstrip("/")
    return doc


def fallback(name: str) -> str:
    p = FALLBACKS / f"{name}.md"
    return p.read_text().strip() if p.exists() else ""


def _request(url: str, method: str = "GET", body: dict | None = None, timeout: float = TIMEOUT):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method,
                                 headers={"Accept": "application/json", "Content-Type": "application/json", "User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read().decode()
    return json.loads(raw) if raw.strip() else None


def _content_text(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, dict):
        if isinstance(content.get("text"), str):
            return content["text"]
        if isinstance(content.get("template"), str):
            return content["template"]
        msgs = content.get("messages")
        if isinstance(msgs, list):
            return "\n\n".join(str(m.get("content", "")) for m in msgs if isinstance(m, dict))
    return str(content)


def fetch(name: str, cfg: dict | None = None) -> Resolved | None:
    """Latest version of a prompt from Evidently, or None when it cannot be reached."""
    cfg = cfg or config()
    if not cfg["project_id"] or os.environ.get("MESEEKS_PROMPTS_OFFLINE"):
        return None
    base = cfg["url"]
    try:
        prompt = _request(f"{base}/api/prompts/by-name/{urllib.parse.quote(name)}?project_id={cfg['project_id']}")
        version = _request(f"{base}/api/prompts/{prompt['id']}/versions/latest")
    except Exception:  # noqa: BLE001 - any failure means "use the fallback"
        return None
    text = _content_text(version.get("content")).strip()
    if not text:
        return None
    return Resolved(name, text, f"evidently:{version.get('id')}", version.get("version"))


def get(name: str, cfg: dict | None = None) -> Resolved:
    """Prompt text to use right now: Evidently if reachable, else the committed fallback."""
    got = fetch(name, cfg)
    if got:
        return got
    return Resolved(name, fallback(name), "fallback")


# --------------------------------------------------------------------------- admin commands

def _project_id(cfg: dict) -> str:
    base = cfg["url"]
    if cfg["project_id"]:
        _request(f"{base}/api/projects/{cfg['project_id']}/info")
        return cfg["project_id"]
    for p in _request(f"{base}/api/projects") or []:
        if p.get("name") == cfg["project_name"]:
            return p["id"]
    created = _request(f"{base}/api/projects", "POST",
                       {"name": cfg["project_name"], "description": "Prompts for the Meseeks inbox agents (legalluminary.com/meseeks)"})
    return created["id"] if isinstance(created, dict) else str(created).strip('"')


def _get_or_create_prompt(base: str, project_id: str, name: str) -> dict:
    try:
        return _request(f"{base}/api/prompts/by-name/{urllib.parse.quote(name)}?project_id={project_id}")
    except urllib.error.HTTPError as e:
        if e.code != 404:
            raise
    return _request(f"{base}/api/prompts?project_id={project_id}", "POST", {"name": name, "project_id": project_id})


def push(name: str, cfg: dict | None = None) -> dict:
    cfg = cfg or config()
    base = cfg["url"]
    project_id = _project_id(cfg)
    prompt = _get_or_create_prompt(base, project_id, name)
    versions = _request(f"{base}/api/prompts/{prompt['id']}/versions") or []
    text = fallback(name)
    latest = max(versions, key=lambda v: v.get("version", 0), default=None)
    if latest and _content_text(latest.get("content")).strip() == text:
        return {"name": name, "prompt_id": prompt["id"], "version": latest["version"], "status": "unchanged"}
    nxt = (latest["version"] + 1) if latest else 1
    created = _request(f"{base}/api/prompts/{prompt['id']}/versions", "POST",
                       {"prompt_id": prompt["id"], "version": nxt, "content": {"type": "evidently:prompt_content:TextPromptContent", "text": text}})
    return {"name": name, "prompt_id": prompt["id"], "version": created.get("version", nxt), "status": "pushed"}


def init(cfg: dict | None = None) -> dict:
    cfg = cfg or config()
    project_id = _project_id(cfg)
    cfg["project_id"] = project_id
    out = {"url": cfg["url"], "project_id": project_id, "prompts": [push(n, cfg) for n in NAMES]}
    doc = yaml.safe_load(CONFIG.read_text()) if CONFIG.exists() else {}
    doc = doc or {}
    doc.update(url=cfg["url"], project_id=project_id, project_name=cfg["project_name"])
    CONFIG.write_text(yaml.safe_dump(doc, sort_keys=False))
    return out


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    cmd = argv[0] if argv else "pull"
    cfg = config()
    if cmd == "init":
        print(json.dumps(init(cfg), indent=2))  # noqa: T201
    elif cmd == "push":
        print(json.dumps([push(n, cfg) for n in (argv[1:] or NAMES)], indent=2))  # noqa: T201
    else:
        rows = [{"name": n, "source": r.source, "version": r.version, "chars": len(r.text)} for n in NAMES for r in [get(n, cfg)]]
        print(json.dumps({"url": cfg["url"], "project_id": cfg["project_id"] or None, "prompts": rows}, indent=2))  # noqa: T201
    return 0


if __name__ == "__main__":
    sys.exit(main())
