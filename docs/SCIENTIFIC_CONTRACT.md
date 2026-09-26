# Scientific Contract

**Status:** PRE-CODE CANDIDATE V1 — freeze only after P0 checklist closure  
**Purpose:** Define what Forge Bio may claim, what it must prove, and what it must never silently assume.

---

## 1. Product scientific statement

Forge Bio is a research prioritization platform.

Its defensible core statement is:

> For a predefined biomedical Question of Interest, historical cutoff, candidate universe, evidence policy, and future-validation endpoint, Forge Bio ranks research hypotheses using only temporally admissible evidence and measures whether those rankings are enriched for later independent scientific events relative to predefined baselines.

The platform is a search-space reduction instrument.

It is not an oracle of therapeutic truth.

---

## 2. V1 Context of Use

V1 is intended for:

- retrospective biomedical research
- target/mechanism prioritization
- later existing-drug / active-moiety repurposing research
- evidence review
- benchmark development
- computational hypothesis generation for further investigation
- evidence-backed disease/pathogen/therapeutic scientific profiles
- Forge Bio Scientific Twin research models under explicit maturity/VVUQ gates

V1 is not intended for:

- patient diagnosis
- patient-specific treatment selection
- patient-specific digital-twin clinical decision support under V1
- dosing
- clinical decision support
- prescribing
- laboratory synthesis instructions
- pharmaceutical manufacturing instructions
- claiming an in-silico result is a proven therapy

No patient-level data are required for the scientific core.

---

## 3. Separation of scientific concepts

Forge Bio must distinguish everywhere:

```text
PREDICTION
    ≠
EVIDENCE
    ≠
VALIDATION
    ≠
CAUSAL TRUTH
    ≠
CLINICAL TRUTH
```

A high rank is not validation.

A validated association is not necessarily causal.

A causal mechanism is not automatically clinically useful.

Clinical investigation is not clinical efficacy.

Regulatory approval is not identical to mechanism proof.

---

## 4. Claim maturity ladder

### L0 — Reproducible output

Allowed claim:

> The platform produces a deterministic/versioned ranking with complete provenance.

Required evidence:

- software verification
- snapshot identity
- model/config identity
- reproducible output

### L1 — Rediscovery

Allowed claim:

> The ranking recovers relationships already known by the cutoff.

Required evidence:

- known-at-T rediscovery track

Interpretation:

Weak evidence of scientific usefulness. Many trivial methods may pass.

### L2 — Development-set retrospective enrichment

Allowed claim:

> The ranking is enriched for later events on development cases.

Required evidence:

- temporal benchmark
- confidence intervals
- baseline comparisons

### L3 — Sealed confirmatory enrichment

Allowed claim:

> On a preregistered sealed benchmark, the method outperformed predefined random, research-attention, and required discoverability/observation-propensity controls for endpoint E.

Required evidence:

- frozen MAP
- sealed lockbox
- one-shot confirmatory evaluation
- MAR
- confidence interval for the baseline delta

### L4 — Generalization

Allowed claim:

> The historical enrichment generalizes across cutoffs, disease families, and/or independent data sources.

Required evidence:

- rolling-origin analysis
- disease-family holdout
- external-source validation
- source ablations

### L5 — Endpoint-calibrated probabilities

Allowed claim:

> Scores are calibrated probabilities for a precisely defined endpoint E within horizon H, inside the evaluated applicability domain.

Required evidence:

- sufficient event count
- held-out calibration
- temporal calibration assessment
- confidence intervals
- explicit endpoint and horizon

This does **not** entitle the platform to say "probability the therapy works" unless that is exactly the statistically evaluated endpoint.

### L6 — Prospective evidence

Allowed claim:

> Predictions registered prospectively at time t were later validated above baseline under the preregistered endpoint.

Required evidence:

- immutable public/timestamped prediction ledger
- future follow-up
- independent outcome collection

This is the strongest protection against hidden retrospective bias.

---

## 5. Claims the platform must never make from rank alone

Forge Bio must not infer any of the following solely from a computational ranking:

- "Drug X treats Disease Y."
- "Target X is clinically validated."
- "This is a cure."
- "This therapy is effective."
- "This candidate is safe."
- "No contradictory evidence exists, therefore the hypothesis is correct."
- "Multiple models agree, therefore the evidence is independent."
- "A retrospective hit proves the platform would have discovered the therapy."
- "A high model score proves causality."
- "No later event occurred, therefore the hypothesis is false."

