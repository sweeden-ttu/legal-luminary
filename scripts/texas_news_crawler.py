#!/usr/bin/env python3
"""
Texas News Crawler — LLM-Enhanced Edition

Fetches articles from whitelisted RSS feeds, scores them for legal relevance,
generates rich multi-paragraph summaries using the local Ollama gemma4 model,
and writes Jekyll posts to _posts/.

Deduplicates against existing posts by checking source_url values.
Falls back gracefully if the LLM is unavailable.

Usage:
    python scripts/texas_news_crawler.py
"""

from __future__ import annotations

import datetime
import html
import logging
import re
import ssl
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
POSTS_DIR = PROJECT_ROOT / "_posts"
RSS_FEEDS_YML = PROJECT_ROOT / "_data" / "rss-feeds.yml"

sys.path.insert(0, str(SCRIPT_DIR))
from write_post import write_new_post, slug_from_title
from llm_article_writer import generate_article_body, generate_excerpt, strip_html

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# Try to import yaml; fall back to simple parsing if unavailable
try:
    import yaml
except ImportError:
    yaml = None  # type: ignore[assignment]


# ---------------------------------------------------------------------------
# Legal relevance keywords (from AGENTS.md + news_agent.py)
# ---------------------------------------------------------------------------

LEGAL_KEYWORDS = [
    "court", "courts", "judge", "judges", "jury", "trial", "hearing",
    "sentencing", "appeal", "appeals", "lawsuit", "lawsuits", "litigation",
    "indict", "indicted", "indictment", "arraignment", "plea", "pleads",
    "convict", "convicted", "conviction", "acquitted", "bail", "bond",
    "probation", "parole", "warrant", "warrants", "crime", "criminal",
    "murder", "homicide", "shooting", "robbery", "burglary", "theft",
    "assault", "battery", "kidnapping", "sexual assault", "fraud", "arson",
    "manslaughter", "felony", "misdemeanor", "dwi", "dui",
    "police", "sheriff", "constable", "trooper", "investigates",
    "investigating", "arrest", "arrests", "arrested", "charged", "charges",
    "suspect", "victim", "district attorney", "prosecutor", "prosecution",
    "attorney", "lawyer", "legal", "jail", "prison", "inmate",
    # Local relevance
    "Bell County", "Killeen", "Temple", "Belton", "Harker Heights",
    "Copperas Cove", "Central Texas", "Texas",
    # Family / personal injury
    "divorce", "child custody", "child support", "personal injury",
    "car accident", "negligence", "compensation",
]


# ---------------------------------------------------------------------------
# Feed parsing (supports RSS 2.0 and Atom)
# ---------------------------------------------------------------------------

ATOM_NS = {"atom": "http://www.w3.org/2005/Atom"}


def _fetch_url(url: str, timeout: int = 15) -> str:
    """Fetch a URL and return the response body as text."""
    req = urllib.request.Request(
        url, headers={"User-Agent": "LegalLuminaryNewsCrawler/2.0"}
    )
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
        return resp.read().decode("utf-8", errors="replace")


def _text(el: ET.Element | None, tag: str, default: str = "") -> str:
    if el is None:
        return default
    child = el.find(tag)
    return (child.text or "").strip() if child is not None else default


def _parse_rss_item(item: ET.Element) -> dict[str, Any] | None:
    title = _text(item, "title")
    link = _text(item, "link") or _text(item, "guid")
    if not title or not link:
        return None
    pub = _text(item, "pubDate") or _text(item, "dc:date") or _text(item, "date")
    desc = _text(item, "description") or _text(item, "content:encoded") or ""
    return {"title": title, "link": link, "date_raw": pub, "raw_excerpt": desc}


