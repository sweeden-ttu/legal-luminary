"""Model backends for the Meseeks ADK agent, tried in order until one answers.

1. A local Ollama / LM Studio / any OpenAI-compatible server on MESEEKS_LLM_HOSTS
   (default 127.0.0.1,192.168.0.15) at MESEEKS_LLM_PORTS (default 1234,15443).
2. Agentic coders run headless with a single prompt, one unattended call each and a
   hard timeout, first success wins: claude, codex, agy, agent, opencode.
3. The Anthropic API through ADK's Claude model, when ANTHROPIC_API_KEY is set.

Every backend is a google.adk BaseLlm, so agent.yaml points at MODEL via `model_code`.
A backend that times out, errors, or returns nothing hands off to the next one; when the
whole chain is exhausted the agent still completes and the keyword rules classify the batch.
"""
from __future__ import annotations

import asyncio
import json
import os
import shlex
import shutil
import subprocess
import time
import urllib.error
import urllib.request
from collections.abc import AsyncGenerator
from dataclasses import dataclass
from typing import Any

from google.adk.models.base_llm import BaseLlm
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.genai import types
from pydantic import Field

HOSTS = [h.strip() for h in os.environ.get("MESEEKS_LLM_HOSTS", "127.0.0.1,192.168.0.15").split(",") if h.strip()]
PORTS = [int(p) for p in os.environ.get("MESEEKS_LLM_PORTS", "1234,15443").split(",") if p.strip()]
PROBE_TIMEOUT = float(os.environ.get("MESEEKS_LLM_PROBE_TIMEOUT", "2"))
#: No single unattended sub-agent call may be waited on longer than this (the "1 minute").
MAX_CALL_SECONDS = float(os.environ.get("MESEEKS_MAX_CALL_SECONDS", "60"))
#: Window per round = WINDOW_SLACK x the sum of sub-agent budgets: room for spawn/probe
#: overhead, but not enough for a stalling model to hold the orchestration. During a
#: human-in-the-loop drill (MESEEKS_HITL=1) a human is standing by, so it shrinks to 90%.
WINDOW_SLACK = float(os.environ.get("MESEEKS_WINDOW_SLACK", "1.3"))
WINDOW_SLACK_DRILL = float(os.environ.get("MESEEKS_WINDOW_SLACK_DRILL", "0.9"))


def hitl_drill() -> bool:
    return os.environ.get("MESEEKS_HITL", "").lower() in ("1", "true", "yes")


def window_slack() -> float:
    return WINDOW_SLACK_DRILL if hitl_drill() else WINDOW_SLACK
LOCAL_TIMEOUT = float(os.environ.get("MESEEKS_LLM_TIMEOUT", "20"))
API_TIMEOUT = float(os.environ.get("MESEEKS_API_TIMEOUT", "30"))
UA = "LegalLuminaryMeseeks/1.0 (+https://legalluminary.com/meseeks/)"

DEFAULT_CODERS: list[dict[str, Any]] = [
    {"name": "claude", "argv": ["claude", "-p", "{prompt}", "--output-format", "text"], "timeout": 15},
    {"name": "codex", "argv": ["codex", "exec", "--skip-git-repo-check", "{prompt}"], "timeout": 15},
    {"name": "agy", "argv": ["agy", "--prompt", "{prompt}"], "timeout": 10},
    {"name": "agent", "argv": ["agent", "-p", "{prompt}", "--output-format", "text"], "timeout": 10},
    {"name": "opencode", "argv": ["opencode", "run", "{prompt}"], "timeout": 20},
]


def coder_specs() -> list[dict[str, Any]]:
    """Coder battery, overridable with MESEEKS_CODERS (JSON list of {name, argv, timeout})."""
    raw = os.environ.get("MESEEKS_CODERS")
    if not raw:
        return DEFAULT_CODERS
    specs = json.loads(raw)
    for s in specs:
        if isinstance(s.get("argv"), str):
            s["argv"] = shlex.split(s["argv"])
        s.setdefault("timeout", 10)
    return specs


def call_budget(seconds: float) -> float:
    """A sub-agent's cycles for one call: its own setting, never above MAX_CALL_SECONDS."""
    return max(0.0, min(float(seconds), MAX_CALL_SECONDS))


