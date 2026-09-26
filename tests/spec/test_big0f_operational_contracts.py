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
        "horizon_selection_policy_ref": "BIG0F-FIRST-PASSING-T_H-V1",
        "subtype_selection_policy_ref": "E1-NOVEL-STRICT-OR-REDESIGN-V1",
        "primary_metric_selection_policy_ref": "EVENT-RANK-PERCENTILE-V1",
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
        "seal_bundle_digest": "sha256:" + "2" * 64,
        "threshold_manifest_digest": "sha256:" + "3" * 64,
        "adjudication_policy_digest": "sha256:" + "4" * 64,
        "nuisance_manifest_digest": "sha256:" + "5" * 64,
        "seal_attestation_ids": ["OTS-1", "OSF-1"],
        "first_adjudication_at": "2026-09-26T12:00:00Z",
        "cutoff": "2008-12-31",
        "horizon": "5y",
        "disease_count": 12,
        "candidate_event_count": 100,
        "event_bearing_disease_count": 10,
        "untouched_confirmatory_disease_count": 60,
        "high_specificity_positive_count": 40,
        "source_family_count": 4,
        "source_family_ids": ["PUB", "GWAS", "IDENTITY", "GENE_MODEL"],
        "prior_inconclusive_count": 0,
        "assignment_metrics": {
            "primary_eligible_fraction": 0.75,
            "author_named_fraction": 0.08,
            "nearest_gene_fraction": 0.08,
            "attention_assignment_association": 0.08,
            "attention_assignment_ci_low": 0.02,
            "attention_assignment_ci_high": 0.14,
            "hypothesis_free_primary_positive_fraction": 0.75,
            "label_feature_method_coupling_fraction": 0.10,
        },
        "ambiguity_metrics": {
            "novelty_ambiguity_fraction": 0.05,
            "variant_harmonization_ambiguity_fraction": 0.05,
            "phenotype_ambiguity_fraction": 0.05,
            "sample_overlap_ambiguity_fraction": 0.05,
            "any_primary_endpoint_ambiguity_fraction": 0.10,
        },
        "provider_metrics": {
            "required_field_availability_fraction": 0.97,
            "historical_search_coverage_distribution": {
                "HIGH": 0.70, "MODERATE": 0.25, "LOW": 0.05, "UNKNOWN": 0.0
            },
            "provider_coupling_risk": "LOW",
        },
        "independence_metrics": {
            "event_family_deduplication_fraction": 0.05,
            "locus_to_many_gene_credit_impact": 0.05,
            "pre_t_cohort_reuse_fraction": 0.15,
        },
        "adjudication_metrics": {
            "duplicate_review_fraction": 0.30,
            "duplicate_review_count": 30,
            "adjudicated_event_case_count": 100,
            "primary_assignment_agreement": 0.82,
            "phenotype_agreement": 0.82,
            "primary_assignment_agreement_statistic": "GWET_AC1",
            "phenotype_agreement_statistic": "GWET_AC1",
            "second_adjudicator_id": "ADJ-2",
            "second_adjudicator_independence_attestation_id": "ADJ-INDEP-1",
            "second_adjudicator_blinded_to_rankings": True,
            "second_adjudicator_blinded_to_first_review": True,
            "rule_revision_count": 0,
            "heldout_retest_completed": False,
        },
        "applicability_metrics": {
            "ancestry_metadata_coverage_fraction": 0.95,
            "ancestry_population_metadata_adequacy": "ADEQUATE",
        },
        "curation_metrics": {
            "retrospective_curation_burden_assessment": "ACCEPTABLE",
            "median_minutes_per_event_case": 20.0,
            "symmetric_non_event_audit_complete": True,
            "non_event_case_count": 100,
            "median_minutes_per_non_event_case": 15.0,
            "operational_capacity_rule_id": "CURATION-CAPACITY-V1",
        },
        "power_metrics": {
            "alpha": 0.05,
            "target_power": 0.80,
            "estimated_power": 0.85,
            "minimum_scientifically_meaningful_effect": 0.05,
            "power_analysis_artifact_id": "BIG0F-POWER-V1",
            "power_analysis_digest": "sha256:" + "6" * 64,
            "required_confirmatory_disease_count": 25,
            "required_high_specificity_positive_count": 30,
        },
        "nuisance_headroom_metrics": {
            "median_positive_rank_fraction": 0.10,
            "top_1pct_fraction": 0.10,
            "top_5pct_fraction": 0.35,
        },
        "decision": "GO",
        "decision_reasons": ["all frozen GO gates passed"],
        "digest": "sha256:" + "7" * 64,
    }


class Big0FOperationalContractTests(unittest.TestCase):
    def test_structure_frozen_estimand_valid(self) -> None:
        validate("estimand.v1.schema.json", structure_estimand())

    def test_structure_frozen_estimand_rejects_exact_choices(self) -> None:
        x = structure_estimand()
        x["exact_horizon"] = "5y"
        with self.assertRaises(ValidationError):
            validate("estimand.v1.schema.json", x)

    def test_structure_frozen_estimand_rejects_policy_ref_smuggling(self) -> None:
        x = structure_estimand()
        x["horizon_selection_policy_ref"] = "use-5y"
        with self.assertRaises(ValidationError):
            validate("estimand.v1.schema.json", x)

    def test_confirmatory_estimand_requires_v0_subtype_and_metric(self) -> None:
        x = structure_estimand()
        x.update({
            "status": "CONFIRMATORY_INSTANCE_FROZEN",
            "exact_horizon": "5y",
            "primary_endpoint_subtype": "E1-MATURATION",
            "primary_metric_id": "whatever",
        })
        with self.assertRaises(ValidationError):
            validate("estimand.v1.schema.json", x)

    def test_valid_pilot_result_schema(self) -> None:
        validate("big0f-pilot-result.v1.schema.json", pilot_result())

    def test_pilot_result_cannot_omit_ancestry_applicability(self) -> None:
        x = pilot_result()
        del x["applicability_metrics"]
        with self.assertRaises(ValidationError):
            validate("big0f-pilot-result.v1.schema.json", x)

    def test_pilot_result_requires_dual_attestations(self) -> None:
        x = pilot_result()
        x["seal_attestation_ids"] = ["only-one"]
        with self.assertRaises(ValidationError):
            validate("big0f-pilot-result.v1.schema.json", x)

    def test_pilot_result_rejects_out_of_grid_cutoff(self) -> None:
        x = pilot_result()
        x["cutoff"] = "2019-06-30"
        with self.assertRaises(ValidationError):
            validate("big0f-pilot-result.v1.schema.json", x)


if __name__ == "__main__":
    unittest.main()