def _parse_atom_entry(entry: ET.Element) -> dict[str, Any] | None:
    title_el = entry.find("atom:title", ATOM_NS) or entry.find("title")
    title = (title_el.text or "").strip() if title_el is not None else ""
    link_el = entry.find("atom:link", ATOM_NS) or entry.find("link")
    link = (link_el.get("href") or "").strip() if link_el is not None else ""
    if not title or not link:
        return None
    updated_el = (
        entry.find("atom:updated", ATOM_NS)
        or entry.find("updated")
        or entry.find("published")
    )
    date_raw = (updated_el.text or "").strip() if updated_el is not None else ""
    summary_el = (
        entry.find("atom:summary", ATOM_NS)
        or entry.find("summary")
        or entry.find("content")
    )
    excerpt = ""
    if summary_el is not None and summary_el.text:
        excerpt = summary_el.text.strip()
    elif summary_el is not None and len(summary_el):
        excerpt = "".join(summary_el.itertext()).strip()
    return {"title": title, "link": link, "date_raw": date_raw, "raw_excerpt": excerpt}


def _normalize_date(date_raw: str) -> str:
    """Return YYYY-MM-DD. Tolerates ISO, RSS, and common formats."""
    if not date_raw:
        return datetime.datetime.now().strftime("%Y-%m-%d")
    date_raw = date_raw.strip()
    if "T" in date_raw:
        try:
            return date_raw.split("T")[0][:10]
        except IndexError:
            pass
    if re.match(r"^\d{4}-\d{2}-\d{2}", date_raw):
        return date_raw[:10]
    for fmt in (
        "%a, %d %b %Y %H:%M:%S %z",
        "%a, %d %b %Y %H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
        "%m/%d/%Y",
    ):
        try:
            cleaned = date_raw.replace("Z", "+00:00").rstrip("Z")[:25].strip()
            dt = datetime.datetime.strptime(cleaned, fmt.replace(" %z", "").strip())
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue
    return datetime.datetime.now().strftime("%Y-%m-%d")


def parse_feed(url: str, source_name: str, timeout: int = 12) -> list[dict[str, Any]]:
    """Fetch a feed URL and return a list of parsed items."""
    raw = _fetch_url(url, timeout=timeout)
    root = ET.fromstring(raw)
    items: list[dict[str, Any]] = []

    # RSS 2.0
    channel = root.find("channel")
    if channel is not None:
        for item in channel.findall("item"):
            parsed = _parse_rss_item(item)
            if parsed:
                parsed["date"] = _normalize_date(parsed["date_raw"])
                parsed["source"] = source_name
                items.append(parsed)
        return items

    # Atom
    if root.tag == "{http://www.w3.org/2005/Atom}feed" or root.tag == "feed":
        entries = root.findall("atom:entry", ATOM_NS) or root.findall("entry")
        for entry in entries:
            parsed = _parse_atom_entry(entry)
            if parsed:
                parsed["date"] = _normalize_date(parsed["date_raw"])
                parsed["source"] = source_name
                items.append(parsed)
    return items


# ---------------------------------------------------------------------------
# Deduplication
# ---------------------------------------------------------------------------

def existing_source_urls(posts_dir: Path) -> set[str]:
    """Collect all source_url values already present in _posts/."""
    urls: set[str] = set()
    for path in posts_dir.glob("*.md"):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
            for m in re.finditer(r"source_url:\s*(\S+)", text):
                url = m.group(1).strip().rstrip("/")
                if url.startswith("http"):
                    urls.add(url)
        except Exception:
            continue
    return urls


def existing_slugs(posts_dir: Path) -> set[str]:
    """Collect all post slugs (date-slug) already in _posts/."""
    slugs: set[str] = set()
    for path in posts_dir.glob("*.md"):
        slugs.add(path.stem.lower())
    return slugs


# ---------------------------------------------------------------------------
# Relevance scoring
# ---------------------------------------------------------------------------

def score_relevance(title: str, excerpt: str) -> int:
    """Score an article's legal/local relevance based on keyword matches."""
    haystack = f"{title} {excerpt}".lower()
    score = 0
    for kw in LEGAL_KEYWORDS:
        if re.search(r"\b" + re.escape(kw.lower()) + r"\b", haystack):
            score += 1
    return score


