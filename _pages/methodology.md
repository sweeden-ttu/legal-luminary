---
layout: default
title: "Eviction & Foreclosure Study Methodology"
permalink: /methodology/
description: "Methodology for the Bell County eviction and foreclosure case study: data sources, search criteria, and analytical approach."
last_updated: 2026-06-10
---

<h1>Eviction &amp; Foreclosure Study &mdash; Methodology</h1>

<p><em>Last updated: June 10, 2026</em></p>

<hr>

<h2 id="overview">1. Overview</h2>

<p>
This study examines the distribution of eviction and foreclosure cases across Bell County, Texas
judicial officers. The goal is to measure whether case filings are concentrated in specific courts
and to provide transparency into the volume and disposition of housing-related civil litigation
in the county.
</p>

<p>
The analysis proceeded in two phases: (1) identification of mortgage servicers, lenders, and
property managers active in Bell County, ranked by federal consumer complaint volume, followed
by (2) systematic search of the county's Odyssey public court records portal for case filings
matching those entities over a four-year period.
</p>

<hr>

<h2 id="data-sources">2. Data Sources</h2>

<h3>2.1 CFPB Consumer Complaint Database</h3>

<p>
The <a href="https://www.consumerfinance.gov/data-research/consumer-complaints/">Consumer
Financial Protection Bureau (CFPB) Consumer Complaint Database</a> was used to rank
servicers by complaint volume. The full database
(<code>complaints.csv.zip</code>) was downloaded from
<a href="https://files.consumerfinance.gov/ccdb/complaints.csv.zip">files.consumerfinance.gov</a>
on June 9, 2026.
</p>

<p>
Complaint counts were aggregated by the company name listed on each complaint. Where subsidiaries
or DBAs appeared separately in the database, counts were noted but not merged to preserve the
CFPB's classification.
</p>

<h3>2.2 Odyssey Public Court Records Portal</h3>

<p>
Bell County's <a href="https://justice.bellcounty.texas.gov/PublicPortal">Odyssey Public Portal</a>
was the source of case records. The portal's Smart Search feature was used to search by party name
(plaintiff, defendant, or law firm) across all case types and all court locations.
</p>

<p>
The search window was set to a four-year filing period (March 1, 2022 to present), matching
the four-year term of a Texas justice of the peace (<a href="https://tcss.legis.texas.gov/resources/cn/htm/cn.5.htm#5.18">Tex. Const. art. V §18</a>). All searches used the "Party Name" criterion
with exact-match and prefix matching, limited to case types containing "Eviction" or "Foreclosure."
</p>

<hr>

<h2 id="odyssey-search">3. Odyssey Court Record Search</h2>

<h3>3.1 Search Methodology</h3>

<p>
The following process was used for each search term:
</p>

<ol>
  <li><strong>Session initiation.</strong> A fresh browser session was established with the Odyssey Public Portal (GET request to <code>/Home/Dashboard/29</code>), which sets an <code>ASP.NET_SessionId</code> cookie.</li>
  <li><strong>Form submission.</strong> A POST request was sent to <code>/SmartSearch/SmartSearch/SmartSearch</code> with form fields replicating the browser's exact submission format: party name search with the "Party Name" criterion enabled, "Business Name" unchecked, "Sounds Like" disabled, "Advanced Search Options" collapsed, "All Locations" selected, and "File Date Start" set to <code>03/01/2022</code>.</li>
  <li><strong>Result retrieval.</strong> The server responds with a 302 redirect to the WorkspaceMode page, which sets a <code>SmartSearchCriteria</code> session cookie. An XHR GET request to <code>/SmartSearch/SmartSearchResults</code> (with the session cookie) returns an HTML page containing a Kendo Grid JSON data payload with party records and their associated case details.</li>
  <li><strong>Data extraction.</strong> The Kendo Grid <code>Data</code> array was extracted via bracket-depth matching, parsed as JSON, and each party's <code>CaseResults</code> array was examined for case type descriptors containing "Eviction" or "Foreclosure."</li>
  <li><strong>Pagination.</strong> Where results exceeded one page (25 records), additional pages were fetched up to a maximum of 5 additional page requests per search term.</li>
  <li><strong>Deduplication.</strong> Cases were deduplicated across search terms by their <code>case_number</code> field (e.g., "42CV2500941").</li>
</ol>

<h3>3.2 Search Terms</h3>

