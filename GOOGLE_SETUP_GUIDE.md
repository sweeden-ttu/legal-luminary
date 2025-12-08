# Google Services Setup Guide for Legal Luminary

This guide will walk you through setting up Google Tag Manager, Google Ads, Google Search Console, and configuring DNS records in GoDaddy for `www.legalluminary.com`.

**Email Address:** sweeden@ttu.edu

---

## Part 1: Google Tag Manager Setup

### Step 1: Create Google Tag Manager Account

1. Go to [Google Tag Manager](https://tagmanager.google.com/)
2. Sign in with **sweeden@ttu.edu**
3. Click **"Create Account"**
4. Fill in the account details:
   - **Account Name:** Legal Luminary
   - **Country:** United States
   - Click **"Continue"**
5. Set up a container:
   - **Container Name:** www.legalluminary.com
   - **Target Platform:** Web
   - Click **"Create"**
6. Accept the Terms of Service
7. **Copy your Container ID** (format: `GTM-XXXXXXX`)

### Step 2: Add GTM Container ID to Website

1. Open `_config.yml` in the project root
2. Find the line: `gtm_container_id: "GTM-XXXXXXX"`
3. Replace `GTM-XXXXXXX` with your actual Container ID
4. Save the file
5. Commit and push to GitHub (the site will rebuild automatically)

### Step 3: Verify GTM Installation

1. After deploying, visit your website
2. Install the [Google Tag Assistant Chrome Extension](https://chrome.google.com/webstore/detail/tag-assistant-legacy-by-g/kejbdjndbnbjgmefkgdddjlbokphdefk)
3. Visit your site and check that GTM is loading correctly
4. You can also use browser DevTools → Network tab to verify `googletagmanager.com` requests

---

## Part 2: Google Ads Setup

### Step 1: Create Google Ads Account

1. Go to [Google Ads](https://ads.google.com/)
2. Sign in with **sweeden@ttu.edu**
3. Click **"Start Now"** or **"New Google Ads Account"**
4. Choose your country/region: **United States**
5. Select your time zone: **Central Time (CT)**
6. Choose your currency: **USD ($)**
7. Enter account details:
   - **Account Type:** Business
   - **Business Name:** Legal Luminary / Central Texas Legal Resource
   - **Website:** https://www.legalluminary.com
   - **Business Category:** Legal Services / Attorney
8. Complete the account setup wizard

### Step 2: Link Google Ads with Google Tag Manager

1. In Google Tag Manager, go to your container
2. Click **"Tags"** → **"New"**
3. Tag Configuration:
   - Choose **"Google Ads: Conversion Tracking"** or **"Google Ads: Remarketing"**
   - Enter your Google Ads Conversion ID (found in Google Ads → Tools → Conversions)
4. Configure triggers as needed
5. Click **"Save"** and **"Submit"** to publish

### Step 3: Set Up Conversion Tracking

1. In Google Ads, go to **Tools & Settings** → **Conversions**
2. Click **"+"** to create a new conversion action
3. Choose conversion type (e.g., "Website", "Phone calls", "App")
4. Configure:
   - **Category:** Lead / Sign-up / Other
   - **Conversion name:** e.g., "Contact Form Submission" or "Phone Call"
   - **Value:** Set if applicable
   - **Count:** One or Every
5. Copy the Conversion ID and Label
6. Add to GTM as a tag (see Step 2 above)

---

## Part 3: Google Search Console Setup

### Step 1: Add Property to Search Console

1. Go to [Google Search Console](https://search.google.com/search-console/)
2. Sign in with **sweeden@ttu.edu**
3. Click **"Add Property"**
4. Select **"URL prefix"** method
5. Enter: `https://www.legalluminary.com`
6. Click **"Continue"**

### Step 2: Verify Ownership

You have several verification options. Choose one:

#### Option A: HTML File Upload (Recommended for GitHub Pages)
1. Download the HTML verification file
2. Upload it to the root of your repository
3. Commit and push to GitHub
4. Click **"Verify"** in Search Console

#### Option B: HTML Tag
1. Copy the meta tag provided
2. Add it to `_layouts/default.html` in the `<head>` section
3. Commit and push
4. Click **"Verify"** in Search Console

#### Option C: DNS Verification (See Part 4 below)
1. Use the TXT record method (will be covered in DNS setup)

### Step 3: Submit Sitemap

1. After verification, go to **Sitemaps** in Search Console
2. Enter: `sitemap.xml`
3. Click **"Submit"**
4. Your sitemap should be at: `https://www.legalluminary.com/sitemap.xml`

---

## Part 4: GoDaddy DNS Configuration

### Step 1: Access GoDaddy DNS Settings

1. Log in to [GoDaddy](https://www.godaddy.com/)
2. Go to **My Products** → **Domains**
3. Find **legalluminary.com**
4. Click **"DNS"** or **"Manage DNS"**

### Step 2: Configure DNS Records

#### A. Verify Current Records
Check if these records exist:
- **A Record** or **CNAME** pointing to GitHub Pages
- **CNAME** for `www` subdomain

#### B. Add Google Search Console Verification (if using DNS method)
1. In Search Console, choose **"Domain name provider"** verification
2. Copy the TXT record value (format: `google-site-verification=XXXXXXXXXX`)
3. In GoDaddy DNS, add:
   - **Type:** TXT
   - **Name:** @ (or leave blank for root domain)
   - **Value:** `google-site-verification=XXXXXXXXXX`
   - **TTL:** 600 (or default)
4. Click **"Save"**
5. Wait 5-10 minutes, then verify in Search Console

#### C. Verify GitHub Pages DNS (if needed)
If not already configured, ensure:
- **CNAME Record:**
  - **Name:** www
  - **Value:** your-username.github.io (or GitHub Pages domain)
  - **TTL:** 600

- **A Records** (if using root domain):
  - Point to GitHub Pages IPs:
    - 185.199.108.153
    - 185.199.109.153
    - 185.199.110.153
    - 185.199.111.153

### Step 3: Additional DNS Records (Optional)

#### Email Records (if using custom email)
- **MX Records:** If you want to use Google Workspace or other email service
- **SPF Record:** For email authentication
- **DKIM Record:** For email security

---

## Part 5: Testing & Verification

### Test Google Tag Manager
1. Visit your website
2. Open browser DevTools (F12)
3. Go to **Console** tab
4. Type: `dataLayer` and press Enter
5. You should see the dataLayer array
6. Check **Network** tab for `googletagmanager.com` requests

### Test Google Ads
1. In Google Ads, go to **Tools & Settings** → **Conversions**
2. Test a conversion by triggering the action on your site
3. Check if the conversion appears in Google Ads (may take 24-48 hours)

### Test Search Console
1. In Search Console, go to **URL Inspection**
2. Enter a page URL from your site
3. Click **"Test Live URL"**
4. Verify it's indexed and accessible

### Verify DNS Propagation
1. Use [DNS Checker](https://dnschecker.org/) to verify DNS records globally
2. Check that `www.legalluminary.com` resolves correctly
3. Verify TXT records are propagated

---

## Part 6: Next Steps

### Recommended GTM Tags to Set Up

1. **Google Analytics 4 (GA4)**
   - Create GA4 property
   - Add GA4 Configuration tag in GTM

2. **Google Ads Conversion Tracking**
   - Set up conversion actions in Google Ads
   - Add conversion tags in GTM

3. **Google Ads Remarketing**
   - Add remarketing tag in GTM
   - Create audiences in Google Ads

4. **Facebook Pixel** (if using Facebook Ads)
   - Add Facebook Pixel tag in GTM

### Security & Privacy

1. **GDPR/CCPA Compliance**
   - Set up cookie consent banner
   - Configure GTM to respect consent
   - Update privacy policy

2. **Data Retention**
   - Configure data retention in GA4
   - Review Google Ads data retention settings

---

## Troubleshooting

### GTM Not Loading
- Check that Container ID is correct in `_config.yml`
- Verify the site has been rebuilt/deployed
- Check browser console for errors
- Ensure no ad blockers are interfering

### DNS Not Propagating
- DNS changes can take 24-48 hours
- Clear DNS cache: `sudo dscacheutil -flushcache` (Mac) or `ipconfig /flushdns` (Windows)
- Use DNS checker tools to verify globally

### Search Console Verification Failing
- Ensure verification file/tag is in the correct location
- Wait a few minutes after deployment
- Try alternative verification method
- Check that the site is publicly accessible

### Google Ads Not Tracking
- Verify tags are published in GTM
- Check that triggers are firing correctly
- Use Google Tag Assistant to debug
- Verify conversion IDs are correct

---

## Important Notes

- **Email:** All Google services should be set up using **sweeden@ttu.edu**
- **Domain:** www.legalluminary.com
- **Website:** https://www.legalluminary.com
- **TTL:** DNS changes may take time to propagate (typically 5 minutes to 48 hours)
- **Testing:** Always test in incognito/private browsing mode to avoid cached data

---

## Support Resources

- [Google Tag Manager Help](https://support.google.com/tagmanager/)
- [Google Ads Help](https://support.google.com/google-ads/)
- [Google Search Console Help](https://support.google.com/webmasters/)
- [GoDaddy DNS Help](https://www.godaddy.com/help/manage-dns-680)

---

**Last Updated:** [Current Date]
**Setup By:** sweeden@ttu.edu

