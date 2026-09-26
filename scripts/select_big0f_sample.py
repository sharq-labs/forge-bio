from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from scripts.scientific_invariants import validate_external_seal

ROOT = Path(__file__).resolve().parents[1]
BEACON_SCHEMA = ROOT / "schemas" / "randomness-beacon.v1.schema.json"
ATTESTATION_SCHEMA = ROOT / "schemas" / "external-seal-attestation.v1.schema.json"
DOMAIN = b"forge-bio-big0f-sampling-v1\0"


def _reject_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON constant prohibited: {value}")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"), parse_constant=_reject_constant)


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def _ts(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _validate(instance: dict[str, Any], schema_path: Path) -> None:
    schema = load_json(schema_path)
    Draft202012Validator.check_schema(schema)
    errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(instance))
    if errors:
        raise ValueError("schema validation failed: " + " | ".join(e.message for e in errors))


def validate_frame_seal(
    *,
    frame_digest: str,
    beacon: dict[str, Any],
    frame_seal_attestation: dict[str, Any],
    frame_seal_attestation_digest: str,
) -> None:
    _validate(frame_seal_attestation, ATTESTATION_SCHEMA)
    semantic = validate_external_seal(frame_seal_attestation)
    if semantic:
        raise ValueError("invalid frame-seal attestation: " + " | ".join(semantic))
    if frame_seal_attestation["artifact_type"] != "BIG0F_DISEASE_FRAME":
        raise ValueError("frame seal must target BIG0F_DISEASE_FRAME")
    if frame_seal_attestation["authority_type"] not in {"THIRD_PARTY_TIMESTAMP_SERVICE", "PUBLIC_REGISTRY"}:
        raise ValueError("frame seal must be third-party timestamp/public registry evidence")
    if frame_seal_attestation["artifact_digest"] != frame_digest:
        raise ValueError("frame-seal artifact digest does not match disease-frame digest")
    if beacon["frame_seal_attestation_id"] != frame_seal_attestation["attestation_id"]:
        raise ValueError("beacon frame-seal attestation ID mismatch")
    if beacon["frame_seal_attestation_digest"] != frame_seal_attestation_digest:
        raise ValueError("beacon frame-seal attestation digest mismatch")
    if beacon["frame_sealed_at"] != frame_seal_attestation["sealed_at"]:
        raise ValueError("beacon frame_sealed_at must equal externally attested seal time")


def derive_sampling_key(frame_digest: str, randomness_hex: str) -> bytes:
    return hashlib.sha256(DOMAIN + frame_digest.encode("ascii") + bytes.fromhex(randomness_hex)).digest()


def deterministic_order(disease_ids: list[str], key: bytes) -> list[str]:
    if len(disease_ids) != len(set(disease_ids)):
        raise ValueError("disease frame contains duplicate IDs")
    return sorted(
        disease_ids,
        key=lambda disease_id: hashlib.sha256(key + b"\0" + disease_id.encode("utf-8")).digest(),
    )


def deterministic_event_sample(
    event_records: list[dict[str, str]],
    key: bytes,
    *,
    cap: int = 150,
) -> list[str]:
    """Deterministically cap events while preserving every event-bearing disease.

    The input event universe is immutable. When it exceeds the cap, one event
    per disease is selected first using the sealed sampling key, then remaining
    slots are filled by the same keyed hash order across all remaining events.
    """
    if cap < 1:
        raise ValueError("cap must be positive")
    seen_ids: set[str] = set()
    by_disease: dict[str, list[str]] = {}
    for record in event_records:
        event_id = record.get("event_id")
        disease_id = record.get("disease_id")
        if not isinstance(event_id, str) or not event_id:
            raise ValueError("event_id must be a non-empty string")
        if not isinstance(disease_id, str) or not disease_id:
            raise ValueError("disease_id must be a non-empty string")
        if event_id in seen_ids:
            raise ValueError(f"duplicate event_id: {event_id}")
        seen_ids.add(event_id)
        by_disease.setdefault(disease_id, []).append(event_id)

    def event_key(event_id: str) -> bytes:
        return hashlib.sha256(key + b"\\0event\\0" + event_id.encode("utf-8")).digest()

    all_ids = sorted(seen_ids, key=event_key)
    if len(all_ids) <= cap:
        return all_ids
    if len(by_disease) > cap:
        raise ValueError("event cap is smaller than the number of event-bearing diseases")

    selected: list[str] = []
    selected_set: set[str] = set()
    for disease_id in sorted(by_disease):
        first = min(by_disease[disease_id], key=event_key)
        selected.append(first)
        selected_set.add(first)

    remaining = [event_id for event_id in all_ids if event_id not in selected_set]
    selected.extend(remaining[: cap - len(selected)])
    return sorted(selected, key=event_key)

def select(
    disease_ids: list[str],
    beacon: dict[str, Any],
    frame_digest: str,
    *,
    frame_seal_attestation: dict[str, Any],
    frame_seal_attestation_digest: str,
    target_n: int = 15,
) -> list[str]:
    _validate(beacon, BEACON_SCHEMA)
    if beacon["frame_digest"] != frame_digest:
        raise ValueError("beacon artifact is not bound to this disease-frame digest")
    validate_frame_seal(
        frame_digest=frame_digest,
        beacon=beacon,
        frame_seal_attestation=frame_seal_attestation,
        frame_seal_attestation_digest=frame_seal_attestation_digest,
    )
    frame_sealed = _ts(frame_seal_attestation["sealed_at"])
    if beacon["selection_rule"] != "FIRST_VERIFIED_ROUND_AFTER_FRAME_SEAL":
        raise ValueError("BIG 0F requires the first verified beacon round after frame sealing")
    if _ts(beacon["published_at"]) <= frame_sealed:
        raise ValueError("randomness beacon must be published after the externally verified disease-frame seal")
    if _ts(beacon["previous_round_published_at"]) > frame_sealed:
        raise ValueError("selected beacon is not the first verified round after the frame seal")
    if target_n < 1 or target_n > len(disease_ids):
        raise ValueError("invalid target_n")
    key = derive_sampling_key(frame_digest, beacon["randomness_hex"])
    return deterministic_order(disease_ids, key)[:target_n]


def main() -> int:
    ap = argparse.ArgumentParser(description="Deterministically select BIG 0F diseases from post-seal public randomness")
    ap.add_argument("--frame", type=Path, required=True, help="JSON array of disease IDs")
    ap.add_argument("--frame-seal-attestation", type=Path, required=True)
    ap.add_argument("--beacon", type=Path, required=True)
    ap.add_argument("--target-n", type=int, default=15)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()

    disease_ids = load_json(args.frame)
    if not isinstance(disease_ids, list) or not all(isinstance(x, str) and x for x in disease_ids):
        raise ValueError("disease frame must be a JSON array of non-empty string IDs")
    frame_digest = sha256_file(args.frame)
    beacon = load_json(args.beacon)
    frame_seal = load_json(args.frame_seal_attestation)
    selected = select(
        disease_ids,
        beacon,
        frame_digest,
        frame_seal_attestation=frame_seal,
        frame_seal_attestation_digest=sha256_file(args.frame_seal_attestation),
        target_n=args.target_n,
    )
    payload = {
        "frame_digest": frame_digest,
        "frame_seal_attestation_id": frame_seal["attestation_id"],
        "frame_seal_attestation_digest": sha256_file(args.frame_seal_attestation),
        "beacon_id": beacon["beacon_id"],
        "selected_order": selected,
    }
    args.output.write_text(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
