# Architecture V1

**Status:** PRE-CODE CANDIDATE V1 — freeze only after P0 checklist closure  
**Project:** Forge Bio  
**Architecture style:** Modular monolith, benchmark-first, evidence-ledger, temporal by construction

---

## 1. Executive decision

Forge Bio is not architected primarily as a drug-discovery AI, knowledge graph, LLM application, or molecule-prediction system.

It is architected as a:

> **Temporally controlled scientific evidence, hypothesis-ranking, and historical-validation platform.**

The primary scientific artifact is not a raw model score. It is a ranked hypothesis generated from an explicitly frozen knowledge state, together with:

- admissible supporting evidence
- counter-evidence
- evidence gaps
- temporal admissibility
- identity mappings
- provenance
- uncertainty
- applicability limits
- ranking rationale
- later evaluation against independently defined future events

Historical validation is therefore an early platform capability, not an evaluation feature added after modeling.

---

## 2. Architectural invariants

### 2.1 Two planes, one wall

The platform has two scientific planes:

```text
PAST / HISTORICAL KNOWLEDGE PLANE
    evidence admissible at cutoff T

FUTURE / OUTCOME PLANE
    events observed after T
```

Only the evaluation layer may read both.

Rankers, feature builders, graph projections, and candidate generators must not import or query the Future plane.

### 2.2 Frozen ranking before label reveal

For confirmatory studies:

```text
freeze MAP
→ freeze historical snapshot
→ build candidate universe
→ run ranking
→ hash + seal ranking artifact
→ unlock future labels
→ evaluate
→ produce MAR
```

A result that was produced after inspecting its future labels is exploratory, not confirmatory.

### 2.3 UNKNOWN is a scientific state

UNKNOWN is never silently converted into:

- old enough
- safe
- negative
- zero uncertainty
- no contradiction
- no risk

This applies to dates, mappings, labels, evidence coverage, temporal provenance, model training cutoffs, and outcome status.

### 2.4 Graph is a projection, not truth

The authoritative scientific state is a ledger of:

- entities
- versioned identifiers/mappings
- claims
- evidence records
- temporal assessments
- provenance
- contradictions/gaps

A graph is generated from those records for a specific historical view.

### 2.5 Models do not define scientific policy

Models may compute scores.

Models may not decide:

- whether evidence is historically admissible
- whether a future event counts as a validation endpoint
- whether a locus/variant event establishes a gene-level outcome
- whether a mapping is scientifically valid
- whether missing evidence is negative
- whether a candidate is clinically effective

### 2.6 Outcome construction is governed scientific logic

Future labels are not treated as raw truth merely because they are stored in the Future plane.

Outcome construction must separately govern:
- historical novelty and HistoricalGeneticSearchCoverage;
- canonical genomic variant/locus identity and harmonization;
- locus/variant-to-gene assignment;
- phenotype identity/matching;
- cohort/dataset/SampleSet identity and independence;
- ScientificEventFamily identity/credit;
- Past/Future provider coupling;
- retrospective curation;
- adjudicator blinding;
- ascertainment/discoverability bias.

The evaluation layer may use modern reconciliation for identity, but modern biomedical reasoning may not silently manufacture a stricter historical endpoint.

### 2.7 Researcher hindsight is a leakage channel

Technical lockbox isolation does not eliminate knowledge already known to present-day researchers.

Confirmatory benchmark design therefore records BenchmarkDesignProvenance and role/exposure information. Strongest retrospective claims require the methodology to be frozen before outcome-aware changes and, where practical, before sealed disease identities are revealed to the ranking team.

---

## 3. Scientific operating mode and historical data policy

Scientific claim mode and historical-data sourcing are orthogonal.

### ScientificOperatingMode

#### 3.1 STRICT_HISTORICAL

Only information and model-visible artifacts whose biomedical knowledge content is defensibly admissible by T may be used.

A strict-historical run may support retrospective temporal claims.

#### 3.2 HISTORICAL_INPUT_MODERN_PRIOR

