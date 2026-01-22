---
layout: default
title: Bell County Judges Directory
permalink: /judges/
description: "Directory of Bell County judges serving District Courts and County Courts at Law. Find judge contact information, court details, and election information."
---

<div class="judges-directory">
  <h1>Bell County Judges Directory</h1>
  <p class="intro-text">
    Directory of judges serving Bell County District Courts and County Courts at Law. This directory includes contact information, court details, and election information for all Bell County judges.
  </p>

  {% if site.data.judges %}
    {% assign district_judges = site.data.judges | where: "court_type", "District Court" %}
    {% assign county_judges = site.data.judges | where: "court_type", "County Court at Law" %}
    
    {% if district_judges.size > 0 %}
      <section class="judges-section">
        <h2>District Court Judges</h2>
        <p class="section-description">
          District Court judges handle felony criminal cases and civil cases over $200,000. Judges serve 4-year terms and are elected in partisan elections.
        </p>
        
        <div class="judges-list">
          {% for judge in district_judges %}
            <div class="judge-card">
              <div class="judge-header">
                <h3>{{ judge.court_name }}</h3>
                {% if judge.judge_name %}
                  <p class="judge-name">{{ judge.judge_name }}, Judge</p>
                {% else %}
                  <p class="judge-name">Judge information not available</p>
                {% endif %}
              </div>

              <div class="judge-contact">
                <h4>Contact Information</h4>
                <div class="contact-details">
                  {% if judge.phone %}
                    <div class="contact-item">
                      <strong>Phone:</strong> 
                      <a href="tel:{{ judge.phone | replace: ' ', '' | replace: '(', '' | replace: ')', '' | replace: '-', '' }}">{{ judge.phone }}</a>
                    </div>
                  {% endif %}
                  
                  {% if judge.fax %}
                    <div class="contact-item">
                      <strong>Fax:</strong> {{ judge.fax }}
                    </div>
                  {% endif %}
                  
                  {% if judge.court_coordinator %}
                    <div class="contact-item">
                      <strong>Court Coordinator:</strong> 
                      {% if judge.coordinator_email %}
                        <a href="mailto:{{ judge.coordinator_email }}">{{ judge.court_coordinator }}</a>
                      {% else %}
                        {{ judge.court_coordinator }}
                      {% endif %}
                    </div>
                  {% endif %}
                  
                  {% if judge.court_reporter %}
                    <div class="contact-item">
                      <strong>Court Reporter:</strong> {{ judge.court_reporter }}
                    </div>
                  {% endif %}
                </div>
              </div>

              {% if judge.address %}
                <div class="judge-section">
                  <h4>Location</h4>
                  <p>{{ judge.address }}</p>
                  {% if judge.mailing_address %}
                    <p class="mailing-address"><strong>Mailing:</strong> {{ judge.mailing_address | replace: "Office Hours:", "<br>Office Hours:" }}</p>
                  {% endif %}
                </div>
              {% endif %}

              {% if judge.election_info %}
                <div class="judge-section election-info">
                  <h4>Election Information</h4>
                  <div class="election-details">
                    {% if judge.election_info.election_year %}
                      <p><strong>Elected:</strong> {{ judge.election_info.election_year }}</p>
                    {% elsif judge.election_info.appointment_year %}
                      <p><strong>Appointed:</strong> {{ judge.election_info.appointment_date | default: judge.election_info.appointment_year }}</p>
                      {% if judge.election_info.appointment_year %}
                        <p class="appointment-note">Appointed by Governor Greg Abbott in {{ judge.election_info.appointment_year }}</p>
                      {% endif %}
                    {% endif %}
                    
                    {% if judge.election_info.next_election %}
                      <p class="next-election">
                        <strong>Next Election:</strong> 
                        <span class="election-year">{{ judge.election_info.next_election }}</span>
                        {% if judge.election_info.days_until_election %}
                          <span class="days-until">({{ judge.election_info.days_until_election }} days)</span>
                        {% endif %}
                      </p>
                    {% endif %}
                    
                    <p><strong>Term Length:</strong> {{ judge.election_info.term_length_years }} years</p>
                    
                    {% if judge.election_info.election_notes %}
                      <p class="election-notes">{{ judge.election_info.election_notes }}</p>
                    {% endif %}
                  </div>
                </div>
              {% endif %}

              {% if judge.url %}
                <div class="judge-section">
                  <p class="court-link">
                    <a href="{{ judge.url }}" target="_blank" rel="noopener noreferrer">View Court Website →</a>
                  </p>
                </div>
              {% endif %}
            </div>
          {% endfor %}
        </div>
      </section>
    {% endif %}

    {% if county_judges.size > 0 %}
      <section class="judges-section">
        <h2>County Court at Law Judges</h2>
        <p class="section-description">
          County Court at Law judges handle misdemeanor cases, probate matters, and smaller civil cases. Judges serve 4-year terms and are elected in partisan elections.
        </p>
        
        <div class="judges-list">
          {% for judge in county_judges %}
            <div class="judge-card">
              <div class="judge-header">
                <h3>{{ judge.court_name }}</h3>
                {% if judge.judge_name %}
                  <p class="judge-name">{{ judge.judge_name }}, Judge</p>
                {% else %}
                  <p class="judge-name">Judge information not available</p>
                {% endif %}
              </div>

              <div class="judge-contact">
                <h4>Contact Information</h4>
                <div class="contact-details">
                  {% if judge.phone %}
                    <div class="contact-item">
                      <strong>Phone:</strong> 
                      <a href="tel:{{ judge.phone | replace: ' ', '' | replace: '(', '' | replace: ')', '' | replace: '-', '' }}">{{ judge.phone }}</a>
                    </div>
                  {% endif %}
                  
                  {% if judge.fax %}
                    <div class="contact-item">
                      <strong>Fax:</strong> {{ judge.fax }}
                    </div>
                  {% endif %}
                  
                  {% if judge.court_coordinator %}
                    <div class="contact-item">
                      <strong>Court Coordinator:</strong> 
                      {% if judge.coordinator_email %}
                        <a href="mailto:{{ judge.coordinator_email }}">{{ judge.court_coordinator }}</a>
                      {% else %}
                        {{ judge.court_coordinator }}
                      {% endif %}
                    </div>
                  {% endif %}
                  
                  {% if judge.court_reporter %}
                    <div class="contact-item">
                      <strong>Court Reporter:</strong> {{ judge.court_reporter }}
                    </div>
                  {% endif %}
                </div>
              </div>

              {% if judge.address %}
                <div class="judge-section">
                  <h4>Location</h4>
                  <p>{{ judge.address }}</p>
                  {% if judge.mailing_address %}
                    <p class="mailing-address"><strong>Mailing:</strong> {{ judge.mailing_address | replace: "Office Hours:", "<br>Office Hours:" }}</p>
                  {% endif %}
                </div>
              {% endif %}

              {% if judge.election_info %}
                <div class="judge-section election-info">
                  <h4>Election Information</h4>
                  <div class="election-details">
                    {% if judge.election_info.election_year %}
                      <p><strong>Elected:</strong> {{ judge.election_info.election_year }}</p>
                    {% elsif judge.election_info.appointment_year %}
                      <p><strong>Appointed:</strong> {{ judge.election_info.appointment_date | default: judge.election_info.appointment_year }}</p>
                      {% if judge.election_info.appointment_year %}
                        <p class="appointment-note">Appointed by Governor Greg Abbott in {{ judge.election_info.appointment_year }}</p>
                      {% endif %}
                    {% endif %}
                    
                    {% if judge.election_info.next_election %}
                      <p class="next-election">
                        <strong>Next Election:</strong> 
                        <span class="election-year">{{ judge.election_info.next_election }}</span>
                        {% if judge.election_info.days_until_election %}
                          <span class="days-until">({{ judge.election_info.days_until_election }} days)</span>
                        {% endif %}
                      </p>
                    {% endif %}
                    
                    <p><strong>Term Length:</strong> {{ judge.election_info.term_length_years }} years</p>
                    
                    {% if judge.election_info.election_notes %}
                      <p class="election-notes">{{ judge.election_info.election_notes }}</p>
                    {% endif %}
                  </div>
                </div>
              {% endif %}

              {% if judge.url %}
                <div class="judge-section">
                  <p class="court-link">
                    <a href="{{ judge.url }}" target="_blank" rel="noopener noreferrer">View Court Website →</a>
                  </p>
                </div>
              {% endif %}
            </div>
          {% endfor %}
        </div>
      </section>
    {% endif %}

    {% if site.data.elected-officials %}
      <section class="other-officials-section">
        <h2>Other Justice System Officials</h2>
        <p class="section-description">
          In addition to judges, several other elected officials play important roles in Bell County's justice system.
        </p>
        
        {% assign prosecutors = site.data.elected-officials | where: "position_type", "District Attorney" %}
        {% assign county_attorneys = site.data.elected-officials | where: "position_type", "County Attorney" %}
        {% assign clerks = site.data.elected-officials | where: "position_type", "District Clerk" %}
        {% assign county_clerks = site.data.elected-officials | where: "position_type", "County Clerk" %}
        {% assign sheriffs = site.data.elected-officials | where: "position_type", "Sheriff" %}
        {% assign constables = site.data.elected-officials | where: "position_type", "Constable" %}
        {% assign jps = site.data.elected-officials | where: "position_type", "Justice of the Peace" %}
        
        {% if prosecutors.size > 0 or county_attorneys.size > 0 %}
          <div class="officials-group">
            <h3>Prosecutors</h3>
            <div class="officials-list">
              {% for official in prosecutors %}
                <div class="official-card">
                  <h4>{{ official.title }}</h4>
                  <p class="official-name"><strong>{{ official.name }}</strong></p>
                  {% if official.phone %}
                    <p><strong>Phone:</strong> <a href="tel:{{ official.phone | replace: '-', '' }}">{{ official.phone }}</a></p>
                  {% endif %}
                  {% if official.email %}
                    <p><strong>Email:</strong> <a href="mailto:{{ official.email }}">{{ official.email }}</a></p>
                  {% endif %}
                  {% if official.elected_year %}
                    <p><strong>Took Office:</strong> {{ official.elected_date }}</p>
                  {% endif %}
                  {% if official.next_election %}
                    <p class="next-election"><strong>Next Election:</strong> {{ official.next_election }}
                      {% if official.days_until_election %}
                        <span class="days-until">({{ official.days_until_election }} days)</span>
                      {% endif %}
                    </p>
                  {% endif %}
                </div>
              {% endfor %}
              {% for official in county_attorneys %}
                <div class="official-card">
                  <h4>{{ official.title }}</h4>
                  <p class="official-name"><strong>{{ official.name }}</strong></p>
                  {% if official.phone %}
                    <p><strong>Phone:</strong> <a href="tel:{{ official.phone | replace: '-', '' }}">{{ official.phone }}</a></p>
                  {% endif %}
                  {% if official.email %}
                    <p><strong>Email:</strong> <a href="mailto:{{ official.email }}">{{ official.email }}</a></p>
                  {% endif %}
                  {% if official.elected_year %}
                    <p><strong>Took Office:</strong> {{ official.elected_date }}</p>
                  {% endif %}
                  {% if official.next_election %}
                    <p class="next-election"><strong>Next Election:</strong> {{ official.next_election }}
                      {% if official.days_until_election %}
                        <span class="days-until">({{ official.days_until_election }} days)</span>
                      {% endif %}
                    </p>
                  {% endif %}
                </div>
              {% endfor %}
            </div>
          </div>
        {% endif %}
        
        {% if clerks.size > 0 or county_clerks.size > 0 %}
          <div class="officials-group">
            <h3>Clerks</h3>
            <div class="officials-list">
              {% for official in clerks %}
                <div class="official-card">
                  <h4>{{ official.title }}</h4>
                  <p class="official-name"><strong>{{ official.name }}</strong></p>
                  {% if official.phone %}
                    <p><strong>Phone:</strong> <a href="tel:{{ official.phone | replace: '-', '' }}">{{ official.phone }}</a></p>
                  {% endif %}
                  {% if official.email %}
                    <p><strong>Email:</strong> <a href="mailto:{{ official.email }}">{{ official.email }}</a></p>
                  {% endif %}
                  {% if official.elected_year %}
                    <p><strong>Took Office:</strong> {{ official.elected_date }}</p>
                  {% endif %}
                  {% if official.next_election %}
                    <p class="next-election"><strong>Next Election:</strong> {{ official.next_election }}
                      {% if official.days_until_election %}
                        <span class="days-until">({{ official.days_until_election }} days)</span>
                      {% endif %}
                    </p>
                  {% endif %}
                </div>
              {% endfor %}
              {% for official in county_clerks %}
                <div class="official-card">
                  <h4>{{ official.title }}</h4>
                  <p class="official-name"><strong>{{ official.name }}</strong></p>
                  {% if official.phone %}
                    <p><strong>Phone:</strong> <a href="tel:{{ official.phone | replace: '-', '' }}">{{ official.phone }}</a></p>
                  {% endif %}
                  {% if official.email %}
                    <p><strong>Email:</strong> <a href="mailto:{{ official.email }}">{{ official.email }}</a></p>
                  {% endif %}
                  {% if official.elected_year %}
                    <p><strong>Took Office:</strong> {{ official.elected_date }}</p>
                  {% endif %}
                  {% if official.next_election %}
                    <p class="next-election"><strong>Next Election:</strong> {{ official.next_election }}
                      {% if official.days_until_election %}
                        <span class="days-until">({{ official.days_until_election }} days)</span>
                      {% endif %}
                    </p>
                  {% endif %}
                </div>
              {% endfor %}
            </div>
          </div>
        {% endif %}
        
        {% if sheriffs.size > 0 or constables.size > 0 %}
          <div class="officials-group">
            <h3>Law Enforcement</h3>
            <div class="officials-list">
              {% for official in sheriffs %}
                <div class="official-card">
                  <h4>{{ official.title }}{% if official.precinct %} - Precinct {{ official.precinct }}{% endif %}</h4>
                  <p class="official-name"><strong>{{ official.name }}</strong></p>
                  {% if official.phone %}
                    <p><strong>Phone:</strong> <a href="tel:{{ official.phone | replace: '-', '' }}">{{ official.phone }}</a></p>
                  {% endif %}
                  {% if official.email %}
                    <p><strong>Email:</strong> <a href="mailto:{{ official.email }}">{{ official.email }}</a></p>
                  {% endif %}
                  {% if official.elected_year %}
                    <p><strong>Took Office:</strong> {{ official.elected_date }}</p>
                  {% endif %}
                  {% if official.next_election %}
                    <p class="next-election"><strong>Next Election:</strong> {{ official.next_election }}
                      {% if official.days_until_election %}
                        <span class="days-until">({{ official.days_until_election }} days)</span>
                      {% endif %}
                    </p>
                  {% endif %}
                </div>
              {% endfor %}
              {% for official in constables %}
                <div class="official-card">
                  <h4>{{ official.title }}{% if official.precinct %} - Precinct {{ official.precinct }}{% endif %}</h4>
                  <p class="official-name"><strong>{{ official.name }}</strong></p>
                  {% if official.phone %}
                    <p><strong>Phone:</strong> <a href="tel:{{ official.phone | replace: '-', '' }}">{{ official.phone }}</a></p>
                  {% endif %}
                  {% if official.email %}
                    <p><strong>Email:</strong> <a href="mailto:{{ official.email }}">{{ official.email }}</a></p>
                  {% endif %}
                  {% if official.elected_year %}
                    <p><strong>Took Office:</strong> {{ official.elected_date }}</p>
                  {% endif %}
                  {% if official.next_election %}
                    <p class="next-election"><strong>Next Election:</strong> {{ official.next_election }}
                      {% if official.days_until_election %}
                        <span class="days-until">({{ official.days_until_election }} days)</span>
                      {% endif %}
                    </p>
                  {% endif %}
                </div>
              {% endfor %}
            </div>
          </div>
        {% endif %}
        
        {% if jps.size > 0 %}
          <div class="officials-group">
            <h3>Justices of the Peace</h3>
            <p class="section-description">
              Justices of the Peace handle Class C misdemeanors, small claims cases, evictions, and truancy matters.
            </p>
            <div class="officials-list">
              {% for official in jps %}
                <div class="official-card">
                  <h4>{{ official.title }}</h4>
                  <p class="official-name"><strong>{{ official.name }}</strong></p>
                  {% if official.phone %}
                    <p><strong>Phone:</strong> <a href="tel:{{ official.phone | replace: '-', '' }}">{{ official.phone }}</a></p>
                  {% endif %}
                  {% if official.email %}
                    <p><strong>Email:</strong> <a href="mailto:{{ official.email }}">{{ official.email }}</a></p>
                  {% endif %}
                  {% if official.elected_year %}
                    <p><strong>Took Office:</strong> {{ official.elected_date }}</p>
                  {% endif %}
                  {% if official.next_election %}
                    <p class="next-election"><strong>Next Election:</strong> {{ official.next_election }}
                      {% if official.days_until_election %}
                        <span class="days-until">({{ official.days_until_election }} days)</span>
                      {% endif %}
                    </p>
                  {% endif %}
                </div>
              {% endfor %}
            </div>
          </div>
        {% endif %}
      </section>
    {% endif %}

    <section class="election-summary">
      <h2>Upcoming Elections</h2>
      <div class="election-timeline">
        <div class="election-year">
          <h3>2026 Elections</h3>
          <p>The following judges and officials are up for re-election in November 2026:</p>
          <ul>
            {% for judge in site.data.judges %}
              {% if judge.election_info and judge.election_info.next_election == 2026 and judge.judge_name %}
                <li><strong>{{ judge.judge_name }}</strong> - {{ judge.court_name }}</li>
              {% endif %}
            {% endfor %}
            {% if site.data.elected-officials %}
              {% for official in site.data.elected-officials %}
                {% if official.next_election == 2026 %}
                  <li><strong>{{ official.name }}</strong> - {{ official.title }}</li>
                {% endif %}
              {% endfor %}
            {% endif %}
          </ul>
        </div>
        
        <div class="election-year">
          <h3>2028 Elections</h3>
          <p>The following judges and officials are up for re-election in November 2028:</p>
          <ul>
            {% for judge in site.data.judges %}
              {% if judge.election_info and judge.election_info.next_election == 2028 and judge.judge_name %}
                <li><strong>{{ judge.judge_name }}</strong> - {{ judge.court_name }}</li>
              {% endif %}
            {% endfor %}
            {% if site.data.elected-officials %}
              {% for official in site.data.elected-officials %}
                {% if official.next_election == 2028 %}
                  <li><strong>{{ official.name }}</strong> - {{ official.title }}</li>
                {% endif %}
              {% endfor %}
            {% endif %}
          </ul>
        </div>
      </div>
    </section>

  {% else %}
    <div class="no-judges">
      <p>Judge information is not yet available. The judge directory is being compiled and will be populated automatically.</p>
    </div>
  {% endif %}
