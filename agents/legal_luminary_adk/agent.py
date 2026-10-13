"""Entry point for ``adk run`` / ``adk web``: the official-source research workflow.

The model is built lazily by ADK on first request, so importing this module
does not require Anthropic credentials.
"""

from .workflows import build_research_workflow

root_agent = build_research_workflow()
