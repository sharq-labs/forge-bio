# Scientific Red-Team Gap Register

**Status:** ACTIVE — policy hardening through BIG 0R3 closed; feasibility/operational blockers remain  
**Scope:** Forge Bio pre-code benchmark, inference, governance, and outcome-label integrity  
**Authority:** This register supplements PRE_CODE_CHECKLIST.md.

A gap marked **CLOSED-POLICY** has an accepted normative design but may still require P1 implementation/verification.

A gap marked **OPEN-P0** blocks production scientific implementation.

## 1. Failure classes

Forge Bio treats these as distinct scientific failure modes:

1. temporal leakage;
2. outcome-construction leakage;
3. ascertainment / discoverability bias;
4. researcher hindsight / design-time leakage;
5. estimand ambiguity;
6. identity / locus-to-gene assignment contamination;
7. phenotype/disease mismatch;
8. false replication from incompatible or dependent evidence;
9. validation-set adaptive reuse;
10. moving Future Outcome ground truth;
11. zero-event disease review-budget blind spots;
12. cross-disease statistical dependence;
13. claim-language inflation;
14. licensing/data-rights mismatch.

A benchmark can be technically clean and still fail scientifically.

## 2. First-pass gap closure ledger

### P0-R1 — Endpoint subtype ambiguity

**Status:** CLOSED-POLICY

Resolved by:
- E1-NOVEL-STRICT;
- E1-MATURATION;
- E1-REPLICATION;
- E1-CROSSMODAL;
- one primary subtype frozen per confirmatory MAP.

Normative source:
- BENCHMARK_V0_SPEC.md
- ADR-009

### P0-R2 — Locus-to-gene outcome contamination

**Status:** CLOSED-POLICY

Resolved by:
- separate locus/variant events and gene assignment;
- OutcomeGeneAssignmentPolicy;
- modern learned L2G cannot act as unqualified strict gene-level truth;
- assignment sensitivity required.

Normative source:
- ADR-006

### P0-R3 — Historical novelty false positives

**Status:** CLOSED-POLICY / OPEN-FEASIBILITY

Policy is defined:
- HistoricalNoveltyAudit;
- PreTGeneticState;
- ambiguity fails closed.

Still requires pilot measurement of novelty ambiguity and historical-audit feasibility.

### P0-R4 — Discoverability / observation-propensity confounding

**Status:** CLOSED-POLICY / P1-IMPLEMENTATION

Required controls now include:
- attention momentum;
- discoverability/observation-propensity baseline;
- research-intensity/evidence-density stratification.

### P0-R5 — Zero-future-event disease estimand

**Status:** CLOSED-POLICY / OPEN-P0 FINAL FREEZE

Policy now:
- zero-event diseases remain in benchmark accounting;
- primary event-ranking estimand is explicitly conditional;
- no fabricated negatives;
- secondary all-frame observed-event review-budget utility is mandatory.

Final numerical estimand choices are frozen only after feasibility.

### P0-R6 — Researcher hindsight / design-time leakage

**Status:** CLOSED-POLICY

Resolved by:
- BenchmarkDesignProvenance;
- ranking/adjudication/custody roles;
- sealed-disease identity governance;
- frozen methodology before outcome reveal;
- strongest-tier blinding requirements.

Normative source:
- ADR-007
- LOCKBOX_POLICY.md

### P0-R7 — Disease-regime heterogeneity

**Status:** CLOSED-POLICY

Primary V0 is restricted to:

```text
common-complex germline disease/trait genetics
```

Mendelian/rare disease, somatic cancer-driver genetics, pharmacogenomics, and materially different regimes are excluded from the pooled V0 headline.

### P0-R8 — Outcome adjudication independence

**Status:** CLOSED-POLICY / P1-VERIFY

For strongest L3:
- sealed adjudicators must be blind to rank/order;
- violation automatically downgrades the tier;
- ambiguous/assignment-dependent cases follow frozen dual-review rules.

Normative source:
- ADR-007
- ADR-010

### P0-R9 — BIG 0 artifact mismatch

**Status:** CLOSED

Normative artifacts now exist:
- glossary;
- QoI schema;
- Context-of-Use schema;
- MAP schema;
- MAR schema;
- core scientific types;
- golden synthetic world;
- dependency rules;
- prohibited-dependency fixtures;
- estimand proposal;
- lockbox/spec governance.

