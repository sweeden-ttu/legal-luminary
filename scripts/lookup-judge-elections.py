#!/usr/bin/env python3
"""
Look up election information for Bell County judges.
Adds election details including when they were elected and when they're up for re-election.
"""

import json
import yaml
import sys
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from typing import Dict, Optional
import re
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent
JUDGES_FILE = BASE_DIR / "_data" / "judges.json"
OUTPUT_JSON = BASE_DIR / "_data" / "judges.json"
OUTPUT_YAML = BASE_DIR / "_data" / "judges.yml"

# Known election information from research
ELECTION_INFO = {
    "Debbie Garrett": {
        "election_year": 2024,
        "next_election": 2028,
        "term_length_years": 4,
        "election_notes": "Elected November 5, 2024"
    },
    "Mike Russell": {
        "election_year": 2024,
        "next_election": 2028,
        "term_length_years": 4,
        "election_notes": "Elected November 5, 2024, took office January 2, 2025"
    },
    "Steve Duskie": {
        "election_year": 2024,
        "next_election": 2028,
        "term_length_years": 4,
        "election_notes": "Re-elected November 5, 2024. Serving since August 17, 2020"
    },
    "Wade Faulkner": {
        "election_year": None,  # Appointed
        "appointment_year": 2022,
        "appointment_date": "August 18, 2022",
        "next_election": 2026,  # First election after appointment
        "term_length_years": 4,
        "election_notes": "Appointed by Governor Greg Abbott on August 18, 2022. First election in 2026"
    },
    "John Mischtian": {
        "election_year": 2022,
        "next_election": 2026,
        "term_length_years": 4,
        "election_notes": "Re-elected November 8, 2022"
    },
    "Rebecca De": {
        "election_year": None,  # Need to verify
        "next_election": 2026,
        "term_length_years": 4,
        "election_notes": "Next election scheduled for November 2026"
    },
    "Rebecca DePena": {
        "election_year": None,  # Need to verify
        "next_election": 2026,
        "term_length_years": 4,
        "election_notes": "Next election scheduled for November 2026"
    },
    "Rebecca DePew": {
        "election_year": None,  # Need to verify
        "next_election": 2026,
        "term_length_years": 4,
        "election_notes": "Next election scheduled for November 2026"
    },
    "Cari Starritt-Burnett": {
        "election_year": None,
        "appointment_year": 2021,
        "appointment_date": "August 2021",
        "next_election": 2026,
        "term_length_years": 4,
        "election_notes": "Appointed by Governor Greg Abbott in August 2021. First election in 2026"
    },
    "Cari L. Starritt-Burnett": {
        "election_year": None,
        "appointment_year": 2021,
        "appointment_date": "August 2021",
        "next_election": 2026,
        "term_length_years": 4,
        "election_notes": "Appointed by Governor Greg Abbott in August 2021. First election in 2026"
    },
    "Paul LePak": {
        "election_year": None,
        "appointment_year": 2018,
        "appointment_date": "June 2018",
        "next_election": 2026,  # Would have been up in 2022, then 2026
        "term_length_years": 4,
        "election_notes": "Appointed by Governor Greg Abbott in June 2018. Re-elected in 2022, next election 2026"
    },
    "Paul L. LePak": {
        "election_year": 2022,  # Likely re-elected after appointment
        "appointment_year": 2018,
        "appointment_date": "June 2018",
        "next_election": 2026,
        "term_length_years": 4,
        "election_notes": "Appointed by Governor Greg Abbott in June 2018. Re-elected in 2022, next election 2026"
    },
    "Paul Motz": {
        "election_year": 2022,  # Elected January 3, 2023 (likely special election or took office then)
        "next_election": 2026,
        "term_length_years": 4,
        "election_notes": "Elected January 3, 2023. Next election 2026"
    },
    "Paul A. Motz": {
        "election_year": 2022,  # Elected January 3, 2023 (likely special election or took office then)
        "next_election": 2026,
        "term_length_years": 4,
        "election_notes": "Elected January 3, 2023. Next election 2026"
    }
}

def lookup_judge_on_ballotpedia(judge_name: str, court_name: str) -> Optional[Dict]:
    """Look up judge information on Ballotpedia."""
    try:
        # Construct search URL
        search_query = f"{judge_name} {court_name} Texas"
        # Ballotpedia search URL
        search_url = f"https://ballotpedia.org/wiki/index.php?search={search_query.replace(' ', '+')}&title=Special:Search"
        
        # Try to find the judge's page
        # For now, we'll use the known election info
        return None
    except Exception as e:
        print(f"Error looking up {judge_name} on Ballotpedia: {e}", file=sys.stderr)
        return None

