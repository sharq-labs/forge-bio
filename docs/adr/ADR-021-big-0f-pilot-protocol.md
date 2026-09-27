# ADR-021 — BIG 0F Pilot Sampling, Independent Adjudication, and Contamination Control

**Status:** Accepted — BIG 0F-0 critical-path hardening. **Amended by [ADR-022](ADR-022-final-scientific-consistency-closure.md)** (D6, D8, D10, D12, D13, D14). Where they differ, ADR-022 and [V0_FREEZE_STATEMENT.md](../V0_FREEZE_STATEMENT.md) win.  
**Decision scope:** the BIG 0F feasibility pilot before B-TGT-E1 implementation. The "manual pilot" **is** BIG 0F; there is no separate manual pilot (ADR-022 D14).

## 1. Purpose

BIG 0F asks:

> Is a scientifically defensible B-TGT-E1 ground-truth benchmark actually constructible from historical and future data?

It does not estimate final model performance.

## 2. Pilot sampling frame

Pilot cases may not be hand-picked famous examples.

Before adjudication, the independent selection custodian runs custody steps S1–S7 ([BIG_0F_SELECTION_CUSTODY.md](../BIG_0F_SELECTION_CUSTODY.md) §2):

1. The protocol registration is public, with OTS.
2. The five frozen cutoff/horizon predicates are evaluated over the 16 pairs in the fixed order; the first passing pair is (T\*, H\*).
3. The frame is built mechanically by the frame rule ([BIG_0F_FRAME_RULE.md](../BIG_0F_FRAME_RULE.md)), and sampling uses frame_cov(T\*).
4. The selection registration is public and **pre-declares** a drand quicknet round R, with seal_time(S4) ≤ time(R) − 24 h.
5. The disease order is ascending HMAC(key, disease UI), where the key is derived from the frame_cov digest, R and its randomness.
6. All qualifying candidate event **families** for the sampled diseases are included, subject only to the frozen 150-family cap.
7. The seal bundle is registered, and only then are events released to adjudicators.

*Superseded (ADR-022 D13):* "externally timestamp/register the frame digest; obtain a verified public randomness-beacon round **after** the frame seal". A post-seal "first round" on an unpinned chain left grinding room.

Showcase cases may come only from diseases that are already DEVELOPMENT_EXPOSED. Each one is logged in the exposure ledger (custody §4; INV-X4), and none can influence GO/REDESIGN/NO-GO.

## 3. Pilot size

The pilot freezes a target size before adjudication.

Frozen V0 rule:

```text
start with 12 diseases
expand one disease at a time, up to 15, only while < 60 raw candidate event families
retain at most 150 event families under the frozen family-level cap (custody §8)
```

The team does not hand-select N after seeing event quality or ambiguity.

## 4. Independent adjudication

A keyed, stratified set of min(N, max(30, ⌈0.30·N⌉)) pilot cases is independently adjudicated by a second reviewer who is blind to the first reviewer's decision (ADR-022 D8; [BIG_0F_ADJUDICATION_DEFINITIONS.md](../BIG_0F_ADJUDICATION_DEFINITIONS.md) §4).

Report separately for:
- phenotype match;
- gene-assignment class;
- PreTGeneticState;
- HistoricalNoveltyAudit;
- event-family identity;
- sample/cohort overlap.

The gated statistic is Gwet AC1 per gated task, with a lower one-sided 90% BCa bound. It is fixed now. Percent agreement, Cohen κ and the confusion matrix are reported and never gated. *Superseded (ADR-022 D8):* "a chance-corrected agreement statistic when mathematically appropriate". Choosing the statistic after prevalence is seen was a GO lever.

Disagreement remains visible and is adjudicated under a frozen rule.

An independent second adjudicator is a **start gate** for BIG 0F scientific adjudication. If no independent adjudicator is available, case review does not begin.

## 5. Pilot contamination rule

Any disease for which per-disease post-T information reaches the study or ranking team, **by any route**, is permanently tagged as follows (INV-X1; custody §4). *Superseded:* "directly inspected".

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

*Amended by ADR-022 D10.* These outputs feed the **Stage A pool-sufficiency screen** of [BIG_0F_POWER_AND_VARIANCE_POLICY.md](../BIG_0F_POWER_AND_VARIANCE_POLICY.md). The confirmatory variance is measured later, in the Stage B Development Lift & Variance Study.

BIG 0F runs the **nuisance-only** arm and produces:
- event-bearing disease count;
- event count distribution;
- candidate-universe sizes;
- within-disease rank variability;
- nuisance-model performance on DEVELOPMENT cases.

These feed a simulation-based power / precision analysis before a confirmatory generation exists.

## 10. GO / REDESIGN / NO-GO

Numeric thresholds are the gates of `config/big0f-thresholds.v2.json`. They are registered at S1 and sealed in the S6 bundle before adjudication begins (ADR-022 D9).

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
