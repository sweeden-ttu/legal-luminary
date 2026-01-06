# AGENTS.md - Guide for AI Agents Working with Legal Luminary Jekyll Site

This document provides comprehensive information for AI agents and developers working with the Central Texas Legal Resource Jekyll site, including folder structure, compilation methods, testing procedures, and verification workflows.

## 📁 Jekyll Folder Structure

### Core Jekyll Directories

```
legal-luminary-1/
├── _config.yml              # Jekyll configuration (site settings, navigation, plugins)
├── _layouts/                # Page layout templates
│   ├── default.html         # Main layout (includes header, footer, sidebar)
│   └── m3u8downloader.html  # Special layout for M3U8 downloader page
├── _includes/               # Reusable HTML components
│   ├── ads-defense.html     # Defense attorney sidebar ads
│   ├── ads-injury.html      # Personal injury sidebar ads
│   ├── ads-general.html     # General/homepage sidebar ads
│   ├── ads-home.html        # Homepage-specific ads
│   ├── footer.html          # Site footer component
│   └── sidebar-feed.html    # Sidebar feed component
├── _pages/                  # Static pages (Markdown with front matter)
│   ├── frontpage.md         # Homepage (/)
│   ├── defense.md           # Defense attorneys page (/defense/)
│   ├── personal-injury.md   # Personal injury page (/personal-injury/)
│   ├── texas-law.md         # Texas law information
│   ├── bell-county.md       # Bell County specific info
│   └── [other pages].md
├── _posts/                  # Blog posts (dated Markdown files)
│   └── YYYY-MM-DD-post-title.md
├── assets/                  # Static assets (CSS, JS, images)
│   ├── css/
│   │   └── style.css        # Main stylesheet
│   ├── js/
│   │   ├── main.js          # Main JavaScript
│   │   └── modules/         # ES6 modules
│   └── imgs/                # Images
└── _site/                   # Generated site (build output, gitignored)
```

### Key Configuration Files

- **`_config.yml`**: Site configuration, navigation, plugins, service area info
- **`Gemfile`**: Ruby dependencies (Jekyll, plugins)
- **`package.json`**: Node.js dependencies (Playwright, TypeScript)
- **`playwright.config.ts`**: Playwright test configuration

## 🔨 Compilation Methods

### Local Development Build

```bash
# Install Ruby dependencies
bundle install

# Build the site (outputs to _site/)
bundle exec jekyll build

# Serve locally with auto-reload (http://127.0.0.1:4000)
bundle exec jekyll serve --livereload --host 127.0.0.1 --port 4000 --baseurl '' --incremental
```

### Using npm Scripts

```bash
# Start Jekyll server (uses package.json script)
npm run jekyll:serve

# Build only (no server)
bundle exec jekyll build
```

### Production Build (GitHub Actions)

The site is automatically built and deployed via GitHub Actions workflow (`.github/workflows/jekyll.yml`). The workflow:
1. Sets up Ruby 3.3
2. Installs dependencies via `bundle install`
3. Builds the site with `bundle exec jekyll build`
4. Deploys to GitHub Pages

### Build Output

- **Destination**: `_site/` directory
- **Base URL**: Configured in `_config.yml` (empty for custom domain, `/repo-name` for project sites)
- **URL**: Set in `_config.yml` (default: `https://www.legalluminary.com`)

## 🧪 Testing with Playwright

### Test Configuration

**File**: `playwright.config.ts`
- **Base URL**: `http://127.0.0.1:4000` (default, configurable via `PLAYWRIGHT_BASE_URL` env var)
- **Test Directory**: `./tests`
- **Timeout**: 30 seconds per test, 10 seconds for expectations

### Running Tests

```bash
# Install Playwright browsers (first time only)
npx playwright install

# Run all tests (requires Jekyll server running)
npm run test:e2e

# Run tests with UI mode (interactive)
npm run test:e2e:ui

# Run tests in headed mode (see browser)
npm run test:e2e:headed

# Run tests with automatic server start/stop
npm run e2e
```

### Test Files

1. **`tests/smoke.spec.ts`**: Basic smoke tests (page loads, navigation, sitemap)
2. **`tests/ads-verification.spec.ts`**: Advertisement section verification (see below)
3. **`tests/cache-js-files.spec.ts`**: JavaScript file caching tests
4. **`tests/mediasite-m3u8.spec.ts`**: M3U8 downloader functionality tests

### Test Structure

Tests use Playwright's test framework with TypeScript:

```typescript
import { test, expect } from '@playwright/test';

test.describe('Test Suite Name', () => {
  test('test name', async ({ page }) => {
    await page.goto('/path');
    await expect(page.locator('selector')).toBeVisible();
  });
});
```

## ✅ Verification Workflow

### Pre-Deployment Verification Checklist

1. **Build Verification**
   ```bash
   bundle exec jekyll build
   # Check for errors in output
   ```

2. **Local Server Test**
   ```bash
   bundle exec jekyll serve
   # Manually verify pages load correctly
   ```

3. **Playwright Test Suite**
   ```bash
   npm run e2e
   # All tests should pass
   ```

4. **Advertisement Verification** (see below)

### Advertisement Section Verification

The site includes advertisement sections in the sidebar that must be verified:

#### Advertisement Locations

