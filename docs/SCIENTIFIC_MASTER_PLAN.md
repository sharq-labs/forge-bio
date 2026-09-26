# Scientific Master Plan

**Status:** PRE-CODE CANDIDATE V1 — active hardening  
**Project:** Forge Bio  
**Execution principle:** prove temporal scientific value before expensive model complexity

---

## 1. Mission

Forge Bio will determine whether a computational therapeutic-hypothesis process has measurable historical predictive value.

The platform must answer:

> If the system had access only to information defensibly available at time T, could it prioritize biological mechanisms, therapeutic targets, and later existing-drug hypotheses that subsequently reached preregistered scientific endpoints — and could it do so better than research-attention, discoverability/observation-opportunity, and other trivial baselines?

The roadmap optimizes for:

```text
scientific correctness
→ temporal integrity
→ reproducibility
→ measurable validation
→ extensibility
→ performance
→ product UX
```

---

## 2. Program-level success ladder

The project progresses through increasingly strong evidence:

```text
verified infrastructure
→ reproducible historical snapshots
→ baseline historical signal
→ sealed confirmatory lift
→ multi-disease / multi-cutoff generalization
→ endpoint calibration where possible
→ target discovery value
→ repurposing value
→ prospective validation
```

A sophisticated demo is not a program milestone unless it improves scientific evidence.

---

## 3. Benchmark families

### B-TGT — Target Program

B-TGT is the umbrella program for biological and eventual therapeutic-target prioritization.

The first V0 benchmark is:

```text
B-TGT-A1 / B-TGT-E1-v0
Disease
→ historical evidence
→ disease–gene association ranking
→ later independent human genetic support
```

Purpose: establish disease–gene association prioritization signal before making stronger causal-target, intervention-direction, or tractability claims.

### B-REP — Drug Repurposing

```text
Disease
→ target/mechanism evidence
→ as-of-T active moiety / existing-drug universe
→ repurposing hypotheses
→ future investigation / efficacy / regulatory events
```

Purpose: establish whether the biological engine translates into useful therapeutic prioritization.

B-REP must not replace B-TGT. They answer different questions.

---

# BIG 0 — Scientific Contract & Threat Model

## Goal

Freeze what the system is allowed to claim and define the core scientific types before data or models create accidental semantics.

## Outputs

- `SCIENTIFIC_CONTRACT.md`
- architecture ADR set
- glossary
- QoI schema
- Context-of-Use schema
- MAP schema
- MAR schema
- claim maturity ladder
- leakage threat model
- scientific red-team gap register
- benchmark scientific estimand
- E1 endpoint subtype semantics including E1-NOVEL-STRICT vs E1-MATURATION
- PreTGeneticState policy
- OutcomeGeneAssignmentPolicy
- OutcomePhenotypeMatchPolicy
- GeneticReplicationPolicy
- HistoricalNoveltyAudit policy
- ValidationGeneration / OutcomeSnapshotCommitment governance
- BenchmarkDesignProvenance / analyst-hindsight policy
- discoverability/ascertainment control policy
- core enums/value objects
- minimal golden synthetic biomedical world

## Required decisions

- strict historical vs contaminated/current modes
- UNKNOWN semantics
- evidence vs prediction vs validation
- target-as-role semantics
- initial endpoint vocabulary
- disease/genetic regime for B-TGT-E1
- zero-future-event disease estimand
- locus-to-gene outcome semantics
- pre-T no-signal vs suggestive/mature genetics
- disease/trait phenotype-match semantics
- genetic replication semantics
- historical novelty audit
- validation-generation reuse/retirement
- Future Outcome snapshot commitment
- discoverability/observation-propensity controls
- researcher-hindsight / analyst-blinding governance
- benchmark holdout governance

## Acceptance

- all output categories have explicit scientific meaning
- no generic `confidence` or `is_correct` concept exists without endpoint semantics
- architecture dependency rules documented
- deliberate prohibited dependency examples are specified
- golden world has known identities, dates, claims, evidence, and future events
- endpoint family distinguishes E1-NOVEL-STRICT, E1-MATURATION, E1-REPLICATION, and E1-CROSSMODAL
- suggestive pre-T genetics cannot be reported as strict de novo novelty
- locus-level evidence cannot silently become gene-level validation
- related traits/risk factors cannot silently become exact disease outcomes
- replication requires allele/direction/phenotype/lineage comparability
- zero-event disease policy and scientific estimand are frozen before sealed outcomes
- all-frame review-budget utility is defined
- validation-generation reuse is explicit
- exact Future Outcome snapshot/ledger is committed before sealed evaluation
- researcher hindsight is governed separately from technical lockbox access
- discoverability/ascertainment is a required benchmark control

## Do not build

- provider integrations
- ML
- GNNs
- frontend
- agent
- drug-generation workflows

---

# BIG 0R3 — Genetics Identity & Benchmark Integrity Hardening

## Goal

Close genetics-specific semantic gaps before collecting the manual feasibility pilot.

## Outputs

