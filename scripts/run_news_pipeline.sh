#!/usr/bin/env bash
# scripts/run_news_pipeline.sh
# Full news pipeline: crawl RSS → generate LLM articles → update JSON feeds → rebuild site
#
# Usage:
#   bash scripts/run_news_pipeline.sh
#   bash scripts/run_news_pipeline.sh --skip-build   # crawl + scan only

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo "════════════════════════════════════════════════════════════"
echo "  Legal Luminary — News Pipeline"
echo "  $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "════════════════════════════════════════════════════════════"

# Step 1: Crawl RSS feeds and generate LLM-enriched posts
echo ""
echo "▶ Step 1/3: Crawling RSS feeds + LLM article generation..."
echo ""
python3 scripts/texas_news_crawler.py

# Step 2: Scan posts and update _data/articles/*.json feeds
echo ""
echo "▶ Step 2/3: Updating article JSON feeds..."
echo ""
python3 scripts/scan_articles.py

# Step 3: Rebuild the site (unless --skip-build)
if [[ "${1:-}" != "--skip-build" ]]; then
    echo ""
    echo "▶ Step 3/3: Rebuilding Jekyll site..."
    echo ""
    bundle exec jekyll build 2>&1 | tail -5
    echo ""
    echo "✓ Site rebuilt successfully in _site/"
else
    echo ""
    echo "⊘ Skipping Jekyll build (--skip-build)"
fi

echo ""
echo "════════════════════════════════════════════════════════════"
echo "  Pipeline complete!"
echo "════════════════════════════════════════════════════════════"
