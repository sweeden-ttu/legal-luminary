# Phase 2: Web Scraper & Record Extraction Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a scraper agent using Selenium/Playwright to extract case decisions (Small Claims, Consumer Complaints, Foreclosures) from the Bell County Tyler Odyssey portal and Official Public Records.

**Architecture:** A Python-based scraping agent will be spawned to navigate the Odyssey portal. It will bypass basic anti-scraping, execute searches by case type, and extract docket entries and judge decisions into the database.

**Tech Stack:** Python, Selenium WebDriver (or Playwright), BeautifulSoup.

---

### Task 1: Scraper Environment Setup

**Files:**
- Create: `../legal-lumany/modules/judiciary-rd-agent/scraper_agent.py`

- [ ] **Step 1: Write initial scraper structure**
    - Set up headless browser configuration.
    - Define target URLs:
        - Odyssey Portal: `https://portal-txbell.tylertech.cloud/Portal/`
        - Public Records (for Foreclosure Notices): `https://belltx.countygovernmentrecords.com/`

- [ ] **Step 2: Commit setup**

### Task 2: Implement Case Type Search Logic

**Files:**
- Modify: `../legal-lumany/modules/judiciary-rd-agent/scraper_agent.py`

- [ ] **Step 1: Implement search by Case Type**
    - Add logic to search "Civil" -> "Small Claims" (JP Courts)
    - Add logic to search "Civil" -> "Debt/Contract" (Consumer Complaints in CCL/District)
    - Add logic to search "Real Property" -> "Rule 736" or "Foreclosure" (District Courts)

- [ ] **Step 2: Implement search by Attorney/Firm**
    - Add logic to search Official Public Records for "Notice of Trustee Sale" where firm is "McCarthy Holthus" or attorneys like "Thuy Frazier", "Cole D. Patton".

### Task 3: Decision Extraction and Parsing

**Files:**
- Modify: `../legal-lumany/modules/judiciary-rd-agent/scraper_agent.py`
- Modify: `../legal-lumany/modules/judiciary-rd-agent/judiciary_db.json`

- [ ] **Step 1: Parse Docket Entries**
    - Extract the "Disposition" or "Order" text from the case details page to capture the judge's decision.

- [ ] **Step 2: Save to DB**
    - Append scraped cases to a new `cases` array in `judiciary_db.json`.

