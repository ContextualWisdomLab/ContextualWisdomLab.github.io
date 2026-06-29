## 2024-06-20 - Unnecessary initial DOM updates for default language
**Learning:** The simple static i18n implementation runs `node.textContent = dict[node.dataset.i18n]` for every translatable node on the initial script load, even when the HTML is already written in the target language (Korean). This creates unnecessary layout/paint operations and blocking time on the main thread for elements that don't need text changes.
**Action:** Always check if the current value matches the desired value before updating the DOM (`node.textContent !== newText`), and add early exits when setting state to the same value to avoid redundant DOM traversal and writes.

## 2024-06-29 - 초기 로딩 시 불필요한 DOM 쿼리 생략
**Learning:** HTML이 이미 기본 언어로 렌더링된 상태에서 초기화할 때, 변경할 필요가 없는 140개 이상의 노드를 모두 탐색하는 것은 메인 스레드를 낭비하는 작업이었습니다.
**Action:** 현재 상태가 서버가 렌더링한 초기 DOM 언어와 일치할 때는 무거운 텍스트 노드 탐색(querySelectorAll)을 조건부로 완전히 건너뛰도록 구현하여 성능을 개선합니다.
