from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
RULE_SCHEMA = ROOT / "schemas" / "endpoint-quality-rule.v1.schema.json"
EVENT_SCHEMA = ROOT / "schemas" / "endpoint-event-input.v1.schema.json"

PRIMARY_ASSIGNMENT_CLASSES = {
    "HYPOTHESIS_FREE_CODING_OR_LOF",
    "HIGH_CONFIDENCE_FINE_MAPPING",
    "PREREGISTERED_COLOCALIZATION",
}
PRIMARY_STUDY_DESIGNS = {"GENOME_WIDE", "EXOME_WIDE", "BIOBANK_WIDE"}


def _reject_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON constant prohibited: {value}")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"), parse_constant=_reject_constant)


def _validate(instance: dict[str, Any], schema_path: Path) -> None:
    schema = load_json(schema_path)
    Draft202012Validator.check_schema(schema)
    errors = sorted(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(instance),
        key=lambda e: list(e.absolute_path),
    )
    if errors:
        parts=[]
        for e in errors:
            loc=".".join(str(p) for p in e.absolute_path) or "<root>"
            parts.append(f"{loc}: {e.message}")
        raise ValueError("schema validation failed: " + " | ".join(parts))


def _values(criterion: dict[str, Any]) -> list[Any]:
    v=criterion.get("value")
    return v if isinstance(v,list) else [v]


def validate_rule_semantics(rule: dict[str, Any]) -> list[str]:
    errors: list[str]=[]
    if rule.get("status") != "FROZEN":
        errors.append("endpoint-quality executor requires FROZEN rule")
        return errors
    if rule.get("endpoint_subtype") != "E1-NOVEL-STRICT":
        errors.append("V0 frozen endpoint-quality rule must target E1-NOVEL-STRICT")
    if rule.get("independence_requirement") != "REQUIRED":
        errors.append("V0 frozen endpoint-quality rule requires independence")

    ids=[]
    fields=[]
    dims=[]
    for c in rule.get("criteria",[]):
        ids.append(c.get("criterion_id"))
        fields.append(c.get("field_or_artifact"))
        dims.append(c.get("scientific_dimension"))
        if c.get("required") is not True:
            errors.append(f"criterion {c.get('criterion_id')} is not mandatory")
        op=c.get("operator")
        field=c.get("field_or_artifact")
        vals=_values(c)
        for v in vals:
            if isinstance(v,float) and not math.isfinite(v):
                errors.append(f"criterion {c.get('criterion_id')} contains non-finite value")

        if field=="p_value":
            if op not in {"LT","LE"}:
                errors.append("p_value criterion must use LT/LE")
            if not vals or not isinstance(vals[0],(int,float)) or isinstance(vals[0],bool) or not (0 < float(vals[0]) <= 1):
                errors.append("p_value threshold must be finite in (0,1]")
        elif field=="sample_size":
            if op not in {"GT","GE"}:
                errors.append("sample_size criterion must use GT/GE")
            if not vals or not isinstance(vals[0],int) or isinstance(vals[0],bool) or vals[0] < 1:
                errors.append("sample_size threshold must be a positive integer")
        elif field=="study_design_class":
            if op!="IN" or not set(vals).issubset(PRIMARY_STUDY_DESIGNS) or not vals:
                errors.append("study_design_class must IN only hypothesis-free study designs")
        elif field=="gene_assignment_class":
            if op!="IN" or not set(vals).issubset(PRIMARY_ASSIGNMENT_CLASSES) or not vals:
                errors.append("gene_assignment_class must IN only frozen primary assignment classes")
        elif field=="independence_status":
            if op not in {"EQ","IN"} or any(v!="INDEPENDENT" for v in vals):
                errors.append("independence_status must require INDEPENDENT")
        elif field=="historical_novelty_status":
            if op not in {"EQ","IN"} or any(v!="NOVEL_CONFIRMED" for v in vals):
                errors.append("historical_novelty_status must require NOVEL_CONFIRMED")
        elif field=="phenotype_relation":
            if op not in {"EQ","IN"} or any(v=="UNRESOLVED" for v in vals):
                errors.append("phenotype_relation may not admit UNRESOLVED")
        elif field=="genomic_harmonization_status":
            if op not in {"EQ","IN"} or any(v in {"AMBIGUOUS","UNKNOWN"} for v in vals):
                errors.append("genomic_harmonization_status may not admit AMBIGUOUS/UNKNOWN")
        elif field=="allele_direction_status":
            if op not in {"EQ","IN"} or any(v=="UNKNOWN" for v in vals):
                errors.append("allele_direction_status may not admit UNKNOWN")
        elif field=="population_ancestry_status":
            if op not in {"EQ","IN"} or any(v=="UNKNOWN" for v in vals):
                errors.append("population_ancestry_status may not admit UNKNOWN")
        elif field=="source_quality_status":
            if op not in {"EQ","IN"} or any(v in {"CURATED_ONLY","UNKNOWN"} for v in vals):
                errors.append("source_quality_status requires primary/independent source quality")
        elif field in {"replication_status","heterogeneity_status"}:
            if op not in {"EQ","IN"} or any(v in {"UNKNOWN","UNRESOLVED","INCONCLUSIVE"} for v in vals):
                errors.append(f"{field} may not admit unresolved/unknown states")
        elif op=="REQUIRE":
            errors.append(f"FROZEN V0 criterion {field} cannot be presence-only")

    if len(ids)!=len(set(ids)):
        errors.append("criterion IDs must be unique")
    if len(fields)!=len(set(fields)):
        errors.append("one frozen criterion per executable field is required")
    if len(dims)!=len(set(dims)):
        errors.append("one frozen criterion per scientific dimension is required")
    return errors


