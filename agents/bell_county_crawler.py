import requests
from bs4 import BeautifulSoup
import json
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BellCountyElectionsAgent:
    """Discovery Agent for monitoring and documenting Bell County elections and officials."""

    BASE_URL = "https://www.bellcountytx.com"
    NOTICES_URL = f"{BASE_URL}/departments/elections/Notices.php"
    MINUTES_URL = f"{BASE_URL}/departments/elections/meeting_agendas_and_minutes.php"
    OFFICIALS_URL = f"{BASE_URL}/about_us/elected_officials/index.php"
    PUBLIC_NOTICE_URL = f"{BASE_URL}/publicnotice_detail_T3_R730.php"
    SOS_TEXAS_URL = "https://www.sos.state.tx.us/elections/voter/important-election-dates.shtml"

    def __init__(self, output_dir: str = "./bell_county_data"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Legal-Luminary-Agent/1.0"
        })
        self.notices = []
        self.minutes = []
        self.officials = []
        self.sos_dates = []

    def fetch_soup(self, url):
        """Helper to fetch and parse HTML."""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            return None

    def crawl_notices(self):
        """Crawls general election notices."""
        logger.info(f"Crawling notices from {self.NOTICES_URL}")
        soup = self.fetch_soup(self.NOTICES_URL)
        if not soup: return

        links = soup.find_all('a', href=True)
        for link in links:
            if 'notice' in link.get_text().lower() or '.pdf' in link['href'].lower():
                href = link['href']
                if href.startswith('/'):
                    href = self.BASE_URL + href
                self.notices.append({
                    "title": link.get_text(strip=True),
                    "url": href,
                    "timestamp": datetime.now().isoformat()
                })

    def crawl_minutes(self):
        """Crawls meeting minutes and agendas."""
        logger.info(f"Crawling minutes from {self.MINUTES_URL}")
        soup = self.fetch_soup(self.MINUTES_URL)
        if not soup: return

        links = soup.find_all('a', href=True)
        for link in links:
            text = link.get_text(strip=True).lower()
            if 'agenda' in text or 'minute' in text or '.pdf' in link['href'].lower():
                href = link['href']
                if href.startswith('/'):
                    href = self.BASE_URL + href
                self.minutes.append({
                    "title": link.get_text(strip=True),
                    "url": href,
                    "timestamp": datetime.now().isoformat()
                })

    def crawl_public_notices(self):
        """Crawls priority public notice details."""
        logger.info(f"Crawling public notices from {self.PUBLIC_NOTICE_URL}")
        soup = self.fetch_soup(self.PUBLIC_NOTICE_URL)
        if not soup: return

        # Look for notice content
        content_div = soup.find('div', class_='freeform')
        if content_div:
            self.notices.append({
                "title": "Priority Public Notice",
                "content": content_div.get_text(strip=True)[:500], # excerpt
                "url": self.PUBLIC_NOTICE_URL,
                "timestamp": datetime.now().isoformat()
            })

    def crawl_elected_officials(self):
        """Extracts initial list of elected officials."""
        logger.info(f"Crawling elected officials from {self.OFFICIALS_URL}")
        soup = self.fetch_soup(self.OFFICIALS_URL)
        if not soup: return

        # Standard extraction (depends on layout, extracting basic links/names)
        content_div = soup.find(id='main-content')
        if content_div:
            paragraphs = content_div.find_all('p')
            for p in paragraphs:
                text = p.get_text(strip=True)
                if text and len(text) > 5:
                    self.officials.append({
                        "raw_text": text,
                        "timestamp": datetime.now().isoformat()
                    })

    def crawl_sos_dates(self):
        """Extracts Texas state election dates."""
        logger.info(f"Crawling SOS dates from {self.SOS_TEXAS_URL}")
        soup = self.fetch_soup(self.SOS_TEXAS_URL)
        if not soup: return

        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all(['td', 'th'])
                col_texts = [c.get_text(strip=True) for c in cols]
                if col_texts and len(col_texts) >= 2:
                    self.sos_dates.append({
                        "event": col_texts[0],
                        "date": col_texts[1],
                        "timestamp": datetime.now().isoformat()
                    })

    def export_data(self):
        """Exports the crawled data."""
        data = {
            "source": "Bell County Discovery Agent",
            "last_updated": datetime.now().isoformat(),
            "notices_count": len(self.notices),
            "minutes_count": len(self.minutes),
            "officials_count": len(self.officials),
            "sos_dates_count": len(self.sos_dates),
            "notices": self.notices,
            "minutes": self.minutes,
            "officials": self.officials,
            "sos_dates": self.sos_dates
        }

        output_file = self.output_dir / "bell_county_discovery.json"
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        logger.info(f"Data exported to {output_file}")

    def run(self):
        """Runs the full discovery phase pipeline."""
        logger.info("Starting Bell County Discovery Agent")
        self.crawl_notices()
        self.crawl_minutes()
        self.crawl_public_notices()
        self.crawl_elected_officials()
        self.crawl_sos_dates()
        self.export_data()

if __name__ == "__main__":
    agent = BellCountyElectionsAgent()
    agent.run()
