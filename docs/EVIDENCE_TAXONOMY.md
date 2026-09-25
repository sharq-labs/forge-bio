# Evidence Taxonomy

**Status:** PRE-CODE CANDIDATE

## 1. Rule

EvidenceRecord uses orthogonal axes. Do not encode all semantics into one flat evidence_type enum.

## 2. Core shape

```text
EvidenceRecord
    evidence_id
    claim_id
    evidence_domain
    experimental_system
    study_design
    stance
    source_channel
    extraction_method
    biological_context
    observation
    effect
    uncertainty
    availability_attestation
    independence_family_id
    provenance_id
    knowledge_watermark
```

Not every axis is populated for every record. Missing values remain explicit.

## 3. Evidence domain

- GENETIC
- FUNCTIONAL
- BIOCHEMICAL
- PHARMACOLOGICAL
- EXPRESSION_OMICS
- PATHWAY_CURATED
- STRUCTURAL
- CLINICAL
- REGULATORY
- SAFETY
- EPIDEMIOLOGICAL
- COMPUTATIONAL

## 4. Experimental system

- HUMAN
- HUMAN_EX_VIVO
- MODEL_ORGANISM
- IN_VIVO
- IN_VITRO
- EX_VIVO
- CELL_FREE
- IN_SILICO
- NOT_APPLICABLE
- UNKNOWN

Species is represented separately in BiologicalContext.

## 5. Study design / method

Controlled, versioned vocabulary, initially including:
- GWAS
- MENDELIAN_OR_RARE_VARIANT
- QTL
- CRISPR_PERTURBATION
- KNOCKOUT
- KNOCKDOWN
- OVEREXPRESSION
- BINDING_ASSAY
- ENZYME_ASSAY
- REPORTER_ASSAY
- EXPRESSION_ASSOCIATION
- PATHWAY_CURATION
- OBSERVATIONAL_COHORT
- CASE_CONTROL
- RANDOMIZED_TRIAL
- NONRANDOMIZED_INTERVENTION
- STRUCTURE_DETERMINATION
- COMPUTATIONAL_PREDICTION
- REGULATORY_REVIEW
- OTHER
- UNKNOWN

The vocabulary may expand without changing the top-level EvidenceRecord shape.

## 6. Stance

- SUPPORTS
- REFUTES
- NULL_RESULT
- QUALIFIES
- INCONCLUSIVE

NULL_RESULT is not automatically REFUTES.

## 7. Source channel

- PUBLICATION
- DATABASE
- REGISTRY
- REGULATORY_DOCUMENT
- GUIDELINE
- CURATED_DATASET
- PRIMARY_DATASET
- INTERNAL_DERIVATION

"Literature" belongs here, not in a scientific strength axis.

## 8. Extraction method

- NATIVE_STRUCTURED
- HUMAN_CURATED
- RULE_BASED
- ML_EXTRACTED
- LLM_EXTRACTED
- INTERNAL_COMPUTATION

ML/LLM extraction carries extractor/model identity and horizon.

## 9. BiologicalContext

Support explicit fields for:
- species
- tissue
- cell_type
- disease_subtype
- phenotype
- population
- sex if scientifically relevant
- age_group if scientifically relevant
- dose/exposure context
- intervention
- measurement_endpoint
- study_setting

Unknown remains UNKNOWN.

## 10. Observation and effect

Do not force all evidence into one scalar.

Possible fields:
- estimate
- effect_direction
- effect_size
- effect_unit
- standard_error
- confidence_interval
- p_value
- sample_size
- assay_value
- assay_unit
- quality_grade
- raw_payload_ref

Method-specific payloads are schema-versioned.

## 11. Independence

```text
IndependenceFamily
    family_id
    origin_type
    originating_study_id?
    cohort_id?
    lab_or_consortium?
    parent_dataset_id?
    lineage_complete
```

The same experiment copied through multiple databases remains one family.

Unknown ancestry must not be interpreted as independence.

## 12. Evidence strength

V0 does not invent arbitrary cross-method weights such as genetic=0.7.

Represent method-specific strength through:
- ordinal grade
- native statistics
- explicit quality flags
- independent replication count

Cross-method aggregation belongs to a versioned ScoringPolicy and requires empirical justification.

## 13. Minimal contradiction primitive before BIG 7

A minimal comparability/conflict layer belongs in the evidence kernel before the first benchmark:

```text
ConflictAssessment
    claim_a
    claim_b
    comparability
    conflict_type
    rationale
    strength
    provenance
```

V0 comparability considers at least:
- entity match
- predicate match
- direction
- species
- tissue/context
- endpoint
- intervention type

BIG 10 expands this into advanced adjudication and reviewer-validated workflows.

## 14. Gaps

Typed gaps:
- NO_DATA_AT_T
- NOT_ASSESSED
- COVERAGE_INSUFFICIENT
- IDENTITY_UNRESOLVED
- TEMPORAL_UNKNOWN
- METHOD_NOT_AVAILABLE
- APPLICABILITY_UNKNOWN

A gap never becomes positive support.

## 15. Derived computational evidence

A model prediction is:

```text
evidence_domain = COMPUTATIONAL
source_channel = INTERNAL_DERIVATION
```

It can be reported as model output but cannot be re-ingested as independent biological evidence without an explicit derived-evidence policy.

## 16. Versioning

The taxonomy has an evidence_schema_version.

Changing category meaning requires a schema/ADR change, not silent remapping.