Explicit inputs are historical, but a modern pretrained model, ontology, embedding, mapping, or representation may encode knowledge beyond T.

This mode is useful for ablation and engineering studies, but must never be presented as evidence that the complete system could have operated at T.

#### 3.3 CURRENT_DISCOVERY

Current evidence and current models are allowed.

This mode produces present-day research hypotheses only.

It does not produce a historical-validity claim.

### HistoricalDataPolicy

```text
ARCHIVED_ONLY
RECONSTRUCTED_ALLOWED
```

A STRICT_HISTORICAL run may use RECONSTRUCTED_ALLOWED only when reconstruction-dependent fields pass the frozen Reconstruction Fidelity gate and all model-visible knowledge watermarks remain <= T.

CONTAMINATED_MODERN_PRIOR is a run classification, not a HistoricalDataPolicy value.

Normative semantics: [adr/ADR-014-operating-mode-data-policy.md](adr/ADR-014-operating-mode-data-policy.md).

---

## 4. Core scientific model

### 4.1 Identity is separate from representation

Every scientific concept receives an internal immutable identity.

External names and IDs are versioned assertions about that identity.

Core concepts include:

- DiseaseConcept
- PhenotypeConcept
- Gene
- GenomeAssembly
- ReferenceSequence
- GenomicVariant
- GenomicLocus
- Protein
- ProteinComplex
- PathwayConcept
- ChemicalStructure
- ChemicalParent / ActiveMoiety
- ActiveIngredient
- MedicinalProduct
- DrugCombination
- Publication
- Study
- Trial
- RegulatoryAction
- Cohort
- Dataset
- Biobank
- Consortium
- SampleSet
- LDReferencePanel

### 4.2 Target is a role

`Target` is not treated as a universal primitive entity.

A therapeutically meaningful target hypothesis is closer to:

```text
TargetHypothesis
    disease
    biological_entity
    desired_intervention_direction
    biological_context
    optional_modality_class
```

A gene, protein, protein complex, pathway component, or other biological entity becomes a target only relative to a disease, mechanism, direction, and context.

### 4.3 Hypothesis classes

Initial candidate classes:

- PathwayCandidate
- MechanismCandidate
- TargetCandidate
- CompoundCandidate
- RepurposingCandidate

Deferred:

- CombinationCandidate
- NovelMoleculeCandidate

Each candidate type has its own candidate universe, endpoint semantics, matching rules, and benchmark.

---

## 5. Evidence model

### 5.1 Claims and evidence are different

A claim is a structured proposition.

Example:

```text
subject: Protein X
predicate: associated_with
object: Disease Y
direction: supports inhibition
context: human / tissue / subtype / assay
```

An EvidenceRecord is one source-backed observation bearing on a claim.

### 5.2 Scientific evidence class vs source channel

Do not mix evidence method with where the evidence was found.

Example:

```text
method_class   = GENETIC_HUMAN
source_channel = PUBLICATION
extraction     = CURATED
```

Evidence semantics are orthogonal rather than one flat enum. An EvidenceRecord separates:

- evidence domain
- experimental system
- study design/method
- stance
- source channel
- extraction method
- biological context
- observation/effect payload

The normative taxonomy is defined in [EVIDENCE_TAXONOMY.md](EVIDENCE_TAXONOMY.md).

"Literature" is a source channel, not a scientific evidence-strength class.

### 5.3 Independence

Multiple databases may repeat the same experiment.

Evidence therefore carries lineage and an independence grouping such as:

```text
evidence_family_id
upstream_claim_ids
derived_from_ids
```

Aggregation must be independence-aware.

### 5.4 Support, contradiction, and gaps remain separate

Every hypothesis dossier exposes at least:

```text
Supporting evidence
Counter-evidence
Coverage / gaps
```

They are not immediately collapsed into one number.

A missing dataset is a gap.

A missing negative trial is not positive evidence.

---

## 6. Contradiction semantics

Opposite observations are not automatically contradictions.

A comparability gate must consider:

