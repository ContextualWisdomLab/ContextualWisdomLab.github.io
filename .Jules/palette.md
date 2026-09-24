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

## 2024-09-10 - [언어 전환 버튼 툴팁 추가]
**Learning:** 다국어 지원 사이트에서 버튼의 title(툴팁)과 같은 접근성 요소도 하드코딩하지 않고 번역 시스템(data-i18n-title)과 연동해야 동적 언어 전환 시 사용자 경험이 깨지지 않음을 확인했습니다.
**Action:** 앞으로 사용자에게 노출되는 모든 UI 텍스트(aria-label, title 등)는 정적인 HTML에 고정하지 않고 다국어 스크립트가 관리하도록 구조를 확장하겠습니다.
## 2026-09-07 - 외부 링크에 다국어 지원 title 속성 추가
**Learning:** 외부 링크(`target="_blank"`)에 새 창에서 열린다는 사실을 안내하는 `title` 속성이 누락되어 스크린 리더 사용자의 접근성이 떨어지는 문제를 발견했습니다. 또한 정적인 `title` 속성을 사용할 경우 다국어 전환 시 반영되지 않는 문제가 있었습니다.
**Action:** 읽을 수 있는 텍스트가 포함된 `title`이나 `aria-label` 등의 접근성 속성을 추가할 때는 반드시 국제화 시스템과 연동(예: `data-i18n-title` 사용)하여 스크린 리더가 올바른 언어로 컨텍스트를 제공하도록 해야 합니다.

## 2026-08-22 - Add aria-labelledby to section landmarks
**Learning:** `<section>`은 접근성 이름이 있을 때만 `region` 랜드마크로 노출되고, 이름이 없으면 `generic`으로 매핑되어 화면 탐색 랜드마크 목록에 나타나지 않습니다. `id` 속성만으로는 부족합니다.
**Action:** `<section>`에는 고유한 `id`를 가진 내부 헤딩(`<h2>`)을 `aria-labelledby`로 참조시켜 접근성 이름을 부여합니다. 회귀 테스트가 참조 대상 id의 실재 여부와 아이디가 있는 모든 섹션의 레이블링을 검증합니다.
