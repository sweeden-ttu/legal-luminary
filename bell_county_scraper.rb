require 'selenium-webdriver'
require 'csv'
require 'fileutils'
require 'date'
require 'json'

BASE_URL = 'https://justice.bellcounty.texas.gov/PublicPortal/Home/Dashboard/26'
OUTPUT_DIR = 'scraped_data'
DETAIL_DIR = 'case_details'

JUDGES = [
  'Johnson, Gregory D.',
  'Wilkey, Larry',
  'MOTZ, PAUL A.',
  'LePak, Paul L',
  'Faulkner, Wade'
]

FileUtils.mkdir_p(OUTPUT_DIR)
FileUtils.mkdir_p(DETAIL_DIR)

options = Selenium::WebDriver::Chrome::Options.new
options.add_argument('--headless=new')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--window-size=1400,900')
options.add_argument('--disable-gpu')
options.add_argument('--disable-web-security')

driver = Selenium::WebDriver.for(:chrome, options: options)
wait = Selenium::WebDriver::Wait.new(timeout: 30)

def set_date_range(driver, date_from, date_to)
  driver.execute_script(
    "var f = document.getElementById('SearchCriteria_DateFrom');
     var t = document.getElementById('SearchCriteria_DateTo');
     if (f) { f.value = '#{date_from}'; $(f).trigger('change'); }
     if (t) { t.value = '#{date_to}'; $(t).trigger('change'); }
     return true;"
  )
end

def extract_grid_data(driver)
  driver.execute_script(<<~JS)
    var grid = $('#hearingResultsGrid').data('kendoGrid');
    if (!grid) return { columns: [], rows: [], error: 'NO_GRID', count: 0 };

    var ds = grid.dataSource;
    ds.pageSize(99999);
    var items = ds.data();
    if (items.toJSON) items = items.toJSON();

    var cols = grid.columns;
    var colFields = cols.map(function(c) { return c.field || c.title || ''; });

    var rows = [];
    for (var i = 0; i < items.length; i++) {
      var row = {};
      for (var key in items[i]) {
        if (items[i].hasOwnProperty(key)) {
          var v = items[i][key];
          if (v === null || v === undefined) {
            row[key] = '';
          } else if (typeof v === 'object') {
            try {
              if (v.Description !== undefined) {
                row[key] = v.Description || '';
                row[key + '_Word'] = v.Word || '';
              } else if (v instanceof Date) {
                row[key] = v.toISOString();
              } else {
                row[key] = JSON.stringify(v);
              }
            } catch(e) {
              row[key] = String(v);
            }
          } else {
            row[key] = String(v);
          }
        }
      }
      rows.push(row);
    }
    return { columns: colFields, rows: rows, count: rows.length };
  JS
end

def generate_month_ranges(end_date, months_back)
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
  ranges.sort_by(&:last).reverse
end

def sanitize_filename(name)
  name.downcase.gsub(/[^a-z]/, '_').gsub(/_+/, '_').gsub(/^_|_$/, '')
end

today = Date.new(2026, 6, 14)
month_ranges = generate_month_ranges(today, 36)

puts "=" * 90
puts "BELL COUNTY PUBLIC PORTAL - JUDICIAL OFFICER SCRAPER"
puts "Date: #{today.strftime('%B %d, %Y')}  |  #{month_ranges.length} month ranges | #{JUDGES.length} judges"
puts "=" * 90

