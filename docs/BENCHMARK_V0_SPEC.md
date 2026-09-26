# Benchmark V0 Specification

**Status:** PRE-CODE HARDENING REQUIRED  
**Benchmark family:** B-TGT  
**Benchmark role:** B-TGT-A1 — Disease–Gene Association Prioritization  
**Benchmark ID:** B-TGT-E1-v0

## 1. Question of Interest

> Given only evidence admissible by historical cutoff T, can Forge Bio rank disease–gene biological target-association candidates that later acquire qualifying independent human genetic support within a fixed horizon H, with positive lift over both historical research-attention and historical discoverability controls?

This benchmark tests **disease–gene association prioritization as an early target-program signal**. It does not itself validate a therapeutic target, intervention direction, causality, target tractability, drug efficacy, safety, or clinical success.

The umbrella B-TGT program may later earn stronger "target discovery" language only after direction/mechanism/causal-target evidence is evaluated.

A temporally clean benchmark is not automatically a valid discovery benchmark. The design must also control outcome ascertainment, modern gene assignment, researcher hindsight, and future-conditioned case selection.

## 2. Unit of prediction

The V0 rankable object remains:

```text
TargetAssociationCandidate
    disease_concept_as_of_T
    gene_entity_as_of_T
```

The primary future gene label is **not** any gene mentioned near a qualifying locus. It must satisfy the high-specificity OutcomeGeneAssignmentPolicy defined by ADR-020.

Author-named, nearest-gene, positional-only, generic database-gene, and modern-L2G-only assignments are secondary/sensitivity labels and cannot by themselves generate a primary positive.

If BIG 0F shows that high-specificity gene assignment is too sparse or too attention-coupled to support an informative test, the benchmark REDESIGN fallback is locus-level primary credit rather than silently broadening gene assignment.

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

Every candidate relevant to E1 first receives a frozen pre-T genetic-state assessment:

```text
PreTGeneticState
    NO_SIGNAL_OBSERVED
    SUGGESTIVE
    QUALIFYING
    AMBIGUOUS
```

`NO_SIGNAL_OBSERVED` means no relevant signal was found after the preregistered historical audit **and** the candidate meets the MAP-frozen minimum HistoricalGeneticSearchCoverage grade. It is not an ontological claim that no signal existed anywhere.

If historical search/measurement coverage is below the frozen threshold, the state is `AMBIGUOUS`, not `NO_SIGNAL_OBSERVED`.

The novelty audit also distinguishes:

```text
KNOWN_TO_RANKER_AT_T
KNOWN_PUBLICLY_AT_T
```

A pre-T result that was publicly available but absent from the ranker's historical provider snapshot is a provider/reconstruction coverage failure, not a novel future discovery.

Normative policy: [adr/ADR-012-historical-genetic-observability.md](adr/ADR-012-historical-genetic-observability.md).

### E1-NOVEL-STRICT — new human genetic support

Requirements:
- `PreTGeneticState = NO_SIGNAL_OBSERVED`;
- `HistoricalNoveltyAudit = NOVEL_CONFIRMED`;
- a qualifying post-T event occurs in (T, T+H];
- phenotype matching, gene assignment, and endpoint-quality rules pass.

This is the only E1 subtype that may support a strict "new genetic support" claim.

### E1-MATURATION — suggestive signal becomes qualifying

Requirements:
- `PreTGeneticState = SUGGESTIVE`;
- post-T evidence crosses the frozen endpoint-quality threshold.

This measures evidence/statistical maturation and must never be merged into E1-NOVEL-STRICT for the headline novelty claim.

### E1-REPLICATION — independent replication

Requirements:
- a preregistered pre-T association exists;
- the post-T evidence satisfies `GeneticReplicationAssessment`;
- phenotype comparability and cohort/sample independence pass;
- effect/allele/direction handling satisfies the frozen replication policy.

Replication is distinct from both de novo discovery and mere threshold maturation.

### E1-CROSSMODAL — non-genetic evidence predicts later genetics

The evaluated model arm uses pre-T non-genetic evidence only, or isolates genetic features in a preregistered ablation.

The future endpoint is qualifying human genetic support after T.

This subtype tests whether non-genetic biological evidence anticipates later genetics rather than simply ranking genetic momentum.

### Primary subtype

The sealed confirmatory MAP must choose exactly one primary E1 subtype after feasibility work and before lockbox opening.

Other subtypes are secondary unless a separate MAP is registered.

