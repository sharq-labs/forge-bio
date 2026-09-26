#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []

required = [
    ROOT / "LICENSE",
    ROOT / ".github" / "CODEOWNERS",
    ROOT / "schemas" / "qoi.v1.schema.json",
    ROOT / "schemas" / "map.v1.schema.json",
    ROOT / "schemas" / "mar.v1.schema.json",
    ROOT / "schemas" / "scientific-twin.v1.schema.json",
    ROOT / "schemas" / "disease-profile.v1.schema.json",
    ROOT / "schemas" / "pathogen-profile.v1.schema.json",
    ROOT / "schemas" / "virus-profile-extension.v1.schema.json",
    ROOT / "schemas" / "pathogen-host-profile.v1.schema.json",
    ROOT / "schemas" / "therapeutic-profile.v1.schema.json",
    ROOT / "schemas" / "quantity-definition.v1.schema.json",
    ROOT / "schemas" / "quantitative-observation.v1.schema.json",
    ROOT / "schemas" / "effect-estimate.v1.schema.json",
    ROOT / "schemas" / "measurement-process.v1.schema.json",
    ROOT / "schemas" / "numerical-verification.v1.schema.json",
    ROOT / "schemas" / "model-credibility.v1.schema.json",
    ROOT / "schemas" / "extraction-artifact.v1.schema.json",
    ROOT / "schemas" / "extraction-quality-card.v1.schema.json",
    ROOT / "schemas" / "source-lifecycle-event.v1.schema.json",
    ROOT / "schemas" / "benchmark-exposure-ledger.v1.schema.json",
    ROOT / "schemas" / "external-seal-attestation.v1.schema.json",
    ROOT / "schemas" / "prediction-exposure-event.v1.schema.json",
    ROOT / "schemas" / "research-program-attempt.v1.schema.json",
    ROOT / "schemas" / "gene-model-release.v1.schema.json",
    ROOT / "schemas" / "confirmatory-program-budget.v1.schema.json",
    ROOT / "schemas" / "estimand.v1.schema.json",
    ROOT / "schemas" / "endpoint-quality-rule.v1.schema.json",
    ROOT / "schemas" / "seal-bundle-manifest.v1.schema.json",
    ROOT / "schemas" / "big0f-pilot-result.v1.schema.json",
    ROOT / "scripts" / "build_seal_bundle.py",
    ROOT / "scripts" / "evaluate_big0f.py",
    ROOT / "tests" / "spec" / "test_seal_bundle.py",
    ROOT / "tests" / "spec" / "test_big0f_decision.py",
    ROOT / "tests" / "spec" / "test_big0f_operational_contracts.py",
    ROOT / "docs" / "ENDPOINT_QUALITY_RULE.md",
    ROOT / "scripts" / "scientific_invariants.py",
    ROOT / "tests" / "spec" / "test_hostile_review_regressions.py",
    ROOT / "docs" / "BIG_0F_PROTOCOL.md",
    ROOT / "docs" / "adr" / "ADR-020-e1-primary-comparator-confirmatory-rule.md",
    ROOT / "docs" / "adr" / "ADR-021-big-0f-pilot-protocol.md",
    ROOT / "tests" / "spec" / "test_schema_contracts.py",
    ROOT / "schemas" / "big0f-threshold-manifest.v1.schema.json",
    ROOT / "schemas" / "big0f-adjudication-policy.v1.schema.json",
    ROOT / "schemas" / "big0f-nuisance-manifest.v1.schema.json",
    ROOT / "schemas" / "big0f-power-analysis.v1.schema.json",
    ROOT / "schemas" / "randomness-beacon.v1.schema.json",
    ROOT / "config" / "big0f-thresholds.v1.json",
    ROOT / "config" / "big0f-adjudication-policy.v1.json",
    ROOT / "config" / "big0f-nuisance-manifest.v1.json",
    ROOT / "scripts" / "select_big0f_sample.py",
    ROOT / "scripts" / "evaluate_endpoint_quality.py",
    ROOT / "scripts" / "validate_research_program.py",
    ROOT / "scripts" / "simulate_big0f_power.py",
    ROOT / "tests" / "spec" / "test_endpoint_quality_executor.py",
    ROOT / "tests" / "spec" / "test_research_program_validator.py",
    ROOT / "tests" / "spec" / "test_round2_hostile_regressions.py",
]
for path in required:
    if not path.exists():
        errors.append(f"missing required file: {path.relative_to(ROOT)}")

