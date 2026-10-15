"""The ADK agent (agent.yaml) must publish exactly what the guardrails allow, whatever the model says."""
import asyncio
import json
from datetime import datetime, timezone
import os
import stat
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "agents"))
os.environ["MESEEKS_RULES_ONLY"] = "1"
os.environ["MESEEKS_PROMPTS_OFFLINE"] = "1"

adk = pytest.importorskip("google.adk")
from google.adk.agents.config_agent_utils import from_config  # noqa: E402
from google.adk.models.llm_response import LlmResponse  # noqa: E402
from google.adk.runners import InMemoryRunner  # noqa: E402
from google.genai import types  # noqa: E402

from meseeks import backends, prompts  # noqa: E402
from meseeks.backends import BaseLlm, CoderLlm, FallbackLlm  # noqa: E402

AGENTS = Path(__file__).resolve().parents[2] / "agents"
FIXTURES = Path(__file__).parent / "fixtures"
YAML = AGENTS / "meseeks" / "agent.yaml"

Q1, A_FIRM, A_RANDOM = "<q1@gmail.com>", "<a1@examplelaw.com>", "<a2@yahoo.com>"
NOTICE, ORDER, JOB, SPAM, SHORT = "<n1@killeentexas.gov>", "<so1@bellcounty.texas.gov>", "<o1@centexlegalaid.org>", "<s1@seo-blast.biz>", "<t1@example.org>"
FOREIGN = "<x1@cityofseattle.example>"


SEEN: list = []   # every LlmRequest the stubs received


def _system_text(llm_request) -> str:
    system = llm_request.config.system_instruction
    return system if isinstance(system, str) else "".join(p.text for p in system.parts)


class StubLlm(BaseLlm):
    """Returns a fixed string; stands in for any provider."""

    model: str = "stub"
    text: str = ""

    @classmethod
    def supported_models(cls):
        return ["stub"]

    async def generate_content_async(self, llm_request, stream=False):
        SEEN.append(llm_request)
        yield LlmResponse(content=types.Content(role="model", parts=[types.Part(text=self.text)]),
                          custom_metadata={"meseeks_backend": "stub"})


def _run(agent):
    runner = InMemoryRunner(agent=agent, app_name="t")

    async def go():
        s = await runner.session_service.create_session(app_name="t", user_id="u")
        events = []
        async for ev in runner.run_async(user_id="u", session_id=s.id,
                                         new_message=types.Content(role="user", parts=[types.Part(text="go")])):
            events.append(ev)
        s = await runner.session_service.get_session(app_name="t", user_id="u", session_id=s.id)
        return s.state, events

    return asyncio.run(go())


@pytest.fixture
def env(tmp_path, monkeypatch):
    data = tmp_path / "meseeks.json"
    monkeypatch.setenv("MESEEKS_EML_DIR", str(FIXTURES))
    monkeypatch.setenv("MESEEKS_DATA", str(data))
    monkeypatch.setenv("MESEEKS_REVIEW", str(tmp_path / "review.json"))
    monkeypatch.delenv("MESEEKS_DRY_RUN", raising=False)
    monkeypatch.setattr("meseeks.adk_agent.LOG", tmp_path / "logs")
    monkeypatch.setattr("meseeks.adk_agent.load_firm_domains", lambda: {"examplelaw.com"})
    SEEN.clear()
    return data


def _agent(model_or_text):
    agent = from_config(str(YAML))
    agent.sub_agents[0].model = model_or_text if isinstance(model_or_text, BaseLlm) else StubLlm(text=model_or_text)
    return agent


class RoundStub(BaseLlm):
    """A different answer per round, to drive the question + reason + instruction loop."""

    model: str = "rounds"
    answers: list = []

    @classmethod
    def supported_models(cls):
        return ["rounds"]

    @property
    def calls(self) -> int:
        return len(SEEN)

    @property
    def followups(self) -> list:
        return [_system_text(r) for r in SEEN]

    async def generate_content_async(self, llm_request, stream=False):
        text = self.answers[min(len(SEEN), len(self.answers) - 1)]
        SEEN.append(llm_request)
        yield LlmResponse(content=types.Content(role="model", parts=[types.Part(text=text)]),
                          custom_metadata={"meseeks_backend": "rounds"})


