# Pre-Code Readiness Checklist

**Status:** ACTIVE — RED-TEAM HARDENED; aligned with ADR-022  
**Rule:** no production scientific implementation begins until every P0 item is closed or explicitly superseded by an accepted ADR.  
**Phase order ([ADR-022](adr/ADR-022-final-scientific-consistency-closure.md) §6, D14):** 0. SPEC FREEZE → 1. minimal pre-BIG 0F verification harness → 2. BIG 0F → 3. core B-TGT-E1. The manual pilot **is** BIG 0F; there is no separate manual pilot. P0 items fall in phases 0–2. P1 items fall in phase 3 and must close before the sealed confirmatory run.  
**Legend (ADR-022 D15; INV-D2):** `[x]` = SPEC-CLOSED, meaning the normative text is final at `SEAL_CANDIDATE` status. `[ ]` = open or IMPLEMENTATION-PENDING. Nothing is `SEALED` yet ([V0_FREEZE_STATEMENT.md](V0_FREEZE_STATEMENT.md) §5), and no checked item means a check is machine-enforced: the code and tests were removed and the harness does not exist yet.  
**Precedence:** [V0_FREEZE_STATEMENT.md](V0_FREEZE_STATEMENT.md) wins where this checklist disagrees with it.

## Phase 0 — SPEC FREEZE (P0: must close before core scientific coding)

Condition and exit (ADR-022 §6): ADR-022 merged, and the targeted consistency attack finds no new false-GO P0 → PLAN FROZEN (last item of this phase).

### Scientific scope and temporal boundary

- [x] Product scientific scope defined.
- [x] Past/Future scientific planes separated.
- [x] UNKNOWN is first-class and fail-closed.
- [x] Target defined as a hypothesis role, not a universal entity.
- [x] Evidence method separated from source channel.
- [x] CandidateUniverse separated from HistoricalKnowledgeView.
- [x] KnowledgeWatermark separated from implementation provenance.
- [x] AvailabilityAttestation defined.
- [x] Field-level provider qualification defined.
- [x] Canonical hashing/serialization policy defined.
- [x] Nested temporal supervised-training policy defined.
- [x] Reconstruction Fidelity Study is a formal gate.

### BIG 0 promised artifacts

- [x] Project glossary exists and ambiguous biomedical/statistical terms are defined.
- [x] Machine-readable or normative QoI schema exists.
- [x] Context-of-Use schema exists.
- [x] MAP schema exists.
- [x] MAR schema exists.
- [x] Machine-verifiable JSON Schemas exist for QoI/MAP/MAR.
- [x] Core scientific enums/value objects are specified.
- [x] Minimal golden synthetic biomedical world is specified.
- [x] Architecture import/dependency rules are specified.
- [x] Deliberate prohibited-dependency fixtures/examples are specified.

### Benchmark estimand and endpoint

- [x] B-TGT-E1 estimand structure is frozen, including population, equal disease weighting, zero-future-event disease policy, comparator family, and selection procedures.
- [x] B-TGT-E1 disease/genetic regime is explicitly restricted or stratified.
- [x] E1-NOVEL-STRICT / E1-MATURATION / E1-REPLICATION / E1-CROSSMODAL semantics are accepted.
- [x] PreTGeneticState separates no-observed-signal from suggestive/qualifying/ambiguous pre-T genetics.
- [x] V0 primary E1 subtype is fixed now as E1-NOVEL-STRICT; no subtype is selected after BIG 0F (Freeze Statement §1; ADR-022 D2). Supersedes "one primary E1 subtype selection procedure is accepted before sealed evaluation".
- [x] Endpoint evidence-quality rule structure/dimensions are specified in a JSON Schema, with the applicability matrix fixed (ADR-022 D17; INV-Q1–Q3).
- [x] Assignment, phenotype, novelty and coverage definitions are fixed before BIG 0F in adjudication policy v2 (`BIG0F-ADJUDICATION-V2`). The endpoint-quality threshold values are set later (phase 3) and may only be equal or stricter (ADR-022 D7; INV-T8).
- [x] Initial H candidate set and feasibility procedure are accepted.
- [x] Fixed-K evaluation has a candidate-universe-normalized companion metric.
- [x] Multiplicity policy for secondary endpoints/cutoffs/subgroups is defined.

### Outcome integrity