Reports must use endpoint-specific language.

---

## 6. Question of Interest template

Every governed study defines a Question of Interest (QoI).

Example:

> Given only publicly available biomedical evidence admissible by cutoff T, can Forge Bio prioritize disease-specific therapeutic target hypotheses that later reach endpoint E within horizon H, with positive lift over historical research-attention and endpoint-appropriate discoverability controls?

Required QoI fields:

```text
question_id
hypothesis_type
disease_scope
historical_cutoff
candidate_universe_policy
future_endpoint
evaluation_horizon
primary_metric
baseline_family
context_of_use
```

---

## 7. Context of Use template

Every MAP must freeze:

```text
intended_use
intended_users
model_influence
consequence_of_false_positive
consequence_of_false_negative
direct_patient_impact
excluded_uses
applicability_domain
```

For V1:

```text
intended_use:
    research prioritization and retrospective benchmarking

model_influence:
    low-to-moderate; humans decide what to review or investigate

direct_patient_impact:
    none by design

excluded_uses:
    diagnosis, prescribing, dosing, patient-level recommendations
```

---

## 8. Temporal integrity contract

### 8.1 Admission is fail-closed

For availability interval A and cutoff T:

```text
A.latest <= T   → ADMIT
A.earliest > T  → REFUSE
otherwise       → UNKNOWN
```

UNKNOWN is excluded from strict model-visible data.

### 8.2 Date precision must be preserved

A year-only source date is not silently converted to January 1.

Partial dates remain partial.

### 8.3 Historical state is stronger than retrospective filtering

Preferred order:

1. archived byte-exact historical release
2. trustworthy row-level public-availability timestamp
3. defensible reconstruction with measured bias
4. current-only retrospective state — prohibited from strict historical input

### 8.4 Knowledge watermark invariant

Every knowledge-bearing derived artifact must satisfy:

```text
artifact.knowledge_watermark <= historical_cutoff
```

in STRICT_HISTORICAL mode.

If the watermark is UNKNOWN, the artifact is inadmissible.

Every relevant code/config/rule dependency also declares whether it is NON_KNOWLEDGE_BEARING, KNOWLEDGE_BEARING, or UNKNOWN. Implementation date/version is provenance, not automatically a biomedical knowledge watermark. Normative semantics are in [TEMPORAL_SEMANTICS.md](TEMPORAL_SEMANTICS.md).

### 8.5 Future outcome isolation

Rankers may not import or query the future outcome plane.

Only evaluation joins:

```text
sealed historical prediction
+
future outcome ledger
```

---

## 9. Leakage threat model

At minimum, the project treats the following as explicit threats:

- direct future-record leakage
- retrospective curation leakage
- ontology leakage
- identity-mapping leakage
- genomic-variant identity / genome-build / liftover leakage
- allele-orientation / harmonization leakage
- LD/reference-panel leakage
- candidate-universe leakage
- graph-topology leakage
- feature-selection leakage
- normalization leakage
- negative-label leakage
- pretrained-model leakage
- foundation-model / LLM leakage
- structural leakage
- disease-selection hindsight
- benchmark overfitting
- repeated lockbox inspection
- publication-version leakage
- similarity leakage across train/test entities
- researcher hindsight encoded in hand-designed features
- outcome-construction leakage
- locus-to-gene assignment leakage
- historical-novelty misclassification
- ascertainment / discoverability bias
- publication / selective-reporting bias
- cohort/sample-overlap masquerading as replication
- duplicated ScientificEventFamily manifestations inflating event counts
- locus-to-many-gene assignments inflating primary credit
- Past/Future provider or curation-pipeline coupling
- rolling-anchor duplicate event reuse
- preprocessing/statistic-fit leakage
- validation-feedback granularity/adaptive reuse
- analyst/adjudicator outcome-aware bias
- ancestry/population applicability bias
- future-conditioned exclusion of zero-event diseases

Every major benchmark MAR includes a leakage audit.

---

## 10. Evidence contract

### 10.1 Evidence must be source-backed

Every evidence item links to:

