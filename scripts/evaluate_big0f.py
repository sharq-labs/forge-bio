from __future__ import annotations

import argparse
import hashlib
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from scripts.build_seal_bundle import manifest_digest, verify_manifest
from scripts.scientific_invariants import validate_external_seal
from scripts.simulate_big0f_power import verify_artifact as verify_power_artifact


ROOT = Path(__file__).resolve().parents[1]
PILOT_SCHEMA_PATH = ROOT / "schemas" / "big0f-pilot-result.v1.schema.json"
THRESHOLD_SCHEMA_PATH = ROOT / "schemas" / "big0f-threshold-manifest.v1.schema.json"
SEAL_SCHEMA_PATH = ROOT / "schemas" / "seal-bundle-manifest.v1.schema.json"
ATTESTATION_SCHEMA_PATH = ROOT / "schemas" / "external-seal-attestation.v1.schema.json"
POWER_SCHEMA_PATH = ROOT / "schemas" / "big0f-power-analysis.v1.schema.json"
ADJUDICATION_SCHEMA_PATH = ROOT / "schemas" / "big0f-adjudication-policy.v1.schema.json"
NUISANCE_SCHEMA_PATH = ROOT / "schemas" / "big0f-nuisance-manifest.v1.schema.json"
DEFAULT_THRESHOLD_PATH = ROOT / "config" / "big0f-thresholds.v1.json"
DEFAULT_SAMPLING_CODE_PATH = ROOT / "scripts" / "select_big0f_sample.py"
DEFAULT_POWER_ENGINE_PATH = ROOT / "scripts" / "simulate_big0f_power.py"


@dataclass(frozen=True)
class Decision:
    decision: str
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class EvaluationContext:
    seal_verified: bool
    threshold_manifest_verified: bool
    power_analysis_verified: bool
    adjudication_policy_verified: bool
    nuisance_manifest_verified: bool
    decision_engine_sealed: bool
    pilot_schema_sealed: bool
    sampling_code_sealed: bool


def _reject_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON constant is prohibited: {value}")


