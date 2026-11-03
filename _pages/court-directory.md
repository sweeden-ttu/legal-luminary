---
layout: default
title: Court Directory
permalink: /court-directory/
hero: true
hero_title: "Bell County Court Directory"
hero_subtitle: "Phone numbers, addresses, judges, and officials for every court in Bell County"
description: "Complete Bell County court directory. District Courts, County Courts at Law, Justice of the Peace, Municipal Courts, and county officials with phone numbers and addresses."
verified_at: 2026-02-19
source_url: "https://www.bellcountytx.com/"
---

{% assign dir = site.data.bell_county_directory %}

<p class="intro-text">
This directory provides contact information for every court and key government office in Bell County, Texas. Information is verified against official county sources. If you are an attorney, defendant, plaintiff, or citizen needing to reach a court or official, use the phone numbers and addresses below.
</p>

<div class="info-box">
<h4>{{ dir.courthouse.name }}</h4>
<p>{{ dir.courthouse.address }}<br>
Main Phone: <a href="tel:+12549335100">{{ dir.courthouse.phone }}</a><br>
<a href="{{ dir.courthouse.website }}" target="_blank" rel="noopener noreferrer">{{ dir.courthouse.website }}</a></p>
</div>

## County Officials

| Office | Name | Phone | Role |
|--------|------|-------|------|
{% for official in dir.county_officials %}{% assign o = official[1] %}| **{{ o.title }}** | {{ o.name }} | [{{ o.phone }}](tel:{{ o.phone | replace: ' ', '' | replace: '(', '' | replace: ')', '' | replace: '-', '' | prepend: '+1' }}) | {{ o.role }} |
{% endfor %}

## District Courts

