# ADR-001 — First Confirmatory Benchmark Endpoint

**Status:** Accepted — amended by ADR-008, ADR-009, ADR-011, and ADR-012

## Decision

The first benchmark family is B-TGT.

The V0 benchmark role is **B-TGT-A1 — Disease–Gene Association Prioritization**.

The confirmatory endpoint family is later independent human genetic support within fixed horizon H, refined into E1-NOVEL-STRICT, E1-MATURATION, E1-REPLICATION, and E1-CROSSMODAL under ADR-009.

The V0 prediction unit is disease–gene association, not full intervention direction.

## Why

This creates a narrow, falsifiable, scalable first target-prioritization problem and avoids pretending that later association alone validates inhibition/activation or clinical utility.

## Consequences

- B-TGT-E1-v0 evaluates biological prioritization only.
- Direction-aware target validation is a later benchmark.
- Drug repurposing remains a separate B-REP family.
- H and evidence-quality thresholds are selected on development data and frozen before sealed evaluation.


## Amendments

- ADR-008 governs disease/phenotype matching.
- ADR-009 governs strict novelty, maturation, and replication semantics.
- ADR-011 governs genomic variant/locus identity, harmonization, and LD provenance.
- ADR-012 governs historical genetic search coverage and observability.

This ADR establishes the benchmark family/unit; the amendment ADRs define the modern normative endpoint semantics.
