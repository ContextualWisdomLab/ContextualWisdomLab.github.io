## 2024-06-19 - Added ARIA roles to generic div containers
**Learning:** Found a recurring pattern in the app where generic `div` elements were being used with `aria-label` but lacked a specific role (e.g., `.language-switch`, `.hero-actions`). This makes screen readers announce them poorly since they don't know what kind of component the label applies to.
**Action:** When adding `aria-label` to group interactive elements in generic containers (`div` or `span`), always remember to add `role="group"` (or another appropriate role) to give screen readers proper context.

## 2024-06-21 - Added skip-to-content link
**Learning:** Found a missing skip-to-content link, which is a key accessibility feature to help keyboard and screen reader users bypass navigation. Additionally learned that giving `<main>` `tabindex="-1"` and removing its outline when `:focus-visible` ensures proper focus handling after clicking the skip link without disruptive visual outlines.
**Action:** Always include a skip-to-content link near the start of the `body` and manage target focus appropriately.

## 2024-06-24 - Anchor Link Scroll Padding
**Learning:** 스티키 헤더가 적용된 페이지에서 앵커 링크로 이동 시, 기본 스크롤 동작은 타겟 요소의 상단을 브라우저 상단에 맞추기 때문에 콘텐츠가 헤더에 가려지는 문제가 발생함을 확인했습니다.
**Action:** 스티키 헤더의 높이만큼 `html` 요소에 `scroll-padding-top` 속성을 추가하여 앵커 링크 이동 시에도 적절한 여백을 확보하고 접근성을 개선합니다.
