from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
RULE_SCHEMA = ROOT / "schemas" / "endpoint-quality-rule.v1.schema.json"

PRIMARY_ASSIGNMENT_CLASSES = {
    "HYPOTHESIS_FREE_CODING_OR_LOF",
    "HIGH_CONFIDENCE_FINE_MAPPING",
    "PREREGISTERED_COLOCALIZATION",
}

FIELD_REGISTRY: dict[str, dict[str, Any]] = {
    "study_design_class": {
        "dimension": "STUDY_DESIGN",
        "operators": {"IN"},
        "allowed_values": {"GENOME_WIDE", "EXOME_WIDE", "BIOBANK_WIDE"},
    },
    "p_value": {
        "dimension": "STATISTICAL_STRENGTH",
        "operators": {"LT", "LE"},
        "numeric_range": (0.0, 1.0),
    },
    "sample_size": {
        "dimension": "SAMPLE_SIZE",
        "operators": {"GT", "GE"},
        "numeric_range": (1.0, None),
    },
    "independence_state": {
        "dimension": "INDEPENDENCE",
        "operators": {"IN", "EQ"},
        "allowed_values": {"INDEPENDENT"},
    },
    "phenotype_relation": {
        "dimension": "PHENOTYPE_MATCH",
        "operators": {"IN", "EQ"},
        "allowed_values": {"EXACT", "SAME_CONCEPT_DIFFERENT_DEFINITION"},
    },
    "genomic_harmonization_status": {
        "dimension": "GENOMIC_HARMONIZATION",
        "operators": {"IN", "EQ"},
        "allowed_values": {"PASS", "RESOLVED"},
    },
    "allele_direction_status": {
        "dimension": "ALLELE_DIRECTION",
        "operators": {"IN", "EQ"},
        "allowed_values": {"CONSISTENT", "RESOLVED", "NOT_APPLICABLE"},
    },
    "population_ancestry_status": {
        "dimension": "POPULATION_ANCESTRY",
        "operators": {"IN", "EQ"},
        "allowed_values": {"ADEQUATE", "KNOWN"},
    },
    "gene_assignment_class": {
        "dimension": "GENE_ASSIGNMENT",
        "operators": {"IN", "EQ"},
        "allowed_values": PRIMARY_ASSIGNMENT_CLASSES,
    },
    "pre_t_genetic_state": {
        "dimension": "HISTORICAL_NOVELTY",
        "operators": {"IN", "EQ"},
        "allowed_values": {"NO_SIGNAL_OBSERVED"},
    },
    "source_quality_status": {
        "dimension": "SOURCE_QUALITY",
        "operators": {"IN", "EQ"},
        "allowed_values": {"PRIMARY_SOURCE", "QUALIFIED_INDEPENDENT_SOURCE"},
    },
}

MANDATORY_DIMENSIONS = {spec["dimension"] for spec in FIELD_REGISTRY.values()}


def _reject_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON constant prohibited: {value}")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"), parse_constant=_reject_constant)


def _schema_errors(rule: dict[str, Any]) -> list[str]:
    schema = load_json(RULE_SCHEMA)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [
        f"{'.'.join(str(x) for x in e.absolute_path) or '<root>'}: {e.message}"
        for e in validator.iter_errors(rule)
    ]


def _finite(value: Any) -> bool:
    if isinstance(value, bool):
        return True
    if isinstance(value, (int, float)):
        return math.isfinite(float(value))
    if isinstance(value, list):
        return all(_finite(v) for v in value)
    return True


