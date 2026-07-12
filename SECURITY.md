# Security Policy

## Supported Versions

The `main` branch receives security fixes for this static homepage.

## Reporting a Vulnerability

Please report suspected vulnerabilities privately through the repository's
GitHub Security Advisory intake instead of opening a public issue:

https://github.com/ContextualWisdomLab/ContextualWisdomLab.github.io/security/advisories/new

Include the affected URL or file, reproduction steps, browser/version details
when relevant, and expected impact.

Disclosure handling SLA: we aim to acknowledge vulnerability reports within 3
business days, provide a status update within 30 days when a fix needs longer
coordination, and ship a fix or mitigation for confirmed high/critical issues as
quickly as practical.

## Scope

This repository hosts a static GitHub Pages site. The security baseline is a
strict Content Security Policy, no third-party runtime scripts, safe DOM APIs
for localization, CodeQL analysis for JavaScript/HTML changes, Dependabot for
GitHub Actions updates, and the organization-wide Trivy/OSV review gates.
