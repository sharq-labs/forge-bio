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

Rules:
- JSON Schema validates structure, types, required fields, enums, and unknown-field rejection.
- Markdown contracts remain authoritative for scientific semantics.
- A runtime freeze validator must additionally reject unresolved placeholders such as `TO_BE_FROZEN` when an artifact status is FROZEN.
- Schema version and content digest are included in frozen artifacts.


Scientific-twin/profile schemas are exercised by executable positive/negative contract tests under `tests/spec/`. A schema file merely parsing as JSON is not sufficient for readiness.
