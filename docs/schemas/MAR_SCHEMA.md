# Model Analysis Report Schema

**Status:** NORMATIVE PRE-CODE V1

The MAR records what actually happened. Negative and invalid results receive a MAR too.

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
  provider_versions: [string]

verification:
  temporal_tests: string
  future_sentinel_tests: string
  watermark_tests: string
  identity_tests: string
  metric_golden_tests: string
  dependency_wall_tests: string
  reproducibility_result: string

coverage:
  admitted_count: integer
  refused_count: integer
  unknown_count: integer
  novelty_ambiguity_fraction: number
  assignment_ambiguity_fraction: number
  lineage_completeness_fraction: number
  outcome_coverage_fraction: number
  ancestry_population_missing_fraction: number

results:
  primary_endpoint_subtype: string
  primary_metric: string
  primary_value: number
  primary_comparator: string
  baseline_delta: number
  confidence_interval: string
  success_rule_result: PASS | FAIL | INVALID
  normalized_companion_metric: string
  secondary_results: [object]

bias_and_sensitivity:
  discoverability_control_result: object
  attention_momentum_result: object
  historical_novelty_result: object
  gene_assignment_sensitivity: object
  outcome_source_ablation: object
  ancestry_population_analysis: object
  reporting_bias_analysis: object
  negative_control_results: [object]

governance:
  benchmark_design_provenance_id: string
  lockbox_access_log_ref: string
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
- zero-event disease handling matches the frozen estimand;
- population/ancestry limitations are explicit;
- post-hoc analyses are labelled exploratory.
