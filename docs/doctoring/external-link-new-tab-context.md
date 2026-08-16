# External-link new-tab context

## Status

Active PR design/accessibility evidence for homepage PR #172. This document does not claim whole-site WCAG conformance or screen-reader interoperability.

## Decision

Links that deliberately open a new tab keep the visible `↗` cue from the design layer, while the language layer adds a localized accessible-name suffix to every `a[target="_blank"]` link. The suffix is `새 탭에서 열림` in Korean and `opens in a new tab` in English.

The accessible name is derived from the link's **current visible text after translation** and then extended with the new-tab context. This preserves the visible label as a contiguous part of the accessible name instead of replacing it with unrelated text. The same selector is used for all target-blank links, including navigation, calls to action, references, project links, and the footer.

Every current target-blank link must also retain both `noopener` and `noreferrer`. The executable static-site test parses the real homepage HTML and fails if any target-blank link loses opener isolation or visible link text. A second contract binds both locale messages, the complete target-blank selector, and the visible-text-derived accessible-name construction.

## Rationale

Opening a new window or tab is a change of context. W3C Technique G201 recommends warning users in advance when a link opens a new window. CSS-generated content remains a useful visual cue, but it is not treated as the sole semantic contract. The localized accessible name supplies the programmatic warning while the visible arrow remains a sighted-user cue.

WCAG 2.2 Success Criterion 2.5.3 requires the visible label text to be included in the accessible name for labeled user-interface components. Building the accessible name from `link.textContent.trim()` after language translation preserves that relationship for both Korean and English and for raw reference URLs.

## Failure and rollback

If a future external link has no visible text, the language adapter deliberately skips synthesizing an accessible label rather than inventing one. The static test independently requires non-empty visible text for all current target-blank links, so such a regression must be fixed at the link content boundary.

Rollback removes the two locale strings, the target-blank node cache and accessible-name update, this doctoring note, and its focused test together. The visual arrow may remain independently useful, but it must not again be described as sufficient assistive-technology evidence.

## References

World Wide Web Consortium. (2023). *Web Content Accessibility Guidelines (WCAG) 2.2*. https://www.w3.org/TR/WCAG22/

World Wide Web Consortium. (n.d.). *G201: Giving users advanced warning when opening a new window*. WAI techniques for WCAG 2.2. Retrieved August 16, 2026, from https://www.w3.org/WAI/WCAG22/Techniques/general/G201

World Wide Web Consortium. (n.d.). *Understanding Success Criterion 2.5.3: Label in Name*. Web Accessibility Initiative. Retrieved August 16, 2026, from https://www.w3.org/WAI/WCAG22/Understanding/label-in-name