- first-class GenomeAssembly / ReferenceSequence / GenomicVariant / GenomicLocus identity
- first-class Phenotype / Cohort / Dataset / Biobank / Consortium / SampleSet identity
- variant normalization, liftover, allele-harmonization provenance
- LDRelation + reference-panel/ancestry provenance
- HistoricalGeneticSearchCoverage
- GeneticObservabilityAtT sensitivity policy
- KNOWN_TO_RANKER_AT_T vs KNOWN_PUBLICLY_AT_T
- ScientificEventFamily / GeneticDiscoveryEventFamily
- one-event-family primary-credit policy
- ProviderLineage + InputOutcomeCouplingAssessment
- CrossAnchorEventReusePolicy
- validation disclosure levels
- ScientificOperatingMode vs HistoricalDataPolicy separation
- machine-verifiable QoI/MAP/MAR JSON Schemas
- repaired ADR status/amendment chain
- repository LICENSE + CODEOWNERS

## Acceptance

- rsID/coordinate strings cannot act as canonical variant identity
- genome-build/allele/LD transformations are provenance-bearing and fail closed when ambiguous
- phenotype/cohort/dataset aliases cannot create false disease/sample independence
- low historical search coverage cannot become E1-NOVEL-STRICT
- public pre-T knowledge missed by the ranker is classified as provider coverage failure
- one locus/event family cannot silently create multiple primary event credits
- same scientific event cannot receive unbounded repeated weight across rolling anchors
- Past/Future provider coupling is measured
- operating-mode enums are non-overlapping
- ADR-001..006 status chain is internally consistent
- executable schemas parse and match normative fields

## Gate

BIG 0F does not start until these policy/schema artifacts are internally consistent.

---

# BIG 0R4 — Disease, Pathogen, Therapeutic & Scientific Digital Twin Semantics

## Goal

Define complete scientific profiles for diseases, pathogens/viruses, pathogen–host systems, and therapeutics, then define strict maturity rules for when a dynamic/mechanistic/predictive model may be called a Scientific Digital Twin.

This milestone is a **platform extension** and does not block the B-TGT-E1 BIG 0F feasibility pilot once BIG 0R3 remains satisfied.

## Outputs

- DiseaseScientificProfile
- PathogenScientificProfile
- VirusScientificProfileExtension
- PathogenHostScientificProfile
- TherapeuticScientificProfile
- first-class pathogen / strain / tissue / cell-type / biological-process / biomarker identity kinds
- ScientificDigitalTwin
- TwinState / ScientificTwinSnapshot
- TwinStateModel
- TwinValidationArtifact
- TwinPerturbation / TwinSimulationResult
- DigitalTwinMaturityLevel
- executable disease/pathogen/virus/pathogen-host/therapeutic profile JSON Schemas
- executable scientific-twin JSON Schema with maturity-specific requirements
- ADR-015 twin terminology/claim boundary
- temporal provenance for state-model structure/update policy/parameters
- MAP/MAR/ValidationGeneration integration for T3/T4
- causal-assumption/intervention/identifiability contract for T4
- VVUQ contract

## Twin maturity

```text
T0_PROFILE_ONLY
T1_DYNAMIC_KNOWLEDGE_TWIN
T2_MECHANISTIC_TWIN
T3_VALIDATED_PREDICTIVE_TWIN
T4_VALIDATED_INTERVENTION_SIMULATION_TWIN
```

## Acceptance

- disease and pathogen are distinct identities;
- infectious-disease modeling can represent pathogen + host biology explicitly;
- a static profile/graph cannot claim T1+ twin maturity;
- T3/T4 requires held-out/future predictive validation and uncertainty quantification;
- simulation output is a research hypothesis, not clinical evidence;
- patient-specific twins remain outside V1 Context of Use;
- historical Twin(subject, T) records explicit cutoff T and obeys HistoricalKnowledgeView, state-model/update-policy watermark, preprocessing, and parameter-fit cutoffs;
- executable schema rejects T2/T3/T4 artifacts missing inherited maturity prerequisites;
- T3 reuses MAP/MAR/ValidationGeneration/BenchmarkDesignProvenance;
- T4 requires causal assumptions, intervention semantics, identifiability, perturbation and sensitivity artifacts.

## Gate

Architecture/schema completion is sufficient for BIG 0R4.

Actual T2–T4 twin implementation is **frozen/deferred until after the core B-TGT program has passed BIG 0F and produced at least one credible historical benchmark result**. No additional Twin complexity is on the E1 critical path.

---

# BIG 0R5 — Model Credibility & Quantitative Integrity

## Goal

Close fit-for-purpose model-credibility, quantitative-semantics, numerical-verification, and applicability gaps before advanced mechanistic/predictive models are allowed to influence scientific claims.

BIG 0R5 is a platform-hardening layer. It does not delay the manual BIG 0F endpoint-feasibility pilot, but its contracts are mandatory before T2+ Scientific Twin claims or endpoint-calibrated probability claims.

## Outputs

- ADR-016 computational model credibility / numerical verification
- ADR-017 quantitative measurement/effect semantics
- MODEL_CREDIBILITY_POLICY.md
- QUANTITATIVE_SEMANTICS.md
- QuantityDefinition
- QuantitativeObservation
- EffectEstimate
- MeasurementProcessArtifact
- NumericalVerificationArtifact
- CredibilityAssessmentArtifact
- ModelDiscrepancyAssessment
- ApplicabilityDomain / prediction risk-of-bias audit
- executable schemas for quantitative/model-credibility artifacts
- executable positive/negative contract tests
- source lifecycle events for corrections/retractions/withdrawals
- BenchmarkExposureLedger / benchmark exhaustion states
- ResearchProgramAttempt ledger
- ExternalSealAttestation
- prospective PredictionExposureEvent / self-fulfilling-attention guard

## Acceptance

