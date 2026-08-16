# External-link new-tab context

## Status

Active PR design/accessibility evidence for homepage PR #172. This document does not claim whole-site WCAG conformance or screen-reader interoperability.

## Decision

Links that deliberately open a new tab keep a visible `↗` cue from the design layer. After `i18n.js` runs, the language layer adds a localized accessible-name suffix to every `a[target="_blank"]` link. The suffix is `새 탭에서 열림` in Korean and `opens in a new tab` in English.

The accessible name is derived from the link's **current visible text after translation** and then extended with the new-tab context. This preserves the visible label as a contiguous part of the accessible name instead of replacing it with unrelated text.

Project cards already use `h3 a::after` as an empty stretch overlay so the whole card is the hit target. The general `a[target="_blank"]::after` marker is more specific than that overlay, so project titles restore the empty overlay with `.project-grid h3 a[target="_blank"]::after` and place their `↗` on `::before`.

Every current target-blank link must also retain both `noopener` and `noreferrer`. The executable static-site test parses the real homepage HTML and fails if any target-blank link loses opener isolation or visible link text. A second contract binds both locale messages, the complete target-blank selector, and the visible-text-derived accessible-name construction. CSS tests fail if the new-tab glyph reuses the project-card overlay.

## Rationale

Opening a new window or tab is a change of context. W3C Technique G201 is the design goal for warning users in advance. This homepage implements a **progressive enhancement**, not a claim that G201 or WCAG Failure F87 are fully satisfied:

- Sighted users with CSS get the `↗` glyph.
- Assistive technology after `i18n.js` runs gets the localized `aria-label`.
- The HTML source still has no visually hidden warning text, so users without JavaScript or with CSS disabled do not receive a document-tree warning. Parent links that use `data-i18n` replace `textContent` and would destroy a child warning span, so the language layer keeps the warning in `aria-label` instead of HTML.

WCAG 2.2 Success Criterion 2.5.3 requires the visible label text to be included in the accessible name for labeled user-interface components. Building the accessible name from `link.textContent.trim()` after language translation preserves that relationship for both Korean and English and for raw reference URLs when JavaScript runs.

## Failure and rollback

If a future external link has no visible text, the language adapter deliberately skips synthesizing an accessible label rather than inventing one. The static test independently requires non-empty visible text for all current target-blank links, so such a regression must be fixed at the link content boundary.

Rollback removes the two locale strings, the target-blank node cache and accessible-name update, this doctoring note, and its focused test together. The visual arrow may remain independently useful, but it must not again be described as sufficient assistive-technology evidence.

## References

World Wide Web Consortium. (2023). *Web Content Accessibility Guidelines (WCAG) 2.2*. https://www.w3.org/TR/WCAG22/

World Wide Web Consortium. (n.d.). *G201: Giving users advanced warning when opening a new window*. WAI techniques for WCAG 2.2. Retrieved August 16, 2026, from https://www.w3.org/WAI/WCAG22/Techniques/general/G201

World Wide Web Consortium. (n.d.). *Understanding Success Criterion 2.5.3: Label in Name*. Web Accessibility Initiative. Retrieved August 16, 2026, from https://www.w3.org/WAI/WCAG22/Understanding/label-in-name

World Wide Web Consortium. (n.d.). *F87: Failure of Success Criterion 1.3.1 due to inserting non-decorative content by using :before and :after pseudo-elements*. WAI techniques for WCAG 2.2. Retrieved August 16, 2026, from https://www.w3.org/WAI/WCAG22/Techniques/failures/F87
