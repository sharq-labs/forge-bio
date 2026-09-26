from __future__ import annotations

import copy
import unittest

from jsonschema import ValidationError

from scripts.scientific_invariants import (
    validate_benchmark_exposure_ledger,
    validate_confirmatory_program_budget,
    validate_external_seal,
    validate_semantics,
)
from test_hostile_review_regressions import assert_schema_invalid, valid_map, validator


class Round2HostileRegressionTests(unittest.TestCase):
    def test_confirmatory_map_cannot_use_current_discovery_mode(self):
        x = valid_map()
        x["policies"]["scientific_operating_mode"] = "CURRENT_DISCOVERY"
        validator("map.v1.schema.json").validate(x)
        self.assertTrue(validate_semantics("map", x))

    def test_confirmatory_map_cannot_use_failed_reconstruction_fidelity(self):
        x = valid_map()
        x["providers"]["reconstruction_fidelity_verdicts"] = ["FAIL"]
        validator("map.v1.schema.json").validate(x)
        self.assertTrue(validate_semantics("map", x))

    def test_disease_specific_attention_volume_is_mandatory(self):
        x = valid_map()
        x["baselines"]["nuisance_feature_family_ids"].remove("DISEASE_SPECIFIC_ATTENTION_VOLUME")
        assert_schema_invalid(self, "map.v1.schema.json", x)

    def test_disease_specific_attention_momentum_is_mandatory(self):
        x = valid_map()
        x["baselines"]["nuisance_feature_family_ids"].remove("DISEASE_SPECIFIC_ATTENTION_MOMENTUM")
        assert_schema_invalid(self, "map.v1.schema.json", x)

    def test_random_cannot_masquerade_as_combined_nuisance(self):
        x = valid_map()
        x["baselines"]["primary_comparator_id"] = "RANDOM"
        x["baselines"]["combined_nuisance_model_id"] = "RANDOM"
        assert_schema_invalid(self, "map.v1.schema.json", x)

    def test_comparison_capacity_parity_is_required(self):
        x = valid_map()
        x["comparison_design"]["capacity_parity_required"] = False
        assert_schema_invalid(self, "map.v1.schema.json", x)

    def test_confirmatory_alpha_is_exactly_005(self):
        x = valid_map()
        x["statistics"]["alpha"] = 0.10
        assert_schema_invalid(self, "map.v1.schema.json", x)

    def active_ledger(self):
        return {
            "ledger_id": "L1",
            "schema_version": "benchmark-exposure-ledger-v1",
            "benchmark_generation_id": "G1",
            "lifecycle_status": "ACTIVE_CONFIRMATORY",
            "exposure_events": [],
            "attempt_ids": [],
            "external_seal_attestation_id": "SEAL1",
            "max_aggregate_disclosures": 10,
            "max_subgroup_disclosures": 3,
            "digest": "sha256:" + "a" * 64,
        }

    def test_public_full_label_retires_active_confirmatory_generation(self):
        x = self.active_ledger()
        x["exposure_events"] = [{
            "exposure_time": "2026-01-01T00:00:00Z",
            "exposure_kind": "LABEL_REVEAL",
            "disclosure_level": "FULL_LABEL",
            "audience_role": "PUBLIC",
            "downstream_change_ref": None,
        }]
        assert_schema_invalid(self, "benchmark-exposure-ledger.v1.schema.json", x)
        self.assertTrue(validate_benchmark_exposure_ledger(x))

    def test_many_subgroup_disclosures_exceed_active_budget(self):
        x = self.active_ledger()
        x["exposure_events"] = [{
            "exposure_time": f"2026-01-{i+1:02d}T00:00:00Z",
            "exposure_kind": "SUBGROUP_RESULT",
            "disclosure_level": "SUBGROUP",
            "audience_role": "RANKING_TEAM",
            "downstream_change_ref": None,
        } for i in range(4)]
        validator("benchmark-exposure-ledger.v1.schema.json").validate(x)
        self.assertTrue(validate_benchmark_exposure_ledger(x))

    def test_active_confirmatory_requires_external_seal(self):
        x = self.active_ledger()
        x.pop("external_seal_attestation_id")
        assert_schema_invalid(self, "benchmark-exposure-ledger.v1.schema.json", x)

    def external_seal(self):
        return {
            "attestation_id": "ES1",
            "schema_version": "external-seal-attestation-v1",
            "artifact_digest": "sha256:" + "b" * 64,
            "artifact_type": "BIG0F_SEAL_BUNDLE",
            "sealed_at": "2026-01-01T00:00:00Z",
            "verified_at": "2026-01-01T00:01:00Z",
            "external_registry_or_custodian_ref": "ots-proof",
            "authority_type": "THIRD_PARTY_TIMESTAMP_SERVICE",
            "attestation_method": "THIRD_PARTY_TIMESTAMP",
            "signer_or_service_identity": "external-service",
            "independence_from_study_team": True,
            "independence_evidence_ref": "independence-proof",
            "verification_status": "VERIFIED",
            "verification_evidence_ref": "proof",
            "provenance_ref": "prov",
            "digest": "sha256:" + "c" * 64,
        }

    def test_big0f_bundle_cannot_be_self_custodian_seal(self):
        x = self.external_seal()
        x["authority_type"] = "INDEPENDENT_CUSTODIAN"
        x["attestation_method"] = "SIGNED_CUSTODIAN_ATTESTATION"
        assert_schema_invalid(self, "external-seal-attestation.v1.schema.json", x)

    def test_unknown_seal_is_not_claim_valid(self):
        x = self.external_seal()
        x["verification_status"] = "UNKNOWN"
        assert_schema_invalid(self, "external-seal-attestation.v1.schema.json", x)
        self.assertTrue(validate_external_seal(x))

    def budget(self):
        return {
            "budget_id": "CPB-FORGE-BIO-B-TGT-E1-V0",
            "schema_version": "confirmatory-program-budget-v1",
            "benchmark_family": "B-TGT-E1",
            "familywise_alpha": 0.05,
            "allocation_method": "FIXED_SPLIT",
            "max_confirmatory_generations": 2,
            "generation_allocations": [
                {"generation_id": "G1", "allocated_alpha": 0.025, "status": "PLANNED"},
                {"generation_id": "G2", "allocated_alpha": 0.025, "status": "PLANNED"},
            ],
            "development_results_can_support_confirmatory_claim": False,
            "post_failure_policy": "no rename reset",
            "research_program_id": "FORGE-BIO-B-TGT-E1-V0",
            "program_scope_lock": "RENAMING_BENCHMARK_ENDPOINT_FRAME_OR_MODEL_DOES_NOT_RESET_BUDGET",
            "digest": "sha256:" + "d" * 64,
        }

    def test_program_budget_cannot_reset_by_family_rename(self):
        x = self.budget()
        x["benchmark_family"] = "NEW-SUCCESSFUL-NAME"
        assert_schema_invalid(self, "confirmatory-program-budget.v1.schema.json", x)

    def test_duplicate_generation_ids_are_rejected_semantically(self):
        x = self.budget()
        x["generation_allocations"][1]["generation_id"] = "G1"
        x["generation_allocations"][1]["status"] = "ACTIVE"
        validator("confirmatory-program-budget.v1.schema.json").validate(x)
        self.assertTrue(validate_confirmatory_program_budget(x))

    def test_program_budget_cannot_exceed_familywise_alpha(self):
        x = self.budget()
        x["generation_allocations"][0]["allocated_alpha"] = 0.04
        x["generation_allocations"][1]["allocated_alpha"] = 0.04
        validator("confirmatory-program-budget.v1.schema.json").validate(x)
        self.assertTrue(validate_confirmatory_program_budget(x))


if __name__ == "__main__":
    unittest.main()