- entity compatibility
- relation compatibility
- direction
- species
- tissue / cell type
- disease subtype
- dose or intervention context
- population
- endpoint
- experimental design
- temporal scope

Conflict states may include:

- DIRECT_CONTRADICTION
- DIRECTIONAL_CONFLICT
- MECHANISTIC_CONFLICT
- NO_EFFECT
- TARGET_ENGAGEMENT_FAILURE
- CLINICAL_EFFICACY_FAILURE
- GENETIC_DIRECTION_CONFLICT
- SAFETY_COUNTEREVIDENCE
- CONTEXTUAL_DISAGREEMENT
- PARTIAL_CONTRADICTION
- RETRACTION_OR_CORRECTION
- INCOMPARABLE
- INCONCLUSIVE
- UNRESOLVED

A high model score never deletes a contradiction.

---

## 7. Temporal model

### 7.1 Distinct time dimensions

Records may have several time dimensions:

- event_time
- published_time
- first_publicly_available_time
- source_release_time
- indexed_time
- valid_from / valid_to
- superseded_time
- ingested_time
- system_observed_time

Historical admissibility is normally governed by the earliest defensible **public availability interval**, not merely by the year printed on a paper.

Every admissible record carries a first-class AvailabilityAttestation including interval, precision, basis, supporting source, and attestation quality. Normative rules are in [TEMPORAL_SEMANTICS.md](TEMPORAL_SEMANTICS.md).

### 7.2 Partial-date semantics

Never fabricate date precision.

If only the year 1998 is known:

```text
earliest_possible = 1998-01-01
latest_possible   = 1998-12-31
precision         = YEAR
```

For cutoff T:

```text
latest_possible <= T  → ADMIT
earliest_possible > T → REFUSE
interval overlaps T   → UNKNOWN
no defensible date    → UNKNOWN
```

Strict historical mode excludes UNKNOWN from model-visible data while retaining it in audit statistics.

### 7.3 Knowledge Watermark

Every knowledge-bearing artifact carries a `KnowledgeWatermark`.

The watermark means:

> the latest biomedical knowledge that the artifact could encode.

It is **not** the date on which the implementation code was written.

Formal states:

```text
NON_KNOWLEDGE_BEARING
DATED(date)
UNKNOWN
```

Join semantics:

```text
join(NON_KNOWLEDGE_BEARING, DATED(2008)) = DATED(2008)
join(DATED(2006), DATED(2008))            = DATED(2008)
join(UNKNOWN, anything)                    = UNKNOWN
```

Every code/config/rule dependency also declares KnowledgeBearingness = NON_KNOWLEDGE_BEARING | KNOWLEDGE_BEARING | UNKNOWN. A modern implementation date alone does not move the watermark, but hard-coded biomedical knowledge does.

Examples of non-knowledge-bearing implementation:

- hashing
- deterministic sorting
- arithmetic
- generic serialization
- generic statistical primitives

Examples of knowledge-bearing artifacts:

- ontology releases
- disease mappings
- manually curated gene-family lists
- pretrained biomedical language models
- current graph topology
- embeddings
- learned negative-sampling distributions
- target classifications

Implementation provenance is stored separately:

```text
code_commit
library_version
container_digest
configuration_hash
```

### 7.4 Transitive temporal taint

The watermark propagates through the full dependency DAG:

```text
raw record
→ normalization
→ mapping
→ knowledge projection
→ feature
→ embedding
→ model
→ prediction
```

If any required knowledge-bearing dependency is UNKNOWN or later than T, the derived artifact is not admissible in STRICT_HISTORICAL mode.

### 7.5 Observation time vs representation time

A historical observation and a later structured representation of that observation carry separate temporal provenance.

Example:

```text
paper_publicly_available = 2008
structured_gene_assignment_created = 2026
```

The 2008 paper does not make the 2026 knowledge-bearing assignment historical.

### 7.6 Knowledge-historical vs technology-contemporaneous

STRICT_HISTORICAL guarantees a biomedical knowledge boundary.

