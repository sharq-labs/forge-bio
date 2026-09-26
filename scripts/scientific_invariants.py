from __future__ import annotations

from datetime import datetime, date
from typing import Any


def _parse_date(value: str) -> date:
    return date.fromisoformat(value[:10])


def _parse_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _wm_date(wm: Any) -> date | None:
    if not isinstance(wm, dict):
        return None
    if wm.get("kind") != "DATED":
        return None
    raw = wm.get("date")
    return _parse_date(raw) if isinstance(raw, str) else None


def validate_map(x: dict[str, Any]) -> list[str]:
    e: list[str] = []
    gov = x.get("governance", {})
    model = x.get("model", {})
    bench = x.get("benchmark", {})
    baselines = x.get("baselines", {})
    stats = x.get("statistics", {})
    gates = x.get("coverage_gates", {})

    if x.get("status") == "FROZEN":
        if not x.get("frozen_at") or not x.get("digest"):
            e.append("FROZEN MAP requires frozen_at and digest")

    if baselines.get("primary_comparator_id") != baselines.get("combined_nuisance_model_id"):
        e.append("primary comparator must be the Combined Nuisance Model")

    mode = x.get("policies", {}).get("scientific_operating_mode")
    if mode == "STRICT_HISTORICAL":
        wm = model.get("knowledge_watermark")
        if not isinstance(wm, dict):
            e.append("STRICT_HISTORICAL model requires typed knowledge watermark")
        elif wm.get("kind") == "UNKNOWN":
            e.append("STRICT_HISTORICAL refuses UNKNOWN model watermark")
        elif wm.get("kind") == "DATED":
            try:
                if _wm_date(wm) and _wm_date(wm) > _parse_date(bench["cutoff"]):
                    e.append("model watermark exceeds historical cutoff")
            except Exception:
                e.append("invalid cutoff/watermark date")

    tier = gov.get("study_tier")
    if tier in {"CONFIRMATORY", "PROSPECTIVE"}:
        ranking = set(gov.get("ranking_team") or [])
        adjud = gov.get("outcome_adjudication_role")
        cust = gov.get("lockbox_custodian_role")
        independents = set(gov.get("independent_adjudicator_ids") or [])
        if adjud in ranking:
            e.append("outcome adjudicator must be independent of ranking team")
        if cust in ranking:
            e.append("lockbox custodian must be independent of ranking team")
        if adjud and cust and adjud == cust:
            e.append("outcome adjudicator and lockbox custodian must be distinct")
        if ranking & independents:
            e.append("independent adjudicators may not be ranking-team members")
        if adjud in independents or cust in independents:
            e.append("independent adjudicator IDs must be distinct from named governance roles")
        if not gov.get("sealed_outcome_adjudicator_blinding_required"):
            e.append("confirmatory/prospective tier requires adjudicator blinding")
        if gov.get("validation_generation_status") != "ACTIVE":
            e.append("confirmatory/prospective tier requires ACTIVE validation generation")
        if gov.get("validation_max_disclosure_level") != "AGGREGATE_ONLY":
            e.append("confirmatory/prospective tier cannot begin after per-case/full-label disclosure")
        if not gov.get("external_seal_attestation_id"):
            e.append("confirmatory/prospective tier requires external seal attestation")
        if gov.get("permitted_lockbox_accesses", 99) > 1:
            e.append("confirmatory/prospective tier permits at most one lockbox opening")

        if gates.get("max_temporal_unknown_fraction", 1) >= 1:
            e.append("confirmatory max temporal UNKNOWN fraction is vacuous")
        if gates.get("max_novelty_ambiguity_fraction", 1) >= 1:
            e.append("confirmatory novelty ambiguity gate is vacuous")
        if gates.get("min_outcome_coverage_fraction", 0) <= 0:
            e.append("confirmatory outcome coverage gate is vacuous")

    if not isinstance(stats.get("alpha"), (int, float)) or not 0 < stats["alpha"] <= 0.1:
        e.append("alpha must be numeric in (0, 0.1]")
    if not isinstance(stats.get("power_target"), (int, float)) or stats["power_target"] < 0.8:
        e.append("power target must be at least 0.80")
    if not isinstance(stats.get("success_threshold_numeric"), (int, float)):
        e.append("success threshold must be numeric")

    return e


