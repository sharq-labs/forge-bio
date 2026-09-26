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
- `estimand.v1.schema.json`
- `endpoint-quality-rule.v1.schema.json`
- `seal-bundle-manifest.v1.schema.json`
- `big0f-pilot-result.v1.schema.json`
- `big0f-threshold-manifest.v1.schema.json`
- `big0f-adjudication-policy.v1.schema.json`
- `big0f-nuisance-manifest.v1.schema.json`
- `big0f-power-analysis.v1.schema.json`
- `randomness-beacon.v1.schema.json`

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

BIG 0F operational-prep contracts additionally provide:
- deterministic seal-bundle construction + tamper detection;
- structure-frozen vs confirmatory-instance estimand distinction;
- endpoint-quality decision structure;
- machine-readable pilot result;
- deterministic GO / REDESIGN / NO_GO evaluation.


Round 2 hostile-review closure adds executable cross-artifact enforcement:
- `scripts/select_big0f_sample.py` — external-frame-seal + post-seal randomness selection;
- `scripts/evaluate_endpoint_quality.py` — executable frozen endpoint criteria;
- `scripts/validate_research_program.py` — one program-wide confirmatory alpha budget;
- `config/big0f-thresholds.v1.json` — sealed decision thresholds/sensitivity variants;
- `config/big0f-adjudication-policy.v1.json` — frozen primary assignment/ascertainment classes;
- `config/big0f-nuisance-manifest.v1.json` — mandatory disease-specific attention/opportunity comparator.
