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
    ROOT / "scripts" / "scientific_invariants.py",
    ROOT / "tests" / "spec" / "test_hostile_review_regressions.py",
    ROOT / "docs" / "BIG_0F_PROTOCOL.md",
    ROOT / "docs" / "adr" / "ADR-020-e1-primary-comparator-confirmatory-rule.md",
    ROOT / "docs" / "adr" / "ADR-021-big-0f-pilot-protocol.md",
    ROOT / "tests" / "spec" / "test_schema_contracts.py",
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

if errors:
    print("SPEC INTEGRITY CHECK FAILED")
    for err in errors:
        print(f"- {err}")
    sys.exit(1)

print("SPEC INTEGRITY CHECK PASSED")