def validate_twin(x: dict[str, Any]) -> list[str]:
    e: list[str] = []
    mode = x.get("scientific_operating_mode")
    wm = x.get("knowledge_watermark")
    if mode in {"STRICT_HISTORICAL", "HISTORICAL_INPUT_MODERN_PRIOR"}:
        if not x.get("cutoff"):
            e.append("historical twin requires cutoff")
        if not isinstance(wm, dict):
            e.append("historical twin requires typed watermark")
        elif wm.get("kind") == "UNKNOWN":
            e.append("historical twin refuses UNKNOWN watermark")
        elif wm.get("kind") == "DATED":
            try:
                if _wm_date(wm) and _wm_date(wm) > _parse_date(x["cutoff"]):
                    e.append("twin watermark exceeds cutoff")
            except Exception:
                e.append("invalid twin cutoff/watermark date")

    maturity = x.get("maturity_level")
    if maturity in {"T3_VALIDATED_PREDICTIVE_TWIN", "T4_VALIDATED_INTERVENTION_SIMULATION_TWIN"}:
        if x.get("validation_verdict") != "PASS":
            e.append("T3/T4 requires PASS validation verdict")
        if x.get("credibility_conclusion") != "ADEQUATE_FOR_COU":
            e.append("T3/T4 requires ADEQUATE_FOR_COU credibility")
    if x.get("model_execution_kind") in {"NUMERICAL_DETERMINISTIC", "NUMERICAL_STOCHASTIC", "HYBRID"}:
        if not x.get("numerical_verification_artifact_id"):
            e.append("numerical twin requires numerical verification artifact")
    return e


def validate_effect_estimate(x: dict[str, Any]) -> list[str]:
    e: list[str] = []
    kind = x.get("effect_measure_kind")
    scale = x.get("scale")
    est = x.get("estimate")
    if kind in {"ODDS_RATIO", "RISK_RATIO", "HAZARD_RATIO"} and scale == "NATURAL":
        if not isinstance(est, (int, float)) or est <= 0:
            e.append("natural ratio effect estimate must be positive")
    lo, hi = x.get("confidence_interval_low"), x.get("confidence_interval_high")
    if lo is not None and hi is not None and lo > hi:
        e.append("confidence interval low exceeds high")
    if x.get("effect_context") == "GENETIC_ASSOCIATION":
        if x.get("effect_allele") == x.get("other_allele"):
            e.append("effect and other allele must differ")
    if kind == "HAZARD_RATIO":
        if not x.get("time_scale_ref") or not x.get("censoring_policy_ref"):
            e.append("hazard ratio requires time scale and censoring policy")
    return e


def validate_quantitative_observation(x: dict[str, Any]) -> list[str]:
    e: list[str] = []
    state = x.get("value_state")
    censored = {"BELOW_DETECTION", "ABOVE_DETECTION", "RIGHT_CENSORED", "LEFT_CENSORED", "INTERVAL_CENSORED"}
    if state in censored:
        if x.get("detection_limit") is None:
            e.append("censored/detection-limited observation requires detection limit")
        if x.get("value") is not None:
            e.append("censored/detection-limited observation cannot masquerade as observed numeric value")
    if state in {"MISSING", "NOT_APPLICABLE"} and x.get("value") is not None:
        e.append("missing/not-applicable observation cannot carry numeric value")
    if x.get("transform") == "Z_SCORE" and not x.get("normalization_artifact_id"):
        e.append("z-score requires normalization artifact")
    return e


def validate_extraction_quality_card(x: dict[str, Any]) -> list[str]:
    e: list[str] = []
    if x.get("qualification_status") == "QUALIFIED":
        if x.get("sample_size", 0) < x.get("minimum_sample_size_required", 10**9):
            e.append("qualified extractor sample size below frozen threshold")
        if x.get("precision", -1) < x.get("minimum_precision_required", 2):
            e.append("qualified extractor precision below frozen threshold")
        if x.get("recall", -1) < x.get("minimum_recall_required", 2):
            e.append("qualified extractor recall below frozen threshold")
        if not x.get("meets_qualification_thresholds"):
            e.append("qualified extractor must explicitly meet frozen thresholds")
    for metric in ("precision", "recall"):
        low = x.get(f"{metric}_ci_low")
        val = x.get(metric)
        if low is not None and val is not None and low > val:
            e.append(f"{metric} CI lower bound exceeds estimate")
    return e


def validate_numerical_verification(x: dict[str, Any]) -> list[str]:
    e: list[str] = []
    if x.get("verdict") == "ADEQUATE":
        typ = x.get("numerical_problem_type")
        if typ in {"CONTINUOUS_NUMERICAL", "STOCHASTIC_NUMERICAL", "HYBRID_NUMERICAL"}:
            if x.get("convergence_study_status") != "PASS":
                e.append("adequate numerical model requires convergence PASS")
            if x.get("numerical_error_estimate") is None:
                e.append("adequate numerical model requires numerical error estimate")
        tol = x.get("tolerances") or {}
        rt = tol.get("relative_tolerance")
        if isinstance(rt, (int, float)) and not 0 < rt <= 0.1:
            e.append("relative tolerance is not scientifically credible")
    return e


