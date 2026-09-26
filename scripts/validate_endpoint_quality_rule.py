from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "endpoint-quality-rule.v1.schema.json"

FIELD_REGISTRY: dict[str, dict[str, Any]] = {
    "study_design_class": {
        "dimension": "STUDY_DESIGN",
        "type": "string",
        "operators": {"IN", "EQ"},
        "allowed_values": {"GENOME_WIDE", "EXOME_WIDE", "BIOBANK_WIDE"},
    },
    "p_value": {
        "dimension": "STATISTICAL_STRENGTH",
        "type": "number",
        "operators": {"LT", "LE"},
        "minimum": 0.0,
        "maximum": 1.0,
    },
    "sample_size": {
        "dimension": "SAMPLE_SIZE",
        "type": "number",
        "operators": {"GT", "GE"},
        "minimum": 1.0,
    },
    "independence_state": {
        "dimension": "INDEPENDENCE",
        "type": "string",
        "operators": {"IN", "EQ"},
        "allowed_values": {"INDEPENDENT", "PARTIALLY_INDEPENDENT"},
    },
    "phenotype_match_state": {
        "dimension": "PHENOTYPE_MATCH",
        "type": "string",
        "operators": {"IN", "EQ"},
        "allowed_values": {"EXACT", "SAME_CONCEPT_DIFFERENT_DEFINITION"},
    },
    "genomic_harmonization_state": {
        "dimension": "GENOMIC_HARMONIZATION",
        "type": "string",
        "operators": {"EQ", "IN"},
        "allowed_values": {"PASS"},
    },
    "allele_direction_state": {
        "dimension": "ALLELE_DIRECTION",
        "type": "string",
        "operators": {"IN", "EQ"},
        "allowed_values": {"CONSISTENT", "NOT_APPLICABLE"},
    },
    "ancestry_metadata_state": {
        "dimension": "POPULATION_ANCESTRY",
        "type": "string",
        "operators": {"IN", "EQ"},
        "allowed_values": {"ADEQUATE"},
    },
    "gene_assignment_class": {
        "dimension": "GENE_ASSIGNMENT",
        "type": "string",
        "operators": {"IN", "EQ"},
        "allowed_values": {
            "HYPOTHESIS_FREE_CODING_OR_LOF",
            "HIGH_CONFIDENCE_FINE_MAPPING",
            "PREREGISTERED_COLOCALIZATION",
        },
    },
    "historical_novelty_state": {
        "dimension": "HISTORICAL_NOVELTY",
        "type": "string",
        "operators": {"IN", "EQ"},
        "allowed_values": {"NOVEL_STRICT"},
    },
    "source_quality_state": {
        "dimension": "SOURCE_QUALITY",
        "type": "string",
        "operators": {"IN", "EQ"},
        "allowed_values": {"PRIMARY_SOURCE", "QUALIFIED_INDEPENDENT_SOURCE"},
    },
}

REQUIRED_DIMENSIONS = {
    "STUDY_DESIGN",
    "STATISTICAL_STRENGTH",
    "SAMPLE_SIZE",
    "INDEPENDENCE",
    "PHENOTYPE_MATCH",
    "GENOMIC_HARMONIZATION",
    "ALLELE_DIRECTION",
    "POPULATION_ANCESTRY",
    "GENE_ASSIGNMENT",
    "HISTORICAL_NOVELTY",
    "SOURCE_QUALITY",
}


def _reject_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON constant is prohibited: {value}")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"), parse_constant=_reject_constant)


def _finite(value: Any) -> bool:
    return not isinstance(value, float) or math.isfinite(value)


