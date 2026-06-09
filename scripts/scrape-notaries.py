#!/usr/bin/env python3
"""
Web crawler to collect notary public information from Notary Rotary.
Extracts names, phone numbers, email addresses, and other profile details.
"""

import requests
from bs4 import BeautifulSoup
import re
import time
import yaml
from urllib.parse import urljoin, urlparse
import sys
from typing import Dict, List, Optional

BASE_URL = "https://www.notaryrotary.com"
LISTING_URL = "https://www.notaryrotary.com/agent/searchdtlbody.asp?id=&PostalCD=76541&Address=&City=&l=&ll=&pfn=01045523001P&bfn=01045523001B&pmc=3&bmc=11&Miles=30&LocType=&StateCD=&PostalState=Texas&PostalCounty=Bell&EstimateCost=0&Lat=31.114961&Lon=-97.723782&Location=&Override=0&type=RSS"

def extract_phone(text: str) -> Optional[str]:
    """Extract phone number from text."""
    # Match phone patterns like (254) 216-2885, 254.216.2885, 254-216-2885
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

def parse_profile_details(soup: BeautifulSoup) -> Dict:
    """Parse the profile details section."""
    details = {}
    
    # Find text containing "Category,Details" which indicates the profile table
    profile_text = soup.find(string=re.compile('Category,Details'))
    if not profile_text:
        return details
    
    # Get the parent table
    profile_table = profile_text.find_parent('table')
    if not profile_table:
        return details
    
    # The data is in a comma-separated format in the text
    # Format: "Category,Details Experience,value Loan Signing Types,value..."
    full_text = profile_table.get_text()
    
    # Split by common category patterns
    categories = {
        'Experience': 'experience',
        'Loan Signing Types': 'loan_signing_types',
        'General Notary Work': 'general_notary_work',
        'Compliance & Skills': 'compliance_skills',
        'Equipment': 'equipment',
        'Additional Services': 'additional_services',
        'Availability': 'availability',
        'Professional Standards': 'professional_standards',
        'Credentials': 'credentials',
        'Service Area': 'service_area'
    }
    
    # Parse the comma-separated format
    # Pattern: CategoryName,Value NextCategoryName,Value
    parts = re.split(r'\s+([A-Z][^,]+),', full_text)
    if len(parts) > 1:
        for i in range(1, len(parts) - 1, 2):
            category = parts[i].strip()
            value = parts[i + 1].strip() if i + 1 < len(parts) else ''
            
            # Remove trailing category names that might have been captured
            # Find where the value ends (before next category or end)
            if i + 2 < len(parts):
                next_category_start = full_text.find(parts[i + 2] if i + 2 < len(parts) else '', 
                                                   full_text.find(category) + len(category))
                if next_category_start > 0:
                    value = full_text[full_text.find(category) + len(category) + 1:next_category_start].strip()
            
            # Clean up value - remove any trailing category names
            for cat_name in categories.keys():
                if value.endswith(cat_name):
                    value = value[:-len(cat_name)].strip()
            
            if category in categories and value:
                details[categories[category]] = value
    
    # Alternative: Try to find table rows with category/value pairs
    if not details:
        rows = profile_table.find_all('tr')
        for row in rows:
            cells = row.find_all(['td', 'th'])
            if len(cells) >= 2:
                category = cells[0].get_text(strip=True)
                value = cells[1].get_text(strip=True)
                
                if category and value and category != value:
                    for cat_name, key in categories.items():
                        if cat_name in category:
                            details[key] = value
                            break
    
    return details