Normative semantics: [adr/ADR-009-genetic-replication-and-signal-state.md](adr/ADR-009-genetic-replication-and-signal-state.md).

## 8. Qualifying genetic event

A qualifying event must:
1. satisfy the endpoint-subtype rule;
2. contain benchmark-approved human genetic evidence;
3. satisfy the predeclared multidimensional evidence-quality threshold;
4. have defensible first public availability in (T, T+H];
5. be independently source/study backed under the lineage policy;
6. pass disease and gene identity adjudication;
7. pass OutcomePhenotypeMatchPolicy for the benchmark disease/trait;
8. not be merely a post-T re-curation of pre-T evidence;
9. satisfy the ADR-020 high-specificity OutcomeGeneAssignmentPolicy when a primary gene-level label depends on locus/variant assignment;
10. satisfy GeneticReplicationPolicy when the subtype is E1-REPLICATION.

The endpoint-quality payload retains, where applicable:
- canonical variant/locus IDs;
- genome assembly/reference sequence;
- harmonization artifact ID;
- LD reference-panel/method ID where a proxy relation is used;
- sample size;
- effect size;
- standard error;
- p-value;
- effect allele;
- effect direction;
- variant/locus;
- population/ancestry;
- discovery vs replication role;
- independent-sample status;
- heterogeneity statistics;
- gene-assignment method.

Genome-wide significance alone is not a complete endpoint-quality rule.

The precise quality threshold is frozen before sealed evaluation.

Genomic harmonization is part of scientific provenance, not a hidden preprocessing utility. Ambiguous strand/orientation, unresolved liftover, or unresolved variant normalization fails closed for strict replication matching.

Normative genomic policy: [adr/ADR-011-genomic-identity-harmonization.md](adr/ADR-011-genomic-identity-harmonization.md).

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

Canonical assignment classes used by BIG 0F-0 include:

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

Only the frozen high-specificity classes may create a primary gene-level positive.

Identity reconciliation may establish that two identifiers refer to the same entity. It may not manufacture causal-gene evidence.

Normative policy: [adr/ADR-006-outcome-gene-assignment.md](adr/ADR-006-outcome-gene-assignment.md).

## 10. Outcome phenotype matching

A future genetic event for a related trait, biomarker, intermediate phenotype, or risk factor is not automatically a positive for the benchmark disease.

Every qualifying event receives an `OutcomePhenotypeMatchAssessment`.

Primary V0 defaults:
- EXACT qualifies;
- SAME_CONCEPT_DIFFERENT_DEFINITION requires explicit adjudication;
- NARROWER is sensitivity/case-specific unless preregistered otherwise;
- BROADER, SURROGATE, RISK_FACTOR, INTERMEDIATE_PHENOTYPE, RELATED do not qualify for the primary endpoint;
- UNRESOLVED fails closed.

Normative policy: [adr/ADR-008-outcome-phenotype-matching.md](adr/ADR-008-outcome-phenotype-matching.md).

## 11. Genetic replication semantics

E1-REPLICATION requires a `GeneticReplicationAssessment` covering at least:
- phenotype match;
- locus/variant compatibility;
- effect allele and harmonization;
- effect-direction consistency;
- LD proxy relation where relevant;
- population/ancestry;
- cohort independence;
- participant overlap;
- analysis compatibility;
- heterogeneity status.

Only preregistered qualifying verdicts count.

Normative policy: [adr/ADR-009-genetic-replication-and-signal-state.md](adr/ADR-009-genetic-replication-and-signal-state.md).

## 12. Historical novelty audit

E1-NOVEL-STRICT requires an evaluation-side HistoricalNoveltyAudit plus `PreTGeneticState = NO_SIGNAL_OBSERVED`.

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

## 13. Non-positive and censoring states

**NEGATIVE_CONFIRMED:** only when an affirmative preregistered failure definition is satisfied.

**UNKNOWN:** no qualifying positive event is observed and evidence does not justify a negative.

**RIGHT_CENSORED:** the complete outcome window cannot be observed because T+H exceeds usable data coverage or required source coverage is materially incomplete.

**COMPETING_EVENT:** a benchmark-defined event prevents interpretation of the primary endpoint.

**CONFLICTED / AMBIGUOUS:** identity, novelty, gene assignment, or outcome evidence prevents defensible assignment.

Absence of future genetic support is not a negative.

## 14. Candidate universe

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

## 15. Disease sampling frame

Diseases must not be selected because designers know famous later successes.

