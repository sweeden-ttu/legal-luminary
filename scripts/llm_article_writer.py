#!/usr/bin/env python3
"""
LLM Article Writer — generates rich, multi-paragraph Jekyll post bodies
using the local Ollama gemma4 model.

Falls back to cleaned raw excerpt if Ollama is unavailable.
Enforces third-person impersonal language per Legal Luminary style guide.
"""

import html
import json
import logging
import re
import urllib.request
import urllib.error

logger = logging.getLogger(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma4:latest"
TIMEOUT_SECONDS = 120  # LLM can be slow on first load


# ---------------------------------------------------------------------------
# HTML / text cleaning
# ---------------------------------------------------------------------------

def strip_html(text: str) -> str:
    """Remove HTML tags, unescape entities, and normalize whitespace."""
    if not text:
        return ""
    # Unescape HTML entities first
    text = html.unescape(text)
    # Remove HTML tags
    text = re.sub(r"<[^>]+>", " ", text)
    # Collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


# ---------------------------------------------------------------------------
# Source Information footer (matches existing post format)
# ---------------------------------------------------------------------------

def _source_footer(source_name: str, source_url: str, date: str) -> str:
    """Generate the ## Source Information block that existing posts use."""
    return (
        f"\n\n## Source Information\n\n"
        f"- **Source**: {source_name}\n"
        f"- **Original URL**: {source_url}\n"
        f"- **Published**: {date}\n"
        f"- **Verified**: {date}\n\n"
        f"---"
    )


# ---------------------------------------------------------------------------
# Ollama LLM integration
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """\
You are a legal news editor for the Central Texas Legal Resources website \
(Legal Luminary). You write concise, factual news summaries for a Bell County, \
Texas audience. Your readers include attorneys, law students, and members \
of the public.

STRICT RULES:
1. Write in THIRD-PERSON IMPERSONAL only. Never use "you", "your", "we", or "our". \
Use "individuals", "residents", "those involved", "the accused", "officials", etc.
2. Write 3-4 short paragraphs (each 2-4 sentences).
3. Be factual — do not invent details. Only summarize what the source material says.
4. Focus on the legal, criminal justice, or community safety angle.
5. Do NOT include any headings, bullet points, or markdown formatting — just paragraphs.
6. Do NOT include a source citation — that is added separately.
7. Do NOT start with the article title or repeat it verbatim.\
"""


def _build_user_prompt(title: str, raw_text: str, source_name: str, date: str) -> str:
    """Build the user prompt for the LLM."""
    cleaned = strip_html(raw_text)
    # Truncate very long text to keep context window reasonable
    if len(cleaned) > 2000:
        cleaned = cleaned[:2000] + "..."
    return (
        f"Summarize this news article for Central Texas readers.\n\n"
        f"TITLE: {title}\n"
        f"SOURCE: {source_name}\n"
        f"DATE: {date}\n\n"
        f"RAW CONTENT:\n{cleaned}"
    )


def _call_ollama(prompt: str) -> str | None:
    """Call the local Ollama API. Returns the response text or None on failure."""
    payload = json.dumps({
        "model": MODEL,
        "prompt": prompt,
        "system": SYSTEM_PROMPT,
        "stream": False,
        "options": {
            "temperature": 0.3,
            "top_p": 0.9,
            "num_predict": 800,
        },
    }).encode("utf-8")

    req = urllib.request.Request(
        OLLAMA_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            return body.get("response", "").strip()
    except urllib.error.URLError as e:
        logger.warning(f"Ollama API unreachable: {e}")
        return None
    except Exception as e:
        logger.warning(f"Ollama API error: {e}")
        return None


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def generate_article_body(
    title: str,
    raw_excerpt: str,
    source_name: str,
    source_url: str,
    date: str,
) -> str:
    """
    Generate a full article body for a Jekyll post.

    Returns multi-paragraph prose + Source Information footer.
    Falls back to cleaned raw excerpt if LLM is unavailable.
    """
    cleaned_excerpt = strip_html(raw_excerpt)

    # Try LLM generation
    user_prompt = _build_user_prompt(title, raw_excerpt, source_name, date)
    llm_body = _call_ollama(user_prompt)

    if llm_body and len(llm_body) > 100:
        # LLM succeeded — use its output
        body = llm_body
        logger.info(f"LLM generated {len(body)} chars for: {title[:60]}")
    else:
        # Fallback — use cleaned excerpt
        body = cleaned_excerpt
        logger.info(f"LLM fallback (cleaned excerpt) for: {title[:60]}")

    # Append the Source Information footer
    body += _source_footer(source_name, source_url, date)

    return body


def generate_excerpt(body: str, max_len: int = 250) -> str:
    """Extract a clean excerpt from the generated body (for frontmatter)."""
    # Remove the Source Information section
    clean = re.split(r"## Source Information", body, maxsplit=1)[0].strip()
    # Take first max_len characters
    if len(clean) > max_len:
        # Try to break at a sentence boundary
        truncated = clean[:max_len]
        last_period = truncated.rfind(".")
        if last_period > max_len // 2:
            truncated = truncated[: last_period + 1]
        return truncated
    return clean