It does not, by itself, prove that the exact modern software stack, algorithms, compute, or infrastructure could have existed at T.

Claims about contemporaneous technological feasibility require a separate study.

---

## 8. Identity model

### 8.1 Historical identity vs evaluation bridge

Modern identity resolution can itself leak future knowledge.

Therefore identity is split into:

**Model-visible historical identity**

- only mappings admissible by T
- usable in candidate generation and features

**Evaluation bridge**

- may use modern mappings
- used only after ranking to reconcile entity identity for later future events
- never visible to feature generation or ranking
- may not convert a locus/variant association into a causal-gene outcome merely by modern assignment
- may not rescue a failed prediction through post-hoc broadening without a preregistered sensitivity analysis

### 8.2 Genomic and study-population identity

For genetic evidence/outcomes:
- rsIDs and coordinate strings are external representations, not canonical variant identity;
- genome assembly/reference sequence, normalized alleles, liftover, strand/orientation, and harmonization are provenance-bearing;
- LD proxy relations carry population/ancestry, reference panel/release, assembly, metric, value, and derivation provenance;
- Cohort/Dataset/Biobank/Consortium/SampleSet identities replace free-text independence assertions;
- PhenotypeConcept is distinct from DiseaseConcept.

Normative policy: [adr/ADR-011-genomic-identity-harmonization.md](adr/ADR-011-genomic-identity-harmonization.md).

### 8.3 Mapping uncertainty is preserved

A mapping is not forced to one answer.

A mapping record should include:

```text
mapping_id
internal_entity_id
external_namespace
external_identifier
relation: EXACT | BROAD | NARROW | RELATED | REPLACED_BY
source
source_version
valid_from
valid_to
availability_interval
mapping_confidence
review_status
provenance_id
```

One-to-many identity is represented explicitly.

---

## 9. HistoricalKnowledgeView

Rankers never receive:

- unrestricted database connections
- raw object-store credentials
- Future Outcome storage
- provider APIs
- arbitrary SQL access
- filesystem paths to raw datasets

They receive a frozen read-only capability:

```text
HistoricalKnowledgeView
    cutoff
    scientific_operating_mode
    historical_data_policy
    temporal_policy
    admitted datasets
    admissibility statistics
    content hashes
    knowledge watermark
```

This view is the only model-visible scientific knowledge boundary.

CandidateUniverse is a **separate immutable input artifact** so the same HistoricalKnowledgeView can support different benchmark families without conflating "what was knowable" with "what this study permits ranking".

---

## 10. Candidate-universe policy

The candidate universe itself is a possible leakage channel.

A historical experiment must not rank all entities known today.

Candidate eligibility must be proven as-of-T.

Conceptually:

```text
entity_known_by_cutoff == TRUE
and
identity_admissible_by_cutoff == TRUE
and
candidate_class_eligible == TRUE
```

Candidate-universe construction is versioned, hashed, included in the MAP, and carries membership provenance.

Historical identity eligibility does not imply equal genetic measurability at T. The benchmark therefore preserves the broad identity-valid universe and reports a preregistered GeneticObservabilityAtT sensitivity universe constructed only from as-of-T criteria.

The normative policy is defined in [IDENTITY_POLICY.md](IDENTITY_POLICY.md) and [BENCHMARK_V0_SPEC.md](BENCHMARK_V0_SPEC.md).

---

## 11. Future Outcome / Oracle plane

Ground truth is not stored as one `is_correct` field.

Future events must carry source lineage, a ScientificEventFamily identity, and an independence family. A post-cutoff database annotation that merely re-curates pre-cutoff evidence is not automatically independent validation.

A preprint, paper, and database rows may be manifestations of one scientific event. Default V0 primary credit is at most one per ScientificEventFamily.

Past input and Future outcome provider lineages are compared for shared upstream/curation machinery. Material coupling requires sensitivity analysis.

