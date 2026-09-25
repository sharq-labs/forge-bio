# Scientific Master Plan

**Status:** PRE-CODE CANDIDATE V1 — active hardening  
**Project:** Forge Bio  
**Execution principle:** prove temporal scientific value before expensive model complexity

---

## 1. Mission

Forge Bio will determine whether a computational therapeutic-hypothesis process has measurable historical predictive value.

The platform must answer:

> If the system had access only to information defensibly available at time T, could it prioritize biological mechanisms, therapeutic targets, and later existing-drug hypotheses that subsequently reached preregistered scientific endpoints — and could it do so better than research-attention and other trivial baselines?

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

### B-TGT — Target Discovery

```text
Disease
→ historical evidence
→ pathway / mechanism
→ therapeutic target + intervention direction
→ future target/mechanism events
```

Purpose: establish whether the platform contains biological prioritization signal.

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
- E1 endpoint subtype semantics
- OutcomeGeneAssignmentPolicy
- HistoricalNoveltyAudit policy
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
- historical novelty audit
- discoverability/observation-propensity controls
- researcher-hindsight / analyst-blinding governance
- benchmark holdout governance

## Acceptance

- all output categories have explicit scientific meaning
- no generic `confidence` or `is_correct` concept exists without endpoint semantics
- architecture dependency rules documented
- deliberate prohibited dependency examples are specified
- golden world has known identities, dates, claims, evidence, and future events
- endpoint family distinguishes novel discovery from replication/evidence maturation
- locus-level evidence cannot silently become gene-level validation
- zero-event disease policy and scientific estimand are frozen before sealed outcomes
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

# BIG 0F — Benchmark Feasibility Pilot

## Goal

Test whether B-TGT-E1 ground truth can be constructed credibly before provider-scale implementation.

This is a scientific feasibility exercise, not a model-performance experiment.

## Manual pilot

Adjudicate a small heterogeneous set of future genetic events and measure:
- historical novelty at T;
- locus-level versus gene-level evidence;
- gene-assignment method and knowledge horizon;
- cohort/sample overlap;
- retrospective curation burden;
- ancestry/population metadata availability;
- adjudicator disagreement;
- fraction of unresolved AMBIGUOUS events.

## Outputs

- pilot event ledger;
- novelty-audit examples;
- gene-assignment examples;
- lineage/overlap examples;
- ambiguity statistics;
- workload estimate;
- GO / REDESIGN / NO-GO recommendation for B-TGT-E1-v0.

## Gate

Do not build provider-scale benchmark machinery if the endpoint cannot be adjudicated with acceptable ambiguity and reconstruction burden.

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
- genes
- proteins
- protein complexes
- pathways
- publications/studies

Drug/chemical identity is added later in BIG 14.

## Outputs

- internal immutable entity IDs
- external identifier assertions
- versioned mapping records
- historical model-visible mapping layer
- modern evaluation bridge
- ambiguity representation
- disease-as-of-T representation

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
- label derivation engine
- OutcomeGeneAssignmentPolicy implementation
- HistoricalNoveltyAudit workflow
- cohort/dataset/sample-overlap lineage
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
- DEVELOPMENT / VALIDATION / SEALED_LOCKBOX tiers
- ranking artifact sealing/hashing
- lockbox access ledger
- metric engine
- case-level bootstrap
- MAP/MAR execution lifecycle
- reproducibility command

## Acceptance

- predictions can be frozen before label reveal
- confirmatory execution requires frozen MAP hash
- rankers have no I/O capability outside HistoricalKnowledgeView
- injected post-cutoff future sentinels cannot affect ranking
- candidate universe itself is historical
- repeated lockbox access is logged and invalidates untouched status according to policy

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

# BIG 7 — First Target Time-Machine Experiment (B-TGT v0)

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
- null/placebo controls do not reproduce the claimed signal
- locus-to-gene and novelty sensitivity analyses pass
- results reported even if negative

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

> **A reproducible historical experiment demonstrating whether transparent, temporally clean evidence ranking contains signal beyond research-attention baselines.**

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
- explicit E1 endpoint subtype
- scientific estimand + zero-event disease policy
- OutcomeGeneAssignmentPolicy + HistoricalNoveltyAudit
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

Do temporal leakage tests, candidate-universe tests, outcome gene-assignment rules, historical-novelty audits, ascertainment controls, zero-event estimand rules, analyst-hindsight governance, and label semantics survive verification?

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
Current milestone: BIG 0
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
- [adr/ADR-006-outcome-gene-assignment.md](adr/ADR-006-outcome-gene-assignment.md)
- [adr/ADR-007-benchmark-design-provenance.md](adr/ADR-007-benchmark-design-provenance.md)
- [adr/](adr/)

No milestone status may be advanced merely because code exists. Acceptance requires its scientific/verification gate.
