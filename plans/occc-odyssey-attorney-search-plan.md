# Plan: Identify Attorneys Defending Consumers Against Financial Companies

## Objective
Use the Office of Consumer Credit Commissioner (OCCC) search results to extract a list of regulated financial companies (e.g., payday lenders, auto title loan companies, collection agencies). Use this list to query the Bell County Odyssey portal's Party Search to find cases where these companies are plaintiffs. From those cases, identify the defense attorneys representing the consumers/defendants.

## Phase 1: OCCC Data Extraction
1.  **Source OCCC Data**: Utilize the existing Texas open data pipeline (e.g., `texas_data_crawler.py` or a specialized script) to query the OCCC Regulated Lenders database.
2.  **Filter Entities**: Extract the names of companies actively licensed to issue or collect debt in Central Texas (focusing on zip codes/cities in Bell County).
3.  **Data Clean-up**: Normalize the company names (e.g., stripping "LLC", "Inc.", expanding DBAs) to maximize search hit rates in the Odyssey portal. Output to `_data/occc_financial_entities.json`.

## Phase 2: Odyssey Portal Integration
1.  **Automate Party Search**: Develop a Playwright/Selenium script (`scripts/odyssey_financial_search.py`) to interface with the Bell County Odyssey portal.
2.  **Query Execution**: Iterate through the `occc_financial_entities.json` list, inputting each name into the Odyssey "Smart Search" as a Business/Agency party.
3.  **Case Filtering**: Filter the results to isolate Civil/Small Claims cases where the financial entity is the **Plaintiff**.

## Phase 3: Attorney Identification
1.  **Case Detail Scraping**: For each matching case, navigate to the case detail page.
2.  **Extract Defense Counsel**: Locate the "Defendant" party block and extract the name and contact information of the "Lead Attorney" or "Retained Attorney".
3.  **Aggregation & Output**: Compile a list of these defense attorneys, tallying the number of cases they've defended against OCCC-regulated entities. Output the final aggregated data to `_data/financial_defense_attorneys.json`.

## Phase 4: Site Integration
1.  **Create Directory Section**: Add a new layout/page (e.g., `/consumer-defense/`) to display the attorneys identified in Phase 3.
2.  **Display Metrics**: Highlight attorneys with significant experience defending against predatory lenders and collection agencies, enhancing the "Legal Representation" resources of the site.