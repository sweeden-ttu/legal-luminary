"""Deterministic guardrails. Everything here runs before and after any model call;
the model can only narrow what gets published, never widen it."""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from email.utils import parseaddr

CATEGORIES = ("opportunity", "notice", "standing_order", "question", "answer")
MAX_BODY_CHARS = 4000
MIN_BODY_CHARS = 40
ALLOWED_ATTACHMENT_TYPES = {"application/pdf"}

_EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
_PHONE_RE = re.compile(r"(?:\+?1[\s.-]?)?\(?\b\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b")
_SSN_RE = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
_CASE_RE = re.compile(r"\b(?:cause|case|docket)\s*(?:no\.?|number|#)?\s*[:#]?\s*[\w-]{4,}\b", re.I)
_STREET_RE = re.compile(
    r"\b\d{1,6}\s+(?:[A-Z][a-z]+\s){0,3}(?:St|Street|Ave|Avenue|Rd|Road|Dr|Drive|Ln|Lane|Blvd|Ct|Court|Way|Trail|Trl|Loop|Pkwy)\b\.?",
    re.I,
)
_URL_RE = re.compile(r"https?://[^\s<>\"')\]]+", re.I)
_SIG_CUT_RE = re.compile(r"^(?:--\s*$|__+$|sent from my|on .+ wrote:$|from: )", re.I | re.M)

_ABUSE_TERMS = (
    "kill you", "i will hurt", "bomb", "shoot up", "slit", "rape you",
)
_SPAM_TERMS = (
    "unsubscribe", "limited time offer", "click here to claim", "crypto", "bitcoin",
    "seo services", "guest post", "backlink", "make money", "viagra", "casino",
)

# Jurisdiction and topic scope. A post must originate in the context of Killeen, Texas or
# Bell County, or be a statutory / political / judicial matter of Texas, Bell County, or the
# municipalities around Killeen: city council, the mayor's office, justices of the peace, the
# Texas Attorney General, and compliance with or decisions by elected judges on the bench.
# Answers inherit the scope of the posted question they reply to (the thread).
SCOPE_PLACES = (
    "killeen", "bell county", "harker heights", "copperas cove", "nolanville", "belton", "temple, tx",
    "temple texas", "fort cavazos", "fort hood", "salado", "troy, tx", "holland, tx", "rogers, tx", "bartlett",
    "little river-academy", "morgan's point", "central texas", "centex",
)
SCOPE_BODIES = (
    "city council", "council member", "councilmember", "councilman", "councilwoman", "mayor",
    "justice of the peace", "justices of the peace", "jp court", "justice court", "county judge",
    "commissioners court", "district court", "county court at law", "municipal court", "attorney general",
    "texas supreme court", "court of criminal appeals", "court of appeals", "western district of texas",
    "district attorney", "county attorney", "city attorney", "county clerk", "district clerk", "judge",
    "election", "ballot", "precinct", "ordinance", "standing order", "local rule",
)
SCOPE_STATUTES = (
    "texas property code", "texas penal code", "texas government code", "local government code",
    "texas family code", "texas election code", "code of criminal procedure", "civil practice and remedies",
    "texas occupations code", "texas transportation code", "health and safety code", "open meetings act",
    "public information act", "tex. ", "texas law", "state of texas", "texas statute", "texas statutes",
)
SCOPE_DOMAINS = (
    "killeentexas.gov", "bellcountytx.com", "bellcounty.texas.gov", "co.bell.tx.us", "texasattorneygeneral.gov",
    "txcourts.gov", "harkerheights.gov", "copperascovetx.gov", "templetx.gov", "beltontexas.gov", "nolanvilletx.gov",
    "capitol.texas.gov", "sos.texas.gov", ".tx.us",
)


def scope_of(msg: Inbound) -> str | None:
    """Why a message is within the Killeen / Bell County / Texas statutory scope, or None."""
    text = (msg.subject + "\n" + msg.body).lower()
    dom = sender_domain(msg.sender)
    for d in SCOPE_DOMAINS:
        if dom == d.lstrip(".") or dom.endswith(d if d.startswith(".") else "." + d):
            return f"domain:{dom}"
    for t in SCOPE_PLACES:
        if t in text:
            return f"place:{t}"
    texas = "texas" in text or " tx " in text or re.search(r"\btx\b", text) is not None
    if texas:
        for t in SCOPE_BODIES + SCOPE_STATUTES:
            if t in text:
                return f"texas:{t.strip()}"
    return None


def in_scope(msg: Inbound) -> bool:
    return scope_of(msg) is not None


_KEYWORDS = {
    "standing_order": ("standing order", "general order", "administrative order", "local rule", "amended order", "it is ordered"),
    "notice": ("public notice", "notice of", "hearing", "agenda", "ordinance", "city council", "commissioners court", "legal notice", "town hall", "meeting", "comment period"),
    "opportunity": ("hiring", "job", "position", "clerkship", "internship", "pro bono", "volunteer", "rfp", "request for proposal", "paralegal", "associate attorney", "apply", "opening"),
    "question": ("?", "can i", "do i", "what should", "how do", "is it legal", "my landlord", "my employer", "i was arrested", "custody", "divorce", "evict", "ticket", "warrant", "need a lawyer", "need an attorney"),
    "answer": ("re:", "in response", "regarding your question", "generally speaking", "you should consult", "this is not legal advice"),
}


@dataclass
class Inbound:
    message_id: str
    sender: str
    subject: str
    body: str
    received: datetime
    attachments: list[tuple[str, str]] = field(default_factory=list)  # (filename, content_type)
    in_reply_to: str | None = None


