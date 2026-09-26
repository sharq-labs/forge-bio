# B-TGT-E1-v0 Estimand Proposal

**Status:** PRE-CODE CANDIDATE — must be accepted/frozen after feasibility pilot

## 1. Target question

For diseases selected from an as-of-T sampling frame in the primary genetic regime, when qualifying future E1 events occur within horizon H, does adding pre-T biological evidence improve future-event gene ranking beyond a preregistered Combined Nuisance Model of attention, discoverability, genomic architecture, pleiotropy, and historical observability?

This is a **conditional ranking estimand**, not a claim that every disease will produce a future qualifying event.

Future positive credit is defined on the frozen ScientificEventFamily / GeneticDiscoveryEventFamily ledger. Multiple manifestations of one discovery do not create multiple primary events, and multiple gene assignments from one locus do not automatically multiply event credit.

## 2. Proposed primary population

Primary V0 regime:

```text
common-complex, germline disease/trait genetics
excluding:
- primary Mendelian/rare-disease benchmark cases
- somatic cancer-driver genetics
- pharmacogenomic endpoints
```

Those regimes may receive separate benchmark families/strata later.

## 3. Frozen disease frame

The disease sampling frame is chosen using only as-of-T criteria.

After frame freeze, diseases remain accounted for even if they later have zero qualifying events.

## 4. Zero-event diseases

A disease with zero qualifying future E1 events is **not deleted**.

Because event-recall ranking metrics are undefined when no future positives exist:
- zero-event diseases are retained in benchmark accounting;
- their count/fraction and characteristics are reported;
- they do not contribute a fabricated 0 or 1 to event-recall unless a different preregistered utility estimand is adopted;
- the primary ranking estimand is explicitly conditional on at least one observable qualifying event;
- no claim of performance across all diseases is inferred from that conditional metric.

The benchmark now also requires a secondary all-frame review-budget estimand that covers zero-event diseases without treating them as negatives.

Historical identity eligibility is analyzed separately from GeneticObservabilityAtT. The MAR reports the primary broad-universe estimand and a preregistered historically-observable sensitivity without constructing either universe from future outcomes.

## 5. Secondary all-frame review-budget estimand

The full frozen disease frame is used to estimate operational search-space efficiency.

A candidate metric is:

```text
ObservedEventYield@TotalReviewBudget =
    observed qualifying future events captured
    /
    total candidates reviewed across all frozen diseases
```

Also report:
- event-bearing disease coverage;
- zero-event disease review burden;
- total candidate review budget;
- ScientificEventFamily deduplication fraction;
- locus-to-many-gene primary-credit sensitivity.

These are **observed-event utility metrics**, not biological precision/false-positive metrics. A zero-event disease does not imply its recommended candidates were biologically false.

## 6. Proposed disease weighting

For the primary event-ranking analysis:
- compute the metric within each event-bearing disease;
- average disease-level results with equal disease weight;
- do not allow a disease with many events to dominate by default.

Event-weighted results may be secondary.

## 7. Proposed comparator

The primary comparator is the preregistered **Combined Nuisance Model**, not the strongest single control.

Primary delta:

```text
metric(nuisance + biological signal)
-
metric(nuisance only)
```

The nuisance model combines historically reconstructable non-biological / detectability predictors, including attention, genomic architecture, cross-trait pleiotropy, observability, and provider/source coverage.

The comparator identity, feature families, capacity constraints, temporal training protocol, and source releases are frozen in MAP.

Single baselines remain diagnostic controls, not the headline comparator.

## 8. Primary metric and candidate-universe normalization

BIG 0F evaluates **event rank percentile** as the preferred primary statistic because sparse events make Recall@K discrete and K-sensitive.

Candidate primary form:

```text
MacroDiseaseMean(
    mean percentile rank of qualifying future event genes
)
```

The primary confirmatory contrast is the paired difference between nuisance+biology and nuisance-only.

Recall@K and Recall@x% remain mandatory secondary metrics unless BIG 0F provides a documented reason to freeze one as primary.

Any final primary metric is selected using DEVELOPMENT-only information and frozen before sealed evaluation.

## 9. Horizon feasibility policy

Candidate horizons are fixed at:

```text
3, 5, 7, 10 years
```

The provider/outcome audit may remove horizons with inadequate observable coverage.

The development procedure selects the smallest remaining H meeting preregistered event-yield, event-bearing-disease, ambiguity/censoring, and CI-width requirements.

The model's lift/performance is not an H-selection criterion.

## 10. Dependence sensitivity

Primary event-bearing-disease analysis uses disease-level paired resampling.

A preregistered disease-family/block resampling sensitivity is also required to test whether shared biology/cohorts/publication ecosystems make ordinary disease-level intervals overconfident.

If results materially weaken under family/block resampling, that limitation is part of the primary interpretation.

Provider-lineage sensitivity is also required when Past inputs and Future outcome sources share material upstream/curation machinery. The primary interpretation must state whether lift survives same-pipeline exclusion or an external-source comparison when feasible.

LD/reference-panel sensitivity is required when proxy-variant matching materially determines replication labels.

## 11. Feasibility decisions still required

The pilot/provider audit must determine:
- exact primary E1 subtype, including strict novelty vs maturation;
- final H;
- whether high-specificity gene-level assignment yields enough events or locus-level redesign is required;
- exact eligible gene-assignment classes;
- primary metric and any K/review-budget secondary metric;
- Combined Nuisance feature set and matched-capacity protocol;
- minimum number of event-bearing diseases;
- acceptable zero-event fraction;
- CI-width requirement;
- simulation-based power target inputs;
- minimum scientifically meaningful effect;
- confirmatory alpha / test direction / test statistic;
- confirmatory-generation multiplicity budget;
- minimum HistoricalGeneticSearchCoverage grade for E1-NOVEL-STRICT;
- acceptable variant/harmonization ambiguity;
- ScientificEventFamily credit policy thresholds if the default one-credit rule needs refinement;
- acceptable Past/Future provider-coupling level;
- observability sensitivity policy details;
- pilot sampling rule, N, second-adjudication fraction, and contamination rule.

Until these are frozen, this document remains PRE-CODE CANDIDATE.


## 12. Assignment-attention robustness

The primary gene-level estimand excludes author-named, nearest-gene, positional-only, generic database-gene, and modern-L2G-only assignments unless they also independently satisfy a preregistered high-specificity assignment class.

BIG 0F reports:
- assignment-class distribution;
- primary-eligible event yield;
- author-named / nearest-gene fractions;
- pre-T attention-rank correlation by assignment class;
- locus-level one-credit sensitivity.

If the primary gene label remains materially attention-coupled or too sparse after restriction, the benchmark REDESIGNS to a locus-level or otherwise attention-resistant primary endpoint.

Normative decision: [adr/ADR-020-e1-primary-comparator-confirmatory-rule.md](adr/ADR-020-e1-primary-comparator-confirmatory-rule.md).
