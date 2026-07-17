# scripts/write_post.py
"""Utility to write a Jekyll post for a news article.
Keeps `original_source_url` for provenance but UI will link to the post's own URL.

Accepts an optional 'body' key in the item dict for LLM-generated content.
Falls back to raw excerpt if no body is provided.
"""
from pathlib import Path
import re


def slug_from_title(title: str, max_len: int = 45) -> str:
    """Create a URL-friendly slug from a title."""
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug[:max_len] if len(slug) > max_len else slug


def _yaml_escape(value: str) -> str:
    """Escape a string for safe YAML frontmatter embedding."""
    # Replace internal double quotes with escaped quotes
    escaped = value.replace('"', '\\"')
    # Replace newlines
    escaped = escaped.replace("\n", " ")
    return escaped


def write_new_post(posts_dir: Path, item: dict) -> Path:
    """Create a markdown post from a feed item.

    Expected keys in *item*:
        title, link, date (YYYY-MM-DD), source
    Optional keys:
        body  — full post body (from LLM); if missing, uses excerpt
        excerpt — raw RSS excerpt (fallback)
    """
    slug = slug_from_title(item["title"])
    post_path = posts_dir / f"{item['date']}-{slug}.md"
    if post_path.exists():
        return post_path

    # Body: prefer LLM-generated body, fall back to excerpt
    body = item.get("body", "") or item.get("excerpt", "")

    # Excerpt for frontmatter: first 250 chars of body, cleaned
    raw_excerpt = item.get("excerpt_clean", "") or body
    excerpt_text = _yaml_escape(raw_excerpt[:250])

    # Generate permalink
    year, month, day = item["date"].split("-")
    permalink = f"/{year}/{month}/{day}/{slug}.html"

    # Escape title for YAML
    safe_title = _yaml_escape(item["title"])

    front = f"""---
category: news
date: {item['date']}
excerpt: "{excerpt_text}..."
layout: default
news_excerpt: true
source_name: {item['source']}
source_url: {item['link']}
original_source_url: {item['link']}
permalink: {permalink}
title: "{safe_title}"
verified_at: {item['date']}
---
"""
    post_path.write_text(front + "\n" + body, encoding="utf-8")
    return post_path
