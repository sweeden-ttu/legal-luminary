require 'selenium-webdriver'
require 'csv'
require 'fileutils'
require 'date'

BASE_URL = 'https://justice.bellcounty.texas.gov/PublicPortal/Home/Dashboard/26'
OUTPUT_DIR = 'scraped_data'
FileUtils.mkdir_p(OUTPUT_DIR)

JUDGE = ARGV[0] or (raise "Usage: ruby run_judge.rb <Judge Name>")
RESUME_FROM = ARGV[1] # optional: resume from this date (MM/DD/YYYY)

options = Selenium::WebDriver::Chrome::Options.new
options.add_argument('--headless=new')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--window-size=1400,900')
options.add_argument('--disable-gpu')

driver = Selenium::WebDriver.for(:chrome, options: options)
wait = Selenium::WebDriver::Wait.new(timeout: 30)

last_name = JUDGE.split(',').first.strip.downcase.gsub(/[^a-z]/, '_')
csv_path = File.join(OUTPUT_DIR, "#{last_name}_06_26.csv")

today = Date.new(2026, 6, 14)

# Generate month ranges newest to oldest
ranges = []
current = Date.new(today.year, today.month, 13)
if current > today
  current = current << 1
end
36.times do
  to_date = current
  from_date = current << 1
  ranges << [from_date, to_date]
  current = from_date
end
ranges.sort_by! { |r| r[1] }.reverse!

already_have = {}
if File.exist?(csv_path)
  puts "Existing file found: #{csv_path}"
  CSV.foreach(csv_path, headers: true) do |row|
    already_have[row['_DateRange']] = true
  end
  puts "  Already have #{already_have.keys.length} date ranges"
end

all_rows = []
unless already_have.empty?
  CSV.foreach(csv_path, headers: true) do |row|
    all_rows << row.to_h
  end
end

headers_done = already_have.any?

puts "=" * 80
puts "SCRAPING: #{JUDGE}"
puts "Output: #{csv_path}"
puts "Date ranges: #{ranges.length} total, #{ranges.length - already_have.length} remaining"
puts "=" * 80

begin
  total = all_rows.length

  ranges.each_with_index do |(from_date, to_date), idx|
    from_str = from_date.strftime('%m/%d/%Y')
    to_str = to_date.strftime('%m/%d/%Y')
    range_key = "#{from_str} - #{to_str}"
    pct = ((idx + 1).to_f / ranges.length * 100).round(1)

    if already_have[range_key]
      puts "  [#{pct}%] #{range_key}: SKIP (already done)"
      next
    end

    begin
      driver.get(BASE_URL)
      sleep 2

      search_select = wait.until { driver.find_element(id: 'cboHSSearchBy') }
      s = Selenium::WebDriver::Support::Select.new(search_select)
      s.select_by(:text, 'Judicial Officer')
      sleep 1

      judge_select = wait.until { driver.find_element(id: 'selHSJudicialOfficer') }
      j = Selenium::WebDriver::Support::Select.new(judge_select)
      j.select_by(:text, JUDGE)
      sleep 1

      driver.execute_script(
        "var f = document.getElementById('SearchCriteria_DateFrom');
         var t = document.getElementById('SearchCriteria_DateTo');
         if (f) { f.value = '#{from_str}'; $(f).trigger('change'); }
         if (t) { t.value = '#{to_str}'; $(t).trigger('change'); }"
      )
      sleep 1

      driver.find_element(id: 'btnHSSubmit').click
      wait.until { driver.find_element(css: 'span.k-pager-info') }
      sleep 3

      result = driver.execute_script(<<~JS)
        var grid = $('#hearingResultsGrid').data('kendoGrid');
        if (!grid) return { rows: [], count: 0 };
        var ds = grid.dataSource;
        ds.pageSize(99999);
        var items = ds.data();
        if (items.toJSON) items = items.toJSON();
        var rows = [];
        for (var i = 0; i < items.length; i++) {
          var row = {};
          for (var key in items[i]) {
            if (!items[i].hasOwnProperty(key)) continue;
            var v = items[i][key];
            if (v === null || v === undefined) { row[key] = ''; }
            else if (typeof v === 'object') {
              if (v.Description !== undefined) { row[key] = v.Description || ''; }
              else { try { row[key] = JSON.stringify(v); } catch(e) { row[key] = String(v); } }
            } else { row[key] = String(v); }
          }
          rows.push(row);
        }
        return { rows: rows, count: rows.length };
      JS

      count = result['count'] || 0
      if count > 0
        result['rows'].each do |row|
          row['_Judge'] = JUDGE
          row['_DateRange'] = range_key
          row['_SearchMonth'] = to_date.strftime('%Y-%m')
          all_rows << row
        end
        total += count
      end

      puts "  [#{pct}%] #{range_key}: #{count} records (total: #{total})"

      all_headers = all_rows.first&.keys || []
      CSV.open(csv_path, 'w') do |csv|
        csv << all_headers
        all_rows.each { |r| csv << all_headers.map { |h| r[h] || '' } }
      end

    rescue => e
      puts "  [#{pct}%] #{range_key}: ERROR - #{e.message}"
      sleep 3
      next
    end

    sleep 0.5
  end

  puts "\nDONE: #{csv_path}"
  puts "Total records: #{all_rows.length}"
  puts "File size: #{File.size(csv_path)} bytes"

rescue => e
  puts "FATAL: #{e.message}"
  puts e.backtrace.first(10).join("\n")
ensure
  driver.quit if driver
end
