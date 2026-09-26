from __future__ import annotations

import argparse
import hashlib
import json
import unicodedata
from pathlib import Path
from typing import Any


DOMAIN = b"forge-bio-big0f-seed-v1\0"


def canonical_json_bytes(obj: Any) -> bytes:
    def normalize(v: Any) -> Any:
        if isinstance(v, str):
            return unicodedata.normalize("NFC", v)
        if isinstance(v, list):
            return [normalize(x) for x in v]
        if isinstance(v, dict):
            return {str(k): normalize(v[k]) for k in sorted(v)}
        return v

    normalized = normalize(obj)
    text = json.dumps(
        normalized,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )
    return text.encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def seed_commitment(seed_hex: str) -> str:
    raw = bytes.fromhex(seed_hex)
    if len(raw) != 32:
        raise ValueError("seed must be exactly 32 bytes / 64 hex chars")
    return sha256_bytes(DOMAIN + raw)


def build_manifest(
    *,
    protocol_path: Path,
    disease_frame_path: Path,
    threshold_manifest_path: Path,
    adjudication_policy_path: Path,
    nuisance_manifest_path: Path,
    seed_hex: str,
    protocol_version: str,
    sampling_algorithm_version: str,
) -> dict[str, Any]:
    return {
        "seal_bundle_version": "big0f-seal-bundle-v1",
        "protocol_version": protocol_version,
        "protocol_sha256": sha256_file(protocol_path),
        "disease_frame_sha256": sha256_file(disease_frame_path),
        "random_seed_commitment_sha256": seed_commitment(seed_hex),
        "candidate_cutoff_order": [
            "2005-12-31",
            "2008-12-31",
            "2011-12-31",
            "2014-12-31",
        ],
        "candidate_horizon_order": ["3y", "5y", "7y", "10y"],
        "sampling_algorithm_version": sampling_algorithm_version,
        "threshold_manifest_sha256": sha256_file(threshold_manifest_path),
        "adjudication_policy_sha256": sha256_file(adjudication_policy_path),
        "nuisance_feature_manifest_sha256": sha256_file(nuisance_manifest_path),
    }


def manifest_digest(manifest: dict[str, Any]) -> str:
    return sha256_bytes(canonical_json_bytes(manifest))


def verify_manifest(
    manifest: dict[str, Any],
    *,
    protocol_path: Path,
    disease_frame_path: Path,
    threshold_manifest_path: Path,
    adjudication_policy_path: Path,
    nuisance_manifest_path: Path,
    seed_hex: str,
) -> list[str]:
    errors: list[str] = []

    checks = {
        "protocol_sha256": sha256_file(protocol_path),
        "disease_frame_sha256": sha256_file(disease_frame_path),
        "random_seed_commitment_sha256": seed_commitment(seed_hex),
        "threshold_manifest_sha256": sha256_file(threshold_manifest_path),
        "adjudication_policy_sha256": sha256_file(adjudication_policy_path),
        "nuisance_feature_manifest_sha256": sha256_file(nuisance_manifest_path),
    }

    for key, actual in checks.items():
        expected = manifest.get(key)
        if expected != actual:
            errors.append(f"{key} mismatch: expected {expected!r}, got {actual!r}")

    if manifest.get("candidate_cutoff_order") != [
        "2005-12-31",
        "2008-12-31",
        "2011-12-31",
        "2014-12-31",
    ]:
        errors.append("candidate_cutoff_order differs from frozen BIG 0F protocol")

    if manifest.get("candidate_horizon_order") != ["3y", "5y", "7y", "10y"]:
        errors.append("candidate_horizon_order differs from frozen BIG 0F protocol")

    return errors


def _path(value: str) -> Path:
    p = Path(value)
    if not p.exists():
        raise argparse.ArgumentTypeError(f"file does not exist: {value}")
    return p


def main() -> int:
    ap = argparse.ArgumentParser(description="Build/verify Forge Bio BIG 0F seal bundle")
    ap.add_argument("--protocol", type=_path, required=True)
    ap.add_argument("--disease-frame", type=_path, required=True)
    ap.add_argument("--threshold-manifest", type=_path, required=True)
    ap.add_argument("--adjudication-policy", type=_path, required=True)
    ap.add_argument("--nuisance-manifest", type=_path, required=True)
    ap.add_argument("--seed-hex", required=True)
    ap.add_argument("--protocol-version", default="BIG-0F-v0")
    ap.add_argument("--sampling-algorithm-version", default="seeded-permutation-v1")
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--verify", action="store_true")
    args = ap.parse_args()

    if args.verify:
        manifest = json.loads(args.output.read_text(encoding="utf-8"))
        errors = verify_manifest(
            manifest,
            protocol_path=args.protocol,
            disease_frame_path=args.disease_frame,
            threshold_manifest_path=args.threshold_manifest,
            adjudication_policy_path=args.adjudication_policy,
            nuisance_manifest_path=args.nuisance_manifest,
            seed_hex=args.seed_hex,
        )
        if errors:
            for e in errors:
                print(e)
            return 1
        print(manifest_digest(manifest))
        return 0

    manifest = build_manifest(
        protocol_path=args.protocol,
        disease_frame_path=args.disease_frame,
        threshold_manifest_path=args.threshold_manifest,
        adjudication_policy_path=args.adjudication_policy,
        nuisance_manifest_path=args.nuisance_manifest,
        seed_hex=args.seed_hex,
        protocol_version=args.protocol_version,
        sampling_algorithm_version=args.sampling_algorithm_version,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(canonical_json_bytes(manifest) + b"\n")
    print(manifest_digest(manifest))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