1. **Homepage** (`/`): General ads (`ads-general.html` or `sidebar_ads_content` in front matter)
2. **Defense Page** (`/defense/`): Defense attorney ads (`ads-defense.html` or `sidebar_ads_content`)
3. **Personal Injury Page** (`/personal-injury/`): Personal injury ads (`ads-injury.html` or `sidebar_ads_content`)

#### Advertisement Structure

Ads are rendered in the sidebar within a `.ad-section` container:
- Each ad is a `.ad-card` element
- Featured ads have class `.ad-card.featured`
- Ads contain:
  - `.ad-specialty`: Service type (e.g., "Criminal Defense", "Personal Injury")
  - `h4`: Attorney/service name
  - `p`: Description
  - `.ad-contact`: Contact information
  - `.ad-cta`: Call-to-action button/link
  - `.ad-disclaimer`: Legal disclaimers (optional)

#### How Ads Are Included

**Method 1: Front Matter (Current Implementation)**
Pages specify ads via `sidebar_ads_content` in front matter:
```yaml
---
layout: default
title: Defense Attorneys
sidebar_ads_content: |
  <div class="ad-card featured">
    <!-- ad content -->
  </div>
---
```

**Method 2: Include Files (Alternative)**
Layout can include ad files based on `sidebar_ads` front matter variable:
```yaml
---
sidebar_ads: defense  # Options: defense, injury, general
---
```

The layout (`_layouts/default.html`) checks for `page.sidebar_ads_content` and renders it in the sidebar.

## 🧪 Advertisement Verification Tests

### Test File: `tests/ads-verification.spec.ts`

This test suite verifies that:
1. Advertisement sections appear on the correct pages
2. Ads contain required elements (specialty, name, contact info, CTA)
3. Featured ads are properly marked
4. Ad disclaimers are present where required
5. Ad links are functional

### Running Advertisement Tests

```bash
# Run only ad verification tests
npx playwright test tests/ads-verification.spec.ts

# Run with UI mode for debugging
npx playwright test tests/ads-verification.spec.ts --ui
```

### Test Coverage

The `ads-verification.spec.ts` test file includes:

1. **Homepage Ad Verification**
   - Verifies `.ad-section` exists in sidebar
   - Checks for "ADVERTISEMENT" label
   - Validates ad cards are present
   - Verifies contact information and CTAs

2. **Defense Page Ad Verification**
   - Verifies defense-specific ads appear
   - Checks for "Criminal Defense" or "Bail Bonds" specialties
   - Validates featured ad is marked correctly

3. **Personal Injury Page Ad Verification**
   - Verifies injury-specific ads appear
   - Checks for "Personal Injury" specialty
   - Validates disclaimers for contingency fee basis

4. **Ad Structure Validation**
   - Ensures all ads have required elements
   - Verifies links are functional
   - Checks for proper ARIA labels

## 🔍 Debugging and Troubleshooting

### Common Issues

1. **Ads Not Appearing**
   - Check `sidebar_ads_content` in page front matter
   - Verify layout includes ad section: `{% if page.sidebar_ads_content %}`
   - Check browser console for JavaScript errors

2. **Build Failures**
   ```bash
   bundle exec jekyll build --trace
   bundle exec jekyll doctor
   ```

3. **Test Failures**
   - Ensure Jekyll server is running on port 4000
   - Check `PLAYWRIGHT_BASE_URL` environment variable
   - Run with `--headed` flag to see browser behavior

4. **Port Conflicts**
   - Change port in `jekyll serve` command
   - Update `PLAYWRIGHT_BASE_URL` accordingly

### Useful Commands

```bash
# Clean build cache
bundle exec jekyll clean

# Rebuild with verbose output
bundle exec jekyll build --trace

# Check Jekyll configuration
bundle exec jekyll doctor

# View Playwright test report
npx playwright show-report
```

## 📝 Content Guidelines for Agents

### Third-Person Wording Requirement

**CRITICAL**: All content must use third-person impersonal wording:
- ✅ Use: "individuals," "clients," "those who," "they," "their"
- ❌ Avoid: "you," "your," "you're"

This is required for compliance and to maintain professional distance.

### Advertisement Content Standards

- All ads must include "ADVERTISEMENT" label
- Attorney ads must include licensing disclaimers
- Contingency fee ads must include fee structure disclaimers
- Contact information must be accurate and functional
- Links must include appropriate `rel` attributes (`sponsored`, `noopener noreferrer`)

### File Modification Guidelines

- **DO NOT** delete or rename existing files
- **DO NOT** change function or class names
- **DO** follow existing patterns when adding content
- **DO** maintain third-person wording throughout

## 🔗 Related Documentation

- **README.md**: General project overview and setup
- **docs/ES6_MODULES_GUIDE.md**: JavaScript module structure
- **docs/PLAYWRIGHT_CACHE_GUIDE.md**: Playwright caching strategies
- **docs/GOOGLE_SETUP_GUIDE.md**: Google Tag Manager setup

## 🚀 Quick Reference

### Start Development Environment
```bash
npm run jekyll:serve  # Starts Jekyll on http://127.0.0.1:4000
```

### Run All Tests
```bash
npm run e2e  # Starts server, runs tests, stops server
```

### Verify Ads
```bash
npx playwright test tests/ads-verification.spec.ts
```

### Build for Production
```bash
bundle exec jekyll build
# Output in _site/
```

---

**Last Updated**: 2025-01-XX  
**Maintained By**: Cloud Fronts Group  
**For Questions**: See README.md or project documentation

