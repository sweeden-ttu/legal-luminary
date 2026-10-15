"""Callbacks and runner behind agents/meseeks/agent.yaml (orchestrator) and round.yaml (sub-agent).

The model never touches the mailbox or the data file. It sees a redacted batch injected into its
instruction, proposes {message_id, category, confidence, reason} per message, and
guardrails.enforce decides what is published. Anything the model skips, mislabels, or cannot
place falls back to the keyword rules, so a weak local model or a failed coder still yields a
safe, auditable run.

Clock. A round is one chain of unattended sub-agent calls (local server, then each coder, then
the API), each with its own budget of at most MESEEKS_MAX_CALL_SECONDS (60 s), inside a window
that is precisely the sum of those budgets (backends.Window). After a round, check_round merges
the proposals and either stops the loop or issues one more question + reason + instruction for
the message ids still unanswered. The loop ends when nothing is missing, no sub-agent answered,
MAX_ROUNDS is reached, or MESEEKS_IDLE_SECONDS (60 s) have passed without a new proposal;
apply_guardrails then decides with whatever was proposed.

  python -m meseeks.run --adk --dry-run --eml ../tests/meseeks/fixtures
  adk run agents/meseeks            # MESEEKS_EML_DIR=... or MESEEKS_IMAP_* in the env
"""
from __future__ import annotations

import json
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from google.genai import types

from . import backends, mailbox
from . import prompts as prompt_registry
from .guardrails import (
    CATEGORIES,
    Inbound,
    enforce,
    extract_links,
    hard_reject,
    in_scope,
    is_firm_domain,
    normalize_body,
    redact,
    rule_classify,
    scope_of,
    sender_domain,
    to_post,
)
from .run import DATA, LOG, expire, load_data, load_firm_domains

ROOT = Path(__file__).resolve().parents[2]

MAX_BATCH = int(os.environ.get("MESEEKS_MAX_BATCH", "25"))
EXCERPT_CHARS = int(os.environ.get("MESEEKS_EXCERPT_CHARS", "1500"))
MAX_ROUNDS = int(os.environ.get("MESEEKS_MAX_ROUNDS", "3"))
IDLE_SECONDS = float(os.environ.get("MESEEKS_IDLE_SECONDS", "60"))
#: Held messages that were not hard-rejected wait here for a human (meseeks.review).
REVIEW = ROOT / "_data" / "meseeks_review.json"

#: Raw messages per invocation; state only ever holds the redacted batch.
_RUNS: dict[str, dict[str, Any]] = {}


def _dry_run() -> bool:
    return os.environ.get("MESEEKS_DRY_RUN", "").lower() in ("1", "true", "yes")


def _source() -> tuple[list[Inbound], mailbox.Imap | None]:
    eml = os.environ.get("MESEEKS_EML_DIR")
    if eml:
        return mailbox.from_directory(eml), None
    if os.environ.get("MESEEKS_IMAP_HOST"):
        imap = mailbox.Imap()
        return imap.unseen(limit=MAX_BATCH), imap
    return [], None


def render_batch(messages: list[Inbound], firm_domains: set[str]) -> list[dict[str, Any]]:
    """Redacted, model-facing view of the inbox. Nothing here identifies a sender."""
    out = []
    for m in messages[:MAX_BATCH]:
        rule_cat, rule_conf = rule_classify(m)
        out.append({
            "message_id": m.message_id,
            "sender_domain": sender_domain(m.sender) or "unknown",
            "from_participating_firm": is_firm_domain(m.sender, firm_domains),
            "replies_to_question": m.in_reply_to,
            "subject": redact(m.subject)[:200],
            "excerpt": redact(normalize_body(m.body))[:EXCERPT_CHARS],
            "has_source_link": bool(extract_links(m.body)),
            "attachments": [ctype for _, ctype in m.attachments],
            "hard_reject": hard_reject(m),
            "scope": scope_of(m),
            "rule_hint": {"category": rule_cat, "confidence": rule_conf},
        })
    return out