# --------------------------------------------------------------------------- clock

class Window:
    """The orchestrator's clock for one round: WINDOW_SLACK (1.3) x the sum of sub-agent budgets.

    Every sub-agent (local server, each coder, the API) is a single unattended call with its own
    budget (<= MAX_CALL_SECONDS). The 30% over their sum absorbs spawn and probe overhead without
    leaving a stalling or malicious model much to exploit; each call is still capped by what is
    left of the window, so the round can never overrun it. When it closes with no answer the
    rules decide.
    """

    def __init__(self, seconds: float | None = None) -> None:
        self.override = seconds
        self.seconds = seconds if seconds is not None else 0.0
        self.started: float | None = None

    def start(self, seconds: float | None = None) -> None:
        if seconds is not None:
            self.seconds = seconds
        elif self.override is not None:
            self.seconds = self.override
        self.started = time.monotonic()

    def elapsed(self) -> float:
        return 0.0 if self.started is None else time.monotonic() - self.started

    def remaining(self) -> float:
        return self.seconds if self.started is None else max(0.0, self.seconds - self.elapsed())

    def budget(self, want: float) -> float:
        """Timeout for one sub-agent call: its own budget, capped by what is left of the window."""
        return max(0.0, min(want, self.remaining()))

    def expired(self) -> bool:
        return self.remaining() <= 0.0


WINDOW = Window(float(os.environ["MESEEKS_WINDOW_SECONDS"]) if os.environ.get("MESEEKS_WINDOW_SECONDS") else None)


# --------------------------------------------------------------------------- prompt flattening

def flatten_request(llm_request: LlmRequest) -> tuple[str, list[dict[str, str]]]:
    """Reduce an LlmRequest to (system_text, [{role, content}]) for chat-completions or a single prompt."""
    system = ""
    si = llm_request.config.system_instruction if llm_request.config else None
    if isinstance(si, str):
        system = si
    elif si is not None:
        parts = getattr(si, "parts", None) or (si if isinstance(si, list) else [])
        system = "\n".join(getattr(p, "text", "") or (p if isinstance(p, str) else "") for p in parts)
    messages = []
    for c in llm_request.contents or []:
        text = "\n".join(p.text for p in (c.parts or []) if getattr(p, "text", None))
        if text.strip():
            messages.append({"role": "assistant" if c.role == "model" else "user", "content": text})
    if not messages:
        messages.append({"role": "user", "content": "Process the batch in the system instruction."})
    return system, messages


def single_prompt(system: str, messages: list[dict[str, str]]) -> str:
    """One unattended prompt for a headless coder: registry wrapper + instruction + turns."""
    from .prompts import get as get_prompt

    wrapper = get_prompt("meseeks.coder_wrapper").text
    body = "\n\n".join(f"[{m['role']}]\n{m['content']}" for m in messages)
    return "\n\n".join(x for x in (wrapper, system, body, "Reply with the JSON object only.") if x)


def text_response(text: str, label: str, **meta: Any) -> LlmResponse:
    return LlmResponse(
        content=types.Content(role="model", parts=[types.Part(text=text)]),
        custom_metadata={"meseeks_backend": label, **meta},
    )


# --------------------------------------------------------------------------- 1. local server

@dataclass
class LocalServer:
    base_url: str
    model: str
    kind: str  # "openai" | "ollama"


def _get_json(url: str, timeout: float) -> Any:
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def _pick(models: list[str]) -> str | None:
    want = os.environ.get("MESEEKS_LLM_MODEL")
    if want:
        for m in models:
            if want in m:
                return m
        return None
    return models[0] if models else None