For genetic outcomes, the event ledger distinguishes locus/variant discovery from gene assignment. Gene-level positives retain assignment method, assignment evidence, assignment time, assignment knowledge watermark, and uncertainty.

Independence lineage may include study, cohort, consortium, dataset/biobank, participant-overlap group, and meta-analysis parents. UNKNOWN overlap is not treated as independent replication.

E1-NOVEL-STRICT outcomes require `PreTGeneticState = NO_SIGNAL_OBSERVED`, `HistoricalNoveltyAudit = NOVEL_CONFIRMED`, and the MAP-frozen minimum HistoricalGeneticSearchCoverage grade. Below-threshold historical coverage becomes AMBIGUOUS, not strict novelty.

The outcome plane distinguishes KNOWN_TO_RANKER_AT_T from KNOWN_PUBLICLY_AT_T so a provider miss is not mistaken for future novelty.

Future genetic outcomes also carry explicit phenotype-match and replication assessments. A related trait/risk factor is not silently promoted to the benchmark disease, and a repeated locus is not automatically independent replication.

It is an immutable ledger of FutureEvents such as:

- biological association
- human genetic validation
- mechanistic validation
- functional intervention evidence
- preclinical validation
- target clinical entry
- drug clinical entry
- clinical efficacy signal
- clinical failure
- regulatory approval
- regulatory withdrawal
- guideline adoption
- mechanistically informative failure

Endpoint-specific labels are derived from this event ledger.

Label states include:

- POSITIVE
- NEGATIVE_CONFIRMED
- UNKNOWN
- RIGHT_CENSORED
- COMPETING_EVENT
- CONFLICTED / AMBIGUOUS
- KNOWN_AT_T where applicable

"Not observed" does not automatically mean negative.

---

## 12. Benchmark families

### 12.1 B-TGT — Target Program

B-TGT is an umbrella program for biological and eventual therapeutic-target prioritization.

The first V0 benchmark is explicitly narrower:

```text
B-TGT-A1 / B-TGT-E1-v0
Disease–Gene Association Prioritization
```

It asks whether temporally clean evidence can rank disease–gene associations that later receive predefined independent human genetic support.

This V0 benchmark does **not** by itself establish causal therapeutic-target validity, intervention direction, or tractability. Stronger target-discovery language requires later mechanism/direction/causal-target endpoints.

### 12.2 B-REP — Drug Repurposing

Primary question:

> Given only evidence available at T and an as-of-T universe of existing active moieties / drugs, can the system prioritize disease–drug hypotheses that later receive predefined investigation or success events?

This benchmark tests translation from biological prioritization into therapeutic prioritization.

Trial entry and therapeutic success are separate endpoints.

---

## 13. Benchmark governance

Every confirmatory benchmark freezes:

- Question of Interest
- Context of Use
- scientific estimand
- zero-future-event disease policy
- disease/genetic regime
- primary endpoint subtype
- cutoff
- observation horizon
- candidate universe
- disease universe
- allowed and forbidden providers
- provider releases
- scientific operating mode
- historical data policy
- temporal policy
- identity policy
- genomic identity / variant-harmonization / LD policy
- historical genetic-search coverage / observability policy
- ScientificEventFamily credit policy
- provider-coupling policy
- endpoint definitions
- pre-T genetic-state policy
- phenotype-match policy
- outcome gene-assignment policy
- genetic-replication policy
- label rules
- matching rules
- validation-generation identity/status/access count/disclosure level
- CrossAnchorEventReusePolicy
- outcome-event discovery freeze
- Future Outcome snapshot/ledger/event-family/provider-coupling commitment
- ranking algorithm
- model/config versions
- random seeds
- primary and secondary metrics
- candidate-universe-normalized companion metric
- all-frame review-budget utility
- discoverability/observation-propensity control
- negative/null control plan
- confidence-interval method
- disease-family/block dependence sensitivity
- multiplicity policy
- historical novelty policy
- BenchmarkDesignProvenance
- success criteria
- exclusions
- subgroup analyses
- ablations
- holdout tier
- permitted lockbox accesses

