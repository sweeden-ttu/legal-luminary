---
layout: default
title: "Bell County Judicial Officers"
description: "Complete directory of all current, former, and visiting judicial officers in Bell County, Texas"
last_updated: 2026-06-09
---

{% assign all = site.candidates | where_exp: "item", "item.path contains 'courts/'" | where_exp: "item", "item.path != 'collections/_candidates/courts/index.md'" %}

{% assign district = all | where_exp: "i", "i.path contains 'courts/district/'" %}
{% assign county = all | where_exp: "i", "i.path contains 'courts/county/'" %}
{% assign jp = all | where_exp: "i", "i.path contains 'courts/jp/'" %}
{% assign associate = all | where_exp: "i", "i.path contains 'courts/associate/'" %}
{% assign senior = all | where_exp: "i", "i.path contains 'courts/senior/'" %}

## District Courts — Current Judges

| Court | Judge | Status |
|-------|-------|--------|
{% for j in district %}{% unless j.title contains "Former" or j.title contains "(Former)" or j.election_status == "former" or j.notes contains "Former" or j.notes contains "Retired" or j.notes contains "preceded" or j.notes contains "Preceded" or j.office contains "Former" %}| {{ j.office }} | [{{ j.title }}]({{ j.url }}) | {% if j.election_status == "general_2026" %}Up for election **2026**{% else %}Incumbent{% endif %} |
{% endunless %}{% endfor %}

### Former District Judges

| Judge | Court |
|-------|-------|
{% for j in district %}{% if j.title contains "Former" or j.election_status == "former" or j.notes contains "Former" or j.notes contains "Retired" or j.notes contains "preceded" or j.notes contains "Preceded" or j.office contains "Former" %}| [{{ j.title }}]({{ j.url }}) | {{ j.office }} |
{% endif %}{% endfor %}

## County Courts at Law

| Court | Judge | Status |
|-------|-------|--------|
{% for j in county %}{% unless j.title contains "Former" or j.office contains "Former" or j.election_status == "former" %}| {{ j.office }} | [{{ j.title }}]({{ j.url }}) | {% if j.election_status == "general_2026" and j.incumbent %}Incumbent, up **2026**{% elsif j.election_status == "general_2026" and j.incumbent == false %}Candidate{% else %}{{ j.notes }}{% endif %} |
{% endunless %}{% endfor %}

### Former County Court Judges

<table class="table">
  <thead>
    <tr>
      <th>Judge</th>
      <th>Court</th>
    </tr>
  </thead>
  <tbody>
    {% for j in county %}
      {% if j.title contains "Former" or j.office contains "Former" or j.election_status == "former" %}
      <tr>
        <td><strong><a href="{{ j.url }}">{{ j.title }}</a></strong></td>
        <td>{{ j.office }}</td>
      </tr>
      {% endif %}
    {% endfor %}
  </tbody>
</table>

## Justices of the Peace

| Precinct | Judge | Status |
|----------|-------|--------|
{% for j in jp %}| {{ j.office }} | [{{ j.title }}]({{ j.url }}) | {% if j.incumbent %}Incumbent{% else %}Candidate{% endif %} |
{% endfor %}

## Associate Judges & Magistrates

| Name | Title |
|------|-------|
{% for j in associate %}| [{{ j.title }}]({{ j.url }}) | {{ j.office }} |
{% endfor %}

## Visiting Senior Judges

| Name | Title |
|------|-------|
{% for j in senior %}| [{{ j.title }}]({{ j.url }}) | {{ j.office }} |
{% endfor %}

---

*Last updated: June 9, 2026. Source: Bell County official website and Odyssey court case records. Many associate judges listed here appear in Odyssey electronic case records; specific court assignments could not be independently confirmed from publicly available county sources.*
