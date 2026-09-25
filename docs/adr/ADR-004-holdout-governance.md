# ADR-004 — Holdout and Lockbox Governance

**Status:** Proposed for freeze before coding

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
