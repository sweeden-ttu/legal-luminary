---
layout: default
title: Broken Links Report
permalink: /broken-links/
description: "Report of external links found on the site and their status, including any 404 errors."
---

<div class="broken-links-report">
  <h1>Broken Links Report</h1>
  <p class="intro-text">
    This page reports the status of all external links found throughout the site. Links are checked periodically for 404 errors and other issues.
  </p>

  {% if site.data.brokenlinks %}
    {% assign report = site.data.brokenlinks %}

    <div class="report-summary">
      <div class="summary-card">
        <h3>Total External Links</h3>
        <p class="summary-number">{{ report.total_links }}</p>
      </div>
      <div class="summary-card {% if report.broken_links_count > 0 %}has-errors{% endif %}">
        <h3>Broken Links (404)</h3>
        <p class="summary-number">{{ report.broken_links_count }}</p>
      </div>
      <div class="summary-card">
        <h3>Last Checked</h3>
        <p class="summary-date">{{ report.last_checked }}</p>
      </div>
    </div>

    {% if report.broken_links_count > 0 %}
      <section class="broken-links-section">
        <h2>Broken Links (404 Errors)</h2>
        <div class="links-list">
          {% for link in report.links %}
            {% if link.error_404 %}
              <div class="link-item broken">
                <div class="link-header">
                  <h3>
                    <a href="{{ link.link_url }}" target="_blank" rel="noopener noreferrer">
                      {{ link.link_name | default: link.link_url }}
                    </a>
                  </h3>
                  <span class="status-badge error">404 Error</span>
                </div>
                <div class="link-details">
                  <p class="link-url">
                    <strong>URL:</strong> 
                    <a href="{{ link.link_url }}" target="_blank" rel="noopener noreferrer">{{ link.link_url }}</a>
                  </p>
                  {% if link.status_code %}
                    <p class="link-status">
                      <strong>Status Code:</strong> {{ link.status_code }}
                    </p>
                  {% endif %}
                  {% if link.error_message %}
                    <p class="link-error">
                      <strong>Error:</strong> {{ link.error_message }}
                    </p>
                  {% endif %}
                  <p class="link-source">
                    <strong>Found in:</strong>
                    {% if link.source_files and link.source_files.size > 0 %}
                      {% for source in link.source_files %}
                        <code>{{ source }}</code>{% unless forloop.last %}, {% endunless %}
                      {% endfor %}
                    {% else %}
                      <code>{{ link.source_file }}</code>
                    {% endif %}
                    {% if link.source_type %}
                      <span class="source-type">({{ link.source_type }})</span>
                    {% endif %}
                  </p>
                </div>
              </div>
            {% endif %}
          {% endfor %}
        </div>
      </section>
    {% endif %}

    <section class="all-links-section">
      <h2>All External Links</h2>
      <div class="links-table-wrapper">
        <table class="links-table">
          <thead>
            <tr>
              <th>Link Name</th>
              <th>URL</th>
              <th>Status</th>
              <th>Source File</th>
            </tr>
          </thead>
          <tbody>
            {% for link in report.links %}
              <tr class="{% if link.error_404 %}broken-row{% endif %}">
                <td>
                  <strong>{{ link.link_name | default: "(no text)" }}</strong>
                </td>
                <td>
                  <a href="{{ link.link_url }}" target="_blank" rel="noopener noreferrer" class="link-url-cell">
                    {{ link.link_url | truncate: 60 }}
                  </a>
                </td>
                <td>
                  {% if link.error_404 %}
                    <span class="status-badge error">404 Error</span>
                  {% elsif link.status_code %}
                    <span class="status-badge success">OK ({{ link.status_code }})</span>
                  {% else %}
                    <span class="status-badge unknown">Unknown</span>
                  {% endif %}
                </td>
                <td>
                  <code class="source-code">{{ link.source_file }}</code>
                  {% if link.source_type %}
                    <span class="source-type">({{ link.source_type }})</span>
                  {% endif %}
                </td>
              </tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
    </section>

  {% else %}
    <div class="no-data">
      <p>No link data available. The link checker may not have run yet.</p>
      <p>To generate this report, run: <code>python3 scripts/check-broken-links.py</code></p>
    </div>
  {% endif %}