for path in sorted((ROOT / "schemas").glob("*.json")):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"invalid JSON schema {path.relative_to(ROOT)}: {exc}")
        continue
    if data.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        errors.append(f"{path.relative_to(ROOT)} must declare JSON Schema 2020-12")
    if data.get("type") != "object":
        errors.append(f"{path.relative_to(ROOT)} top-level type must be object")
    if data.get("additionalProperties") is not False:
        errors.append(f"{path.relative_to(ROOT)} must reject unknown top-level fields")

link_re = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
for path in sorted(ROOT.rglob("*.md")):
    text = path.read_text(encoding="utf-8")
    for raw in link_re.findall(text):
        target = raw.strip().split("#", 1)[0]
        if not target or target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        resolved = (path.parent / target).resolve()
        try:
            resolved.relative_to(ROOT)
        except ValueError:
            errors.append(f"{path.relative_to(ROOT)} links outside repository: {raw}")
            continue
        if not resolved.exists():
            errors.append(f"broken local link in {path.relative_to(ROOT)}: {raw}")

for path in sorted((ROOT / "docs" / "adr").glob("ADR-*.md")):
    text = path.read_text(encoding="utf-8")
    m = re.search(r"\*\*Status:\*\*\s*([^\n]+)", text)
    if not m:
        errors.append(f"ADR missing status: {path.relative_to(ROOT)}")
        continue
    status = m.group(1).strip()
    if status.startswith("Proposed") or status.startswith("OPEN"):
        errors.append(f"unresolved ADR status in {path.relative_to(ROOT)}: {status}")

legacy_re = re.compile(r"\bE1-NOVEL\b(?!-STRICT)")
for path in sorted((ROOT / "docs").rglob("*.md")):
    text = path.read_text(encoding="utf-8")
    if legacy_re.search(text):
        errors.append(f"legacy E1-NOVEL wording in {path.relative_to(ROOT)}")

checklist = (ROOT / "docs" / "PRE_CODE_CHECKLIST.md").read_text(encoding="utf-8")
if "- [x] ADR-005 licensing posture decided" not in checklist:
    errors.append("PRE_CODE_CHECKLIST must record ADR-005 as decided")



# Scientific twin claim-boundary checks
twin_arch = (ROOT / "docs" / "SCIENTIFIC_DIGITAL_TWIN_ARCHITECTURE.md").read_text(encoding="utf-8")
for required_phrase in [
    "T0_PROFILE_ONLY",
    "T3_VALIDATED_PREDICTIVE_TWIN",
    "T4_VALIDATED_INTERVENTION_SIMULATION_TWIN",
    "Patient-specific twins are excluded from V1.",
]:
    if required_phrase not in twin_arch:
        errors.append(f"scientific twin architecture missing required claim boundary: {required_phrase}")

# BIG 0R5 credibility/quantitative contract checks
for required_doc in [
    ROOT / "docs" / "MODEL_CREDIBILITY_POLICY.md",
    ROOT / "docs" / "QUANTITATIVE_SEMANTICS.md",
    ROOT / "docs" / "adr" / "ADR-016-model-credibility-numerical-verification.md",
    ROOT / "docs" / "adr" / "ADR-017-quantitative-semantics.md",
]:
    if not required_doc.exists():
        errors.append(f"missing R5 scientific contract: {required_doc.relative_to(ROOT)}")


# Evidence extraction assurance checks
for required_doc in [
    ROOT / "docs" / "EVIDENCE_EXTRACTION_POLICY.md",
    ROOT / "docs" / "adr" / "ADR-018-evidence-extraction-quality.md",
]:
    if not required_doc.exists():
        errors.append(f"missing extraction assurance contract: {required_doc.relative_to(ROOT)}")



# Research-program lifecycle integrity checks
for required_doc in [
    ROOT / "docs" / "BENCHMARK_LIFECYCLE_POLICY.md",
    ROOT / "docs" / "adr" / "ADR-019-source-benchmark-lifecycle.md",
]:
    if not required_doc.exists():
        errors.append(f"missing lifecycle integrity contract: {required_doc.relative_to(ROOT)}")