def discover(hosts: list[str] | None = None, ports: list[int] | None = None) -> LocalServer | None:
    """First reachable local server, probing /v1/models then Ollama's /api/tags."""
    for host in hosts or HOSTS:
        for port in ports or PORTS:
            schemes = ("http", "https") if port == 15443 else ("http",)
            for scheme in schemes:
                base = f"{scheme}://{host}:{port}"
                try:
                    data = _get_json(f"{base}/v1/models", PROBE_TIMEOUT)
                    m = _pick([x["id"] for x in data.get("data", [])])
                    if m:
                        return LocalServer(f"{base}/v1", m, "openai")
                except Exception:
                    pass
                try:
                    data = _get_json(f"{base}/api/tags", PROBE_TIMEOUT)
                    m = _pick([x["name"] for x in data.get("models", [])])
                    if m:
                        return LocalServer(f"{base}/v1", m, "ollama")
                except Exception:
                    pass
    return None


class LocalServerLlm(BaseLlm):
    """ADK model over an OpenAI-compatible /v1/chat/completions endpoint found by discover()."""

    model: str = "local-server"
    timeout: float = LOCAL_TIMEOUT

    def budget(self) -> float:
        return call_budget(self.timeout)

    @classmethod
    def supported_models(cls) -> list[str]:
        return ["local-server"]

    async def generate_content_async(self, llm_request: LlmRequest, stream: bool = False) -> AsyncGenerator[LlmResponse, None]:
        server = discover()
        if not server:
            raise RuntimeError("no local model server on " + ", ".join(f"{h}:{p}" for h in HOSTS for p in PORTS))
        system, messages = flatten_request(llm_request)
        if system:
            messages = [{"role": "system", "content": system}, *messages]
        cfg = llm_request.config
        payload = {
            "model": server.model,
            "messages": messages,
            "temperature": getattr(cfg, "temperature", None) if cfg else None,
            "max_tokens": getattr(cfg, "max_output_tokens", None) if cfg else None,
            "stream": False,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        req = urllib.request.Request(
            f"{server.base_url}/chat/completions",
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json", "Authorization": "Bearer local", "User-Agent": UA},
        )
        budget = WINDOW.budget(self.budget())
        if budget <= 0:
            raise RuntimeError("window expired before local server call")
        with urllib.request.urlopen(req, timeout=budget) as r:
            data = json.loads(r.read().decode())
        text = (data.get("choices") or [{}])[0].get("message", {}).get("content") or ""
        if not text.strip():
            raise RuntimeError(f"empty completion from {server.base_url} ({server.model})")
        yield text_response(text, f"local:{server.kind}:{server.base_url}:{server.model}")


# --------------------------------------------------------------------------- 2. headless coders

class CoderLlm(BaseLlm):
    """Runs the coder battery headless, one unattended call each, until one returns usable text."""

    model: str = "coder-battery"
    specs: list[dict[str, Any]] = Field(default_factory=coder_specs)
    min_chars: int = 20
    attempts: list[dict[str, Any]] = Field(default_factory=list)

    @classmethod
    def supported_models(cls) -> list[str]:
        return ["coder-battery"]

    def budget(self) -> float:
        return sum(call_budget(s["timeout"]) for s in (self.specs or coder_specs()))

    def run(self, prompt: str) -> tuple[str, str] | None:
        self.attempts = []
        for spec in self.specs or coder_specs():
            name, argv, timeout = spec["name"], list(spec["argv"]), float(spec["timeout"])
            exe = shutil.which(argv[0])
            if not exe:
                self.attempts.append({"coder": name, "status": "missing"})
                continue
            timeout = WINDOW.budget(call_budget(timeout))
            if timeout <= 0:
                self.attempts.append({"coder": name, "status": "window expired"})
                break
            argv = [exe, *(a.replace("{prompt}", prompt) for a in argv[1:])]
            env = {**os.environ, "CI": "1", "TERM": "dumb", "NO_COLOR": "1"}
            try:
                cp = subprocess.run(argv, input="", capture_output=True, text=True, timeout=timeout, env=env)
            except subprocess.TimeoutExpired:
                self.attempts.append({"coder": name, "status": f"timeout {timeout:g}s"})
                continue
            except OSError as e:
                self.attempts.append({"coder": name, "status": f"error {type(e).__name__}"})
                continue
            text = cp.stdout.strip()
            if cp.returncode == 0 and len(text) >= self.min_chars:
                self.attempts.append({"coder": name, "status": "ok"})
                return text, name
            self.attempts.append({"coder": name, "status": f"rc={cp.returncode}", "stderr": cp.stderr[-300:]})
        return None

    async def generate_content_async(self, llm_request: LlmRequest, stream: bool = False) -> AsyncGenerator[LlmResponse, None]:
        system, messages = flatten_request(llm_request)
        got = self.run(single_prompt(system, messages))
        if not got:
            raise RuntimeError("no coder produced output: " + json.dumps(self.attempts))
        text, name = got
        yield text_response(text, f"coder:{name}", attempts=list(self.attempts))


# --------------------------------------------------------------------------- 3. chain

def backend_budget(backend: BaseLlm) -> float:
    """Cycles one backend may take for a single call (a coder battery counts each coder)."""
    fn = getattr(backend, "budget", None)
    if callable(fn):
        return float(fn())
    return call_budget(API_TIMEOUT)


class FallbackLlm(BaseLlm):
    """One round: try each sub-agent in order inside a window equal to the sum of their budgets.

    Never hangs on one (each call is awaited for at most its budget, capped by what is left of
    the window) and never fails the run: if every backend fails, yields an empty classification
    object with error_message set so the after-agent guardrails fall back to the keyword rules.
    """

    model: str = "meseeks-fallback"
    backends: list[BaseLlm] = Field(default_factory=list)
    trace: list[dict[str, Any]] = Field(default_factory=list)

    @classmethod
    def supported_models(cls) -> list[str]:
        return ["meseeks-fallback"]

    def window_seconds(self) -> float:
        return round(window_slack() * sum(backend_budget(b) for b in self.backends), 3)

    async def _first_response(self, backend: BaseLlm, llm_request: LlmRequest) -> LlmResponse | None:
        gen = backend.generate_content_async(llm_request, stream=False)
        try:
            async for resp in gen:
                if resp.content and resp.content.parts and any(getattr(p, "text", "") for p in resp.content.parts):
                    return resp
            return None
        finally:
            await gen.aclose()

    async def generate_content_async(self, llm_request: LlmRequest, stream: bool = False) -> AsyncGenerator[LlmResponse, None]:
        self.trace = []
        WINDOW.start(None if WINDOW.override is not None else self.window_seconds())
        for backend in self.backends:
            label = type(backend).__name__
            budget = WINDOW.budget(backend_budget(backend))
            if budget <= 0:
                self.trace.append({"backend": label, "status": f"skipped: window of {WINDOW.seconds:g}s expired"})
                continue
            try:
                resp = await asyncio.wait_for(self._first_response(backend, llm_request), timeout=budget)
                if resp is not None:
                    self.trace.append({"backend": label, "status": "ok", "elapsed_s": round(WINDOW.elapsed(), 2)})
                    meta = dict(resp.custom_metadata or {})
                    meta["meseeks_trace"] = list(self.trace)
                    resp.custom_metadata = meta
                    yield resp
                    return
                self.trace.append({"backend": label, "status": "empty"})
            except asyncio.TimeoutError:
                self.trace.append({"backend": label, "status": f"timeout {budget:g}s"})
            except Exception as e:  # noqa: BLE001 - every backend failure must hand off
                self.trace.append({"backend": label, "status": f"error {type(e).__name__}: {e}"[:300]})
        yield LlmResponse(
            content=types.Content(role="model", parts=[types.Part(text='{"classifications": []}')]),
            error_message="all model backends failed or window expired; rules only",
            custom_metadata={"meseeks_backend": "none", "meseeks_trace": list(self.trace)},
        )


def build_chain() -> FallbackLlm:
    chain: list[BaseLlm] = [LocalServerLlm(), CoderLlm()]
    if os.environ.get("ANTHROPIC_API_KEY") and not os.environ.get("MESEEKS_NO_API"):
        try:
            from google.adk.models.anthropic_llm import Claude

            chain.append(Claude(model=os.environ.get("LL_ADK_MODEL", "claude-sonnet-5-5")))  # budget: API_TIMEOUT
        except Exception:  # noqa: BLE001 - anthropic SDK optional
            pass
    return FallbackLlm(backends=chain)


#: Referenced from agent.yaml as `model_code: {name: meseeks.backends.MODEL}`.
MODEL = build_chain()
