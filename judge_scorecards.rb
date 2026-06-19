require 'csv'

data_dir = '/Users/sweeden/legal-luminary/scraped_data'
files = Dir.glob("#{data_dir}/case_details*.csv")

judges_stats = Hash.new do |h, judge|
  h[judge] = { total: 0, case_types: Hash.new { |h2, ct| h2[ct] = { total: 0, wins: 0, losses: 0, pending: 0 } } }
end

files.each do |file|
  begin
    CSV.foreach(file, headers: true, liberal_parsing: true, encoding: 'bom|utf-8') do |row|
      judge = row['JudicialOfficer_detail'] || row['_Judge'] || 'Unknown Judge'
      case_type = row['CaseType_detail'] || row['_GridCaseType'] || 'Unknown Type'
      judge = judge.strip
      case_type = case_type.strip

      judge = "Unknown Judge" if judge.empty?
      case_type = "Unknown Type" if case_type.empty?
      
      # Determine outcome
      judg_type = row['JudgmentType'].to_s.strip
      status = row['CaseStatus'].to_s.strip
      
      outcome = :pending
      if judg_type.downcase.include?('dismiss') || status.downcase == 'dismissed' || judg_type.downcase.include?('non-suit')
        outcome = :loss
      elsif judg_type.downcase.include?('judgment')
        outcome = :win
      end

      if outcome == :win
        judges_stats[judge][:total] += 1
        judges_stats[judge][:case_types][case_type][:total] += 1
        judges_stats[judge][:case_types][case_type][:wins] += 1
      elsif outcome == :loss
        judges_stats[judge][:total] += 1
        judges_stats[judge][:case_types][case_type][:total] += 1
        judges_stats[judge][:case_types][case_type][:losses] += 1
      end
    end
  rescue => e
    puts "Error processing #{file}: #{e.message}"
  end
end

md_file = '/Users/sweeden/.gemini/antigravity-ide/brain/65b32708-be3e-4f0b-9769-831e674f00c1/artifacts/judge_scorecards.md'
csv_file = '/Users/sweeden/.gemini/antigravity-ide/brain/65b32708-be3e-4f0b-9769-831e674f00c1/artifacts/judge_scorecards.csv'

# Make sure directory exists (it should, but just in case)
require 'fileutils'
FileUtils.mkdir_p(File.dirname(md_file))

md_content = "# Judge Scorecards\n\n"
md_content += "This report summarizes the major case load for each judge and their **Plaintiff Success Rate**.\n"
md_content += "The Success Rate is calculated as: `Judgments / (Judgments + Dismissals)`. Pending cases are excluded.\n\n"

CSV.open(csv_file, 'w') do |csv|
  csv << ['Judge', 'Total Cases', 'Major Case Type 1', 'Type 1 Cases', 'Type 1 Success Rate', 'Major Case Type 2', 'Type 2 Cases', 'Type 2 Success Rate', 'Major Case Type 3', 'Type 3 Cases', 'Type 3 Success Rate']
  
  judges_stats.sort_by { |j, s| -s[:total] }.each do |judge, stats|
    next if judge == "Unknown Judge"
    
    md_content += "## #{judge}\n"
    md_content += "**Total Resolved Cases:** #{stats[:total]}\n\n"
    
    csv_row = [judge, stats[:total]]
    
    # Get top 3 case types
    top_types = stats[:case_types].sort_by { |_, c_stats| -c_stats[:total] }.first(3)
    
    md_content += "| Case Type | Total Resolved | Judgments | Dismissals | **Success Rate** |\n"
    md_content += "|---|---|---|---|---|\n"
    
    top_types.each do |type, c_stats|
      resolved = c_stats[:total]
      rate = resolved > 0 ? (c_stats[:wins].to_f / resolved * 100).round(1) : 0
      
      md_content += "| #{type} | #{resolved} | #{c_stats[:wins]} | #{c_stats[:losses]} | **#{rate}%** |\n"
      csv_row += [type, resolved, "#{rate}%"]
    end
    
    # Pad CSV row if less than 3 case types
    while csv_row.length < 11
      csv_row += ['', '', '']
    end
    
    csv << csv_row
    md_content += "\n"
  end
end

File.write(md_file, md_content)
puts "Reports generated successfully at #{md_file} and #{csv_file}"
