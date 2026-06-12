#!/usr/bin/env python3
import os
import re
import yaml
import logging
import feedparser
import requests
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# --- Configuration ---
DATA_DIR = Path("_data")
POSTS_DIR = Path("_posts")
CITY_FEED_FILES = [
    DATA_DIR / "bell-county-news.yml",
    DATA_DIR / "killeen-news.yml",
    DATA_DIR / "temple-news.yml",
    DATA_DIR / "copperas-cove-news.yml"
]

LEGAL_KEYWORDS = [
    'court', 'courts', 'judge', 'judges', 'jury', 'trial', 'hearing', 'sentencing',
    'appeal', 'appeals', 'lawsuit', 'lawsuits', 'litigation', 'indict', 'indicted',
    'indictment', 'arraignment', 'plea', 'pleads', 'pleaded', 'convict', 'convicted',
    'conviction', 'acquitted', 'bail', 'bond', 'probation', 'parole', 'warrant',
    'warrants', 'subpoena', 'subpoenas', 'crime', 'criminal', 'murder', 'homicide',
    'shooting', 'robbery', 'burglary', 'theft', 'stolen', 'assault', 'battery',
    'kidnapping', 'rape', 'sexual assault', 'fraud', 'scam', 'arson', 'manslaughter',
    'felony', 'misdemeanor', 'dwi', 'dui', 'police', 'sheriff', 'constable',
    'trooper', 'investigates', 'investigating', 'arrest', 'arrests', 'arrested',
    'charged', 'charges', 'booking', 'booked', 'suspect', 'victim',
    'district attorney', 'prosecutor', 'prosecution', 'public defender',
    'attorney', 'lawyer', 'legal', 'department of justice', 'ice', 'jail',
    'prison', 'inmate', 'incarcerated', 'council', 'budget', 'election'
]

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_feeds():
    all_feeds = []
    for path in CITY_FEED_FILES:
        if not path.exists():
            continue
        try:
            with open(path, 'r') as f:
                config = yaml.safe_load(f)
                if config and 'feeds' in config:
                    city_key = path.stem.replace('-news', '')
                    for feed in config['feeds']:
                        if feed.get('enabled', True):
                            feed['city'] = city_key
                            all_feeds.append(feed)
        except Exception as e:
            logger.error(f"Error loading {path}: {e}")
    return all_feeds

def clean_html(html):
    if not html:
        return ""
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator=' ')
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def get_existing_posts():
    existing = set()
    if not POSTS_DIR.exists():
        return existing
    
    for post_file in POSTS_DIR.glob("*.md"):
        name = post_file.stem
        match = re.match(r'\d{4}-\d{2}-\d{2}-(.+)', name)
        if match:
            existing.add(match.group(1).lower())
    return existing

def generate_slug(title):
    slug = title.lower()
    # Replace non-alphanumeric with hyphens
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    return slug

def rank_story(title, summary):
    haystack = f"{title} {summary}".lower()
    score = 0
    for kw in LEGAL_KEYWORDS:
        if re.search(r'\b' + re.escape(kw) + r'\b', haystack):
            score += 1
    return score

def fetch_items(feeds):
    items = []
    for feed_cfg in feeds:
        url = feed_cfg['url']
        logger.info(f"Fetching feed: {feed_cfg['name']} ({url})")
        try:
            response = requests.get(url, timeout=15, headers={'User-Agent': 'Legal Luminary News Agent/1.0'})
            response.raise_for_status()
            
            feed = feedparser.parse(response.content)
            for entry in feed.entries:
                title = entry.get('title', 'No Title')
                link = entry.get('link', '')
                summary = clean_html(entry.get('summary', entry.get('description', '')))
                
                dt = None
                for date_key in ['published_parsed', 'updated_parsed', 'created_parsed']:
                    if entry.get(date_key):
                        dt = datetime(*entry[date_key][:6])
                        break
                if not dt:
                    dt = datetime.now()
                
                items.append({
                    'title': title,
                    'link': link,
                    'summary': summary,
                    'date': dt,
                    'city': feed_cfg.get('city', 'local'),
                    'source': feed_cfg['name']
                })
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
    return items

def create_jekyll_post(story):
    slug = generate_slug(story['title'])
    if not slug:
        slug = "untitled-story"
    
    date_str = story['date'].strftime('%Y-%m-%d')
    filename = f"{date_str}-{slug}.md"
    filepath = POSTS_DIR / filename
    
    if filepath.exists():
        logger.info(f"Post already exists: {filename}")
        return False

    escaped_title = story['title'].replace('"', '\\"')
    
    content = f"""---
layout: post
title: "{escaped_title}"
date: {story['date'].strftime('%Y-%m-%d %H:%M:%S')}
categories: news
source_url: {story['link']}
source_name: "{story['source']}"
city: {story['city']}
---

{story['summary']}

[Read the full story on {story['source']}]({story['link']})
"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        logger.info(f"Created post: {filename}")
        return True
    except Exception as e:
        logger.error(f"Error writing post {filename}: {e}")
        return False

def main():
    if not POSTS_DIR.exists():
        POSTS_DIR.mkdir(parents=True)
        
    feeds = load_feeds()
    if not feeds:
        logger.error("No feeds found to process.")
        return

    existing_slugs = get_existing_posts()
    logger.info(f"Found {len(existing_slugs)} existing posts.")

    all_items = fetch_items(feeds)
    logger.info(f"Fetched {len(all_items)} total items.")

    new_items = []
    for item in all_items:
        slug = generate_slug(item['title'])
        if slug in existing_slugs:
            continue
        
        item['rank'] = rank_story(item['title'], item['summary'])
        
        if item['rank'] > 0:
            new_items.append(item)

    new_items.sort(key=lambda x: (x['rank'], x['date']), reverse=True)
    selected_items = new_items[:10]
    logger.info(f"Selected {len(selected_items)} new stories for posting.")

    count = 0
    for item in selected_items:
        if create_jekyll_post(item):
            count += 1
            
    logger.info(f"Successfully created {count} new posts.")

if __name__ == "__main__":
    main()
