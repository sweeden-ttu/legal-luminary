#!/usr/bin/env python3
"""
scripts/migrate_old_posts.py
Migrates old-format _posts/ files to the new standard frontmatter schema.

Old format problems:
  - layout: post           → must be: layout: default
  - categories: news       → must be: category: news
  - No permalink field     → generates /YYYY/MM/DD/slug.html
  - source_name in quotes  → must be: source_name (unquoted, flat)
  - No verified_at         → copies from date
  - source_url may be missing

Run: python3 scripts/migrate_old_posts.py [--dry-run]
"""

from __future__ import annotations

import re
import sys
import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
POSTS_DIR = SCRIPT_DIR.parent / "_posts"

DRY_RUN = "--dry-run" in sys.argv


def slug_from_title(title: str, max_len: int = 45) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug[:max_len] if len(slug) > max_len else slug


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Split a post into {key: raw_value} dict and body string."""
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    fm_raw = parts[1].strip()
    body = parts[2].strip()
    meta: dict = {}
    current_key = None
    current_val_lines: list[str] = []

    for line in fm_raw.splitlines():
        m = re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*):\s*(.*)', line)
        if m:
            # Save previous
            if current_key:
                meta[current_key] = " ".join(current_val_lines).strip()
            current_key = m.group(1)
            current_val_lines = [m.group(2)]
        elif current_key and (line.startswith("  ") or line.startswith("\t")):
            # Multi-line YAML continuation
            current_val_lines.append(line.strip())
        # else: ignore blank lines within FM

    if current_key:
        meta[current_key] = " ".join(current_val_lines).strip()

    return meta, body


def needs_migration(meta: dict) -> bool:
    """Return True if this post is in the old format."""
    return (
        meta.get("layout") == "post"
        or "categories" in meta
        or "permalink" not in meta
    )


def yaml_val(v: str) -> str:
    """Unwrap YAML string value (remove surrounding quotes)."""
    v = v.strip()
    if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
        v = v[1:-1]
    return v


def make_permalink(date_str: str, filename_stem: str) -> str:
    """Generate /YYYY/MM/DD/slug.html from the post's date and filename."""
    # Extract date part from filename: YYYY-MM-DD-slug...
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})-(.+)", filename_stem)
    if m:
        y, mo, d, slug = m.group(1), m.group(2), m.group(3), m.group(4)
    else:
        # Fall back to parsing from date field
        try:
            dt = datetime.datetime.strptime(date_str[:10], "%Y-%m-%d")
            y, mo, d = dt.strftime("%Y"), dt.strftime("%m"), dt.strftime("%d")
            slug = slug_from_title(filename_stem)
        except Exception:
            return ""
    return f"/{y}/{mo}/{d}/{slug[:45]}.html"


def migrate_post(path: Path, dry_run: bool = False) -> bool:
    """Migrate a single post file. Returns True if changed."""
    text = path.read_text(encoding="utf-8", errors="replace")
    meta, body = parse_frontmatter(text)

    if not meta:
        return False
    if not needs_migration(meta):
        return False

    # --- Extract fields ---
    title = yaml_val(meta.get("title", ""))
    raw_date = yaml_val(meta.get("date", ""))
    date_str = raw_date[:10] if raw_date else datetime.date.today().isoformat()

    # Unify source fields: may be source_name or source
    source = (
        yaml_val(meta.get("source_name", ""))
        or yaml_val(meta.get("source", ""))
        or "Legal Luminary"
    )

    source_url = (
        yaml_val(meta.get("source_url", ""))
        or yaml_val(meta.get("link", ""))
        or ""
    )

    # --- Permalink ---
    permalink = make_permalink(date_str, path.stem)

    # --- Excerpt from body (first 250 non-empty chars) ---
    clean_body = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", body)  # strip links
    clean_body = re.sub(r"[*#\[\]`]", "", clean_body).strip()
    excerpt_text = re.sub(r"\s+", " ", clean_body[:250])
    excerpt_safe = excerpt_text.replace('"', '\\"')

    safe_title = title.replace('"', '\\"')
    safe_source = source.replace('"', '\\"')

    # --- Build new frontmatter ---
    new_front = f"""---
category: news
date: {date_str}
excerpt: "{excerpt_safe}..."
layout: default
news_excerpt: true
source_name: {safe_source}
source_url: {source_url}
original_source_url: {source_url}
permalink: {permalink}
title: "{safe_title}"
verified_at: {date_str}
---
"""

    # --- Clean body: remove old markdown link-to-source lines ---
    clean_body_final = re.sub(
        r"\[Read the full story[^\]]*\]\([^)]*\)\s*", "", body
    ).strip()

    # Add Source Information footer if missing
    if "## Source Information" not in clean_body_final and source_url:
        clean_body_final += (
            f"\n\n## Source Information\n\n"
            f"- **Source**: {source}\n"
            f"- **Original URL**: {source_url}\n"
            f"- **Published**: {date_str}\n"
            f"- **Verified**: {date_str}\n\n"
            f"---"
        )

    new_content = new_front + "\n" + clean_body_final + "\n"

    if dry_run:
        print(f"  [DRY RUN] Would migrate: {path.name}")
        return True

    path.write_text(new_content, encoding="utf-8")
    print(f"  ✓ Migrated: {path.name}")
    return True


def main():
    posts = list(POSTS_DIR.glob("*.md"))
    print(f"Scanning {len(posts)} posts in {POSTS_DIR}")
    if DRY_RUN:
        print("  (dry-run mode — no files will be changed)\n")

    migrated = 0
    for post in sorted(posts):
        try:
            if migrate_post(post, dry_run=DRY_RUN):
                migrated += 1
        except Exception as e:
            print(f"  ✗ Error migrating {post.name}: {e}")

    print(f"\nDone. {migrated} posts {'would be' if DRY_RUN else ''} migrated.")


if __name__ == "__main__":
    main()