Holdout tiers:

```text
DEVELOPMENT
VALIDATION
SEALED_LOCKBOX
```

A lockbox that has been repeatedly inspected is no longer an untouched lockbox.

VALIDATION is also versioned into generations. Once a validation generation materially influences methodology, it is marked SPENT_FOR_MODEL_SELECTION rather than represented as untouched evidence.

The exact Future Outcome snapshot/ledger/adjudication/identity-bridge artifacts are committed before sealed evaluation so labels cannot silently move after ranking freeze.

---

## 14. Metrics and success criterion

Important metrics may include:

- Recall@K
- Recall at percentage of candidate universe
- event MRR
- NDCG@K where graded relevance is predeclared
- enrichment@K vs random
- candidate rank percentile
- cumulative event recall
- all-frame observed-event yield per total review budget
- event-bearing disease coverage
- zero-event disease review burden
- disease-level confidence intervals with disease-family/block sensitivity

Hit@K may be reported descriptively but must not be the sole headline metric.

The central scientific comparator is lift over the strongest preregistered non-biological explanation available for the endpoint.

For B-TGT-E1 this includes both research attention and discoverability/observation propensity.

Examples:

```text
ΔRecall@K vs historical research attention
ΔRecall@K vs discoverability control
ΔNDCG@K vs attention/discoverability control
```

A sophisticated model that only re-ranks what researchers were already studying — or what was simply easiest to measure next — has not demonstrated biological discovery value.

---

## 15. Modeling progression

Promotion is evidence-gated:

```text
Random
→ Research attention / popularity
→ Deterministic evidence ranking
→ Regularized classical models
→ Nonlinear tabular models
→ Historical graph features
→ KGE
→ GNN
→ Approved historical-safe pretrained representations
→ Multimodal models
→ Ensembles
```

Each stage must show incremental value over the best simpler stage.

Modern pretrained artifacts whose training knowledge horizon exceeds T are excluded from STRICT_HISTORICAL mode.

---

## 16. Storage architecture

V1 is a modular monolith.

Recommended storage:

- immutable raw provider artifacts: content-addressed object storage or local equivalent
- normalized analytical datasets: Parquet
- local analytical query: DuckDB / Polars
- scientific registry and relational integrity: PostgreSQL when operationally justified
- graph projections: in-memory / per-view, using NetworkX, igraph, or later tensor formats
- MAP/MAR/specifications: content-addressed JSON/YAML + rendered Markdown/HTML

A graph database is not the system of record.

PostgreSQL is not required merely to begin BIG 0; it is introduced when the registry, identity constraints, access logs, and experiment lifecycle need transactional persistence.

---

## 17. Provider architecture

Provider adapters expose source facts, not scientific truth.

A provider should conceptually support:

```text
metadata()
license_info()
list_available_releases()
get_release_manifest()
fetch_release()
verify_release()
parse_snapshot()
availability_evidence()
record_provenance()
capabilities()
```

Provider qualification states include:

- HISTORICAL_SAFE
- HISTORICAL_CONDITIONAL
- CURRENT_ONLY
- FUTURE_VALIDATION_ONLY
- PROHIBITED_FOR_BENCHMARK
- UNKNOWN

UNKNOWN is never treated as safe.

Historical cutoffs are chosen after provider temporal audit, not assumed in advance.

Provider qualification is field/derivation-level, not only provider-level: (provider, release, field_or_derivation, intended_use). The normative process and Reconstruction Fidelity Study are defined in [PROVIDER_QUALIFICATION.md](PROVIDER_QUALIFICATION.md).

---

## 18. Repository bounded contexts

Target repository structure:

```text
src/forge_bio/
├── kernel/
├── identity/
├── temporal/
├── provenance/
├── uncertainty/
├── providers/
├── corpus/
├── evidence/
├── knowledge/
├── hypotheses/
├── ranking/
├── outcomes/
├── benchmarks/
├── experiments/
├── validation/
├── reporting/
└── interfaces/
```