- a numeric value without quantity/unit/scale/transform/context semantics cannot act as a scientific measurement;
- incompatible dimensions/scales/transforms cannot be silently combined;
- p-value alone cannot act as an effect estimate;
- missing/censored observations cannot become numeric zero;
- measurement/normalization/batch transforms carry provenance and cutoff;
- numerical error is separated from measurement/parameter/model-form uncertainty;
- T2+ numerical simulation records solver/method/tolerance/convergence evidence where applicable;
- model credibility is explicitly Context-of-Use specific;
- T3+ evaluation audits development/evaluation separation, applicability, and distribution shift;
- probabilistic claims require held-out calibration plus a proper scoring rule;
- material model/dependency change invalidates prior validation until re-assessed;
- later source correction/retraction does not silently rewrite historical state;
- benchmark reuse/adaptive exposure is tracked and can exhaust a generation;
- strongest confirmatory/prospective artifacts are externally sealed;
- prospective prediction exposure is tracked so self-fulfilling research activity is not mislabelled independent validation.

## Gate

R5 policy/schema completion is sufficient for pre-code hardening.

Empirical adequacy is demonstrated later by the actual model/twin validation artifacts; the policy itself is not evidence that a future model is credible.

---

# BIG 0F-0 — Critical-Path Protocol Hardening

## Goal

Close the hostile-review blockers that determine whether a positive B-TGT-E1 result would mean biological predictive value rather than attention, genomic architecture, repeated benchmark mining, or label construction bias.

This milestone is intentionally narrow. It precedes BIG 0F and blocks it.

## Required outputs

- ADR-020 primary gene-assignment eligibility / Combined Nuisance comparator / confirmatory decision rule
- ADR-021 BIG 0F sampling / second-adjudication / contamination protocol
- high-specificity primary gene-assignment classes
- author-named / nearest-gene assignments demoted to secondary sensitivity
- Combined Nuisance Model specification
- mandatory genomic-architecture and cross-trait pleiotropy baselines
- historical GeneModelRelease identity
- typed/cross-field scientific artifact invariants
- confirmatory alpha / MDE / power workflow
- ConfirmatoryProgramBudget
- research-program multiplicity / attempt accounting
- BIG 0F sampling frame + random seed commitment procedure
- deterministic seal-bundle builder + tamper verification
- executable estimand structure contract
- executable endpoint-quality rule template
- executable BIG 0F result contract
- deterministic GO / REDESIGN / NO_GO evaluator
- second-adjudicator protocol
- pilot DEVELOPMENT_EXPOSED exclusion rule
- symmetric non-event historical-audit sample
- mini historical-provider availability audit
- development-only nuisance-headroom study

## Combined Nuisance Model

Required families, where historically reconstructable:

```text
attention
attention momentum
global popularity
annotation density
gene length / historical gene geometry
variant opportunity
regional gene density
LD architecture
cross-trait pleiotropy
historical genetic observability
disease sample-size trajectory
provider/source coverage
```

The headline contrast becomes:

```text
Nuisance + Biological Signal
vs
Nuisance Only
```

## Primary label rule

The primary gene-level endpoint accepts only frozen high-specificity assignment classes.

AUTHOR_NAMED, NEAREST_GENE, positional-only, generic database-gene, and modern-L2G-only mappings cannot independently create a primary positive.

If this leaves inadequate event yield or remains attention-coupled, REDESIGN to a locus-level primary endpoint.

## Statistical gate

Before a confirmatory generation exists, freeze:

- test statistic;
- direction;
- alpha;
- minimum scientifically meaningful effect;
- target power;
- simulation-based power artifact;
- numeric success rule;
- confirmatory-generation budget / alpha-spending rule.

A free-text success threshold is prohibited.

## BIG 0F entry gate

BIG 0F cannot start until:
- local seal-bundle/tamper dry-run passes CI;
- pilot-result and deterministic-decision contracts pass CI;
- pilot sampling rule is frozen;
- target pilot N is frozen from source availability without outcome adjudication;
- numeric GO / REDESIGN / NO-GO threshold categories are defined;
- second-adjudication plan is assigned or the reduced claim ceiling is accepted;
- pilot contamination rule is frozen;
- schemas + semantic invariants reject the hostile-review probes.

---

# BIG 0F — Benchmark Feasibility Pilot

## Goal

Test whether B-TGT-E1 ground truth can be constructed credibly before provider-scale implementation.

This is a scientific feasibility exercise, not a confirmatory model-performance experiment.

A small **DEVELOPMENT-only Combined Nuisance headroom analysis** is allowed because its purpose is to test whether a plausible biological signal has room to improve beyond nuisance structure; all pilot cases remain permanently excluded from sealed confirmation.

## Manual pilot

Adjudicate a small heterogeneous set of future genetic events and measure:
- canonical variant/locus resolution and genome-build/allele harmonization ambiguity;
- LD/reference-panel dependence where proxy matching is used;
- historical genetic-search coverage grade;
- historical genetic observability grade;
- pre-T genetic state: no-observed-signal vs suggestive vs qualifying vs ambiguous;
- historical novelty at T;
- locus-level versus gene-level evidence;
- gene-assignment method and knowledge horizon;
- benchmark disease vs future phenotype relation;
- replication allele/direction/LD/population comparability where applicable;
- cohort/sample overlap and SampleSet identity resolution;
- ScientificEventFamily deduplication / locus-to-many-gene credit impact;
- Past/Future provider-lineage coupling;
- retrospective curation burden;
- ancestry/population metadata availability;
- adjudicator disagreement;
- fraction of unresolved AMBIGUOUS events;
- assignment-class distribution and author-named / nearest-gene fraction;
- correlation between pre-T attention rank and assignment class;
- share of post-T events using pre-T cohorts;
- symmetric non-event audit cost;
- archived field-level source availability;
- Combined Nuisance headroom;
- event-count / rank-variance inputs for simulation-based power.