def load_inbox(callback_context) -> types.Content | None:
    """Orchestrator before_agent_callback: start the loop clock, read mail, put the redacted batch in state."""
    now = datetime.now(timezone.utc)
    started = time.monotonic()
    messages, imap = _source()
    data = load_data(Path(os.environ.get("MESEEKS_DATA", str(DATA))))
    firm_domains = load_firm_domains()
    open_questions = [{"id": p["id"], "title": p["title"]} for p in data["posts"] if p["category"] == "question"]
    # Before any model sees anything: hard rejects (spam, abuse, bad attachments, short
    # bodies) are held outright, and the thread each sub-agent loop runs in must originate
    # in the Killeen / Bell County / Texas statutory context. Out-of-scope mail is held here
    # and never reaches a model; a reply to a question ([Q-id]) inherits its thread's scope
    # and is judged by the gate against the questions actually posted.
    in_thread, pre_held = [], []
    for m in messages[:MAX_BATCH]:
        reason = hard_reject(m)
        if reason:
            pre_held.append((m, reason, "hard-reject guardrail (never sent to a model)"))
        elif in_scope(m) or m.in_reply_to:
            in_thread.append(m)
        else:
            pre_held.append((m, "out of scope: not a Killeen / Bell County / Texas statutory matter",
                             "scope guardrail (never sent to a model)"))
    batch = render_batch(in_thread, firm_domains)

    _RUNS[callback_context.invocation_id] = {
        "messages": {m.message_id: m for m in in_thread},
        "pre_held": pre_held,
        "imap": imap,
        "data": data,
        "firm_domains": firm_domains,
        "now": now,
        "started": started,
        "last_progress": started,
    }
    instruction = prompt_registry.get("meseeks.instruction")
    st = callback_context.state
    st["meseeks_instruction"] = instruction.text
    st["meseeks_instruction_source"] = instruction.source
    st["meseeks_batch"] = json.dumps(batch, indent=1, ensure_ascii=False)
    st["meseeks_firm_domains"] = ", ".join(sorted(firm_domains)) or "(none yet)"
    st["meseeks_open_questions"] = json.dumps(open_questions, ensure_ascii=False)
    st["meseeks_batch_size"] = len(batch)
    st["meseeks_round"] = 0
    st["meseeks_merged"] = {}
    st["meseeks_rounds"] = []
    st["meseeks_followup"] = ""

    if not batch:
        if pre_held:
            return None   # nothing for a model, but apply_guardrails still records the holds
        if imap:
            imap.close()
        st["meseeks_result"] = {"messages": 0, "published": 0, "held": 0, "expired": 0, "audit": [], "backend": "skipped"}
        return types.Content(role="model", parts=[types.Part(text="No new mail for Meseeks.")])
    return None


def _parse_classifications(text: str) -> dict[str, dict[str, Any]]:
    """Pull {"classifications": [...]} out of whatever the model (or coder) printed."""
    text = re.sub(r"```(?:json)?", "", text or "")
    best: dict[str, dict[str, Any]] = {}
    for m in re.finditer(r"\{", text):
        try:
            obj, _ = json.JSONDecoder().raw_decode(text[m.start():])
        except json.JSONDecodeError:
            continue
        items = obj.get("classifications") if isinstance(obj, dict) else None
        if isinstance(items, list):
            for it in items:
                if isinstance(it, dict) and it.get("message_id"):
                    best[str(it["message_id"])] = it
            return best
    return best


def check_round(callback_context) -> types.Content | None:
    """Round after_agent_callback: merge proposals; stop the loop or ask again for what is missing.

    Stops (escalates) when every message has a proposal, when MAX_ROUNDS is reached, or when the
    window has closed. Otherwise writes the next question + reason + instruction into state for
    the following round. Never waits: the sub-agent call for this round has already returned.
    """
    st = callback_context.state
    run = _RUNS.get(callback_context.invocation_id)
    ids = list(run["messages"]) if run else []
    rnd = int(st.get("meseeks_round") or 0) + 1
    merged = dict(st.get("meseeks_merged") or {})
    got = _parse_classifications(str(st.get("meseeks_proposals") or ""))
    new = {k: v for k, v in got.items() if k in ids and k not in merged}
    merged.update(new)
    missing = [i for i in ids if i not in merged]
    if not ids:
        st["meseeks_round"] = rnd
        st["meseeks_rounds"] = [*list(st.get("meseeks_rounds") or []), {"round": rnd, "stop": "nothing in scope"}]
        callback_context.actions.escalate = True
        return None
    window = backends.WINDOW
    t = time.monotonic()
    if run and new:
        run["last_progress"] = t
    idle = t - run["last_progress"] if run else 0.0
    stop_reason = None
    if not missing:
        stop_reason = "complete"
    elif st.get("meseeks_backend", "none") == "none":
        stop_reason = "no sub-agent answered"
    elif not new and idle >= IDLE_SECONDS:
        stop_reason = f"idle: {IDLE_SECONDS:g}s without a new proposal"
    elif rnd >= MAX_ROUNDS:
        stop_reason = f"max rounds ({MAX_ROUNDS})"

    st["meseeks_round"] = rnd
    st["meseeks_merged"] = merged
    st["meseeks_rounds"] = [*list(st.get("meseeks_rounds") or []), {
        "round": rnd, "backend": st.get("meseeks_backend", "none"), "proposed": len(got), "new": len(new),
        "missing": len(missing), "window_s": window.seconds, "round_s": round(window.elapsed(), 2),
        "idle_s": round(idle, 2), "stop": stop_reason,
    }]
    if stop_reason:
        st["meseeks_followup"] = ""
        callback_context.actions.escalate = True
        return None
    st["meseeks_followup"] = (
        f"FOLLOW-UP, ROUND {rnd + 1} OF {MAX_ROUNDS}\n"
        f"Question: which category applies to each of these {len(missing)} message ids: {json.dumps(missing)}?\n"
        f"Reason: no classification for them was received in round {rnd}.\n"
        "Instruction: reply with one JSON object containing classifications for exactly those ids and no others."
    )
    return None