- [x] GenomicVariant / GenomicLocus / GenomeAssembly / ReferenceSequence are first-class identities.
- [x] Phenotype / Cohort / Dataset / Biobank / Consortium / SampleSet are first-class identities.
- [x] Variant normalization/liftover/allele harmonization is provenance-bearing.
- [x] LD relation requires ancestry/reference-panel/version provenance.
- [x] ScientificEventFamily / GeneticDiscoveryEventFamily primary-credit policy accepted.
- [x] HistoricalGeneticSearchCoverage gates E1-NOVEL-STRICT.
- [x] KNOWN_TO_RANKER_AT_T is distinct from KNOWN_PUBLICLY_AT_T.
- [x] Historical genetic observability sensitivity policy accepted.
- [x] OutcomeGeneAssignmentPolicy accepted.
- [x] OutcomePhenotypeMatchPolicy accepted.
- [x] GeneticReplicationPolicy accepted.
- [x] HistoricalNoveltyAudit policy accepted.
- [x] Locus/variant-level events cannot silently become gene-level positives.
- [x] Current/modern learned L2G output is prohibited as unqualified primary strict-historical ground truth.
- [x] Future-event independence includes cohort/dataset/sample-overlap semantics.
- [x] UNKNOWN sample overlap is not treated as independent replication.
- [x] Outcome adjudication blinding/dual-review policy is accepted.
- [x] Strongest L3 sealed adjudication requires rank/order blinding or automatic tier downgrade.
- [x] Population/ancestry applicability fields are defined for relevant outcome classes.
- [x] Validation-generation reuse/retirement policy is accepted.
- [x] Exact Future Outcome snapshot/ledger commitment policy is accepted.
- [x] Outcome event discovery/adjudication freeze-before-rank policy is accepted.
- [x] Input/Outcome provider-coupling policy is accepted.
- [x] Cross-anchor event reuse policy is accepted.
- [x] Validation disclosure-level policy is accepted.

### Ascertainment and hindsight

- [x] Discoverability / observation-propensity confounding is part of the formal threat model.
- [x] Required historical discoverability baseline family is defined.
- [x] Attention-momentum control is defined.
- [x] Researcher hindsight / design-time leakage policy is accepted.
- [x] BenchmarkDesignProvenance schema is defined.
- [x] Ranking-team / outcome-adjudication / lockbox-custodian roles are defined.
- [x] Sealed disease identity blinding policy is decided.
- [x] Knowledge-historical vs technology-contemporaneous claims are explicitly separated.
- [x] ScientificOperatingMode is separated from HistoricalDataPolicy.

### BIG 0F-0 critical-path hardening

- [x] Primary gene-level endpoint restricts primary positives to high-specificity assignment classes.
- [x] AUTHOR_NAMED / NEAREST_GENE / positional-only / generic-database mappings are non-primary unless independently high-specificity.
- [x] Assignment-attention audit is mandatory.
- [x] Combined Nuisance Model is the primary comparator.
- [x] Genomic-architecture, cross-trait pleiotropy, observability, and attention nuisance families are mandatory. A family that cannot be historically reconstructed forces REDESIGN; it is never silently dropped (manifest v2; [BIG_0F_NUISANCE_EXECUTION_CONTRACT.md](BIG_0F_NUISANCE_EXECUTION_CONTRACT.md) §1). Supersedes "where reconstructable".
- [x] GeneModelRelease is first-class for historical gene geometry/length/windows.
- [x] Confirmatory MAP requires numeric alpha / effect / power / success fields.
- [x] ConfirmatoryProgramBudget schema exists for research-program multiplicity.
- [x] BIG 0F sampling rule and target-size rule are frozen in BIG_0F_PROTOCOL.md (sampling key, disease order, expansion and cap: [BIG_0F_SELECTION_CUSTODY.md](BIG_0F_SELECTION_CUSTODY.md) §7–§8).
- [x] BIG 0F numeric GO / REDESIGN / NO-GO thresholds are specified in threshold manifest v2 (`SEAL_CANDIDATE`), to be sealed at S1 before adjudication (ADR-022 D9).
- [x] BIG 0F pilot cases are permanently DEVELOPMENT_EXPOSED (exposure scope and untouched pool: BIG_0F_SELECTION_CUSTODY.md §4–§5).
- [x] BIG 0F requires symmetric non-event historical audit.
- [x] BIG 0F requires mini historical-provider availability audit.
- [x] BIG 0F requires development-only Combined Nuisance headroom analysis.
- [x] Biomedical-domain dependencies default to knowledge-bearing/UNKNOWN unless explicitly qualified.
- [x] Primary outcomes cannot rely solely on the same curation pipeline used as historical input.
- [x] Cross-disease shared-control/study lineage is included in dependence sensitivity.
- [x] Cross-field scientific semantic rules are specified.
- [x] Hostile-review attack cases are documented as future regression-test requirements.
- [x] Round 2 false-GO attacks are preserved as permanent implementation/test requirements.
- [x] Disease-specific content-free attention volume and momentum are mandatory in the primary nuisance comparator (14 families incl. global attention volume and momentum, manifest v2; ADR-022 D11).
- [x] BIG 0F model-evaluation mode is NUISANCE_ONLY; biological-model lift is not inspected in the pilot.
- [x] V0 primary subtype and metric are fixed now, for BIG 0F and confirmation alike, as E1-NOVEL-STRICT / EVENT_RANK_PERCENTILE_V1 (Freeze Statement §1; ADR-022 D2, D3).
- [x] Primary positive ascertainment is restricted to hypothesis-free genome/exome/biobank-wide designs.
- [x] OTHER_HIGH_SPECIFICITY_METHOD is closed for V0 primary credit.
- [x] BIG 0F decision contract requires rejection of non-finite values, incomplete cross-field state, and unstable threshold decisions.
- [x] BIG 0F threshold-sensitivity recomputation from a frozen manifest is specified; self-reporting is prohibited.
- [x] INCONCLUSIVE is bounded and cannot be carried indefinitely.
- [x] Power-analysis artifact and deterministic revalidation requirements are specified.
- [x] Disease sampling uses the mechanical frame rule and the pinned drand quicknet round R pre-declared in the public S4 selection registration (ADR-022 D6, D13; BIG_0F_SELECTION_CUSTODY.md §7). Supersedes "first verified post-seal public randomness-beacon round".
- [x] The S1 protocol-registration and S4 selection-registration attestation pairs are committed into the BIG 0F root seal bundle (`big0f-seal-bundle-v3`). This supersedes the frame-seal attestation of bundle v2 (ADR-022 D13).
- [x] Future decision, sampling, and power implementations plus governing schemas/manifests must be committed by the seal bundle before use.
- [x] Endpoint-quality field/operator and event-evaluation semantics are specified for a sealable rule (status `SEAL_CANDIDATE`/`SEALED`; formerly "FROZEN").
- [x] Confirmatory attempts must be checked against one canonical program-wide alpha budget; renaming cannot reset the budget.
- [x] Independent sealing mechanism identified: OpenTimestamps + OSF Registration dual-seal candidate; seal_time = max(OTS Bitcoin block time, public registry time) (ADR-022 §5, D13).
- [x] T/H selection and the 16-pair audit are specified as duties of an independent selection custodian; the study team sees aggregates only (ADR-022 D12).

