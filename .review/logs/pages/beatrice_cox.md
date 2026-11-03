# Verification log — pages/texas/bell_county/beatrice_cox.md (2026-11-03)

| Line | Text (first 100 chars) | Verdict | Source URL |
|---|---|---|---|
| 1-10 | front matter (layout, title, office, incumbent, jurisdiction, campaign_website, slug, headshot) | NON-CLAIM (rendering keys); `office` and `incumbent: false` confirmed; added `party: Republican` and `sources:` | https://kdhnews.com/centerforpolitics/cox-and-gonzalez-participate-in-justice-of-the-peace-forum-ahead-of-nov-3-election/article_f3226aea-4314-4639-9f1d-804bfbe9c839.html |
| 7 | campaign_website facebook.com/BeaForJP/ | NON-CLAIM (link). Returns 200 (redirects to FB login); same URL is `facebook_url` on the JP profile. Kept. | — |
| 12 | Beatrice Cox is a candidate for Justice of the Peace, Precinct 4, Place 2 in Bell County. | KEPT-CITED (expanded: Republican; faces Democrat Jessica Gonzalez on Nov. 3, 2026) | https://kdhnews.com/centerforpolitics/cox-and-gonzalez-participate-in-justice-of-the-peace-forum-ahead-of-nov-3-election/article_f3226aea-4314-4639-9f1d-804bfbe9c839.html (KDH, Oct. 7, 2026) |

New facts added: party Republican; opponent Jessica Gonzalez (D); election date Nov. 3, 2026 — all from the KDH forum article above. Added pointer link to the JP profile `/candidates/courts/jp/beatrice_bea_cox/`.

DATA-FILE: layout `candidate-profile` reads `_data/candidates/bell_county/<slug>` for sidebar articles; not edited.

**Recommendation: REDIRECT.** This page duplicates `/candidates/courts/jp/beatrice_bea_cox/` (collections/_candidates/courts/jp/beatrice_bea_cox.md), which carries the fuller sourced profile, the same office, the same Facebook link and a Bell County official_profile. Keep one canonical URL: make this page a redirect (e.g. `redirect_to: /candidates/courts/jp/beatrice_bea_cox/` via jekyll-redirect-from) or remove it from `site.candidates` listings. Not deleted per instructions.
