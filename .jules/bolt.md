## 2024-06-20 - Unnecessary initial DOM updates for default language
**Learning:** The simple static i18n implementation runs `node.textContent = dict[node.dataset.i18n]` for every translatable node on the initial script load, even when the HTML is already written in the target language (Korean). This creates unnecessary layout/paint operations and blocking time on the main thread for elements that don't need text changes.
**Action:** Always check if the current value matches the desired value before updating the DOM (`node.textContent !== newText`), and add early exits when setting state to the same value to avoid redundant DOM traversal and writes.
## 2024-06-25 - Prevent redundant initial DOM updates
**Learning:** Initializing the app triggers an unnecessary `querySelectorAll` and textContent update loop for the default language, causing layout thrashing even when the HTML is already rendered correctly.
**Action:** Add early exit logic to skip expensive DOM lookups and writes if the requested language matches the pre-rendered default language, while ensuring essential state (like `aria-pressed`) still initializes.
