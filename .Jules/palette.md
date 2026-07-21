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

## 2024-05-30 - 카드 컴포넌트의 클릭 가능 영역 확장
**Learning:** 그리드나 리스트 형식의 카드 컴포넌트에서 링크 텍스트에만 클릭 이벤트를 바인딩하면, 사용자가 정확하게 텍스트를 겨냥하여 클릭해야 하므로 사용성이 저하됨을 확인했습니다.
**Action:** CSS 가상 요소 `::after`와 `inset: 0` 속성을 활용해 텍스트 링크의 클릭 가능 영역을 카드(article) 전체로 확장하여, 사용자가 카드 영역 어디든 편하게 클릭할 수 있도록 접근성과 사용성을 크게 개선합니다.
