# ADR-009 — Genetic Replication and Pre-T Signal State

**Status:** Accepted — pre-code hardening  
**Decision scope:** B-TGT-E1 novelty, maturation, and replication semantics

## Problem

"No qualifying pre-T genetics" is too weak to mean novel.

A pre-T suggestive association may become genome-wide significant after a larger study. Counting that as de novo discovery confounds biological anticipation with statistical-power maturation.

Likewise, a later study is not necessarily a replication merely because it reports the same gene or locus.

## Decision A — Pre-T genetic state

Every disease-gene candidate relevant to E1 is assigned a `PreTGeneticState` under the frozen historical-audit policy:

```text
NO_SIGNAL_OBSERVED
SUGGESTIVE
QUALIFYING
AMBIGUOUS
```

`NO_SIGNAL_OBSERVED` means no relevant genetic signal was found after the preregistered audit with adequate coverage. It does not claim proof that no signal existed anywhere.

## Decision B — endpoint subtype refinement

### E1-NOVEL-STRICT

Requires:

```text
PreTGeneticState = NO_SIGNAL_OBSERVED
+
HistoricalNoveltyAudit = NOVEL_CONFIRMED
+
qualifying post-T event
```

### E1-MATURATION

Requires:

```text
PreTGeneticState = SUGGESTIVE
+
post-T evidence crosses the qualifying endpoint
```

This is evidence/statistical maturation, not de novo discovery.

### E1-REPLICATION

Requires a pre-existing pre-T association and a post-T study satisfying `GeneticReplicationAssessment`.

### E1-CROSSMODAL

Uses a model arm where pre-T genetic features are excluded or isolated, then evaluates later qualifying genetics.

## Decision C — replication assessment

Minimum `GeneticReplicationAssessment`:

```text
phenotype_match
locus_or_variant_match
effect_allele
allele_harmonization_status
effect_direction_consistency
ld_proxy_relation
population_ancestry
cohort_independence
analysis_compatibility
sample_overlap_status
heterogeneity_status
replication_verdict
```

Possible verdicts:

```text
REPLICATED
PARTIAL_REPLICATION
DIRECTION_CONFLICT
PHENOTYPE_MISMATCH
NON_INDEPENDENT
INCONCLUSIVE
UNRESOLVED
```

Only preregistered qualifying verdicts count for the primary replication endpoint.

## Endpoint-quality payload

A qualifying genetic event must retain, where available/applicable:

```text
sample_size
effect_size
standard_error
p_value
effect_allele
effect_direction
variant_or_locus
population_ancestry
discovery_or_replication_role
independent_sample_status
heterogeneity_statistics
gene_assignment_method
```

Genome-wide significance alone is not a complete endpoint-quality policy.

## Consequences

- suggestive → significant is not called novel;
- replication requires biological/statistical comparability, not just a repeated label;
- Winner's Curse / power / heterogeneity become endpoint-quality concerns;
- E1 subtype results remain separate in MAR.
