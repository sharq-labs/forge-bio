# ADR-018 — Evidence Extraction, Curation Quality, and Source-Grounded Claim Integrity

**Status:** Accepted — final pre-code hardening  
**Decision scope:** human, rule-based, ML, and LLM extraction of scientific claims/evidence

## Problem

A perfectly versioned source can still produce corrupted scientific evidence if the extraction layer is wrong.

Risks include:
- hallucinated or over-generalized claims;
- incorrect entity/relationship extraction;
- omitted negation or null results;
- source-span mismatch;
- extractor-version drift;
- low-quality human curation;
- duplicate claims from one source counted as independent evidence;
- confidence scores treated as truth.

## Decision

Every non-native structured extraction creates an ExtractionArtifact.

```text
ExtractionArtifact
    extraction_id
    source_artifact_id
    source_record_id
    source_locator_or_span

    extraction_method
    extractor_id
    extractor_version
    prompt_or_rule_config_hash?
    model_training_horizon?
    knowledge_watermark

    output_schema_version
    extracted_claim_ids
    abstention_state
    reviewer_state

    provenance
    digest
```

### Source grounding

ML/LLM/human extracted claims must resolve to a source locator/span sufficient for review.

An extracted statement without recoverable source grounding cannot become admissible EvidenceRecord in confirmatory work.

### Extraction quality

Each extractor/task family has an ExtractionQualityCard.

```text
ExtractionQualityCard
    extractor_id/version
    task_definition
    domain_scope
    gold_set_id
    sample_size
    precision
    recall
    false_positive_review
    false_negative_review
    abstention_rate
    inter_reviewer_agreement?
    known_failure_modes
    qualification_status
```

Quality is task/domain specific.

A good result on one evidence type does not qualify the extractor for another.

### Human curation

High-impact human curation records reviewer identity and adjudication policy.

Where independent review is required, disagreement is measured and unresolved disagreement remains explicit.

### Independence rule

Multiple extracted claims from one publication/database manifestation do not create independent evidence.

Extraction method changes representation; it does not create a new biological observation.

### Confidence rule

Extractor confidence/probability is a quality signal, not scientific truth and not biological evidence strength.

### Version drift

A material extractor/model/prompt/rule change creates a new extractor version and requires requalification for affected tasks.

## Consequences

- LLM extraction cannot silently become scientific truth;
- human curation is auditable;
- extraction errors can be measured separately from source quality;
- source grounding remains reviewable;
- extractor updates cannot inherit validation automatically.
