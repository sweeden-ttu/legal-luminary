---
layout: default
title: "Bell County Judicial Officers"
permalink: /candidates/courts/
description: "Complete directory of all current, former, and visiting judicial officers in Bell County, Texas"
last_updated: 2026-06-09
---

<h1>Bell County Judicial Officers</h1>

<div style="display:flex;gap:24px;flex-wrap:wrap;margin:16px 0">
  <div style="text-align:center">
    <img src="/assets/images/headshots/gregory_johnson.png" alt="Gregory Johnson" style="width:180px;height:220px;object-fit:cover;border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,0.15)">
    <div style="margin-top:6px"><strong>Gregory Johnson</strong><br>JP4 Place 1</div>
  </div>
  <div style="text-align:center">
    <img src="/assets/images/headshots/nicola_james.png" alt="Nicola J. James" style="width:180px;height:220px;object-fit:cover;border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,0.15)">
    <div style="margin-top:6px"><strong>Nicola J. James</strong><br>JP4 Place 2</div>
  </div>
  <div style="text-align:center">
    <img src="/assets/images/headshots/larry_wilke.png" alt="Larry Wilkey" style="width:180px;height:220px;object-fit:cover;border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,0.15)">
    <div style="margin-top:6px"><strong>Larry Wilkey</strong><br>JP3 Place 2</div>
  </div>
</div>

<p style="font-size:0.9em;color:#555;margin:0 0 20px 0"><strong>78.1%</strong> of eviction/foreclosure cases in our dataset are filed in these three JP courts. (<a href="/methodology">Methodology</a>)</p>

## District Courts

### Current Judges

| Court | Judge | Status |
|-------|-------|--------|
{% for j in site.candidates %}{% if j.path contains "courts/district/" and j.incumbent == true and j.election_status != "former" %}| {{ j.office }} | **[{{ j.title }}]({{ j.url }})** | {% if j.election_status == "general_2026" %}Up for election **2026**{% else %}Incumbent{% endif %} |
{% endif %}{% endfor %}

## County Courts at Law

| Court | Judge | Status |
|-------|-------|--------|
{% for j in site.candidates %}{% if j.path contains "courts/county/" and j.election_status != "former" %}| {{ j.office }} | **[{{ j.title }}]({{ j.url }})** | {% if j.incumbent == false %}Candidate{% elsif j.election_status == "general_2026" %}Up for election **2026**{% else %}Incumbent{% endif %} |
{% endif %}{% endfor %}

## Justices of the Peace

| Precinct | Judge | Status |
|----------|-------|--------|
{% for j in site.candidates %}{% if j.path contains "courts/jp/" %}| {{ j.office }} | **[{{ j.title }}]({{ j.url }})**{% if j.rubber_stamp %} <span style="display:inline-block;font-size:0.8em;border:1px solid #c00;border-radius:3px;padding:0 3px;color:#c00;font-weight:bold;margin-left:4px;transform:rotate(-8deg);text-transform:uppercase;line-height:1.2" title="Eviction case judge">STAMP</span>{% endif %} | {% if j.incumbent %}Incumbent{% else %}Candidate{% endif %} |
{% endif %}{% endfor %}

## Visiting Senior Judges

| Name | Title |
|------|-------|
{% for j in site.candidates %}{% if j.path contains "courts/senior/" %}| **[{{ j.title }}]({{ j.url }})** | {{ j.office }} |
{% endif %}{% endfor %}

---

*Last updated: June 9, 2026. Source: Bell County official website and Odyssey court case records. Many associate judges listed here appear in Odyssey electronic case records; specific court assignments could not be independently confirmed from publicly available county sources.*
