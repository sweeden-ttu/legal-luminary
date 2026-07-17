import os
import json
import glob
import datetime
import re

DATA_DIR = "/Users/sweeden/legal-luminary/_data/articles"
POSTS_DIR = "/Users/sweeden/legal-luminary/_posts"

def parse_post(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    parts = content.split('---', 2)
    if len(parts) >= 3:
        frontmatter_text = parts[1]
        body = parts[2]
    else:
        return None, None
        
    meta = {}
    for line in frontmatter_text.split('\n'):
        if ':' in line:
            key, val = line.split(':', 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            meta[key] = val
    # Generate Jekyll permalink if missing
    if 'permalink' not in meta:
        import os, re
        filename = os.path.basename(filepath)
        m = re.match(r'^(\d{4}-\d{2}-\d{2})-(.+)\.md$', filename)
        if m:
            date_part, slug_part = m.groups()
            category = meta.get('category', 'news')
            meta['permalink'] = f'/{category}/{date_part}-{slug_part}.html'
    return meta, body

def get_post_date(filename, meta):
    # Try meta first
    if 'date' in meta:
        date_str = meta['date'].split(' ')[0] # Handle "2026-06-22 00:00:00 -0500"
        try:
            return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            pass
            
    # Try filename
    match = re.search(r'(\d{4}-\d{2}-\d{2})', os.path.basename(filename))
    if match:
        try:
            return datetime.datetime.strptime(match.group(1), "%Y-%m-%d").date()
        except ValueError:
            pass
            
    return None

def main():
    schemas = glob.glob(os.path.join(DATA_DIR, "*.schema.json"))
    feeds = {}
    
    for schema_file in schemas:
        name = os.path.basename(schema_file).replace(".schema.json", "")
        with open(schema_file, 'r') as f:
            schema_data = json.load(f)
            
        try:
            # Depending on how the schema was generated, the enum might be under definitions or directly in items
            if "definitions" in schema_data:
                keywords = schema_data["definitions"]["article"]["properties"]["matched_keywords"]["items"]["enum"]
            else:
                keywords = schema_data["items"]["properties"]["matched_keywords"]["items"]["enum"]
        except KeyError:
            print(f"Could not find keywords enum in {schema_file}")
            continue
            
        feeds[name] = {
            "keywords": keywords,
            "max_days": 14,
            "articles": []
        }

    posts = glob.glob(os.path.join(POSTS_DIR, "*.md"))
    today = datetime.date.today()
    
    for post_file in posts:
        meta, body = parse_post(post_file)
        if meta is None:
            continue
            
        post_date = get_post_date(post_file, meta)
        if not post_date:
            continue
            
        age_days = (today - post_date).days
        if age_days < 0: # Future post?
            age_days = 0
            
        content_to_search = (meta.get('title', '') + " " + body).lower()
        
        for feed_name, feed_data in feeds.items():
            if age_days > feed_data["max_days"]:
                continue
                
            matched = []
            count = 0
            for kw in feed_data["keywords"]:
                # Use regex word boundaries for precise matching
                matches = len(re.findall(r'\b' + re.escape(kw.lower()) + r'\b', content_to_search))
                if matches > 0:
                    matched.append(kw)
                    count += matches
                    
            if count > 0:
                if count >= 5:
                    relevance = "critical"
                elif count >= 3:
                    relevance = "high"
                elif count >= 2:
                    relevance = "medium"
                else:
                    relevance = "low"
                    
                article_obj = {
                    "title": meta.get('title', 'Untitled'),
                    "date": post_date.strftime("%Y-%m-%d"),
                    "source": meta.get('source', 'Unknown Source'),
                    "url": meta.get('source_url', ''),
                    "path": meta.get('permalink', ''),
                    "score": float(count),
                    "keyword_count": count,
                    "relevance": relevance,
                    "matched_keywords": matched
                }
                feed_data["articles"].append(article_obj)

    # Write output JSONs
    for feed_name, feed_data in feeds.items():
        out_json = {
            "validated_at": datetime.datetime.utcnow().isoformat() + "Z",
            "total_articles": len(feed_data["articles"]),
            "by_relevance": {
                "critical": [a for a in feed_data["articles"] if a["relevance"] == "critical"],
                "high": [a for a in feed_data["articles"] if a["relevance"] == "high"],
                "medium": [a for a in feed_data["articles"] if a["relevance"] == "medium"],
                "low": [a for a in feed_data["articles"] if a["relevance"] == "low"]
            }
        }
        
        out_path = os.path.join(DATA_DIR, f"{feed_name}.json")
        with open(out_path, 'w') as f:
            json.dump(out_json, f, indent=2)
            
        print(f"Updated {feed_name}.json with {len(feed_data['articles'])} articles.")

if __name__ == "__main__":
    main()
