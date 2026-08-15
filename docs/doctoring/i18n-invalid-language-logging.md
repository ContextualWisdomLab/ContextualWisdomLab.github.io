# Invalid-language logging boundary

## Decision

The public `setLanguage(lang)` boundary accepts only the finite values `ko` and
`en`. An invalid value still produces an operator-visible warning and falls back
to Korean, but the warning is a constant string and never includes the rejected
value.

```text
untrusted language candidate
  -> finite allow-list validation
  -> constant invalid-input classification
  -> Korean fallback
```

This keeps the useful event classification without transporting attacker-
controlled control characters, markup-shaped text, identifiers, or personal
content into the browser console or any downstream console collector.

## Threat and claim boundary

MITRE CWE-117 describes the integrity risk created when external input is written
to logs without suitable neutralization. The OWASP Logging Cheat Sheet likewise
requires data crossing trust zones to be treated as untrusted and recommends
purpose-bound selection of event content.

For this static site, the immediate sink is the browser console rather than a
server-owned audit log. A local console entry alone is not a durable security log,
and this change does not claim centralized log integrity, non-repudiation,
retention, access control, or incident-response completeness. It prevents the
known raw-value transport and preserves only the finite event category. Should a
telemetry collector later capture browser console output, that collector must
establish its own schema, encoding, authentication, tenant separation, retention,
and access-control contract.

## Verification

The permanent regression test:

1. locates the exact invalid-language branch;
2. requires exactly one `console.warn` call in that branch;
3. requires the reviewed constant warning argument; and
4. rejects interpolation or another direct `lang` reference in the warning call.

The browser harness continues to exercise prototype-shaped and markup-shaped
invalid values. The regression is structural; representative browser execution
and deployed telemetry review remain separate acceptance evidence.

## Rollback

Rollback must not restore raw `lang` interpolation. If operators later require a
rejected-value correlation key, introduce a separately reviewed bounded value
classification or digest with an explicit purpose and privacy contract rather
than writing the original input.

## References

MITRE. (2026). *CWE-117: Improper output neutralization for logs* (Version
4.20). https://cwe.mitre.org/data/definitions/117.html

OWASP Foundation. (n.d.). *Logging cheat sheet*. OWASP Cheat Sheet Series.
Retrieved August 15, 2026, from
https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