### P0-R10 — Licensing posture

**Status:** CLOSED-POLICY

ADR-005 is accepted with a commercial-later engineering posture.

Repository code/docs are Apache-2.0. Provider data and derived artifacts retain source-specific licensing/redistribution constraints.

## 3. Second-pass gap closure ledger

### P0-R11 — Suggestive pre-T genetics mislabeled as novel

**Status:** CLOSED-POLICY

Resolved by `PreTGeneticState`.

Only:

```text
NO_SIGNAL_OBSERVED
+
NOVEL_CONFIRMED
```

may support E1-NOVEL-STRICT.

`SUGGESTIVE → qualifying` is E1-MATURATION.

Normative source:
- ADR-009

### P0-R12 — Trait/phenotype promoted to disease outcome

**Status:** CLOSED-POLICY

Resolved by OutcomePhenotypeMatchPolicy.

Primary V0 does not silently count:
- risk factors;
- surrogate traits;
- intermediate phenotypes;
- broadly related phenotypes.

Normative source:
- ADR-008

### P0-R13 — Weak genetic replication semantics

**Status:** CLOSED-POLICY / OPEN-P0 QUALITY THRESHOLD

Replication assessment now includes:
- phenotype;
- locus/variant;
- effect allele;
- allele harmonization;
- effect direction;
- LD relation;
- population/ancestry;
- cohort/sample independence;
- analysis compatibility;
- heterogeneity.

Genome-wide significance alone is not a complete endpoint-quality rule.

The final endpoint-quality threshold remains OPEN-P0 until the feasibility/provider audit.

Normative source:
- ADR-009

### P1-R11 — Validation-set adaptive reuse

**Status:** CLOSED-POLICY / P1-IMPLEMENTATION

Validation sets are versioned generations:

```text
ACTIVE
SPENT_FOR_MODEL_SELECTION
RETIRED
```

A spent generation is not called untouched evidence.

Normative source:
- ADR-010

### P1-R12 — Moving Future Outcome snapshot

**Status:** CLOSED-POLICY / P1-IMPLEMENTATION

Before sealed evaluation the project commits:
- outcome source releases;
- snapshot IDs/digest;
- outcome-ledger digest;
- adjudication-batch digest;
- evaluation identity-bridge digest;
- outcome-policy versions.

A changed release creates a new evaluation generation.

Normative source:
- ADR-010

### P1-R13 — Conditional estimand hides full review burden

**Status:** CLOSED-POLICY / P1-IMPLEMENTATION

Required secondary all-frame measures include:
- observed qualifying event yield per total review budget;
- event-bearing disease coverage;
- zero-event disease review burden.

These are observed-event utility metrics, not biological precision.

### P1-R14 — Cross-disease dependence

**Status:** CLOSED-POLICY / P1-IMPLEMENTATION

Primary disease-level intervals require a preregistered disease-family/block or other cluster-aware dependence sensitivity.

### P0-R15 — "Target Discovery" claim inflation

**Status:** CLOSED-POLICY

V0 is now described as:

```text
B-TGT-A1 / B-TGT-E1-v0
Disease–Gene Association Prioritization
```

It does not by itself establish:
- causal target status;
- intervention direction;
- tractability;
- clinical value.

The B-TGT umbrella may later contain stronger target-discovery benchmarks.

## 4. Third-pass / BIG 0R3 closure ledger

### P0-R16 — Variant/locus not first-class

**Status:** CLOSED-POLICY

Resolved by ADR-011 and IDENTITY_POLICY:
- GenomeAssembly;
- ReferenceSequence;
- GenomicVariant;
- GenomicLocus;
- canonical normalized allele identity;
- rsID treated as an external identifier.

### P0-R17 — Genome build / allele harmonization / LD provenance

**Status:** CLOSED-POLICY / OPEN-FEASIBILITY

Policy now requires provenance-bearing normalization/liftover/strand resolution and LDRelation with population, reference panel, release, assembly, metric, and value.

Pilot must measure harmonization ambiguity and LD/reference-panel dependence.

### P0-R18 — Phenotype and cohort/sample identity gaps

