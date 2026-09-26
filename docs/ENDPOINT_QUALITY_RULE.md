# Endpoint Evidence-Quality Rule Template — B-TGT-E1

**Status:** STRUCTURE FROZEN / VALUES EMPIRICAL-OPEN

The endpoint-quality rule is not a single p-value threshold.

The final rule is instantiated only after the BIG 0F provider/outcome audit, but the **shape of the decision is frozen now** so the audit cannot invent new dimensions after seeing favorable events.

## Required dimensions

Every qualifying primary E1 event must be evaluated across the applicable dimensions:

1. study-design class;
2. statistical strength;
3. sample size / event count where relevant;
4. sample/cohort independence;
5. phenotype match;
6. genome-build / variant / allele harmonization;
7. allele/effect-direction semantics where relevant;
8. population/ancestry context;
9. replication status where relevant;
10. heterogeneity where relevant;
11. high-specificity gene-assignment eligibility;
12. HistoricalNoveltyAudit / PreTGeneticState;
13. source/lineage quality.

Genome-wide significance alone is not sufficient.

## Freeze procedure

BIG 0F may estimate feasibility and distributions, but it does not choose thresholds based on Forge Bio model lift.

After provider/outcome feasibility measurements and before any sealed confirmatory generation:

```text
provider audit
→ endpoint-quality candidate rule
→ development-only sensitivity
→ freeze rule
→ external seal
→ confirmatory generation
```

The frozen artifact uses:
`schemas/endpoint-quality-rule.v1.schema.json`.

## Fail-closed rules

- missing required criterion → event does not qualify;
- UNKNOWN independence where independence is required → event does not qualify as independent support;
- unresolved phenotype match → event does not qualify;
- unresolved allele/liftover/orientation ambiguity → strict replication event does not qualify;
- non-primary gene assignment cannot create a primary gene-level positive;
- post-T recuration of pre-T evidence cannot create a novel event.

## Claim boundary

This template closes the **decision structure**, not the empirical threshold values.

The checklist item for final endpoint evidence quality remains open until BIG 0F provides the provider/outcome feasibility evidence needed to freeze the values.


## Executable criterion rule

Comparison operators are executable, not descriptive placeholders:

- `GT / GE / LT / LE` require a numeric operand;
- `EQ / NE` require a scalar operand;
- `IN / NOT_IN` require a non-empty primitive list;
- `REQUIRE` asserts presence/availability and does not require a comparison operand.

A FROZEN rule with a missing or unusable comparison operand is schema-invalid.
