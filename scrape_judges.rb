require 'selenium-webdriver'
require 'csv'
require 'fileutils'
require 'date'

BASE_URL = 'https://justice.bellcounty.texas.gov/PublicPortal/Home/Dashboard/26'
OUTPUT_DIR = 'scraped_data'

JUDGES = [
  'Johnson, Gregory D.',
  'Wilkey, Larry',
  'MOTZ, PAUL A.',
  'LePak, Paul L',
  'Faulkner, Wade'
]

FileUtils.mkdir_p(OUTPUT_DIR)

options = Selenium::WebDriver::Chrome::Options.new
options.add_argument('--headless=new')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--window-size=1400,900')

driver = Selenium::WebDriver.for(:chrome, options: options)
wait = Selenium::WebDriver::Wait.new(timeout: 30)

def set_date_range(driver, wait, date_from, date_to)
  driver.execute_script(
    "var f = document.getElementById('SearchCriteria_DateFrom');
     var t = document.getElementById('SearchCriteria_DateTo');
     if (f) { f.value = '#{date_from}'; $(f).trigger('change'); }
     if (t) { t.value = '#{date_to}'; $(t).trigger('change'); }
     return 'Dates set: #{date_from} - #{date_to}';"
  )
end

def extract_grid_data(driver)
  driver.execute_script(<<~JS)
    var grid = $('#hearingResultsGrid').data('kendoGrid');
    if (!grid) return { columns: [], rows: [], error: 'NO_GRID' };
    var ds = grid.dataSource;
    ds.pageSize(99999);
    var items = ds.data();
    if (items.toJSON) items = items.toJSON();
    var cols = grid.columns.map(function(c) { return c.field || c.title || ''; });
    var rows = [];
    for (var i = 0; i < items.length; i++) {
      var row = {};
      for (var j = 0; j < cols.length; j++) {
        if (cols[j]) {
          row[cols[j]] = items[i][cols[j]] || '';
        }
      }
      rows.push(row);
    }
    return { columns: cols, rows: rows, count: rows.length };
  JS
end

def month_ranges(end_date, months_back)
  ranges = []
  current = Date.new(end_date.year, end_date.month, 13)
  if current > end_date
    current = current << 1
  end

  months_back.times do
    to_date = current
    from_date = current << 1
    ranges << [from_date, to_date]
    current = from_date
  end
  ranges
end

today = Date.new(2026, 6, 14)
ranges = month_ranges(today, 36)

ranges = ranges.sort_by(&:last).reverse

puts "=" * 80
puts "Bell County Public Portal - Judicial Officer Record Scraper"
puts "Starting: #{Time.now.strftime('%Y-%m-%d %H:%M:%S')}"
puts "=" * 80

begin
  driver.get(BASE_URL)
  sleep 3

  JUDGES.each_with_index do |judge, judge_idx|
    last_name = judge.split(',').first.strip.downcase.gsub(/[^a-z]/, '_')
    csv_filename = File.join(OUTPUT_DIR, "#{last_name}_#{Time.now.strftime('%m_%y')}.csv")

    puts "\n#{'=' * 80}"
    puts "[#{judge_idx + 1}/#{JUDGES.length}] Processing: #{judge}"
    puts "Output: #{csv_filename}"
    puts "#{'=' * 80}"

    all_rows = []
    header_written = false
    columns = []

    ranges.each_with_index do |(from_date, to_date), idx|
      from_str = from_date.strftime('%m/%d/%Y')
      to_str = to_date.strftime('%m/%d/%Y')
      progress = ((idx + 1).to_f / ranges.length * 100).round(1)

      begin
        unless idx == 0 && judge_idx == 0
          driver.get(BASE_URL)
          sleep 2
        end

        search_select = wait.until { driver.find_element(id: 'cboHSSearchBy') }
        select = Selenium::WebDriver::Support::Select.new(search_select)
        select.select_by(:text, 'Judicial Officer')
        sleep 1

        judge_select = wait.until { driver.find_element(id: 'selHSJudicialOfficer') }
        jselect = Selenium::WebDriver::Support::Select.new(judge_select)
        jselect.select_by(:text, judge)
        sleep 1

        set_date_range(driver, wait, from_str, to_str)
        sleep 1

        submit_btn = driver.find_element(id: 'btnHSSubmit')
        submit_btn.click

        wait.until { driver.find_element(css: 'span.k-pager-info') }
        sleep 2

        result = extract_grid_data(driver)
        count = result['count'] || 0

        if count > 0
          if result['columns'] && !columns.any?
            columns = result['columns']
          end
          result['rows'].each do |row|
            all_rows << row.merge('_judge' => judge, '_date_range' => "#{from_str} - #{to_str}")
          end
        end

        puts "  [#{progress}%] #{from_str} - #{to_str}: #{count} records"

      rescue => e
        puts "  [#{progress}%] #{from_str} - #{to_str}: ERROR - #{e.message}"
        next
      end

      sleep 1
    end

    if all_rows.any?
      all_headers = ['_judge', '_date_range'] + columns
      CSV.open(csv_filename, 'w') do |csv|
        csv << all_headers
        all_rows.each do |row|
          csv << all_headers.map { |h| row[h] || '' }
        end
      end
      puts "  => Saved #{all_rows.length} total records to #{csv_filename}"
    else
      puts "  => No records found for #{judge}"
    end
  end

rescue => e
  puts "FATAL ERROR: #{e.message}"
  puts e.backtrace.first(10).join("\n")
ensure
  driver.quit if driver
end

puts "\n#{'=' * 80}"
puts "Scraping complete: #{Time.now.strftime('%Y-%m-%d %H:%M:%S')}"
puts "#{'=' * 80}"
