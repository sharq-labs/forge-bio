# ADR-002 — Historical Candidate Universe

**Status:** Accepted — amended by ADR-011 and ADR-012

## Decision

CandidateUniverse is a separate immutable benchmark artifact, not a field inside HistoricalKnowledgeView.

Candidates must be provably eligible as-of-T. A present-day "all known targets" or "all druggable genes" universe is prohibited in STRICT_HISTORICAL mode unless its own historical provenance passes.

## Why

Candidate-universe leakage can reveal future entities even when every feature record is pre-cutoff.

## Consequences

- universe construction is versioned, hashed, and preregistered;
- membership carries provenance;
- the same HistoricalKnowledgeView may support multiple benchmark universes;
- evaluation reports candidate-universe coverage and sensitivity.


## Amendments

Historical identity eligibility does not imply equal genetic observability.

- ADR-011 defines canonical genomic identity required by genetic evidence/outcome matching.
- ADR-012 requires a separate GeneticObservabilityAtT sensitivity universe built only from as-of-T technology/source criteria.

The primary CandidateUniverse remains broad and identity-valid; observability is a preregistered sensitivity, not a future-outcome-driven exclusion.
