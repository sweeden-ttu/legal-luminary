# ES6 Modules in Jekyll - Setup Guide

This guide explains how to add ES6 modules to your Jekyll site, specifically for the M3U8 downloader functionality.

## Directory Structure

ES6 modules should be placed in the `assets/js/modules/` directory:

```
assets/
  js/
    modules/
      options.js
      hls.es.js
      iso-boxer.js
      saveAs.js
      hls-decrypter.js
      ffmpeg/
        index.js
        (other ffmpeg files)
```

## How Jekyll Handles ES6 Modules

### 1. **Static Asset Serving**
- Files in the `assets/` directory are copied to `_site/assets/` during build
- Jekyll does NOT process JavaScript files (unlike HTML/Markdown)
- ES6 modules are served as-is with proper MIME types

### 2. **Path Resolution**
- Use Jekyll's `relative_url` filter for paths in templates
- Example: `{{ '/assets/js/modules/options.js' | relative_url }}`
- This ensures paths work correctly with `baseurl` configuration

### 3. **Module Syntax**
ES6 modules use `import`/`export` syntax:

**Example module (`options.js`):**
```javascript
// Export default
export default {
  downloadThreads: 4,
  autoSave: false,
  // ... other options
};

// Or named exports
export const DEFAULT_OPTIONS = { ... };
export function getOption(key) { ... }
```

**Using the module:**
```javascript
import options from './options.js';
// or
import { DEFAULT_OPTIONS, getOption } from './options.js';
```

## Module Paths in the Layout

The module paths are defined in `_layouts/m3u8downloader.html`:

```javascript
const MODULES = {
  "OPTIONS": "{{ '/assets/js/modules/options.js' | relative_url }}",
  "HLS": "{{ '/assets/js/modules/hls.es.js' | relative_url }}",
  // ... etc
};
```

Jekyll processes the `{{ }}` Liquid tags during build, generating the correct URLs.

## Adding New Modules

1. **Create the module file** in `assets/js/modules/`
2. **Add the path** to the `MODULES` object in `_layouts/m3u8downloader.html`
3. **Use ES6 export syntax** in your module
4. **Rebuild the site** - Jekyll will copy the file to `_site/assets/js/modules/`

## Module Loading

The module loader script in the layout:
- Defines all module paths
- Loads modules dynamically using `import()`
- Makes modules available globally via `window.loadedModules`
- Dispatches events when modules are ready

## Example: Creating a Simple Module

**File: `assets/js/modules/utils.js`**
```javascript
export function formatFileSize(bytes) {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

export function formatTime(seconds) {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const secs = Math.floor(seconds % 60);
  return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
}
```

**Add to MODULES:**
```javascript
"UTILS": "{{ '/assets/js/modules/utils.js' | relative_url }}"
```

**Use in your code:**
```javascript
const utils = await window.loadM3U8Module('UTILS');
const size = utils.formatFileSize(1024000); // "1000 KB"
```

## External Modules (CDN)

For modules hosted externally (like the FetchV workers), use full URLs:

```javascript
"HLS_WORKER": "https://fetchv.net/extensions/dist/modules/web-worker.js"
```

These are loaded directly without Jekyll processing.

## Troubleshooting

### Modules Not Loading

1. **Check file paths**: Verify files exist in `assets/js/modules/`
2. **Check browser console**: Look for 404 errors or CORS issues
3. **Verify MIME types**: Jekyll should serve `.js` files with `application/javascript`
4. **Check baseurl**: If using a baseurl, paths must account for it

### CORS Issues

- ES6 modules require proper CORS headers
- Local development: Use `jekyll serve` (serves with proper headers)
- Production: Ensure your server sends correct CORS headers

### Module Not Found Errors

- Ensure file extensions match (`.js`, `.mjs`)
- Check that paths use Jekyll's `relative_url` filter
- Verify files are in the correct directory structure

## Development Workflow

1. **Create/edit modules** in `assets/js/modules/`
2. **Run Jekyll**: `bundle exec jekyll serve`
3. **Test in browser**: Check console for module loading
4. **Build for production**: `bundle exec jekyll build`

## Best Practices

1. **Use named exports** for better tree-shaking
2. **Keep modules focused** - one responsibility per module
3. **Document exports** - use JSDoc comments
4. **Handle errors** - modules should fail gracefully
5. **Test modules** - write unit tests for complex logic

## References

- [Jekyll Assets Documentation](https://jekyllrb.com/docs/structure/)
- [ES6 Modules MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules)
- [Jekyll Liquid Filters](https://jekyllrb.com/docs/liquid/filters/)

