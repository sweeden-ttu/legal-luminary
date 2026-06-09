#!/usr/bin/env python3
"""
Scrape judge profiles from Bell County court websites.
Extracts judge names, court coordinators, court reporters, and contact information.
"""

import requests
from bs4 import BeautifulSoup
import re
import time
import yaml
import json
from urllib.parse import urljoin, urlparse
import sys
from typing import Dict, List, Optional

BASE_URL = "https://www.bellcountytx.com"

# District Court URLs
DISTRICT_COURTS = [
    ("27th Judicial District Court", "county_government/district_courts/27th_district_court/index.php"),
    ("146th Judicial District Court", "county_government/district_courts/146th_district_court/index.php"),
    ("169th Judicial District Court", "county_government/district_courts/169th_district_court/index.php"),
    ("264th Judicial District Court", "county_government/district_courts/264th_district_court/index.php"),
    ("426th Judicial District Court", "county_government/district_courts/426th_district_court/index.php"),
    ("478th Judicial District Court", "county_government/district_courts/478th_judicial_district_court/index.php"),
]

# County Court at Law URLs
COUNTY_COURTS = [
    ("Court at Law 1", "county_government/county_courts/court_at_law_1/index.php"),
    ("Court at Law 2", "county_government/county_courts/court_at_law_2/index.php"),
    ("Court at Law 3", "county_government/county_courts/court_at_law_3/index.php"),
]

def extract_phone(text: str) -> Optional[str]:
    """Extract phone number from text."""
    phone_patterns = [
        r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
        r'\d{3}\.\d{3}\.\d{4}',
    ]
    for pattern in phone_patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0)
    return None

def extract_email(text: str) -> Optional[str]:
    """Extract email address from text."""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    match = re.search(email_pattern, text)
    if match:
        return match.group(0)
    return None

