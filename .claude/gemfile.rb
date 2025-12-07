source "https://rubygems.org"

gem "jekyll", "~> 4.3"
gem "jekyll-seo-tag", "~> 2.8"
gem "webrick", "~> 1.8"

# GitHub Pages compatibility
group :jekyll_plugins do
  gem "github-pages", "~> 228"
end