**Status:** CLOSED-POLICY / P1-VERIFY

PhenotypeConcept, Cohort, Dataset, Biobank, Consortium, and SampleSet are first-class identities. Identity gold sets must verify aliases, releases, overlap, and phenotype relations.

### P0-R19 — Low historical coverage masquerading as novelty

**Status:** CLOSED-POLICY / OPEN-FEASIBILITY

E1-NOVEL-STRICT now requires a MAP-frozen minimum HistoricalGeneticSearchCoverage grade.

Below-threshold coverage yields AMBIGUOUS rather than NO_SIGNAL_OBSERVED.

KNOWN_TO_RANKER_AT_T and KNOWN_PUBLICLY_AT_T are distinct.

Pilot must measure coverage-grade distribution and provider-missed public knowledge.

### P0-R20 — One scientific event counted multiple times

**Status:** CLOSED-POLICY / OPEN-FEASIBILITY

ScientificEventFamily / GeneticDiscoveryEventFamily separate underlying discovery from preprint/publication/database manifestations.

Default V0 primary credit is at most one event credit per event family.

Pilot must measure event-family deduplication and locus-to-many-gene credit sensitivity.

### P1-R15 — Rolling-anchor duplicate event weight

**Status:** CLOSED-POLICY / P1-IMPLEMENTATION

CrossAnchorEventReusePolicy groups labels by ScientificEventFamily, bounds total event-family training weight, and requires effective-sample-size reporting.

### P0-R21 — Past/Future provider coupling

**Status:** CLOSED-POLICY / OPEN-FEASIBILITY

ProviderLineage and InputOutcomeCouplingAssessment now capture shared upstream sources, curation pipelines, ontologies, and identity mapping families.

Pilot/provider audit must estimate coupling; confirmatory work requires same-pipeline exclusion or external-source sensitivity when material.

### P0-R22 — Operating-mode enum collision

**Status:** CLOSED-POLICY

ADR-014 separates:
- ScientificOperatingMode;
- HistoricalDataPolicy;
- provider/field qualification.

CONTAMINATED_MODERN_PRIOR is a run classification, not a reconstruction-policy enum.

### P0-R23 — ADR status chain inconsistent/stale

**Status:** CLOSED

ADR-001..004 are accepted with amendment references, ADR-005 is decided, and ADR-006 is aligned with E1-NOVEL-STRICT / ADR-012 coverage semantics.

### P1-R16 — Validation feedback granularity untracked

**Status:** CLOSED-POLICY / P1-IMPLEMENTATION

Validation generations now record maximum disclosure level:
- AGGREGATE_ONLY;
- SUBGROUP;
- PER_CASE;
- FULL_LABEL.

### P1-R17 — Markdown-only schemas

**Status:** CLOSED-POLICY / P1-IMPLEMENTATION

Executable JSON Schemas now exist for QoI/MAP/MAR under `/schemas`. Runtime freeze validation still must be implemented/tested.

### P1-R18 — Repository governance not enforced

**Status:** PARTIAL / OPEN-OPERATIONAL

Repository now contains:
- LICENSE;
- CODEOWNERS;
- scientific PR template;
- independent-review policy.

GitHub branch protection/ruleset must still be enabled and verified before FROZEN V1. Self-merge without independent review does not satisfy freeze governance.

## 5. Active P0 blockers after BIG 0R3

Production scientific implementation remains blocked by the following evidence/owner decisions:

1. **Final B-TGT-E1 estimand freeze**
   - primary metric;
   - K/review budget;
   - normalized companion metric;
   - acceptable zero-event fraction;
   - minimum event-bearing disease count;
   - CI-width requirement.

2. **Final endpoint evidence-quality threshold**
   - exact qualifying statistical/evidence rule;
   - required replication quality;
   - handling of heterogeneity;
   - minimum lineage/phenotype/gene-assignment quality.