The disease frame is constructed mechanically from as-of-T criteria and, for development/pilot sampling, uses a committed random seed or fully deterministic sampling rule sealed before adjudication.

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

## 16. Future-event independence

Distinct database rows, publications, or PMIDs do not guarantee independent evidence.

Every OutcomeEvent belongs to a canonical `ScientificEventFamily` when multiple records/publications/databases are manifestations of the same underlying discovery.

For genetic outcomes, use `GeneticDiscoveryEventFamily` to group locus-level discovery and its gene assignments.

Default V0 primary-credit rule:

```text
one scientific event family receives at most one primary event credit
```

Multiple gene assignments from one locus do not automatically create multiple independent future discoveries.

Every OutcomeEvent carries, where applicable:

```text
outcome_event_id
event_family_id
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
shared_control_group_id
cross_disease_study_family_id
meta_analysis_parent_ids
independence_family_id
independence_confidence
lineage_complete
derivation_type
evaluation_identity_bridge_version
```

Cohort, Dataset, Biobank, Consortium, and SampleSet references must resolve through the identity layer rather than free-text aliases.

UNKNOWN cohort/sample overlap is not interpreted as independent replication.

A post-T annotation that only re-curates pre-T evidence does not qualify as new independent support.

For the primary confirmatory outcome, prefer primary publications, deposited summary statistics, or an outcome extraction path operationally independent of any Past input curation pipeline.

A catalog/database that materially contributes to historical model inputs may not simultaneously serve as the sole primary future ground-truth pipeline. If unavoidable, the same-pipeline result is secondary and an independent-primary-source sensitivity is required.

Normative event/source policy: [adr/ADR-013-event-identity-source-coupling.md](adr/ADR-013-event-identity-source-coupling.md).

## 17. Discoverability / observation-propensity control

Later outcome observation is not assumed to be missing at random.

A candidate may receive future support preferentially because it is:
- heavily funded or published;
- studied in larger cohorts;
- associated with common/measurable phenotypes;
- represented in major biobanks;
- highly annotated;
- already near a significance/replication threshold.

The benchmark therefore requires a historical discoverability control or nuisance model using only as-of-T information.

Candidate variables for the **Combined Nuisance Model** include, where historically reconstructable:
- historical disease study count;
- historical GWAS availability;
- historical sample-size trajectory;
- research-attention velocity;
- prior association momentum;
- global gene/entity popularity;
- gene annotation density;
- gene length / historical gene-model span;
- variant density or callable/genotyped-variant opportunity;
- regional gene density;
- LD/locus architecture summaries;
- cross-trait pre-T GWAS-hit burden / pleiotropy;
- historical assay / array / measurement observability;
- phenotype measurability proxies;
- disease prevalence/recruitability proxies;
- evidence-source/provider coverage.

These variables must use as-of-T representations and may not silently use current gene models, current LD, current annotation, or future study design.

These controls are benchmark comparators; they are not automatically allowed as ranker features.

A claimed biological-discovery signal must be distinguishable from discoverability/measurement opportunity.

The benchmark also records `GeneticObservabilityAtT` and reports a preregistered historically-observable sensitivity universe. Historical identity eligibility is not assumed to imply equal genetic measurability across eras/technologies.

This observability sensitivity is constructed from as-of-T technology/source criteria only and may not use future outcomes.

## 18. Baselines

Mandatory:
- random;
- historical disease–gene publication/co-mention attention;
- global gene/entity popularity;
- admissible evidence-volume ranking;
- deterministic evidence-quality baseline;
- historical attention momentum;
- discoverability / observation-propensity baseline;
- genomic-architecture baseline;
- cross-trait pleiotropy baseline;
- historical genetic-observability baseline;
- **Combined Nuisance Model** combining the preregistered non-biological/discoverability/genomic-architecture variables.

Graph degree/network proximity is added only when historically admissible.

The Combined Nuisance Model is the primary comparator. Beating random or any single baseline is insufficient for the headline biological-predictive-value claim.

## 19. Primary and secondary metrics

The primary statistic reports absolute performance and paired incremental value over the preregistered **Combined Nuisance Model**.

Primary scientific contrast:

```text
DeltaPrimaryMetric =
    Metric(nuisance + biological signal)
    -
    Metric(nuisance only)
```

The two arms use the same frozen candidate universe, temporal protocol, and matched capacity constraints where practical.

BIG 0F evaluates event-rank percentile as the preferred primary metric because sparse future events can make Recall@K highly discrete.

Recall@K and a candidate-universe-normalized Recall@x% remain mandatory secondary metrics unless BIG 0F justifies a different freeze.

