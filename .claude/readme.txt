# Central Texas Legal Resource

A professional legal information website for Bell County and Central Texas, built with Jekyll for GitHub Pages hosting.

## File Structure

```
central-texas-legal/
├── _config.yml                 # Jekyll configuration
├── _layouts/
│   └── default.html            # Main page layout
├── _includes/
│   ├── ads-defense.html        # Defense attorney ads sidebar
│   ├── ads-injury.html         # Personal injury ads sidebar
│   └── ads-general.html        # General/homepage ads sidebar
├── assets/
│   ├── css/
│   │   └── style.css           # Main stylesheet
│   └── js/
│       └── main.js             # JavaScript functionality
├── index.md                    # Homepage
├── texas-law.md                # Texas Law information
├── bell-county.md              # Bell County specific info
├── defense.md                  # Criminal defense section
├── personal-injury.md          # Personal injury section
├── resources.md                # Legal resources
├── Gemfile                     # Ruby dependencies
└── README.md                   # This file
```

## Setup Instructions

### Local Development

1. **Install Ruby and Jekyll**
   ```bash
   # macOS with Homebrew
   brew install ruby
   gem install bundler jekyll
   ```

2. **Clone and install dependencies**
   ```bash
   git clone https://github.com/yourusername/central-texas-legal.git
   cd central-texas-legal
   bundle install
   ```

3. **Run locally**
   ```bash
   bundle exec jekyll serve
   ```
   Visit `http://localhost:4000`

### GitHub Pages Deployment

1. Create a new GitHub repository
2. Push all files to the repository
3. Go to Settings → Pages
4. Select "Deploy from a branch" and choose `main` branch
5. Your site will be available at `https://yourusername.github.io/repo-name/`

### Custom Domain (Optional)

1. Add a `CNAME` file with your domain name
2. Configure DNS with your registrar
3. Enable HTTPS in GitHub Pages settings

## Customization

### Adding Advertisers

Edit the appropriate `_includes/ads-*.html` file:
- `ads-defense.html` - Defense attorney page sidebar
- `ads-injury.html` - Personal injury page sidebar  
- `ads-general.html` - Homepage and other pages

### Adding Common Charges

The defense page (`defense.md`) has a placeholder section for common Bell County charges. Add content under the "Other Common Charges" heading.

### Modifying Colors/Theme

Edit CSS variables in `assets/css/style.css`:
```css
:root {
  --navy-dark: #0f233c;
  --navy: #1a3a5c;
  --gold: #c9a227;
  /* etc. */
}
```

## Features

- Responsive design for mobile/tablet/desktop
- Professional attorney/law firm aesthetic
- Right-sidebar advertising areas with context-specific ads
- SEO-optimized with Jekyll SEO Tag
- Accessible navigation with keyboard support
- Analytics-ready click tracking for phone/email

## Legal Disclaimer

This website template is for informational purposes. Ensure all content complies with Texas State Bar advertising rules and regulations. Consult with a legal advertising compliance professional before launching.

## License

Content and design © 2024. All rights reserved.
