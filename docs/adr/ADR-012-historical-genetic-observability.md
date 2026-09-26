# ADR-012 — Historical Genetic Observability and Novelty Coverage

**Status:** Accepted — BIG 0R3 hardening  
**Decision scope:** E1-NOVEL-STRICT and historical genetic-state classification

## Problem

"No signal observed before T" is only meaningful relative to the search/measurement coverage available before T.

A poorly studied disease and a deeply studied disease must not receive the same novelty confidence merely because neither has a qualifying recorded signal.

## Decision

Every pre-T genetic-state assessment carries a `HistoricalGeneticSearchCoverage` artifact.

```text
HistoricalGeneticSearchCoverage
    disease_id
    cutoff
    source_coverage
    study_count
    aggregate_sample_size
    ancestry_coverage
    phenotype_coverage
    genome_or_variant_class_coverage
    technology_coverage
    summary_statistics_availability
    search_completeness_grade
    provenance
```

Coverage grade:

```text
HIGH
MODERATE
LOW
UNKNOWN
```

The MAP freezes the minimum grade required for E1-NOVEL-STRICT.

If coverage is below the frozen threshold:

```text
PreTGeneticState != NO_SIGNAL_OBSERVED
PreTGeneticState = AMBIGUOUS
```

unless a stronger source-backed reason exists.

## Public knowledge vs ranker knowledge

The benchmark distinguishes:

```text
KNOWN_TO_RANKER_AT_T
KNOWN_PUBLICLY_AT_T
```

A publication may have been public before T but absent from the historical provider snapshot.

Such a case is:
- a provider/reconstruction coverage failure;
- not a genuinely novel future discovery.

## Historical observability sensitivity

Candidate identity eligibility and genetic observability are distinct.

The primary universe remains broad and historically identity-valid.

A required sensitivity artifact records:

```text
GeneticObservabilityAtT
    candidate_id
    disease_id
    cutoff
    technology_classes_available
    ascertainment_feasibility
    variant_classes_observable
    evidence_sources_available
    observability_grade
    provenance
```

The MAR compares the broad universe against a preregistered historically-observable sensitivity universe without using future outcomes to construct it.

## Consequences

- low historical study coverage cannot masquerade as strict novelty;
- benchmark failures can be separated into model failure vs provider-coverage failure;
- technological measurement opportunity becomes explicit rather than hidden inside discoverability;
- novelty ambiguity becomes measurable during BIG 0F.
