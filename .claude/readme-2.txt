# Central Texas Legal Resource

A professional legal information website for Bell County and Central Texas, built with Jekyll for GitHub Pages hosting using GitHub Actions.

## 🚀 Quick Start

### Option 1: Deploy with GitHub Actions (Recommended)

1. **Create a new repository** on GitHub
2. **Upload all files** from this project
3. **Enable GitHub Pages with Actions**:
   - Go to repository **Settings** → **Pages**
   - Under "Build and deployment", select **GitHub Actions** as the source
4. **The workflow will run automatically** on your first push to `main`
5. **Visit your site** at `https://yourusername.github.io/repo-name/`

### Option 2: Local Development First

```bash
# Clone the repository
git clone https://github.com/yourusername/central-texas-legal.git
cd central-texas-legal

# Install dependencies
bundle install

# Run locally
bundle exec jekyll serve

# Visit http://localhost:4000
```

---

## 📁 File Structure

```
central-texas-legal/
├── .github/
│   └── workflows/
│       ├── jekyll.yml              # Standard workflow (recommended)
│       ├── jekyll-gh-pages.yml     # Simple workflow (no Gemfile needed)
│       └── jekyll-advanced.yml     # Advanced with PR checks
├── _layouts/
│   └── default.html                # Main page layout
├── _includes/
│   ├── ads-defense.html            # Defense attorney sidebar ads
│   ├── ads-injury.html             # Personal injury sidebar ads
│   └── ads-general.html            # Homepage sidebar ads
├── assets/
│   ├── css/
│   │   └── style.css               # Main stylesheet
│   └── js/
│       └── main.js                 # JavaScript functionality
├── index.md                        # Homepage
├── texas-law.md                    # Texas Law information
├── bell-county.md                  # Bell County specific info
├── defense.md                      # Criminal defense section
├── personal-injury.md              # Personal injury section
├── resources.md                    # Legal resources
├── _config.yml                     # Jekyll configuration
├── Gemfile                         # Ruby dependencies
└── README.md                       # This file
```

---

## ⚙️ GitHub Actions Workflows

This project includes three workflow options. **Choose ONE** and place it in `.github/workflows/`:

### 1. `jekyll.yml` - Standard Workflow (Recommended)

The official GitHub starter workflow. Uses your `Gemfile` to install exact gem versions.

**Best for:** Sites with custom plugins or specific gem requirements.

### 2. `jekyll-gh-pages.yml` - Simple Workflow

Uses GitHub's pre-installed Jekyll dependencies. No `Gemfile` required.

**Best for:** Simple sites using only default GitHub Pages plugins.

### 3. `jekyll-advanced.yml` - Advanced Workflow

Includes PR build verification, HTML validation, and detailed deployment summaries.

**Best for:** Team projects requiring code review before deployment.

---

## 🔧 Configuration

### Setting Your Site URL

Edit `_config.yml`:

```yaml
# For GitHub Pages project site:
baseurl: "/your-repo-name"
url: "https://yourusername.github.io"

# For custom domain:
baseurl: ""
url: "https://yourdomain.com"
```

> **Note:** When using GitHub Actions, the `baseurl` is automatically set by the workflow.

### Custom Domain Setup

1. Create a `CNAME` file in the root with your domain:
   ```
   www.yourdomain.com
   ```
2. Configure DNS with your registrar:
   - **A records** pointing to GitHub's IPs
   - **CNAME record** pointing to `yourusername.github.io`
3. Enable HTTPS in repository Settings → Pages

---

## 📝 Customization

### Updating Advertiser Information

Edit the `_includes/ads-*.html` files:

| File | Used On |
|------|---------|
| `ads-defense.html` | Defense attorneys page |
| `ads-injury.html` | Personal injury page |
| `ads-general.html` | Homepage and other pages |

### Adding Content

Pages use front matter to configure layout and sidebar ads:

```yaml
---
layout: default
title: "Page Title"
permalink: /page-url/
sidebar_ads: defense    # Options: defense, injury, or omit for general
hero: true
hero_title: "Hero Section Title"
hero_subtitle: "Subtitle text"
---
```

### Modifying Theme Colors

Edit CSS variables in `assets/css/style.css`:

```css
:root {
  --navy-dark: #0f233c;
  --navy: #1a3a5c;
  --gold: #c9a227;
  --cream: #f8f6f1;
  /* ... */
}
```

---

## 🔒 Compliance Notes

### Texas State Bar Advertising Rules

Before launching, ensure compliance with:
- **Texas Disciplinary Rules of Professional Conduct**, Rule 7.01-7.07
- Required disclaimers for attorney advertising
- Proper labeling of paid advertisements

### Required Disclaimers

The site includes standard disclaimers:
- "This website provides general legal information only"
- "Attorney Advertising"
- "Prior results do not guarantee similar outcomes"

---

## 🛠 Troubleshooting

### Build Failures

1. Check the **Actions** tab for error logs
2. Ensure `Gemfile.lock` is committed
3. Verify Ruby version compatibility (3.1+ recommended)

### Local Development Issues

```bash
# Clear Jekyll cache
bundle exec jekyll clean

# Rebuild with verbose output
bundle exec jekyll build --trace

# Check for config errors
bundle exec jekyll doctor
```

### CSS Not Loading

- Verify `baseurl` is set correctly
- Check that asset paths use `{{ '/path' | relative_url }}`

---

## 📄 License

Content © 2024 Central Texas Legal Resource. All rights reserved.

---

## 🔗 Resources

- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [GitHub Actions for Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site#publishing-with-a-custom-github-actions-workflow)
- [Official Starter Workflows](https://github.com/actions/starter-workflows/tree/main/pages)
