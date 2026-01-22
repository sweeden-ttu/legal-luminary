#!/usr/bin/env python3
"""
Check all external links on the Jekyll site for 404 errors.
Scans pages, posts, includes, and layouts for external links and verifies their status.
"""

import os
import re
import json
import sys
import time
from pathlib import Path
from typing import List, Dict, Set, Optional
from urllib.parse import urlparse, urljoin
import requests
from bs4 import BeautifulSoup

# Site configuration
SITE_URL = "https://www.legalluminary.com"
BASE_DIR = Path(__file__).parent.parent
PAGES_DIR = BASE_DIR / "_pages"
POSTS_DIR = BASE_DIR / "_posts"
INCLUDES_DIR = BASE_DIR / "_includes"
LAYOUTS_DIR = BASE_DIR / "_layouts"
OUTPUT_FILE = BASE_DIR / "_data" / "brokenlinks.json"

# Directories to scan
SCAN_DIRS = [
    (PAGES_DIR, "page"),
    (POSTS_DIR, "post"),
    (INCLUDES_DIR, "include"),
    (LAYOUTS_DIR, "layout"),
]

# Request settings
REQUEST_TIMEOUT = 10
REQUEST_DELAY = 0.5  # Delay between requests to be polite
MAX_RETRIES = 2

def extract_links_from_markdown(content: str, file_path: Path) -> List[Dict[str, str]]:
    """Extract links from Markdown content."""
    links = []
    
    # Extract markdown links: [text](url)
    markdown_link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    for match in re.finditer(markdown_link_pattern, content):
        link_text = match.group(1)
        link_url = match.group(2)
        # Skip if it's a reference-style link (we'll handle those separately)
        if not link_url.startswith('['):
            links.append({
                'url': link_url,
                'text': link_text,
                'source': 'markdown'
            })
    
    # Extract reference-style markdown links: [text][ref] and [ref]: url
    # First find all link references
    ref_pattern = r'^\s*\[([^\]]+)\]:\s*(.+?)(?:\s+"([^"]+)")?\s*$'
    refs = {}
    for line in content.split('\n'):
        match = re.match(ref_pattern, line)
        if match:
            ref_id = match.group(1).lower()
            ref_url = match.group(2).strip()
            ref_title = match.group(3) if match.group(3) else None
            refs[ref_id] = {'url': ref_url, 'title': ref_title}
    
    # Now find uses of references: [text][ref] or [text][]
    ref_use_pattern = r'\[([^\]]+)\]\[([^\]]*)\]'
    for match in re.finditer(ref_use_pattern, content):
        link_text = match.group(1)
        ref_id = match.group(2).lower() if match.group(2) else link_text.lower()
        if ref_id in refs:
            links.append({
                'url': refs[ref_id]['url'],
                'text': link_text,
                'source': 'markdown_ref'
            })
    
    # Extract HTML links in markdown: <a href="url">text</a>
    html_link_pattern = r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>([^<]*)</a>'
    for match in re.finditer(html_link_pattern, content, re.IGNORECASE):
        link_url = match.group(1)
        link_text = match.group(2).strip()
        # Remove HTML tags from link text
        link_text = re.sub(r'<[^>]+>', '', link_text).strip()
        links.append({
            'url': link_url,
            'text': link_text or link_url,
            'source': 'html_in_markdown'
        })
    
    # Also parse as HTML to catch any HTML links we might have missed
    try:
        soup = BeautifulSoup(content, 'html.parser')
        for anchor in soup.find_all('a', href=True):
            href = anchor.get('href', '').strip()
            text = anchor.get_text(strip=True) or href
            # Avoid duplicates
            if not any(l['url'] == href for l in links):
                links.append({
                    'url': href,
                    'text': text,
                    'source': 'html_in_markdown'
                })
    except:
        pass
    
    return links

def extract_links_from_html(content: str, file_path: Path) -> List[Dict[str, str]]:
    """Extract links from HTML content."""
    links = []
    soup = BeautifulSoup(content, 'html.parser')
    
    for anchor in soup.find_all('a', href=True):
        href = anchor.get('href', '').strip()
        text = anchor.get_text(strip=True) or href
        links.append({
            'url': href,
            'text': text,
            'source': 'html'
        })
    
    return links

