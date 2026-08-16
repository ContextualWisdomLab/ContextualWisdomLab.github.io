# External-link new-tab context

## Status

Active homepage accessibility evidence. This document does not claim whole-site WCAG conformance or screen-reader interoperability.

## Decision

Links that deliberately open a new tab keep three coordinated cues:

1. A visible `↗` from CSS. Ordinary links use `::after`. Project-card titles keep `::after` as the empty stretch overlay and place `↗` on `::before`.
2. A document-tree warning in a `.visually-hidden` child: Korean source text `새 탭에서 열림`, translated by `data-i18n="a11y.opensNewTab"` to `opens in a new tab`.
3. The visible label stays in a sibling node. `data-i18n` must not sit on the same `<a>` as the warning child, because `setLanguage()` writes `textContent` and would destroy the child.

The accessible name is the concatenation of visible text and the hidden warning. That keeps WCAG 2.2 Success Criterion 2.5.3 (Label in Name) without a synthesized `aria-label`.

Every current target-blank link must also retain both `noopener` and `noreferrer`. Static tests parse the real homepage and fail if a target-blank link loses opener isolation, visible text, or the HTML warning.

## Rationale

Opening a new window or tab is a change of context. W3C Technique G201 is the design goal for warning users in advance. This homepage now puts the warning in the HTML tree so first paint and no-JavaScript users receive it in the source language. CSS `↗` remains a sighted-user enhancement and is not treated as the only warning, which avoids claiming that Failure F87 is solved by generated content.

Technique C7 hides a portion of the text with CSS clipping rather than `display: none` or `visibility: hidden`, so the warning stays in the accessibility tree (World Wide Web Consortium, n.d.-a).

## Failure and rollback

If a future external link has no visible text besides the warning, the static test fails. Add a visible label at the link-content boundary; do not invent an `aria-label`.

Rollback removes the `.visually-hidden` children, the `a11y.opensNewTab` locale strings, this note, and the focused tests together. Do not restore parent-level `data-i18n` on those anchors without also removing the warning child.

## References

World Wide Web Consortium. (2023). *Web Content Accessibility Guidelines (WCAG) 2.2*. https://www.w3.org/TR/WCAG22/

World Wide Web Consortium. (n.d.). *G201: Giving users advanced warning when opening a new window*. WAI techniques for WCAG 2.2. Retrieved August 16, 2026, from https://www.w3.org/WAI/WCAG22/Techniques/general/G201

World Wide Web Consortium. (n.d.-a). *C7: Using CSS to hide a portion of the text*. WAI techniques for WCAG 2.2. Retrieved August 16, 2026, from https://www.w3.org/WAI/WCAG22/Techniques/css/C7

World Wide Web Consortium. (n.d.). *Understanding Success Criterion 2.5.3: Label in Name*. Web Accessibility Initiative. Retrieved August 16, 2026, from https://www.w3.org/WAI/WCAG22/Understanding/label-in-name

World Wide Web Consortium. (n.d.). *F87: Failure of Success Criterion 1.3.1 due to inserting non-decorative content by using :before and :after pseudo-elements*. WAI techniques for WCAG 2.2. Retrieved August 16, 2026, from https://www.w3.org/WAI/WCAG22/Techniques/failures/F87
