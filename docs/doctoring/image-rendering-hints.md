# Image rendering hints

## Decision

The homepage separates image loading, fetch priority, and decode strategy instead of treating them as a single performance switch.

- The single declared Largest Contentful Paint candidate remains eagerly discoverable and uses `fetchpriority="high"`.
- Eager first-viewport images omit the `decoding` attribute. The HTML Standard defines the missing value as the `auto` state, allowing the user agent to choose its decode behavior.
- Explicitly lazy-loaded, below-the-fold images retain `decoding="async"`.
- Automated tests prove that the eager, lazy, and high-priority image sets are non-empty before checking their contracts, preventing vacuous passes.

## Rationale

The `decoding` attribute is a preference hint, not a guarantee that a particular thread or rendering path will be used. Omitting it does not mean synchronous decoding; it selects the standards-defined `auto` state. Likewise, `fetchpriority` affects fetch priority and is independent from image decoding. Therefore this change does not claim a universal LCP improvement from removing `decoding="async"` alone.

The contract is intentionally measurable:

1. Static regression tests verify markup invariants.
2. Deployment performance should be evaluated separately with repeated field or laboratory measurements, including LCP distributions and representative device/network conditions.
3. Any future change to preload, lazy loading, or fetch priority must preserve a single explicit LCP candidate unless measurements justify a different strategy.

## References

Osmani, A., Sohoni, L., Meenan, P., & Pollard, B. (2023, November 14). *Optimize resource loading with the Fetch Priority API*. web.dev. https://web.dev/articles/fetch-priority

WHATWG. (2026, July 20). *HTML living standard: The img element*. https://html.spec.whatwg.org/multipage/embedded-content.html#the-img-element
