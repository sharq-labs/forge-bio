# ADR-006 — Outcome Gene Assignment and Historical Novelty

**Status:** Accepted — pre-code hardening  
**Decision scope:** B-TGT gene-level future outcomes

## Decision

A locus/variant-level genetic event and a gene-level validation event are different scientific objects.

A future disease-gene POSITIVE may not be created merely because a modern mapping system assigns a historical or post-cutoff locus to a gene.

Forge Bio introduces two governed components:

1. **OutcomeGeneAssignmentPolicy**
2. **HistoricalNoveltyAudit**

## OutcomeGeneAssignmentPolicy

Every gene-level genetic outcome records:

```text
source_locus_or_variant_event_id
assigned_gene_id
assignment_method
assignment_evidence
assignment_publicly_available_interval
assignment_knowledge_watermark
assignment_confidence
assignment_review_status
evaluation_bridge_version
```

Assignment methods may include direct coding/LoF evidence, experimentally supported mapping, contemporaneous fine-mapping/colocalization, or other benchmark-approved methods.

Modern learned L2G scores, current curated target knowledge, or other post-event knowledge-bearing assignments are not primary gene-level ground truth unless the benchmark explicitly labels the study contaminated/modern-prior.

Assignment-dependent positives are reported separately or sensitivity-tested.

## HistoricalNoveltyAudit

A candidate classified as E1-NOVEL must pass an evaluation-side audit for qualifying pre-T evidence.

The audit:
- may use sources unavailable to the ranker;
- must never feed those sources back into historical features;
- records search/source coverage and reviewer decision;
- returns NOVEL_CONFIRMED, KNOWN_AT_T, or NOVELTY_AMBIGUOUS.

NOVELTY_AMBIGUOUS is excluded or handled only by preregistered policy; it is never silently counted as novel.

## Consequences

- current identity reconciliation remains allowed for entity matching;
- identity reconciliation cannot create causal-gene evidence;
- gene assignment provenance becomes part of outcome provenance;
- locus-level and gene-level benchmarks may coexist but are never conflated.
