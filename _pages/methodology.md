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
Financial Protection Bureau (CFPB) Consumer Complaint Database</a> contains approximately
15.7 million complaints filed against financial institutions. The full database
(<code>complaints.csv.zip</code>, 1.37 GB) was downloaded from
<a href="https://files.consumerfinance.gov/ccdb/complaints.csv.zip">files.consumerfinance.gov</a>
on June 9, 2026.
</p>

<p>
Complaint counts were aggregated by the company name listed on each complaint. Where subsidiaries
or DBAs appeared separately in the database, counts were noted but not merged to preserve the
CFPB's classification. For example, Nationstar Mortgage (19,296) and Mr. Cooper (15,430) are
the same entity but the CFPB assigns separate complaint records to each label.
</p>

<h3>2.2 Odyssey Public Court Records Portal</h3>

<p>
Bell County's <a href="https://justice.bellcounty.texas.gov/PublicPortal">Odyssey Public Portal</a>
(Tyler Technologies, version 2017.1.61.2) provides public access to civil, criminal, and
traffic case records. The portal's Smart Search feature was used to search by party name
(plaintiff, defendant, or law firm) across all case types and all court locations.
</p>

<p>
The search window was set to a four-year filing period (March 1, 2022 to present), matching
the term length for Justices of the Peace in Texas. All searches used the "Party Name" criterion
with exact-match and prefix matching, limited to case types containing "Eviction" or "Foreclosure."
</p>

<hr>

<h2 id="cfpb-findings">3. CFPB Complaint Findings</h2>

<p>
The following table ranks mortgage servicers, lenders, and noteholders by their total CFPB
complaint count. Entities were selected based on their appearance on the Bell County Clerk's
website and Odyssey court records as parties in foreclosure or eviction proceedings.
</p>

<table>
  <thead>
    <tr>
      <th style="text-align:right">Rank</th>
      <th>Servicer</th>
      <th style="text-align:right">CFPB Complaints</th>
      <th style="width:40%">Relative Volume</th>
    </tr>
  </thead>
  <tbody>
{% assign max_comp = 179887 %}
{% assign servicers = "Bank of America|179887,Wells Fargo|168815,Ocwen Financial|37488,Shellpoint Mortgage Servicing|18275,Select Portfolio Servicing|16115,Nationstar Mortgage / Mr. Cooper|34726,Ditech Financial|14947,HSBC|12361,M&T Bank|9814,Freedom Mortgage|9673,Specialized Loan Servicing|8770,LoanCare LLC|8027,Carrington Mortgage Services|6878,PennyMac Loan Services|5998,Caliber Home Loans|4742,Flagstar Bank|4707,Seterus Inc.|4487,PHH Mortgage|2450,U.S. Bank|907,Deutsche Bank|164,NewRez LLC|0" | split: "," %}
{% for s in servicers %}
{% assign parts = s | split: "|" %}
{% assign name = parts[0] %}
{% assign count = parts[1] | plus: 0 %}
{% assign pct = count | times: 100.0 | divided_by: max_comp | round: 1 %}
    <tr>
      <td style="text-align:right">{{ forloop.index }}</td>
      <td>{{ name }}</td>
      <td style="text-align:right">{{ count | number_with_delimiter }}</td>
      <td><div style="background:#e53935;height:14px;width:{{ pct }}%;border-radius:3px;min-width:{% if count > 0 %}2px{% else %}0{% endif %}"></div></td>
    </tr>
{% endfor %}
  </tbody>
</table>

<div style="margin:16px 0;padding:12px;background:#f5f5f5;border-radius:4px;font-size:0.9em">
  <strong>Key observations:</strong>
  <ul>
    <li>The three highest-complaint servicers (Bank of America, Wells Fargo, Ocwen) account for 386,190 complaints &mdash; 63% of the servicers tracked.</li>
    <li>Nationstar Mortgage (dba Mr. Cooper) ranks 4th with 34,726 combined complaints &mdash; placing it among the most-complained-about mortgage servicers in Bell County's foreclosure ecosystem.</li>
    <li>Law firms and trustees (Zwicker &amp; Associates, McCalla Raymer, Barrett Daffin, etc.) rarely appear in the CFPB database, as their work is foreclosure processing rather than consumer lending.</li>
    <li>NewRez LLC (formed 2018 from New Penn Financial / Caliber merger) has no CFPB complaint history but appears in Odyssey foreclosure records.</li>
  </ul>
</div>

<hr>

<h2 id="odyssey-search">4. Odyssey Court Record Search</h2>

<h3>4.1 Search Methodology</h3>

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

<h3>4.2 Search Terms</h3>

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

<h3>4.3 Case Classification</h3>

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

<h2 id="results">5. Results</h2>

<h3>5.1 Overall Volumes</h3>