3. **Manual outcome feasibility pilot**
   must measure:
   - canonical variant/locus resolution;
   - genome-build/liftover/allele-harmonization ambiguity;
   - LD/reference-panel dependence;
   - HistoricalGeneticSearchCoverage distribution;
   - GeneticObservabilityAtT distribution;
   - PreTGeneticState distribution;
   - novelty ambiguity;
   - provider-missed KNOWN_PUBLICLY_AT_T cases;
   - locus-to-gene assignment dependence;
   - phenotype-match ambiguity;
   - replication comparability / direction conflicts;
   - cohort/SampleSet overlap ambiguity;
   - ScientificEventFamily deduplication / locus-credit sensitivity;
   - Past/Future provider-coupling risk;
   - retrospective-curation burden;
   - ancestry/population metadata coverage;
   - adjudicator disagreement;
   - label-construction workload.

4. **Pilot GO / REDESIGN / NO-GO verdict**
   for B-TGT-E1-v0.

These are not documentation gaps and must not be checked off without evidence.

## 6. P1 requirements before sealed confirmation

At minimum:

- ProviderCards complete;
- Future Outcome providers independently qualified;
- reconstruction fidelity measured;
- disease frame and CandidateUniverse frozen;
- development/validation/sealed generations frozen;
- validation-generation access/status tracked;
- exact Future Outcome snapshot commitment frozen;
- OutcomeGeneAssignmentPolicy tested;
- OutcomePhenotypeMatchPolicy tested;
- GeneticReplicationPolicy tested;
- HistoricalNoveltyAudit tested;
- cohort/sample-overlap lineage coverage measured;
- strongest L3 outcome adjudication verified rank-blind;
- ancestry/population coverage reported;
- publication/reporting-bias sensitivity planned;
- all-frame utility implemented;
- disease-family/block dependence sensitivity frozen;
- negative/null controls frozen;
- MAP/ranking/outcome commitments verified;
- genomic identity/harmonization gold sets measured;
- HistoricalGeneticSearchCoverage threshold frozen;
- observability sensitivity universe frozen;
- ScientificEventFamily ledger/credit policy tested;
- CrossAnchorEventReusePolicy tested before supervised ML;
- provider-coupling sensitivity frozen;
- executable schema validation implemented;
- lockbox and branch-governance controls operationally verified.

## 7. Stop rule

No result may be described as historical biological discovery signal if a plausible uncontrolled explanation is that the method predicts:

- research attention;
- measurement opportunity;
- statistical power;
- known suggestive signals becoming mature;
- phenotype/risk-factor proxying;
- database curation;
- modern locus-to-gene assignment;
- non-independent replication;
- validation-set adaptation;
- outcome-snapshot drift;
- genome-build/allele normalization artifacts;
- ancestry/reference-panel-specific LD artifacts;
- low historical search coverage;
- duplicated scientific-event manifestations;
- repeated anchor credit for one discovery;
- shared Past/Future curation pipeline behavior.

Those explanations must be controlled, stratified, falsified, or retained explicitly as limitations.


## BIG 0R4 scientific-twin closure ledger

### R4-01 — Twin maturity text not machine-enforced

**Status:** CLOSED-POLICY / EXECUTABLE-SCHEMA

The Scientific Twin JSON Schema now uses maturity-specific conditional requirements:
- T1 requires dynamic state + update-policy artifact;
- T2 requires state-model artifact + parameters + verification;
- T3 requires prediction spec + MAP + MAR + ValidationGeneration + BenchmarkDesignProvenance + validation artifact;
- T4 inherits T3 and adds perturbation/sensitivity/causal/intervention/identifiability requirements.

Executable positive/negative schema tests enforce these cases.

### R4-02 — Historical twin had no explicit cutoff

**Status:** CLOSED-POLICY / EXECUTABLE-SCHEMA

STRICT_HISTORICAL and HISTORICAL_INPUT_MODERN_PRIOR twin/profile artifacts require explicit cutoff T. `valid_at` is not a substitute.

### R4-03 — Future knowledge hidden in state-model structure

**Status:** CLOSED-POLICY / P1-IMPLEMENTATION

TwinStateModelArtifact and TwinUpdatePolicyArtifact are knowledge-bearing unless proven otherwise. Their structure, biomedical priors, transition rules, provenance, and watermarks join the twin's transitive watermark.

### R4-04 — Parallel validation regime

**Status:** CLOSED-POLICY / P1-IMPLEMENTATION

T3/T4 reuse MAP, MAR, ValidationGeneration, BenchmarkDesignProvenance, and lockbox/outcome commitments where applicable.

