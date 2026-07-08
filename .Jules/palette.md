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

## 2026-07-08 - [접근성] prefers-reduced-motion 설정 지원
**Learning:** 시스템에서 애니메이션 축소 옵션을 켠 사용자에게도 스무스 스크롤링과 페이드 전환 효과가 불쾌감을 줄 수 있음을 확인했습니다.
**Action:** 사용자 시스템 설정에 맞춰 CSS의 `scroll-behavior`와 `transition-duration`을 비활성화하는 `@media (prefers-reduced-motion: reduce)` 쿼리를 전역으로 추가하도록 개선해야 합니다.
