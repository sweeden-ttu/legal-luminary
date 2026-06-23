import json
import os
import yaml
import re
import sys

def main():
    if len(sys.argv) < 2:
        print("No files provided.")
        return

    posts = sys.argv[1:]
    new_entries = []

    for p in posts:
        if not p.startswith("_posts/") or not p.endswith(".md"):
            continue
        if not os.path.exists(p):
            print(f"File not found: {p}")
            continue
        
        with open(p, 'r') as f:
            content = f.read()
        
        # Extract YAML frontmatter
        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if match:
            try:
                fm = yaml.safe_load(match.group(1))
                entry = {
                    "title": fm.get('title', ''),
                    "date": str(fm.get('date', ''))[:10],
                    "source": fm.get('source', 'Legal Luminary'),
                    "url": fm.get('source_url', ''),
                    "path": p,
                    "score": 1000,
                    "matched_keywords": [],
                    "relevance": "critical"
                }
                new_entries.append(entry)
            except Exception as e:
                print(f"Error parsing yaml in {p}: {e}")

    if not new_entries:
        print("No valid new entries found.")
        return

    data_file = '_data/important_articles.json'
    if not os.path.exists(data_file):
        print(f"{data_file} not found.")
        return

    with open(data_file, 'r') as f:
        data = json.load(f)

    if 'by_relevance' not in data or 'critical' not in data['by_relevance']:
        print("Invalid important_articles.json format.")
        return

    # Remove existing entries for these paths to avoid duplicates
    existing_paths = set(e['path'] for e in new_entries)
    new_critical = [x for x in data['by_relevance']['critical'] if x.get('path') not in existing_paths]

    # Prepend new entries
    data['by_relevance']['critical'] = new_entries + new_critical

    with open(data_file, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"Successfully updated {data_file} with {len(new_entries)} articles.")

if __name__ == '__main__':
    main()
