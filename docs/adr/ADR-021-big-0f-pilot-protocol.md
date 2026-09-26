# ADR-021 — BIG 0F Pilot Sampling, Independent Adjudication, and Contamination Control

**Status:** Accepted — BIG 0F-0 critical-path hardening  
**Decision scope:** manual feasibility pilot before B-TGT-E1 implementation

## 1. Purpose

BIG 0F asks:

> Is a scientifically defensible B-TGT-E1 ground-truth benchmark actually constructible from historical and future data?

It does not estimate final model performance.

## 2. Pilot sampling frame

Pilot cases may not be hand-picked famous examples.

Before adjudication:

1. choose candidate cutoff T from the predeclared feasibility range;
2. construct an as-of-T disease frame mechanically from the frozen disease vocabulary/regime rules;
3. externally seal the frame digest and random seed;
4. draw diseases reproducibly;
5. include all qualifying candidate outcome events for sampled diseases within the pilot horizon, or apply a frozen random event-sampling rule when volume is excessive.

Manual showcase cases may be examined separately and cannot influence GO/REDESIGN/NO-GO.

## 3. Pilot size

The pilot freezes a target size before adjudication.

Initial planning range:

```text
8–15 diseases
60–150 candidate outcome events
```

This is a planning range, not a claim that the upper count is available.

The actual frozen N is chosen from a pre-pilot source-availability count without inspecting event labels/ambiguity decisions.

## 4. Independent adjudication

At least 30% of pilot cases are independently adjudicated by a second reviewer blind to the first reviewer's decision.

Report separately for:
- phenotype match;
- gene-assignment class;
- PreTGeneticState;
- HistoricalNoveltyAudit;
- event-family identity;
- sample/cohort overlap.

Report percent agreement plus a chance-corrected agreement statistic when mathematically appropriate.

Disagreement remains visible and is adjudicated under a frozen rule.

If no independent adjudicator is available:
- BIG 0F may proceed as DEVELOPMENT;
- strongest claim ceiling is explicitly reduced;
- the missing independence is not marked "passed".

## 5. Pilot contamination rule

All diseases/events directly inspected during BIG 0F are permanently tagged:

```text
DEVELOPMENT_EXPOSED
```

They may:
- inform policy redesign;
- appear in documentation/examples;
- be used for development/regression tests.

They may not enter a future strongest-tier sealed confirmatory generation.

## 6. Symmetric historical audit

BIG 0F measures the cost of PreTGeneticState / novelty review on:
- future positive candidate events; and
- a frozen random sample of candidate non-event disease–gene pairs.

This tests whether the historical audit can be applied symmetrically enough to avoid positivity-conditioned adjudication.

## 7. Mini provider-availability audit

Before GO, audit at least 3–4 candidate source families for:
- archived/as-of-T availability;
- field-level historical availability;
- version/release identifiers;
- retrospective curation;
- identity mapping requirements;
- licensing/access constraints.

A source being available today is not evidence that its historical representation can be reconstructed.

## 8. Required measurements

BIG 0F reports at least:

```text
events_per_disease
events_per_E1_subtype
assignment_class_distribution
author_named_fraction
nearest_gene_fraction
primary_eligible_assignment_fraction
attention_vs_assignment_rank_correlation
phenotype_ambiguity
novelty_ambiguity
historical_search_coverage
variant_harmonization_ambiguity
preT_cohort_reuse_fraction
event_family_deduplication_fraction
locus_to_many_gene_sensitivity
provider_coupling
sample_overlap_ambiguity
retrospective_curation_burden
ancestry_metadata_coverage
second_adjudicator_agreement
symmetric_non_event_audit_cost
archived_source_field_availability
combined_nuisance_model_headroom
```

## 9. Power simulation input

BIG 0F produces:
- event-bearing disease count;
- event count distribution;
- candidate-universe sizes;
- within-disease rank variability;
- nuisance-model performance on DEVELOPMENT cases.

These feed a simulation-based power / precision analysis before a confirmatory generation exists.

## 10. GO / REDESIGN / NO-GO

Numeric thresholds must be externally sealed before adjudication begins.

The threshold document distinguishes:
- hard STOP conditions;
- REDESIGN triggers;
- GO requirements.

Thresholds must cover at least:
- ambiguity;
- adjudicator agreement;
- high-specificity gene-assignment yield;
- provider availability;
- event-bearing disease count;
- power/precision;
- nuisance-model headroom;
- curation burden.

## 11. Claim boundary

Passing BIG 0F means only:

> a defensible confirmatory benchmark appears constructible.

It does not mean Forge Bio predicts future biology.