### R4-05 — Missing profile/twin dependency wall

**Status:** CLOSED-POLICY / P1-IMPLEMENTATION

DEPENDENCY_RULES now prohibits historical profile/twin construction from importing FutureEvent, lockbox readers, evaluation-only bridges, future validation labels, or unrestricted current/latest providers.

### R4-06 — Profiles were Markdown-only

**Status:** CLOSED-POLICY / EXECUTABLE-SCHEMA

Executable schemas now exist for Disease, Pathogen, Virus extension, PathogenHost, and Therapeutic profiles.

### R4-07 — T4 associational simulation could masquerade as intervention

**Status:** CLOSED-POLICY / P1-IMPLEMENTATION

T4 requires CausalAssumptionSet, InterventionSemantics, IdentifiabilityStatus, perturbation artifacts, sensitivity artifacts, and uncertainty propagation. NOT_IDENTIFIED/UNKNOWN cannot support T4.

### R4-08 — Digital-twin terminology could overclaim clinical meaning

**Status:** CLOSED-POLICY

"Forge Bio Scientific Twin" is explicitly a project-defined research construct. Patient/clinical digital-twin claims require a future separate Context of Use.

### R4-09 — Twin maturity confused with scientific claim maturity

**Status:** CLOSED-POLICY

DigitalTwinMaturityLevel T0–T4 and ClaimMaturityLevel L0–L6 are independent ladders. T3 does not imply L3 and vice versa.

### R4-10 — Spec CI only checked file shape

**Status:** CLOSED-TEST-HARNESS

Spec Integrity now executes JSON Schema positive/negative tests, including invalid T1/T2/T3/T4 and missing historical cutoff cases.

### R4-11 — Repository enforcement

**Status:** OPEN-OPERATIONAL

Branch protection / required independent review remains unresolved under GitHub Issue #2 and blocks FROZEN V1, though it does not block BIG 0F exploratory feasibility work.


## BIG 0R5 model-credibility / quantitative-integrity closure ledger

### R5-01 — VVUQ not tied tightly enough to Context of Use

**Status:** CLOSED-POLICY / P1-IMPLEMENTATION

CredibilityAssessmentArtifact now ties model credibility to the exact research decision, model influence, consequence-if-wrong, and CoU.

### R5-02 — Quantitative values could carry ambiguous unit/scale/transform semantics

**Status:** CLOSED-POLICY / EXECUTABLE-SCHEMA

QuantityDefinition, QuantitativeObservation, EffectEstimate, and MeasurementProcessArtifact are first-class. Unit/dimension/scale/transform/missingness/censoring rules fail closed where comparability is required.

### R5-03 — Numerical solver error could masquerade as biological/model certainty

**Status:** CLOSED-POLICY / EXECUTABLE-SCHEMA

NumericalVerificationArtifact separates solver/discretization/stochastic numerical error from measurement, parameter, sampling, and model-form uncertainty.

### R5-04 — Parameter identifiability / model discrepancy under-specified

**Status:** CLOSED-POLICY / P1-IMPLEMENTATION

T2+ credibility now requires parameter adequacy/identifiability where applicable and a ModelDiscrepancyAssessment. Calibration cannot silently compensate for structural error.

### R5-05 — Predictive applicability / distribution shift under-specified

**Status:** CLOSED-POLICY / P1-IMPLEMENTATION

T3+ requires applicability/shift analysis across relevant temporal, source, population, disease/target family, phenotype/measurement, platform, and base-rate axes.

### R5-06 — Probability claims could rely on discrimination alone

**Status:** CLOSED-POLICY / P1-IMPLEMENTATION

Probability claims require held-out calibration plus at least one proper scoring rule and an explicit endpoint/horizon.

### R5-07 — Material model changes could inherit stale validation

**Status:** CLOSED-POLICY / P1-IMPLEMENTATION

Validation attaches to an exact dependency digest. Material changes to model structure, features/preprocessing, parameters, measurement model, numerical configuration, endpoint, update policy, or applicability create a new validation target.

### R5-08 — Development quality and evaluation risk of bias were not explicitly separated

**Status:** CLOSED-POLICY / P1-IMPLEMENTATION

