# Disease, Pathogen, and Therapeutic Scientific Profile Model

**Status:** NORMATIVE PRE-CODE CANDIDATE — BIG 0R4

The scientific profile layer defines what Forge Bio can know about a disease, pathogen, virus, or therapeutic without collapsing evidence into unsupported truth.

Every field below is represented through identity + claim/evidence + provenance + uncertainty. A profile field is not automatically a fact merely because one provider contains it.

---

## 1. DiseaseScientificProfile

```text
DiseaseScientificProfile
    disease_id
    classification
    disease_family
    subtype_relations

    phenotype_ids
    manifestation_claim_ids

    affected_organ_ids
    affected_tissue_ids
    affected_cell_type_ids

    gene_claim_ids
    protein_claim_ids
    variant_claim_ids
    pathway_claim_ids
    biological_process_claim_ids

    mechanism_claim_ids
    biomarker_claim_ids

    epidemiology_claim_ids
    population_context_ids
    risk_factor_claim_ids

    stage_model_id?
    progression_model_id?

    target_hypothesis_ids
    therapeutic_evidence_ids

    contradiction_ids
    evidence_gap_ids
    uncertainty_bundle

    temporal_state
    provenance
```

### Key rule

Disease identity, phenotype, mechanism, and treatment evidence are separate layers.

```text
Disease X
ASSOCIATED_WITH
Gene Y
```

is not equivalent to:

```text
Gene Y
CAUSES
Disease X
```

and neither automatically means:

```text
Inhibiting Y treats Disease X
```.

---

## 2. PathogenScientificProfile

```text
PathogenScientificProfile
    pathogen_id
    pathogen_type
    taxonomy
    taxonomic_rank

    genome_representation_ids
    gene_ids
    protein_ids

    strain_ids
    pathogen_variant_ids

    host_species_ids
    tissue_tropism_claim_ids
    cell_tropism_claim_ids

    host_receptor_claim_ids
    host_interaction_claim_ids

    lifecycle_stage_ids
    replication_process_claim_ids

    immune_interaction_claim_ids
    immune_evasion_claim_ids

    associated_disease_ids
    virulence_claim_ids

    resistance_claim_ids

    pathogen_target_hypothesis_ids
    host_target_hypothesis_ids
    therapeutic_evidence_ids

    contradiction_ids
    evidence_gap_ids
    uncertainty_bundle

    temporal_state
    provenance
```

### Pathogen kinds

Initial semantic kinds include:

```text
VIRUS
BACTERIUM
FUNGUS
PARASITE
OTHER_PATHOGEN
```

Specific taxonomic knowledge belongs to versioned taxonomy providers rather than hard-coded enums.

---

## 3. Virus-specific profile extension

A virus may additionally expose evidence-backed fields such as:

```text
VirusScientificProfileExtension
    genome_material_class
    strandedness
    genome_segmentation
    envelope_state

    viral_gene_ids
    viral_protein_ids

    entry_mechanism_claim_ids
    replication_compartment_claim_ids
    assembly_release_claim_ids

    host_receptor_claim_ids
    host_factor_claim_ids

    lineage_ids
    viral_variant_ids

    immune_escape_claim_ids
    antiviral_resistance_claim_ids
```

These are research representations, not instructions for modifying, culturing, or engineering pathogens.

---

## 4. PathogenHostScientificProfile

For infectious disease, pathogen-only representation is often incomplete.

```text
PathogenHostScientificProfile
    pathogen_id
    host_species_id

    interaction_claim_ids
    host_receptor_claim_ids
    host_factor_claim_ids

    affected_tissue_ids
    affected_cell_type_ids

    innate_immune_claim_ids
    adaptive_immune_claim_ids

    disease_mechanism_claim_ids
    phenotype_claim_ids

    pathogen_target_hypothesis_ids
    host_target_hypothesis_ids

    therapeutic_evidence_ids

    uncertainty_bundle
    provenance
```

This layer distinguishes:

```text
direct pathogen target
host-directed target
shared disease mechanism
```

rather than treating all therapeutic hypotheses as equivalent.

---

## 5. TherapeuticScientificProfile

```text
TherapeuticScientificProfile
    therapeutic_entity_id

    chemical_structure_id?
    active_moiety_id?
    active_ingredient_ids
    medicinal_product_ids

    therapeutic_modality
    formulation_or_product_context?

    target_claim_ids
    binding_or_engagement_claim_ids
    mechanism_of_action_claim_ids
    intervention_direction_claim_ids
    pathway_effect_claim_ids

    indication_claim_ids
    investigation_event_ids
    approval_event_ids
    withdrawal_event_ids

    efficacy_evidence_ids
    safety_evidence_ids
    adverse_event_evidence_ids

    pharmacokinetic_evidence_ids
    pharmacodynamic_evidence_ids
    metabolism_claim_ids
    interaction_claim_ids

    resistance_claim_ids
    combination_claim_ids

    pathogen_target_claim_ids
    host_target_claim_ids

    contradiction_ids
    evidence_gap_ids
    uncertainty_bundle

    temporal_state
    provenance
```

### Therapeutic modality

Initial semantic categories may include:

```text
SMALL_MOLECULE
ANTIBODY
PROTEIN_BIOLOGIC
PEPTIDE
NUCLEIC_ACID
GENE_THERAPY
CELL_THERAPY
VACCINE
OTHER
```

The profile does not make a patient-specific treatment recommendation.

---

## 6. Evidence-backed property contract

Every property used scientifically is represented as one or more claims.

Example:

```text
Claim
    subject = PathogenProtein P
    predicate = INTERACTS_WITH
    object = HostProtein H
    context = host_species/tissue/cell type
```

with supporting or refuting EvidenceRecords.

The profile stores:
- support;
- contradiction;
- missing evidence;
- uncertainty;
- context;
- time.

It does not flatten them prematurely into one truth flag.

---

## 7. Temporal profiles

Every profile can be reconstructed as-of-T.

```text
DiseaseScientificProfile@T
PathogenScientificProfile@T
TherapeuticScientificProfile@T
PathogenHostScientificProfile@T
```

Historical profile materialization obeys:
- HistoricalKnowledgeView;
- identity policy;
- availability attestations;
- knowledge-watermark propagation;
- provider qualification.

Modern-only profile fields may appear in CURRENT_DISCOVERY but not silently in STRICT_HISTORICAL.

---

## 8. Relationship to digital twins

Profiles are the input substrate.

```text
Scientific Profile
    ↓
T1 Dynamic Knowledge Twin
    ↓
T2 Mechanistic Twin
    ↓
T3 Validated Predictive Twin
    ↓
T4 Validated Intervention Simulation Twin
```

A profile is necessary but not sufficient for a predictive digital twin.
