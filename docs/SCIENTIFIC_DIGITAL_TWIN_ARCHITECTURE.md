# Scientific Digital Twin Architecture

**Status:** NORMATIVE PRE-CODE CANDIDATE — BIG 0R4

## 1. Goal

Create reusable, versioned computational representations of diseases, pathogens, pathogen–host systems, and therapeutics that can evolve with evidence and—only when scientifically justified—support validated simulation or prediction.

## 2. Why a hierarchy is required

A database, graph, or dashboard is not automatically a digital twin.

Forge Bio uses explicit maturity levels:

| Level | Name | Minimum capability |
|---|---|---|
| T0 | PROFILE_ONLY | structured evidence-backed profile |
| T1 | DYNAMIC_KNOWLEDGE_TWIN | versioned state updated from new evidence |
| T2 | MECHANISTIC_TWIN | explicit state-transition / mechanistic model |
| T3 | VALIDATED_PREDICTIVE_TWIN | predicts held-out/future observations with quantified uncertainty |
| T4 | VALIDATED_INTERVENTION_SIMULATION_TWIN | validated research simulation of defined perturbations/interventions |

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

    state_definition_id
    state_model_id?
    parameter_artifact_ids

    update_policy_id

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

Examples of allowed model families include:
- causal/state-transition graphs;
- differential-equation systems;
- probabilistic graphical models;
- agent-based models;
- hybrid mechanistic/statistical models;
- other transparent simulation models.

The architecture does not mandate one mathematical formalism.

Each state variable and parameter records:
- meaning;
- units where applicable;
- estimation method;
- source evidence;
- uncertainty;
- temporal admissibility;
- applicability domain.

## 7. Predictive validation

T3 cannot be declared because a model fits existing data.

It requires a frozen validation target and held-out/future evaluation.

```text
TwinValidationArtifact
    validation_id
    twin_id
    model_version
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

## 8. Intervention simulation

T4 is research simulation only.

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

A T3/T4 historical twin is valid only if:
- model-visible evidence is admissible at T;
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

Checks:
- held-out/future predictive performance;
- calibration where probabilities are emitted;
- external-source validation where possible;
- subgroup/applicability behavior;
- negative/null controls.

### Uncertainty

Distinguish at least:
- measurement uncertainty;
- parameter uncertainty;
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
