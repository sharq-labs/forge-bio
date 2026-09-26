# BIG 0F V0 Pilot Protocol

**Status:** PRE-ADJUDICATION FROZEN CANDIDATE — must be externally sealed before first case review  
**Purpose:** decide whether B-TGT-E1-v0 is scientifically constructible  
**Claim level:** DEVELOPMENT only; this pilot cannot support a confirmatory performance claim

## 1. Pilot cutoff and horizon

Choose the first cutoff/horizon pair that passes the mini provider-availability audit using only source availability and observation-window coverage.

Model lift is not inspected for this choice.

Candidate cutoffs remain within the predeclared 2005–2014 feasibility range.

Candidate horizons remain:

```text
3y / 5y / 7y / 10y
```

## 2. Disease sampling

Construct the eligible disease frame mechanically from the as-of-T vocabulary and B-TGT common-complex germline regime.

Before any event adjudication:

1. serialize and hash the disease frame;
2. obtain an external seal for the frame digest;
3. obtain an external seal for the random seed;
4. order eligible diseases by seeded random permutation.

Pilot selection proceeds down that immutable order.

Target:

```text
12 diseases
```

Allowed expansion:

```text
up to 15 diseases
```

only if fewer than 60 candidate future genetic events are available after the first 12.

The pilot stops adding diseases once either:
- at least 60 candidate events are available; or
- 15 diseases have been included.

If more than 150 candidate events exist, select 150 with a sealed stratified random rule that preserves disease representation.

No famous/manual disease additions enter the decision dataset.

## 3. Pilot event sampling

For each selected disease, enumerate candidate post-T genetic events in (T, T+H] using the frozen outcome-discovery procedure.

All enumerated events are retained unless the 150-event cap applies.

Events are grouped into ScientificEventFamily / GeneticDiscoveryEventFamily before adjudication.

## 4. Permanent development contamination

Every disease/event inspected in BIG 0F is tagged:

```text
DEVELOPMENT_EXPOSED
```

These diseases/events may never enter the strongest-tier sealed confirmatory generation.

Changing this rule requires a new pilot on untouched diseases.

## 5. Independent adjudication

A second independent reviewer adjudicates a seeded stratified sample of:

```text
max(30 cases, 30% of adjudicated event cases)
```

capped at the total pilot size.

The second reviewer is blind to:
- first-reviewer decisions;
- Forge Bio rankings;
- Combined Nuisance rankings.

Agreement is reported for:
- phenotype relation;
- assignment class;
- PreTGeneticState;
- novelty verdict;
- event-family identity;
- sample-overlap verdict.

Report percent agreement and Cohen's kappa where the category structure makes kappa meaningful.

One frozen rule revision is allowed after disagreement review. The revised rules are then re-tested on a new held-out subset of the pilot cases.

## 6. Symmetric non-event historical audit

Historical-search / PreTGeneticState burden cannot be measured only on future positives.

Draw a seeded random sample of non-event disease–gene pairs from the same pilot diseases:

```text
N_non_event =
min(100, max(50, N_event_cases))
```

Apply the same historical-search coverage and PreTGeneticState process.

Report:
- minutes per case;
- UNKNOWN/AMBIGUOUS fraction;
- sources required;
- reviewer disagreement on a 30% duplicate subset where feasible.

## 7. Mini provider-availability audit

Audit at least four source families before GO:

1. primary publications / publication metadata;
2. GWAS primary reports and/or historical summary-statistic sources;
3. disease/gene/variant identity or ontology releases;
4. historical gene-model / annotation releases.

For every field needed by the proposed benchmark, record:

```text
historical release obtainable?
release/version identifiable?
field existed at T?
retrospectively curated?
mapping needed?
license/access constraint?
coverage fraction?
```

Current availability is not accepted as evidence of historical reconstructability.

## 8. Assignment-attention audit

Every gene-level outcome receives one assignment class:

```text
DIRECT_CODING_OR_LOF
HIGH_CONFIDENCE_FINE_MAPPING
PREREGISTERED_COLOCALIZATION
OTHER_HIGH_SPECIFICITY_METHOD
AUTHOR_NAMED
NEAREST_GENE
POSITIONAL_PROXIMITY_ONLY
GENERIC_DATABASE_GENE_FIELD
MODERN_L2G_ONLY
OTHER
```

