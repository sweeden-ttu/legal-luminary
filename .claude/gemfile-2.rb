source "https://rubygems.org"

# Jekyll version - use latest 4.x for GitHub Actions deployment
gem "jekyll", "~> 4.3"

# Plugins
group :jekyll_plugins do
  gem "jekyll-seo-tag", "~> 2.8"      # SEO meta tags
  gem "jekyll-sitemap", "~> 1.4"      # Auto-generate sitemap.xml
  gem "jekyll-feed", "~> 0.17"        # RSS feed generation
end

# Required for local development server
gem "webrick", "~> 1.8"

# Windows and JRuby does not include zoneinfo files
platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end

# Performance-booster for watching directories on Windows
gem "wdm", "~> 0.1", :platforms => [:mingw, :x64_mingw, :mswin]

# Lock `http_parser.rb` gem to `v0.6.x` on JRuby builds
gem "http_parser.rb", "~> 0.6.0", :platforms => [:jruby]