- source artifact
- source record
- evidence domain
- experimental system
- study design/method
- source channel
- biological context
- AvailabilityAttestation
- provenance lineage
- extraction method
- independence family

The normative orthogonal schema is defined in [EVIDENCE_TAXONOMY.md](EVIDENCE_TAXONOMY.md).

### 10.2 Literature is not a strength class

A publication may contain:

- genetic evidence
- biochemical evidence
- functional evidence
- structural evidence
- clinical evidence
- review/opinion material

Therefore:

```text
scientific_method_class != source_channel
```

### 10.3 Computational predictions are derived evidence

A model prediction may be stored as a derived computational artifact.

It may not be silently promoted to independent biological evidence.

### 10.4 Missing evidence is not evidence

```text
NO_DATA_AT_T
NOT_ASSESSED
UNKNOWN
```

never improve a hypothesis score unless a predeclared, scientifically justified policy explicitly models missingness as information.

---

## 11. Contradiction contract

Support, counter-evidence, and gaps are kept distinct.

A contradiction requires contextual comparability.

The project must not define:

```text
contradiction_score =
    supporting_source_count
    - negative_source_count
```

without method/context semantics.

Important conflict types include:

- directional conflict
- mechanistic conflict
- no-effect evidence
- target-engagement failure
- clinical efficacy failure
- genetic direction conflict
- safety counter-evidence
- contextual disagreement
- retraction/correction
- unresolved conflict

A strong score with a material unresolved contradiction is presented as **contested**, not as a strong validated candidate.

---

## 12. Identity contract

Names are never authoritative scientific joins.

Identity resolution must:

- preserve external namespace and version
- preserve mapping provenance
- preserve ambiguity
- distinguish gene, protein, complex, active moiety, ingredient, product, and combination
- treat PhenotypeConcept, GenomicVariant, GenomicLocus, GenomeAssembly, ReferenceSequence, Cohort, Dataset, Biobank, Consortium, SampleSet, and LDReferencePanel as first-class where they affect benchmark semantics
- treat rsIDs/coordinate strings and cohort/dataset names as external representations, not canonical identity
- preserve genome-build/normalization/liftover/allele-harmonization provenance
- support historical model-visible mappings
- isolate modern evaluation mappings from historical feature generation

A mapping with ambiguity is not silently coerced to EXACT.

---

## 13. Ground-truth contract

Ground truth is an event ledger with canonical scientific-event identity.

A preprint, journal article, database row, and secondary curation may be multiple manifestations of one ScientificEventFamily. Primary event credit is governed at the event-family level, not raw-row count.

A future event counts as independent only when its lineage satisfies the benchmark's independence rule. A later annotation that merely re-curates pre-cutoff evidence is not automatically independent validation.

Distinct publications or databases are not sufficient proof of independence or distinct scientific events. Where relevant, outcome lineage must retain cohort, consortium, dataset/biobank, meta-analysis parents, and participant-overlap state. UNKNOWN sample overlap is not interpreted as independent replication.

For gene-level genetic outcomes, identity reconciliation and causal-gene assignment are separate operations. A modern identity bridge may reconcile identifiers, but it may not create a gene-level validation from a locus/variant event without passing the governed OutcomeGeneAssignmentPolicy.

Disease/trait identity and phenotype applicability are also separate. A related biomarker, risk factor, intermediate phenotype, broader trait, or narrower trait is not automatically the same benchmark disease. OutcomePhenotypeMatchPolicy governs this relation.

Historical novelty distinguishes KNOWN_TO_RANKER_AT_T from KNOWN_PUBLICLY_AT_T. A public pre-T result missed by the ranker's provider is a coverage failure, not future novelty.

E1-NOVEL-STRICT requires the frozen minimum HistoricalGeneticSearchCoverage grade. Below-threshold coverage yields AMBIGUOUS rather than NO_SIGNAL_OBSERVED.

A later genetic record is not automatically replication. E1-REPLICATION requires a GeneticReplicationAssessment covering phenotype, locus/variant, allele harmonization, effect direction, LD relation where relevant, population, cohort independence, participant overlap, analysis compatibility, and heterogeneity.

Benchmarks derive labels for a named endpoint.

Examples of distinct endpoints:

- later biological association
- human genetic support
- mechanistic validation
- functional intervention evidence
- clinical entry
- efficacy signal
- regulatory approval
- regulatory withdrawal
- guideline adoption
- mechanistically informative failure

