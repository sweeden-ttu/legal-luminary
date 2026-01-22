#!/usr/bin/env ruby
# frozen_string_literal: true

# RSS Feed Fetcher for Legal News
# Fetches RSS feeds from configured sources and generates JSON for Jekyll

require 'yaml'
require 'json'
require 'feedjira'
require 'faraday'
require 'time'
require 'logger'

# ---
# Content filtering
# ---
# Goal: keep only items that are legal / crime / justice / law enforcement / court related.
# We do this at fetch-time so the generated _data/news-feed.json is already curated.

LEGAL_KEYWORDS = [
  # courts / process
  'court', 'courts', 'judge', 'judges', 'jury', 'trial', 'hearing', 'sentencing',
  'appeal', 'appeals', 'lawsuit', 'lawsuits', 'litigation', 'indict', 'indicted',
  'indictment', 'arraignment', 'plea', 'pleads', 'pleaded', 'convict', 'convicted',
  'conviction', 'acquitted', 'bail', 'bond', 'probation', 'parole', 'warrant',
  'warrants', 'subpoena', 'subpoenas',

  # crime
  'crime', 'criminal', 'murder', 'homicide', 'shooting', 'robbery', 'burglary',
  'theft', 'stolen', 'assault', 'battery', 'kidnapping', 'rape', 'sexual assault',
  'fraud', 'scam', 'arson', 'manslaughter', 'felony', 'misdemeanor',
  'dwi', 'dui',

  # law enforcement
  'police', 'sheriff',
  # "deputy" is too ambiguous (e.g., deputy superintendent).
  'constable', 'trooper',
  # "investigation" is too broad; many non-legal stories use it.
  'investigates', 'investigating',
  'arrest', 'arrests', 'arrested', 'charged',
  'charges', 'booking', 'booked', 'suspect', 'victim',

  # legal system / institutions
  'district attorney',
  # "da" by itself is too ambiguous (matches words like "update"), so we don't
  # include it as a standalone keyword.
  'prosecutor', 'prosecution', 'public defender',
  'attorney', 'lawyer', 'legal',
  # note: "justice" is too broad and causes false positives (social justice, etc.)
  # note: "immigration" is too broad; keep the more specific "ice" keyword
  'department of justice',
  # Keep immigration-enforcement stories but avoid false positives like "practice".
  # We match with word boundaries in looks_legal_related?
  'ice',

  # corrections
  'jail', 'prison', 'inmate', 'incarcerated'
].freeze