The MAP freezes the exact comparator, metric, direction, and decision rule.

Fixed K must be accompanied by at least one candidate-universe-normalized metric, such as:
- Recall at x% of candidate universe;
- candidate rank percentile.

The benchmark also requires a secondary **all-frame review-budget utility** that includes zero-event diseases, for example:

```text
ObservedEventYield@TotalReviewBudget =
    observed qualifying future events captured
    /
    total candidates reviewed across the full frozen disease frame
```

This measures observed future-event yield, not biological precision. It does not convert non-observation into a negative label.

Secondary metrics may also include:
- event MRR;
- preregistered NDCG;
- enrichment versus random;
- event-bearing disease coverage;
- zero-event disease review burden;
- per-disease distributions.

The zero-future-event policy from the estimand section governs all aggregate metrics.

## 20. Confidence intervals and multiplicity

The primary baseline delta uses paired disease/challenge-level resampling unless a justified alternative is preregistered.

Candidate rows within one disease are not treated as independent samples.

Because related diseases may share genes, pathways, cohorts, consortia, **shared control sets**, cross-disorder studies, or publication ecosystems, confirmatory analysis must include a preregistered dependence sensitivity.

Where applicable, resampling blocks must include:
- disease family;
- consortium/study family;
- shared-control group;
- cross-disease meta-analysis/study lineage.

Disease IDs alone are not sufficient clustering units when one study/control set contributes outcomes to multiple diseases.

If the apparent signal disappears under family/block dependence, the MAR must report that limitation.

Before sealed evaluation, MAP freezes:
- null and alternative hypotheses;
- test statistic;
- test direction;
- alpha;
- minimum scientifically meaningful / detectable effect;
- target power;
- power-analysis artifact;
- numeric success decision threshold;
- resampling unit;
- interval method;
- resample count;
- one primary endpoint subtype;
- one primary metric;
- one primary K/budget if applicable;
- primary Combined Nuisance comparator;
- multiplicity policy for secondary endpoints, cutoffs, subgroups, and sensitivity analyses;
- confirmatory-generation budget / alpha-spending policy across the research program.

A free-text success rule is prohibited.

## 21. Coverage and ascertainment gates

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

## 22. Outcome adjudication

Outcome classification must be protected from ranking-aware confirmation bias.

For strongest L3 SEALED_CONFIRMATORY evaluation:
- outcome adjudicators **must be blinded** to model rank/order;
- violation automatically downgrades the confirmatory tier.

For development/exploratory work, weaker blinding is allowed only when declared.

In all tiers:
- ambiguous or assignment-dependent positives receive dual review according to the frozen policy;
- disagreements are logged and resolved by versioned policy;
- adjudicator identity, timestamp, source set, and rationale are provenance;
- the ranking team does not alter endpoint rules after seeing sealed errors.

Normative governance: [adr/ADR-010-validation-generations-and-outcome-freeze.md](adr/ADR-010-validation-generations-and-outcome-freeze.md).

## 23. Negative controls / benchmark falsification

Before accepting a scientific signal, run preregistered controls where applicable:
- future-sentinel invariance;
- shuffled outcome assignment;
- temporal placebo cutoff;
- attention/degree-preserving null ranking;
- outcome-source ablation;
- gene-assignment sensitivity;
- exact-only vs broader identity bridge sensitivity.

A null/control method that reproduces the claimed signal invalidates or materially weakens the interpretation until explained.

## 24. Ancestry and population applicability

Evidence and OutcomeEvents preserve population/ancestry metadata where scientifically relevant and available.

The MAR reports:
- evaluated population/ancestry distribution;
- missingness;
- stratified results where sample size permits;
- explicit applicability limits.

Performance in an ancestry-skewed historical evidence base is not silently generalized to all populations.

## 25. Representation-time provenance

For structured facts derived after the primary observation, retain both:
- time the underlying observation became public;
- time/method/knowledge horizon of the structured derivation.

An old paper processed by a modern knowledge-bearing curation or model does not automatically become strict-historical structured evidence.

## 26. Validation-generation governance

VALIDATION is not an infinitely reusable tuning surface.

Each validation case/outcome set belongs to a versioned generation with:
- case-set digest;
- outcome-snapshot digest;
- access count;
- maximum disclosure level observed;
- ACTIVE / SPENT_FOR_MODEL_SELECTION / RETIRED status.

Disclosure levels are:

