"""Content checks on the Jekyll source that guard against regressions fixed by hand.

Each check names the defect it prevents. None of them touch the network.
"""

from pathlib import Path

import pytest
import yaml

pytestmark = pytest.mark.unit

REPO = Path(__file__).resolve().parents[2]
CANDIDATES = sorted((REPO / "collections" / "_candidates").rglob("*.md"))
AG_PAGES = sorted((REPO / "_pages" / "texas-ag-race-26").glob("*.md"))
ELECTION_PAGES = AG_PAGES + [
    REPO / "_pages" / "housing-act-2026.md",
    REPO / "_pages" / "nov-3-2026-ballot-guide.md",
]


def front_matter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---\n"), f"{path} has no front matter"
    return yaml.safe_load(text.split("---\n", 2)[1]) or {}


@pytest.mark.parametrize("path", CANDIDATES + ELECTION_PAGES, ids=lambda p: p.name)
def test_front_matter_is_valid_yaml(path):
    # An unescaped apostrophe in a single-quoted value broke the Jekyll build once.
    assert isinstance(front_matter(path), dict)


@pytest.mark.parametrize("path", CANDIDATES, ids=lambda p: p.name)
def test_candidate_pages_do_not_use_the_endorsement_layout(path):
    # The site is informational; a candidate page once carried an endorsement badge.
    assert front_matter(path).get("layout") != "candidate-profile-endorsed"


@pytest.mark.parametrize("path", ELECTION_PAGES, ids=lambda p: p.name)
def test_election_pages_cite_sources_and_a_verification_date(path):
    fm = front_matter(path)
    assert fm.get("verified_at"), "verified_at is required"
    assert fm.get("sources"), "at least one source is required"
    for source in fm["sources"]:
        assert str(source["url"]).startswith("https://")


@pytest.mark.parametrize(
    "phrase",
    [
        "insuitable",  # unsourced editorial line removed from a JP profile
        "This preserves strong criticism",  # leftover drafting note in a post
        "Official Support",
    ],
)
def test_known_bad_phrases_are_gone(phrase):
    for path in list(REPO.glob("_posts/*.md")) + CANDIDATES + ELECTION_PAGES:
        assert phrase not in path.read_text(encoding="utf-8"), f"{phrase!r} in {path}"


def test_dev_and_archive_paths_are_hidden_from_search():
    robots = (REPO / "robots.txt").read_text(encoding="utf-8")
    assert "Disallow: /modules/" in robots
    assert "Disallow: /archive/" in robots
    config = yaml.safe_load((REPO / "_config.yml").read_text(encoding="utf-8"))
    hidden = {
        d["scope"].get("path"): d["values"].get("robots") for d in config["defaults"]
    }
    assert hidden.get("modules", "").startswith("noindex")
    assert hidden.get("archive", "").startswith("noindex")
