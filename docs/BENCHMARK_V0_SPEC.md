# Benchmark V0 Specification

**Status:** PRE-CODE HARDENING REQUIRED  
**Benchmark family:** B-TGT  
**Benchmark ID:** B-TGT-E1-v0

## 1. Question of Interest

> Given only evidence admissible by historical cutoff T, can Forge Bio rank disease–gene biological target-association candidates that later acquire qualifying independent human genetic support within a fixed horizon H, with positive lift over both historical research-attention and historical discoverability controls?

This benchmark tests biological target-prioritization signal. It does not validate intervention direction, causality, drug efficacy, safety, or clinical success.

A temporally clean benchmark is not automatically a valid discovery benchmark. The design must also control outcome ascertainment, modern gene assignment, researcher hindsight, and future-conditioned case selection.

## 2. Unit of prediction

The V0 rankable object is:

```text
TargetAssociationCandidate
    disease_concept_as_of_T
    gene_entity_as_of_T
```

Intervention direction remains outside the V0 endpoint.

A later direction-aware benchmark evaluates full TargetHypothesis objects against mechanistic/functional endpoints.

## 3. Scientific estimand

Before any sealed outcome access, the MAP must state exactly what population-level quantity the benchmark estimates.

Required fields:

```text
target_disease_population
candidate_population
disease_weighting
candidate_weighting
zero_future_event_disease_policy
macro_vs_micro_aggregation
observation_horizon
outcome_observability_requirements
primary_endpoint_subtype
primary_metric
primary_review_budget_or_K
```

Diseases with zero qualifying future events may not be removed after outcome inspection merely because Recall@K is undefined for them.

Any conditional estimand such as "performance among diseases with at least one future event" must be justified and the conditioning rule must be frozen before sealed outcome access.

## 4. Disease/genetic regime

"Human genetic support" does not have one universal interpretation across Mendelian disease, common-complex disease, somatic cancer, and pharmacogenomic settings.

The **primary B-TGT-E1-v0 confirmatory regime is fixed to common-complex germline disease/trait genetics**.

Excluded from the primary V0 pool:
- primary Mendelian / rare-disease gene-discovery cases;
- somatic cancer-driver genetics;
- pharmacogenomic endpoints;
- other regimes whose endpoint semantics materially differ.

Those domains may receive separate benchmark families or explicitly separate strata later.

They may not be pooled into the V0 headline result.

## 5. Cutoff selection

The cutoff is not hard-coded.

BIG 1 evaluates candidate eras approximately 2005–2014 using provider qualification.

The chosen T must satisfy preregistered minimums for:
- historical provider fidelity;
- disease and gene identity coverage;
- candidate-universe completeness;
- outcome-source coverage;
- sufficient future observation horizon;
- feasible novelty audit;
- feasible outcome gene assignment;
- acceptable retrospective-curation burden.

The selected cutoff becomes immutable inside the MAP.

## 6. Future horizon

H is a fixed duration, not "until today".

Pre-code candidate horizons are:

```text
3 years
5 years
7 years
10 years
```

Provider/outcome feasibility may eliminate a candidate horizon when observation coverage is inadequate.

Among feasible horizons, the development procedure chooses the **smallest H** that satisfies preregistered minimums for:
- qualifying event yield;
- number of event-bearing diseases;
- outcome-source coverage;
- censoring/ambiguity;
- expected confidence-interval width.

H is **not** selected because it maximizes Forge Bio lift or makes the model look best.

The chosen H is frozen before sealed evaluation. Sealed case outcomes may not be inspected to choose H.

## 7. Endpoint family E1

A single undifferentiated "later human genetic support" label is prohibited.

Every qualifying positive belongs to an explicit endpoint subtype.

### E1-NOVEL — new human genetic support

Requirements:
- no qualifying human genetic support is established at or before T under the historical endpoint rule;
- the candidate passes HistoricalNoveltyAudit;
- a qualifying post-T event occurs in (T, T+H].

This is the strongest V0 subtype for a claim about previously unestablished genetic support.

### E1-REPLICATION — independent maturation / replication

Requirements:
- some preregistered pre-T genetic signal exists but does not meet the future qualifying endpoint;
- post-T evidence meets the replication endpoint;
- independence requirements pass.

This measures replication/evidence maturation, not de novo discovery.

### E1-CROSSMODAL — non-genetic evidence predicts later genetics

The evaluated model arm uses pre-T non-genetic evidence only, or isolates genetic features in a preregistered ablation.

The future endpoint is qualifying human genetic support after T.

This subtype is designed to test whether non-genetic biological evidence anticipates later genetics rather than simply ranking genetic momentum.

### Primary subtype

The sealed confirmatory MAP must choose exactly one primary E1 subtype after feasibility work and before lockbox opening.

Other subtypes are secondary unless a separate MAP is registered.

## 8. Qualifying genetic event

