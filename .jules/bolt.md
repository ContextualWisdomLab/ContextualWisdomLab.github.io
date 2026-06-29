## 2024-06-20 - Unnecessary initial DOM updates for default language
**Learning:** The simple static i18n implementation runs `node.textContent = dict[node.dataset.i18n]` for every translatable node on the initial script load, even when the HTML is already written in the target language (Korean). This creates unnecessary layout/paint operations and blocking time on the main thread for elements that don't need text changes.
**Action:** Always check if the current value matches the desired value before updating the DOM (`node.textContent !== newText`), and add early exits when setting state to the same value to avoid redundant DOM traversal and writes.

## 2024-06-23 - Lazy initializing DOM queries to improve Time To Interactive (TTI)
**Learning:** Even if `textContent` modifications are gated by early returns, eagerly executing `querySelectorAll` for all translatable strings on a static page block the main thread and degrade TTI, especially on initial loads when the language requested matches the server-rendered default.
**Action:** Always check if the current state requires an update *before* executing expensive initial DOM queries, initializing state variables silently when the desired language aligns with the document's initial `lang` attribute.
