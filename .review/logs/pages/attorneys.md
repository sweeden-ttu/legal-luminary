# Verification log — _pages/attorneys.md (2026-11-03)

DATA-FILE: the directory renders from `_data/attorneys_bell_county.yml` (45 firms; cities Belton, Harker Heights, Killeen, Temple; every entry has `source` = firm website and `verified: 2026-11-01`). Per the owner, entries were compiled from firms' own websites; the data file was not edited (separate pass).

| Line | Text (first 100 chars) | Verdict | Source URL |
|---|---|---|---|
| 7 | hero_subtitle: "…offices in Killeen, Temple, Belton, Harker Heights, Copperas Cove and Salado" | CORRECTED to "Killeen, Temple, Belton and Harker Heights" — the data file contains no Copperas Cove or Salado firms | DATA-FILE _data/attorneys_bell_county.yml |
| 8 | description: "Compiled from the firms' own websites; no paid listings" | NON-CLAIM (site statement) | — |
| 17 | "This directory lists {{ firms | size }} law firms… read from the firm's own website… not a paid listing… not an endorsement" | NON-CLAIM (site statement; count is Liquid) | — |
| 22 | "Any attorney's license status, disciplinary history and date of admission can be confirmed free of charge in the State Bar of Texas Find a Lawyer directory" | CORRECTED: the Find a Lawyer page was opened (curl) but its search widget returned an error and the page text does not state what the directory shows or that it is free; reduced to a plain pointer to the directory | https://www.texasbar.com/AM/Template.cfm?Section=Find_A_Lawyer |
| 22 | "Years listed below are the firm's own statements…" | NON-CLAIM (site statement) | — |
| 25-69 | nav, filter, Liquid rendering of firm cards | NON-CLAIM (Liquid; data under separate pass) | DATA-FILE |
| 71 | "Listings were compiled from each firm's public website on {{ page.verified_at }}… confirm with the firm and the State Bar" | NON-CLAIM (site statement; `verified_at` left at 2026-11-01 because it is the compile date shown to readers) | — |
| 73-90 | script | NON-CLAIM | — |

Counts: 8 units checked; 0 cited; 2 corrected; 0 removed. No literal numbers in the prose.
