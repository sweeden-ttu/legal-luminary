# Legal News Feed System

This system automatically fetches RSS feeds from Bell County Texas and Texas state sources, and displays them on the website.

## How It Works

1. **GitHub Actions Workflow** (`.github/workflows/fetch-news-feeds.yml`)
   - Runs daily at 6:00 AM UTC (1:00 AM CT)
   - Can be manually triggered from the Actions tab
   - Fetches RSS feeds using the script

2. **RSS Fetch Script** (`scripts/fetch-rss-feeds.rb`)
   - Reads feed configuration from `_data/rss-feeds.yml`
   - Fetches and parses each RSS feed
   - Generates `_data/news-feed.json` with aggregated news items

3. **Jekyll Integration**
   - Sidebar widget (`_includes/sidebar-news-feed.html`) shows 5 most recent items
   - Legal news page (`_pages/legal-news.md`) shows all items grouped by source

## Configuration

Edit `_data/rss-feeds.yml` to:
- Add new RSS feed sources
- Enable/disable feeds
- Adjust max items per feed
- Configure timeouts and retries

## RSS Feed Sources

### Currently Configured

**Local Bell County:**
- City of Killeen RSS feed
- Killeen Daily Herald

**Texas State:**
- Texas Legislature - Today's Bills Filed
- Texas Legislature - Today's Passed Bills
- Texas Legislature - Upcoming House Committee Meetings
- Texas Legislature - Upcoming Senate Committee Meetings

## Adding New Feeds

1. Find the RSS feed URL
2. Add to `_data/rss-feeds.yml`:
```yaml
- name: "Feed Name"
  url: "https://legalluminary.com/feed.xml"
  category: "local"  # or "state"
  type: "news"  # or "government", "legislature"
  max_items: 10
  enabled: true
```

3. The next scheduled run will include the new feed

## Testing

Test RSS feeds locally:
```bash
bundle install
bundle exec ruby scripts/test-rss-feeds.rb
```

Run the full fetch script:
```bash
bundle exec ruby scripts/fetch-rss-feeds.rb
```

## Troubleshooting

**No news items showing:**
- Check if `_data/news-feed.json` exists and has content
- Verify RSS feed URLs are accessible
- Check GitHub Actions logs for errors

**Feed not updating:**
- Verify the GitHub Actions workflow is running
- Check workflow logs for errors
- Ensure feed URLs are still valid

**Invalid feed errors:**
- Some feeds may require specific headers or authentication
- Check feed URL directly in browser
- Verify feed returns valid RSS/XML format

## Manual Updates

To manually trigger a feed update:
1. Go to GitHub Actions tab
2. Select "Fetch Legal News Feeds" workflow
3. Click "Run workflow"

## File Structure

```
_data/
  rss-feeds.yml          # Feed configuration
  news-feed.json         # Generated feed data (auto-generated)

_includes/
  sidebar-news-feed.html # Sidebar widget

_pages/
  legal-news.md          # Full news page

scripts/
  fetch-rss-feeds.rb     # Main fetch script
  test-rss-feeds.rb      # Test script

.github/workflows/
  fetch-news-feeds.yml   # GitHub Actions workflow
```
