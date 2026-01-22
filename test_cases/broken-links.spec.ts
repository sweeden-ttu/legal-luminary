import { test, expect } from '@playwright/test';

interface LinkInfo {
  url: string;
  sourcePage: string;
  text: string;
}

test.describe('Broken Links Check', () => {
  test('find all broken links on the site', async ({ page, request }) => {
    const baseURL = process.env.PLAYWRIGHT_BASE_URL || 'http://127.0.0.1:4000';
    const visitedUrls = new Set<string>();
    const linksToCheck = new Map<string, LinkInfo[]>();
    const brokenLinks: Array<{ url: string; status: number; sourcePages: string[] }> = [];
    
    // Normalize URL to avoid duplicates
    const normalizeUrl = (url: string): string => {
      try {
        const urlObj = new URL(url, baseURL);
        // Remove trailing slash for consistency (except root)
        const pathname = urlObj.pathname === '/' ? '/' : urlObj.pathname.replace(/\/$/, '');
        return `${urlObj.origin}${pathname}${urlObj.search}${urlObj.hash}`;
      } catch {
        return url;
      }
    };

    // Check if URL is internal to the site
    const isInternalUrl = (url: string): boolean => {
      try {
        const urlObj = new URL(url, baseURL);
        const baseUrlObj = new URL(baseURL);
        return urlObj.origin === baseUrlObj.origin;
      } catch {
        return false;
      }
    };

    // Collect all links from a page
    const collectLinks = async (pageUrl: string): Promise<void> => {
      if (visitedUrls.has(pageUrl)) {
        return;
      }
      visitedUrls.add(pageUrl);

      try {
        const response = await page.goto(pageUrl, { waitUntil: 'domcontentloaded', timeout: 10000 });
        
        if (!response || response.status() >= 400) {
          console.warn(`Skipping ${pageUrl} - status: ${response?.status() || 'no response'}`);
          return;
        }

        // Get all links on the page
        const links = await page.locator('a[href]').all();
        
        for (const link of links) {
          const href = await link.getAttribute('href');
          const text = await link.textContent() || '';
          
          if (!href) continue;
          
          const absoluteUrl = normalizeUrl(href);
          
          // Only check internal links
          if (!isInternalUrl(absoluteUrl)) {
            continue;
          }

          // Skip anchors (same page links)
          if (absoluteUrl.includes('#')) {
            const urlWithoutHash = absoluteUrl.split('#')[0];
            if (urlWithoutHash === pageUrl || urlWithoutHash === `${pageUrl}/`) {
              continue;
            }
          }

          // Skip javascript:, mailto:, tel:, etc.
          if (href.startsWith('javascript:') || href.startsWith('mailto:') || href.startsWith('tel:')) {
            continue;
          }

          if (!linksToCheck.has(absoluteUrl)) {
            linksToCheck.set(absoluteUrl, []);
          }
          
          linksToCheck.get(absoluteUrl)!.push({
            url: absoluteUrl,
            sourcePage: pageUrl,
            text: text.trim().substring(0, 50) // Limit text length
          });
        }

        console.log(`Collected ${links.length} links from ${pageUrl}`);
      } catch (error) {
        console.error(`Error collecting links from ${pageUrl}:`, error);
      }
    };

    // Start crawling from homepage
    console.log('Starting link collection from homepage...');
    await collectLinks('/');

    // Also check common pages
    const commonPages = [
      '/about/',
      '/archive/',
      '/resources/',
      '/news-feeds/',
      '/advertise/',
      '/defense/',
      '/personal-injury/',
      '/bail-bonds/',
      '/bell-county/',
      '/texas-law/',
      '/artificial-intelligence/'
    ];

    for (const pagePath of commonPages) {
      const normalized = normalizeUrl(pagePath);
      if (!visitedUrls.has(normalized)) {
        await collectLinks(pagePath);
      }
    }

    // Check all collected links
    console.log(`\nChecking ${linksToCheck.size} unique internal links...`);
    
    for (const [url, linkInfos] of linksToCheck.entries()) {
      try {
        const response = await request.get(url, { timeout: 10000 });
        const status = response.status();
        
        if (status >= 400) {
          const sourcePages = [...new Set(linkInfos.map(li => li.sourcePage))];
          brokenLinks.push({
            url,
            status,
            sourcePages
          });
          console.error(`BROKEN: ${url} (${status}) - found on: ${sourcePages.join(', ')}`);
        }
      } catch (error) {
        const sourcePages = [...new Set(linkInfos.map(li => li.sourcePage))];
        brokenLinks.push({
          url,
          status: 0, // Network error or timeout
          sourcePages
        });
        console.error(`ERROR checking ${url} - found on: ${sourcePages.join(', ')}`, error);
      }
    }

    // Report results
    console.log(`\n=== Broken Links Report ===`);
    console.log(`Total links checked: ${linksToCheck.size}`);
    console.log(`Broken links found: ${brokenLinks.length}`);
    
    if (brokenLinks.length > 0) {
      console.log('\nBroken Links:');
      brokenLinks.forEach(({ url, status, sourcePages }) => {
        console.log(`  - ${url} (Status: ${status})`);
        console.log(`    Found on pages: ${sourcePages.join(', ')}`);
      });
    }

    // Fail the test if broken links are found
    expect(brokenLinks.length, `Found ${brokenLinks.length} broken link(s). See console output for details.`).toBe(0);
  });

  test('check all links on homepage', async ({ page, request }) => {
    await page.goto('/', { waitUntil: 'domcontentloaded' });
    
    const links = await page.locator('a[href]').all();
    const brokenLinks: Array<{ url: string; status: number; text: string }> = [];
    
    const baseURL = process.env.PLAYWRIGHT_BASE_URL || 'http://127.0.0.1:4000';
    
    for (const link of links) {
      const href = await link.getAttribute('href');
      const text = await link.textContent() || '';
      
      if (!href) continue;
      
      // Skip external links, anchors, and special protocols
      if (href.startsWith('http') && !href.startsWith(baseURL)) continue;
      if (href.startsWith('#') || href.startsWith('javascript:') || href.startsWith('mailto:') || href.startsWith('tel:')) continue;
      
      try {
        const url = href.startsWith('http') ? href : new URL(href, baseURL).href;
        const response = await request.get(url, { timeout: 5000 });
        
        if (response.status() >= 400) {
          brokenLinks.push({
            url,
            status: response.status(),
            text: text.trim().substring(0, 50)
          });
        }
      } catch (error) {
        // Skip errors for anchors or other non-http links
        if (!href.startsWith('#')) {
          brokenLinks.push({
            url: href,
            status: 0,
            text: text.trim().substring(0, 50)
          });
        }
      }
    }
    
    if (brokenLinks.length > 0) {
      console.log('\nBroken links on homepage:');
      brokenLinks.forEach(({ url, status, text }) => {
        console.log(`  - ${url} (${status}) - "${text}"`);
      });
    }
    
    expect(brokenLinks.length, `Found ${brokenLinks.length} broken link(s) on homepage`).toBe(0);
  });
});
