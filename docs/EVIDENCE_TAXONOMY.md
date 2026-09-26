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
- GWAS_SINGLE_VARIANT
- GWAS_META_ANALYSIS
- FINE_MAPPING
- COLOCALIZATION
- EXOME_ASSOCIATION
- WGS_ASSOCIATION
- GENE_BURDEN
- RARE_VARIANT_AGGREGATION
- CNV_ASSOCIATION
- PHEWAS
- MENDELIAN_SEGREGATION
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

Quantitative evidence references typed artifacts:

```text
EvidenceRecord
    observation_id? -> QuantitativeObservation
    effect_id?      -> EffectEstimate
    raw_payload_ref?
```

Normative quantitative semantics are defined in [QUANTITATIVE_SEMANTICS.md](QUANTITATIVE_SEMANTICS.md).

Executable schemas include:
- QuantityDefinition;
- QuantitativeObservation;
- EffectEstimate;
- MeasurementProcessArtifact.

Rules:
- a number without quantity/scale/transform/context semantics is not a scientific measurement;
- a p-value alone is not an effect estimate;
- ratio, log-ratio, odds ratio, risk ratio, hazard ratio, and regression coefficients are not interchangeable;
- unit-bearing values require dimensional compatibility before arithmetic/aggregation;
- missing/censored measurements are not coerced to numeric zero;
- normalization/imputation/batch correction are provenance-bearing transforms.

Method-specific payloads remain schema-versioned.

Human-genetic payloads may additionally include:
- canonical variant/locus IDs;
- genome assembly/reference sequence;
- reference/alternate/effect allele;
- allele frequency;
- harmonization artifact ID;
- fine-mapping/credible-set metadata;
- LD relation/reference-panel ID;
- phenotype concept ID;
- ancestry/population;
- cohort/dataset/SampleSet IDs;
- meta-analysis membership;
- heterogeneity statistics.

Free-text rsIDs, coordinates, cohort names, or trait labels are not substitutes for resolved identities when the field affects benchmark matching.

## 11. Independence

```text
IndependenceFamily
    family_id
    origin_type
    originating_study_id?
    cohort_id?
    consortium_id?
    biobank_id?
    dataset_id?
    sample_set_ids?
    participant_overlap_group?
    lab_or_consortium?
    parent_dataset_id?
    meta_analysis_parent_ids?
    independence_confidence
    lineage_complete
```

The same experiment copied through multiple databases remains one family.

Distinct publications are not sufficient evidence of independent samples.

Unknown lineage or participant overlap must not be interpreted as independence.

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

## 17. Representation-time provenance

Structured evidence derived from an older observation must preserve both:
- the underlying observation/publication availability;
- the structured derivation availability, method, and knowledge watermark.

A 2008 publication converted into a gene assignment by a 2026 knowledge-bearing model is not automatically a 2008 structured gene-level fact.

## 18. Population / ancestry metadata

For human evidence, population and ancestry are retained where scientifically relevant and available.

Missing values remain UNKNOWN. Evidence aggregated across populations must not silently erase population-specific applicability.


## 19. Scientific event family

Evidence manifestations and scientific events are separate.

A preprint, journal article, database row, and secondary curation may all describe one underlying discovery.

```text
ScientificEventFamily
    event_family_id
    event_domain
    originating_study_ids
    primary_public_manifestations
    secondary_curated_manifestations
    provenance
```

For genetic outcomes, GeneticDiscoveryEventFamily additionally preserves locus IDs and gene assignments.

Event-family identity is used for outcome counting and cross-anchor reuse; IndependenceFamily is used for evidentiary dependence. They are related but not interchangeable.


## 20. Measurement and batch provenance

Quantitative observations preserve the process that produced them.

```text
MeasurementProcessArtifact
    assay_or_measurement_type
    platform
    protocol/provider
    calibration
    normalization
    batch context
    detection limits
    measurement-error model
    provenance
    knowledge watermark
```

Platform/batch/normalization effects are retained where they may alter comparability.

A normalization fitted using post-cutoff data is temporal leakage.

## 21. Quantitative uncertainty decomposition

Where relevant, distinguish:
- measurement uncertainty;
- sampling uncertainty;
- parameter uncertainty;
- numerical uncertainty;
- model-form uncertainty.

These are not collapsed into one generic confidence scalar.
