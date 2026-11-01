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
<div class="card"><h3><a href="/courts/statewide/">Supreme Court &amp; Court of Criminal Appeals</a></h3><p>Texas's two courts of last resort. Seven seats on the 2026 ballot, all contested.</p></div>
<div class="card"><h3><a href="/courts/appeals/">Courts of Appeals</a></h3><p>The Third Court (Austin) hears Bell County appeals; the Fifteenth hears state and business cases. Four seats on the 2026 ballot.</p></div>
<div class="card"><h3><a href="/courts/district/">District Courts</a></h3><p>Six courts — 27th, 146th, 169th, 264th, 426th, 478th — plus associate and visiting judges.</p></div>
<div class="card"><h3><a href="/courts/county/">County Courts at Law &amp; County Judge</a></h3><p>Three statutory courts and the constitutional County Judge.</p></div>
<div class="card"><h3><a href="/courts/jp/">Justices of the Peace</a></h3><p>Six precinct seats; Precinct 4, Place 2 is the county's only contested judicial race in 2026.</p></div>
<div class="card"><h3><a href="/nov-3-2026-ballot-guide/">Nov. 3, 2026 Ballot</a></h3><p>All 21 judicial-branch races on a Killeen ballot, contested and unopposed.</p></div>
</div>

## County Judge

| Office | Judge | Status |
|--------|-------|--------|
{% for j in site.candidates %}{% if j.path contains "texas/bell_county/david_blackburn" %}| {{ j.office }} | **[{{ j.title }}]({{ j.url }})** | Incumbent; unopposed, Nov. 3, 2026 |
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
