# Scientific Red-Team Gap Register

**Status:** ACTIVE — P0 blockers prevent scientific-core implementation  
**Scope:** Forge Bio pre-code benchmark, inference, governance, and outcome-label integrity  
**Authority:** This register supplements PRE_CODE_CHECKLIST.md. A P0 item here is a hard stop unless explicitly superseded by ADR.

## 1. Why this exists

A benchmark can be temporally clean and still produce a misleading scientific conclusion.

Forge Bio therefore treats the following as distinct failure classes:

1. **temporal leakage** — future information enters model-visible inputs;
2. **outcome-construction leakage** — future/modern knowledge changes what counts as a label;
3. **ascertainment bias** — later evidence appears preferentially for candidates that are easier or more fashionable to study;
4. **researcher hindsight** — benchmark design is influenced by knowledge of later successes even when the lockbox is technically closed;
5. **estimand ambiguity** — metrics do not correspond to a stable scientific question;
6. **identity/assignment contamination** — modern mapping or locus-to-gene reasoning creates a future disease-gene label that did not exist in that form;
7. **dependency masquerading as replication** — multiple records represent the same cohort, dataset, consortium, or experiment.

The project does not progress because a model runs. It progresses only when the scientific interpretation is defensible.

## 2. P0 blockers

### P0-R1 — Endpoint subtype ambiguity

**Risk:** "later human genetic support" can mix genuinely new discovery, replication of an existing weak signal, and evidence maturation.

**Required closure:**
- define separate endpoint subtypes;
- freeze which subtype is primary before sealed evaluation;
- report subtype-specific results;
- never merge them into one headline metric without a preregistered rationale.

Minimum endpoint family:
- **E1-NOVEL:** no qualifying pre-T human genetic support, followed by qualifying post-T support;
- **E1-REPLICATION:** pre-T suggestive/initial genetic support, followed by independent qualifying replication;
- **E1-CROSSMODAL:** a pre-T non-genetic evidence model predicts later human genetic support; pre-T genetic evidence is excluded from or isolated in the tested arm.

### P0-R2 — Locus-to-gene outcome contamination

**Risk:** a post-T locus can be retrospectively assigned to a gene using modern QTL, fine-mapping, curated target knowledge, or learned L2G models. This can create an apparently historical gene-level validation that did not exist at the event date.

**Required closure:**
- add an OutcomeGeneAssignmentPolicy;
- preserve locus/variant-level events separately from gene-level events;
- record assignment method, evidence, date, knowledge horizon, and confidence;
- prohibit current learned L2G output from acting as unqualified primary ground truth;
- require sensitivity analysis for assignment-dependent positives.

### P0-R3 — Historical novelty false positives

**Risk:** incomplete Past sources can mark a relationship "not known at T" even though a qualifying pre-T publication or dataset existed.

**Required closure:**
- define an independent HistoricalNoveltyAudit;
- use evaluation-side sources to verify absence of qualifying pre-T evidence without exposing those sources to the ranker;
- mark unresolved cases AMBIGUOUS rather than NOVEL;
- quantify novelty-audit failure rate.

### P0-R4 — Discoverability / observation-propensity confounding

**Risk:** the benchmark may reward genes or diseases that later receive evidence because they are easier to study, better funded, better measured, or represented in larger cohorts.

**Required closure:**
- create a historical DiscoverabilityBaseline or equivalent nuisance model;
- include variables such as historical study count, GWAS availability, sample-size trajectory, phenotype measurability, disease prevalence where justified, gene annotation density, prior association momentum, and research-growth velocity;
- compare model lift against this baseline;
- report performance stratified by research intensity and evidence density.

The discoverability control is a **benchmark control**, not automatically a model feature.

### P0-R5 — Zero-future-event disease estimand

**Risk:** Recall@K is undefined for diseases with no qualifying future events. Dropping these diseases after outcome inspection creates future-conditioned selection bias.

**Required closure:**
- define the target population / estimand;
- define disease weighting;
- define how zero-event diseases contribute to primary analysis;
- define macro vs micro aggregation;
- freeze the policy before sealed outcome access.

### P0-R6 — Researcher hindsight / design-time leakage

**Risk:** a team in the present may know famous later-success targets and may unintentionally encode that knowledge in disease selection, feature design, thresholds, or manual adjudication.

**Required closure:**
- maintain BenchmarkDesignProvenance;
- record analyst exposure to future outcomes and sealed disease identities;
- separate ranking-team and outcome-adjudication roles where practical;
- freeze algorithm/config before sealed outcome reveal;
- for strongest confirmatory claims, keep sealed disease identities hidden from the ranking methodology team until the method is frozen.

### P0-R7 — Disease-regime heterogeneity

**Risk:** Mendelian/rare disease, common-complex disease, and somatic cancer genetics do not share one meaning of "human genetic support".

**Required closure:**
- restrict B-TGT-E1-v0 to a clearly specified genetic/disease regime, or
- define separate benchmark strata with separate endpoint rules;
- prohibit pooled headline interpretation across incompatible regimes.

