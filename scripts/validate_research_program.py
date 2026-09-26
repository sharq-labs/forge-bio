from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from scripts.scientific_invariants import (
    validate_confirmatory_program_budget,
    validate_research_program_attempt,
    validate_research_program_ledger,
)

ROOT = Path(__file__).resolve().parents[1]
BUDGET_SCHEMA = ROOT / "schemas" / "confirmatory-program-budget.v1.schema.json"
ATTEMPT_SCHEMA = ROOT / "schemas" / "research-program-attempt.v1.schema.json"
LEDGER_SCHEMA = ROOT / "schemas" / "research-program-ledger.v1.schema.json"


def _reject_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON constant prohibited: {value}")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"), parse_constant=_reject_constant)


def _validate_schema(instance: Any, schema_path: Path) -> list[str]:
    schema = load_json(schema_path)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [
        f"{'.'.join(str(x) for x in err.absolute_path) or '<root>'}: {err.message}"
        for err in validator.iter_errors(instance)
    ]


def canonical_digest(payload: dict[str, Any]) -> str:
    body = dict(payload)
    body.pop("digest", None)
    encoded = json.dumps(body, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def validate_ledger_chain(
    current: dict[str, Any],
    previous: dict[str, Any] | None,
) -> list[str]:
    errors: list[str] = []
    errors.extend(f"current ledger: {e}" for e in _validate_schema(current, LEDGER_SCHEMA))
    errors.extend(f"current ledger: {e}" for e in validate_research_program_ledger(current))
    if errors:
        return errors

    if current.get("digest") != canonical_digest(current):
        errors.append("current ledger canonical digest mismatch")

    sequence = current["ledger_sequence"]
    if sequence == 0:
        if previous is not None:
            errors.append("genesis ledger cannot declare a previous ledger")
        return errors

    if previous is None:
        errors.append("non-genesis ledger requires the immediately previous ledger artifact")
        return errors

    errors.extend(f"previous ledger: {e}" for e in _validate_schema(previous, LEDGER_SCHEMA))
    errors.extend(f"previous ledger: {e}" for e in validate_research_program_ledger(previous))
    if errors:
        return errors
    if previous.get("digest") != canonical_digest(previous):
        errors.append("previous ledger canonical digest mismatch")
        return errors

    if sequence != previous["ledger_sequence"] + 1:
        errors.append("ledger_sequence must increment exactly by one")
    if current["previous_ledger_digest"] != previous["digest"]:
        errors.append("previous_ledger_digest does not match the supplied previous ledger")

    previous_attempts = previous.get("attempts") or []
    current_attempts = current.get("attempts") or []
    if len(current_attempts) < len(previous_attempts):
        errors.append("research-program ledger is not append-only: prior attempts were removed")
    elif current_attempts[: len(previous_attempts)] != previous_attempts:
        errors.append("research-program ledger is not append-only: prior attempts were modified or reordered")

    return errors


def validate_program(budget: dict[str, Any], attempts: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    errors.extend(f"budget: {e}" for e in _validate_schema(budget, BUDGET_SCHEMA))
    errors.extend(f"budget: {e}" for e in validate_confirmatory_program_budget(budget))

    for i, attempt in enumerate(attempts):
        errors.extend(f"attempt[{i}]: {e}" for e in _validate_schema(attempt, ATTEMPT_SCHEMA))
        errors.extend(f"attempt[{i}]: {e}" for e in validate_research_program_attempt(attempt))

    if errors:
        return errors

    attempt_ids = [a["attempt_id"] for a in attempts]
    if len(attempt_ids) != len(set(attempt_ids)):
        errors.append("attempt IDs must be unique")

    indices = [a.get("attempt_index") for a in attempts if a.get("attempt_index") is not None]
    if len(indices) != len(set(indices)):
        errors.append("attempt_index values must be unique")
    if indices and sorted(indices) != list(range(1, max(indices) + 1)):
        errors.append("attempt_index values must be contiguous from 1")

    allocations = {a["generation_id"]: a for a in budget["generation_allocations"]}
    used_confirmatory_generations: dict[str, str] = {}
    for attempt in attempts:
        if attempt["attempt_tier"] not in {"CONFIRMATORY", "PROSPECTIVE"}:
            continue
        gid = attempt["allocation_generation_id"]
        if gid not in allocations:
            errors.append(f"attempt {attempt['attempt_id']} references unknown generation {gid}")
            continue
        allocation = allocations[gid]
        if abs(float(attempt["allocated_alpha"]) - float(allocation["allocated_alpha"])) > 1e-12:
            errors.append(f"attempt {attempt['attempt_id']} allocated alpha does not match budget generation {gid}")
        prior = used_confirmatory_generations.get(gid)
        if prior is not None and prior != attempt["attempt_id"]:
            errors.append(f"confirmatory generation {gid} is reused by attempts {prior} and {attempt['attempt_id']}")
        used_confirmatory_generations[gid] = attempt["attempt_id"]

    confirmatory_attempts = [
        a for a in attempts if a["attempt_tier"] in {"CONFIRMATORY", "PROSPECTIVE"}
    ]
    if len(confirmatory_attempts) > budget["max_confirmatory_generations"]:
        errors.append("confirmatory attempts exceed the single program-wide generation budget")

    return errors


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate Forge Bio research-program multiplicity and append-only history")
    ap.add_argument("--budget", type=Path)
    ap.add_argument("--attempts", type=Path, help="JSON array of ResearchProgramAttempt artifacts")
    ap.add_argument("--ledger", type=Path, help="current ResearchProgramLedger artifact")
    ap.add_argument("--previous-ledger", type=Path, help="immediately previous ledger artifact")
    args = ap.parse_args()

    if args.ledger is not None:
        current = load_json(args.ledger)
        previous = load_json(args.previous_ledger) if args.previous_ledger is not None else None
        errors = validate_ledger_chain(current, previous)
        if errors:
            for err in errors:
                print(err)
            return 1
        print("research-program append-only ledger validation passed")
        return 0

    if args.budget is None or args.attempts is None:
        ap.error("provide --ledger [--previous-ledger] or both --budget and --attempts")

    budget = load_json(args.budget)
    attempts = load_json(args.attempts)
    if not isinstance(attempts, list):
        raise ValueError("--attempts must contain a JSON array")

    errors = validate_program(budget, attempts)
    if errors:
        for err in errors:
            print(err)
        return 1
    print("research-program multiplicity validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