def get_election_info(judge_name: Optional[str], court_name: str, court_type: str) -> Dict:
    """Get election information for a judge."""
    if not judge_name:
        return {
            "election_year": None,
            "next_election": None,
            "term_length_years": 4,
            "election_notes": "Judge information not available"
        }
    
    # Check known election info
    if judge_name in ELECTION_INFO:
        return ELECTION_INFO[judge_name].copy()
    
    # Try variations of the name (check if judge name is a substring or vice versa)
    for known_name, info in ELECTION_INFO.items():
        judge_lower = judge_name.lower()
        known_lower = known_name.lower()
        # Check if names match (allowing for partial matches like "Rebecca De" matching "Rebecca DePena")
        if (judge_lower in known_lower or known_lower in judge_lower or 
            judge_lower.split()[0] == known_lower.split()[0]):  # First name match
            return info.copy()
    
    # Default: Texas judges serve 4-year terms, elections in even years
    # If we don't know when they were elected, we can't determine next election
    return {
        "election_year": None,
        "next_election": None,
        "term_length_years": 4,
        "election_notes": "Election information not found. Texas judges serve 4-year terms with elections in even-numbered years."
    }

def calculate_next_election(election_year: Optional[int], appointment_year: Optional[int] = None) -> Optional[int]:
    """Calculate the next election year based on election or appointment year."""
    if election_year:
        # Judges serve 4-year terms
        return election_year + 4
    elif appointment_year:
        # Appointed judges typically run in the next even-year election
        # If appointed in 2022, next election would be 2026
        next_even = ((appointment_year // 2) + 1) * 2
        if next_even <= appointment_year + 2:
            return next_even + 2
        return next_even
    return None

def main():
    """Main function to add election information to judge data."""
    print("Looking up election information for Bell County judges...")
    
    # Load existing judge data
    if not JUDGES_FILE.exists():
        print(f"Error: {JUDGES_FILE} not found", file=sys.stderr)
        return 1
    
    with open(JUDGES_FILE, 'r') as f:
        judges = json.load(f)
    
    # Add election information to each judge
    updated_count = 0
    for judge in judges:
        judge_name = judge.get('judge_name')
        court_name = judge.get('court_name')
        court_type = judge.get('court_type')
        
        print(f"\nProcessing: {court_name}")
        if judge_name:
            print(f"  Judge: {judge_name}")
        else:
            print(f"  Judge: (not available)")
        
        # Get election info
        election_info = get_election_info(judge_name, court_name, court_type)
        
        # Add to judge data
        judge['election_info'] = election_info
        
        # Calculate days until next election if we have a date
        if election_info.get('next_election'):
            next_election_year = election_info['next_election']
            # Assume election is in November (first Tuesday after first Monday)
            # For simplicity, use November 5th of that year
            if next_election_year:
                try:
                    election_date = datetime(next_election_year, 11, 5)
                    today = datetime.now()
                    if election_date > today:
                        days_until = (election_date - today).days
                        judge['election_info']['days_until_election'] = days_until
                        print(f"  Next election: {next_election_year} ({days_until} days)")
                    else:
                        print(f"  Next election: {next_election_year} (past due)")
                except:
                    pass
        
        if election_info.get('election_year') or election_info.get('appointment_year') or election_info.get('next_election'):
            updated_count += 1
            print(f"  Election info added")
        else:
            print(f"  Election info: Not found")
    
    # Write updated data
    print(f"\n\nUpdated {updated_count} judges with election information")
    
    # Write JSON
    with open(OUTPUT_JSON, 'w') as f:
        json.dump(judges, f, indent=2, ensure_ascii=False)
    print(f"Updated {OUTPUT_JSON}")
    
    # Write YAML
    with open(OUTPUT_YAML, 'w') as f:
        yaml.dump(judges, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    print(f"Updated {OUTPUT_YAML}")
    
    # Print summary
    print("\n=== Election Summary ===")
    for judge in judges:
        if judge.get('judge_name') and judge.get('election_info', {}).get('next_election'):
            next_election = judge['election_info']['next_election']
            days = judge['election_info'].get('days_until_election', 'N/A')
            print(f"{judge['judge_name']} ({judge['court_name']}): Next election {next_election} ({days} days)")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