### Round 2 false-GO closure plan

- [x] Event-bearing disease diversity is a formal GO gate with sensitivity handling.
- [x] First-passing cutoff/horizon selection requires a reconstructable feasibility ledger.
- [x] Disease expansion from 12 to 15 is prefix-only and event-count-triggered (counted in event families; BIG_0F_SELECTION_CUSTODY.md §8).
- [x] >150-event capping requires a committed raw universe and deterministic disease-preserving sampling (over event families; BIG_0F_SELECTION_CUSTODY.md §8; INV-C10).
- [x] A freely supplied disease-level SD is prohibited; power planning requires a frozen derivation/scenario contract without biological-arm leakage.
- [x] Actual nuisance execution must bind to the complete frozen nuisance manifest and reproducible rank outputs.
- [x] External timestamp/registry/beacon trust cannot be established by a self-declared VERIFIED field.
- [x] Provider, applicability, curation, and adjudicator summary states must be regenerable from evidence artifacts.
- [x] Confirmatory program history must be append-only/hash-chained and externally anchorable.
- [x] One canonical endpoint decision semantics source is required.
- [x] Threshold provenance/digest hygiene and locus-level robustness requirements are specified.
- [x] Power and Variance Policy v2 specified: Stage A model-free pool-sufficiency screen at BIG 0F, Stage B DLVS before the confirmatory seal; proxy-only variance cannot support GO ([BIG_0F_POWER_AND_VARIANCE_POLICY.md](BIG_0F_POWER_AND_VARIANCE_POLICY.md); ADR-022 D10). Supersedes the removed Power Input Derivation Contract.
- [x] Nuisance Execution Artifact contract frozen with candidate-universe/full-rank/training identity binding (frozen learner, out-of-fold ranks, adequacy check; ADR-022 D11).
- [x] Provider/applicability/curation/adjudicator evidence-artifact schemas (v2) specified and evidence-bound.
- [ ] ADR-022 merged, and the targeted consistency attack on D1–D19 finds no new false-GO P0 → **PLAN FROZEN** (ADR-022 §6, §9). The attack is done: round 5 found no new false-GO P0 (ADR-022 §8a). The item checks on merge. This replaces the item "Final hostile review of the frozen closure contracts completed; no new P0 false-GO design gap identified". That item was checked, and is now unchecked: the independent hostile review of `a1326e3` found false-GO P0 gaps (ADR-022 §1, §7).

Normative detail: [BIG_0F_FALSE_GO_CLOSURE_PLAN.md](BIG_0F_FALSE_GO_CLOSURE_PLAN.md).

### Governance

- [x] BIG 0F pilot result has a machine-readable schema.
- [x] BIG 0F GO/REDESIGN/NO_GO decision rules are specified deterministically (threshold manifest v2, ADR-022 D9); executable implementation is deferred.
- [x] ADR-005 licensing posture decided: commercial-later; repository Apache-2.0; provider-data licenses remain separate.
- [x] Initial lockbox custodian/storage mechanism chosen.
- [x] Authoritative scientific-spec change governance chosen (protected branch or equivalent reviewed process).

