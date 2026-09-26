# Question of Interest Schema

**Status:** NORMATIVE PRE-CODE V1

Every governed study must instantiate one Question of Interest (QoI).

Executable companion: [QoI JSON Schema](../../schemas/qoi.v1.schema.json).

## Required schema

```yaml
question_id: string
schema_version: string
benchmark_family: string
benchmark_role: string
hypothesis_type: string

disease_scope:
  regime: string
  inclusion_policy_id: string
  exclusion_policy_id: string

historical_cutoff: date
candidate_universe_policy_id: string

future_endpoint:
  endpoint_family: string
  primary_subtype: string
  endpoint_policy_version: string
  evidence_quality_policy_version: string
  pre_t_genetic_state_policy_version: string
  phenotype_match_policy_version: string
  gene_assignment_policy_version: string
  replication_policy_version: string
  genomic_identity_policy_version: string
  variant_harmonization_policy_version: string
  ld_policy_version: string
  historical_genetic_coverage_policy_version: string
  event_family_credit_policy_version: string

evaluation_horizon:
  duration: string
  observation_end_policy: string

estimand_id: string
primary_metric_id: string
primary_review_budget_or_k: string
secondary_all_frame_utility_metric_id: string
baseline_family_ids: [string]
discoverability_control_id: string
historical_observability_sensitivity_policy_id: string
provider_coupling_policy_id: string

context_of_use_id: string
claim_boundary: string
```

## Invariants

- exactly one primary endpoint subtype;
- exactly one primary metric;
- cutoff and horizon are explicit;
- disease/genetic regime is explicit;
- candidate universe is versioned;
- estimand and zero-event policy are not implicit;
- baseline family includes endpoint-appropriate attention/discoverability controls;
- genomic identity/harmonization/LD policy is explicit;
- historical genetic-search coverage policy is explicit;
- event-family credit policy is explicit;
- historical observability and provider-coupling sensitivities are named;
- claim boundary states what the study does **not** establish.

## B-TGT-E1-v0 example

```yaml
question_id: B-TGT-E1-v0-Q1
schema_version: qoi-v1
benchmark_family: B-TGT
benchmark_role: B-TGT-A1-disease-gene-association-prioritization
hypothesis_type: TargetAssociationCandidate

disease_scope:
  regime: common-complex-germline
  inclusion_policy_id: disease-frame-v0
  exclusion_policy_id: disease-exclusions-v0

historical_cutoff: TO_BE_SELECTED_BY_PROVIDER_AUDIT
candidate_universe_policy_id: gene-universe-v0

future_endpoint:
  endpoint_family: E1-human-genetic-support
  primary_subtype: TO_BE_FROZEN
  endpoint_policy_version: e1-v0
  evidence_quality_policy_version: TO_BE_FROZEN
  pre_t_genetic_state_policy_version: pre-t-genetic-state-v1
  phenotype_match_policy_version: phenotype-match-v1
  gene_assignment_policy_version: outcome-gene-assignment-v1
  replication_policy_version: genetic-replication-v1
  genomic_identity_policy_version: genomic-identity-v1
  variant_harmonization_policy_version: variant-harmonization-v1
  ld_policy_version: ld-provenance-v1
  historical_genetic_coverage_policy_version: historical-genetic-coverage-v1
  event_family_credit_policy_version: event-family-credit-v1

evaluation_horizon:
  duration: TO_BE_FROZEN
  observation_end_policy: fixed-horizon

estimand_id: b-tgt-e1-estimand-v0
primary_metric_id: TO_BE_FROZEN
primary_review_budget_or_k: TO_BE_FROZEN
secondary_all_frame_utility_metric_id: observed-event-yield-per-total-review-budget
baseline_family_ids:
  - random
  - historical-attention
  - attention-momentum
  - discoverability-control
  - deterministic-evidence
discoverability_control_id: discoverability-v0
historical_observability_sensitivity_policy_id: genetic-observability-v1
provider_coupling_policy_id: input-outcome-coupling-v1

context_of_use_id: research-prioritization-v1
claim_boundary: disease-gene association prioritization only; no causal-target, intervention-direction, tractability, or clinical claim
```