Predictive evaluation now audits data/source, predictors/features, outcome/label, and analysis/evaluation separately.

### R5-09 — Measurement/batch process could be hidden behind one numeric field

**Status:** CLOSED-POLICY / EXECUTABLE-SCHEMA

MeasurementProcessArtifact and normalization/batch provenance are explicit; future-fitted normalization remains temporal leakage.

### R5-10 — Scientific credibility could be treated as a universal model property

**Status:** CLOSED-POLICY

Credibility is explicitly CoU-specific. "Validated model" without the validated target/domain/use is prohibited language.


## Final evidence-extraction closure ledger

### RX-01 — Source quality could be undermined by extraction error

**Status:** CLOSED-POLICY / EXECUTABLE-SCHEMA

ExtractionArtifact now preserves source grounding, extractor/version/config, horizon/watermark, output schema, abstention, review state, and provenance.

### RX-02 — Automated extractor confidence could masquerade as evidence strength

**Status:** CLOSED-POLICY

Extractor confidence is a pipeline-quality signal only. Scientific evidence strength remains method/source/context based.

### RX-03 — LLM/ML/rule extractor changes could inherit old validation

**Status:** CLOSED-POLICY / P1-IMPLEMENTATION

Material model/training-data/prompt/rule/ontology/output-schema changes create a new extractor version and trigger task-specific requalification.

### RX-04 — Human curation quality under-specified

**Status:** CLOSED-POLICY / P1-IMPLEMENTATION

Human workflows retain reviewer identity, disagreement, adjudication, and changes from machine output. Independent-review requirements can be frozen per task.

### RX-05 — Extracted statements could inflate independence

**Status:** CLOSED-POLICY

Extraction never creates a new biological observation. Multiple claims from one originating observation retain shared source/IndependenceFamily lineage.


## Final research-program integrity closure ledger

### RP-01 — Retractions/corrections could rewrite history

**Status:** CLOSED-POLICY / EXECUTABLE-SCHEMA

SourceLifecycleEvent preserves correction/retraction/withdrawal/supersession/restoration events with public timing. Historical reconstruction resolves status as-of-T; later lifecycle events trigger current fragility analysis instead of rewriting history.

### RP-02 — Repeated benchmark reuse could overfit the benchmark

**Status:** CLOSED-POLICY / EXECUTABLE-SCHEMA

BenchmarkExposureLedger tracks disclosure and downstream adaptation. Generations transition through ACTIVE_CONFIRMATORY, DEVELOPMENT_EXPOSED, EXHAUSTED, and RETIRED states. EXHAUSTED generations cannot support new strongest-tier confirmation.

### RP-03 — Internal Git history alone could be overinterpreted as preregistration

**Status:** CLOSED-POLICY / P1-OPERATIONAL

ExternalSealAttestation is required for strongest confirmatory/prospective artifacts. It proves sequencing/existence at study time but does not erase researcher-hindsight risk.

### RP-04 — Prospective predictions could influence their own future validation

**Status:** CLOSED-POLICY / P1-IMPLEMENTATION

PredictionExposureEvent records private/public exposure and contamination risk. Prospective evidence is stratified by exposure; exposed outcomes are not automatically counted as clean independent confirmation.

### RP-05 — Selective reporting across many benchmark attempts

**Status:** CLOSED-POLICY / P1-IMPLEMENTATION

ResearchProgramAttempt ledger records positive, null, negative, inconclusive, and failed attempts across generations/endpoints/horizons/model families.

### RP-06 — Provider/schema/ontology drift could silently mutate frozen artifacts

**Status:** CLOSED-POLICY / P1-IMPLEMENTATION

Material migrations are new immutable derivation artifacts with source/target versions, migration rule, affected semantics, provenance, and digest.


## Independent hostile review — BIG 0F-0 action ledger

An independent adversarial review materially downgraded the prior self-assessment and reopened the B-TGT-E1 critical path.

The previous statement that no major design gap remained is not used after this review.

