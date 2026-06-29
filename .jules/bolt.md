## 2024-06-20 - Unnecessary initial DOM updates for default language
**Learning:** The simple static i18n implementation runs `node.textContent = dict[node.dataset.i18n]` for every translatable node on the initial script load, even when the HTML is already written in the target language (Korean). This creates unnecessary layout/paint operations and blocking time on the main thread for elements that don't need text changes.
**Action:** Always check if the current value matches the desired value before updating the DOM (`node.textContent !== newText`), and add early exits when setting state to the same value to avoid redundant DOM traversal and writes.

## 2026-06-24 - Initializing state cache with actual DOM state
**Learning:** If a state cache (e.g., `let currentLang = null;`) doesn't reflect the actual DOM state (`document.documentElement.lang`), early returns in state setters (e.g., `if (currentLang === lang) return;`) will fail on initial load. This causes redundant DOM traversals and layout/paint operations when setting up the initial state, even when the UI already matches the requested state.
**Action:** Always initialize local state caches using the actual values already present in the DOM (`let currentLang = document.documentElement.lang;`) so that early returns correctly skip redundant updates on initial render.
