# BIG 0F V0 Pilot Protocol

**Status:** SEAL_CANDIDATE — SPEC-CLOSED / IMPLEMENTATION-PENDING. It is registered at S1 ([BIG_0F_SELECTION_CUSTODY.md](BIG_0F_SELECTION_CUSTODY.md) §2) before any cutoff/horizon predicate is computed.
**Precedence:** [V0_FREEZE_STATEMENT.md](V0_FREEZE_STATEMENT.md) wins over this page. The decisions are recorded in [ADR-022](adr/ADR-022-final-scientific-consistency-closure.md).
**Purpose:** decide whether B-TGT-E1-v0 is scientifically constructible
**Claim level:** DEVELOPMENT only; this pilot cannot support a confirmatory performance claim
**Start gates (ADR-022 §9):** BIG 0F adjudication cannot begin until all four exist:

- the minimal verification harness;
- a successful external-seal dry run;
- an independent second adjudicator;
- an independent selection custodian.

## 1. Pilot cutoff and horizon

Cutoff/horizon selection is deterministic and completed by the selection custodian before event adjudication.

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

The 16 pairs are evaluated in cutoff-major order (cutoff ascending, then 3y, 5y, 7y, 10y). The selected pair (T\*, H\*) is the **first pair** for which all five frozen predicates pass: P_prov, P_obs, P_cov, P_anchor and P_evt ([BIG_0F_SELECTION_CUSTODY.md](BIG_0F_SELECTION_CUSTODY.md) §3).

Model lift, biological-model rankings, nuisance-model lift and ambiguity outcomes are never inspected to choose T/H. No predicate uses a per-disease outcome that the study team can see.

If no pair passes, BIG 0F returns REDESIGN rather than choosing a new cutoff/horizon post hoc.

**Required artifact.** The custodian emits `big0f-selection-provenance-v1` (`schemas/big0f-selection-provenance.v1.schema.json`). It contains:

- the complete 16-pair audit in the frozen order;
- per-predicate results with evidence digests;
- frame-level aggregates;
- the **digest** of each custody-held raw event universe.

The raw universes themselves are never released to the study team (INV-C3). The future evaluator must reconstruct the first passing pair (INV-C2); a later favorable pair cannot be declared manually.

## 2. Disease sampling

The disease frame is a deterministic function of the frozen frame rule ([BIG_0F_FRAME_RULE.md](BIG_0F_FRAME_RULE.md)) and of pinned as-of-T releases. Sampling uses only frame_cov(T\*), the coverage-eligible subset.

Before any event adjudication, the custody sequence S1–S7 runs exactly as written in [BIG_0F_SELECTION_CUSTODY.md](BIG_0F_SELECTION_CUSTODY.md) §2:

1. protocol registration;
2. predicates;
3. selection of (T\*, H\*);
4. selection registration with a **pre-declared** drand quicknet round R;
5. key derivation and ordering at time(R);
6. seal bundle;
7. release of events to adjudicators after seal_time(S6).

The study team does not choose, see or grind seeds. A round other than the pre-declared R, or a chain other than quicknet, is invalid (INV-C6). The ordering condition is seal_time(S4) ≤ time(R) − 24 h (INV-C7).

Pilot selection proceeds down the keyed order:

- **Start** with the first 12 diseases.
- **Expand** one disease at a time, up to 15, only while the cumulative **raw candidate event-family count** is below 60.
- **Cap.** If more than 150 families exist, apply the family-level cap in custody §8. At least one family is kept per disease that has at least one raw candidate family; the remaining slots are filled in ascending `cap` key order.

No famous or manual disease additions enter the decision dataset. Showcase cases are governed by custody §4.

The future evaluator must reconstruct the ordered prefix from the sealed frame_cov digest and the verified beacon, and then recompute expansion and cap mechanically (INV-C9, INV-C10). A pilot result that stops early, expands unnecessarily or reports a different disease order is invalid.

## 3. Pilot event sampling