## Phase 1 — Minimal pre-BIG 0F verification harness (P0)

Entry: PLAN FROZEN. Exit: all items below (ADR-022 §6). Each item is IMPLEMENTATION-PENDING until the harness implements it.

- [ ] Schema/config validation.
- [ ] Implement and run the hostile-review regression suite: one check per INV-* ID with at least one passing and one failing fixture ([SEMANTIC_INVARIANTS.md](SEMANTIC_INVARIANTS.md)), including the ADR-022 §4 simulations as fixtures (INV-D4).
- [ ] Implement and run the local canonical hashing and seal-bundle build/verify/tamper dry run before BIG 0F.
- [ ] OTS/OSF/drand verifiers implemented; complete independent external-authority/beacon verification before adjudication.
- [ ] Metric reference implementation of EVENT_RANK_PERCENTILE_V1 ([METRIC_EVENT_RANK_PERCENTILE_V1.md](METRIC_EVENT_RANK_PERCENTILE_V1.md)).
- [ ] Stage A power engine ([BIG_0F_POWER_AND_VARIANCE_POLICY.md](BIG_0F_POWER_AND_VARIANCE_POLICY.md) §2).
- [ ] External OpenTimestamps/OSF seal mechanism dry-run tested end-to-end with synthetic artifacts (external-seal dry run passed).

## Phase 2 — BIG 0F (P0)

### Start gates

BIG 0F adjudication cannot start until all of these exist (ADR-022 §6, §9):

- [ ] The minimal pre-BIG 0F verification harness (Phase 1 complete).
- [ ] A successful external-seal dry run.
- [ ] Independent second adjudicator assigned for BIG 0F duplicate review.
- [ ] Independent selection custodian assigned (ADR-022 D12).

Before the first case is released to adjudicators:

- [ ] S1 protocol registration, S4 selection registration (with the pre-declared drand round) and S6 seal bundle are externally sealed, and seal_time(S6) is independently verified ([BIG_0F_SELECTION_CUSTODY.md](BIG_0F_SELECTION_CUSTODY.md) §2; ADR-022 §5). Supersedes "BIG 0F protocol/frame/random seed receives external seal before first adjudication".

### BIG 0F execution and decision

- [ ] BIG 0F completed on the custodian-selected diseases and event families (BIG_0F_SELECTION_CUSTODY.md §2, §8). Supersedes "Manual outcome feasibility pilot completed on heterogeneous events"; the manual pilot is BIG 0F (ADR-022 D14).
- [ ] Pilot reports novelty ambiguity rate.
- [ ] Pilot reports historical genetic-search coverage grade distribution.
- [ ] Pilot reports variant/liftover/allele-harmonization ambiguity.
- [ ] Pilot reports phenotype-match ambiguity.
- [ ] Pilot reports event-family deduplication / locus-to-many-gene credit impact.
- [ ] Pilot reports Past/Future provider-coupling risk.
- [ ] Pilot reports locus-to-gene assignment dependence.
- [ ] Pilot reports cohort/sample-overlap ambiguity.
- [ ] Pilot reports retrospective-curation burden.
- [ ] Pilot reports population/ancestry metadata coverage.
- [ ] BIG 0F yields GO / REDESIGN / NO_GO / INCONCLUSIVE for B-TGT-E1-v0 under threshold manifest v2, including the Stage A power screen (ADR-022 §6, D9, D10). GO is the entry condition for phase 3.

## Phase 3 — Core B-TGT-E1 (P1: must close before sealed confirmatory run)

Entry: BIG 0F GO. Sequence: DLVS (Stage B) → confirmatory seal → confirmatory generation (ADR-022 §6).

### Providers and historical reconstruction

- [ ] ProviderCards complete for every Past source.
- [ ] Future outcome sources qualified independently.
- [ ] Reconstruction fidelity verdicts available for conditional providers.
- [ ] Representation-time provenance is captured for modern structured derivations.
- [ ] Coverage/UNKNOWN thresholds frozen in MAP.

### Sampling and universes

- [ ] Disease sampling frame frozen from as-of-T criteria.
- [ ] Candidate universe policy frozen.
- [ ] Development/validation/sealed split frozen (untouched pool: BIG_0F_SELECTION_CUSTODY.md §5; confirmatory sample drawn by the beacon/hash-sort mechanism: Freeze Statement §2).
- [ ] Sealed-case selection cannot be changed in response to outcomes.
- [ ] Identity gold-set error rate reported, including variants/loci/phenotypes/cohorts/datasets.
- [ ] Variant normalization/liftover/allele-orientation gold-set error rate reported.
- [ ] Historical observability sensitivity universe frozen from as-of-T criteria.

### Statistics and controls

