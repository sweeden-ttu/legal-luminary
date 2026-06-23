import json
import os
import yaml
import re

# Posts to add
posts = [
    "_posts/2026-06-21-abbott-slams-democratic-candidates-at-texas-gop-convention.md",
    "_posts/2026-06-21-ken-paxton-easily-defeats-john-cornyn-in-texas-republican-senate-runoff.md",
    "_posts/2026-06-21-texas-man-charged-after-friday-officer-involved-shooting-in-bell-county.md",
    "_posts/2026-06-22-historic-bastrop-brick-company-owner-alleges-fraud-in-29-million-lawsuit.md",
    "_posts/2026-06-22-talarico-hopes-to-turn-ken-paxtons-scandals-into-victory.md"
]

new_entries = []
for p in posts:
    if not os.path.exists(p):
        print(f"File not found: {p}")
        continue
    with open(p, 'r') as f:
        content = f.read()
    
    # Extract YAML frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if match:
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

# Update important_articles.json
with open('_data/important_articles.json', 'r') as f:
    data = json.load(f)

# Remove existing entries for these paths to avoid duplicates
existing_paths = set(p for p in posts)
new_critical = [x for x in data['by_relevance']['critical'] if x.get('path') not in existing_paths]

# Prepend new entries
data['by_relevance']['critical'] = new_entries + new_critical

with open('_data/important_articles.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Updated important_articles.json")

# Remove 'One killed, two injured in crash in Temple' from news-feed.json
with open('_data/news-feed.json', 'r') as f:
    news_data = json.load(f)

def filter_items(items):
    return [i for i in items if 'One killed, two injured in crash in Temple' not in i.get('title', '')]

news_data['all_items'] = filter_items(news_data.get('all_items', []))
for feed in news_data.get('feeds', []):
    feed['items'] = filter_items(feed.get('items', []))
    feed['item_count'] = len(feed['items'])

with open('_data/news-feed.json', 'w') as f:
    json.dump(news_data, f, indent=2)

print("Updated news-feed.json")
