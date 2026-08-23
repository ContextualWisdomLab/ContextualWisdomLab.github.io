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

## 2026-08-05 - Separate image fetch and decode hints
**Learning:** The HTML Standard defines `decoding` as a preference hint whose missing-value default is `auto`; it does not guarantee a particular main-thread or background-thread execution path. `fetchpriority` independently influences fetch priority. Removing `decoding="async"` must therefore not be described as a guaranteed LCP improvement.
**Action:** Let eager first-viewport images use the user agent's `auto` decode strategy, retain `decoding="async"` for explicitly lazy images, and require non-vacuous tests for eager, lazy, and single high-priority LCP-candidate sets. Record the evidence and measurement limits in `docs/doctoring/image-rendering-hints.md`.

## 2026-08-08 - 애니메이션 성능을 위해 top/left 대신 transform 사용
**Learning:** 이 skip-link 전환을 `top`에서 `transform`으로 바꾸면 애니메이션 중 레이아웃 재계산을 피하는 데 유리합니다. 개발자 도구에서 이 전환의 Layout 이벤트가 관찰되지 않았지만, 브라우저·장치별 GPU 가속이나 메인 스레드 비용 0ms를 보장하지는 않습니다.
**Action:** 레이아웃 속성 대신 `transform` 전환을 우선 검토하고, 성능 효과는 브라우저별 측정으로 확인하며 절대적인 GPU·비용 보장으로 기록하지 않습니다.

## 2026-08-23 - DOM dataset 접근자 오버헤드 회피
**Learning:** `dataset` 속성은 프록시 객체를 통해 접근하므로 `getAttribute`보다 훨씬 느립니다. 언어 변경 시 많은 요소의 `dataset.i18n`을 읽으면 메인 스레드 블로킹 시간이 증가합니다.
**Action:** DOM 노드를 처음 순회할 때 `getAttribute`를 사용해 키를 추출하여 배열 객체 형태로 캐싱하면 언어 전환 시 DOM 속성 읽기 비용을 완전히 제거할 수 있습니다.
