# B-TGT-E1-v0 Estimand Proposal

**Status:** PRE-CODE CANDIDATE — must be accepted/frozen after feasibility pilot

## 1. Target question

For diseases selected from an as-of-T sampling frame in the primary genetic regime, when qualifying future E1 events occur within horizon H, does Forge Bio rank the event-associated genes higher than preregistered historical attention/discoverability controls?

This is a **conditional ranking estimand**, not a claim that every disease will produce a future qualifying event.

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
- total candidate review budget.

These are **observed-event utility metrics**, not biological precision/false-positive metrics. A zero-event disease does not imply its recommended candidates were biologically false.

## 6. Proposed disease weighting

For the primary event-ranking analysis:
- compute the metric within each event-bearing disease;
- average disease-level results with equal disease weight;
- do not allow a disease with many events to dominate by default.

Event-weighted results may be secondary.

## 7. Proposed comparator

Primary delta:

```text
metric(Forge Bio)
-
metric(strongest preregistered attention/discoverability control)
```

The comparator identity is frozen in MAP.

## 8. Candidate-universe normalization

Fixed K must be paired with at least one normalized metric:
- Recall at x% of candidate universe; or
- event rank percentile.

The final primary pair is selected on development data and frozen before sealed evaluation.

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

## 11. Feasibility decisions still required

The pilot/provider audit must determine:
- exact primary E1 subtype, including strict novelty vs maturation;
- final H;
- primary K/review budget;
- normalized companion metric;
- minimum number of event-bearing diseases;
- acceptable zero-event fraction;
- CI-width requirement.

Until these are frozen, this document remains PRE-CODE CANDIDATE.
