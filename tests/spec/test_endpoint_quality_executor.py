from __future__ import annotations

import unittest

from scripts.evaluate_endpoint_quality import evaluate_event, validate_rule_semantics


def rule():
    return {
        "rule_id":"EQR-V1",
        "schema_version":"endpoint-quality-rule-v1",
        "status":"FROZEN",
        "endpoint_subtype":"E1-NOVEL-STRICT",
        "provider_audit_ref":"sha256:"+"1"*64,
        "criteria":[
            {"criterion_id":"C01","scientific_dimension":"STUDY_DESIGN","field_or_artifact":"study_design_class","operator":"IN","value":["GENOME_WIDE","EXOME_WIDE","BIOBANK_WIDE"],"unit":None,"required":True,"justification":"hypothesis-free ascertainment"},
            {"criterion_id":"C02","scientific_dimension":"STATISTICAL_STRENGTH","field_or_artifact":"p_value","operator":"LE","value":5e-8,"unit":None,"required":True,"justification":"predeclared statistical strength"},
            {"criterion_id":"C03","scientific_dimension":"SAMPLE_SIZE","field_or_artifact":"sample_size","operator":"GE","value":1000,"unit":"participants","required":True,"justification":"minimum effective study size"},
            {"criterion_id":"C04","scientific_dimension":"INDEPENDENCE","field_or_artifact":"independence_status","operator":"EQ","value":"INDEPENDENT","unit":None,"required":True,"justification":"independent support"},
            {"criterion_id":"C05","scientific_dimension":"PHENOTYPE_MATCH","field_or_artifact":"phenotype_relation","operator":"IN","value":["EXACT","SAME_CONCEPT_DIFFERENT_DEFINITION"],"unit":None,"required":True,"justification":"phenotype specificity"},
            {"criterion_id":"C06","scientific_dimension":"GENOMIC_HARMONIZATION","field_or_artifact":"genomic_harmonization_status","operator":"EQ","value":"RESOLVED","unit":None,"required":True,"justification":"resolved variant identity"},
            {"criterion_id":"C07","scientific_dimension":"ALLELE_DIRECTION","field_or_artifact":"allele_direction_status","operator":"IN","value":["CONSISTENT","NOT_APPLICABLE"],"unit":None,"required":True,"justification":"allele semantics"},
            {"criterion_id":"C08","scientific_dimension":"POPULATION_ANCESTRY","field_or_artifact":"population_ancestry_status","operator":"EQ","value":"ADEQUATE","unit":None,"required":True,"justification":"population interpretation"},
            {"criterion_id":"C09","scientific_dimension":"GENE_ASSIGNMENT","field_or_artifact":"gene_assignment_class","operator":"IN","value":["HYPOTHESIS_FREE_CODING_OR_LOF","HIGH_CONFIDENCE_FINE_MAPPING","PREREGISTERED_COLOCALIZATION"],"unit":None,"required":True,"justification":"primary assignment"},
            {"criterion_id":"C10","scientific_dimension":"HISTORICAL_NOVELTY","field_or_artifact":"historical_novelty_status","operator":"EQ","value":"NOVEL_CONFIRMED","unit":None,"required":True,"justification":"strict novelty"},
            {"criterion_id":"C11","scientific_dimension":"SOURCE_QUALITY","field_or_artifact":"source_quality_status","operator":"IN","value":["PRIMARY_SOURCE_VERIFIED","INDEPENDENT_REEXTRACTION"],"unit":None,"required":True,"justification":"source quality"},
        ],
        "independence_requirement":"REQUIRED",
        "phenotype_policy_ref":"ADR-008",
        "gene_assignment_policy_ref":"BIG0F-ADJUDICATION-V1",
        "genomic_harmonization_policy_ref":"ADR-011",
        "frozen_at":"2026-09-26T00:00:00Z",
        "digest":"sha256:"+"2"*64,
    }


def event():
    return {
        "event_id":"EV1",
        "schema_version":"endpoint-event-input-v1",
        "fields":{
            "study_design_class":"GENOME_WIDE",
            "p_value":1e-9,
            "sample_size":50000,
            "independence_status":"INDEPENDENT",
            "phenotype_relation":"EXACT",
            "genomic_harmonization_status":"RESOLVED",
            "allele_direction_status":"CONSISTENT",
            "population_ancestry_status":"ADEQUATE",
            "gene_assignment_class":"HIGH_CONFIDENCE_FINE_MAPPING",
            "historical_novelty_status":"NOVEL_CONFIRMED",
            "source_quality_status":"PRIMARY_SOURCE_VERIFIED",
        },
        "digest":"sha256:"+"3"*64,
    }


class EndpointQualityExecutorTests(unittest.TestCase):
    def test_valid_event_qualifies(self):
        self.assertEqual([], validate_rule_semantics(rule()))
        self.assertTrue(evaluate_event(rule(),event())["qualifies"])

    def test_targeted_candidate_gene_does_not_qualify(self):
        e=event()
        e["fields"]["study_design_class"]="TARGETED_CANDIDATE_GENE"
        self.assertFalse(evaluate_event(rule(),e)["qualifies"])

    def test_unknown_independence_does_not_qualify(self):
        e=event()
        e["fields"]["independence_status"]="UNKNOWN"
        self.assertFalse(evaluate_event(rule(),e)["qualifies"])

    def test_missing_required_field_fails_closed(self):
        e=event()
        del e["fields"]["phenotype_relation"]
        self.assertFalse(evaluate_event(rule(),e)["qualifies"])

    def test_wrong_pvalue_direction_is_invalid_rule(self):
        r=rule()
        r["criteria"][1]["operator"]="GE"
        self.assertTrue(validate_rule_semantics(r))
        with self.assertRaises(ValueError):
            evaluate_event(r,event())

    def test_non_hypothesis_free_gene_assignment_is_invalid_rule(self):
        r=rule()
        r["criteria"][8]["value"]=["AUTHOR_NAMED"]
        self.assertTrue(validate_rule_semantics(r))

    def test_duplicate_field_is_invalid_rule(self):
        r=rule()
        r["criteria"][10]["field_or_artifact"]="p_value"
        self.assertTrue(validate_rule_semantics(r))

    def test_presence_only_frozen_criterion_is_invalid(self):
        r=rule()
        r["criteria"][4].pop("value")
        r["criteria"][4]["operator"]="REQUIRE"
        self.assertTrue(validate_rule_semantics(r))


if __name__=="__main__":
    unittest.main()
