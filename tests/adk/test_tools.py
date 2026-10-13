"""Unit tests for the deterministic web tools (no network)."""

import pytest
from legal_luminary_adk import tools

from .conftest import html, make_pdf

pytestmark = pytest.mark.unit


@pytest.mark.parametrize(
    ("status", "final", "expected"),
    [
        (200, "https://a.gov/x", "ok"),
        (200, "https://a.gov/x/", "ok"),
        (200, "https://www.a.gov/x", "ok"),
        (200, "https://a.gov/moved", "redirected"),
        (202, "https://a.gov/x", "unverified"),
        (403, "https://a.gov/x", "blocked"),
        (406, "https://a.gov/x", "blocked"),
        (429, "https://a.gov/x", "blocked"),
        (404, "https://a.gov/x", "dead"),
        (410, "https://a.gov/x", "dead"),
        (502, "https://a.gov/x", "server_error"),
        (None, None, "unreachable"),
    ],
)
def test_classify(status, final, expected):
    assert tools.classify(status, "https://a.gov/x", final) == expected


def test_normalize_url_strips_fragment_and_punctuation():
    assert tools.normalize_url(" https://a.gov/p#section. ") == "https://a.gov/p"
    assert tools.normalize_url("https://a.gov/p.") == "https://a.gov/p"


def test_extract_urls_keeps_balanced_parentheses():
    # Regression: an earlier ad-hoc regex cut this URL at "(Texas".
    md = "See [Ballotpedia](https://ballotpedia.org/Nathan_Johnson_(Texas)) for more."
    assert tools.extract_urls(md) == ["https://ballotpedia.org/Nathan_Johnson_(Texas)"]


def test_extract_urls_reads_front_matter_and_keeps_prefix_urls():
    md = (
        "---\nsources:\n  - url: https://kdhnews.com/\n"
        '  - url: "https://kdhnews.com/news/a.html"\n---\n'
        "Body (https://www.sos.texas.gov/elections/index.shtml).\n"
    )
    assert tools.extract_urls(md) == [
        "https://kdhnews.com/",
        "https://kdhnews.com/news/a.html",
        "https://www.sos.texas.gov/elections/index.shtml",
    ]


@pytest.mark.parametrize(
    ("url", "allowed"),
    [
        ("https://www.killeentexas.gov/231/Police", True),
        ("https://bellcountytx.com/x", True),
        ("https://evil-killeentexas.gov.example.com/", False),
        ("https://example.com/", False),
    ],
)
def test_is_allowed(url, allowed):
    assert tools.is_allowed(url) is allowed


def test_parse_html_skips_scripts_and_resolves_links():
    page = tools.parse_html(
        html("Police | Killeen", "Chief of Police", ("/231/Police", "mailto:x@y.z")),
        "https://www.killeentexas.gov/",
    )
    assert page["title"] == "Police | Killeen"
    assert "hidden" not in page["text"]
    assert page["links"] == [
        {"url": "https://www.killeentexas.gov/231/Police", "text": "/231/Police"}
    ]


def test_parse_html_prefers_main_and_lists_content_links_first():
    page = tools.parse_html(
        "<body><nav><a href='/menu'>Menu</a> Departments</nav>"
        "<main><h1>Elections</h1><a href='/ballot.pdf'>Sample ballot</a></main>"
        "<footer>Copyright</footer></body>",
        "https://www.bellcountytx.com/",
    )
    assert page["text"] == "Elections Sample ballot"
    assert [link["text"] for link in page["links"]] == ["Sample ballot", "Menu"]
    assert "Departments" in page["all_text"]


def test_parse_html_without_main_drops_nav_text():
    page = tools.parse_html(
        "<body><nav>Menu</nav><div>Charter election notice</div></body>",
        "https://www.killeentexas.gov/",
    )
    assert page["text"] == "Charter election notice"


@pytest.mark.parametrize(
    ("quote", "expected"),
    [
        ("chief of police", True),
        ("“Chief of Police”", False),  # quotation marks are not on the page
        ("Pedro Lopez ... Chief of Police", True),
        ("Chief of Police ... Pedro Lopez", False),  # order matters
        ("Interim Chief", False),
        ("", False),
    ],
)
def test_quote_in_text(quote, expected):
    assert tools.quote_in_text(quote, "Pedro  Lopez, Chief of Police") is expected


