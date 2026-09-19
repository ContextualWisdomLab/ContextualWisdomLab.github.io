# Product and technical gap baseline

Status: **Proposed**  
Canonical writer: [ContextualWisdomLab.github.io#240](https://github.com/ContextualWisdomLab/ContextualWisdomLab.github.io/pull/240)  
Evidence ancestor: `97e480a06ed97418d8ce6a4186eb6ec6af55c6b1` (2026-09-20)  
Current exact head and hosted evidence are recorded on the PR after every ordinary-forward update.

This document is the buyer-visible design-assurance ledger for the public
ContextualWisdomLab website. A checked source contract is not a browser,
assistive-technology, deployment, approval, certification, or release claim.

## PRD

### Goal

A visitor can understand ContextualWisdomLab's public purpose and navigate to
the authoritative product repositories without the website replacing product
domain truth.

### Users and scenes

- A prospective buyer scans the homepage by headings and region landmarks.
- A keyboard or screen-reader user skips to main content and navigates sections.
- A multilingual visitor needs equivalent names, wrapping, and next actions.
- An operator must distinguish published website evidence from repository claims.

### Acceptance

The homepage must preserve deterministic content, meaningful landmarks,
keyboard/pointer/touch operation, responsive layout, reduced motion, safe
external navigation, eight locales (ko/en/ja/zh/vi/es/de/fr), and recovery from
offline or missing destinations. Claims require evidence from the same exact
head.

## TRD

The product is a static HTML/CSS/JavaScript site. Semantic HTML and the browser
accessibility tree are the interaction boundary. Python standard-library parsers
provide source contracts; they do not replace Chromium, Firefox, WebKit, or
assistive-technology runs. No new runtime dependency is justified for landmark
validation.

Translation strings currently live in the browser JavaScript object. That is a
presentation resource, not organization or product domain truth. It does not
satisfy the target DB-backed versioned translation authority.

## UML

```mermaid
flowchart LR
    V[Visitor] --> H[index.html]
    H --> C[styles.css]
    H --> I[i18n.js]
    H --> R[Authoritative product repositories]
    T[Source contracts] --> H
    B[Browser and AT evidence] --> H
```

## ERD

No application database is present in this bounded context, so a product-data
ERD is not applicable. If the shared translation authority is introduced, its
minimum independent model is:

```mermaid
erDiagram
    SCREEN_KEY ||--o{ TRANSLATION_RESOURCE : versions
    TRANSLATION_RESOURCE }o--|| LOCALE : uses
    TRANSLATION_RESOURCE ||--o{ REVIEW_DECISION : governed_by
    TRANSLATION_RESOURCE ||--o{ DEPLOYMENT_RECORD : publishes
```

The website must consume a released contract through an API/cache boundary; it
must not copy another owner's source or query its database.

## Context Map

- **Public Narrative (this repository):** homepage composition, public
  navigation, static presentation, Pages deployment evidence.
- **Product repositories (upstream authority):** product behavior, release,
  security, domain language, and operational truth.
- **Translation authority (required shared owner, not yet released):** versioned
  translation, review, approval, deployment, and rollback.
- **GitHub (external):** repository destinations behind ordinary links; the
  website does not infer product readiness from an open PR.

## Exact-head acceptance matrix

| Boundary | Evidence at ancestor | Status | Required action |
| --- | --- | --- | --- |
| Determinism | 11 homepage sections; 11 heading targets | PASS, source only | Keep exact structure contract |
| Semantics | hero uses `aria-labelledby="hero-title"`; parser checks every section and exactly one real heading target | PASS, source only | Replay accessibility tree |
| Keyboard/pointer/touch | No current-head real-browser trace | FAIL | Chromium/Firefox/WebKit interaction run |
| WCAG 2.2 AA / AT | No current-head AT transcript or audit | FAIL | Screen reader and automated/manual audit |
| Responsive | No 320/768/desktop screenshots at current head | FAIL | Capture overflow, wrapping, focus, zoom |
| Reduced motion | Source policy exists; no current-head browser observation | PARTIAL | Verify OS preference in each browser |
| Locales | `i18n.js` exposes ko/en only | FAIL | Released ko/en/ja/zh/vi/es/de/fr screen resources and E2E |
| Loading/empty/error/offline/permission/read-only/stale/conflict/retry/busy | Static surface has no complete evidence set | FAIL | Mark N/A per state with rationale or provide replay |
| CTA to API/destination | Static links exist; no current-head destination replay | FAIL | Validate real destinations and failure guidance |
| Large-data performance | Not applicable to hero landmark; whole-page p95 unmeasured | FAIL (site) | Measure render/interaction p50 and p95 without sample reduction |
| Import/export | No import/export surface | N/A | Reassess if introduced |
| Persistence/reload/rollback | No current-head cache/reload/deploy rollback evidence | FAIL | Exercise reload, offline cache behavior, and deployment rollback |
| Independent approval | Previous approval targets an older head | FAIL | Obtain qualifying current-head approval |
| Hosted Checks | Fresh exact-head generation required after repair | PENDING | Wait without blind rerun |

## Gap and action register

| Gap | Owner | Action | Status |
| --- | --- | --- | --- |
| Existing landmark test skipped anonymous sections | Public Narrative | Validate every section and exactly one heading target | Repaired in #240; hosted evidence pending |
| Palette entry used a stale 2024 date and `h2`-only rule | Public Narrative | Bind guidance to 2026-09-20 evidence and h1-h6 | Repaired in #240 |
| Only ko/en resources exist | Translation authority + Public Narrative consumer | Release eight-locale resource contract, then consume by screen key | Proposed / blocked |
| Browser, AT, responsive, recovery evidence absent | Public Narrative | Produce current-head evidence artifacts | Open |
| Static DTO/catalog may be mistaken for domain truth | Public Narrative | Keep product claims linked to canonical repositories | Open |
| Page performance target is unmeasured | Public Narrative | Measure all pages; repair causal render/runtime bottleneck | Open |
| Exact-head approval and hosted Checks absent | Repository governance | Preserve Draft until independently satisfied | Open |

## Standards and evidence

- World Wide Web Consortium. (2023). *Web Content Accessibility Guidelines
  (WCAG) 2.2*. https://www.w3.org/TR/WCAG22/
- Web Hypertext Application Technology Working Group. (2026). *HTML Living
  Standard: The section element*. https://html.spec.whatwg.org/multipage/sections.html#the-section-element
- World Wide Web Consortium. (2026). *Accessible Rich Internet Applications
  (WAI-ARIA) 1.2: region role*. https://www.w3.org/TR/wai-aria-1.2/#region

These standards explain the semantic boundary. Repository source, tests,
current-head workflow logs, browser artifacts, and review records remain the
acceptance evidence.