For each selected disease, the custodian enumerates candidate post-T genetic events in (T\*, T\* + H\*] using the frozen outcome-discovery procedure ([OUTCOME_DISCOVERY_SPEC_V1.md](OUTCOME_DISCOVERY_SPEC_V1.md), executed once, INV-O1).

- Events are grouped into event families (500 kb single linkage) before adjudication.
- Counts, expansion and cap all operate on families, never on raw records.
- Families tagged PRE_T_LOCUS do not count toward the raw candidate count (INV-O2).

## 4. Development exposure

Exposure is accounted for per disease in the exposure ledger ([BIG_0F_SELECTION_CUSTODY.md](BIG_0F_SELECTION_CUSTODY.md) §4–§6):

- Any per-disease post-T information that reaches the study, design or ranking team, or any other audience that is not role-separated, by any route, makes that disease DEVELOPMENT_EXPOSED (INV-X1).
- Every pilot disease whose events were released is DEVELOPMENT_EXPOSED.
- Frame-level aggregates do not expose a disease.
- The custodian's role-separated access does not expose a disease either (INV-X3).
- Confirmatory NOVEL-STRICT families within 500 kb of an adjudicated family of any DEVELOPMENT_EXPOSED disease at (T\*, H\*) are excluded from primary positives. Those diseases are the pilot, the DLVS and any showcase (INV-X5).

DEVELOPMENT_EXPOSED diseases may never enter the strongest-tier sealed confirmatory generation. Changing this rule requires a new pilot on untouched diseases.

## 5. Independent adjudication

The agreement policy is frozen in `config/big0f-adjudication-policy.v2.json` → `agreement_policy` and explained in [BIG_0F_ADJUDICATION_DEFINITIONS.md](BIG_0F_ADJUDICATION_DEFINITIONS.md) §4.

- **Duplicate-review set.** A second independent reviewer reviews min(N, max(30, ⌈0.30·N⌉)) event cases. They are stratified by disease and selected in **salted** keyed-hash order (`dup-review` domain plus the custodian review salt). The custodian uses the salt privately once the complete first-review label set is registered, and publishes it only after the second-review labels are registered. Neither reviewer can foresee or infer the audit set. The set must equal the recomputed selection (INV-A3).
- **Blinding.** The second reviewer is blind to first-reviewer decisions, to Forge Bio rankings and to the Combined Nuisance rankings.
- **Statistic.** Gwet AC1 for each of the four gated tasks: primary assignment eligibility, phenotype qualification, novelty eligibility and primary-positive status. Each task must clear its thresholds on **both** the point estimate and the lower one-sided 90% BCa bound.
- **Also reported.** Cohen κ, percent agreement and the full confusion matrix are reported for every task, including the reported-only tasks (full assignment class, PreTGeneticState, event-family identity, sample overlap). κ is never gated, and no statistic is chosen after prevalence is seen (INV-A1).
- **Stored labels.** Both reviewers' labels are stored for every duplicate-reviewed case (`big0f-curation-audit-v2`, INV-A4).
- **Rule revision.** One clarification-only rule revision is allowed; it changes no policy value and applies to all cases. The re-labelled set is registered first. The retest set is then drawn from all cases, stratified by disease, with a second salt that is still secret, and gates are evaluated on it (INV-A5; custody S9).

## 6. Symmetric non-event historical audit

Historical-search and PreTGeneticState burden cannot be measured only on future positives.

The custodian draws a keyed random sample (`non-event` domain) of non-event disease–gene pairs from the same pilot diseases:

```text
N_non_event =
min(100, max(50, N_event_cases))
```

Apply the same historical-search coverage and PreTGeneticState process.

Report:
- minutes per case;
- UNKNOWN/AMBIGUOUS fraction;
- sources required;
- reviewer agreement (AC1 with its lower bound) on a deterministically sized duplicate subset.

The non-event duplicate-review minimum is:

```text
min(N_non_event, max(30, ceil(0.30 * N_non_event)))
```

The `big0f-curation-audit-v2` artifact records:

