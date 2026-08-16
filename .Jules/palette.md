## 2024-06-19 - Added ARIA roles to generic div containers
**Learning:** Found a recurring pattern in the app where generic `div` elements were being used with `aria-label` but lacked a specific role (e.g., `.language-switch`, `.hero-actions`). This makes screen readers announce them poorly since they don't know what kind of component the label applies to.
**Action:** When adding `aria-label` to group interactive elements in generic containers (`div` or `span`), always remember to add `role="group"` (or another appropriate role) to give screen readers proper context.

## 2024-06-21 - Added skip-to-content link
**Learning:** Found a missing skip-to-content link, which is a key accessibility feature to help keyboard and screen reader users bypass navigation. Additionally learned that giving `<main>` `tabindex="-1"` and removing its outline when `:focus-visible` ensures proper focus handling after clicking the skip link without disruptive visual outlines.
**Action:** Always include a skip-to-content link near the start of the `body` and manage target focus appropriately.

## 2026-06-25 - Fix Header Overlap
**Learning:** When using a sticky header, clicking anchor links can cause the target element to scroll under the header, hindering the user experience.
**Action:** Use `scroll-padding-top` on the `html` element with the height of the sticky header to ensure anchor links scroll to a position just below the header.

## 2024-06-25 - Improve Color Contrast
**Learning:** Found that using `--gold` for text on white or light backgrounds (like `--paper`) fails WCAG AA contrast standards, making the text difficult to read for some users.
**Action:** Avoid using `--gold` on light backgrounds. Instead, use alternatives with better contrast like `--teal`. Retain `--gold` for dark backgrounds (like `--ink`) where it provides excellent contrast.

## 2024-07-10 - prefers-reduced-motion 지원 추가
**Learning:** 시스템 레벨에서 애니메이션 줄이기(prefers-reduced-motion)를 설정한 사용자를 위해 과도한 애니메이션과 부드러운 스크롤을 비활성화하는 것이 필요합니다. 이때 `0s` 대신 `0.01ms`를 사용하여 `transitionend`와 같은 브라우저 이벤트가 정상적으로 발생하도록 해야 자바스크립트 콜백이 멈추는(hanging) 문제를 방지할 수 있습니다.
**Action:** 항상 `styles.css` 하단에 `prefers-reduced-motion: reduce` 미디어 쿼리를 추가하여 모든 요소의 `animation-duration`과 `transition-duration`을 `0.01ms`로 설정하고 `scroll-behavior: auto`를 적용합니다.

## 2024-07-15 - Expand clickable area of project cards
**Learning:** Using an anchor tag to wrap an entire card (block-level element) can result in verbose and confusing screen reader output. However, restricting the clickable area to just the title makes the UI harder to interact with (violating Fitts's Law).
**Action:** Apply `position: relative` to the card container and use a `::after` pseudo-element with `position: absolute; inset: 0;` on the title's anchor tag. This expands the clickable area to the whole card while keeping semantic and accessible HTML structure.
## 2026-08-16 - 텍스트 선택 영역 및 외부 링크 시각적 개선
**Learning:** 텍스트 드래그 시 기본 파란색 선택 영역은 브랜드 정체성을 저해하며, 새 창으로 열리는 링크에 대한 시각적 힌트 부재는 사용자의 탐색 맥락을 끊을 수 있습니다. `a[target="_blank"]::after`로 `↗`를 넣으면 프로젝트 카드가 이미 쓰는 빈 `::after` 히트 영역(`content: ""` + `inset: 0`)을 덮어 카드 전체가 아니라 글리프만 클릭 대상이 됩니다.
**Action:** `::selection`에 Teal/white를 적용합니다. 일반 `target="_blank"` 링크는 `::after`로 `↗`를 붙이고, 프로젝트 카드는 같은 `::after`를 빈 스트레치 오버레이로 되돌린 뒤 `::before`에 `↗`를 둡니다. 새 탭 안내는 JS `aria-label`로 제공하고, CSS 생성 콘텐츠만으로 G201/F87을 충족했다고 기록하지 않습니다.
