# ADR-011 — Genomic Identity, Harmonization, and LD Provenance

**Status:** Accepted — BIG 0R3 hardening  
**Decision scope:** B-TGT genetic evidence and future genetic outcomes

## Problem

B-TGT-E1 reasons about variants, loci, alleles, LD proxies, and locus-to-gene assignment. These objects cannot be represented safely as free-text rsIDs or coordinates.

The same biological allele may appear under:
- different genome assemblies;
- shifted indel representations;
- changed rsIDs;
- different strand/orientation conventions;
- multiple provider-specific locus definitions.

## Decision

The identity layer adds first-class scientific entities:

```text
GenomeAssembly
ReferenceSequence
GenomicVariant
GenomicLocus
PhenotypeConcept
Cohort
Dataset
Biobank
Consortium
SampleSet
LDReferencePanel
```

### GenomicVariant

Canonical identity includes a normalized molecular state against an explicit reference sequence.

```text
GenomicVariant
    variant_id
    reference_sequence_id
    normalized_location
    reference_allele
    alternate_allele
    normalization_policy_version
```

An rsID is an external identifier, not the scientific identity.

### GenomicLocus

```text
GenomicLocus
    locus_id
    assembly_id
    interval
    lead_variant_id?
    credible_set_id?
    locus_definition_policy_version
```

### Harmonization

Every coordinate/allele transformation is a provenance-bearing artifact:

```text
VariantHarmonizationArtifact
    source_variant_representation
    source_assembly_id
    target_assembly_id
    reference_release
    normalization_algorithm
    liftover_chain_or_mapping_ref?
    strand_resolution
    ambiguity_state
    knowledge_watermark
    provenance_id
```

Ambiguous allele orientation, failed liftover, or unresolved normalization fails closed for strict replication matching.

### LD relation

LD is not a timeless property.

```text
LDRelation
    variant_a
    variant_b
    population_or_ancestry
    reference_panel_id
    reference_panel_release
    assembly_id
    metric
    value
    derivation_method
    availability_attestation
    knowledge_watermark
```

The replication policy freezes the allowed LD metric/threshold and reference-panel mode.

Allowed evaluation modes:

```text
HISTORICAL_LD
MODERN_EVALUATION_LD
```

MODERN_EVALUATION_LD is evaluation-only, versioned, and sensitivity-tested when outcome classification changes.

## Consequences

- variant/locus identity becomes deterministic and reviewable;
- genome-build/allele normalization is not a hidden utility step;
- LD proxy matching carries ancestry/reference-panel provenance;
- phenotype and cohort/sample lineage gain canonical identities;
- current harmonization resources cannot silently become historical model-visible knowledge.
