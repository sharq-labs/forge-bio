# Forge Bio Scientific Twin Architecture

**Status:** NORMATIVE PRE-CODE CANDIDATE — BIG 0R4

**Terminology scope:** "Forge Bio Scientific Twin" is a project-defined research construct. It is not presented as a patient/clinical health digital twin merely by using the word twin.

## 1. Goal

Create reusable, versioned computational representations of diseases, pathogens, pathogen–host systems, and therapeutics that can evolve with evidence and—only when scientifically justified—support validated simulation or prediction.

## 2. Why a hierarchy is required

A database, graph, or dashboard is not automatically a digital twin.

Forge Bio uses explicit maturity levels:

| Level | Canonical enum | Minimum capability |
|---|---|---|
| T0 | T0_PROFILE_ONLY | structured evidence-backed profile |
| T1 | T1_DYNAMIC_KNOWLEDGE_TWIN | versioned state updated from new evidence |
| T2 | T2_MECHANISTIC_TWIN | explicit state-transition / mechanistic model |
| T3 | T3_VALIDATED_PREDICTIVE_TWIN | predicts held-out/future observations with quantified uncertainty |
| T4 | T4_VALIDATED_INTERVENTION_SIMULATION_TWIN | validated research simulation of defined perturbations/interventions |

No artifact may claim a maturity level it has not passed.

## 3. Twin object

```text
ScientificDigitalTwin
    twin_id
    twin_family
    subject_entity_ids

    maturity_level

    scientific_operating_mode
    historical_data_policy

    profile_snapshot_ids
    evidence_snapshot_ids

    cutoff?

    state_definition_id
    state_model_artifact_id?
    parameter_artifact_ids

    update_policy_artifact_id

    prediction_spec_id?
    map_id?
    mar_ids
    validation_generation_id?
    benchmark_design_provenance_id?

    perturbation_artifact_ids
    sensitivity_artifact_ids
    causal_assumption_set_id?
    intervention_semantics_id?
    identifiability_status

    verification_artifact_ids
    validation_artifact_ids

    uncertainty_bundle
    applicability_domain

    knowledge_watermark
    created_at
    valid_at
    digest
```

## 4. Twin families

```text
DISEASE_TWIN
PATHOGEN_TWIN
PATHOGEN_HOST_TWIN
THERAPEUTIC_TWIN
```

Future families may include:
- organ/cell/tissue systems;
- pathway/mechanism twins;
- tumor-system twins;
- population twins.

Patient-specific twins are excluded from V1.

## 5. Dynamic state

T1+ twins expose versioned state.

For STRICT_HISTORICAL and HISTORICAL_INPUT_MODERN_PRIOR, the twin object itself carries an explicit `cutoff`. `valid_at` is not a substitute for the historical admission boundary.

```text
TwinState
    state_id
    twin_id
    effective_time
    cutoff
    state_variables
    evidence_snapshot_ids
    parameter_artifact_ids
    uncertainty_bundle
    knowledge_watermark
    digest
```

Updates never overwrite scientific history.

```text
TwinState v1
→ evidence update
→ TwinState v2
```

Both remain addressable.

## 6. Mechanistic state models

T2+ requires an explicit state model.

The **state-model structure itself is knowledge-bearing unless proven otherwise**. A model topology, manually chosen mechanism, causal edge set, state variable set, or transition rule may encode later biomedical knowledge even when its numeric parameters were fitted only on historical data.

Therefore use:

```text
TwinStateModelArtifact
    state_model_artifact_id
    structure_definition
    model_family
    structural_assumption_ids
    source_evidence_ids
    created_from_snapshot_ids
    knowledge_bearingness
    knowledge_watermark
    provenance
    digest

TwinUpdatePolicyArtifact
    update_policy_artifact_id
    update_rule
    source_dependencies
    knowledge_bearingness
    knowledge_watermark
    provenance
    digest
```

The twin watermark joins profile/evidence, state-model structure, update policy, parameters, mappings, representations, and any other knowledge-bearing dependency.

Examples of allowed model families include:
- causal/state-transition graphs;
- differential-equation systems;
- probabilistic graphical models;
- agent-based models;
- hybrid mechanistic/statistical models;
- other transparent simulation models.

The architecture does not mandate one mathematical formalism.

Each state variable and parameter references a QuantityDefinition and records:
- meaning;
- dimension/unit where applicable;
- scale/transform;
- estimation method;
- source evidence;
- uncertainty;
- temporal admissibility;
- applicability domain.

## 6.1 Numerical verification

For models that use numerical solvers/simulation engines, T2+ requires a NumericalVerificationArtifact when applicable.

It records:
- solver/engine/version;
- numerical method;
- tolerances;
- timestep/grid/resolution;
- convergence/refinement evidence;
- stochastic replication error where relevant;
- invariant/residual checks;
- numerical error estimate;
- reproducibility tolerance.

A plausible trajectory or solver-to-solver agreement is not sufficient by itself.

