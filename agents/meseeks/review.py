"""Human in the loop for the Meseeks inbox.

Messages the guardrails held (other than hard rejects) wait in _data/meseeks_review.json. A
human confirms one into a category or acknowledges it as held. A confirmation is not a
bypass: it goes through guardrails.enforce at full confidence, against the questions posted
so far, exactly like the model's proposals did (HumanConfirm in specs/tla/Meseeks.tla).

  python -m meseeks.review login                       # OpenID Connect sign-in (device flow or PKCE)
  python -m meseeks.review list
  python -m meseeks.review confirm <id> <category>     # as the signed-in witness (ID token), or MESEEKS_WITNESS
  python -m meseeks.review ack <id> [note]

Only a witness agent may confirm or acknowledge (_data/meseeks_witnesses.yml): a known
person's address at an allowed domain, acting from the local or wide-area network, on a
witness platform (macOS, Rocky Linux, Kodachi Linux). Anyone else is refused.
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from . import witness as witness_mod
from .adk_agent import _advisory
from .guardrails import CATEGORIES, Inbound, enforce, to_post
from .run import DATA, LOG, load_data, load_firm_domains, order_posts

ROOT = Path(__file__).resolve().parents[2]
REVIEW = ROOT / "_data" / "meseeks_review.json"


def _paths() -> tuple[Path, Path]:
    return (Path(os.environ.get("MESEEKS_REVIEW", str(REVIEW))), Path(os.environ.get("MESEEKS_DATA", str(DATA))))


def _load_queue(path: Path) -> dict:
    return json.loads(path.read_text()) if path.exists() else {"inbox": "meseeks@legalluminary.com", "items": []}


def _inbound(item: dict) -> Inbound:
    received = datetime.strptime(item["received"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    body = item["body"] + ("\n" + "\n".join(x["url"] for x in item.get("links", [])) if item.get("links") else "")
    return Inbound(message_id=item["message_id"], sender=f"redacted@{item['sender_domain']}", subject=item["subject"],
                   body=body, received=received, attachments=[("", t) for t in item.get("attachments", [])],
                   in_reply_to=item.get("in_reply_to"))


def pending(queue: dict) -> list[dict]:
    return [i for i in queue["items"] if i.get("status") == "pending"]


def _witness(who, channel: str = "review") -> tuple[witness_mod.Identity, str | None]:
    """Resolve who is acting; a non-witness gets a refusal reason."""
    ident = who if isinstance(who, witness_mod.Identity) else witness_mod.local_identity(who if isinstance(who, str) else None)
    ident = witness_mod.Identity(witness_mod.bare_address(ident.address), ident.ip, ident.platform, ident.verified, ident.claims)
    ok, why = witness_mod.is_witness(ident, channel=channel)
    return ident, (None if ok else why)


def confirm(item_id: str, category: str, who="", channel: str = "review") -> dict:
    """Publish a held message as `category` if, and only if, a witness asks and the guardrails accept it at confidence 1.0."""
    ident, refusal = _witness(who, channel)
    if refusal:
        return {"id": item_id, "status": "refused", "reason": f"not a witness: {refusal}", "by": ident.address}
    who = ident.address
    review_path, data_path = _paths()
    queue, data = _load_queue(review_path), load_data(data_path)
    item = next((i for i in pending(queue) if i["id"] == item_id or i["message_id"] == item_id), None)
    if item is None:
        return {"id": item_id, "status": "not pending"}
    if category not in CATEGORIES:
        return {"id": item_id, "status": "refused", "reason": f"unknown category {category!r}"}
    firms = load_firm_domains()
    question_ids = {p["id"] for p in data["posts"] if p["category"] == "question"}
    msg = _inbound(item)
    # A confirmation is a proposal at full confidence: same advisory layer (a citizen's
    # question cannot be confirmed out of its anonymity), same gate as the model's proposals.
    category, conf, how = _advisory(msg, {"category": category, "confidence": 1.0, "reason": f"confirmed by {who}"})
    d = enforce(msg, category, conf, firms, question_ids)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if not d.publish:
        item.update(last_refusal={"category": category, "reason": d.reason, "utc": now, "by": who})  # stays pending
        outcome = {"id": item_id, "status": "refused", "reason": d.reason}
    else:
        post = to_post(msg, category, firms)
        if post["id"] in {p["id"] for p in data["posts"]}:
            outcome = {"id": item_id, "status": "duplicate"}
            item.update(status="duplicate", decided_utc=now, decided_by=who)
        else:
            data["posts"].append(post)
            data["posts"] = order_posts(data["posts"])
            data["generated_utc"] = now
            data_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
            item.update(status="confirmed", category=category, decided_utc=now, decided_by=who,
                        decided_auth={"verified": ident.verified, "sub": ident.claims[0] if ident.claims else None, "iss": ident.claims[1] if ident.claims else None})
            outcome = {"id": item_id, "status": "published", "category": category, "post_id": post["id"], "advisory": how, "verified": ident.verified}
    review_path.write_text(json.dumps(queue, indent=2, ensure_ascii=False) + "\n")
    LOG.mkdir(parents=True, exist_ok=True)
    with (LOG / f"{now[:10]}.jsonl").open("a") as fh:
        fh.write(json.dumps({"run": now, "agent": "human", "message_id": item["message_id"], **outcome}) + "\n")
    return outcome


def ack(item_id: str, note: str = "", who="", channel: str = "review") -> dict:
    """Acknowledge a held message (witnesses only): it stays held and leaves the queue."""
    ident, refusal = _witness(who, channel)
    if refusal:
        return {"id": item_id, "status": "refused", "reason": f"not a witness: {refusal}", "by": ident.address}
    who = ident.address
    review_path, _ = _paths()
    queue = _load_queue(review_path)
    item = next((i for i in pending(queue) if i["id"] == item_id or i["message_id"] == item_id), None)
    if item is None:
        return {"id": item_id, "status": "not pending"}
    item.update(status="acknowledged", note=note, decided_utc=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), decided_by=who)
    review_path.write_text(json.dumps(queue, indent=2, ensure_ascii=False) + "\n")
    return {"id": item_id, "status": "acknowledged"}


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    cmd = argv[0] if argv else "list"
    if cmd == "login":
        from . import oidc, witness

        tok = oidc.login(oidc.Provider.from_config(witness.load()))
        claims = oidc.verify(tok["id_token"], oidc.Provider.from_config(witness.load()))
        out = {"status": "signed in", "as": oidc.address_of(claims, oidc.Provider.from_config(witness.load())), "token_file": str(oidc.TOKEN_FILE)}
    elif cmd == "confirm" and len(argv) >= 3:
        out = confirm(argv[1], argv[2])
    elif cmd == "ack" and len(argv) >= 2:
        out = ack(argv[1], " ".join(argv[2:]))
    else:
        review_path, _ = _paths()
        items = pending(_load_queue(review_path))
        out = [{k: i[k] for k in ("id", "sender_domain", "subject", "proposed", "reason", "received")} for i in items]
    print(json.dumps(out, indent=2, ensure_ascii=False))  # noqa: T201
    return 0


if __name__ == "__main__":
    sys.exit(main())