def is_external_link(url: str) -> bool:
    """Check if a URL is external (not relative to the site)."""
    if not url:
        return False
    
    # Skip special protocols
    if url.startswith(('mailto:', 'tel:', 'javascript:', '#', '/')):
        return False
    
    # Check if it's an absolute URL
    if url.startswith(('http://', 'https://')):
        try:
            parsed = urlparse(url)
            site_parsed = urlparse(SITE_URL)
            # External if different domain
            return parsed.netloc and parsed.netloc != site_parsed.netloc
        except:
            return False
    
    return False

def extract_contact_info(content: str, url: str) -> Dict[str, Optional[str]]:
    """Extract phone numbers and email addresses from page content."""
    contact_info = {
        'phone': None,
        'email': None
    }
    
    soup = BeautifulSoup(content, 'html.parser')
    text = soup.get_text()
    
    # Extract phone numbers - patterns like (254) 933-5160, 254-933-5160, 254.933.5160
    phone_patterns = [
        r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
        r'\d{3}\.\d{3}\.\d{4}',
    ]
    
    phones_found = []
    for pattern in phone_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            # Filter out common false positives (years, zip codes, etc.)
            if len(match.replace('(', '').replace(')', '').replace('-', '').replace('.', '').replace(' ', '')) == 10:
                phones_found.append(match)
    
    # Prefer phone numbers that appear near "phone", "call", "contact", "main", etc.
    phone_context_pattern = r'(?:phone|call|contact|main|number|tel)[:\s]*\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    context_matches = re.findall(phone_context_pattern, text, re.IGNORECASE)
    if context_matches:
        for match in context_matches:
            phone = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', match)
            if phone:
                contact_info['phone'] = phone.group(0)
                break
    
    # If no context match, use first valid phone found
    if not contact_info['phone'] and phones_found:
        contact_info['phone'] = phones_found[0]
    
    # Extract email addresses
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails_found = re.findall(email_pattern, text)
    
    # Prefer emails from county/government domains
    for email in emails_found:
        if any(domain in email.lower() for domain in ['county', 'gov', 'texas', 'bell']):
            contact_info['email'] = email
            break
    
    # If no government email found, use first email
    if not contact_info['email'] and emails_found:
        contact_info['email'] = emails_found[0]
    
    return contact_info

def check_link_status(url: str, extract_contacts: bool = False) -> Dict[str, any]:
    """Check if a link returns a 404 error. Optionally extract contact info."""
    error_404 = False
    status_code = None
    error_message = None
    contact_info = {'phone': None, 'email': None}
    
    try:
        # Normalize URL
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Make request with retries
        response_content = None
        for attempt in range(MAX_RETRIES + 1):
            try:
                response = requests.head(
                    url,
                    timeout=REQUEST_TIMEOUT,
                    allow_redirects=True,
                    headers={
                        'User-Agent': 'Mozilla/5.0 (compatible; LegalLuminaryLinkChecker/1.0)'
                    }
                )
                status_code = response.status_code
                
                # Check for 404
                if status_code == 404:
                    error_404 = True
                # Some servers return 405 for HEAD, try GET
                elif status_code == 405:
                    response = requests.get(
                        url,
                        timeout=REQUEST_TIMEOUT,
                        allow_redirects=True,
                        headers={
                            'User-Agent': 'Mozilla/5.0 (compatible; LegalLuminaryLinkChecker/1.0)'
                        }
                    )
                    status_code = response.status_code
                    response_content = response.text
                    if status_code == 404:
                        error_404 = True
                    # Also check content for "404" text
                    elif '404' in response.text.lower() or 'not found' in response.text.lower():
                        error_404 = True
                
                break  # Success, exit retry loop
                
            except requests.exceptions.RequestException as e:
                if attempt == MAX_RETRIES:
                    # Last attempt failed
                    error_message = str(e)
                    # Try GET request as fallback
                    try:
                        response = requests.get(
                            url,
                            timeout=REQUEST_TIMEOUT,
                            allow_redirects=True,
                            headers={
                                'User-Agent': 'Mozilla/5.0 (compatible; LegalLuminaryLinkChecker/1.0)'
                            }
                        )
                        status_code = response.status_code
                        response_content = response.text
                        if status_code == 404:
                            error_404 = True
                        elif '404' in response.text.lower() or 'not found' in response.text.lower():
                            error_404 = True
                    except:
                        pass
                else:
                    time.sleep(0.5)  # Brief delay before retry
        
        # Extract contact info if requested and page loaded successfully
        if extract_contacts and response_content and not error_404 and status_code == 200:
            contact_info = extract_contact_info(response_content, url)
        
    except Exception as e:
        error_message = str(e)
    
    result = {
        'error_404': error_404,
        'status_code': status_code,
        'error_message': error_message
    }
    
    if extract_contacts:
        result['contact_info'] = contact_info
    
    return result

