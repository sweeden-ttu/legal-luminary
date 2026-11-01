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
<div class="card"><h3><a href="/courts/statewide/">Supreme Court &amp; Court of Criminal Appeals</a></h3><p>Texas's two nine-member courts of last resort, elected statewide. Seven seats on the 2026 ballot, every one contested.</p><a href="/courts/statewide/" class="btn btn-primary">Statewide courts</a></div>
<div class="card"><h3><a href="/courts/appeals/">Courts of Appeals</a></h3><p>The Third Court of Appeals in Austin hears Bell County's appeals; the Fifteenth hears state and business cases. Four seats on the 2026 ballot.</p><a href="/courts/appeals/" class="btn btn-primary">Courts of appeals</a></div>
<div class="card"><h3><a href="/courts/district/">District Courts</a></h3><p>Six state district courts at the Bell County Justice Center — the 27th, 146th, 169th, 264th, 426th and 478th — with their associate and visiting judges.</p><a href="/courts/district/" class="btn btn-primary">District courts</a></div>
<div class="card"><h3><a href="/courts/county/">County Courts at Law &amp; County Judge</a></h3><p>Three statutory county courts and the constitutional County Judge who presides over the Commissioners Court.</p><a href="/courts/county/" class="btn btn-primary">County courts</a></div>
<div class="card"><h3><a href="/courts/jp/">Justices of the Peace</a></h3><p>Six precinct courts for evictions, small claims, Class C misdemeanors and magistration — the courts most residents actually meet.</p><a href="/courts/jp/" class="btn btn-primary">Justices of the peace</a></div>
<div class="card"><h3><a href="/attorneys/">Attorney Directory</a></h3><p>The bar the bench is drawn from: {{ site.data.attorneys_bell_county.firms | size }} Bell County law firms, their attorneys, practice areas and years in practice.</p><a href="/attorneys/" class="btn btn-secondary">Attorneys</a></div>
</div>

## The Bell County bench today

{% assign cj = site.candidates | where_exp: "j", "j.path contains 'texas/bell_county/david_blackburn'" | first %}
| Court | Judge | 2026 election |
|---|---|---|
{% if cj %}| {{ cj.office }} | **[{{ cj.title }}]({{ cj.url }})** | Unopposed |
{% endif %}{% assign dist = site.candidates | where_exp: "j", "j.path contains 'courts/district/'" | where: "incumbent", true | sort: "office" %}{% for j in dist %}{% unless j.election_status == "former" %}| {{ j.office }} | **[{{ j.title }}]({{ j.url }})** | {% if j.listing_status contains "Nominee" %}Unopposed{% else %}Not up until later{% endif %} |
{% endunless %}{% endfor %}{% assign cty = site.candidates | where_exp: "j", "j.path contains 'courts/county/'" | sort: "office" %}{% for j in cty %}{% unless j.election_status == "former" %}| {{ j.office }} | **[{{ j.title }}]({{ j.url }})** | {% if j.incumbent == false %}Open seat — unopposed nominee{% elsif j.listing_status contains "Nominee" %}Unopposed{% else %}Not up until later{% endif %} |
{% endunless %}{% endfor %}{% assign jps = site.candidates | where_exp: "j", "j.path contains 'courts/jp/'" | where: "incumbent", true | sort: "office" %}{% for j in jps %}{% unless j.election_status == "former" %}{% assign st = "Not up until 2028" %}{% if j.office contains "Precinct 4, Place 2" %}{% assign st = "Contested: [Cox](/candidates/courts/jp/beatrice_bea_cox/) (R) v. [Gonzalez](/candidates/courts/jp/jessica_a_gonzalez/) (D)" %}{% elsif j.office contains "Precinct 1" %}{% assign st = "Retiring; Patrick Patterson (R) unopposed" %}{% elsif j.office contains "Precinct 3, Place 2" or j.listing_status contains "Nominee" %}{% assign st = "Unopposed" %}{% endif %}| {{ j.office }} | **[{{ j.title }}]({{ j.url }})** | {{ st }} |
{% endunless %}{% endfor %}

Full tables, former judges and candidates: [The Bell County Bench](/candidates/courts/).

## Elections

<div class="cards-grid">
<div class="card"><h3>Nov. 3, 2026 ballot guide</h3><p>All 21 judicial-branch races on a Killeen ballot — contested and unopposed — plus the hospital district tax and Killeen charter propositions.</p><a href="/nov-3-2026-ballot-guide/" class="btn btn-primary">Ballot guide</a></div>
<div class="card"><h3>How to run for judge</h3><p>Who is eligible for each bench, filing windows, fees and petition signatures in Bell County.</p><a href="/run-for-judge/" class="btn btn-secondary">Run for judge</a></div>
<div class="card"><h3>Voting in Bell County</h3><p>Early voting, polling places, mail ballots and what the county's election office publishes.</p><a href="/elections/" class="btn btn-secondary">Elections</a></div>
</div>

{% include front-page-featured-articles.html %}

## How this site works

Profiles are built from Killeen Daily Herald, Temple Daily Telegram, KWTX, KCEN, the Texas Tribune, San Antonio Report and official records such as txcourts.gov and the Governor's appointment announcements — the full list is on the [sources page](/advertise/). Claims that cannot be matched to a public source are marked unverified, and every correction is logged on the [corrections page](/corrections/). Read the [about page](/about/) for the mission and the legal basis for publishing.
