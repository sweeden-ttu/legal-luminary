---
layout: default
article_feed: judicial-officers-articles
title: "The Bell County Bench — Who's Who"
permalink: /candidates/courts/
description: "Every elected judge in Bell County, Texas — district courts, county courts at law, county judge and justices of the peace — plus the statewide and appellate seats on the Bell County ballot, with sourced profiles."
last_updated: 2026-11-01
---

<h1>The Bell County Bench</h1>

<p class="intro-text">Every judge below holds an elected office (or is a candidate for one) and has a profile built from public news reporting and official records. Pick a tier for the full court, or scan the current bench here.</p>

<div class="cards-grid tier-grid">
<div class="card"><h3><a href="/courts/statewide/">Supreme Court &amp; Court of Criminal Appeals</a></h3><p>Texas's two courts of last resort (<a href="https://tcss.legis.texas.gov/resources/cn/htm/cn.5.htm#5.3">Tex. Const. art. V §§3, 5</a>). Seven seats on the 2026 ballot, all contested (<a href="https://www.bellcountytx.com/departments/elections/ballot_samples.php">Bell County ballot samples</a>).</p></div>
<div class="card"><h3><a href="/courts/appeals/">Courts of Appeals</a></h3><p>The Third Court (Austin) hears Bell County appeals (<a href="https://tcss.legis.texas.gov/resources/gv/htm/gv.22.htm#22.201">Gov't Code §22.201(d)</a>; <a href="https://www.txcourts.gov/3rdcoa/">Texas Courts</a>); the Fifteenth hears appeals involving the state and the business court (<a href="https://tcss.legis.texas.gov/resources/gv/htm/gv.22.htm#22.220">§22.220(d)</a>; <a href="https://tcss.legis.texas.gov/resources/gv/htm/gv.25a.htm#25A.007">§25A.007</a>). Four seats on the 2026 ballot (<a href="https://www.bellcountytx.com/departments/elections/ballot_samples.php">Bell County ballot samples</a>).</p></div>
<div class="card"><h3><a href="/courts/district/">District Courts</a></h3><p>Six courts — 27th, 146th, 169th, 264th, 426th, 478th (<a href="https://tcss.legis.texas.gov/resources/gv/htm/gv.24.htm#24.129">Gov't Code §24.129</a>) — plus associate and visiting judges.</p></div>
<div class="card"><h3><a href="/courts/county/">County Courts at Law &amp; County Judge</a></h3><p>Three statutory courts (<a href="https://tcss.legis.texas.gov/resources/gv/htm/gv.25.htm#25.0161">Gov't Code §25.0161</a>) and the constitutional County Judge (<a href="https://tcss.legis.texas.gov/resources/cn/htm/cn.5.htm#5.15">Tex. Const. art. V §15</a>).</p></div>
<div class="card"><h3><a href="/courts/jp/">Justices of the Peace</a></h3><p>Six precinct seats (<a href="https://www.bellcountytx.com/county_government/justice_of_the_peace/precinct_1/index.php">Bell County JP Pct 1</a>, <a href="https://www.bellcountytx.com/county_government/justice_of_the_peace/precinct_2/index.php">Pct 2</a>, <a href="https://www.bellcountytx.com/county_government/justice_of_the_peace/precinct_3_place_1/index.php">Pct 3 Pl 1</a>, <a href="https://www.bellcountytx.com/county_government/justice_of_the_peace/precinct_3_place_2/index.php">Pct 3 Pl 2</a>, <a href="https://www.bellcountytx.com/county_government/justice_of_the_peace/precinct_4_place_1/index.php">Pct 4 Pl 1</a>, <a href="https://www.bellcountytx.com/county_government/justice_of_the_peace/precinct_4_place_2/index.php">Pct 4 Pl 2</a>); Precinct 4, Place 2 is the county's only contested judicial race in 2026 (<a href="https://www.bellcountytx.com/departments/elections/ballot_samples.php">Bell County ballot samples</a>; <a href="https://kdhnews.com/centerforpolitics/cox-and-gonzalez-participate-in-justice-of-the-peace-forum-ahead-of-nov-3-election/article_f3226aea-4314-4639-9f1d-804bfbe9c839.html">KDH</a>).</p></div>
<div class="card"><h3><a href="/nov-3-2026-ballot-guide/">Nov. 3, 2026 Ballot</a></h3><p>The 19 judicial races and two clerk races on a Killeen ballot, contested and unopposed (<a href="https://www.bellcountytx.com/departments/elections/ballot_samples.php">Bell County ballot samples</a>).</p></div>
</div>

## County Judge

| Office | Judge | Status |
|--------|-------|--------|
{% for j in site.candidates %}{% if j.path contains "texas/bell_county/david_blackburn" %}| {{ j.office }} | **[{{ j.title }}]({{ j.url }})** | Incumbent; unopposed, Nov. 3, 2026 ([Bell County ballot samples](https://www.bellcountytx.com/departments/elections/ballot_samples.php); [KDH](https://kdhnews.com/news/region/patterson-to-follow-in-stepfathers-justice-of-the-peace-footsteps-blackburn-keeps-county-judge-seat/article_95f7afcb-3ab6-5651-9b0b-d42467c264f5.html)) |
{% endif %}{% endfor %}

## District Courts

{% include bench-table.html group="district" %}

## County Courts at Law

{% include bench-table.html group="county" %}

## Justices of the Peace

{% include bench-table.html group="jp" %}

## Statewide and appellate seats on the Bell County ballot

{% assign appellate = site.candidates | where_exp: "j", "j.path contains 'courts/appellate/'" | sort: "ballot_order" %}
| Court | Seat | Candidate | Party | Status |
|-------|------|-----------|-------|--------|
{% for j in appellate %}| {{ j.office | split: ", " | first }} | {{ j.seat }} | **[{{ j.title }}]({{ j.url }})** | {{ j.party }} | {% if j.incumbent %}Incumbent{% else %}Candidate{% endif %} |
{% endfor %}

Former judges, past candidates, associate judges and visiting senior judges are listed on each tier's page. Court addresses and phone numbers are in the [court directory](/court-directory/).
