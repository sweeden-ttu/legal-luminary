"""Model backends, in preference order:

1. A local OpenAI-compatible or Ollama server on DIGEST_LLM_HOSTS at ports 1234 and 15443,
   driven through a Google ADK LlmAgent (LiteLlm).
2. Agentic coders over stdio, one unattended prompt each, first success wins:
   claude (60s), agy (60s), opencode (180s), agent / cursor (60s).
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import urllib.error
import urllib.request
from dataclasses import dataclass

HOSTS = [h.strip() for h in os.environ.get("DIGEST_LLM_HOSTS", "192.168.0.15,127.0.0.1").split(",") if h.strip()]
PORTS = [int(p) for p in os.environ.get("DIGEST_LLM_PORTS", "1234,15443").split(",")]
PROBE_TIMEOUT = float(os.environ.get("DIGEST_PROBE_TIMEOUT", "2"))

CODERS: list[tuple[str, list[str], int]] = [
    ("claude", ["claude", "-p", "--output-format", "text"], 60),
    ("agy", ["agy"], 60),
    ("opencode", ["opencode", "run"], 180),
    ("agent", ["agent", "-p"], 60),
]


@dataclass
class LocalModel:
    base_url: str      # OpenAI-compatible base, e.g. http://192.168.0.15:1234/v1
    model: str
    kind: str          # "openai" | "ollama"


def _get_json(url: str):
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=PROBE_TIMEOUT) as r:
        return json.loads(r.read().decode())


def _pick(models: list[str]) -> str | None:
    if not models:
        return None
    want = os.environ.get("DIGEST_LLM_MODEL")
    if want:
        for m in models:
            if want in m:
                return m
    return models[0]


def discover() -> LocalModel | None:
    for host in HOSTS:
        for port in PORTS:
            for scheme in ("http", "https") if port == 15443 else ("http",):
                base = f"{scheme}://{host}:{port}"
                try:
                    data = _get_json(f"{base}/v1/models")
                    m = _pick([x["id"] for x in data.get("data", [])])
                    if m:
                        return LocalModel(f"{base}/v1", m, "openai")
                except Exception:
                    pass
                try:
                    data = _get_json(f"{base}/api/tags")
                    m = _pick([x["name"] for x in data.get("models", [])])
                    if m:
                        return LocalModel(f"{base}/v1", m, "ollama")
                except Exception:
                    pass
    return None


def run_adk(local: LocalModel, system: str, prompt: str) -> str:
    """Run a single-turn ADK LlmAgent against the discovered local server."""
    import asyncio

    from google.adk.agents import LlmAgent
    from google.adk.models.lite_llm import LiteLlm
    from google.adk.runners import InMemoryRunner
    from google.genai import types

    os.environ.setdefault("OPENAI_API_KEY", "local")
    model = LiteLlm(model=f"openai/{local.model}", api_base=local.base_url, api_key="local")
    agent = LlmAgent(name="bell_county_digest", model=model, instruction=system)
    runner = InMemoryRunner(agent=agent, app_name="meseeks_digest")

    async def go() -> str:
        session = await runner.session_service.create_session(app_name="meseeks_digest", user_id="digest")
        out = []
        async for ev in runner.run_async(user_id="digest", session_id=session.id,
                                         new_message=types.Content(role="user", parts=[types.Part(text=prompt)])):
            if ev.content and ev.content.parts:
                out.extend(p.text for p in ev.content.parts if getattr(p, "text", None))
        return "".join(out).strip()

    return asyncio.run(go())


def run_coders(system: str, prompt: str, log: list[dict] | None = None) -> str | None:
    full = f"{system}\n\n{prompt}"
    for name, argv, timeout in CODERS:
        exe = shutil.which(argv[0])
        if not exe:
            (log if log is not None else []).append({"coder": name, "status": "missing"})
            continue
        try:
            cp = subprocess.run([exe, *argv[1:]], input=full, capture_output=True, text=True,
                                timeout=timeout, env={**os.environ, "CI": "1", "TERM": "dumb"})
            text = cp.stdout.strip()
            if cp.returncode == 0 and len(text) > 80:
                (log if log is not None else []).append({"coder": name, "status": "ok"})
                return text
            (log if log is not None else []).append({"coder": name, "status": f"rc={cp.returncode}", "stderr": cp.stderr[-500:]})
        except subprocess.TimeoutExpired:
            (log if log is not None else []).append({"coder": name, "status": f"timeout {timeout}s"})
    return None


def generate(system: str, prompt: str, log: list[dict] | None = None) -> tuple[str, str]:
    """Return (text, backend_label)."""
    local = discover()
    if local:
        try:
            text = run_adk(local, system, prompt)
            if text:
                return text, f"adk:{local.kind}:{local.base_url}:{local.model}"
            (log if log is not None else []).append({"backend": local.base_url, "status": "empty"})
        except Exception as e:
            (log if log is not None else []).append({"backend": local.base_url, "status": f"error {type(e).__name__}: {e}"[:300]})
    text = run_coders(system, prompt, log)
    if text:
        return text, "coder"
    raise RuntimeError("no model backend produced a digest: " + json.dumps(log or []))