- case-level historical-search state;
- source families and provenance;
- both reviewers' labels;
- keyed selection ranks;
- the derived agreement summaries.

Failing to reach the frozen sample size or the duplicate-review minimum makes the pilot INCONCLUSIVE (gates `NON_EVENT_AUDIT_COMPLETION_RATIO` and `NON_EVENT_DUPLICATE_REVIEW_COVERAGE_RATIO`). The audit is never silently waived.

## 7. Mini provider-availability audit

Audit the four mandatory source-family kinds:

1. primary publications / publication metadata;
2. GWAS primary reports and/or historical summary-statistic sources;
3. disease/gene/variant identity or ontology releases;
4. historical gene-model / annotation releases.

**Scope.** The scope is derived mechanically: the selected pilot diseases × every field in `config/big0f-required-field-registry.v1.json` (`big0f-provider-audit-scope-v2`). The study team does not choose fields or diseases, and OPTIONAL fields are not in scope.

**Recorded per cell:**

```text
historical release obtainable?
release/version identifiable?
field existed at T?            (AS_OF_T fields)
value reconstructable?
retrospectively curated?
mapping needed?
license/access constraint?
coverage grade
criticality: CRITICAL | REQUIRED
time_scope: AS_OF_T | EVALUATION
```

Current availability is not accepted as evidence of historical reconstructability.

**Derived metrics.** The `big0f-provider-audit-v2` artifact binds the registry digest and the selection-provenance digest. Required-field availability, source-family kinds present, ancestry metadata coverage and the shared-pipeline fraction are all re-derived from its cells before GO can be evaluated.

### Required-field availability score

```text
available cells (registry availability predicate for the cell's time_scope)
/
all cells in scope
```

Rules:
- CRITICAL fields are not averaged away. A missing CRITICAL field makes the affected case AMBIGUOUS or UNUSABLE.
- CRITICAL and REQUIRED cells enter the denominator equally.
- No field may be reclassified after its availability rate has been seen. Doing so needs a new registry version and a versioned REDESIGN.

## 8. Assignment-attention audit

Every gene-level outcome receives one assignment class under `config/big0f-adjudication-policy.v2.json`:

- **Primary:** HYPOTHESIS_FREE_CODING_OR_LOF, HIGH_CONFIDENCE_FINE_MAPPING, PREREGISTERED_COLOCALIZATION
- **Secondary:** AUTHOR_NAMED, NEAREST_GENE, POSITIONAL_PROXIMITY_ONLY, GENERIC_DATABASE_GENE_FIELD, MODERN_L2G_ONLY, CURRENT_CURATED_TARGET_ONLY, TARGETED_CANDIDATE_GENE_CODING
- **Unresolved:** LOCUS_ONLY

A **primary** gene-level positive also requires hypothesis-free ascertainment at the relevant scale: GENOME_WIDE, EXOME_WIDE or BIOBANK_WIDE. Targeted candidate-gene follow-up cannot create a primary positive on its own. There is no `OTHER_HIGH_SPECIFICITY_METHOD`. A new assignment method requires a versioned REDESIGN.

Report:
- class fractions;
- primary-eligible high-specificity fraction;
- author-named and nearest-gene fractions;
- pre-T attention-rank distribution by assignment class;
- the attention–assignment association and the label-resolution-bias audit (adjudication definitions §5), each computed over all adjudicated post-T event families in the pilot, with no matched sample;
- event yield after removing non-primary classes;
- locus-level one-credit sensitivity. This is a diagnostic only; locus-level credit is a V1 redesign.

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

The power-maturation pathway enters the nuisance comparator through the pre-specified interaction of variant opportunity with disease sample-size trajectory (nuisance manifest v2).

## 10. Combined Nuisance headroom

On pilot-only DEVELOPMENT data, build **only the Combined Nuisance Model**, using `config/big0f-nuisance-manifest.v2.json` with its 14 mandatory families, global attention volume and momentum included.

Canonical pilot model-evaluation mode:

```text
NUISANCE_ONLY
```