def _compare(actual: Any, op: str, expected: Any) -> bool:
    if op=="REQUIRE":
        return actual is not None
    if op=="EQ":
        return actual==expected
    if op=="NE":
        return actual!=expected
    if op=="GT":
        return actual>expected
    if op=="GE":
        return actual>=expected
    if op=="LT":
        return actual<expected
    if op=="LE":
        return actual<=expected
    if op=="IN":
        return actual in expected
    if op=="NOT_IN":
        return actual not in expected
    raise ValueError(f"unsupported operator: {op}")


def evaluate_event(rule: dict[str, Any], event: dict[str, Any]) -> dict[str, Any]:
    _validate(rule,RULE_SCHEMA)
    _validate(event,EVENT_SCHEMA)
    semantic_errors=validate_rule_semantics(rule)
    if semantic_errors:
        raise ValueError("invalid frozen endpoint rule: " + " | ".join(semantic_errors))

    fields=event["fields"]
    results=[]
    passed=True
    for c in rule["criteria"]:
        field=c["field_or_artifact"]
        if field not in fields:
            ok=False
            reason="missing required field"
        else:
            expected=c.get("value")
            ok=_compare(fields[field],c["operator"],expected)
            reason="pass" if ok else "criterion failed"
        results.append({"criterion_id":c["criterion_id"],"field":field,"passed":ok,"reason":reason})
        passed = passed and ok

    return {
        "event_id":event["event_id"],
        "rule_id":rule["rule_id"],
        "qualifies":passed,
        "criteria":results,
    }


def main() -> int:
    ap=argparse.ArgumentParser(description="Evaluate one future event against a frozen endpoint-quality rule")
    ap.add_argument("--rule",type=Path,required=True)
    ap.add_argument("--event",type=Path,required=True)
    args=ap.parse_args()
    result=evaluate_event(load_json(args.rule),load_json(args.event))
    print(json.dumps(result,indent=2,allow_nan=False))
    return 0 if result["qualifies"] else 3


if __name__=="__main__":
    raise SystemExit(main())