<table>
  <thead>
    <tr><th>Category</th><th style="text-align:right">Count</th><th style="text-align:right">Percentage</th></tr>
  </thead>
  <tbody>
    <tr><td>Residential Evictions</td><td style="text-align:right">463</td><td style="text-align:right">84.6%</td></tr>
    <tr><td>Home Equity Foreclosures (Expedited)</td><td style="text-align:right">57</td><td style="text-align:right">10.4%</td></tr>
    <tr><td>Other Foreclosures</td><td style="text-align:right">19</td><td style="text-align:right">3.5%</td></tr>
    <tr><td>JP Appeal Evictions</td><td style="text-align:right">7</td><td style="text-align:right">1.3%</td></tr>
    <tr><td>Commercial Evictions</td><td style="text-align:right">1</td><td style="text-align:right">0.2%</td></tr>
    <tr style="font-weight:bold"><td>Total</td><td style="text-align:right">547</td><td style="text-align:right">100%</td></tr>
  </tbody>
</table>

<h3>5.2 Distribution by Court</h3>

<table>
  <thead>
    <tr><th>Court</th><th>Judge</th><th style="text-align:right">Cases</th><th style="text-align:right">%</th><th style="width:30%">Bar</th></tr>
  </thead>
  <tbody>
{% assign total_cases = 547 %}
{% assign courts = "Justice of the Peace Precinct 4, Place 2|154|Nicola J. James,Justice of the Peace Precinct 4, Place 1|137|Gregory Johnson,Justice of the Peace Precinct 3, Place 2|136|Larry Wilkey,146th Judicial District Court|42|(Various),169th Judicial District Court|34|(Various),Justice of the Peace Precinct 1|24|Ted Duffield,Justice of the Peace Precinct 3, Place 1|12|Rosanne Fisher,County Court at Law #1|7|(Various),Justice of the Peace Precinct 2|1|Cliff Coleman" | split: "," %}
{% for c in courts %}
{% assign parts2 = c | split: "|" %}
{% assign court_name = parts2[0] %}
{% assign court_count = parts2[1] | plus: 0 %}
{% assign court_judge = parts2[2] %}
{% assign c_pct = court_count | times: 100.0 | divided_by: total_cases | round: 1 %}
    <tr>
      <td>{{ court_name }}</td>
      <td>{{ court_judge }}</td>
      <td style="text-align:right">{{ court_count }}</td>
      <td style="text-align:right">{{ c_pct }}%</td>
      <td><div style="background:#1e88e5;height:14px;width:{{ c_pct }}%;border-radius:3px;min-width:{% if court_count > 0 %}2px{% else %}0{% endif %}"></div></td>
    </tr>
{% endfor %}
  </tbody>
</table>

<h3>5.3 Case Status Distribution</h3>

<table>
  <thead>
    <tr><th>Status</th><th style="text-align:right">Cases</th><th style="text-align:right">%</th></tr>
  </thead>
  <tbody>
    <tr><td>Disposed</td><td style="text-align:right">349</td><td style="text-align:right">63.8%</td></tr>
    <tr><td>Dismissed</td><td style="text-align:right">160</td><td style="text-align:right">29.3%</td></tr>
    <tr><td>Active</td><td style="text-align:right">31</td><td style="text-align:right">5.7%</td></tr>
    <tr><td>Appealed</td><td style="text-align:right">7</td><td style="text-align:right">1.3%</td></tr>
  </tbody>
</table>

<h3>5.4 Concentration by Judicial Officer</h3>

<p>
Three Justice of the Peace courts account for 427 of the 547 eviction and foreclosure cases
identified (78.1%):
</p>

<table>
  <thead>
    <tr><th>Judge</th><th>Court</th><th style="text-align:right">Cases</th><th style="text-align:right">% of Total</th></tr>
  </thead>
  <tbody>
    <tr><td>Nicola J. James</td><td>JP4 Place 2 (Killeen)</td><td style="text-align:right">154</td><td style="text-align:right">28.2%</td></tr>
    <tr><td>Gregory Johnson</td><td>JP4 Place 1 (Killeen)</td><td style="text-align:right">137</td><td style="text-align:right">25.0%</td></tr>
    <tr><td>Larry Wilkey</td><td>JP3 Place 2 (Temple)</td><td style="text-align:right">136</td><td style="text-align:right">24.9%</td></tr>
  </tbody>
</table>

<h3>5.5 Top Plaintiffs by Filing Volume</h3>

