# ADR-015 — Disease, Pathogen, Therapeutic, and Scientific Digital Twin Semantics

**Status:** Accepted — BIG 0R4 hardening  
**Decision scope:** disease/pathogen/therapeutic representation and digital-twin terminology

## Problem

Forge Bio already models diseases, phenotypes, genes, proteins, pathways, genomic evidence, and future events, but it does not yet define a complete scientific profile for:

- diseases;
- pathogens/viruses;
- therapeutics.

Calling a static knowledge graph a "digital twin" would overclaim capability.

## Decision

Forge Bio introduces a **Scientific Digital Twin hierarchy**.

A twin is not a patient-specific clinical model in V1. It is a versioned research object that represents a biological system, its evidence state, uncertainty, and—at higher maturity—validated dynamic or predictive behavior.

### Twin maturity

```text
T0_PROFILE_ONLY
T1_DYNAMIC_KNOWLEDGE_TWIN
T2_MECHANISTIC_TWIN
T3_VALIDATED_PREDICTIVE_TWIN
T4_VALIDATED_INTERVENTION_SIMULATION_TWIN
```

Rules:

- T0 is not called a digital twin in scientific claims.
- T1 requires dynamic evidence-backed state updates and full provenance.
- T2 requires an explicit mechanistic/state-transition model.
- T3 requires predictive validation against held-out or future observations.
- T4 requires validated intervention/perturbation simulation for research use.
- a level is never inferred from model complexity alone;
- each higher level inherits all lower-level requirements;
- uncertainty, applicability, and validation status are first-class.

## Twin families

### DiseaseScientificTwin

Represents a disease/trait concept and its evolving scientific state.

### PathogenScientificTwin

Represents a pathogen taxon, strain, or variant and its biological state.

### PathogenHostScientificTwin

Represents pathogen–host interaction as a system-of-systems.

For infectious disease, this is the preferred predictive/mechanistic abstraction when host biology materially determines disease behavior.

### TherapeuticScientificTwin

Represents an active moiety, therapeutic modality, medicinal product, or intervention class and its evidence state.

## Claim boundary

A twin may support research hypotheses and simulations.

It does not, by itself:
- diagnose a person;
- recommend patient treatment;
- prescribe dose;
- establish clinical efficacy;
- establish safety;
- replace clinical trials or experimental validation.

## Temporal rule

Every twin can be materialized **as-of-T**.

```text
ScientificTwinSnapshot
    twin_id
    subject_entity_id
    cutoff
    admitted_evidence_snapshot_ids
    state_model_version
    parameter_artifact_ids
    uncertainty_bundle
    knowledge_watermark
    validation_status
    digest
```

A historical twin cannot contain future evidence through parameters, mappings, pretrained representations, or state-model calibration.

## Validation rule

Predictive/intervention twin levels require explicit:

- verification tests;
- calibration/fit provenance;
- held-out or future validation;
- uncertainty quantification;
- applicability domain;
- failure cases;
- versioned model and parameter artifacts.

## Consequences

- static profiles and predictive twins are not conflated;
- disease/pathogen/therapeutic knowledge becomes reusable across benchmark families;
- infectious-disease modeling can explicitly represent pathogen–host interaction;
- historical time-machine experiments can instantiate twins as-of-T;
- future patient-specific digital twins remain out of V1 Context of Use.
