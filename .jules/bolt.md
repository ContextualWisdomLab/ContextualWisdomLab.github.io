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

## 2024-07-18 - SVG 및 LCP 이미지의 decoding 속성 최적화
**Learning:** SVG 이미지는 디코딩(decoding) 과정이 아니라 파싱(parsing) 과정을 거치므로 `decoding="async"` 속성이 무의미하며, LCP(Largest Contentful Paint) 이미지에 `fetchpriority="high"`와 함께 사용하면 중요 렌더링이 지연될 수 있는 안티 패턴이 됨을 학습함.
**Action:** 성능 최적화 시 `decoding="async"`는 오프스크린(off-screen) 또는 지연 로딩(lazy-loaded)되는 래스터 이미지에만 적용하고, SVG 이미지나 핵심 렌더링을 담당하는 LCP 이미지에는 적용하지 않도록 주의할 것.