```text
AGGREGATE_ONLY
SUBGROUP
PER_CASE
FULL_LABEL
```

Adaptive risk is evaluated from both access count and feedback granularity.

A generation that materially influences model/feature/endpoint selection is marked spent and is not described as untouched evidence.

## 27. Future outcome discovery and snapshot commitment

For strongest L3 evaluation, sealed future-event discovery/adjudication is completed and committed **before model rank/order is revealed**. Searching for additional outcome events after seeing ranks automatically downgrades the strongest confirmatory tier.

Before sealed evaluation, freeze/commit:
- future outcome source release IDs;
- future outcome snapshot IDs/digest;
- outcome-ledger digest;
- adjudication-batch digest;
- evaluation identity-bridge digest;
- phenotype-match policy version;
- gene-assignment policy version;
- replication policy version;
- scientific-event-family ledger digest;
- provider-lineage / input-outcome coupling assessment digest.

Changing a provider release, adjudication batch, event-family ledger, mapping bridge, or outcome policy creates a new evaluation artifact/generation.

Past input providers and Future outcome providers are assessed for shared upstream sources, curation pipelines, ontologies, and identity-mapping families. Where coupling is material, the MAR includes same-pipeline exclusion or external-source sensitivity.

Normative governance: [adr/ADR-013-event-identity-source-coupling.md](adr/ADR-013-event-identity-source-coupling.md).

Normative governance: [adr/ADR-010-validation-generations-and-outcome-freeze.md](adr/ADR-010-validation-generations-and-outcome-freeze.md).

## 28. Success criterion

A sealed confirmatory claim requires all of:
1. no unresolved P0 scientific-integrity blocker;
2. primary endpoint subtype and estimand frozen;
3. ranking sealed before outcome reveal;
4. HistoricalNoveltyAudit and PreTGeneticState policy passed;
5. OutcomeGeneAssignmentPolicy passed;
6. OutcomePhenotypeMatchPolicy passed;
7. GeneticReplicationPolicy passed when applicable;
8. exact Future Outcome snapshot/ledger/event-family commitment matches the frozen MAP;
9. strict novelty meets the frozen HistoricalGeneticSearchCoverage threshold;
10. genomic variant/locus harmonization and LD provenance pass;
11. input/outcome provider coupling is measured and required sensitivities pass;
12. primary delta exceeds the preregistered threshold against the strongest required attention/discoverability control;
13. confidence interval satisfies the preregistered rule and dependence sensitivity is reported;
14. signal is not driven by one disease/family/research-intensity stratum;
15. null/placebo controls do not reproduce the result;
16. sensitivity analyses show no material identity, reconstruction, phenotype-match, gene-assignment, replication, observability, event-family, provider-coupling, or outcome-source artifact.

Results are reported even when negative.

## 29. Interpretation boundary

This benchmark does not prove:
- causal gene status;
- intervention direction;
- target tractability;
- drug existence;
- clinical efficacy;
- safety;
- treatment success.

A positive B-TGT-E1 result supports only the endpoint-specific **disease–gene association prioritization** claim earned by the primary subtype. It is not, by itself, "therapeutic target discovery".

The project must not call the result "discovery signal" if a plausible alternative explanation remains that the model primarily predicts:
- future research attention;
- statistical power;
- measurement opportunity;
- database curation;
- known weak signals becoming mature;
- modern locus-to-gene assignment artifacts.


## 30. BIG 0F contamination and adjudication rule

BIG 0F is governed by ADR-021.

All diseases/events directly inspected in BIG 0F are permanently DEVELOPMENT_EXPOSED and cannot later enter a strongest-tier sealed confirmatory generation.

At least 30% of pilot cases require independent second adjudication when such a reviewer is available; absence of an independent adjudicator is reported as a limitation and caps claim strength rather than being marked passed.

The pilot protocol, sampling frame/random seed, target N, and numeric GO/REDESIGN/NO-GO thresholds are frozen before case adjudication.

BIG 0F must also include:
- a symmetric PreTGeneticState/novelty-audit cost sample on non-events;
- a mini historical-provider availability audit;
- assignment-method/attention audit;
- development-only Combined Nuisance headroom analysis;
- inputs for simulation-based confirmatory power analysis.

Normative critical-path decisions:
- [adr/ADR-020-e1-primary-comparator-confirmatory-rule.md](adr/ADR-020-e1-primary-comparator-confirmatory-rule.md)
- [adr/ADR-021-big-0f-pilot-protocol.md](adr/ADR-021-big-0f-pilot-protocol.md)