A qualifying event must:
1. satisfy the endpoint-subtype rule;
2. contain benchmark-approved human genetic evidence;
3. satisfy the predeclared evidence-quality threshold;
4. have defensible first public availability in (T, T+H];
5. be independently source/study backed under the lineage policy;
6. pass disease and gene identity adjudication;
7. not be merely a post-T re-curation of pre-T evidence;
8. satisfy OutcomeGeneAssignmentPolicy when a gene-level label depends on locus/variant assignment.

The precise quality threshold is frozen before sealed evaluation.

## 9. Locus/variant to gene assignment

A locus-level event is not automatically a gene-level event.

Every assignment-dependent future event records at least:

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

Current learned locus-to-gene models, modern QTL resources, current curated target databases, or later therapeutic knowledge may not silently create strict historical gene-level ground truth.

Identity reconciliation may establish that two identifiers refer to the same entity. It may not manufacture causal-gene evidence.

Normative policy: [adr/ADR-006-outcome-gene-assignment.md](adr/ADR-006-outcome-gene-assignment.md).

## 10. Historical novelty audit

E1-NOVEL requires an evaluation-side HistoricalNoveltyAudit.

The audit may use sources that are never exposed to ranking/features.

Possible states:

```text
NOVEL_CONFIRMED
KNOWN_AT_T
NOVELTY_AMBIGUOUS
```

NOVELTY_AMBIGUOUS is never silently treated as novel.

The audit records:
- searched sources/releases;
- temporal coverage;
- matching policy;
- reviewer/adjudicator;
- evidence found;
- decision and rationale.

The Future Outcome plane must not be used as a model feature when auditing novelty.

## 11. Non-positive and censoring states

**NEGATIVE_CONFIRMED:** only when an affirmative preregistered failure definition is satisfied.

**UNKNOWN:** no qualifying positive event is observed and evidence does not justify a negative.

**RIGHT_CENSORED:** the complete outcome window cannot be observed because T+H exceeds usable data coverage or required source coverage is materially incomplete.

**COMPETING_EVENT:** a benchmark-defined event prevents interpretation of the primary endpoint.

**CONFLICTED / AMBIGUOUS:** identity, novelty, gene assignment, or outcome evidence prevents defensible assignment.

Absence of future genetic support is not a negative.

## 12. Candidate universe

CandidateUniverse is a separate immutable artifact from HistoricalKnowledgeView.

```text
CandidateUniverse
    universe_id
    benchmark_family
    cutoff
    disease_set_id
    entity_class
    inclusion_policy_version
    exclusion_policy_version
    source_snapshot_ids
    identity_policy_version
    knowledge_watermark
    candidate_ids
    digest
```

Eligibility requires:
- gene identity known/admissible by T;
- disease identity known/admissible by T;
- benchmark inclusion rule satisfied.

The universe may not be constructed from a current "all known targets" or "all druggable genes" list unless that artifact itself passes temporal qualification.

The primary universe policy is frozen before sealed evaluation. Alternative universes may be sensitivity analyses only.

## 13. Disease sampling frame

Diseases must not be selected because designers know famous later successes.

Before sealed outcome inspection, construct and freeze the sampling frame from as-of-T criteria including:
- disease vocabulary/release;
- genetic/disease regime;
- minimum historical data coverage;
- exclusions;
- research-intensity strata;
- evidence-density strata;
- disease-family strata;
- candidate-universe-size strata.

Manual/famous-case additions are exploratory and reported separately.

Where practical, sealed disease identities remain hidden from the ranking methodology team until algorithm and feature families are frozen.

## 14. Future-event independence

Distinct database rows, publications, or PMIDs do not guarantee independent evidence.

Every OutcomeEvent carries, where applicable:

```text
outcome_event_id
endpoint_type
event_time
first_publicly_available_interval
source_artifact_ids
source_record_ids
publication_ids
study_ids
cohort_ids
consortium_ids
biobank_or_dataset_ids
participant_overlap_group
meta_analysis_parent_ids
independence_family_id
independence_confidence
lineage_complete
derivation_type
evaluation_identity_bridge_version
```

UNKNOWN cohort/sample overlap is not interpreted as independent replication.

A post-T annotation that only re-curates pre-T evidence does not qualify as new independent support.

## 15. Discoverability / observation-propensity control

Later outcome observation is not assumed to be missing at random.

A candidate may receive future support preferentially because it is:
- heavily funded or published;
- studied in larger cohorts;
- associated with common/measurable phenotypes;
- represented in major biobanks;
- highly annotated;
- already near a significance/replication threshold.

The benchmark therefore requires a historical discoverability control or nuisance model using only as-of-T information.

Candidate variables may include, where available and scientifically justified:
- historical disease study count;
- historical GWAS availability;
- historical sample-size trajectory;
- research-attention velocity;
- prior association momentum;
- gene annotation density;
- phenotype measurability proxies;
- disease prevalence/recruitability proxies;
- evidence-source coverage.

These controls are benchmark comparators; they are not automatically allowed as ranker features.