Do not collapse them into one generic `SUCCESS`.

---

## 14. Label-state contract

At minimum:

### POSITIVE

A preregistered qualifying event occurred within the evaluation horizon.

### NEGATIVE_CONFIRMED

Affirmative evidence satisfies a preregistered failure definition for the same endpoint.

### UNKNOWN

Available observations do not establish positive or negative status.

### RIGHT_CENSORED

Follow-up is insufficient to fully observe the endpoint horizon.

### COMPETING_EVENT

A different event materially prevents interpretation of the primary endpoint.

### CONFLICTED / AMBIGUOUS

Outcome evidence cannot be reliably assigned to one state.

### KNOWN_AT_T

The endpoint or a stronger relationship was already established by T.

Used for rediscovery/training policy, but excluded from the main "future discovery" evaluation.

---

## 15. Benchmark contract

A confirmatory benchmark must freeze before evaluation. Disease selection and the candidate universe must themselves be defined from as-of-T criteria; famous later-success cases cannot be hand-picked into the primary confirmatory sample.

A confirmatory benchmark must freeze:

- scientific operating mode
- historical data policy
- cutoff
- candidate universe
- disease universe
- provider releases
- temporal policy
- identity policy
- genomic identity / variant-harmonization / LD policy
- historical genetic-search coverage and observability policy
- scientific-event-family credit policy
- Past/Future provider-coupling policy
- endpoint
- horizon
- matching policy
- baseline definitions
- model/version
- features
- metrics
- primary metric
- success threshold
- CI method
- exclusions
- ablations
- holdout tier
- validation disclosure policy
- cross-anchor event reuse policy
- outcome-event discovery freeze
- exact Future Outcome event-family/provider-coupling commitment
- access policy

Changes after freeze are deviations and appear in the MAR.

They are not silently edited out of the study history.

---

## 16. Baseline and ascertainment-control contract

Every advanced ranking result is compared to at least:

- random
- historical research attention / publication popularity
- attention momentum / research-growth velocity
- evidence-volume popularity
- candidate popularity / graph-degree control where applicable
- deterministic transparent evidence ranking
- a historical discoverability / observation-propensity control for endpoints whose future observation depends materially on study opportunity

The discoverability control may include only defensible as-of-T nuisance predictors such as prior study availability, cohort/sample-size trajectory, phenotype measurability proxies, annotation density, or prior-association momentum.

These variables are benchmark controls first; they are not automatically ranker features.

The scientific value question is:

> Does the method add biological prioritization signal beyond what the field was already studying and beyond what was simply easiest or most likely to be measured next?

Beating random or cumulative publication count alone is insufficient.

---

## 17. Statistical contract

### 17.1 Disease-level dependence

Targets within one disease are not independent samples.

Primary confidence intervals should resample at the disease/challenge level unless a justified alternative is preregistered.

Related diseases may themselves share genes, pathways, cohorts, consortia, controls, or publication ecosystems. Confirmatory studies therefore include a preregistered disease-family/block or other cluster-aware dependence sensitivity. If the signal materially weakens, that limitation is part of the primary interpretation.

### 17.2 Unknown labels

Do not compute ordinary classification metrics by treating UNKNOWN candidates as negatives.

### 17.3 Calibration

A probability is displayed only when:

- the event is precisely defined
- the horizon is defined
- calibration has been evaluated
- event counts are sufficient
- applicability conditions are satisfied

Otherwise the output remains a score/rank with explicit uncertainty, not a fake probability.

### 17.4 Estimand and zero-event diseases

Every primary benchmark defines the target estimand before sealed outcome access.

At minimum it freezes:
- target disease population;
- disease weighting;
- candidate weighting;
- zero-future-event disease policy;
- macro vs micro aggregation;
- outcome observability requirements;
- primary endpoint subtype;
- primary K/review budget and normalized companion metric.

Diseases may not be removed after outcome inspection merely because the chosen metric is undefined when no qualifying future event occurs.

The conditional event-ranking estimand must be accompanied by an all-frame observed-event review-budget utility that includes zero-event diseases without treating non-observation as biological failure.

### 17.5 Multiplicity

The MAP freezes one primary endpoint/subtype, one primary metric, and one primary review budget/K.

