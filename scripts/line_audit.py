#!/usr/bin/env python3
"""Line-by-line verification walker for legalluminary.com.

The site owner's rule: every line of the site is checked in order; a line with a
factual claim either gets a public source or is removed. This script keeps the
pointer (which page, which line) in .review/line-audit-state.json and the running
log in .review/line-audit-log.md so that a fresh session can resume exactly where
the last one stopped.

Usage:
  scripts/line_audit.py pages            # print the ordered page inventory
  scripts/line_audit.py next             # show the next line that carries a claim
  scripts/line_audit.py record --verdict KEPT|CORRECTED|REMOVED [--source URL] [--note TEXT]
                                         # log the verdict for the line last shown by `next`
                                         # and advance (REMOVED keeps the same line number,
                                         # because the following line has moved up)
  scripts/line_audit.py status           # where the walk stands

Page order: home page, then the pages in the site navigation, then the court tier
pages, then every judge profile (statewide, appeals, district, county, JP, associate,
senior), then the other candidate profiles, then the remaining _pages, then _posts.
"""
import argparse, glob, json, os, re, sys, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(ROOT, ".review", "line-audit-state.json")
LOG = os.path.join(ROOT, ".review", "line-audit-log.md")

def page_order():
    pages = ["_pages/frontpage.md", "_pages/judicial-officers.md",
             "_pages/courts/statewide.md", "_pages/courts/appeals.md", "_pages/courts/district.md",
             "_pages/courts/county.md", "_pages/courts/jp.md", "_pages/court-directory.md",
             "_pages/nov-3-2026-ballot-guide.md", "_pages/run-for-judge.md", "_pages/elections.md",
             "_pages/attorneys.md", "_pages/legal-news.md", "_pages/about.md", "_pages/advertise.md",
             "_pages/corrections.md", "_pages/methodology.md"]
    for tier in ["appellate", "district", "county", "jp", "associate", "senior"]:
        pages += sorted(glob.glob(f"collections/_candidates/courts/{tier}/*.md", root_dir=ROOT))
    pages += sorted(glob.glob("collections/_candidates/courts/*.md", root_dir=ROOT))
    pages += sorted(glob.glob("collections/_candidates/texas/**/*.md", root_dir=ROOT, recursive=True))
    pages += sorted(p for p in glob.glob("_pages/**/*.md", root_dir=ROOT, recursive=True) if p not in pages)
    pages += sorted(glob.glob("_posts/*.md", root_dir=ROOT))
    seen, out = set(), []
    for p in pages:
        if p not in seen and os.path.exists(os.path.join(ROOT, p)):
            seen.add(p); out.append(p)
    return out

# front-matter keys whose values are prose that can carry claims
PROSE_KEYS = ("profile_summary", "credentials", "professional_history", "notes", "description",
              "hero_subtitle", "excerpt", "news_excerpt", "election_notes", "listing_status")
STRUCT_RE = re.compile(r"^\s*(---|layout:|title:|hero_title:|permalink:|candidate_slug:|headshot:|campaign_website:|official_profile:|"
                       r"incumbent:|election_status:|office_up_for_election:|court_group:|seat:|ballot_order:|"
                       r"category:|categories:|date:|verified_at:|hero:|article_feed:|sources:|- title:|  publisher:|"
                       r"  url:|  date:|  accessed:|source_url:|source_name:|source:|original_source_url:|city:|"
                       r"author:|author_url:|court_contact:|election_info:|  [a-z_]+: *(\(|\d|P\.O|[A-Z0-9@]|null)|\{%|\{\{|</?[a-z]+[^>]*>\s*$|#+ |\s*$)")

def is_claim_line(line):
    s = line.strip()
    if not s or STRUCT_RE.match(line):
        return False
    words = re.findall(r"[A-Za-z]{2,}", re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s))
    return len(words) >= 3

def load_state():
    if os.path.exists(STATE):
        return json.load(open(STATE))
    return {"page_index": 0, "line_no": 1, "started": datetime.date.today().isoformat(), "checked": 0, "removed": 0, "corrected": 0, "kept": 0}

def save_state(st):
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    json.dump(st, open(STATE, "w"), indent=2)

def current(st, pages):
    """Advance past non-claim lines and empty pages; return (page, line_no, text) or None when done."""
    while st["page_index"] < len(pages):
        page = pages[st["page_index"]]
        lines = open(os.path.join(ROOT, page), encoding="utf-8", errors="ignore").read().splitlines()
        n = st["line_no"]
        while n <= len(lines) and not is_claim_line(lines[n - 1]):
            n += 1
        if n <= len(lines):
            st["line_no"] = n
            return page, n, lines[n - 1]
        st["page_index"] += 1
        st["line_no"] = 1
    return None

def cmd_next(args):
    pages = page_order(); st = load_state()
    cur = current(st, pages); save_state(st)
    if not cur:
        print("DONE: every page has been walked. Reset .review/line-audit-state.json to start another pass."); return
    page, n, text = cur
    print(f"PAGE {st['page_index']+1}/{len(pages)}: {page}\nLINE {n}:\n{text}\n")
    print("Context (3 lines before/after):")
    lines = open(os.path.join(ROOT, page), encoding="utf-8", errors="ignore").read().splitlines()
    for i in range(max(1, n - 3), min(len(lines), n + 3) + 1):
        print(f"{'>>' if i == n else '  '} {i:4d}  {lines[i-1][:200]}")

def cmd_record(args):
    pages = page_order(); st = load_state()
    cur = current(st, pages)
    if not cur:
        print("Nothing to record; walk is complete."); return
    page, n, text = cur
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    new = not os.path.exists(LOG)
    with open(LOG, "a") as f:
        if new:
            f.write("# Line-by-line audit log\n\n| When (UTC) | Page | Line | Verdict | Source | Note | Text |\n|---|---|---|---|---|---|---|\n")
        esc = lambda s: (s or "").replace("|", "\\|").replace("\n", " ")
        f.write(f"| {datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='minutes')} | {page} | {n} | {args.verdict} | {esc(args.source)} | {esc(args.note)} | {esc(text[:160])} |\n")
    st["checked"] += 1
    st[args.verdict.lower()] = st.get(args.verdict.lower(), 0) + 1
    if args.verdict != "REMOVED":
        st["line_no"] = n + 1
    save_state(st)
    print(f"Recorded {args.verdict} for {page}:{n}. Next: run `next`.")

def cmd_status(args):
    pages = page_order(); st = load_state()
    print(json.dumps(st, indent=2)); print(f"pages in walk: {len(pages)}")

def cmd_pages(args):
    for i, p in enumerate(page_order(), 1): print(f"{i:4d}  {p}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("next"); sub.add_parser("status"); sub.add_parser("pages")
    r = sub.add_parser("record"); r.add_argument("--verdict", required=True, choices=["KEPT", "CORRECTED", "REMOVED"])
    r.add_argument("--source", default=""); r.add_argument("--note", default="")
    a = ap.parse_args(); {"next": cmd_next, "record": cmd_record, "status": cmd_status, "pages": cmd_pages}[a.cmd](a)
