from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
BEACON_SCHEMA = ROOT / "schemas" / "randomness-beacon.v1.schema.json"
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


def derive_sampling_key(frame_digest: str, randomness_hex: str) -> bytes:
    return hashlib.sha256(DOMAIN + frame_digest.encode("ascii") + bytes.fromhex(randomness_hex)).digest()


def deterministic_order(disease_ids: list[str], key: bytes) -> list[str]:
    if len(disease_ids) != len(set(disease_ids)):
        raise ValueError("disease frame contains duplicate IDs")
    return sorted(
        disease_ids,
        key=lambda disease_id: hashlib.sha256(key + b"\0" + disease_id.encode("utf-8")).digest(),
    )


def select(disease_ids: list[str], beacon: dict[str, Any], frame_digest: str, target_n: int = 15) -> list[str]:
    schema = load_json(BEACON_SCHEMA)
    Draft202012Validator.check_schema(schema)
    errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(beacon))
    if errors:
        raise ValueError("invalid randomness beacon artifact: " + " | ".join(e.message for e in errors))
    if beacon["frame_digest"] != frame_digest:
        raise ValueError("beacon artifact is not bound to this disease-frame digest")
    frame_sealed = _ts(beacon["frame_sealed_at"])
    if beacon["selection_rule"] != "FIRST_VERIFIED_ROUND_AFTER_FRAME_SEAL":
        raise ValueError("BIG 0F requires the first verified beacon round after frame sealing")
    if _ts(beacon["published_at"]) <= frame_sealed:
        raise ValueError("randomness beacon must be published after the disease frame was externally sealed")
    if _ts(beacon["previous_round_published_at"]) > frame_sealed:
        raise ValueError("selected beacon is not the first verified round after the frame seal")
    if target_n < 1 or target_n > len(disease_ids):
        raise ValueError("invalid target_n")
    key = derive_sampling_key(frame_digest, beacon["randomness_hex"])
    return deterministic_order(disease_ids, key)[:target_n]


def main() -> int:
    ap = argparse.ArgumentParser(description="Deterministically order/select BIG 0F diseases from post-seal public randomness")
    ap.add_argument("--frame", type=Path, required=True, help="JSON array of disease IDs")
    ap.add_argument("--beacon", type=Path, required=True)
    ap.add_argument("--target-n", type=int, default=15)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()

    disease_ids = load_json(args.frame)
    if not isinstance(disease_ids, list) or not all(isinstance(x, str) and x for x in disease_ids):
        raise ValueError("disease frame must be a JSON array of non-empty string IDs")
    frame_digest = sha256_file(args.frame)
    beacon = load_json(args.beacon)
    selected = select(disease_ids, beacon, frame_digest, args.target_n)
    payload = {
        "frame_digest": frame_digest,
        "beacon_id": beacon["beacon_id"],
        "selected_order": selected,
    }
    args.output.write_text(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
