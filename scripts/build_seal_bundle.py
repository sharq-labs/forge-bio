from __future__ import annotations

import argparse
import hashlib
import json
import unicodedata
from datetime import datetime
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from scripts.select_big0f_sample import derive_sampling_key


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "seal-bundle-manifest.v1.schema.json"
ATTESTATION_SCHEMA_PATH = ROOT / "schemas" / "external-seal-attestation.v1.schema.json"
BEACON_SCHEMA_PATH = ROOT / "schemas" / "randomness-beacon.v1.schema.json"


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


def manifest_digest(manifest: dict[str, Any]) -> str:
    return sha256_bytes(canonical_json_bytes(manifest))


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"), parse_constant=lambda v: (_ for _ in ()).throw(ValueError(f"non-finite JSON constant: {v}")))


def _validate(instance: dict[str, Any], schema_path: Path) -> list[str]:
    schema = _load_json(schema_path)
    Draft202012Validator.check_schema(schema)
    errors = sorted(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(instance),
        key=lambda err: list(err.absolute_path),
    )
    return [
        f"{'.'.join(str(p) for p in e.absolute_path) or '<root>'}: {e.message}"
        for e in errors
    ]


def build_manifest(
    *,
    protocol_path: Path,
    disease_frame_path: Path,
    randomness_beacon_path: Path,
    threshold_manifest_path: Path,
    adjudication_policy_path: Path,
    nuisance_manifest_path: Path,
    decision_engine_path: Path,
    pilot_result_schema_path: Path,
    sampling_code_path: Path,
    threshold_manifest_schema_path: Path,
    adjudication_policy_schema_path: Path,
    nuisance_manifest_schema_path: Path,
    power_analysis_schema_path: Path,
    created_at: str,
    created_by_role: str,
) -> dict[str, Any]:
    frame_digest = sha256_file(disease_frame_path)
    beacon = _load_json(randomness_beacon_path)
    beacon_errors = _validate(beacon, BEACON_SCHEMA_PATH)
    if beacon_errors:
        raise ValueError("invalid randomness beacon artifact: " + " | ".join(beacon_errors))
    if beacon["frame_digest"] != frame_digest:
        raise ValueError("randomness beacon artifact is not bound to the sealed disease frame")
    published = datetime.fromisoformat(beacon["published_at"].replace("Z", "+00:00"))
    frame_sealed = datetime.fromisoformat(beacon["frame_sealed_at"].replace("Z", "+00:00"))
    if published <= frame_sealed:
        raise ValueError("randomness beacon must be published after the frame seal")
    key = derive_sampling_key(frame_digest, beacon["randomness_hex"])
    return {
        "seal_bundle_version": "big0f-seal-bundle-v2",
        "created_at": created_at,
        "created_by_role": created_by_role,
        "protocol_version": "BIG-0F-v0",
        "protocol_sha256": sha256_file(protocol_path),
        "disease_frame_sha256": frame_digest,
        "randomness_beacon_id": beacon["beacon_id"],
        "randomness_beacon_sha256": sha256_file(randomness_beacon_path),
        "derived_sampling_key_commitment_sha256": sha256_bytes(key),
        "candidate_cutoff_order": ["2005-12-31", "2008-12-31", "2011-12-31", "2014-12-31"],
        "candidate_horizon_order": ["3y", "5y", "7y", "10y"],
        "sampling_algorithm_version": "external-beacon-hash-sort-v1",
        "threshold_manifest_sha256": sha256_file(threshold_manifest_path),
        "adjudication_policy_sha256": sha256_file(adjudication_policy_path),
        "nuisance_feature_manifest_sha256": sha256_file(nuisance_manifest_path),
        "decision_engine_sha256": sha256_file(decision_engine_path),
        "pilot_result_schema_sha256": sha256_file(pilot_result_schema_path),
        "sampling_code_sha256": sha256_file(sampling_code_path),
        "threshold_manifest_schema_sha256": sha256_file(threshold_manifest_schema_path),
        "adjudication_policy_schema_sha256": sha256_file(adjudication_policy_schema_path),
        "nuisance_manifest_schema_sha256": sha256_file(nuisance_manifest_schema_path),
        "power_analysis_schema_sha256": sha256_file(power_analysis_schema_path),
    }


