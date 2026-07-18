## 2026-07-18 - Card Component Hit Areas
**Learning:** Making entire cards clickable by extending a nested link's `::after` pseudo-element to `inset: 0` dramatically improves the hit area (Fitts's Law) without requiring JavaScript or invalid HTML (like wrapping block elements in `<a>`).
**Action:** Apply this pattern to all list/grid cards that have a single primary action link.
