# Model Analysis Report Schema

**Status:** NORMATIVE PRE-CODE V1

The MAR records what actually happened.

Executable companion: [MAR JSON Schema](../../../schemas/mar.v1.schema.json). Negative and invalid results receive a MAR too.

## Required top-level structure

```yaml
mar_id: string
schema_version: string
map_id: string
map_digest: string
benchmark_id: string
benchmark_generation: string

execution:
  code_commit: string
  environment_digest: string
  container_digest: string
  started_at: datetime
  completed_at: datetime
  ranking_artifact_digest: string

data:
  historical_snapshot_ids: [string]
  candidate_universe_digest: string
  future_outcome_snapshot_ids: [string]
  future_outcome_snapshot_digest: string
  outcome_ledger_digest: string
  adjudication_batch_digest: string
  evaluation_identity_bridge_digest: string
  validation_generation_id: string
  scientific_event_family_ledger_digest: string
  provider_coupling_assessment_digest: string
  provider_versions: [string]
  genomic_harmonization_artifact_ids: [string]

verification:
  temporal_tests: string
  future_sentinel_tests: string
  watermark_tests: string
  identity_tests: string
  metric_golden_tests: string
  dependency_wall_tests: string
  genomic_identity_tests: string
  cross_anchor_event_reuse_tests: string
  preprocessing_lineage_tests: string
  reproducibility_result: string

coverage:
  admitted_count: integer
  refused_count: integer
  unknown_count: integer
  novelty_ambiguity_fraction: number
  assignment_ambiguity_fraction: number
  phenotype_match_ambiguity_fraction: number
  pre_t_genetic_state_ambiguity_fraction: number
  replication_inconclusive_fraction: number
  lineage_completeness_fraction: number
  outcome_coverage_fraction: number
  ancestry_population_missing_fraction: number
  historical_genetic_coverage_grade_distribution: object
  variant_harmonization_ambiguity_fraction: number
  event_family_deduplication_fraction: number

results:
  primary_endpoint_subtype: string
  primary_metric: string
  primary_value: number
  primary_comparator: string
  baseline_delta: number
  confidence_interval: string
  success_rule_result: PASS | FAIL | INVALID
  normalized_companion_metric: string
  all_frame_review_budget_utility: object
  event_bearing_disease_coverage: number
  zero_event_disease_review_burden: object
  secondary_results: [object]

bias_and_sensitivity:
  discoverability_control_result: object
  attention_momentum_result: object
  historical_novelty_result: object
  gene_assignment_sensitivity: object
  phenotype_match_sensitivity: object
  replication_policy_sensitivity: object
  disease_family_block_ci_sensitivity: object
  outcome_source_ablation: object
  ancestry_population_analysis: object
  reporting_bias_analysis: object
  historical_observability_sensitivity: object
  ld_reference_panel_sensitivity: object
  input_outcome_provider_coupling_sensitivity: object
  event_family_credit_sensitivity: object
  negative_control_results: [object]

governance:
  benchmark_design_provenance_id: string
  lockbox_access_log_ref: string
  validation_generation_status: string
  validation_access_count: integer
  validation_max_disclosure_level: string
  adjudication_blinding_status: string
  adjudication_summary: string
  deviations: [object]

interpretation:
  claim_maturity_level: string
  applicability_domain: string
  limitations: [string]
  failed_analyses: [string]
  scientific_interpretation: string
```

## Reporting invariants

- a failed primary endpoint is not replaced by a successful secondary endpoint;
- negative controls are reported even when embarrassing;
- ambiguity and missingness are reported, not hidden;
- exact claim language is bounded by the endpoint actually evaluated;
- zero-event disease handling matches the frozen estimand and all-frame utility is reported;
- strongest L3 status is not claimed when sealed outcome adjudicators saw rank/order;
- exact outcome snapshot/ledger/event-family/provider-coupling commitments match the MAP;
- strict novelty cases meet the frozen historical genetic-search coverage threshold;
- genomic harmonization/LD provenance is complete for outcome-defining matches;
- provider-coupling and historical-observability sensitivities are reported;
- phenotype-match and replication-policy sensitivities are reported where material;
- disease-family/block dependence sensitivity is reported;
- population/ancestry limitations are explicit;
- post-hoc analyses are labelled exploratory.