- [ ] Confirmatory estimand instance sealed with the BIG 0F-selected (T\*, H\*), which the custodian's first-passing-pair rule produces (Freeze Statement §2). Primary subtype and primary metric are already fixed (Freeze Statement §1). Supersedes "(H, primary E1 subtype, primary metric) frozen after BIG 0F".
- [ ] Endpoint evidence-quality threshold values set after BIG 0F and sealed before the custodian's release of any DLVS label (release log). They are equal to or stricter than adjudication policy v2 (Freeze Statement §2; INV-T8). Moved from P0.
- [ ] Sample-size/event-yield feasibility completed on development-visible sources.
- [ ] Stage B Development Lift & Variance Study (≥ 20 event-bearing development diseases) completed, and the Stage B power gate passes ([BIG_0F_POWER_AND_VARIANCE_POLICY.md](BIG_0F_POWER_AND_VARIANCE_POLICY.md) §3; ADR-022 D10). This is the simulation-based power analysis.
- [x] Confirmatory alpha (0.05 one-sided), minimum scientifically meaningful effect (0.05, planning only) and target power (0.80) are fixed (Freeze Statement §1; ADR-022 D18).
- [ ] Zero-event disease handling verified in metric engine.
- [ ] All-frame observed-event review-budget utility implemented.
- [ ] K/review-budget secondary metric chosen on development data only. The primary metric is already fixed as EVENT_RANK_PERCENTILE_V1 (Freeze Statement §1); Recall@K is a secondary companion only (INV-E9).
- [ ] Candidate-universe-normalized primary/secondary metric implemented.
- [ ] Combined Nuisance comparator implementation and exact as-of-T feature sources frozen.
- [x] Paired disease/challenge-level CI method specified: disease-level BCa bootstrap 95% CI plus the disease-family block bootstrap CI, at the single confirmatory cutoff (Freeze Statement §3; INV-E8).
- [ ] Disease-family + consortium/study-family + shared-control dependence sensitivity method frozen.
- [ ] Within-study multiplicity policy frozen.
- [x] ConfirmatoryProgramBudget allocation: the V0 confirmatory generation holds the full α = 0.05 (FIXED_SPLIT). Tests use the allocated α (Freeze Statement §1, §3; INV-L11).
> Every sensitivity, control or diagnostic item below is either in the closed list of Freeze Statement §3a (BLOCKING, LABEL or REPORT) or is a REPORT-only diagnostic. No item outside §3a can grant or veto confirmatory success (INV-E11).

- [ ] Negative-control suite frozen.
- [ ] Temporal placebo control defined where feasible.
- [ ] Outcome-source and gene-assignment sensitivity analyses frozen.
- [ ] Ambiguous-event tipping-point / best-worst-case sensitivity frozen.
- [ ] Precision-weighted or hierarchical disease sensitivity frozen alongside equal-disease primary weighting.
- [x] Label/feature method-family coupling sensitivity: SENS-COUPLING (LABEL; Freeze Statement §3a).
- [x] Attention-volume survival is satisfied by design. Disease-specific and global attention volume and momentum are mandatory nuisance families in the primary contrast, and SENS-ATTENTION is a LABEL analysis. There is no separate veto (Freeze Statement §3a; INV-E11).
- [x] Input/outcome provider-coupling sensitivity: SENS-PROVIDER (LABEL; Freeze Statement §3a).
- [ ] LD reference-panel / modern-evaluation-LD sensitivity frozen where applicable.
- [ ] ScientificEventFamily credit sensitivity frozen.

### Outcome integrity and applicability

- [ ] HistoricalNoveltyAudit + PreTGeneticState process tested.
- [ ] Outcome gene-assignment adjudication process tested.
- [ ] Outcome phenotype-match adjudication process tested.
- [ ] Genetic replication assessment process tested.
- [ ] Cohort/sample-overlap lineage coverage measured.
- [ ] Strongest L3 sealed outcome adjudicators verified blind to ranking/order.
- [ ] Ancestry/population coverage reported.
- [ ] Reporting/publication-bias sensitivity plan included in MAP.

### Lockbox and reproducibility

- [ ] MAP hash frozen.
- [ ] Validation generation ID/status/access count/max-disclosure-level frozen.
- [ ] Exact Future Outcome source releases/snapshot/ledger/event-family/adjudication/identity-bridge/provider-coupling commitment frozen.
- [ ] Sealed outcome-event discovery completed before ranking reveal.
- [ ] Lockbox credentials unavailable to ranking runtime/team path.
- [ ] Ranking artifact commitment mechanism tested.
- [ ] Append-only lockbox access log tested.
- [ ] BenchmarkDesignProvenance record frozen.
- [ ] Temporal metamorphic test suite passes.
- [ ] Benchmark null/falsification tests pass.
- [ ] Reproduction from manifest succeeds.
- [ ] Protected-authoritative-branch / reviewed-merge controls are operationally verified.
- [ ] Lockbox storage isolation and credential separation are operationally verified.

## Platform extension — Scientific Digital Twin readiness

