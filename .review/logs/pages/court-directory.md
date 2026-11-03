# court-directory

File: `_pages/court-directory.md` (/court-directory/). Nearly all names/phones come from `_data/bell_county_directory.json` — DATA-FILE, not edited; needs its own pass (front matter `verified_at: 2026-02-19`).

| Line | Text (first 100 chars) | Verdict | Source URL |
|---|---|---|---|
| 1-11 | front matter; `source_url: bellcountytx.com` | NON-CLAIM |  |
| 13 | `{% assign dir = site.data.bell_county_directory %}` | DATA-FILE `_data/bell_county_directory.json` |  |
| 16 | intro "Information is verified against official county sources…" | NON-CLAIM (site statement) |  |
| 19-31 | courthouse box, county officials table | DATA-FILE |  |
| 35 | "District Courts handle felony criminal cases, civil cases over $200,000, family law, and juvenile matters. All are located at … 1201 Huey Drive" | CORRECTED → felony (art. 4.05) and civil over $500 (§24.007); "over $200,000" was wrong; family/juvenile dropped (unsourced); address corrected to "1201 Huey Road" per county page | https://tcss.legis.texas.gov/resources/cr/htm/cr.4.htm#4.05; https://tcss.legis.texas.gov/resources/gv/htm/gv.24.htm#24.007; https://tcss.legis.texas.gov/resources/gv/htm/gv.24.htm#24.129; https://www.bellcountytx.com/county_government/district_courts/426th_district_court/index.php (evidence file steve_duskie.txt) |
| 38-46 | district court cards | DATA-FILE |  |
| 50 | "County Courts at Law handle Class A and B misdemeanors, civil cases between $500 and $200,000, probate matters, and appeals from JP courts." | CORRECTED → misdemeanors per art. 4.07; civil $500–$325,000 (§25.0003(c), not $200,000); JP appeals (CPRC §51.001); probate/mental health in CCL No. 1 (Bell County) | https://tcss.legis.texas.gov/resources/cr/htm/cr.4.htm#4.07; https://tcss.legis.texas.gov/resources/gv/htm/gv.25.htm#25.0003; https://tcss.legis.texas.gov/resources/cp/htm/cp.51.htm#51.001; https://tcss.legis.texas.gov/resources/gv/htm/gv.25.htm#25.0161; https://www.bellcountytx.com/county_government/county_courts/court_at_law_1/index.php (evidence file paul_a_motz.txt) |
| 53-60 | CCL cards | DATA-FILE |  |
| 64 | "JP courts handle Class C misdemeanors (fine-only offenses), small claims civil cases up to $20,000, evictions, and truancy cases." | KEPT-CITED (reworded to statutory terms) | https://tcss.legis.texas.gov/resources/cr/htm/cr.4.htm#4.11; https://tcss.legis.texas.gov/resources/gv/htm/gv.27.htm#27.031; https://tcss.legis.texas.gov/resources/pr/htm/pr.24.htm#24.004; https://tcss.legis.texas.gov/resources/fa/htm/fa.65.htm#65.004 |
| 67-76 | JP cards | DATA-FILE |  |
| 80 | "Municipal courts handle city ordinance violations and Class C misdemeanors that occur within city limits." | KEPT-CITED (ordinance jurisdiction per art. 4.14; Class C narrowed to Killeen's court per city page) | https://tcss.legis.texas.gov/resources/cr/htm/cr.4.htm#4.14; https://killeentexas.gov/172/Municipal-Court |
| 83-116 | municipal cards, online resources, service areas | DATA-FILE (service-area descriptions are prose in the JSON — flag for the data pass) |  |
| 119 | legal notice: "(254) 933-5100" main courthouse line | DATA-FILE (number also hard-coded in line 22; could not verify — bellcountytx.com blocked) |  |

**Counts:** lines checked 120 / claim lines 4 (prose) / cited 4 / corrected 2 / removed 0; DATA-FILE rows: 8 blocks