# BIG 0F-0 critical-path checks
benchmark_spec = (ROOT / "docs" / "BENCHMARK_V0_SPEC.md").read_text(encoding="utf-8")
for phrase in [
    "Combined Nuisance Model",
    "AUTHOR_NAMED",
    "DEVELOPMENT_EXPOSED",
]:
    if phrase not in benchmark_spec:
        errors.append(f"benchmark spec missing BIG 0F-0 contract: {phrase}")

audit = (ROOT / "docs" / "PLAN_STRENGTH_AUDIT.md").read_text(encoding="utf-8")
if "No currently known major architecture/specification gap remains" in audit:
    errors.append("PLAN_STRENGTH_AUDIT still contains superseded no-known-gap conclusion")



# BIG 0F operational-prep contract checks
estimand_doc = (ROOT / "docs" / "BENCHMARK_ESTIMAND_V0.md").read_text(encoding="utf-8")
if "STRUCTURE FROZEN" not in estimand_doc:
    errors.append("B-TGT-E1 estimand structure must remain explicitly frozen")

endpoint_doc = (ROOT / "docs" / "ENDPOINT_QUALITY_RULE.md").read_text(encoding="utf-8")
if "STRUCTURE FROZEN / VALUES EMPIRICAL-OPEN" not in endpoint_doc:
    errors.append("endpoint-quality rule must separate frozen structure from empirical threshold values")

for phrase in [
    "Local canonical seal-bundle build/verify/tamper dry run is executable and tested.",
    "BIG 0F GO/REDESIGN/NO_GO decision rules are executable and deterministic.",
]:
    if phrase not in checklist:
        errors.append(f"readiness checklist missing operational-prep closure: {phrase}")



# Round 2 hostile-review closure checks
round2_required_phrases = {
    ROOT / "docs" / "BIG_0F_PROTOCOL.md": [
        "NUISANCE_ONLY",
        "E1-NOVEL-STRICT",
        "EVENT_RANK_PERCENTILE_V1",
        "public randomness-beacon",
    ],
    ROOT / "docs" / "adr" / "ADR-020-e1-primary-comparator-confirmatory-rule.md": [
        "HYPOTHESIS_FREE_CODING_OR_LOF",
        "disease-specific attention",
        "EVENT_RANK_PERCENTILE_V1",
    ],
    ROOT / "docs" / "EXTERNAL_SEAL_RUNBOOK.md": [
        "frame_seal_attestation_sha256",
        "decision_engine_sha256",
        "sampling_code_sha256",
        "power_engine_sha256",
    ],
}
for path, phrases in round2_required_phrases.items():
    text = path.read_text(encoding="utf-8")
    for phrase in phrases:
        if phrase not in text:
            errors.append(f"{path.relative_to(ROOT)} missing Round 2 contract phrase: {phrase}")

nuisance = json.loads((ROOT / "config" / "big0f-nuisance-manifest.v1.json").read_text(encoding="utf-8"))
for family in [
    "DISEASE_SPECIFIC_ATTENTION_VOLUME",
    "DISEASE_SPECIFIC_ATTENTION_MOMENTUM",
]:
    if family not in nuisance.get("mandatory_feature_families", []):
        errors.append(f"BIG 0F nuisance manifest missing mandatory family: {family}")
if nuisance.get("pilot_model_evaluation_mode") != "NUISANCE_ONLY":
    errors.append("BIG 0F pilot must remain NUISANCE_ONLY")

adjudication = json.loads((ROOT / "config" / "big0f-adjudication-policy.v1.json").read_text(encoding="utf-8"))
if adjudication.get("other_high_specificity_method_allowed") is not False:
    errors.append("BIG 0F V0 may not reopen OTHER_HIGH_SPECIFICITY_METHOD")
if adjudication.get("primary_metric_id") != "EVENT_RANK_PERCENTILE_V1":
    errors.append("BIG 0F V0 primary metric drifted from EVENT_RANK_PERCENTILE_V1")

thresholds = json.loads((ROOT / "config" / "big0f-thresholds.v1.json").read_text(encoding="utf-8"))
if thresholds.get("thresholds", {}).get("alpha") != 0.05:
    errors.append("BIG 0F alpha must remain frozen at 0.05")

if errors:
    print("SPEC INTEGRITY CHECK FAILED")
    for err in errors:
        print(f"- {err}")
    sys.exit(1)

print("SPEC INTEGRITY CHECK PASSED")


