# Model Analysis Plan Schema

**Status:** NORMATIVE PRE-CODE V1

The MAP is frozen (that is, `SEALED`) before confirmatory execution.

Executable companion: [MAP JSON Schema](../../schemas/map.v1.schema.json). The runtime must reject configuration drift from the sealed MAP hash.

## Required top-level structure

```yaml
map_id: string
schema_version: map-v1
status: DRAFT | SEAL_CANDIDATE | SEALED | RETIRED
sealed_by_attestation_id: string?   # non-null iff status = SEALED
created_at: datetime                # self-reported; never proves order (INV-S3)
digest: string?                     # required (sha256, 64 hex) when status = SEALED

qoi_ref: string
context_of_use_ref: string
estimand_ref: string

benchmark:
  benchmark_id: string
  generation: string
  cutoff: date
  horizon: duration   # e.g. "5y"
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
  endpoint_primary_subtype: string   # V0: const E1-NOVEL-STRICT (Freeze Statement §1)
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
  combined_nuisance_model_id: string   # pattern CNM-…
  baseline_ids: [string]
  discoverability_control_id: string
  nuisance_feature_family_ids:   # unique, ≥ 7, drawn from:
    [DISEASE_SPECIFIC_ATTENTION_VOLUME, DISEASE_SPECIFIC_ATTENTION_MOMENTUM,
     GLOBAL_ATTENTION_VOLUME, GLOBAL_ATTENTION_MOMENTUM, GLOBAL_GENE_POPULARITY,
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
  alpha: 0.05                                    # const in the schema
  minimum_scientifically_meaningful_effect: number   # > 0; planning effect only (INV-E7)
  power_target: number                           # 0.80–0.99
  power_analysis_artifact_id: string
  success_threshold_numeric: number
  success_threshold_semantics: ONE_SIDED_P_VALUE_STRICTLY_BELOW | OTHER_PREREGISTERED
  success_rule_ref: string
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
  outcome_discovery_spec_digest: string            # sha256, 64 hex
  outcome_discovery_run_digest: string             # sha256, 64 hex
  outcome_discovery_seal_attestation_id: string    # order proven by seal_time (INV-S3), not a self-reported date

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
  permitted_lockbox_accesses: integer   # 0–1
  sealed_disease_blinding_policy: string
  sealed_outcome_adjudicator_blinding_required: boolean
  validation_generation_status: ACTIVE | SPENT_FOR_MODEL_SELECTION | RETIRED
  validation_access_count: integer
  validation_max_disclosure_level: AGGREGATE_ONLY | SUBGROUP | PER_CASE | FULL_LABEL
  deviation_policy: string

stop_conditions: [string]

comparison_design:
  primary_comparison_semantics: NESTED_ADD_DISEASE_SPECIFIC_EVIDENCE_ONLY
  capacity_parity_required: true
  learner_family_id: string
  nuisance_feature_block_id: string
  nuisance_feature_block_digest: string       # sha256, 64 hex
  biological_feature_block_id: string
  biological_feature_block_digest: string     # sha256, 64 hex
  preprocessing_artifact_id: string
  hyperparameter_search_space_digest: string  # sha256, 64 hex
  tuning_budget_id: string
  early_stopping_policy_id: string
  random_seed_policy_id: string
  placebo_arm_policy_id: string
  ranking_universe_rule_id: string
```

## Conditional requirements (encoded in the JSON Schema)

- `status = SEALED` requires a 64-hex `digest` and a non-null `sealed_by_attestation_id`. Any other status requires `sealed_by_attestation_id = null` (INV-S1). There is no `frozen_at` (INV-S5).
- `governance.study_tier` ∈ {CONFIRMATORY, PROSPECTIVE} requires at least one independent adjudicator, a non-null `external_seal_attestation_id`, `sealed_outcome_adjudicator_blinding_required = true`, `validation_generation_status = ACTIVE`, `validation_max_disclosure_level = AGGREGATE_ONLY`, and non-vacuous coverage gates.

