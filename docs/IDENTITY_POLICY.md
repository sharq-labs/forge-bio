# Identity Policy

**Status:** PRE-CODE CANDIDATE

## 1. Principle

Names are attributes, not scientific identities.

Forge Bio uses immutable internal entity IDs and provenance-bearing external identifier assignments.

## 2. MVP identity classes

- DiseaseConcept
- Gene
- Protein
- ProteinComplex
- PathwayConcept
- Publication
- Study

Drug/chemical identity is deferred to the repurposing layer, but follows the same policy.

## 3. Entity and representation

```text
Entity
    entity_id
    entity_kind

EntityRevision
    revision_id
    entity_id
    representation
    valid_interval
    availability_attestation
    provenance
```

A current provider representation is not silently substituted for a historical revision.

## 4. ExternalIdentifierAssignment

```text
ExternalIdentifierAssignment
    assignment_id
    entity_id
    namespace
    local_id
    relation
    valid_from
    valid_to
    availability_attestation
    source_release
    mapping_confidence
    review_status
    provenance_id
```

Relations:
- EXACT
- BROAD
- NARROW
- RELATED
- REPLACED_BY
- MERGED_INTO
- SPLIT_FROM

Ambiguity is preserved.

## 5. Historical identity plane

Model-visible resolution may use only mappings admissible by T.

Historical resolution returns:
- resolved entity ID(s)
- ambiguity state
- mapping provenance
- knowledge watermark
- resolution-policy version

Modern reconciliation cannot become a hidden feature.

## 6. Evaluation bridge

Modern mappings may be used after prediction sealing solely to match a historical candidate to a future outcome identity.

The bridge:
- lives behind the evaluation boundary;
- has its own version and digest;
- cannot be imported by ranking/feature code;
- is included in sensitivity analysis when materially outcome-changing;
- reconciles identity but does not establish biological causality;
- cannot convert a locus/variant association into a gene-level validation without OutcomeGeneAssignmentPolicy;
- cannot broaden a failed match post hoc outside preregistered sensitivity rules.

## 7. Disease-as-of-T

Disease concepts may split, merge, or change definition.

```text
HistoricalDiseaseConcept
    historical_term_id
    vocabulary
    vocabulary_release
    label_at_T
    admissible_relations
    mapping_to_internal_entity
```

Present-day subtype structure is not model-visible unless admissible by T.

## 8. Gene / protein / target separation

Never equate:

```text
gene == protein == target
```

A gene may map to multiple protein products or isoforms.

Target is a role in a disease/context-specific hypothesis.

Protein complexes are first-class where required.

## 9. Candidate eligibility

Candidate inclusion is evidence-backed.

For B-TGT V0:

```text
eligible
IF gene identity existed/admissible by T
AND disease identity is admissible by T
AND benchmark inclusion policy permits the entity
```

A present-day curated "druggable genes" list is prohibited unless its own knowledge watermark passes.

## 10. CandidateUniverse artifact

CandidateUniverse is separate from HistoricalKnowledgeView.

```text
CandidateUniverse
    universe_id
    benchmark_id
    cutoff
    entity_kind
    disease_set_id
    inclusion_policy_version
    exclusion_policy_version
    source_snapshot_ids
    identity_policy_version
    knowledge_watermark
    candidate_membership_records
    digest
```

Membership records retain the provenance establishing historical eligibility.

## 11. Deterministic hypothesis identity

Every hypothesis has a deterministic scientific key independent of ranking/run.

For V0:

```text
HypothesisKey =
canonical_hash(
    hypothesis_type,
    historical_disease_entity_id,
    gene_entity_id,
    context_key,
    direction_if_applicable,
    hypothesis_schema_version
)
```

Run-specific prediction IDs are separate.

## 12. Canonical serialization

Any object used for identity or content hashing follows a defined canonical serialization:
- explicit schema version
- stable field ordering
- stable enum encoding
- normalized Unicode
- explicit null/UNKNOWN representation
- no unordered map/set serialization
- deterministic float policy
- canonical date/interval encoding

Equivalent scientific content must not receive a different hash merely because a different JSON library was used.

## 13. Mapping sensitivity

When an outcome match requires non-EXACT modern mapping, report:
- exact-only result
- broader-mapping result
- affected candidates
- mapping uncertainty

No post-hoc mapping expansion may rescue a failed prediction.

## 14. Gold-set verification

Before confirmatory benchmarking, create a reviewed fixture covering:
- renamed genes
- merged/withdrawn IDs
- disease splits/merges
- one-to-many mappings
- protein isoforms
- complexes
- ambiguous aliases

Measure and retain resolution errors.

## 15. Identity reconciliation vs outcome assignment

Evaluation identity asks:

> Are these historical and future identifiers representations of the same entity?

Outcome assignment asks a different question:

> Does the future evidence scientifically establish this gene/entity as the endpoint object?

These operations are separate.

Modern identifier reconciliation is allowed behind the evaluation boundary. Modern biological assignment (for example locus-to-gene inference) is not identity resolution and must follow the benchmark's outcome-assignment policy.

## 16. Historical novelty mapping

Historical novelty audits may use evaluation-side identity reconciliation to search for pre-T evidence.

The audit result is provenance-bearing and may be:
- NOVEL_CONFIRMED;
- KNOWN_AT_T;
- NOVELTY_AMBIGUOUS.

Ambiguous mapping may not be coerced into novelty.
