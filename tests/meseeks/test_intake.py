"""Client intake briefs: lemmas from the notices, dilemmas, and the consequences of non-action."""
import json
import os
import stat
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "agents"))

from meseeks import intake  # noqa: E402

TODAY = date(2026, 10, 15)


def test_cases_carry_no_party_names_or_property_addresses():
    text = (Path(__file__).resolve().parents[2] / "_data" / "meseeks_cases.yml").read_text().lower()
    for word in ("barrow", "watkins", "hays", "hinchman", "cook", "connell", "7th st", "avenue r"):
        assert word not in text


def test_citation_brief_counts_down_to_the_answer_deadline():
    b = intake.brief("25DCV352411", TODAY)
    l2 = next(x for x in b.lemmas if x.id == "L2")
    assert l2.deadline == "2026-10-26" and l2.days_left == 11
    assert [o.id for o in b.options] == ["A", "B", "C"] and "default judgment" in b.options[2].consequence
    assert "11 day(s)" in b.inaction
    late = intake.brief("25DCV352411", date(2026, 10, 30))
    assert "passed 4 day(s) ago" in late.inaction


def test_hud_brief_reinstatement_sale_and_no_redemption():
    b = intake.brief("LO-54089-TX", TODAY)
    ids = {x.id: x for x in b.lemmas}
    assert ids["L3"].deadline == "2026-11-02" and ids["L3"].days_left == 18
    assert ids["L2"].deadline == "2026-11-03" and "no right of redemption" in ids["L4"].statement.lower()
    assert all(o.net is None for o in b.options)          # no money comparison without client numbers


def test_money_only_from_client_numbers():
    b = intake.brief("LO-54089-TX", TODAY, value=310000, other_costs=4500)
    a, c = b.options[0], b.options[2]
    assert a.net == round(310000 - 260235.45 - 4500, 2) and "client-supplied" in a.net_basis
    assert c.net == round(310000 - 260235.45, 2) and "equity at risk" in c.net_basis
    under = intake.brief("LO-54089-TX", TODAY, value=200000)
    assert under.options[2].net == 0.0                     # no equity to lose when underwater


def test_save_is_private(tmp_path):
    b = intake.brief("26DCV360297", TODAY)
    p = intake.save(b, {"value": 1}, base=tmp_path / "intake")
    assert stat.S_IMODE(os.stat(p).st_mode) == 0o600 and stat.S_IMODE(os.stat(p.parent).st_mode) == 0o700
    assert json.loads(p.read_text())["brief"]["case"] == "26DCV360297"
    assert "legal-luminary" not in str(p.resolve()) or "tmp" in str(p.resolve())