### P0-R8 — Outcome adjudication independence

**Risk:** an adjudicator who knows the model ranking can unconsciously classify borderline future evidence in favor of the model.

**Required closure:**
- blinded outcome adjudication where feasible;
- dual review for ambiguous/assignment-dependent positives;
- disagreement logging;
- versioned adjudication rubric;
- adjudicator identity and timestamp in provenance.

### P0-R9 — BIG 0 acceptance/checklist mismatch

**Risk:** PRE_CODE_CHECKLIST can be completed even when outputs promised by BIG 0 do not yet exist.

**Required closure:**
PRE_CODE_CHECKLIST must explicitly require:
- glossary;
- QoI schema;
- Context-of-Use schema;
- MAP schema;
- MAR schema;
- core enums/value objects;
- minimal golden synthetic biomedical world;
- architecture import/dependency rules;
- prohibited-dependency fixtures/examples.

### P0-R10 — Licensing posture

**Risk:** provider architecture can become dependent on data that cannot support the intended distribution/commercial posture.

**Required closure:** ADR-005 must be decided before provider implementation.

## 3. P1 requirements before sealed confirmation

### P1-R1 — Cohort/sample-overlap lineage

Independence requires more than distinct publications or databases.

Outcome/evidence lineage must support, where applicable:
- study_id;
- cohort_id;
- consortium_id;
- biobank/dataset_id;
- participant_overlap_group;
- meta-analysis parents;
- independence confidence;
- lineage completeness.

UNKNOWN overlap is not treated as independent replication.

### P1-R2 — Publication/reporting bias sensitivity

The MAR must discuss and, where feasible, quantify bias caused by selective publication and incomplete negative-result availability.

Preferred mitigations:
- primary/full-summary-statistic sources where available;
- registry or dataset-level evidence where applicable;
- source-coverage sensitivity analyses;
- explicit limitation when the outcome process is publication-driven.

### P1-R3 — Ancestry/population applicability

Outcome and evidence events should retain population/ancestry metadata where scientifically relevant.

Confirmatory MAR must:
- report evaluated ancestry/population distribution;
- stratify where sample size allows;
- avoid implying generalization beyond evaluated populations.

### P1-R4 — Stronger attention controls

Historical publication count alone is insufficient.

At least one control should model attention momentum / discoverability trajectory, not just cumulative popularity.

### P1-R5 — Candidate-universe-normalized metrics

Fixed K is retained only with a companion normalized metric, e.g.:
- Recall at x% of candidate universe;
- rank percentile;
- review-budget-normalized utility.

### P1-R6 — Representation-time provenance

For structured evidence derived long after the primary observation, preserve:
- observation/publication time;
- structured derivation time;
- derivation method;
- knowledge watermark of the derivation.

An old paper does not make a modern annotation historically admissible.

### P1-R7 — Negative-control benchmark suite

Required controls should include, where meaningful:
- shuffled outcome assignment;
- future-sentinel invariance;
- temporal placebo cutoffs;
- attention/degree-preserving nulls;
- label-source ablations.

A benchmark that can be "passed" by a null control is invalid until explained.

### P1-R8 — Multiplicity

MAP must freeze:
- one primary benchmark endpoint/subtype;
- one primary metric;
- one primary K/budget;
- multiplicity policy for secondary endpoints/cutoffs/subgroups.

### P1-R9 — Knowledge-time vs technology-time claims

Forge Bio distinguishes:

- **knowledge-historical:** inputs encode no biomedical knowledge after T;
- **technology-contemporaneous:** the complete implementation could realistically have been run with technology available at T.

STRICT_HISTORICAL supports the first claim unless a study explicitly establishes the second. Reports must not silently convert one into the other.

### P1-R10 — Repository governance

Before declaring any scientific specification frozen:
- protect the authoritative branch or enforce equivalent review controls;
- require reviewed PRs for scientific contract/benchmark changes;
- version frozen specs;
- retain immutable commit/hash references in MAP/MAR.

## 4. Manual feasibility pilot required before provider-scale implementation

Before building the complete outcome engine, manually adjudicate a small but heterogeneous sample of candidate future events.

Measure at least:
- whether the relationship was truly unknown at T;
- whether the event was locus-level or gene-level;
- how gene assignment was produced;
- whether the assignment uses post-event knowledge;
- whether the replication is cohort-independent;
- whether outcome ancestry/population is known;
- whether current curation disagrees with historical interpretation;
- fraction of events ending AMBIGUOUS;
- retrospective-curation rate;
- estimated label-construction workload.

The pilot is a **benchmark-feasibility study**, not a performance study.

If ambiguity, retrospective reconstruction, or assignment contamination exceed preregistered tolerances, redesign the endpoint before implementing large-scale ranking.

## 5. Stop rule

No result may be described as "historical discovery signal" if a plausible alternative explanation is that the model predicts:
- research attention;
- measurement opportunity;
- statistical power;
- database curation;
- locus-to-gene assignment artifacts;
- or known weak signals becoming mature.

Those explanations must be controlled, stratified, or explicitly retained as limitations.
