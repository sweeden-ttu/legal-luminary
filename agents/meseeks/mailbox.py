"""Mail sources: IMAP (production) and a directory of .eml files (dry run / tests)."""
from __future__ import annotations

import email
import imaplib
import os
import re
import ssl
from datetime import datetime, timezone
from email import policy
from email.message import EmailMessage
from email.utils import parsedate_to_datetime
from pathlib import Path

from .guardrails import Inbound

_QID_RE = re.compile(r"\[Q-([0-9a-f]{10})\]", re.I)
_IP_RE = re.compile(r"\[(?:IPv6:)?([0-9a-fA-F.:]+)\]|\((?:[^()]*\s)?(\d{1,3}(?:\.\d{1,3}){3})\)")


def _origin_ip(msg: EmailMessage) -> str | None:
    """Client address of the earliest hop: the last Received header the MTA stack added first."""
    received = msg.get_all("Received") or []
    for header in reversed(received):
        head = str(header).split(" by ", 1)[0]
        m = _IP_RE.search(head)
        if m:
            return m.group(1) or m.group(2)
    return None


def _body_text(msg: EmailMessage) -> str:
    part = msg.get_body(preferencelist=("plain", "html"))
    if part is None:
        return ""
    text = part.get_content()
    if part.get_content_type() == "text/html":
        text = re.sub(r"<(script|style).*?</\1>", "", text, flags=re.S | re.I)
        text = re.sub(r"<br\s*/?>|</p>|</div>|</li>", "\n", text, flags=re.I)
        text = re.sub(r"<[^>]+>", "", text)
        text = email.utils.unquote(text)
    return text


def _attachments(msg: EmailMessage) -> list[tuple[str, str]]:
    return [(p.get_filename() or "", p.get_content_type()) for p in msg.iter_attachments()]


def _in_reply_to(msg: EmailMessage) -> str | None:
    for field in (msg.get("Subject", ""), msg.get("In-Reply-To", ""), msg.get("References", "")):
        m = _QID_RE.search(field)
        if m:
            return m.group(1).lower()
    return None


def parse_eml(raw: bytes) -> Inbound:
    msg = email.message_from_bytes(raw, policy=policy.default)
    try:
        received = parsedate_to_datetime(msg.get("Date"))
        if received.tzinfo is None:
            received = received.replace(tzinfo=timezone.utc)
    except Exception:
        received = datetime.now(timezone.utc)
    return Inbound(
        message_id=(msg.get("Message-ID") or f"<no-id-{abs(hash(raw))}>").strip(),
        sender=msg.get("From", ""),
        subject=msg.get("Subject", "").strip(),
        body=_body_text(msg),
        received=received,
        attachments=_attachments(msg),
        in_reply_to=_in_reply_to(msg),
        origin_ip=_origin_ip(msg),
    )


def from_directory(path: str | Path) -> list[Inbound]:
    return [parse_eml(p.read_bytes()) for p in sorted(Path(path).glob("*.eml"))]


class Imap:
    """Minimal IMAP-over-TLS reader. Env: MESEEKS_IMAP_HOST, MESEEKS_IMAP_USER, MESEEKS_IMAP_PASSWORD,
    MESEEKS_IMAP_FOLDER (default INBOX), MESEEKS_IMAP_PORT (default 993), MESEEKS_IMAP_CA (path to the
    CA bundle that signed the server certificate, for a private CA). Remote clients must use TLS;
    certificates are always verified. Processed messages get the \\Seen flag."""

    def __init__(self) -> None:
        self.host = os.environ["MESEEKS_IMAP_HOST"]
        self.user = os.environ["MESEEKS_IMAP_USER"]
        self.password = os.environ["MESEEKS_IMAP_PASSWORD"]
        self.folder = os.environ.get("MESEEKS_IMAP_FOLDER", "INBOX")
        port = int(os.environ.get("MESEEKS_IMAP_PORT", "993"))
        ctx = ssl.create_default_context(cafile=os.environ.get("MESEEKS_IMAP_CA") or None)
        self.conn = imaplib.IMAP4_SSL(self.host, port, ssl_context=ctx)
        self.conn.login(self.user, self.password)
        self.conn.select(self.folder)
        self._uids: dict[str, bytes] = {}

    def unseen(self, limit: int = 200) -> list[Inbound]:
        _, data = self.conn.uid("search", None, "UNSEEN")
        out = []
        for uid in data[0].split()[:limit]:
            _, raw = self.conn.uid("fetch", uid, "(BODY.PEEK[])")
            if not raw or raw[0] is None:
                continue
            msg = parse_eml(raw[0][1])
            if os.environ.get("MESEEKS_MAIL_STORE"):   # keep every input privately, thread by thread
                from .store import store

                try:
                    store(raw[0][1])
                except OSError:
                    pass
            self._uids[msg.message_id] = uid
            out.append(msg)
        return out

    def mark_processed(self, message_id: str) -> None:
        uid = self._uids.get(message_id)
        if uid:
            self.conn.uid("store", uid, "+FLAGS", "(\\Seen)")

    def close(self) -> None:
        try:
            self.conn.logout()
        except Exception:
            pass