begin
  driver.get(BASE_URL)
  sleep 4

  hearings_csv_path = File.join(OUTPUT_DIR, 'all_hearings_master.csv')
  all_hearings = []
  all_headers = nil

  JUDGES.each_with_index do |judge, judge_idx|
    judge_key = sanitize_filename(judge.split(',').first.strip)
    judge_csv = File.join(OUTPUT_DIR, "#{judge_key}_#{today.strftime('%m_%y')}.csv")
    
    puts "\n#{'=' * 90}"
    puts "[#{judge_idx + 1}/#{JUDGES.length}] JUDGE: #{judge}"
    puts "Output: #{judge_csv}"
    puts "#{'=' * 90}"

    judge_rows = []
    judge_columns = nil
    total_for_judge = 0

    month_ranges.each_with_index do |(from_date, to_date), range_idx|
      from_str = from_date.strftime('%m/%d/%Y')
      to_str = to_date.strftime('%m/%d/%Y')
      pct = ((range_idx + 1).to_f / month_ranges.length * 100).round(1)

      begin
        driver.get(BASE_URL)
        sleep 2

        search_select = wait.until { driver.find_element(id: 'cboHSSearchBy') }
        s = Selenium::WebDriver::Support::Select.new(search_select)
        s.select_by(:text, 'Judicial Officer')
        sleep 1

        judge_select = wait.until { driver.find_element(id: 'selHSJudicialOfficer') }
        j = Selenium::WebDriver::Support::Select.new(judge_select)
        j.select_by(:text, judge)
        sleep 1

        set_date_range(driver, from_str, to_str)
        sleep 1

        driver.find_element(id: 'btnHSSubmit').click
        wait.until { driver.find_element(css: 'span.k-pager-info') }
        sleep 3

        result = extract_grid_data(driver)
        count = result['count'] || 0

        if count > 0 && result['rows'].any?
          judge_columns ||= result['rows'].first.keys
          result['rows'].each do |row|
            row['_Judge'] = judge
            row['_DateRange'] = "#{from_str} - #{to_str}"
            row['_SearchMonth'] = to_date.strftime('%Y-%m')
            judge_rows << row
          end
          total_for_judge += count
        end

        puts "  [#{pct}%] #{from_str} - #{to_str}: #{count} records (total: #{total_for_judge})"

      rescue => e
        puts "  [#{pct}%] #{from_str} - #{to_str}: ERROR - #{e.message}"
        sleep 3
        next
      end

      sleep 0.5
    end

    if judge_rows.any?
      all_headers = ['_Judge', '_DateRange', '_SearchMonth'] + (judge_columns || [])
      safe_headers = all_headers.reject { |h| h.nil? || h.empty? }
      
      CSV.open(judge_csv, 'w') do |csv|
        csv << safe_headers
        judge_rows.each do |row|
          csv << safe_headers.map { |h| row[h] || '' }
        end
      end
      
      all_hearings.concat(judge_rows)
      
      file_size = File.size(judge_csv)
      puts "\n  >> SAVED: #{judge_csv}"
      puts "  >> Records: #{judge_rows.length} | Size: #{file_size} bytes"
    else
      puts "\n  >> No records found for #{judge}"
    end
  end

  if all_hearings.any?
    master_headers = ['_Judge', '_DateRange', '_SearchMonth'] + (all_headers || [])
    safe_headers = master_headers.reject { |h| h.nil? || h.empty? }
    
    CSV.open(hearings_csv_path, 'w') do |csv|
      csv << safe_headers
      all_hearings.each do |row|
        csv << safe_headers.map { |h| row[h] || '' }
      end
    end
    
    puts "\n#{'=' * 90}"
    puts "MASTER FILE: #{hearings_csv_path}"
    puts "Total records across all judges: #{all_hearings.length}"
    puts "File size: #{File.size(hearings_csv_path)} bytes"
  end

  puts "\n#{'=' * 90}"
  puts "PHASE 2: Scraping case detail pages for judgment amounts & attorney names"
  puts "#{'=' * 90}"

  if all_hearings.any?
    detail_csv_path = File.join(OUTPUT_DIR, "case_details_#{today.strftime('%m_%y')}.csv")
    detail_rows = []
    processed = 0
    total_cases = all_hearings.length

    all_hearings.each_with_index do |hearing, idx|
      case_num = hearing['CaseNumber'] || ''
      judge_name = hearing['_Judge'] || ''
      detail_url = hearing['CaseLoadUrl'] || ''
      style = hearing['Style'] || ''
      
      next if detail_url.empty?

      begin
        pct = ((idx + 1).to_f / total_cases * 100).round(1)
        processed += 1

        if processed % 25 == 0 || processed == 1
          puts "  [#{pct}%] Processing case #{processed}/#{total_cases}: #{case_num}"
        end

        driver.get(detail_url)
        sleep 1

        detail = driver.execute_script(<<~JS)
          var body = document.body.innerText || '';
          var result = {};

          var caseInfoMatch = body.match(/Case Number[s]*\\s*([^\\n]+)/);
          if (caseInfoMatch) result['CaseNumber_detail'] = caseInfoMatch[1].trim().split(/\\n/)[0].split('|')[0].trim();

          var styleMatch = body.match(/\\|[^\\n]*\\n\\nCase Number/);
          var caseHeader = body.match(/\\d+[A-Z]+\\d+\\s*\\|\\s*([^\\n]+)/);
          if (caseHeader) result['CaseStyle'] = caseHeader[1].trim();

          var courtMatch = body.match(/Court[^a-z]+([^\\n]+)/);
          if (courtMatch) result['Court'] = courtMatch[1].trim();

          var caseTypeMatch = body.match(/Case Type[^a-z]+([^\\n]+)/);
          if (caseTypeMatch) result['CaseType_detail'] = caseTypeMatch[1].trim();

          var caseStatusMatch = body.match(/Case Status[^a-z]+([^\\n]+)/);
          if (caseStatusMatch) result['CaseStatus'] = caseStatusMatch[1].trim();

          var fileDateMatch = body.match(/File Date[^a-z]+([^\\n]+)/);
          if (fileDateMatch) result['FileDate_detail'] = fileDateMatch[1].trim();

          var judgeMatch = body.match(/Judicial Officer[^a-z]+([^\\n]+)/);
          if (judgeMatch) result['JudicialOfficer_detail'] = judgeMatch[1].trim();

          var judgmentAmountMatch = body.match(/Judgment Amount:\\s*\\$?([^\\n]+)/);
          if (judgmentAmountMatch) result['JudgmentAmount'] = judgmentAmountMatch[1].trim();

          var costsMatch = body.match(/Court Costs:\\s*\\$?([^\\n]+)/);
          if (costsMatch) result['CourtCosts'] = costsMatch[1].trim();

          var totalMatch = body.match(/Total Judgment:\\s*of\\s*\\$?([^\\n]+)/);
          if (totalMatch) result['TotalJudgment'] = totalMatch[1].trim();
          
          var totalMatch2 = body.match(/Total Judgment:\\s*\\$?([^\\n]+)/);
          if (totalMatch2 && !result['TotalJudgment']) result['TotalJudgment'] = totalMatch2[1].trim();

          var awardedToMatch = body.match(/Awarded To[^a-z]+([^\\n]+)/);
          if (awardedToMatch) result['AwardedTo'] = awardedToMatch[1].trim();

          var awardedAgainstMatch = body.match(/Awarded Against[^a-z]+([^\\n]+)/);
          if (awardedAgainstMatch) result['AwardedAgainst'] = awardedAgainstMatch[1].trim();

          var judgmentTypeMatch = body.match(/Judgment Type[^a-z]+([^\\n]+)/);
          if (judgmentTypeMatch) result['JudgmentType'] = judgmentTypeMatch[1].trim();

          var judgmentDateMatch = body.match(/(\\d{2}\\/\\d{2}\\/\\d{4})\\s*Judgment[\\s\\S]{0,200}?Judgment Type/);
          if (judgmentDateMatch) result['JudgmentDate'] = judgmentDateMatch[1].trim();

          var attorneys = [];
          var attorneyMatches = body.matchAll(/Lead Attorney[^a-z]+([^\\n]+)/gi);
          for (var m of attorneyMatches) { attorneys.push(m[1].trim()); }
          if (!attorneys.length) {
            var altMatches = body.matchAll(/Attorney[^a-z]+([^\\n]+)/gi);
            for (var m of altMatches) {
              var txt = m[1].trim();
              if (txt.length > 0 && txt.length < 60 && !txt.includes('Active') && !txt.includes('Service')) {
                attorneys.push(txt);
              }
            }
          }
          result['Attorneys'] = attorneys.join('; ');

          var plaintiffMatch = body.match(/Plaintiff[^a-z]+\\n([^\\n]+)/);
          if (plaintiffMatch) result['Plaintiff'] = plaintiffMatch[1].trim();

          var defendantMatch = body.match(/Defendant[^a-z]+\\n([^\\n]+)/);
          if (defendantMatch) result['Defendant'] = defendantMatch[1].trim();

          var recentEvents = body.match(/Disposition Events[\\s\\S]{0,2000}?Events and Hearings/);
          if (recentEvents) result['DispositionEvents'] = recentEvents[0].substring(0, 500).replace(/\\n/g, ' | ').substring(0, 300);

          return result;
        JS

        detail['CaseNumber'] = case_num
        detail['_Judge'] = judge_name
        detail['_Style'] = style
        detail['_GridCaseType'] = hearing['CaseTypeId_Description'] || hearing['CaseTypeId'] || ''
        detail_rows << detail

      rescue => e
        detail_rows << {
          'CaseNumber' => case_num,
          '_Judge' => judge_name,
          '_Style' => style,
          '_Error' => e.message
        }
        next
      end

      sleep 0.3 if processed % 10 == 0
    end

    if detail_rows.any?
      detail_headers = detail_rows.flat_map(&:keys).uniq
      CSV.open(detail_csv_path, 'w') do |csv|
        csv << detail_headers
        detail_rows.each do |row|
          csv << detail_headers.map { |h| row[h] || '' }
        end
      end

      puts "\n  >> SAVED: #{detail_csv_path}"
      puts "  >> Total case details scraped: #{detail_rows.length}"
      puts "  >> Cases with judgments: #{detail_rows.count { |r| r['TotalJudgment'] && !r['TotalJudgment'].empty? }}"
      puts "  >> Cases with attorneys: #{detail_rows.count { |r| r['Attorneys'] && !r['Attorneys'].empty? }}"
    end
  end

rescue => e
  puts "FATAL ERROR: #{e.message}"
  puts e.backtrace.first(10).join("\n")
ensure
  driver.quit if driver
end

puts "\n#{'=' * 90}"
puts "COMPLETE: #{Time.now.strftime('%Y-%m-%d %H:%M:%S')}"
puts "Output files in: #{OUTPUT_DIR}/"
Dir.glob("#{OUTPUT_DIR}/*.csv").each do |f|
  puts "  #{File.basename(f)} - #{File.size(f)} bytes"
end
puts "#{'=' * 90}"