## Outputs

- pilot event ledger;
- novelty-audit examples;
- gene-assignment examples;
- lineage/overlap examples;
- ambiguity statistics;
- workload estimate;
- externally sealed BIG 0F protocol;
- second-adjudicator agreement report;
- development-only Combined Nuisance headroom report;
- simulation-based power inputs/report;
- GO / REDESIGN / NO-GO recommendation for B-TGT-E1-v0.

## Gate

Do not build provider-scale benchmark machinery if the endpoint cannot be adjudicated with acceptable ambiguity, assignment independence, power/headroom, source availability, and reconstruction burden.

All BIG 0F diseases/events are permanently DEVELOPMENT_EXPOSED and cannot enter a strongest-tier sealed generation.

---

# BIG 1 — Provider Temporal Audit & Temporal Integrity Kernel

## Goal

Determine which sources can support historical science and make future information technically inadmissible.

## Outputs

- provider due-diligence template
- release/availability capability model
- PartialDate / AvailabilityInterval
- TemporalAdmissionDecision
- KnowledgeWatermark algebra
- TemporalGuard
- strict / reconstructed / contaminated temporal policies
- provider audit matrix across candidate cutoff eras
- field-level provider qualification
- Reconstruction Fidelity Study protocol and first verdicts where archived comparisons exist

## Candidate audit eras

Evaluate approximately:

```text
2005
2006
...
2014
```

The initial production cutoff is selected from evidence coverage and outcome observability, not assumed in advance.

## Acceptance

- direct post-cutoff records fail closed
- incomplete date precision is preserved
- UNKNOWN is excluded in strict mode
- transitive watermark contamination is detected
- non-knowledge-bearing code does not acquire a biomedical date merely because it was written later
- provider temporal capabilities and licensing are recorded
- candidate cutoff recommendation is data-driven

## Scientific gate

If no cutoff has defensible historical fidelity, the main benchmark design must change before modeling proceeds.

---

# BIG 2 — Canonical Biomedical Identity

## Goal

Represent biomedical identity without using names or present-day mappings as hidden truth.

## Scope

Initial identity classes:

- diseases
- phenotypes
- genes
- proteins
- protein complexes
- pathways
- publications/studies
- genome assemblies / reference sequences
- genomic variants / loci
- cohorts / datasets / biobanks / consortia / sample sets
- LD reference panels

Drug/chemical identity is added later in BIG 12.

## Outputs

- internal immutable entity IDs
- external identifier assertions
- versioned mapping records
- historical model-visible mapping layer
- modern evaluation bridge
- ambiguity representation
- disease/phenotype-as-of-T representation
- genomic normalization/liftover identity artifacts
- canonical cohort/dataset/SampleSet lineage

## Acceptance

- scientific joins do not require free-text names
- one-to-many mappings remain ambiguous unless evidence resolves them
- evaluation bridge is unreachable from ranking/feature code
- mapping provenance is complete
- small reviewed gold set has measured identity-resolution error

---

# BIG 3 — Evidence, Claims, Provenance & Immutable Snapshots

## Goal

Create a replayable scientific ledger from raw provider bytes to admitted evidence.

## Outputs

- immutable SourceArtifact
- SourceSnapshot / manifest
- SourceRecord
- ScientificClaim
- EvidenceRecord
- ExtractionArtifact / ExtractionQualityCard
- evidence extraction quality policy + source grounding
- evidence method classes
- source channels
- evidence-family / independence semantics
- minimal comparability + ConflictAssessment primitive
- provenance DAG
- content hashing
- reproducible normalized datasets

## Acceptance

- unchanged inputs reproduce identical manifest/content identities
- every evidence item traces to raw source bytes
- every transformation records code/config identity
- non-native extraction retains source span/locator and extractor/version/config
- automated extraction has task/domain-specific quality qualification
- human curation disagreement/adjudication remains auditable
- extractor confidence is not scientific evidence strength
- literature is represented as a source channel, not a strength class
- duplicate database propagation does not create false independent evidence
- contradiction/comparability primitive exists before BIG 7; BIG 10 expands it rather than introducing it from scratch

## Do not build

- giant enterprise data lake
- graph database as truth store
- ML ranking

---

# BIG 4 — Future Outcome Plane & Label Derivation

## Goal

Build ground truth as endpoint-specific future events isolated from historical ranking.

## Outputs

- FutureEvent taxonomy
- physically/logically separate outcome storage
- endpoint definitions and E1 subtype rules
- PreTGeneticState derivation
- label derivation engine
- OutcomeGeneAssignmentPolicy implementation
- OutcomePhenotypeMatchPolicy implementation
- GeneticReplicationAssessment implementation
- HistoricalNoveltyAudit workflow
- cohort/dataset/sample-overlap lineage
- ScientificEventFamily / GeneticDiscoveryEventFamily ledger
- provider-lineage/input-outcome coupling assessment
- blinded outcome-adjudication workflow
- POSITIVE / NEGATIVE_CONFIRMED / UNKNOWN / RIGHT_CENSORED / COMPETING_EVENT / CONFLICTED states
- evaluation-only modern identity bridge

