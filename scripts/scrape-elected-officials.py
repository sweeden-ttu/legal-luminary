#!/usr/bin/env python3
"""
Scrape elected officials information from Bell County website.
Focuses on justice-related positions: District Attorney, County Attorney, Sheriff, 
District Clerk, County Clerk, Justices of the Peace, and Constables.
"""

import requests
from bs4 import BeautifulSoup
import re
import time
import yaml
import json
from urllib.parse import urljoin
import sys
from typing import Dict, List, Optional
from datetime import datetime

BASE_URL = "https://www.bellcountytx.com"
ELECTED_OFFICIALS_URL = "https://www.bellcountytx.com/about_us/elected_officials/index.php"

# Justice-related positions to extract
JUSTICE_POSITIONS = [
    "District Attorney",
    "County Attorney",
    "Sheriff",
    "District Clerk",
    "County Clerk",
    "Peace Justice",
    "Constable"
]

def parse_date(date_str: str) -> Optional[Dict]:
    """Parse date string like '1/02/25' or '8/27/18' into year."""
    if not date_str:
        return None
    
    # Format is typically M/DD/YY or MM/DD/YY
    # The date represents when they took office (not necessarily when elected)
    parts = date_str.split('/')
    if len(parts) >= 3:
        year_part = parts[2].strip()
        # Convert 2-digit year to 4-digit
        if len(year_part) == 2:
            year_int = int(year_part)
            # Assume years 00-30 are 2000-2030, 31-99 are 1931-1999
            if year_int <= 30:
                year = 2000 + year_int
            else:
                year = 1900 + year_int
        else:
            year = int(year_part)
        
        return {
            'year': year,
            'date_string': date_str
        }
    return None

