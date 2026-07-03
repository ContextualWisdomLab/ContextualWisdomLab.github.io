## 2024-06-20 - Unnecessary initial DOM updates for default language
**Learning:** The simple static i18n implementation runs `node.textContent = dict[node.dataset.i18n]` for every translatable node on the initial script load, even when the HTML is already written in the target language (Korean). This creates unnecessary layout/paint operations and blocking time on the main thread for elements that don't need text changes.
**Action:** Always check if the current value matches the desired value before updating the DOM (`node.textContent !== newText`), and add early exits when setting state to the same value to avoid redundant DOM traversal and writes.
## 2024-06-27 - 초기 언어 로드 시 불필요한 DOM 탐색 제거
**Learning:** 초기 로드 시 요청된 언어가 HTML의 기본 언어(ko)와 동일한 경우, 모든 DOM 텍스트 노드를 탐색하고 치환하는 불필요한 작업을 생략하면 성능이 향상됨을 확인했습니다.
**Action:** `isInitialDefault` 조건을 추가하여 초기 로드 시 불필요한 DOM 순회 코드가 실행되지 않도록 개선했습니다.
## 2024-07-03 - Off-screen rendering optimization with content-visibility
**Learning:** 뷰포트 바깥의 긴 섹션을 렌더링하면 렌더링 성능이 저하될 수 있습니다. `content-visibility: auto`를 사용하면 오프스크린 요소의 렌더링을 지연시킬 수 있으나, `contain-intrinsic-size`를 설정하지 않으면 스크롤바 점핑과 레이아웃 시프트가 발생합니다.
**Action:** 항상 `content-visibility: auto`를 사용할 때 `contain-intrinsic-size`를 함께 사용하고 구버전 브라우저 호환성을 위해 fallback 크기를 지정합니다 (예: `contain-intrinsic-size: 600px;` 이후 `contain-intrinsic-size: auto 600px;` 적용).
