from __future__ import annotations

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker, ValidationError

ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = ROOT / "schemas"


def validate(name: str, instance: dict) -> None:
    schema = json.loads((SCHEMAS / name).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(instance)


def structure_estimand() -> dict:
    return {
        "estimand_id": "EST-B-TGT-E1-v1",
        "schema_version": "b-tgt-e1-estimand-v1",
        "status": "STRUCTURE_FROZEN",
        "benchmark_id": "B-TGT-E1-v0",
        "primary_population": "COMMON_COMPLEX_GERMLINE_DISEASE_TRAIT_GENETICS",
        "conditioning_rule": "QUALIFYING_FUTURE_EVENT_OBSERVED_WITHIN_H",
        "disease_weighting": "EQUAL_WEIGHT_ACROSS_EVENT_BEARING_DISEASES",
        "zero_event_policy": "RETAIN_IN_FRAME_NO_FABRICATED_RANK_SCORE_REPORT_ALL_FRAME_UTILITY",
        "primary_contrast": "ASCERTAINMENT_OPPORTUNITY_PLUS_DISEASE_EVIDENCE_MINUS_ASCERTAINMENT_OPPORTUNITY_ONLY",
        "horizon_selection_policy_ref": "BIG_0F_PROTOCOL#1",
        "subtype_selection_policy_ref": "BENCHMARK_V0_SPEC#Primary-subtype",
        "primary_metric_selection_policy_ref": "BIG_0F_PROTOCOL#11",
        "all_frame_utility_metric_id": "OBSERVED_EVENT_YIELD_AT_TOTAL_REVIEW_BUDGET",
        "exact_horizon": None,
        "primary_endpoint_subtype": None,
        "primary_metric_id": None,
        "frozen_at": "2026-09-26T00:00:00Z",
        "digest": "sha256:" + "a" * 64,
    }


def pilot_result() -> dict:
    return {
        "pilot_id": "PILOT-1",
        "schema_version": "big0f-pilot-result-v1",
        "protocol_digest": "sha256:" + "1" * 64,
        "seal_attestation_ids": ["SEAL-1"],
        "cutoff": "2008-12-31",
        "horizon": "5y",
        "disease_count": 12,
        "candidate_event_count": 100,
        "event_bearing_disease_count": 10,
        "untouched_confirmatory_disease_count": 20,
        "high_specificity_positive_count": 30,
        "assignment_metrics": {
            "primary_eligible_fraction": 0.70,
            "author_named_fraction": 0.10,
            "nearest_gene_fraction": 0.10,
            "attention_assignment_association": 0.10,
        },
        "ambiguity_metrics": {
            "novelty_ambiguity_fraction": 0.10,
            "variant_harmonization_ambiguity_fraction": 0.05,
            "phenotype_ambiguity_fraction": 0.10,
            "sample_overlap_ambiguity_fraction": 0.10,
            "any_primary_endpoint_ambiguity_fraction": 0.15,
        },
        "provider_metrics": {
            "required_field_availability_fraction": 0.95,
            "historical_search_coverage_distribution": {"HIGH": 0.6, "MODERATE": 0.4},
            "provider_coupling_risk": "LOW",
        },
        "independence_metrics": {
            "event_family_deduplication_fraction": 0.10,
            "locus_to_many_gene_credit_impact": 0.05,
            "pre_t_cohort_reuse_fraction": 0.20,
        },
        "adjudication_metrics": {
            "duplicate_review_fraction": 0.30,
            "duplicate_review_count": 30,
            "adjudicated_event_case_count": 100,
            "primary_assignment_agreement": 0.80,
            "phenotype_agreement": 0.80,
        },
        "applicability_metrics": {
            "ancestry_metadata_coverage_fraction": 0.90,
            "ancestry_population_metadata_adequacy": "ADEQUATE",
        },
        "curation_metrics": {
            "retrospective_curation_burden_assessment": "ACCEPTABLE",
            "median_minutes_per_event_case": 20.0,
            "symmetric_non_event_audit_complete": True,
            "non_event_case_count": 100,
            "median_minutes_per_non_event_case": 12.0,
        },
        "threshold_sensitivity_stable": True,
        "power_metrics": {
            "alpha": 0.05,
            "target_power": 0.80,
            "estimated_power": 0.85,
            "minimum_scientifically_meaningful_effect": 0.05,
        },
        "nuisance_headroom_metrics": {
            "median_positive_rank_fraction": 0.10,
            "top_1pct_fraction": 0.10,
            "top_5pct_fraction": 0.30,
        },
        "decision": "GO",
        "decision_reasons": ["all frozen GO gates passed"],
        "digest": "sha256:" + "2" * 64,
    }


class Big0FOperationalContractTests(unittest.TestCase):
    def test_structure_frozen_estimand_does_not_fake_exact_horizon(self) -> None:
        validate("estimand.v1.schema.json", structure_estimand())

    def test_structure_frozen_estimand_rejects_exact_choices(self) -> None:
        x = structure_estimand()
        x["exact_horizon"] = "5y"
        x["primary_endpoint_subtype"] = "E1-NOVEL-STRICT"
        x["primary_metric_id"] = "EVENT_RANK_PERCENTILE_V1"
        with self.assertRaises(ValidationError):
            validate("estimand.v1.schema.json", x)

    def test_confirmatory_estimand_requires_exact_instance(self) -> None:
        x = structure_estimand()
        x["status"] = "CONFIRMATORY_INSTANCE_FROZEN"
        with self.assertRaises(ValidationError):
            validate("estimand.v1.schema.json", x)

    def test_endpoint_quality_frozen_requires_timestamp(self) -> None:
        x = {
            "rule_id": "EQ1",
            "schema_version": "endpoint-quality-rule-v1",
            "status": "FROZEN",
            "endpoint_subtype": "E1-NOVEL-STRICT",
            "provider_audit_ref": "AUDIT1",
            "criteria": [{
                "criterion_id": "C1",
                "scientific_dimension": "PHENOTYPE_MATCH",
                "field_or_artifact": "OutcomePhenotypeMatchAssessment",
                "operator": "IN",
                "value": ["EXACT"],
                "unit": None,
                "required": True,
                "justification": "primary endpoint specificity",
            }],
            "independence_requirement": "REQUIRED",
            "phenotype_policy_ref": "ADR-008",
            "gene_assignment_policy_ref": "ADR-020",
            "genomic_harmonization_policy_ref": "ADR-011",
            "frozen_at": None,
            "digest": "sha256:" + "b" * 64,
        }
        with self.assertRaises(ValidationError):
            validate("endpoint-quality-rule.v1.schema.json", x)

    def test_endpoint_numeric_comparison_requires_operand(self) -> None:
        x = {
            "rule_id": "EQ2",
            "schema_version": "endpoint-quality-rule-v1",
            "status": "FROZEN",
            "endpoint_subtype": "E1-NOVEL-STRICT",
            "provider_audit_ref": "AUDIT1",
            "criteria": [{
                "criterion_id": "C1",
                "scientific_dimension": "STATISTICAL_STRENGTH",
                "field_or_artifact": "p_value",
                "operator": "LE",
                "unit": None,
                "required": True,
                "justification": "frozen statistical criterion",
            }],
            "independence_requirement": "REQUIRED",
            "phenotype_policy_ref": "ADR-008",
            "gene_assignment_policy_ref": "ADR-020",
            "genomic_harmonization_policy_ref": "ADR-011",
            "frozen_at": "2026-09-26T00:00:00Z",
            "digest": "sha256:" + "b" * 64,
        }
        with self.assertRaises(ValidationError):
            validate("endpoint-quality-rule.v1.schema.json", x)

    def test_valid_pilot_result_requires_all_go_prerequisites(self) -> None:
        validate("big0f-pilot-result.v1.schema.json", pilot_result())

    def test_pilot_result_cannot_omit_ancestry_applicability(self) -> None:
        x = pilot_result()
        del x["applicability_metrics"]
        with self.assertRaises(ValidationError):
            validate("big0f-pilot-result.v1.schema.json", x)

    def test_pilot_result_cannot_omit_symmetric_non_event_curation_metrics(self) -> None:
        x = pilot_result()
        del x["curation_metrics"]
        with self.assertRaises(ValidationError):
            validate("big0f-pilot-result.v1.schema.json", x)


if __name__ == "__main__":
    unittest.main()
