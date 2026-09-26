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
        if mode != "STRICT_HISTORICAL":
            e.append("confirmatory/prospective MAP requires STRICT_HISTORICAL operating mode")
        fidelity = x.get("providers", {}).get("reconstruction_fidelity_verdicts") or []
        if any(v not in {"PASS", "NOT_APPLICABLE"} for v in fidelity):
            e.append("confirmatory/prospective MAP requires PASS/NOT_APPLICABLE reconstruction fidelity")
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
        required_nuisance = {
            "DISEASE_SPECIFIC_ATTENTION_VOLUME",
            "DISEASE_SPECIFIC_ATTENTION_MOMENTUM",
            "GENE_LENGTH",
            "LD_ARCHITECTURE",
            "CROSS_TRAIT_PLEIOTROPY",
            "GENETIC_OBSERVABILITY",
            "DISEASE_SAMPLE_SIZE_TRAJECTORY",
        }
        observed_nuisance = set(baselines.get("nuisance_feature_family_ids") or [])
        missing_nuisance = sorted(required_nuisance - observed_nuisance)
        if missing_nuisance:
            e.append("confirmatory Combined Nuisance missing mandatory families: " + ",".join(missing_nuisance))
        if not str(baselines.get("combined_nuisance_model_id", "")).startswith("CNM-"):
            e.append("combined nuisance model ID must identify a CNM artifact")
        comparison = x.get("comparison_design", {})
        if comparison.get("capacity_parity_required") is not True:
            e.append("confirmatory primary comparison requires capacity parity")
        for key in (
            "learner_family_id",
            "nuisance_feature_block_digest",
            "preprocessing_artifact_id",
            "hyperparameter_search_space_digest",
            "tuning_budget_id",
            "early_stopping_policy_id",
            "random_seed_policy_id",
        ):
            if not comparison.get(key):
                e.append(f"confirmatory comparison missing {key}")
        if gov.get("permitted_lockbox_accesses", 99) > 1:
            e.append("confirmatory/prospective tier permits at most one lockbox opening")

        if gates.get("max_temporal_unknown_fraction", 1) >= 1:
            e.append("confirmatory max temporal UNKNOWN fraction is vacuous")
        if gates.get("max_novelty_ambiguity_fraction", 1) >= 1:
            e.append("confirmatory novelty ambiguity gate is vacuous")
        if gates.get("min_outcome_coverage_fraction", 0) <= 0:
            e.append("confirmatory outcome coverage gate is vacuous")

    if not isinstance(stats.get("alpha"), (int, float)) or stats["alpha"] != 0.05:
        e.append("confirmatory alpha must equal frozen 0.05")
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
        events = x.get("exposure_events") or []
        aggregate_count = 0
        subgroup_count = 0
        for ev in events:
            if ev.get("downstream_change_ref"):
                e.append("ACTIVE_CONFIRMATORY cannot survive evaluation-driven downstream change")
            if ev.get("disclosure_level") in {"PER_CASE", "FULL_LABEL"}:
                e.append("ACTIVE_CONFIRMATORY cannot reveal per-case/full labels to any audience")
            if ev.get("exposure_kind") == "LABEL_REVEAL":
                e.append("ACTIVE_CONFIRMATORY cannot contain a label-reveal event")
            if ev.get("disclosure_level") == "AGGREGATE_ONLY":
                aggregate_count += 1
            if ev.get("disclosure_level") == "SUBGROUP":
                subgroup_count += 1
        if not x.get("external_seal_attestation_id"):
            e.append("ACTIVE_CONFIRMATORY requires an external seal")
        if aggregate_count > x.get("max_aggregate_disclosures", -1):
            e.append("aggregate disclosure count exceeds frozen active-generation budget")
        if subgroup_count > x.get("max_subgroup_disclosures", -1):
            e.append("subgroup disclosure count exceeds frozen active-generation budget")
    return e


def validate_external_seal(x: dict[str, Any]) -> list[str]:
    e: list[str] = []
    if x.get("verification_status") != "VERIFIED":
        e.append("claim-valid external seal must be VERIFIED")
        return e
    if x.get("independence_from_study_team") is not True:
        e.append("verified external seal must be independent")
    authority = x.get("authority_type")
    method = x.get("attestation_method")
    expected = {
        "INDEPENDENT_CUSTODIAN": "SIGNED_CUSTODIAN_ATTESTATION",
        "THIRD_PARTY_TIMESTAMP_SERVICE": "THIRD_PARTY_TIMESTAMP",
        "PUBLIC_REGISTRY": "PUBLIC_PREREGISTRATION",
    }
    if authority not in expected:
        e.append("verified seal authority is not recognized")
    elif method != expected[authority]:
        e.append("attestation method does not match authority type")
    try:
        sealed = _parse_datetime(x["sealed_at"])
        verified = _parse_datetime(x["verified_at"])
        if sealed > verified:
            e.append("sealed_at cannot be later than verified_at")
    except Exception:
        e.append("seal timestamps are invalid")
    if not x.get("verification_evidence_ref") or not x.get("independence_evidence_ref"):
        e.append("verified seal requires verification and independence evidence")
    digest = x.get("artifact_digest", "")
    if not isinstance(digest, str) or len(digest) != 71 or not digest.startswith("sha256:"):
        e.append("external seal requires a full sha256 digest")
    return e


