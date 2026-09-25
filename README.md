# Forge Bio

Forge Bio is a **computational therapeutic hypothesis discovery and historical validation platform**.

It is designed to answer a narrow scientific question:

> Given only biomedical information that was genuinely available at time **T**, can a computational system prioritize disease mechanisms, therapeutic targets, and later existing-drug hypotheses that subsequently receive predefined independent validation?

The project is **benchmark-first**, not AI-first. Historical validity, provenance, evidence semantics, uncertainty, identity, and reproducibility are first-class requirements.

## What Forge Bio is

Forge Bio is a research platform for:

- temporally controlled biomedical evidence
- disease → mechanism → target prioritization
- later disease → existing active-moiety / drug repurposing prioritization
- supporting evidence, counter-evidence, and explicit gaps
- uncertainty and applicability reporting
- sealed historical benchmarking
- prospective shadow validation

## What Forge Bio is not

Forge Bio is not:

- a patient diagnosis system
- a treatment recommender
- a dosing system
- clinical decision support
- a system that claims computational predictions are proven therapies
- a pharmaceutical synthesis/manufacturing workflow
- an LLM whose output is treated as scientific truth

The platform produces **research hypotheses for further scientific investigation**.

## Scientific operating modes

1. **STRICT_HISTORICAL** — all model-visible knowledge must be defensibly admissible by cutoff T.
2. **HISTORICAL_INPUT_MODERN_PRIOR** — historical explicit inputs may use modern/unknown-horizon priors, but the run is labelled contaminated and cannot support a strict historical claim.
3. **CURRENT_DISCOVERY** — current evidence/models are allowed for present-day research prioritization only.

## Core architecture

A ranker never receives unrestricted storage plus a cutoff parameter.

It receives:

```text
HistoricalKnowledgeView
+
CandidateUniverse
```

The Historical Knowledge plane and Future Outcome plane are isolated. A confirmatory ranking is frozen and hashed before future labels are opened.

## Scientific north star

Beating random is insufficient.

The central question is whether the platform shows reproducible lift over **historical research attention** and other trivial popularity/evidence-volume baselines.

## Initial benchmark families

- **B-TGT — Target Discovery:** establishes biological prioritization signal.
- **B-REP — Drug Repurposing:** tests whether biological signal translates into therapeutic prioritization.

The first proposed benchmark is **B-TGT-E1-v0**, a narrow disease–gene target-association benchmark evaluated against later independent human genetic support. It does not claim intervention-direction or clinical validation.

## Pre-code status

Current phase: **Pre-Code Hardening / BIG 0**

The high-level architecture is stable, but V1 is not frozen until every P0 item in the readiness checklist is closed or explicitly superseded by ADR.

Do not start production scientific code before that gate.

## Core documents

- [Architecture V1 Candidate](docs/ARCHITECTURE_V1.md)
- [Scientific Contract V1 Candidate](docs/SCIENTIFIC_CONTRACT.md)
- [Scientific Master Plan](docs/SCIENTIFIC_MASTER_PLAN.md)
- [Benchmark V0 Specification](docs/BENCHMARK_V0_SPEC.md)
- [Temporal Semantics](docs/TEMPORAL_SEMANTICS.md)
- [Evidence Taxonomy](docs/EVIDENCE_TAXONOMY.md)
- [Identity Policy](docs/IDENTITY_POLICY.md)
- [Provider Qualification](docs/PROVIDER_QUALIFICATION.md)
- [Model Training Policy](docs/MODEL_TRAINING_POLICY.md)
- [Pre-Code Readiness Checklist](docs/PRE_CODE_CHECKLIST.md)
- [Architecture Decision Records](docs/adr/)

## Current unresolved P0 decisions

The readiness checklist is authoritative. At present, the remaining owner/research decisions include:

- licensing posture
- final B-TGT-E1 evidence-quality rule
- candidate H values / feasibility procedure
- lockbox custody mechanism

Once P0 is closed, the next step is a final red-team review. Only then do we declare **GO FOR BIG 0 CODE**.
