## 2024-06-19 - Added ARIA roles to generic div containers
**Learning:** Found a recurring pattern in the app where generic `div` elements were being used with `aria-label` but lacked a specific role (e.g., `.language-switch`, `.hero-actions`). This makes screen readers announce them poorly since they don't know what kind of component the label applies to.
**Action:** When adding `aria-label` to group interactive elements in generic containers (`div` or `span`), always remember to add `role="group"` (or another appropriate role) to give screen readers proper context.

## 2024-06-21 - Added skip-to-content link
**Learning:** Found a missing skip-to-content link, which is a key accessibility feature to help keyboard and screen reader users bypass navigation. Additionally learned that giving `<main>` `tabindex="-1"` and removing its outline when `:focus-visible` ensures proper focus handling after clicking the skip link without disruptive visual outlines.
**Action:** Always include a skip-to-content link near the start of the `body` and manage target focus appropriately.