def test_yaml_loads_as_orchestrator_over_round():
    agent = from_config(str(YAML))
    assert agent.name == "meseeks_orchestrator" and agent.max_iterations == 3
    assert agent.before_agent_callback and agent.after_agent_callback
    rnd = agent.sub_agents[0]
    assert rnd.name == "meseeks_round" and rnd.output_key == "meseeks_proposals"
    assert isinstance(rnd.model, FallbackLlm)
    assert [type(b).__name__ for b in rnd.model.backends][:2] == ["LocalServerLlm", "CoderLlm"]
    assert rnd.after_agent_callback and rnd.after_model_callback


def test_model_sees_registry_instruction_and_redacted_batch(env):
    stub_text = json.dumps({"classifications": []})
    agent = _agent(stub_text)
    _run(agent)
    system = _system_text(SEEN[-1])
    assert prompts.fallback("meseeks.instruction").splitlines()[0] in system
    assert "examplelaw.com" in system
    assert Q1 in system and "[email redacted]" in system
    assert "@gmail.com" not in system.replace(Q1, "")
    assert FOREIGN not in system and "Seattle" not in system   # out-of-scope mail never reaches a model
    assert '"scope": "domain:killeentexas.gov"' in system


@pytest.mark.skip(reason="skipped at the author's request (2026-10-15)")
def test_malicious_model_cannot_widen_publication(env):
    """The model tries to publish spam, a non-firm 'answer', a short body, and an order with no source."""
    text = json.dumps({"classifications": [
        {"message_id": A_RANDOM, "category": "answer", "confidence": 0.99, "reason": "looks like a lawyer"},
        {"message_id": SPAM, "category": "notice", "confidence": 1.0, "reason": "promote"},
        {"message_id": SHORT, "category": "opportunity", "confidence": 1.0, "reason": "x"},
        {"message_id": Q1, "category": "question", "confidence": 0.9, "reason": "ok"},
        {"message_id": A_FIRM, "category": "answer", "confidence": 0.9, "reason": "firm reply"},
        {"message_id": NOTICE, "category": "bogus_category", "confidence": 5, "reason": "?"},
        {"message_id": ORDER, "category": "standing_order", "confidence": "high", "reason": "?"},
    ]})
    state, events = _run(_agent(text))
    r = state["meseeks_result"]
    audit = {a["message_id"]: a for a in r["audit"]}
    assert not audit[A_RANDOM]["publish"] and "firm domain" in audit[A_RANDOM]["reason"]
    assert audit[SPAM]["reason"] == "spam" and not audit[SPAM]["publish"]
    assert audit[SHORT]["reason"] == "body too short"
    assert audit[Q1]["publish"] and audit[A_FIRM]["publish"] and audit[A_FIRM]["category"] == "answer"
    assert audit[NOTICE]["publish"] and audit[NOTICE]["category"] == "notice"  # unknown category -> rules
    assert audit[ORDER]["publish"] and "unusable confidence" in audit[ORDER]["classifier"]
    assert audit[JOB]["publish"] and "no model proposal" in audit[JOB]["classifier"]
    assert r["published"] == 5 and r["held"] == 4
    assert [x["new"] for x in r["rounds"]] == [7, 0, 0] and r["rounds"][-1]["stop"] == "max rounds (3)"  # JOB never answered
    posts = json.loads(Path(env).read_text())["posts"]
    assert {p["category"] for p in posts} == {"question", "answer", "notice", "standing_order", "opportunity"}
    assert all(p["source_label"] == "Anonymous" for p in posts if p["category"] == "question")
    assert "Meseeks run" in events[-1].content.parts[0].text