These items are **non-blocking for the B-TGT-E1 BIG 0F pilot** unless that pilot explicitly uses twin outputs.

### BIG 0R4 contracts

- [x] DiseaseScientificProfile contract exists.
- [x] Pathogen/Virus/PathogenHost scientific profile contracts exist.
- [x] TherapeuticScientificProfile contract exists.
- [x] Disease and pathogen are represented as distinct scientific identities.
- [x] Twin maturity hierarchy T0–T4 is accepted.
- [x] Static profile/graph is prohibited from claiming predictive twin maturity.
- [x] Patient-specific digital twins are excluded from V1 Context of Use.
- [x] Scientific Twin JSON Schema exists.
- [x] Disease/Pathogen/Virus/PathogenHost/Therapeutic machine-readable profile schemas exist.
- [x] Twin schema enforces inherited T1/T2/T3/T4 maturity prerequisites.
- [x] Historical twin/profile schemas require explicit cutoff T.
- [x] Twin state-model structure/update policy are knowledge-bearing provenance/watermark dependencies.
- [x] Profile/twin dependency wall is defined.
- [x] Scientific Contract includes twin maturity, temporal, validation, causal, and clinical claim boundaries.
- [x] T3 reuses MAP/MAR/ValidationGeneration/BenchmarkDesignProvenance governance.
- [x] T4 requires causal assumptions/intervention semantics/identifiability/sensitivity artifacts.
- [ ] Implement positive/negative schema contract tests when coding begins.

### Before any T2 mechanistic-twin claim

- [ ] State variables and transitions are explicitly defined.
- [ ] Parameter units/meaning/provenance are complete.
- [ ] Model assumptions and applicability domain are documented.
- [ ] Mechanistic verification tests pass.
- [ ] Historical twin state-model structure, update policy, parameters, preprocessing, and representations obey cutoff/watermark rules when used as-of-T.

### Before any T3 predictive-twin claim

- [ ] Prediction target/horizon frozen.
- [ ] MAP is frozen for the twin prediction target/horizon.
- [ ] Held-out or future validation completed.
- [ ] MAR records the actual twin validation execution.
- [ ] ValidationGeneration and BenchmarkDesignProvenance are recorded.
- [ ] Predictive metrics and calibration reported where applicable.
- [ ] Uncertainty quantification evaluated.
- [ ] Applicability/OOD behavior evaluated.
- [ ] Failure analysis reported.
- [ ] No validation data entered model construction through parameters, feature selection, or tuning.

### Before any T4 intervention-simulation claim

- [ ] T3 predictive validity is established for the relevant state/target.
- [ ] CausalAssumptionSet is explicit and versioned.
- [ ] InterventionSemantics are explicit and versioned.
- [ ] IdentifiabilityStatus is IDENTIFIED, PARTIALLY_IDENTIFIED, or ASSUMPTION_DEPENDENT.
- [ ] Perturbation semantics are explicit and versioned.
- [ ] Sensitivity analysis completed.
- [ ] Model-form/parameter uncertainty propagated.
- [ ] Simulation output is labelled a research hypothesis, not clinical evidence.
- [ ] No patient-specific treatment or dosing recommendation is produced.

## Platform extension — BIG 0R5 model credibility & quantitative integrity

These are non-blocking for BIG 0F (the endpoint-feasibility pilot), but mandatory before T2+ Scientific Twin claims, probabilistic endpoint claims, or model-supported intervention simulation.

### Policy/schema readiness

- [x] Context-of-Use-specific model credibility policy exists.
- [x] Quantitative semantics policy exists.
- [x] QuantityDefinition schema exists.
- [x] QuantitativeObservation schema exists.
- [x] EffectEstimate schema exists.
- [x] MeasurementProcessArtifact schema exists.
- [x] NumericalVerificationArtifact schema exists.
- [x] CredibilityAssessmentArtifact schema exists.
- [x] Numeric missing/censoring/unit/transform fail-closed rules are defined.
- [x] Model discrepancy is separated from parameter/numerical/measurement uncertainty.
- [x] T3 applicability/shift and prediction-risk audit requirements are defined.
- [x] Validation invalidation after material dependency change is defined.
- [ ] Implement positive/negative quantitative schema tests when coding begins.

### Before any numerical T2+ claim

- [ ] Solver/engine/version recorded.
- [ ] Method/tolerances/discretization or timestep recorded.
- [ ] Convergence/refinement study completed where applicable.
- [ ] Stochastic replicate / Monte Carlo error assessed where applicable.
- [ ] Residual/invariant checks completed.
- [ ] Numerical error estimate reported.
- [ ] Reproducibility tolerance frozen.

### Before any T3 probability claim

- [ ] Endpoint/horizon frozen.
- [ ] Held-out calibration evaluated.
- [ ] Proper scoring rule frozen and reported.
- [ ] Temporal/source/population/measurement shift assessed as applicable.
- [ ] Prediction risk-of-bias audit completed.
- [ ] Applicability domain frozen.
- [ ] Out-of-domain outputs explicitly labelled extrapolation.

