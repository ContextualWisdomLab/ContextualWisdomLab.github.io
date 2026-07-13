# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

The static homepage for the Contextual Wisdom Lab GitHub organization, served by GitHub Pages directly from the repository root of `main` (`.nojekyll` disables Jekyll). There is no build step, package manager, framework, or bundler — plain HTML/CSS/JS with all assets (including the Pretendard font) self-hosted.

## Commands

```bash
# Local preview (from repo root)
python3 -m http.server 4173

# i18n tests: open http://localhost:4173/test_i18n.html in a browser
# and check the console — success prints "ALL_TESTS_PASSED_SUCCESSFULLY"
```

There is no lint/build/deploy command. Deployment is automatic: pushing to `main` updates the live site. CI is limited to GitHub's CodeQL default setup (`.github/workflows/codeql.yml` is only a marker workflow), Dependabot for GitHub Actions, and a ClusterFuzzLite marker Dockerfile.

## Architecture

Three moving parts:

- **`index.html`** — the entire single-page site. Korean is the source language: all Korean text is authored inline, and every translatable node carries a `data-i18n="section.key"` attribute.
- **`i18n.js`** — contains the `messages` dictionary with `ko` and `en` variants for every key, plus the runtime. Language resolution order: `?lang=` query param (validated against the `["ko", "en"]` whitelist — this guards against prototype pollution, do not weaken it) → `localStorage["cwl-language"]` (wrapped in try/catch for strict privacy modes) → `navigator.language`. `setLanguage()` swaps `textContent` on `[data-i18n]` nodes and also updates `document.title`, `<html lang>`, meta/og descriptions, the language-specific footer logo (`logoSrc`/`logoAlt` — there are separate KO and EN logo SVGs in `assets/`), and `aria-pressed` on the KO/EN buttons. It deliberately skips the DOM traversal on initial load when the resolved language is Korean, since the HTML already is Korean.
- **`styles.css`** — brand design tokens live in `:root` (`--ink`, `--teal`, `--gold`, `--paper`, `--line`, ...). Korean typography uses `word-break: keep-all` / `line-break: keep-all`. A `prefers-reduced-motion` block at the bottom sets durations to `0.01ms` (not `0s`, so `transitionend` events still fire).

**`components/`** is a standalone KRDS component-library gallery (`components/index.html` + `krds-components.css`), a vanilla, token-bound mirror of a Figma design system. It is scoped under `.krds-scope`, consumes the brand tokens from `styles.css`, and adds its own status tokens. It is not loaded by the main page.

**`test_i18n.html`** is a minimal browser test harness: it mocks `localStorage`, loads `i18n.js`, and asserts language switching updates `currentLang` and node text.

## Conventions

- **Adding or changing copy**: every user-visible string needs a `data-i18n` key present in *both* the `ko` and `en` dictionaries in `i18n.js`, with the Korean text also inlined in `index.html` as the default. `metaTitle`, `metaDescription`, `logoSrc`, `logoAlt` are special non-`data-i18n` keys handled explicitly in `setLanguage()`.
- **Strict CSP with Trusted Types**: the CSP meta tag in `index.html` includes `default-src 'self'` and `require-trusted-types-for 'script'`. Only safe DOM APIs (`textContent`, `setAttribute`) may be used — introducing `innerHTML` or similar sinks will throw at runtime unless a Trusted Types policy/sanitizer is added. No third-party runtime scripts or CDN resources; everything must be self-hosted.
- **External links** always get `target="_blank" rel="noopener noreferrer"`.
- **Guarded DOM writes**: check the current value before writing (`if (node.textContent !== newText)`) to avoid layout thrash; early-exit when setting state to its current value. Performance-motivated code is annotated with `⚡ Bolt:` comments.
- **Accessibility**: grouped interactive containers get `role="group"` + `aria-label`; the language toggle uses `aria-pressed`; focus ring convention is `2px solid var(--teal)` with `2px` offset; avoid `--gold` text on light backgrounds (fails WCAG AA contrast — use `--teal`; `--gold` is fine on dark `--ink`).
- **Learning journals**: `.jules/bolt.md` (performance), `.jules/sentinel.md` (security), and `.Jules/palette.md` (accessibility/UX) record past incidents and the rules derived from them — consult and extend them when making changes in those areas.
- **`CHANGELOG.md`** is written in Korean and updated under `[Unreleased]` for user-facing changes.