def looks_legal_related?(title, excerpt)
  haystack = [title, excerpt].compact.join(' ').downcase
  return false if haystack.strip.empty?

  # Extra guardrails to reduce false positives from generic words like "investigates".
  # These are intentionally conservative.
  return false if haystack.match?(/\bnaval drills?\b/)

  LEGAL_KEYWORDS.any? do |kw|
    if kw.match?(/\A[a-z0-9\s\-']+\z/)
      # word-boundary-ish match for short tokens; allow spaces for phrases.
      if kw.include?(' ')
        haystack.include?(kw)
      else
        !!haystack.match(/\b#{Regexp.escape(kw)}\b/)
      end
    else
      haystack.include?(kw)
    end
  end
end

# Set up logging
logger = Logger.new(STDERR)
logger.level = Logger::INFO

# Configuration
DATA_DIR = File.join(__dir__, '..', '_data')

# The site now keeps *city-specific* feed lists in _data/*.yml.
# This script aggregates them and generates a single _data/news-feed.json
# so Jekyll (and GitHub Pages) can render headlines without runtime fetching.
CITY_FEED_FILES = [
  File.join(DATA_DIR, 'bell-county-news.yml'),
  File.join(DATA_DIR, 'killeen-news.yml'),
  File.join(DATA_DIR, 'temple-news.yml'),
  File.join(DATA_DIR, 'copperas-cove-news.yml')
].freeze

OUTPUT_FILE = File.join(DATA_DIR, 'news-feed.json')

# Load and merge city feed configs
def load_config
  log = Logger.new(STDERR)
  log.level = Logger::INFO

  merged = {
    'feeds' => [],
    'config' => {}
  }

  CITY_FEED_FILES.each do |path|
    next unless File.exist?(path)

    city_cfg = YAML.load_file(path) || {}
    feeds = city_cfg['feeds'] || []
    # Add the city identifier so templates can filter later
    city_key = File.basename(path, '.yml')

    feeds.each do |f|
      next unless f.is_a?(Hash)
      f = f.dup
      f['city'] ||= city_key
      merged['feeds'] << f
    end

    # Merge config with last-one-wins. (They are currently identical anyway.)
    merged['config'] = merged['config'].merge(city_cfg['config'] || {})
  end

  if merged['feeds'].empty?
    log.error "No feed configuration files found / no feeds enabled. Expected one of: #{CITY_FEED_FILES.join(', ')}"
    exit 1
  end

  log.info "Loaded #{merged['feeds'].size} feeds from city configs"
  merged
end

# Fetch RSS feed with error handling
def fetch_feed(url, timeout: 10, retries: 2)
  log = Logger.new(STDERR)
  log.level = Logger::INFO
  
  retries.times do |attempt|
    begin
      log.info "Fetching feed: #{url} (attempt #{attempt + 1}/#{retries})"
      
      response = Faraday.get(url) do |req|
        req.options.timeout = timeout
        req.headers['User-Agent'] = 'Legal Luminary RSS Fetcher/1.0'
      end
      
      unless response.success?
        log.warn "HTTP error #{response.status} for #{url}"
        next
      end
      
      feed = Feedjira.parse(response.body)
      log.info "Successfully parsed feed: #{feed.title || 'Untitled'}"
      return feed
      
    rescue Faraday::TimeoutError => e
      log.warn "Timeout fetching #{url}: #{e.message}"
      next if attempt < retries - 1
      
    rescue Faraday::Error => e
      log.warn "Network error fetching #{url}: #{e.message}"
      next if attempt < retries - 1
      
    rescue Feedjira::NoParserAvailable => e
      log.error "No parser available for #{url}: #{e.message}"
      return nil
      
    rescue StandardError => e
      log.error "Error parsing feed #{url}: #{e.message}"
      log.error e.backtrace.first(3).join("\n")
      return nil
    end
  end
  
  nil
end

# Convert feed item to hash
def item_to_hash(item, source_name)
  {
    'title' => item.title || 'No title',
    'link' => item.url || item.link || '#',
    'date' => parse_date(item.published || item.updated),
    'excerpt' => extract_excerpt(item.summary || item.content || ''),
    'source' => source_name
  }
rescue StandardError => e
  log = Logger.new(STDERR)
  log.warn "Error converting item: #{e.message}"
  {
    'title' => 'Error parsing item',
    'link' => '#',
    'date' => Time.now.iso8601,
    'excerpt' => '',
    'source' => source_name
  }
end

# Parse date from various formats
def parse_date(date_string)
  return Time.now.iso8601 if date_string.nil? || date_string.empty?
  
  Time.parse(date_string.to_s).iso8601
rescue StandardError
  Time.now.iso8601
end

# Extract excerpt from content
def extract_excerpt(content, max_length: 200)
  return '' if content.nil? || content.empty?
  
  # Remove HTML tags
  text = content.gsub(/<[^>]+>/, ' ').gsub(/\s+/, ' ').strip
  
  if text.length > max_length
    text[0, max_length] + '...'
  else
    text
  end
end

# Filter items by date
def filter_by_date(items, max_age_days: 30)
  cutoff_date = Time.now - (max_age_days * 24 * 60 * 60)
  
  items.select do |item|
    begin
      item_date = Time.parse(item['date'])
      item_date >= cutoff_date
    rescue StandardError
      false
    end
  end
end

# Main execution
def main
  log = Logger.new(STDERR)
  log.level = Logger::INFO
  log.info "Starting RSS feed fetch at #{Time.now}"
  
  config = load_config
  feeds_config = config['feeds'] || []
  global_config = config['config'] || {}
  
  max_age_days = global_config['max_age_days'] || 30
  timeout = global_config['timeout_seconds'] || 10
  retries = global_config['retry_attempts'] || 2
  delay = global_config['delay_between_feeds'] || 1
  
  all_items = []
  feed_results = []
  
  feeds_config.each do |feed_config|
    next unless feed_config['enabled']
    
    source_name = feed_config['name']
    url = feed_config['url']
    city = feed_config['city']
    max_items = feed_config['max_items'] || 10
    
    log.info "Processing feed: #{source_name}"
    
    feed = fetch_feed(url, timeout: timeout, retries: retries)
    
    if feed.nil?
      log.warn "Failed to fetch feed: #{source_name}"
      feed_results << {
        'source' => source_name,
        'url' => url,
        'items' => [],
        'error' => 'Failed to fetch or parse feed'
      }
      sleep delay
      next
    end
    
    # Convert feed items
    items = feed.entries.map { |entry| item_to_hash(entry, source_name) }
    # attach city to each item for city-page filtering
    items.each { |it| it['city'] = city if city }
    
    # Filter by date
    items = filter_by_date(items, max_age_days: max_age_days)

    # Filter by topic (legal / crime / justice / law enforcement / court)
    before_legal_filter = items.size
    items = items.select { |it| looks_legal_related?(it['title'], it['excerpt']) }
    log.info "Topic filter removed #{before_legal_filter - items.size} non-legal items from #{source_name}" if before_legal_filter != items.size
    
    # Limit items
    items = items.first(max_items)
    
    # Add to results
    feed_results << {
      'source' => source_name,
      'url' => url,
      'city' => city,
      'items' => items,
      'item_count' => items.size
    }
    
    # Add to all items
    all_items.concat(items)
    
    log.info "Fetched #{items.size} items from #{source_name}"
    
    # Delay between feeds to be respectful
    sleep delay
  end
  
  # Sort all items by date (newest first)
  all_items.sort_by! { |item| Time.parse(item['date']) }.reverse!
  
  # Generate output
  output = {
    'last_updated' => Time.now.iso8601,
    'feeds' => feed_results,
    'all_items' => all_items,
    'total_items' => all_items.size
  }
  
  # Write JSON file
  File.write(OUTPUT_FILE, JSON.pretty_generate(output))
  log.info "Wrote #{all_items.size} total items to #{OUTPUT_FILE}"
  
  # Summary
  successful_feeds = feed_results.count { |f| f['items'].any? }
  log.info "Summary: #{successful_feeds}/#{feed_results.size} feeds successful, #{all_items.size} total items"
  
  exit 0
rescue StandardError => e
  log.error "Fatal error: #{e.message}"
  log.error e.backtrace.join("\n")
  exit 1
end

# Run if executed directly
main if __FILE__ == $PROGRAM_NAME