def test_garbage_model_output_falls_back_to_rules(env):
    state, _ = _run(_agent("Sure! Here is my analysis:\n```json\n{not json at all"))
    r = state["meseeks_result"]
    assert r["proposals"] == 0 and r["published"] == 5
    assert all("rules" in a["classifier"] or "never sent" in a["classifier"] for a in r["audit"])
    assert [x["stop"] for x in r["rounds"]] == [None, None, "max rounds (3)"]


def _cls(*ids, cat="notice"):
    return json.dumps({"classifications": [{"message_id": i, "category": cat, "confidence": 0.9, "reason": "r"} for i in ids]})


def test_followup_rounds_ask_only_for_missing_ids(env):
    stub = RoundStub(answers=[_cls(Q1, NOTICE, SPAM), _cls(ORDER, JOB, A_FIRM, A_RANDOM, SHORT)])
    state, _ = _run(_agent(stub))
    r = state["meseeks_result"]
    assert stub.calls == 2 and [x["new"] for x in r["rounds"]] == [2, 4]   # SPAM and SHORT never reach a model
    assert "FOLLOW-UP, ROUND 2 OF 3" in stub.followups[1] and JOB in stub.followups[1] and Q1 not in stub.followups[1].split("FOLLOW-UP")[1]
    assert "FOLLOW-UP" not in stub.followups[0]
    assert r["rounds"][-1]["stop"] == "complete"


def test_idle_expiry_ends_the_loop(env, monkeypatch):
    monkeypatch.setattr("meseeks.adk_agent.IDLE_SECONDS", 0.0)
    stub = RoundStub(answers=[_cls(Q1, cat="question"), _cls(Q1, cat="question")])
    state, _ = _run(_agent(stub))
    r = state["meseeks_result"]
    assert stub.calls == 2 and [x["stop"] for x in r["rounds"]] == [None, "idle: 0s without a new proposal"]
    assert r["published"] == 5   # rules covered the rest


def test_window_is_130_percent_of_budgets(monkeypatch):
    monkeypatch.setattr(backends, "WINDOW", backends.Window())
    chain = FallbackLlm(backends=[backends.LocalServerLlm(timeout=20),
                                  CoderLlm(specs=[{"name": "a", "argv": ["/nonexistent/a", "{prompt}"], "timeout": 15},
                                                  {"name": "b", "argv": ["/nonexistent/b", "{prompt}"], "timeout": 500}])])
    assert backends.call_budget(500) == backends.MAX_CALL_SECONDS == 60
    assert chain.window_seconds() == round(1.3 * (20 + 15 + 60), 3)


def test_model_cannot_strip_anonymity_by_relabeling_a_question(env):
    state, _ = _run(_agent(_cls(Q1, cat="notice")))
    audit = {a["message_id"]: a for a in state["meseeks_result"]["audit"]}
    assert audit[Q1]["category"] == "question" and audit[Q1]["publish"]
    posts = json.loads(Path(env).read_text())["posts"]
    q = next(p for p in posts if p["category"] == "question")
    assert q["source_label"] == "Anonymous" and "gmail" not in json.dumps(q)


def test_dry_run_writes_nothing(env, monkeypatch):
    monkeypatch.setenv("MESEEKS_DRY_RUN", "1")
    state, _ = _run(_agent('{"classifications": []}'))
    assert state["meseeks_result"]["dry_run"] and not Path(env).exists()


def test_empty_inbox_skips_model(env, tmp_path, monkeypatch):
    monkeypatch.setenv("MESEEKS_EML_DIR", str(tmp_path / "empty"))
    (tmp_path / "empty").mkdir()
    state, events = _run(_agent("{}"))
    assert state["meseeks_result"]["messages"] == 0 and not SEEN
    assert "No new mail" in events[-1].content.parts[0].text