| ID | Finding | Status after BIG 0F-0 hardening |
|---|---|---|
| HR-01 | Gene assignment can re-import research attention | CLOSED-POLICY / EMPIRICAL-OPEN — high-specificity primary classes; attention audit required |
| HR-02 | Genomic-architecture / pleiotropy baselines missing | CLOSED-POLICY / DATA-OPEN — mandatory nuisance families added |
| HR-03 | Strongest-single comparator is inadequate | CLOSED-POLICY — Combined Nuisance Model is primary comparator |
| HR-04 | No confirmatory alpha / power / MDE / numeric success rule | CLOSED-SCHEMA / EMPIRICAL-OPEN — MAP fields required; pilot supplies power inputs |
| HR-05 | Repeated confirmatory generations mine one finite history | CLOSED-POLICY / SCHEMA — ConfirmatoryProgramBudget + attempt ledger |
| HR-06 | Solo designer/adjudicator/custodian cannot support strongest tier | OPERATIONAL-OPEN — independent adjudicator/custodian required |
| HR-07 | Strict novelty may be power maturation | EMPIRICAL-OPEN — pre-T cohort reuse + power-maturation audit in BIG 0F |
| HR-08 | Positive-only historical audit can be asymmetric | CLOSED-POLICY / EMPIRICAL-OPEN — seeded non-event audit required |
| HR-09 | Disease frame can be chosen with hindsight | CLOSED-POLICY / OPERATIONAL-OPEN — mechanical frame + sealed seed |
| HR-10 | Schemas accepted policy-invalid artifacts | CLOSED-TEST — JSON Schema + semantic validator + hostile regression suite pass in CI |
| HR-11 | Knowledge-bearingness was too self-declared | CLOSED-POLICY — biomedical-domain dependencies default UNKNOWN/knowledge-bearing |
| HR-12 | Same curation pipeline can feed Past and Future | CLOSED-POLICY / EMPIRICAL-OPEN — primary-source/independent outcome path required |
| HR-13 | External seals / null reporting were self-attestable | CLOSED-SCHEMA / OPERATIONAL-OPEN — approved external authority types + disclosure schedule |
| HR-14 | Recall@K is discrete under sparse events | CLOSED-POLICY / EMPIRICAL-OPEN — event-rank percentile preferred for pilot |
| HR-15 | Cross-disease shared controls create dependence | CLOSED-POLICY / IMPLEMENTATION-OPEN — shared-control/study-family blocks required |
| HR-16 | Gene annotation release was not first-class | CLOSED-POLICY / SCHEMA — GeneModelRelease added |
| HR-17 | EffectEstimate could not safely represent GWAS effects | CLOSED-SCHEMA — allele/variant/context + ratio/HR constraints added |
| HR-18 | Scientific Twin / VVUQ gates were too weak and off critical path | DEFERRED — advanced Twin work frozen until core B-TGT evidence exists |
| HR-19 | Extraction qualification could be vacuous | CLOSED-SCHEMA / EMPIRICAL-OPEN — task thresholds and negation/null metrics required |
| HR-20 | Prospective validation starts too late | CLOSED-ROADMAP — private externally timestamped ledger starts with stable BIG 7 ranker |

### Critical interpretation

BIG 0F-0 is complete only when HR-10 regression tests pass and HR-06/HR-09 operational prerequisites required for pilot start are satisfied.

BIG 0F then determines whether HR-01, HR-04, HR-07, HR-08, HR-12, HR-14, HR-19 and related feasibility risks are scientifically tolerable.

No documentation-only closure may convert an EMPIRICAL-OPEN item into PASS.


### Post-BIG 0F-0 sharp consistency findings

| ID | Finding | Status |
|---|---|---|
| HR-21 | Cutoff/horizon feasibility procedure had an unspecified selection order | CLOSED-POLICY — deterministic T/H order; no post-hoc expansion |
| HR-22 | GO/REDESIGN thresholds had ambiguous denominators/statistic semantics | CLOSED-POLICY — field-availability formula, critical fields, agreement statistic, and sensitivity reporting defined |
| HR-23 | Nuisance+biology arm could win through larger learner/tuning capacity | CLOSED-POLICY — primary comparison is nested and capacity/tuning-budget matched |
| HR-24 | "External seal" lacked an operational implementation candidate | PARTIAL-OPERATIONAL — dual OpenTimestamps + OSF Registration runbook identified; dry run and independent custodian remain open |


## Independent hostile review — Round 2 action ledger