## B-TGT-E1-v0 constants

When `benchmark.benchmark_id = B-TGT-E1-v0`, the schema fixes the values from [V0_FREEZE_STATEMENT.md](../V0_FREEZE_STATEMENT.md):

| Field | Constant |
|---|---|
| `benchmark.cutoff` | one of 2005-12-31, 2008-12-31, 2011-12-31, 2014-12-31 (the custodian-selected T\*) |
| `benchmark.horizon` | one of 3y, 5y, 7y, 10y (the custodian-selected H\*) |
| `statistics.primary_metric_id` | `EVENT_RANK_PERCENTILE_V1` |
| `statistics.primary_metric_kind` | `EVENT_RANK_PERCENTILE` |
| `statistics.primary_review_budget` | `null` |
| `statistics.test_statistic_id` | `PAIRED_SIGNFLIP_MEAN_DELTA_ONE_SIDED_V1` |
| `statistics.test_direction` | `ONE_SIDED_GREATER` |
| `statistics.resampling_unit` | `DISEASE` |
| `statistics.ci_method` | `DISEASE_LEVEL_BCA_BOOTSTRAP_95` |
| `statistics.dependence_sensitivity_method` | `DISEASE_FAMILY_BLOCK_BOOTSTRAP_AND_FAMILY_LEVEL_SIGNFLIP` |
| `statistics.alpha` | 0.05 |
| `statistics.minimum_scientifically_meaningful_effect` | 0.05 (planning only) |
| `statistics.power_target` | 0.8 |
| `statistics.success_threshold_numeric` | 0.05 |
| `statistics.success_threshold_semantics` | `ONE_SIDED_P_VALUE_STRICTLY_BELOW` |
| `statistics.success_rule_ref` | `docs/V0_FREEZE_STATEMENT.md#3` |
| `statistics.confirmatory_generation_budget_id` | `CPB-FORGE-BIO-B-TGT-E1-V0` |
| `baselines.nuisance_feature_family_ids` | exactly 14 items (the families of `config/big0f-nuisance-manifest.v2.json`) |
| `comparison_design.placebo_arm_policy_id` | `PERMUTED_BIOLOGY_WITHIN_DISEASE_K19_V1` |
| `comparison_design.ranking_universe_rule_id` | `NOVEL-STRICT-ELIGIBILITY-FILTERED-V1` |
| `policies.endpoint_primary_subtype` | `E1-NOVEL-STRICT` |
| `coverage_gates.min_historical_genetic_coverage_grade` | `MODERATE`. NOVEL-STRICT is undefined below MODERATE, and HIGH-only is the SENS-COVERAGE-HIGH label analysis, never the primary population. |

`success_threshold_numeric` is therefore the p-value threshold of the frozen sign-flip test, never an effect-size threshold (INV-E7).

## Freeze invariants

A MAP with status `SEAL_CANDIDATE` or `SEALED` must not contain unresolved placeholders for:
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
- Combined Nuisance primary comparator, placebo-arm policy and ranking-universe rule;
- confirmatory-generation budget;
- governance role separation / external sealing for confirmatory tiers.

Any post-freeze change creates a new MAP generation or a documented deviation. It never silently mutates the original plan.

## Cross-field semantic invariants

JSON Schema is not the only validator.

When implementation begins, one canonical cross-field semantic validator must enforce scientific invariants ([SEMANTIC_INVARIANTS.md](../SEMANTIC_INVARIANTS.md); HARNESS rows are not enforced until the verification harness exists) including:
- STRICT_HISTORICAL watermark is not UNKNOWN and does not exceed cutoff;
- primary comparator equals Combined Nuisance Model;
- confirmatory ranking/adjudication/custodian roles are separated;
- confirmatory disclosure/lockbox rules remain sealed;
- confirmatory coverage gates are non-vacuous;
- alpha/power/success thresholds are numeric.

A SEALED artifact is valid only when both JSON Schema and the future canonical semantic-invariant checks pass.
