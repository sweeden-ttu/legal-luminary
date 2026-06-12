#!/usr/bin/env python3
import os
import yaml
import json
import re
from datetime import datetime
from pathlib import Path

# Paths
POSTS_DIR = Path('_posts')
OUTPUT_FILE = Path('_data/important_articles.json')

# Keywords and scores
KEYWORDS = {
    'killeen': 50,
    'city council': 40,
    'budget': 30,
    'murder': 30,
    'arrest': 25,
    'police': 20,
    'court': 20,
    'advertisement': 50,
    'fee schedule': 40,
    'street maintenance fee': 40
}

def get_relevance(score):
    if score >= 100:
        return 'critical'
    if score >= 60:
        return 'high'
    if score >= 30:
        return 'medium'
    return 'low'

def parse_post(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract front matter
        match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not match:
            return None
            
        front_matter = yaml.safe_load(match.group(1))
        body = content[match.end():]
        
        # Calculate score
        score = 0
        title = front_matter.get('title', '').lower()
        full_text = (title + ' ' + body).lower()
        
        matched_keywords = []
        for kw, boost in KEYWORDS.items():
            count = full_text.count(kw)
            if count > 0:
                kw_score = count * boost
                score += kw_score
                matched_keywords.append({
                    'keyword': kw,
                    'priority': 'high' if boost >= 30 else 'medium',
                    'count': count,
                    'score': kw_score
                })
        
        # Boost recent posts (within 7 days of 2026-06-12)
        post_date_str = str(front_matter.get('date', ''))
        # Jekyll dates can be date objects or strings
        if isinstance(front_matter.get('date'), datetime):
             post_date = front_matter.get('date').date()
        else:
             try:
                 post_date = datetime.strptime(post_date_str[:10], '%Y-%m-%d').date()
             except:
                 post_date = datetime(2000, 1, 1).date()
                 
        target_date = datetime(2026, 6, 12).date()
        days_diff = (target_date - post_date).days
        if days_diff <= 7:
            score += 100 - (days_diff * 10)
            
        return {
            'title': front_matter.get('title'),
            'date': post_date.strftime('%Y-%m-%d'),
            'source': front_matter.get('source_name', 'Legal Luminary'),
            'url': front_matter.get('source_url', ''),
            'path': str(file_path),
            'score': int(score),
            'matched_keywords': matched_keywords
        }
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return None

def main():
    articles = []
    for post_file in POSTS_DIR.glob('*.md'):
        article = parse_post(post_file)
        if article:
            articles.append(article)
            
    # Sort by score descending
    articles.sort(key=lambda x: x['score'], reverse=True)
    
    by_relevance = {
        'critical': [],
        'high': [],
        'medium': [],
        'low': []
    }
    
    for article in articles:
        rel = get_relevance(article['score'])
        article['relevance'] = rel
        by_relevance[rel].append(article)
        
    result = {
        'validated_at': datetime(2026, 6, 12, 10, 45).isoformat(),
        'total_articles': len(articles),
        'by_relevance': by_relevance
    }
    
    os.makedirs(OUTPUT_FILE.parent, exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2)
        
    print(f"Successfully updated {OUTPUT_FILE} with {len(articles)} articles.")

if __name__ == '__main__':
    main()
