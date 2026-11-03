# broken-links

File: `_pages/broken-links.md` (/broken-links/, 432 lines: 134 Liquid/HTML + 298 CSS). Renders `_data/brokenlinks.json`.

| Line | Text (first 100 chars) | Verdict | Source URL |
|---|---|---|---|
| 1-6 | front matter (indexable; no `sitemap: false`, no `robots: noindex`) | NON-CLAIM |  |
| 11 | "This page reports the status of all external links… Links are checked periodically for 404 errors" | NON-CLAIM (site statement) |  |
| 14-127 | report tables | DATA-FILE `_data/brokenlinks.json` (lists every external URL on the site with HTTP status and the repo source file path) |  |
| 130-131 | "No link data available… To generate this report, run: python3 scripts/check-broken-links.py" | NON-CLAIM (developer instruction rendered to the public) |  |
| 136-432 | CSS | NON-CLAIM |  |

**Belongs on the public site?** No. It is an internal QA report: it exposes repository file paths (`source_file`), a build command, and a public list of every outbound link marked "404 Error" — including links on judge profiles this review is in the middle of fixing. Recommend unpublishing (move out of `_pages/` or add `published: false`); at minimum set `sitemap: false` and `robots: noindex`. The data file can stay for internal use.

**Counts:** lines checked 432 / claim lines 0 / cited 0 / corrected 0 / removed 0
