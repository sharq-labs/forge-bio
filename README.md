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
- evidence-backed disease/pathogen/therapeutic scientific profiles
- time-indexed Scientific Digital Twins with explicit maturity/validation gates

## What Forge Bio is not

Forge Bio is not:

- a system that calls a static graph/profile a validated predictive digital twin
- a patient diagnosis system
- a treatment recommender
- a dosing system
- clinical decision support
- a system that claims computational predictions are proven therapies
- a pharmaceutical synthesis/manufacturing workflow
- an LLM whose output is treated as scientific truth

The platform produces **research hypotheses for further scientific investigation**.

## Scientific operating modes

Scientific claim mode and historical-data sourcing are separate axes.

**ScientificOperatingMode**
1. **STRICT_HISTORICAL** — all model-visible knowledge must be defensibly admissible by cutoff T.
2. **HISTORICAL_INPUT_MODERN_PRIOR** — historical explicit inputs may use modern/unknown-horizon priors, but the run is labelled contaminated and cannot support a strict historical claim.
3. **CURRENT_DISCOVERY** — current evidence/models are allowed for present-day research prioritization only.

**HistoricalDataPolicy**
- **ARCHIVED_ONLY**
- **RECONSTRUCTED_ALLOWED** — only when reconstruction fidelity and watermarks pass the frozen policy.

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

- **B-TGT — Target Program:** umbrella program for biological/target prioritization. Its first benchmark is intentionally narrower than "target discovery".
- **B-REP — Drug Repurposing:** tests whether biological signal translates into therapeutic prioritization.

The first proposed benchmark is **B-TGT-A1 / B-TGT-E1-v0 — Disease–Gene Association Prioritization**, evaluated against later independent human genetic support.

E1 is explicitly split into:
- **E1-NOVEL-STRICT** — no observed pre-T genetic signal after adequate audit, followed by qualifying post-T support;
- **E1-MATURATION** — a suggestive pre-T signal later becomes qualifying;
- **E1-REPLICATION** — genuine independent replication under allele/direction/phenotype/lineage rules;
- **E1-CROSSMODAL** — pre-T non-genetic evidence anticipating later genetics.

The benchmark also governs:
- canonical genomic variant/locus identity;
- genome-build/liftover/allele harmonization;
- LD/reference-panel provenance;
- historical genetic-search coverage and observability;
- locus→gene assignment;
- disease/trait phenotype matching;
- pre-T signal-state auditing;
- replication comparability;
- cohort/dataset/biobank/SampleSet identity and independence;
- ScientificEventFamily deduplication and one-event-family credit;
- Past/Future provider-lineage coupling;
- cross-anchor event reuse;
- discoverability bias;
- zero-event disease review burden;
- validation-set reuse;
- immutable Future Outcome snapshots;
- researcher hindsight.

A positive V0 result is evidence about **disease–gene association prioritization**, not therapeutic-target validation or clinical efficacy.

## Pre-code status

Current phase: **Pre-Code Hardening / BIG 0R3 + BIG 0R4 + BIG 0R5 → BIG 0F**

