---
layout: default
title: Sources
permalink: /advertise/
hero: true
hero_title: "Where our information comes from"
hero_subtitle: "This site carries no paid advertising"
description: "Legal Luminary carries no paid advertising. Every judicial profile and election page is built from public news reporting and official records, listed here."
verified_at: 2026-11-01
robots: index,follow
---

<p class="intro-text">
Legal Luminary no longer publishes sponsored listings for attorneys, notaries, process servers or other legal services. The sidebar space those advertisements occupied now lists the sources behind the site's judicial profiles and election coverage, so readers can check the reporting for themselves.
</p>

## News coverage we rely on

{% for s in site.data.news_sources.news %}
- **[{{ s.name }}]({{ s.url }})** — {{ s.note }}
{%- endfor %}

## Official records

{% for s in site.data.news_sources.official %}
- **[{{ s.name }}]({{ s.url }})** — {{ s.note }}
{%- endfor %}

## How citations work on this site

Every factual statement on a judge or candidate profile links to the article or record that supports it. Each profile's **In the News** panel repeats those citations as a reading list. Statements that have not yet been matched to a public source are marked as unverified rather than presented as fact. Corrections are logged on the [corrections page](/corrections/).

See the [Nov. 3, 2026 ballot guide](/nov-3-2026-ballot-guide/) for every judicial race on the Killeen ballot and the [Bell County judicial officers directory](/candidates/courts/) for current judges.