Secondary endpoints, cutoffs, subgroups, and sensitivity analyses require a preregistered multiplicity/reporting policy.

---

## 18. Uncertainty contract

Forge Bio does not emit one universal "confidence = 87%" number.

Uncertainty may include:

- predictive
- epistemic
- model-form
- dataset
- identity-mapping
- temporal
- evidence-quality
- evidence-completeness
- contradiction
- applicability
- aleatoric where meaningful

Missing uncertainty is `NOT_ASSESSED` or UNKNOWN, not zero.

Out-of-domain predictions are explicitly marked.

---

## 19. Verification contract

Verification is implementation correctness.

Required categories include:

- temporal invariants
- partial-date rules
- watermark lattice/property tests
- future sentinel tests
- deterministic snapshots
- cryptographic manifest checks
- metric golden tests
- identity mapping invariants
- genomic variant/locus normalization, liftover, allele-orientation, and LD-provenance invariants
- phenotype/cohort/dataset/SampleSet identity invariants
- candidate-universe determinism
- feature and preprocessing-fit lineage completeness
- cross-anchor event-reuse invariants
- ScientificEventFamily deduplication invariants
- provider-lineage/input-outcome coupling audit
- import/dependency wall tests
- holdout access controls
- reproducibility from manifest

Metamorphic requirement:

> Adding an inadmissible post-cutoff source record must not change historical features or rankings.

---

## 20. Validation contract

Validation is scientific adequacy for the intended use.

Eventually includes:

- temporal holdout
- disease holdout
- disease-family holdout
- target-family holdout
- similarity-aware holdout
- independent outcome providers
- source ablations
- multiple cutoffs
- calibration
- applicability analysis
- sealed confirmatory evaluation
- prospective validation

Solver/model agreement is not validation.

---

## 21. MAP contract

A frozen Model Analysis Plan or equivalent study plan contains:

```text
QoI
Context of Use
scientific assumptions
scientific estimand
cutoff
observation horizon
candidate universe
provider versions
temporal policy
identity policy
features
model specification
baselines
discoverability control
endpoint family
primary endpoint subtype
pre-T genetic-state policy
outcome gene-assignment policy
outcome phenotype-match policy
genetic replication policy
historical novelty policy
matching rules
zero-event disease policy
validation generation
Future Outcome snapshot/ledger commitment
primary/secondary metrics
all-frame review-budget utility
dependence-sensitivity method
multiplicity policy
success criteria
uncertainty strategy
planned sensitivity analyses
validation plan
benchmark design provenance
holdout access rules
stop conditions
```

Confirmatory execution must refuse to start if the run configuration does not match the frozen MAP hash.

---

## 22. MAR contract

A Model Analysis Report or equivalent contains:

- MAP ID/hash
- exact code commit
- environment/container identity
- dataset snapshot IDs
- model IDs
- deviations
- verification results
- admissibility statistics
- benchmark results
- confidence intervals
- baseline deltas
- sensitivity analyses
- leakage diagnostics
- calibration/applicability where relevant
- failed analyses
- limitations
- scientific interpretation
- claim maturity level earned

Negative results receive a MAR too.

---

## 23. LLM contract

In strict historical V1:

```text
LLM ranking path = forbidden
```

Later extraction assistants:

- receive explicit documents
- return structured candidate extractions
- provide exact supporting spans
- record model/version
- are independently validated
- cannot create validated scientific truth
- cannot control temporal admission
- cannot access future labels during ranking

---

## 24. Project stop / escalation rules

### Gate A — Data/benchmark viability

If historical provider fidelity is inadequate for a cutoff, move the cutoff or downgrade the study claim.

Do not patch over missing history with modern annotations.

### Gate B — Baseline value

If transparent models do not beat research-attention, evidence-count, and endpoint-appropriate discoverability controls on development data, investigate the scientific premise before adding complexity.

### Gate C — Sealed confirmation

If improvement disappears on the sealed benchmark, the stronger claim is not earned.

### Gate D — Advanced ML

No GNN/multimodal/pretrained-model investment is justified without a credible simpler-baseline foundation.

### Gate E — Drug repurposing

B-REP is promoted only after identity, active-moiety semantics, and drug/target temporal evidence pass the same historical-integrity standards as B-TGT.

---

## 25. Safety boundary

Forge Bio must remain a computational research tool.

