from __future__ import annotations

import copy
import unittest

from scripts.validate_research_program import validate_program


def budget():
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
        "post_failure_policy": "no reset by rename",
        "research_program_id": "FORGE-BIO-B-TGT-E1-V0",
        "program_scope_lock": "RENAMING_BENCHMARK_ENDPOINT_FRAME_OR_MODEL_DOES_NOT_RESET_BUDGET",
        "digest": "sha256:" + "a" * 64,
    }


def attempt(idx=1, gid="G1", alpha=0.025, attempt_id="A1"):
    return {
        "attempt_id": attempt_id,
        "schema_version": "research-program-attempt-v1",
        "benchmark_family": "B-TGT-E1",
        "benchmark_generation": gid,
        "endpoint": "E1-NOVEL-STRICT",
        "horizon": "5y",
        "primary_metric": "EVENT_RANK_PERCENTILE_V1",
        "model_family": "ranker-v1",
        "result_status": "NULL",
        "visibility": "INTERNAL",
        "relationship_to_prior_attempts": "canonical program",
        "digest": "sha256:" + "b" * 64,
        "attempt_tier": "CONFIRMATORY",
        "registered_at": "2026-01-01T00:00:00Z",
        "map_digest": "sha256:" + "c" * 64,
        "external_seal_attestation_id": "SEAL1",
        "disclosure_status": "SCHEDULED",
        "disclosure_due_at": "2027-01-01T00:00:00Z",
        "research_program_id": "FORGE-BIO-B-TGT-E1-V0",
        "result_recorded_at": "2026-02-01T00:00:00Z",
        "confirmatory_program_budget_id": "CPB-FORGE-BIO-B-TGT-E1-V0",
        "allocation_generation_id": gid,
        "allocated_alpha": alpha,
        "attempt_index": idx,
    }


class ResearchProgramValidatorTests(unittest.TestCase):
    def test_valid_program(self):
        self.assertEqual([], validate_program(budget(), [attempt()]))

    def test_alpha_must_match_generation(self):
        errors = validate_program(budget(), [attempt(alpha=0.01)])
        self.assertTrue(any("allocated alpha does not match" in e for e in errors))

    def test_generation_cannot_be_reused(self):
        errors = validate_program(
            budget(),
            [attempt(idx=1, gid="G1", attempt_id="A1"), attempt(idx=2, gid="G1", attempt_id="A2")],
        )
        self.assertTrue(any("generation G1 is reused" in e for e in errors))

    def test_attempt_indices_are_contiguous(self):
        errors = validate_program(
            budget(),
            [attempt(idx=1, gid="G1", attempt_id="A1"), attempt(idx=3, gid="G2", attempt_id="A2")],
        )
        self.assertTrue(any("contiguous" in e for e in errors))

    def test_canonical_budget_blocks_family_rename_reset(self):
        b = budget()
        b["benchmark_family"] = "B-TGT-E1-v2"
        errors = validate_program(b, [attempt()])
        self.assertTrue(errors)


if __name__ == "__main__":
    unittest.main()
