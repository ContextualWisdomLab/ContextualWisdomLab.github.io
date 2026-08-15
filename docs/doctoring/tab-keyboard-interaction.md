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

A requested tab is validated against its controlled panel before selection,
`tabindex`, visibility, or focus changes begin. If the target panel is absent,
the prior selected state remains intact and a constant diagnostic category is
emitted. The untrusted or malformed `aria-controls` value is not copied into
console output.

Tag-removal controls likewise verify that `closest(".krds-tag")` returns a
container before mutation. A missing container emits a constant diagnostic and
leaves the page unchanged; a valid container is removed once. These checks are
reliability boundaries for a static demonstration page, not authorization or a
claim that arbitrary hostile DOM mutation is a supported product mode.

A Node harness executes the actual gallery script with a missing target panel,
a missing tag container, and a valid tag container. It proves no partial tab
state mutation, no focus movement, exact static warnings, no raw identifier
transport, and preserved valid removal behavior.

## Limitations and validation

The Python regression suite validates the markup relationships, the single
roving tab stop, the accessible tab-list name, panel reachability, supported
keyboard transitions, and the missing-target runtime contract. Browser and
assistive-technology interoperability still requires manual validation on
representative browser and screen-reader combinations before treating the
gallery as a conformance demonstration.

Automatic activation is appropriate only while panel display remains
instantaneous. If a future panel requires remote loading or expensive
rendering, use manual activation with `Enter` and `Space` instead so arrow-key
navigation remains responsive.

## References

World Wide Web Consortium. (2023, June 6). *Accessible Rich Internet
Applications (WAI-ARIA) 1.2*. https://www.w3.org/TR/wai-aria-1.2/

World Wide Web Consortium. (n.d.). *Tabs pattern*. WAI-ARIA Authoring Practices
Guide. Retrieved August 15, 2026, from
https://www.w3.org/WAI/ARIA/apg/patterns/tabs/

World Wide Web Consortium. (n.d.). *Developing a keyboard interface*. WAI-ARIA
Authoring Practices Guide. Retrieved August 15, 2026, from
https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/

WHATWG. (2026). *DOM Standard: Element attribute lookup and tree traversal*.
https://dom.spec.whatwg.org/
