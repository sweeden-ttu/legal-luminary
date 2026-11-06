# Nov. 3, 2026 results update (2026-11-06)

Owner's request: update the site with the candidates who won, starting from the KDH rundown
https://kdhnews.com/centerforpolitics/here-s-a-rundown-of-area-election-results-from-tuesday-night/article_61b4fae6-2d44-4b71-a8c9-cca408c33344.html

The KDH rundown covers local, legislative and congressional races only (no statewide or appellate courts, no unopposed county races), and some of its counts are early. Every result on the site was therefore taken from the primary returns:

| Races | Source | As of |
|---|---|---|
| Statewide courts, 3rd COA, 169th/264th/478th district judges, statewide executive, US House 17/31, SD 24, HD 54/55 | Texas SOS, https://electionresults.sos.state.tx.us/results.html (fetched from the owner's computer; 100% of polling locations) | page updated 11/04/2026 4:59 PM |
| County judge, CCL 1-3, JP 1/2/3-2/4-2, clerks, treasurer, commissioners 2/4, CAD 1-3, hospital district, Killeen Props A-H | Bell County ENR (Clarity), https://results.enr.clarityelections.com/TX/Bell/127475/ summary.json v385515, read in the owner's built-in browser | last updated 11/4/2026 1:48:46 AM |
| Cross-checks | Texas Tribune 2026-11-04 (all ten statewide-court winners); KSAT (3rd COA); KDH JP 4-2, commissioner, HD 55 and tax-measure stories | |

All figures are in `_data/results_2026_general.yml`, which drives `_includes/race-result.html`, `_includes/results-group.html` and `_includes/profile-election-result.html`. Shares are computed from the published counts (votes / all votes in the race, write-ins included for statewide races, write-in rows not shown).

KDH vs. county counts: the rundown's JP 4-2 figures (Gonzalez 25,059 / Cox 14,048) and HD 55 figures (29,308 / 29,128) are earlier counts; the county ENR and SOS have Gonzalez 31,485 / Cox 18,588 (35 of 36 precincts) and Rabroker 30,378 / Hickland 29,959. The site uses the later official-source counts.

Corrected along the way: the ballot guide said the appraisal district board races had no candidates (corrections VV-2026-002).
