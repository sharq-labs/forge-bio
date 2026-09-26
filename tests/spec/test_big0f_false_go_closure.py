from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.select_big0f_sample import (
    derive_sampling_key,
    deterministic_event_sample,
    select,
)
from scripts.simulate_big0f_power import build_artifact, verify_artifact
from scripts.verify_big0f_provenance import (
    CUTOFF_ORDER,
    HORIZON_ORDER,
    canonical_digest,
    derive_curation_metrics,
    verify_curation_audit,
    verify_nuisance_run,
    verify_selection_provenance,
)


ROOT = Path(__file__).resolve().parents[2]
THRESHOLDS = json.loads(
    (ROOT / "config" / "big0f-thresholds.v1.json").read_text(encoding="utf-8")
)["thresholds"]
NUISANCE_MANIFEST = json.loads(
    (ROOT / "config" / "big0f-nuisance-manifest.v1.json").read_text(encoding="utf-8")
)


def sampling_context():
    disease_ids = [f"D{i:02d}" for i in range(30)]
    frame_digest = "sha256:" + "a" * 64
    frame_seal_digest = "sha256:" + "b" * 64
    frame_seal = {
        "attestation_id": "FRAME-SEAL-1",
        "schema_version": "external-seal-attestation-v1",
        "artifact_digest": frame_digest,
        "artifact_type": "BIG0F_DISEASE_FRAME",
        "sealed_at": "2026-09-26T10:00:30Z",
        "verified_at": "2026-09-26T10:00:40Z",
        "external_registry_or_custodian_ref": "ots-frame-proof",
        "authority_type": "THIRD_PARTY_TIMESTAMP_SERVICE",
        "attestation_method": "THIRD_PARTY_TIMESTAMP",
        "signer_or_service_identity": "opentimestamps-calendar",
        "independence_from_study_team": True,
        "independence_evidence_ref": "external-service-proof",
        "verification_status": "VERIFIED",
        "verification_evidence_ref": "ots-proof",
        "provenance_ref": "prov-frame",
        "digest": "sha256:" + "c" * 64,
    }
    beacon = {
        "beacon_id": "DRAND-101",
        "schema_version": "randomness-beacon-v1",
        "source": "DRAND",
        "round_id": "101",
        "published_at": "2026-09-26T10:01:00Z",
        "randomness_hex": "11" * 32,
        "verification_status": "VERIFIED",
        "verification_evidence_ref": "drand-proof-101",
        "frame_digest": frame_digest,
        "frame_sealed_at": "2026-09-26T10:00:30Z",
        "frame_seal_attestation_id": "FRAME-SEAL-1",
        "frame_seal_attestation_digest": frame_seal_digest,
        "selection_rule": "FIRST_VERIFIED_ROUND_AFTER_FRAME_SEAL",
        "previous_round_id": "100",
        "previous_round_published_at": "2026-09-26T10:00:00Z",
        "digest": "sha256:" + "d" * 64,
    }
    ordered = select(
        disease_ids,
        beacon,
        frame_digest,
        frame_seal_attestation=frame_seal,
        frame_seal_attestation_digest=frame_seal_digest,
        target_n=15,
    )
    return disease_ids, frame_digest, frame_seal_digest, frame_seal, beacon, ordered