<table>
  <thead>
    <tr><th>Plaintiff</th><th style="text-align:right">Cases</th><th>Type</th></tr>
  </thead>
  <tbody>
    <tr><td>MARIE CURTIS FLP</td><td style="text-align:right">68</td><td>Property management</td></tr>
    <tr><td>Pleasant View PLNDV TX LLC</td><td style="text-align:right">50</td><td>Property management</td></tr>
    <tr><td>MCG Homestead Rentals and Sales</td><td style="text-align:right">17</td><td>Property management</td></tr>
    <tr><td>ALL ZIP LLC</td><td style="text-align:right">7</td><td>Property management</td></tr>
    <tr><td>Ditech Financial LLC</td><td style="text-align:right">16</td><td>Mortgage servicer</td></tr>
    <tr><td>M&amp;T Bank</td><td style="text-align:right">12</td><td>Bank / lender</td></tr>
    <tr><td>NewRez LLC</td><td style="text-align:right">11</td><td>Mortgage servicer</td></tr>
    <tr><td>PennyMac Loan Services</td><td style="text-align:right">9</td><td>Mortgage servicer</td></tr>
    <tr><td>Nationstar Mortgage LLC</td><td style="text-align:right">8</td><td>Mortgage servicer</td></tr>
    <tr><td>Carrington Mortgage Services</td><td style="text-align:right">7</td><td>Mortgage servicer</td></tr>
    <tr><td>Deutsche Bank National Trust</td><td style="text-align:right">6</td><td>Trustee / noteholder</td></tr>
  </tbody>
</table>

<hr>

<h2 id="discussion">6. Discussion</h2>

<h3>6.1 Geographic Concentration</h3>

<p>
The concentration of eviction filings in Precinct 4 (Killeen) and Precinct 3 Place 2 (Temple)
is consistent with the population distribution of Bell County. Killeen, the county's largest
city and home to a significant population affiliated with Fort Cavazos, has a large rental
housing market. Temple, the second-largest city, has also seen substantial rental property
development in recent years.
</p>

<p>
The three JP courts that handle the majority of eviction cases serve the two largest
population centers in the county. The remaining JP precincts (Precinct 1, Precinct 2,
and Precinct 3 Place 1) cover more rural areas with lower population density and
correspondingly fewer eviction filings.
</p>

<h3>6.2 Foreclosure Venue</h3>

<p>
Foreclosure cases in Texas are filed in District Court, not JP court. All 76 foreclosure
cases identified (Home Equity - Expedited and Other) were filed in the 146th Judicial
District Court (42 cases) and 169th Judicial District Court (34 cases). These cases
involve mortgage servicers (Ditech, PennyMac, Carrington, NewRez, Nationstar,
Deutsche Bank) and typically proceed under the Texas Home Equity expedited process.
</p>

<h3>6.3 Eviction Filing Patterns</h3>

<p>
The majority of eviction filings come from a small number of property management companies
and real estate investment entities, not from individual landlords:
</p>

<ul>
  <li><strong>Marie Curtis FLP</strong> (68 cases) and <strong>Pleasant View</strong> entities (50 cases) together account for 21.6% of all eviction filings in the dataset.</li>
  <li>Rental property investment firms (MCG Homestead, ALL ZIP LLC, Brad Martin / Real Star) account for a significant share of filings.</li>
  <li>Mortgage servicers rarely file evictions in Bell County &mdash; their presence in JP court is minimal compared to property managers.</li>
</ul>

<h3>6.4 Limitations</h3>

<ul>
  <li><strong>Search-term bias.</strong> Cases were identified by searching for specific plaintiff, servicer, and law firm names. This methodology will undercount cases filed by entities not included in the search list. The concentration figures should be interpreted as the share of <em>identified</em> cases, not the share of all eviction/foreclosure filings in Bell County.</li>
  <li><strong>Date range.</strong> The four-year search window (March 2022 to present) captures approximately one full term for JP judges. Cases filed before March 2022 are not included.</li>
  <li><strong>Data completeness.</strong> The Odyssey Public Portal returns results through the Kendo Grid interface, which enforces server-side pagination. Very large result sets (e.g., MCG Homestead: 44 parties) required pagination and may not capture every related case.</li>
  <li><strong>Case type classification.</strong> Classification relies on the Odyssey case type descriptor text. Cases with atypical descriptors (e.g., "Other Contract" or "Debt/Contract: Debt Collection") that nonetheless involve eviction or foreclosure were excluded.</li>
  <li><strong>Party name matching.</strong> The Odyssey Smart Search uses prefix-based matching on party names. Variants in entity naming (e.g., "Pleasant View PLNDV TX LLC" vs. "Pleasant View TX LLC") may produce duplicate or incomplete results across search terms.</li>
</ul>

<hr>

<h2 id="context">7. Context &amp; Motivation</h2>

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

<h2 id="data-access">8. Data Access</h2>

<p>
The full deduplicated dataset (547 records) is available at:
</p>

<ul>
  <li><strong>CSV:</strong> <a href="/data/bell_county_evictions_foreclosures.csv"><code>/data/bell_county_evictions_foreclosures.csv</code></a></li>
  <li><strong>Source code:</strong> The scraping methodology and scripts are available in the project repository.</li>
</ul>

<p><em>This page will be updated as additional cases are identified and as case statuses change in the Odyssey portal.</em></p>

<hr>

<p><a href="/candidates/courts/">&larr; Back to Judicial Officers</a></p>