Cross-cutting architecture rules are enforced with tests/import contracts.

---

## 19. Verification vs validation

### Verification

Asks whether the software behaves according to specification.

Required examples:

- temporal admission property tests
- UNKNOWN fail-closed tests
- knowledge-watermark propagation tests
- future-sentinel tests
- candidate-universe determinism
- identity mapping invariants
- genomic normalization/liftover/allele/LD provenance invariants
- cohort/dataset/SampleSet identity/overlap invariants
- snapshot checksum tests
- feature/preprocessing lineage completeness
- ScientificEventFamily deduplication tests
- cross-anchor event-reuse tests
- provider-coupling audit tests
- metric golden tests
- reproducibility from manifests
- ranking determinism
- network-disabled confirmatory runs where applicable
- forbidden import/dependency tests

Critical metamorphic invariant:

> Adding a post-cutoff inadmissible record must produce no change in historical features or ranking.

### Validation

Asks whether the system has scientifically useful predictive behavior.

Eventually includes:

- rolling temporal holdouts
- unseen diseases
- disease-family holdouts
- target-family holdouts
- similarity-aware splits
- external future-outcome sources
- multiple historical cutoffs
- outcome gene-assignment sensitivity
- genomic harmonization / LD-reference-panel sensitivity
- historical-novelty/search-coverage audit
- historical genetic-observability sensitivity
- ScientificEventFamily credit sensitivity
- Past/Future provider-coupling sensitivity
- discoverability/ascertainment controls
- blinded outcome adjudication
- benchmark null/placebo controls
- ablation studies
- calibration where meaningful
- sealed lockbox
- prospective shadow validation

---

## 20. LLM policy

No LLM participates in the strict V1 ranking path.

Later LLM/NLP extraction may be introduced only behind controlled interfaces with:

- explicitly supplied documents
- span grounding
- model/version provenance
- unsupported-fact rejection
- extraction validation
- null/shuffled-document canaries
- strict vs contaminated-arm comparison

An LLM never controls temporal admission, labels, validation status, or scientific truth.

---

## 21. Scientific stop rule

Before expensive graph/deep/multimodal development:

> If deterministic and classical models cannot show credible lift over research-attention, evidence-count, and endpoint-appropriate discoverability controls on sealed historical cases, stop advanced modeling and investigate the data, endpoint definition, candidate universe, ascertainment process, and scientific premise.

A clean negative result is preferable to an impressive contaminated demo.

---

## 22. Architectural decisions frozen in V1

The following are frozen unless superseded by ADR:

1. Benchmark-first development.
2. Past/Future plane separation.
3. HistoricalKnowledgeView as model input capability.
4. UNKNOWN is first-class and fail-closed.
5. KnowledgeWatermark is separate from implementation provenance.
6. Graph is a projection.
7. Target is a disease/context-specific role.
8. Evidence method is distinct from source channel.
9. Candidate universes are historical.
10. Future ground truth is event-based and endpoint-specific.
11. Research-attention and endpoint-appropriate discoverability controls are mandatory.
12. Cutoff era is selected through provider audit.
13. Gene-level future outcomes separate identity reconciliation from locus-to-gene assignment.
14. Strict novelty distinguishes no-observed-signal from suggestive pre-T genetics.
15. Disease/trait phenotype matching is explicit.
16. Genetic replication requires allele/direction/phenotype/lineage comparability.
17. Historical novelty is audited independently for discovery claims.
18. Researcher hindsight is governed separately from technical future-label isolation.
19. Validation generations track adaptive reuse.
20. Exact Future Outcome snapshots/ledgers are committed before sealed evaluation.
21. The benchmark estimand and zero-event disease policy are frozen before sealed outcome access.
22. B-TGT precedes or accompanies B-REP as the biological foundation.
23. No LLM/deep model requirement in V1.
24. No clinical-treatment claims.
25. Genomic variant/locus identity is reference/assembly/allele aware; rsIDs are external identifiers.
26. Harmonization/liftover/LD relations are provenance-bearing scientific derivations.
27. Strict novelty is gated by historical genetic-search coverage.
28. KNOWN_TO_RANKER_AT_T and KNOWN_PUBLICLY_AT_T are distinct.
29. ScientificEventFamily identity prevents duplicated manifestations/locus-to-many-gene inflation.
30. Past/Future provider coupling is measured and sensitivity-tested.
31. Cross-anchor event reuse is explicitly bounded.
32. ScientificOperatingMode and HistoricalDataPolicy are orthogonal.


