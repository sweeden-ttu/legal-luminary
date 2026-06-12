import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import feedparser
from duckduckgo_search import DDGS
import os

class MonitorAgent:
    """
    Perception Agent grounded in 'Agents in Trustworthy' (Section 2.1.1).
    Scans government sites, news feeds, and search engines for recent content.
    """

    def __init__(self, lookback_days=30):
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
                    "published": published.isoformat(),
                    "type": "news"
                })
        return results

    def search_duckduckgo(self, query):
        """Searches DuckDuckGo for latest news."""
        print(f"Searching DuckDuckGo for: {query}")
        results = []
        with DDGS() as ddgs:
            # Get latest news from the last week
            for r in ddgs.news(query, max_results=10):
                results.append({
                    "title": r['title'],
                    "link": r['url'],
                    "content": r['body'],
                    "source": "DuckDuckGo",
                    "published": datetime.now().isoformat(), # DDG news results often lack exact timestamp in this format
                    "type": "news"
                })
        return results

    def scan_killeen_agendas(self):
        """
        Specific scraper for Killeen Agenda Center.
        Finds and downloads meeting minutes and agendas.
        """
        # Using the main Agendas & Minutes portal
        url = "https://www.killeentexas.gov/284/Agendas-Minutes"
        print(f"Scanning Killeen Agendas: {url}")
        results = []
        try:
            response = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # This is a bit complex as it might use an iframe or Legistar links.
            # Simpler-First: Look for recent links to Agendas/Minutes
            # Often they are in a table or list
            links = soup.find_all('a', href=True)
            for link in links:
                text = link.text.lower()
                href = link['href']
                if 'agenda' in text or 'minutes' in text:
                    full_url = requests.compat.urljoin(url, href)
                    if full_url.endswith('.pdf'):
                        results.append({
                            "title": f"Killeen City Council {link.text.strip()}",
                            "link": full_url,
                            "content": f"Meeting document: {link.text.strip()}",
                            "source": "Killeen Gov",
                            "published": datetime.now().isoformat(),
                            "type": "meeting_doc"
                        })
            
            return results
        except Exception as e:
            print(f"Error scanning Killeen: {e}")
            return []

    def run_all(self):
        """Executes all perception tasks."""
        all_results = []
        
        # News feeds
        feeds = [
            "https://www.kdhnews.com/search/?f=rss&t=article&l=50&s=start_time&sd=desc&c[]=local*",
            "https://communityimpact.com/feed/",
            "https://www.texastribune.org/feeds/main/",
            "https://www.tdtnews.com/search/?f=rss&t=article&l=50&s=start_time&sd=desc"
        ]
        
        for f in feeds:
            try:
                results = self.scan_rss_feed(f)
                all_results.extend(results)
            except Exception as e:
                print(f"Error scanning feed {f}: {e}")
            
        # Search integration
        queries = [
            "Bell County Texas latest news",
            "Killeen Texas city council news",
            "Temple Texas legal news",
            "Texas governor election 2026"
        ]
        
        for query in queries:
            try:
                search_results = self.search_duckduckgo(query)
                all_results.extend(search_results)
            except Exception as e:
                print(f"Error searching DuckDuckGo for '{query}': {e}")

        # Meeting documents
        try:
            meeting_results = self.scan_killeen_agendas()
            all_results.extend(meeting_results)
        except Exception as e:
            print(f"Error scanning meetings: {e}")
        
        return all_results

if __name__ == "__main__":
    monitor = MonitorAgent()
    results = monitor.run_all()
    print(f"Found {len(results)} recent items.")
