import os
import sqlite3
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
import tempfile
import pdfplumber
import subprocess

try:
    from docling.document_converter import DocumentConverter
    DOCLING_AVAILABLE = True
except ImportError:
    DOCLING_AVAILABLE = False

DB_PATH = 'judicial_officials.db'

def get_urls_from_agents_md():
    """Extracts URLs dynamically from AGENTS.md passed via environment variable."""
    urls = []
    context = os.environ.get("AGENTS_CONTEXT", "")
    if context:
        # Look for typical markdown link patterns or raw URLs
        found_urls = re.findall(r'(https?://[^\s]+)', context)
        # Strip trailing punctuation
        urls = [re.sub(r'[)\]}>,\'"]$', '', u) for u in found_urls]

    # If empty for some reason, fallback to defaults
    if not urls:
        print("Warning: No URLs found in AGENTS_CONTEXT. Using defaults.")
        urls = [
            "https://www.bellcountytx.com/publicnotice_detail_T3_R730.php",
            "https://www.bellcountytx.com/county_government/index.php",
            "https://www.bellcountytx.com/about_us/elected_officials/index.php",
            "https://www.bellcountytx.com/about_us/public_records.php",
            "https://www.bellcountytx.com/departments/elections/meeting_agendas_and_minutes.php",
            "https://www.bellcountytx.com/departments/elections/Notices.php"
        ]
    return list(set(urls))

URLS = get_urls_from_agents_md()


