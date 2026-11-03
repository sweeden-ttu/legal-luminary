# Verification rules for legalluminary.com judge profiles

Site owner's instruction (verbatim): "VERIFY AND VALIDATE THE CLAIMS — OR REMOVE THEM. DO NOT PUBLISH ANYTHING THAT LACKS SOURCE OR EVIDENCE."

Background: on 2026-06-09 most profile prose was mass-written by `generate_dossiers.py` (literal strings, no research, no sources). Treat every sentence in every profile as unverified until you have personally confirmed it.

## The standard
1. **A claim may stay only if you have opened a public web page (WebFetch, or a WebSearch result whose snippet contains the fact) that states it.** You must have seen the supporting text yourself in this session. Recognition from memory is not a source.
2. **Every kept factual sentence carries an inline citation** in the site's existing format: `... sentence ([Source Name](https://full.url/...))`. Short source names: `Killeen Daily Herald` or `KDH`, `Office of the Governor`, `Ballotpedia`, `Texas Courts`, `Bell County`, `Texas Lawyer`, etc.
3. **Anything you cannot source is deleted.** Not softened, not hedged — deleted. This includes:
   - "J.D., accredited law school" and any education/bar/membership line without a source
   - generic docket/jurisdiction descriptions ("presides over a wide-ranging docket…", "charges juries…")
   - characterizations ("known for", "reputation for", "busy docket", "thousands of cases", "committed to", "emphasizes")
   - party affiliation unless a primary-ballot, filing, or news source gives it (set `party:` to `null` if unsourced)
   - dates (appointment, swearing-in, election, term expiry) unless a source gives the date
   - `odyssey_statistics`, `odyssey_results_placeholder`, `rubber_stamp`, `days_until_election` — remove these keys entirely
   - the `credentials` and `professional_history` blocks: rebuild from sourced facts only, each item followed by its cite; if nothing is sourced, set the field to an empty string `''`
4. **Re-verify existing citations.** A link already on the page is not proof: open it and confirm it says what the sentence says. If the page is unreachable or does not support the claim, the claim goes (or gets a different source you did find).
5. **Never fabricate or guess a URL.** Cite only URLs returned by WebSearch or successfully opened by WebFetch, or the official-page evidence files described below.
6. Quote sparingly: at most one quote under 15 words per source, and only when the exact words matter (e.g. a court's own wording). Paraphrase otherwise.
7. Do not add opinion, analysis, or context the sources do not state. The profile may end up short. Short and sourced beats long and invented.

## Official-page evidence (already fetched today from the user's machine)
`/home/claude/ll/work/.review/evidence/<slug>.txt` holds today's text of each profile's `official_profile` page on bellcountytx.com (that site blocks this container, so do not try to fetch it; the file is the evidence). It gives: judge's name as listed, court, coordinator/reporter names, phone, fax, address. Cite it as `([Bell County](<the SOURCE_URL on line 1>))`. Update `court_contact` to match the file exactly; remove any contact field the file does not support.
Also: `_elected_officials.txt`, `_district_courts_index.txt`, `_county_courts_index.txt` (mostly empty/unhelpful).

## Good sources to look for
- gov.texas.gov appointment press releases ("Governor Abbott Appoints X To Nth Judicial District Court")
- Killeen Daily Herald (kdhnews.com), Temple Daily Telegram (tdtnews.com), KWTX, KCEN, Texas Lawyer (law.com)
- txcourts.gov court pages and judge bios (Supreme Court, CCA, 3rd and 15th COA)
- Ballotpedia, Texas Secretary of State election results (results.texas-election.com / sos.state.tx.us), Bell County election canvass PDFs if reachable
- State Bar of Texas member directory for bar admission date / law school (texasbar.com — may block; if so, do not claim)
- Candidate's own campaign site (cite as the campaign's statement: "according to his campaign website")
- Secondary aggregators (BallotReady, branch.vote, trellis.law, txdirectory) are weaker: use only when no primary source is found and label them by name.
- The site's own Nov. 3 ballot guide (/nov-3-2026-ballot-guide/) and the project research in `/home/claude/ll/work/.review/` may be referenced for ballot facts (candidate lists per race come from the official Bell County sample ballots, OCR'd on 2026-11-01).

## File mechanics
- Edit the file in place under `/home/claude/ll/work/collections/_candidates/courts/<tier>/<slug>.md`. Keep `layout`, `title`, `candidate_slug`, `office`, `jurisdiction`, `court_group`, `seat`, `ballot_order`, `listing_status`, `election_status`, `office_up_for_election`, `incumbent`, `official_profile`, `campaign_website`, `headshot` keys as they are unless a key states a fact you found to be false (then fix it and log it).
- Multi-line fields use single-quoted YAML scalars with `''` for apostrophes, blank lines between paragraphs (see existing files). After editing, validate: `python3 -c "import yaml,sys; t=open(sys.argv[1]).read().split('---',2)[1]; yaml.safe_load(t); print('ok')" <file>`.
- Add a front-matter list:
  ```
  sources:
  - title: Governor Abbott Appoints Duskie To 426th Judicial District Court
    publisher: Office of the Texas Governor
    url: https://gov.texas.gov/news/post/...
    date: 2020-07-23
    accessed: 2026-11-03
  ```
  one entry per distinct URL cited anywhere in the file. `date` is the article/page date if known, else omit.
- The markdown body after the closing `---` is one or two sentences; it must also be sourced (cite inline) or reduced to a bare statement that is fully supported by the front matter's cited facts.
- Write a verification log at `/home/claude/ll/work/logs/<slug>.md`: a table with columns `Claim (as it was) | Verdict (KEPT / REMOVED / CORRECTED) | Source URL | Note`. Every sentence of the original file must appear. Then a line "New facts added:" listing anything you added, each with URL.
- Do not touch files outside your assigned list. Do not run git.
