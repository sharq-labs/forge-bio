# ADR-008 — Outcome Phenotype Matching

**Status:** Accepted — pre-code hardening  
**Decision scope:** disease/trait matching for B-TGT gene-level future outcomes

## Problem

A genetic association for a related trait, biomarker, intermediate phenotype, or risk factor is not automatically genetic support for the benchmark disease.

Examples of unsafe silent promotion include:

```text
LDL cholesterol → coronary artery disease
BMI → type 2 diabetes
eosinophil count → asthma
blood pressure → stroke
```

These relations may be scientifically relevant, but they are not identity-equivalent disease outcomes.

## Decision

Every future genetic event used for B-TGT-E1 receives an explicit `OutcomePhenotypeMatchAssessment`.

Minimum relation states:

```text
EXACT
SAME_CONCEPT_DIFFERENT_DEFINITION
NARROWER
BROADER
SURROGATE
RISK_FACTOR
INTERMEDIATE_PHENOTYPE
RELATED
UNRESOLVED
```

## Primary endpoint rule

The primary confirmatory MAP must freeze which relations qualify.

Default V0 strict policy:

```text
EXACT
SAME_CONCEPT_DIFFERENT_DEFINITION  -> only with explicit adjudication
NARROWER                           -> sensitivity / case-specific only
BROADER                            -> not primary
SURROGATE                          -> not primary
RISK_FACTOR                        -> not primary
INTERMEDIATE_PHENOTYPE             -> not primary
RELATED                            -> not primary
UNRESOLVED                         -> fail closed
```

The benchmark may define a broader secondary endpoint, but it must be reported separately.

## Required provenance

```text
benchmark_disease_id
future_phenotype_id
future_phenotype_definition
relation
mapping_source
mapping_version
assessment_basis
reviewer
review_timestamp
adjudication_status
```

## Rule

Identity reconciliation cannot silently answer the phenotype-equivalence question.

A modern ontology relation may help evaluation-side reconciliation, but the scientific relation between the benchmark disease and future trait remains explicit and reviewable.

## Consequences

- phenotype matching becomes part of outcome adjudication;
- outcome ambiguity can arise from disease/trait mismatch;
- primary endpoint counts cannot silently include risk factors or surrogate traits;
- phenotype-match sensitivity analysis is required when broader relations materially change results.
