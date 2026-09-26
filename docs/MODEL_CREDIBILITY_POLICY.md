# Model Credibility Policy

**Status:** NORMATIVE PRE-CODE V1 — BIG 0R5

## 1. Principle

A model is credible only relative to a defined Context of Use.

Forge Bio does not assign a universal "validated model" label.

```text
Model M
credible for CoU A
!=
Model M credible for CoU B
```

## 2. Credibility dimensions

Every T2+ model records:
- code/model verification;
- numerical verification where applicable;
- data/measurement adequacy;
- parameter estimation adequacy;
- model-form discrepancy;
- validation adequacy;
- uncertainty adequacy;
- applicability/domain adequacy;
- development/evaluation separation;
- prediction risk-of-bias audit.

## 3. Model discrepancy

```text
ModelDiscrepancyAssessment
    represented_mechanisms
    omitted_mechanisms
    known_simplifications
    unresolved_structural_uncertainty
    calibration_compensation_risk
    impact_on_cou
```

Calibration must not be used to hide structural model error.

## 4. Numerical verification

Required for numerical simulation when applicable:
- solver/engine/version;
- method/order;
- tolerances;
- timestep/grid/resolution;
- convergence/refinement study;
- residual/invariant checks;
- stochastic replicate/Monte Carlo error;
- reference/analytic/synthetic solution checks when available;
- numerical error estimate;
- reproducibility tolerance across supported environments.

Bitwise identity is not required when scientifically justified floating-point/stochastic tolerance is frozen.

## 5. Parameter adequacy

For parameterized mechanistic models:
- parameter source/provenance;
- structural identifiability status;
- practical identifiability/estimability where applicable;
- parameter uncertainty;
- correlation/sloppiness warning;
- sensitivity to parameter priors/constraints;
- calibration dataset cutoff and separation from validation.

## 6. Predictive evaluation risk audit

T3+ requires a structured audit of:
- data/source selection;
- feature/predictor construction;
- outcome/label derivation;
- analysis/evaluation.

The audit records leakage, selection, missingness, censoring, dependence, sample size, class/event sparsity, and adaptive reuse risks.

## 7. Applicability and shift

```text
ApplicabilityDomain
    population_scope
    disease_scope
    phenotype_scope
    source_scope
    measurement_scope
    temporal_scope
    intervention_scope?
```

Required shift checks are chosen from:
- temporal;
- source/provider;
- population/ancestry;
- disease/family;
- target/family;
- measurement/platform;
- prevalence/base-rate;
- intervention regime.

A T3 result outside the evaluated applicability domain is extrapolation, not validated prediction.

## 8. Calibration and scoring

If probabilistic outputs are claimed:
- probability endpoint/horizon is explicit;
- held-out calibration is required;
- calibration intercept/slope or equivalent is reported where meaningful;
- at least one proper scoring rule is frozen;
- discrimination alone is insufficient;
- recalibration creates a new model artifact/version.

## 9. Validation invalidation

Validation is scoped to a dependency digest.

Material changes create a new model-validation target, including:
- state/model structure;
- feature set;
- preprocessing;
- parameterization;
- measurement model;
- solver configuration that materially changes outputs;
- endpoint/label policy;
- applicability domain;
- update policy.

## 10. Stop rule

Do not upgrade model/twin maturity if:
- numerical error is uncontrolled;
- key parameters are non-identifiable for the claimed use;
- predictive validation is biased or non-independent;
- applicability is outside the evaluated domain;
- model discrepancy dominates the claimed signal;
- uncertainty is materially under-characterized.
