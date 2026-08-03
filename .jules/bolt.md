## 2024-06-20 - Unnecessary initial DOM updates for default language
**Learning:** The simple static i18n implementation runs `node.textContent = dict[node.dataset.i18n]` for every translatable node on the initial script load, even when the HTML is already written in the target language (Korean). This creates unnecessary layout/paint operations and blocking time on the main thread for elements that don't need text changes.
**Action:** Always check if the current value matches the desired value before updating the DOM (`node.textContent !== newText`), and add early exits when setting state to the same value to avoid redundant DOM traversal and writes.
## 2024-06-27 - 초기 언어 로드 시 불필요한 DOM 탐색 제거
**Learning:** 초기 로드 시 요청된 언어가 HTML의 기본 언어(ko)와 동일한 경우, 모든 DOM 텍스트 노드를 탐색하고 치환하는 불필요한 작업을 생략하면 성능이 향상됨을 확인했습니다.
**Action:** `isInitialDefault` 조건을 추가하여 초기 로드 시 불필요한 DOM 순회 코드가 실행되지 않도록 개선했습니다.

## 2026-07-05 - content-visibility와 scrollbar jumping 방지
**Learning:** 긴 단일 페이지(static site)에서 `content-visibility: auto`를 사용하여 오프스크린 섹션의 렌더링을 최적화할 때, `contain-intrinsic-size`를 함께 지정하지 않으면 스크롤바가 튀거나 레이아웃 시프트가 발생할 수 있습니다.
**Action:** 항상 길이 기반 폴백(예: `contain-intrinsic-size: 600px;`)을 선행하고, 브라우저가 실제 높이를 기억할 수 있도록 `auto` 키워드를 포함한 속성을 설정합니다. 섹션별 실제 높이에 맞춰 크기를 조정합니다.

## 2026-07-10 - Remove unnecessary DOMPurify for performance
**Learning:** 애플리케이션이 `textContent`와 같은 안전한 DOM API만 사용하고 `innerHTML` 등의 위험한 싱크를 사용하지 않는다면 DOMPurify와 같은 라이브러리를 통해 Trusted Types 정책을 생성할 필요가 없음.
**Action:** 불필요한 번들 다운로드 및 스크립트 실행을 방지하기 위해 사용하지 않는 라이브러리를 식별하고 제거할 것.
## 2026-08-03 - Above-the-fold SVG 이미지의 decoding="async" 제거로 LCP 최적화
**Learning:** `decoding="async"`는 이미지 디코딩을 메인 스레드에서 분리하여 렌더링 블로킹을 방지하지만, 크리티컬 렌더링 패스에 있는 above-the-fold 이미지(특히 작은 인라인 SVG나 LCP 히어로 이미지)에 적용할 경우 오히려 페인트 타이밍이 늦어져 LCP(Largest Contentful Paint) 성능을 저하시킬 수 있습니다.
**Action:** `loading="lazy"`가 적용된 off-screen 이미지에만 `decoding="async"`를 유지하고, 초기 렌더링에 필수적인 above-the-fold SVG 요소(헤더 로고, 히어로 이미지)에서는 `decoding="async"`를 제거하고 성능을 모니터링합니다.
