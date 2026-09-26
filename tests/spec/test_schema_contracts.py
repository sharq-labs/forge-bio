from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError, FormatChecker

ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = ROOT / "schemas"


def load(name: str) -> dict:
    data = json.loads((SCHEMAS / name).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(data)
    return data


class ScientificTwinSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = load("scientific-twin.v1.schema.json")
        cls.validator = Draft202012Validator(cls.schema, format_checker=FormatChecker())

    def base(self) -> dict:
        return {
            "twin_id": "TW-1",
            "schema_version": "scientific-twin-v1",
            "terminology_scope": "FORGE_BIO_RESEARCH_SCIENTIFIC_TWIN",
            "twin_family": "DISEASE_TWIN",
            "subject_entity_ids": ["D1"],
            "maturity_level": "T0_PROFILE_ONLY",
            "scientific_operating_mode": "CURRENT_DISCOVERY",
            "historical_data_policy": "ARCHIVED_ONLY",
            "profile_snapshot_ids": ["profile-1"],
            "evidence_snapshot_ids": [],
            "parameter_artifact_ids": [],
            "mar_ids": [],
            "perturbation_artifact_ids": [],
            "sensitivity_artifact_ids": [],
            "verification_artifact_ids": [],
            "validation_artifact_ids": [],
            "uncertainty_bundle_ref": "uq-1",
            "applicability_domain_ref": "app-1",
            "knowledge_watermark": {"kind": "DATED", "date": "2026-09-26"},
            "digest": "sha256:test",
        }

    def t3(self) -> dict:
        x = self.base()
        x.update({
            "maturity_level": "T3_VALIDATED_PREDICTIVE_TWIN",
            "evidence_snapshot_ids": ["evidence-1"],
            "state_definition_id": "state-def-1",
            "state_model_artifact_id": "state-model-1",
            "parameter_artifact_ids": ["param-1"],
            "update_policy_artifact_id": "update-1",
            "prediction_spec_id": "prediction-1",
            "map_id": "map-1",
            "mar_ids": ["mar-1"],
            "validation_generation_id": "vg-1",
            "benchmark_design_provenance_id": "bdp-1",
            "credibility_assessment_id": "cred-1",
            "model_execution_kind": "STATIC_GRAPH",
            "validation_verdict": "PASS",
            "credibility_conclusion": "ADEQUATE_FOR_COU",
            "verification_artifact_ids": ["verify-1"],
            "validation_artifact_ids": ["validate-1"],
        })
        return x

    def assert_invalid(self, instance: dict) -> None:
        with self.assertRaises(ValidationError):
            self.validator.validate(instance)

    def test_valid_t0_profile_only(self) -> None:
        self.validator.validate(self.base())

    def test_research_twin_terminology_scope_is_required(self) -> None:
        x = self.base()
        x.pop("terminology_scope")
        self.assert_invalid(x)

    def test_t1_requires_dynamic_state_and_update_policy(self) -> None:
        x = self.base()
        x["maturity_level"] = "T1_DYNAMIC_KNOWLEDGE_TWIN"
        x["evidence_snapshot_ids"] = ["e1"]
        self.assert_invalid(x)

    def test_t2_requires_model_parameters_and_verification(self) -> None:
        x = self.base()
        x.update({
            "maturity_level": "T2_MECHANISTIC_TWIN",
            "state_definition_id": "state-def-1",
            "update_policy_artifact_id": "update-1",
            "evidence_snapshot_ids": ["e1"],
        })
        self.assert_invalid(x)

    def test_t3_requires_validation_governance(self) -> None:
        x = self.t3()
        x["validation_artifact_ids"] = []
        self.assert_invalid(x)

    def test_historical_twin_requires_cutoff(self) -> None:
        x = self.t3()
        x["scientific_operating_mode"] = "STRICT_HISTORICAL"
        self.assert_invalid(x)

    def test_valid_historical_t3(self) -> None:
        x = self.t3()
        x["scientific_operating_mode"] = "STRICT_HISTORICAL"
        x["cutoff"] = "2010-12-31"
        self.validator.validate(x)

    def test_t4_requires_causal_intervention_contract(self) -> None:
        x = self.t3()
        x["maturity_level"] = "T4_VALIDATED_INTERVENTION_SIMULATION_TWIN"
        self.assert_invalid(x)

    def test_valid_t4(self) -> None:
        x = self.t3()
        x.update({
            "maturity_level": "T4_VALIDATED_INTERVENTION_SIMULATION_TWIN",
            "perturbation_artifact_ids": ["perturb-1"],
            "sensitivity_artifact_ids": ["sens-1"],
            "causal_assumption_set_id": "causal-1",
            "intervention_semantics_id": "intervention-1",
            "identifiability_status": "ASSUMPTION_DEPENDENT",
        })
        self.validator.validate(x)

    def test_not_identified_cannot_support_t4(self) -> None:
        x = self.t3()
        x.update({
            "maturity_level": "T4_VALIDATED_INTERVENTION_SIMULATION_TWIN",
            "perturbation_artifact_ids": ["perturb-1"],
            "sensitivity_artifact_ids": ["sens-1"],
            "causal_assumption_set_id": "causal-1",
            "intervention_semantics_id": "intervention-1",
            "identifiability_status": "NOT_IDENTIFIED",
        })
        self.assert_invalid(x)


class ProfileSchemaTests(unittest.TestCase):
    def validate(self, schema_name: str, instance: dict) -> None:
        Draft202012Validator(load(schema_name), format_checker=FormatChecker()).validate(instance)

    def assert_invalid(self, schema_name: str, instance: dict) -> None:
        with self.assertRaises(ValidationError):
            self.validate(schema_name, instance)

    def common(self, version: str, subject: str = "X1") -> dict:
        return {
            "profile_id": "P1",
            "schema_version": version,
            "subject_entity_id": subject,
            "scientific_operating_mode": "CURRENT_DISCOVERY",
            "historical_data_policy": "ARCHIVED_ONLY",
            "uncertainty_bundle_ref": "uq-1",
            "provenance_ref": "prov-1",
            "knowledge_watermark": "DATED(2026-09-26)",
            "digest": "sha256:test",
        }

    def test_minimal_current_profiles_validate(self) -> None:
        disease = self.common("disease-profile-v1", "D1")
        disease["disease_id"] = "D1"
        self.validate("disease-profile.v1.schema.json", disease)

        pathogen = self.common("pathogen-profile-v1", "P1")
        pathogen.update({"pathogen_id": "P1", "pathogen_type": "VIRUS", "taxonomy_ref": "tax-1"})
        self.validate("pathogen-profile.v1.schema.json", pathogen)

        host = self.common("pathogen-host-profile-v1", "PH1")
        host.update({"pathogen_id": "P1", "host_species_id": "H1"})
        self.validate("pathogen-host-profile.v1.schema.json", host)

        therapeutic = self.common("therapeutic-profile-v1", "T1")
        therapeutic.update({"therapeutic_entity_id": "T1", "therapeutic_modality": "SMALL_MOLECULE"})
        self.validate("therapeutic-profile.v1.schema.json", therapeutic)

        virus = {
            "extension_id": "VX1",
            "schema_version": "virus-profile-extension-v1",
            "pathogen_id": "P1",
            "scientific_operating_mode": "CURRENT_DISCOVERY",
            "historical_data_policy": "ARCHIVED_ONLY",
            "provenance_ref": "prov-1",
            "knowledge_watermark": "DATED(2026-09-26)",
            "digest": "sha256:test",
        }
        self.validate("virus-profile-extension.v1.schema.json", virus)

    def test_historical_profile_requires_cutoff(self) -> None:
        disease = self.common("disease-profile-v1", "D1")
        disease.update({"disease_id": "D1", "scientific_operating_mode": "STRICT_HISTORICAL"})
        self.assert_invalid("disease-profile.v1.schema.json", disease)


class QuantitativeAndCredibilitySchemaTests(unittest.TestCase):
    def validate(self, schema_name: str, instance: dict) -> None:
        Draft202012Validator(load(schema_name), format_checker=FormatChecker()).validate(instance)

    def assert_invalid(self, schema_name: str, instance: dict) -> None:
        with self.assertRaises(ValidationError):
            self.validate(schema_name, instance)

    def test_unit_required_observation_needs_unit_and_dimension(self) -> None:
        x = {
            "observation_id": "O1",
            "schema_version": "quantitative-observation-v1",
            "quantity_definition_id": "Q1",
            "value_state": "OBSERVED",
            "value": 1.2,
            "unit_required": True,
            "value_domain": "POSITIVE",
            "measurement_scale": "RATIO",
            "transform": "NONE",
            "measurement_process_id": "MP1",
            "provenance_ref": "prov-1",
            "knowledge_watermark": {"kind": "DATED", "date": "2010-01-01"},
            "digest": "sha256:test",
        }
        self.assert_invalid("quantitative-observation.v1.schema.json", x)

    def test_missing_observation_cannot_carry_numeric_value(self) -> None:
        x = {
            "observation_id": "O2",
            "schema_version": "quantitative-observation-v1",
            "quantity_definition_id": "Q1",
            "value_state": "MISSING",
            "value": 0,
            "unit_required": False,
            "value_domain": "ANY_REAL",
            "measurement_scale": "RATIO",
            "transform": "NONE",
            "measurement_process_id": "MP1",
            "provenance_ref": "prov-1",
            "knowledge_watermark": {"kind": "DATED", "date": "2010-01-01"},
            "digest": "sha256:test",
        }
        self.assert_invalid("quantitative-observation.v1.schema.json", x)

    def test_custom_transform_requires_artifact(self) -> None:
        x = {
            "observation_id": "O3",
            "schema_version": "quantitative-observation-v1",
            "quantity_definition_id": "Q1",
            "value_state": "OBSERVED",
            "value": 2.0,
            "unit_required": False,
            "value_domain": "ANY_REAL",
            "measurement_scale": "STANDARDIZED",
            "transform": "CUSTOM",
            "measurement_process_id": "MP1",
            "provenance_ref": "prov-1",
            "knowledge_watermark": {"kind": "DATED", "date": "2010-01-01"},
            "digest": "sha256:test",
        }
        self.assert_invalid("quantitative-observation.v1.schema.json", x)

    def test_adequate_numerical_verification_cannot_have_failed_convergence(self) -> None:
        x = {
            "verification_id": "NV1",
            "schema_version": "numerical-verification-v1",
            "model_artifact_id": "M1",
            "solver_or_engine": "solver",
            "solver_version": "1",
            "numerical_method": "method",
            "numerical_problem_type": "CONTINUOUS_NUMERICAL",
            "tolerances": {"relative_tolerance": 1e-6, "absolute_tolerance": 1e-9, "tolerance_justification": "development fixture"},
            "convergence_study_status": "FAIL",
            "stochastic_replication_status": "NOT_APPLICABLE",
            "numerical_error_estimate": 0.01,
            "invariant_or_residual_checks": ["residual"],
            "reproducibility_tolerance": "1e-6 relative",
            "verdict": "ADEQUATE",
            "digest": "sha256:test",
        }
        self.assert_invalid("numerical-verification.v1.schema.json", x)

    def test_adequate_credibility_cannot_have_high_prediction_bias(self) -> None:
        x = {
            "assessment_id": "CA1",
            "schema_version": "model-credibility-v1",
            "model_artifact_id": "M1",
            "context_of_use_id": "COU1",
            "model_execution_kind": "STATIC",
            "external_validation_status": "INTERNAL_ONLY",
            "research_decision": "prioritize experiments",
            "model_influence": "MATERIAL",
            "consequence_if_wrong": "MODERATE_RESEARCH_COST",
            "credibility_goal": "support ranking",
            "verification_adequacy": "ADEQUATE",
            "numerical_verification_adequacy": "NOT_APPLICABLE",
            "validation_adequacy": "ADEQUATE",
            "uncertainty_adequacy": "ADEQUATE",
            "applicability_adequacy": "ADEQUATE",
            "prediction_risk_of_bias": "HIGH",
            "limitations": [],
            "residual_risks": [],
            "conclusion": "ADEQUATE_FOR_COU",
            "provenance_ref": "prov-1",
            "digest": "sha256:test",
        }
        self.assert_invalid("model-credibility.v1.schema.json", x)

    def test_valid_effect_estimate(self) -> None:
        x = {
            "effect_id": "E1",
            "schema_version": "effect-estimate-v1",
            "estimand_id": "EST1",
            "effect_measure_kind": "ODDS_RATIO",
            "effect_context": "GENERAL",
            "estimate": 1.4,
            "scale": "NATURAL",
            "transform": "NONE",
            "reference_group_ref": "R",
            "comparison_group_ref": "C",
            "provenance_ref": "prov-1",
            "digest": "sha256:test",
        }
        self.validate("effect-estimate.v1.schema.json", x)


class ExtractionQualitySchemaTests(unittest.TestCase):
    def validate(self, schema_name: str, instance: dict) -> None:
        Draft202012Validator(load(schema_name), format_checker=FormatChecker()).validate(instance)

    def assert_invalid(self, schema_name: str, instance: dict) -> None:
        with self.assertRaises(ValidationError):
            self.validate(schema_name, instance)

    def test_llm_extraction_requires_quality_card(self) -> None:
        x = {
            "extraction_id": "X1",
            "schema_version": "extraction-artifact-v1",
            "source_artifact_id": "SA1",
            "source_record_id": "SR1",
            "source_locator_or_span": "p1:paragraph2",
            "extraction_method": "LLM_EXTRACTED",
            "extractor_id": "ext",
            "extractor_version": "1",
            "knowledge_watermark": "DATED(2020-01-01)",
            "output_schema_version": "claims-v1",
            "extracted_claim_ids": ["C1"],
            "abstention_state": "NOT_ABSTAINED",
            "reviewer_state": "PENDING",
            "provenance_ref": "prov-1",
            "digest": "sha256:test",
        }
        self.assert_invalid("extraction-artifact.v1.schema.json", x)

    def test_valid_llm_extraction_with_quality_card(self) -> None:
        x = {
            "extraction_id": "X2",
            "schema_version": "extraction-artifact-v1",
            "source_artifact_id": "SA1",
            "source_record_id": "SR1",
            "source_locator_or_span": "p1:paragraph2",
            "extraction_method": "LLM_EXTRACTED",
            "extractor_id": "ext",
            "extractor_version": "1",
            "knowledge_watermark": "DATED(2020-01-01)",
            "output_schema_version": "claims-v1",
            "extracted_claim_ids": ["C1"],
            "abstention_state": "NOT_ABSTAINED",
            "reviewer_state": "REVIEWED",
            "quality_card_id": "Q1",
            "provenance_ref": "prov-1",
            "digest": "sha256:test",
        }
        self.validate("extraction-artifact.v1.schema.json", x)

    def test_conditional_quality_requires_condition(self) -> None:
        x = {
            "quality_card_id": "Q1",
            "schema_version": "extraction-quality-card-v1",
            "extractor_id": "ext",
            "extractor_version": "1",
            "task_definition": "claim extraction",
            "domain_scope": "genetics",
            "gold_set_id": "G1",
            "sample_size": 100,
            "precision": 0.95,
            "recall": 0.90,
            "precision_ci_low": 0.90,
            "recall_ci_low": 0.85,
            "abstention_rate": 0.05,
            "negation_evaluation_status": "NOT_APPLICABLE",
            "null_result_evaluation_status": "NOT_APPLICABLE",
            "qualification_threshold_artifact_id": "QT1",
            "meets_qualification_thresholds": True,
            "minimum_sample_size_required": 50,
            "minimum_precision_required": 0.90,
            "minimum_recall_required": 0.80,
            "known_failure_modes": [],
            "qualification_status": "CONDITIONAL",
            "digest": "sha256:test",
        }
        self.assert_invalid("extraction-quality-card.v1.schema.json", x)


class ResearchProgramLifecycleSchemaTests(unittest.TestCase):
    def validate(self, schema_name: str, instance: dict) -> None:
        Draft202012Validator(load(schema_name), format_checker=FormatChecker()).validate(instance)

    def test_valid_source_retraction_event(self) -> None:
        x = {
            "event_id": "SL1",
            "schema_version": "source-lifecycle-event-v1",
            "source_artifact_id": "S1",
            "event_type": "RETRACTED",
            "event_public_time": "2025-01-01",
            "reason": "publisher retraction",
            "provenance_ref": "prov-1",
            "digest": "sha256:test",
        }
        self.validate("source-lifecycle-event.v1.schema.json", x)

    def test_valid_exhausted_benchmark_ledger(self) -> None:
        x = {
            "ledger_id": "BL1",
            "schema_version": "benchmark-exposure-ledger-v1",
            "benchmark_generation_id": "BG1",
            "lifecycle_status": "EXHAUSTED",
            "exposure_events": [{
                "exposure_time": "2026-01-01",
                "exposure_kind": "FULL_LABEL" if False else "LABEL_REVEAL",
                "disclosure_level": "FULL_LABEL",
                "audience_role": "RANKING_TEAM",
                "downstream_change_ref": "change-1",
            }],
            "attempt_ids": ["A1"],
            "digest": "sha256:test",
        }
        self.validate("benchmark-exposure-ledger.v1.schema.json", x)

    def test_valid_external_seal(self) -> None:
        x = {
            "attestation_id": "ES1",
            "schema_version": "external-seal-attestation-v1",
            "artifact_digest": "sha256:abcdef12",
            "artifact_type": "ranking",
            "sealed_at": "2026-01-01T00:00:00Z",
            "external_registry_or_custodian_ref": "custodian-1",
            "authority_type": "INDEPENDENT_CUSTODIAN",
            "attestation_method": "SIGNED_CUSTODIAN_ATTESTATION",
            "signer_or_service_identity": "independent-custodian",
            "independence_from_study_team": True,
            "verification_status": "VERIFIED",
            "verification_evidence_ref": "seal-proof-1",
            "provenance_ref": "prov-1",
            "digest": "sha256:test",
        }
        self.validate("external-seal-attestation.v1.schema.json", x)

    def test_valid_prediction_exposure(self) -> None:
        x = {
            "event_id": "PE1",
            "schema_version": "prediction-exposure-event-v1",
            "prediction_artifact_id": "PRED1",
            "exposure_time": "2026-01-01",
            "exposure_scope": "PUBLIC_RELEASE",
            "audience": "public",
            "target_visibility": "FULL",
            "contamination_risk": "HIGH",
            "provenance_ref": "prov-1",
            "digest": "sha256:test",
        }
        self.validate("prediction-exposure-event.v1.schema.json", x)

    def test_valid_null_research_attempt(self) -> None:
        x = {
            "attempt_id": "RA1",
            "schema_version": "research-program-attempt-v1",
            "benchmark_family": "B-TGT",
            "benchmark_generation": "G1",
            "attempt_tier": "DEVELOPMENT",
            "registered_at": "2026-01-01T00:00:00Z",
            "map_digest": "sha256:abcdef12",
            "endpoint": "E1",
            "horizon": "5y",
            "primary_metric": "recall@k",
            "model_family": "baseline",
            "result_status": "NULL",
            "visibility": "INTERNAL",
            "disclosure_status": "SCHEDULED",
            "disclosure_due_at": "2026-12-31T00:00:00Z",
            "relationship_to_prior_attempts": "first attempt",
            "digest": "sha256:test",
        }
        self.validate("research-program-attempt.v1.schema.json", x)


if __name__ == "__main__":
    unittest.main()
