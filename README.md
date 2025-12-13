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
│       └── jekyll.yml              # GitHub Actions workflow
├── _layouts/
│   └── default.html                # Main page layout
├── _includes/
│   ├── ads-defense.html            # Defense attorney sidebar ads
│   ├── ads-injury.html             # Personal injury sidebar ads
│   └── ads-general.html            # Homepage sidebar ads
├── _pages/
│   ├── frontpage.md                # Homepage
│   ├── texas-law.md                # Texas Law information
│   ├── bell-county.md              # Bell County specific info
│   ├── defense.md                  # Criminal defense section
│   ├── personal-injury.md          # Personal injury section
│   └── resources.md                # Legal resources
├── assets/
│   ├── css/
│   │   └── style.css               # Main stylesheet
│   └── js/
│       └── main.js                 # JavaScript functionality
├── _config.yml                     # Jekyll configuration
├── Gemfile                         # Ruby dependencies
├── .ruby-version                   # Ruby version specification
└── README.md                       # This file
```

---
## 💡 Site Branding, Color Theme, and Font

Whenever creating new pages, blog posts or UI functionality, developers and engineers should follow the style and branding guidelines below.

### Visual Elements

- Scales of Justice with embedded AI nodes (glowing blue circles) symbolizing the fusion of legal tradition and AI technology
- Texas Lone Star prominently displayed in gold, reinforcing the Central Texas identity
- Deep navy blue background with subtle circuit patterns conveying technological sophistication
- Golden accents providing a classic, prestigious legal aesthetic

### Typography

Title headings should be elegant serif font with gold gradient
Sections and subsections should be a modern sans-serif with tech-blue glow
Metadata and footers should have a supporting tagline for Texas attorneys

### Color Palette

The main colors of the site are below, however, pages and UI elements are not limited to only these colors:

- Navy/midnight blue (#0a1628 to #1a2744) Representing professionalism and trust
- Gold (#d4af37 to #f4d03f)  Representing prestige and legal tradition
- Cyan blue (#4da6ff) Representing AI and technology

## ⚙️ GitHub Actions Workflow

This project uses GitHub Actions for automated deployment. The workflow:

- Builds on pushes to the `main` branch
- Uses Ruby 3.3 with bundler caching
- Deploys to GitHub Pages automatically

---

## 🔧 Configuration

### Setting Your Site URL

Edit `_config.yml`:

```yaml
# For GitHub Pages project site:
baseurl: "/legal-luminary"
url: "https://sweeden-ttu.github.io"

# For custom domain:
baseurl: ""
url: "https://www.legalluminary.com"
```

> **Note:** When using GitHub Actions, the `baseurl` is automatically set by the workflow.

### Custom Domain Setup

1. Create a `CNAME` file in the root with your domain:
   ```
   www.yourdomain.com
   ```
2. Configure DNS with your registrar:
   - **A records** pointing to GitHub's IPs
   - **CNAME record** pointing to `sweeden-ttu.github.io`
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

## 📝 Content Guidelines: Third-Person Wording

### Why Third-Person is Required

**This website must use third-person impersonal wording throughout all content.** This is a critical requirement for several important reasons:

#### 1. AI Tool, Not Legal Advice Provider

This website is an **AI-enhanced legal information tool** that assists attorneys and their clients. It does **not** replace attorneys or provide direct legal advice. Using third-person wording (e.g., "individuals," "clients," "those who") rather than second-person ("you," "your") clearly establishes that:

- The content is informational and educational, not personalized legal advice
- The site serves as a resource tool, not a direct service provider
- Users should consult with licensed attorneys for advice specific to their situations

#### 2. Professional Distance and Objectivity

Third-person wording maintains appropriate professional distance and objectivity, which is essential for:

- **Attorneys using the site** as a resource for their clients
- **Clients reviewing information** before or after attorney consultations
- **Maintaining clear boundaries** between informational content and legal representation

#### 3. Compliance and Liability Protection

Using third-person impersonal language helps protect against:

- Unintended formation of attorney-client relationships
- Misinterpretation of general information as specific legal advice
- Claims that the website provides direct legal services

#### 4. Target Audience Clarity

The primary audience includes both:
- **Attorneys** who may reference this site when discussing cases with clients
- **Clients** who are researching legal topics before or during attorney consultations

Third-person wording accommodates both audiences without creating confusion about who is being addressed.

### Implementation Guidelines

When creating or editing content:

✅ **DO use:**
- "Individuals," "clients," "residents," "those who"
- "Their," "they," "them"
- "One's" (when appropriate)
- Impersonal constructions: "When facing charges..." instead of "When you face charges..."

❌ **DON'T use:**
- "You," "your," "you're"
- Direct address: "You should consult..." → "Individuals should consult..."
- Personal commands: "Contact an attorney" → "Individuals should contact an attorney"

### Examples

**Before (Second-Person):**
> "If you're facing criminal charges, you should understand your rights. You have the right to an attorney, and if you cannot afford one, one will be appointed."

**After (Third-Person):**
> "If individuals are facing criminal charges, they should understand their rights. They have the right to an attorney, and if they cannot afford one, one will be appointed."

**Before (Second-Person):**
> "When you've been injured due to someone else's negligence, you shouldn't have to bear the financial burden alone."

**After (Third-Person):**
> "When individuals have been injured due to someone else's negligence, they shouldn't have to bear the financial burden alone."

### Files Requiring Third-Person Wording

All content files must maintain third-person wording:
- `_pages/*.md` - All page content
- `_layouts/*.html` - Layout templates with content
- `_includes/*.html` - Include files with content
- Any new content files added to the site

---

## 🛠 Troubleshooting

### Build Failures

1. Check the **Actions** tab for error logs
2. Ensure `Gemfile.lock` is committed
3. Verify Ruby version compatibility (3.3+ recommended)

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

Content © 2024 Cloud Fronts Group, Killeen, TX. All rights reserved.

---

## 🔗 Resources

- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [GitHub Actions for Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site#publishing-with-a-custom-github-actions-workflow)
- [Official Starter Workflows](https://github.com/actions/starter-workflows/tree/main/pages)
