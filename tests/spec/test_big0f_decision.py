from __future__ import annotations

import copy
import unittest

from scripts.evaluate_big0f import EvaluationContext, evaluate, load_threshold_manifest
from tests.spec.test_big0f_operational_contracts import pilot_result


CTX = EvaluationContext(
    seal_verified=True,
    threshold_manifest_verified=True,
    power_analysis_verified=True,
    adjudication_policy_verified=True,
    nuisance_manifest_verified=True,
    decision_engine_sealed=True,
    pilot_schema_sealed=True,
    sampling_code_sealed=True,
)


def decide(x):
    return evaluate(x, load_threshold_manifest(), context=CTX).decision


class Big0FDecisionTests(unittest.TestCase):
    def test_go(self):
        self.assertEqual("GO", decide(pilot_result()))

    def test_no_go_on_low_availability(self):
        x = pilot_result()
        x["provider_metrics"]["required_field_availability_fraction"] = 0.60
        self.assertEqual("NO_GO", decide(x))

    def test_no_go_on_low_power(self):
        x = pilot_result()
        x["power_metrics"]["estimated_power"] = 0.60
        self.assertEqual("NO_GO", decide(x))

    def test_no_go_uses_union_ambiguity(self):
        x = pilot_result()
        x["ambiguity_metrics"]["any_primary_endpoint_ambiguity_fraction"] = 0.60
        self.assertEqual("NO_GO", decide(x))

    def test_missing_verified_context_cannot_go(self):
        self.assertNotEqual("GO", evaluate(pilot_result(), load_threshold_manifest()).decision)

    def test_inconclusive_if_duplicate_review_below_minimum(self):
        x = pilot_result()
        x["adjudication_metrics"]["duplicate_review_count"] = 20
        x["adjudication_metrics"]["duplicate_review_fraction"] = 0.20
        self.assertEqual("INCONCLUSIVE", decide(x))

    def test_redesign_after_second_inconclusive(self):
        x = pilot_result()
        x["prior_inconclusive_count"] = 1
        x["adjudication_metrics"]["duplicate_review_count"] = 20
        x["adjudication_metrics"]["duplicate_review_fraction"] = 0.20
        self.assertEqual("REDESIGN", decide(x))

    def test_redesign_on_attention_ci_touching_boundary(self):
        x = pilot_result()
        x["assignment_metrics"]["attention_assignment_ci_high"] = 0.30
        self.assertEqual("REDESIGN", decide(x))

    def test_redesign_if_hypothesis_free_fraction_low(self):
        x = pilot_result()
        x["assignment_metrics"]["hypothesis_free_primary_positive_fraction"] = 0.30
        self.assertEqual("REDESIGN", decide(x))

    def test_redesign_on_nuisance_top1_saturation(self):
        x = pilot_result()
        x["nuisance_headroom_metrics"]["top_1pct_fraction"] = 0.30
        self.assertEqual("REDESIGN", decide(x))

    def test_impossible_top1_gt_top5_raises(self):
        x = pilot_result()
        x["nuisance_headroom_metrics"]["top_1pct_fraction"] = 0.90
        x["nuisance_headroom_metrics"]["top_5pct_fraction"] = 0.10
        with self.assertRaises(ValueError):
            decide(x)

    def test_event_bearing_cannot_exceed_diseases(self):
        x = pilot_result()
        x["event_bearing_disease_count"] = 13
        with self.assertRaises(ValueError):
            decide(x)

    def test_high_spec_cannot_exceed_candidate_events(self):
        x = pilot_result()
        x["high_specificity_positive_count"] = 101
        with self.assertRaises(ValueError):
            decide(x)

    def test_all_candidate_events_must_be_adjudicated(self):
        x = pilot_result()
        x["adjudication_metrics"]["adjudicated_event_case_count"] = 50
        x["adjudication_metrics"]["duplicate_review_count"] = 30
        x["adjudication_metrics"]["duplicate_review_fraction"] = 0.60
        self.assertEqual("INCONCLUSIVE", decide(x))

    def test_moderate_provider_coupling_redesigns(self):
        x = pilot_result()
        x["provider_metrics"]["provider_coupling_risk"] = "MODERATE"
        self.assertEqual("REDESIGN", decide(x))

    def test_curation_burden_is_not_self_declared_only(self):
        x = pilot_result()
        x["curation_metrics"]["median_minutes_per_event_case"] = 900.0
        self.assertEqual("REDESIGN", decide(x))

    def test_asymmetric_non_event_burden_redesigns(self):
        x = pilot_result()
        x["curation_metrics"]["median_minutes_per_non_event_case"] = 0.1
        self.assertEqual("REDESIGN", decide(x))

    def test_ancestry_coverage_low_redesigns(self):
        x = pilot_result()
        x["applicability_metrics"]["ancestry_metadata_coverage_fraction"] = 0.20
        self.assertEqual("REDESIGN", decide(x))

    def test_power_pool_must_meet_computed_requirement(self):
        x = pilot_result()
        x["untouched_confirmatory_disease_count"] = 20
        x["power_metrics"]["required_confirmatory_disease_count"] = 25
        self.assertEqual("NO_GO", decide(x))

    def test_nan_cannot_reach_decision(self):
        for path in [
            ("adjudication_metrics", "primary_assignment_agreement"),
            ("ambiguity_metrics", "any_primary_endpoint_ambiguity_fraction"),
            ("power_metrics", "estimated_power"),
            ("provider_metrics", "required_field_availability_fraction"),
            ("nuisance_headroom_metrics", "median_positive_rank_fraction"),
        ]:
            x = pilot_result()
            x[path[0]][path[1]] = float("nan")
            with self.assertRaises(ValueError, msg=str(path)):
                decide(x)


if __name__ == "__main__":
    unittest.main()
