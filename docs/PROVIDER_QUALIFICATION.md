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
outcome_ascertainment_risk
locus_to_gene_dependency
population_ancestry_coverage
measurement_platform_semantics
unit_scale_transform_semantics
batch_normalization_semantics
representation_derivation_time_semantics
ontology_dependency
derived_model_dependency
upstream_source_families
curation_pipeline_family
ontology_families
identity_mapping_families
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
retrospective_curation_fraction
population_ancestry_metadata_fraction
assignment_dependency_fraction
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
- outcome ascertainment/discoverability risks;
- representation-derivation timing;
- locus-to-gene assignment dependencies where applicable;
- population/ancestry coverage where relevant;
- measurement/platform/unit/scale/transform semantics where quantitative fields are used;
- batch/normalization provenance where relevant;
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


## 13. Future outcome provider qualification

Future outcome sources are qualified independently from Past providers.

Independence of qualification does not imply independence of curation lineage.

Each provider/release also emits:

```text
ProviderLineage
    provider_id
    upstream_source_families
    curation_pipeline_family
    ontology_families
    identity_mapping_families
```

For every benchmark generation, Past input providers and Future outcome providers receive an `InputOutcomeCouplingAssessment`.

Material coupling requires preregistered sensitivity analysis such as:
- exclude the same curation-pipeline family;
- external future-source replication;
- upstream-source-family ablation.

A result that only predicts the later state of the same curation pipeline does not earn an independent biological-discovery claim.

Normative decision: [adr/ADR-013-event-identity-source-coupling.md](adr/ADR-013-event-identity-source-coupling.md).

A source may be excellent for current discovery and still be unsuitable as benchmark ground truth because of:
- retrospective curation;
- opaque gene assignment;
- selective reporting;
- unstable historical coverage;
- missing cohort/sample lineage;
- unknown first-public availability;
- poor population/ancestry metadata.

Outcome-provider qualification records whether the source is acceptable for:
- event discovery;
- historical novelty audit;
- gene-assignment evidence;
- independent replication;
- negative/failure evidence;
- censoring/coverage accounting.

## 14. Representation-time rule

Provider records that expose modern structured annotations over older primary observations must preserve both layers.

A field is not HISTORICAL_SAFE merely because it points to an old publication.

If the structured derivation itself depends on later knowledge, the field's watermark follows that derivation.