It must not generate operational pharmaceutical synthesis protocols, patient medication instructions, or dosing recommendations.

The system ranks hypotheses for qualified scientific investigation; experimental, clinical, and regulatory confirmation remain outside the authority of the platform.


---

## 26. Benchmark V0 scope lock

The first benchmark is intentionally narrow and is defined in [BENCHMARK_V0_SPEC.md](BENCHMARK_V0_SPEC.md).

B-TGT-A1 / B-TGT-E1-v0 predicts **disease–gene association prioritization** and evaluates later independent human genetic support. It does **not** by itself claim therapeutic-target validation, intervention direction, causal target status, clinical efficacy, or treatment success.

The endpoint-quality threshold, H, primary K, success threshold, and coverage thresholds are development-time decisions that must be frozen in the MAP before sealed evaluation.

---

## 27. Provider qualification contract

Historical safety is qualified at:

```text
(provider, release/version, field_or_derivation, intended_use)
```

not at provider-name level.

The full process is defined in [PROVIDER_QUALIFICATION.md](PROVIDER_QUALIFICATION.md), including the Reconstruction Fidelity Study for conditional reconstructed sources.

---

## 28. Identity and hashing contract

Historical identity, evaluation-only modern bridges, deterministic HypothesisKey semantics, CandidateUniverse identity, and canonical serialization are defined in [IDENTITY_POLICY.md](IDENTITY_POLICY.md).

Any artifact used as a cryptographic scientific identity must use canonical serialization and an explicit schema version.

---

## 29. Training contract

Strict supervised learning is allowed through **nested temporal training**, not by attaching future labels to a present-day table.

The normative training rules are defined in [MODEL_TRAINING_POLICY.md](MODEL_TRAINING_POLICY.md).

A model evaluated at T_eval may train on historical anchor challenges t_i only when each training outcome window is fully observable by T_eval under the frozen policy.

---

## 30. Outcome-construction and novelty contract

Temporal cleanliness of model inputs does not guarantee correctness of future labels.

For B-TGT gene-level outcomes:

- locus/variant discovery and gene assignment are distinct;
- modern learned locus-to-gene scores are not unqualified strict-historical ground truth;
- assignment method, evidence, availability, knowledge horizon, and uncertainty are provenance;
- every candidate relevant to novelty has an explicit PreTGeneticState;
- E1-NOVEL-STRICT requires PreTGeneticState = NO_SIGNAL_OBSERVED plus HistoricalNoveltyAudit = NOVEL_CONFIRMED;
- suggestive pre-T genetics followed by stronger post-T evidence is E1-MATURATION, not de novo novelty;
- disease/trait phenotype matching is explicit and risk-factor/surrogate relations are not silently promoted to the primary disease endpoint;
- E1-REPLICATION requires a governed GeneticReplicationAssessment rather than a repeated label;
- unresolved novelty, phenotype match, replication, or assignment becomes AMBIGUOUS/INCONCLUSIVE rather than a rescued positive.

Normative decisions:
- [adr/ADR-006-outcome-gene-assignment.md](adr/ADR-006-outcome-gene-assignment.md)
- [adr/ADR-008-outcome-phenotype-matching.md](adr/ADR-008-outcome-phenotype-matching.md)
- [adr/ADR-009-genetic-replication-and-signal-state.md](adr/ADR-009-genetic-replication-and-signal-state.md)

---

## 31. Researcher-hindsight and adjudication contract

A sealed database does not erase modern biomedical knowledge from researchers.

Confirmatory studies maintain BenchmarkDesignProvenance and:
- separate ranking/model development from outcome adjudication where organizationally possible;
- record researcher exposure to sealed diseases and future outcomes;
- freeze feature families/algorithm/config before sealed outcome reveal;
- keep sealed disease identities hidden from the ranking methodology team for the strongest retrospective claim when operationally possible.

For the **strongest L3 SEALED_CONFIRMATORY tier**, sealed outcome adjudicators must be blinded to model rank/order. If rank/order is visible during sealed adjudication, the tier is automatically downgraded.

A technically sealed benchmark with outcome-aware design may be downgraded to exploratory evidence.

