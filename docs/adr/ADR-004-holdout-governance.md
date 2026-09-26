# ADR-004 — Holdout and Lockbox Governance

**Status:** Accepted — amended by ADR-010 and ADR-013

## Decision

Benchmarks use three tiers:
- DEVELOPMENT
- VALIDATION
- SEALED_LOCKBOX

The sealed lockbox is stored under separate access controls. Confirmatory evaluation requires a frozen MAP and sealed ranking hash before future labels are opened.

Every access records who, when, why, benchmark generation, MAP hash, and model/ranking identity.

## Consequences

Once individual sealed errors are inspected and methodology changes in response, that lockbox generation is considered spent for future confirmatory claims.

Hashes alone are not sufficient custody; storage/credentials/access logging must enforce separation.


## Amendments

ADR-010 adds:
- versioned validation generations;
- SPENT_FOR_MODEL_SELECTION status;
- exact Future Outcome snapshot commitments;
- mandatory strongest-L3 adjudicator rank blinding.

ADR-013 adds:
- validation disclosure level;
- outcome-event discovery freeze before ranking reveal;
- ScientificEventFamily commitments.

These amendments are normative where they are stricter than the original ADR.