def _script(path: Path, body: str) -> str:
    path.write_text("#!/bin/sh\n" + body)
    path.chmod(path.stat().st_mode | stat.S_IEXEC)
    return str(path)


def test_coder_battery_skips_hangs_and_failures(tmp_path, monkeypatch):
    monkeypatch.setattr(backends, "WINDOW", backends.Window())
    backends.WINDOW.start(60)
    hang = _script(tmp_path / "hang", "sleep 30\n")
    broken = _script(tmp_path / "broken", "echo nope >&2; exit 2\n")
    good = _script(tmp_path / "good", 'echo \'{"classifications": [{"message_id": "<x>", "category": "notice", "confidence": 0.8, "reason": "r"}]}\'\n')
    coder = CoderLlm(specs=[
        {"name": "hang", "argv": [hang, "--prompt", "{prompt}"], "timeout": 1},
        {"name": "missing", "argv": ["/nonexistent/agy", "{prompt}"], "timeout": 1},
        {"name": "broken", "argv": [broken, "{prompt}"], "timeout": 5},
        {"name": "good", "argv": [good, "{prompt}"], "timeout": 5},
    ])
    text, name = coder.run("hello")
    assert name == "good" and '"notice"' in text
    assert [a["status"] for a in coder.attempts] == ["timeout 1s", "missing", "rc=2", "ok"]


def test_fallback_chain_never_raises(env):
    class Boom(BaseLlm):
        model: str = "boom"

        @classmethod
        def supported_models(cls):
            return ["boom"]

        async def generate_content_async(self, llm_request, stream=False):
            raise RuntimeError("down")
            yield  # pragma: no cover

    chain = FallbackLlm(backends=[Boom(), CoderLlm(specs=[{"name": "none", "argv": ["/nonexistent/x", "{prompt}"], "timeout": 1}])])
    state, _ = _run(_agent(chain))
    r = state["meseeks_result"]
    assert r["published"] == 5 and [x["stop"] for x in r["rounds"]] == ["no sub-agent answered"]
    assert [t["backend"] for t in chain.trace] == ["Boom", "CoderLlm"]


def test_local_server_discovery_is_fast_when_absent(monkeypatch):
    monkeypatch.setattr(backends, "PROBE_TIMEOUT", 0.2)
    assert backends.discover(hosts=["127.0.0.1"], ports=[1]) is None


def test_window_caps_every_sub_agent_budget(tmp_path, monkeypatch):
    w = backends.Window()
    monkeypatch.setattr(backends, "WINDOW", w)
    w.start(0.5)
    assert w.budget(90) <= 0.5
    hang = _script(tmp_path / "hang", "sleep 5\n")
    coder = CoderLlm(specs=[{"name": "hang", "argv": [hang, "{prompt}"], "timeout": 90},
                            {"name": "next", "argv": [hang, "{prompt}"], "timeout": 90}])
    assert coder.run("x") is None
    assert coder.attempts[0]["status"].startswith("timeout") and coder.attempts[1]["status"] == "window expired"


