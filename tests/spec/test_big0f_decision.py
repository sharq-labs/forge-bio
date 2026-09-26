from __future__ import annotations

import unittest

from scripts.evaluate_big0f import evaluate


def base():
    return {
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
        "untouched_confirmatory_disease_count": 20,
        "high_specificity_positive_count": 30,
    }


class Big0FDecisionTests(unittest.TestCase):
    def test_go(self):
        self.assertEqual("GO", evaluate(base()).decision)

    def test_no_go_on_low_availability(self):
        x = base()
        x["provider_metrics"]["required_field_availability_fraction"] = 0.60
        self.assertEqual("NO_GO", evaluate(x).decision)

    def test_no_go_on_low_power(self):
        x = base()
        x["power_metrics"]["estimated_power"] = 0.60
        self.assertEqual("NO_GO", evaluate(x).decision)

    def test_no_go_uses_union_ambiguity_not_max_component(self):
        x = base()
        x["ambiguity_metrics"].update({
            "novelty_ambiguity_fraction": 0.15,
            "variant_harmonization_ambiguity_fraction": 0.15,
            "phenotype_ambiguity_fraction": 0.15,
            "sample_overlap_ambiguity_fraction": 0.15,
            "any_primary_endpoint_ambiguity_fraction": 0.60,
        })
        self.assertEqual("NO_GO", evaluate(x).decision)

    def test_inconclusive_if_union_ambiguity_is_inconsistent(self):
        x = base()
        x["ambiguity_metrics"]["phenotype_ambiguity_fraction"] = 0.30
        x["ambiguity_metrics"]["any_primary_endpoint_ambiguity_fraction"] = 0.10
        self.assertEqual("INCONCLUSIVE", evaluate(x).decision)

    def test_inconclusive_if_duplicate_review_below_protocol_minimum(self):
        x = base()
        x["adjudication_metrics"]["duplicate_review_count"] = 20
        x["adjudication_metrics"]["duplicate_review_fraction"] = 0.20
        self.assertEqual("INCONCLUSIVE", evaluate(x).decision)

    def test_inconclusive_if_duplicate_fraction_disagrees_with_count(self):
        x = base()
        x["adjudication_metrics"]["duplicate_review_fraction"] = 0.90
        self.assertEqual("INCONCLUSIVE", evaluate(x).decision)

    def test_inconclusive_if_threshold_sensitivity_is_unstable(self):
        x = base()
        x["threshold_sensitivity_stable"] = False
        self.assertEqual("INCONCLUSIVE", evaluate(x).decision)

    def test_inconclusive_if_ancestry_adequacy_unknown(self):
        x = base()
        x["applicability_metrics"]["ancestry_population_metadata_adequacy"] = "UNKNOWN"
        self.assertEqual("INCONCLUSIVE", evaluate(x).decision)

    def test_redesign_if_ancestry_metadata_inadequate(self):
        x = base()
        x["applicability_metrics"]["ancestry_population_metadata_adequacy"] = "INADEQUATE"
        self.assertEqual("REDESIGN", evaluate(x).decision)

    def test_inconclusive_if_symmetric_non_event_audit_incomplete(self):
        x = base()
        x["curation_metrics"]["symmetric_non_event_audit_complete"] = False
        self.assertEqual("INCONCLUSIVE", evaluate(x).decision)

    def test_inconclusive_if_symmetric_non_event_sample_too_small(self):
        x = base()
        x["curation_metrics"]["non_event_case_count"] = 50
        self.assertEqual("INCONCLUSIVE", evaluate(x).decision)

    def test_redesign_on_attention_circularity(self):
        x = base()
        x["assignment_metrics"]["attention_assignment_association"] = 0.50
        self.assertEqual("REDESIGN", evaluate(x).decision)

    def test_redesign_on_nuisance_saturation(self):
        x = base()
        x["nuisance_headroom_metrics"]["median_positive_rank_fraction"] = 0.005
        self.assertEqual("REDESIGN", evaluate(x).decision)

    def test_no_go_takes_priority_over_redesign_when_measurements_complete(self):
        x = base()
        x["provider_metrics"]["required_field_availability_fraction"] = 0.60
        x["assignment_metrics"]["attention_assignment_association"] = 0.50
        self.assertEqual("NO_GO", evaluate(x).decision)


if __name__ == "__main__":
    unittest.main()
