---
layout: default
title: "Courts of Appeals for Bell County — 3rd and 15th Districts"
permalink: /courts/appeals/
description: "The Third Court of Appeals in Austin hears appeals from Bell County; the Fifteenth Court of Appeals hears statewide business and government cases. Candidates on the Nov. 3, 2026 ballot with sourced profiles."
verified_at: 2026-11-01
---

# Courts of Appeals

<p class="intro-text">Appeals from Bell County's district and county courts go to the <strong>Third Court of Appeals</strong> in Austin, a six-justice court elected by the voters of 24 counties. The <strong>Fifteenth Court of Appeals</strong>, created in 2024, hears appeals involving the state and certain business cases from anywhere in Texas and is elected statewide. Justices serve six-year terms. Four of these seats are on the November 3, 2026 ballot.</p>

{% assign appellate = site.candidates | where_exp: "j", "j.path contains 'courts/appellate/'" | sort: "ballot_order" %}

## Third Court of Appeals — on the 2026 ballot

<div class="table-responsive"><table class="bench-table"><thead><tr><th>Seat</th><th>Candidate</th><th>Party</th><th>Status</th></tr></thead><tbody>
{% for j in appellate %}{% if j.court_group == "coa3" %}<tr><td>{{ j.seat }}</td><td><strong><a href="{{ j.url }}">{{ j.title }}</a></strong></td><td>{{ j.party }}</td><td>{% if j.incumbent %}Incumbent{% else %}Candidate{% endif %}</td></tr>
{% endif %}{% endfor %}</tbody></table></div>

## Fifteenth Court of Appeals — on the 2026 ballot

<div class="table-responsive"><table class="bench-table"><thead><tr><th>Seat</th><th>Candidate</th><th>Party</th><th>Status</th></tr></thead><tbody>
{% for j in appellate %}{% if j.court_group == "coa15" %}<tr><td>{{ j.seat }}</td><td><strong><a href="{{ j.url }}">{{ j.title }}</a></strong></td><td>{{ j.party }}</td><td>{% if j.incumbent %}Incumbent{% else %}Candidate{% endif %}</td></tr>
{% endif %}{% endfor %}</tbody></table></div>

<p><em>Justices of both courts whose seats are not on the 2026 ballot are not yet profiled. The official rosters are on the <a href="https://www.txcourts.gov/3rdcoa/" target="_blank" rel="noopener noreferrer">Third Court</a> and <a href="https://www.txcourts.gov/15thcoa/" target="_blank" rel="noopener noreferrer">Fifteenth Court</a> pages at txcourts.gov.</em></p>
