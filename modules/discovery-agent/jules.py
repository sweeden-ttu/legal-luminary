import json
import os
from concurrent.futures import ThreadPoolExecutor
from monitor import MonitorAgent
from analyst import AnalystAgent

class JulesOrchestrator:
    """
    Coordinator grounded in 'Agent-Oriented Programming' (Chapter 4).
    Orchestrates perception and interpretation tasks.
    """

    def __init__(self, output_file="../../_data/recent_articles.json"):
        self.monitor = MonitorAgent()
        self.analyst = AnalystAgent()
        # Ensure path is relative to the script location or absolute
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.output_file = os.path.join(script_dir, output_file)

    def run_discovery_cycle(self):
        """
        Main execution loop:
        1. Perception (Monitor)
        2. Interpretation (Analyst)
        3. Memory/Storage (Archivist)
        """
        print("Starting Jules Discovery Cycle...")
        
        # Step 1: Perception
        articles = self.monitor.run_all()
        print(f"Perception complete. {len(articles)} articles found.")

        # Step 2: Interpretation (using parallelism for ranking)
        print("Starting Interpretation and Ranking...")
        final_results = []
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            # We map the ranking task across all articles
            # In a more complex version, we'd use 'speculative parallelism' 
            # to rank items as they come in.
            results = list(executor.map(self.process_article, articles))
            
        # Filter out Low confidence if desired, or keep all
        final_results = [r for r in results if r['analysis']['confidence_score'] > 0]
        
        # Sort by confidence
        final_results.sort(key=lambda x: x['analysis']['confidence_score'], reverse=True)

        # Step 3: Archive / Save
        self.save_results(final_results)
        print(f"Cycle complete. {len(final_results)} articles ranked and archived.")

    def process_article(self, article):
        """Helper to combine perception and analysis."""
        analysis = self.analyst.rank_article(article)
        article['analysis'] = analysis
        return article

    def save_results(self, results):
        """Saves the output to the specified data file."""
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        
        with open(self.output_file, 'w') as f:
            json.dump(results, f, indent=2)

if __name__ == "__main__":
    jules = JulesOrchestrator()
    jules.run_discovery_cycle()
