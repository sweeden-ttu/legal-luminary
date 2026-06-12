import json
import os
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup
import subprocess
import tempfile

from monitor import MonitorAgent
from analyst import AnalystAgent
from interpreter import InterpreterAgent
from verifier import VerifierAgent
from publisher import PublisherAgent

class JulesOrchestrator:
    """
    Coordinator grounded in 'Agent-Oriented Programming' (Chapter 4).
    Orchestrates perception, interpretation, verification, and action tasks.
    """

    def __init__(self, output_file="../../_data/recent_articles.json"):
        self.monitor = MonitorAgent()
        self.analyst = AnalystAgent()
        self.interpreter = InterpreterAgent()
        self.verifier = VerifierAgent()
        self.publisher = PublisherAgent()
        
        # Ensure path is relative to the script location or absolute
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.output_file = os.path.join(script_dir, output_file)

    def run_discovery_cycle(self):
        """
        Main execution loop:
        1. Perception (Monitor)
        2. Content Enrichment (Fetch full story or PDF text)
        3. Interpretation & Cleaning (Interpreter)
        4. Ranking (Analyst)
        5. Verification (Verifier)
        6. Publication (Publisher)
        """
        print("Starting Jules News Automation Cycle...")
        
        # Step 1: Perception
        items = self.monitor.run_all()
        # Cap at 10 items for stability testing
        items = items[:10]
        print(f"Perception complete. {len(items)} potential items found.")

        # Step 2-5: Interpretation, Ranking, Verification in parallel
        print("Starting Pipeline Processing...")
        final_results = []
        
        # Sequential processing for local Ollama stability
        with ThreadPoolExecutor(max_workers=1) as executor:
            results = list(executor.map(self.process_item, items))
            
        # Step 6: Publication
        print(f"Publishing verified items...")
        published_count = 0
        for article in results:
            if not article: continue
            try:
                # Threshold for publishing
                if article.get('verification', {}).get('status') == 'APPROVED' and article.get('analysis', {}).get('confidence_score', 0) >= 2.0:
                    filepath = self.publisher.publish(
                        title=article['title'],
                        content=article['refined_content'],
                        date_str=article.get('published', '').split('T')[0],
                        categories=article.get('type', 'news')
                    )
                    article['published_path'] = filepath
                    print(f"Published: {article['title']} -> {filepath}")
                    published_count += 1
                else:
                    reason = "Low score" if article.get('analysis', {}).get('confidence_score', 0) < 2.0 else "Verifier Rejected"
                    # print(f"Skipping ({reason}): {article['title']} (Score: {article.get('analysis', {}).get('confidence_score')})")
            except Exception as e:
                print(f"Error publishing {article.get('title')}: {e}")

        # Step 7: Archive / Save metadata
        self.save_results(results)
        print(f"Cycle complete. {published_count} items published. {len(results)} metadata entries saved.")

    def process_item(self, item):
        """
        Full pipeline for a single item (news or meeting doc).
        """
        url = item['link']
        item_type = item.get('type', 'news')
        
        # Enrichment
        if item_type == 'meeting_doc' and url.endswith('.pdf'):
            # Download and extract PDF text
            try:
                print(f"Downloading meeting doc: {url}")
                resp = requests.get(url, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
                with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
                    tmp.write(resp.content)
                    tmp_path = tmp.name
                
                # Extract text
                result = subprocess.run(['pdftotext', tmp_path, '-'], capture_output=True, text=True)
                item['raw_content'] = result.stdout
                os.remove(tmp_path)
            except Exception as e:
                print(f"Failed to process PDF {url}: {e}")
                item['raw_content'] = item['content']
        else:
            # Fetch full HTML if content is short
            if len(item.get('content', '')) < 500:
                try:
                    # print(f"Enriching: {url}")
                    response = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
                    if response.status_code == 200:
                        item['raw_content'] = response.text
                    else:
                        item['raw_content'] = item['content']
                except Exception as e:
                    item['raw_content'] = item['content']
            else:
                item['raw_content'] = item['content']

        # Interpretation & Cleaning
        try:
            # print(f"Interpreting: {item['title']}")
            refined = self.interpreter.extract_story(item['raw_content'], url)
            item['refined_content'] = refined
        except Exception as e:
            print(f"Error interpreting {url}: {e}")
            return None

        # Ranking
        analysis = self.analyst.rank_article({
            "title": item['title'],
            "content": item['refined_content']
        })
        item['analysis'] = analysis

        # Verification
        try:
            # print(f"Verifying: {item['title']}")
            verification_raw = self.verifier.verify(item['refined_content'], item['raw_content'], url)
            try:
                json_str = verification_raw.strip()
                if "```json" in json_str:
                    json_str = json_str.split("```json")[1].split("```")[0].strip()
                elif "```" in json_str:
                    json_str = json_str.split("```")[1].split("```")[0].strip()
                item['verification'] = json.loads(json_str)
            except:
                item['verification'] = {"status": "REJECTED", "explanation": "Failed to parse verification response"}
        except Exception as e:
            item['verification'] = {"status": "REJECTED", "explanation": str(e)}

        return item

    def save_results(self, results):
        """Saves the output to the specified data file."""
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        with open(self.output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)

if __name__ == "__main__":
    jules = JulesOrchestrator()
    jules.run_discovery_cycle()
