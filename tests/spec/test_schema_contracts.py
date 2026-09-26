from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError

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
        cls.validator = Draft202012Validator(cls.schema)

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
            "knowledge_watermark": "DATED(2026-09-26)",
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
        Draft202012Validator(load(schema_name)).validate(instance)

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


if __name__ == "__main__":
    unittest.main()
