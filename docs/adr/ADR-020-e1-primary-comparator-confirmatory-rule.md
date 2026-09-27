# ADR-020 — E1 Primary Gene Endpoint, Nuisance Comparator, and Confirmatory Decision Rule

**Status:** Accepted — BIG 0F-0 critical-path hardening  
**Decision scope:** B-TGT-E1-v0 primary endpoint and confirmatory interpretation  
**Amended by:** [ADR-022](ADR-022-final-scientific-consistency-closure.md) (§4 nuisance family list superseded by D11; confirmatory test fixed by D18). [V0_FREEZE_STATEMENT.md](../V0_FREEZE_STATEMENT.md) takes precedence.

## 1. Problem

A positive disease–gene result is not scientifically persuasive if:
- the future gene label is primarily the gene named by discovery-paper authors;
- the comparator omits genomic architecture / cross-trait pleiotropy;
- the confirmatory result has no frozen decision rule or power target.

These failure modes can make a literature-aware ranker appear biologically predictive while it is only predicting which genes are easier to implicate or more likely to be named.

## 2. Primary gene-assignment eligibility

The primary B-TGT-E1-v0 gene-level endpoint uses a **high-specificity assignment set** frozen before confirmatory evaluation.

Initial eligible assignment classes:

```text
HYPOTHESIS_FREE_CODING_OR_LOF
HIGH_CONFIDENCE_FINE_MAPPING
PREREGISTERED_COLOCALIZATION
```

The class definitions are frozen **before BIG 0F adjudication** in `config/big0f-adjudication-policy.v2.json` (`BIG0F-ADJUDICATION-V2`; [BIG_0F_ADJUDICATION_DEFINITIONS.md](../BIG_0F_ADJUDICATION_DEFINITIONS.md) §1).

A primary gene-level positive additionally requires hypothesis-free study ascertainment (GENOME_WIDE, EXOME_WIDE, or BIOBANK_WIDE). Targeted candidate-gene studies are secondary only. `OTHER_HIGH_SPECIFICITY_METHOD` does not exist in V0 (`other_high_specificity_method_allowed: false`).

The following do **not** qualify for the primary gene-level label by themselves:

```text
AUTHOR_NAMED
NEAREST_GENE
POSITIONAL_PROXIMITY_ONLY
GENERIC_DATABASE_GENE_FIELD
MODERN_L2G_ONLY
CURRENT_CURATED_TARGET_ONLY
TARGETED_CANDIDATE_GENE_CODING
```

They may be reported as secondary/sensitivity assignments.

If BIG 0F shows that high-specificity gene assignment yields too few events for a scientifically informative confirmatory test, B-TGT-E1-v0 must REDESIGN rather than silently broaden the primary assignment rule.

A locus-level endpoint remains the preferred redesign fallback if gene-level assignment is dominated by attention-sensitive methods. It is a V1 redesign, not a V0 option ([V0_FREEZE_STATEMENT.md](../V0_FREEZE_STATEMENT.md) §4).

## 3. Assignment-attention audit

BIG 0F must report:

- share of future events by assignment class;
- fraction relying on AUTHOR_NAMED / NEAREST_GENE;
- a preregistered attention/assignment association with confidence interval, computed over all adjudicated post-T event families in the pilot with no separate matched sample ([BIG_0F_ADJUDICATION_DEFINITIONS.md](../BIG_0F_ADJUDICATION_DEFINITIONS.md) §5);
- event yield after retaining only primary-eligible assignment classes;
- sensitivity of headline conclusions to locus-level one-credit scoring.

A strong attention correlation in author-named assignments is treated as evidence that those labels are unsuitable for the primary endpoint.

## 4. Combined nuisance comparator

The primary comparator is not the strongest single baseline.

Forge Bio must be evaluated incrementally over a preregistered **Combined Nuisance Model** built from as-of-T variables intended to capture research attention, measurement opportunity, genomic detectability/architecture, pleiotropy, and other alternative explanations for future discovery.

