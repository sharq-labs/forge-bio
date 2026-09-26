# ADR-013 — Scientific Event Identity, Source Coupling, and Adaptive Reuse

**Status:** Accepted — BIG 0R3 hardening  
**Decision scope:** future-event counting, provider independence, temporal training, and validation feedback

## 1. Scientific event identity

Database rows, preprints, publications, and curated records may be manifestations of one underlying scientific event.

Introduce:

```text
ScientificEventFamily
    event_family_id
    disease_id
    event_domain
    originating_study_ids
    primary_public_manifestations
    secondary_curated_manifestations
    provenance
```

For genetic discovery:

```text
GeneticDiscoveryEventFamily
    event_family_id
    disease_id
    locus_ids
    discovery_study_ids
    gene_assignments
    independence_family_ids
```

The primary benchmark freezes a credit policy. Default V0:

```text
one scientific event family receives at most one primary event credit
```

Multiple gene assignments from one locus do not automatically create multiple independent future discoveries.

## 2. Outcome-event discovery freeze

Sealed outcome event discovery/adjudication is completed and committed before model rank/order is revealed.

The committed artifact includes:
- discovered event families;
- event manifestations;
- phenotype matching;
- gene assignment;
- replication assessment;
- adjudication batch digest.

Searching for future events after seeing the rank invalidates strongest L3 status.

## 3. Input/outcome provider coupling

Every provider declares:

```text
ProviderLineage
    provider_id
    upstream_source_families
    curation_pipeline_family
    ontology_families
    identity_mapping_families
```

The benchmark derives an `InputOutcomeCouplingAssessment` between Past inputs and Future outcome sources.

Required sensitivities include, where feasible:
- exclude same curation-pipeline family;
- external future-source replication;
- upstream-source-family ablation.

A model that only predicts the future state of the same curation pipeline does not earn an independent biological-discovery claim.

## 4. Cross-anchor event reuse

Rolling-origin training must prevent one future event from receiving uncontrolled repeated training weight across overlapping anchors.

Introduce:

```text
CrossAnchorEventReusePolicy
    event_family_grouping
    maximum_total_event_credit
    anchor_weighting
    overlap_handling
```

Default:
- group by ScientificEventFamily;
- total weight contributed by one event family is bounded;
- report effective sample size after grouping.

## 5. Validation disclosure level

Adaptive risk depends on feedback granularity, not access count alone.

```text
ValidationDisclosureLevel
    AGGREGATE_ONLY
    SUBGROUP
    PER_CASE
    FULL_LABEL
```

Validation-generation provenance records both access count and disclosure level.

## Consequences

- duplicated database manifestations cannot inflate event counts;
- locus-to-many-gene assignments cannot silently multiply primary credit;
- Past/Future source coupling becomes visible;
- rolling-origin event duplication is controlled;
- validation adaptivity accounting reflects information revealed, not only number of accesses.
