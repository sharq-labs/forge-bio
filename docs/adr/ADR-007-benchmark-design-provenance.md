# ADR-007 — Benchmark Design Provenance and Analyst Blinding

**Status:** Proposed — P0 blocker  
**Decision scope:** confirmatory historical benchmarking

## Decision

Technical isolation of future labels is necessary but not sufficient.

Forge Bio treats researcher/analyst hindsight as a separate leakage channel.

Every confirmatory benchmark maintains a **BenchmarkDesignProvenance** record containing:

```text
benchmark_generation
designers
ranking_team
outcome_adjudicators
lockbox_custodian
future-outcome exposure declarations
sealed-disease exposure declarations
feature-definition freeze timestamp
algorithm/config freeze hash
MAP freeze hash
deviations
```

## Role separation

Where feasible:
- ranking/model developers do not inspect sealed outcome labels;
- outcome adjudicators do not see candidate rank/order during classification;
- the lockbox custodian is distinct from the ranking runtime and ordinary developer credentials.

For the strongest retrospective claim, sealed disease identities should remain hidden from the methodology team until feature families, ranking algorithm, and evaluation protocol are frozen.

## Manual knowledge

Public biomedical knowledge already known by a researcher cannot be cryptographically erased.

Therefore confirmatory claims must rely on governance:
- preregistration;
- blinded adjudication;
- sealed disease/case selection where practical;
- exposure declarations;
- independent replication of the benchmark by a second team or later prospective validation.

## Consequences

A technically sealed benchmark with uncontrolled outcome-aware design is classified as exploratory or lower-evidence retrospective validation, not the strongest confirmatory tier.
