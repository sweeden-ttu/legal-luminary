"""Client intake: lemmas, dilemmas and the consequences of non-action, per case.

A lemma is a fact a decision rests on, taken from the published notice, with its source and,
where it has one, its deadline. A dilemma is a choice between options; for each option the
brief states what follows on the notice's own terms and how much time is left. Money is
compared only with numbers the client or attorney supplies (property value, payoff, costs);
nothing is estimated. The brief is information for the defendant and an attorney to decide
with, not legal advice, and it does not choose for them.

  python -m meseeks.intake list
  python -m meseeks.intake brief 25DCV352411 [--today 2026-10-15]
  python -m meseeks.intake brief LO-54089-TX --value 310000 --other-costs 4500
  python -m meseeks.intake brief LO-54089-TX --value 310000 --save    # private, never in the repo

Intake answers (--value etc.) are stored only under MESEEKS_INTAKE_DIR
(default ~/.local/share/meseeks/intake, mode 0600), never in _data/ or the site.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import asdict, dataclass, field
from datetime import date, datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CASES = ROOT / "_data" / "meseeks_cases.yml"
INTAKE_DIR = Path(os.environ.get("MESEEKS_INTAKE_DIR", str(Path.home() / ".local" / "share" / "meseeks" / "intake")))

HELP = [
    {"label": "TexasLawHelp.org", "url": "https://texaslawhelp.org"},
    {"label": "Lone Star Legal Aid", "url": "https://www.lonestarlegal.org"},
    {"label": "State Bar of Texas Lawyer Referral", "url": "https://www.texasbar.com/lris"},
    {"label": "HUD-approved housing counseling", "url": "https://www.hud.gov/counseling"},
]


@dataclass
class Lemma:
    id: str
    statement: str
    source: str
    deadline: str | None = None
    days_left: int | None = None


@dataclass
class Option:
    id: str
    action: str
    requires: list[str]
    consequence: str
    by: str | None = None
    days_left: int | None = None
    net: float | None = None          # only when the client supplied numbers
    net_basis: str | None = None


@dataclass
class Brief:
    case: str
    kind: str
    court: str
    today: str
    lemmas: list[Lemma] = field(default_factory=list)
    dilemma: str = ""
    options: list[Option] = field(default_factory=list)
    inaction: str = ""
    clipping: str | None = None
    help: list[dict] = field(default_factory=lambda: list(HELP))
    notice: str = ("Information from the published notice for the defendant and an attorney to decide with; "
                   "not legal advice. Confirm every date with the clerk or the foreclosure commissioner.")


def load_cases(path: Path = CASES) -> dict[str, dict]:
    doc = yaml.safe_load(path.read_text()) or {}
    return {str(c["id"]): c for c in doc.get("cases") or []}


def _d(value) -> date:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    return datetime.fromisoformat(str(value)).date()


def _left(deadline, today: date) -> int:
    return (_d(deadline) - today).days


def _money(x: float) -> str:
    return f"-${-x:,.2f}" if x < 0 else f"${x:,.2f}"


def brief(case_id: str, today: date | None = None, value: float | None = None, payoff: float | None = None,
          other_costs: float = 0.0, cases: dict[str, dict] | None = None) -> Brief:
    cases = cases or load_cases()
    c = cases[case_id]
    today = today or date.today()
    b = Brief(case=case_id, kind=c["kind"], court=c["court"], today=today.isoformat(), clipping=c.get("clipping"))
    pub = ", ".join(_d(p).strftime("%b %-d") for p in c.get("published", []))
    src = f"published notice, Killeen Daily Herald ({pub})"

    if c["kind"] == "citation_by_publication":
        due = c["answer_due"]
        n = _left(due, today)
        b.lemmas = [
            Lemma("L1", f"A suit is pending in the {c['court']}, Cause No. {case_id}, seeking to {c['relief_sought']}.", src),
            Lemma("L2", f"The citation was issued {_d(c['issued']):%B %-d, %Y}; an answer is due by 10:00 AM on the first Monday after 42 days from issuance.", src,
                  _d(due).isoformat(), n),
            Lemma("L3", "If no written answer is filed with the clerk by the deadline, a default judgment may be taken against the defendant.", src + " (Notice to Defendant)"),
            Lemma("L4", "Because service was by publication, a default judgment generally requires the court to appoint an attorney ad litem for the defendant, and a defendant served by publication may have up to two years to seek a new trial (Tex. R. Civ. P. 244, 329). An attorney should confirm how these apply.", "Texas Rules of Civil Procedure"),
        ]
        b.dilemma = "Answer the suit (with counsel or pro se), or let the deadline pass."
        b.options = [
            Option("A", "File a written answer (general denial at minimum) with the Bell County District Clerk.",
                   ["a written answer filed by the deadline", "the cause number"],
                   "The case proceeds on the merits; the defendant can contest the lien and title claims, raise defenses and counterclaims, and negotiate.",
                   _d(due).isoformat(), n),
            Option("B", "Retain an attorney (hourly, legal aid, or the contingency template) to answer and defend.",
                   ["an attorney engaged before the deadline", "documents: deed, note, payment history, heirship facts"],
                   "Same as A, with representation; an attorney can also seek more time by agreement or motion.",
                   _d(due).isoformat(), n),
            Option("C", "Take no action.", [],
                   "After the deadline the plaintiff may seek a default judgment granting the relief it asks for (here: " + c["relief_sought"] + "). Post-judgment remedies may exist but are narrower and slower than answering."),
        ]
        b.inaction = (f"{n} day(s) remain until the answer deadline. Doing nothing does not stop the case; it lets the plaintiff ask "
                      "for judgment without the defendant's side being heard." if n >= 0 else
                      f"The answer deadline passed {-n} day(s) ago. An answer filed before a default judgment is signed is generally still considered; speak to an attorney now.")

    elif c["kind"] == "hud_nonjudicial_foreclosure":
        sale, reinstate = c["sale"], c["reinstate_by"]
        ns, nr = _left(sale, today), _left(reinstate, today)
        amt = float(c["reinstatement_amount"])
        b.lemmas = [
            Lemma("L1", "HUD holds the deed of trust and its foreclosure commissioner has scheduled a nonjudicial sale under the Single Family Mortgage Foreclosure Act of 1994 (12 U.S.C. 3751 et seq.); no court case is required.", src),
            Lemma("L2", f"Sale: {_d(sale):%A, %B %-d, %Y}, {c['sale_window']}.", src, _d(sale).isoformat(), ns),
            Lemma("L3", f"The loan may be reinstated before the sale by paying {_money(amt)} as of {_d(reinstate):%B %-d, %Y}, plus other amounts due, advertising, commissioner fees and costs.", src,
                  _d(reinstate).isoformat(), nr),
            Lemma("L4", "There is no right of redemption, or right of possession based on redemption, after the sale.", src),
            Lemma("L5", f"HUD will bid {_money(float(c['hud_bid']))}; other bidders need a {c['deposit_pct']}% deposit by certified or cashier's check.", src),
            Lemma("L6", "Transfers of residential real property to entity or trust buyers are subject to FinCEN reporting effective March 1, 2026; the trustee may require that information from bidders.", src + " (Notice to Potential Bidders)"),
        ]
        b.dilemma = "Pay to reinstate before the sale, pursue another route with counsel or a housing counselor, or let the sale go forward."
        reinstate_opt = Option("A", "Reinstate the loan by paying the full reinstatement amount to the foreclosure commissioner.",
                               ["certified or cashier's check, or an approved application to cancel the sale", "a current payoff statement from the commissioner"],
                               "The sale is cancelled and the loan continues.", _d(reinstate).isoformat(), nr)
        sale_opt = Option("C", "Take no action.", [],
                          f"The property is sold at auction on {_d(sale):%B %-d}; with no redemption right, title passes to the buyer (HUD, if no higher bid) and the occupants' right to stay ends.",
                          _d(sale).isoformat(), ns)
        if value is not None:
            pay = payoff if payoff is not None else amt
            reinstate_opt.net = round(value - pay - other_costs, 2)
            reinstate_opt.net_basis = (f"position after keeping the property: client-supplied value {_money(value)} − payment {_money(pay)}"
                                       f" − other costs {_money(other_costs)}")
            sale_opt.net = round(max(0.0, value - pay), 2)
            sale_opt.net_basis = (f"equity at risk at the sale: client-supplied value {_money(value)} − amount owed {_money(pay)}; "
                                  "whether any of it returns to the borrower depends on the sale price and on the law; ask counsel")
        b.options = [
            reinstate_opt,
            Option("B", "Engage an attorney or a HUD-approved housing counselor about alternatives (loss mitigation, a payment arrangement, a sale before foreclosure, or other relief).",
                   ["contact before the sale date", "loan documents and the notice"],
                   "Any alternative must be agreed or ordered before the sale; this brief does not assume one is available.",
                   _d(sale).isoformat(), ns),
            sale_opt,
        ]
        b.inaction = (f"{nr} day(s) remain to reinstate and {ns} day(s) until the sale. After the sale there is no redemption." if ns >= 0
                      else "The sale date has passed; there is no right of redemption. Speak to an attorney about any remaining remedies.")
    else:
        raise ValueError(f"unknown case kind {c['kind']!r}")
    b.lemmas.append(road_act_lemma(today))
    return b


ROAD_ACT_SOURCES = (
    "21st Century ROAD to Housing Act, P.L. 119-101, Title X, sec. 1001 (enacted July 11, 2026); summaries: "
    "Mayer Brown (July 2026), CRS R49354"
)


def road_act_lemma(today: date) -> Lemma:
    """The new federal law, stated only as far as the sources go."""
    effective = date(2027, 1, 7)
    return Lemma(
        "L-ROAD",
        "Sec. 1001 of the 21st Century ROAD to Housing Act ('Homes are for people, not corporations') bars large "
        "institutional investors (investment control of 350+ single-family homes) from buying single-family homes, "
        "with a civil penalty of up to $1,000,000 per violation or three times the purchase price, whichever is greater. "
        "It takes effect about January 7, 2027, is not retroactive, excepts repossession and foreclosure or loss-mitigation "
        "acquisitions by lenders and servicers, and the summaries describe no private right of action. On these facts it "
        "does not by itself give a defendant or borrower a claim; an attorney should confirm how it bears on the case.",
        ROAD_ACT_SOURCES, effective.isoformat(), (effective - today).days)


def save(b: Brief, client_answers: dict, base: Path = INTAKE_DIR) -> Path:
    base.mkdir(parents=True, exist_ok=True)
    os.chmod(base, 0o700)
    p = base / f"{b.case}-{b.today}.json"
    p.write_text(json.dumps({"brief": asdict(b), "client_answers": client_answers}, indent=2))
    os.chmod(p, 0o600)
    return p


def render(b: Brief) -> str:
    out = [f"Case {b.case} — {b.court}", f"As of {b.today}", "", "Lemmas"]
    for lm in b.lemmas:
        tail = f"  [deadline {lm.deadline}, {lm.days_left} day(s) left]" if lm.deadline else ""
        out.append(f"  {lm.id}. {lm.statement}{tail}\n      source: {lm.source}")
    out += ["", f"Dilemma: {b.dilemma}"]
    for o in b.options:
        when = f" — by {o.by} ({o.days_left} day(s))" if o.by else ""
        out.append(f"  {o.id}. {o.action}{when}\n      consequence: {o.consequence}")
        if o.net is not None:
            out.append(f"      on the client's numbers: {_money(o.net)} ({o.net_basis})")
    out += ["", f"Non-action: {b.inaction}", "", b.notice]
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["list", "brief"])
    ap.add_argument("case", nargs="?")
    ap.add_argument("--today")
    ap.add_argument("--value", type=float, help="client-supplied property value")
    ap.add_argument("--payoff", type=float, help="client-supplied reinstatement / payoff quote")
    ap.add_argument("--other-costs", type=float, default=0.0)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--save", action="store_true", help="store the brief and answers privately under MESEEKS_INTAKE_DIR")
    a = ap.parse_args(argv)
    if a.cmd == "list":
        for cid, c in load_cases().items():
            print(f"{cid}\t{c['kind']}\t{c['court']}")  # noqa: T201
        return 0
    b = brief(a.case, _d(a.today) if a.today else None, a.value, a.payoff, a.other_costs)
    print(json.dumps(asdict(b), indent=2) if a.json else render(b))  # noqa: T201
    if a.save:
        print(f"\nsaved privately: {save(b, {'value': a.value, 'payoff': a.payoff, 'other_costs': a.other_costs})}")  # noqa: T201
    return 0


if __name__ == "__main__":
    sys.exit(main())
