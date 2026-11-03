---
layout: default
title: "Texas Supreme Court and Court of Criminal Appeals — 2026 candidates"
permalink: /courts/statewide/
description: "Texas's two courts of last resort, the Supreme Court (civil) and the Court of Criminal Appeals, and the candidates for the seven seats on the Nov. 3, 2026 ballot, with sourced profiles."
verified_at: 2026-11-01
---

# Texas Supreme Court and Court of Criminal Appeals

<p class="intro-text">Texas has two courts of last resort, each with nine members elected statewide to six-year terms (<a href="https://tcss.legis.texas.gov/resources/cn/htm/cn.5.htm#5.2">Tex. Const. art. V §§2, 4</a>): the <strong>Supreme Court</strong>, whose appellate jurisdiction covers all cases except criminal matters, and the <strong>Court of Criminal Appeals</strong> for criminal cases (<a href="https://tcss.legis.texas.gov/resources/cn/htm/cn.5.htm#5.3">art. V §§3, 5</a>). Four Supreme Court seats (one an unexpired term) and three Court of Criminal Appeals seats are on the November 3, 2026 ballot, and every one is contested (<a href="https://www.bellcountytx.com/departments/elections/ballot_samples.php">Bell County ballot samples</a>).</p>

{% assign appellate = site.candidates | where_exp: "j", "j.path contains 'courts/appellate/'" | sort: "ballot_order" %}

## Supreme Court of Texas — on the 2026 ballot

<div class="table-responsive"><table class="bench-table"><thead><tr><th>Seat</th><th>Candidate</th><th>Party</th><th>Status</th></tr></thead><tbody>
{% for j in appellate %}{% if j.court_group == "sc" %}<tr><td>{{ j.seat }}</td><td><strong><a href="{{ j.url }}">{{ j.title }}</a></strong></td><td>{{ j.party }}</td><td>{% if j.incumbent %}Incumbent{% else %}Candidate{% endif %}</td></tr>
{% endif %}{% endfor %}</tbody></table></div>

## Court of Criminal Appeals — on the 2026 ballot

<div class="table-responsive"><table class="bench-table"><thead><tr><th>Seat</th><th>Candidate</th><th>Party</th><th>Status</th></tr></thead><tbody>
{% for j in appellate %}{% if j.court_group == "cca" %}<tr><td>{{ j.seat }}</td><td><strong><a href="{{ j.url }}">{{ j.title }}</a></strong></td><td>{{ j.party }}</td><td>{% if j.incumbent %}Incumbent{% else %}Candidate{% endif %}</td></tr>
{% endif %}{% endfor %}</tbody></table></div>

<p><em>Members of both courts whose seats are not on the 2026 ballot are not yet profiled. Official rosters: <a href="https://www.txcourts.gov/supreme/" target="_blank" rel="noopener noreferrer">Supreme Court</a>, <a href="https://www.txcourts.gov/cca/" target="_blank" rel="noopener noreferrer">Court of Criminal Appeals</a>.</em></p>
