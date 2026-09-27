# B-TGT-E1-v0 Estimand Contract

**Status:** NORMATIVE — SEAL_CANDIDATE. Structure, primary subtype (`E1-NOVEL-STRICT`) and primary metric (`EVENT_RANK_PERCENTILE_V1`) are fixed now; only (T\*, H\*) and the other values in [V0_FREEZE_STATEMENT.md](V0_FREEZE_STATEMENT.md) §2 are instantiated later, by frozen rules. The Freeze Statement takes precedence over this page.

## 1. Target question

For diseases selected from an as-of-T sampling frame in the primary genetic regime, when qualifying future E1 events occur within horizon H, does adding pre-T biological evidence improve future-event gene ranking beyond a preregistered Combined Nuisance Model of attention, discoverability, genomic architecture, pleiotropy, and historical observability?

This is a **conditional ranking estimand**, not a claim that every disease will produce a future qualifying event.

Future positive credit is defined on the frozen ScientificEventFamily / GeneticDiscoveryEventFamily ledger. Multiple manifestations of one discovery do not create multiple primary events, and multiple gene assignments from one locus do not automatically multiply event credit.

## 2. Frozen primary population

Primary V0 regime:

```text
common-complex, germline disease/trait genetics
excluding:
- primary Mendelian/rare-disease benchmark cases
- somatic cancer-driver genetics
- pharmacogenomic endpoints
```

Those regimes may receive separate benchmark families/strata later.

## 3. Frozen disease frame

The disease sampling frame is chosen using only as-of-T criteria. For V0 it is the mechanical MeSH frame rule with no manual additions ([BIG_0F_FRAME_RULE.md](BIG_0F_FRAME_RULE.md), `config/big0f-frame-rule.v1.json`); pilot sampling and the untouched confirmatory pool are drawn only from the coverage-eligible frame frame_cov(T\*).

After frame freeze, diseases remain accounted for even if they later have zero qualifying events.

## 4. Zero-event diseases

A disease with zero qualifying future E1 events is **not deleted**.

Because event-recall ranking metrics are undefined when no future positives exist:
- zero-event diseases are retained in benchmark accounting;
- their count/fraction and characteristics are reported;
- they do not contribute a fabricated 0 or 1 to event-recall unless a different preregistered utility estimand is adopted;
- the primary ranking estimand is explicitly conditional on at least one observable qualifying event;
- no claim of performance across all diseases is inferred from that conditional metric.

The benchmark now also requires a secondary all-frame review-budget estimand that covers zero-event diseases without treating them as negatives.

Historical identity eligibility is analyzed separately from GeneticObservabilityAtT. The MAR reports the primary broad-universe estimand and a preregistered historically-observable sensitivity without constructing either universe from future outcomes.

## 5. Secondary all-frame review-budget estimand

The full frozen disease frame is used to estimate operational search-space efficiency.

A candidate metric is:

```text
ObservedEventYield@TotalReviewBudget =
    observed qualifying future events captured
    /
    total candidates reviewed across all frozen diseases
```

Also report:
- event-bearing disease coverage;
- zero-event disease review burden;
- total candidate review budget;
- ScientificEventFamily deduplication fraction;
- locus-to-many-gene primary-credit sensitivity.

These are **observed-event utility metrics**, not biological precision/false-positive metrics. A zero-event disease does not imply its recommended candidates were biologically false.

## 6. Frozen disease weighting

For the primary event-ranking analysis:
- compute the metric within each event-bearing disease;
- average disease-level results with equal disease weight;
- do not allow a disease with many events to dominate by default.

Event-weighted results may be secondary.

## 7. Frozen primary comparator family

The primary comparator is the preregistered **Combined Nuisance Model**, not the strongest single control.

Primary delta:

```text
metric(nuisance + biological signal)
-
metric(nuisance only)
```

The nuisance model combines historically reconstructable non-biological / detectability predictors, including attention, genomic architecture, cross-trait pleiotropy, observability, and provider/source coverage. For V0 its families are exactly the 14 mandatory families of `config/big0f-nuisance-manifest.v2.json` (ADR-022 D11).

The comparator identity, feature families, capacity constraints, temporal training protocol, and source releases are frozen in MAP. The feature families and their definitions are already fixed by the nuisance manifest before BIG 0F.

Single baselines remain diagnostic controls, not the headline comparator.

## 8. Primary metric and candidate-universe normalization

The primary metric is **`EVENT_RANK_PERCENTILE_V1`**, fixed now ([V0_FREEZE_STATEMENT.md](V0_FREEZE_STATEMENT.md) §1; ADR-022 D2; INV-E1). It was chosen because sparse events make Recall@K discrete and K-sensitive. Its canonical definition (ranking universe, filtered competitor set, mid-rank ties, family credit, disease-macro mean) is [METRIC_EVENT_RANK_PERCENTILE_V1.md](METRIC_EVENT_RANK_PERCENTILE_V1.md); the formula is not restated here.

The primary confirmatory contrast is the paired difference between nuisance+biology and nuisance-only. The test, placebo guard and success rule are in Freeze Statement §3.

Recall@K and Recall@x% are mandatory secondary (companion) metrics only. They are never promoted to primary in V0 (INV-E9).

> Superseded by the Freeze Statement §6: "BIG 0F evaluates event rank percentile as the preferred primary statistic", the informal "MacroDiseaseMean(mean percentile rank…)" form, the Recall@K promotion route, and "any final primary metric is selected using DEVELOPMENT-only information".

## 9. Horizon feasibility policy

Candidate horizons are fixed at:

```text
3, 5, 7, 10 years
```

