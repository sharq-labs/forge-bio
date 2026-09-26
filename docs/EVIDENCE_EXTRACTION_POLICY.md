# Evidence Extraction Quality Policy

**Status:** NORMATIVE PRE-CODE V1

## 1. Principle

Scientific evidence quality and extraction quality are different.

```text
high-quality source
+
bad extraction
=
bad EvidenceRecord
```

## 2. Admission path

```text
SourceArtifact
→ SourceRecord
→ ExtractionArtifact
→ identity/context resolution
→ ScientificClaim
→ EvidenceRecord
```

NATIVE_STRUCTURED sources may skip text extraction but still retain provider-field provenance.

## 3. Required source grounding

For literature/regulatory/guideline text extraction:
- source artifact ID;
- record/document ID;
- page/section/paragraph/span locator where feasible;
- extracted text span hash or stable locator;
- extractor version/config.

The full source need not be reproduced in derived artifacts when licensing prohibits it.

## 4. Qualification

ExtractionQualityCard qualification states:

```text
QUALIFIED
CONDITIONAL
UNQUALIFIED
UNKNOWN
```

UNKNOWN and UNQUALIFIED extraction is refused for confirmatory evidence generation.

CONDITIONAL requires the frozen condition, such as mandatory human review.

## 5. Gold sets

Gold sets are versioned and separated from evaluation sources where practical.

Report task-specific:
- precision;
- recall;
- class/relationship-specific errors;
- negation/null-result errors;
- entity-resolution errors;
- source-grounding errors;
- abstention rate.

Aggregate F1 alone is insufficient for high-impact extraction.

## 6. Human review

Human-reviewed workflows record:
- reviewer;
- review status;
- disagreement;
- adjudication;
- changes from machine output.

Human review does not erase the original machine extraction provenance.

## 7. Temporal semantics

Knowledge-bearing extraction models/rules carry KnowledgeWatermark.

A modern extractor may structure an old publication for evaluation/current use, but its derived structure is not automatically historical model-visible knowledge.

## 8. Circularity and duplication

Extracted model outputs cannot cite other Forge Bio predictions as independent source evidence.

Multiple claims extracted from the same originating observation retain the same IndependenceFamily/source lineage.

## 9. Change control

Material changes to:
- model;
- training data;
- prompt;
- rules;
- ontology;
- output schema

create a new extractor version and trigger task-specific requalification.

## 10. Stop rule

Do not scale automated extraction into a benchmark/provider pipeline if:
- source-grounding failure is material;
- negation/null-result error is unacceptable;
- high-impact false positives remain uncontrolled;
- required recall cannot be achieved without unbounded manual burden.
