from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Decision:
    decision: str
    reasons: tuple[str, ...]


def evaluate(metrics: dict[str, Any]) -> Decision:
    no_go: list[str] = []
    redesign: list[str] = []
    inconclusive: list[str] = []

    assignment = metrics["assignment_metrics"]
    ambiguity = metrics["ambiguity_metrics"]
    provider = metrics["provider_metrics"]
    adjudication = metrics["adjudication_metrics"]
    power = metrics["power_metrics"]
    nuisance = metrics["nuisance_headroom_metrics"]
    independence = metrics["independence_metrics"]
    applicability = metrics["applicability_metrics"]
    curation = metrics["curation_metrics"]

    if metrics.get("threshold_sensitivity_stable") is not True:
        inconclusive.append("GO/REDESIGN/NO_GO conclusion is unstable under plausible sealed threshold sensitivity")

    component_ambiguity = max(
        ambiguity["novelty_ambiguity_fraction"],
        ambiguity["variant_harmonization_ambiguity_fraction"],
        ambiguity["phenotype_ambiguity_fraction"],
        ambiguity["sample_overlap_ambiguity_fraction"],
    )
    primary_ambiguity = ambiguity["any_primary_endpoint_ambiguity_fraction"]
    if primary_ambiguity + 1e-12 < component_ambiguity:
        inconclusive.append("union primary-endpoint ambiguity is smaller than a component ambiguity fraction")
    if primary_ambiguity > 0.40:
        no_go.append("fraction ambiguous on any primary endpoint dimension > 0.40")
    elif primary_ambiguity > 0.20:
        redesign.append("fraction ambiguous on any primary endpoint dimension is >0.20–0.40")

    total_cases = adjudication["adjudicated_event_case_count"]
    duplicate_count = adjudication["duplicate_review_count"]
    duplicate_fraction = adjudication["duplicate_review_fraction"]
    if total_cases > 0:
        computed_fraction = duplicate_count / total_cases
        if abs(computed_fraction - duplicate_fraction) > 1e-9:
            inconclusive.append("duplicate_review_fraction is inconsistent with duplicate review count")
        required_duplicate_count = min(total_cases, max(30, math.ceil(0.30 * total_cases)))
        if duplicate_count < required_duplicate_count:
            inconclusive.append(
                f"independent duplicate review incomplete: {duplicate_count} < required {required_duplicate_count}"
            )

    agreement = min(
        adjudication["primary_assignment_agreement"],
        adjudication["phenotype_agreement"],
    )
    if agreement < 0.60:
        no_go.append("primary adjudication agreement < 0.60")
    elif agreement < 0.70:
        redesign.append("primary adjudication agreement is 0.60–<0.70")

    availability = provider["required_field_availability_fraction"]
    if availability < 0.70:
        no_go.append("required-field availability < 0.70")
    elif availability < 0.90:
        redesign.append("required-field availability is 0.70–<0.90")

    if provider["provider_coupling_risk"] == "UNKNOWN":
        inconclusive.append("provider coupling risk remains UNKNOWN")
    elif provider["provider_coupling_risk"] == "HIGH":
        redesign.append("provider coupling risk is HIGH")

    ancestry = applicability["ancestry_population_metadata_adequacy"]
    if ancestry == "UNKNOWN":
        inconclusive.append("ancestry/population metadata adequacy remains UNKNOWN")
    elif ancestry == "INADEQUATE":
        redesign.append("ancestry/population metadata is inadequate for intended primary interpretation")

    burden = curation["retrospective_curation_burden_assessment"]
    if burden == "UNKNOWN":
        inconclusive.append("retrospective curation burden remains UNKNOWN")
    elif burden == "EXCESSIVE":
        redesign.append("retrospective curation burden is excessive")

    if curation["symmetric_non_event_audit_complete"] is not True:
        inconclusive.append("symmetric non-event historical audit is incomplete")
    expected_non_event = min(100, max(50, total_cases))
    if curation["non_event_case_count"] < expected_non_event:
        inconclusive.append(
            f"symmetric non-event audit sample too small: {curation['non_event_case_count']} < required {expected_non_event}"
        )

    if power["estimated_power"] < power["target_power"] or power["estimated_power"] < 0.80:
        no_go.append("estimated confirmatory power below target / 0.80")

    if metrics.get("untouched_confirmatory_disease_count", 0) <= 0:
        no_go.append("no untouched confirmatory disease pool remains")

    if metrics.get("high_specificity_positive_count", 0) <= 0:
        no_go.append("no high-specificity primary positive events remain")

    if (
        assignment["author_named_fraction"] + assignment["nearest_gene_fraction"]
        > 0.50
    ):
        redesign.append("author-named + nearest-gene assignment fraction > 0.50")

    if abs(assignment["attention_assignment_association"]) > 0.30:
        redesign.append("attention/assignment association exceeds default 0.30 redesign threshold")

    if assignment["primary_eligible_fraction"] < 0.50:
        redesign.append("primary-eligible high-specificity assignment fraction < 0.50")

    if independence["pre_t_cohort_reuse_fraction"] > 0.50:
        redesign.append("strict novelty is substantially exposed to pre-T cohort reuse")

    if nuisance["median_positive_rank_fraction"] <= 0.01:
        redesign.append("Combined Nuisance median positive already ranks in top 1%")

    if inconclusive:
        return Decision("INCONCLUSIVE", tuple(inconclusive + no_go + redesign))
    if no_go:
        return Decision("NO_GO", tuple(no_go + redesign))
    if redesign:
        return Decision("REDESIGN", tuple(redesign))
    return Decision("GO", ("all frozen GO gates passed",))


def main() -> int:
    ap = argparse.ArgumentParser(description="Evaluate BIG 0F GO/REDESIGN/NO_GO rules")
    ap.add_argument("pilot_result", type=Path)
    args = ap.parse_args()
    data = json.loads(args.pilot_result.read_text(encoding="utf-8"))
    result = evaluate(data)
    declared = data.get("decision")
    payload = {"decision": result.decision, "reasons": result.reasons}
    if declared is not None and declared != result.decision:
        payload["declared_decision"] = declared
        payload["error"] = "declared decision does not match frozen deterministic rules"
        print(json.dumps(payload, indent=2))
        return 2
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