def test_check_links_groups_outcomes(mock_web):
    mock_web.update(
        {
            "https://a.gov/ok": (200, html("ok", "ok"), None),
            "https://a.gov/old": (301, "", "https://a.gov/new"),
            "https://a.gov/new": (200, html("new", "new"), None),
            "https://ballotpedia.org/X": (202, "", None),
            "https://a.gov/forbidden": (403, "", None),
        }
    )
    report = tools.check_links(
        [
            "https://a.gov/ok",
            "https://a.gov/ok#frag",
            "https://a.gov/old",
            "https://ballotpedia.org/X",
            "https://a.gov/forbidden",
            "https://a.gov/missing",
        ]
    )
    assert report["checked"] == 5
    assert [c["url"] for c in report["dead"]] == ["https://a.gov/missing"]
    assert [c["url"] for c in report["redirected"]] == ["https://a.gov/old"]
    assert {c["classification"] for c in report["needs_manual_check"]} == {
        "unverified",
        "blocked",
    }


def test_fetch_page_refuses_hosts_off_the_allowlist(mock_web):
    result = tools.fetch_page("https://example.com/")
    assert result["classification"] == "not_allowed"
    assert result["text"] == ""


def test_fetch_page_truncates_long_text(mock_web, monkeypatch):
    monkeypatch.setattr(tools.config, "MAX_PAGE_CHARS", 10)
    mock_web["https://www.killeentexas.gov/231/Police"] = (
        200,
        html("Police", "Pedro Lopez, Chief of Police"),
        None,
    )
    result = tools.fetch_page("https://www.killeentexas.gov/231/Police")
    assert result["classification"] == "ok"
    assert result["text"] == "Pedro Lope"
    assert result["truncated"] is True


def test_verify_quote(mock_web):
    mock_web["https://www.killeentexas.gov/231/Police"] = (
        200,
        html("Police", "Pedro Lopez, Chief of Police"),
        None,
    )
    ok = tools.verify_quote(
        "https://www.killeentexas.gov/231/Police", "Chief of Police"
    )
    bad = tools.verify_quote("https://www.killeentexas.gov/231/Police", "interim chief")
    gone = tools.verify_quote("https://www.killeentexas.gov/999/Gone", "anything")
    assert ok["verified"] is True
    assert bad["verified"] is False
    assert gone["verified"] is False and gone["check"]["classification"] == "dead"


def test_crawl_site_seeds_from_sitemap_and_follows_links(mock_web):
    mock_web.update(
        {
            "https://legalluminary.com/sitemap.xml": (
                200,
                "<urlset><url><loc>https://legalluminary.com/a/</loc></url></urlset>",
                None,
            ),
            "https://legalluminary.com/": (
                200,
                html("Home", "home", ("/a/", "/b/", "/logo.png", "https://other.org/")),
                None,
            ),
            "https://legalluminary.com/a/": (200, html("A", "a"), None),
        }
    )
    pages = {p["url"]: p for p in tools.crawl_site("https://legalluminary.com/")}
    assert set(pages) == {
        "https://legalluminary.com/",
        "https://legalluminary.com/a/",
        "https://legalluminary.com/b/",
    }
    assert pages["https://legalluminary.com/a/"]["in_sitemap"] is True
    assert pages["https://legalluminary.com/b/"]["classification"] == "dead"


def test_collect_source_urls_reads_directories(tmp_path):
    (tmp_path / "one.md").write_text("[a](https://a.gov/1)", encoding="utf-8")
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "two.md").write_text("https://a.gov/2 and [a](https://a.gov/1)")
    assert tools.collect_source_urls([str(tmp_path)]) == [
        "https://a.gov/1",
        "https://a.gov/2",
    ]


BALLOT = "https://www.bellcountytx.com/elections/Sample/SAMPLE_401KIL.pdf"


def test_fetch_document_reads_pdf_text(mock_web):
    url = BALLOT + "?t=202609171627090"  # the county appends a cache-buster
    mock_web[url] = (200, make_pdf("Justice of the Peace Precinct 4 Place 2"), None)
    doc = tools.fetch_document(url)
    assert doc["classification"] == "ok"
    assert doc["pages"] == 1
    assert doc["text"] == "Justice of the Peace Precinct 4 Place 2"


def test_fetch_document_refuses_html_oversize_and_off_allowlist(mock_web, monkeypatch):
    mock_web["https://www.bellcountytx.com/page"] = (200, html("x", "x"), None)
    assert (
        tools.fetch_document("https://www.bellcountytx.com/page")["error"]
        == "not a PDF"
    )
    assert (
        tools.fetch_document("https://example.com/a.pdf")["classification"]
        == "not_allowed"
    )
    monkeypatch.setattr(tools.config, "MAX_DOC_BYTES", 100)
    mock_web[BALLOT] = (200, make_pdf("x" * 200), None)
    assert "size limit" in tools.fetch_document(BALLOT)["error"]


def test_verify_quote_reads_pdfs(mock_web):
    mock_web[BALLOT] = (200, make_pdf("Proposition A Charter Amendment"), None)
    assert tools.verify_quote(BALLOT, "proposition a")["verified"] is True
    assert tools.verify_quote(BALLOT, "proposition z")["verified"] is False
