## 2025-05-15 - [Accessibility Gaps in Templates]
**Learning:** Even when accessibility features (like skip-to-content links) are partially implemented in CSS or JS, they can be missing from the actual HTML templates, leading to a "phantom" feature that doesn't actually benefit users.
**Action:** Always verify that accessibility hooks defined in stylesheets are correctly anchored in the core layout templates.

## 2025-05-15 - [Generic Link Labels]
**Learning:** Repetitive "Read More" links without context are a common accessibility hurdle for screen reader users.
**Action:** Use `aria-label` to provide specific context to generic call-to-action links when they appear in lists or grids.

## 2026-06-19 - [Keyboard Accessible Dropdowns]
**Learning:** Hover-based dropdown menus are inaccessible to keyboard users unless explicitly handled with `:focus-within` or JavaScript.
**Action:** Use `.parent:focus-within .submenu { display: block; }` to ensure submenus reveal themselves when a keyboard user tabs into the parent menu item.

## 2026-06-19 - [YAML Validation in Jekyll]
**Learning:** Jekyll's YAML parser fails when unquoted strings in front matter contain colons (e.g., "Divorce: Children"), as it interprets them as nested mappings.
**Action:** Always wrap data strings containing colons in double quotes in `.md` collection files to ensure build stability.