</div>

<style>
.broken-links-report {
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

.report-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.summary-card {
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  padding: 1.5rem;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.summary-card.has-errors {
  border-color: #dc3545;
  background: #fff5f5;
}

.summary-card h3 {
  margin: 0 0 1rem 0;
  color: var(--navy-dark, #1a365d);
  font-size: 1rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.summary-number {
  font-size: 2.5rem;
  font-weight: bold;
  margin: 0;
  color: var(--navy-dark, #1a365d);
}

.summary-card.has-errors .summary-number {
  color: #dc3545;
}

.summary-date {
  font-size: 0.9rem;
  color: #666;
  margin: 0;
}

.broken-links-section,
.all-links-section {
  margin-bottom: 3rem;
}

.broken-links-section h2,
.all-links-section h2 {
  color: var(--navy-dark, #1a365d);
  border-bottom: 2px solid var(--navy-dark, #1a365d);
  padding-bottom: 0.5rem;
  margin-bottom: 1.5rem;
}

.links-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.link-item {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.link-item.broken {
  border-color: #dc3545;
  background: #fff5f5;
}

.link-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.link-header h3 {
  margin: 0;
  font-size: 1.25rem;
}

.link-header h3 a {
  color: var(--navy-dark, #1a365d);
  text-decoration: none;
}

.link-header h3 a:hover {
  text-decoration: underline;
}

.link-details {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.link-details p {
  margin: 0;
  line-height: 1.6;
}

.link-url {
  word-break: break-all;
}

.link-url a {
  color: #0066cc;
  text-decoration: none;
}

.link-url a:hover {
  text-decoration: underline;
}

.link-status,
.link-error {
  font-size: 0.9rem;
}

.link-error {
  color: #dc3545;
}

.link-source {
  font-size: 0.9rem;
  color: #666;
}

.link-source code {
  background: #f5f5f5;
  padding: 0.2rem 0.4rem;
  border-radius: 3px;
  font-size: 0.85rem;
}

.source-type {
  color: #999;
  font-size: 0.85rem;
  margin-left: 0.5rem;
}

.status-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.85rem;
  font-weight: 600;
  white-space: nowrap;
}

.status-badge.error {
  background: #fee;
  color: #dc3545;
  border: 1px solid #dc3545;
}

.status-badge.success {
  background: #efe;
  color: #28a745;
  border: 1px solid #28a745;
}

.status-badge.unknown {
  background: #f5f5f5;
  color: #666;
  border: 1px solid #ccc;
}

.links-table-wrapper {
  overflow-x: auto;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.links-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 800px;
}

.links-table thead {
  background: var(--navy-dark, #1a365d);
  color: white;
}

.links-table th {
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.links-table td {
  padding: 1rem;
  border-bottom: 1px solid #e0e0e0;
  vertical-align: top;
}

.links-table tbody tr:hover {
  background: #f9f9f9;
}

.links-table tbody tr.broken-row {
  background: #fff5f5;
}

.links-table tbody tr.broken-row:hover {
  background: #ffe5e5;
}

.link-url-cell {
  color: #0066cc;
  text-decoration: none;
  word-break: break-all;
}

.link-url-cell:hover {
  text-decoration: underline;
}

.source-code {
  background: #f5f5f5;
  padding: 0.2rem 0.4rem;
  border-radius: 3px;
  font-size: 0.85rem;
  display: inline-block;
}

.no-data {
  text-align: center;
  padding: 3rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.no-data p {
  margin: 1rem 0;
  color: #666;
}

.no-data code {
  background: #f5f5f5;
  padding: 0.2rem 0.5rem;
  border-radius: 3px;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .report-summary {
    grid-template-columns: 1fr;
  }
  
  .link-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .links-table {
    font-size: 0.85rem;
  }
  
  .links-table th,
  .links-table td {
    padding: 0.75rem 0.5rem;
  }
}
</style>
