# Button active-feedback boundary

## Decision

The homepage supplements the browser's temporary `:active` state with a small,
bounded scale transform for ordinary call-to-action links styled as `.button`
and for the language-switch buttons. The short transition preserves the existing
`opacity` transition and adds `transform`; existing hover, focus-visible,
pressed-state, target-size, text, and click behavior remain separate contracts.

```text
pointer or equivalent activation
  -> browser matches :active
  -> bounded visual compression
  -> browser releases :active
```

The effect is feedback that an activation gesture is currently being applied.
It is not confirmation that navigation, storage, network work, or another
business action succeeded. Completion feedback must be owned by the action that
can observe completion.

## Accessibility and motion boundary

Selectors Level 4 defines `:active` as the activated state of a user-action
pseudo-class. The state can arise through different input modalities depending
on the user agent; this stylesheet does not assume mouse-only activation.
Keyboard focus remains visible through the repository's separate
`:focus-visible` rule, and the scale effect does not remove the native element,
accessible name, focus order, or pressed state.

The repository-wide `prefers-reduced-motion: reduce` block reduces transition
duration to `0.01ms`. The transform state may still be observable for the
instant of activation, but prolonged animation is not required. This supports
the user's reduced-motion preference without claiming that every vestibular,
vision, motor, or cognitive accessibility need is satisfied.

## Verification

Static regressions require:

- the exact reviewed `opacity` and `transform` transition on both control families;
- bounded active scales of `0.98` and `0.92`;
- the existing `:focus-visible` outline rule; and
- the global reduced-motion transition-duration override.

These checks prove source configuration, not rendered ergonomics. Representative
browser, touch, pointer, keyboard, zoom, forced-colors, and reduced-motion
validation remains necessary before a release-level usability or accessibility
claim. Any performance effect must be measured; use of `transform` alone does
not guarantee a frame rate, compositor path, or absence of main-thread work.

## Rollback

If rendered validation shows motion discomfort, accidental layout overlap, or
poor input feedback, remove the scale transition while preserving focus-visible,
hover, and semantic control behavior. Do not replace it with a success-shaped
message unless the corresponding action can truthfully observe completion.

## References

World Wide Web Consortium. (2026, January 22). *Selectors Level 4* (Working
Draft). https://www.w3.org/TR/selectors-4/

World Wide Web Consortium. (2026, February 19). *Media Queries Level 5* (Working
Draft). https://www.w3.org/TR/mediaqueries-5/
