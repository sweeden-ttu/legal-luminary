import { test, expect } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';

/**
 * Example test that downloads and caches all JavaScript files
 * Run with: npx playwright test tests/cache-js-files.spec.ts
 */

test.describe('JavaScript File Caching and Downloading', () => {
  const downloadDir = path.join(__dirname, '../downloaded-js');
  
  test.beforeAll(() => {
    // Create download directory
    if (!fs.existsSync(downloadDir)) {
      fs.mkdirSync(downloadDir, { recursive: true });
    }
  });

  test('download and cache all JS files from m3u8downloader page', async ({ page, context }) => {
    const baseURL = process.env.PLAYWRIGHT_BASE_URL || 'http://127.0.0.1:4000';
    const jsFiles: Array<{ url: string; filename: string; size: number; cached: boolean }> = [];
    
    // Track which files are served from cache
    const cacheMap = new Map<string, boolean>();
    
    // Intercept responses to check cache status
    page.on('response', async (response) => {
      const request = response.request();
      const url = response.url();
      
      if (request.resourceType() === 'script') {
        // Check if response was from cache (304 Not Modified or served from cache)
        const fromCache = response.status() === 304 || 
                         response.headers()['x-from-cache'] === 'true' ||
                         response.headers()['x-cache']?.includes('HIT');
        
        cacheMap.set(url, fromCache);
        
        if (response.status() === 200) {
          try {
            const buffer = await response.body();
            const urlObj = new URL(url);
            const filename = urlObj.pathname.split('/').pop() || 'script.js';
            
            // Sanitize filename
            const safeFilename = filename.replace(/[^a-zA-Z0-9.-]/g, '_');
            const filepath = path.join(downloadDir, safeFilename);
            
            // Save file
            fs.writeFileSync(filepath, buffer);
            
            jsFiles.push({
              url,
              filename: safeFilename,
              size: buffer.length,
              cached: fromCache
            });
            
            console.log(`Downloaded: ${safeFilename} (${(buffer.length / 1024).toFixed(2)} KB) ${fromCache ? '[CACHED]' : '[FRESH]'}`);
          } catch (error) {
            console.error(`Failed to save ${url}:`, error);
          }
        }
      }
    });
    
    // Navigate to the page
    await page.goto(`${baseURL}/m3u8downloader`, { waitUntil: 'networkidle' });
    
    // Wait for all scripts to load
    await page.waitForLoadState('networkidle');
    
    // Also check for dynamically loaded modules
    await page.waitForTimeout(2000);
    
    console.log(`\nTotal JS files downloaded: ${jsFiles.length}`);
    console.log(`Cached: ${jsFiles.filter(f => f.cached).length}`);
    console.log(`Fresh: ${jsFiles.filter(f => !f.cached).length}`);
    
    // Verify MODULES are loaded
    const modulesDefined = await page.evaluate(() => {
      return typeof window !== 'undefined' && (window as any).MODULES !== undefined;
    });
    
    expect(modulesDefined).toBe(true);
    
    // List all downloaded files
    if (jsFiles.length > 0) {
      console.log('\nDownloaded JS files:');
      jsFiles.forEach(file => {
        console.log(`  - ${file.filename} (${(file.size / 1024).toFixed(2)} KB) ${file.cached ? '[CACHED]' : ''}`);
      });
    }
  });

  test('cache JS files per site/origin', async ({ context }) => {
    const siteCache = new Map<string, Map<string, { buffer: Buffer; headers: Record<string, string> }>>();
    
    // Set up route interception for caching
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
        const cached = originCache.get(pathname)!;
        await route.fulfill({
          body: cached.buffer,
          headers: cached.headers,
          contentType: 'application/javascript',
          status: 200
        });
        console.log(`Served from cache: ${pathname} (origin: ${origin})`);
        return;
      }
      
      // Fetch and cache
      const response = await route.fetch();
      const buffer = await response.body();
      const headers = response.headers();
      
      originCache.set(pathname, { buffer, headers });
      console.log(`Cached: ${pathname} (origin: ${origin})`);
      
      await route.fulfill({ response, body: buffer });
    });
    
    const page = await context.newPage();
    const baseURL = process.env.PLAYWRIGHT_BASE_URL || 'http://127.0.0.1:4000';
    
    // First visit - files will be downloaded and cached
    await page.goto(`${baseURL}/m3u8downloader`, { waitUntil: 'networkidle' });
    
    // Second visit - files should be served from cache
    await page.goto(`${baseURL}/m3u8downloader`, { waitUntil: 'networkidle' });
    
    // Verify cache was used
    const cacheStats = Array.from(siteCache.entries()).map(([origin, files]) => ({
      origin,
      fileCount: files.size
    }));
    
    console.log('\nCache statistics per origin:');
    cacheStats.forEach(stat => {
      console.log(`  ${stat.origin}: ${stat.fileCount} files cached`);
    });
  });

  test('list all JS modules loaded on page', async ({ page }) => {
    const baseURL = process.env.PLAYWRIGHT_BASE_URL || 'http://127.0.0.1:4000';
    const loadedModules: string[] = [];
    
    // Track script loads
    page.on('response', async (response) => {
      if (response.request().resourceType() === 'script' && response.status() === 200) {
        loadedModules.push(response.url());
      }
    });
    
    await page.goto(`${baseURL}/m3u8downloader`, { waitUntil: 'networkidle' });
    
    // Also check for ES6 modules defined in the page
    const moduleInfo = await page.evaluate(() => {
      const modules = (window as any).MODULES || {};
      const loadedModules = (window as any).loadedModules || {};
      
      return {
        definedModules: Object.keys(modules),
        loadedModules: Object.keys(loadedModules),
        modulePaths: modules
      };
    });
    
    console.log('\nModule Information:');
    console.log('Defined modules:', moduleInfo.definedModules);
    console.log('Loaded modules:', moduleInfo.loadedModules);
    console.log('\nAll JS files loaded:', loadedModules.length);
    loadedModules.forEach(url => console.log(`  - ${url}`));
    
    expect(moduleInfo.definedModules.length).toBeGreaterThan(0);
  });
});

