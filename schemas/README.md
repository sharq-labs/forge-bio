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
- `seal-bundle-manifest.v1.schema.json` (bundle version `big0f-seal-bundle-v3`)
- `research-program-ledger.v1.schema.json`
- `randomness-beacon.v1.schema.json`

BIG 0F (normative summary: [../docs/V0_FREEZE_STATEMENT.md](../docs/V0_FREEZE_STATEMENT.md); decisions: [../docs/adr/ADR-022-final-scientific-consistency-closure.md](../docs/adr/ADR-022-final-scientific-consistency-closure.md)):

| Schema | Instance / config |
|---|---|
| `big0f-threshold-manifest.v2.schema.json` | `config/big0f-thresholds.v2.json` |
| `big0f-adjudication-policy.v2.schema.json` | `config/big0f-adjudication-policy.v2.json` |
| `big0f-nuisance-manifest.v2.schema.json` | `config/big0f-nuisance-manifest.v2.json` |
| `big0f-power-policy.v2.schema.json` | `config/big0f-power-policy.v2.json` |
| `big0f-frame-rule.v1.schema.json` | `config/big0f-frame-rule.v1.json` |
| `big0f-required-field-registry.v1.schema.json` | `config/big0f-required-field-registry.v1.json` |
| `outcome-discovery.v1.schema.json` | `config/outcome-discovery.v1.json` |
| `big0f-pilot-result.v2.schema.json` | produced by BIG 0F |
| `big0f-power-analysis.v2.schema.json` | produced by the Stage A / Stage B power engine |
| `big0f-variance-source-registry.v2.schema.json` | Stage B only (optional external sources) |
| `big0f-selection-provenance.v1.schema.json` | produced by the selection custodian |
| `big0f-nuisance-run.v2.schema.json` | produced by the nuisance-only run |
| `big0f-provider-audit-scope.v2.schema.json` | derived mechanically from the selection and the registry |
| `big0f-provider-audit.v2.schema.json` | produced by the provider audit |
| `big0f-curation-audit.v2.schema.json` | produced by adjudication (both reviewers' labels) |
| `big0f-adjudicator-independence.v1.schema.json` | second adjudicator and selection custodian attestations |

Replaced in the closure change (ADR-022; the old files were removed):

| Removed | Replacement |
|---|---|
| `big0f-pilot-result.v1`, `big0f-threshold-manifest.v1`, `big0f-adjudication-policy.v1`, `big0f-nuisance-manifest.v1`, `big0f-power-analysis.v1`, `big0f-variance-source-registry.v1`, `big0f-nuisance-run.v1`, `big0f-provider-audit-scope.v1`, `big0f-provider-audit.v1`, `big0f-curation-audit.v1` | the same name at `.v2` |
| `big0f-power-input-derivation.v1` (schema and config) | `big0f-power-policy.v2` |
| configs `big0f-thresholds.v1`, `big0f-adjudication-policy.v1`, `big0f-nuisance-manifest.v1` (removed) | the `.v2.json` configs above |

Rules:
- JSON Schema validates structure, types, required fields, enums, and unknown-field rejection.
- Markdown contracts remain authoritative for scientific semantics.
- Artifact status is `SEAL_CANDIDATE` or `SEALED` with `sealed_by_attestation_id`; `frozen_at` and a FROZEN status no longer exist (INV-S1, INV-S5).
- A future validator must additionally reject unresolved placeholders such as `TO_BE_FROZEN` in any SEAL_CANDIDATE or SEALED artifact.
- Schema version and content digest are included in sealed artifacts.
- Rules of meaning that JSON Schema cannot express are listed in [../docs/SEMANTIC_INVARIANTS.md](../docs/SEMANTIC_INVARIANTS.md). Each one is marked SCHEMA or HARNESS. Nothing marked HARNESS is enforced until the verification harness exists.


When implementation begins, scientific-twin/profile schemas must be exercised by positive/negative contract tests. A schema file merely parsing as JSON is not sufficient for implementation readiness.


BIG 0R5 schemas enforce quantitative/credibility semantics, including unit-required observations, missing/censoring state, custom-transform provenance, numerical-verification adequacy, and Context-of-Use-specific credibility conclusions.

BIG 0F-0 defines a second enforcement layer for future implementation:
- cross-field scientific invariant checks;
- permanent adversarial regression tests derived from the hostile-review attack catalog.

A sealed artifact is not considered valid merely because it passes JSON Schema.

BIG 0F operational-prep contracts additionally specify:
- deterministic seal-bundle construction + tamper-detection requirements;
- structure vs confirmatory-instance estimand distinction (`instance_state`);
- endpoint-quality decision structure;
- machine-readable pilot result;
- deterministic GO / REDESIGN / NO_GO decision semantics.


Round 2 hostile-review closure adds cross-artifact implementation requirements:
- the pre-declared drand quicknet round and the seal_time ordering must be reconstructable (superseded wording: "external-frame-seal + post-seal randomness", ADR-022 D13);
- frozen endpoint criteria must have one canonical future evaluator;
- confirmatory attempts must consume one program-wide alpha budget;
- the BIG 0F configs are listed in the table above.
