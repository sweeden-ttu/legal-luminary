"""Runtime configuration for the Legal Luminary ADK agents.

Every value can be overridden with an environment variable so CI and local
runs can share one code path.
"""

from __future__ import annotations

import os

from google.adk.models.anthropic_llm import AnthropicGenerateContentConfig, AnthropicLlm

#: Claude model used by every LLM agent. Override with LL_ADK_MODEL.
MODEL_ID = os.environ.get("LL_ADK_MODEL", "claude-opus-5-5")

#: Reasoning effort. Claude Opus 5.5 defaults to "medium"; source validation
#: for election content is accuracy-sensitive, so default to "high".
EFFORT = os.environ.get("LL_ADK_EFFORT", "high")

#: Per-response output ceiling (non-streaming requests).
MAX_TOKENS = int(os.environ.get("LL_ADK_MAX_TOKENS", "16000"))

#: Seconds before an HTTP fetch is abandoned.
HTTP_TIMEOUT = float(os.environ.get("LL_ADK_HTTP_TIMEOUT", "20"))

#: Largest document (PDF) the research agent may download, in bytes.
MAX_DOC_BYTES = int(os.environ.get("LL_ADK_MAX_DOC_BYTES", str(15 * 1024 * 1024)))

#: Characters of page text handed to the model per fetch.
MAX_PAGE_CHARS = int(os.environ.get("LL_ADK_MAX_PAGE_CHARS", "20000"))

USER_AGENT = "LegalLuminaryAudit/1.0 (+https://legalluminary.com/about/)"

#: Hosts the research agent may fetch. Government and court sites are primary
#: sources; the news and reference sites are secondary and must be labeled so.
PRIMARY_DOMAINS = (
    "killeentexas.gov",
    "bellcountytx.com",
    "sos.state.tx.us",
    "sos.texas.gov",
    "txcourts.gov",
    "scjc.texas.gov",
    "capitol.texas.gov",
    "senate.texas.gov",
    "house.texas.gov",
    "ethics.state.tx.us",
    "clerk.house.gov",
    "congress.gov",
    "govinfo.gov",
    "texasattorneygeneral.gov",
)
SECONDARY_DOMAINS = (
    "legalluminary.com",
    "kdhnews.com",
    "tdtnews.com",
    "texastribune.org",
    "ballotpedia.org",
    "kcentv.com",
    "kwtx.com",
    "kxxv.com",
)
ALLOWED_DOMAINS = PRIMARY_DOMAINS + SECONDARY_DOMAINS


def claude_model() -> AnthropicLlm:
    """Return the Claude model wrapper used by every LLM agent.

    ``AnthropicLlm`` calls the first-party Anthropic API and lets the Anthropic
    SDK resolve credentials (``ANTHROPIC_API_KEY`` or a signed-in profile).
    """
    return AnthropicLlm(model=MODEL_ID, max_tokens=MAX_TOKENS)


def claude_config() -> AnthropicGenerateContentConfig:
    """Return generation settings: explicit effort, adaptive thinking by default."""
    return AnthropicGenerateContentConfig(effort=EFFORT)
