from __future__ import annotations

import copy
import math
import unittest

from scripts.evaluate_endpoint_quality import evaluate_rule, validate_rule


def frozen_rule():
    criteria = [
        {"criterion_id":"C1","scientific_dimension":"STUDY_DESIGN","field_or_artifact":"study_design_class","operator":"IN","value":["GENOME_WIDE","EXOME_WIDE","BIOBANK_WIDE"],"unit":None,"required":True,"justification":"hypothesis-free ascertainment"},
        {"criterion_id":"C2","scientific_dimension":"STATISTICAL_STRENGTH","field_or_artifact":"p_value","operator":"LE","value":5e-8,"unit":None,"required":True,"justification":"frozen significance criterion"},
        {"criterion_id":"C3","scientific_dimension":"SAMPLE_SIZE","field_or_artifact":"sample_size","operator":"GE","value":1000,"unit":"participants","required":True,"justification":"minimum evidence size"},
        {"criterion_id":"C4","scientific_dimension":"INDEPENDENCE","field_or_artifact":"independence_state","operator":"IN","value":["INDEPENDENT"],"unit":None,"required":True,"justification":"independent future support"},
        {"criterion_id":"C5","scientific_dimension":"PHENOTYPE_MATCH","field_or_artifact":"phenotype_relation","operator":"IN","value":["EXACT","SAME_CONCEPT_DIFFERENT_DEFINITION"],"unit":None,"required":True,"justification":"phenotype specificity"},
        {"criterion_id":"C6","scientific_dimension":"GENOMIC_HARMONIZATION","field_or_artifact":"genomic_harmonization_status","operator":"IN","value":["PASS","RESOLVED"],"unit":None,"required":True,"justification":"variant identity"},
        {"criterion_id":"C7","scientific_dimension":"ALLELE_DIRECTION","field_or_artifact":"allele_direction_status","operator":"IN","value":["CONSISTENT","RESOLVED","NOT_APPLICABLE"],"unit":None,"required":True,"justification":"allele semantics"},
        {"criterion_id":"C8","scientific_dimension":"POPULATION_ANCESTRY","field_or_artifact":"population_ancestry_status","operator":"IN","value":["ADEQUATE","KNOWN"],"unit":None,"required":True,"justification":"applicability"},
        {"criterion_id":"C9","scientific_dimension":"GENE_ASSIGNMENT","field_or_artifact":"gene_assignment_class","operator":"IN","value":["HYPOTHESIS_FREE_CODING_OR_LOF","HIGH_CONFIDENCE_FINE_MAPPING","PREREGISTERED_COLOCALIZATION"],"unit":None,"required":True,"justification":"high-specificity assignment"},
        {"criterion_id":"C10","scientific_dimension":"HISTORICAL_NOVELTY","field_or_artifact":"pre_t_genetic_state","operator":"IN","value":["NO_SIGNAL_OBSERVED"],"unit":None,"required":True,"justification":"strict novelty"},
        {"criterion_id":"C11","scientific_dimension":"SOURCE_QUALITY","field_or_artifact":"source_quality_status","operator":"IN","value":["PRIMARY_SOURCE","QUALIFIED_INDEPENDENT_SOURCE"],"unit":None,"required":True,"justification":"source integrity"},
    ]
    return {
        "rule_id":"EQ1",
        "schema_version":"endpoint-quality-rule-v1",
        "status":"FROZEN",
        "endpoint_subtype":"E1-NOVEL-STRICT",
        "provider_audit_ref":"sha256:"+"a"*64,
        "criteria":criteria,
        "independence_requirement":"REQUIRED",
        "phenotype_policy_ref":"ADR-008",
        "gene_assignment_policy_ref":"BIG0F-ADJUDICATION-V1",
        "genomic_harmonization_policy_ref":"ADR-011",
        "frozen_at":"2026-09-26T00:00:00Z",
        "digest":"sha256:"+"b"*64,
    }


def qualifying_event():
    return {
        "study_design_class":"GENOME_WIDE",
        "p_value":1e-9,
        "sample_size":50000,
        "independence_state":"INDEPENDENT",
        "phenotype_relation":"EXACT",
        "genomic_harmonization_status":"PASS",
        "allele_direction_status":"CONSISTENT",
        "population_ancestry_status":"ADEQUATE",
        "gene_assignment_class":"HIGH_CONFIDENCE_FINE_MAPPING",
        "pre_t_genetic_state":"NO_SIGNAL_OBSERVED",
        "source_quality_status":"PRIMARY_SOURCE",
    }


class EndpointQualityExecutorTests(unittest.TestCase):
    def test_valid_rule_executes(self):
        rule=frozen_rule()
        self.assertEqual([],validate_rule(rule))
        self.assertTrue(evaluate_rule(rule,qualifying_event())[0])

    def test_unknown_field_is_rejected(self):
        rule=frozen_rule()
        rule["criteria"][1]["field_or_artifact"]="vibes"
        self.assertTrue(validate_rule(rule))

    def test_p_value_wrong_direction_is_rejected(self):
        rule=frozen_rule()
        rule["criteria"][1]["operator"]="GE"
        self.assertTrue(validate_rule(rule))

    def test_nan_operand_is_rejected(self):
        rule=frozen_rule()
        rule["criteria"][1]["value"]=float("nan")
        self.assertTrue(validate_rule(rule))

    def test_infinity_operand_is_rejected(self):
        rule=frozen_rule()
        rule["criteria"][1]["value"]=float("inf")
        self.assertTrue(validate_rule(rule))

    def test_unknown_independence_is_rejected(self):
        rule=frozen_rule()
        rule["criteria"][3]["value"]=["INDEPENDENT","UNKNOWN"]
        self.assertTrue(validate_rule(rule))

    def test_duplicate_criterion_is_rejected(self):
        rule=frozen_rule()
        duplicate=copy.deepcopy(rule["criteria"][1])
        duplicate["value"]=0.05
        rule["criteria"].append(duplicate)
        self.assertTrue(validate_rule(rule))

    def test_targeted_candidate_gene_design_is_not_primary(self):
        rule=frozen_rule()
        rule["criteria"][0]["value"]=["GENOME_WIDE","TARGETED_CANDIDATE_GENE"]
        self.assertTrue(validate_rule(rule))

    def test_event_unknown_independence_fails_execution(self):
        event=qualifying_event()
        event["independence_state"]="UNKNOWN"
        passed,failures=evaluate_rule(frozen_rule(),event)
        self.assertFalse(passed)
        self.assertTrue(any("independence_state" in f for f in failures))

    def test_event_nan_pvalue_fails_execution(self):
        event=qualifying_event()
        event["p_value"]=float("nan")
        passed,failures=evaluate_rule(frozen_rule(),event)
        self.assertFalse(passed)


if __name__=="__main__":
    unittest.main()
