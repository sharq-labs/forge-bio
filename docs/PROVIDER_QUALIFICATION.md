# Provider Qualification

**Status:** PRE-CODE CANDIDATE

## 1. Principle

"High quality", "open", and "contains old records" do not imply historical safety.

Qualification unit:

```text
(provider, release/version, field_or_derivation, intended_use)
```

The same source may be safe for one field and unsafe for another.

## 2. Qualification states

- HISTORICAL_SAFE
- HISTORICAL_CONDITIONAL
- CURRENT_ONLY
- FUTURE_VALIDATION_ONLY
- PROHIBITED_FOR_BENCHMARK
- UNKNOWN

UNKNOWN is never treated as safe.

## 3. ProviderCard

Each dossier records:

```text
provider_id
release_id
retrieval_method
raw_artifact_hashes
license_manifest
release_date
archive_availability
record_history_capability
availability_semantics
retrospective_curation_risk
identity_mapping_risk
ontology_dependency
derived_model_dependency
coverage_scope
known_gaps
qualification_by_field
approved_operating_modes
reviewer
review_date
```

## 4. Field-level qualification

Example:

```text
Provider X / Release R
    publication_id          HISTORICAL_SAFE
    publication_date        HISTORICAL_CONDITIONAL
    current_disease_mapping CURRENT_ONLY
    model_derived_score     PROHIBITED_FOR_BENCHMARK
```

Adapters expose source facts. They do not upgrade fields into scientific truth.

## 5. Historical-fidelity priority

Preferred order:
1. archived byte-exact release near T;
2. record/version history with strong public-availability semantics;
3. reconstructed historical state with measured fidelity;
4. current-only retrospectively curated state.

Tier 4 is not strict historical input.

## 6. Reconstruction Fidelity Study

For every important HISTORICAL_CONDITIONAL source where an archived reference exists, compare:

```text
archived release as-of-T
vs
reconstruction from newer release
```

Measure:
- record additions/removals;
- identity mapping changes;
- ontology changes;
- field-value differences;
- retrospective annotation rate;
- candidate-universe differences;
- feature differences;
- ranking differences under a fixed baseline.

Output a versioned verdict:
- acceptable under declared fields/thresholds;
- exploratory only;
- unacceptable.

## 7. Availability audit

Sample historical records and verify claimed public-availability semantics against primary metadata/artifacts.

Record:
- nominal date;
- attested interval;
- basis;
- attestation quality;
- mismatch rate.

Qualification may be downgraded if nominal timestamps do not support the admission policy.

## 8. Coverage matrix

For each candidate cutoff year and required modality, report:

```text
coverage
unknown_fraction
identity_resolution_fraction
archive_fidelity
outcome_window_length
license_status
```

The first benchmark cutoff is selected from this matrix.

## 9. Licensing posture

Before provider implementation, record project posture:
- academic/open research;
- commercial later;
- commercial from day one.

Every SourceSnapshot manifest includes:
- license name/version;
- source terms version/hash;
- attribution requirement;
- share-alike flag;
- commercial-use status;
- redistribution constraints;
- derived-data constraints;
- review status.

Provider eligibility may differ by distribution/commercial mode.

This is engineering metadata, not legal advice.

## 10. Provider adapter contract

A provider adapter may implement:

```text
metadata()
license_info()
list_available_releases()
get_release_manifest()
fetch_release()
verify_release()
parse_snapshot()
availability_evidence(record, field)
record_provenance(record)
capabilities()
```

It must not:
- declare a therapeutic target valid;
- convert modern identity into historical truth;
- create benchmark labels;
- aggregate evidence strength;
- access Future Outcome data when serving the historical plane.

## 11. Cutoff selection gate

No cutoff becomes authoritative until the provider audit documents:
- required source availability;
- minimum coverage thresholds;
- acceptable UNKNOWN fractions;
- outcome observation horizon;
- disease/candidate identity coverage;
- reconstruction dependencies.

"2010" remains a working hypothesis until this gate is passed.

## 12. Provider change control

A new provider release is a new scientific input.

Never silently point an adapter to "latest".

Changing provider/release/field qualification requires:
- a new manifest;
- updated ProviderCard;
- new dataset snapshot IDs;
- affected benchmark reclassification;
- an ADR if semantics change.