def parse_communications(soup: BeautifulSoup) -> Dict:
    """Parse the communications section."""
    comm = {
        'phone': None,
        'email': None,
        'website': None
    }
    
    # Find Communications section
    comm_header = soup.find('th', string=re.compile('Communications'))
    if not comm_header:
        # Try finding by text content
        comm_header = soup.find(string=re.compile('Communications'))
        if comm_header:
            comm_header = comm_header.find_parent(['th', 'td'])
    
    if not comm_header:
        return comm
    
    # Find the table with phone/email info
    comm_table = comm_header.find_parent('table')
    if comm_table:
        # First, look for actual links (mailto: and http/https)
        # Check for email links
        email_links = comm_table.find_all('a', href=re.compile(r'^mailto:'))
        if email_links:
            for link in email_links:
                href = link.get('href', '')
                email = href.replace('mailto:', '').strip()
                if email:
                    comm['email'] = email
                    break
        
        # Check for website links
        website_links = comm_table.find_all('a', href=re.compile(r'^https?://'))
        if website_links:
            for link in website_links:
                href = link.get('href', '').strip()
                if href and 'notaryrotary.com' not in href:
                    comm['website'] = href
                    break
        
        # Also check link text for website URLs
        if not comm['website']:
            all_links = comm_table.find_all('a', href=True)
            for link in all_links:
                href = link.get('href', '').strip()
                link_text = link.get_text(strip=True)
                # If link text looks like a domain, use it
                if link_text and '.' in link_text and not link_text.startswith('http'):
                    # Check if it's a domain-like string
                    if re.match(r'^[a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\.[a-zA-Z]{2,}', link_text):
                        comm['website'] = f'http://{link_text}'
                        break
        
        # Look for rows with "Mobile:" or "Phone:"
        rows = comm_table.find_all('tr')
        for row in rows:
            cells = row.find_all(['td', 'th'])
            if len(cells) >= 2:
                label = cells[0].get_text(strip=True)
                value_cell = cells[1]
                value_text = value_cell.get_text(strip=True)
                
                if 'Mobile' in label or 'Phone' in label:
                    if not comm['phone']:
                        phone = extract_phone(value_text)
                        if phone:
                            comm['phone'] = phone
                elif 'E-mail' in label or 'Email' in label:
                    if not comm['email']:
                        # Check for mailto link in this cell
                        email_link = value_cell.find('a', href=re.compile(r'^mailto:'))
                        if email_link:
                            email = email_link.get('href', '').replace('mailto:', '').strip()
                            if email:
                                comm['email'] = email
                        else:
                            # Extract email from text
                            email = extract_email(value_text)
                            if email:
                                comm['email'] = email
                elif 'Website' in label:
                    if not comm['website']:
                        # Check for link in this cell
                        website_link = value_cell.find('a', href=True)
                        if website_link:
                            href = website_link.get('href', '').strip()
                            if href and 'notaryrotary.com' not in href:
                                if not href.startswith('http'):
                                    href = f'http://{href}'
                                comm['website'] = href
                        else:
                            # Extract website from text
                            website = value_text.strip()
                            if website and website != 'null':
                                # Clean up common patterns
                                website = re.sub(r'^Website:\s*', '', website, flags=re.IGNORECASE)
                                website = website.strip()
                                if website and '.' in website:
                                    if not website.startswith('http'):
                                        website = f'http://{website}'
                                    comm['website'] = website
        
        # Fallback: extract from full text
        if not comm['phone'] or not comm['email'] or not comm['website']:
            text = comm_table.get_text()
            
            if not comm['phone']:
                phone = extract_phone(text)
                if phone:
                    comm['phone'] = phone
            
            if not comm['email']:
                email = extract_email(text)
                if email:
                    comm['email'] = email
            
            if not comm['website']:
                # Try multiple patterns for website
                website_patterns = [
                    r'Website:\s*([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\.[a-zA-Z]{2,}[^\s]*)',
                    r'Website:\s*([^\s]+\.(com|org|net|edu|gov)[^\s]*)',
                    r'(www\.[a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\.[a-zA-Z]{2,}[^\s]*)',
                ]
                for pattern in website_patterns:
                    website_match = re.search(pattern, text, re.IGNORECASE)
                    if website_match:
                        website = website_match.group(1).strip()
                        # Remove trailing slashes and clean up
                        website = website.rstrip('/')
                        if website and '.' in website:
                            if not website.startswith('http'):
                                website = f'http://{website}'
                            comm['website'] = website
                            break
    
    return comm

def parse_addresses(soup: BeautifulSoup) -> List[Dict]:
    """Parse the addresses section."""
    addresses = []
    
    # Find Addresses section
    addr_header = soup.find('th', string=re.compile('Addresses'))
    if not addr_header:
        return addresses
    
    addr_table = addr_header.find_parent('table')
    if addr_table:
        rows = addr_table.find_all('tr')
        current_address = {}
        address_parts = []
        
        for row in rows:
            cells = row.find_all(['td', 'th'])
            if len(cells) >= 2:
                label = cells[0].get_text(strip=True)
                value = cells[1].get_text(strip=True)
                
                # Check if this is a new address (Primary/Secondary label)
                if 'Primary' in label or 'Secondary' in label:
                    # Save previous address if exists
                    if current_address and address_parts:
                        current_address['address'] = ' '.join(address_parts)
                        addresses.append(current_address)
                    
                    # Start new address
                    addr_type = 'primary' if 'Primary' in label else 'secondary'
                    current_address = {'type': addr_type}
                    address_parts = []
                    # The value might be the first part of the address
                    if value and value not in ['Primary', 'Secondary']:
                        address_parts.append(value)
                elif value and current_address:
                    # This is a continuation of the current address
                    if value not in ['Primary', 'Secondary']:
                        address_parts.append(value)
            elif len(cells) == 1:
                # Single cell might contain address info
                text = cells[0].get_text(strip=True)
                if text and text not in ['Primary', 'Secondary', 'Addresses']:
                    if current_address:
                        address_parts.append(text)
                    elif 'Primary' in text or 'Secondary' in text:
                        # This might be the type
                        addr_type = 'primary' if 'Primary' in text else 'secondary'
                        current_address = {'type': addr_type}
                        address_parts = []
        
        # Save last address
        if current_address and address_parts:
            current_address['address'] = ' '.join(address_parts)
            addresses.append(current_address)
    
    return addresses