<p>
Search terms were derived from three sources:
</p>

<table>
  <thead>
    <tr><th>Source</th><th>Examples</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>CFPB top-complaint servicers</td>
      <td>Bank of America, Wells Fargo, Ocwen, Nationstar, Shellpoint, Select Portfolio Servicing, Ditech, HSBC, M&amp;T Bank, Freedom Mortgage, Carrington, PennyMac, Caliber, Flagstar, PHH, U.S. Bank, Deutsche Bank, NewRez, LoanCare, Specialized Loan Servicing</td>
    </tr>
    <tr>
      <td>Trustee and law firms from county clerk records</td>
      <td>Zwicker &amp; Associates, McCalla Raymer, Barrett Daffin, Hughes Watters, Mackie Wolf, Orlans, Shapiro, Shapiro Schwartz</td>
    </tr>
    <tr>
      <td>Property management plaintiffs from early search results</td>
      <td>Marie Curtis FLP, MCG Homestead, Pleasant View, ALL ZIP LLC, Brad Martin / Real Star, Mike Pilkington, Shine Residential</td>
    </tr>
  </tbody>
</table>

<h3>3.3 Case Classification</h3>

<p>
Cases were classified using the Odyssey case type descriptor. The following case type strings
triggered inclusion:
</p>

<ul>
  <li><strong>Eviction:</strong> "Contract: Evictions - Residential", "Contract: Evictions - Commercial", "JP Appeal Contract: Evictions - Residential"</li>
  <li><strong>Foreclosure:</strong> "Contract: Foreclosure - Home Equity - Expedited", "Contract: Foreclosure - Other"</li>
</ul>

<p>
Each case record includes: case number, case style (plaintiff vs. defendant), file date, case type, current status, court location, party name, defendant name, and an encrypted case identifier for detail-page retrieval.
</p>

<hr>

<h2 id="limitations">4. Limitations</h2>

<ul>
  <li><strong>Search-term bias.</strong> Cases were identified by searching for specific plaintiff, servicer, and law firm names. This methodology will undercount cases filed by entities not included in the search list. Any concentration figure derived from this dataset should be read as the share of <em>identified</em> cases, not the share of all eviction/foreclosure filings in Bell County.</li>
  <li><strong>Date range.</strong> The four-year search window (March 2022 to present) captures approximately one full term for JP judges. Cases filed before March 2022 are not included.</li>
  <li><strong>Data completeness.</strong> The Odyssey Public Portal returns results through the Kendo Grid interface, which enforces server-side pagination. Very large result sets required pagination and may not capture every related case.</li>
  <li><strong>Case type classification.</strong> Classification relies on the Odyssey case type descriptor text. Cases with atypical descriptors (e.g., "Other Contract" or "Debt/Contract: Debt Collection") that nonetheless involve eviction or foreclosure were excluded.</li>
  <li><strong>Party name matching.</strong> The Odyssey Smart Search uses prefix-based matching on party names. Variants in entity naming (e.g., "Pleasant View PLNDV TX LLC" vs. "Pleasant View TX LLC") may produce duplicate or incomplete results across search terms.</li>
</ul>

<hr>

<h2 id="context">5. Context &amp; Motivation</h2>

<p>
This study was conducted independently. The domain and project were initiated following
personal experience with a judicial system in which an appointed (rather than elected)
judge presided over civil proceedings that resulted in the loss of the author's residence.
That experience led to a focus on judicial accountability and the principle that judges
should be elected rather than appointed, so that communities retain direct democratic
control over those who adjudicate their civil and criminal matters.
</p>

<p>
The study does not publish party membership information for any judge. The analysis is
limited to case volume, filing patterns, and case disposition data available through
public court records. The goal is to inform voters about the performance of their local
judiciary regardless of party affiliation.
</p>

<hr>

<h2 id="data-access">6. Results and Data Access</h2>

<p>
Case counts by court, by judge, by plaintiff and by status are not published on this page. They will be
published only together with the case-level dataset (case numbers, filing dates, court and status for
every record) so that each figure can be checked against the Odyssey portal. The CFPB complaint
rankings used to choose search terms are likewise not reproduced here, because the database changes
daily and a snapshot cannot be checked against a fixed public page.
</p>

<p><em>This page will be updated when the dataset is published.</em></p>

<hr>

<p><a href="/candidates/courts/">&larr; Back to Judicial Officers</a></p>
