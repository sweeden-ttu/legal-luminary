---
layout: default
title: Bell County Attorney Directory
permalink: /attorneys/
hero: true
hero_title: "Bell County Attorney Directory"
hero_subtitle: "Law firms and attorneys with offices in Killeen, Temple, Belton and Harker Heights"
description: "Directory of law firms and attorneys practicing in Bell County, Texas, with each firm's website, attorneys, practice areas and how long the firm has been in practice. Compiled from the firms' own websites; no paid listings."
verified_at: 2026-11-01
robots: index,follow
---

{% assign firms = site.data.attorneys_bell_county.firms | sort: "firm" %}
{% assign cities = firms | map: "city" | uniq | sort %}

<p class="intro-text">
This directory lists {{ firms | size }} law firms with offices in Bell County. Every entry — firm name, website, attorneys, practice areas and how long the firm has been in practice — was read from the firm's own website on the date shown; nothing here is a paid listing, and inclusion is not an endorsement. Firms are listed alphabetically within each city. To correct or add an entry, see the <a href="/corrections/">corrections page</a>.
</p>

<div class="info-box">
<h4>Checking a lawyer's license</h4>
<p>Look up any attorney in the <a href="https://www.texasbar.com/AM/Template.cfm?Section=Find_A_Lawyer" target="_blank" rel="noopener noreferrer">State Bar of Texas "Find a Lawyer" directory</a> before relying on a listing here. Years listed below are the firm's own statements about when it was founded, not a measure of any individual attorney's experience.</p>
</div>

<nav class="attorney-dir__jumps" aria-label="Jump to city">
  <strong>Jump to:</strong>
  {% for c in cities %}<a href="#{{ c | slugify }}">{{ c }}</a>{% unless forloop.last %} · {% endunless %}{% endfor %}
</nav>

<div class="attorney-dir__filter">
  <label for="practice-filter"><strong>Filter by practice area:</strong></label>
  <select id="practice-filter">
    <option value="">All practice areas</option>
    {% assign areas = "" | split: "" %}
    {% for f in firms %}{% for a in f.practice_areas %}{% assign areas = areas | push: a %}{% endfor %}{% endfor %}
    {% assign areas = areas | uniq | sort %}
    {% for a in areas %}<option value="{{ a | slugify }}">{{ a }}</option>{% endfor %}
  </select>
</div>

{% for c in cities %}
<h2 id="{{ c | slugify }}">{{ c }}</h2>
<div class="attorney-dir__list">
{% for f in firms %}{% if f.city == c %}
{% assign tags = "" %}{% for a in f.practice_areas %}{% assign tags = tags | append: " " | append: a | slugify %}{% endfor %}
<article class="attorney-card" data-practice="{{ tags | strip }}">
  <header class="attorney-card__header">
    <h3 class="attorney-card__name">{% if f.website %}<a href="{{ f.website }}" target="_blank" rel="noopener noreferrer">{{ f.firm }}</a>{% else %}{{ f.firm }}{% endif %}</h3>
    {% if f.founded %}{% assign yrs = site.time | date: "%Y" | minus: f.founded %}<span class="attorney-card__years">Founded {{ f.founded }} · {{ yrs }} years</span>{% elsif f.years_in_practice_claim %}<span class="attorney-card__years">Firm's statement: {{ f.years_in_practice_claim }}</span>{% endif %}
  </header>
  {% if f.practice_areas %}<p class="attorney-card__areas">{% for a in f.practice_areas %}<span class="attorney-card__tag">{{ a }}</span>{% endfor %}</p>{% endif %}
  {% if f.attorneys and f.attorneys.size > 0 %}
  <p class="attorney-card__label">Attorneys</p>
  <ul class="attorney-card__attorneys">
    {% for p in f.attorneys %}<li>{{ p.name }}{% if p.title %} <span class="attorney-card__title">— {{ p.title }}</span>{% endif %}</li>{% endfor %}
  </ul>
  {% else %}
  <p class="attorney-card__label">Attorneys: not listed on the firm's website</p>
  {% endif %}
  <p class="attorney-card__contact">
    {% if f.address %}{{ f.address }}{% endif %}
    {% if f.phone %}{% if f.address %} · {% endif %}<a href="tel:+1{{ f.phone | replace: '(', '' | replace: ')', '' | replace: ' ', '' | replace: '-', '' | replace: '.', '' }}">{{ f.phone }}</a>{% endif %}
    {% if f.website %}{% if f.address or f.phone %} · {% endif %}<a href="{{ f.website }}" target="_blank" rel="noopener noreferrer">{{ f.website | replace: "https://", "" | replace: "http://", "" | replace: "www.", "" | split: "/" | first }}</a>{% endif %}
  </p>
  {% if f.source %}<p class="attorney-card__source">Source: <a href="{{ f.source }}" target="_blank" rel="noopener noreferrer">firm website</a>, checked {{ f.verified | default: page.verified_at }}.</p>{% endif %}
</article>
{% endif %}{% endfor %}
</div>
{% endfor %}

<p class="attorney-dir__note"><em>Listings were compiled from each firm's public website on {{ page.verified_at | date: "%B %-d, %Y" }}. Firm names, attorney rosters and practice areas change; confirm current details with the firm and the State Bar of Texas before relying on them.</em></p>

<script>
(function () {
  var sel = document.getElementById('practice-filter');
  if (!sel) return;
  sel.addEventListener('change', function () {
    var v = sel.value;
    document.querySelectorAll('.attorney-card').forEach(function (card) {
      var tags = (card.getAttribute('data-practice') || '').split(' ');
      card.style.display = (!v || tags.indexOf(v) !== -1) ? '' : 'none';
    });
    document.querySelectorAll('.attorney-dir__list').forEach(function (list) {
      var visible = Array.prototype.some.call(list.querySelectorAll('.attorney-card'), function (c) { return c.style.display !== 'none'; });
      list.style.display = visible ? '' : 'none';
      var h = list.previousElementSibling; if (h && h.tagName === 'H2') h.style.display = visible ? '' : 'none';
    });
  });
})();
</script>
