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


class Big0FOperationalContractTests(unittest.TestCase):
    def test_structure_frozen_estimand_does_not_fake_exact_horizon(self) -> None:
        x = {
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
        validate("estimand.v1.schema.json", x)

    def test_confirmatory_estimand_requires_exact_instance(self) -> None:
        x = {
            "estimand_id": "EST-B-TGT-E1-v1",
            "schema_version": "b-tgt-e1-estimand-v1",
            "status": "CONFIRMATORY_INSTANCE_FROZEN",
            "benchmark_id": "B-TGT-E1-v0",
            "primary_population": "COMMON_COMPLEX_GERMLINE_DISEASE_TRAIT_GENETICS",
            "conditioning_rule": "QUALIFYING_FUTURE_EVENT_OBSERVED_WITHIN_H",
            "disease_weighting": "EQUAL_WEIGHT_ACROSS_EVENT_BEARING_DISEASES",
            "zero_event_policy": "RETAIN_IN_FRAME_NO_FABRICATED_RANK_SCORE_REPORT_ALL_FRAME_UTILITY",
            "primary_contrast": "ASCERTAINMENT_OPPORTUNITY_PLUS_DISEASE_EVIDENCE_MINUS_ASCERTAINMENT_OPPORTUNITY_ONLY",
            "horizon_selection_policy_ref": "P1",
            "subtype_selection_policy_ref": "P2",
            "primary_metric_selection_policy_ref": "P3",
            "all_frame_utility_metric_id": "OBSERVED_EVENT_YIELD_AT_TOTAL_REVIEW_BUDGET",
            "exact_horizon": None,
            "primary_endpoint_subtype": None,
            "primary_metric_id": None,
            "frozen_at": "2026-09-26T00:00:00Z",
            "digest": "sha256:" + "a" * 64,
        }
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


if __name__ == "__main__":
    unittest.main()
