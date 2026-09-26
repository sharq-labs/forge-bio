# Machine-Verifiable Scientific Schemas

These JSON Schemas are executable companions to the normative Markdown contracts.

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

Rules:
- JSON Schema validates structure, types, required fields, enums, and unknown-field rejection.
- Markdown contracts remain authoritative for scientific semantics.
- A runtime freeze validator must additionally reject unresolved placeholders such as `TO_BE_FROZEN` when an artifact status is FROZEN.
- Schema version and content digest are included in frozen artifacts.


Scientific-twin/profile schemas are exercised by executable positive/negative contract tests under `tests/spec/`. A schema file merely parsing as JSON is not sufficient for readiness.


BIG 0R5 schemas enforce quantitative/credibility semantics, including unit-required observations, missing/censoring state, custom-transform provenance, numerical-verification adequacy, and Context-of-Use-specific credibility conclusions.

BIG 0F-0 adds a second enforcement layer:
- `scripts/scientific_invariants.py` for cross-field scientific invariants;
- `tests/spec/test_hostile_review_regressions.py` for permanent adversarial regression tests.

A frozen artifact is not considered valid merely because it passes JSON Schema.