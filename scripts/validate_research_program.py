from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from scripts.scientific_invariants import (
    validate_confirmatory_program_budget,
    validate_research_program_attempt,
)

ROOT = Path(__file__).resolve().parents[1]
BUDGET_SCHEMA = ROOT / "schemas" / "confirmatory-program-budget.v1.schema.json"
ATTEMPT_SCHEMA = ROOT / "schemas" / "research-program-attempt.v1.schema.json"


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
    ap = argparse.ArgumentParser(description="Validate Forge Bio research-program attempts against one canonical alpha budget")
    ap.add_argument("--budget", type=Path, required=True)
    ap.add_argument("--attempts", type=Path, required=True, help="JSON array of ResearchProgramAttempt artifacts")
    args = ap.parse_args()

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