def scrape_elected_officials() -> List[Dict]:
    """Scrape elected officials page."""
    try:
        response = requests.get(ELECTED_OFFICIALS_URL, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; LegalLuminaryOfficialScraper/1.0)'
        })
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        officials = []
        
        # Find the table with elected officials
        table = soup.find('table')
        if not table:
            return officials
        
        # Find all rows (skip header)
        rows = table.find_all('tr')[1:]  # Skip header row
        
        for row in rows:
            cells = row.find_all(['td', 'th'])
            if len(cells) >= 4:
                title = cells[0].get_text(strip=True)
                name = cells[1].get_text(strip=True)
                elected_date = cells[2].get_text(strip=True)
                phone = cells[3].get_text(strip=True)
                
                # Check if this is a justice-related position
                is_justice_related = any(pos in title for pos in JUSTICE_POSITIONS)
                
                if is_justice_related and name:
                    # Extract email if available
                    email = None
                    name_link = cells[1].find('a', href=re.compile(r'^mailto:'))
                    if name_link:
                        email = name_link.get('href', '').replace('mailto:', '').strip()
                    
                    # Parse election date
                    date_info = parse_date(elected_date)
                    
                    official_data = {
                        'title': title,
                        'name': name,
                        'phone': phone if phone else None,
                        'email': email,
                        'elected_date': elected_date,
                        'elected_year': date_info['year'] if date_info else None
                    }
                    
                    # Determine position type and next election
                    # All these positions serve 4-year terms, elections in even-numbered years (2026, 2028, 2030, etc.)
                    current_year = datetime.now().year
                    
                    # Calculate next election
                    # The "elected_date" shows when they took office (typically January after November election)
                    # If they took office in 2007, they were elected in November 2006
                    # Elections are every 4 years in even-numbered years
                    if date_info and date_info['year']:
                        office_year = date_info['year']
                        # If they took office in January of year X, election was November of year X-1 (if X is even, it might be X)
                        # For simplicity, assume election year is the year before taking office (for Jan dates)
                        # Or if the date is late in the year, election might be same year
                        # Most take office in January, so election was previous November (even year)
                        election_year = office_year - 1 if office_year % 2 == 1 else office_year
                        # Ensure it's an even year (elections are always in even years)
                        if election_year % 2 != 0:
                            election_year -= 1
                        
                        # Calculate next election: find next even year that's 4+ years from election year
                        next_even = current_year
                        if next_even % 2 != 0:
                            next_even += 1
                        
                        # Find next valid election year (must be at least 4 years from original election, and even)
                        while next_even < election_year + 4 or (next_even - election_year) % 4 != 0:
                            next_even += 2
                        
                        official_data['next_election'] = next_even
                        official_data['last_election_year'] = election_year
                    else:
                        official_data['next_election'] = None
                        official_data['last_election_year'] = None
                    
                    if 'District Attorney' in title:
                        official_data['position_type'] = 'District Attorney'
                        official_data['term_length_years'] = 4
                    elif 'County Attorney' in title:
                        official_data['position_type'] = 'County Attorney'
                        official_data['term_length_years'] = 4
                    elif 'Sheriff' in title:
                        official_data['position_type'] = 'Sheriff'
                        official_data['term_length_years'] = 4
                    elif 'District Clerk' in title:
                        official_data['position_type'] = 'District Clerk'
                        official_data['term_length_years'] = 4
                    elif 'County Clerk' in title:
                        official_data['position_type'] = 'County Clerk'
                        official_data['term_length_years'] = 4
                    elif 'Peace Justice' in title or 'Justice' in title:
                        official_data['position_type'] = 'Justice of the Peace'
                        official_data['term_length_years'] = 4
                        # Extract precinct info
                        precinct_match = re.search(r'Pct\.\s*(\d+)', title)
                        if precinct_match:
                            official_data['precinct'] = int(precinct_match.group(1))
                        place_match = re.search(r'Pl\.\s*(\d+)', title)
                        if place_match:
                            official_data['place'] = int(place_match.group(1))
                    elif 'Constable' in title:
                        official_data['position_type'] = 'Constable'
                        official_data['term_length_years'] = 4
                        # Extract precinct info
                        precinct_match = re.search(r'Pct\.\s*(\d+)', title)
                        if precinct_match:
                            official_data['precinct'] = int(precinct_match.group(1))
                    
                    # Calculate days until next election
                    if official_data.get('next_election'):
                        try:
                            election_date = datetime(official_data['next_election'], 11, 5)  # Assume November 5
                            today = datetime.now()
                            if election_date > today:
                                official_data['days_until_election'] = (election_date - today).days
                        except:
                            pass
                    
                    officials.append(official_data)
        
        return officials
        
    except Exception as e:
        print(f"Error scraping elected officials: {e}", file=sys.stderr)
        return []

def main():
    """Main function to scrape elected officials and generate YAML/JSON."""
    print("Scraping elected officials from Bell County website...")
    
    officials = scrape_elected_officials()
    
    print(f"\nFound {len(officials)} justice-related elected officials")
    
    # Write to YAML file
    yaml_file = '_data/elected-officials.yml'
    with open(yaml_file, 'w') as f:
        yaml.dump(officials, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    
    print(f"Data written to {yaml_file}")
    
    # Also write to JSON for easy access
    json_file = '_data/elected-officials.json'
    with open(json_file, 'w') as f:
        json.dump(officials, f, indent=2, ensure_ascii=False)
    
    print(f"Data also written to {json_file}")
    
    # Print summary by position type
    print("\n=== Summary by Position ===")
    position_groups = {}
    for official in officials:
        pos_type = official.get('position_type', 'Other')
        if pos_type not in position_groups:
            position_groups[pos_type] = []
        position_groups[pos_type].append(official)
    
    for pos_type, group in sorted(position_groups.items()):
        print(f"\n{pos_type}: {len(group)}")
        for official in group:
            next_election = official.get('next_election', 'N/A')
            days = official.get('days_until_election', 'N/A')
            print(f"  - {official['name']} ({official['title']}): Next election {next_election} ({days} days)")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