## Acceptance

- ranking code cannot import/query future outcomes
- "not observed" never becomes negative by default
- endpoint labels are reproducible from event ledger + policy version
- future event source coverage is auditable
- event-time and public-availability semantics are preserved
- locus/variant events cannot silently become gene-level positives
- suggestive pre-T signals cannot become E1-NOVEL-STRICT
- related phenotype/risk-factor events cannot silently become exact disease positives
- replication direction/allele/phenotype conflicts are explicit
- novelty ambiguity is explicit
- UNKNOWN cohort/sample overlap is not treated as independent replication
- outcome adjudication provenance is complete

---

# BIG 5 — Historical Benchmark Runtime & Holdout Governance

## Goal

Make Forge Bio measurable before building a sophisticated ranker.

## Outputs

- BenchmarkSpec
- HistoricalKnowledgeView
- historical candidate-universe builder
- DEVELOPMENT / versioned VALIDATION / SEALED_LOCKBOX tiers
- validation-generation lifecycle, access count, and disclosure level
- ranking artifact sealing/hashing
- exact Future Outcome snapshot/ledger/event-family/provider-coupling commitment
- lockbox access ledger
- metric engine including all-frame review-budget utility
- disease-level bootstrap + disease-family/block sensitivity
- MAP/MAR execution lifecycle
- reproducibility command

## Acceptance

- predictions can be frozen before label reveal
- confirmatory execution requires frozen MAP hash
- rankers have no I/O capability outside HistoricalKnowledgeView
- injected post-cutoff future sentinels cannot affect ranking
- candidate universe itself is historical
- repeated lockbox access is logged and invalidates untouched status according to policy
- validation generations become SPENT_FOR_MODEL_SELECTION after adaptive reuse
- exact outcome snapshot/ledger/adjudication/identity-bridge commitment is verified before evaluation

---

# BIG 6 — Stage-0 Controls & Research-Attention Baselines

## Goal

Establish the real performance floor.

## Required controls

- random
- historical research attention / publication count
- historical attention momentum / research-growth velocity
- historical discoverability / observation-propensity control
- evidence-volume popularity
- entity popularity
- graph-degree popularity where historical graph exists
- simple deterministic biological baseline
- benchmark falsification/null controls where applicable

## North-star comparison

Primary value is expressed as a baseline delta, for example:

```text
ΔRecall@K vs research attention
ΔNDCG@K vs research attention
Enrichment@K over attention baseline
```

## Acceptance

- every baseline is temporally clean
- all scores reproduce exactly from manifest
- disease-level confidence intervals implemented
- metrics are cross-checked against independent implementations/golden fixtures

## Stop condition

If benchmark construction itself makes controls behave implausibly, stop and audit the benchmark.

---

# BIG 7 — First Disease–Gene Time-Machine Experiment (B-TGT-A1 v0)

## Goal

Answer the first scientific question with the smallest credible model.

## Design

Start with a provider-audit-selected cutoff, likely within the 2005–2014 range.

Use a modest disease set with:

- development diseases
- sealed diseases
- multiple disease families
- varied research intensity
- varied evidence density
- varied candidate-universe sizes

## Initial features

Only historically admissible transparent features such as:

- human genetic evidence
- functional evidence
- pathway/process evidence
- evidence independence
- evidence age
- contradiction burden
- evidence coverage

No LLM, PLM, GNN, current graph, or future-trained representation.

## Outputs

- frozen MAP
- deterministic target ranking
- sealed ranking artifact
- MAR
- failure analysis

## Acceptance

- zero unresolved temporal-integrity violations
- reproducible historical snapshot
- sealed evaluation completed
- result compared to research-attention and discoverability controls
- zero-event disease policy enforced
- fixed K accompanied by a candidate-universe-normalized metric
- all-frame observed-event review-budget utility reported
- disease-family/block CI sensitivity reported
- null/placebo controls do not reproduce the claimed signal
- strict novelty/search-coverage, phenotype-match, genomic-harmonization/LD, locus-to-gene, replication, event-family-credit, provider-coupling, observability, and outcome-source sensitivities pass
- exact Future Outcome snapshot commitment matches the frozen MAP
- strongest L3 outcome adjudication is rank-blinded
- results reported even if negative


## Early prospective shadow ledger

As soon as a stable baseline/ranker exists in BIG 7, begin a **private externally timestamped prospective prediction ledger**. Predictions remain under custody to limit self-fulfilling research-attention effects. This starts the prospective clock early; it does not upgrade claims until independent future outcomes mature.

---

# BIG 8 — Classical ML Ranking

## Goal

Determine whether learned weighting adds predictive information beyond transparent heuristics.

## Candidate models

- regularized logistic models
- learning-to-rank models
- gradient boosting
- PU-aware approaches where label semantics require them

## Rules

- nested temporal training per MODEL_TRAINING_POLICY.md
- each training anchor has features as-of t_i and labels only from a fully observed window ending no later than T_eval
- no post-T_eval outcome may enter training
- grouped disease-aware validation
- complete feature lineage
- model knowledge horizon recorded

## Acceptance

- predefined improvement on development benchmark
- sealed confirmation at milestone boundary
- confidence interval for lift over best simpler baseline
- no degradation hidden by aggregate averages

