# Homepage product destinations

## Status

Active product-boundary evidence for the public project and fork cards.

## Decision

Homepage cards that look like products must open a repository the organization currently owns, or they must not be links.

- The WAF/IDS/AI SOC gateway is published as `wardnet`. The former `waf-ids-ai-soc` name is treated as an old caller name and is not shown or linked.
- `argos` and `vooster` are owned forks, so their cards use the same `target="_blank"` + `rel="noopener noreferrer"` + project-grid hit-area pattern as first-party project cards.
- `vooster-v2-mvp` has no `ContextualWisdomLab/vooster-v2-mvp` repository. The card stays an introduction until that ownership exists. A guessed or upstream-only URL is not added.

## Rationale

Buyers use the homepage to open the product they just read about. A card titled with an old repository name, or a fork card with no destination, looks like a broken catalog. Linking a name the organization does not own creates a 404 and is worse than a non-link.

ISO/IEC 25010 treats functional correctness and appropriateness as product quality characteristics: the named software and the opened software must be the same thing (ISO/IEC, 2023).

## Failure and rollback

Rollback restores the `waf-ids-ai-soc` label/href and removes the `argos`/`vooster` anchors. Do not restore a `vooster-v2-mvp` href unless a live owned repository exists.

## References

International Organization for Standardization. (2023). *Systems and software engineering — Systems and software Quality Requirements and Evaluation (SQuaRE) — Product quality model* (ISO/IEC 25010:2023). https://www.iso.org/standard/78176.html
