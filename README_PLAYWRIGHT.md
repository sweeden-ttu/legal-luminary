# Playwright (E2E) against `jekyll serve`

These smoke tests verify that the site builds and key pages load **via the Jekyll dev server**.

## Prereqs
- Ruby/Bundler (repo already uses Bundler)
- Node (for Playwright)

## Install
```bash
bundle install
npm install
npx playwright install
```

## Run
Start Jekyll + run tests (auto-start/stop server):
```bash
npm run e2e
```

Or run manually:
```bash
bundle exec jekyll serve --host 127.0.0.1 --port 4000 --baseurl ""
PLAYWRIGHT_BASE_URL=http://127.0.0.1:4000 npm run test:e2e
```

## Notes
- Base URL defaults to `http://127.0.0.1:4000`.
- Tests live in `tests/`.
