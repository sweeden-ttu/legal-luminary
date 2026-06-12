import { test, expect } from '@playwright/test';

test('skip to content link is present and functional on homepage', async ({ page }) => {
  await page.goto('http://127.0.0.1:4000/');

  const skipLink = page.locator('a.skip-link');
  await expect(skipLink).toBeAttached();
  await expect(skipLink).toHaveAttribute('href', '#main-content');
  await expect(skipLink).toHaveText('Skip to content');

  // Check if it's the first focusable element
  await page.keyboard.press('Tab');
  await expect(skipLink).toBeFocused();

  // Check if main content is focused after clicking
  await skipLink.click();
  const mainContent = page.locator('#main-content');
  await expect(mainContent).toBeFocused();
});
