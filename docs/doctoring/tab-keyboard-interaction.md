# Tab keyboard interaction decision

## Scope

This decision applies to the standalone KRDS component gallery in
`components/index.html` and `components/krds-gallery.js`. The gallery uses
native `button` elements with ARIA `tab`, `tablist`, and `tabpanel` roles.

## Implemented contract

- The `tablist` has an accessible name.
- Exactly one selected tab participates in the page tab sequence with
  `tabindex="0"`; inactive tabs use `tabindex="-1"`.
- `ArrowLeft` and `ArrowRight` move through tabs with wraparound.
- `Home` moves to the first tab and `End` moves to the last tab.
- Focus movement automatically activates the corresponding panel because the
  local panel content is already available and activation has no network or
  rendering latency.
- Selection, roving `tabindex`, panel visibility, and focus are updated as one
  state transition.
- Each panel is keyboard reachable with `tabindex="0"` because the example
  panels contain plain text rather than a naturally focusable first element.

## Missing-target and diagnostic boundary

Every tab in a tab set is resolved to its `aria-controls` target before any
selection, `tabindex`, panel-visibility, or focus mutation begins. This is a
set-level integrity check rather than only a requested-target check: if the
requested panel exists but a sibling tab points to a missing panel, activation
still fails atomically and preserves the previous selected/visible state. This
keeps the DOM relationships that assistive technology relies on from drifting
into a partially updated tab set.

If any controlled panel is absent, a constant diagnostic category is emitted.
The untrusted or malformed `aria-controls` value is not copied into console
output. The WAI-ARIA Tabs Pattern requires each tab to control its associated
`tabpanel`; resolving the whole local set before mutation makes that relationship
an executable precondition for this static gallery rather than a best-effort
postcondition.

Tag-removal controls likewise verify that `closest(".krds-tag")` returns a
container before mutation. A missing container emits a constant diagnostic and
leaves the page unchanged; a valid container is removed once. These checks are
reliability boundaries for a static demonstration page, not authorization or a
claim that arbitrary hostile DOM mutation is a supported product mode.

Dependency-free Node harnesses execute the actual gallery script with a missing
requested panel, a valid requested panel plus a missing sibling panel, a missing
tag container, and a valid tag container. They prove no partial tab-state
mutation, no focus movement, exact static warnings, no raw identifier transport,
and preserved valid removal behavior.

A separate executable keyboard harness invokes the actual registered `keydown`
listeners rather than inspecting source strings. It proves `ArrowLeft` and
`ArrowRight` wrap between the first and last tabs, `Home` and `End` select the
respective boundary tab, every handled key calls `preventDefault()`, focus moves
to the activated tab, `aria-selected` and roving `tabindex` remain synchronized,
and only the activated panel is visible. An unhandled `Tab` event remains outside
the scripted navigation contract and is not prevented.

## Limitations and validation

The Python regression suite validates the markup relationships, the single
roving tab stop, the accessible tab-list name, panel reachability, and invokes
the dependency-free Node interaction harnesses for keyboard transitions and
missing-target behavior. These harnesses exercise the checked-in production
JavaScript and DOM-facing contracts, but they are not a substitute for a real
browser accessibility tree or assistive-technology interoperability test.
Representative browser and screen-reader combinations still require manual or
future browser-automation validation before treating the gallery as a complete
conformance demonstration.

Automatic activation is appropriate only while panel display remains
instantaneous. If a future panel requires remote loading or expensive
rendering, use manual activation with `Enter` and `Space` instead so arrow-key
navigation remains responsive.

## References

World Wide Web Consortium. (2023, June 6). *Accessible Rich Internet
Applications (WAI-ARIA) 1.2*. https://www.w3.org/TR/wai-aria-1.2/

World Wide Web Consortium. (n.d.). *Tabs pattern*. WAI-ARIA Authoring Practices
Guide. Retrieved August 17, 2026, from
https://www.w3.org/WAI/ARIA/apg/patterns/tabs/

World Wide Web Consortium. (n.d.). *Example of tabs with automatic activation*.
WAI-ARIA Authoring Practices Guide. Retrieved August 17, 2026, from
https://www.w3.org/WAI/ARIA/apg/patterns/tabs/examples/tabs-automatic/

World Wide Web Consortium. (n.d.). *Developing a keyboard interface*. WAI-ARIA
Authoring Practices Guide. Retrieved August 17, 2026, from
https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/

WHATWG. (2026). *DOM Standard: Element attribute lookup and tree traversal*.
https://dom.spec.whatwg.org/
