"""End-to-end test of the research workflow on real Claude and live sources.

Skipped unless the Anthropic SDK can find a credential. Each run makes a few
billed Claude requests. Run with ``-m llm``.
"""

import pytest
from legal_luminary_adk import workflows

from .test_workflows import node_name, run

pytestmark = [pytest.mark.integration, pytest.mark.network, pytest.mark.llm]


def _has_anthropic_credential() -> bool:
    try:
        import anthropic

        client = anthropic.Anthropic()
    except Exception:
        return False
    return any(
        getattr(client, a, None) for a in ("api_key", "auth_token", "credentials")
    )


@pytest.mark.asyncio
@pytest.mark.skipif(not _has_anthropic_credential(), reason="no Anthropic credential")
async def test_research_workflow_returns_a_verified_official_finding(request):
    events = await run(
        workflows.build_research_workflow(),
        "Who is the City of Killeen's chief of police? Start at "
        "https://www.killeentexas.gov/231/Police and cite that page.",
        request.node.name,
    )
    report = [e for e in events if node_name(e) == "render_report" and e.output][
        -1
    ].output
    assert report["verified"], report
    assert any("killeentexas.gov" in f["source_url"] for f in report["verified"])
