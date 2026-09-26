from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.build_seal_bundle import (
    build_manifest,
    manifest_digest,
    sha256_file,
    verify_manifest,
)


ROOT = Path(__file__).resolve().parents[2]


class SealBundleV2Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

        self.protocol = self.root / "protocol.md"
        self.protocol.write_text("BIG 0F protocol\n", encoding="utf-8")

        self.frame = self.root / "frame.json"
        self.frame.write_text(json.dumps([f"D{i}" for i in range(30)]) + "\n", encoding="utf-8")
        frame_digest = sha256_file(self.frame)

        self.beacon = self.root / "beacon.json"
        self.beacon.write_text(json.dumps({
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
            "selection_rule": "FIRST_VERIFIED_ROUND_AFTER_FRAME_SEAL",
            "previous_round_id": "100",
            "previous_round_published_at": "2026-09-26T10:00:00Z",
            "digest": "sha256:" + "8" * 64,
        }, sort_keys=True) + "\n", encoding="utf-8")

        self.thresholds = ROOT / "config" / "big0f-thresholds.v1.json"
        self.adjudication = ROOT / "config" / "big0f-adjudication-policy.v1.json"
        self.nuisance = ROOT / "config" / "big0f-nuisance-manifest.v1.json"

        self.engine = self.root / "evaluate_big0f.py"
        shutil.copyfile(ROOT / "scripts" / "evaluate_big0f.py", self.engine)
        self.sampling = self.root / "select_big0f_sample.py"
        shutil.copyfile(ROOT / "scripts" / "select_big0f_sample.py", self.sampling)
        self.power_engine = self.root / "simulate_big0f_power.py"
        shutil.copyfile(ROOT / "scripts" / "simulate_big0f_power.py", self.power_engine)

        self.pilot_schema = ROOT / "schemas" / "big0f-pilot-result.v1.schema.json"
        self.threshold_schema = ROOT / "schemas" / "big0f-threshold-manifest.v1.schema.json"
        self.adjudication_schema = ROOT / "schemas" / "big0f-adjudication-policy.v1.schema.json"
        self.nuisance_schema = ROOT / "schemas" / "big0f-nuisance-manifest.v1.schema.json"
        self.power_schema = ROOT / "schemas" / "big0f-power-analysis.v1.schema.json"

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def build(self):
        return build_manifest(
            protocol_path=self.protocol,
            disease_frame_path=self.frame,
            randomness_beacon_path=self.beacon,
            threshold_manifest_path=self.thresholds,
            adjudication_policy_path=self.adjudication,
            nuisance_manifest_path=self.nuisance,
            decision_engine_path=self.engine,
            pilot_result_schema_path=self.pilot_schema,
            sampling_code_path=self.sampling,
            threshold_manifest_schema_path=self.threshold_schema,
            adjudication_policy_schema_path=self.adjudication_schema,
            nuisance_manifest_schema_path=self.nuisance_schema,
            power_analysis_schema_path=self.power_schema,
            power_engine_path=self.power_engine,
            created_at="2026-09-26T10:02:00Z",
            created_by_role="INDEPENDENT_CUSTODIAN",
        )

    def components(self):
        return {
            "protocol": self.protocol,
            "disease_frame": self.frame,
            "randomness_beacon": self.beacon,
            "threshold_manifest": self.thresholds,
            "adjudication_policy": self.adjudication,
            "nuisance_manifest": self.nuisance,
            "decision_engine": self.engine,
            "pilot_result_schema": self.pilot_schema,
            "sampling_code": self.sampling,
            "threshold_manifest_schema": self.threshold_schema,
            "adjudication_policy_schema": self.adjudication_schema,
            "nuisance_manifest_schema": self.nuisance_schema,
            "power_analysis_schema": self.power_schema,
            "power_engine": self.power_engine,
        }

    def attestation(self, manifest, authority="THIRD_PARTY_TIMESTAMP_SERVICE"):
        method = {
            "THIRD_PARTY_TIMESTAMP_SERVICE": "THIRD_PARTY_TIMESTAMP",
            "PUBLIC_REGISTRY": "PUBLIC_PREREGISTRATION",
        }[authority]
        return {
            "attestation_id": f"ATT-{authority}",
            "schema_version": "external-seal-attestation-v1",
            "artifact_digest": manifest_digest(manifest),
            "artifact_type": "BIG0F_SEAL_BUNDLE",
            "sealed_at": "2026-09-26T10:03:00Z",
            "verified_at": "2026-09-26T10:04:00Z",
            "external_registry_or_custodian_ref": "external-ref",
            "authority_type": authority,
            "attestation_method": method,
            "signer_or_service_identity": "external-service",
            "independence_from_study_team": True,
            "independence_evidence_ref": "independence-proof",
            "verification_status": "VERIFIED",
            "verification_evidence_ref": "verification-proof",
            "provenance_ref": "prov",
            "digest": "sha256:" + "9" * 64,
        }

    def test_clean_bundle_verifies(self):
        m = self.build()
        self.assertEqual([], verify_manifest(m, attestation=self.attestation(m), component_paths=self.components()))

    def test_component_tamper_is_detected(self):
        m = self.build()
        self.frame.write_text(json.dumps(["D-EVIL"]) + "\n", encoding="utf-8")
        errors = verify_manifest(m, attestation=self.attestation(m), component_paths=self.components())
        self.assertTrue(any("disease_frame_sha256 mismatch" in e for e in errors))

    def test_decision_engine_tamper_is_detected(self):
        m = self.build()
        self.engine.write_text(self.engine.read_text(encoding="utf-8") + "\n# mutation\n", encoding="utf-8")
        errors = verify_manifest(m, attestation=self.attestation(m), component_paths=self.components())
        self.assertTrue(any("decision_engine_sha256 mismatch" in e for e in errors))

    def test_sampling_code_tamper_is_detected(self):
        m = self.build()
        self.sampling.write_text(self.sampling.read_text(encoding="utf-8") + "\n# mutation\n", encoding="utf-8")
        errors = verify_manifest(m, attestation=self.attestation(m), component_paths=self.components())
        self.assertTrue(any("sampling_code_sha256 mismatch" in e for e in errors))

    def test_power_engine_tamper_is_detected(self):
        m = self.build()
        self.power_engine.write_text(self.power_engine.read_text(encoding="utf-8") + "\n# mutation\n", encoding="utf-8")
        errors = verify_manifest(m, attestation=self.attestation(m), component_paths=self.components())
        self.assertTrue(any("power_engine_sha256 mismatch" in e for e in errors))

    def test_manifest_mutation_cannot_be_resealed_by_caller_argument(self):
        m = self.build()
        att = self.attestation(m)
        m["protocol_version"] = "EVIL"
        errors = verify_manifest(m, attestation=att, component_paths=self.components())
        self.assertTrue(errors)
        self.assertTrue(any("externally attested digest" in e or "schema violation" in e for e in errors))

    def test_beacon_must_be_first_round_after_frame_seal(self):
        b = json.loads(self.beacon.read_text(encoding="utf-8"))
        b["previous_round_published_at"] = "2026-09-26T10:00:45Z"
        self.beacon.write_text(json.dumps(b) + "\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            self.build()

    def test_beacon_must_be_bound_to_frame(self):
        b = json.loads(self.beacon.read_text(encoding="utf-8"))
        b["frame_digest"] = "sha256:" + "0" * 64
        self.beacon.write_text(json.dumps(b) + "\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            self.build()

    def test_field_reordering_does_not_change_manifest_digest(self):
        m = self.build()
        reordered = dict(reversed(list(m.items())))
        self.assertEqual(manifest_digest(m), manifest_digest(reordered))


if __name__ == "__main__":
    unittest.main()
