from __future__ import annotations

import hashlib
import json
import math
import statistics
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from scripts.select_big0f_sample import (
    derive_sampling_key,
    deterministic_event_sample,
    select,
)


ROOT = Path(__file__).resolve().parents[1]
SELECTION_SCHEMA_PATH = ROOT / "schemas" / "big0f-selection-provenance.v1.schema.json"
NUISANCE_RUN_SCHEMA_PATH = ROOT / "schemas" / "big0f-nuisance-run.v1.schema.json"
PROVIDER_AUDIT_SCHEMA_PATH = ROOT / "schemas" / "big0f-provider-audit.v1.schema.json"
ADJUDICATOR_INDEPENDENCE_SCHEMA_PATH = ROOT / "schemas" / "big0f-adjudicator-independence.v1.schema.json"
CURATION_AUDIT_SCHEMA_PATH = ROOT / "schemas" / "big0f-curation-audit.v1.schema.json"

CUTOFF_ORDER = ["2005-12-31", "2008-12-31", "2011-12-31", "2014-12-31"]
HORIZON_ORDER = ["3y", "5y", "7y", "10y"]


def canonical_digest(payload: dict[str, Any]) -> str:
    body = dict(payload)
    body.pop("digest", None)
    encoded = json.dumps(
        body,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def _validate_schema(instance: dict[str, Any], schema_path: Path) -> list[str]:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    errors = sorted(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(instance),
        key=lambda err: list(err.absolute_path),
    )
    return [
        f"{'.'.join(str(x) for x in err.absolute_path) or '<root>'}: {err.message}"
        for err in errors
    ]


def derive_nuisance_metrics(run: dict[str, Any]) -> dict[str, float]:
    ranks = [float(row["rank_fraction"]) for row in run["event_rank_records"]]
    if not ranks:
        raise ValueError("nuisance run has no event-rank records")
    if any(not math.isfinite(x) or not 0.0 <= x <= 1.0 for x in ranks):
        raise ValueError("nuisance rank fractions must be finite and in [0,1]")

    by_disease: dict[str, list[float]] = {}
    for row in run["event_rank_records"]:
        by_disease.setdefault(row["disease_id"], []).append(float(row["rank_fraction"]))
    if len(by_disease) < 2:
        raise ValueError("power proxy requires at least two event-bearing diseases")

    disease_means = [statistics.fmean(values) for _, values in sorted(by_disease.items())]
    disease_level_sd = statistics.stdev(disease_means)
    if not math.isfinite(disease_level_sd) or disease_level_sd <= 0:
        raise ValueError("derived disease-level SD must be finite and positive")

    return {
        "median_positive_rank_fraction": statistics.median(ranks),
        "top_1pct_fraction": sum(x <= 0.01 for x in ranks) / len(ranks),
        "top_5pct_fraction": sum(x <= 0.05 for x in ranks) / len(ranks),
        "disease_level_sd": disease_level_sd,
    }


def verify_nuisance_run(
    run: dict[str, Any],
    *,
    nuisance_manifest: dict[str, Any],
    nuisance_manifest_digest: str,
    selected_event_ids: set[str] | None = None,
    selected_disease_ids: set[str] | None = None,
    expected_positive_count: int | None = None,
) -> list[str]:
    errors = _validate_schema(run, NUISANCE_RUN_SCHEMA_PATH)
    if errors:
        return errors

    if run["digest"] != canonical_digest(run):
        errors.append("nuisance-run canonical digest mismatch")
    if run["nuisance_manifest_digest"] != nuisance_manifest_digest:
        errors.append("nuisance run is not bound to the current nuisance manifest")
    if run["pilot_model_evaluation_mode"] != nuisance_manifest["pilot_model_evaluation_mode"]:
        errors.append("nuisance run model-evaluation mode differs from frozen manifest")
    if nuisance_manifest.get("semantic_evidence_features_forbidden") and run["semantic_evidence_features_used"]:
        errors.append("semantic biological evidence was used in the nuisance-only pilot run")

    mandatory = set(nuisance_manifest["mandatory_feature_families"])
    actual = set(run["actual_feature_families"])
    if actual != mandatory:
        errors.append(
            "actual nuisance feature families do not exactly match the frozen manifest "
            f"(missing={sorted(mandatory - actual)}, extra={sorted(actual - mandatory)})"
        )
    artifact_families = set(run["feature_artifact_digests"])
    if artifact_families != mandatory:
        errors.append(
            "feature-artifact digests do not exactly cover the frozen nuisance families "
            f"(missing={sorted(mandatory - artifact_families)}, extra={sorted(artifact_families - mandatory)})"
        )

    event_ids = [row["event_id"] for row in run["event_rank_records"]]
    if len(event_ids) != len(set(event_ids)):
        errors.append("nuisance run contains duplicate event IDs")
    if selected_event_ids is not None and not set(event_ids).issubset(selected_event_ids):
        errors.append("nuisance run contains event IDs outside the deterministically selected pilot event set")
    disease_ids = {row["disease_id"] for row in run["event_rank_records"]}
    if selected_disease_ids is not None and not disease_ids.issubset(selected_disease_ids):
        errors.append("nuisance run contains diseases outside the deterministic pilot sample")
    if expected_positive_count is not None and len(event_ids) != expected_positive_count:
        errors.append(
            f"nuisance rank record count {len(event_ids)} does not equal "
            f"high-specificity positive count {expected_positive_count}"
        )
    try:
        derive_nuisance_metrics(run)
    except Exception as exc:
        errors.append(f"cannot derive nuisance metrics: {exc}")
    return errors


def derive_provider_metrics(audit: dict[str, Any]) -> dict[str, Any]:
    required = [
        cell for cell in audit["required_field_cells"]
        if cell["criticality"] in {"CRITICAL", "REQUIRED"}
    ]
    if not required:
        raise ValueError("provider audit has no CRITICAL/REQUIRED field cells")

    def available(cell: dict[str, Any]) -> bool:
        return bool(
            cell["historical_release_obtainable"]
            and cell["release_version_identifiable"]
            and cell["field_existed_at_t"]
            and cell["value_reconstructable"]
        )

    availability = sum(available(cell) for cell in required) / len(required)
    coverage = {grade: 0 for grade in ("HIGH", "MODERATE", "LOW", "UNKNOWN")}
    for cell in required:
        coverage[cell["coverage_grade"]] += 1
    coverage = {grade: count / len(required) for grade, count in coverage.items()}

    ancestry_records = audit["ancestry_population_audit"]["case_records"]
    if not ancestry_records:
        raise ValueError("provider audit has no ancestry/population case records")
    ancestry_coverage = (
        sum(bool(row["metadata_available"]) for row in ancestry_records)
        / len(ancestry_records)
    )
    return {
        "source_family_ids": [row["source_family_id"] for row in audit["source_families"]],
        "required_field_availability_fraction": availability,
        "historical_search_coverage_distribution": coverage,
        "provider_coupling_risk": audit["provider_coupling"]["risk"],
        "ancestry_metadata_coverage_fraction": ancestry_coverage,
        "ancestry_population_metadata_adequacy": audit["ancestry_population_audit"]["adequacy"],
    }


def verify_provider_audit(audit: dict[str, Any]) -> list[str]:
    errors = _validate_schema(audit, PROVIDER_AUDIT_SCHEMA_PATH)
    if errors:
        return errors
    if audit["digest"] != canonical_digest(audit):
        errors.append("provider-audit canonical digest mismatch")

    source_ids = [row["source_family_id"] for row in audit["source_families"]]
    if len(source_ids) != len(set(source_ids)):
        errors.append("provider audit contains duplicate source_family_id values")
    required_kinds = {
        "PRIMARY_PUBLICATION_METADATA",
        "GWAS_HISTORICAL",
        "IDENTITY_ONTOLOGY",
        "HISTORICAL_GENE_MODEL_ANNOTATION",
    }
    actual_kinds = {row["family_kind"] for row in audit["source_families"]}
    if not required_kinds.issubset(actual_kinds):
        errors.append(
            "provider audit is missing one or more mandatory source-family kinds: "
            + ", ".join(sorted(required_kinds - actual_kinds))
        )

    source_set = set(source_ids)
    for cell in audit["required_field_cells"]:
        if cell["source_family_id"] not in source_set:
            errors.append(
                f"provider field cell references unknown source family {cell['source_family_id']}"
            )
    try:
        derive_provider_metrics(audit)
    except Exception as exc:
        errors.append(f"cannot derive provider metrics: {exc}")
    return errors


def verify_adjudicator_independence(attestation: dict[str, Any]) -> list[str]:
    errors = _validate_schema(attestation, ADJUDICATOR_INDEPENDENCE_SCHEMA_PATH)
    if errors:
        return errors
    if attestation["digest"] != canonical_digest(attestation):
        errors.append("adjudicator-independence canonical digest mismatch")
    return errors


def derive_curation_metrics(
    audit: dict[str, Any],
    *,
    total_event_cases: int,
    max_median_event_curation_minutes: float,
) -> dict[str, Any]:
    event_records = audit["event_case_records"]
    non_event_records = audit["non_event_case_records"]
    if len(event_records) != total_event_cases:
        raise ValueError(
            f"curation event-case records {len(event_records)} != adjudicated event cases {total_event_cases}"
        )
    event_ids = [row["case_id"] for row in event_records]
    non_event_ids = [row["case_id"] for row in non_event_records]
    if len(event_ids) != len(set(event_ids)):
        raise ValueError("curation audit contains duplicate event case IDs")
    if len(non_event_ids) != len(set(non_event_ids)):
        raise ValueError("curation audit contains duplicate non-event case IDs")
    if set(event_ids) & set(non_event_ids):
        raise ValueError("curation audit event and non-event case IDs overlap")

    event_median = statistics.median(float(row["minutes"]) for row in event_records)
    non_event_median = statistics.median(float(row["minutes"]) for row in non_event_records)
    expected_non_event = min(100, max(50, total_event_cases))
    complete = len(non_event_records) >= expected_non_event
    burden = "EXCESSIVE" if event_median > max_median_event_curation_minutes else "ACCEPTABLE"
    return {
        "retrospective_curation_burden_assessment": burden,
        "median_minutes_per_event_case": event_median,
        "symmetric_non_event_audit_complete": complete,
        "non_event_case_count": len(non_event_records),
        "median_minutes_per_non_event_case": non_event_median,
        "operational_capacity_rule_id": audit["operational_capacity_rule_id"],
    }


def verify_curation_audit(
    audit: dict[str, Any],
    *,
    total_event_cases: int,
    max_median_event_curation_minutes: float,
) -> list[str]:
    errors = _validate_schema(audit, CURATION_AUDIT_SCHEMA_PATH)
    if errors:
        return errors
    if audit["digest"] != canonical_digest(audit):
        errors.append("curation-audit canonical digest mismatch")
    try:
        derive_curation_metrics(
            audit,
            total_event_cases=total_event_cases,
            max_median_event_curation_minutes=max_median_event_curation_minutes,
        )
    except Exception as exc:
        errors.append(f"cannot derive curation metrics: {exc}")
    return errors


def verify_selection_provenance(
    provenance: dict[str, Any],
    *,
    thresholds: dict[str, Any],
    result: dict[str, Any],
    disease_ids: list[str],
    beacon: dict[str, Any],
    frame_digest: str,
    frame_seal_attestation: dict[str, Any],
    frame_seal_attestation_digest: str,
) -> list[str]:
    errors = _validate_schema(provenance, SELECTION_SCHEMA_PATH)
    if errors:
        return errors
    if provenance["digest"] != canonical_digest(provenance):
        errors.append("selection-provenance canonical digest mismatch")

    expected_pairs = [(cutoff, horizon) for cutoff in CUTOFF_ORDER for horizon in HORIZON_ORDER]
    actual_pairs = [(row["cutoff"], row["horizon"]) for row in provenance["candidate_pairs"]]
    if actual_pairs != expected_pairs:
        errors.append("candidate cutoff/horizon audits are not the complete frozen lexicographic grid")
        return errors

    try:
        deterministic_diseases = select(
            disease_ids,
            beacon,
            frame_digest,
            frame_seal_attestation=frame_seal_attestation,
            frame_seal_attestation_digest=frame_seal_attestation_digest,
            target_n=min(15, len(disease_ids)),
        )
    except Exception as exc:
        errors.append(f"cannot reconstruct deterministic disease order: {exc}")
        return errors
    if len(deterministic_diseases) < 15:
        errors.append("eligible disease frame has fewer than the frozen maximum pilot size of 15")
        return errors

    first_passing: dict[str, Any] | None = None
    expected_disease_set = set(deterministic_diseases[:15])
    for row in provenance["candidate_pairs"]:
        raw = row["raw_event_records"]
        ids = [event["event_id"] for event in raw]
        if len(ids) != len(set(ids)):
            errors.append(f"duplicate raw event IDs in {row['cutoff']} / {row['horizon']}")
        if any(event["disease_id"] not in expected_disease_set for event in raw):
            errors.append(f"raw event outside deterministic first-15 diseases in {row['cutoff']} / {row['horizon']}")
        feasible = (
            row["provider_availability_pass"]
            and row["observation_window_pass"]
            and len(raw) >= thresholds["min_candidate_event_count"]
        )
        if first_passing is None and feasible:
            first_passing = row

    if first_passing is None:
        errors.append("no cutoff/horizon pair passes the frozen feasibility rule")
        return errors
    if (result["cutoff"], result["horizon"]) != (first_passing["cutoff"], first_passing["horizon"]):
        errors.append("pilot result did not use the first feasible cutoff/horizon pair")

    selected_pair = next(
        (
            row for row in provenance["candidate_pairs"]
            if row["cutoff"] == result["cutoff"] and row["horizon"] == result["horizon"]
        ),
        None,
    )
    if selected_pair is None:
        errors.append("selected cutoff/horizon pair missing from provenance")
        return errors

    raw_all = selected_pair["raw_event_records"]
    target_n = 12
    while target_n < 15:
        prefix = set(deterministic_diseases[:target_n])
        count = sum(event["disease_id"] in prefix for event in raw_all)
        if count >= thresholds["min_candidate_event_count"]:
            break
        target_n += 1

    expected_diseases = deterministic_diseases[:target_n]
    if provenance["selected_disease_ids"] != expected_diseases:
        errors.append(
            "selected diseases do not follow the deterministic 12-to-15 expansion rule"
        )
    if result["disease_count"] != target_n:
        errors.append("pilot disease_count does not match deterministic expansion")
    selected_disease_set = set(expected_diseases)
    raw_selected = [event for event in raw_all if event["disease_id"] in selected_disease_set]

    if len(raw_selected) < thresholds["min_candidate_event_count"]:
        errors.append("selected first-passing pair cannot reach the frozen minimum event count by 15 diseases")
        return errors

    try:
        key = derive_sampling_key(frame_digest, beacon["randomness_hex"])
        expected_events = deterministic_event_sample(
            raw_selected,
            key,
            cap=thresholds["max_candidate_event_count"],
        )
    except Exception as exc:
        errors.append(f"cannot reconstruct deterministic event sample: {exc}")
        return errors

    if provenance["selected_event_ids"] != expected_events:
        errors.append("selected events do not match the sealed deterministic event-cap algorithm")
    if result["candidate_event_count"] != len(expected_events):
        errors.append("pilot candidate_event_count does not match deterministic event selection")

    event_by_id = {event["event_id"]: event for event in raw_selected}
    event_bearing = {
        event_by_id[event_id]["disease_id"]
        for event_id in expected_events
        if event_id in event_by_id
    }
    if result["event_bearing_disease_count"] != len(event_bearing):
        errors.append("pilot event_bearing_disease_count does not match deterministic selected events")
    return errors
