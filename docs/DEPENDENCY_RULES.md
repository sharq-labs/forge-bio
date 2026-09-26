# Architecture Dependency Rules

**Status:** NORMATIVE PRE-CODE V1

These rules define allowed dependency direction for the modular monolith.

## 1. Core rule

Past/ranking code must be structurally unable to import Future Outcome implementation.

The evaluation boundary is the only place allowed to combine sealed historical predictions with future outcomes.

## 2. Intended dependency direction

```text
kernel
  ↑
temporal     provenance     uncertainty
  ↑              ↑
identity         |
  ↑              |
providers/corpus |
  ↑              |
evidence --------+
  ↑
knowledge
  ↑
profiles
  ↑
twins
  ↑
hypotheses
  ↑
ranking

outcomes  <--- separate scientific plane
   ↑
validation/evaluation  <--- only layer allowed to read ranking + outcomes

benchmarks/experiments
   orchestrate frozen capabilities/specs
   but may not bypass module boundaries

reporting
   consumes immutable artifacts/results
```

## 3. Module rules

### kernel
May depend only on generic standard/library utilities.

Must not import biomedical providers, outcomes, ranking, or current ontologies.

### temporal
May depend on kernel/provenance abstractions.

Must not depend on FutureEvent labels or ranking results.

### identity
May depend on kernel/temporal/provenance.

Historical identity code must not import evaluation bridge implementations.

### providers
Adapters expose source facts and provenance.

Past-provider adapters must not import outcomes or label derivation.

### evidence
May consume historical identity, temporal decisions, source records, and provenance.

Must not import model rankings as independent biological evidence.

### knowledge
Builds cutoff-specific projections from admitted evidence.

Must not access unrestricted provider APIs or future storage at runtime.

### profiles

Build evidence-backed Disease/Pathogen/PathogenHost/Therapeutic profile snapshots from admitted identity/evidence/knowledge capabilities.

Historical profile construction must not import:
- FutureEvent/outcome repositories;
- evaluation-only identity bridges;
- unrestricted current/latest providers;
- ranking results as biological evidence.

### twins

Twin construction receives only:
- frozen profile snapshots;
- admitted evidence snapshots;
- HistoricalKnowledgeView or current-discovery equivalent;
- versioned state-model/update-policy/parameter artifacts allowed by the run mode.

STRICT_HISTORICAL / HISTORICAL_INPUT_MODERN_PRIOR twin construction must not import:
- FutureEvent/outcome repositories;
- lockbox readers;
- evaluation-only identity bridges;
- unrestricted current/latest provider clients;
- future validation labels/results.

Twin prediction/simulation output is not written back as EvidenceRecord.

State-model structure, update policies, parameter artifacts, manually selected mechanism graphs, and pretrained representations are scientific dependencies and obey provenance/KnowledgeWatermark rules.

### hypotheses/ranking
Receive HistoricalKnowledgeView + CandidateUniverse only.

Must not import:
- outcome repositories;
- evaluation bridge;
- lockbox readers;
- unrestricted DB/storage clients;
- current provider "latest" clients.

### outcomes
Owns FutureEvent, novelty audit, outcome assignment, and label derivation.

Must not mutate historical evidence or candidate universes.

### validation/evaluation
May read:
- sealed ranking artifact;
- frozen twin prediction/simulation artifact;
- frozen MAP;
- Future Outcome plane;
- evaluation-only identity bridge.

Twin validation is performed here rather than inside twin-construction modules when future/sealed outcomes are required.

Must not retroactively modify ranking/config/features.

## 4. Boundary enforcement

Required techniques:
- package/import contract tests;
- dependency graph test;
- forbidden symbol/module fixtures;
- profile/twin import-wall tests;
- future-sentinel tests against historical twin construction;
- model-structure/update-policy watermark tests;
- separate credentials/configuration for future storage;
- network-disabled confirmatory ranking runtime where feasible;
- capability interfaces instead of raw database handles.

## 5. Fail-closed rule

A newly introduced dependency crossing a forbidden boundary fails CI/verification.

It is not waived because the code path "isn't used in production yet".

## 6. Scientific-data side inputs

Configuration files, lookup tables, manually curated constants, embeddings, model weights, and ontology files are dependencies.

If they carry biomedical knowledge they require:
- provenance;
- KnowledgeBearingness;
- KnowledgeWatermark;
- inclusion in dependency/hash manifests.

"Just a config file" is not an exemption.
