# Model Analysis Plan Schema

**Status:** NORMATIVE PRE-CODE V1

The MAP is frozen before confirmatory execution.

Executable companion: [MAP JSON Schema](../../schemas/map.v1.schema.json). The runtime must reject configuration drift from the frozen MAP hash.

## Required top-level structure

```yaml
map_id: string
schema_version: string
status: DRAFT | FROZEN | RETIRED
created_at: datetime
frozen_at: datetime?
digest: string?

qoi_ref: string
context_of_use_ref: string
estimand_ref: string

benchmark:
  benchmark_id: string
  generation: string
  cutoff: date
  horizon: duration
  disease_sampling_frame_id: string
  candidate_universe_id: string
  development_split_id: string
  validation_split_id: string
  validation_generation_id: string
  sealed_lockbox_id: string

providers:
  past_snapshot_ids: [string]
  future_outcome_source_ids: [string]
  provider_card_versions: [string]
  reconstruction_fidelity_verdicts: [string]

policies:
  scientific_operating_mode: STRICT_HISTORICAL | HISTORICAL_INPUT_MODERN_PRIOR | CURRENT_DISCOVERY
  historical_data_policy: ARCHIVED_ONLY | RECONSTRUCTED_ALLOWED
  temporal_policy_version: string
  identity_policy_version: string
  evidence_schema_version: string
  endpoint_policy_version: string
  endpoint_primary_subtype: string
  outcome_gene_assignment_policy_version: string
  historical_novelty_policy_version: string
  pre_t_genetic_state_policy_version: string
  outcome_phenotype_match_policy_version: string
  genetic_replication_policy_version: string
  genomic_identity_policy_version: string
  variant_harmonization_policy_version: string
  ld_policy_version: string
  historical_genetic_coverage_policy_version: string
  genetic_observability_policy_version: string
  scientific_event_family_policy_version: string
  provider_coupling_policy_version: string
  cross_anchor_event_reuse_policy_version: string
  independence_policy_version: string
  adjudication_policy_version: string
  zero_event_policy_version: string
  multiplicity_policy_version: string

model:
  algorithm_id: string
  model_version: string
  feature_set_id: string
  config_hash: string
  random_seeds: [integer]
  knowledge_watermark:
    kind: NON_KNOWLEDGE_BEARING | DATED | UNKNOWN
    date: date?
  preprocessing_artifact_ids: [string]
  feature_selection_artifact_id: string?

baselines:
  primary_comparator_id: string
  combined_nuisance_model_id: string
  baseline_ids: [string]
  discoverability_control_id: string
  nuisance_feature_family_ids:
    [ATTENTION, ATTENTION_MOMENTUM, GLOBAL_GENE_POPULARITY,
     ANNOTATION_DENSITY, GENE_LENGTH, VARIANT_OPPORTUNITY,
     REGIONAL_GENE_DENSITY, LD_ARCHITECTURE, CROSS_TRAIT_PLEIOTROPY,
     GENETIC_OBSERVABILITY, DISEASE_SAMPLE_SIZE_TRAJECTORY, PROVIDER_COVERAGE]

statistics:
  primary_metric_id: typed identifier
  primary_metric_kind: EVENT_RANK_PERCENTILE | RECALL_AT_K | RECALL_AT_PERCENT | NDCG | MRR | OTHER_PREREGISTERED
  primary_k_or_budget: string
  primary_review_budget: integer?
  normalized_companion_metric_id: string
  ci_method: string
  resampling_unit: string
  multiplicity_policy: string
  null_hypothesis: string
  alternative_hypothesis: string
  test_statistic_id: string
  test_direction: ONE_SIDED_GREATER | ONE_SIDED_LESS | TWO_SIDED
  alpha: number
  minimum_scientifically_meaningful_effect: number
  power_target: number
  power_analysis_artifact_id: string
  success_threshold_numeric: number
  confirmatory_generation_budget_id: string
  all_frame_utility_metric_id: string
  dependence_sensitivity_method: string

outcome_commitment:
  future_outcome_source_release_ids: [string]
  future_outcome_snapshot_ids: [string]
  future_outcome_snapshot_digest: string
  outcome_ledger_digest: string
  adjudication_batch_digest: string
  evaluation_identity_bridge_digest: string
  scientific_event_family_ledger_digest: string
  provider_coupling_assessment_digest: string
  outcome_event_discovery_frozen_at: datetime

coverage_gates:
  max_temporal_unknown_fraction: number
  min_identity_resolution_fraction: number
  min_outcome_coverage_fraction: number
  max_novelty_ambiguity_fraction: number
  max_assignment_ambiguity_fraction: number
  min_lineage_completeness_fraction: number
  min_historical_genetic_coverage_grade: HIGH | MODERATE | LOW
  max_variant_harmonization_ambiguity_fraction: number

planned_analyses:
  subgroup_analyses: [string]
  sensitivity_analyses: [string]
  source_ablations: [string]
  negative_controls: [string]

governance:
  benchmark_design_provenance_id: string
  study_tier: DEVELOPMENT | CONFIRMATORY | PROSPECTIVE
  ranking_team: [string]
  outcome_adjudication_role: string
  lockbox_custodian_role: string
  independent_adjudicator_ids: [string]
  external_seal_attestation_id: string?
  permitted_lockbox_accesses: integer
  sealed_disease_blinding_policy: string
  sealed_outcome_adjudicator_blinding_required: boolean
  validation_generation_status: ACTIVE | SPENT_FOR_MODEL_SELECTION | RETIRED
  validation_access_count: integer
  validation_max_disclosure_level: AGGREGATE_ONLY | SUBGROUP | PER_CASE | FULL_LABEL
  deviation_policy: string

stop_conditions: [string]
```

## Freeze invariants

A FROZEN MAP must not contain unresolved placeholders for:
- primary endpoint subtype;
- primary metric;
- primary comparator;
- cutoff;
- horizon;
- candidate universe;
- disease frame;
- scientific operating mode and historical data policy;
- genomic identity / variant-harmonization / LD policy;
- historical genetic-search coverage and observability policy;
- scientific-event-family / provider-coupling / cross-anchor reuse policy;
- outcome gene-assignment policy;
- phenotype-match policy;
- genetic-replication policy;
- novelty / pre-T genetic-state policy;
- zero-event policy;
- validation generation;
- exact future-outcome snapshot/event-family/provider-coupling commitment;
- all-frame utility metric;
- dependence-sensitivity method;
- numeric success rule / alpha / power / minimum effect;
- Combined Nuisance primary comparator;
- confirmatory-generation budget;
- governance role separation / external sealing for confirmatory tiers.

Any post-freeze change creates a new MAP generation or a documented deviation. It never silently mutates the original plan.

## Cross-field semantic invariants

JSON Schema is not the only validator.

`scripts/scientific_invariants.py` additionally enforces scientific invariants including:
- STRICT_HISTORICAL watermark is not UNKNOWN and does not exceed cutoff;
- primary comparator equals Combined Nuisance Model;
- confirmatory ranking/adjudication/custodian roles are separated;
- confirmatory disclosure/lockbox rules remain sealed;
- confirmatory coverage gates are non-vacuous;
- alpha/power/success thresholds are numeric.

A FROZEN artifact is valid only when both JSON Schema and semantic invariants pass.
