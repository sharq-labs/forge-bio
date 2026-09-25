# Pre-Code Readiness Checklist

**Status:** ACTIVE — RED-TEAM HARDENED  
**Rule:** no production scientific implementation begins until every P0 item is closed or explicitly superseded by an accepted ADR.

## P0 — must close before core scientific coding

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

- [ ] Project glossary exists and ambiguous biomedical/statistical terms are defined.
- [ ] Machine-readable or normative QoI schema exists.
- [ ] Context-of-Use schema exists.
- [ ] MAP schema exists.
- [ ] MAR schema exists.
- [ ] Core scientific enums/value objects are specified.
- [ ] Minimal golden synthetic biomedical world is specified.
- [ ] Architecture import/dependency rules are specified.
- [ ] Deliberate prohibited-dependency fixtures/examples are specified.

### Benchmark estimand and endpoint

- [ ] B-TGT-E1 primary scientific estimand is frozen, including disease weighting and zero-future-event disease policy.
- [ ] B-TGT-E1 disease/genetic regime is explicitly restricted or stratified.
- [x] E1-NOVEL / E1-REPLICATION / E1-CROSSMODAL semantics are accepted.
- [x] One primary E1 subtype selection procedure is accepted before sealed evaluation.
- [ ] Endpoint evidence-quality rule is chosen after provider/outcome feasibility audit.
- [ ] Initial H candidate set and feasibility procedure are accepted.
- [x] Fixed-K evaluation has a candidate-universe-normalized companion metric.
- [x] Multiplicity policy for secondary endpoints/cutoffs/subgroups is defined.

### Outcome integrity

- [x] OutcomeGeneAssignmentPolicy accepted.
- [x] HistoricalNoveltyAudit policy accepted.
- [x] Locus/variant-level events cannot silently become gene-level positives.
- [x] Current/modern learned L2G output is prohibited as unqualified primary strict-historical ground truth.
- [x] Future-event independence includes cohort/dataset/sample-overlap semantics.
- [x] UNKNOWN sample overlap is not treated as independent replication.
- [x] Outcome adjudication blinding/dual-review policy is accepted.
- [x] Population/ancestry applicability fields are defined for relevant outcome classes.

### Ascertainment and hindsight

- [x] Discoverability / observation-propensity confounding is part of the formal threat model.
- [x] Required historical discoverability baseline family is defined.
- [x] Attention-momentum control is defined.
- [x] Researcher hindsight / design-time leakage policy is accepted.
- [x] BenchmarkDesignProvenance schema is defined.
- [ ] Ranking-team / outcome-adjudication / lockbox-custodian roles are defined.
- [ ] Sealed disease identity blinding policy is decided.
- [x] Knowledge-historical vs technology-contemporaneous claims are explicitly separated.

### Feasibility and governance

- [ ] Manual outcome feasibility pilot completed on heterogeneous events.
- [ ] Pilot reports novelty ambiguity rate.
- [ ] Pilot reports locus-to-gene assignment dependence.
- [ ] Pilot reports cohort/sample-overlap ambiguity.
- [ ] Pilot reports retrospective-curation burden.
- [ ] Pilot reports population/ancestry metadata coverage.
- [ ] Pilot yields go/redesign/no-go recommendation for B-TGT-E1-v0.
- [ ] ADR-005 licensing posture decided by project owner.
- [ ] Initial lockbox custodian/storage mechanism chosen.
- [ ] Authoritative scientific-spec change governance chosen (protected branch or equivalent reviewed process).

## P1 — must close before sealed confirmatory run

### Providers and historical reconstruction

- [ ] ProviderCards complete for every Past source.
- [ ] Future outcome sources qualified independently.
- [ ] Reconstruction fidelity verdicts available for conditional providers.
- [ ] Representation-time provenance is captured for modern structured derivations.
- [ ] Coverage/UNKNOWN thresholds frozen in MAP.

### Sampling and universes

- [ ] Disease sampling frame frozen from as-of-T criteria.
- [ ] Candidate universe policy frozen.
- [ ] Development/validation/sealed split frozen.
- [ ] Sealed-case selection cannot be changed in response to outcomes.
- [ ] Identity gold-set error rate reported.

### Statistics and controls

- [ ] Sample-size/event-yield feasibility completed on development-visible sources.
- [ ] Zero-event disease handling verified in metric engine.
- [ ] Primary K/review budget chosen on development data only.
- [ ] Candidate-universe-normalized primary/secondary metric implemented.
- [ ] Strongest required attention/discoverability comparator frozen.
- [ ] Paired disease/challenge-level CI method frozen.
- [ ] Multiplicity policy frozen.
- [ ] Negative-control suite frozen.
- [ ] Temporal placebo control defined where feasible.
- [ ] Outcome-source and gene-assignment sensitivity analyses frozen.

### Outcome integrity and applicability

- [ ] HistoricalNoveltyAudit process tested.
- [ ] Outcome gene-assignment adjudication process tested.
- [ ] Cohort/sample-overlap lineage coverage measured.
- [ ] Outcome adjudicators blinded to ranking where feasible.
- [ ] Ancestry/population coverage reported.
- [ ] Reporting/publication-bias sensitivity plan included in MAP.

### Lockbox and reproducibility

- [ ] MAP hash frozen.
- [ ] Lockbox credentials unavailable to ranking runtime/team path.
- [ ] Ranking artifact commitment mechanism tested.
- [ ] Append-only lockbox access log tested.
- [ ] BenchmarkDesignProvenance record frozen.
- [ ] Temporal metamorphic test suite passes.
- [ ] Benchmark null/falsification tests pass.
- [ ] Reproduction from manifest succeeds.

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

## Manual outcome feasibility pilot

Before provider-scale implementation, manually adjudicate a small heterogeneous set of future events and record:
- whether evidence was truly novel at T;
- locus-level versus gene-level status;
- gene-assignment method and knowledge horizon;
- cohort/sample overlap;
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

**GO FOR CORE SCIENTIFIC CODE** only when all P0 items are closed.

**GO FOR SEALED CONFIRMATORY RUN** only when all P1 items are closed.

A failed gate changes the plan; it is never bypassed to keep schedule.

The active red-team register is [SCIENTIFIC_RED_TEAM_GAPS.md](SCIENTIFIC_RED_TEAM_GAPS.md).