Report:
- class fractions;
- primary-eligible high-specificity fraction;
- author-named fraction;
- nearest-gene fraction;
- Spearman correlation between assigned-gene pre-T attention rank and assignment class-specific positive status;
- event yield after removing non-primary assignment classes;
- locus-level one-credit sensitivity.

## 9. Power-maturation audit

For every candidate post-T event, record whether the post-T study includes cohorts or samples that materially overlap with pre-T studies.

Report:

```text
preT_cohort_reuse_fraction
sample_size_growth
preT_summary_statistics_available?
preT_signal_state
```

A development-only power-maturation baseline is constructed from historically available sample-size trajectory and observability variables.

## 10. Combined Nuisance headroom

On pilot-only DEVELOPMENT data, build a nuisance comparator using as-of-T features from the frozen nuisance families.

This is not a performance result.

Report:
- median percentile rank of positive events under nuisance only;
- distribution by disease;
- fraction of events already in the top 1% and top 5%;
- incremental room available to a biological model;
- sensitivity to removing attention variables.

## 11. Power-analysis inputs

The pilot outputs:
- event-bearing disease count;
- high-specificity positive count;
- event-count distribution by disease;
- candidate-universe size distribution;
- within-disease positive rank variance;
- nuisance-model rank distribution;
- observed dependence clusters.

These feed a simulation-based confirmatory power analysis.

Planning confirmatory defaults:

```text
one-sided alpha = 0.05
target power >= 0.80
```

The minimum scientifically meaningful effect is frozen from the pilot's rank scale **without inspecting Forge Bio biological-model performance**.

## 12. GO / REDESIGN / NO-GO thresholds

These thresholds are frozen before adjudication.

### Hard NO-GO for current B-TGT-E1 design

NO-GO if any remains true after one allowed rule clarification/revision:

- archived/as-of-T required-field availability < 70%;
- unresolved/AMBIGUOUS fraction across primary endpoint adjudication > 40%;
- second-adjudicator kappa < 0.60 on either primary gene-assignment class or phenotype match;
- simulation-based confirmatory power < 0.80 at alpha 0.05 for the frozen scientifically meaningful effect even after using all feasible untouched confirmatory diseases/cutoff resources;
- no plausible untouched disease pool remains after excluding pilot contamination;
- high-specificity assignment yields too few positives to support the planned confirmatory test and locus-level redesign is not feasible.

### REDESIGN triggers

REDESIGN if any occurs:

- author-named + nearest-gene assignments > 50% of candidate gene-level positives;
- absolute Spearman correlation between pre-T attention rank and author-named positive assignment > 0.30;
- primary-eligible high-specificity assignments < 50% of gene-level positives;
- strict novelty is dominated by pre-T cohort reuse / power maturation;
- same curation pipeline materially dominates both inputs and outcomes;
- unresolved ambiguity is >20% and <=40%;
- second-adjudicator kappa is >=0.60 and <0.70;
- archived required-field availability is >=70% and <90%;
- Combined Nuisance already ranks the median positive in the top 1% of its disease candidate universe, leaving little plausible headroom.

Default redesign options:
- move primary endpoint to locus level;
- make E1-MATURATION primary with explicit power-maturation baseline;
- replace shared curation outcomes with independently re-extracted primary-source outcomes;
- narrow disease era/regime;
- strengthen assignment criteria.

### GO requirements

GO requires all:

- archived required-field availability >= 90%;
- unresolved/AMBIGUOUS fraction <= 20%;
- second-adjudicator kappa >= 0.70 for primary assignment and phenotype match;
- high-specificity primary-eligible assignment fraction >= 50%;
- no material unmitigated Past/Future curation coupling;
- sample-overlap / lineage ambiguity within the frozen acceptable policy;
- ancestry/population metadata adequate for the intended primary interpretation;
- nuisance headroom not saturated under the top-1% rule above;
- simulation-based target power >= 0.80 at the frozen alpha/effect;
- untouched diseases remain available for sealed confirmation.

Passing GO means only:

> a confirmatory historical benchmark appears constructible.

## 13. Protocol amendment rule

After external sealing and first adjudication, a material change to:
- sampling;
- thresholds;
- assignment eligibility;
- disease frame;
- provider families;
- adjudication rules;
- nuisance families

spends this pilot protocol.

A changed design requires:
- explicit REDESIGN;
- a new protocol version;
- a new externally sealed seed/frame;
- untouched development cases for the revised pilot where the change could have learned from outcomes.
