---
layout: default
title: "Bell County Courts at Law and County Judge"
permalink: /courts/county/
description: "Bell County's three County Courts at Law and the constitutional County Judge, with the judges who hold them, terms and elections."
verified_at: 2026-11-01
---

# County Courts at Law and County Judge

<p class="intro-text">Bell County has three statutory County Courts at Law, which hear misdemeanors, family, probate, juvenile and civil cases, plus the constitutional County Judge, who presides over the Commissioners Court. All four are elected countywide to four-year terms, and all four are on the November 3, 2026 ballot with unopposed Republican nominees.</p>

## County Judge

| Office | Judge | Status |
|---|---|---|
{% for j in site.candidates %}{% if j.path contains "texas/bell_county/david_blackburn" %}| {{ j.office }} | **[{{ j.title }}]({{ j.url }})** | Incumbent; unopposed Republican nominee, Nov. 3, 2026 |
{% endif %}{% endfor %}

## County Courts at Law — current bench

{% include bench-table.html group="county" %}

## Former county court judges

{% include bench-table.html group="county" former="true" %}

<p><a href="/court-directory/" class="btn btn-secondary">Court addresses and phone numbers</a></p>
