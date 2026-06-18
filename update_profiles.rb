require 'csv'

DETAIL_CSV = 'scraped_data/case_details_06_26.csv'
unless File.exist?(DETAIL_CSV)
  puts "Details CSV not found."
  exit
end

stats = Hash.new { |h, k| h[k] = { cases: 0, judgements: 0, total_amount: 0.0, attorneys: {}, case_types: Hash.new(0) } }

CSV.foreach(DETAIL_CSV, headers: true) do |row|
  judge = row['_Judge']
  next unless judge
  stats[judge][:cases] += 1
  
  if row['TotalJudgment'] && !row['TotalJudgment'].empty?
    stats[judge][:judgements] += 1
    amt = row['TotalJudgment'].gsub(/[^\d\.]/, '').to_f
    stats[judge][:total_amount] += amt
  end
  
  attys = row['Attorneys']
  if attys && !attys.empty?
    attys.split(';').each do |a|
      stats[judge][:attorneys][a.strip] = true
    end
  end
  
  ctype = row['_GridCaseType'] || row['CaseType_detail']
  if ctype && !ctype.empty?
    stats[judge][:case_types][ctype.strip] += 1
  end
end

JUDGE_FILE_MAP = {
  'Johnson, Gregory D.' => 'collections/_candidates/courts/jp/gregory_johnson.md',
  'Wilkey, Larry' => 'collections/_candidates/courts/jp/larry_wilkey.md',
  'MOTZ, PAUL A.' => 'collections/_candidates/courts/county/paul_a_motz.md',
  'LePak, Paul L' => 'collections/_candidates/courts/district/paul_l_lepak.md',
  'Faulkner, Wade' => 'collections/_candidates/courts/district/wade_faulkner.md'
}

stats.each do |judge, data|
  file = JUDGE_FILE_MAP[judge]
  next unless file && File.exist?(file)
  
  top_types = data[:case_types].sort_by { |_, count| -count }.first(5).map do |type, count|
    "#{type}: #{count} cases"
  end.join("\n    - ")
  
  avg_judgment = data[:judgements] > 0 ? (data[:total_amount] / data[:judgements]).round(2) : 0
  
  yaml_stats = <<~YAML
  odyssey_statistics:
    total_cases_scraped: #{data[:cases]}
    total_judgments_awarded: #{data[:judgements]}
    total_judgment_amount_awarded: $#{'%.2f' % data[:total_amount]}
    average_judgment_amount: $#{'%.2f' % avg_judgment}
    distinct_attorneys_appeared: #{data[:attorneys].keys.size}
    top_case_types:
      - #{top_types}
  YAML
  
  content = File.read(file)
  new_content = content.sub(/odyssey_results_placeholder:.*?(?=\n\w)/m, yaml_stats.strip + "\n")
  
  File.write(file, new_content)
  puts "Updated #{file}"
end
