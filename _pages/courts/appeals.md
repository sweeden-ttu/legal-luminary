---
layout: default
title: "Courts of Appeals for Bell County — 3rd and 15th Districts"
permalink: /courts/appeals/
description: "The Third Court of Appeals in Austin hears appeals from Bell County; the Fifteenth Court of Appeals hears statewide business and government cases. Candidates on the Nov. 3, 2026 ballot with sourced profiles."
verified_at: 2026-11-01
---

# Courts of Appeals

<p class="intro-text">Bell County is in the Third Court of Appeals District, so its appeals go to the <strong>Third Court of Appeals</strong> in Austin, a six-justice court elected by the voters of 24 counties (<a href="https://tcss.legis.texas.gov/resources/gv/htm/gv.22.htm#22.201">Gov't Code §22.201(d)</a>; <a href="https://tcss.legis.texas.gov/resources/gv/htm/gv.22.htm#22.216">§22.216(c)</a>; <a href="https://www.txcourts.gov/3rdcoa/">Texas Courts</a>). The <strong>Fifteenth Court of Appeals</strong>, created by the Legislature in 2023 with its first term beginning September 1, 2024, has statewide civil intermediate appellate jurisdiction over cases involving state agencies and officers and over appeals from the business court; its district is every county in Texas, so its justices are elected statewide (<a href="https://www.txcourts.gov/15thcoa/">Texas Courts</a>; <a href="https://tcss.legis.texas.gov/resources/gv/htm/gv.22.htm#22.220">Gov't Code §22.220(d)</a>; <a href="https://tcss.legis.texas.gov/resources/gv/htm/gv.25a.htm#25A.007">§25A.007</a>; <a href="https://tcss.legis.texas.gov/resources/gv/htm/gv.22.htm#22.201">§22.201(p)</a>). Justices serve six-year terms (<a href="https://tcss.legis.texas.gov/resources/cn/htm/cn.5.htm#5.6">Tex. Const. art. V §6</a>). Four of these seats are on the November 3, 2026 ballot (<a href="https://www.bellcountytx.com/departments/elections/ballot_samples.php">Bell County ballot samples</a>).</p>

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