def _advisory(msg: Inbound, proposal: dict[str, Any] | None) -> tuple[str | None, float, str]:
    """Model output is advisory: validated, clamped, and capped when it disagrees with the rules."""
    rule_cat, rule_conf = rule_classify(msg)
    if not proposal:
        return rule_cat, rule_conf, "rules (no model proposal)"
    cat = proposal.get("category")
    if cat in (None, "null", "none", ""):
        return None, 0.0, "model: " + str(proposal.get("reason", "unplaceable"))[:120]
    if cat not in CATEGORIES:
        return rule_cat, rule_conf, f"rules (model gave unknown category {cat!r})"
    try:
        conf = max(0.0, min(1.0, float(proposal.get("confidence", 0))))
    except (TypeError, ValueError):
        return rule_cat, rule_conf, f"rules (model gave unusable confidence {proposal.get('confidence')!r})"
    if rule_cat == "question" and cat != "question":
        # Privacy dominates: a message the rules read as a person's own question is never
        # re-labeled into a public category that skips the question-level anonymization.
        return "question", max(rule_conf, conf), "rules (question kept over model's " + cat + ")"
    if rule_cat and rule_cat != cat:
        conf = min(conf, 0.6)
    return cat, round(conf, 2), "model: " + str(proposal.get("reason", ""))[:120]


def apply_guardrails(callback_context) -> types.Content | None:
    """Orchestrator after_agent_callback: enforce, publish, audit, and replace the model's text with the summary."""
    run = _RUNS.pop(callback_context.invocation_id, None)
    if run is None:
        return None
    st = callback_context.state
    proposals = dict(st.get("meseeks_merged") or {})
    if not proposals:
        proposals = _parse_classifications(str(st.get("meseeks_proposals") or ""))
    data, firm_domains, now = run["data"], run["firm_domains"], run["now"]
    existing_ids = {p["id"] for p in data["posts"]}
    existing_hashes = {p.get("hash") for p in data["posts"]}
    question_ids = {p["id"] for p in data["posts"] if p["category"] == "question"}

    expired = expire(data, now)
    audit = [{"message_id": m.message_id, "sender_domain": sender_domain(m.sender), "category": None, "publish": False,
              "reason": reason, "confidence": 0.0, "classifier": how} for m, reason, how in run.get("pre_held", [])]
    thread_ok = all(mid in run["messages"] for mid in proposals)
    for mid, msg in run["messages"].items():
        cat, conf, how = _advisory(msg, proposals.get(mid))
        d = enforce(msg, cat, conf, firm_domains, question_ids)
        entry = {"message_id": mid, "sender_domain": sender_domain(msg.sender), "category": d.category,
                 "publish": d.publish, "reason": d.reason, "confidence": d.confidence, "classifier": how}
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
    data["posts"].sort(key=lambda p: p["received"], reverse=True)
    data["generated_utc"] = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    published = [a for a in audit if a["publish"]]
    review = [review_item(run["messages"][a["message_id"]], a) for a in audit
              if not a["publish"] and a["reason"] != "duplicate" and a["message_id"] in run["messages"]
              and hard_reject(run["messages"][a["message_id"]]) is None]
    result = {"messages": len(audit), "published": len(published), "held": len(audit) - len(published),
              "for_review": len(review), "hitl_drill": backends.hitl_drill(), "thread_in_scope": thread_ok,
              "out_of_scope": sum(1 for _, reason, _ in run.get("pre_held", []) if reason.startswith("out of scope")),
              "pre_held": len(run.get("pre_held", [])),
              "expired": expired, "proposals": len(proposals), "dry_run": _dry_run(),
              "rounds": list(st.get("meseeks_rounds") or []), "window_s": backends.WINDOW.seconds,
              "elapsed_s": round(time.monotonic() - run["started"], 2), "audit": audit}

    if not _dry_run():
        path = Path(os.environ.get("MESEEKS_DATA", str(DATA)))
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
        LOG.mkdir(parents=True, exist_ok=True)
        with (LOG / f"{now:%Y-%m-%d}.jsonl").open("a") as fh:
            for a in audit:
                fh.write(json.dumps({"run": data["generated_utc"], "agent": "adk", **a}) + "\n")
        if review:
            queue_for_review(review, Path(os.environ.get("MESEEKS_REVIEW", str(REVIEW))))
        if run["imap"]:
            for a in audit:
                run["imap"].mark_processed(a["message_id"])
    if run["imap"]:
        run["imap"].close()

    st["meseeks_result"] = result
    by_cat: dict[str, int] = {}
    for a in published:
        by_cat[a["category"]] = by_cat.get(a["category"], 0) + 1
    held = "; ".join(f"{a['sender_domain']}: {a['reason']}" for a in audit if not a["publish"]) or "none"
    summary = (f"Meseeks run{' (dry run)' if _dry_run() else ''}: {len(published)} published "
               f"{json.dumps(by_cat)}, {len(audit) - len(published)} held [{held}], {expired} expired; "
               f"{len(result['rounds'])} round(s) in {result['elapsed_s']}s (window {backends.WINDOW.seconds:g}s per round).")
    return types.Content(role="model", parts=[types.Part(text=summary)])


