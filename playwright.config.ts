import { defineConfig } from '@playwright/test';

const baseURL = process.env.PLAYWRIGHT_BASE_URL || 'https://legalluminary.com';

export default defineConfig({
  testDir: './test_cases',
  timeout: 30_000,
  expect: {
    timeout: 10_000
  },
  use: {
    baseURL,
    trace: 'on-first-retry'
  },
  reporter: [['list']]
});
