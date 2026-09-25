# ADR-002 — Historical Candidate Universe

**Status:** Proposed for freeze before coding

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
