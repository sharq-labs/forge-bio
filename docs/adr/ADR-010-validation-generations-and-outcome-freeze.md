# ADR-010 — Validation Generations and Outcome Snapshot Commitment

**Status:** Accepted — pre-code hardening  
**Decision scope:** validation reuse, sealed outcomes, and evaluation immutability

## Problem

Two distinct forms of adaptive overfitting remain possible even with a sealed lockbox:

1. repeatedly tuning methodology against the same VALIDATION cases;
2. allowing the Future Outcome source/curation/mapping state to change after the MAP or ranking is frozen.

## Decision A — validation generations

Validation data are versioned into generations.

```text
ValidationGeneration
    generation_id
    benchmark_id
    case_set_digest
    outcome_snapshot_digest
    access_count
    status
```

Status:

```text
ACTIVE
SPENT_FOR_MODEL_SELECTION
RETIRED
```

If validation results materially influence:
- feature design;
- endpoint design;
- model class;
- hyperparameters;
- threshold selection;
- disease/candidate selection;

the generation is marked `SPENT_FOR_MODEL_SELECTION`.

A spent validation generation may still be used descriptively, but it is not represented as untouched evidence.

## Decision B — outcome snapshot commitment

Before sealed evaluation, the following evaluation-side artifacts are frozen/committed:

```text
future_outcome_source_release_ids
future_outcome_snapshot_ids
future_outcome_snapshot_digest
outcome_ledger_digest
adjudication_batch_digest
evaluation_identity_bridge_digest
phenotype_match_policy_version
gene_assignment_policy_version
replication_policy_version
```

The ranking artifact and outcome commitment are both immutable inputs to the evaluation.

A provider moving from release R1 to R2 creates a new evaluation artifact/generation.

## Decision C — strongest confirmatory blinding

For strongest L3 sealed confirmation:

```text
outcome adjudicator sees model rank/order -> automatic tier downgrade
```

The deviation is not phrased as optional or merely "where feasible".

Exploratory/development adjudication may use weaker blinding if explicitly declared.

## Consequences

- validation reuse becomes visible instead of silently accumulating;
- sealed outcome labels cannot move between freeze and evaluation;
- exact outcome snapshot is part of scientific provenance;
- unblinded sealed adjudication cannot earn the strongest confirmatory tier.