BIG 0F **must not run the nuisance + disease-specific biological-evidence arm** and must not inspect Forge Bio biological-model lift (INV-P6).

The run follows the [Nuisance Execution Contract](BIG_0F_NUISANCE_EXECUTION_CONTRACT.md):

- the frozen learner;
- out-of-fold ranks only;
- the eligibility-filtered universe;
- mid-rank ties;
- the adequacy check.

It is recorded as a `big0f-nuisance-run-v2` artifact. Headline metrics are reconstructed from the committed ranks.

Report:
- mean and median positive event percentile under the nuisance comparator (higher = less headroom);
- distribution by disease;
- fraction of positives in the top 1% and top 5%;
- combined-minus-best-single-family adequacy;
- attention-family removal, as a labelled diagnostic only.

## 11. Power

BIG 0F runs the **Stage A pool-sufficiency screen** of [BIG_0F_POWER_AND_VARIANCE_POLICY.md](BIG_0F_POWER_AND_VARIANCE_POLICY.md) §2.

- **What it is.** The screen is model-free. It simulates the frozen sign-flip test under the frozen scenario family, using the event-level SD bound from the nuisance run.
- **Reservation.** It reserves N_DLVS diseases for Stage B.
- **Inputs.** No caller-supplied SD is accepted, and no scenario is chosen after results are seen.
- **Stage B.** Confirmatory variance is measured later, in the Development Lift & Variance Study. That is a P1 item and gates the confirmatory seal, not BIG 0F.

α = 0.05 one-sided, planning effect = 0.05 (planning only) and target power = 0.80 are fixed in [V0_FREEZE_STATEMENT.md](V0_FREEZE_STATEMENT.md) §1. BIG 0F cannot change them.

## 12. GO / REDESIGN / NO-GO / INCONCLUSIVE

**Every numeric threshold is a gate in `config/big0f-thresholds.v2.json`.** This page deliberately restates no values (INV-T1). For each gate the manifest gives:

- the metric definition;
- the source artifact;
- the direction;
- the GO bound;
- the fail consequence;
- the NO_GO bound;
- the stricter and looser bounds;
- the rationale.

The gates cover:

| Area | Gate IDs |
|---|---|
| Ambiguity | ANY_PRIMARY_ENDPOINT_AMBIGUITY_FRACTION, UNKNOWN_SAMPLE_OVERLAP_FRACTION |
| Agreement | AGREEMENT_AC1_MIN_OVER_GATED_TASKS, AGREEMENT_AC1_LOWER90_MIN_OVER_GATED_TASKS, DUPLICATE_REVIEW_COVERAGE_RATIO |
| Provider | REQUIRED_FIELD_AVAILABILITY, SOURCE_FAMILY_KINDS_PRESENT, ANCESTRY_METADATA_COVERAGE, SHARED_PIPELINE_FRACTION_PRIMARY |
| Assignment and attention | PRIMARY_ELIGIBLE_FRACTION, AUTHOR_NEAREST_FRACTION, HIGH_SPECIFICITY_POSITIVE_COUNT, HYPOTHESIS_FREE_DISCOVERY_FRACTION, LABEL_FEATURE_METHOD_COUPLING_FRACTION, ATTENTION_ASSIGNMENT_ASSOC_UPPER95, LABEL_RESOLUTION_BIAS_UPPER95, LOCUS_TO_MANY_GENE_FRACTION, PRE_T_COHORT_REUSE_FRACTION |
| Nuisance headroom | NUISANCE_MEAN_POSITIVE_PERCENTILE, NUISANCE_MEDIAN_POSITIVE_PERCENTILE, NUISANCE_TOP1_POSITIVE_FRACTION, NUISANCE_ADEQUACY_MARGIN |
| Curation burden | MEDIAN_EVENT_CURATION_MINUTES, NON_EVENT_TO_EVENT_TIME_RATIO_MIN, NON_EVENT_TO_EVENT_TIME_RATIO_MAX, NON_EVENT_AUDIT_COMPLETION_RATIO, NON_EVENT_DUPLICATE_REVIEW_COVERAGE_RATIO |
| Yield and discovery | EVENT_BEARING_DISEASE_FRACTION, OUTCOME_DISCOVERY_RECALL |
| Selection predicates (custodian; always PASS for the selected pair) | FRAME_COVERAGE_FRACTION, FRAME_COVERED_DISEASE_COUNT, MEAN_RAW_CANDIDATES_PER_COVERED_DISEASE |
| Power | POWER_POOL_SUFFICIENCY (REDESIGN), POWER_POOL_OPTIMISTIC_FLOOR (NO_GO) |

