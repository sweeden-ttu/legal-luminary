# candidates

File: `candidates.html` (/candidates/). Liquid loop over every `site.candidates` entry.

| Line | Text (first 100 chars) | Verdict | Source URL |
|---|---|---|---|
| 1-5 | front matter | NON-CLAIM |  |
| 7 | heading "Bell County Judicial Candidates – November 2026" | NON-CLAIM but misleading: the loop also prints former judges, primary losers and statewide candidates; see recommendation |  |
| 8 | visible "TODO: Add Attorney General of Texas and other statewide offices later." | NON-CLAIM (developer note rendered to readers) |  |
| 10-22 | Liquid cards (headshot, office, incumbent flag) | LIQUID (profile data verified separately) |  |

**Recommendation:** remove the rendered TODO line and either filter the loop to `election_status == "general_2026"` or retire the page in favor of /nov-3-2026-ballot-guide/ and /candidates/courts/. The corrections page links here as the place where "updated labels are listed", so keep a redirect if retired.

**Counts:** lines checked 23 / claim lines 0 / cited 0 / corrected 0 / removed 0
