# Core Scientific Types V1

**Status:** NORMATIVE PRE-CODE V1

These are semantic contracts, not implementation-language commitments.

## Operating and temporal types

```text
ScientificOperatingMode
    STRICT_HISTORICAL
    HISTORICAL_INPUT_MODERN_PRIOR
    CURRENT_DISCOVERY

HistoricalDataPolicy
    ARCHIVED_ONLY
    RECONSTRUCTED_ALLOWED

KnowledgeBearingness
    NON_KNOWLEDGE_BEARING
    KNOWLEDGE_BEARING
    UNKNOWN

KnowledgeWatermark
    NON_KNOWLEDGE_BEARING
    DATED(date)
    UNKNOWN

TemporalAdmissionDecision
    ADMIT
    REFUSE
    UNKNOWN
```

## Identity and mapping

```text
EntityKind
    DISEASE
    PHENOTYPE
    ORGANISM_TAXON
    PATHOGEN
    VIRUS
    BACTERIUM
    FUNGUS
    PARASITE
    STRAIN
    PATHOGEN_VARIANT
    ANATOMICAL_STRUCTURE
    TISSUE
    CELL_TYPE
    BIOLOGICAL_PROCESS
    BIOMARKER
    GENE
    GENOME_ASSEMBLY
    REFERENCE_SEQUENCE
    GENOMIC_VARIANT
    GENOMIC_LOCUS
    PROTEIN
    PROTEIN_COMPLEX
    PATHWAY
    CHEMICAL_STRUCTURE
    ACTIVE_MOIETY
    ACTIVE_INGREDIENT
    MEDICINAL_PRODUCT
    DRUG_COMBINATION
    PUBLICATION
    STUDY
    TRIAL
    REGULATORY_ACTION
    COHORT
    DATASET
    BIOBANK
    CONSORTIUM
    SAMPLE_SET
    LD_REFERENCE_PANEL

MappingRelation
    EXACT
    BROAD
    NARROW
    RELATED
    REPLACED_BY
    MERGED_INTO
    SPLIT_FROM

MappingReviewStatus
    UNREVIEWED
    ACCEPTED
    REJECTED
    AMBIGUOUS
```

## Evidence

```text
EvidenceDomain
    GENETIC
    FUNCTIONAL
    BIOCHEMICAL
    PHARMACOLOGICAL
    EXPRESSION_OMICS
    PATHWAY_CURATED
    STRUCTURAL
    CLINICAL
    REGULATORY
    SAFETY
    EPIDEMIOLOGICAL
    COMPUTATIONAL

EvidenceStance
    SUPPORTS
    REFUTES
    NULL_RESULT
    QUALIFIES
    INCONCLUSIVE

SourceChannel
    PUBLICATION
    DATABASE
    REGISTRY
    REGULATORY_DOCUMENT
    GUIDELINE
    CURATED_DATASET
    PRIMARY_DATASET
    INTERNAL_DERIVATION

ExtractionMethod
    NATIVE_STRUCTURED
    HUMAN_CURATED
    RULE_BASED
    ML_EXTRACTED
    LLM_EXTRACTED
    INTERNAL_COMPUTATION
```

## Benchmark and outcomes

```text
HoldoutTier
    DEVELOPMENT
    VALIDATION
    SEALED_LOCKBOX

LabelState
    POSITIVE
    NEGATIVE_CONFIRMED
    UNKNOWN
    RIGHT_CENSORED
    COMPETING_EVENT
    CONFLICTED
    AMBIGUOUS
    KNOWN_AT_T

PreTGeneticState
    NO_SIGNAL_OBSERVED
    SUGGESTIVE
    QUALIFYING
    AMBIGUOUS

E1Subtype
    E1_NOVEL_STRICT
    E1_MATURATION
    E1_REPLICATION
    E1_CROSSMODAL

OutcomePhenotypeRelation
    EXACT
    SAME_CONCEPT_DIFFERENT_DEFINITION
    NARROWER
    BROADER
    SURROGATE
    RISK_FACTOR
    INTERMEDIATE_PHENOTYPE
    RELATED
    UNRESOLVED

GeneticReplicationVerdict
    REPLICATED
    PARTIAL_REPLICATION
    DIRECTION_CONFLICT
    PHENOTYPE_MISMATCH
    NON_INDEPENDENT
    INCONCLUSIVE
    UNRESOLVED

ValidationGenerationStatus
    ACTIVE
    SPENT_FOR_MODEL_SELECTION
    RETIRED

ValidationDisclosureLevel
    AGGREGATE_ONLY
    SUBGROUP
    PER_CASE
    FULL_LABEL

HistoricalGeneticCoverageGrade
    HIGH
    MODERATE
    LOW
    UNKNOWN

DigitalTwinMaturityLevel
    T0_PROFILE_ONLY
    T1_DYNAMIC_KNOWLEDGE_TWIN
    T2_MECHANISTIC_TWIN
    T3_VALIDATED_PREDICTIVE_TWIN
    T4_VALIDATED_INTERVENTION_SIMULATION_TWIN

ScientificTwinFamily
    DISEASE_TWIN
    PATHOGEN_TWIN
    PATHOGEN_HOST_TWIN
    THERAPEUTIC_TWIN

ModelInfluence
    ADVISORY
    MATERIAL
    DOMINANT

CredibilityConclusion
    ADEQUATE_FOR_COU
    CONDITIONALLY_ADEQUATE
    INADEQUATE
    UNKNOWN

PredictionRiskOfBias
    LOW
    SOME_CONCERNS
    HIGH
    UNKNOWN
    NOT_APPLICABLE

MissingnessState
    OBSERVED
    MISSING
    NOT_APPLICABLE

CensoringState
    NONE
    BELOW_DETECTION
    ABOVE_DETECTION
    RIGHT_CENSORED
    LEFT_CENSORED
    INTERVAL_CENSORED

TherapeuticModality
    SMALL_MOLECULE
    ANTIBODY
    PROTEIN_BIOLOGIC
    PEPTIDE
    NUCLEIC_ACID
    GENE_THERAPY
    CELL_THERAPY
    VACCINE
    OTHER

NoveltyAuditState
    NOVEL_CONFIRMED
    KNOWN_AT_T
    NOVELTY_AMBIGUOUS

AssignmentReviewState
    ACCEPTED
    REJECTED
    AMBIGUOUS
    NOT_APPLICABLE

ProviderQualification
    HISTORICAL_SAFE
    HISTORICAL_CONDITIONAL
    CURRENT_ONLY
    FUTURE_VALIDATION_ONLY
    PROHIBITED_FOR_BENCHMARK
    UNKNOWN

ClaimMaturityLevel
    L0_REPRODUCIBLE_OUTPUT
    L1_REDISCOVERY
    L2_DEVELOPMENT_RETROSPECTIVE
    L3_SEALED_CONFIRMATORY
    L4_GENERALIZATION
    L5_ENDPOINT_CALIBRATED
    L6_PROSPECTIVE
```