def _redact_keeping_ids(text: str, ids: list[str]) -> str:
    """Redact identifiers in model output, but leave the batch's message ids intact (they are keys, not PII)."""
    keep = {f"\x00MID{i}\x00": mid for i, mid in enumerate(ids) if mid in text}
    for token, mid in keep.items():
        text = text.replace(mid, token)
    text = redact(text)
    for token, mid in keep.items():
        text = text.replace(token, mid)
    return text


def review_item(msg: Inbound, entry: dict[str, Any]) -> dict[str, Any]:
    """What the human sees: the redacted message and why it was held. The sender is never stored."""
    return {
        "id": entry.get("post_id") or msg.message_id,
        "message_id": msg.message_id,
        "sender_domain": sender_domain(msg.sender),
        "subject": redact(msg.subject.strip())[:140],
        "body": redact(normalize_body(msg.body)),
        "received": msg.received.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "attachments": [ctype for _, ctype in msg.attachments],
        "has_source_link": bool(extract_links(msg.body)),
        "links": extract_links(msg.body),
        "in_reply_to": msg.in_reply_to,
        "proposed": entry.get("category"),
        "reason": entry["reason"],
        "classifier": entry.get("classifier", ""),
        "status": "pending",
    }


def queue_for_review(items: list[dict[str, Any]], path: Path) -> None:
    queue = json.loads(path.read_text()) if path.exists() else {"inbox": "meseeks@legalluminary.com", "items": []}
    known = {i["message_id"] for i in queue["items"]}
    queue["items"].extend(i for i in items if i["message_id"] not in known)
    path.write_text(json.dumps(queue, indent=2, ensure_ascii=False) + "\n")


def redact_model_text(callback_context, llm_response):
    """after_model_callback: the model's own words never carry identifiers either."""
    run = _RUNS.get(callback_context.invocation_id) or {}
    ids = list(run.get("messages") or [])
    content = getattr(llm_response, "content", None)
    if content and content.parts:
        for p in content.parts:
            if getattr(p, "text", None):
                p.text = _redact_keeping_ids(p.text, ids)
    meta = getattr(llm_response, "custom_metadata", None) or {}
    if meta.get("meseeks_backend"):
        callback_context.state["meseeks_backend"] = meta["meseeks_backend"]
        callback_context.state["meseeks_backend_trace"] = meta.get("meseeks_trace", [])
    return None


def run_adk(config_path: str | Path | None = None, user_text: str = "Process the Meseeks inbox batch.") -> dict[str, Any]:
    """Load agent.yaml, run it once, return the result dict apply_guardrails left in state."""
    import asyncio

    from google.adk.agents.config_agent_utils import from_config
    from google.adk.runners import InMemoryRunner

    agent = from_config(str(config_path or Path(__file__).with_name("agent.yaml")))
    runner = InMemoryRunner(agent=agent, app_name="meseeks")

    async def go() -> dict[str, Any]:
        session = await runner.session_service.create_session(app_name="meseeks", user_id="meseeks")
        async for _ in runner.run_async(user_id="meseeks", session_id=session.id,
                                        new_message=types.Content(role="user", parts=[types.Part(text=user_text)])):
            pass
        session = await runner.session_service.get_session(app_name="meseeks", user_id="meseeks", session_id=session.id)
        result = dict(session.state.get("meseeks_result") or {})
        result.setdefault("backend", session.state.get("meseeks_backend", "none"))
        result["instruction_source"] = session.state.get("meseeks_instruction_source", "fallback")
        result["backend_trace"] = session.state.get("meseeks_backend_trace", [])
        return result

    return asyncio.run(go())
