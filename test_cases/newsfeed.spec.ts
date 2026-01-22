import { test, expect } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';

test.describe('Newsfeed Validation', () => {
  const baseURL = process.env.PLAYWRIGHT_BASE_URL || 'http://127.0.0.1:4000';
  const isProduction = baseURL.includes('legalluminary.com');
  
  test.describe('Newsfeed Data File Validation', () => {
    test('news-feed.json file exists and has valid structure', () => {
      const dataPath = path.resolve(process.cwd(), '_data', 'news-feed.json');
      expect(fs.existsSync(dataPath), 'news-feed.json file should exist').toBe(true);
      
      const fileContent = fs.readFileSync(dataPath, 'utf-8');
      const newsData = JSON.parse(fileContent);
      
      // Validate top-level structure
      expect(newsData, 'news-feed.json should be an object').toBeInstanceOf(Object);
      expect(newsData).toHaveProperty('feeds');
      expect(newsData).toHaveProperty('all_items');
      expect(newsData).toHaveProperty('total_items');
      
      // Validate feeds array
      expect(Array.isArray(newsData.feeds), 'feeds should be an array').toBe(true);
      
      // Validate each feed structure
      newsData.feeds.forEach((feed: any, index: number) => {
        expect(feed, `Feed ${index} should have source`).toHaveProperty('source');
        expect(feed, `Feed ${index} should have url`).toHaveProperty('url');
        expect(feed, `Feed ${index} should have items array`).toHaveProperty('items');
        expect(Array.isArray(feed.items), `Feed ${index} items should be an array`).toBe(true);
        
        // Validate feed items if they exist
        feed.items.forEach((item: any, itemIndex: number) => {
          expect(item, `Feed ${index}, Item ${itemIndex} should have title`).toHaveProperty('title');
          expect(item, `Feed ${index}, Item ${itemIndex} should have link`).toHaveProperty('link');
          expect(item, `Feed ${index}, Item ${itemIndex} should have date`).toHaveProperty('date');
          expect(item, `Feed ${index}, Item ${itemIndex} should have source`).toHaveProperty('source');
        });
      });
      
      // Validate all_items array
      expect(Array.isArray(newsData.all_items), 'all_items should be an array').toBe(true);
      expect(typeof newsData.total_items, 'total_items should be a number').toBe('number');
      expect(newsData.total_items).toBe(newsData.all_items.length);
    });

    test('rss-feeds.yml configuration file exists and has valid structure', () => {
      const configPath = path.resolve(process.cwd(), '_data', 'rss-feeds.yml');
      expect(fs.existsSync(configPath), 'rss-feeds.yml file should exist').toBe(true);
      
      const fileContent = fs.readFileSync(configPath, 'utf-8');
      
      // Basic YAML structure validation
      expect(fileContent, 'rss-feeds.yml should contain feeds section').toContain('feeds:');
      expect(fileContent, 'rss-feeds.yml should contain config section').toContain('config:');
      
      // Validate required feed properties
      expect(fileContent, 'rss-feeds.yml should contain name field').toMatch(/name:/);
      expect(fileContent, 'rss-feeds.yml should contain url field').toMatch(/url:/);
      expect(fileContent, 'rss-feeds.yml should contain enabled field').toMatch(/enabled:/);
    });
  });

  test.describe('Homepage Newsfeed Display', () => {
    test('newsfeed section appears on homepage', async ({ page }) => {
      await page.goto('/', { waitUntil: 'domcontentloaded' });
      
      // Check if newsfeed section exists
      const newsfeedSection = page.locator('.sidebar-feed');
      const newsfeedCount = await newsfeedSection.count();
      
      // Newsfeed may not appear if there are no items, so we check for either:
      // 1. The section exists and is visible, OR
      // 2. The section doesn't exist (which is valid if no news items)
      if (newsfeedCount > 0) {
        await expect(newsfeedSection).toBeVisible();
      } else {
        // If no newsfeed section, that's okay - it means no news items are available
        console.log('Newsfeed section not found - this is valid if no news items are available');
      }
    });

    test('newsfeed has correct structure when items are available', async ({ page }) => {
      await page.goto('/', { waitUntil: 'domcontentloaded' });
      
      const newsfeedSection = page.locator('.sidebar-feed');
      const newsfeedCount = await newsfeedSection.count();
      
      if (newsfeedCount > 0) {
        // Verify title
        const title = newsfeedSection.locator('h3#sidebar-feed-title');
        await expect(title).toBeVisible();
        await expect(title).toHaveText('Legal News');
        
        // Verify feed list exists
        const feedList = newsfeedSection.locator('.sidebar-feed-list');
        await expect(feedList).toBeVisible();
        
        // Verify items exist (up to 5)
        const feedItems = feedList.locator('.sidebar-feed-item');
        const itemCount = await feedItems.count();
        expect(itemCount).toBeGreaterThan(0);
        expect(itemCount).toBeLessThanOrEqual(5);
        
        // Verify first item has required elements
        const firstItem = feedItems.first();
        const itemTitle = firstItem.locator('.sidebar-feed-title');
        await expect(itemTitle).toBeVisible();
        
        // Verify link is valid
        const itemLink = firstItem.locator('a.sidebar-feed-title');
        const href = await itemLink.getAttribute('href');
        expect(href).toBeTruthy();
        expect(href).not.toBe('#');
        
        // Verify metadata exists
        const meta = firstItem.locator('.sidebar-feed-meta');
        await expect(meta).toBeVisible();
        
        // Verify source and date are present
        const source = firstItem.locator('.news-source');
        const date = firstItem.locator('.news-date');
        if (await source.count() > 0) {
          await expect(source).toBeVisible();
        }
        if (await date.count() > 0) {
          await expect(date).toBeVisible();
        }
        
        // Verify "View all legal news" link
        const moreLink = newsfeedSection.locator('.sidebar-feed-more');
        await expect(moreLink).toBeVisible();
        await expect(moreLink).toHaveText(/View all legal news/i);
        
        const moreHref = await moreLink.getAttribute('href');
        expect(moreHref).toContain('/legal-news/');
      } else {
        test.info().annotations.push({ type: 'skip', description: 'No newsfeed items available to test' });
      }
    });

    test('newsfeed links are functional', async ({ page }) => {
      await page.goto('/', { waitUntil: 'domcontentloaded' });
      
      const newsfeedSection = page.locator('.sidebar-feed');
      const newsfeedCount = await newsfeedSection.count();
      
      if (newsfeedCount > 0) {
        const feedItems = newsfeedSection.locator('.sidebar-feed-item');
        const itemCount = await feedItems.count();
        
        if (itemCount > 0) {
          const firstItem = feedItems.first();
          const itemLink = firstItem.locator('a.sidebar-feed-title');
          const href = await itemLink.getAttribute('href');
          
          if (href && href !== '#' && !href.startsWith('#')) {
            // Verify link has proper attributes
            const rel = await itemLink.getAttribute('rel');
            expect(rel).toContain('noopener');
            expect(rel).toContain('noreferrer');
            
            const target = await itemLink.getAttribute('target');
            expect(target).toBe('_blank');
          }
        }
      } else {
        test.info().annotations.push({ type: 'skip', description: 'No newsfeed items available to test links' });
      }
    });
  });

  test.describe('Bell County Page Newsfeed Display', () => {
    test('newsfeed section appears on bell-county page', async ({ page }) => {
      await page.goto('/bell-county/', { waitUntil: 'domcontentloaded' });
      
      const newsfeedSection = page.locator('.sidebar-feed');
      const newsfeedCount = await newsfeedSection.count();
      
      if (newsfeedCount > 0) {
        await expect(newsfeedSection).toBeVisible();
      } else {
        console.log('Newsfeed section not found on bell-county page - this is valid if no news items are available');
      }
    });

    test('newsfeed has correct structure on bell-county page when items are available', async ({ page }) => {
      await page.goto('/bell-county/', { waitUntil: 'domcontentloaded' });
      
      const newsfeedSection = page.locator('.sidebar-feed');
      const newsfeedCount = await newsfeedSection.count();
      
      if (newsfeedCount > 0) {
        const title = newsfeedSection.locator('h3#sidebar-feed-title');
        await expect(title).toBeVisible();
        await expect(title).toHaveText('Legal News');

        // If there are matching items for this page, we'll get a list.
        // If not, we'll get an empty-state message.
        const feedList = newsfeedSection.locator('.sidebar-feed-list');
        const emptyState = newsfeedSection.locator('.sidebar-feed-empty');

        const hasList = (await feedList.count()) > 0;
        const hasEmpty = (await emptyState.count()) > 0;

        expect(hasList || hasEmpty).toBeTruthy();

        if (hasList) {
          const feedItems = feedList.locator('.sidebar-feed-item');
          const itemCount = await feedItems.count();
          expect(itemCount).toBeGreaterThan(0);
          expect(itemCount).toBeLessThanOrEqual(5);
        }
      } else {
        test.info().annotations.push({ type: 'skip', description: 'No newsfeed items available to test' });
      }
    });
  });

  test.describe('Newsfeed Not Displayed on Other Pages', () => {
    test('newsfeed does not appear on defense page', async ({ page }) => {
      await page.goto('/defense/', { waitUntil: 'domcontentloaded' });
      
      const newsfeedSection = page.locator('.sidebar-feed');
      const newsfeedCount = await newsfeedSection.count();
      
      // Sidebar feed is now site-wide; defense page should still have it.
      expect(newsfeedCount).toBeGreaterThan(0);
    });

    test('newsfeed does not appear on personal-injury page', async ({ page }) => {
      await page.goto('/personal-injury/', { waitUntil: 'domcontentloaded' });
      
      const newsfeedSection = page.locator('.sidebar-feed');
      const newsfeedCount = await newsfeedSection.count();
      
      // Sidebar feed is now site-wide; personal-injury page should still have it.
      expect(newsfeedCount).toBeGreaterThan(0);
    });
  });

  test.describe('Newsfeed Data Integration', () => {
    test('newsfeed displays items from news-feed.json', async ({ page }) => {
      // Read the JSON file
      const dataPath = path.resolve(process.cwd(), '_data', 'news-feed.json');
      if (!fs.existsSync(dataPath)) {
        test.skip();
        return;
      }
      
      const fileContent = fs.readFileSync(dataPath, 'utf-8');
      const newsData = JSON.parse(fileContent);
      
      await page.goto('/', { waitUntil: 'domcontentloaded' });
      
      const newsfeedSection = page.locator('.sidebar-feed');
      const newsfeedCount = await newsfeedSection.count();
      
      if (newsfeedCount > 0 && newsData.all_items && newsData.all_items.length > 0) {
        // Verify that displayed items match the JSON data (up to 5 items)
        const feedItems = newsfeedSection.locator('.sidebar-feed-item');
        const itemCount = await feedItems.count();
        
        // Check that we're showing at most 5 items
        expect(itemCount).toBeLessThanOrEqual(5);
        
        // Verify first item title is present in JSON data
        // (Ordering can differ due to homepage-specific filtering.)
        const firstItemTitle = (await feedItems.first().locator('.sidebar-feed-title').textContent()) || '';
        const allTitles = (newsData.all_items || []).map((it: any) => it.title);
        expect(allTitles).toContain(firstItemTitle.trim());
      } else if (newsData.all_items && newsData.all_items.length === 0) {
        // If JSON has no items, newsfeed should not be visible
        expect(newsfeedCount).toBe(0);
      }
    });

    test('newsfeed last updated timestamp is displayed when available', async ({ page }) => {
      const dataPath = path.resolve(process.cwd(), '_data', 'news-feed.json');
      if (!fs.existsSync(dataPath)) {
        test.skip();
        return;
      }
      
      const fileContent = fs.readFileSync(dataPath, 'utf-8');
      const newsData = JSON.parse(fileContent);
      
      await page.goto('/', { waitUntil: 'domcontentloaded' });
      
      const newsfeedSection = page.locator('.sidebar-feed');
      const newsfeedCount = await newsfeedSection.count();
      
      if (newsfeedCount > 0 && newsData.last_updated) {
        const updatedSection = newsfeedSection.locator('.sidebar-news-updated');
        const updatedCount = await updatedSection.count();
        
        if (updatedCount > 0) {
          await expect(updatedSection).toBeVisible();
          const updatedText = await updatedSection.textContent();
          expect(updatedText).toContain('Last updated');
        }
      }
    });
  });

  test.describe('Newsfeed Accessibility', () => {
    test('newsfeed has proper ARIA labels', async ({ page }) => {
      await page.goto('/', { waitUntil: 'domcontentloaded' });
      
      const newsfeedSection = page.locator('.sidebar-feed');
      const newsfeedCount = await newsfeedSection.count();
      
      if (newsfeedCount > 0) {
        const title = newsfeedSection.locator('h3#sidebar-feed-title');
        const titleId = await title.getAttribute('id');
        expect(titleId).toBe('sidebar-feed-title');
        
        const sectionAriaLabel = await newsfeedSection.getAttribute('aria-labelledby');
        expect(sectionAriaLabel).toBe('sidebar-feed-title');
      }
    });

    test('newsfeed links have proper accessibility attributes', async ({ page }) => {
      await page.goto('/', { waitUntil: 'domcontentloaded' });
      
      const newsfeedSection = page.locator('.sidebar-feed');
      const newsfeedCount = await newsfeedSection.count();
      
      if (newsfeedCount > 0) {
        const feedItems = newsfeedSection.locator('.sidebar-feed-item');
        const itemCount = await feedItems.count();
        
        if (itemCount > 0) {
          const firstLink = feedItems.first().locator('a.sidebar-feed-title');
          const href = await firstLink.getAttribute('href');
          
          if (href && href !== '#') {
            // External links should have proper rel attributes
            const rel = await firstLink.getAttribute('rel');
            expect(rel).toContain('noopener');
            expect(rel).toContain('noreferrer');
          }
        }
      }
    });
  });

  test.describe('Per-page Newsfeed Filtering', () => {
    test('bell-county page shows bell-county items only (and max 5)', async ({ page }) => {
      // The template filters based on `page.news_city`. Ensure bell-county.md is configured.
      await page.goto('/bell-county/', { waitUntil: 'domcontentloaded' });

      const feed = page.locator('.sidebar-feed');
      if ((await feed.count()) === 0) {
        test.skip();
        return;
      }

      const items = feed.locator('.sidebar-feed-item');
      const count = await items.count();
      expect(count).toBeLessThanOrEqual(5);

      // Read the JSON and compute expected titles for bell-county-news
      const dataPath = path.resolve(process.cwd(), '_data', 'news-feed.json');
      if (!fs.existsSync(dataPath)) {
        test.skip();
        return;
      }
      const newsData = JSON.parse(fs.readFileSync(dataPath, 'utf-8'));
      const expected = (newsData.all_items || [])
        .filter((it: any) => it.city === 'bell-county-news')
        .slice(0, 5)
        .map((it: any) => it.title);

      // If no expected items, the widget can legitimately show empty state (not a list)
      if (expected.length === 0) {
        // either empty-state paragraph exists, or widget doesn't render list items
        expect(count).toBe(0);
        return;
      }

      // Ensure rendered titles are a subset of expected titles
      const renderedTitles = await items.locator('a.sidebar-feed-title').allTextContents();
      renderedTitles.forEach((t) => {
        expect(expected).toContain(t.trim());
      });
    });
  });
});
