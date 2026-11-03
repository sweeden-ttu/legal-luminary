# methodology

File: `_pages/methodology.md` (366 lines → 177). Rule applied: a described method is the owner's own statement and may stay; any statistic or characterization about a specific judge, court, plaintiff or company must be sourced to a public record I opened, or go. No per-judge statistic could be tied to a public page (the dataset is only in `_data/`, which Jekyll does not serve, and the Odyssey portal fetch was blocked), so all result tables were removed.

| Line | Text (first 100 chars) | Verdict | Source URL |
|---|---|---|---|
| 1-7 | front matter | NON-CLAIM |  |
| 17-29 | §1 Overview (goal, two-phase design) | NON-CLAIM (method description) |  |
| 38-43 | "CFPB database contains approximately 15.7 million complaints… (complaints.csv.zip, 1.37 GB) was downloaded… on June 9, 2026" | CORRECTED → number and file size removed (CFPB page fetch blocked; count changes daily); download statement kept as owner's own action | blocked: https://www.consumerfinance.gov/data-research/consumer-complaints/ |
| 47-50 | "Nationstar Mortgage (19,296) and Mr. Cooper (15,430) are the same entity…" | REMOVED (unsourced company fact + unverifiable counts); aggregation rule sentence kept |  |
| 56-59 | "Odyssey Public Portal (Tyler Technologies, version 2017.1.61.2) provides public access to civil, criminal, and traffic case records" | CORRECTED → vendor/version and record-type claims removed; portal named as the source used | blocked: https://justice.bellcounty.texas.gov/PublicPortal/ |
| 63-66 | "four-year filing period… matching the term length for Justices of the Peace in Texas" | KEPT-CITED | https://tcss.legis.texas.gov/resources/cn/htm/cn.5.htm#5.18 |
| 70-113 | §3 CFPB Complaint Findings: 21-row complaint table, "386,190 complaints — 63%", "Nationstar… among the most-complained-about… in Bell County's foreclosure ecosystem", "Law firms … rarely appear", "NewRez LLC (formed 2018 from New Penn Financial / Caliber merger)" | REMOVED (snapshot numbers cannot be checked against a fixed page; NewRez/Caliber formation claim unsourced and, as written, inaccurate; "ecosystem" characterization unsourced) |  |
| 117-174 | §4 search methodology, search terms, case classification, record fields | NON-CLAIM (method description; renumbered §3) |  |
| 178-194 | §5.1 Overall volumes (547 cases, 463 residential evictions…) | REMOVED (derived statistics, no public page) |  |
| 196-220 | §5.2 Distribution by court with judge names (James 154, Johnson 137, Wilkey 136, 146th 42, 169th 34, Duffield 24, Fisher 12, CCL1 7, Coleman 1) | REMOVED (per-judge statistics; must be sourced to a public record) |  |
| 222-234 | §5.3 case status distribution | REMOVED |  |
| 236-252 | §5.4 "Three JP courts account for 427 of 547 (78.1%)" with judge names | REMOVED (per-judge) |  |
| 254-273 | §5.5 top plaintiffs (Marie Curtis FLP 68, Pleasant View 50, …) | REMOVED (facts about named private parties; no public page) |  |
| 279-294 | §6.1 geographic concentration ("consistent with population distribution", Killeen largest city, Temple second-largest, rural precincts) | REMOVED (unsourced; depends on removed results) |  |
| 296-304 | §6.2 "Foreclosure cases in Texas are filed in District Court, not JP court. All 76 … 146th (42) and 169th (34)… typically proceed under the Texas Home Equity expedited process" | REMOVED (court-specific statistics; the general venue statement was not sourced either) |  |
| 306-317 | §6.3 eviction filing patterns (21.6%, "Mortgage servicers rarely file evictions") | REMOVED |  |
| 319-327 | §6.4 Limitations | NON-CLAIM (method; kept, renumbered §4; "MCG Homestead: 44 parties" example and "concentration figures" cross-reference adjusted) |  |
| 333-346 | §7 Context & Motivation (author's personal history; "does not publish party membership") | NON-CLAIM (owner's own statement) |  |
| 353-360 | §8 "The full deduplicated dataset (547 records) is available at /data/bell_county_evictions_foreclosures.csv; source code … in the project repository" | CORRECTED → link removed: the CSV lives at `_data/bell_county_evictions_foreclosures.csv` (806 rows, not 547) and `_data/` is not served, so the link 404s; replaced with a statement that counts will be published only with the case-level dataset |  |
| 362 | "This page will be updated as additional cases are identified…" | CORRECTED → "when the dataset is published" |  |

**Recommendation:** keep the page published as a method statement. To restore the per-court/per-judge tables, publish the CSV under a served path (e.g. `/assets/data/`) with case numbers so each row is checkable on the Odyssey portal, and cite it from every table; otherwise the tables stay out. Title/description still say "Study" — acceptable, since the method is described.

**Counts:** lines checked 366 / claim lines (blocks) 19 / cited 1 / corrected 5 / removed 13