"Nuisance" does **not** mean "non-biological". Gene geometry, LD architecture, variant opportunity, and pleiotropy are biological/genomic properties. They are placed in the comparator because they can predict future discovery without demonstrating Forge Bio's disease-specific hypothesis-evidence contribution.

Required nuisance families — the 14 mandatory families of `config/big0f-nuisance-manifest.v2.json` (ADR-022 D11), which is the normative list and holds each family's level, class, as-of-T definition and transform:

```text
DISEASE_SPECIFIC_ATTENTION_VOLUME
DISEASE_SPECIFIC_ATTENTION_MOMENTUM
GLOBAL_ATTENTION_VOLUME
GLOBAL_ATTENTION_MOMENTUM
GLOBAL_GENE_POPULARITY
ANNOTATION_DENSITY
GENE_LENGTH
VARIANT_OPPORTUNITY
REGIONAL_GENE_DENSITY
LD_ARCHITECTURE
CROSS_TRAIT_PLEIOTROPY
GENETIC_OBSERVABILITY
DISEASE_SAMPLE_SIZE_TRAJECTORY
PROVIDER_COVERAGE
```

> Superseded by ADR-022 D11: the earlier prose family list here ("where historically reconstructable") and the v1 manifest.

The mandatory nuisance **families** are frozen before BIG 0F in `config/big0f-nuisance-manifest.v2.json`; execution follows [BIG_0F_NUISANCE_EXECUTION_CONTRACT.md](../BIG_0F_NUISANCE_EXECUTION_CONTRACT.md). The disease-specific attention terms are content-free counts/momentum and may not encode semantic evidence strength.

If a mandatory family cannot be historically reconstructed, the result is REDESIGN; the family is not silently dropped from the headline comparator.

## 5. Primary incremental estimand

The primary scientific contrast is:

```text
Performance(Ascertainment/Opportunity Comparator + Disease-Specific Hypothesis Evidence)
-
Performance(Ascertainment/Opportunity Comparator Only)
```

Both models:
- use the same candidate universe;
- use the same temporal training protocol;
- use the same development/validation generations;
- use the same learner family;
- use the exact same nuisance feature block;
- use the same hyperparameter search space, tuning budget, early-stopping rules, random-seed policy, and preprocessing family;
- differ only by the addition of the preregistered disease-specific hypothesis-evidence feature block in the primary nested comparison.

The primary comparison is invalid if learner family, preprocessing, hyperparameter search space, tuning budget, early stopping, or seed policy differs between arms. These parity commitments are first-class MAP fields.

The primary contrast also carries the K = 19 permuted-biology placebo guard, run with the same learner, search space and budget ([V0_FREEZE_STATEMENT.md](../V0_FREEZE_STATEMENT.md) §3 item 5; MAP `comparison_design.placebo_arm_policy_id`).

Beating random or any single attention baseline is insufficient for a biological-predictive-value claim.

## 6. Primary metric direction

B-TGT-E1-v0 fixes `EVENT_RANK_PERCENTILE_V1` as its primary metric. BIG 0F evaluates whether enough events exist to make that metric scientifically useful; it does not choose a different primary metric after inspecting the pilot.

The canonical definition (filtered competitor set, mid-rank ties, family credit, disease-macro mean) is [METRIC_EVENT_RANK_PERCENTILE_V1.md](../METRIC_EVENT_RANK_PERCENTILE_V1.md), used with the paired incremental contrast above.

> Superseded by ADR-022 D3: the earlier informal form "DiseaseMacroMean(mean percentile rank of qualifying future event genes)".

Recall@K and normalized Recall@x% remain mandatory secondary (companion) metrics and are never promoted to primary in V0 (INV-E9).

## 7. Confirmatory decision rule

Before sealed confirmatory evaluation, the MAP must freeze:

```text
null_hypothesis
alternative_hypothesis
test_statistic_id
alpha
test_direction
minimum_scientifically_meaningful_effect
power_target
power_analysis_artifact_id
primary_metric_id
primary_comparator_id
success_threshold_numeric
success_threshold_semantics
success_rule_ref
```