---

# BIG 9 — Uncertainty, Applicability & Calibration

## Goal

Represent when a ranking is uncertain or outside the evaluated operating domain.

## Outputs

- UncertaintyBundle
- evidence-quality uncertainty
- identity uncertainty
- temporal uncertainty
- model-form uncertainty
- data-completeness uncertainty
- contradiction dimension
- applicability/OOD flags
- calibration diagnostics only for endpoints with sufficient events

## Acceptance

- UNKNOWN uncertainty never becomes zero
- OUT_OF_DOMAIN is explicit
- probabilities are not displayed unless endpoint/horizon calibration requirements are met
- calibration is checked on later cutoffs than fitting where possible

---

# BIG 10 — Counter-Evidence & Contradiction Engine

## Goal

Prevent confirmation-only hypothesis ranking.

## Outputs

- comparability gate
- contradiction taxonomy
- Support / Counter-evidence / Gaps dossier
- independence-aware counts
- contested-candidate state
- curated contradiction validation set

## Acceptance

- different tissues/species/endpoints are not automatically called contradictions
- hard direction conflicts are surfaced
- model score cannot suppress material counter-evidence
- reviewer agreement measured on curated examples

---

# BIG 11 — Multi-Disease / Multi-Cutoff Generalization

## Goal

Determine whether historical signal survives outside development conditions.

## Evaluations

- unseen diseases
- leave-disease-family-out
- later/earlier cutoff
- source ablation
- evidence-density strata
- research-intensity strata
- candidate-universe-size strata

## Acceptance

- no tuning on sealed family holdouts
- baseline lift persists across more than one disease family
- fragile single-family performance is reported as limited applicability

## Scientific gate

This milestone determines whether the project has platform-level target-prioritization value rather than disease-specific demonstration value.

---

# BIG 12 — Drug / Active-Moiety Historical Layer

## Goal

Add therapeutic-chemical identity and historical drug-target evidence early enough to test product-value translation before expensive representation learning.

## Scope

- exact chemical structure identity
- parent/active moiety
- active ingredient
- medicinal product
- combination distinction
- historical drug-target relationships
- historical indication state
- historical approval state
- mode-of-action direction

## Outputs

- chemical/drug identity model
- historically admissible as-of-T drug universe
- drug ↔ active moiety ↔ product mappings
- drug-target evidence ledger
- provider qualification for chemical/pharmacology sources

## Acceptance

- salts/products/combinations are not silently collapsed
- present-day indication fields do not leak into historical scoring
- active-moiety candidate universe is provably as-of-T
- mechanism direction is explicit

---

# BIG 13 — Drug Repurposing Historical Benchmark (B-REP)

## Goal

Test whether target/mechanism signal translates into useful therapeutic prioritization before investing in advanced graph/deep models.

## Separate endpoints

At minimum distinguish:

- repurposing research/clinical entry
- efficacy evidence
- regulatory approval
- mechanistically informative failure

Trial entry measures where the field went, not whether treatment worked.

## Baselines

- drug popularity
- research attention
- number of prior indications
- target-overlap guilt-by-association
- network proximity where historically admissible
- deterministic evidence ranking

## Acceptance

- B-REP is evaluated against field-attention controls on sealed data
- success endpoints are reported separately from trial-entry endpoints
- candidate universe and drug identity are historically safe
- no patient-level or treatment-recommendation output

## Scientific gate

If B-TGT signal does not translate into B-REP value, keep the platform scoped to biological/target prioritization until the failure mode is understood.

---

# BIG 14 — Historical Graph Projections & Graph Features

## Goal

Add relational biology only after B-TGT and an initial B-REP value test exist.

## Outputs

- cutoff-specific graph projection
- evidence-bearing edges
- path/network features
- degree-controlled analyses
- network proximity
- historical metapath features where justified

## Acceptance

- every edge traces to admitted evidence
- graph topology is recomputed per historical view
- graph features add value beyond degree/popularity controls
- no present-day topology enters strict mode

## Do not build

- graph database as source of truth

---

# BIG 15 — Representation Learning

## Goal

Test whether learned graph representations add value beyond simple historical graph statistics and existing repurposing baselines.

## Candidate families

- KGE
- R-GCN / HGT-like approaches
- other heterogeneous graph models

## Rules

- training occurs on historical views
- similarity-aware and family-aware splits
- compute cost tracked
- no prestige exemption: advanced models must beat simpler graph and therapeutic baselines

## Acceptance

- clear improvement on predefined generalization benchmark
- gain survives disease-family holdout
- leakage audit passes
- model artifact has complete training provenance

---

# BIG 16 — Structural, Safety/ADMET & Pretrained Evidence Extensions

## Goal

Add expensive/supporting modalities only after the historical benchmark engine is mature.

## Scope

- historically released structures
- structural compatibility evidence
- computational safety/ADMET evidence
- historical-safe pretrained representations where training cutoff is known
- contaminated modern-prior arm where it is not

## Rules

Each new modality must show incremental historical value through ablation.

If it does not, it remains a present-day exploratory feature rather than a core ranking dependency.

## Acceptance

- structure release date enforced
- pretrained-model horizon recorded
- unknown model training composition => historical_safe = UNKNOWN
- strict vs contaminated deltas reported
- no synthesis/manufacturing workflow

---

# BIG 16A — Scientific Digital Twin Engine

## Goal

