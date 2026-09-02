## 2026-09-02 - [External Link Accessibility]
**Learning:** Hardcoding `title` attributes on links in a localized site breaks dynamic language switching. The site uses a custom `i18n.js` script that manages text via data attributes.
**Action:** Always extend the custom i18n system (e.g., adding `data-i18n-title`) instead of relying on static HTML attributes when adding user-visible accessibility metadata.
