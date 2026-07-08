## 2024-06-20 - Unnecessary initial DOM updates for default language
**Learning:** The simple static i18n implementation runs `node.textContent = dict[node.dataset.i18n]` for every translatable node on the initial script load, even when the HTML is already written in the target language (Korean). This creates unnecessary layout/paint operations and blocking time on the main thread for elements that don't need text changes.
**Action:** Always check if the current value matches the desired value before updating the DOM (`node.textContent !== newText`), and add early exits when setting state to the same value to avoid redundant DOM traversal and writes.
## 2024-06-27 - 초기 언어 로드 시 불필요한 DOM 탐색 제거
**Learning:** 초기 로드 시 요청된 언어가 HTML의 기본 언어(ko)와 동일한 경우, 모든 DOM 텍스트 노드를 탐색하고 치환하는 불필요한 작업을 생략하면 성능이 향상됨을 확인했습니다.
**Action:** `isInitialDefault` 조건을 추가하여 초기 로드 시 불필요한 DOM 순회 코드가 실행되지 않도록 개선했습니다.
## 2026-07-05 - content-visibility와 scrollbar jumping 방지
**Learning:** 긴 단일 페이지(static site)에서 `content-visibility: auto`를 사용하여 오프스크린 섹션의 렌더링을 최적화할 때, `contain-intrinsic-size`를 함께 지정하지 않으면 스크롤바가 튀거나 레이아웃 시프트가 발생할 수 있습니다.
**Action:** 항상 길이 기반 폴백(예: `contain-intrinsic-size: 600px;`)을 선행하고, 브라우저가 실제 높이를 기억할 수 있도록 `auto` 키워드를 포함한 속성을 설정합니다. 섹션별 실제 높이에 맞춰 크기를 조정합니다.
## 2024-05-24 - 이미지 디코딩 최적화를 통한 메인 스레드 차단 방지
**Learning:** 이미지 로드 시 기본적으로 메인 스레드에서 디코딩을 수행하기 때문에 메인 스레드 차단 및 UI jank가 발생할 수 있습니다.
**Action:** 오프스크린 이미지나 레이지 로드 이미지 등에 `decoding="async"` 속성을 추가하여 백그라운드 스레드에서 디코딩 작업을 처리하도록 함으로써 초기 페이지 로드 성능을 개선합니다.
## 2024-05-24 - LCP 최적화 및 SVG 이미지 처리 패턴
**Learning:** LCP(가장 큰 콘텐츠 풀 페인트) 대상 이미지에 `decoding="async"` 속성을 부여하면 브라우저가 디코딩을 백그라운드로 넘기게 되어 초기 페인팅이 지연되는 안티패턴이 될 수 있습니다. 또한, SVG 이미지는 래스터 이미지처럼 디코딩되는 것이 아니라 파싱되므로 `decoding="async"`의 효과가 거의 없음을 확인했습니다.
**Action:** LCP 이미지에는 `fetchpriority="high"`를 유지하되 `decoding="async"`는 사용하지 않아 빠르게 동기적으로 그려지도록 하며, 다른 요소들에서 SVG를 사용할 때는 이 사실을 인지하고 무분별한 속성 적용을 지양합니다.
