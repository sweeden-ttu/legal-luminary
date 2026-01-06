import { test, expect } from '@playwright/test';

const paths = [
  '/',
  '/about/',
  '/archive/',
  '/resources/',
  '/news-feeds/'
];

test.describe('Jekyll site smoke', () => {
  for (const path of paths) {
    test(`loads ${path}`, async ({ page }) => {
      const response = await page.goto(path, { waitUntil: 'domcontentloaded' });
      expect(response, `No response for ${path}`).not.toBeNull();
      expect(response!.status(), `Bad status for ${path}`).toBeLessThan(400);

      await expect(page).toHaveTitle(/.+/);

      // Basic sanity: page should have visible body content.
      await expect(page.locator('body')).toContainText(/\S+/);

      // If the layout uses a <main> element, ensure it has something.
      const main = page.locator('main');
      if (await main.count()) {
        await expect(main).toContainText(/\S+/);
      }
    });
  }

  test('homepage has navigation links', async ({ page }) => {
    await page.goto('/', { waitUntil: 'domcontentloaded' });

    // These are intentionally loose checks to avoid coupling to a specific layout.
    // We just want to ensure there is some sort of nav/header and that links exist.
    const linkCount = await page.locator('a').count();
    expect(linkCount).toBeGreaterThan(3);
  });

  test('sitemap.xml contains recent posts', async ({ page }) => {
    // 1. Fetch the sitemap
    const response = await page.goto('/sitemap.xml');
    expect(response?.status()).toBe(200);
    
    // 2. Get XML text
    const xml = await response?.text();
    expect(xml).toContain('<urlset');
    
    // 3. Verify it has at least one post URL (assuming some recent posts exist)
    // We look for post URL patterns - this site uses /_posts/ format
    expect(xml).toMatch(/<loc>.*\/_posts\/20\d\d-\d\d-\d\d-.*<\/loc>/);
  });

  test('verify latest post loads', async ({ page }) => {
    // 1. Go to archive or home to find a post link
    await page.goto('/archive/', { waitUntil: 'domcontentloaded' });
    
    // 2. Find the first post link (usually in a list)
    const postLink = page.locator('.post-list a').first();
    const count = await postLink.count();
    
    if (count > 0) {
      const href = await postLink.getAttribute('href');
      console.log(`Checking post: ${href}`);
      
      // 3. Navigate to the post
      const response = await page.goto(href!);
      expect(response?.status()).toBeLessThan(400);
      
      // 4. Ensure post title is visible
      await expect(page.locator('h1.post-title')).toBeVisible();
    } else {
      console.warn('No posts found on /archive/ to test!');
    }
  });
});
