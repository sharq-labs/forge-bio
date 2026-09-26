# ADR-016 — Computational Model Credibility, Numerical Verification, and Applicability

**Status:** Accepted — BIG 0R5 hardening  
**Decision scope:** mechanistic, predictive, and intervention-simulation models

## Problem

Verification, validation, and uncertainty quantification are necessary but not sufficient if they are not tied to the exact research Context of Use.

A model may be technically reproducible yet scientifically unfit because:
- the decision relies too heavily on the model for the available evidence;
- numerical error is not separated from biological/model uncertainty;
- the validation distribution differs from the intended applicability domain;
- model development and evaluation share hidden information;
- model changes invalidate prior validation.

## Decision

Forge Bio uses a **risk-informed research credibility assessment**.

This is inspired by established computational-model credibility principles but is a Forge Bio research governance artifact, not a claim of regulatory compliance.

### CredibilityAssessmentArtifact

```text
CredibilityAssessmentArtifact
    assessment_id
    model_artifact_id
    context_of_use_id

    research_decision
    model_influence
    consequence_if_wrong

    credibility_goal
    verification_adequacy
    numerical_verification_adequacy
    validation_adequacy
    uncertainty_adequacy
    applicability_adequacy
    prediction_risk_of_bias

    known_model_discrepancy
    limitations
    residual_risks

    conclusion
    provenance
    digest
```

### Model influence

```text
ADVISORY
MATERIAL
DOMINANT
```

### Consequence if wrong

For Forge Bio V1 this concerns research consequences such as:
- wasted experimental/review effort;
- incorrect prioritization;
- misleading mechanistic interpretation;
- invalid benchmark claims.

It does not represent patient treatment consequence because patient-specific clinical use is outside V1.

### Credibility conclusion

```text
ADEQUATE_FOR_COU
CONDITIONALLY_ADEQUATE
INADEQUATE
UNKNOWN
```

UNKNOWN never upgrades maturity.

## Numerical verification

T2+ models using numerical simulation require a NumericalVerificationArtifact when applicable.

```text
NumericalVerificationArtifact
    model_artifact_id
    solver_or_engine
    solver_version
    numerical_method
    tolerances
    discretization
    timestep_or_resolution
    convergence_study
    stochastic_replication
    numerical_error_estimate
    invariant_or_residual_checks
    reference_solution_checks
    reproducibility_tolerance
    hardware_runtime_context
    verdict
```

A visually plausible trajectory is not numerical verification.

## Prediction risk / applicability

T3+ evaluation distinguishes:
- model development quality;
- evaluation risk of bias;
- applicability to the intended domain.

Required audit domains:
- data/source population;
- predictors/features;
- outcome/label construction;
- analysis/evaluation.

Shift is assessed across at least:
- time;
- source/provider;
- population/ancestry when relevant;
- phenotype/measurement definition;
- disease/target family;
- assay/platform where relevant.

## Validation scope

Validation attaches to the exact dependency digest.

A material change to:
- model structure;
- parameters;
- feature/preprocessing definitions;
- measurement model;
- solver/numerical configuration;
- update policy;
- endpoint;
- applicability domain

creates a new validation target. Prior validation is not silently inherited.

## Consequences

- twin maturity is supported by fit-for-purpose credibility evidence;
- numerical error is not hidden inside biological uncertainty;
- model-development success is separated from evaluation credibility;
- applicability and distribution shift are explicit;
- validation cannot survive material model changes by name alone.