---

## 23. Pre-code hardening references

The following documents are normative for implementation detail and close gaps intentionally left abstract in this architecture:

- [BENCHMARK_V0_SPEC.md](BENCHMARK_V0_SPEC.md) — first falsifiable benchmark, disease sampling frame, candidate universe, future-event independence, paired baseline delta.
- [TEMPORAL_SEMANTICS.md](TEMPORAL_SEMANTICS.md) — AvailabilityAttestation, KnowledgeBearingness, watermark algebra, retractions, temporal metamorphic tests.
- [EVIDENCE_TAXONOMY.md](EVIDENCE_TAXONOMY.md) — orthogonal evidence schema and minimal contradiction primitive.
- [IDENTITY_POLICY.md](IDENTITY_POLICY.md) — historical identity, evaluation bridge, deterministic hypothesis identity, canonical serialization.
- [PROVIDER_QUALIFICATION.md](PROVIDER_QUALIFICATION.md) — field-level provider qualification and Reconstruction Fidelity Study.
- [MODEL_TRAINING_POLICY.md](MODEL_TRAINING_POLICY.md) — nested temporal supervised training and leakage-safe tuning.
- [PRE_CODE_CHECKLIST.md](PRE_CODE_CHECKLIST.md) — P0/P1 go/no-go gates.
- [SCIENTIFIC_RED_TEAM_GAPS.md](SCIENTIFIC_RED_TEAM_GAPS.md) — active adversarial scientific-integrity blockers.
- [adr/ADR-006-outcome-gene-assignment.md](adr/ADR-006-outcome-gene-assignment.md) — locus/gene assignment and historical novelty.
- [adr/ADR-007-benchmark-design-provenance.md](adr/ADR-007-benchmark-design-provenance.md) — researcher hindsight, role separation, and blinding.
- [adr/ADR-008-outcome-phenotype-matching.md](adr/ADR-008-outcome-phenotype-matching.md) — disease/trait phenotype equivalence for future outcomes.
- [adr/ADR-009-genetic-replication-and-signal-state.md](adr/ADR-009-genetic-replication-and-signal-state.md) — strict novelty, maturation, and genetic replication semantics.
- [adr/ADR-010-validation-generations-and-outcome-freeze.md](adr/ADR-010-validation-generations-and-outcome-freeze.md) — validation reuse and immutable Future Outcome commitments.
- [adr/ADR-011-genomic-identity-harmonization.md](adr/ADR-011-genomic-identity-harmonization.md) — canonical genomic identity, harmonization, and LD provenance.
- [adr/ADR-012-historical-genetic-observability.md](adr/ADR-012-historical-genetic-observability.md) — historical search coverage, public-vs-ranker knowledge, and observability.
- [adr/ADR-013-event-identity-source-coupling.md](adr/ADR-013-event-identity-source-coupling.md) — event-family identity, provider coupling, cross-anchor reuse, and validation disclosure.
- [adr/ADR-014-operating-mode-data-policy.md](adr/ADR-014-operating-mode-data-policy.md) — operating mode vs historical data policy.
- [../schemas/README.md](../schemas/README.md) — executable QoI/MAP/MAR schemas.
- [adr/](adr/) — explicit decisions that may change architecture.

### Freeze rule

This document becomes **FROZEN V1** only after every P0 item in PRE_CODE_CHECKLIST is closed or explicitly superseded by an ADR. Until then, implementation may cover tooling/document schemas needed to close P0, but scientific production code must not outrun unresolved contracts.