### Before any model credibility conclusion

- [ ] Research decision and model influence classified.
- [ ] Consequence-if-wrong classified.
- [ ] Verification adequacy assessed.
- [ ] Numerical verification adequacy assessed.
- [ ] Validation adequacy assessed.
- [ ] Uncertainty adequacy assessed.
- [ ] Applicability adequacy assessed.
- [ ] Model discrepancy/residual risk documented.
- [ ] Credibility conclusion is CoU-specific.

## Platform extension — Evidence extraction & curation assurance

- [x] ExtractionArtifact contract exists.
- [x] ExtractionQualityCard contract exists.
- [x] Source grounding/span is required for non-native confirmatory extraction.
- [x] Automated/rule extraction requires task/domain qualification.
- [x] Extractor confidence is explicitly not scientific evidence strength.
- [x] Extraction does not create a new IndependenceFamily.
- [x] Human-review disagreement/adjudication remains explicit.
- [x] Material extractor/model/prompt/rule/ontology/schema change triggers requalification.
- [x] Extraction schemas exist; executable extraction tests are deferred to implementation.

Before provider-scale automated extraction:
- [ ] Gold set frozen for each extraction task/domain.
- [ ] Precision/recall and high-impact false-positive/false-negative rates reported.
- [ ] Negation/null-result error measured.
- [ ] Source-grounding error measured.
- [ ] Manual-review burden measured.
- [ ] QUALIFIED/CONDITIONAL verdict frozen.

## Platform extension — Research-program lifecycle integrity

- [x] SourceLifecycleEvent contract exists.
- [x] Historical source lifecycle is resolved as-of-T.
- [x] Later corrections/retractions trigger fragility sensitivity rather than retroactive historical rewriting.
- [x] BenchmarkExposureLedger contract exists.
- [x] Benchmark generation states ACTIVE_CONFIRMATORY / DEVELOPMENT_EXPOSED / EXHAUSTED / RETIRED are defined.
- [x] ResearchProgramAttempt ledger is required.
- [x] ExternalSealAttestation contract exists.
- [x] Prospective PredictionExposureEvent contract exists.
- [x] Self-fulfilling research-attention risk is explicitly separated from independent prospective validation.
- [x] Schema/provider/ontology drift is versioned rather than in-place rewritten.
- [x] Lifecycle/exposure schemas exist; executable lifecycle tests are deferred to implementation.

Before strongest L3/L6:
- [ ] Benchmark generation is ACTIVE_CONFIRMATORY.
- [ ] Exposure ledger is complete.
- [ ] ResearchProgramAttempt ledger is complete.
- [ ] Required external seals verify successfully.
- [ ] Prospective prediction exposure status is classified.
- [ ] Source lifecycle state is resolved for outcome-defining evidence.
- [ ] Independent final frozen-state review completed.

## Sample-size / feasibility rule

Before freezing the sealed benchmark, use only development-visible information to estimate:
- number of diseases;
- candidate counts;
- qualifying event prevalence by endpoint subtype;
- zero-event disease frequency;
- censoring;
- ambiguity;
- expected CI width;
- sensitivity to K/review budget;
- discoverability imbalance.

This is a feasibility analysis, not permission to inspect sealed outcomes.

If expected uncertainty is too wide, ambiguity is too high, or the endpoint is dominated by discoverability/curation effects, redesign the benchmark before lockbox use.

## BIG 0F outcome feasibility pilot (formerly "manual outcome feasibility pilot")

The manual pilot is BIG 0F (ADR-022 D14); there is no separate manual pilot. Before provider-scale implementation, manually adjudicate the event families that the selection custodian samples and caps ([BIG_0F_SELECTION_CUSTODY.md](BIG_0F_SELECTION_CUSTODY.md) §2, §8). This replaces "a small heterogeneous set of future events": sampling is mechanical. Record:
- pre-T genetic state: no-observed-signal vs suggestive vs qualifying vs ambiguous;
- whether evidence was truly novel at T;
- locus-level versus gene-level status;
- gene-assignment method and knowledge horizon;
- benchmark-disease vs future-phenotype relation;
- replication allele/direction/LD/population comparability where applicable;
- cohort/sample overlap;
- historical genetic-search coverage;
- variant build/normalization/liftover/allele ambiguity;
- event-family deduplication and locus-to-many-gene credit;
- Past/Future provider lineage/coupling;
- retrospective curation;
- ancestry/population metadata;
- adjudicator disagreement;
- unresolved ambiguity.

The pilot evaluates whether the benchmark can be constructed credibly. It does not evaluate model performance.

## Lockbox custody rule

A Git hash alone is not custody.

SEALED_LOCKBOX requires:
- separate storage/schema or encrypted artifact;
- separate credentials from ranking runtime;
- append-only access event log;
- named custodian/process;
- MAP hash + ranking hash before opening;
- benchmark generation retirement after outcome-driven methodology changes.

