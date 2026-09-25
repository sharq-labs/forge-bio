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

The central question is whether the platform shows reproducible lift over **historical research attention**, **historical discoverability / observation opportunity**, and other trivial popularity/evidence-volume baselines.

A model that mainly predicts what researchers were about to study or what was easiest to measure has not demonstrated biological discovery value.

## Initial benchmark families

- **B-TGT — Target Discovery:** establishes biological prioritization signal.
- **B-REP — Drug Repurposing:** tests whether biological signal translates into therapeutic prioritization.

The first proposed benchmark is **B-TGT-E1-v0**, a narrow disease–gene target-association benchmark evaluated against later independent human genetic support.

E1 is no longer treated as one undifferentiated endpoint. The design separates:
- **E1-NOVEL** — genuinely new post-cutoff human genetic support;
- **E1-REPLICATION** — later independent maturation/replication of a pre-T weak signal;
- **E1-CROSSMODAL** — pre-T non-genetic evidence anticipating later genetics.

The benchmark also governs locus→gene assignment, historical novelty auditing, cohort/sample independence, discoverability bias, zero-event diseases, and researcher hindsight.

It does not claim intervention-direction or clinical validation.

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
- [Scientific Red-Team Gap Register](docs/SCIENTIFIC_RED_TEAM_GAPS.md)
- [ADR-006 — Outcome Gene Assignment and Historical Novelty](docs/adr/ADR-006-outcome-gene-assignment.md)
- [ADR-007 — Benchmark Design Provenance and Analyst Blinding](docs/adr/ADR-007-benchmark-design-provenance.md)
- [Architecture Decision Records](docs/adr/)

## Current unresolved P0 decisions

The readiness checklist and red-team gap register are authoritative.

Important unresolved P0 work now includes:
- licensing posture;
- BIG 0 schemas/artifacts promised by the master plan;
- scientific estimand and zero-future-event disease policy;
- disease/genetic regime for B-TGT-E1;
- final E1 primary subtype and evidence-quality rule;
- candidate H feasibility;
- manual outcome-feasibility pilot;
- locus→gene outcome-assignment policy operationalization;
- HistoricalNoveltyAudit operationalization;
- discoverability/observation-propensity control definition;
- analyst-hindsight / blinding governance;
- lockbox custody;
- scientific-spec repository governance.

Do **not** start production scientific code while any P0 blocker remains active.

Once P0 is closed, run a final red-team review against the frozen commit. Only then declare **GO FOR CORE SCIENTIFIC CODE**.