def load_json_strict(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"), parse_constant=_reject_constant)


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def _ensure_finite(value: Any, path: str = "<root>") -> None:
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError(f"non-finite numeric value at {path}")
    elif isinstance(value, list):
        for i, item in enumerate(value):
            _ensure_finite(item, f"{path}[{i}]")
    elif isinstance(value, dict):
        for key, item in value.items():
            _ensure_finite(item, f"{path}.{key}")


def _validate_schema(instance: dict[str, Any], schema_path: Path) -> None:
    _ensure_finite(instance)
    schema = load_json_strict(schema_path)
    Draft202012Validator.check_schema(schema)
    errors = sorted(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(instance),
        key=lambda err: list(err.absolute_path),
    )
    if errors:
        formatted = []
        for err in errors:
            location = ".".join(str(x) for x in err.absolute_path) or "<root>"
            formatted.append(f"{location}: {err.message}")
        raise ValueError("schema validation failed: " + " | ".join(formatted))


def load_threshold_manifest(path: Path = DEFAULT_THRESHOLD_PATH) -> dict[str, Any]:
    manifest = load_json_strict(path)
    _validate_schema(manifest, THRESHOLD_SCHEMA_PATH)
    t = manifest["thresholds"]
    if t["max_ambiguity_go"] > t["max_ambiguity_redesign"]:
        raise ValueError("ambiguity GO threshold cannot exceed REDESIGN/NO-GO boundary")
    if t["min_agreement_go"] < t["min_agreement_redesign"]:
        raise ValueError("agreement GO threshold cannot be below REDESIGN/NO-GO boundary")
    if t["min_required_field_availability_go"] < t["min_required_field_availability_redesign"]:
        raise ValueError("availability GO threshold cannot be below REDESIGN/NO-GO boundary")
    if t["min_non_event_to_event_time_ratio"] > t["max_non_event_to_event_time_ratio"]:
        raise ValueError("curation time-ratio bounds are inverted")
    return manifest


def _reference_context_missing(context: EvaluationContext | None) -> list[str]:
    if context is None:
        return ["reference verification context missing"]
    missing = []
    for field in (
        "seal_verified",
        "threshold_manifest_verified",
        "power_analysis_verified",
        "adjudication_policy_verified",
        "nuisance_manifest_verified",
        "decision_engine_sealed",
        "pilot_schema_sealed",
        "sampling_code_sealed",
    ):
        if not getattr(context, field):
            missing.append(f"{field} is false")
    return missing


def _evaluate_once(
    metrics: dict[str, Any],
    thresholds: dict[str, Any],
    *,
    context: EvaluationContext | None,
) -> Decision:
    no_go: list[str] = []
    redesign: list[str] = []
    incomplete: list[str] = []

    assignment = metrics["assignment_metrics"]
    ambiguity = metrics["ambiguity_metrics"]
    provider = metrics["provider_metrics"]
    adjudication = metrics["adjudication_metrics"]
    power = metrics["power_metrics"]
    nuisance = metrics["nuisance_headroom_metrics"]
    independence = metrics["independence_metrics"]
    applicability = metrics["applicability_metrics"]
    curation = metrics["curation_metrics"]

    incomplete.extend(_reference_context_missing(context))

    if metrics["source_family_count"] != len(metrics["source_family_ids"]):
        incomplete.append("source_family_count disagrees with source_family_ids")
    if metrics["source_family_count"] < thresholds["min_source_family_count"]:
        incomplete.append("historical provider audit has fewer than the sealed minimum source families")

    if metrics["event_bearing_disease_count"] > metrics["disease_count"]:
        raise ValueError("event-bearing disease count exceeds total disease count")
    if metrics["adjudication_metrics"]["adjudicated_event_case_count"] > metrics["candidate_event_count"]:
        raise ValueError("adjudicated event cases exceed candidate events")
    if metrics["high_specificity_positive_count"] > metrics["candidate_event_count"]:
        raise ValueError("high-specificity positives exceed candidate event count")

    if metrics["candidate_event_count"] < thresholds["min_candidate_event_count"]:
        if metrics["disease_count"] < thresholds["max_disease_count"]:
            incomplete.append("pilot must expand disease sample before judging event-count feasibility")
        else:
            no_go.append("candidate event count below frozen minimum after maximum pilot expansion")

    total_cases = adjudication["adjudicated_event_case_count"]
    if total_cases != metrics["candidate_event_count"]:
        incomplete.append("not every candidate event has been adjudicated")

    duplicate_count = adjudication["duplicate_review_count"]
    duplicate_fraction = adjudication["duplicate_review_fraction"]
    if total_cases <= 0:
        incomplete.append("no adjudicated event cases")
    else:
        computed_fraction = duplicate_count / total_cases
        if abs(computed_fraction - duplicate_fraction) > 1e-9:
            incomplete.append("duplicate_review_fraction is inconsistent with duplicate review count")
        required_duplicate_count = min(total_cases, max(30, math.ceil(0.30 * total_cases)))
        if duplicate_count < required_duplicate_count:
            incomplete.append(
                f"independent duplicate review incomplete: {duplicate_count} < required {required_duplicate_count}"
            )

    if adjudication["rule_revision_count"] == 1 and adjudication["heldout_retest_completed"] is not True:
        incomplete.append("post-revision held-out adjudication retest is incomplete")

    component_ambiguity = max(
        ambiguity["novelty_ambiguity_fraction"],
        ambiguity["variant_harmonization_ambiguity_fraction"],
        ambiguity["phenotype_ambiguity_fraction"],
        ambiguity["sample_overlap_ambiguity_fraction"],
    )
    primary_ambiguity = ambiguity["any_primary_endpoint_ambiguity_fraction"]
    if primary_ambiguity + 1e-12 < component_ambiguity:
        raise ValueError("union primary-endpoint ambiguity is smaller than a component ambiguity fraction")
    if primary_ambiguity > thresholds["max_ambiguity_redesign"]:
        no_go.append("fraction ambiguous on any primary-endpoint dimension exceeds NO-GO boundary")
    elif primary_ambiguity > thresholds["max_ambiguity_go"]:
        redesign.append("primary-endpoint ambiguity exceeds GO boundary")

    for name, low, point, high in (
        (
            "attention assignment association",
            assignment["attention_assignment_ci_low"],
            assignment["attention_assignment_association"],
            assignment["attention_assignment_ci_high"],
        ),
    ):
        if low > high or not (low <= point <= high):
            raise ValueError(f"{name} estimate/interval is inconsistent")

    max_abs_attention = max(
        abs(assignment["attention_assignment_ci_low"]),
        abs(assignment["attention_assignment_ci_high"]),
    )
    if max_abs_attention >= thresholds["max_abs_attention_association"]:
        redesign.append("attention-assignment confidence interval reaches/exceeds sealed redesign boundary")

    if assignment["hypothesis_free_primary_positive_fraction"] < thresholds["min_hypothesis_free_primary_positive_fraction"]:
        redesign.append("too few primary positives arise from hypothesis-free study designs")

    if assignment["label_feature_method_coupling_fraction"] > thresholds["max_label_feature_method_coupling_fraction"]:
        redesign.append("label/feature method-family coupling exceeds sealed boundary")

    if assignment["primary_eligible_fraction"] < thresholds["min_primary_eligible_fraction"]:
        redesign.append("primary-eligible high-specificity assignment fraction below sealed minimum")

    if assignment["author_named_fraction"] + assignment["nearest_gene_fraction"] >= thresholds["max_author_nearest_fraction"]:
        redesign.append("author-named + nearest-gene assignment fraction reaches/exceeds sealed boundary")

    agreement = min(
        adjudication["primary_assignment_agreement"],
        adjudication["phenotype_agreement"],
    )
    if agreement < thresholds["min_agreement_redesign"]:
        no_go.append("primary adjudication agreement below NO-GO boundary")
    elif agreement < thresholds["min_agreement_go"]:
        redesign.append("primary adjudication agreement below GO boundary")

    availability = provider["required_field_availability_fraction"]
    if availability < thresholds["min_required_field_availability_redesign"]:
        no_go.append("required-field availability below NO-GO boundary")
    elif availability < thresholds["min_required_field_availability_go"]:
        redesign.append("required-field availability below GO boundary")

    coverage = provider["historical_search_coverage_distribution"]
    coverage_sum = sum(coverage.values())
    if abs(coverage_sum - 1.0) > 1e-6:
        raise ValueError("historical search coverage distribution must sum to 1")

    if provider["provider_coupling_risk"] == "UNKNOWN":
        incomplete.append("provider coupling risk remains UNKNOWN")
    elif provider["provider_coupling_risk"] in {"MODERATE", "HIGH"}:
        redesign.append("provider coupling is not LOW")

    if applicability["ancestry_population_metadata_adequacy"] == "UNKNOWN":
        incomplete.append("ancestry/population metadata adequacy remains UNKNOWN")
    elif applicability["ancestry_population_metadata_adequacy"] == "INADEQUATE":
        redesign.append("ancestry/population metadata is inadequate")
    if applicability["ancestry_metadata_coverage_fraction"] < thresholds["min_ancestry_metadata_coverage_fraction"]:
        redesign.append("ancestry metadata coverage below sealed minimum")

    if curation["retrospective_curation_burden_assessment"] == "UNKNOWN":
        incomplete.append("retrospective curation burden remains UNKNOWN")
    elif curation["retrospective_curation_burden_assessment"] == "EXCESSIVE":
        redesign.append("retrospective curation burden is excessive")
    if curation["median_minutes_per_event_case"] > thresholds["max_median_event_curation_minutes"]:
        redesign.append("median event curation time exceeds sealed operational capacity")
    if curation["median_minutes_per_event_case"] > 0:
        ratio = curation["median_minutes_per_non_event_case"] / curation["median_minutes_per_event_case"]
        if not (
            thresholds["min_non_event_to_event_time_ratio"]
            <= ratio
            <= thresholds["max_non_event_to_event_time_ratio"]
        ):
            redesign.append("event/non-event audit burden is too asymmetric for the sealed process")
    if curation["symmetric_non_event_audit_complete"] is not True:
        incomplete.append("symmetric non-event historical audit is incomplete")
    expected_non_event = min(100, max(50, total_cases))
    if curation["non_event_case_count"] < expected_non_event:
        incomplete.append(
            f"symmetric non-event audit sample too small: {curation['non_event_case_count']} < {expected_non_event}"
        )

    if power["alpha"] != thresholds["alpha"]:
        raise ValueError("pilot alpha differs from sealed threshold manifest")
    if power["minimum_scientifically_meaningful_effect"] != thresholds["minimum_scientifically_meaningful_effect"]:
        raise ValueError("minimum scientifically meaningful effect differs from sealed threshold manifest")
    if power["estimated_power"] < power["target_power"] or power["estimated_power"] < 0.80:
        no_go.append("estimated confirmatory power below target / 0.80")
    if metrics["untouched_confirmatory_disease_count"] < power["required_confirmatory_disease_count"]:
        no_go.append("untouched confirmatory disease pool is smaller than power requirement")
    if metrics["high_specificity_positive_count"] < max(
        thresholds["min_high_specificity_positive_count"],
        power["required_high_specificity_positive_count"],
    ):
        redesign.append("high-specificity positive count below sealed/power requirement")

    if independence["pre_t_cohort_reuse_fraction"] >= thresholds["max_pre_t_cohort_reuse_fraction"]:
        redesign.append("pre-T cohort reuse reaches/exceeds sealed boundary")
    if independence["event_family_deduplication_fraction"] > thresholds["max_event_family_deduplication_fraction"]:
        redesign.append("event-family deduplication impact exceeds sealed boundary")
    if independence["locus_to_many_gene_credit_impact"] > thresholds["max_locus_to_many_gene_credit_impact_fraction"]:
        redesign.append("locus-to-many-gene credit impact exceeds sealed boundary")

    if nuisance["top_1pct_fraction"] > nuisance["top_5pct_fraction"]:
        raise ValueError("top-1% positive fraction cannot exceed top-5% positive fraction")
    if nuisance["median_positive_rank_fraction"] <= thresholds["max_nuisance_median_rank_fraction"]:
        redesign.append("Combined Nuisance median positive rank indicates saturation")
    if nuisance["top_1pct_fraction"] >= thresholds["max_nuisance_top1_positive_fraction"]:
        redesign.append("Combined Nuisance places too many positives in the top 1%")

    if incomplete:
        return Decision("INCONCLUSIVE", tuple(incomplete + no_go + redesign))
    if no_go:
        return Decision("NO_GO", tuple(no_go + redesign))
    if redesign:
        return Decision("REDESIGN", tuple(redesign))
    return Decision("GO", ("all frozen GO gates passed",))


def evaluate(
    metrics: dict[str, Any],
    threshold_manifest: dict[str, Any] | None = None,
    *,
    context: EvaluationContext | None = None,
) -> Decision:
    _validate_schema(metrics, PILOT_SCHEMA_PATH)
    threshold_manifest = threshold_manifest or load_threshold_manifest()
    _validate_schema(threshold_manifest, THRESHOLD_SCHEMA_PATH)
    thresholds = threshold_manifest["thresholds"]

    base = _evaluate_once(metrics, thresholds, context=context)

    if base.decision == "INCONCLUSIVE":
        next_count = metrics["prior_inconclusive_count"] + 1
        if next_count >= threshold_manifest["max_inconclusive_evaluations"]:
            return Decision(
                "REDESIGN",
                tuple(base.reasons) + ("maximum INCONCLUSIVE evaluations exhausted",),
            )
        return base

    variant_decisions = set()
    for variant in threshold_manifest["sensitivity_variants"]:
        variant_thresholds = dict(thresholds)
        variant_thresholds.update(variant["overrides"])
        variant_decisions.add(_evaluate_once(metrics, variant_thresholds, context=context).decision)

    variant_decisions.discard("INCONCLUSIVE")
    if variant_decisions and (len(variant_decisions) > 1 or base.decision not in variant_decisions):
        return Decision(
            "REDESIGN",
            (
                "GO/REDESIGN/NO_GO conclusion is unstable across sealed threshold sensitivity variants",
                f"base={base.decision}",
                f"variants={sorted(variant_decisions)}",
            ),
        )
    return base


def _verified_context_from_files(
    result: dict[str, Any],
    *,
    protocol_path: Path,
    disease_frame_path: Path,
    randomness_beacon_path: Path,
    threshold_manifest_path: Path,
    seal_bundle_manifest_path: Path,
    seal_attestation_paths: list[Path],
    power_analysis_path: Path,
    adjudication_policy_path: Path,
    nuisance_manifest_path: Path,
    sampling_code_path: Path,
    power_engine_path: Path,
) -> EvaluationContext:
    threshold_manifest = load_json_strict(threshold_manifest_path)
    _validate_schema(threshold_manifest, THRESHOLD_SCHEMA_PATH)

    adjudication_policy = load_json_strict(adjudication_policy_path)
    _validate_schema(adjudication_policy, ADJUDICATION_SCHEMA_PATH)
    nuisance_manifest = load_json_strict(nuisance_manifest_path)
    _validate_schema(nuisance_manifest, NUISANCE_SCHEMA_PATH)

    seal_manifest = load_json_strict(seal_bundle_manifest_path)
    _validate_schema(seal_manifest, SEAL_SCHEMA_PATH)
    bundle_digest = manifest_digest(seal_manifest)
    if bundle_digest != result["seal_bundle_digest"]:
        raise ValueError("pilot seal_bundle_digest does not match seal-bundle manifest")

    if len(seal_attestation_paths) < 2:
        raise ValueError("BIG 0F requires both third-party timestamp and public-registry attestations")

    component_paths = {
        "protocol": protocol_path,
        "disease_frame": disease_frame_path,
        "randomness_beacon": randomness_beacon_path,
        "threshold_manifest": threshold_manifest_path,
        "adjudication_policy": adjudication_policy_path,
        "nuisance_manifest": nuisance_manifest_path,
        "decision_engine": Path(__file__),
        "pilot_result_schema": PILOT_SCHEMA_PATH,
        "sampling_code": sampling_code_path,
        "threshold_manifest_schema": THRESHOLD_SCHEMA_PATH,
        "adjudication_policy_schema": ADJUDICATION_SCHEMA_PATH,
        "nuisance_manifest_schema": NUISANCE_SCHEMA_PATH,
        "power_analysis_schema": POWER_SCHEMA_PATH,
        "power_engine": power_engine_path,
    }

    authorities: set[str] = set()
    attestation_ids: set[str] = set()
    first_adjudication = __import__("datetime").datetime.fromisoformat(
        result["first_adjudication_at"].replace("Z", "+00:00")
    )
    for path in seal_attestation_paths:
        attestation = load_json_strict(path)
        _validate_schema(attestation, ATTESTATION_SCHEMA_PATH)
        semantic_errors = validate_external_seal(attestation)
        if semantic_errors:
            raise ValueError("external seal attestation invalid: " + " | ".join(semantic_errors))
        if attestation["artifact_type"] != "BIG0F_SEAL_BUNDLE":
            raise ValueError("BIG 0F seal attestation must target BIG0F_SEAL_BUNDLE")
        if attestation["artifact_digest"] != bundle_digest:
            raise ValueError("external attestation does not match sealed bundle digest")
        sealed_at = __import__("datetime").datetime.fromisoformat(
            attestation["sealed_at"].replace("Z", "+00:00")
        )
        if sealed_at >= first_adjudication:
            raise ValueError("every external seal must precede first adjudication")
        verify_errors = verify_manifest(
            seal_manifest,
            attestation=attestation,
            component_paths=component_paths,
        )
        if verify_errors:
            raise ValueError("seal-bundle verification failed: " + " | ".join(verify_errors))
        authorities.add(attestation["authority_type"])
        attestation_ids.add(attestation["attestation_id"])

    required_authorities = {"THIRD_PARTY_TIMESTAMP_SERVICE", "PUBLIC_REGISTRY"}
    if not required_authorities.issubset(authorities):
        raise ValueError("BIG 0F requires both third-party timestamp and public-registry seals")
    if set(result["seal_attestation_ids"]) != attestation_ids:
        raise ValueError("pilot seal_attestation_ids do not exactly match verified attestations")

    threshold_digest = sha256_file(threshold_manifest_path)
    if threshold_digest != result["threshold_manifest_digest"]:
        raise ValueError("threshold manifest digest mismatch")
    adjudication_digest = sha256_file(adjudication_policy_path)
    if adjudication_digest != result["adjudication_policy_digest"]:
        raise ValueError("adjudication policy digest mismatch")
    nuisance_digest = sha256_file(nuisance_manifest_path)
    if nuisance_digest != result["nuisance_manifest_digest"]:
        raise ValueError("nuisance manifest digest mismatch")
    if seal_manifest["protocol_sha256"] != result["protocol_digest"]:
        raise ValueError("pilot protocol digest does not match sealed protocol")

    power = load_json_strict(power_analysis_path)
    _validate_schema(power, POWER_SCHEMA_PATH)
    if seal_manifest["power_engine_sha256"] != sha256_file(power_engine_path):
        raise ValueError("power engine is not the version committed by the seal")
    power_recompute_errors = verify_power_artifact(
        power,
        engine_sha256=sha256_file(power_engine_path),
    )
    if power_recompute_errors:
        raise ValueError("power artifact failed deterministic recomputation: " + " | ".join(power_recompute_errors))
    power_digest = sha256_file(power_analysis_path)
    if power_digest != result["power_metrics"]["power_analysis_digest"]:
        raise ValueError("power analysis digest mismatch")
    if power["power_analysis_id"] != result["power_metrics"]["power_analysis_artifact_id"]:
        raise ValueError("power analysis ID mismatch")
    for key in (
        "alpha",
        "target_power",
        "minimum_scientifically_meaningful_effect",
        "estimated_power",
        "required_confirmatory_disease_count",
        "required_high_specificity_positive_count",
    ):
        if power[key] != result["power_metrics"][key]:
            raise ValueError(f"power analysis value mismatch for {key}")

    return EvaluationContext(
        seal_verified=True,
        threshold_manifest_verified=True,
        power_analysis_verified=True,
        adjudication_policy_verified=True,
        nuisance_manifest_verified=True,
        decision_engine_sealed=True,
        pilot_schema_sealed=True,
        sampling_code_sealed=True,
    )


def main() -> int:
    ap = argparse.ArgumentParser(description="Evaluate BIG 0F GO/REDESIGN/NO_GO rules")
    ap.add_argument("pilot_result", type=Path)
    ap.add_argument("--protocol", type=Path, required=True)
    ap.add_argument("--disease-frame", type=Path, required=True)
    ap.add_argument("--randomness-beacon", type=Path, required=True)
    ap.add_argument("--threshold-manifest", type=Path, default=DEFAULT_THRESHOLD_PATH)
    ap.add_argument("--seal-bundle-manifest", type=Path, required=True)
    ap.add_argument("--seal-attestation", type=Path, action="append", required=True)
    ap.add_argument("--power-analysis", type=Path, required=True)
    ap.add_argument("--adjudication-policy", type=Path, required=True)
    ap.add_argument("--nuisance-manifest", type=Path, required=True)
    ap.add_argument("--sampling-code", type=Path, default=DEFAULT_SAMPLING_CODE_PATH)
    ap.add_argument("--power-engine", type=Path, default=DEFAULT_POWER_ENGINE_PATH)
    args = ap.parse_args()

    data = load_json_strict(args.pilot_result)
    _validate_schema(data, PILOT_SCHEMA_PATH)
    threshold_manifest = load_threshold_manifest(args.threshold_manifest)
    context = _verified_context_from_files(
        data,
        protocol_path=args.protocol,
        disease_frame_path=args.disease_frame,
        randomness_beacon_path=args.randomness_beacon,
        threshold_manifest_path=args.threshold_manifest,
        seal_bundle_manifest_path=args.seal_bundle_manifest,
        seal_attestation_paths=args.seal_attestation,
        power_analysis_path=args.power_analysis,
        adjudication_policy_path=args.adjudication_policy,
        nuisance_manifest_path=args.nuisance_manifest,
        sampling_code_path=args.sampling_code,
        power_engine_path=args.power_engine,
    )
    result = evaluate(data, threshold_manifest, context=context)

    declared = data["decision"]
    payload = {"decision": result.decision, "reasons": result.reasons}
    if declared != result.decision:
        payload["declared_decision"] = declared
        payload["error"] = "declared decision does not match frozen deterministic rules"
        print(json.dumps(payload, indent=2, allow_nan=False))
        return 2
    print(json.dumps(payload, indent=2, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