Normative decisions:
- [adr/ADR-007-benchmark-design-provenance.md](adr/ADR-007-benchmark-design-provenance.md)
- [adr/ADR-010-validation-generations-and-outcome-freeze.md](adr/ADR-010-validation-generations-and-outcome-freeze.md)

### 31.1 Validation-generation contract

VALIDATION is versioned into generations.

Each generation records both access count and maximum disclosure level: AGGREGATE_ONLY, SUBGROUP, PER_CASE, or FULL_LABEL.

If validation results materially influence features, model class, endpoint design, hyperparameters, thresholds, disease selection, or candidate selection, that generation becomes SPENT_FOR_MODEL_SELECTION.

A spent generation remains reportable but is not called untouched validation.

### 31.2 Future Outcome commitment contract

For strongest L3, outcome-event discovery/adjudication is frozen before model rank/order is revealed.

Before sealed evaluation, freeze/commit the exact:
- future outcome source releases;
- Future Outcome snapshot/digest;
- outcome-ledger digest;
- ScientificEventFamily ledger digest;
- adjudication-batch digest;
- provider-lineage/input-outcome coupling assessment digest;
- evaluation identity-bridge digest;
- phenotype-match, gene-assignment, and replication policy versions.

Changing these artifacts creates a new evaluation generation rather than silently changing ground truth.

---

## 32. Discoverability and reporting-bias contract

Future biomedical evidence is not assumed to be observed at random.

The benchmark must consider whether later support is driven by:
- research intensity;
- sample-size/statistical-power growth;
- phenotype measurability;
- annotation density;
- funding/study opportunity;
- selective publication/reporting.

Where material, MARs report sensitivity to these processes and compare against a historical discoverability/observation-propensity control.

---

## 33. Population/ancestry applicability contract

Evidence and outcomes retain population/ancestry metadata where scientifically relevant and available.

A result derived from a historically ancestry-skewed evidence base is not silently generalized to populations not adequately represented in the evaluation.

Missing ancestry/applicability information is reported as UNKNOWN or NOT_ASSESSED.

---

## 34. Knowledge-historical vs technology-contemporaneous claims

Forge Bio distinguishes:

```text
KNOWLEDGE_HISTORICAL
    model-visible biomedical knowledge is admissible by T

TECHNOLOGY_CONTEMPORANEOUS
    the complete computational method could realistically have been implemented/run with technology available at T
```

STRICT_HISTORICAL establishes the first property unless a study explicitly evaluates the second.

The platform must not claim "this exact system could have run in year T" merely because its biomedical knowledge watermark is <= T.

---

## 35. Red-team gap authority

[SCIENTIFIC_RED_TEAM_GAPS.md](SCIENTIFIC_RED_TEAM_GAPS.md) records active scientific-integrity blockers discovered by adversarial review.

Any ACTIVE P0 blocker in that register is a hard stop for production scientific implementation unless:
- it is closed with evidence;
- or it is explicitly superseded by an accepted ADR that preserves the intended claim boundary.

---

## 36. Readiness rule

[PRE_CODE_CHECKLIST.md](PRE_CODE_CHECKLIST.md) is the operational go/no-go authority.

This contract becomes FROZEN V1 only when all P0 items are closed or explicitly superseded by ADR.


---

## 37. BIG 0R3 genomic-integrity contract

The following rules are normative before BIG 0F feasibility work:

1. **Canonical genomic identity** — variants/loci use explicit reference sequence/assembly and normalized alleles. rsIDs are external identifiers, not identity.
2. **Harmonization provenance** — liftover, strand resolution, allele normalization, and reference-panel/LD derivations are provenance-bearing artifacts with watermarks.
3. **LD context** — LD proxy equivalence requires population/ancestry, reference panel/release, assembly, metric, threshold, and derivation method.
4. **Coverage-gated strict novelty** — E1-NOVEL-STRICT requires a MAP-frozen minimum HistoricalGeneticSearchCoverage grade.
5. **Historical observability sensitivity** — identity eligibility is separate from genetic measurability at T; a preregistered GeneticObservabilityAtT sensitivity is required.
6. **Canonical cohort/sample lineage** — Cohort/Dataset/Biobank/Consortium/SampleSet identities replace free-text independence assertions.
7. **Scientific event identity** — multiple manifestations of one discovery form one ScientificEventFamily; V0 grants at most one primary event credit per family.
8. **Source coupling** — Past input and Future outcome providers declare shared upstream/curation lineage; material coupling requires ablation/external-source sensitivity.
9. **Cross-anchor reuse** — one ScientificEventFamily cannot receive uncontrolled repeated training weight across overlapping historical anchors.
10. **Mode separation** — ScientificOperatingMode and HistoricalDataPolicy are orthogonal configuration axes.

