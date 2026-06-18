require 'open3'

OTHER_JUDGES = [
  'Garrett, Debbie',
  'Russell, Mike',
  'Starritt-Burnett, Cari',
  'Duskie, Steven J',
  'Mischtian, John M',
  'DePew, Rebecca A',
  'Gauntt, John T',
  'Duffield, Theodore R',
  'Coleman, Clifford',
  'Fisher, Rosanne',
  'James, Nicola J',
  'Cox, Beatrice'
]

puts "Starting scraping for other judges sequentially..."

OTHER_JUDGES.each do |judge|
  puts "Running scrape for #{judge}..."
  stdout, stderr, status = Open3.capture3("ruby run_judge.rb \"#{judge}\"")
  if status.success?
    puts "Successfully finished scraping for #{judge}"
  else
    puts "Failed for #{judge}: #{stderr}"
  end
end
puts "All done!"
