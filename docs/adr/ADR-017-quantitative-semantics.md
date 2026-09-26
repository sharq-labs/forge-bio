# ADR-017 — Quantitative Measurement, Effect, Unit, and Transform Semantics

**Status:** Accepted — BIG 0R5 hardening  
**Decision scope:** quantitative evidence, features, twin state variables, and model outputs

## Problem

Fields such as `effect_size`, `assay_value`, or `unit` are unsafe without precise semantics.

The same numeric value may represent:
- an odds ratio;
- log odds ratio;
- hazard ratio;
- standardized beta;
- concentration;
- fold change;
- probability;
- count;
- normalized assay intensity.

Silent unit/scale/transform mismatch can produce scientifically invalid joins, features, and simulations.

## Decision

Quantitative values use explicit typed semantics.

### QuantityDefinition

```text
QuantityDefinition
    quantity_id
    semantic_kind
    biological_subject
    measurement_endpoint
    context
    canonical_dimension
    preferred_unit?
    valid_range?
    provenance
```

### QuantitativeObservation

```text
QuantitativeObservation
    observation_id
    quantity_definition_id

    value
    unit_id?
    measurement_scale
    transform
    reference_value?
    detection_limit?
    censoring_state?

    uncertainty_representation
    standard_error?
    confidence_interval?
    sample_size?

    measurement_process_id
    normalization_artifact_id?
    batch_id?

    provenance
    availability_attestation
    knowledge_watermark
```

### EffectEstimate

```text
EffectEstimate
    effect_id
    estimand
    effect_measure_kind
    estimate
    scale
    transform
    reference_group
    comparison_group
    standard_error?
    confidence_interval?
    p_value?
    sample_size?
    provenance
```

Initial effect-measure kinds include semantic categories such as:
- DIFFERENCE;
- RATIO;
- ODDS_RATIO;
- RISK_RATIO;
- HAZARD_RATIO;
- REGRESSION_COEFFICIENT;
- STANDARDIZED_EFFECT;
- CORRELATION;
- PROBABILITY.

## Unit/transform rules

- unit-bearing values cannot be combined until dimensional compatibility is verified;
- unit conversion is explicit and provenance-bearing;
- transformed values retain the transform definition;
- log-ratio and ratio values are not interchangeable;
- normalized assay values are not treated as physical concentration;
- reference ranges are context-specific;
- UNKNOWN unit/scale/transform fails closed where numeric comparability is required.

## Measurement process

```text
MeasurementProcessArtifact
    process_id
    assay_or_measurement_type
    platform
    protocol_or_provider_ref
    calibration_ref?
    normalization_ref?
    batch_context?
    limit_of_detection?
    measurement_error_model?
    provenance
    knowledge_watermark
```

The measurement process may itself be knowledge-bearing.

## Missingness and censoring

Missing, below-detection, right-censored, interval-censored, and structurally-not-applicable states are not coerced into numeric zero.

Imputation is a separate provenance-bearing transform.

## Model/twin rule

Twin state variables and parameters reference QuantityDefinition objects.

Numerical solvers receive dimensionally coherent state/parameter definitions.

Model outputs preserve units/scales/transforms so validation compares like with like.

## Consequences

- quantitative evidence becomes composable without silent scale errors;
- twin variables gain unit/dimension discipline;
- measurement/batch effects become auditable;
- effect estimates retain estimand semantics;
- missingness/censoring cannot silently become data.
