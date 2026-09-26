from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from scripts.verify_external_authorities import (
    verify_drand_beacon,
    verify_external_attestation,
    verify_osf_registry,
    verify_ots_bytes,
)


class ExternalAuthorityVerifierTests(unittest.TestCase):
    def test_ots_requires_real_client_success_marker(self):
        with tempfile.TemporaryDirectory() as tmp:
            proof = Path(tmp) / "proof.ots"
            proof.write_bytes(b"proof")
            runner = lambda *args, **kwargs: SimpleNamespace(
                returncode=0,
                stdout="Success! Bitcoin block 123 attests existence as of 2026-01-01",
                stderr="",
            )
            self.assertEqual([], verify_ots_bytes(b"artifact", proof, runner=runner))

    def test_ots_zero_exit_without_verified_result_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            proof = Path(tmp) / "proof.ots"
            proof.write_bytes(b"proof")
            runner = lambda *args, **kwargs: SimpleNamespace(
                returncode=0,
                stdout="pending calendar attestation",
                stderr="",
            )
            self.assertTrue(verify_ots_bytes(b"artifact", proof, runner=runner))

    def test_public_registry_must_be_approved_osf_host_and_contain_digest(self):
        attestation = {
            "verification_evidence_ref": "https://osf.io/abcd1/",
            "artifact_digest": "sha256:" + "a" * 64,
        }
        fetcher = lambda url, timeout: (
            b'{"registered_commitment":"sha256:' + b"a" * 64 + b'"}'
        )
        self.assertEqual([], verify_osf_registry(attestation, fetcher=fetcher))

        bad = dict(attestation)
        bad["verification_evidence_ref"] = "https://example.com/fake"
        self.assertTrue(verify_osf_registry(bad, fetcher=fetcher))

    def test_external_attestation_recomputes_exact_artifact_digest(self):
        artifact = b"exact bytes"
        import hashlib

        attestation = {
            "authority_type": "PUBLIC_REGISTRY",
            "artifact_digest": "sha256:" + hashlib.sha256(artifact).hexdigest(),
            "verification_evidence_ref": "https://osf.io/abcd1/",
        }
        fetcher = lambda url, timeout: attestation["artifact_digest"].encode("ascii")
        self.assertEqual(
            [],
            verify_external_attestation(attestation, artifact, fetcher=fetcher),
        )

        self.assertTrue(
            verify_external_attestation(attestation, b"tampered", fetcher=fetcher)
        )

    def test_drand_round_is_checked_against_external_api(self):
        beacon = {
            "source": "DRAND",
            "round_id": "101",
            "previous_round_id": "100",
            "published_at": "1970-01-01T01:06:40Z",
            "previous_round_published_at": "1970-01-01T01:06:10Z",
            "randomness_hex": "11" * 32,
        }

        def fetcher(url, timeout):
            if url.endswith("/info"):
                return json.dumps({"period": 30, "genesis_time": 1000}).encode("utf-8")
            return json.dumps({
                "round": 101,
                "randomness": "11" * 32,
                "signature": "22" * 48,
            }).encode("utf-8")

        self.assertEqual([], verify_drand_beacon(beacon, fetcher=fetcher))

        def wrong(url, timeout):
            if url.endswith("/info"):
                return json.dumps({"period": 30, "genesis_time": 1000}).encode("utf-8")
            return json.dumps({
                "round": 101,
                "randomness": "ff" * 32,
            }).encode("utf-8")

        self.assertTrue(verify_drand_beacon(beacon, fetcher=wrong))

    def test_drand_forged_previous_round_time_is_rejected(self):
        beacon = {
            "source": "DRAND",
            "round_id": "101",
            "previous_round_id": "100",
            "published_at": "1970-01-01T01:06:40Z",
            "previous_round_published_at": "1970-01-01T00:00:00Z",
            "randomness_hex": "11" * 32,
        }

        def fetcher(url, timeout):
            if url.endswith("/info"):
                return json.dumps({"period": 30, "genesis_time": 1000}).encode("utf-8")
            return json.dumps({"round": 101, "randomness": "11" * 32}).encode("utf-8")

        errors = verify_drand_beacon(beacon, fetcher=fetcher)
        self.assertTrue(any("previous_round_published_at" in e for e in errors))

    def test_unsupported_beacon_source_fails_closed(self):
        self.assertTrue(verify_drand_beacon({
            "source": "NIST_RANDOMNESS_BEACON",
            "round_id": "1",
            "randomness_hex": "00" * 32,
        }))


if __name__ == "__main__":
    unittest.main()