V0 has one confirmatory cutoff and horizon (T\*, H\*), with no pooling across cutoffs. (T\*, H\*) is the first of the 16 (T, H) pairs, in lexicographic order, whose five frozen predicates all pass, computed by the independent selection custodian; if none passes, the result is REDESIGN ([BIG_0F_SELECTION_CUSTODY.md](BIG_0F_SELECTION_CUSTODY.md) §2–§3; INV-C2).

> Superseded by the Freeze Statement §6: the "smallest remaining H meeting preregistered event-yield, event-bearing-disease, ambiguity/censoring and CI-width requirements" rule, and horizon removal by the provider/outcome audit.

The model's lift/performance is not an H-selection criterion, and no predicate uses a per-disease outcome visible to the study team.

## 10. Dependence sensitivity

Primary event-bearing-disease analysis uses disease-level paired resampling.

A preregistered disease-family/block resampling sensitivity is also required to test whether shared biology/cohorts/publication ecosystems make ordinary disease-level intervals overconfident.

If results materially weaken under family/block resampling, that limitation is part of the primary interpretation. In V0, a non-significant family-level sign-flip result labels the claim dependence-fragile ([V0_FREEZE_STATEMENT.md](V0_FREEZE_STATEMENT.md) §3 item 7).

Provider-lineage sensitivity is also required when Past inputs and Future outcome sources share material upstream/curation machinery. The primary interpretation must state whether lift survives same-pipeline exclusion or an external-source comparison when feasible.

LD/reference-panel sensitivity is required when proxy-variant matching materially determines replication labels.

## 11. Frozen structure vs confirmatory instantiation

The following are **fixed now** (status SEAL_CANDIDATE until externally sealed):
- primary population/regime;
- equal disease weighting across event-bearing diseases;
- zero-event disease retention/accounting rule;
- conditional ranking estimand interpretation;
- secondary all-frame utility requirement;
- primary nested comparator family;
- no headline claim from beating random/single popularity controls;
- cutoff/horizon selection rule (custodian first-passing pair; §9);
- high-specificity gene-assignment requirement (adjudication policy v2); locus-level credit is a V1 redesign only ([V0_FREEZE_STATEMENT.md](V0_FREEZE_STATEMENT.md) §4);
- every other item in [V0_FREEZE_STATEMENT.md](V0_FREEZE_STATEMENT.md) §1, including the primary subtype `E1-NOVEL-STRICT`, the primary metric `EVENT_RANK_PERCENTILE_V1`, the ranking universe, α, the planning effect, target power and the confirmatory test.

The following are **confirmatory instance parameters**. Their values are produced later, by rules that are fixed now ([V0_FREEZE_STATEMENT.md](V0_FREEZE_STATEMENT.md) §2):
- T\* and H\* (produced by the custodian predicates, not chosen);
- endpoint-quality rule values (equal to or stricter than adjudication policy v2; INV-T8);
- exact Combined Nuisance feature source releases as of T\*, under the frozen definitions of nuisance manifest v2;
- planning variance for confirmation (Stage B Development Lift & Variance Study);
- the untouched confirmatory pool and the confirmatory disease sample.

> Superseded by ADR-022 D2 and the Freeze Statement §6: "exact primary E1 subtype", "exact primary metric" and "confirmatory minimum effect" as parameters selected after BIG 0F.

This distinction is machine-readable in `schemas/estimand.v1.schema.json` (`instance_state` = STRUCTURE or CONFIRMATORY_INSTANCE).

The pilot/provider audit no longer determines the primary subtype, H, the eligible assignment classes, the primary metric, the nuisance family set, the minimum effect, α, test direction or statistic, the minimum HistoricalGeneticSearchCoverage grade, the event-family credit rule, the pilot sampling rule, N, the second-adjudication fraction or the contamination rule. These are fixed now or produced by frozen rules (Freeze Statement §1–§2; ADR-022 D2–D13). BIG 0F measures, under the gates of `config/big0f-thresholds.v2.json`:
- whether high-specificity gene-level assignment yields enough events (otherwise REDESIGN to V1);
- the event-bearing disease fraction and the Stage A pool-sufficiency power screen ([BIG_0F_POWER_AND_VARIANCE_POLICY.md](BIG_0F_POWER_AND_VARIANCE_POLICY.md) §2);
- provider availability, source-family coverage and Past/Future provider coupling.

Still to be set in the MAP before the confirmatory seal:
- the confirmatory learner and matched-capacity protocol (nuisance manifest v2 `confirmatory_comparator`);
- K for the secondary Recall@K;
- acceptable variant/harmonization ambiguity and the other MAP coverage-gate values;
- observability sensitivity policy details.

These empirical instance parameters remaining open do not reopen the frozen estimand structure. They block a sealed confirmatory run, not implementation of the parameterized metric/benchmark machinery.


## 12. Assignment-attention robustness

The primary gene-level estimand excludes author-named, nearest-gene, positional-only, generic database-gene, modern-L2G-only, current-curated-target-only and targeted candidate-gene coding assignments unless they also independently satisfy a preregistered high-specificity assignment class (adjudication policy v2; [BIG_0F_ADJUDICATION_DEFINITIONS.md](BIG_0F_ADJUDICATION_DEFINITIONS.md) §1).

BIG 0F reports:
- assignment-class distribution;
- primary-eligible event yield;
- author-named / nearest-gene fractions;
- pre-T attention-rank correlation by assignment class;
- locus-level one-credit sensitivity.

If the primary gene label remains materially attention-coupled or too sparse after restriction, the benchmark REDESIGNS to a locus-level or otherwise attention-resistant primary endpoint. That redesign is a new version (V1), not a V0 option ([V0_FREEZE_STATEMENT.md](V0_FREEZE_STATEMENT.md) §4).

Normative decision: [adr/ADR-020-e1-primary-comparator-confirmatory-rule.md](adr/ADR-020-e1-primary-comparator-confirmatory-rule.md).