## Required value objects

```text
PartialDate
AvailabilityInterval
AvailabilityAttestation
KnowledgeWatermark
EntityId
EntityRevision
ExternalIdentifierAssignment
GenomeAssembly
ReferenceSequence
GenomicVariant
GenomicLocus
VariantHarmonizationArtifact
LDReferencePanel
LDRelation
PhenotypeConcept
OrganismTaxon
PathogenConcept
VirusConcept
BacteriumConcept
FungusConcept
ParasiteConcept
StrainConcept
PathogenVariant
AnatomicalStructure
TissueConcept
CellTypeConcept
BiologicalProcess
BiomarkerConcept
DiseaseScientificProfile
PathogenScientificProfile
VirusScientificProfileExtension
PathogenHostScientificProfile
TherapeuticScientificProfile
ScientificDigitalTwin
ScientificTwinSnapshot
TwinState
TwinStateModelArtifact
TwinUpdatePolicyArtifact
TwinValidationArtifact
CausalAssumptionSet
InterventionSemantics
IdentifiabilityStatus
TwinPerturbation
TwinSimulationResult
QuantityDefinition
UnitDefinition
TransformDefinition
QuantitativeObservation
EffectEstimate
MeasurementProcessArtifact
ExtractionArtifact
ExtractionQualityCard
NumericalVerificationArtifact
ModelDiscrepancyAssessment
ApplicabilityDomain
CredibilityAssessmentArtifact
PredictionRiskAssessment
Cohort
Dataset
Biobank
Consortium
SampleSet
ScientificClaim
EvidenceRecord
IndependenceFamily
ConflictAssessment
CandidateUniverse
HistoricalKnowledgeView
TargetAssociationCandidate
TargetHypothesis
FutureEvent
OutcomeGeneAssignment
OutcomePhenotypeMatchAssessment
PreTGeneticStateAssessment
GeneticReplicationAssessment
HistoricalGeneticSearchCoverage
GeneticObservabilityAtT
HistoricalNoveltyAudit
ScientificEventFamily
GeneticDiscoveryEventFamily
ProviderLineage
InputOutcomeCouplingAssessment
CrossAnchorEventReusePolicy
ValidationGeneration
OutcomeSnapshotCommitment
BenchmarkDesignProvenance
BenchmarkSpec
MAP
MAR
UncertaintyBundle
```

## Semantic invariants

- UNKNOWN is never numerically coerced to zero.
- LabelState is endpoint-specific.
- gene != protein != target.
- locus/variant event != gene assignment.
- rsID/coordinate string != canonical variant identity.
- LD relation is population/reference-panel/version dependent.
- harmonization/liftover is a provenance-bearing derivation.
- phenotype/trait relation != disease identity.
- database row/publication != scientific event family.
- cohort/dataset aliases do not imply independent samples.
- suggestive pre-T genetics != novel discovery.
- replication != repeated database annotation.
- identity reconciliation != causal assignment.
- EvidenceRecord != model prediction.
- distinct database rows != independent evidence.
- current representation != historical representation.
- disease != pathogen.
- pathogen != disease manifestation.
- pathogen-only model != pathogen-host system.
- scientific profile != predictive digital twin.
- T0 profile is not claimed as a digital twin.
- T3/T4 requires explicit predictive validation and uncertainty quantification.
- historical twin cutoff != valid_at timestamp.
- state-model structure/update policy may be knowledge-bearing and must carry provenance/watermark.
- T4 perturbation != causal intervention unless causal assumptions/intervention semantics/identifiability requirements pass.
- numeric value != scientific measurement without quantity/unit/scale/transform/context semantics.
- p-value != effect estimate.
- extractor confidence != scientific evidence strength.
- extracted claim != independent observation.
- extraction representation change != new IndependenceFamily.
- numerical solver agreement != biological validation.
- numerical error != parameter uncertainty != model-form uncertainty != measurement uncertainty.
- calibration != model correctness.
- model credibility is Context-of-Use specific.
- model validation does not survive a material dependency change without re-assessment.
- out-of-domain prediction != validated prediction.
- simulation result != clinical evidence.
- therapeutic profile != patient-specific treatment recommendation.
- candidate-universe membership requires provenance.
- every frozen scientific artifact has a schema version and digest.
