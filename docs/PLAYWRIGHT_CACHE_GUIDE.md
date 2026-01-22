# Playwright JavaScript File Caching Guide

## How Playwright Handles Cache

### Default Behavior

1. **Browser Cache**: Playwright uses the browser's native HTTP cache (Chromium/Firefox/WebKit)
2. **Per Context**: Each browser context has its own isolated cache
3. **Per Site**: Cache is effectively per origin/domain within a context
4. **Automatic**: The browser automatically caches based on HTTP cache headers

### Cache Storage Location

- **Chromium**: `~/.cache/ms-playwright/chromium-<version>/Default/Cache/`
- **Firefox**: `~/.cache/ms-playwright/firefox-<version>/default/`
- **WebKit**: `~/.cache/ms-playwright/webkit-<version>/`

Cache is stored **per browser type and version**, not per site. However, the browser's cache mechanism ensures files are cached per origin/domain.

## Configuring Cache in Playwright

### Option 1: Use Browser Context with Cache Enabled (Default)

```typescript
import { test } from '@playwright/test';

test('test with cache', async ({ context }) => {
  // Cache is enabled by default
  const page = await context.newPage();
  await page.goto('https://legalluminary.com');
  // JS files are cached automatically
});
```

### Option 2: Disable Cache (For Testing)

```typescript
test('test without cache', async ({ context }) => {
  // Disable cache for fresh requests
  await context.route('**/*', route => {
    route.continue({ headers: { ...route.request().headers(), 'Cache-Control': 'no-cache' } });
  });
  
  const page = await context.newPage();
  await page.goto('https://legalluminary.com');
});
```

### Option 3: Custom Cache Interception

Intercept and cache JavaScript files manually:

```typescript
import { test } from '@playwright/test';

test('cache JS files manually', async ({ page, context }) => {
  const jsCache = new Map<string, { data: Buffer; headers: Record<string, string> }>();
  
  // Intercept JS file requests
  await context.route('**/*.js', async (route) => {
    const url = route.request().url();
    
    // Check cache
    if (jsCache.has(url)) {
      const cached = jsCache.get(url)!;
      await route.fulfill({
        body: cached.data,
        headers: cached.headers,
        status: 200
      });
      return;
    }
    
    // Fetch and cache
    const response = await route.fetch();
    const buffer = await response.body();
    jsCache.set(url, {
      data: buffer,
      headers: response.headers()
    });
    
    await route.fulfill({
      response,
      body: buffer
    });
  });
  
  await page.goto('https://legalluminary.com');
});
```

## Viewing Downloaded/Cached Files

### Method 1: Network Logging

```typescript
test('log all JS files', async ({ page }) => {
  const jsFiles: string[] = [];
  
  page.on('response', async (response) => {
    if (response.request().resourceType() === 'script') {
      const url = response.url();
      const status = response.status();
      jsFiles.push(`${status} ${url}`);
      
      // Optionally save the file
      if (status === 200) {
        const buffer = await response.body();
        const filename = url.split('/').pop() || 'script.js';
        // Save to disk if needed
      }
    }
  });
  
  await page.goto('https://legalluminary.com');
  console.log('JS files loaded:', jsFiles);
});
```

### Method 2: Download All JS Files

```typescript
test('download all JS files', async ({ page }) => {
  const fs = require('fs');
  const path = require('path');
  const downloadDir = './downloaded-js';
  
  if (!fs.existsSync(downloadDir)) {
    fs.mkdirSync(downloadDir, { recursive: true });
  }
  
  page.on('response', async (response) => {
    if (response.request().resourceType() === 'script' && response.status() === 200) {
      const url = response.url();
      const urlObj = new URL(url);
      const filename = urlObj.pathname.split('/').pop() || 'script.js';
      const filepath = path.join(downloadDir, filename);
      
      const buffer = await response.body();
      fs.writeFileSync(filepath, buffer);
      console.log(`Downloaded: ${filename} from ${url}`);
    }
  });
  
  await page.goto('https://legalluminary.com');
  await page.waitForLoadState('networkidle');
});
```

## Cache Per Site/Origin

While Playwright's cache is per browser context, you can organize cache by site:

```typescript
test('cache per site', async ({ context }) => {
  const siteCache = new Map<string, Map<string, Buffer>>();
  
  await context.route('**/*.js', async (route) => {
    const url = new URL(route.request().url());
    const origin = url.origin;
    const pathname = url.pathname;
    
    // Get or create cache for this origin
    if (!siteCache.has(origin)) {
      siteCache.set(origin, new Map());
    }
    const originCache = siteCache.get(origin)!;
    
    // Check cache
    if (originCache.has(pathname)) {
      await route.fulfill({
        body: originCache.get(pathname)!,
        contentType: 'application/javascript'
      });
      return;
    }
    
    // Fetch and cache
    const response = await route.fetch();
    const buffer = await response.body();
    originCache.set(pathname, buffer);
    
    await route.fulfill({ response, body: buffer });
  });
  
  const page = await context.newPage();
  await page.goto('https://legalluminary.com');
});
```

## Checking What's Cached

### View Cache in Browser DevTools

```typescript
test('inspect cache', async ({ page }) => {
  await page.goto('https://legalluminary.com');
  
  // Open DevTools (if not headless)
  // Or use CDP to inspect cache
  const client = await page.context().newCDPSession(page);
  const cacheData = await client.send('Network.getResponseBody', {
    requestId: '...' // Get from network events
  });
});
```

### List All Cached Resources

```typescript
test('list cached resources', async ({ page }) => {
  const cachedResources: Array<{url: string; type: string}> = [];
  
  page.on('response', async (response) => {
    const request = response.request();
    const url = response.url();
    const fromCache = response.fromServiceWorker() || 
                      (await response.headerValue('x-from-cache')) === 'true';
    
    if (fromCache || response.status() === 304) {
      cachedResources.push({
        url,
        type: request.resourceType()
      });
    }
  });
  
  await page.goto('https://legalluminary.com');
  await page.waitForLoadState('networkidle');
  
  console.log('Cached resources:', cachedResources.filter(r => r.type === 'script'));
});
```

## Best Practices

1. **Use Default Cache**: Let the browser handle caching automatically
2. **Clear Cache When Needed**: Use `context.clearCookies()` and navigate with `cache: false` option
3. **Monitor Cache**: Log responses to see what's being cached
4. **Test Cache Behavior**: Verify your site works with cached and fresh resources

## Clearing Cache

```typescript
test('clear cache', async ({ context }) => {
  // Clear browser cache
  const pages = context.pages();
  for (const page of pages) {
    await page.evaluate(() => {
      if ('caches' in window) {
        caches.keys().then(keys => {
          keys.forEach(key => caches.delete(key));
        });
      }
    });
  }
  
  // Or create new context (fresh cache)
  const newContext = await context.browser()!.newContext();
});
```

## References

- [Playwright Browser Contexts](https://playwright.dev/docs/browser-contexts)
- [Playwright Network Interception](https://playwright.dev/docs/network)
- [Playwright CDP Session](https://playwright.dev/docs/api/class-cdpsession)

