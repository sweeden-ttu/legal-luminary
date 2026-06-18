require 'selenium-webdriver'
require 'csv'
require 'fileutils'
require 'date'

OUTPUT_DIR = 'scraped_data'
FileUtils.mkdir_p(OUTPUT_DIR)

all_cases = {}
Dir.glob("#{OUTPUT_DIR}/[a-z]*_06_26.csv").each do |csv_file|
  CSV.foreach(csv_file, headers: true) do |row|
    case_num = row['CaseNumber']
    url = row['CaseLoadUrl']
    next if case_num.nil? || case_num.empty? || url.nil? || url.empty?
    key = case_num.strip
    unless all_cases[key]
      all_cases[key] = {
        case_number: case_num.strip,
        url: url.strip,
        judge: row['_Judge'] || File.basename(csv_file, '_06_26.csv'),
        style: row['Style'] || row['SortStyleOrDefendant'] || '',
        case_type: row['CaseTypeId'] || ''
      }
    end
  end
end

detail_csv = File.join(OUTPUT_DIR, 'case_details_06_26.csv')
already_done = {}
if File.exist?(detail_csv)
  CSV.foreach(detail_csv, headers: true) { |row| already_done[row['CaseNumber']] = true }
end

remaining = all_cases.length - already_done.length
puts "=" * 80
puts "PHASE 2: CASE DETAIL SCRAPING (#{all_cases.length} unique)"
puts "Done: #{already_done.length} | Remaining: #{remaining}"
puts "=" * 80

return if remaining == 0

options = Selenium::WebDriver::Chrome::Options.new
options.add_argument('--headless=new')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--window-size=1400,900')
options.add_argument('--disable-gpu')

driver = Selenium::WebDriver.for(:chrome, options: options)
driver.manage.timeouts.implicit_wait = 3

detail_rows = []
if already_done.any?
  CSV.foreach(detail_csv, headers: true) { |row| detail_rows << row.to_h }
end

case_list = all_cases.values.reject { |c| already_done[c[:case_number]] }
total = case_list.length
total_all = all_cases.length

