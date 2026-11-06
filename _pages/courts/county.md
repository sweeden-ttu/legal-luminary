---
layout: default
title: "Bell County Courts at Law and County Judge"
permalink: /courts/county/
description: "Bell County's three County Courts at Law and the constitutional County Judge, with the judges who hold them, terms and elections."
verified_at: 2026-11-01
---

# County Courts at Law and County Judge

<p class="intro-text">Bell County has three statutory County Courts at Law (<a href="https://tcss.legis.texas.gov/resources/gv/htm/gv.25.htm#25.0161">Gov't Code §25.0161</a>), which hear misdemeanors (<a href="https://tcss.legis.texas.gov/resources/cr/htm/cr.4.htm#4.07">Code Crim. Proc. art. 4.07</a>) and civil cases where the amount in controversy is more than $500 and not more than $325,000 (<a href="https://tcss.legis.texas.gov/resources/gv/htm/gv.25.htm#25.0003">Gov't Code §25.0003(c)</a>); County Court at Law No. 1 also sits as the probate and mental health court (<a href="https://www.bellcountytx.com/county_government/county_courts/court_at_law_1/index.php">Bell County</a>). They are joined by the constitutional County Judge, who presides over the Commissioners Court (<a href="https://tcss.legis.texas.gov/resources/lg/htm/lg.81.htm#81.001">Local Gov't Code §81.001</a>). The County Judge serves a four-year term (<a href="https://tcss.legis.texas.gov/resources/cn/htm/cn.5.htm#5.15">Tex. Const. art. V §15</a>). All four offices were on the November 3, 2026 ballot with unopposed Republican nominees (<a href="https://www.bellcountytx.com/departments/elections/ballot_samples.php">Bell County ballot samples</a>), and all four were elected without opposition, according to unofficial returns (<a href="https://results.enr.clarityelections.com/TX/Bell/127475/">Bell County Elections</a>).</p>

## County Judge

| Office | Judge | Status |
|---|---|---|
{% for j in site.candidates %}{% if j.path contains "texas/bell_county/david_blackburn" %}| {{ j.office }} | **[{{ j.title }}]({{ j.url }})** | Incumbent; elected without opposition, Nov. 3, 2026 ([Bell County Elections](https://results.enr.clarityelections.com/TX/Bell/127475/), unofficial; [Bell County ballot samples](https://www.bellcountytx.com/departments/elections/ballot_samples.php); [KDH](https://kdhnews.com/news/region/patterson-to-follow-in-stepfathers-justice-of-the-peace-footsteps-blackburn-keeps-county-judge-seat/article_95f7afcb-3ab6-5651-9b0b-d42467c264f5.html)) |
{% endif %}{% endfor %}

## Nov. 3, 2026 results

{% include results-group.html group="county_judge" %}
{% include results-group.html group="county" %}

## County Courts at Law — current bench

{% include bench-table.html group="county" %}

## Former county court judges

{% include bench-table.html group="county" former="true" %}

<p><a href="/court-directory/" class="btn btn-secondary">Court addresses and phone numbers</a></p>