BIG 0R4 and BIG 0R5 are parallel platform-hardening extensions and do not block the B-TGT-E1 manual feasibility pilot.

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
- [Scientific Glossary](docs/GLOSSARY.md)
- [Core Scientific Types](docs/CORE_TYPES.md)
- [Golden Synthetic Biomedical World](docs/GOLDEN_SYNTHETIC_WORLD.md)
- [Golden Scientific Twin World](docs/GOLDEN_TWIN_WORLD.md)
- [Architecture Dependency Rules](docs/DEPENDENCY_RULES.md)
- [Prohibited Dependency / Leakage Fixtures](docs/PROHIBITED_DEPENDENCY_FIXTURES.md)
- [B-TGT-E1 Estimand Proposal](docs/BENCHMARK_ESTIMAND_V0.md)
- [Scientific Specification Governance](docs/SCIENTIFIC_SPEC_GOVERNANCE.md)
- [Lockbox Policy](docs/LOCKBOX_POLICY.md)
- [QoI Schema](docs/schemas/QOI_SCHEMA.md)
- [Context-of-Use Schema](docs/schemas/CONTEXT_OF_USE_SCHEMA.md)
- [MAP Schema](docs/schemas/MAP_SCHEMA.md)
- [MAR Schema](docs/schemas/MAR_SCHEMA.md)
- [Machine-Verifiable JSON Schemas](schemas/README.md)
- [Repository License](LICENSE)
- [Disease / Pathogen / Therapeutic Profile Model](docs/DISEASE_PATHOGEN_THERAPEUTIC_PROFILE.md)
- [Forge Bio Scientific Twin Architecture](docs/SCIENTIFIC_DIGITAL_TWIN_ARCHITECTURE.md)
- [Model Credibility Policy](docs/MODEL_CREDIBILITY_POLICY.md)
- [Quantitative Semantics](docs/QUANTITATIVE_SEMANTICS.md)
- [Scientific Twin JSON Schema](schemas/scientific-twin.v1.schema.json)
- [ADR-006 — Outcome Gene Assignment and Historical Novelty](docs/adr/ADR-006-outcome-gene-assignment.md)
- [ADR-007 — Benchmark Design Provenance and Analyst Blinding](docs/adr/ADR-007-benchmark-design-provenance.md)
- [ADR-008 — Outcome Phenotype Matching](docs/adr/ADR-008-outcome-phenotype-matching.md)
- [ADR-009 — Genetic Replication and Pre-T Signal State](docs/adr/ADR-009-genetic-replication-and-signal-state.md)
- [ADR-010 — Validation Generations and Outcome Snapshot Commitment](docs/adr/ADR-010-validation-generations-and-outcome-freeze.md)
- [ADR-011 — Genomic Identity, Harmonization, and LD Provenance](docs/adr/ADR-011-genomic-identity-harmonization.md)
- [ADR-012 — Historical Genetic Observability and Novelty Coverage](docs/adr/ADR-012-historical-genetic-observability.md)
- [ADR-013 — Scientific Event Identity, Source Coupling, and Adaptive Reuse](docs/adr/ADR-013-event-identity-source-coupling.md)
- [ADR-014 — Scientific Operating Mode vs Historical Data Policy](docs/adr/ADR-014-operating-mode-data-policy.md)
- [ADR-015 — Scientific Digital Twin Semantics](docs/adr/ADR-015-scientific-digital-twin-semantics.md)
- [ADR-016 — Model Credibility & Numerical Verification](docs/adr/ADR-016-model-credibility-numerical-verification.md)
- [ADR-017 — Quantitative Semantics](docs/adr/ADR-017-quantitative-semantics.md)
- [Architecture Decision Records](docs/adr/)

## Current unresolved P0 decisions

The readiness checklist and red-team gap register are authoritative.

Important unresolved P0 work is now limited to evidence-bearing feasibility decisions:
- final frozen B-TGT-E1 estimand after feasibility evidence;
- final primary E1 subtype and endpoint evidence-quality threshold;
- manual outcome-feasibility pilot and its ambiguity/coverage/curation/lineage measurements;
- pilot GO / REDESIGN / NO-GO verdict.

ADR-005 is decided: commercial-later engineering posture; repository code/docs Apache-2.0; provider-data licenses remain source-specific.

The V0 primary genetic regime, H candidate procedure, strict novelty/maturation semantics, genomic identity/harmonization/LD provenance, phenotype-match policy, locus→gene policy, genetic-replication policy, historical-search coverage, observability sensitivity, ScientificEventFamily accounting, provider-coupling controls, cross-anchor reuse, validation-generation rules, immutable outcome-snapshot commitment, analyst-hindsight governance, lockbox mechanism, executable schemas, core types, golden world, and dependency rules are now specified.

Do **not** start production scientific code while any P0 blocker remains active.

Once P0 is closed, run a final red-team review against the frozen commit. Only then declare **GO FOR CORE SCIENTIFIC CODE**.


## Forge Bio Scientific Twins

Forge Bio uses a project-defined **research Scientific Twin** maturity hierarchy rather than treating every model as a clinical/health digital twin:

```text
T0_PROFILE_ONLY
→ T1_DYNAMIC_KNOWLEDGE_TWIN
→ T2_MECHANISTIC_TWIN
→ T3_VALIDATED_PREDICTIVE_TWIN
→ T4_VALIDATED_INTERVENTION_SIMULATION_TWIN
```

For infectious disease, the architecture distinguishes the pathogen from the disease and supports a **Pathogen–Host Scientific Twin** so viral/pathogen biology and host response are not collapsed into one object.

T3/T4 claims require explicit validation, uncertainty quantification, and applicability limits. Simulation output remains a research hypothesis, not patient-specific medical advice.
