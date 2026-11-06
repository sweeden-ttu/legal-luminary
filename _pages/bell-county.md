---
layout: default
article_feed: bell-county-articles
title: Bell County Law
permalink: /bell-county/
hero: true
hero_title: "Bell County Legal Information"
hero_subtitle: "Local courts, procedures, and resources for Central Texas residents"
description: "Bell County judges directory with verified phone numbers, which court handles which case, and local legal resources for Killeen, Temple, and Belton area residents."
news_city: bell-county-news
hide_sidebar_listings: true
hide_ad_label: true
---
{% assign bc = site.data.bell_county_courts %}
<style>
.bc-quick{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1rem;margin:1.5rem 0 .75rem}
.bc-quick>div{background:var(--cream,#f8f6f1);border:1px solid var(--gray-light,#e8e6e1);border-left:4px solid var(--gold,#c9a227);border-radius:8px;padding:.9rem 1rem;line-height:1.5}
.bc-label{display:block;font-size:.75rem;font-weight:700;letter-spacing:.04em;text-transform:uppercase;color:var(--gray-dark,#374151)}
.bc-muted{color:var(--gray-dark,#374151);font-size:.9rem}
.bc-muted a{white-space:nowrap}
.bc-verified{font-size:.9rem;color:var(--gray-dark,#374151);margin:0 0 1.5rem}
.bc-jump{display:flex;flex-wrap:wrap;gap:.5rem;margin:0 0 2rem;padding:.75rem 0;border-top:1px solid var(--gray-light,#e8e6e1);border-bottom:1px solid var(--gray-light,#e8e6e1)}
.bc-jump a{padding:.35rem .75rem;border:1px solid var(--navy-light,#2d5a87);border-radius:999px;font-size:.9rem;text-decoration:none;color:var(--navy,#1a3a5c)}
.bc-jump a:hover,.bc-jump a:focus{background:var(--navy,#1a3a5c);color:#fff}
.bc-table{width:100%;border-collapse:collapse;margin:0 0 2rem;font-size:.95rem}
.bc-table caption{text-align:left;font-weight:700;font-size:1.15rem;color:var(--navy-dark,#0f233c);padding:0 0 .5rem}
.bc-table th,.bc-table td{text-align:left;vertical-align:top;padding:.7rem .75rem;border-bottom:1px solid var(--gray-light,#e8e6e1)}
.bc-table thead th{background:var(--navy-dark,#0f233c);color:#fff;font-size:.8rem;letter-spacing:.04em;text-transform:uppercase}
.bc-table tbody th{background:transparent;color:var(--text,#1f2937);font-family:inherit;font-size:inherit;font-weight:700;text-transform:none;letter-spacing:normal}
.bc-table tbody tr:hover th{background:var(--cream,#f8f6f1)}
.bc-table tbody th a{color:var(--navy,#1a3a5c)}
.bc-tel{white-space:nowrap;font-weight:700}
.bc-fax,.bc-note,.bc-src{display:block;font-size:.8rem;color:var(--gray-dark,#374151);margin-top:.2rem}
.bc-src a{color:var(--gray-dark,#374151)}
.bc-badge{display:inline-block;padding:.15rem .55rem;border-radius:999px;background:#fdf6dc;border:1px solid var(--gold-dark,#a88620);color:#5c4a0f;font-size:.8rem;font-weight:700;text-decoration:none;white-space:nowrap}
.bc-offices{list-style:none;padding:0;margin:0 0 2rem}
.bc-offices li{padding:.9rem 0;border-bottom:1px solid var(--gray-light,#e8e6e1)}
.bc-sources ol{padding-left:2rem}
.bc-sources li{margin:.3rem 0;font-size:.9rem;overflow-wrap:anywhere}
@media (max-width:640px){
.bc-table thead{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
.bc-table,.bc-table tbody,.bc-table tr,.bc-table th,.bc-table td{display:block;width:100%;box-sizing:border-box}
.bc-table tbody tr{border:1px solid var(--gray-light,#e8e6e1);border-radius:8px;margin:0 0 1rem;padding:.5rem .25rem;background:#fff}
.bc-table th,.bc-table td{border:0;padding:.35rem .75rem}
.bc-table tbody th{font-size:1.05rem}
.bc-table td[data-label]::before{content:attr(data-label);display:block;font-size:.72rem;font-weight:700;letter-spacing:.04em;text-transform:uppercase;color:var(--gray-dark,#374151)}
.bc-tel{display:inline-block;min-height:44px;line-height:44px;padding:0 1rem;border-radius:8px;background:var(--navy,#1a3a5c);color:#fff !important;text-decoration:none}
.bc-table caption{display:block;width:100%;padding:0 0 .75rem}
}
</style>

<p class="intro-text">
This page lists the state and county courts that sit in Bell County, Texas, which kinds of cases each hears, and how to reach them.
</p>

<div class="bc-quick" aria-label="Quick contacts">
<div><span class="bc-label">Courthouse</span><strong>{{ bc.courthouse.name }}</strong><br>{{ bc.courthouse.address }}<br><span class="bc-muted">District Courts and County Courts at Law</span></div>
<div><span class="bc-label">{{ bc.county_clerk.name }}</span><a class="bc-tel" href="tel:{{ bc.county_clerk.tel }}">{{ bc.county_clerk.phone }}</a><br><span class="bc-muted">{{ bc.county_clerk.note }}</span></div>
{% for o in bc.offices %}{% if o.phone %}<div><span class="bc-label">{{ o.title }}</span><a class="bc-tel" href="tel:{{ o.tel }}">{{ o.phone }}</a><br><span class="bc-muted">{{ o.name }}</span></div>{% endif %}{% endfor %}
</div>

<p class="bc-verified">Judge names and phone numbers on this page were checked against the sources listed at the bottom on {{ bc.verified_on_text }}. Numbers that could not be confirmed are left out. <a href="mailto:scott_weeden@fronts.cloud?subject=Bell%20County%20page%20correction">Report a correction</a>.</p>

<nav class="bc-jump" aria-label="On this page">
<a href="#which-court">Which court?</a>
<a href="#judges">Judges directory</a>
<a href="#prosecutors">Prosecutors and clerk</a>
<a href="#municipal">Municipal courts</a>
<a href="#sources">Sources</a>
</nav>

<h2 id="which-court">Which Court Handles My Case?</h2>

<p>Each row links to the statute that sets the court's jurisdiction.</p>

<table class="bc-table">
<thead><tr><th scope="col">Court</th><th scope="col">Handles</th></tr></thead>
<tbody>
<tr><th scope="row">District Courts (6) (<a href="https://tcss.legis.texas.gov/resources/gv/htm/gv.24.htm#24.129">Gov't Code §24.129</a>)</th><td data-label="Handles">Felony criminal cases (<a href="https://tcss.legis.texas.gov/resources/cr/htm/cr.4.htm#4.05">Code Crim. Proc. art. 4.05</a>); civil matters where the amount in controversy exceeds $500 (<a href="https://tcss.legis.texas.gov/resources/gv/htm/gv.24.htm#24.007">Gov't Code §24.007</a>)</td></tr>
<tr><th scope="row">County Courts at Law (3) (<a href="https://tcss.legis.texas.gov/resources/gv/htm/gv.25.htm#25.0161">Gov't Code §25.0161</a>)</th><td data-label="Handles">Misdemeanors not within the exclusive jurisdiction of justice courts (<a href="https://tcss.legis.texas.gov/resources/cr/htm/cr.4.htm#4.07">Code Crim. Proc. art. 4.07</a>); civil cases over $500 and up to $325,000 (<a href="https://tcss.legis.texas.gov/resources/gv/htm/gv.25.htm#25.0003">Gov't Code §25.0003(c)</a>); appeals from justice courts (<a href="https://tcss.legis.texas.gov/resources/cp/htm/cp.51.htm#51.001">Civ. Prac. &amp; Rem. Code §51.001</a>); probate and mental health in Court at Law No. 1 (<a href="https://www.bellcountytx.com/county_government/county_courts/court_at_law_1/index.php">Bell County</a>)</td></tr>
<tr><th scope="row">Justice of the Peace Courts (6 seats in 4 precincts: <a href="https://www.bellcountytx.com/county_government/justice_of_the_peace/precinct_1/index.php">Bell County JP Pct 1</a>, <a href="https://www.bellcountytx.com/county_government/justice_of_the_peace/precinct_2/index.php">Pct 2</a>, <a href="https://www.bellcountytx.com/county_government/justice_of_the_peace/precinct_3_place_1/index.php">Pct 3 Pl 1</a>, <a href="https://www.bellcountytx.com/county_government/justice_of_the_peace/precinct_3_place_2/index.php">Pct 3 Pl 2</a>, <a href="https://www.bellcountytx.com/county_government/justice_of_the_peace/precinct_4_place_1/index.php">Pct 4 Pl 1</a>, <a href="https://www.bellcountytx.com/county_government/justice_of_the_peace/precinct_4_place_2/index.php">Pct 4 Pl 2</a>)</th><td data-label="Handles">Criminal cases punishable by fine only (<a href="https://tcss.legis.texas.gov/resources/cr/htm/cr.4.htm#4.11">Code Crim. Proc. art. 4.11</a>); civil cases up to $20,000 (<a href="https://tcss.legis.texas.gov/resources/gv/htm/gv.27.htm#27.031">Gov't Code §27.031</a>); evictions (<a href="https://tcss.legis.texas.gov/resources/pr/htm/pr.24.htm#24.004">Prop. Code §24.004</a>); truancy (<a href="https://tcss.legis.texas.gov/resources/fa/htm/fa.65.htm#65.004">Family Code §65.004</a>)</td></tr>
<tr><th scope="row">Municipal Courts</th><td data-label="Handles">Cases arising under city ordinances (<a href="https://tcss.legis.texas.gov/resources/cr/htm/cr.4.htm#4.14">Code Crim. Proc. art. 4.14</a>); Killeen's court also hears Class C misdemeanors (<a href="https://killeentexas.gov/172/Municipal-Court">City of Killeen</a>)</td></tr>
</tbody>
</table>

<h2 id="judges">Bell County Judges Directory</h2>

<p>All District Courts and County Courts at Law sit at the {{ bc.courthouse.name }}, {{ bc.courthouse.address }} (<a href="https://www.bellcountytx.com/county_government/district_courts/426th_district_court/index.php">Bell County</a>). District judges serve four-year terms (<a href="https://tcss.legis.texas.gov/resources/cn/htm/cn.5.htm#5.7">Tex. Const. art. V §7</a>). Each court name links to its official county page; the small numbers link to the sources for that row.</p>

{% assign groups = "district|District Court Judges,county|County Court at Law Judges" | split: "," %}
{% for g in groups %}{% assign gp = g | split: "|" %}{% assign gcourts = bc.courts | where: "group", gp[0] %}
<table class="bc-table">
<caption>{{ gp[1] }}</caption>
<thead><tr><th scope="col">Court</th><th scope="col">Judge</th><th scope="col">Phone</th><th scope="col">Next election</th></tr></thead>
<tbody>
{% for c in gcourts %}<tr>
<th scope="row"><a href="{{ c.official_url }}" target="_blank" rel="noopener noreferrer">{{ c.court }}</a><span class="bc-src">Sources: {% for sid in c.sources %}{% assign s = bc.sources | where: "id", sid | first %}<a href="#src-{{ s.n }}" aria-label="Source {{ s.n }}">{{ s.n }}</a>{% unless forloop.last %}, {% endunless %}{% endfor %}</span></th>
<td data-label="Judge">{{ c.judge }}{% if c.note %}<span class="bc-note">{{ c.note }}</span>{% endif %}</td>
<td data-label="Phone">{% if c.phone %}<a class="bc-tel" href="tel:{{ c.tel }}">{{ c.phone }}</a>{% else %}<span class="bc-muted">Call the {{ bc.county_clerk.name }}, <a href="tel:{{ bc.county_clerk.tel }}">{{ bc.county_clerk.phone }}</a></span>{% endif %}{% if c.fax %}<span class="bc-fax">Fax {{ c.fax }}</span>{% endif %}</td>
<td data-label="Next election">{% if c.ballot_2026 %}<a class="bc-badge" href="/nov-3-2026-ballot-guide/">Elected without opposition Nov. 3, 2026 (unofficial)</a> <a href="https://results.enr.clarityelections.com/TX/Bell/127475/" target="_blank" rel="noopener noreferrer">Bell County results</a>{% else %}{{ c.next_election }}{% endif %}</td>
</tr>
{% endfor %}</tbody>
</table>
{% endfor %}

<h2 id="prosecutors">Prosecutors and Clerk</h2>

<ul class="bc-offices">
{% for o in bc.offices %}<li><strong>{{ o.title }}: {{ o.name }}</strong>{% if o.phone %} · <a class="bc-tel" href="tel:{{ o.tel }}">{{ o.phone }}</a>{% endif %}<br>{{ o.role }}<span class="bc-src">Sources: {% for sid in o.sources %}{% assign s = bc.sources | where: "id", sid | first %}<a href="#src-{{ s.n }}" aria-label="Source {{ s.n }}">{{ s.n }}</a>{% unless forloop.last %}, {% endunless %}{% endfor %}</span></li>
{% endfor %}<li><strong>{{ bc.county_clerk.name }}</strong> · <a class="bc-tel" href="tel:{{ bc.county_clerk.tel }}">{{ bc.county_clerk.phone }}</a><br>{{ bc.county_clerk.note }}.<span class="bc-src">Sources: {% for sid in bc.county_clerk.sources %}{% assign s = bc.sources | where: "id", sid | first %}<a href="#src-{{ s.n }}" aria-label="Source {{ s.n }}">{{ s.n }}</a>{% unless forloop.last %}, {% endunless %}{% endfor %}</span></li>
</ul>

<h2 id="municipal">Municipal Courts</h2>

Cities in Bell County maintain their own municipal courts for cases arising under city ordinances (<a href="https://tcss.legis.texas.gov/resources/cr/htm/cr.4.htm#4.14">Code Crim. Proc. art. 4.14</a>).

**Killeen Municipal Court** — 200 E. Avenue D, Suite 1, Killeen, TX 76541; 254-501-7850; hears Class C misdemeanors and city ordinance cases ([City of Killeen](https://killeentexas.gov/172/Municipal-Court)).

## Fort Hood

The main business area of Fort Hood, the Army post near Killeen, is in Bell County; the post was named Fort Cavazos from May 9, 2023 until the name reverted to Fort Hood effective June 11, 2025 ([Wikipedia](https://en.wikipedia.org/wiki/Fort_Hood)).

<div class="cards-grid">
<div class="card">
<h3>The Bench</h3>
<p>Every elected judge in Bell County, with sourced profiles.</p>
<a href="/candidates/courts/" class="btn btn-primary">The Bell County Bench</a>
</div>

<div class="card">
<h3>Attorney Directory</h3>
<p>Law firms and attorneys with offices in Bell County, with websites and practice areas.</p>
<a href="/attorneys/" class="btn btn-primary">Attorney Directory</a>
</div>
</div>

<section class="bc-sources" aria-labelledby="sources">
<h2 id="sources">Sources</h2>
<p class="bc-muted">All sources accessed {{ bc.verified_on_text }}.</p>
{% for grp in bc.source_groups %}{% assign gsrc = bc.sources | where: "group", grp.key %}
<h3>{{ grp.title }}</h3>
<ol>
{% for s in gsrc %}<li id="src-{{ s.n }}" value="{{ s.n }}"><a href="{{ s.url }}" target="_blank" rel="noopener noreferrer">{{ s.title }}</a> — {{ s.publisher }}</li>
{% endfor %}</ol>
{% endfor %}
</section>
