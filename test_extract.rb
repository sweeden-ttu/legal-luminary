require 'selenium-webdriver'

options = Selenium::WebDriver::Chrome::Options.new
options.add_argument('--headless=new')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--window-size=1400,900')

driver = Selenium::WebDriver.for(:chrome, options: options)

begin
  # Test Portfolio Recovery case with judgment
  url1 = 'https://justice.bellcounty.texas.gov/PublicPortal/Case/CaseDetail?eid=3FE7831D74BFE382CB5FFA4BD1E83F3C&tabIndex=3'
  driver.get(url1)
  sleep 3

  result = driver.execute_script(<<~'JS')
    var body = document.body.innerText || '';
    var r = {};
    
    var m = body.match(/Case Number\s*\n\s*([^\n]+)/);
    if (m) r['CaseNumber_detail'] = m[1].trim();
    
    m = body.match(/^Court\s*\n\s*([^\n]+)/m);
    if (m) r['Court'] = m[1].trim();
    
    m = body.match(/Case Type\s*\n\s*([^\n]+)/);
    if (m) r['CaseType_detail'] = m[1].trim();
    
    m = body.match(/Case Status\s*\n\s*([^\n]+)/);
    if (m) r['CaseStatus'] = m[1].trim();
    
    m = body.match(/File Date\s*\n\s*([^\n]+)/);
    if (m) r['FileDate_detail'] = m[1].trim();
    
    m = body.match(/Judicial Officer\s*\n\s*([^\n]+)/);
    if (m) r['JudicialOfficer_detail'] = m[1].trim();
    
    m = body.match(/Plaintiff[^\n]*\n\s*([A-Z][A-Za-z0-9\'.,\s-]+)/);
    if (m) r['Plaintiff'] = m[1].trim();
    
    m = body.match(/Defendant[^\n]*\n\s*([A-Z][A-Za-z0-9\'.,\s-]+)/);
    if (m) r['Defendant'] = m[1].trim();
    
    var attorneys = [];
    var attyRe = /Lead Attorney\s*\n\s*([^\n]+)/g;
    var attyMatch;
    while ((attyMatch = attyRe.exec(body)) !== null) {
      attorneys.push(attyMatch[1].trim());
    }
    r['Attorneys'] = attorneys.join('; ');
    
    m = body.match(/Judgment Type\s*\n\s*([^\n]+)/);
    if (m) r['JudgmentType'] = m[1].trim();
    
    m = body.match(/Judgment Amount[:\s]*\$?([\d,]+\.\d{2})/);
    if (m) r['JudgmentAmount'] = '$' + m[1].trim();
    
    m = body.match(/Court Costs[:\s]*\$?([\d,]+\.\d{2})/);
    if (m) r['CourtCosts'] = '$' + m[1].trim();
    
    m = body.match(/Total Judgment[:\s]*(?:of\s*)?\$?([\d,]+\.\d{2})/);
    if (m) r['TotalJudgment'] = '$' + m[1].trim();
    
    m = body.match(/Awarded To[^\n]*\n\s*([^\n]+)/);
    if (m) r['AwardedTo'] = m[1].trim();
    
    m = body.match(/Awarded Against[^\n]*\n\s*([^\n]+)/);
    if (m) r['AwardedAgainst'] = m[1].trim();
    
    m = body.match(/(\d{2}\/\d{2}\/\d{4})[\s\S]{0,300}?\bJudgment\b[\s\S]{0,300}?Judgment Type/);
    if (m) r['JudgmentDate'] = m[1];
    
    return r;
  JS

  puts "Portfolio Case (with judgment):"
  result.each { |k, v| puts "  #{k}: #{v}" }

  # Also test a case from Faulkner to see format
  puts "\n\nFaulkner Case:"
  url2 = 'https://justice.bellcounty.texas.gov/PublicPortal/Case/CaseDetail?eid=C5A372C2DF5F4C802F0BC338814EF897&tabIndex=3'
  driver.get(url2)
  sleep 3
  
  result2 = driver.execute_script(<<~'JS')
    var body = document.body.innerText || '';
    var r = {};
    
    var m = body.match(/Case Number\s*\n\s*([^\n]+)/);
    if (m) r['CaseNumber_detail'] = m[1].trim();
    
    m = body.match(/^Court\s*\n\s*([^\n]+)/m);
    if (m) r['Court'] = m[1].trim();
    
    m = body.match(/Case Type\s*\n\s*([^\n]+)/);
    if (m) r['CaseType_detail'] = m[1].trim();
    
    m = body.match(/Case Status\s*\n\s*([^\n]+)/);
    if (m) r['CaseStatus'] = m[1].trim();
    
    m = body.match(/File Date\s*\n\s*([^\n]+)/);
    if (m) r['FileDate_detail'] = m[1].trim();
    
    m = body.match(/Judicial Officer\s*\n\s*([^\n]+)/);
    if (m) r['JudicialOfficer_detail'] = m[1].trim();
    
    m = body.match(/Plaintiff[^\n]*\n\s*([A-Z][A-Za-z0-9\'.,\s-]+)/);
    if (m) r['Plaintiff'] = m[1].trim();
    
    m = body.match(/Defendant[^\n]*\n\s*([A-Z][A-Za-z0-9\'.,\s-]+)/);
    if (m) r['Defendant'] = m[1].trim();
    
    var attorneys = [];
    var attyRe = /Lead Attorney\s*\n\s*([^\n]+)/g;
    var attyMatch;
    while ((attyMatch = attyRe.exec(body)) !== null) {
      attorneys.push(attyMatch[1].trim());
    }
    r['Attorneys'] = attorneys.join('; ');
    
    m = body.match(/Judgment Type\s*\n\s*([^\n]+)/);
    if (m) r['JudgmentType'] = m[1].trim();
    
    m = body.match(/Judgment Amount[:\s]*\$?([\d,]+\.\d{2})/);
    if (m) r['JudgmentAmount'] = '$' + m[1].trim();
    
    m = body.match(/Court Costs[:\s]*\$?([\d,]+\.\d{2})/);
    if (m) r['CourtCosts'] = '$' + m[1].trim();
    
    m = body.match(/Total Judgment[:\s]*(?:of\s*)?\$?([\d,]+\.\d{2})/);
    if (m) r['TotalJudgment'] = '$' + m[1].trim();
    
    m = body.match(/Awarded To[^\n]*\n\s*([^\n]+)/);
    if (m) r['AwardedTo'] = m[1].trim();
    
    m = body.match(/Awarded Against[^\n]*\n\s*([^\n]+)/);
    if (m) r['AwardedAgainst'] = m[1].trim();
    
    return r;
  JS
  
  result2.each { |k, v| puts "  #{k}: #{v}" }

rescue => e
  puts "ERROR: #{e.message}"
  puts e.backtrace.first(10).join("\n")
ensure
  driver.quit if driver
end