A claimed biological-discovery signal must be distinguishable from discoverability/measurement opportunity.

## 16. Baselines

Mandatory:
- random;
- historical disease–gene publication/co-mention attention;
- global gene/entity popularity;
- admissible evidence-volume ranking;
- deterministic evidence-quality baseline;
- historical attention momentum;
- discoverability / observation-propensity baseline.

Graph degree/network proximity is added only when historically admissible.

## 17. Primary and secondary metrics

The primary statistic reports absolute performance and paired delta against the strongest preregistered non-biological attention/discoverability control.

A candidate form is:

```text
DeltaRecall@K =
    Recall@K(model)
    -
    Recall@K(best_preregistered_attention_or_discoverability_control)
```

The MAP freezes the exact comparator.

Fixed K must be accompanied by at least one candidate-universe-normalized metric, such as:
- Recall at x% of candidate universe;
- candidate rank percentile;
- review-budget-normalized utility.

Secondary metrics may include event MRR, preregistered NDCG, enrichment versus random, and per-disease distributions.

The zero-future-event policy from the estimand section governs all aggregate metrics.

## 18. Confidence intervals and multiplicity

The primary baseline delta uses paired disease/challenge-level resampling unless a justified alternative is preregistered.

Candidate rows within one disease are not treated as independent samples.

Before sealed evaluation, MAP freezes:
- resampling unit;
- interval method;
- resample count;
- one primary endpoint subtype;
- one primary metric;
- one primary K/budget;
- multiplicity policy for secondary endpoints, cutoffs, subgroups, and sensitivity analyses.

## 19. Coverage and ascertainment gates

Confirmatory studies freeze:
- maximum UNKNOWN fraction per required Past source;
- minimum identity-resolved candidate fraction;
- minimum outcome-source coverage across H;
- minimum admitted-evidence coverage;
- maximum novelty-audit ambiguity;
- maximum assignment-dependent ambiguity;
- minimum lineage completeness for events counted as independent;
- acceptable retrospective-curation fraction;
- minimum population/ancestry metadata coverage where applicable.

Cases failing hard thresholds are INVALID_CASE or handled only according to preregistered policy.

They are never silently repaired or excluded after viewing model performance.

## 20. Outcome adjudication

Outcome classification must be protected from ranking-aware confirmation bias.

Where feasible:
- adjudicators are blinded to model rank/order;
- ambiguous or assignment-dependent positives receive dual review;
- disagreements are logged and resolved by versioned policy;
- adjudicator identity, timestamp, source set, and rationale are provenance;
- the ranking team does not alter endpoint rules after seeing sealed errors.

## 21. Negative controls / benchmark falsification

Before accepting a scientific signal, run preregistered controls where applicable:
- future-sentinel invariance;
- shuffled outcome assignment;
- temporal placebo cutoff;
- attention/degree-preserving null ranking;
- outcome-source ablation;
- gene-assignment sensitivity;
- exact-only vs broader identity bridge sensitivity.

A null/control method that reproduces the claimed signal invalidates or materially weakens the interpretation until explained.

## 22. Ancestry and population applicability

Evidence and OutcomeEvents preserve population/ancestry metadata where scientifically relevant and available.

The MAR reports:
- evaluated population/ancestry distribution;
- missingness;
- stratified results where sample size permits;
- explicit applicability limits.

Performance in an ancestry-skewed historical evidence base is not silently generalized to all populations.

## 23. Representation-time provenance

For structured facts derived after the primary observation, retain both:
- time the underlying observation became public;
- time/method/knowledge horizon of the structured derivation.

An old paper processed by a modern knowledge-bearing curation or model does not automatically become strict-historical structured evidence.

## 24. Success criterion

A sealed confirmatory claim requires all of:
1. no unresolved P0 scientific-integrity blocker;
2. primary endpoint subtype and estimand frozen;
3. ranking sealed before outcome reveal;
4. HistoricalNoveltyAudit policy passed;
5. OutcomeGeneAssignmentPolicy passed;
6. primary delta exceeds the preregistered threshold against the strongest required attention/discoverability control;
7. confidence interval satisfies the preregistered rule;
8. signal is not driven by one disease/family/research-intensity stratum;
9. null/placebo controls do not reproduce the result;
10. sensitivity analyses show no material identity, reconstruction, gene-assignment, or outcome-source artifact.

Results are reported even when negative.

## 25. Interpretation boundary

This benchmark does not prove:
- causal gene status;
- intervention direction;
- target tractability;
- drug existence;
- clinical efficacy;
- safety;
- treatment success.

A positive B-TGT-E1 result supports only the endpoint-specific claim earned by the primary subtype.

The project must not call the result "discovery signal" if a plausible alternative explanation remains that the model primarily predicts:
- future research attention;
- statistical power;
- measurement opportunity;
- database curation;
- known weak signals becoming mature;
- modern locus-to-gene assignment artifacts.
