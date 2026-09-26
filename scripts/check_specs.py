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

if errors:
    print("SPEC INTEGRITY CHECK FAILED")
    for err in errors:
        print(f"- {err}")
    sys.exit(1)

print("SPEC INTEGRITY CHECK PASSED")