For strongest retrospective claims, methodology should be frozen before sealed disease identities are revealed to the ranking team where practical.

## Go/no-go rule

**PLAN FROZEN → BEGIN MINIMAL PRE-BIG0F VERIFICATION IMPLEMENTATION** only when phase 0 is complete (ADR-022 §9).

**BIG 0F adjudication** only when phase 1 is complete and every phase 2 start gate is met (ADR-022 §6, §9).

**GO FOR CORE SCIENTIFIC CODE** only when all P0 items are closed, including a BIG 0F GO (ADR-022 §6).

**GO FOR SEALED CONFIRMATORY RUN** only when all P1 items are closed.

A failed gate changes the plan; it is never bypassed to keep schedule.

The active red-team register is [SCIENTIFIC_RED_TEAM_GAPS.md](SCIENTIFIC_RED_TEAM_GAPS.md).


## Normative P0 artifact index

- [V0_FREEZE_STATEMENT.md](V0_FREEZE_STATEMENT.md) — takes precedence over every document below
- [adr/ADR-022-final-scientific-consistency-closure.md](adr/ADR-022-final-scientific-consistency-closure.md)
- [SEMANTIC_INVARIANTS.md](SEMANTIC_INVARIANTS.md)
- [BIG_0F_POWER_AND_VARIANCE_POLICY.md](BIG_0F_POWER_AND_VARIANCE_POLICY.md)
- [BIG_0F_SELECTION_CUSTODY.md](BIG_0F_SELECTION_CUSTODY.md)
- [GLOSSARY.md](GLOSSARY.md)
- [schemas/QOI_SCHEMA.md](schemas/QOI_SCHEMA.md)
- [schemas/CONTEXT_OF_USE_SCHEMA.md](schemas/CONTEXT_OF_USE_SCHEMA.md)
- [schemas/MAP_SCHEMA.md](schemas/MAP_SCHEMA.md)
- [schemas/MAR_SCHEMA.md](schemas/MAR_SCHEMA.md)
- [CORE_TYPES.md](CORE_TYPES.md)
- [GOLDEN_SYNTHETIC_WORLD.md](GOLDEN_SYNTHETIC_WORLD.md)
- [GOLDEN_TWIN_WORLD.md](GOLDEN_TWIN_WORLD.md)
- [DEPENDENCY_RULES.md](DEPENDENCY_RULES.md)
- [PROHIBITED_DEPENDENCY_FIXTURES.md](PROHIBITED_DEPENDENCY_FIXTURES.md)
- [BENCHMARK_ESTIMAND_V0.md](BENCHMARK_ESTIMAND_V0.md)
- [SCIENTIFIC_SPEC_GOVERNANCE.md](SCIENTIFIC_SPEC_GOVERNANCE.md)
- [LOCKBOX_POLICY.md](LOCKBOX_POLICY.md)
- [../schemas/README.md](../schemas/README.md)
- [DISEASE_PATHOGEN_THERAPEUTIC_PROFILE.md](DISEASE_PATHOGEN_THERAPEUTIC_PROFILE.md)
- [SCIENTIFIC_DIGITAL_TWIN_ARCHITECTURE.md](SCIENTIFIC_DIGITAL_TWIN_ARCHITECTURE.md)
- [MODEL_CREDIBILITY_POLICY.md](MODEL_CREDIBILITY_POLICY.md)
- [QUANTITATIVE_SEMANTICS.md](QUANTITATIVE_SEMANTICS.md)
- [adr/ADR-016-model-credibility-numerical-verification.md](adr/ADR-016-model-credibility-numerical-verification.md)
- [adr/ADR-017-quantitative-semantics.md](adr/ADR-017-quantitative-semantics.md)
- [EVIDENCE_EXTRACTION_POLICY.md](EVIDENCE_EXTRACTION_POLICY.md)
- [adr/ADR-018-evidence-extraction-quality.md](adr/ADR-018-evidence-extraction-quality.md)
- [BENCHMARK_LIFECYCLE_POLICY.md](BENCHMARK_LIFECYCLE_POLICY.md)
- [adr/ADR-019-source-benchmark-lifecycle.md](adr/ADR-019-source-benchmark-lifecycle.md)
- [adr/ADR-015-scientific-digital-twin-semantics.md](adr/ADR-015-scientific-digital-twin-semantics.md)
- [adr/ADR-011-genomic-identity-harmonization.md](adr/ADR-011-genomic-identity-harmonization.md)
- [adr/ADR-012-historical-genetic-observability.md](adr/ADR-012-historical-genetic-observability.md)
- [adr/ADR-013-event-identity-source-coupling.md](adr/ADR-013-event-identity-source-coupling.md)
- [adr/ADR-014-operating-mode-data-policy.md](adr/ADR-014-operating-mode-data-policy.md)