# ---------------------------------------------------------------------------
# Feed configuration
# ---------------------------------------------------------------------------

def load_feeds_config() -> list[dict[str, Any]]:
    """Load enabled feeds from _data/rss-feeds.yml."""
    if not RSS_FEEDS_YML.exists():
        logger.error(f"RSS feeds config not found: {RSS_FEEDS_YML}")
        return []
    if yaml is None:
        logger.error("PyYAML not installed — cannot parse rss-feeds.yml")
        return []
    data = yaml.safe_load(RSS_FEEDS_YML.read_text(encoding="utf-8"))
    feeds = [f for f in (data.get("feeds") or []) if f.get("enabled") is True]
    logger.info(f"Loaded {len(feeds)} enabled RSS feeds")
    return feeds


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def crawl_and_publish() -> int:
    """Main crawl loop. Returns count of new posts created."""
    feeds = load_feeds_config()
    if not feeds:
        return 0

    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    known_urls = existing_source_urls(POSTS_DIR)
    known_slugs = existing_slugs(POSTS_DIR)
    new_count = 0

    for feed_cfg in feeds:
        name = feed_cfg.get("name", "Unknown")
        url = feed_cfg.get("url", "")
        max_items = int(feed_cfg.get("max_items") or 10)
        if not url:
            continue

        logger.info(f"━━━ Fetching: {name}")
        try:
            items = parse_feed(url, name)
        except Exception as e:
            logger.error(f"  ✗ Failed to fetch {name}: {e}")
            continue

        logger.info(f"  Found {len(items)} entries")

        for item in items[:max_items]:
            link = (item.get("link") or "").rstrip("/")

            # --- Dedup by URL ---
            if link in known_urls:
                continue

            # --- Dedup by slug ---
            slug = slug_from_title(item["title"])
            date = item.get("date") or datetime.datetime.now().strftime("%Y-%m-%d")
            full_slug = f"{date}-{slug}".lower()
            if full_slug in known_slugs:
                known_urls.add(link)
                continue

            # --- Relevance filter ---
            raw_text = strip_html(item.get("raw_excerpt", ""))
            relevance = score_relevance(item["title"], raw_text)
            if relevance == 0:
                logger.info(f"  ⊘ Skipped (no legal relevance): {item['title'][:60]}")
                continue

            # --- LLM article generation ---
            logger.info(f"  ✦ Generating article (score={relevance}): {item['title'][:60]}")
            body = generate_article_body(
                title=item["title"],
                raw_excerpt=item.get("raw_excerpt", ""),
                source_name=name,
                source_url=link,
                date=date,
            )
            excerpt_clean = generate_excerpt(body)

            # --- Build item for write_post ---
            post_item = {
                "title": item["title"],
                "link": link,
                "date": date,
                "source": name,
                "body": body,
                "excerpt": item.get("raw_excerpt", ""),
                "excerpt_clean": excerpt_clean,
            }

            post_path = write_new_post(POSTS_DIR, post_item)
            logger.info(f"  ✓ Created: {post_path.name}")
            known_urls.add(link)
            known_slugs.add(full_slug)
            new_count += 1

            # Small delay between LLM calls to avoid overwhelming Ollama
            time.sleep(1)

    return new_count


def main() -> int:
    logger.info("=" * 60)
    logger.info("Texas News Crawler — LLM-Enhanced Edition")
    logger.info("=" * 60)

    new_count = crawl_and_publish()

    logger.info("")
    logger.info(f"Pipeline complete: {new_count} new posts created")
    logger.info("Run 'python scripts/scan_articles.py' to update JSON feeds")
    logger.info("Run 'bundle exec jekyll build' to rebuild the site")
    return 0


if __name__ == "__main__":
    sys.exit(main())
