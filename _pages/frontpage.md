---
layout: default
article_feed: top-articles
title: Legal Luminary — Who's Who on the Central Texas Bench
permalink: /
hero: true
hero_title: "Who's Who on the Central Texas Bench"
hero_subtitle: "Every elected judge in Bell County, and the statewide courts on its ballot — sourced, verified, no advertising"
description: "A who's who of the elected judiciary of Central Texas: Bell County district courts, county courts at law, county judge and justices of the peace, plus the Texas Supreme Court, Court of Criminal Appeals and courts of appeals seats on the Bell County ballot. Every profile cites public news reporting and official records."
verified_at: 2026-11-01
---

<p class="intro-text">
Legal Luminary profiles the judges who sit in Bell County, Texas, and the candidates who want to replace them. Every statement on a profile links to the news article or official record that supports it; nothing on the site is paid for or endorsed. Start with a court, or go straight to the <a href="/nov-3-2026-ballot-guide/">November 3, 2026 ballot</a>.
</p>

## The courts

<div class="cards-grid tier-grid">
<div class="card"><h3><a href="/courts/statewide/">Supreme Court &amp; Court of Criminal Appeals</a></h3><p>Texas's two nine-member courts of last resort, elected statewide (<a href="https://tcss.legis.texas.gov/resources/cn/htm/cn.5.htm#5.2">Tex. Const. art. V §§2, 4</a>). Seven seats on the 2026 ballot, every one contested (<a href="https://www.bellcountytx.com/departments/elections/ballot_samples.php">Bell County ballot samples</a>; <a href="https://ballotpedia.org/Texas_Supreme_Court_elections,_2026">Ballotpedia: Texas Supreme Court elections, 2026</a>; <a href="https://ballotpedia.org/Texas_Court_of_Criminal_Appeals_elections">Ballotpedia: Court of Criminal Appeals elections</a>).</p><a href="/courts/statewide/" class="btn btn-primary">Statewide courts</a></div>
<div class="card"><h3><a href="/courts/appeals/">Courts of Appeals</a></h3><p>The Third Court of Appeals in Austin hears Bell County's appeals (<a href="https://tcss.legis.texas.gov/resources/gv/htm/gv.22.htm#22.201">Gov't Code §22.201(d)</a>); the Fifteenth hears appeals involving the state and the business court (<a href="https://tcss.legis.texas.gov/resources/gv/htm/gv.22.htm#22.220">§22.220(d)</a>; <a href="https://tcss.legis.texas.gov/resources/gv/htm/gv.25a.htm#25A.007">§25A.007</a>). Four seats on the 2026 ballot (<a href="https://www.bellcountytx.com/departments/elections/ballot_samples.php">Bell County ballot samples</a>; <a href="https://www.sos.texas.gov/elections/candidates/guide/2026/offices2026.shtml">Texas SOS 2026 offices</a>).</p><a href="/courts/appeals/" class="btn btn-primary">Courts of appeals</a></div>
<div class="card"><h3><a href="/courts/district/">District Courts</a></h3><p>Six state district courts — the 27th, 146th, 169th, 264th, 426th and 478th (<a href="https://tcss.legis.texas.gov/resources/gv/htm/gv.24.htm#24.129">Gov't Code §24.129</a>) — at the Bell County Justice Center (<a href="https://www.bellcountytx.com/county_government/district_courts/426th_district_court/index.php">Bell County</a>), with their associate and visiting judges.</p><a href="/courts/district/" class="btn btn-primary">District courts</a></div>
<div class="card"><h3><a href="/courts/county/">County Courts at Law &amp; County Judge</a></h3><p>Three statutory county courts (<a href="https://tcss.legis.texas.gov/resources/gv/htm/gv.25.htm#25.0161">Gov't Code §25.0161</a>) and the constitutional County Judge, who presides over the Commissioners Court (<a href="https://tcss.legis.texas.gov/resources/lg/htm/lg.81.htm#81.001">Local Gov't Code §81.001</a>).</p><a href="/courts/county/" class="btn btn-primary">County courts</a></div>
<div class="card"><h3><a href="/courts/jp/">Justices of the Peace</a></h3><p>Six precinct courts (<a href="https://www.bellcountytx.com/county_government/justice_of_the_peace/precinct_1/index.php">Bell County JP Pct 1</a>, <a href="https://www.bellcountytx.com/county_government/justice_of_the_peace/precinct_2/index.php">Pct 2</a>, <a href="https://www.bellcountytx.com/county_government/justice_of_the_peace/precinct_3_place_1/index.php">Pct 3 Pl 1</a>, <a href="https://www.bellcountytx.com/county_government/justice_of_the_peace/precinct_3_place_2/index.php">Pct 3 Pl 2</a>, <a href="https://www.bellcountytx.com/county_government/justice_of_the_peace/precinct_4_place_1/index.php">Pct 4 Pl 1</a>, <a href="https://www.bellcountytx.com/county_government/justice_of_the_peace/precinct_4_place_2/index.php">Pct 4 Pl 2</a>) for evictions (<a href="https://tcss.legis.texas.gov/resources/pr/htm/pr.24.htm#24.004">Prop. Code §24.004</a>), small claims (<a href="https://tcss.legis.texas.gov/resources/gv/htm/gv.27.htm#27.031">Gov't Code §27.031</a>), fine-only misdemeanors (<a href="https://tcss.legis.texas.gov/resources/cr/htm/cr.4.htm#4.11">Code Crim. Proc. art. 4.11</a>) and magistration (<a href="https://tcss.legis.texas.gov/resources/cr/htm/cr.2a.htm#2A.151">art. 2A.151</a>).</p><a href="/courts/jp/" class="btn btn-primary">Justices of the peace</a></div>
<div class="card"><h3><a href="/attorneys/">Attorney Directory</a></h3><p>The bar the bench is drawn from: {{ site.data.attorneys_bell_county.firms | size }} Bell County law firms, their attorneys, practice areas and years in practice.</p><a href="/attorneys/" class="btn btn-secondary">Attorneys</a></div>
</div>

## The Bell County bench today

{% assign cj = site.candidates | where_exp: "j", "j.path contains 'texas/bell_county/david_blackburn'" | first %}
| Court | Judge | 2026 election ([Bell County ballot samples](https://www.bellcountytx.com/departments/elections/ballot_samples.php)) |
|---|---|---|
{% if cj %}| {{ cj.office }} | **[{{ cj.title }}]({{ cj.url }})** | Unopposed |
{% endif %}{% assign dist = site.candidates | where_exp: "j", "j.path contains 'courts/district/'" | where: "incumbent", true | sort: "office" %}{% for j in dist %}{% unless j.election_status == "former" %}| {{ j.office }} | **[{{ j.title }}]({{ j.url }})** | {% if j.listing_status contains "Nominee" %}Unopposed{% else %}Not up until later{% endif %} |
{% endunless %}{% endfor %}{% assign cty = site.candidates | where_exp: "j", "j.path contains 'courts/county/'" | sort: "office" %}{% for j in cty %}{% unless j.election_status == "former" %}| {{ j.office }} | **[{{ j.title }}]({{ j.url }})** | {% if j.incumbent == false %}Open seat — unopposed nominee{% elsif j.listing_status contains "Nominee" %}Unopposed{% else %}Not up until later{% endif %} |
{% endunless %}{% endfor %}{% assign jps = site.candidates | where_exp: "j", "j.path contains 'courts/jp/'" | where: "incumbent", true | sort: "office" %}{% for j in jps %}{% unless j.election_status == "former" %}{% assign st = "Not up until 2028" %}{% if j.office contains "Precinct 4, Place 2" %}{% assign st = "Contested: [Cox](/candidates/courts/jp/beatrice_bea_cox/) (R) v. [Gonzalez](/candidates/courts/jp/jessica_a_gonzalez/) (D) ([KDH](https://kdhnews.com/centerforpolitics/cox-and-gonzalez-participate-in-justice-of-the-peace-forum-ahead-of-nov-3-election/article_f3226aea-4314-4639-9f1d-804bfbe9c839.html))" %}{% elsif j.office contains "Precinct 1" %}{% assign st = "Not seeking re-election; Patrick Patterson (R) unopposed ([KDH](https://kdhnews.com/news/region/patterson-to-follow-in-stepfathers-justice-of-the-peace-footsteps-blackburn-keeps-county-judge-seat/article_95f7afcb-3ab6-5651-9b0b-d42467c264f5.html))" %}{% elsif j.office contains "Precinct 3, Place 2" or j.listing_status contains "Nominee" %}{% assign st = "Unopposed" %}{% endif %}| {{ j.office }} | **[{{ j.title }}]({{ j.url }})** | {{ st }} |
{% endunless %}{% endfor %}

Full tables, former judges and candidates: [The Bell County Bench](/candidates/courts/).

## Elections

<div class="cards-grid">
<div class="card"><h3>Nov. 3, 2026 ballot guide</h3><p>The 19 judicial races and the two clerk races on a Killeen ballot — contested and unopposed — plus the hospital district tax and Killeen charter propositions (<a href="https://www.bellcountytx.com/departments/elections/ballot_samples.php">Bell County ballot samples</a>).</p><a href="/nov-3-2026-ballot-guide/" class="btn btn-primary">Ballot guide</a></div>
<div class="card"><h3>How to run for judge</h3><p>Who is eligible for each bench, filing windows, fees and petition signatures in Bell County.</p><a href="/run-for-judge/" class="btn btn-secondary">Run for judge</a></div>
<div class="card"><h3>Voting in Bell County</h3><p>Early voting, polling places, mail ballots and what the county's election office publishes.</p><a href="/elections/" class="btn btn-secondary">Elections</a></div>
</div>

{% include front-page-featured-articles.html %}

## How this site works

Profiles are built from local news reporting and official records — the full list is on the [sources page](/advertise/). Claims that cannot be matched to a public source are marked unverified, and every correction is logged on the [corrections page](/corrections/). Read the [about page](/about/) for the mission and the legal basis for publishing.
