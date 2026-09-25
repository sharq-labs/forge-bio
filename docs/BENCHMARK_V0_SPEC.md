# Benchmark V0 Specification

**Status:** PRE-CODE CANDIDATE  
**Benchmark family:** B-TGT  
**Benchmark ID:** B-TGT-E1-v0

## 1. Question of Interest

> Given only evidence admissible by historical cutoff T, can Forge Bio rank disease–gene biological target-association candidates that later acquire new independent human genetic support within a fixed horizon H, with positive lift over historical research-attention baselines?

This is deliberately narrower than "predict the correct treatment". B-TGT-E1-v0 tests biological target-prioritization signal. It does not validate intervention direction, drug efficacy, or clinical success.

## 2. Unit of prediction

The V0 rankable object is:

```text
TargetAssociationCandidate
    disease_concept_as_of_T
    gene_entity_as_of_T
```

Intervention direction remains part of the broader platform model but is not validated by this endpoint. A later direction-aware benchmark evaluates full TargetHypothesis objects against mechanistic/functional endpoints.

## 3. Cutoff selection

The cutoff is not hard-coded. BIG 1 evaluates candidate eras approximately 2005–2014 using provider qualification.

The chosen T must satisfy preregistered minimums for:
- historical provider fidelity;
- disease and gene identity coverage;
- candidate-universe completeness;
- outcome-source coverage;
- sufficient future observation horizon.

The selected cutoff becomes immutable inside the MAP.

## 4. Future horizon

H is a fixed duration, not "until today". Candidate H values may be explored on development data for event yield and censoring, then frozen before sealed evaluation.

## 5. Positive endpoint: E1

A candidate is POSITIVE only when a qualifying post-cutoff event occurs in (T, T+H] and the relationship was not KNOWN_AT_T.

A qualifying event must:
1. contain human genetic evidence for the disease–gene relationship;
2. satisfy the predeclared evidence-quality rule;
3. be independently source-backed;
4. be publicly available after T;
5. map to the historical disease and gene only through the evaluation-side identity bridge;
6. not be merely a post-T re-curation of a pre-T evidence item already visible to the model.

The precise quality threshold is a BenchmarkSpec parameter frozen before confirmatory evaluation.

## 6. KNOWN_AT_T

A candidate is KNOWN_AT_T when the same endpoint, or a benchmark-declared stronger equivalent, is already established by admissible evidence at or before T.

KNOWN_AT_T candidates may appear in a separate rediscovery track and may support explicitly defined nested temporal training, but are excluded from primary future-discovery metrics.

The Future Outcome plane must never be used to determine KNOWN_AT_T.

## 7. Non-positive states

**NEGATIVE_CONFIRMED:** used only when an affirmative preregistered failure definition is satisfied. Absence of later human genetic support is not a negative.

**UNKNOWN:** no qualifying positive event is observed and the available evidence does not justify a negative.

**RIGHT_CENSORED:** the complete horizon cannot be observed because T+H exceeds the outcome data end or material source coverage is missing.

**CONFLICTED / AMBIGUOUS:** identity or outcome evidence prevents a defensible state.

## 8. Candidate universe

CandidateUniverse is a separate immutable artifact from HistoricalKnowledgeView.

```text
CandidateUniverse
    universe_id
    benchmark_family
    cutoff
    disease_set_id
    entity_class
    inclusion_policy_version
    exclusion_policy_version
    source_snapshot_ids
    identity_policy_version
    knowledge_watermark
    candidate_ids
    digest
```

Eligibility requires:
- gene entity known/admissible by T;
- disease concept known/admissible by T;
- benchmark-specific inclusion rule satisfied.

The universe may not be built from a present-day "all known targets" list.

## 9. Disease sampling frame

Diseases must not be selected because designers know famous later successes.

Before outcome inspection, construct the sampling frame using only information admissible at T. Freeze:
- disease vocabulary/release as-of-T;
- minimum historical evidence/publication coverage;
- exclusions;
- research-intensity strata;
- disease-family strata;
- candidate-universe-size strata.

Development and sealed diseases are sampled from this frame. Manual additions are reported separately.

## 10. Future-event independence

A later database row is not automatically independent validation.

Every OutcomeEvent carries:
- outcome_event_id;
- endpoint_type;
- event_time;
- first_publicly_available_interval;
- source artifact/record IDs;
- upstream study/evidence IDs;
- independence_family_id;
- derivation_type;
- evaluation identity-bridge version.

A post-T annotation that only re-curates pre-T evidence does not qualify as new independent support.

## 11. Baselines

Mandatory:
- random;
- historical disease–gene publication/co-mention attention;
- global gene/entity popularity;
- admissible evidence-volume ranking;
- deterministic evidence-quality baseline.

Graph degree or network proximity is optional only when historically admissible.

## 12. Primary statistic

Report absolute performance and a paired delta against research attention.

Candidate primary statistic:

```text
DeltaRecall@K = Recall@K(model) - Recall@K(attention_baseline)
```

K is selected on development cases and frozen before sealed evaluation.

Secondary metrics may include Recall at a percentage of the candidate universe, event MRR, preregistered NDCG, enrichment versus random, rank percentile, and per-disease distributions.

## 13. Confidence interval

The primary baseline delta uses paired disease-level resampling. Candidate rows within one disease are not treated as independent observations.

The MAP freezes resampling unit, resample count, interval method, and multiplicity policy.

## 14. Coverage gates

Confirmatory studies freeze:
- maximum UNKNOWN fraction per required source;
- minimum identity-resolved candidate fraction;
- minimum outcome coverage across H;
- minimum admitted-evidence coverage.

Cases failing hard thresholds are INVALID_CASE or excluded only according to the preregistered policy; they are never silently repaired.

## 15. Success criterion

A sealed confirmatory claim requires all of:
1. no unresolved P0 temporal-integrity violation;
2. ranking sealed before outcome access;
3. primary delta above the preregistered threshold;
4. confidence interval satisfying the preregistered rule;
5. result not driven by one disease/candidate family;
6. sensitivity analyses showing no material identity/reconstruction artifact.

Numerical thresholds are chosen on development data and frozen in the MAP.

## 16. What this benchmark does not prove

It does not prove clinical actionability, intervention direction, drug existence, efficacy, safety, causality, or treatment success.

It is the first test of whether temporally clean evidence contains useful biological prioritization signal beyond historical research attention.
