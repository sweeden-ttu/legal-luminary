---
layout: default
title: Notary Public Directory
permalink: /notaries/
description: "Directory of notary publics serving Bell County and Central Texas. Find mobile notaries, loan signing agents, and general notary services."
---

<div class="notary-directory">
  <h1>Notary Public Directory</h1>
  <p class="intro-text">
    Find qualified notary publics serving Bell County and Central Texas. This directory includes mobile notaries, loan signing agents, and general notary services.
  </p>

  {% if site.data.notaries %}
    <div class="notary-list">
      {% for notary in site.data.notaries %}
        <div class="notary-card">
          <div class="notary-header">
            <h2>{{ notary.name }}</h2>
            {% if notary.location %}
              <p class="notary-location">{{ notary.location }}</p>
            {% endif %}
          </div>

          {% if notary.experience %}
            <div class="notary-section">
              <h3>Experience</h3>
              <p>{{ notary.experience }}</p>
            </div>
          {% endif %}

          {% if notary.loan_signing_types %}
            <div class="notary-section">
              <h3>Loan Signing Types</h3>
              <p>{{ notary.loan_signing_types }}</p>
            </div>
          {% endif %}

          {% if notary.general_notary_work %}
            <div class="notary-section">
              <h3>General Notary Work</h3>
              <p>{{ notary.general_notary_work }}</p>
            </div>
          {% endif %}

          {% if notary.compliance_skills %}
            <div class="notary-section">
              <h3>Compliance & Skills</h3>
              <p>{{ notary.compliance_skills }}</p>
            </div>
          {% endif %}

          {% if notary.equipment %}
            <div class="notary-section">
              <h3>Equipment</h3>
              <p>{{ notary.equipment }}</p>
            </div>
          {% endif %}

          {% if notary.additional_services %}
            <div class="notary-section">
              <h3>Additional Services</h3>
              <p>{{ notary.additional_services }}</p>
            </div>
          {% endif %}

          {% if notary.availability %}
            <div class="notary-section">
              <h3>Availability</h3>
              <p>{{ notary.availability }}</p>
            </div>
          {% endif %}

          {% if notary.professional_standards %}
            <div class="notary-section">
              <h3>Professional Standards</h3>
              <p>{{ notary.professional_standards }}</p>
            </div>
          {% endif %}

          {% if notary.credentials %}
            <div class="notary-section">
              <h3>Credentials</h3>
              <p>{{ notary.credentials }}</p>
            </div>
          {% endif %}

          {% if notary.service_area %}
            <div class="notary-section">
              <h3>Service Area</h3>
              <p>{{ notary.service_area }}</p>
            </div>
          {% endif %}

          <div class="notary-communications">
            <h3>Contact Information</h3>
            <div class="contact-details">
              {% if notary.phone %}
                <div class="contact-item">
                  <strong>Phone:</strong> 
                  <a href="tel:{{ notary.phone | replace: ' ', '' | replace: '(', '' | replace: ')', '' | replace: '-', '' | replace: '.', '' }}">{{ notary.phone }}</a>
                </div>
              {% endif %}
              
              {% if notary.email %}
                <div class="contact-item">
                  <strong>Email:</strong> 
                  <a href="mailto:{{ notary.email }}">{{ notary.email }}</a>
                </div>
              {% endif %}
              
              {% if notary.website %}
                <div class="contact-item">
                  <strong>Website:</strong> 
                  <a href="{{ notary.website }}" target="_blank" rel="noopener noreferrer">{{ notary.website }}</a>
                </div>
              {% endif %}
            </div>
          </div>

          {% if notary.addresses and notary.addresses.size > 0 %}
            <div class="notary-section">
              <h3>Addresses</h3>
              {% for address in notary.addresses %}
                <div class="address-item">
                  {% if address.type %}
                    <strong>{{ address.type | capitalize }}:</strong>
                  {% endif %}
                  <p>{{ address.address }}</p>
                </div>
              {% endfor %}
            </div>
          {% endif %}

          {% if notary.last_updated %}
            <div class="notary-section">
              <p class="last-updated">Profile last updated: {{ notary.last_updated }}</p>
            </div>
          {% endif %}

          {% if notary.hr_service or notary.does_fingerprinting or notary.has_laser_printer or notary.home_inspections %}
            <div class="notary-details">
              <h3>Notary Details</h3>
              <ul class="notary-features">
                {% if notary.hr_service %}
                  <li>24 Hr Service: {{ notary.hr_service }}</li>
                {% endif %}
                {% if notary.does_fingerprinting %}
                  <li>Does Fingerprinting: {{ notary.does_fingerprinting }}</li>
                {% endif %}
                {% if notary.has_laser_printer %}
                  <li>Has Laser Printer: {{ notary.has_laser_printer }}</li>
                {% endif %}
                {% if notary.home_inspections %}
                  <li>Home Inspections: {{ notary.home_inspections }}</li>
                {% endif %}
              </ul>
            </div>
          {% endif %}
        </div>
      {% endfor %}
    </div>
  {% else %}
    <div class="no-notaries">
      <p>No notary information available at this time. Please check back later.</p>
    </div>
  {% endif %}
</div>

<style>
.notary-directory {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.notary-list {
  display: grid;
  gap: 2rem;
  margin-top: 2rem;
}

.notary-card {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.notary-header {
  border-bottom: 2px solid var(--navy-dark, #1a365d);
  padding-bottom: 1rem;
  margin-bottom: 1.5rem;
}

.notary-header h2 {
  margin: 0 0 0.5rem 0;
  color: var(--navy-dark, #1a365d);
  font-size: 1.75rem;
}

.notary-location {
  color: #666;
  font-size: 1.1rem;
  margin: 0;
}

.notary-section {
  margin-bottom: 1.5rem;
}

.notary-section h3 {
  color: var(--navy-dark, #1a365d);
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
  border-bottom: 1px solid #e0e0e0;
  padding-bottom: 0.25rem;
}

.notary-section p {
  margin: 0.5rem 0;
  line-height: 1.6;
}

.notary-communications {
  background: #f5f5f5;
  padding: 1.5rem;
  border-radius: 4px;
  margin: 1.5rem 0;
}

.notary-communications h3 {
  margin-top: 0;
  color: var(--navy-dark, #1a365d);
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
}

.contact-item a {
  color: var(--navy-dark, #1a365d);
  text-decoration: none;
}

.contact-item a:hover {
  text-decoration: underline;
}

.address-item {
  margin-bottom: 1rem;
}

.address-item p {
  margin: 0.25rem 0;
}

.notary-details {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e0e0e0;
}

.notary-features {
  list-style: none;
  padding: 0;
  margin: 0.5rem 0;
}

.notary-features li {
  padding: 0.5rem 0;
  border-bottom: 1px solid #f0f0f0;
}

.notary-features li:last-child {
  border-bottom: none;
}

.last-updated {
  font-size: 0.9rem;
  color: #666;
  font-style: italic;
  margin-top: 1rem;
}

.no-notaries {
  text-align: center;
  padding: 3rem;
  color: #666;
}

@media (max-width: 768px) {
  .notary-card {
    padding: 1.5rem;
  }
  
  .contact-details {
    font-size: 0.9rem;
  }
}
</style>
