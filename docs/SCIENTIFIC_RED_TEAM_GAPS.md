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
