# BIG 0F V0 Pilot Protocol

**Status:** PRE-ADJUDICATION FROZEN CANDIDATE — must be externally sealed before first case review  
**Purpose:** decide whether B-TGT-E1-v0 is scientifically constructible  
**Claim level:** DEVELOPMENT only; this pilot cannot support a confirmatory performance claim

## 1. Pilot cutoff and horizon

Cutoff/horizon selection is deterministic and sealed before event adjudication.

The candidate cutoff order is:

```text
2005-12-31
2008-12-31
2011-12-31
2014-12-31
```

The candidate horizon order is:

```text
3y
5y
7y
10y
```

Evaluate candidate pairs lexicographically in the order above and choose the **first pair** that passes only the preregistered provider-availability, observation-window, and minimum event-count feasibility criteria.

Model lift, biological-model rankings, nuisance-model lift, or ambiguity outcomes are not inspected to choose T/H.

If none pass, BIG 0F returns REDESIGN rather than choosing a new cutoff/horizon post hoc.

Machine-enforcement requirement for the future implementation: the pilot must emit a `big0f-selection-provenance-v1` artifact containing the complete 16-pair lexicographic feasibility audit, the raw event universe for every pair with per-event provenance digests, and evidence digests for provider availability and observation-window feasibility. The future evaluator must reconstruct the first passing pair; a later favorable pair cannot be declared manually.

## 2. Disease sampling

Construct the eligible disease frame mechanically from the as-of-T vocabulary and B-TGT common-complex germline regime.

Before any event adjudication:

1. serialize and hash the disease frame;
2. externally timestamp/register the frame digest;
3. after that frame seal exists, obtain a verified public randomness-beacon round;
4. bind the beacon artifact to the already-sealed frame digest;
5. derive the sampling key deterministically from frame digest + beacon randomness;
6. order eligible diseases with the frozen deterministic BIG 0F hash-sort sampling contract.

The study team does not choose or grind candidate seeds. A beacon published before the frame seal is invalid.

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

The future evaluator must reconstruct the first 15 diseases from the sealed frame + verified beacon. It must then recompute the 12→15 expansion mechanically from the raw event universe. A pilot result that stops early, expands unnecessarily, or reports a different disease order is invalid.

## 3. Pilot event sampling

For each selected disease, enumerate candidate post-T genetic events in (T, T+H] using the frozen outcome-discovery procedure.

All enumerated events are retained unless the 150-event cap applies.

When the cap applies, the frozen deterministic event-sampling contract performs keyed sampling over the immutable raw event universe, first preserving at least one event from every event-bearing disease and then filling remaining slots by keyed hash order. The selected event IDs must be recorded in the selection-provenance artifact and independently reconstructable by the future evaluator implementation.

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

Record both:
- adjudicated_event_case_count;
- duplicate_review_count;
- duplicate_review_fraction = duplicate_review_count / adjudicated_event_case_count.

A GO decision is invalid unless duplicate_review_count reaches `min(N_event_cases, max(30, ceil(0.30 * N_event_cases)))`.

Report percent agreement plus a chance-corrected agreement statistic.

Cohen's kappa is used only when category prevalence/balance makes it interpretable. For strongly imbalanced categorical decisions, also report a prevalence-robust agreement statistic (for example Gwet's AC1/AC2 or a preregistered equivalent) and the full confusion matrix.

The GO/REDESIGN threshold is applied to the **preregistered primary agreement statistic for each adjudication task**, not automatically to kappa for every task.

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
- reviewer disagreement on a deterministically sized duplicate subset.

The non-event duplicate-review minimum is:

```text
min(N_non_event, max(30, ceil(0.30 * N_non_event)))
```

