require 'csv'
require 'fileutils'

csv_file = '/Users/sweeden/.gemini/antigravity-ide/brain/65b32708-be3e-4f0b-9769-831e674f00c1/artifacts/judge_scorecards.csv'

# Map CSV judge names to their markdown files
judge_file_map = {
  "Johnson, Gregory D." => "collections/_candidates/courts/jp/gregory_johnson.md",
  "Wilkey, Larry" => "collections/_candidates/courts/jp/larry_wilkey.md",
  "LePak, Paul L" => "collections/_candidates/courts/district/paul_l_lepak.md",
  "MOTZ, PAUL A." => "collections/_candidates/courts/county/paul_a_motz.md",
  "Parker, Jeanne" => "collections/_candidates/courts/county/jeanne_parker.md",
  "Faulkner, Wade" => "collections/_candidates/courts/district/wade_faulkner.md",
  "Ivey, G.W." => "collections/_candidates/courts/associate/ivey.md"
}

judges_data = {}

CSV.foreach(csv_file, headers: true) do |row|
  judge = row['Judge']
  total_cases = row['Total Cases']
  
  stats = []
  [1, 2, 3].each do |i|
    type = row["Major Case Type #{i}"]
    next if type.nil? || type.strip.empty?
    cases = row["Type #{i} Cases"]
    rate = row["Type #{i} Success Rate"]
    stats << { type: type, cases: cases, rate: rate }
  end
  
  judges_data[judge] = { total: total_cases, stats: stats }
end

base_dir = '/Users/sweeden/legal-luminary'

judges_data.each do |judge, data|
  rel_path = judge_file_map[judge]
  if rel_path
    full_path = File.join(base_dir, rel_path)
    if File.exist?(full_path)
      # Build the markdown content to append
      append_content = "\n\n## Case Load & Decision Summary\n\n"
      append_content += "Based on an analysis of **#{data[:total]}** recently resolved cases, the following is a summary of the judge's major caseload and how they typically decide them.\n\n"
      append_content += "The **Success Rate** measures how often the Plaintiff/Filer (e.g., the landlord, debt collector, or state) wins a judgment. Cases that were dismissed or resulted in a judgment for the defendant lower this rate. Active or pending cases are excluded.\n\n"
      
      append_content += "| Case Type | Resolved Cases | Plaintiff Success Rate |\n"
      append_content += "|---|---|---|\n"
      
      data[:stats].each do |stat|
        append_content += "| #{stat[:type]} | #{stat[:cases]} | **#{stat[:rate]}** |\n"
      end
      
      append_content += "\n"
      
      # Append to file
      File.open(full_path, 'a') do |f|
        f.write(append_content)
      end
      
      puts "Appended stats to #{rel_path}"
    else
      puts "WARNING: File not found: #{full_path}"
    end
  else
    puts "WARNING: No mapping found for judge: #{judge}"
  end
end