@dataclass
class Decision:
    publish: bool
    category: str | None
    reason: str
    confidence: float = 0.0


def sender_domain(sender: str) -> str:
    _, addr = parseaddr(sender)
    return addr.rsplit("@", 1)[-1].lower().strip() if "@" in addr else ""


def is_firm_domain(sender: str, firm_domains: set[str]) -> bool:
    d = sender_domain(sender)
    return bool(d) and (d in firm_domains or any(d.endswith("." + f) for f in firm_domains))


_CLOSING_RE = re.compile(
    r"^(?:thanks|thank you|regards|best|best regards|sincerely|cheers|respectfully|v/r|thx)[,.!]?\s*$", re.I)


def strip_signature(body: str) -> str:
    m = _SIG_CUT_RE.search(body)
    if m:
        body = body[: m.start()].rstrip()
    lines = body.rstrip().split("\n")
    for i in range(len(lines) - 1, max(len(lines) - 5, -1), -1):
        if _CLOSING_RE.match(lines[i].strip()):
            return "\n".join(lines[:i]).rstrip()
    return body


def redact_sender_name(body: str, sender: str) -> str:
    name, _ = parseaddr(sender)
    for token in re.findall(r"[A-Za-z][A-Za-z'-]{2,}", name):
        body = re.sub(r"\b" + re.escape(token) + r"\b", "[name redacted]", body)
    return body


def extract_links(body: str) -> list[dict]:
    seen, out = set(), []
    for u in _URL_RE.findall(body):
        u = u.rstrip(".,;")
        if u not in seen:
            seen.add(u)
            out.append({"url": u, "label": u.split("//", 1)[-1][:80]})
    return out[:8]


def redact(body: str) -> str:
    body = _SSN_RE.sub("[redacted]", body)
    body = _EMAIL_RE.sub("[email redacted]", body)
    body = _PHONE_RE.sub("[phone redacted]", body)
    body = _CASE_RE.sub("[case number redacted]", body)
    body = _STREET_RE.sub("[address redacted]", body)
    return body


def normalize_body(body: str) -> str:
    body = body.replace("\r\n", "\n")
    body = strip_signature(body)
    body = re.sub(r"\n{3,}", "\n\n", body).strip()
    return body[:MAX_BODY_CHARS]


def content_hash(subject: str, body: str) -> str:
    key = re.sub(r"\W+", " ", (subject + " " + body).lower()).strip()
    return hashlib.sha256(key.encode()).hexdigest()[:16]


def post_id(msg: Inbound) -> str:
    return hashlib.sha256(msg.message_id.encode()).hexdigest()[:10]


def hard_reject(msg: Inbound) -> str | None:
    text = (msg.subject + "\n" + msg.body).lower()
    if any(t in text for t in _ABUSE_TERMS):
        return "abusive content"
    if sum(t in text for t in _SPAM_TERMS) >= 2:
        return "spam"
    for _, ctype in msg.attachments:
        if ctype not in ALLOWED_ATTACHMENT_TYPES:
            return f"disallowed attachment type {ctype}"
    if len(normalize_body(msg.body)) < MIN_BODY_CHARS:
        return "body too short"
    return None


def rule_classify(msg: Inbound) -> tuple[str | None, float]:
    text = (msg.subject + "\n" + msg.body).lower()
    scores = {c: 0 for c in CATEGORIES}
    for cat, terms in _KEYWORDS.items():
        for t in terms:
            if t in text:
                scores[cat] += 2 if t in msg.subject.lower() else 1
    if msg.in_reply_to:
        scores["answer"] += 3
    best = max(scores, key=scores.get)
    total = sum(scores.values()) or 1
    conf = scores[best] / total
    if scores[best] == 0:
        return None, 0.0
    return best, round(conf, 2)


def enforce(msg: Inbound, category: str | None, confidence: float, firm_domains: set[str],
            known_question_ids: set[str], min_confidence: float = 0.5) -> Decision:
    """Final gate. Model output never bypasses this."""
    reason = hard_reject(msg)
    if reason:
        return Decision(False, None, reason)
    if category not in CATEGORIES:
        return Decision(False, None, "unclassified")
    if confidence < min_confidence:
        return Decision(False, category, f"low confidence {confidence}")
    if category == "answer":
        if not is_firm_domain(msg.sender, firm_domains):
            return Decision(False, "answer", "answer not from participating firm domain")
        if not msg.in_reply_to or msg.in_reply_to not in known_question_ids:
            return Decision(False, "answer", "answer does not reference a posted question")
    if category == "standing_order" and not extract_links(msg.body) and not msg.attachments:
        return Decision(False, "standing_order", "standing order without source link or PDF")
    if category != "answer" and not in_scope(msg):
        return Decision(False, category, "out of scope: not a Killeen / Bell County / Texas statutory matter")
    return Decision(True, category, "ok", confidence)


def to_post(msg: Inbound, category: str, firm_domains: set[str]) -> dict:
    body = redact(normalize_body(msg.body))
    subject = redact(msg.subject.strip()) or category.replace("_", " ").title()
    if category == "question":
        body = redact_sender_name(body, msg.sender)
        subject = redact_sender_name(subject, msg.sender)
    if category == "answer":
        source_label = f"Participating firm ({sender_domain(msg.sender)})"
    elif category == "question":
        source_label = "Anonymous"
    else:
        source_label = sender_domain(msg.sender) or "forwarded"
    return {
        "id": post_id(msg),
        "category": category,
        "title": subject[:140],
        "body": body,
        "received": msg.received.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source_label": source_label,
        "links": extract_links(msg.body),
        "in_reply_to": msg.in_reply_to if category == "answer" else None,
        "hash": content_hash(subject, body),
    }
