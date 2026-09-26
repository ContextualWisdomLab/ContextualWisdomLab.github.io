# Product and technical gap baseline

Status: **Proposed**
Canonical writer: [ContextualWisdomLab.github.io#240](https://github.com/ContextualWisdomLab/ContextualWisdomLab.github.io/pull/240)
Evidence ancestor: `818d38088fb22408185a987074161aba9dbb399b` (2026-09-20)
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
| Literal `\\n-` merged adjacent Unreleased entries | Public Narrative | Reject escaped list separators with `tests/test_changelog.py`; store a real line break | Repaired at `818d38088fb22408185a987074161aba9dbb399b`; hosted evidence pending |
| Existing landmark test skipped anonymous sections | Public Narrative | Validate every section and exactly one heading target | Repaired in #240; hosted evidence pending |
| Palette entry used a stale 2024 date and `h2`-only rule | Public Narrative | Bind guidance to 2026-09-20 evidence and h1-h6 | Repaired in #240 |
| Only ko/en resources exist | Translation authority + Public Narrative consumer | Release eight-locale resource contract, then consume by screen key | Proposed / blocked |
| Browser, AT, responsive, recovery evidence absent | Public Narrative | Produce current-head evidence artifacts | Open |
| Static DTO/catalog may be mistaken for domain truth | Public Narrative | Keep product claims linked to canonical repositories | Open |
| Page performance target is unmeasured | Public Narrative | Measure all pages; repair causal render/runtime bottleneck | Open |
| Exact-head approval and hosted Checks absent | Repository governance | Preserve Draft until independently satisfied | Open |

## External-link indicator acceptance — #265

Product source remains single-writer #265. This documentation lane records evidence
only and does not copy mutable homepage source.

- Product evidence exact: `96c3ba8022816ce0f76f94095af6587675cba6ac`
- RED contract: `50938ba62ab7ec9fdb35bd77c2cd062a9a387b38`
  found 23 new-tab links but only 21 visual indicators; both omissions were
  primary CTA links.
- Production repair: `ef9e2bbe62f6259fed114ae0e5933422bfc4f6f0`
  moves CTA translation keys to visible child spans and adds decorative,
  assistive-technology-hidden indicators.
- Changelog binding and concurrent-regression recovery exact: `96c3ba8022816ce0f76f94095af6587675cba6ac`.
  A successor deleted both executable contracts, removed the CHANGELOG entry, and
  reverted the two CTA repairs; three ordinary-forward commits restored the
  verified blobs without force or discarding the successor's separate metadata.

| Acceptance dimension | Exact evidence | Status |
| --- | --- | --- |
| Determinism | 23 `target="_blank"` links / 23 visual indicators | Source GREEN |
| Locale persistence | translated CTA text is a child span; indicator is a sibling | Source GREEN |
| Semantics | `aria-describedby` new-window description and hidden decoration remain separate | Source GREEN |
| Real browser / AT | Chromium, Firefox, WebKit and assistive-technology replay absent | FAIL |
| Responsive / touch | 320px, 768px, desktop and touch evidence absent | FAIL |
| Eight locales | ko/en/ja/zh/vi/es/de/fr screenshots and overflow checks absent | FAIL |
| Performance | deployed page median/p95 and layout-shift evidence absent | FAIL |
| Review / hosted gates | current exact-head independent approval and terminal required Checks absent | Pending |

Keep #265 Draft / Proposed. No publication, merge, release, or carryover claim is
authorized from source-level evidence alone.

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
