import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "agents"))
os.environ["MESEEKS_RULES_ONLY"] = "1"

from meseeks import guardrails, mailbox  # noqa: E402
from meseeks.run import load_data, process  # noqa: E402

FIXTURES = Path(__file__).parent / "fixtures"
FIRMS = {"examplelaw.com"}
NOW = datetime(2026, 10, 15, 18, 0, tzinfo=timezone.utc)


def _run(firms=FIRMS):
    data = load_data(Path("/nonexistent"))
    msgs = mailbox.from_directory(FIXTURES)
    audit = process(msgs, data, firms, NOW)
    return data, {a["message_id"]: a for a in audit}


def test_fixture_outcomes():
    data, audit = _run()
    assert audit["<q1@gmail.com>"]["publish"] and audit["<q1@gmail.com>"]["category"] == "question"
    assert audit["<a1@examplelaw.com>"]["publish"] and audit["<a1@examplelaw.com>"]["category"] == "answer"
    assert not audit["<a2@yahoo.com>"]["publish"]
    assert "firm domain" in audit["<a2@yahoo.com>"]["reason"]
    assert audit["<n1@killeentexas.gov>"]["category"] == "notice" and audit["<n1@killeentexas.gov>"]["publish"]
    assert audit["<so1@bellcounty.texas.gov>"]["category"] == "standing_order" and audit["<so1@bellcounty.texas.gov>"]["publish"]
    assert audit["<o1@centexlegalaid.org>"]["category"] == "opportunity" and audit["<o1@centexlegalaid.org>"]["publish"]
    assert audit["<s1@seo-blast.biz>"]["reason"] == "spam"
    assert audit["<t1@example.org>"]["reason"] == "body too short"
    assert len(data["posts"]) == 5


def test_question_is_redacted():
    data, _ = _run()
    q = next(p for p in data["posts"] if p["category"] == "question")
    body = q["body"]
    assert "jane.doe@gmail.com" not in body
    assert "555-0199" not in body
    assert "Elm Street" not in body
    assert "[email redacted]" in body and "[phone redacted]" in body and "[address redacted]" in body
    assert q["source_label"] == "Anonymous"
    assert "Jane" not in body.split("\n")[-1]


def test_answer_links_to_question_and_never_names_sender():
    data, _ = _run()
    q = next(p for p in data["posts"] if p["category"] == "question")
    a = next(p for p in data["posts"] if p["category"] == "answer")
    assert a["in_reply_to"] == q["id"]
    assert "info@examplelaw.com" not in json.dumps(a)
    assert a["source_label"].startswith("Participating firm")


def test_answer_without_firm_list_is_held():
    data, audit = _run(firms=set())
    assert not audit["<a1@examplelaw.com>"]["publish"]
    assert all(p["category"] != "answer" for p in data["posts"])


def test_rerun_is_idempotent():
    data, _ = _run()
    msgs = mailbox.from_directory(FIXTURES)
    audit = process(msgs, data, FIRMS, NOW)
    assert all(not a["publish"] for a in audit)
    assert len(data["posts"]) == 5


def test_model_cannot_widen_gate():
    msg = mailbox.parse_eml((FIXTURES / "03_answer_from_random.eml").read_bytes())
    d = guardrails.enforce(msg, "answer", 0.99, FIRMS, {msg.in_reply_to})
    assert not d.publish


def test_subdomain_of_firm_allowed():
    assert guardrails.is_firm_domain("x <a@mail.examplelaw.com>", FIRMS)
    assert not guardrails.is_firm_domain("x <a@examplelaw.com.evil.net>", FIRMS)


def test_page_data_shape():
    data, _ = _run()
    for p in data["posts"]:
        assert set(p) >= {"id", "category", "title", "body", "received", "source_label", "links", "hash"}
        assert p["category"] in guardrails.CATEGORIES
