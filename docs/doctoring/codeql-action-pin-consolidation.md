# CodeQL action pin consolidation

## Decision

The repository's manual CodeQL marker workflow uses one reviewed immutable release identity for both `github/codeql-action/init` and the disabled documentation-only `github/codeql-action/analyze` step:

- `github/codeql-action` v4.37.6: `5595ccaf912efad79be6eef63a5619ff05969be3`;
- `actions/checkout` v7.0.1: `3d3c42e5aac5ba805825da76410c181273ba90b1`.

The checkout step explicitly sets `persist-credentials: false`. The workflow remains manually dispatched, read-only, and does not upload SARIF. GitHub CodeQL default setup or the organization-owned required checks continue to own analysis publication.

## Why this consolidation is necessary

Three independent dependency pull requests proposed overlapping updates to checkout, CodeQL initialization, and the disabled analyze marker. Keeping those changes separate would leave temporary version skew and multiple competing merge paths. The consolidated change applies the newest reviewed CodeQL release to both CodeQL action references and includes the checkout credential hardening already validated in the predecessor branch.

The CodeQL v4.37.6 tag resolves exactly to commit `5595ccaf912efad79be6eef63a5619ff05969be3`. The checkout v7.0.1 release commit is `3d3c42e5aac5ba805825da76410c181273ba90b1`. Full-length commit pins prevent a mutable tag or branch from changing the code executed by the workflow without a reviewed repository change.

## Trust and behavior boundaries

This change does not:

- enable the disabled `analyze` step;
- transfer SARIF ownership from default or central setup;
- add write permissions, tokens, model credentials, caches, or artifacts;
- execute pull-request-controlled code with retained Git credentials; or
- alter branch protection, review identities, or required status contexts.

The manual workflow still receives the ordinary runner environment. Disabling persisted checkout credentials removes automatic authenticated Git access from later steps, but it does not remove every GitHub-provided environment variable. Repository permissions therefore remain explicitly read-only.

## Test-first evidence

Commit `496474275cb3fdb8f8a54dee02a4767acdb0b8f8` introduced the permanent regression contract before the production workflow changed. Against the protected-base workflow, that contract fails because checkout is still v7.0.0, credential persistence is not disabled, and CodeQL is still v4.37.0. The implementation commit then updates only the reviewed action references and credential setting required to satisfy the contract.

## Verification

For each candidate exact head:

1. Run the complete repository test suite, including `tests/test_codeql_workflow_security.py`.
2. Confirm the workflow contains each required action SHA exactly where expected.
3. Confirm `persist-credentials: false` remains attached to the checkout step.
4. Confirm repository security, static-analysis, and policy checks complete successfully on that exact head.
5. Confirm all actionable review threads are resolved and an independent non-last-pusher approval applies to that exact head before merge.

Queued, pending, skipped-required, cancelled, absent, failed, or predecessor-head evidence is not accepted.

## Rollback

Rollback requires a reviewed commit that replaces both CodeQL action references together and updates the regression contract. Do not move one CodeQL component independently or replace a full commit SHA with a tag. If v4.37.6 causes a verified regression, pin both CodeQL references to the last known-good immutable commit, retain `persist-credentials: false`, rerun the exact-head checks, and document the incident in this record and the changelog.

## References

Actions. (2026, July 17). *Checkout v7.0.1* [Software release]. GitHub. https://github.com/actions/checkout/releases/tag/v7.0.1

GitHub. (2026, August 4). *CodeQL Action v4.37.6* [Software release]. GitHub. https://github.com/github/codeql-action/releases/tag/v4.37.6

GitHub. (n.d.). *Secure use reference*. GitHub Docs. Retrieved August 7, 2026, from https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions
