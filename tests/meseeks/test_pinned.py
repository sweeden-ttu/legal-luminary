"""Thread -1 stays on top until removed; everything else is most recently updated first."""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "agents"))

from meseeks.run import expire, order_posts  # noqa: E402


def _p(pid, received, **kw):
    return {"id": pid, "category": kw.pop("category", "notice"), "received": received, **kw}


def test_pinned_first_then_most_recently_updated():
    posts = [
        _p("old", "2026-01-01T00:00:00Z"),
        _p("pin", "2025-12-01T00:00:00Z", pinned=True, thread=-1),
        _p("new", "2026-10-01T00:00:00Z"),
        _p("bumped", "2026-02-01T00:00:00Z", updated="2026-10-10T00:00:00Z"),
    ]
    assert [p["id"] for p in order_posts(posts)] == ["pin", "bumped", "new", "old"]


def test_pinned_threads_sorted_by_thread_number():
    posts = [_p("b", "2026-10-01T00:00:00Z", pinned=True, thread=0),
             _p("a", "2026-01-01T00:00:00Z", pinned=True, thread=-1),
             _p("c", "2026-10-02T00:00:00Z")]
    assert [p["id"] for p in order_posts(posts)] == ["a", "b", "c"]


def test_answer_bumps_its_question_thread():
    posts = [_p("q", "2026-09-01T00:00:00Z", category="question"),
             _p("n", "2026-09-15T00:00:00Z"),
             _p("ans", "2026-10-01T00:00:00Z", category="answer", in_reply_to="q")]
    ordered = order_posts(posts)
    q = next(p for p in ordered if p["id"] == "q")
    assert q["updated"] == "2026-10-01T00:00:00Z"
    assert [p["id"] for p in ordered].index("q") < [p["id"] for p in ordered].index("n")


def test_updated_defaults_to_received_and_never_goes_backwards():
    (p,) = order_posts([_p("x", "2026-10-01T00:00:00Z", updated="2026-01-01T00:00:00Z")])
    assert p["updated"] == "2026-10-01T00:00:00Z"


def test_pinned_post_survives_retention():
    data = {"retention_days": 60, "posts": [
        _p("pin", "2025-01-01T00:00:00Z", pinned=True, thread=-1),
        _p("stale", "2025-01-01T00:00:00Z"),
        _p("fresh", "2026-10-01T00:00:00Z")]}
    assert expire(data, datetime(2026, 10, 15, tzinfo=timezone.utc)) == 1
    assert {p["id"] for p in data["posts"]} == {"pin", "fresh"}


def test_site_data_has_thread_minus_one_on_top():
    data = json.loads((ROOT / "_data" / "meseeks.json").read_text())
    top = data["posts"][0]
    assert top["pinned"] is True and top["thread"] == -1
    assert "Pro Se" in top["title"] and any("oscar.uscourts.gov" in link["url"] for link in top["links"])
    assert data["posts"] == order_posts([dict(p) for p in data["posts"]])
