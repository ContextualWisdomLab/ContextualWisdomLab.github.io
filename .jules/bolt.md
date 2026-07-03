## 2024-06-20 - Unnecessary initial DOM updates for default language
**Learning:** The simple static i18n implementation runs `node.textContent = dict[node.dataset.i18n]` for every translatable node on the initial script load, even when the HTML is already written in the target language (Korean). This creates unnecessary layout/paint operations and blocking time on the main thread for elements that don't need text changes.
**Action:** Always check if the current value matches the desired value before updating the DOM (`node.textContent !== newText`), and add early exits when setting state to the same value to avoid redundant DOM traversal and writes.
## 2024-06-27 - 초기 언어 로드 시 불필요한 DOM 탐색 제거
**Learning:** 초기 로드 시 요청된 언어가 HTML의 기본 언어(ko)와 동일한 경우, 모든 DOM 텍스트 노드를 탐색하고 치환하는 불필요한 작업을 생략하면 성능이 향상됨을 확인했습니다.
**Action:** `isInitialDefault` 조건을 추가하여 초기 로드 시 불필요한 DOM 순회 코드가 실행되지 않도록 개선했습니다.
## 2024-05-24 - content-visibility 최적화
**Learning:** 긴 랜딩 페이지에 `content-visibility: auto`를 적용하면 화면 밖 섹션의 렌더링을 지연시켜 초기 Layout 및 Paint 시간을 크게 줄일 수 있습니다. 단, 스크롤바 점프를 방지하기 위해 반드시 `contain-intrinsic-size`를 함께 사용해야 합니다.
**Action:** 스크롤을 내려야 보이는 독립적이고 무거운 섹션이 많은 페이지에는 항상 `content-visibility` 적용을 고려해야 합니다.
