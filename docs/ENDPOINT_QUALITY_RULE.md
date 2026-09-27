# Endpoint Evidence-Quality Rule Template — B-TGT-E1

**Status:** Structure and applicability SPEC-CLOSED. Values are EMPIRICAL-OPEN and may only be equal to or stricter than adjudication policy v2 (`BIG0F-ADJUDICATION-V2`; ADR-022 D7, D17; INV-T8).

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

## Applicability matrix (fixed now; INV-Q1–Q3)

Every rule carries an `applicability` entry for all 13 dimensions. For **E1-NOVEL-STRICT**, the V0 primary, the matrix is fixed:

| Dimension | E1-NOVEL-STRICT |
|---|---|
| STUDY_DESIGN, STATISTICAL_STRENGTH, SAMPLE_SIZE, INDEPENDENCE, PHENOTYPE_MATCH, GENOMIC_HARMONIZATION, ALLELE_DIRECTION, POPULATION_ANCESTRY, GENE_ASSIGNMENT, HISTORICAL_NOVELTY, SOURCE_QUALITY | APPLICABLE |
| HETEROGENEITY | APPLICABLE. The criterion applies to meta-analytic discoveries; a single-study discovery satisfies it by recording that it is not a meta-analysis. |
| REPLICATION | NOT_APPLICABLE |

**Why REPLICATION does not apply.** The NOVEL-STRICT event is the first qualifying discovery. Requiring later replication would make positives depend on follow-up effort, and follow-up effort tracks research attention. That would re-introduce the attention bias the design removes. Replication is the endpoint of E1-REPLICATION, a V1 subtype.

- Every criterion is binding (`required: true`).
- A SEAL_CANDIDATE or SEALED NOVEL-STRICT rule has at least one criterion for each applicable dimension and none for REPLICATION.
- The matrices for other subtypes are fixed when those subtypes are introduced (V1).

## Freeze procedure

BIG 0F may estimate feasibility and distributions, but it does not choose thresholds based on Forge Bio model lift.

After provider/outcome feasibility measurements and before any sealed confirmatory generation:

```text
provider audit
→ endpoint-quality candidate rule
→ development-only sensitivity (BIG 0F pilot data only)
→ seal the rule (seal_time before the custodian's first DLVS label release)
→ DLVS
→ confirmatory generation
```

The artifact (status DRAFT → SEAL_CANDIDATE → SEALED; no `frozen_at`) uses:
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

The checklist item for the endpoint evidence-quality **values** stays EMPIRICAL-OPEN until BIG 0F provides the provider and outcome feasibility evidence. The values are then set before the confirmatory seal.


## Executable criterion rule

Comparison operators are executable, not descriptive placeholders:

- `GT / GE / LT / LE` require a numeric operand;
- `EQ / NE` require a scalar operand;
- `IN / NOT_IN` require a non-empty primitive list;
- `REQUIRE` asserts presence/availability and does not require a comparison operand.

A rule with a missing or unusable comparison operand is schema-invalid.