Normative decisions:
- [adr/ADR-011-genomic-identity-harmonization.md](adr/ADR-011-genomic-identity-harmonization.md)
- [adr/ADR-012-historical-genetic-observability.md](adr/ADR-012-historical-genetic-observability.md)
- [adr/ADR-013-event-identity-source-coupling.md](adr/ADR-013-event-identity-source-coupling.md)
- [adr/ADR-014-operating-mode-data-policy.md](adr/ADR-014-operating-mode-data-policy.md)

These policies must be represented in the QoI/MAP/MAR artifacts and their executable JSON Schemas.


---

## 38. Forge Bio Scientific Twin contract

"Forge Bio Scientific Twin" is a project-defined research construct. It must not be represented as a patient/clinical health digital twin merely by terminology.

### 38.1 Profile vs twin

```text
Scientific Profile
    !=
Validated Predictive Twin
```

T0_PROFILE_ONLY is a profile maturity state and is not called a digital twin in scientific claims.

### 38.2 Twin maturity is not claim maturity

```text
DigitalTwinMaturityLevel
    !=
ClaimMaturityLevel
```

For example:
- T3_VALIDATED_PREDICTIVE_TWIN does not automatically imply L3_SEALED_CONFIRMATORY;
- L3 sealed benchmark confirmation does not automatically imply T3 twin maturity.

Both ladders must be satisfied independently for any combined claim.

### 38.3 Historical twin contract

STRICT_HISTORICAL and HISTORICAL_INPUT_MODERN_PRIOR twins require an explicit cutoff T.

The transitive watermark includes:
- profile/evidence snapshots;
- identity/mapping artifacts;
- state-variable definitions;
- state-model structure/topology;
- transition/mechanism rules;
- update-policy artifact;
- parameter artifacts;
- preprocessing/feature artifacts;
- pretrained representations;
- manually selected biomedical priors.

A state model designed later may not inherit an old watermark merely because its numeric parameters were fit on old data.

### 38.4 Dependency isolation

Historical twin construction cannot read:
- FutureEvent/outcome storage;
- lockbox outcomes;
- evaluation-only identity bridges;
- future validation labels/results;
- unrestricted current/latest biomedical providers.

Prediction/simulation output is not EvidenceRecord.

### 38.5 T3 validation contract

T3 requires the platform's existing validation governance:
- frozen prediction target/horizon;
- MAP;
- MAR;
- ValidationGeneration provenance;
- BenchmarkDesignProvenance;
- held-out/future evaluation;
- uncertainty evaluation;
- applicability/OOD evaluation;
- failure analysis.

A model that only reproduces fit/training data remains at most T2.

### 38.6 T4 intervention-simulation contract

T4 additionally requires:
- CausalAssumptionSet;
- InterventionSemantics;
- IdentifiabilityStatus;
- perturbation artifacts;
- sensitivity artifacts;
- uncertainty propagation.

A favorable associational perturbation is not a causal intervention effect.

Allowed maturity-supporting identifiability states are:
- IDENTIFIED;
- PARTIALLY_IDENTIFIED;
- ASSUMPTION_DEPENDENT.

NOT_IDENTIFIED or UNKNOWN cannot support T4.

### 38.7 Clinical claim boundary

Twin simulation output is a research hypothesis.

It does not by itself establish:
- therapeutic efficacy;
- safety;
- patient-specific treatment choice;
- dose;
- clinical utility.

Patient-specific digital twins require a separate future Context of Use.

Normative documents:
- [DISEASE_PATHOGEN_THERAPEUTIC_PROFILE.md](DISEASE_PATHOGEN_THERAPEUTIC_PROFILE.md)
- [SCIENTIFIC_DIGITAL_TWIN_ARCHITECTURE.md](SCIENTIFIC_DIGITAL_TWIN_ARCHITECTURE.md)
- [adr/ADR-015-scientific-digital-twin-semantics.md](adr/ADR-015-scientific-digital-twin-semantics.md)
