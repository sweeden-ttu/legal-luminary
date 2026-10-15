"""Optional Claude classifier. Falls back to rules when no credential is present.
Returns (category | None, confidence). The result is advisory: guardrails.enforce decides."""
from __future__ import annotations

import json
import os

from .guardrails import CATEGORIES, Inbound, rule_classify
from .prompts import get as get_prompt


def classify(msg: Inbound) -> tuple[str | None, float]:
    if not os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("MESEEKS_RULES_ONLY"):
        return rule_classify(msg)
    try:
        import anthropic
    except ImportError:
        return rule_classify(msg)
    client = anthropic.Anthropic()
    model = os.environ.get("LL_ADK_MODEL", "claude-sonnet-5-5")
    user = f"Subject: {msg.subject}\nIn-Reply-To: {msg.in_reply_to or ''}\n\n{msg.body[:6000]}"
    try:
        resp = client.messages.create(
            model=model, max_tokens=200, system=get_prompt("meseeks.classifier").text,
            messages=[{"role": "user", "content": user}],
        )
        text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")
        data = json.loads(text[text.find("{"): text.rfind("}") + 1])
        cat = data.get("category")
        conf = float(data.get("confidence", 0))
        if cat not in CATEGORIES:
            return None, 0.0
        rule_cat, rule_conf = rule_classify(msg)
        if rule_cat and rule_cat != cat:
            conf = min(conf, 0.6)
        return cat, round(conf, 2)
    except Exception:
        return rule_classify(msg)
