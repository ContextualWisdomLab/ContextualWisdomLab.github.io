# Contextual Wisdom Lab Homepage

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/ContextualWisdomLab/ContextualWisdomLab.github.io)

**The public home for ContextualWisdomLab: research context, product direction, and a human-readable path into the organization’s work.**

This repository owns the static organization homepage. The site explains the Contextual Wisdom thesis—turning scattered documents, messages, logs, schedules, and other evidence into context that supports human judgment and action—and gives visitors a curated route into the lab’s research and projects.

It is a presentation and navigation surface, not the runtime or system of record for the products it links to. Product capabilities, releases, security boundaries, licenses, and integration contracts remain authoritative in their owning repositories.

## What visitors can explore

The current site provides:

- a Korean/English language switch;
- the Contextual Wisdom and DIKW framing used to explain the lab’s research direction;
- research/evidence and reference sections;
- a dedicated Naruon introduction;
- project and fork discovery sections; and
- direct navigation to the ContextualWisdomLab GitHub organization.

The homepage deliberately separates a research thesis from product authority. A statement on this site should not be used to infer that a linked repository has shipped a release, passed certification, reached production readiness, or acquired customers unless the owning repository exposes that evidence itself.

## Repository boundary

| This repository owns | Owning product repositories retain |
| --- | --- |
| Organization-level public narrative and navigation | Runtime behavior and APIs |
| Homepage information architecture and visual presentation | Product PRDs, ADRs, schemas, databases, and domain authority |
| Korean/English homepage copy | Release and deployment evidence |
| Static homepage assets and accessibility behavior | Security, compliance, and operational claims |
| Links into current organization work | Product-specific license and integration obligations |

When a product changes materially, update its owning repository first and then reconcile this homepage. Do not make the homepage the only place where a product claim exists.

## Local preview

The site is static and does not require a package manager or application server. From the repository root:

```bash
python3 -m http.server 4173
```

Then open `http://127.0.0.1:4173/`.

Before changing public copy or navigation, verify both language states and the responsive layout. The current document includes a skip link, semantic navigation labels, keyboard-focus targets, explicit image dimensions, a restrictive Content Security Policy, and self-hosted assets; preserve those accessibility, security, and performance boundaries unless a reviewed change intentionally replaces them.

## Editing the public surface

The primary files are intentionally small and direct:

- `index.html` — page structure, public copy, navigation, metadata, and asset references;
- `i18n.js` — Korean/English copy and language switching;
- `styles.css` — layout, typography, responsive behavior, and interaction styling;
- `assets/` — images, diagrams, and self-hosted presentation assets;
- `CHANGELOG.md` — repository-facing change history;
- `AGENTS.md` and `CLAUDE.md` — contributor and automation constraints.

For a content change, keep the Korean and English surfaces semantically aligned rather than translating labels independently. For a project link or capability statement, verify the target repository’s current default branch, product documentation, and release evidence before publishing it here.

## Quality and trust rules

- Do not publish customer, certification, deployment, benchmark, adoption, revenue, or release claims without owning-repository evidence.
- Do not expose internal implementation boundaries as customer-facing product language.
- Treat externally sourced images, fonts, code, and other assets as inbound dependencies: commercial-use-compatible provenance is required before inclusion.
- Prefer organization-owned or properly licensed local assets; do not introduce noncommercial, research-only, evaluation-only, or commercially restrictive material.
- Preserve the site’s restrictive browser security posture rather than loosening CSP or external-resource policy for convenience.

## Where to go next

- [ContextualWisdomLab organization](https://github.com/ContextualWisdomLab) — browse source repositories and their current product documentation.
- [Ask DeepWiki](https://deepwiki.com/ContextualWisdomLab/ContextualWisdomLab.github.io) — explore this homepage repository structure.

For product integration, installation, security, contribution, or release questions, follow the documentation in the repository that owns that product rather than treating this homepage as a substitute.

## License

ContextualWisdomLab original source and documentation in this repository are licensed under the [MIT License](LICENSE). Third-party assets or materials, when present, retain their own license and attribution requirements; the repository’s MIT grant does not relicense them.
