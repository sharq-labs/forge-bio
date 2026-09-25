# Temporal Semantics

**Status:** PRE-CODE CANDIDATE

## 1. Principle

Historical mode asks whether information, in the form used by the system, could have been available by cutoff T. A cutoff is a capability boundary, not a SQL filter.

## 2. Time dimensions

Keep distinct:
- event_time
- published_time
- first_publicly_available_interval
- source_release_time
- indexed_time
- valid_from / valid_to
- superseded_time
- retracted_time
- representation_created_time
- adjudicated_time
- ingested_time
- system_time

Historical admission normally uses first_publicly_available_interval.

## 3. PartialDate

```text
PartialDate
    year
    month?
    day?
    precision: DAY | MONTH | YEAR | UNKNOWN
```

Missing precision is never silently converted to an arbitrary date.

## 4. AvailabilityAttestation

```text
AvailabilityAttestation
    earliest_possible
    latest_possible
    precision
    basis
    source_artifact_id
    source_record_id?
    supporting_locator?
    attestation_quality
    notes?
```

Recommended basis values:
- ARCHIVED_RELEASE_CONTAINS_RECORD
- PUBLICATION_OR_DEPOSITION_DATE
- PROVIDER_PUBLIC_POSTING_DATE
- PROVIDER_RECORD_VERSION_DATE
- INFERRED_FROM_LINKED_PRIMARY_SOURCE
- MANUAL_DOCUMENTED_ATTESTATION
- NONE

Quality:
- STRONG
- MODERATE
- WEAK
- UNKNOWN

Quality never overrides time. It supports provider/case coverage policy and sensitivity analysis.

## 5. Admission

For attestation A and cutoff T:

```text
if A.latest_possible <= T:
    ADMIT
elif A.earliest_possible > T:
    REFUSE
else:
    UNKNOWN
```

Missing/undefended availability may force UNKNOWN even when a nominal provider date exists.

## 6. Retractions and corrections

An as-of-T view preserves what was publicly knowable at T.

If a record was available at T and retracted later:
- the historical view retains the then-available record;
- the later retraction is represented as a later event/state;
- current corrected content must not silently replace historical content.

If correction/retraction occurred before T, the as-of-T state reflects that status.

## 7. Knowledge-bearingness

Implementation provenance and biomedical knowledge are separate.

```text
KnowledgeBearingness
    NON_KNOWLEDGE_BEARING
    KNOWLEDGE_BEARING
    UNKNOWN
```

NON_KNOWLEDGE_BEARING examples:
- cryptographic hashing
- generic sorting
- canonical serialization
- arithmetic
- generic numerical algorithms

KNOWLEDGE_BEARING examples:
- ontology/mapping releases
- curated biomedical lists
- hand-written biomedical rules
- domain-specific configs
- learned encoders
- embeddings
- pretrained models
- graph-derived constants
- feature choices informed by future biomedical outcomes

UNKNOWN is refused in STRICT_HISTORICAL mode.

## 8. KnowledgeWatermark

```text
KnowledgeWatermark
    NON_KNOWLEDGE_BEARING
    DATED(date)
    UNKNOWN
```

Join semantics:

```text
NB + NB             = NB
NB + DATED(t)       = DATED(t)
DATED(a)+DATED(b)   = DATED(max(a,b))
UNKNOWN + x         = UNKNOWN
```

A KNOWLEDGE_BEARING artifact may not claim NON_KNOWLEDGE_BEARING.

## 9. Code/config rule

Code creation date does not determine biomedical knowledge time.

But code/config can be knowledge-bearing. A hard-coded biomedical target list, curated rule, or manually chosen domain prior needs a dated or UNKNOWN watermark from its source.

Generic code such as hashing does not.

Manual feature choices that encode hindsight must be declared in the MAP and may be prohibited from confirmatory strict mode.

## 10. Transitive taint

Every derived artifact declares all scientifically relevant parents.

```text
output.watermark =
    join(parent watermarks,
         embedded knowledge-bearing rules,
         model/representation watermark)
```

This applies to normalized records, mappings, graph projections, candidate universes, features, sampling distributions, embeddings, models, and rankings.

Hidden side inputs are prohibited.

## 10.1 Observation time vs structured representation time

The temporal status of an underlying observation and the temporal status of a derived structured assertion are separate.

Example:

```text
primary_publication_available = 2008
modern_gene_assignment_created = 2026
```

A 2026 knowledge-bearing assignment cannot inherit a 2008 watermark merely because it cites the 2008 paper.

Strict mode evaluates the exact representation visible to the model, not only the age of its cited source.

## 11. Operating policies

### STRICT_ARCHIVED
Archived releases or strong row-level availability evidence only.

### RECONSTRUCTED_HISTORICAL
A newer/current source is reconstructed using temporal evidence. Allowed only when explicitly labelled and supported by provider policy; a Reconstruction Fidelity Study is required where reference archives exist.

### CONTAMINATED_MODERN_PRIOR
Historical explicit inputs plus a later/unknown-horizon model, mapping, ontology, or representation. Never presented as strict historical evidence.

## 11.1 Knowledge-historical vs technology-contemporaneous

Temporal admissibility answers whether biomedical knowledge visible to the method is defensibly available by T.

It does not establish that the exact algorithm, software stack, hardware, or compute budget existed at T.

Reports distinguish:
- KNOWLEDGE_HISTORICAL;
- TECHNOLOGY_CONTEMPORANEOUS.

The second requires separate evidence and is not implied by STRICT_HISTORICAL.

## 12. Coverage accounting

Every HistoricalKnowledgeView reports by source and required field:
- admitted count
- refused count
- unknown count
- attestation-quality distribution
- reconstruction status
- watermark distribution

Confirmatory MAPs freeze maximum acceptable UNKNOWN and reconstruction fractions.

## 13. Metamorphic tests

Required:
1. add a T+1 inadmissible record -> ranking unchanged;
2. move a required parent post-T -> derived artifact becomes inadmissible;
3. replace exact date with interval crossing T -> UNKNOWN;
4. insert future graph edge -> strict graph/features rejected;
5. change generic implementation version only -> watermark unchanged;
6. add a 2026 biomedical constant -> watermark becomes 2026 or UNKNOWN;
7. replace historical text with current corrected text -> snapshot verification fails;
8. derive a gene assignment in 2026 from a 2008 paper -> assignment watermark remains 2026/UNKNOWN, not 2008;
9. change only generic compute infrastructure -> biomedical knowledge watermark remains unchanged.
