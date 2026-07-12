# AGENTS.md

Cross-agent guidance for this repository, readable by any coding agent
(Claude, Codex, Cursor, opencode, and others). This is the static homepage
for Contextual Wisdom Lab — plain HTML/CSS/JS served via GitHub Pages
(`index.html`, `styles.css`, `i18n.js`; no build step, no package manager).
Preview locally with `python3 -m http.server 4173`.

<!-- BEGIN cwl-agent-guidance -->
## Agent guidance (CWL governance)

### Security & review gate
- Every PR runs a central **Security Scan** required gate: `osv-scan` +
  `dependency-review` (diff-scoped) and `trivy-fs` (repo-wide, CRITICAL/HIGH,
  fixable only). It runs against every PR base, **including stacked PRs**.
- A **failing `trivy-fs` is a REAL finding, not a flake.** Read the job log
  (it prints each finding's rule id / severity / file) or the run's SARIF
  results, then **remediate** — do NOT weaken, ignore, or disable the gate.
- This repo is a static site with no `package.json`, lockfile, Dockerfile, or
  k8s manifests, so `trivy-fs` here most likely flags a **checked-in secret or
  a misconfiguration in a committed config file**. Fix it at the source
  (remove/rotate the secret, correct the config). Only for a genuine false
  positive, add a narrow, documented `.trivyignore` (or `.trivyignore.yaml`)
  entry explaining why.
- Reproduce locally against the **merge ref, not just the PR head**, and
  refresh the DB first so a stale local DB doesn't miss findings:
  ```bash
  trivy --download-db-only
  trivy fs --severity CRITICAL,HIGH --ignore-unfixed .
  ```
- The org `code_scanning` ruleset is intentionally **CodeQL-only** (multiple
  code-scanning tools can't converge on one PR ref). Gating is enforced by the
  Security Scan **job result**, not the `code_scanning` rule — do **not** add
  tools to that rule.

### Code exploration
- This repo has **no `.codegraph/` index**, so use normal search (grep/find,
  editor search) to locate and understand code. If a `.codegraph/` directory
  is ever added at the repo root, prefer CodeGraph
  (`codegraph explore "<query>"`, or the code-review-graph MCP tools) BEFORE
  grep/find — it surfaces callers/callees/impact that text search misses.
<!-- END cwl-agent-guidance -->
