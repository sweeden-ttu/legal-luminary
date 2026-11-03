# Verification rules for legalluminary.com content pages (non-profile)

Site owner's instruction: "VERIFY EVERY SINGLE LINE, LINE BY LINE. EITHER FIND A SOURCE FOR THE INFORMATION ONLINE OR REMOVE THE INFORMATION."

Work on copies under /home/claude/ll/work/pages/ (mirrors the repo paths: `_pages/...`, `_posts/...`, `texas/...`, `candidates.html`, `courts-directory.md`). Edit in place. Do not run git.

## What counts as a line that needs a source
Every sentence that asserts a fact about the world: who holds an office, what a court does, what a law says, numbers, dates, election results, what a person did or said, what a county/city is like. Each such sentence must end with an inline markdown citation `([Source](https://...))` to a page you personally opened this session (WebFetch) or whose WebSearch snippet states the fact. Statute citations must link to the statute text (tcss.legis.texas.gov/resources/{code}/htm/{code}.{chapter}.htm#{section} works; statutes.capitol.texas.gov is a JS shell — don't cite it).

## What does NOT need a source (leave alone)
- Navigation, headings, link text, labels, button text, layout/Liquid markup, front matter keys that drive rendering (`layout`, `permalink`, `title`, `description`, `hero_*`), CSS/JS.
- Statements about the site itself ("this site lists…", "we do not accept advertising", "see the ballot guide") — these are the owner's own statements of policy, not claims about the world.
- Generic definitions the reader can check in any civics text ARE claims; cite them to the Texas Constitution / Government Code / txcourts.gov "About Texas Courts" page or remove.

## Procedure per page
1. Number the lines (`cat -n`). Walk them in order. For each line with a factual claim: search, open, confirm. Keep a running table in `/home/claude/ll/work/logs/pages/<file>.md`: `Line | Text (first 100 chars) | Verdict (KEPT-CITED / CORRECTED / REMOVED / NON-CLAIM) | Source URL`.
2. Fix: add the citation, correct the text to what the source says, or delete the sentence. If deleting a sentence leaves a paragraph or table row meaningless, delete the whole unit.
3. Tables of candidates/races: each row needs a source (official sample ballot → cite /nov-3-2026-ballot-guide/ only if that page itself cites the Bell County ballot PDF; otherwise cite the Bell County elections ballot-samples page https://www.bellcountytx.com/departments/elections/ballot_samples.php, which the owner downloaded on 2026-11-01 — that URL may be cited for Bell County ballot composition; KDH primary-results articles for who won primaries; txcourts.gov / Ballotpedia for incumbency).
4. Liquid-generated content (`{% for c in site.candidates %}`) pulls from profile files that are being verified separately — leave the Liquid alone, but any literal prose around it is in scope.
5. Data files in `_data/` that feed a page: if a page renders facts from a data file, note it in the log as DATA-FILE and list which file; do not edit data files (they get a separate pass) unless the page is unusable without it.
6. After editing, confirm the file still starts with valid front matter (`python3 -c "import yaml,sys;yaml.safe_load(open(sys.argv[1]).read().split('---',2)[1])" <file>`).
7. Copyright: paraphrase; at most one quote under 15 words per source.
8. Never invent URLs. If you can't find a source, the line comes out — a shorter true page is the goal.

## News posts (`_posts/`)
Each post must (a) have an external `source_url` that resolves (WebFetch it; a 404/removed page → delete the post), (b) contain only a short attributed excerpt/summary of that source, not claims the source doesn't make, and (c) name the outlet. Posts with no external source, or sourced to legalluminary.com itself, are deleted unless every claim in them can be cited to an external public source. "Articles update" digest posts that are just lists of linked headlines are fine if each headline links to its outlet.
