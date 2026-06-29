## 2024-06-20 - Unnecessary initial DOM updates for default language
**Learning:** The simple static i18n implementation runs `node.textContent = dict[node.dataset.i18n]` for every translatable node on the initial script load, even when the HTML is already written in the target language (Korean). This creates unnecessary layout/paint operations and blocking time on the main thread for elements that don't need text changes.
**Action:** Always check if the current value matches the desired value before updating the DOM (`node.textContent !== newText`), and add early exits when setting state to the same value to avoid redundant DOM traversal and writes.

## 2024-06-26 - 초기 언어 로드를 위한 빠른 경로(Fast path) 적용
**Learning:** 초기 페이지 로드 시 요청된 기본 언어가 이미 렌더링된 HTML과 완벽하게 일치함에도 불구하고, 정적 i18n 구현이 무거운 DOM 쿼리(`querySelectorAll`)와 트리 순회를 실행하고 있었습니다.
**Action:** 초기 상태가 이미 요청된 상태와 일치하는지 항상 확인해야 합니다. `currentLang`이 null이고 `document.documentElement.lang`이 요청된 언어와 일치할 때 DOM 쿼리를 우회하도록 `setLanguage`에 빠른 종료(early exit)를 추가했으며, 실제 언어 전환이 일어날 때만 노드를 쿼리하도록 지연(lazy) 처리했습니다.
