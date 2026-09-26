from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tempfile
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Callable


OSF_HOSTS = {"osf.io", "api.osf.io"}
DRAND_API = "https://api.drand.sh/public/{round_id}"


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def _fetch_bytes(
    url: str,
    *,
    fetcher: Callable[..., Any] | None = None,
    timeout: float = 30.0,
) -> bytes:
    fetcher = fetcher or urllib.request.urlopen
    response = fetcher(url, timeout=timeout)
    if isinstance(response, bytes):
        return response
    if hasattr(response, "__enter__"):
        with response as opened:
            return opened.read()
    try:
        return response.read()
    finally:
        close = getattr(response, "close", None)
        if callable(close):
            close()


def verify_ots_bytes(
    artifact_bytes: bytes,
    proof_path: Path | None,
    *,
    runner: Callable[..., Any] | None = None,
) -> list[str]:
    if proof_path is None:
        return ["OpenTimestamps verification requires a proof file"]
    if not proof_path.exists():
        return [f"OpenTimestamps proof does not exist: {proof_path}"]

    runner = runner or subprocess.run
    with tempfile.TemporaryDirectory(prefix="forge-bio-ots-") as tmp:
        target = Path(tmp) / "artifact.bin"
        proof = Path(tmp) / "artifact.bin.ots"
        target.write_bytes(artifact_bytes)
        shutil.copyfile(proof_path, proof)
        try:
            result = runner(
                ["ots", "verify", str(proof)],
                capture_output=True,
                text=True,
                timeout=120,
                check=False,
            )
        except FileNotFoundError:
            return ["OpenTimestamps client 'ots' is not installed; verification fails closed"]
        except Exception as exc:
            return [f"OpenTimestamps verification could not execute: {exc}"]

    output = f"{getattr(result, 'stdout', '')}\n{getattr(result, 'stderr', '')}"
    if getattr(result, "returncode", 1) != 0:
        return [f"OpenTimestamps proof verification failed: {output.strip()}"]
    if "Success!" not in output:
        return ["OpenTimestamps client returned success status without a verified timestamp result"]
    return []


def verify_osf_registry(
    attestation: dict[str, Any],
    *,
    fetcher: Callable[..., Any] | None = None,
) -> list[str]:
    evidence_url = attestation.get("verification_evidence_ref")
    if not isinstance(evidence_url, str):
        return ["public-registry verification evidence must be an HTTPS OSF URL"]
    parsed = urllib.parse.urlparse(evidence_url)
    if parsed.scheme != "https" or parsed.hostname not in OSF_HOSTS:
        return ["BIG 0F public-registry evidence must resolve through an approved OSF host"]

    try:
        body = _fetch_bytes(evidence_url, fetcher=fetcher)
    except Exception as exc:
        return [f"could not fetch public-registry evidence: {exc}"]

    digest = attestation.get("artifact_digest")
    if not isinstance(digest, str) or digest.encode("ascii", errors="ignore") not in body:
        return ["OSF registry evidence does not contain the exact committed artifact digest"]
    return []


def verify_external_attestation(
    attestation: dict[str, Any],
    artifact_bytes: bytes,
    *,
    ots_proof_path: Path | None = None,
    runner: Callable[..., Any] | None = None,
    fetcher: Callable[..., Any] | None = None,
) -> list[str]:
    errors: list[str] = []
    actual_digest = sha256_bytes(artifact_bytes)
    if attestation.get("artifact_digest") != actual_digest:
        errors.append(
            "external attestation artifact digest does not match the exact artifact bytes "
            f"({attestation.get('artifact_digest')!r} != {actual_digest!r})"
        )
        return errors

    authority = attestation.get("authority_type")
    if authority == "THIRD_PARTY_TIMESTAMP_SERVICE":
        errors.extend(verify_ots_bytes(artifact_bytes, ots_proof_path, runner=runner))
    elif authority == "PUBLIC_REGISTRY":
        errors.extend(verify_osf_registry(attestation, fetcher=fetcher))
    else:
        errors.append("BIG 0F external verification only accepts timestamp service or public registry")
    return errors


def verify_drand_beacon(
    beacon: dict[str, Any],
    *,
    fetcher: Callable[..., Any] | None = None,
) -> list[str]:
    if beacon.get("source") != "DRAND":
        return ["BIG 0F V0 machine verification currently requires DRAND; unsupported beacon source fails closed"]

    round_id = str(beacon.get("round_id", ""))
    if not round_id.isdigit():
        return ["DRAND round_id must be an integer string"]
    url = DRAND_API.format(round_id=round_id)
    try:
        raw = _fetch_bytes(url, fetcher=fetcher)
        external = json.loads(raw.decode("utf-8"))
    except Exception as exc:
        return [f"could not fetch/parse DRAND round {round_id}: {exc}"]

    errors: list[str] = []
    if str(external.get("round")) != round_id:
        errors.append("DRAND API round does not match beacon round_id")
    expected_randomness = str(beacon.get("randomness_hex", "")).lower()
    actual_randomness = str(external.get("randomness", "")).lower()
    if actual_randomness != expected_randomness:
        errors.append("DRAND API randomness does not match sealed beacon artifact")
    if len(actual_randomness) != 64:
        errors.append("DRAND API randomness is not a 32-byte hex value")
    return errors
