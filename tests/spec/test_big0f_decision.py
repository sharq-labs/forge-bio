from __future__ import annotations

import copy
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
            "primary_assignment_agreement": 0.80,
            "phenotype_agreement": 0.80,
        },
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
        x=base()
        x["provider_metrics"]["required_field_availability_fraction"]=0.60
        self.assertEqual("NO_GO", evaluate(x).decision)

    def test_no_go_on_low_power(self):
        x=base()
        x["power_metrics"]["estimated_power"]=0.60
        self.assertEqual("NO_GO", evaluate(x).decision)

    def test_redesign_on_attention_circularity(self):
        x=base()
        x["assignment_metrics"]["attention_assignment_association"]=0.50
        self.assertEqual("REDESIGN", evaluate(x).decision)

    def test_redesign_on_nuisance_saturation(self):
        x=base()
        x["nuisance_headroom_metrics"]["median_positive_rank_fraction"]=0.005
        self.assertEqual("REDESIGN", evaluate(x).decision)

    def test_no_go_takes_priority_over_redesign(self):
        x=base()
        x["provider_metrics"]["required_field_availability_fraction"]=0.60
        x["assignment_metrics"]["attention_assignment_association"]=0.50
        self.assertEqual("NO_GO", evaluate(x).decision)


if __name__ == "__main__":
    unittest.main()
