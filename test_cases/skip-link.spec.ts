import { test, expect } from '@playwright/test';

test('Skip to Content link is present and works', async ({ page }) => {
  await page.goto('http://127.0.0.1:4000/');

  const skipLink = page.locator('a.skip-link');
  await expect(skipLink).toBeAttached();
  await expect(skipLink).toHaveAttribute('href', '#main-content');
  await expect(skipLink).toHaveText('Skip to content');

  // Verify it's initially hidden (off-screen)
  const boundingBox = await skipLink.boundingBox();
  expect(boundingBox.y).toBeLessThan(0);

  // Focus the link and verify it's visible
  await page.keyboard.press('Tab');
  await page.waitForTimeout(300); // Wait for transition
  const visibleBoundingBox = await skipLink.boundingBox();
  expect(visibleBoundingBox.y).toBeGreaterThanOrEqual(0);

  // Click the link and verify focus moves to main content
  await skipLink.click();
  const mainContent = page.locator('#main-content');
  await expect(mainContent).toBeFocused();
});