Instantiate validated disease/pathogen/pathogen-host/therapeutic twins after the scientific evidence and modality layers are mature enough to support them.

## Initial implementation order

1. T1 Dynamic Knowledge Twins
2. T2 Mechanistic Twins for narrowly defined systems
3. T3 Predictive Twins only after held-out/future validation
4. T4 Intervention Simulation Twins only after T3-level predictive validity and sensitivity/VVUQ requirements are met

## Required inputs

- canonical identity and scientific profiles
- evidence/provenance ledger
- temporal snapshots
- mechanism/state-model artifact with structural knowledge provenance/watermark
- update-policy artifact with provenance/watermark
- parameter provenance
- uncertainty model
- validation target
- applicability domain

## Acceptance

- every twin has an explicit maturity level
- TwinState history is immutable/versioned
- historical twins cannot ingest future evidence through model structure/topology, update policies, parameters, preprocessing, or calibration
- T3 prediction claims are governed by MAP/MAR/ValidationGeneration and reproduce on held-out/future data
- T4 simulations require causal assumptions/intervention semantics/identifiability and report uncertainty, sensitivity, and applicability
- no patient-specific diagnosis/treatment/dosing functionality

## Scientific gate

A plausible simulation is not enough. If predictive validation fails, the twin remains T1/T2 and the failure is reported.

---

# BIG 17 — Research Workbench & Controlled Automation

## Goal

Improve researcher throughput after scientific semantics are stable.

## Scope

Present-day "Investigate Disease X" workflow may orchestrate:

- evidence acquisition
- candidate generation
- counter-evidence review
- ranking
- report generation

## Agent rules

An agent/LLM:

- uses deterministic services/tools
- logs every action
- cannot grant validation
- cannot alter temporal policy
- cannot alter ground-truth labels
- cannot silently write evidence without provenance
- cannot create patient treatment instructions

## Acceptance

- all actions reproducible/auditable
- claims linter passes
- human review shows no evidence-integrity degradation

---

# BIG 18 — Prospective Shadow Validation

## Goal

Move beyond retrospective reconstruction.

## Method

Freeze new predictions today:

```text
timestamp
MAP
candidate universe
ranking
evidence dossier
model/data hashes
public/external commitment hash
```

Then wait for future evidence.

## Outputs

- prospective prediction ledger
- immutable external timestamp anchoring
- prospective endpoint evaluation
- longitudinal MARs

## Acceptance

- predictions cannot be changed after registration
- future validation source is independent of the prediction process
- sufficient follow-up before scientific claims
- baseline comparisons remain preregistered

---

# 4. MVP definition

The smallest valuable MVP is not a dashboard.

It is:

> **A reproducible historical disease–gene association experiment demonstrating whether transparent, temporally clean evidence ranking contains signal beyond research-attention and discoverability controls.**

Practical MVP target:

```text
BIG 0 → BIG 7
```

It should contain:

- one provider-audit-selected cutoff era
- one B-TGT endpoint family
- a small multi-disease set
- development + sealed cases
- 2–3 defensible evidence modalities
- historical candidate universe
- random baseline
- research-attention baseline
- attention-momentum/discoverability baseline
- deterministic scientific baseline
- explicit E1 endpoint subtype + PreTGeneticState + HistoricalGeneticSearchCoverage
- scientific estimand + zero-event disease policy + all-frame utility
- genomic identity/harmonization/LD policy + OutcomeGeneAssignmentPolicy + OutcomePhenotypeMatchPolicy + GeneticReplicationPolicy + HistoricalNoveltyAudit
- ScientificEventFamily credit + ProviderLineage/InputOutcomeCoupling + GeneticObservabilityAtT
- validation-generation lifecycle + exact Future Outcome snapshot commitment
- MAP + MAR
- temporal leakage and benchmark-falsification suite
- complete provenance + BenchmarkDesignProvenance

No GUI is required.

---

# 5. Explicitly deferred from MVP

Do not build in MVP:

- graph database
- GNN
- KG embeddings
- foundation-model dependency
- LLM ranking
- research agent
- docking pipeline
- de novo molecule generation
- combination therapy engine
- broad ADMET stack
- patient data
- probability claims without calibration
- public multi-tenant SaaS layer

---

# 6. Program gates

## Gate 1 — Historical fidelity

Can the provider stack reconstruct a defensible historical state?

If no: change cutoff/source design.

## Gate 2 — Benchmark validity

Do temporal leakage tests, genomic identity/harmonization/LD tests, candidate-universe/observability tests, strict-novelty coverage rules, phenotype matching, outcome gene-assignment rules, genetic replication rules, event-family/provider-coupling rules, cross-anchor reuse controls, historical-novelty audits, ascertainment controls, zero-event/all-frame estimand rules, validation-generation governance, exact outcome commitments, analyst-hindsight governance, and label semantics survive verification?

If no: do not model.

## Gate 3 — Baseline signal

Does transparent evidence ranking beat field-attention controls on development data?

If no: audit data/scientific premise.

## Gate 4 — Sealed confirmation

Does lift survive a frozen sealed benchmark?

If no: no stronger claim is earned.

## Gate 5 — Generalization

Does signal survive diseases/families/cutoffs?

If no: restrict applicability.

## Gate 6 — Repurposing value

Does target/mechanism signal translate into B-REP value?

If no: keep the platform scoped to target prioritization while investigating the gap.

## Gate 7 — Advanced ML

After B-TGT and B-REP baselines exist, do graph/deep models improve over simpler baselines?

