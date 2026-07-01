## 2024-06-20 - Unnecessary initial DOM updates for default language
**Learning:** The simple static i18n implementation runs `node.textContent = dict[node.dataset.i18n]` for every translatable node on the initial script load, even when the HTML is already written in the target language (Korean). This creates unnecessary layout/paint operations and blocking time on the main thread for elements that don't need text changes.
**Action:** Always check if the current value matches the desired value before updating the DOM (`node.textContent !== newText`), and add early exits when setting state to the same value to avoid redundant DOM traversal and writes.
## 2024-06-27 - 초기 언어 로드 시 불필요한 DOM 탐색 제거
**Learning:** 초기 로드 시 요청된 언어가 HTML의 기본 언어(ko)와 동일한 경우, 모든 DOM 텍스트 노드를 탐색하고 치환하는 불필요한 작업을 생략하면 성능이 향상됨을 확인했습니다.
**Action:** `isInitialDefault` 조건을 추가하여 초기 로드 시 불필요한 DOM 순회 코드가 실행되지 않도록 개선했습니다.
## 2024-06-27 - content-visibility를 이용한 초기 렌더링 성능 최적화
**Learning:** 초기 로드 시 화면 바깥에 위치한 요소들(.section, .site-footer)로 인해 초기 Layout 시간과 Style Recalculation 시간이 불필요하게 소요됨을 확인했습니다.
**Action:** `content-visibility: auto` 속성을 적용해 브라우저가 화면 바깥 요소의 렌더링을 지연시키도록 하고, `contain-intrinsic-size`를 지정하여 스크롤 점프를 방지하도록 최적화합니다.
