---
layout: default
title: "Meseeks — Legal Opportunities, Notices & Public Q&A"
permalink: /meseeks/
description: "An automated, guard-railed inbox for Bell County: legal job opportunities, public notices, standing orders from local courts, and anonymous questions answered in public by participating law firms."
---

<div class="meseeks-page" id="meseeks">
  <header class="meseeks-hero">
    <h1>Meseeks</h1>
    <p class="meseeks-tagline">Existence is pain — unless you have a purpose. Ours is helping people and automatons find legal opportunities and notices in Bell County.</p>
    <p class="meseeks-howto">
      Email <a href="mailto:{{ site.data.meseeks.inbox }}">{{ site.data.meseeks.inbox }}</a>.
      Everything sent to that address is reviewed automatically and, if it passes the guardrails below, posted here. Nothing is posted by hand, and nothing is posted with your name on it.
    </p>
  </header>

  <nav class="meseeks-jumps" aria-label="Jump to section">
    <a href="#opportunities">Opportunities</a> ·
    <a href="#notices">Notices</a> ·
    <a href="#standing-orders">Standing Orders</a> ·
    <a href="#questions">Questions</a> ·
    <a href="#answers">Answers</a> ·
    <a href="#guardrails">Guardrails</a>
  </nav>

  {% comment %}Pinned threads (e.g. thread -1) stay on top until removed; the rest are newest-updated first.{% endcomment %}
  {% assign pinned = site.data.meseeks.posts | where: "pinned", true | sort: "thread" %}
  {% assign unpinned = site.data.meseeks.posts | where_exp: "p", "p.pinned != true" | sort: "updated" | reverse %}
  {% assign posts = pinned | concat: unpinned %}
  {% assign opportunities = posts | where: "category", "opportunity" %}
  {% assign notices = posts | where: "category", "notice" %}
  {% assign orders = posts | where: "category", "standing_order" %}
  {% assign questions = posts | where: "category", "question" %}
  {% assign answers = posts | where: "category", "answer" %}

  <section id="opportunities" class="meseeks-section">
    <h2>Opportunities</h2>
    <p class="meseeks-section-note">Jobs, clerkships, internships, pro bono calls, and RFPs for legal services in Central Texas.</p>
    {% if opportunities.size > 0 %}
      {% for p in opportunities %}{% include meseeks-post.html post=p %}{% endfor %}
    {% else %}
      <p class="meseeks-empty">No opportunities posted yet.</p>
    {% endif %}
  </section>

  <section id="notices" class="meseeks-section">
    <h2>Notices</h2>
    <p class="meseeks-section-note">Public notices from city council members, county offices, and newspaper legal notices, forwarded to the inbox.</p>
    {% if notices.size > 0 %}
      {% for p in notices %}{% include meseeks-post.html post=p %}{% endfor %}
    {% else %}
      <p class="meseeks-empty">No notices posted yet.</p>
    {% endif %}
  </section>

  <section id="standing-orders" class="meseeks-section">
    <h2>Standing Orders</h2>
    <p class="meseeks-section-note">Standing orders and general administrative orders from Bell County courts and the Western District of Texas. Always confirm against the court's own posted copy.</p>
    {% if orders.size > 0 %}
      {% for p in orders %}{% include meseeks-post.html post=p %}{% endfor %}
    {% else %}
      <p class="meseeks-empty">No standing orders posted yet.</p>
    {% endif %}
  </section>

  <section id="questions" class="meseeks-section">
    <h2>Questions</h2>
    <p class="meseeks-section-note">Anonymous questions from people seeking representation or counsel. Names, addresses, case numbers, phone numbers and email addresses are removed before posting.</p>
    {% if questions.size > 0 %}
      {% for p in questions %}{% include meseeks-post.html post=p %}{% endfor %}
    {% else %}
      <p class="meseeks-empty">No questions posted yet.</p>
    {% endif %}
  </section>

  <section id="answers" class="meseeks-section">
    <h2>Answers</h2>
    <p class="meseeks-section-note">Limited, anonymous guidance from participating law firms. An answer is general information, not legal advice, and does not create an attorney-client relationship. The best next step is always to consult private counsel.</p>
    {% if answers.size > 0 %}
      {% for p in answers %}{% include meseeks-post.html post=p %}{% endfor %}
    {% else %}
      <p class="meseeks-empty">No answers posted yet.</p>
    {% endif %}
  </section>

  <section id="guardrails" class="meseeks-section meseeks-guardrails">
    <h2>Guardrails</h2>
    <ol>
      <li><strong>Answers come only from law firms.</strong> A message is published as an answer only if it is sent from a domain on the participating-firm list and it references a posted question. Anything else claiming to be an answer is held.</li>
      <li><strong>Questions are anonymized.</strong> Sender identity is never stored with the post. Personal identifiers in the body are redacted before publication.</li>
      <li><strong>Public forum, limited guidance.</strong> Firms agree their replies are general, public, and end with a referral to private counsel. Nothing here is legal advice.</li>
      <li><strong>Notices and orders are linked to source.</strong> Where the message carries an official link or attachment, the post links to it; the text is a summary, not the record.</li>
      <li><strong>Everything else is dropped.</strong> Solicitations, attachments that are not PDFs, messages with threats or abuse, and anything the classifier cannot place with confidence are not posted. Posts expire after {{ site.data.meseeks.retention_days }} days.</li>
    </ol>
    <p class="meseeks-small">Posting pipeline: <code>agents/meseeks/</code>. Firms that want to participate: email <a href="mailto:{{ site.email }}">{{ site.email }}</a> from the firm's domain.</p>
  </section>
</div>