If no: do not keep complexity for appearance.

## Gate 8 — Prospective evidence

Do timestamped present-day predictions validate above baseline over time?

This is the ultimate long-term evidence.

---

# 7. Current execution state

```text
Current milestone: BIG 0F-0 critical-path hardening → BIG 0F
Implementation status: not started
Architecture status: PRE-CODE CANDIDATE V1
Scientific contract: PRE-CODE CANDIDATE V1
Historical benchmark result: none yet
ML result: none yet
Repurposing result: none yet
Prospective result: none yet
```

The next implementation work must start from BIG 0 and should not skip directly to models.


---

# 8. Pre-code hardening references

Implementation order is governed by:

- [BENCHMARK_V0_SPEC.md](BENCHMARK_V0_SPEC.md)
- [TEMPORAL_SEMANTICS.md](TEMPORAL_SEMANTICS.md)
- [EVIDENCE_TAXONOMY.md](EVIDENCE_TAXONOMY.md)
- [IDENTITY_POLICY.md](IDENTITY_POLICY.md)
- [PROVIDER_QUALIFICATION.md](PROVIDER_QUALIFICATION.md)
- [MODEL_TRAINING_POLICY.md](MODEL_TRAINING_POLICY.md)
- [PRE_CODE_CHECKLIST.md](PRE_CODE_CHECKLIST.md)
- [SCIENTIFIC_RED_TEAM_GAPS.md](SCIENTIFIC_RED_TEAM_GAPS.md)
- [GLOSSARY.md](GLOSSARY.md)
- [CORE_TYPES.md](CORE_TYPES.md)
- [GOLDEN_SYNTHETIC_WORLD.md](GOLDEN_SYNTHETIC_WORLD.md)
- [DEPENDENCY_RULES.md](DEPENDENCY_RULES.md)
- [PROHIBITED_DEPENDENCY_FIXTURES.md](PROHIBITED_DEPENDENCY_FIXTURES.md)
- [BENCHMARK_ESTIMAND_V0.md](BENCHMARK_ESTIMAND_V0.md)
- [SCIENTIFIC_SPEC_GOVERNANCE.md](SCIENTIFIC_SPEC_GOVERNANCE.md)
- [LOCKBOX_POLICY.md](LOCKBOX_POLICY.md)
- [schemas/QOI_SCHEMA.md](schemas/QOI_SCHEMA.md)
- [schemas/CONTEXT_OF_USE_SCHEMA.md](schemas/CONTEXT_OF_USE_SCHEMA.md)
- [schemas/MAP_SCHEMA.md](schemas/MAP_SCHEMA.md)
- [schemas/MAR_SCHEMA.md](schemas/MAR_SCHEMA.md)
- [adr/ADR-006-outcome-gene-assignment.md](adr/ADR-006-outcome-gene-assignment.md)
- [adr/ADR-007-benchmark-design-provenance.md](adr/ADR-007-benchmark-design-provenance.md)
- [adr/ADR-008-outcome-phenotype-matching.md](adr/ADR-008-outcome-phenotype-matching.md)
- [adr/ADR-009-genetic-replication-and-signal-state.md](adr/ADR-009-genetic-replication-and-signal-state.md)
- [adr/ADR-010-validation-generations-and-outcome-freeze.md](adr/ADR-010-validation-generations-and-outcome-freeze.md)
- [adr/ADR-011-genomic-identity-harmonization.md](adr/ADR-011-genomic-identity-harmonization.md)
- [adr/ADR-012-historical-genetic-observability.md](adr/ADR-012-historical-genetic-observability.md)
- [adr/ADR-013-event-identity-source-coupling.md](adr/ADR-013-event-identity-source-coupling.md)
- [adr/ADR-014-operating-mode-data-policy.md](adr/ADR-014-operating-mode-data-policy.md)
- [../schemas/README.md](../schemas/README.md)
- [DISEASE_PATHOGEN_THERAPEUTIC_PROFILE.md](DISEASE_PATHOGEN_THERAPEUTIC_PROFILE.md)
- [SCIENTIFIC_DIGITAL_TWIN_ARCHITECTURE.md](SCIENTIFIC_DIGITAL_TWIN_ARCHITECTURE.md)
- [MODEL_CREDIBILITY_POLICY.md](MODEL_CREDIBILITY_POLICY.md)
- [QUANTITATIVE_SEMANTICS.md](QUANTITATIVE_SEMANTICS.md)
- [EVIDENCE_EXTRACTION_POLICY.md](EVIDENCE_EXTRACTION_POLICY.md)
- [BENCHMARK_LIFECYCLE_POLICY.md](BENCHMARK_LIFECYCLE_POLICY.md)
- [adr/ADR-015-scientific-digital-twin-semantics.md](adr/ADR-015-scientific-digital-twin-semantics.md)
- [adr/ADR-016-model-credibility-numerical-verification.md](adr/ADR-016-model-credibility-numerical-verification.md)
- [adr/ADR-017-quantitative-semantics.md](adr/ADR-017-quantitative-semantics.md)
- [adr/ADR-018-evidence-extraction-quality.md](adr/ADR-018-evidence-extraction-quality.md)
- [adr/ADR-019-source-benchmark-lifecycle.md](adr/ADR-019-source-benchmark-lifecycle.md)
- [adr/](adr/)

No milestone status may be advanced merely because code exists. Acceptance requires its scientific/verification gate.