The `big0f-curation-audit-v1` artifact records case-level historical-search state, source families, provenance, duplicate-review status/outcome, and the derived disagreement/agreement summaries. Failure to reach the frozen duplicate-review minimum makes the pilot INCONCLUSIVE rather than silently waiving the audit.

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
criticality: CRITICAL | REQUIRED | OPTIONAL
```

Current availability is not accepted as evidence of historical reconstructability.

Provider metrics used by the decision engine are not accepted as free scalar assertions. A `big0f-provider-audit-v1` artifact must enumerate the source families and field-level audit cells. It must contain at least one source from each of the four mandatory family kinds above; four arbitrary/OTHER entries do not satisfy the rule. The disease/source/field audit scope is frozen before availability is inspected, and every source release and required-field cell carries immutable evidence provenance. Required-field availability, coverage distribution, source-family count/IDs, provider coupling, and ancestry metadata coverage are re-derived from that artifact before GO can be evaluated.

### Required-field availability score

The GO/REDESIGN/NO-GO "archived required-field availability" metric is computed as:

```text
available_required_field_cells
/
all_required_field_cells
```

across the sealed disease/source sample.

Rules:
- CRITICAL fields are not averaged away: any missing CRITICAL field required to determine the primary endpoint forces the affected case to AMBIGUOUS/UNUSABLE;
- REQUIRED fields enter the denominator equally unless a weighting scheme was frozen before audit;
- OPTIONAL fields do not improve the availability score;
- source families and fields are enumerated before the first audit;
- no field may be reclassified after seeing its availability rate without a versioned REDESIGN.

## 8. Assignment-attention audit

Every gene-level outcome receives one assignment class under the externally sealed `config/big0f-adjudication-policy.v1.json`.

A **primary** gene-level positive additionally requires the discovery/test ascertainment to be hypothesis-free at the relevant scale (GENOME_WIDE, EXOME_WIDE, or BIOBANK_WIDE). Targeted candidate-gene follow-up cannot independently create a primary positive.

`OTHER_HIGH_SPECIFICITY_METHOD` is not an open primary category in V0. New assignment methods require a versioned REDESIGN before use.

Every gene-level outcome receives one assignment class:

```text
HYPOTHESIS_FREE_CODING_OR_LOF
HIGH_CONFIDENCE_FINE_MAPPING
PREREGISTERED_COLOCALIZATION
AUTHOR_NAMED
NEAREST_GENE
POSITIONAL_PROXIMITY_ONLY
GENERIC_DATABASE_GENE_FIELD
MODERN_L2G_ONLY
TARGETED_CANDIDATE_GENE_CODING
```

Report:
- class fractions;
- primary-eligible high-specificity fraction;
- author-named fraction;
- nearest-gene fraction;
- pre-T attention-rank distribution by assignment class;
- a preregistered association statistic comparing attention rank with probability of receiving an attention-sensitive assignment, using the event set plus a frozen matched comparison sample where required;
- event yield after removing non-primary assignment classes;
- locus-level one-credit sensitivity.

A raw correlation computed only among already-positive author-named genes is not sufficient to establish attention circularity.

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

On pilot-only DEVELOPMENT data, build **only the Combined Nuisance Model** using the frozen nuisance manifest.

Canonical pilot model-evaluation mode:

```text
NUISANCE_ONLY
```

BIG 0F **must not run the nuisance + disease-specific biological-evidence arm** and must not inspect Forge Bio biological-model lift. This prevents the pilot from tuning subtype, nuisance definition, metric, or minimum effect toward a favorable biological result.

The nuisance manifest requires content-free disease-specific attention volume and attention momentum in addition to genomic architecture, pleiotropy, observability, sample-size trajectory, and provider coverage.

This is a nuisance-saturation / feasibility analysis, not a Forge Bio performance experiment.

The actual fitted nuisance execution must be recorded as a `big0f-nuisance-run-v1` artifact under the frozen [Nuisance Execution Contract](BIG_0F_NUISANCE_EXECUTION_CONTRACT.md). Its feature-family set and per-family feature-artifact digests must match the frozen nuisance manifest exactly; semantic biological evidence remains prohibited. The run also binds historical source releases, candidate-universe digest, full rank-output digest, feature transforms, preprocessing, learner family, hyperparameter search space, tuning budget, early-stopping rule, seed policy, and fitted-model digest. The eligible positive-event set is also committed by digest; event-rank records must exactly cover that set. Headline nuisance metrics are reconstructed from committed rank positions and candidate-universe sizes rather than accepted as free summary values.

Report:
- median percentile rank of positive events under nuisance only;
- distribution by disease;
- fraction of events already in the top 1% and top 5%;
- remaining rank-space/headroom available beyond nuisance-only prediction;
- sensitivity to removing attention variables as a diagnostic only; the mandatory disease-specific attention volume/momentum families are not removable from the eventual headline comparator.

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

V0 does **not** accept a caller-supplied disease-level standard deviation. Because BIG 0F is NUISANCE_ONLY, its nuisance-rank dispersion cannot be treated as an empirical estimate of future paired biological-lift variance.

The frozen [Power Input Derivation Contract](BIG_0F_POWER_INPUT_DERIVATION.md) therefore requires GO-capable variance evidence from at least one independent DEVELOPMENT source measuring the same estimand and primary metric, disjoint from the untouched confirmatory pool. The primary planning SD is the conservative bootstrap upper 95% bound after the frozen dependence adjustment. The nuisance-rank SD proxy remains a sensitivity diagnostic only and is explicitly **not GO-eligible**. If no eligible independent same-estimand variance source exists, the power gate is INCONCLUSIVE.

Planning confirmatory defaults:

```text
one-sided alpha = 0.05
target power >= 0.80
```

The minimum scientifically meaningful effect is frozen in the sealed threshold manifest at **0.05 rank-fraction units** for V0. BIG 0F may estimate variance/power inputs but may not change that effect threshold in response to Forge Bio biological-model performance.

## 12. GO / REDESIGN / NO-GO thresholds

These thresholds are frozen before adjudication.

### Hard NO-GO for current B-TGT-E1 design

NO-GO if any remains true after one allowed rule clarification/revision:

- archived/as-of-T required-field availability < 70%;
- fraction of unique cases AMBIGUOUS on **any** primary-endpoint dimension > 40%;
- preregistered primary agreement statistic < 0.60 on either primary gene-assignment class or phenotype match;
- simulation-based confirmatory power < 0.80 at alpha 0.05 for the frozen scientifically meaningful effect even after using all feasible untouched confirmatory diseases/cutoff resources;
- no plausible untouched disease pool remains after excluding pilot contamination;
- high-specificity assignment yields too few positives to support the planned confirmatory test and locus-level redesign is not feasible.

### REDESIGN triggers

REDESIGN if any occurs:

- author-named + nearest-gene assignments > 50% of candidate gene-level positives;
- the confidence interval for the preregistered attention/assignment association reaches or exceeds the sealed absolute boundary 0.30;
- primary-eligible high-specificity assignments < 50% of gene-level positives;
- strict novelty is dominated by pre-T cohort reuse / power maturation;
- same curation pipeline materially dominates both inputs and outcomes;
- fraction of unique cases AMBIGUOUS on any primary-endpoint dimension is >20% and <=40%;
- preregistered primary agreement statistic is >=0.60 and <0.70;
- archived required-field availability is >=70% and <90%;
- Combined Nuisance already ranks the median positive in the top 1% of its disease candidate universe, leaving little plausible headroom.

Default redesign options:
- move primary endpoint to locus level;
- create a **new versioned pilot** if a different E1 subtype is scientifically preferred;
- replace shared curation outcomes with independently re-extracted primary-source outcomes;
- narrow disease era/regime;
- strengthen assignment criteria.

The current V0 pilot does not switch to E1-MATURATION/E1-REPLICATION/E1-CROSSMODAL after inspecting results. V0's primary subtype is E1-NOVEL-STRICT and its primary metric is EVENT_RANK_PERCENTILE_V1.

### GO requirements

GO requires all:

- archived required-field availability >= 90%;
- fraction of unique cases AMBIGUOUS on any primary-endpoint dimension <= 20%;
- preregistered primary agreement statistic >= 0.70 for primary assignment and phenotype match;
- high-specificity primary-eligible assignment fraction >= 50%;
- hypothesis-free study-design fraction among primary positives meets the sealed threshold;
- label/feature method-family coupling remains below the sealed threshold;
- no material unmitigated Past/Future curation coupling;
- sample-overlap / lineage ambiguity within the frozen acceptable policy;
- ancestry/population metadata adequate for the intended primary interpretation;
- retrospective curation burden assessed ACCEPTABLE under the sealed operational-capacity rule;
- symmetric non-event audit completed at the frozen sample size;
- independent duplicate-adjudication minimum coverage completed;
- nuisance headroom not saturated under both the median-rank and sealed top-1%-positive-fraction rules;
- event-bearing disease fraction meets the sealed diversity threshold;
- power variance evidence is GO-eligible under the frozen Power Input Derivation Contract;
- simulation-based target power >= 0.80 at the frozen alpha/effect under the primary conservative scenario;
- untouched diseases remain available for sealed confirmation.

### Incomplete prerequisite rule

The deterministic evaluator returns `INCONCLUSIVE` rather than GO when a mandatory decision prerequisite is unresolved, including:
- union ambiguity is internally inconsistent with component ambiguity;
- independent duplicate-review coverage is below the frozen minimum;
- ancestry/population adequacy is UNKNOWN;
- provider-coupling risk is UNKNOWN;
- retrospective-curation burden is UNKNOWN;
- symmetric non-event audit is incomplete/undersized;
- no eligible independent same-estimand variance source exists for a GO-capable power conclusion;
- a mandatory prerequisite remains unresolved.

Threshold sensitivity is not self-declared: the evaluator reloads the sealed threshold manifest, evaluates all sealed sensitivity variants, and returns REDESIGN if the terminal decision changes.

INCONCLUSIVE may occur at most twice for V0. Reaching the frozen limit forces REDESIGN rather than indefinite re-evaluation.

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


## 14. Threshold provenance

Numeric pilot thresholds are decision rules, not universal scientific constants.

Before external sealing, every threshold receives:

```text
threshold_id
metric_definition
direction
value
rationale
sensitivity_range
decision_consequence
```

The MAR must report a sensitivity table around each threshold that materially changes GO/REDESIGN/NO-GO.

If the conclusion flips under a small scientifically plausible threshold change, the correct outcome is REDESIGN / INCONCLUSIVE rather than selectively choosing the favorable threshold.


## 15. Evidence-binding contract added by preflight hardening

A future GO-capable pilot implementation must require all of the following independently reconstructable artifacts in addition to the scalar result:

- selection provenance for the full cutoff/horizon grid, deterministic disease expansion, raw event universe, and capped event IDs;
- the fitted nuisance-only run with exact frozen feature families and immutable feature/model/preprocessing digests;
- a field-level provider audit artifact;
- a second-adjudicator independence attestation bound to role-registry and independence-evidence digests;
- a power artifact bound to the sealed Power Input Derivation Contract and eligible independent same-estimand variance evidence, with the nuisance-run proxy retained only as sensitivity;
- real external-authority verification: OpenTimestamps proof verification for timestamp-service attestations, an independently fetched OSF record containing the exact committed digest for public-registry attestations, and an independently fetched DRAND round matching the sealed randomness.

A JSON field that merely says `VERIFIED` is not sufficient for BIG 0F claim-valid execution.