</div>

<style>
.judges-directory {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.intro-text {
  font-size: 1.1rem;
  color: #666;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.judges-section {
  margin-bottom: 3rem;
}

.judges-section h2 {
  color: var(--navy-dark, #1a365d);
  border-bottom: 2px solid var(--navy-dark, #1a365d);
  padding-bottom: 0.5rem;
  margin-bottom: 1rem;
  margin-top: 2rem;
}

.section-description {
  color: #666;
  margin-bottom: 2rem;
  font-size: 0.95rem;
}

.judges-list {
  display: grid;
  gap: 2rem;
  margin-top: 2rem;
}

.judge-card {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.judge-header {
  border-bottom: 2px solid var(--navy-dark, #1a365d);
  padding-bottom: 1rem;
  margin-bottom: 1.5rem;
}

.judge-header h3 {
  margin: 0 0 0.5rem 0;
  color: var(--navy-dark, #1a365d);
  font-size: 1.5rem;
}

.judge-name {
  color: #666;
  font-size: 1.1rem;
  margin: 0;
  font-weight: 600;
}

.judge-contact,
.judge-section {
  margin-bottom: 1.5rem;
}

.judge-contact h4,
.judge-section h4 {
  color: var(--navy-dark, #1a365d);
  font-size: 1.1rem;
  margin-bottom: 0.75rem;
  border-bottom: 1px solid #e0e0e0;
  padding-bottom: 0.25rem;
}

.contact-details {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.contact-item a {
  color: var(--navy-dark, #1a365d);
  text-decoration: none;
}

.contact-item a:hover {
  text-decoration: underline;
}

.mailing-address {
  font-size: 0.9rem;
  color: #666;
  margin-top: 0.5rem;
}

.election-info {
  background: #f5f5f5;
  padding: 1.5rem;
  border-radius: 4px;
  border-left: 4px solid var(--navy-dark, #1a365d);
}

.election-details p {
  margin: 0.5rem 0;
  line-height: 1.6;
}

.next-election {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--navy-dark, #1a365d);
}

.election-year {
  color: var(--navy-dark, #1a365d);
  font-weight: 600;
}

.days-until {
  color: #666;
  font-weight: normal;
  font-size: 0.9rem;
}

.appointment-note {
  font-size: 0.9rem;
  color: #666;
  font-style: italic;
}

.election-notes {
  font-size: 0.9rem;
  color: #666;
  margin-top: 0.75rem;
  padding-top: 0.75rem;
  border-top: 1px solid #e0e0e0;
}

.court-link {
  margin-top: 1rem;
}

.court-link a {
  color: var(--navy-dark, #1a365d);
  text-decoration: none;
  font-weight: 600;
}

.court-link a:hover {
  text-decoration: underline;
}

.election-summary {
  margin-top: 3rem;
  padding: 2rem;
  background: #f9f9f9;
  border-radius: 8px;
}

.election-summary h2 {
  color: var(--navy-dark, #1a365d);
  margin-bottom: 1.5rem;
}

.election-timeline {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.election-year {
  background: white;
  padding: 1.5rem;
  border-radius: 4px;
  border: 1px solid #e0e0e0;
}

.election-year h3 {
  color: var(--navy-dark, #1a365d);
  margin-top: 0;
  margin-bottom: 0.75rem;
}

.election-year ul {
  margin: 1rem 0;
  padding-left: 1.5rem;
}

.election-year li {
  margin: 0.5rem 0;
  line-height: 1.6;
}

.other-officials-section {
  margin-top: 3rem;
  padding-top: 3rem;
  border-top: 2px solid #e0e0e0;
}

.officials-group {
  margin-bottom: 3rem;
}

.officials-group h3 {
  color: var(--navy-dark, #1a365d);
  border-bottom: 2px solid var(--navy-dark, #1a365d);
  padding-bottom: 0.5rem;
  margin-bottom: 1.5rem;
  margin-top: 2rem;
}

.officials-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.official-card {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.official-card h4 {
  margin: 0 0 0.75rem 0;
  color: var(--navy-dark, #1a365d);
  font-size: 1.1rem;
}

.official-name {
  font-size: 1.1rem;
  margin-bottom: 0.75rem;
}

.official-card p {
  margin: 0.5rem 0;
  line-height: 1.6;
  font-size: 0.95rem;
}

.official-card a {
  color: var(--navy-dark, #1a365d);
  text-decoration: none;
}

.official-card a:hover {
  text-decoration: underline;
}

.no-judges {
  text-align: center;
  padding: 3rem;
  color: #666;
}

@media (max-width: 768px) {
  .judge-card {
    padding: 1.5rem;
  }
  
  .contact-details {
    font-size: 0.9rem;
  }
  
  .election-timeline {
    grid-template-columns: 1fr;
  }
}
</style>
