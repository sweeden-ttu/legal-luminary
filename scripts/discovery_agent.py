import os
import requests
from bs4 import BeautifulSoup
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("DiscoveryAgent")

class DiscoveryAgent:
    def __init__(self):
        self.entry_points = [
            "https://www.bellcountytx.com/county_government/",
            "https://www.bellcountytx.com/about_us/elected_officials/index.php",
            "https://www.bellcountytx.com/about_us/public_records.php",
            "https://www.bellcountytx.com/county_government/index.php",
            "https://www.bellcountytx.com/publicnotice_detail_T3_R730.php",
            "https://www.bellcountytx.com/departments/elections/meeting_agendas_and_minutes.php",
            "https://www.bellcountytx.com/departments/elections/Notices.php",
            "https://www.sos.state.tx.us/elections/voter/important-election-dates.shtml"
        ]
        self.discovered_officials = []
        self.output_dir = "modules/judiciary-rd-agent/data"
        os.makedirs(self.output_dir, exist_ok=True)

    def scrape_url(self, url):
        logger.info(f"Scraping {url}")
        try:
            # We add a User-Agent to avoid 403 Forbidden errors
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            logger.error(f"Failed to scrape {url}: {e}")
            return None

    def run(self):
        logger.info("Initializing Phase 1: Knowledge Acquisition")
        for url in self.entry_points:
            soup = self.scrape_url(url)
            if soup:
                # Basic extraction logic, could be expanded using LLM or more specific rules
                logger.info(f"Successfully retrieved content from {url}")
                # Storing raw text for now as a mock discovery step
                text_content = soup.get_text(separator=' ', strip=True)[:500]
                self.discovered_officials.append({
                    "source": url,
                    "content_preview": text_content
                })

        output_file = os.path.join(self.output_dir, "initial_discovery.json")
        with open(output_file, 'w') as f:
            json.dump(self.discovered_officials, f, indent=4)
        logger.info(f"Discovery phase complete. Results saved to {output_file}")

if __name__ == "__main__":
    agent = DiscoveryAgent()
    agent.run()