def make_events(prefix: str, diseases: list[str], counts: list[int]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    n = 0
    for disease_id, count in zip(diseases, counts):
        for _ in range(count):
            rows.append({"event_id": f"{prefix}-E{n:03d}", "disease_id": disease_id})
            n += 1
    return rows


def make_pairs(first_events: list[dict[str, str]], second_events: list[dict[str, str]] | None = None):
    pairs = []
    for i, (cutoff, horizon) in enumerate(
        (pair for cutoff in CUTOFF_ORDER for pair in ((cutoff, h) for h in HORIZON_ORDER))
    ):
        raw = first_events if i == 0 else (second_events if i == 1 and second_events is not None else [])
        pairs.append({
            "cutoff": cutoff,
            "horizon": horizon,
            "provider_availability_pass": i <= (1 if second_events is not None else 0),
            "provider_availability_evidence_digest": "sha256:" + f"{i + 1:064x}"[-64:],
            "observation_window_pass": i <= (1 if second_events is not None else 0),
            "observation_window_evidence_digest": "sha256:" + f"{i + 101:064x}"[-64:],
            "raw_event_records": raw,
        })
    return pairs


def build_valid_selection(raw_events: list[dict[str, str]]):
    disease_ids, frame_digest, frame_seal_digest, frame_seal, beacon, ordered = sampling_context()
    selected_diseases = ordered[:12]
    key = derive_sampling_key(frame_digest, beacon["randomness_hex"])
    selected_events = deterministic_event_sample(
        [row for row in raw_events if row["disease_id"] in set(selected_diseases)],
        key,
        cap=THRESHOLDS["max_candidate_event_count"],
    )
    provenance = {
        "selection_id": "BIG0F-SELECTION-V1",
        "schema_version": "big0f-selection-provenance-v1",
        "candidate_pairs": make_pairs(raw_events),
        "selected_disease_ids": selected_diseases,
        "selected_event_ids": selected_events,
    }
    provenance["digest"] = canonical_digest(provenance)
    result = {
        "cutoff": "2005-12-31",
        "horizon": "3y",
        "disease_count": 12,
        "candidate_event_count": len(selected_events),
        "event_bearing_disease_count": len({r["disease_id"] for r in raw_events if r["disease_id"] in set(selected_diseases)}),
    }
    return provenance, result, (disease_ids, frame_digest, frame_seal_digest, frame_seal, beacon, ordered)


def nuisance_run():
    mandatory = NUISANCE_MANIFEST["mandatory_feature_families"]
    run = {
        "run_id": "BIG0F-NUISANCE-RUN-V1",
        "schema_version": "big0f-nuisance-run-v1",
        "nuisance_manifest_digest": "sha256:" + "e" * 64,
        "pilot_model_evaluation_mode": "NUISANCE_ONLY",
        "actual_feature_families": mandatory,
        "feature_artifact_digests": {
            family: "sha256:" + f"{i + 1:064x}"[-64:]
            for i, family in enumerate(mandatory)
        },
        "semantic_evidence_features_used": False,
        "learner_family_id": "GBDT-V1",
        "preprocessing_digest": "sha256:" + "1" * 64,
        "training_config_digest": "sha256:" + "2" * 64,
        "model_artifact_digest": "sha256:" + "3" * 64,
        "event_rank_records": [
            {"event_id": "E1", "disease_id": "D1", "rank_fraction": 0.10},
            {"event_id": "E2", "disease_id": "D1", "rank_fraction": 0.11},
            {"event_id": "E3", "disease_id": "D2", "rank_fraction": 0.12},
            {"event_id": "E4", "disease_id": "D2", "rank_fraction": 0.13},
        ],
    }
    run["digest"] = canonical_digest(run)
    return run


class Big0FFalseGoClosureTests(unittest.TestCase):
    def test_non_first_cutoff_horizon_cannot_be_selected(self):
        _, _, _, _, _, ordered = sampling_context()
        first = make_events("P0", ordered[:12], [5] * 12)
        second = make_events("P1", ordered[:12], [5] * 12)
        provenance, result, ctx = build_valid_selection(second)
        provenance["candidate_pairs"] = make_pairs(first, second)
        provenance["digest"] = canonical_digest(provenance)
        result["cutoff"] = "2005-12-31"
        result["horizon"] = "5y"
        errors = verify_selection_provenance(
            provenance,
            thresholds=THRESHOLDS,
            result=result,
            disease_ids=ctx[0],
            beacon=ctx[4],
            frame_digest=ctx[1],
            frame_seal_attestation=ctx[3],
            frame_seal_attestation_digest=ctx[2],
        )
        self.assertTrue(any("first feasible" in e for e in errors))

    def test_disease_expansion_cannot_stop_at_twelve_when_events_are_insufficient(self):
        disease_ids, frame_digest, frame_seal_digest, frame_seal, beacon, ordered = sampling_context()
        raw = make_events("EXPAND", ordered[:13], [4] * 12 + [12])
        provenance, result, _ = build_valid_selection(raw)
        result["candidate_event_count"] = 48
        result["event_bearing_disease_count"] = 12
        errors = verify_selection_provenance(
            provenance,
            thresholds=THRESHOLDS,
            result=result,
            disease_ids=disease_ids,
            beacon=beacon,
            frame_digest=frame_digest,
            frame_seal_attestation=frame_seal,
            frame_seal_attestation_digest=frame_seal_digest,
        )
        self.assertTrue(any("12-to-15" in e or "disease_count" in e for e in errors))

    def test_event_cap_cannot_be_manually_cherry_picked(self):
        _, _, _, _, _, ordered = sampling_context()
        raw = make_events("CAP", ordered[:12], [17] * 8 + [16] * 4)
        provenance, result, ctx = build_valid_selection(raw)
        self.assertEqual(150, len(provenance["selected_event_ids"]))
        provenance["selected_event_ids"][0] = "MANUAL-FAVORABLE-EVENT"
        provenance["digest"] = canonical_digest(provenance)
        errors = verify_selection_provenance(
            provenance,
            thresholds=THRESHOLDS,
            result=result,
            disease_ids=ctx[0],
            beacon=ctx[4],
            frame_digest=ctx[1],
            frame_seal_attestation=ctx[3],
            frame_seal_attestation_digest=ctx[2],
        )
        self.assertTrue(any("deterministic event-cap" in e for e in errors))

    def test_nuisance_run_must_use_every_frozen_family(self):
        run = nuisance_run()
        run["actual_feature_families"] = run["actual_feature_families"][:-1]
        run["digest"] = canonical_digest(run)
        errors = verify_nuisance_run(
            run,
            nuisance_manifest=NUISANCE_MANIFEST,
            nuisance_manifest_digest="sha256:" + "e" * 64,
        )
        self.assertTrue(any("exactly match" in e for e in errors))

    def test_power_sd_cannot_be_supplied_or_tampered_independently(self):
        run = nuisance_run()
        artifact = build_artifact(
            power_analysis_id="POWER-1",
            nuisance_run=run,
            target_power=0.80,
            replicates=10000,
            seed=7,
            input_provenance_ids=["PILOT-1"],
            engine_sha256="sha256:" + "f" * 64,
        )
        artifact["disease_level_sd"] += 0.01
        errors = verify_artifact(
            artifact,
            engine_sha256="sha256:" + "f" * 64,
            nuisance_run=run,
        )
        self.assertTrue(any("disease_level_sd" in e or "digest" in e for e in errors))

    def test_curation_burden_is_derived_from_case_records(self):
        audit = {
            "audit_id": "CURATION-1",
            "schema_version": "big0f-curation-audit-v1",
            "operational_capacity_rule_id": "CURATION-CAPACITY-V1",
            "event_case_records": [
                {"case_id": f"E{i}", "minutes": 121.0, "provenance_digest": "sha256:" + "1" * 64}
                for i in range(60)
            ],
            "non_event_case_records": [
                {"case_id": f"N{i}", "minutes": 30.0, "provenance_digest": "sha256:" + "2" * 64}
                for i in range(60)
            ],
        }
        audit["digest"] = canonical_digest(audit)
        self.assertEqual(
            [],
            verify_curation_audit(
                audit,
                total_event_cases=60,
                max_median_event_curation_minutes=120,
            ),
        )
        metrics = derive_curation_metrics(
            audit,
            total_event_cases=60,
            max_median_event_curation_minutes=120,
        )
        self.assertEqual("EXCESSIVE", metrics["retrospective_curation_burden_assessment"])
        self.assertTrue(metrics["symmetric_non_event_audit_complete"])


if __name__ == "__main__":
    unittest.main()
