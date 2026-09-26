# ADR-019 — Source Lifecycle, Benchmark Exposure, External Sealing, and Prospective Independence

**Status:** Accepted — final research-program integrity hardening  
**Decision scope:** evidence lifecycle, benchmark reuse, lockbox credibility, and prospective validation independence

## Problem

A benchmark can remain internally correct yet lose confirmatory credibility through repeated exposure, source revisions, or intervention by the research program itself.

Critical risks include:
- a source being corrected, retracted, withdrawn, or superseded;
- repeated adaptive use of the same benchmark/outcomes;
- inability to prove when a ranking/artifact was sealed relative to evaluation;
- public predictions changing research attention and thereby influencing later outcomes;
- provider/ontology/schema changes silently altering historical or evaluation artifacts.

## 1. Source lifecycle

Every scientific source may receive versioned lifecycle events.

```text
SourceLifecycleEvent
    event_id
    source_artifact_id
    event_type
    event_public_time
    effective_time?
    replacement_or_correction_ref?
    reason
    provenance
    digest
```

Initial event types:

```text
CORRECTED
RETRACTED
EXPRESSION_OF_CONCERN
WITHDRAWN
SUPERSEDED
RESTORED
```

### Historical rule

Historical reconstruction uses the source status publicly knowable at cutoff T.

A retraction/correction announced after T:
- does not retroactively erase what a historical actor could have seen at T;
- is invisible to STRICT_HISTORICAL ranking at T;
- is recorded in current/evaluation metadata;
- triggers a sensitivity analysis if the historical rank materially depended on the affected source.

A retraction/correction public before T is part of the historical state at T.

## 2. Benchmark exposure lifecycle

Repeated use of a validation/benchmark outcome set is itself a scientific dependency.

```text
BenchmarkExposureEvent
    benchmark_generation_id
    exposure_time
    exposure_kind
    disclosure_level
    disclosed_artifacts
    audience
    downstream_change_ref?
    provenance
```

```text
BenchmarkGenerationLifecycle
    ACTIVE_CONFIRMATORY
    DEVELOPMENT_EXPOSED
    EXHAUSTED
    RETIRED
```

A generation becomes DEVELOPMENT_EXPOSED when results influence:
- endpoint definitions;
- feature construction;
- model choice;
- thresholds;
- candidate-universe rules;
- adjudication policy;
- disease selection;
- source/provider selection.

Repeated exposure can move the generation to EXHAUSTED.

EXHAUSTED generations remain useful for regression/research history but cannot support a new strongest confirmatory claim.

## 3. External sealing / timestamp attestation

For strongest confirmatory or prospective work, internal Git hashes alone are insufficient evidence of study sequencing.

```text
ExternalSealAttestation
    attestation_id
    artifact_digest
    artifact_type
    sealed_at
    external_registry_or_custodian_ref
    attestation_method
    signer_or_service_identity
    verification_status
    provenance
```

The exact implementation may use an independent custodian or third-party timestamp/registration mechanism.

External sealing proves artifact existence/commitment at a study time. It does not prove that researchers never saw historical future outcomes before study design; analyst-hindsight governance remains separately required.

## 4. Prospective prediction exposure

Publishing predictions can change research behavior.

```text
PredictionExposureEvent
    prediction_artifact_id
    exposure_time
    exposure_scope
    audience
    target_visibility
    publication_or_release_ref?
    contamination_risk
    provenance
```

Prospective outcome labels distinguish:

```text
UNEXPOSED_PROSPECTIVE
EXPOSURE_POSSIBLE
EXPOSURE_CONFIRMED
UNKNOWN_EXPOSURE
```

A later result that may have been causally influenced by a public Forge Bio prediction is not treated as clean independent prospective validation without sensitivity/qualification.

## 5. Schema/provider/ontology drift

Material source-schema, ontology, mapping, or provider-pipeline changes create new versioned artifacts.

Migrations preserve:
- source version;
- target version;
- migration rule/version;
- changed semantics;
- affected artifacts;
- reproducibility impact;
- provenance/digest.

Frozen historical artifacts are never silently rewritten in place.

## Consequences

- retractions/corrections do not create hidden temporal paradoxes;
- repeated benchmark reuse cannot masquerade as fresh confirmation;
- strongest prospective claims gain an external sequencing attestation;
- self-fulfilling research attention is separated from independent prediction;
- schema/ontology/provider drift becomes explicit and reproducible.
