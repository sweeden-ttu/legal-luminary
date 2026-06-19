files = Dir.glob('/Users/sweeden/legal-luminary/collections/_candidates/courts/**/*.md')

files.each do |file|
  next if file.include?('courts-directory.md')
  
  content = File.read(file)
  
  # Check if it starts with ---
  if content.start_with?("---\n")
    # Find the second ---
    parts = content.split("\n---\n", 2)
    
    if parts.length == 1
      # Missing closing ---
      # Let's find where the frontmatter logically ends.
      # Usually it ends before the first line that is just normal text not indented.
      lines = content.split("\n")
      frontmatter = []
      body = []
      
      in_frontmatter = true
      lines.each_with_index do |line, index|
        next if index == 0 # Skip the first ---
        
        if in_frontmatter
          # If a line doesn't look like YAML key: value or indented array, it might be body
          # But let's look for a blank line followed by text, or just insert it after the last known YAML key block
          if line.match?(/^[A-Z]/) && !line.match?(/^[A-Za-z_]+:/) && !line.match?(/^- /)
            in_frontmatter = false
            body << line
          else
            frontmatter << line
          end
        else
          body << line
        end
      end
      
      new_content = "---\n" + frontmatter.join("\n") + "\n---\n" + body.join("\n")
      File.write(file, new_content)
      puts "Fixed missing closing --- in #{file}"
    end
  end
end