Numerical uncertainty is reported separately from biological, measurement, parameter, and model-form uncertainty.

## 6.2 Model credibility

Twin maturity is not enough by itself.

A T2+ model also receives a Context-of-Use-specific CredibilityAssessmentArtifact covering:
- model influence on the research decision;
- consequence if wrong;
- verification adequacy;
- numerical verification;
- validation;
- uncertainty;
- applicability;
- risk of bias;
- model discrepancy.

Normative policy: [MODEL_CREDIBILITY_POLICY.md](MODEL_CREDIBILITY_POLICY.md).

## 7. Predictive validation

T3 cannot be declared because a model fits existing data.

It requires a frozen validation target and held-out/future evaluation.

```text
TwinValidationArtifact
    validation_id
    twin_id
    model_version
    map_id
    mar_id
    validation_generation_id
    benchmark_design_provenance_id
    prediction_target
    prediction_horizon
    dataset_snapshot_ids
    split_policy
    metric_ids
    calibration_result
    uncertainty_evaluation
    applicability_evaluation
    failure_analysis
    digest
```

## 8. Intervention simulation and causal claim boundary

T4 is research simulation only.

A perturbation operator is not automatically a causal intervention. T4 therefore requires an explicit:

```text
CausalAssumptionSet
InterventionSemantics
IdentifiabilityStatus
```

Allowed maturity-supporting identifiability states are:

```text
IDENTIFIED
PARTIALLY_IDENTIFIED
ASSUMPTION_DEPENDENT
```

`NOT_IDENTIFIED` or `UNKNOWN` cannot support T4 maturity.

A favorable associational simulation cannot be relabelled as an intervention effect.

A perturbation is a formal computational experiment:

```text
TwinPerturbation
    perturbation_id
    target_entity_or_state
    direction_or_operation
    context
    model_version
    parameterization
    assumptions
```

Output:

```text
TwinSimulationResult
    perturbation_id
    predicted_state_change
    uncertainty
    sensitivity_analysis
    applicability_domain
    provenance
```

Simulation output is a hypothesis, not evidence that a therapy works clinically.

## 9. Historical twins

A core Forge Bio capability is time-indexed twin reconstruction:

```text
Twin(subject, T)
```

A T2/T3/T4 historical twin is valid only if:
- the twin has an explicit cutoff T;
- model-visible evidence is admissible at T;
- state-model structure/transition rules are admissible at T;
- update-policy knowledge is admissible at T;
- parameters are fit only from data allowed by T;
- feature/preprocessing artifacts obey T;
- future outcomes are excluded from fitting and model choice;
- future observations are used only in the evaluation plane.

This enables questions such as:

> Could the scientific twin as-of-T have anticipated later observations?

## 10. Pathogen–host twin

For infectious disease:

```text
PathogenTwin
      +
HostContext
      ↓
PathogenHostTwin
      ↓
DiseaseMechanismState
      ↓
Target / Therapeutic Hypotheses
```

The PathogenHostTwin may include:
- pathogen lifecycle states;
- pathogen proteins;
- host receptors/factors;
- tissue/cell context;
- immune response states;
- disease phenotypes;
- resistance state;
- therapeutic target hypotheses.

No pathogenic engineering or experimental manipulation instructions are part of this architecture.

## 11. Twin update pipeline

```text
new source snapshot
→ temporal qualification
→ identity resolution
→ claim/evidence update
→ contradiction/gap update
→ profile snapshot
→ twin state update
→ verification
→ optional prediction/simulation
→ validation
```

A future record cannot silently rewrite an older historical twin.

## 12. VVUQ contract

Verification, Validation, and Uncertainty Quantification are required progressively.

### Verification

Checks:
- schema integrity;
- units/types;
- dependency DAG;
- deterministic replay;
- conservation/domain invariants where relevant;
- historical watermark integrity;
- state-transition integrity.

### Validation

T3/T4 validation reuses the platform's existing governance rather than creating a parallel regime:
- frozen MAP;
- MAR;
- ValidationGeneration;
- BenchmarkDesignProvenance;
- lockbox/outcome commitments where the validation target uses sealed future outcomes.

Checks:
- held-out/future predictive performance;
- calibration where probabilities are emitted;
- at least one proper scoring rule for probability claims;
- external-source validation where possible;
- temporal/source/population/phenotype/measurement shift as applicable;
- subgroup/applicability/OOD behavior;
- negative/null controls;
- prediction-study risk-of-bias audit.

### Uncertainty

Distinguish at least:
- measurement uncertainty;
- sampling uncertainty;
- parameter uncertainty;
- numerical uncertainty;
- model-form uncertainty;
- evidence uncertainty;
- mapping uncertainty;
- temporal uncertainty;
- applicability uncertainty.

## 13. Stop rule

Do not advance a twin from T1/T2 to T3/T4 merely because simulation output looks plausible.

If predictive validation fails:
- maturity remains lower;
- failure is recorded;
- simulation may remain exploratory;
- clinical/therapeutic claims are not upgraded.