def setup_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create the judicial_officials table with ALL requested columns
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS judicial_officials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            title TEXT,
            office_name TEXT,
            precinct TEXT,
            is_elected BOOLEAN,
            term_start_year INTEGER,
            term_end_year INTEGER,
            re_election_year INTEGER,
            cases_studied TEXT,
            headshot_base64 TEXT,
            social_media_links TEXT,
            news_articles TEXT,
            previous_role TEXT,
            source_url TEXT NOT NULL,
            verified BOOLEAN DEFAULT 0,
            last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
            political_affiliation TEXT,
            education_law_school TEXT,
            year_admitted_to_bar INTEGER,
            appointing_governor TEXT,
            bar_number TEXT,
            contact_phone TEXT,
            contact_email TEXT,
            court_address TEXT,
            chief_clerk_name TEXT,
            judicial_philosophy_or_statements TEXT
        )
    ''')
    conn.commit()
    conn.close()

def resolve_ocr_discrepancy(text_docling, text_plumber):
    """
    Intelligently resolves OCR discrepancies.
    If texts mismatch significantly, it can attempt logic. For now, it leverages
    docling's superior markdown formatting, falling back to pdfplumber text if
    docling's output is strangely short.
    """
    len_d = len(text_docling)
    len_p = len(text_plumber)

    # If one is completely empty, return the other
    if len_d == 0: return text_plumber
    if len_p == 0: return text_docling

    # If they are roughly the same length, docling usually has better structural preservation
    if abs(len_d - len_p) < (0.2 * max(len_d, len_p)):
        return text_docling

    # If one is significantly larger, it probably captured more text correctly
    if len_d > len_p:
        return text_docling
    else:
        return text_plumber

def parse_pdf(url):
    """Downloads a PDF and extracts text using multiple OCR methods including docling."""
    try:
        print(f"Downloading PDF: {url}")
        response = requests.get(url, stream=True, timeout=10)
        if response.status_code == 200:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
                for chunk in response.iter_content(chunk_size=1024):
                    temp_pdf.write(chunk)
                temp_pdf_path = temp_pdf.name

            text_plumber = ""
            text_docling = ""

            try:
                with pdfplumber.open(temp_pdf_path) as pdf:
                    for page in pdf.pages:
                        extracted = page.extract_text()
                        if extracted:
                            text_plumber += extracted + "\n"
            except Exception as e:
                print(f"pdfplumber error on {url}: {e}")

            if DOCLING_AVAILABLE:
                try:
                    converter = DocumentConverter()
                    result = converter.convert(temp_pdf_path)
                    text_docling = result.document.export_to_markdown()
                except Exception as e:
                    print(f"docling error on {url}: {e}")

            final_text = resolve_ocr_discrepancy(text_docling, text_plumber)

            os.remove(temp_pdf_path)
            return final_text
    except Exception as e:
        print(f"Failed to process PDF {url}: {e}")
    return ""

def process_page(url, html):
    """Extracts officials from standard HTML table or list formats"""
    officials = []
    soup = BeautifulSoup(html, 'html.parser')

    # 1. Check for tables first
    tables = soup.find_all('table')
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all(['td', 'th'])
            if len(cols) >= 4:
                title = cols[0].get_text(strip=True)
                name = cols[1].get_text(strip=True)

                if title.lower() == 'title' and name.lower() == 'name':
                    continue

                if name and title and ('judge' in title.lower() or 'commissioner' in title.lower() or 'attorney' in title.lower() or 'clerk' in title.lower()):
                    name = re.sub(r'\s+', ' ', name)
                    parts = name.split()

                    first_name = parts[0] if parts else ""
                    last_name = " ".join(parts[1:]) if len(parts) > 1 else ""
                    contact_phone = cols[3].get_text(strip=True)

                    officials.append({
                        'first_name': first_name,
                        'last_name': last_name,
                        'title': title,
                        'contact_phone': contact_phone,
                        'source_url': url
                    })

    # 2. Check for explicit paragraphs or headers
    elements = soup.find_all(['h2', 'h3', 'h4', 'p', 'li', 'a'])
    for el in elements:
        text = el.get_text(strip=True)
        if re.search(r'Judge\s+[A-Z][a-z]+', text):
            match = re.search(r'Judge\s+([A-Z][a-z]+)\s+([A-Z][a-z]+)', text)
            if match:
                first = match.group(1)
                last = match.group(2)
                if not any(o['first_name'] == first and o['last_name'] == last for o in officials):
                    officials.append({
                        'first_name': first,
                        'last_name': last,
                        'title': 'Judge',
                        'source_url': url
                    })

    return officials

def extract_officials_from_text(text, source_url):
    """Basic extraction of officials from raw text (e.g. OCR'd PDF)"""
    officials = []
    lines = text.split('\n')
    for line in lines:
        if re.search(r'(Judge|Commissioner|Attorney)\s+([A-Z][a-z]+)\s+([A-Z][a-z]+)', line):
            match = re.search(r'(Judge|Commissioner|Attorney)\s+([A-Z][a-z]+)\s+([A-Z][a-z]+)', line)
            if match:
                title = match.group(1)
                first = match.group(2)
                last = match.group(3)
                officials.append({
                    'first_name': first,
                    'last_name': last,
                    'title': title,
                    'source_url': source_url
                })
    return officials

def crawl_and_extract():
    visited = set()
    to_visit = list(URLS)
    officials_found = []

    while to_visit:
        url = to_visit.pop(0)
        if url in visited:
            continue
        visited.add(url)

        print(f"Crawling: {url}")
        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                continue

            content_type = response.headers.get('content-type', '')
            if 'application/pdf' in content_type.lower() or url.lower().endswith('.pdf'):
                text = parse_pdf(url)
                if text:
                    new_officials = extract_officials_from_text(text, url)
                    officials_found.extend(new_officials)
            elif 'text/html' in content_type.lower():
                html = response.text
                new_officials = process_page(url, html)
                officials_found.extend(new_officials)

                soup = BeautifulSoup(html, 'html.parser')
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    full_url = urljoin(url, href)
                    if full_url.lower().endswith('.pdf') and full_url not in visited:
                        to_visit.append(full_url)

        except Exception as e:
            print(f"Error crawling {url}: {e}")

    return officials_found

def insert_into_db(officials):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    count = 0
    for official in officials:
        cursor.execute("SELECT id FROM judicial_officials WHERE first_name=? AND last_name=? AND title=?",
                       (official['first_name'], official['last_name'], official['title']))
        if not cursor.fetchone():
            contact_phone = official.get('contact_phone', None)
            if contact_phone:
                contact_phone = re.sub(r'[^\x00-\x7F]+', '', contact_phone)

            cursor.execute('''
                INSERT INTO judicial_officials (first_name, last_name, title, contact_phone, source_url)
                VALUES (?, ?, ?, ?, ?)
            ''', (official['first_name'], official['last_name'], official['title'], contact_phone, official['source_url']))
            count += 1

    conn.commit()
    conn.close()
    print(f"Inserted {count} new judicial officials into the database.")

if __name__ == '__main__':
    print("Starting Discovery Agent...")
    setup_database()
    officials = crawl_and_extract()
    print(f"Found {len(officials)} potential officials.")
    if officials:
        insert_into_db(officials)
    print("Discovery Phase Complete.")
