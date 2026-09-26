# Quantitative Semantics

**Status:** NORMATIVE PRE-CODE V1 — BIG 0R5

## 1. Goal

Prevent silent scientific errors caused by mixing incompatible numeric meanings, units, scales, transforms, references, or measurement processes.

## 2. Core rule

A number without semantic quantity metadata is not a scientific measurement.

```text
value
+
quantity definition
+
unit/dimension
+
scale/transform
+
measurement process
+
context
+
uncertainty
+
provenance
```

## 3. Quantitative types

Required semantic objects:
- QuantityDefinition
- QuantitativeObservation
- EffectEstimate
- MeasurementProcessArtifact
- UnitDefinition
- TransformDefinition
- MissingnessState
- CensoringState
- NumericalUncertainty

## 4. Comparability

Two values are directly comparable only when:
- semantic quantity is compatible;
- units/dimensions are compatible;
- transforms/scales are compatible or explicitly converted;
- reference/comparison definitions are compatible;
- measurement contexts do not invalidate the comparison.

## 5. Transform lineage

Examples:
- raw → normalized;
- concentration → log concentration;
- ratio → log ratio;
- count → rate;
- provider field → standardized feature.

Every transformation records:
- input artifact;
- operation/version;
- fit/reference population if any;
- cutoff;
- output quantity definition;
- provenance/watermark.

## 6. Batch and platform effects

Batch/platform metadata are first-class where they may affect comparability.

A normalization learned on future data is temporal leakage.

## 7. Effect estimates

Effect estimates retain:
- estimand;
- effect-measure kind;
- reference/comparison groups;
- scale/transform;
- uncertainty;
- population/context;
- lineage.

A p-value alone is never treated as an effect estimate.

## 8. Twin integration

T2+ state variables and parameters reference QuantityDefinition.

Numerical/state invariants may include dimensional checks.

Validation compares predicted and observed quantities only after semantic/unit compatibility is established.

## 9. Fail-closed examples

Reject or mark UNKNOWN:
- concentration with no unit where unit matters;
- log hazard ratio compared directly with hazard ratio;
- odds ratio treated as risk ratio;
- normalized expression intensity treated as absolute abundance;
- censored measurement replaced with zero;
- missing value imputed without imputation artifact;
- state variable combined with dimensionally incompatible parameter.
