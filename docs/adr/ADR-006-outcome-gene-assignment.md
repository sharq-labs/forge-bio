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

Assignment methods are classified explicitly.

Primary-eligible classes may include only preregistered high-specificity methods such as:

```text
DIRECT_CODING_OR_LOF
HIGH_CONFIDENCE_FINE_MAPPING
PREREGISTERED_COLOCALIZATION
OTHER_HIGH_SPECIFICITY_METHOD
```

The exact evidentiary threshold for each class is frozen after BIG 0F feasibility work and before confirmatory evaluation.

The following are not primary-eligible by themselves:

```text
AUTHOR_NAMED
NEAREST_GENE
POSITIONAL_PROXIMITY_ONLY
GENERIC_DATABASE_GENE_FIELD
MODERN_L2G_ONLY
CURRENT_CURATED_TARGET_ONLY
```

Author naming or nearest-gene assignment may be preserved as provenance/sensitivity labels, but cannot independently create a primary disease–gene positive.

Modern learned L2G scores, current curated target knowledge, or other post-event knowledge-bearing assignments are not primary gene-level ground truth unless the benchmark explicitly labels the study contaminated/modern-prior.

Assignment-dependent positives are stratified by assignment class.

BIG 0F must measure:
- assignment-class shares;
- author-named and nearest-gene fractions;
- correlation of assigned-gene pre-T attention rank with assignment class;
- event yield after keeping only primary-eligible high-specificity assignments;
- locus-level one-credit sensitivity.

If primary-eligible gene assignments are too sparse or remain materially attention-coupled, the benchmark must REDESIGN to a locus-level or otherwise attention-resistant primary endpoint rather than relaxing the assignment rule.

## HistoricalNoveltyAudit

A candidate classified as E1-NOVEL-STRICT must pass an evaluation-side HistoricalNoveltyAudit and satisfy the ADR-012 historical-search-coverage threshold.

The audit:
- may use sources unavailable to the ranker;
- must never feed those sources back into historical features;
- records search/source coverage and reviewer decision;
- returns NOVEL_CONFIRMED, KNOWN_AT_T, or NOVELTY_AMBIGUOUS, while separately recording KNOWN_TO_RANKER_AT_T vs KNOWN_PUBLICLY_AT_T.

NOVELTY_AMBIGUOUS is excluded or handled only by preregistered policy; it is never silently counted as novel.

## Consequences

- current identity reconciliation remains allowed for entity matching;
- identity reconciliation cannot create causal-gene evidence;
- gene assignment provenance becomes part of outcome provenance;
- locus-level and gene-level benchmarks may coexist but are never conflated.


Genomic locus/variant identity and harmonization are governed by ADR-011. Historical search coverage and observability are governed by ADR-012.


## Attention-circularity rule

Gene assignment is part of the outcome definition and therefore a possible source of label circularity.

A label path such as:

```text
pre-T literature attention
    → famous gene
    → discovery paper names famous gene
    → Forge Bio receives positive credit
```

is not accepted as evidence of biological predictive value.

Primary interpretation therefore requires the ADR-020 assignment-attention audit and Combined Nuisance comparator.

Normative amendment:
- [ADR-020 — E1 Primary Gene Endpoint, Nuisance Comparator, and Confirmatory Decision Rule](ADR-020-e1-primary-comparator-confirmatory-rule.md)
