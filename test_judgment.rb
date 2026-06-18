require 'selenium-webdriver'
require 'csv'

options = Selenium::WebDriver::Chrome::Options.new
options.add_argument('--headless=new')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--window-size=1400,900')

driver = Selenium::WebDriver.for(:chrome, options: options)
wait = Selenium::WebDriver::Wait.new(timeout: 30)

begin
  # Check a Portfolio Recovery case that likely has a judgment
  # Let's get one from the grid first
  driver.get('https://justice.bellcounty.texas.gov/PublicPortal/Home/Dashboard/26')
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
     if (f) { f.value = '05/01/2026'; $(f).trigger('change'); }
     if (t) { t.value = '06/14/2026'; $(t).trigger('change'); }
     return 'OK';"
  )
  sleep 1

  driver.find_element(id: 'btnHSSubmit').click
  wait.until { driver.find_element(css: 'span.k-pager-info') }
  sleep 3

  # Get a portfolio recovery case URL
  case_url = driver.execute_script(<<~JS)
    var grid = $('#hearingResultsGrid').data('kendoGrid');
    if (!grid) return null;
    var items = grid.dataSource.data();
    if (items.toJSON) items = items.toJSON();
    for (var i = 0; i < items.length; i++) {
      if (items[i].Style && items[i].Style.toLowerCase().indexOf('portfolio') >= 0) {
        return { url: items[i].CaseLoadUrl, style: items[i].Style, caseNumber: items[i].CaseNumber };
      }
    }
    return null;
  JS

  if case_url
    puts "Found Portfolio case: #{case_url['caseNumber']} - #{case_url['style']}"
    puts "URL: #{case_url['url']}"
    
    driver.get(case_url['url'])
    sleep 5

    body = driver.find_element(tag_name: 'body').text
    puts "\n=== Full page text ==="
    puts body

    # Check for tabs - the URL has tabIndex=3, let's try clicking other tabs
    puts "\n=== Looking for tabs/buttons ==="
    tabs = driver.find_elements(css: 'a[role="tab"], .k-tabstrip-item, .tab, button, .k-link')
    tabs.each do |tab|
      begin
        txt = tab.text.strip
        if !txt.empty? && txt.length < 50
          puts "Tab element: '#{txt}' (tag: #{tab.tag_name})"
        end
      rescue => e
        # stale element
      end
    end

    # Try to find judgment amount by looking for "$" or "damages" patterns
    if body =~ /\$[\d,]+\.\d{2}/
      puts "\nFound dollar amounts:"
      body.scan(/\$[\d,]+\.\d{2}/).each { |m| puts "  #{m}" }
    else
      puts "\nNo dollar amounts found in page text"
    end
  else
    puts "No Portfolio case found"
  end

rescue => e
  puts "ERROR: #{e.message}"
  puts e.backtrace.first(10).join("\n")
ensure
  driver.quit if driver
end
