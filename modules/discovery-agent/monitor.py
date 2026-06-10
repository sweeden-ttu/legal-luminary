import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import feedparser

class MonitorAgent:
    """
    Perception Agent grounded in 'Agents in Trustworthy' (Section 2.1.1).
    Scans government sites and news feeds for recent relevant content.
    """

    def __init__(self, lookback_days=60):
        self.lookback_days = lookback_days
        self.cutoff_date = datetime.now() - timedelta(days=lookback_days)

    def scan_rss_feed(self, feed_url):
        """Scans an RSS feed and filters by date."""
        print(f"Scanning RSS feed: {feed_url}")
        feed = feedparser.parse(feed_url)
        results = []
        for entry in feed.entries:
            published = None
            if hasattr(entry, 'published_parsed'):
                published = datetime(*entry.published_parsed[:6])
            elif hasattr(entry, 'updated_parsed'):
                published = datetime(*entry.updated_parsed[:6])
            
            if published and published > self.cutoff_date:
                results.append({
                    "title": entry.title,
                    "link": entry.link,
                    "content": entry.summary if hasattr(entry, 'summary') else "",
                    "source": feed_url,
                    "published": published.isoformat()
                })
        return results

    def scan_killeen_agendas(self):
        """
        Specific scraper for Killeen Agenda Center.
        Simpler-First: Just gets the list of recent agendas.
        """
        url = "https://www.killeentexas.gov/AgendaCenter"
        print(f"Scanning Killeen Agendas: {url}")
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            # This is a placeholder for actual selector logic which varies by site
            # For now, we return a mock structure if we can't find specific tags
            # to demonstrate the flow.
            agendas = []
            # Typical AgendaCenter structure: look for table rows with dates
            rows = soup.find_all('tr', class_='cat-row')
            for row in rows:
                date_cell = row.find('td', class_='date')
                if date_cell:
                    # Parse date and check against cutoff
                    pass
            
            return agendas # Return list of discovered items
        except Exception as e:
            print(f"Error scanning Killeen: {e}")
            return []

    def run_all(self):
        """Executes all perception tasks."""
        all_results = []
        
        # Example feeds
        feeds = [
            "https://www.kdhnews.com/search/?f=rss&t=article&l=10&s=start_time&sd=desc&c[]=local*",
            "https://communityimpact.com/feed/",
            "https://www.texastribune.org/feeds/main/" # Fallback/Verification feed
        ]
        
        for f in feeds:
            results = self.scan_rss_feed(f)
            print(f"Feed {f} returned {len(results)} results.")
            all_results.extend(results)
            
        # all_results.extend(self.scan_killeen_agendas())
        
        return all_results

if __name__ == "__main__":
    monitor = MonitorAgent()
    results = monitor.run_all()
    print(f"Found {len(results)} recent articles.")