def validate_model_credibility(x: dict[str, Any]) -> list[str]:
    e: list[str] = []
    if x.get("conclusion") == "ADEQUATE_FOR_COU":
        required = (
            "model_discrepancy_assessment_id",
            "sensitivity_analysis_artifact_id",
            "transportability_assessment_id",
        )
        for key in required:
            if not x.get(key):
                e.append(f"adequate credibility requires {key}")
        high_stakes = x.get("model_influence") == "DOMINANT" or x.get("consequence_if_wrong") == "MISLEADING_SCIENTIFIC_CLAIM"
        if high_stakes and x.get("external_validation_status") not in {"EXTERNAL_SOURCE", "EXTERNAL_TEAM"}:
            e.append("dominant/misleading-claim CoU requires external validation for ADEQUATE_FOR_COU")
    return e


def validate_benchmark_exposure_ledger(x: dict[str, Any]) -> list[str]:
    e: list[str] = []
    if x.get("lifecycle_status") == "ACTIVE_CONFIRMATORY":
        for ev in x.get("exposure_events") or []:
            if ev.get("downstream_change_ref"):
                e.append("ACTIVE_CONFIRMATORY cannot survive evaluation-driven downstream change")
            if ev.get("audience_role") == "RANKING_TEAM" and ev.get("disclosure_level") in {"PER_CASE", "FULL_LABEL"}:
                e.append("ACTIVE_CONFIRMATORY cannot reveal per-case/full labels to ranking team")
    return e


def validate_external_seal(x: dict[str, Any]) -> list[str]:
    e: list[str] = []
    if x.get("verification_status") == "VERIFIED":
        if x.get("independence_from_study_team") is not True:
            e.append("verified external seal must be independent")
        if x.get("authority_type") not in {"INDEPENDENT_CUSTODIAN", "THIRD_PARTY_TIMESTAMP_SERVICE", "PUBLIC_REGISTRY"}:
            e.append("verified seal authority is not external")
        try:
            _parse_datetime(x["sealed_at"])
        except Exception:
            e.append("sealed_at is not a valid timestamp")
        if not x.get("verification_evidence_ref"):
            e.append("verified seal requires verification evidence")
    return e


def validate_research_program_attempt(x: dict[str, Any]) -> list[str]:
    e: list[str] = []
    try:
        _parse_datetime(x["registered_at"])
        _parse_datetime(x["disclosure_due_at"])
    except Exception:
        e.append("attempt registration/disclosure dates must be valid timestamps")
    if x.get("attempt_tier") in {"CONFIRMATORY", "PROSPECTIVE"} and not x.get("external_seal_attestation_id"):
        e.append("confirmatory/prospective attempt requires external seal")
    if x.get("disclosure_status") not in {"SCHEDULED", "PUBLIC"}:
        e.append("every attempt requires scheduled/public disclosure")
    return e


def validate_confirmatory_program_budget(x: dict[str, Any]) -> list[str]:
    e: list[str] = []
    allocations = x.get("generation_allocations") or []
    if len(allocations) > x.get("max_confirmatory_generations", 0):
        e.append("generation allocations exceed confirmatory-generation budget")
    total = sum(float(a.get("allocated_alpha", 0)) for a in allocations)
    if total > float(x.get("familywise_alpha", 0)) + 1e-12:
        e.append("allocated alpha exceeds familywise alpha budget")
    return e


VALIDATORS = {
    "map": validate_map,
    "scientific_twin": validate_twin,
    "effect_estimate": validate_effect_estimate,
    "quantitative_observation": validate_quantitative_observation,
    "extraction_quality_card": validate_extraction_quality_card,
    "numerical_verification": validate_numerical_verification,
    "model_credibility": validate_model_credibility,
    "benchmark_exposure_ledger": validate_benchmark_exposure_ledger,
    "external_seal": validate_external_seal,
    "research_program_attempt": validate_research_program_attempt,
    "confirmatory_program_budget": validate_confirmatory_program_budget,
}


def validate_semantics(kind: str, artifact: dict[str, Any]) -> list[str]:
    if kind not in VALIDATORS:
        raise KeyError(f"unknown scientific artifact kind: {kind}")
    return VALIDATORS[kind](artifact)