def validate_research_program_attempt(x: dict[str, Any]) -> list[str]:
    e: list[str] = []
    try:
        registered = _parse_datetime(x["registered_at"])
        result_time = _parse_datetime(x["result_recorded_at"])
        disclosure_due = _parse_datetime(x["disclosure_due_at"])
        if registered > result_time:
            e.append("research attempt must be registered before result recording")
        if result_time > disclosure_due:
            e.append("disclosure due date cannot precede result recording")
    except Exception:
        e.append("attempt registration/result/disclosure dates must be valid timestamps")
    if x.get("research_program_id") != "FORGE-BIO-B-TGT-E1-V0":
        e.append("attempt must belong to the fixed Forge Bio B-TGT-E1 research program")
    if x.get("attempt_tier") in {"CONFIRMATORY", "PROSPECTIVE"}:
        if not x.get("external_seal_attestation_id"):
            e.append("confirmatory/prospective attempt requires external seal")
        if x.get("confirmatory_program_budget_id") != "CPB-FORGE-BIO-B-TGT-E1-V0":
            e.append("confirmatory/prospective attempt must link the single program-wide budget")
        if not x.get("allocation_generation_id"):
            e.append("confirmatory/prospective attempt requires an allocation generation")
        if not isinstance(x.get("allocated_alpha"), (int, float)) or not 0 < x["allocated_alpha"] <= 0.05:
            e.append("confirmatory/prospective attempt requires allocated alpha in (0, 0.05]")
    if x.get("disclosure_status") not in {"SCHEDULED", "PUBLIC"}:
        e.append("every attempt requires scheduled/public disclosure")
    return e


def validate_confirmatory_program_budget(x: dict[str, Any]) -> list[str]:
    e: list[str] = []
    allocations = x.get("generation_allocations") or []
    if x.get("research_program_id") != "FORGE-BIO-B-TGT-E1-V0":
        e.append("confirmatory budget research_program_id is not the canonical program")
    if x.get("budget_id") != "CPB-FORGE-BIO-B-TGT-E1-V0":
        e.append("confirmatory budget ID is not canonical")
    if x.get("familywise_alpha") != 0.05:
        e.append("familywise alpha must equal 0.05")
    if len(allocations) > x.get("max_confirmatory_generations", 0):
        e.append("generation allocations exceed confirmatory-generation budget")
    generation_ids = [a.get("generation_id") for a in allocations]
    if len(generation_ids) != len(set(generation_ids)):
        e.append("generation IDs must be unique within the program-wide alpha budget")
    total = sum(float(a.get("allocated_alpha", 0)) for a in allocations)
    if total > 0.05 + 1e-12:
        e.append("allocated alpha exceeds the single program-wide 0.05 budget")
    return e


def validate_research_program_ledger(x: dict[str, Any]) -> list[str]:
    e: list[str] = []
    if x.get("research_program_id") != "FORGE-BIO-B-TGT-E1-V0":
        e.append("research-program ledger must use the canonical program ID")
    if x.get("confirmatory_program_budget_id") != "CPB-FORGE-BIO-B-TGT-E1-V0":
        e.append("research-program ledger must link the canonical confirmatory budget")
    attempts = x.get("attempts") or []
    attempt_ids = [a.get("attempt_id") for a in attempts]
    attempt_indexes = [a.get("attempt_index") for a in attempts]
    if len(attempt_ids) != len(set(attempt_ids)):
        e.append("research-program attempt IDs must be unique")
    if len(attempt_indexes) != len(set(attempt_indexes)):
        e.append("research-program attempt indexes must be unique")
    confirmatory = [a for a in attempts if a.get("attempt_tier") in {"CONFIRMATORY", "PROSPECTIVE"}]
    generations = [a.get("allocation_generation_id") for a in confirmatory]
    if len(generations) != len(set(generations)):
        e.append("confirmatory/prospective attempts may not reuse one allocation generation as independent attempts")
    alpha = sum(float(a.get("allocated_alpha") or 0) for a in confirmatory)
    if alpha > 0.05 + 1e-12:
        e.append("research-program ledger spends more than the single 0.05 alpha budget")
    if len(generations) > 2:
        e.append("research-program ledger exceeds maximum confirmatory generations")
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
    "research_program_ledger": validate_research_program_ledger,
}


def validate_semantics(kind: str, artifact: dict[str, Any]) -> list[str]:
    if kind not in VALIDATORS:
        raise KeyError(f"unknown scientific artifact kind: {kind}")
    return VALIDATORS[kind](artifact)
