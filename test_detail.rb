require 'selenium-webdriver'
require 'csv'

BASE_URL = 'https://justice.bellcounty.texas.gov/PublicPortal/Home/Dashboard/26'

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

  driver.execute_script(
    "var f = document.getElementById('SearchCriteria_DateFrom');
     var t = document.getElementById('SearchCriteria_DateTo');
     if (f) { f.value = '01/01/2026'; $(f).trigger('change'); }
     if (t) { t.value = '06/14/2026'; $(t).trigger('change'); }
     return 'OK';"
  )
  sleep 1

  driver.find_element(id: 'btnHSSubmit').click
  wait.until { driver.find_element(css: 'span.k-pager-info') }
  sleep 3

  # Extract ALL data fields from first 5 rows to see available fields
  all_fields = driver.execute_script(<<~JS)
    var grid = $('#hearingResultsGrid').data('kendoGrid');
    if (!grid) return [];
    var ds = grid.dataSource;
    ds.pageSize(99999);
    var items = ds.data();
    if (items.toJSON) items = items.toJSON();
    
    var samples = [];
    for (var i = 0; i < Math.min(5, items.length); i++) {
      var row = {};
      for (var key in items[i]) {
        if (items[i].hasOwnProperty(key)) {
          var v = items[i][key];
          if (v && typeof v === 'object' && v.Description !== undefined) {
            row[key] = '[Obj] ' + (v.Description || '') + ' / Word=' + (v.Word || '');
          } else if (v && typeof v === 'object') {
            row[key] = '[Obj] ' + JSON.stringify(v).substring(0, 100);
          } else {
            row[key] = String(v);
          }
        }
      }
      samples.push(row);
    }
    return samples;
  JS

  puts "ALL available fields from first 5 rows:\n\n"
  all_keys = all_fields.flat_map(&:keys).uniq
  puts "Fields: #{all_keys.join(', ')}\n\n"

  all_fields.each_with_index do |row, i|
    puts "--- Row #{i + 1} (Case: #{row['CaseNumber']}) ---"
    row.each { |k, v| puts "  #{k}: #{v}" }
    puts
  end

  # Now try to navigate to a case detail page
  case_url = all_fields[0]['CaseLoadUrl']
  puts "Navigating to case detail: #{case_url}"
  driver.get(case_url)
  sleep 5

  puts "\nPage title: #{driver.title}"
  
  # Get page source snippets to find judgment info
  page_text = driver.find_element(tag_name: 'body').text
  puts "\nPage text (first 2000 chars):"
  puts page_text[0..2000]

  # Check for common judgment-related terms
  ['judgment', 'judgement', 'docket', 'disposition', 'attorney', 'attorney', 'amount', 'award'].each do |term|
    if page_text.downcase.include?(term)
      # Find context
      idx = page_text.downcase.index(term)
      start = [0, idx - 40].max
      finish = [page_text.length - 1, idx + 80].min
      puts "\nFound '#{term}': ...#{page_text[start..finish]}..."
    end
  end

rescue => e
  puts "ERROR: #{e.message}"
  puts e.backtrace.first(10).join("\n")
ensure
  driver.quit if driver
end
