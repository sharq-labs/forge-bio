from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.build_seal_bundle import (
    build_manifest,
    canonical_json_bytes,
    manifest_digest,
    seed_commitment,
    verify_manifest,
)


class SealBundleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.files = {}
        for name, content in {
            "protocol": "protocol-v1\n",
            "frame": "D1\nD2\nD3\n",
            "thresholds": '{"go": 0.9}\n',
            "adjudication": "blind-v1\n",
            "nuisance": "ATTENTION\nGENE_LENGTH\nPLEIOTROPY\n",
        }.items():
            p = self.root / f"{name}.txt"
            p.write_text(content, encoding="utf-8")
            self.files[name] = p
        self.seed = "11" * 32

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def manifest(self):
        return build_manifest(
            protocol_path=self.files["protocol"],
            disease_frame_path=self.files["frame"],
            threshold_manifest_path=self.files["thresholds"],
            adjudication_policy_path=self.files["adjudication"],
            nuisance_manifest_path=self.files["nuisance"],
            seed_hex=self.seed,
            protocol_version="BIG-0F-v0-test",
            sampling_algorithm_version="seeded-permutation-v1",
        )

    def test_canonical_manifest_is_deterministic(self) -> None:
        a = self.manifest()
        b = json.loads(canonical_json_bytes(a))
        self.assertEqual(canonical_json_bytes(a), canonical_json_bytes(b))
        self.assertEqual(manifest_digest(a), manifest_digest(b))

    def test_seed_commitment_is_domain_separated(self) -> None:
        self.assertTrue(seed_commitment(self.seed).startswith("sha256:"))
        self.assertNotEqual(seed_commitment(self.seed), "sha256:" + "11" * 32)

    def test_verify_clean_bundle(self) -> None:
        errors = verify_manifest(
            self.manifest(),
            protocol_path=self.files["protocol"],
            disease_frame_path=self.files["frame"],
            threshold_manifest_path=self.files["thresholds"],
            adjudication_policy_path=self.files["adjudication"],
            nuisance_manifest_path=self.files["nuisance"],
            seed_hex=self.seed,
        )
        self.assertEqual([], errors)

    def test_one_byte_tamper_is_detected(self) -> None:
        manifest = self.manifest()
        self.files["frame"].write_text("D1\nD2\nD4\n", encoding="utf-8")
        errors = verify_manifest(
            manifest,
            protocol_path=self.files["protocol"],
            disease_frame_path=self.files["frame"],
            threshold_manifest_path=self.files["thresholds"],
            adjudication_policy_path=self.files["adjudication"],
            nuisance_manifest_path=self.files["nuisance"],
            seed_hex=self.seed,
        )
        self.assertTrue(any("disease_frame_sha256 mismatch" in e for e in errors))

    def test_wrong_seed_is_detected(self) -> None:
        manifest = self.manifest()
        errors = verify_manifest(
            manifest,
            protocol_path=self.files["protocol"],
            disease_frame_path=self.files["frame"],
            threshold_manifest_path=self.files["thresholds"],
            adjudication_policy_path=self.files["adjudication"],
            nuisance_manifest_path=self.files["nuisance"],
            seed_hex="22" * 32,
        )
        self.assertTrue(any("random_seed_commitment_sha256 mismatch" in e for e in errors))

    def test_seed_must_be_256_bit(self) -> None:
        with self.assertRaises(ValueError):
            seed_commitment("11" * 8)


if __name__ == "__main__":
    unittest.main()