(Field names as in `schemas/map.v1.schema.json`; see [MAP_SCHEMA.md](../schemas/MAP_SCHEMA.md).)

A free-text "looks better" threshold is prohibited.

For V0 the confirmatory test and success rule are fixed in [V0_FREEZE_STATEMENT.md](../V0_FREEZE_STATEMENT.md) §3: a one-sided paired sign-flip test on the mean disease contrast Δ̄, plus the BLOCKING analyses of the closed §3a list (placebo guard, leave-one-disease-out) and the §28 preconditions. The MAP's `success_threshold_numeric` is the p-value threshold (`success_threshold_semantics = ONE_SIDED_P_VALUE_STRICTLY_BELOW`), and `success_rule_ref` points to Freeze Statement §3.

Default planning target for BIG 0F power simulation:

```text
one-sided alpha = 0.05
target power >= 0.80
```

For V0, one-sided alpha = 0.05 and the minimum scientifically meaningful rank-fraction effect = 0.05 are frozen before adjudication. The 0.05 effect is a planning effect for power only; it is never a success threshold (INV-E7). BIG 0F supplies only the inputs of the Stage A pool-sufficiency screen; the planning variance for confirmation comes from the Stage B Development Lift & Variance Study ([BIG_0F_POWER_AND_VARIANCE_POLICY.md](../BIG_0F_POWER_AND_VARIANCE_POLICY.md)). Neither stage gives permission to tune the effect from biological-model performance.

## 8. Research-program multiplicity

The confirmatory program must freeze:
- maximum number of confirmatory generations;
- alpha-spending / family-wise decision policy across confirmatory generations;
- which cutoffs/horizons/subtypes are DEVELOPMENT only;
- conditions that force a new independent generation.

Development attempts do not consume confirmatory alpha if their outcomes can never support a confirmatory claim and are recorded in the ResearchProgramAttempt ledger.

Repeated failed confirmatory generations cannot be reset indefinitely by renaming a benchmark.

## 9. Consequences

A positive B-TGT-E1 result can support a biological-predictive-value claim only if:
1. primary outcomes use the frozen high-specificity gene-assignment rule;
2. the combined nuisance model is the primary comparator;
3. incremental lift is positive under the frozen confirmatory decision rule ([V0_FREEZE_STATEMENT.md](../V0_FREEZE_STATEMENT.md) §3, including the placebo guard);
4. power/precision are adequate for the prespecified effect, as established before the seal by the Stage B gate. This is a design precondition, not an outcome-time veto;
5. confirmatory-generation multiplicity is respected (p < the generation's allocated α; INV-L11).

The closed sensitivity list of Freeze Statement §3a applies. No other analysis can grant or veto success.


## 10. Comparator fairness and over-control

The Combined Nuisance Model is an **alternative-explanation comparator**, not a claim that all its inputs are scientifically uninteresting or non-biological.

The MAP classifies every nuisance feature family as one of:

```text
ATTENTION
MEASUREMENT_OPPORTUNITY
GENOMIC_DETECTABILITY
GENOMIC_ARCHITECTURE
PLEIOTROPY
PROVIDER_COVERAGE
OTHER_PREREGISTERED_ALTERNATIVE_EXPLANATION
```

In V0 each family's class is fixed in `config/big0f-nuisance-manifest.v2.json`; its schema (`schemas/big0f-nuisance-manifest.v2.schema.json`) allows only the first six classes.

A feature that is itself part of Forge Bio's intended disease-specific biological hypothesis signal must not be moved into the nuisance block merely because doing so lowers measured lift.

Conversely, a feature chosen because it strongly predicts outcome discovery on development data cannot be omitted from nuisance without a frozen scientific justification.

BIG 0F does **not** compare the Forge biological arm against nuisance. It runs nuisance-only headroom diagnostics under the already-frozen nuisance family manifest. The eventual confirmatory nuisance block cannot omit mandatory disease-specific attention volume/momentum because doing so improves apparent biological lift.
