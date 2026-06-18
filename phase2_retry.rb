require 'selenium-webdriver'
require 'csv'
require 'fileutils'

OUTPUT_DIR = 'scraped_data'

# Build map of all case numbers -> their proper CaseLoadUrl from grid CSVs
case_map = {}
Dir.glob("#{OUTPUT_DIR}/[a-z]*_06_26.csv").each do |f|
  CSV.foreach(f, headers: true) do |row|
    cn = row['CaseNumber']
    url = row['CaseLoadUrl']
    next if cn.nil? || cn.empty? || url.nil? || url.empty?
    key = cn.strip
    unless case_map[key]
      case_map[key] = {
        url: url.strip,
        judge: row['_Judge'] || '',
        style: row['Style'] || row['SortStyleOrDefendant'] || '',
        case_type: row['CaseTypeId'] || ''
      }
    end
  end
end

puts "Case map built: #{case_map.length} cases with URLs"

# Read existing case_details CSV and find errors
detail_csv = File.join(OUTPUT_DIR, 'case_details_06_26.csv')
good_rows = []
error_cases = []

CSV.foreach(detail_csv, headers: true) do |row|
  if row['_Error'] && !row['_Error'].empty?
    cn = row['CaseNumber']
    if case_map[cn]
      error_cases << { case_number: cn, info: case_map[cn] }
    else
      good_rows << row.to_h
    end
  else
    good_rows << row.to_h
  end
end

puts "Good rows: #{good_rows.length} | To retry: #{error_cases.length}"

return if error_cases.empty?

options = Selenium::WebDriver::Chrome::Options.new
options.add_argument('--headless=new')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--window-size=1400,900')

driver = Selenium::WebDriver.for(:chrome, options: options)
driver.manage.timeouts.implicit_wait = 3

detail_rows = good_rows
success = 0
fail = 0

begin
  error_cases.each_with_index do |c, idx|
    begin
      driver.get(c[:info][:url])

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
        var am;
        while ((am = attyRe.exec(b)) !== null) attorneys.push(am[1].trim());
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

      result['CaseNumber'] = c[:case_number]
      result['_Judge'] = c[:info][:judge]
      result['_Style'] = c[:info][:style]
      result['_GridCaseType'] = c[:info][:case_type]
      detail_rows << result
      success += 1

      if (idx + 1) % 100 == 0 || idx == 0
        has_j = result['TotalJudgment'] && !result['TotalJudgment'].empty?
        puts "  [#{((idx+1).to_f/error_cases.length*100).round(1)}%] #{c[:case_number]} #{has_j ? '$' : ''} | OK:#{success} FAIL:#{fail}"
      end

    rescue => e
      puts "  [#{((idx+1).to_f/error_cases.length*100).round(1)}%] #{c[:case_number]}: #{e.message[0..60]}"
      detail_rows << { 'CaseNumber' => c[:case_number], '_Judge' => c[:info][:judge], '_Style' => c[:info][:style], '_Error' => e.message[0..200] }
      fail += 1
      next
    end
  end

  headers = detail_rows.flat_map(&:keys).uniq
  CSV.open(detail_csv, 'w') { |csv| csv << headers; detail_rows.each { |r| csv << headers.map { |h| r[h] || '' } } }

  puts "\nRETRY COMPLETE: Succeeded=#{success} Failed=#{fail}"
  puts "Final: #{detail_rows.length} rows in #{detail_csv}"

rescue => e
  puts "FATAL: #{e.message}"
ensure
  driver.quit if driver
end