def scan_file(file_path: Path, file_type: str) -> List[Dict[str, any]]:
    """Scan a single file for external links."""
    links_found = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract links based on file type
        if file_path.suffix == '.md':
            links = extract_links_from_markdown(content, file_path)
        elif file_path.suffix == '.html':
            links = extract_links_from_html(content, file_path)
        else:
            return links_found
        
        # Filter for external links only
        for link in links:
            if is_external_link(link['url']):
                links_found.append({
                    'link_name': link['text'],
                    'link_url': link['url'],
                    'source_file': str(file_path.relative_to(BASE_DIR)),
                    'source_type': file_type
                })
    
    except Exception as e:
        print(f"Error scanning {file_path}: {e}", file=sys.stderr)
    
    return links_found

def main():
    """Main function to scan all files and check links."""
    print("Scanning site for external links...")
    
    all_links: List[Dict[str, any]] = []
    seen_links: Set[str] = set()
    
    # Scan all directories
    for scan_dir, file_type in SCAN_DIRS:
        if not scan_dir.exists():
            print(f"Warning: Directory {scan_dir} does not exist", file=sys.stderr)
            continue
        
        print(f"Scanning {file_type} files in {scan_dir.name}...")
        
        for file_path in scan_dir.rglob('*'):
            if file_path.is_file() and file_path.suffix in ['.md', '.html']:
                links = scan_file(file_path, file_type)
                for link in links:
                    # Use URL as key to avoid duplicates
                    link_key = link['link_url'].lower()
                    if link_key not in seen_links:
                        seen_links.add(link_key)
                        # Initialize source_files as a list
                        link['source_files'] = [link['source_file']]
                        all_links.append(link)
                    else:
                        # Add source file to existing link
                        existing = next(l for l in all_links if l['link_url'].lower() == link_key)
                        if link['source_file'] not in existing['source_files']:
                            existing['source_files'].append(link['source_file'])
    
    print(f"\nFound {len(all_links)} unique external links")
    print("Checking links for 404 errors...")
    
    # Check each link
    broken_links = []
    checked_count = 0
    
    for link in all_links:
        checked_count += 1
        url = link['link_url']
        print(f"[{checked_count}/{len(all_links)}] Checking: {url}")
        
        # For broken links to county/government sites, extract contact info
        is_county_site = any(domain in url.lower() for domain in ['county', 'gov', 'bellcounty', 'templetx', 'beltontexas', 'killeentexas'])
        extract_contacts = is_county_site
        
        status = check_link_status(url, extract_contacts=extract_contacts)
        link['error_404'] = status['error_404']
        link['status_code'] = status['status_code']
        if status['error_message']:
            link['error_message'] = status['error_message']
        
        # Add contact info if extracted
        if 'contact_info' in status:
            link['contact_phone'] = status['contact_info'].get('phone')
            link['contact_email'] = status['contact_info'].get('email')
        
        if status['error_404']:
            broken_links.append(link)
            print(f"  ✗ BROKEN (404)")
            if 'contact_info' in status and (status['contact_info'].get('phone') or status['contact_info'].get('email')):
                print(f"    Contact: {status['contact_info'].get('phone') or ''} {status['contact_info'].get('email') or ''}")
        elif status['status_code']:
            print(f"  ✓ OK ({status['status_code']})")
        else:
            print(f"  ? UNKNOWN")
        
        # Be polite - delay between requests
        if checked_count < len(all_links):
            time.sleep(REQUEST_DELAY)
    
    # Prepare output data
    output_data = {
        'last_checked': time.strftime('%Y-%m-%d %H:%M:%S'),
        'total_links': len(all_links),
        'broken_links_count': len(broken_links),
        'links': all_links
    }
    
    # Write to JSON file
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n=== Summary ===")
    print(f"Total external links: {len(all_links)}")
    print(f"Broken links (404): {len(broken_links)}")
    print(f"Results saved to: {OUTPUT_FILE}")
    
    if broken_links:
        print(f"\nBroken Links:")
        for link in broken_links:
            print(f"  - {link['link_name']}: {link['link_url']}")
            print(f"    Found in: {link.get('source_files', [link['source_file']])}")
    
    return 0 if len(broken_links) == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
