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

1. evaluate cutoff/horizon pairs in the fixed lexicographic order from BIG_0F_PROTOCOL;
2. construct an as-of-T disease frame mechanically from frozen vocabulary/regime rules;
3. externally timestamp/register the frame digest;
4. obtain a verified public randomness-beacon round **after** the frame seal;
5. derive the disease order with the frozen external-beacon hash-sort algorithm;
6. include all qualifying candidate outcome events for sampled diseases within the pilot horizon, subject only to the frozen 150-event cap rule.

Manual showcase cases may be examined separately and cannot influence GO/REDESIGN/NO-GO.

## 3. Pilot size

The pilot freezes a target size before adjudication.

Frozen V0 rule:

```text
start with 12 diseases
expand deterministically up to 15 only if <60 candidate events
retain 60–150 candidate events under the frozen cap rule
```

The team does not hand-select N after seeing event quality or ambiguity.

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

An independent second adjudicator is a **start gate** for BIG 0F scientific adjudication. If no independent adjudicator is available, case review does not begin.

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

Before GO, audit at least 4 candidate source families for:
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
attention_assignment_association_with_ci
hypothesis_free_primary_positive_fraction
label_feature_method_coupling_fraction
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
nuisance_top1_positive_fraction
```

## 9. Power simulation input

BIG 0F runs the **nuisance-only** arm and produces:
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
