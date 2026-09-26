# Core Scientific Types V1

**Status:** NORMATIVE PRE-CODE V1

These are semantic contracts, not implementation-language commitments.

## Operating and temporal types

```text
OperatingMode
    STRICT_HISTORICAL
    HISTORICAL_INPUT_MODERN_PRIOR
    CURRENT_DISCOVERY

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
    GENE
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
HistoricalNoveltyAudit
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
- phenotype/trait relation != disease identity.
- suggestive pre-T genetics != novel discovery.
- replication != repeated database annotation.
- identity reconciliation != causal assignment.
- EvidenceRecord != model prediction.
- distinct database rows != independent evidence.
- current representation != historical representation.
- candidate-universe membership requires provenance.
- every frozen scientific artifact has a schema version and digest.
