"""Private store for what the inbox receives: one folder per mail thread.

Layout (the same one witnesses use by hand under ~/ll/mail_attachments):

    <store>/thread_id_<N>/attachedtomessage<K>.<ext>   every distinct attachment, numbered per thread
    <store>/thread_id_<N>/link_id_<K>                  every distinct URL the thread carried, one per file
    <store>/thread_id_<N>/thread.json                  metadata: messages, attachments (sha256, size,
                                                       original filename and type), links, and the
                                                       posts or intake briefs made from the thread
    <store>/index.json                                 thread key (root Message-ID) -> thread_id_<N>

Messages join a thread through In-Reply-To / References. An attachment identical to one already
stored (same sha256) is recorded again but not written twice. Nothing is extracted or opened:
archives stay archives. Everything is private (dirs 0700, files 0600) and lives outside the
repository; MESEEKS_MAIL_STORE sets the location (default ~/.local/share/meseeks/mail_attachments).
Only what the guardrails publish reaches the site.
"""
from __future__ import annotations

import hashlib
import json
import mimetypes
import os
import re
from datetime import datetime, timezone
from email import policy
from email.message import EmailMessage
from email.parser import BytesParser
from pathlib import Path

DEFAULT = Path.home() / ".local" / "share" / "meseeks" / "mail_attachments"
MAX_BYTES = int(os.environ.get("MESEEKS_STORE_MAX_BYTES", str(50 * 1024 * 1024)))
_URL_RE = re.compile(r"https?://[^\s<>\"')\]]+", re.I)
_MID_RE = re.compile(r"<[^<>\s]+>")


def base_dir() -> Path:
    return Path(os.environ.get("MESEEKS_MAIL_STORE", str(DEFAULT))).expanduser()


def _private_dir(p: Path) -> Path:
    p.mkdir(parents=True, exist_ok=True)
    os.chmod(p, 0o700)
    return p


def _write(p: Path, data: bytes) -> None:
    fd = os.open(p, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "wb") as fh:
        fh.write(data)


def _load(p: Path, default):
    try:
        return json.loads(p.read_text())
    except (OSError, json.JSONDecodeError):
        return default


def thread_key(msg: EmailMessage) -> str:
    """Root Message-ID of the conversation: first of References, else In-Reply-To, else itself."""
    refs = _MID_RE.findall(str(msg.get("References", "")))
    if refs:
        return refs[0]
    irt = _MID_RE.findall(str(msg.get("In-Reply-To", "")))
    if irt:
        return irt[0]
    return (msg.get("Message-ID") or "").strip() or f"<no-id-{hashlib.sha256(msg.as_bytes()).hexdigest()[:16]}>"


def _ext(part: EmailMessage) -> str:
    name = part.get_filename() or ""
    if "." in name:
        return name.rsplit(".", 1)[-1].lower()[:8]
    return (mimetypes.guess_extension(part.get_content_type()) or ".bin").lstrip(".")


def _links(msg: EmailMessage) -> list[str]:
    body = msg.get_body(preferencelist=("plain", "html"))
    text = body.get_content() if body is not None else ""
    seen, out = set(), []
    for u in _URL_RE.findall(text):
        u = u.rstrip(".,;")
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


def store(raw: bytes, base: Path | None = None) -> dict:
    """Store one raw message; returns {thread, dir, attachments, links} for the audit."""
    base = _private_dir(base or base_dir())
    msg = BytesParser(policy=policy.default).parsebytes(raw)
    index_path = base / "index.json"
    index = _load(index_path, {})
    key = thread_key(msg)
    if key not in index:
        used = {int(m.group(1)) for d in base.glob("thread_id_*") if (m := re.match(r"thread_id_(\d+)$", d.name))}
        used |= {int(v.rsplit("_", 1)[-1]) for v in index.values()}
        index[key] = f"thread_id_{min(set(range(len(used) + 1)) - used)}"
    tdir = _private_dir(base / index[key])
    meta_path = tdir / "thread.json"
    meta = _load(meta_path, {"thread": index[key], "root": key, "messages": [], "outputs": []})
    mid = (msg.get("Message-ID") or "").strip()
    if any(m["message_id"] == mid for m in meta["messages"]):
        return {"thread": index[key], "dir": str(tdir), "attachments": [], "links": [], "duplicate_message": True}

    by_hash = {a["sha256"]: a["file"] for m in meta["messages"] for a in m["attachments"] if a.get("file")}
    n_att = sum(1 for p in tdir.glob("attachedtomessage*"))
    entry = {"message_id": mid, "date": str(msg.get("Date", "")),
             "from_domain": str(msg.get("From", "")).rsplit("@", 1)[-1].strip(" >").lower(),
             "subject": str(msg.get("Subject", ""))[:200], "stored_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
             "attachments": [], "links": []}
    for part in msg.iter_attachments():
        data = part.get_payload(decode=True) or b""
        rec = {"filename": part.get_filename() or "", "content_type": part.get_content_type(), "size": len(data),
               "sha256": hashlib.sha256(data).hexdigest()}
        if len(data) > MAX_BYTES:
            rec["file"], rec["skipped"] = None, f"larger than {MAX_BYTES} bytes"
        elif rec["sha256"] in by_hash:
            rec["file"], rec["duplicate_of"] = by_hash[rec["sha256"]], by_hash[rec["sha256"]]
        else:
            n_att += 1
            rec["file"] = f"attachedtomessage{n_att}.{_ext(part)}"
            _write(tdir / rec["file"], data)
            by_hash[rec["sha256"]] = rec["file"]
        entry["attachments"].append(rec)

    known = {(tdir / p.name).read_text().strip() for p in tdir.glob("link_id_*")}
    n_link = len(list(tdir.glob("link_id_*")))
    for url in _links(msg):
        if url in known:
            entry["links"].append({"url": url, "file": None})
            continue
        f = f"link_id_{n_link}"
        _write(tdir / f, url.encode())
        known.add(url)
        n_link += 1
        entry["links"].append({"url": url, "file": f})

    meta["messages"].append(entry)
    _write(meta_path, json.dumps(meta, indent=2).encode())
    _write(index_path, json.dumps(index, indent=2).encode())
    return {"thread": index[key], "dir": str(tdir), "attachments": [a["file"] for a in entry["attachments"] if a.get("file")],
            "links": [link["url"] for link in entry["links"]]}


def record_output(thread: str, output: dict, base: Path | None = None) -> None:
    """Note a post or intake brief made from a thread, e.g. {"post": "8c3984a620", "category": "opportunity"}."""
    tdir = (base or base_dir()) / thread
    meta = _load(tdir / "thread.json", None)
    if meta is None:
        return
    meta.setdefault("outputs", []).append({**output, "utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")})
    _write(tdir / "thread.json", json.dumps(meta, indent=2).encode())