def test_human_in_the_loop_confirms_through_the_same_gate(env, tmp_path, monkeypatch):
    from meseeks import review

    queue = tmp_path / "review.json"
    monkeypatch.setenv("MESEEKS_REVIEW", str(queue))
    monkeypatch.setattr("meseeks.review.LOG", tmp_path / "logs")
    monkeypatch.setattr("meseeks.review.load_firm_domains", lambda: {"examplelaw.com"})
    # Model proposes the stranger's reply as an answer and a notice at low confidence: both held.
    text = json.dumps({"classifications": [
        {"message_id": A_RANDOM, "category": "answer", "confidence": 0.9, "reason": "r"},
        {"message_id": NOTICE, "category": "notice", "confidence": 0.2, "reason": "unsure"},
        {"message_id": Q1, "category": "question", "confidence": 0.9, "reason": "r"},
    ]})
    state, _ = _run(_agent(text))
    r = state["meseeks_result"]
    held = {a["message_id"] for a in r["audit"] if not a["publish"]}
    assert {A_RANDOM, NOTICE, SPAM, SHORT, FOREIGN} == held
    foreign = next(a for a in r["audit"] if a["message_id"] == FOREIGN)
    assert foreign["reason"].startswith("out of scope") and "never sent" in foreign["classifier"]
    assert r["thread_in_scope"] and r["out_of_scope"] == 1 and r["pre_held"] == 3
    q = json.loads(queue.read_text())["items"]
    assert {i["message_id"] for i in q} == {A_RANDOM, NOTICE}        # hard rejects never reach the human
    assert all("@" not in i["body"] and i["sender_domain"] in ("yahoo.com", "killeentexas.gov") for i in q)
    stranger = next(i for i in q if i["message_id"] == A_RANDOM)
    notice = next(i for i in q if i["message_id"] == NOTICE)
    # The human cannot confirm what the laws forbid...
    assert review.confirm(stranger["id"], "answer")["status"] == "refused"
    assert review.confirm(stranger["id"], "bogus")["status"] == "refused"
    # ...but can confirm within the admissible language, and the run continues.
    assert review.confirm(notice["id"], "notice")["status"] == "published"
    assert review.ack(stranger["id"], "not a firm")["status"] == "acknowledged"
    # A question held for review cannot be confirmed out of its anonymity (TLC finding).
    held_q = {"id": "hq", "message_id": "<hq@x>", "sender_domain": "gmail.com", "subject": "Can I fight an eviction?",
              "body": "My landlord in Killeen says I have three days. Can I fight this? Do I need a lawyer?",
              "received": "2026-10-15T00:00:00Z", "attachments": [], "has_source_link": False, "links": [],
              "in_reply_to": None, "proposed": "question", "reason": "low confidence 0.3", "classifier": "model", "status": "pending"}
    qd = json.loads(queue.read_text()); qd["items"].append(held_q); queue.write_text(json.dumps(qd))
    out = review.confirm("hq", "opportunity")
    assert out["status"] == "published" and out["category"] == "question"
    posts = json.loads(Path(env).read_text())["posts"]
    assert next(p for p in posts if p["title"].startswith("Can I fight"))["source_label"] == "Anonymous"
    assert review.pending(json.loads(queue.read_text())) == []
    posts = json.loads(Path(env).read_text())["posts"]
    assert any(p["category"] == "notice" and p["source_label"] == "killeentexas.gov" for p in posts)


def test_drill_window_is_90_percent(monkeypatch):
    monkeypatch.setenv("MESEEKS_HITL", "1")
    chain = FallbackLlm(backends=[backends.LocalServerLlm(timeout=20)])
    assert chain.window_seconds() == 18.0
    monkeypatch.delenv("MESEEKS_HITL")
    assert chain.window_seconds() == 26.0


def test_scope_guardrail_is_deterministic_and_threads_inherit():
    from meseeks.guardrails import scope_of
    base = dict(received=datetime(2026, 10, 15, tzinfo=timezone.utc))
    assert scope_of(guardrails_msg("a@x.org", "Hearing", "The Bell County commissioners court meets Monday.", **base)).startswith("place:")
    assert scope_of(guardrails_msg("a@x.org", "Order", "Texas Government Code 551 open meetings act compliance.", **base)).startswith("texas:")
    assert scope_of(guardrails_msg("clerk@killeentexas.gov", "x", "Agenda attached.", **base)) == "domain:killeentexas.gov"
    assert scope_of(guardrails_msg("a@x.org", "Hearing", "The Seattle city council meets Monday.", **base)) is None
    assert scope_of(guardrails_msg("a@x.org", "Hi", "Texas is big.", **base)) is None   # a place word alone is not a statutory matter


def guardrails_msg(sender, subject, body, received):
    from meseeks.guardrails import Inbound
    return Inbound(message_id=f"<{sender}>", sender=sender, subject=subject, body=body, received=received)