def verify_manifest(
    manifest: dict[str, Any],
    *,
    attestation: dict[str, Any],
    component_paths: dict[str, Path],
) -> list[str]:
    errors = _validate(manifest, SCHEMA_PATH)
    errors.extend(f"attestation {e}" for e in _validate(attestation, ATTESTATION_SCHEMA_PATH))

    actual_digest = manifest_digest(manifest)
    if attestation.get("verification_status") != "VERIFIED":
        errors.append("external attestation is not VERIFIED")
    if attestation.get("artifact_digest") != actual_digest:
        errors.append(
            f"manifest digest does not match externally attested digest: {attestation.get('artifact_digest')!r} != {actual_digest!r}"
        )

    checks = {
        "protocol_sha256": sha256_file(component_paths["protocol"]),
        "disease_frame_sha256": sha256_file(component_paths["disease_frame"]),
        "randomness_beacon_sha256": sha256_file(component_paths["randomness_beacon"]),
        "threshold_manifest_sha256": sha256_file(component_paths["threshold_manifest"]),
        "adjudication_policy_sha256": sha256_file(component_paths["adjudication_policy"]),
        "nuisance_feature_manifest_sha256": sha256_file(component_paths["nuisance_manifest"]),
        "decision_engine_sha256": sha256_file(component_paths["decision_engine"]),
        "pilot_result_schema_sha256": sha256_file(component_paths["pilot_result_schema"]),
        "sampling_code_sha256": sha256_file(component_paths["sampling_code"]),
        "threshold_manifest_schema_sha256": sha256_file(component_paths["threshold_manifest_schema"]),
        "adjudication_policy_schema_sha256": sha256_file(component_paths["adjudication_policy_schema"]),
        "nuisance_manifest_schema_sha256": sha256_file(component_paths["nuisance_manifest_schema"]),
        "power_analysis_schema_sha256": sha256_file(component_paths["power_analysis_schema"]),
    }
    for key, actual in checks.items():
        if manifest.get(key) != actual:
            errors.append(f"{key} mismatch: manifest={manifest.get(key)!r}, actual={actual!r}")

    beacon = _load_json(component_paths["randomness_beacon"])
    frame_digest = checks["disease_frame_sha256"]
    if beacon.get("frame_digest") != frame_digest:
        errors.append("randomness beacon is not bound to the current disease frame")
    try:
        key = derive_sampling_key(frame_digest, beacon["randomness_hex"])
        if manifest.get("derived_sampling_key_commitment_sha256") != sha256_bytes(key):
            errors.append("derived sampling-key commitment mismatch")
    except Exception as exc:
        errors.append(f"cannot derive sampling key: {exc}")

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
    ap.add_argument("--randomness-beacon", type=_path, required=True)
    ap.add_argument("--threshold-manifest", type=_path, required=True)
    ap.add_argument("--adjudication-policy", type=_path, required=True)
    ap.add_argument("--nuisance-manifest", type=_path, required=True)
    ap.add_argument("--decision-engine", type=_path, default=ROOT / "scripts" / "evaluate_big0f.py")
    ap.add_argument("--pilot-result-schema", type=_path, default=ROOT / "schemas" / "big0f-pilot-result.v1.schema.json")
    ap.add_argument("--sampling-code", type=_path, default=ROOT / "scripts" / "select_big0f_sample.py")
    ap.add_argument("--threshold-manifest-schema", type=_path, default=ROOT / "schemas" / "big0f-threshold-manifest.v1.schema.json")
    ap.add_argument("--adjudication-policy-schema", type=_path, default=ROOT / "schemas" / "big0f-adjudication-policy.v1.schema.json")
    ap.add_argument("--nuisance-manifest-schema", type=_path, default=ROOT / "schemas" / "big0f-nuisance-manifest.v1.schema.json")
    ap.add_argument("--power-analysis-schema", type=_path, default=ROOT / "schemas" / "big0f-power-analysis.v1.schema.json")
    ap.add_argument("--created-at", required=True)
    ap.add_argument("--created-by-role", choices=["INDEPENDENT_CUSTODIAN", "PREREGISTRATION_OPERATOR"], required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--attestation-record", type=_path)
    args = ap.parse_args()

    component_paths = {
        "protocol": args.protocol,
        "disease_frame": args.disease_frame,
        "randomness_beacon": args.randomness_beacon,
        "threshold_manifest": args.threshold_manifest,
        "adjudication_policy": args.adjudication_policy,
        "nuisance_manifest": args.nuisance_manifest,
        "decision_engine": args.decision_engine,
        "pilot_result_schema": args.pilot_result_schema,
        "sampling_code": args.sampling_code,
        "threshold_manifest_schema": args.threshold_manifest_schema,
        "adjudication_policy_schema": args.adjudication_policy_schema,
        "nuisance_manifest_schema": args.nuisance_manifest_schema,
        "power_analysis_schema": args.power_analysis_schema,
    }

    if args.verify:
        if args.attestation_record is None:
            ap.error("--attestation-record is required with --verify")
        manifest = _load_json(args.output)
        attestation = _load_json(args.attestation_record)
        errors = verify_manifest(manifest, attestation=attestation, component_paths=component_paths)
        if errors:
            for err in errors:
                print(err)
            return 1
        print(manifest_digest(manifest))
        return 0

    manifest = build_manifest(
        protocol_path=args.protocol,
        disease_frame_path=args.disease_frame,
        randomness_beacon_path=args.randomness_beacon,
        threshold_manifest_path=args.threshold_manifest,
        adjudication_policy_path=args.adjudication_policy,
        nuisance_manifest_path=args.nuisance_manifest,
        decision_engine_path=args.decision_engine,
        pilot_result_schema_path=args.pilot_result_schema,
        sampling_code_path=args.sampling_code,
        threshold_manifest_schema_path=args.threshold_manifest_schema,
        adjudication_policy_schema_path=args.adjudication_policy_schema,
        nuisance_manifest_schema_path=args.nuisance_manifest_schema,
        power_analysis_schema_path=args.power_analysis_schema,
        created_at=args.created_at,
        created_by_role=args.created_by_role,
    )
    errors = _validate(manifest, SCHEMA_PATH)
    if errors:
        raise ValueError("generated manifest violates schema: " + " | ".join(errors))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(canonical_json_bytes(manifest) + b"\n")
    print(manifest_digest(manifest))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
