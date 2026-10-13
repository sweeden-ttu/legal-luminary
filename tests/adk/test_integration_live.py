"""Integration tests against the live web (no model). Run with ``-m integration``."""

from pathlib import Path

import pytest
from legal_luminary_adk import tools, workflows

pytestmark = [pytest.mark.integration, pytest.mark.network]

REPO = Path(__file__).resolve().parents[2]


def test_live_site_home_and_key_pages_load():
    pages = {
        p["url"]: p
        for p in tools.crawl_site("https://legalluminary.com/", max_pages=25)
    }
    assert pages["https://legalluminary.com/"]["classification"] == "ok"
    assert len(pages) == 25


def test_election_page_sources_have_no_dead_links():
    urls = workflows.collect_urls(
        "_pages/texas-ag-race-26\n_pages/housing-act-2026.md\n"
        "_pages/nov-3-2026-ballot-guide.md\n"
        "collections/_candidates/courts/jp/jessica_a_gonzalez.md"
    )
    report = tools.check_links(urls)
    assert report["checked"] > 20
    assert report["dead"] == [], [c["url"] for c in report["dead"]]


def test_official_sources_are_fetchable():
    page = tools.fetch_page("https://www.killeentexas.gov/231/Police")
    assert page["classification"] in ("ok", "redirected"), page.get("status_code")
    assert "police" in page["text"].lower()
