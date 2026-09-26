# ADR-020 — E1 Primary Gene Endpoint, Nuisance Comparator, and Confirmatory Decision Rule

**Status:** Accepted — BIG 0F-0 critical-path hardening  
**Decision scope:** B-TGT-E1-v0 primary endpoint and confirmatory interpretation

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
DIRECT_CODING_OR_LOF
HIGH_CONFIDENCE_FINE_MAPPING
PREREGISTERED_COLOCALIZATION
OTHER_HIGH_SPECIFICITY_METHOD
```

The exact evidence rule for each class is frozen in the MAP after BIG 0F feasibility measurement.

The following do **not** qualify for the primary gene-level label by themselves:

```text
AUTHOR_NAMED
NEAREST_GENE
POSITIONAL_PROXIMITY_ONLY
GENERIC_DATABASE_GENE_FIELD
MODERN_L2G_ONLY
CURRENT_CURATED_TARGET_ONLY
```

They may be reported as secondary/sensitivity assignments.

If BIG 0F shows that high-specificity gene assignment yields too few events for a scientifically informative confirmatory test, B-TGT-E1-v0 must REDESIGN rather than silently broaden the primary assignment rule.

A locus-level endpoint remains the preferred redesign fallback if gene-level assignment is dominated by attention-sensitive methods.

## 3. Assignment-attention audit

BIG 0F must report:

- share of future events by assignment class;
- fraction relying on AUTHOR_NAMED / NEAREST_GENE;
- Spearman rank correlation between pre-T attention rank and each assignment class;
- event yield after retaining only primary-eligible assignment classes;
- sensitivity of headline conclusions to locus-level one-credit scoring.

A strong attention correlation in author-named assignments is treated as evidence that those labels are unsuitable for the primary endpoint.

## 4. Combined nuisance comparator

The primary comparator is not the strongest single baseline.

Forge Bio must be evaluated incrementally over a preregistered **Combined Nuisance Model** built only from as-of-T non-biological / discoverability variables.

Required nuisance families where historically reconstructable:

```text
research attention / publication volume
attention momentum
global gene popularity
gene annotation density
gene length / gene-model span
variant density or callable/genotyped-variant opportunity
regional gene density
LD / locus architecture summaries
cross-trait pre-T GWAS hit burden / pleiotropy
historical assay / array / measurement observability
disease historical sample-size trajectory
provider/source coverage
```

The exact variables and historical sources are frozen before confirmatory evaluation.

## 5. Primary incremental estimand

The primary scientific contrast is:

```text
Performance(Nuisance + Biological Signal)
-
Performance(Nuisance Only)
```

Both models:
- use the same candidate universe;
- use the same temporal training protocol;
- use matched model-capacity constraints where practical;
- use the same development/validation generations.

Beating random or any single attention baseline is insufficient for a biological-predictive-value claim.

## 6. Primary metric direction

BIG 0F evaluates feasibility of an event-rank-percentile primary metric because sparse events can make Recall@K highly discrete.

Candidate primary form:

```text
DiseaseMacroMean(
    mean percentile rank of qualifying future event genes
)
```

with the paired incremental contrast above.

Recall@K and normalized Recall@x% remain mandatory secondary metrics unless BIG 0F supports keeping one as primary.

## 7. Confirmatory decision rule

Before sealed confirmatory evaluation, the MAP must freeze:

```text
null_hypothesis
alternative_hypothesis
test_statistic
alpha
test_direction
minimum_detectable_or_scientifically_meaningful_effect
power_target
power_analysis_artifact_id
primary_metric_id
primary_comparator_id
success_threshold_numeric
failure_threshold_numeric?
```

A free-text "looks better" threshold is prohibited.

Default planning target for BIG 0F power simulation:

```text
one-sided alpha = 0.05
target power >= 0.80
```

These are planning defaults, not frozen scientific values until BIG 0F supplies realistic event counts/effect variability.

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
3. incremental lift is positive under the frozen confirmatory decision rule;
4. power/precision are adequate for the prespecified effect;
5. confirmatory-generation multiplicity is respected.