def parse_notary_details(soup: BeautifulSoup) -> Dict:
    """Parse the notary details section."""
    details = {}
    
    # Find Notary Details section
    details_header = soup.find('th', string=re.compile('Notary Details'))
    if not details_header:
        return details
    
    details_table = details_header.find_parent('table')
    if details_table:
        rows = details_table.find_all('tr')
        for row in rows:
            cells = row.find_all(['td', 'th'])
            if len(cells) >= 2:
                key = cells[0].get_text(strip=True).rstrip(':')
                value = cells[1].get_text(strip=True)
                if key and value:
                    # Convert to lowercase with underscores
                    key_lower = key.lower().replace(' ', '_').replace(':', '')
                    details[key_lower] = value
    
    return details

def scrape_notary_detail(url: str) -> Optional[Dict]:
    """Scrape a single notary's detail page."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract name and location from page title or header
        title = soup.find('title')
        name = None
        location = None
        
        if title:
            title_text = title.get_text()
            # Format: "Name, Notary Public in City, State"
            match = re.match(r'(.+?),\s*Notary Public in\s*(.+)', title_text)
            if match:
                name = match.group(1).strip()
                location = match.group(2).strip()
        
        # Try to find name in profile header
        if not name:
            profile_header = soup.find('td', string=re.compile('-'))
            if profile_header:
                header_text = profile_header.get_text()
                match = re.match(r'(.+?)\s*-\s*(.+)', header_text)
                if match:
                    name = match.group(1).strip()
                    location = match.group(2).strip()
        
        if not name:
            return None
        
        # Parse all sections
        profile_details = parse_profile_details(soup)
        communications = parse_communications(soup)
        addresses = parse_addresses(soup)
        notary_details = parse_notary_details(soup)
        
        # Extract last updated date
        last_updated = None
        updated_text = soup.find(string=re.compile('last updated'))
        if updated_text:
            date_match = re.search(r'(\d{1,2}/\d{1,2}/\d{4})', updated_text)
            if date_match:
                last_updated = date_match.group(1)
        
        notary_data = {
            'name': name,
            'location': location,
            'phone': communications.get('phone'),
            'email': communications.get('email'),
            'website': communications.get('website'),
            'addresses': addresses if addresses else [],
            'last_updated': last_updated,
            **profile_details,
            **notary_details
        }
        
        # Debug output
        print(f"  - Name: {name}")
        print(f"  - Phone: {communications.get('phone')}")
        print(f"  - Email: {communications.get('email')}")
        print(f"  - Website: {communications.get('website')}")
        
        return notary_data
        
    except Exception as e:
        print(f"Error scraping {url}: {e}", file=sys.stderr)
        return None

def scrape_notary_listing() -> List[str]:
    """Scrape the listing page to get all notary detail URLs."""
    try:
        response = requests.get(LISTING_URL, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        detail_urls = []
        
        # Find all links to detail pages
        # Links are in format: details.asp?ID=...
        for link in soup.find_all('a', href=True):
            href = link['href']
            if 'details.asp' in href:
                full_url = urljoin(BASE_URL + '/agent/', href)
                if full_url not in detail_urls:
                    detail_urls.append(full_url)
        
        return detail_urls
        
    except Exception as e:
        print(f"Error scraping listing page: {e}", file=sys.stderr)
        return []

def main():
    """Main function to scrape all notaries and generate YAML."""
    print("Fetching notary listing page...")
    detail_urls = scrape_notary_listing()
    
    if not detail_urls:
        print("No notary detail URLs found.", file=sys.stderr)
        return 1
    
    print(f"Found {len(detail_urls)} notaries. Scraping detail pages...")
    
    notaries = []
    for i, url in enumerate(detail_urls, 1):
        print(f"Scraping {i}/{len(detail_urls)}: {url}")
        notary_data = scrape_notary_detail(url)
        if notary_data:
            notaries.append(notary_data)
        
        # Be polite - add delay between requests
        if i < len(detail_urls):
            time.sleep(1)
    
    print(f"\nSuccessfully scraped {len(notaries)} notaries.")
    
    # Write to YAML file
    output_file = '_data/notaries.yml'
    with open(output_file, 'w') as f:
        yaml.dump(notaries, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    
    print(f"Data written to {output_file}")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
