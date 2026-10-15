"""Inputs for the digest: the notices inbox on the LAN mail host, posted Meseeks notices,
and the enabled local RSS feeds."""
from __future__ import annotations

import json
import os
import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
LOOKBACK_HOURS = int(os.environ.get("DIGEST_LOOKBACK_HOURS", "26"))
FETCH_TIMEOUT = float(os.environ.get("DIGEST_FETCH_TIMEOUT", "15"))
UA = "LegalLuminaryDigest/1.0 (+https://legalluminary.com/about/)"


def _since(now: datetime) -> datetime:
    return now - timedelta(hours=LOOKBACK_HOURS)


def inbox_items(now: datetime, log: list[dict]) -> list[dict]:
    """Unseen mail on the notices inbox (DIGEST_IMAP_* or MESEEKS_IMAP_*; host defaults to 192.168.0.15)."""
    env = {k: os.environ.get(f"DIGEST_IMAP_{k}") or os.environ.get(f"MESEEKS_IMAP_{k}") for k in ("HOST", "USER", "PASSWORD", "FOLDER")}
    env["HOST"] = env["HOST"] or "192.168.0.15"
    if not (env["USER"] and env["PASSWORD"]):
        log.append({"source": "inbox", "status": "skipped: no IMAP credentials"})
        return []
    import sys
    sys.path.insert(0, str(ROOT / "agents"))
    from meseeks.guardrails import normalize_body, redact
    from meseeks.mailbox import Imap

    for k, v in env.items():
        if v:
            os.environ[f"MESEEKS_IMAP_{k}"] = v
    try:
        imap = Imap()
        msgs = imap.unseen(limit=100)
        imap.close()
    except Exception as e:
        log.append({"source": "inbox", "status": f"error {type(e).__name__}: {e}"[:200]})
        return []
    items = [{"kind": "inbox", "title": m.subject, "date": m.received.isoformat(), "from": m.sender.split("@")[-1].strip(">"),
              "text": redact(normalize_body(m.body))[:2500]} for m in msgs if m.received >= _since(now)]
    log.append({"source": "inbox", "status": f"{len(items)} of {len(msgs)} unseen in window"})
    return items


def meseeks_items(now: datetime, log: list[dict]) -> list[dict]:
    p = ROOT / "_data" / "meseeks.json"
    if not p.exists():
        return []
    posts = json.loads(p.read_text()).get("posts", [])
    out = []
    for x in posts:
        if x["category"] in ("notice", "standing_order", "opportunity"):
            d = datetime.strptime(x["received"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
            if d >= _since(now):
                out.append({"kind": x["category"], "title": x["title"], "date": x["received"],
                            "from": x.get("source_label", ""), "text": x["body"][:2500],
                            "url": f"https://www.legalluminary.com/meseeks/#post-{x['id']}"})
    log.append({"source": "meseeks.json", "status": f"{len(out)} posts"})
    return out


def _parse_feed(xml_bytes: bytes) -> list[dict]:
    root = ET.fromstring(xml_bytes)
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    items = []
    for it in root.iter("item"):
        items.append({"title": (it.findtext("title") or "").strip(), "url": (it.findtext("link") or "").strip(),
                      "date": (it.findtext("pubDate") or "").strip(),
                      "text": re.sub(r"<[^>]+>", "", it.findtext("description") or "").strip()[:800]})
    for it in root.iter("{http://www.w3.org/2005/Atom}entry"):
        link = it.find("atom:link", ns)
        items.append({"title": (it.findtext("atom:title", default="", namespaces=ns) or "").strip(),
                      "url": link.get("href", "") if link is not None else "",
                      "date": (it.findtext("atom:updated", default="", namespaces=ns) or "").strip(),
                      "text": re.sub(r"<[^>]+>", "", it.findtext("atom:summary", default="", namespaces=ns) or "").strip()[:800]})
    return items


def rss_items(now: datetime, log: list[dict]) -> list[dict]:
    cfg = yaml.safe_load((ROOT / "_data" / "rss-feeds.yml").read_text()) or {}
    out = []
    for f in cfg.get("feeds", []):
        if not f.get("enabled", True) or f.get("category") not in ("local", "county", "state", None):
            continue
        try:
            req = urllib.request.Request(f["url"], headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=FETCH_TIMEOUT) as r:
                items = _parse_feed(r.read())[: int(f.get("max_items", 10))]
            for it in items:
                it.update(kind="rss", **{"from": f["name"]})
            out.extend(items)
            log.append({"source": f["name"], "status": f"{len(items)} items"})
        except Exception as e:
            log.append({"source": f["name"], "status": f"error {type(e).__name__}"[:120]})
    return out


def collect(now: datetime, log: list[dict]) -> list[dict]:
    return inbox_items(now, log) + meseeks_items(now, log) + rss_items(now, log)