**Decision rules (manifest `decision_semantics`, SEMANTIC_INVARIANTS INV-T):**

- A missing or non-finite value → INCONCLUSIVE.
- Precedence: NO_GO > REDESIGN > INCONCLUSIVE > GO.
- GO requires every gate to PASS at the base bounds, and every non-exempt gate to PASS at its **stricter** bound. The decision must also be GO under all three bound sets (INV-T6).
- If the terminal decision differs across bound sets, the decision is the higher-precedence of the BASE decision and REDESIGN.
- Every evaluation is registered (public OSF + OTS). Between evaluations, only procedural completion is allowed. After two INCONCLUSIVE evaluations, the next result cannot be INCONCLUSIVE (INV-T7).
- The result is recorded as `big0f-pilot-result-v2`. Every gate appears by ID with its value and outcome under all three bound sets, and all bound artifacts are included by digest.

**V0 subtype.** The V0 pilot does not switch to E1-MATURATION, E1-REPLICATION or E1-CROSSMODAL after results are seen. The V0 primary subtype is E1-NOVEL-STRICT and the primary metric is EVENT_RANK_PERCENTILE_V1 (Freeze Statement §1). REDESIGN leads to V1 with a new pilot on untouched diseases (Freeze Statement §4). Typical V1 redesign options:

- locus-level primary credit;
- independently re-extracted primary-source outcomes;
- a narrower era or regime;
- stronger assignment criteria.

Passing GO means only:

> a confirmatory historical benchmark appears constructible.

## 13. Protocol amendment rule

After S1, any change to a sealed artifact requires a new protocol version (INV-S6; custody §9). This covers sampling, thresholds, assignment eligibility, the disease frame, provider families, adjudication rules and nuisance families.

- The old registration is never overwritten.
- If any per-disease post-T information has reached the design team, the revised pilot uses untouched diseases, even if no case has been adjudicated (INV-X6).

## 14. Threshold provenance

Numeric pilot thresholds are decision rules, not universal scientific constants.

Each gate in `config/big0f-thresholds.v2.json` carries:

- its metric definition and source artifact;
- its direction;
- GO, NO_GO, stricter and looser bounds, or an exemption reason;
- its fail consequence;
- a rationale type (CONVENTION, JUDGEMENT, OPERATIONAL, DERIVED) and a rationale.

The MAR reports the base/stricter/looser table. A conclusion that flips across bound sets resolves under INV-T6. The favorable threshold is never chosen selectively.

## 15. Evidence binding

A GO-capable pilot result binds, by digest, every artifact listed in `big0f-pilot-result-v2` → `bound_artifacts` ([BIG_0F_EVIDENCE_BINDING_CONTRACT.md](BIG_0F_EVIDENCE_BINDING_CONTRACT.md)). These include:

- selection provenance, the selection registration and the beacon;
- the outcome-discovery run and its recall audit;
- the nuisance-only run;
- the provider-audit scope and the provider audit;
- the curation audit;
- the independence attestations for the second adjudicator and the selection custodian;
- the Stage A power analysis under power policy v2;
- the exposure ledger;
- the release log.

External-authority verification must be real:

- OpenTimestamps proof verification;
- an independently fetched, **public** OSF record containing the exact committed digest;
- an independently fetched drand quicknet round R, with its BLS signature verified against the pinned chain.

A JSON field that merely says `VERIFIED` is not sufficient for BIG 0F claim-valid execution.
