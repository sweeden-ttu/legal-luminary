#!/usr/bin/env ruby
# frozen_string_literal: true

# Quick test script to validate RSS feed URLs
require 'faraday'
require 'feedjira'

test_feeds = [
  {
    name: "Texas Legislature - Today's Bills Filed",
    url: "https://capitol.texas.gov/MyTLO/RSS/RSSFeeds.aspx?FeedType=TodayBillsFiledHouse"
  },
  {
    name: "Texas Legislature - Today's Passed Bills",
    url: "https://capitol.texas.gov/MyTLO/RSS/RSSFeeds.aspx?FeedType=TodayPassedBills"
  },
  {
    name: "City of Killeen RSS",
    url: "https://www.killeentexas.gov/rss.aspx"
  }
]

puts "Testing RSS Feeds..."
puts "=" * 60

test_feeds.each do |feed|
  puts "\nTesting: #{feed[:name]}"
  puts "URL: #{feed[:url]}"
  
  begin
    response = Faraday.get(feed[:url]) do |req|
      req.options.timeout = 10
      req.headers['User-Agent'] = 'Legal Luminary RSS Tester/1.0'
    end
    
    if response.success?
      puts "✓ HTTP Status: #{response.status}"
      
      begin
        parsed = Feedjira.parse(response.body)
        puts "✓ Feed Title: #{parsed.title || 'N/A'}"
        puts "✓ Feed Items: #{parsed.entries.size}"
        puts "✓ Format: Valid RSS/Atom"
        
        if parsed.entries.any?
          sample = parsed.entries.first
          puts "  Sample item: #{sample.title || 'No title'}"
        end
      rescue => e
        puts "✗ Parse Error: #{e.message}"
      end
    else
      puts "✗ HTTP Error: #{response.status}"
    end
  rescue Faraday::TimeoutError
    puts "✗ Timeout: Feed did not respond in time"
  rescue => e
    puts "✗ Error: #{e.message}"
  end
end

puts "\n" + "=" * 60
puts "Test complete"