District courts have original jurisdiction in felony criminal cases ([Code Crim. Proc. art. 4.05](https://tcss.legis.texas.gov/resources/cr/htm/cr.4.htm#4.05)) and in civil matters where the amount in controversy exceeds $500 ([Gov't Code §24.007](https://tcss.legis.texas.gov/resources/gv/htm/gv.24.htm#24.007)). The six district courts with jurisdiction in Bell County ([Gov't Code §24.129](https://tcss.legis.texas.gov/resources/gv/htm/gv.24.htm#24.129)) sit at the Bell County Justice Center, 1201 Huey Road, Belton, TX 76513 ([Bell County](https://www.bellcountytx.com/county_government/district_courts/426th_district_court/index.php)).

<div class="cards-grid two-columns">
{% for court in dir.district_courts %}
<div class="card">
<h3>{{ court.name }}</h3>
<p><strong>{{ court.judge }}</strong></p>
<p>Phone: <a href="tel:{{ court.phone | replace: ' ', '' | replace: '(', '' | replace: ')', '' | replace: '-', '' | prepend: '+1' }}">{{ court.phone }}</a></p>
<p class="card-meta">{{ court.location }}</p>
</div>
{% endfor %}
</div>

## County Courts at Law

County courts have original jurisdiction of misdemeanors not within the exclusive jurisdiction of justice courts ([Code Crim. Proc. art. 4.07](https://tcss.legis.texas.gov/resources/cr/htm/cr.4.htm#4.07)); statutory county courts hear civil cases where the amount in controversy exceeds $500 but not $325,000 ([Gov't Code §25.0003(c)](https://tcss.legis.texas.gov/resources/gv/htm/gv.25.htm#25.0003)) and appeals from justice courts ([Civ. Prac. & Rem. Code §51.001](https://tcss.legis.texas.gov/resources/cp/htm/cp.51.htm#51.001)). Bell County's three courts at law ([Gov't Code §25.0161](https://tcss.legis.texas.gov/resources/gv/htm/gv.25.htm#25.0161)) sit at the Bell County Justice Center; County Court at Law No. 1 also serves as the probate and mental health court ([Bell County](https://www.bellcountytx.com/county_government/county_courts/court_at_law_1/index.php)).

<div class="cards-grid">
{% for court in dir.county_courts_at_law %}
<div class="card">
<h3>{{ court.name }}</h3>
<p><strong>{{ court.judge }}</strong></p>
<p>Phone: <a href="tel:{{ court.phone | replace: ' ', '' | replace: '(', '' | replace: ')', '' | replace: '-', '' | prepend: '+1' }}">{{ court.phone }}</a></p>
</div>
{% endfor %}
</div>

## Justice of the Peace Courts

Justice courts handle criminal cases punishable by fine only ([Code Crim. Proc. art. 4.11](https://tcss.legis.texas.gov/resources/cr/htm/cr.4.htm#4.11)), civil cases in which the amount in controversy is not more than $20,000 ([Gov't Code §27.031](https://tcss.legis.texas.gov/resources/gv/htm/gv.27.htm#27.031)), evictions ([Prop. Code §24.004](https://tcss.legis.texas.gov/resources/pr/htm/pr.24.htm#24.004)) and truancy cases ([Family Code §65.004](https://tcss.legis.texas.gov/resources/fa/htm/fa.65.htm#65.004)).

<div class="cards-grid two-columns">
{% for jp in dir.justice_of_the_peace %}
<div class="card">
<h3>{{ jp.name }}</h3>
<p><strong>{{ jp.judge }}</strong></p>
<p>Phone: <a href="tel:{{ jp.phone | replace: ' ', '' | replace: '(', '' | replace: ')', '' | replace: '-', '' | prepend: '+1' }}">{{ jp.phone }}</a></p>
{% if jp.email %}<p>Email: <a href="mailto:{{ jp.email }}">{{ jp.email }}</a></p>{% endif %}
<p class="card-meta">{{ jp.location }}</p>
</div>
{% endfor %}
</div>

## Municipal Courts

Municipal courts have exclusive original jurisdiction within city limits over cases arising under city ordinances ([Code Crim. Proc. art. 4.14](https://tcss.legis.texas.gov/resources/cr/htm/cr.4.htm#4.14)); the Killeen Municipal Court also hears Class C misdemeanors ([City of Killeen](https://killeentexas.gov/172/Municipal-Court)).

<div class="cards-grid two-columns">
{% for court in dir.municipal_courts %}
<div class="card">
<h3>{{ court.name }}</h3>
<p>{{ court.address }}</p>
<p>Phone: <a href="tel:{{ court.phone | replace: ' ', '' | replace: '(', '' | replace: ')', '' | replace: '-', '' | prepend: '+1' }}">{{ court.phone }}</a></p>
{% if court.website %}<p><a href="{{ court.website }}" target="_blank" rel="noopener noreferrer">Website</a></p>{% endif %}
</div>
{% endfor %}
</div>

## Online Resources

<div class="info-box">
<h4>{{ dir.key_resources.odyssey_portal.name }}</h4>
<p>{{ dir.key_resources.odyssey_portal.description }}<br>
<a href="{{ dir.key_resources.odyssey_portal.url }}" target="_blank" rel="noopener noreferrer">{{ dir.key_resources.odyssey_portal.url }}</a></p>
</div>

<div class="info-box">
<h4>{{ dir.key_resources.online_payments.name }}</h4>
<p>{{ dir.key_resources.online_payments.description }}<br>
<a href="{{ dir.key_resources.online_payments.url }}" target="_blank" rel="noopener noreferrer">{{ dir.key_resources.online_payments.url }}</a></p>
</div>

## Service Areas

{% for area in dir.service_areas %}
### {{ area.name }} — {{ area.type }}

{{ area.description }}

{% if area.key_facilities.size > 0 %}**Key Facilities:** {{ area.key_facilities | join: ", " }}{% endif %}

{% endfor %}

<div class="legal-notice">
<strong>Note:</strong> Court contact information is verified against official Bell County sources. Phone numbers and personnel may change. For the most current information, visit <a href="https://www.bellcountytx.com" target="_blank" rel="noopener noreferrer">bellcountytx.com</a> or call the main courthouse line at (254) 933-5100.
</div>