def validate_rule(rule: dict[str, Any]) -> list[str]:
    errors = _schema_errors(rule)
    if errors:
        return errors

    criteria = rule.get("criteria") or []
    ids = [c["criterion_id"] for c in criteria]
    if len(ids) != len(set(ids)):
        errors.append("criterion_id values must be unique")

    fields = [c["field_or_artifact"] for c in criteria]
    if len(fields) != len(set(fields)):
        errors.append("FROZEN endpoint rule may define each executable field only once")

    observed_dimensions: set[str] = set()
    for c in criteria:
        field = c["field_or_artifact"]
        if field not in FIELD_REGISTRY:
            errors.append(f"unknown/non-executable endpoint field: {field}")
            continue
        spec = FIELD_REGISTRY[field]
        observed_dimensions.add(c["scientific_dimension"])
        if c["scientific_dimension"] != spec["dimension"]:
            errors.append(f"{field} must use scientific dimension {spec['dimension']}")
        if c["operator"] not in spec["operators"]:
            errors.append(f"{field} operator {c['operator']} is not scientifically executable")
        if c.get("required") is not True:
            errors.append(f"{field} must be required in a FROZEN primary endpoint rule")

        value = c.get("value")
        if not _finite(value):
            errors.append(f"{field} contains NaN/Infinity")

        allowed = spec.get("allowed_values")
        if allowed is not None and value is not None:
            values = value if isinstance(value, list) else [value]
            if any(v not in allowed for v in values):
                errors.append(f"{field} includes prohibited/UNKNOWN value")
            if not values:
                errors.append(f"{field} value set cannot be empty")

        numeric_range = spec.get("numeric_range")
        if numeric_range is not None:
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(float(value)):
                errors.append(f"{field} requires a finite numeric operand")
            else:
                low, high = numeric_range
                if low is not None and float(value) < low:
                    errors.append(f"{field} operand below valid range")
                if high is not None and float(value) > high:
                    errors.append(f"{field} operand above valid range")

    if rule.get("status") == "FROZEN":
        missing = sorted(MANDATORY_DIMENSIONS - observed_dimensions)
        if missing:
            errors.append("FROZEN endpoint rule missing mandatory dimensions: " + ",".join(missing))
        if rule.get("endpoint_subtype") == "E1-NOVEL-STRICT":
            by_field = {c["field_or_artifact"]: c for c in criteria}
            study = by_field.get("study_design_class", {})
            vals = set(study.get("value") or [])
            if not vals or not vals.issubset(FIELD_REGISTRY["study_design_class"]["allowed_values"]):
                errors.append("E1-NOVEL-STRICT requires hypothesis-free primary study designs")
            novelty = by_field.get("pre_t_genetic_state", {})
            novelty_vals = novelty.get("value")
            novelty_vals = novelty_vals if isinstance(novelty_vals, list) else [novelty_vals]
            if set(novelty_vals) != {"NO_SIGNAL_OBSERVED"}:
                errors.append("E1-NOVEL-STRICT primary rule requires NO_SIGNAL_OBSERVED pre-T state")

    return errors


def _apply(operator: str, actual: Any, expected: Any) -> bool:
    if actual is None:
        return False
    if operator == "REQUIRE":
        return actual is not None
    if operator == "EQ":
        return actual == expected
    if operator == "NE":
        return actual != expected
    if operator == "GT":
        return actual > expected
    if operator == "GE":
        return actual >= expected
    if operator == "LT":
        return actual < expected
    if operator == "LE":
        return actual <= expected
    if operator == "IN":
        return actual in expected
    if operator == "NOT_IN":
        return actual not in expected
    raise ValueError(f"unsupported operator: {operator}")


def evaluate_rule(rule: dict[str, Any], event: dict[str, Any]) -> tuple[bool, list[str]]:
    errors = validate_rule(rule)
    if errors:
        raise ValueError("endpoint rule is not executable: " + " | ".join(errors))
    failures: list[str] = []
    for c in rule["criteria"]:
        field = c["field_or_artifact"]
        actual = event.get(field)
        if not _finite(actual):
            failures.append(f"{field}: event value is non-finite")
            continue
        if not _apply(c["operator"], actual, c.get("value")):
            failures.append(f"{field}: criterion {c['operator']} {c.get('value')!r} failed for {actual!r}")
    return not failures, failures


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate/execute a frozen BIG 0F endpoint-quality rule")
    ap.add_argument("--rule", type=Path, required=True)
    ap.add_argument("--event", type=Path)
    args = ap.parse_args()

    rule = load_json(args.rule)
    errors = validate_rule(rule)
    if errors:
        for e in errors:
            print(e)
        return 1
    if args.event is None:
        print("endpoint rule validation passed")
        return 0

    event = load_json(args.event)
    passed, failures = evaluate_rule(rule, event)
    print(json.dumps({"qualifies": passed, "failures": failures}, indent=2, allow_nan=False))
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
