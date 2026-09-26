# Machine-Verifiable Scientific Schemas

These JSON Schemas are machine-readable specification companions to the normative Markdown contracts.

Files:
- `qoi.v1.schema.json`
- `map.v1.schema.json`
- `mar.v1.schema.json`
- `scientific-twin.v1.schema.json`
- `disease-profile.v1.schema.json`
- `pathogen-profile.v1.schema.json`
- `virus-profile-extension.v1.schema.json`
- `pathogen-host-profile.v1.schema.json`
- `therapeutic-profile.v1.schema.json`
- `quantity-definition.v1.schema.json`
- `quantitative-observation.v1.schema.json`
- `effect-estimate.v1.schema.json`
- `measurement-process.v1.schema.json`
- `numerical-verification.v1.schema.json`
- `model-credibility.v1.schema.json`
- `extraction-artifact.v1.schema.json`
- `extraction-quality-card.v1.schema.json`
- `source-lifecycle-event.v1.schema.json`
- `benchmark-exposure-ledger.v1.schema.json`
- `external-seal-attestation.v1.schema.json`
- `prediction-exposure-event.v1.schema.json`
- `research-program-attempt.v1.schema.json`
- `gene-model-release.v1.schema.json`
- `confirmatory-program-budget.v1.schema.json`
- `estimand.v1.schema.json`
- `endpoint-quality-rule.v1.schema.json`
- `seal-bundle-manifest.v1.schema.json`
- `big0f-pilot-result.v1.schema.json`
- `big0f-threshold-manifest.v1.schema.json`
- `big0f-adjudication-policy.v1.schema.json`
- `big0f-nuisance-manifest.v1.schema.json`
- `big0f-power-analysis.v1.schema.json`
- `big0f-power-input-derivation.v1.schema.json`
- `big0f-variance-source-registry.v1.schema.json`
- `big0f-selection-provenance.v1.schema.json`
- `big0f-nuisance-run.v1.schema.json`
- `big0f-provider-audit-scope.v1.schema.json`
- `big0f-provider-audit.v1.schema.json`
- `big0f-curation-audit.v1.schema.json`
- `big0f-adjudicator-independence.v1.schema.json`
- `research-program-ledger.v1.schema.json`
- `randomness-beacon.v1.schema.json`

Rules:
- JSON Schema validates structure, types, required fields, enums, and unknown-field rejection.
- Markdown contracts remain authoritative for scientific semantics.
- A runtime freeze validator must additionally reject unresolved placeholders such as `TO_BE_FROZEN` when an artifact status is FROZEN.
- Schema version and content digest are included in frozen artifacts.


When implementation begins, scientific-twin/profile schemas must be exercised by positive/negative contract tests. A schema file merely parsing as JSON is not sufficient for implementation readiness.


BIG 0R5 schemas enforce quantitative/credibility semantics, including unit-required observations, missing/censoring state, custom-transform provenance, numerical-verification adequacy, and Context-of-Use-specific credibility conclusions.

BIG 0F-0 defines a second enforcement layer for future implementation:
- cross-field scientific invariant checks;
- permanent adversarial regression tests derived from the hostile-review attack catalog.

A frozen artifact is not considered valid merely because it passes JSON Schema.

BIG 0F operational-prep contracts additionally specify:
- deterministic seal-bundle construction + tamper-detection requirements;
- structure-frozen vs confirmatory-instance estimand distinction;
- endpoint-quality decision structure;
- machine-readable pilot result;
- deterministic GO / REDESIGN / NO_GO decision semantics.


Round 2 hostile-review closure adds cross-artifact implementation requirements:
- external-frame-seal + post-seal randomness selection must be reconstructable;
- frozen endpoint criteria must have one canonical future evaluator;
- confirmatory attempts must consume one program-wide alpha budget;
- `config/big0f-thresholds.v1.json` — sealed decision thresholds/sensitivity variants;
- `config/big0f-adjudication-policy.v1.json` — frozen primary assignment/ascertainment classes;
- `config/big0f-nuisance-manifest.v1.json` — mandatory disease-specific attention/opportunity comparator.
- `config/big0f-power-input-derivation.v1.json` — frozen fail-closed variance/power-input policy.