Round 2 materially confirmed the conceptual improvements from Round 1, but found that several machine-enforcement and program-governance surfaces could still be bypassed.

The latest independent Round 2 assessment before this closure patch was:

```text
Scientific-plan strength: 5.5/10
Current evidence strength: 0/10
Readiness to start BIG 0F: 4/10
```

The project does not self-rescore after applying these fixes.

| ID | Round 2 finding | Current closure status |
|---|---|---|
| R2-01 | Disease-specific attention volume/momentum not mandatory in the primary nuisance block | CLOSED-SCHEMA/CONFIG/TEST — both are mandatory content-free nuisance families |
| R2-02 | BIG 0F evaluator admitted false GO paths | CLOSED-ENGINE/TEST — strict finite JSON, schema validation, cross-field bounds, deterministic thresholds, bounded INCONCLUSIVE |
| R2-03 | Decision code/result schema/sampling/power code outside seal root | CLOSED-SEAL/TEST — bundle v2 commits all decision-critical code/schemas/manifests |
| R2-04 | Random seed could be ground before commitment | CLOSED-DESIGN/TEST — externally sealed frame then first verified post-seal public randomness beacon; exact frame-seal artifact committed |
| R2-05 | Pilot augmented biological arm could tune later contrast | CLOSED-POLICY/CONFIG — pilot mode is NUISANCE_ONLY; V0 subtype/metric are frozen |
| R2-06 | Alpha budget could reset by renaming benchmark family | CLOSED-SCHEMA/VALIDATOR/TEST — canonical research_program_id/budget plus cross-artifact generation allocation validation |
| R2-07 | Primary-positive ascertainment could include targeted candidate-gene studies | CLOSED-POLICY/CONFIG/EXECUTOR — V0 primary study designs are genome/exome/biobank-wide only |
| R2-08 | Comparator capacity parity lived mainly in prose | CLOSED-MAP/SEMANTIC — learner/search/tuning/preprocessing/early-stop/seed parity are first-class MAP fields |
| R2-09 | Endpoint-quality FROZEN rule could be non-executable | CLOSED-EXECUTOR/TEST — frozen field registry/operators/mandatory dimensions and event evaluation |
| R2-10 | Ambiguity used component max rather than unique-case union | CLOSED-RESULT/ENGINE/TEST — any_primary_endpoint_ambiguity_fraction is required and consistency-checked |
| R2-11 | Threshold sensitivity was self-reported | CLOSED-ENGINE — sealed sensitivity variants are re-evaluated; unstable conclusion becomes REDESIGN |
| R2-12 | INCONCLUSIVE could be carried indefinitely | CLOSED-ENGINE — bounded attempts; repeated INCONCLUSIVE becomes REDESIGN |
| R2-13 | Power could be self-reported | CLOSED-ARTIFACT/ENGINE — power artifact is schema-bound, code-sealed and deterministically recomputed |
| R2-14 | Exposure ledger allowed adaptive disclosure routes | CLOSED-SCHEMA/SEMANTIC/TEST — active confirmatory generation forbids label/per-case/full disclosures and enforces aggregate/subgroup budgets |
| R2-15 | External seal could be internally asserted | CLOSED-SCHEMA/SEMANTIC for BIG 0F — frame/bundle require external timestamp/public-registry authority; real service dry run remains OPERATIONAL-OPEN |
| R2-16 | Empirical adjudicator/custodian independence not yet instantiated | OPERATIONAL-OPEN — real independent second adjudicator and custodian remain start gates |
| R2-17 | BIG 0F evidence/provider feasibility is untested | EMPIRICAL-OPEN — this is the purpose of BIG 0F, not a documentation closure |
| R2-18 | Twin/quantitative side surfaces have residual P2 issues | DEFERRED/NON-BLOCKING — no T2+ twin claim is on the BIG 0F critical path |

### Round 2 closure boundary

BIG 0F may not begin scientific adjudication merely because R2-01..R2-15 are implemented.

The remaining start gates are operational:
- assign an independent second adjudicator;
- assign an independent custodian;
- complete an external frame/bundle seal dry run with real third-party/public-registry evidence;
- seal the real protocol/frame/policies before the first case is seen.

Empirical BIG 0F findings remain open by design.
