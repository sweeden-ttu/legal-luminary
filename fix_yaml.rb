files = Dir.glob('/Users/sweeden/legal-luminary/collections/_candidates/courts/**/*.md')

files.each do |file|
  next if file.include?('courts-directory.md')
  
  content = File.read(file)
  new_content = []
  in_top_case_types = false
  
  content.each_line do |line|
    if line.match?(/^  top_case_types:/)
      in_top_case_types = true
      new_content << line
    elsif in_top_case_types && line.match?(/^    - /)
      # Extract the value after "- "
      val = line.sub(/^    - /, '').strip
      # If it's already quoted, or doesn't have a colon, we can leave it (or just quote it anyway to be safe)
      if val.start_with?("'") || val.start_with?('"')
        new_content << line
      else
        new_content << "    - \"#{val}\"\n"
      end
    elsif in_top_case_types && !line.match?(/^    - /) && !line.strip.empty?
      # We left the top_case_types block
      in_top_case_types = false
      new_content << line
    else
      new_content << line
    end
  end
  
  File.write(file, new_content.join)
end

puts "Fixed YAML top_case_types quoting in markdown files."
