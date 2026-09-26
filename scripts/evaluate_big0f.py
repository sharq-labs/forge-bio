from __future__ import annotations

import argparse
import json
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

    assignment = metrics["assignment_metrics"]
    ambiguity = metrics["ambiguity_metrics"]
    provider = metrics["provider_metrics"]
    adjudication = metrics["adjudication_metrics"]
    power = metrics["power_metrics"]
    nuisance = metrics["nuisance_headroom_metrics"]
    independence = metrics["independence_metrics"]

    availability = provider["required_field_availability_fraction"]
    if availability < 0.70:
        no_go.append("required-field availability < 0.70")
    elif availability < 0.90:
        redesign.append("required-field availability is 0.70–<0.90")

    primary_ambiguity = max(
        ambiguity["novelty_ambiguity_fraction"],
        ambiguity["variant_harmonization_ambiguity_fraction"],
        ambiguity["phenotype_ambiguity_fraction"],
        ambiguity["sample_overlap_ambiguity_fraction"],
    )
    if primary_ambiguity > 0.40:
        no_go.append("primary endpoint ambiguity > 0.40")
    elif primary_ambiguity > 0.20:
        redesign.append("primary endpoint ambiguity is >0.20–0.40")

    agreement = min(
        adjudication["primary_assignment_agreement"],
        adjudication["phenotype_agreement"],
    )
    if agreement < 0.60:
        no_go.append("primary adjudication agreement < 0.60")
    elif agreement < 0.70:
        redesign.append("primary adjudication agreement is 0.60–<0.70")

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

    if provider["provider_coupling_risk"] in {"HIGH","UNKNOWN"}:
        redesign.append("provider coupling risk is HIGH/UNKNOWN")

    if independence["pre_t_cohort_reuse_fraction"] > 0.50:
        redesign.append("strict novelty is substantially exposed to pre-T cohort reuse")

    if nuisance["median_positive_rank_fraction"] <= 0.01:
        redesign.append("Combined Nuisance median positive already ranks in top 1%")

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
    print(json.dumps({"decision": result.decision, "reasons": result.reasons}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