def validate_rule_semantics(rule: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    schema = load_json(SCHEMA)
    Draft202012Validator.check_schema(schema)
    for err in Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(rule):
        loc = ".".join(str(x) for x in err.absolute_path) or "<root>"
        errors.append(f"schema:{loc}:{err.message}")
    if errors:
        return errors

    criteria = rule.get("criteria") or []
    ids = [c["criterion_id"] for c in criteria]
    if len(ids) != len(set(ids)):
        errors.append("criterion_id values must be unique")

    seen_dimension: dict[str, dict[str, Any]] = {}
    for c in criteria:
        dim = c["scientific_dimension"]
        field = c["field_or_artifact"]
        op = c["operator"]

        spec = FIELD_REGISTRY.get(field)
        if spec is None:
            errors.append(f"unknown endpoint-quality field: {field}")
            continue
        if spec["dimension"] != dim:
            errors.append(f"{field} belongs to {spec['dimension']}, not {dim}")
        if op not in spec["operators"] and op != "REQUIRE":
            errors.append(f"operator {op} is not allowed for {field}")

        if dim in seen_dimension:
            errors.append(f"duplicate/possibly contradictory criteria for required dimension {dim}")
        else:
            seen_dimension[dim] = c

        if op == "REQUIRE":
            if c.get("required") is not True:
                errors.append(f"REQUIRE criterion must set required=true: {c['criterion_id']}")
            if "value" in c:
                errors.append(f"REQUIRE criterion may not carry a comparison value: {c['criterion_id']}")
            continue

        value = c.get("value")
        values = value if isinstance(value, list) else [value]
        for v in values:
            if not _finite(v):
                errors.append(f"non-finite operand in criterion {c['criterion_id']}")
                continue
            if spec["type"] == "number":
                if isinstance(v, bool) or not isinstance(v, (int, float)):
                    errors.append(f"numeric field {field} requires numeric operand")
                    continue
                if "minimum" in spec and v < spec["minimum"]:
                    errors.append(f"operand below allowed domain for {field}")
                if "maximum" in spec and v > spec["maximum"]:
                    errors.append(f"operand above allowed domain for {field}")
            elif spec["type"] == "string":
                if not isinstance(v, str):
                    errors.append(f"categorical field {field} requires string operand")
                    continue
                allowed = spec.get("allowed_values")
                if allowed is not None and v not in allowed:
                    errors.append(f"forbidden/UNKNOWN value {v!r} for {field}")

    if rule.get("status") == "FROZEN":
        missing = sorted(REQUIRED_DIMENSIONS - set(seen_dimension))
        if missing:
            errors.append("FROZEN endpoint rule missing dimensions: " + ",".join(missing))
        if rule.get("independence_requirement") != "REQUIRED":
            errors.append("FROZEN E1 endpoint rule requires independence")

    return errors


def _compare(actual: Any, op: str, expected: Any) -> bool:
    if op == "REQUIRE":
        return actual is not None
    if op == "EQ":
        return actual == expected
    if op == "NE":
        return actual != expected
    if op == "GT":
        return actual > expected
    if op == "GE":
        return actual >= expected
    if op == "LT":
        return actual < expected
    if op == "LE":
        return actual <= expected
    if op == "IN":
        return actual in expected
    if op == "NOT_IN":
        return actual not in expected
    raise KeyError(op)


def evaluate_event(rule: dict[str, Any], event: dict[str, Any]) -> tuple[bool, list[str]]:
    errors = validate_rule_semantics(rule)
    if errors:
        raise ValueError("endpoint-quality rule is not executable: " + " | ".join(errors))

    failures: list[str] = []
    for c in rule["criteria"]:
        field = c["field_or_artifact"]
        if field not in event:
            failures.append(f"missing required field {field}")
            continue
        actual = event[field]
        if isinstance(actual, float) and not math.isfinite(actual):
            failures.append(f"non-finite event value for {field}")
            continue
        if not _compare(actual, c["operator"], c.get("value")):
            failures.append(f"criterion failed: {c['criterion_id']}")
    return (not failures, failures)


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate/execute Forge Bio endpoint-quality rules")
    ap.add_argument("rule", type=Path)
    ap.add_argument("--event", type=Path)
    args = ap.parse_args()

    rule = load_json(args.rule)
    errors = validate_rule_semantics(rule)
    if errors:
        for err in errors:
            print(err)
        return 1

    if args.event:
        event = load_json(args.event)
        passed, failures = evaluate_event(rule, event)
        print(json.dumps({"passed": passed, "failures": failures}, indent=2))
        return 0 if passed else 2

    print("VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
