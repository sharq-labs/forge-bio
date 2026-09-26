# ADR-014 — Scientific Operating Mode vs Historical Data Policy

**Status:** Accepted — BIG 0R3 hardening  
**Decision scope:** temporal configuration semantics

## Problem

Two different concepts were previously expressed with overlapping "mode/policy" names:

- whether a run makes a strict historical scientific claim;
- how historical data are sourced/reconstructed.

Conflating them risks invalid enum combinations and silent contamination.

## Decision

Use two orthogonal axes.

### ScientificOperatingMode

```text
STRICT_HISTORICAL
HISTORICAL_INPUT_MODERN_PRIOR
CURRENT_DISCOVERY
```

### HistoricalDataPolicy

```text
ARCHIVED_ONLY
RECONSTRUCTED_ALLOWED
```

Provider/field qualification remains separate:

```text
HISTORICAL_SAFE
HISTORICAL_CONDITIONAL
CURRENT_ONLY
FUTURE_VALIDATION_ONLY
PROHIBITED_FOR_BENCHMARK
UNKNOWN
```

A strict run may use RECONSTRUCTED_ALLOWED only when every reconstruction-dependent field passes the frozen Reconstruction Fidelity gate and all model-visible knowledge watermarks remain <= T.

"CONTAMINATED_MODERN_PRIOR" is a run classification/outcome, not a HistoricalDataPolicy enum.

## Consequences

Examples:

```text
STRICT_HISTORICAL + ARCHIVED_ONLY
STRICT_HISTORICAL + RECONSTRUCTED_ALLOWED
HISTORICAL_INPUT_MODERN_PRIOR + RECONSTRUCTED_ALLOWED
CURRENT_DISCOVERY + any current-provider policy
```

The runtime validates combinations explicitly.
