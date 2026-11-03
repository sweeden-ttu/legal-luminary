# bell-county

File: `_pages/bell-county.md` (/bell-county/). Judge/phone tables are Liquid over `_data/bell_county_courts.yml` (DATA-FILE, has its own in-page source list).

| Line | Text (first 100 chars) | Verdict | Source URL |
|---|---|---|---|
| 1-13 | front matter | NON-CLAIM |  |
| 14-50 | Liquid assign + CSS | NON-CLAIM |  |
| 53 | "Bell County, located in Central Texas, has its own court system and procedures… Understanding local practices is essential…" | CORRECTED → replaced with a plain description of what the page lists (vague/unsourced generalities removed) |  |
| 56-62 | quick contacts, "checked against the sources listed at the bottom on {{ bc.verified_on_text }}" | DATA-FILE `_data/bell_county_courts.yml` |  |
| 74 | "Bell County operates multiple courts handling different types of cases. Knowing which court…" | CORRECTED → "Each row links to the statute that sets the court's jurisdiction." |  |
| 79 | District Courts (6): "Felony…; civil cases over $200,000; family law…; juvenile cases" | CORRECTED → felony (art. 4.05); civil over $500 (§24.007); family/juvenile dropped | https://tcss.legis.texas.gov/resources/cr/htm/cr.4.htm#4.05; https://tcss.legis.texas.gov/resources/gv/htm/gv.24.htm#24.007; https://tcss.legis.texas.gov/resources/gv/htm/gv.24.htm#24.129 |
| 80 | County Courts at Law (3): "Class A and B misdemeanors; civil … $500 and $200,000; appeals from JP; probate" | CORRECTED → art. 4.07 misdemeanors; $500–$325,000; JP appeals §51.001; probate/mental health in CCL No. 1 | https://tcss.legis.texas.gov/resources/gv/htm/gv.25.htm#25.0161; https://tcss.legis.texas.gov/resources/cr/htm/cr.4.htm#4.07; https://tcss.legis.texas.gov/resources/gv/htm/gv.25.htm#25.0003; https://tcss.legis.texas.gov/resources/cp/htm/cp.51.htm#51.001; https://www.bellcountytx.com/county_government/county_courts/court_at_law_1/index.php (evidence file paul_a_motz.txt) |
| 81 | "Justice of the Peace Courts (5 precincts)" | CORRECTED → "6 seats in 4 precincts" with links to the six county JP pages; jurisdiction cited | Bell County JP pages (six, precinct_1 … precinct_4_place_2; evidence files in .review/evidence); https://tcss.legis.texas.gov/resources/cr/htm/cr.4.htm#4.11; https://tcss.legis.texas.gov/resources/gv/htm/gv.27.htm#27.031; https://tcss.legis.texas.gov/resources/pr/htm/pr.24.htm#24.004; https://tcss.legis.texas.gov/resources/fa/htm/fa.65.htm#65.004 |
| 82 | Municipal Courts: "City ordinance violations and certain Class C misdemeanors" | KEPT-CITED (Class C narrowed to Killeen's court) | https://tcss.legis.texas.gov/resources/cr/htm/cr.4.htm#4.14; https://killeentexas.gov/172/Municipal-Court |
| 88 | "All District Courts and County Courts at Law sit at the {{ bc.courthouse.name }}… Judges serve 4-year terms." | KEPT-CITED (district judges four-year term; "all judges" narrowed to district judges) | https://www.bellcountytx.com/county_government/district_courts/426th_district_court/index.php (evidence file steve_duskie.txt); https://tcss.legis.texas.gov/resources/cn/htm/cn.5.htm#5.7 |
| 90-111 | judge tables, prosecutors list | DATA-FILE `_data/bell_county_courts.yml` |  |
| 115 | "Local cities maintain their own municipal courts for city ordinance violations and certain Class C misdemeanors" | KEPT-CITED (reworded to art. 4.14) | https://tcss.legis.texas.gov/resources/cr/htm/cr.4.htm#4.14 |
| 117 | "Killeen Municipal Court — 714 N. 2nd Street, Killeen, TX 76541" | CORRECTED → 200 E. Avenue D, Suite 1, Killeen, TX 76541; 254-501-7850 | https://killeentexas.gov/172/Municipal-Court |
| 119 | "Temple Municipal Court — 210 N. Main Street, Temple, TX 76501" | REMOVED (city page fetch blocked by proxy; address unverified) | blocked: https://www.templetx.gov/government/departments/municipal_court/index.php |
| 121 | "Belton Municipal Court — 520 E. Central Avenue, Belton, TX 76513" | REMOVED (Belton notice page gives phone 254-933-5838 and a drop-box at 100 S. Davis St. but no court street address) | https://beltontexas.gov/news_detail_T11_R761.php |
| 127 | "Bell County is home to Fort Cavazos (formerly Fort Hood), one of the largest military installations in the world. This creates unique legal considerations:" | CORRECTED → main business area of Fort Hood is in Bell County; named Fort Cavazos May 9, 2023 – June 11, 2025 when the name reverted to Fort Hood. "one of the largest … in the world" and "unique legal considerations" removed | https://en.wikipedia.org/wiki/Fort_Hood (home.army.mil/cavazos fetch blocked by proxy) |
| 129 | "Service members facing charges have additional rights… may face both civilian and military legal proceedings. Attorneys familiar with military-civilian interactions provide valuable guidance" | REMOVED (unsourced; advertising copy) |  |
| 131-141 | "Population Centers": Killeen largest city/high volume of cases; Temple "significant personal injury caseload due to traffic volume"; Belton county seat; Harker Heights/Copperas Cove "increasing court activity" | REMOVED (unsourced characterizations; Copperas Cove is not in Bell County at all) |  |
| 143-164 | "Finding Legal Representation" box, "What to Look For", "Take Action" notice ("Personal injury claims have statutes of limitations") | REMOVED (unsourced advice/advertising; "attorneys featured on this site have experience in Bell County courts" unverifiable) |  |
| 166-178 | cards | NON-CLAIM |  |
| 180-189 | sources section (Liquid over data file) | DATA-FILE |  |

**Counts:** lines checked 189 / claim lines 17 / cited 6 / corrected 8 / removed 7 (blocks)
