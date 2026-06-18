require 'selenium-webdriver'
require 'csv'
require 'fileutils'
require 'date'

BASE_URL = 'https://justice.bellcounty.texas.gov/PublicPortal/Home/Dashboard/26'
OUTPUT_DIR = 'scraped_data'

FileUtils.mkdir_p(OUTPUT_DIR)

options = Selenium::WebDriver::Chrome::Options.new
options.add_argument('--headless=new')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--window-size=1400,900')

driver = Selenium::WebDriver.for(:chrome, options: options)
wait = Selenium::WebDriver::Wait.new(timeout: 30)

begin
  driver.get(BASE_URL)
  sleep 3

  search_select = wait.until { driver.find_element(id: 'cboHSSearchBy') }
  select = Selenium::WebDriver::Support::Select.new(search_select)
  select.select_by(:text, 'Judicial Officer')
  sleep 1

  judge_select = wait.until { driver.find_element(id: 'selHSJudicialOfficer') }
  jselect = Selenium::WebDriver::Support::Select.new(judge_select)
  jselect.select_by(:text, 'Johnson, Gregory D.')
  sleep 1

  from_str = '05/13/2026'
  to_str = '06/13/2026'
  driver.execute_script(
    "var f = document.getElementById('SearchCriteria_DateFrom');
     var t = document.getElementById('SearchCriteria_DateTo');
     if (f) { f.value = '#{from_str}'; $(f).trigger('change'); }
     if (t) { t.value = '#{to_str}'; $(t).trigger('change'); }
     return 'Dates set: #{from_str} - #{to_str}';"
  )
  sleep 1

  driver.find_element(id: 'btnHSSubmit').click
  sleep 3

  pager = wait.until { driver.find_element(css: 'span.k-pager-info') }
  puts "Pager text: #{pager.text}"

  sleep 2

  grid_info = driver.execute_script(<<~JS)
    var grid = $('#hearingResultsGrid').data('kendoGrid');
    if (!grid) return { error: 'NO_GRID' };
    var cols = grid.columns.map(function(c) {
      return { field: c.field, title: c.title };
    });
    var ds = grid.dataSource;
    ds.pageSize(99999);
    var items = ds.data();
    if (items.toJSON) items = items.toJSON();
    return {
      columns: cols,
      total: items.length,
      firstRow: items[0]
    };
  JS

  puts "\nGrid columns:"
  grid_info['columns'].each { |c| puts "  - #{c['title']} (field: #{c['field']})" }
  puts "\nTotal rows available: #{grid_info['total']}"
  puts "\nFirst row sample:"
  grid_info['firstRow'].each { |k, v| puts "  #{k}: #{v}" }

  # Now try the CSV download approach
  puts "\n--- Testing CSV extraction ---"
  csv_data = driver.execute_script(<<~JS)
    var grid = $('#hearingResultsGrid').data('kendoGrid');
    if (!grid) return 'NO_GRID';
    var ds = grid.dataSource;
    ds.pageSize(99999);
    var items = ds.data();
    if (items.toJSON) items = items.toJSON();
    var cols = grid.columns;
    var csv = '';
    for (var j = 0; j < cols.length; j++) {
      csv += (cols[j].title || cols[j].field || 'Col'+j);
      if (j < cols.length-1) csv += ',';
    }
    for (var i = 0; i < items.length; i++) {
      csv += '\\n';
      for (var j = 0; j < cols.length; j++) {
        var v = items[i][cols[j].field];
        if (v === null || v === undefined) v = '';
        v = String(v).replace(/"/g, '""');
        if (v.includes(',') || v.includes('"') || v.includes('\\n')) v = '"'+v+'"';
        csv += v;
        if (j < cols.length-1) csv += ',';
      }
    }
    return csv;
  JS

  # Save to file
  csv_path = File.join(OUTPUT_DIR, "johnson_06_26.csv")
  File.write(csv_path, csv_data)
  puts "\nCSV written to: #{csv_path}"
  puts "File size: #{File.size(csv_path)} bytes"
  puts "First 5 lines:"
  File.readlines(csv_path).first(5).each { |l| puts "  #{l.chomp}" }

rescue => e
  puts "ERROR: #{e.message}"
  puts e.backtrace.first(10).join("\n")
ensure
  driver.quit if driver
end
