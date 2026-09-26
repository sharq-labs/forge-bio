# ADR-003 — Knowledge Watermark vs Implementation Provenance

**Status:** Accepted — pre-code V1

## Decision

Biomedical knowledge time is independent from software creation time.

Every dependency declares KnowledgeBearingness:
- NON_KNOWLEDGE_BEARING
- KNOWLEDGE_BEARING
- UNKNOWN

KnowledgeWatermark is:
- NON_KNOWLEDGE_BEARING
- DATED(date)
- UNKNOWN

Generic algorithms may be written today and remain non-knowledge-bearing. Domain lists, rules, configs, pretrained models, ontologies, mappings, embeddings, and hindsight-informed features are knowledge-bearing.

## Consequences

STRICT_HISTORICAL refuses UNKNOWN and post-cutoff knowledge. Code commit/library/container data remain implementation provenance, not the biomedical watermark.


Genomic harmonization, liftover, reference-panel/LD derivations, feature preprocessing artifacts, and source-specific normalization are subject to the same watermark/provenance rule when knowledge-bearing.
