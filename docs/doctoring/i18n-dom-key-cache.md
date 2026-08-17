# i18n DOM-key cache boundary

## Decision

The static homepage reads each stable `data-i18n` translation key into an
application-owned cache the first time translated nodes are needed. It also
stores each stable `data-lang` value with its language control. Later language
changes reuse those values rather than reading the same custom attributes again.

```text
static DOM discovery
  -> bounded node/key pairs
  -> repeated language projection
  -> text and aria-pressed updates
```

The cached values are descriptive page data, not authorization or executable
instructions. The design assumes the static site does not mutate `data-i18n` or
`data-lang` after initialization. A future dynamic component system must either
invalidate the cache or establish a different ownership contract.

## Standards and performance claim boundary

The HTML Standard defines `data-*` custom attributes and `dataset`, which returns
a `DOMStringMap` associated with the element. The DOM Standard defines
`Element.getAttribute()` as an attribute lookup returning the first matching
value or `null`.

Neither standard promises that `dataset` or `getAttribute()` is faster, nor does
it define browser allocation, proxy, layout, paint, or main-thread cost. This
change therefore claims only the code-observable result: after initial cache
construction, subsequent language changes do not invoke those `data-*` reads in
the tested path. Browser-level latency, memory, and rendering impact remain
measurement questions for representative deployed engines and devices.

## Verification

The Node harness executes the actual `i18n.js` source with controlled DOM-like
objects and performs English -> Korean -> English transitions. It verifies:

- bounded `data-i18n` and `data-lang` read counts;
- Korean text differs from English;
- English text is restored after the round trip; and
- the final `aria-pressed` values identify English.

This harness is deterministic semantic evidence. It is not a real-browser
benchmark, accessibility-tree assessment, layout/paint trace, or compatibility
claim for every browser.

## Rollback

If dynamic mutation or browser evidence shows stale-key behavior, revert to
live attribute reads or introduce explicit cache invalidation. Preserve the
round-trip text and ARIA regressions during rollback, and do not retain an
unmeasured absolute performance claim.

## References

WHATWG. (2026). *HTML Standard: Common microsyntaxes, custom data attributes,
and `dataset`*. https://html.spec.whatwg.org/multipage/dom.html

WHATWG. (2026). *DOM Standard: `Element.getAttribute()`*.
https://dom.spec.whatwg.org/
