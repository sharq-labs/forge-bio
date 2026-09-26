# Model Analysis Plan Schema

**Status:** NORMATIVE PRE-CODE V1

The MAP is frozen before confirmatory execution. The runtime must reject configuration drift from the frozen MAP hash.

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
  knowledge_watermark: string

baselines:
  primary_comparator_id: string
  baseline_ids: [string]
  discoverability_control_id: string

statistics:
  primary_metric_id: string
  primary_k_or_budget: string
  normalized_companion_metric_id: string
  ci_method: string
  resampling_unit: string
  multiplicity_policy: string
  success_threshold: string
  all_frame_utility_metric_id: string
  dependence_sensitivity_method: string

outcome_commitment:
  future_outcome_source_release_ids: [string]
  future_outcome_snapshot_ids: [string]
  future_outcome_snapshot_digest: string
  outcome_ledger_digest: string
  adjudication_batch_digest: string
  evaluation_identity_bridge_digest: string

coverage_gates:
  max_temporal_unknown_fraction: number
  min_identity_resolution_fraction: number
  min_outcome_coverage_fraction: number
  max_novelty_ambiguity_fraction: number
  max_assignment_ambiguity_fraction: number
  min_lineage_completeness_fraction: number

planned_analyses:
  subgroup_analyses: [string]
  sensitivity_analyses: [string]
  source_ablations: [string]
  negative_controls: [string]

governance:
  benchmark_design_provenance_id: string
  ranking_team: [string]
  outcome_adjudication_role: string
  lockbox_custodian_role: string
  permitted_lockbox_accesses: integer
  sealed_disease_blinding_policy: string
  sealed_outcome_adjudicator_blinding_required: boolean
  validation_generation_status: ACTIVE | SPENT_FOR_MODEL_SELECTION | RETIRED
  validation_access_count: integer
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
- outcome gene-assignment policy;
- phenotype-match policy;
- genetic-replication policy;
- novelty / pre-T genetic-state policy;
- zero-event policy;
- validation generation;
- exact future-outcome snapshot commitment;
- all-frame utility metric;
- dependence-sensitivity method;
- success rule.

Any post-freeze change creates a new MAP generation or a documented deviation. It never silently mutates the original plan.