def scrape_judge_profile(url: str, court_name: str, court_type: str) -> Optional[Dict]:
    """Scrape a single judge's profile page."""
    try:
        full_url = urljoin(BASE_URL + '/', url)
        response = requests.get(full_url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; LegalLuminaryJudgeScraper/1.0)'
        })
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Get main article content
        article = soup.find('article')
        if not article:
            return None
        
        text = article.get_text()
        
        # Extract judge name - look for patterns like "27th Judicial District Judge - Debbie Garrett"
        judge_name = None
        
        # First, try to find the paragraph containing judge information
        judge_paragraph = None
        for p in article.find_all(['p', 'div']):
            p_text = p.get_text()
            if re.search(r'Judge\s*[-–]', p_text, re.IGNORECASE):
                judge_paragraph = p
                break
        
        if judge_paragraph:
            judge_text = judge_paragraph.get_text()
            # Pattern: "27th Judicial District Judge - Debbie Garrett" or "Judge - Name"
            match = re.search(r'(?:\d+(?:st|nd|rd|th)?\s+Judicial\s+District\s+Judge|County\s+Court\s+at\s+Law\s+\d+\s+Judge|Judge)\s*[-–]\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)', judge_text)
            if match:
                judge_name = match.group(1).strip()
            else:
                # Try simpler pattern
                match = re.search(r'Judge\s*[-–]\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)', judge_text)
                if match:
                    judge_name = match.group(1).strip()
        
        # If still not found, search entire article text
        if not judge_name:
            match = re.search(r'(?:\d+(?:st|nd|rd|th)?\s+Judicial\s+District\s+Judge|County\s+Court\s+at\s+Law\s+\d+\s+Judge|Judge)\s*[-–]\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)', text)
            if match:
                judge_name = match.group(1).strip()
        
        # Extract court coordinator
        court_coordinator = None
        coordinator_email = None
        
        # Look for "Court Coordinator:" text
        coordinator_section = article.find(string=re.compile(r'Court\s+Coordinator', re.IGNORECASE))
        if coordinator_section:
            parent = coordinator_section.find_parent(['p', 'div'])
            if parent:
                coord_text = parent.get_text()
                # Extract name after "Court Coordinator:"
                match = re.search(r'Court\s+Coordinator[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', coord_text, re.IGNORECASE)
                if match:
                    court_coordinator = match.group(1).strip()
                    # Stop at "Court Reporter" if it appears
                    if 'Court Reporter' in coord_text:
                        court_coordinator = court_coordinator.split('Court Reporter')[0].strip()
                
                # Check for mailto link
                email_link = parent.find('a', href=re.compile(r'^mailto:'))
                if email_link:
                    coordinator_email = email_link.get('href', '').replace('mailto:', '').strip()
                else:
                    # Extract email from text
                    email = extract_email(coord_text)
                    if email:
                        coordinator_email = email
        
        # Extract court reporter
        court_reporter = None
        
        # Look for "Court Reporter:" text
        reporter_section = article.find(string=re.compile(r'Court\s+Reporter', re.IGNORECASE))
        if reporter_section:
            parent = reporter_section.find_parent(['p', 'div'])
            if parent:
                reporter_text = parent.get_text()
                # Extract name after "Court Reporter:"
                match = re.search(r'Court\s+Reporter[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', reporter_text, re.IGNORECASE)
                if match:
                    court_reporter = match.group(1).strip()
                    # Stop at newline or next section
                    if '\n' in court_reporter:
                        court_reporter = court_reporter.split('\n')[0].strip()
        
        # Extract phone and fax
        phone = None
        fax = None
        
        # Look for "Phone:" or "Fax:" patterns
        phone_match = re.search(r'Phone[:\s]*\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})', text, re.IGNORECASE)
        if phone_match:
            phone = f"({phone_match.group(1)}) {phone_match.group(2)}-{phone_match.group(3)}"
        
        fax_match = re.search(r'Fax[:\s]*\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})', text, re.IGNORECASE)
        if fax_match:
            fax = f"({fax_match.group(1)}) {fax_match.group(2)}-{fax_match.group(3)}"
        
        # Extract address
        address = None
        address_patterns = [
            r'1201\s+Huey\s+(?:Road|Drive)[^.]*Belton,\s+Texas\s+\d{5}',
            r'Bell\s+County\s+Justice\s+Center[^.]*1201[^.]*Belton',
        ]
        
        for pattern in address_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                address = match.group(0)
                break
        
        # If no specific address found, use default
        if not address:
            address = "Bell County Justice Center, 1201 Huey Road, Belton, Texas 76513"
        
        # Extract mailing address
        mailing_address = None
        mailing_match = re.search(r'Mailing\s+Address[:\s]+(P\.O\.\s+Box\s+\d+[^.]*Belton[^.]*)', text, re.IGNORECASE)
        if mailing_match:
            mailing_address = mailing_match.group(1).strip()
        
        judge_data = {
            'court_name': court_name,
            'court_type': court_type,
            'judge_name': judge_name,
            'court_coordinator': court_coordinator,
            'coordinator_email': coordinator_email,
            'court_reporter': court_reporter,
            'phone': phone,
            'fax': fax,
            'address': address,
            'mailing_address': mailing_address,
            'url': full_url
        }
        
        return judge_data
        
    except Exception as e:
        print(f"Error scraping {url}: {e}", file=sys.stderr)
        return None

def main():
    """Main function to scrape all judges and generate YAML/JSON."""
    print("Scraping judge profiles from Bell County court websites...")
    
    all_judges = []
    
    # Scrape District Courts
    print("\nScraping District Courts...")
    for court_name, url_path in DISTRICT_COURTS:
        print(f"  Scraping {court_name}...")
        judge_data = scrape_judge_profile(url_path, court_name, "District Court")
        if judge_data:
            all_judges.append(judge_data)
        time.sleep(1)  # Be polite
    
    # Scrape County Courts at Law
    print("\nScraping County Courts at Law...")
    for court_name, url_path in COUNTY_COURTS:
        print(f"  Scraping {court_name}...")
        judge_data = scrape_judge_profile(url_path, court_name, "County Court at Law")
        if judge_data:
            all_judges.append(judge_data)
        time.sleep(1)  # Be polite
    
    print(f"\nSuccessfully scraped {len(all_judges)} judge profiles.")
    
    # Write to YAML file
    yaml_file = '_data/judges.yml'
    with open(yaml_file, 'w') as f:
        yaml.dump(all_judges, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    
    print(f"Data written to {yaml_file}")
    
    # Also write to JSON for easy access
    json_file = '_data/judges.json'
    with open(json_file, 'w') as f:
        json.dump(all_judges, f, indent=2, ensure_ascii=False)
    
    print(f"Data also written to {json_file}")
    
    # Print summary
    print("\n=== Summary ===")
    for judge in all_judges:
        print(f"{judge['court_name']}: {judge.get('judge_name', 'N/A')}")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
