from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError, FormatChecker

from scripts.scientific_invariants import validate_semantics

ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = ROOT / "schemas"


def validator(name: str) -> Draft202012Validator:
    schema = json.loads((SCHEMAS / name).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def assert_schema_invalid(test: unittest.TestCase, schema: str, artifact: dict) -> None:
    with test.assertRaises(ValidationError):
        validator(schema).validate(artifact)


def valid_map() -> dict:
    versions = {
        "temporal_policy_version": "v1",
        "identity_policy_version": "v1",
        "evidence_schema_version": "v1",
        "endpoint_policy_version": "v1",
        "endpoint_primary_subtype": "E1_NOVEL_STRICT",
        "outcome_gene_assignment_policy_version": "v2",
        "historical_novelty_policy_version": "v1",
        "pre_t_genetic_state_policy_version": "v1",
        "outcome_phenotype_match_policy_version": "v1",
        "genetic_replication_policy_version": "v1",
        "genomic_identity_policy_version": "v1",
        "variant_harmonization_policy_version": "v1",
        "ld_policy_version": "v1",
        "historical_genetic_coverage_policy_version": "v1",
        "genetic_observability_policy_version": "v1",
        "scientific_event_family_policy_version": "v1",
        "provider_coupling_policy_version": "v1",
        "cross_anchor_event_reuse_policy_version": "v1",
        "independence_policy_version": "v1",
        "adjudication_policy_version": "v1",
        "zero_event_policy_version": "v1",
        "multiplicity_policy_version": "v1",
    }
    return {
        "map_id": "MAP-1",
        "schema_version": "map-v1",
        "status": "FROZEN",
        "created_at": "2026-01-01T00:00:00Z",
        "frozen_at": "2026-01-02T00:00:00Z",
        "digest": "sha256:abcdef1234567890",
        "qoi_ref": "QOI-1",
        "context_of_use_ref": "COU-1",
        "estimand_ref": "EST-1",
        "benchmark": {
            "benchmark_id": "B-TGT-E1-v0",
            "generation": "G1",
            "cutoff": "2010-12-31",
            "horizon": "5y",
            "disease_sampling_frame_id": "DF1",
            "candidate_universe_id": "CU1",
            "development_split_id": "DEV1",
            "validation_split_id": "VAL1",
            "validation_generation_id": "VG1",
            "sealed_lockbox_id": "LB1",
        },
        "providers": {
            "past_snapshot_ids": ["P1"],
            "future_outcome_source_ids": ["F1"],
            "provider_card_versions": ["PC1"],
            "reconstruction_fidelity_verdicts": ["PASS"],
        },
        "policies": {
            "scientific_operating_mode": "STRICT_HISTORICAL",
            "historical_data_policy": "ARCHIVED_ONLY",
            **versions,
        },
        "model": {
            "algorithm_id": "ALG1",
            "model_version": "M1",
            "feature_set_id": "FS1",
            "config_hash": "sha256:11111111",
            "random_seeds": [7],
            "knowledge_watermark": {"kind": "DATED", "date": "2010-12-31"},
            "preprocessing_artifact_ids": ["PP1"],
            "feature_selection_artifact_id": None,
        },
        "baselines": {
            "primary_comparator_id": "CNM-B-TGT-E1-V0",
            "combined_nuisance_model_id": "CNM-B-TGT-E1-V0",
            "baseline_ids": ["RANDOM", "ATTENTION", "PLEIOTROPY", "GENOMIC_ARCH"],
            "discoverability_control_id": "DISC1",
            "nuisance_feature_family_ids": [
                "DISEASE_SPECIFIC_ATTENTION_VOLUME",
                "DISEASE_SPECIFIC_ATTENTION_MOMENTUM",
                "GLOBAL_GENE_POPULARITY",
                "ANNOTATION_DENSITY",
                "GENE_LENGTH",
                "VARIANT_OPPORTUNITY",
                "REGIONAL_GENE_DENSITY",
                "LD_ARCHITECTURE",
                "CROSS_TRAIT_PLEIOTROPY",
                "GENETIC_OBSERVABILITY",
                "DISEASE_SAMPLE_SIZE_TRAJECTORY",
                "PROVIDER_COVERAGE"
            ],
        },
        "statistics": {
            "primary_metric_id": "EVENT_RANK_PERCENTILE_V1",
            "primary_metric_kind": "EVENT_RANK_PERCENTILE",
            "primary_k_or_budget": "NA",
            "primary_review_budget": None,
            "normalized_companion_metric_id": "RECALL_AT_1_PERCENT",
            "ci_method": "paired_block_bootstrap",
            "resampling_unit": "disease",
            "multiplicity_policy": "program-alpha-budget",
            "all_frame_utility_metric_id": "OBSERVED_EVENT_YIELD",
            "dependence_sensitivity_method": "family_and_consortium_blocks",
            "null_hypothesis": "incremental lift <= 0",
            "alternative_hypothesis": "incremental lift > 0",
            "test_statistic_id": "PAIRED_DELTA_EVENT_RANK_PERCENTILE",
            "test_direction": "ONE_SIDED_GREATER",
            "alpha": 0.05,
            "minimum_scientifically_meaningful_effect": 0.05,
            "power_target": 0.80,
            "power_analysis_artifact_id": "POWER1",
            "success_threshold_numeric": 0.0,
            "confirmatory_generation_budget_id": "BUDGET1",
        },
        "comparison_design": {
            "primary_comparison_semantics": "NESTED_ADD_DISEASE_SPECIFIC_EVIDENCE_ONLY",
            "capacity_parity_required": True,
            "learner_family_id": "LEARNER-V1",
            "nuisance_feature_block_id": "NUISANCE-BLOCK-V1",
            "nuisance_feature_block_digest": "sha256:" + "a" * 64,
            "biological_feature_block_id": "BIO-BLOCK-V1",
            "biological_feature_block_digest": "sha256:" + "b" * 64,
            "preprocessing_artifact_id": "PREP-V1",
            "hyperparameter_search_space_digest": "sha256:" + "c" * 64,
            "tuning_budget_id": "TUNE-V1",
            "early_stopping_policy_id": "STOP-V1",
            "random_seed_policy_id": "SEEDPOL-V1",
        },
        "outcome_commitment": {
            "future_outcome_source_release_ids": ["REL1"],
            "future_outcome_snapshot_ids": ["SNAP1"],
            "future_outcome_snapshot_digest": "sha256:22222222",
            "outcome_ledger_digest": "sha256:33333333",
            "adjudication_batch_digest": "sha256:44444444",
            "evaluation_identity_bridge_digest": "sha256:55555555",
            "scientific_event_family_ledger_digest": "sha256:66666666",
            "provider_coupling_assessment_digest": "sha256:77777777",
            "outcome_event_discovery_frozen_at": "2026-01-02T00:00:00Z",
        },
        "coverage_gates": {
            "max_temporal_unknown_fraction": 0.10,
            "min_identity_resolution_fraction": 0.90,
            "min_outcome_coverage_fraction": 0.90,
            "max_novelty_ambiguity_fraction": 0.20,
            "max_assignment_ambiguity_fraction": 0.20,
            "min_lineage_completeness_fraction": 0.90,
            "min_historical_genetic_coverage_grade": "MODERATE",
            "max_variant_harmonization_ambiguity_fraction": 0.10,
        },
        "planned_analyses": {
            "subgroup_analyses": [],
            "sensitivity_analyses": [],
            "source_ablations": [],
            "negative_controls": ["attention-stratified permutation"],
        },
        "governance": {
            "benchmark_design_provenance_id": "BDP1",
            "study_tier": "CONFIRMATORY",
            "ranking_team": ["ranker"],
            "outcome_adjudication_role": "adjudicator",
            "lockbox_custodian_role": "custodian",
            "independent_adjudicator_ids": ["second-adjudicator"],
            "permitted_lockbox_accesses": 1,
            "sealed_disease_blinding_policy": "sealed",
            "sealed_outcome_adjudicator_blinding_required": True,
            "validation_generation_status": "ACTIVE",
            "validation_access_count": 0,
            "validation_max_disclosure_level": "AGGREGATE_ONLY",
            "deviation_policy": "no post-freeze changes",
            "external_seal_attestation_id": "SEAL1",
        },
        "stop_conditions": ["power below frozen threshold"],
    }


def valid_twin() -> dict:
    return {
        "twin_id": "TW-X",
        "schema_version": "scientific-twin-v1",
        "terminology_scope": "FORGE_BIO_RESEARCH_SCIENTIFIC_TWIN",
        "twin_family": "DISEASE_TWIN",
        "subject_entity_ids": ["D1"],
        "maturity_level": "T4_VALIDATED_INTERVENTION_SIMULATION_TWIN",
        "scientific_operating_mode": "STRICT_HISTORICAL",
        "historical_data_policy": "ARCHIVED_ONLY",
        "cutoff": "2010-01-01",
        "profile_snapshot_ids": ["p"],
        "evidence_snapshot_ids": ["e"],
        "state_definition_id": "s",
        "state_model_artifact_id": "m",
        "parameter_artifact_ids": ["x"],
        "update_policy_artifact_id": "u",
        "prediction_spec_id": "ps",
        "map_id": "map",
        "mar_ids": ["mar"],
        "validation_generation_id": "vg",
        "benchmark_design_provenance_id": "bdp",
        "perturbation_artifact_ids": ["pt"],
        "sensitivity_artifact_ids": ["sa"],
        "causal_assumption_set_id": "ca",
        "intervention_semantics_id": "is",
        "identifiability_status": "ASSUMPTION_DEPENDENT",
        "credibility_assessment_id": "cred",
        "model_execution_kind": "STATIC_GRAPH",
        "numerical_verification_artifact_id": None,
        "validation_verdict": "PASS",
        "credibility_conclusion": "ADEQUATE_FOR_COU",
        "verification_artifact_ids": ["ver"],
        "validation_artifact_ids": ["val"],
        "uncertainty_bundle_ref": "uq",
        "applicability_domain_ref": "ad",
        "knowledge_watermark": {"kind": "DATED", "date": "2009-01-01"},
        "digest": "sha256:abcdef12",
    }


class HostileReviewRegressionTests(unittest.TestCase):
    def test_valid_confirmatory_map_passes_schema_and_semantics(self) -> None:
        x = valid_map()
        validator("map.v1.schema.json").validate(x)
        self.assertEqual([], validate_semantics("map", x))

    def test_frozen_map_requires_digest_and_time(self) -> None:
        x = valid_map()
        x["digest"] = None
        x["frozen_at"] = None
        assert_schema_invalid(self, "map.v1.schema.json", x)

    def test_confirmatory_roles_must_be_separate(self) -> None:
        x = valid_map()
        x["governance"]["outcome_adjudication_role"] = "ranker"
        x["governance"]["lockbox_custodian_role"] = "ranker"
        self.assertTrue(validate_semantics("map", x))

    def test_strict_map_rejects_unknown_watermark(self) -> None:
        x = valid_map()
        x["model"]["knowledge_watermark"] = {"kind": "UNKNOWN", "date": None}
        self.assertTrue(validate_semantics("map", x))

    def test_strict_map_rejects_post_cutoff_watermark(self) -> None:
        x = valid_map()
        x["model"]["knowledge_watermark"] = {"kind": "DATED", "date": "2026-09-26"}
        self.assertTrue(validate_semantics("map", x))

    def test_confirmatory_vacuous_coverage_gate_is_rejected(self) -> None:
        x = valid_map()
        x["coverage_gates"]["max_temporal_unknown_fraction"] = 1.0
        assert_schema_invalid(self, "map.v1.schema.json", x)

    def test_free_text_success_threshold_no_longer_exists(self) -> None:
        x = valid_map()
        x["statistics"]["success_threshold"] = "looks better"
        assert_schema_invalid(self, "map.v1.schema.json", x)

    def test_valid_t4_passes_schema(self) -> None:
        validator("scientific-twin.v1.schema.json").validate(valid_twin())

    def test_twin_rejects_post_cutoff_watermark_semantically(self) -> None:
        x = valid_twin()
        x["knowledge_watermark"] = {"kind": "DATED", "date": "2026-09-26"}
        self.assertTrue(validate_semantics("scientific_twin", x))

    def test_twin_rejects_unknown_watermark_semantically(self) -> None:
        x = valid_twin()
        x["knowledge_watermark"] = {"kind": "UNKNOWN", "date": None}
        self.assertTrue(validate_semantics("scientific_twin", x))

    def test_twin_rejects_free_text_cutoff(self) -> None:
        x = valid_twin()
        x["cutoff"] = "sometime before the pandemic"
        assert_schema_invalid(self, "scientific-twin.v1.schema.json", x)

    def test_t4_failed_validation_is_rejected(self) -> None:
        x = valid_twin()
        x["validation_verdict"] = "FAIL"
        assert_schema_invalid(self, "scientific-twin.v1.schema.json", x)

    def test_negative_natural_odds_ratio_is_rejected(self) -> None:
        x = {
            "effect_id": "e", "schema_version": "effect-estimate-v1",
            "estimand_id": "x", "effect_measure_kind": "ODDS_RATIO",
            "effect_context": "GENERAL", "estimate": -2.0,
            "scale": "NATURAL", "transform": "NONE",
            "reference_group_ref": "a", "comparison_group_ref": "b",
            "provenance_ref": "p", "digest": "d",
        }
        assert_schema_invalid(self, "effect-estimate.v1.schema.json", x)

    def test_inverted_confidence_interval_is_rejected_semantically(self) -> None:
        x = {
            "effect_id": "e", "schema_version": "effect-estimate-v1",
            "estimand_id": "x", "effect_measure_kind": "ODDS_RATIO",
            "effect_context": "GENERAL", "estimate": 2.0,
            "scale": "NATURAL", "transform": "NONE",
            "reference_group_ref": "a", "comparison_group_ref": "b",
            "confidence_interval_low": 3.0, "confidence_interval_high": 1.0,
            "provenance_ref": "p", "digest": "d",
        }
        validator("effect-estimate.v1.schema.json").validate(x)
        self.assertTrue(validate_semantics("effect_estimate", x))

    def test_genetic_effect_requires_variant_and_alleles(self) -> None:
        x = {
            "effect_id": "e", "schema_version": "effect-estimate-v1",
            "estimand_id": "x", "effect_measure_kind": "ODDS_RATIO",
            "effect_context": "GENETIC_ASSOCIATION", "estimate": 1.2,
            "scale": "NATURAL", "transform": "NONE",
            "reference_group_ref": "a", "comparison_group_ref": "b",
            "provenance_ref": "p", "digest": "d",
        }
        assert_schema_invalid(self, "effect-estimate.v1.schema.json", x)

    def test_detection_limited_zero_without_limit_is_rejected(self) -> None:
        x = {
            "observation_id": "o", "schema_version": "quantitative-observation-v1",
            "quantity_definition_id": "q", "value_state": "BELOW_DETECTION",
            "value": 0.0, "unit_required": False, "value_domain": "NONNEGATIVE",
            "measurement_scale": "RATIO", "transform": "NONE",
            "measurement_process_id": "mp", "provenance_ref": "p",
            "knowledge_watermark": "DATED(2008-01-01)", "digest": "d",
        }
        assert_schema_invalid(self, "quantitative-observation.v1.schema.json", x)

    def test_z_score_requires_normalization_artifact(self) -> None:
        x = {
            "observation_id": "o", "schema_version": "quantitative-observation-v1",
            "quantity_definition_id": "q", "value_state": "OBSERVED",
            "value": 5.1, "unit_required": False, "value_domain": "ANY_REAL",
            "measurement_scale": "STANDARDIZED", "transform": "Z_SCORE",
            "measurement_process_id": "mp", "provenance_ref": "p",
            "knowledge_watermark": "DATED(2008-01-01)", "digest": "d",
        }
        assert_schema_invalid(self, "quantitative-observation.v1.schema.json", x)

    def test_qualified_extractor_below_frozen_thresholds_is_rejected_semantically(self) -> None:
        x = {
            "quality_card_id": "q", "schema_version": "extraction-quality-card-v1",
            "extractor_id": "llm", "extractor_version": "1",
            "task_definition": "extract gene-disease assertions", "domain_scope": "all",
            "gold_set_id": "g", "sample_size": 5,
            "precision": 0.4, "recall": 0.1,
            "precision_ci_low": 0.2, "recall_ci_low": 0.05,
            "abstention_rate": 0.0,
            "negation_evaluation_status": "NOT_APPLICABLE",
            "null_result_evaluation_status": "NOT_APPLICABLE",
            "known_failure_modes": [],
            "qualification_threshold_artifact_id": "QT1",
            "meets_qualification_thresholds": True,
            "minimum_sample_size_required": 100,
            "minimum_precision_required": 0.9,
            "minimum_recall_required": 0.8,
            "qualification_status": "QUALIFIED", "digest": "d",
        }
        validator("extraction-quality-card.v1.schema.json").validate(x)
        self.assertTrue(validate_semantics("extraction_quality_card", x))

    def test_rtol_one_cannot_be_numerically_adequate(self) -> None:
        x = {
            "verification_id": "n", "schema_version": "numerical-verification-v1",
            "model_artifact_id": "m", "solver_or_engine": "scipy",
            "solver_version": "1", "numerical_method": "RK45",
            "numerical_problem_type": "CONTINUOUS_NUMERICAL",
            "tolerances": {"relative_tolerance": 1.0, "tolerance_justification": "none"},
            "convergence_study_status": "PASS",
            "stochastic_replication_status": "NOT_APPLICABLE",
            "numerical_error_estimate": 0.1,
            "invariant_or_residual_checks": ["residual"],
            "reproducibility_tolerance": "n/a",
            "verdict": "ADEQUATE", "digest": "d",
        }
        assert_schema_invalid(self, "numerical-verification.v1.schema.json", x)

    def test_high_risk_credibility_needs_external_validation(self) -> None:
        x = {
            "assessment_id": "c", "schema_version": "model-credibility-v1",
            "model_artifact_id": "m", "context_of_use_id": "cou",
            "model_execution_kind": "STATIC",
            "external_validation_status": "INTERNAL_ONLY",
            "research_decision": "prioritise targets",
            "model_influence": "DOMINANT",
            "consequence_if_wrong": "MISLEADING_SCIENTIFIC_CLAIM",
            "credibility_goal": "high",
            "verification_adequacy": "ADEQUATE",
            "numerical_verification_adequacy": "NOT_APPLICABLE",
            "validation_adequacy": "ADEQUATE",
            "uncertainty_adequacy": "ADEQUATE",
            "applicability_adequacy": "ADEQUATE",
            "prediction_risk_of_bias": "LOW",
            "known_model_discrepancy": ["simplification"],
            "model_discrepancy_assessment_id": "MD1",
            "sensitivity_analysis_artifact_id": "SA1",
            "transportability_assessment_id": "TA1",
            "limitations": ["limited source range"],
            "residual_risks": ["residual bias"],
            "conclusion": "ADEQUATE_FOR_COU",
            "provenance_ref": "p", "digest": "d",
        }
        validator("model-credibility.v1.schema.json").validate(x)
        self.assertTrue(validate_semantics("model_credibility", x))

    def test_active_confirmatory_cannot_reveal_labels_to_ranker_and_change_model(self) -> None:
        x = {
            "ledger_id": "l", "schema_version": "benchmark-exposure-ledger-v1",
            "benchmark_generation_id": "g", "lifecycle_status": "ACTIVE_CONFIRMATORY",
            "exposure_events": [{
                "exposure_time": "2026-01-01T00:00:00Z",
                "exposure_kind": "LABEL_REVEAL",
                "disclosure_level": "FULL_LABEL",
                "audience_role": "RANKING_TEAM",
                "downstream_change_ref": "feature-set-v7",
            }],
            "attempt_ids": [], "digest": "d",
        }
        assert_schema_invalid(self, "benchmark-exposure-ledger.v1.schema.json", x)

    def test_self_signed_promise_is_not_external_seal(self) -> None:
        x = {
            "attestation_id": "s", "schema_version": "external-seal-attestation-v1",
            "artifact_digest": "sha256:abcdef12", "artifact_type": "MAP",
            "sealed_at": "later", "external_registry_or_custodian_ref": "me",
            "authority_type": "INDEPENDENT_CUSTODIAN",
            "attestation_method": "I promise",
            "signer_or_service_identity": "project owner",
            "independence_from_study_team": True,
            "verification_status": "VERIFIED",
            "verification_evidence_ref": "none",
            "provenance_ref": "p", "digest": "d",
        }
        assert_schema_invalid(self, "external-seal-attestation.v1.schema.json", x)

    def test_confirmatory_attempt_requires_external_seal_and_disclosure_schedule(self) -> None:
        x = {
            "attempt_id": "a", "schema_version": "research-program-attempt-v1",
            "benchmark_family": "B-TGT", "benchmark_generation": "g",
            "attempt_tier": "CONFIRMATORY",
            "registered_at": "2026-01-01T00:00:00Z",
            "map_digest": "sha256:abcdef12",
            "endpoint": "E1", "horizon": "5y",
            "primary_metric": "EVENT_RANK_PERCENTILE",
            "model_family": "gbm", "result_status": "NULL",
            "visibility": "INTERNAL", "disclosure_status": "SCHEDULED",
            "disclosure_due_at": "2027-01-01T00:00:00Z",
            "relationship_to_prior_attempts": "first", "digest": "d",
        }
        assert_schema_invalid(self, "research-program-attempt.v1.schema.json", x)

    def test_alpha_allocations_cannot_exceed_program_budget(self) -> None:
        x = {
            "budget_id": "B1", "schema_version": "confirmatory-program-budget-v1",
            "benchmark_family": "B-TGT", "familywise_alpha": 0.05,
            "allocation_method": "FIXED_SPLIT",
            "max_confirmatory_generations": 2,
            "generation_allocations": [
                {"generation_id": "G1", "allocated_alpha": 0.04, "status": "PLANNED"},
                {"generation_id": "G2", "allocated_alpha": 0.04, "status": "PLANNED"},
            ],
            "development_results_can_support_confirmatory_claim": False,
            "post_failure_policy": "stop or prospectively validate",
            "digest": "sha256:abcdef12",
        }
        validator("confirmatory-program-budget.v1.schema.json").validate(x)
        self.assertTrue(validate_semantics("confirmatory_program_budget", x))


if __name__ == "__main__":
    unittest.main()