begin
  start_time = Time.now

  case_list.each_with_index do |case_info, idx|
    begin
      driver.get(case_info[:url])

      result = driver.execute_script(<<~'JS')
        var b = document.body.innerText || '';
        var r = {};
        var m;

        m = b.match(/Case Number\s*\n\s*([^\n]+)/);
        if (m) r['CaseNumber_detail'] = m[1].trim();

        m = b.match(/^Court\s*\n\s*([^\n]+)/m);
        if (m) r['Court'] = m[1].trim();

        m = b.match(/Case Type\s*\n\s*([^\n]+)/);
        if (m) r['CaseType_detail'] = m[1].trim();

        m = b.match(/Case Status\s*\n\s*([^\n]+)/);
        if (m) r['CaseStatus'] = m[1].trim();

        m = b.match(/File Date\s*\n\s*([^\n]+)/);
        if (m) r['FileDate_detail'] = m[1].trim();

        m = b.match(/Judicial Officer\s*\n\s*([^\n]+)/);
        if (m) r['JudicialOfficer_detail'] = m[1].trim();

        m = b.match(/Plaintiff[^\n]*\n\s*([A-Z][A-Za-z0-9\'.,\s-]+)/);
        if (m) r['Plaintiff'] = m[1].trim();

        m = b.match(/Defendant[^\n]*\n\s*([A-Z][A-Za-z0-9\'.,\s-]+)/);
        if (m) r['Defendant'] = m[1].trim();

        var attorneys = [];
        var attyRe = /Lead Attorney\s*\n\s*([^\n]+)/g;
        var attyMatch;
        while ((attyMatch = attyRe.exec(b)) !== null)
          attorneys.push(attyMatch[1].trim());
        r['Attorneys'] = attorneys.filter(function(x,i,a){return a.indexOf(x)===i;}).join('; ');

        m = b.match(/Judgment Type\s*\n\s*([^\n]+)/);
        if (m) r['JudgmentType'] = m[1].trim();

        m = b.match(/Judgment Amount[:\s]*\$?([\d,]+\.\d{2})/);
        if (m) r['JudgmentAmount'] = '$' + m[1];
        m = b.match(/Court Costs[:\s]*\$?([\d,]+\.\d{2})/);
        if (m) r['CourtCosts'] = '$' + m[1];
        m = b.match(/Total Judgment[:\s]*(?:of\s*)?\$?([\d,]+\.\d{2})/);
        if (m) r['TotalJudgment'] = '$' + m[1];

        m = b.match(/Awarded To[:\s]+([^\n]+)/);
        if (m) r['AwardedTo'] = m[1].trim();
        m = b.match(/Awarded Against[:\s]+([^\n]+)/);
        if (m) r['AwardedAgainst'] = m[1].trim();

        m = b.match(/(\d{2}\/\d{2}\/\d{4})[\s\S]{0,300}?\bJudgment\b[\s\S]{0,300}?Judgment Type/);
        if (m) r['JudgmentDate'] = m[1];

        return r;
      JS

      result['CaseNumber'] = case_info[:case_number]
      result['_Judge'] = case_info[:judge]
      result['_Style'] = case_info[:style]
      result['_GridCaseType'] = case_info[:case_type]
      detail_rows << result

      if (idx + 1) % 100 == 0 || idx == 0 || idx == total - 1
        elapsed = Time.now - start_time
        rate = (idx + 1) / elapsed
        eta = (total - idx - 1) / rate
        has_j = result['TotalJudgment'] && !result['TotalJudgment'].empty?
        tag = has_j ? ' $JUDGMENT' : ''
        puts "  [#{((idx+1).to_f/total*100).round(1)}%] #{case_info[:case_number]} #{tag} | #{case_info[:judge][0..25]} | #{(elapsed/60).round(0)}min elapsed, #{(eta/60).round(0)}min remaining"
        
        headers = detail_rows.flat_map(&:keys).uniq
        CSV.open(detail_csv, 'w') { |csv| csv << headers; detail_rows.each { |r| csv << headers.map { |h| r[h] || '' } } }
      end

    rescue => e
      puts "  [#{((idx+1).to_f/total*100).round(1)}%] #{case_info[:case_number]}: ERROR #{e.message[0..60]}"
      detail_rows << { 'CaseNumber' => case_info[:case_number], '_Judge' => case_info[:judge], '_Style' => case_info[:style], '_Error' => e.message[0..200] }
      next
    end
  end

  headers = detail_rows.flat_map(&:keys).uniq
  CSV.open(detail_csv, 'w') { |csv| csv << headers; detail_rows.each { |r| csv << headers.map { |h| r[h] || '' } } }

  with_j = detail_rows.count { |r| r['TotalJudgment'] && !r['TotalJudgment'].empty? }
  with_a = detail_rows.count { |r| r['Attorneys'] && !r['Attorneys'].empty? }
  elapsed = Time.now - start_time

  puts "\n#{'=' * 80}"
  puts "PHASE 2 COMPLETE in #{(elapsed/60).round(0)} min"
  puts "Cases: #{detail_rows.length} | Judgments: #{with_j} | Attorneys: #{with_a}"
  puts "File: #{detail_csv} (#{File.size(detail_csv)} bytes)"
  puts "#{'=' * 80}"

rescue => e
  puts "FATAL: #{e.message}"
  if detail_rows.any?
    headers = detail_rows.flat_map(&:keys).uniq
    CSV.open(detail_csv, 'w') { |csv| csv << headers; detail_rows.each { |r| csv << headers.map { |h| r[h] || '' } } }
    puts "Progress saved: #{detail_rows.length} rows"
  end
ensure
  driver.quit if driver
end
