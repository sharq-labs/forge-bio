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

V1 is not intended for:

- patient diagnosis
- patient-specific treatment selection
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

> Given only publicly available biomedical evidence admissible by cutoff T, can Forge Bio prioritize disease-specific therapeutic target hypotheses that later reach endpoint E within horizon H, with positive lift over historical research-attention baselines?

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
- support historical model-visible mappings
- isolate modern evaluation mappings from historical feature generation

A mapping with ambiguity is not silently coerced to EXACT.

---

## 13. Ground-truth contract

Ground truth is an event ledger.

A future event counts as independent only when its lineage satisfies the benchmark's independence rule. A later annotation that merely re-curates pre-cutoff evidence is not automatically independent validation.

Distinct publications or databases are not sufficient proof of independence. Where relevant, outcome lineage must retain cohort, consortium, dataset/biobank, meta-analysis parents, and participant-overlap state. UNKNOWN sample overlap is not interpreted as independent replication.

For gene-level genetic outcomes, identity reconciliation and causal-gene assignment are separate operations. A modern identity bridge may reconcile identifiers, but it may not create a gene-level validation from a locus/variant event without passing the governed OutcomeGeneAssignmentPolicy.

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

- cutoff
- candidate universe
- disease universe
- provider releases
- temporal policy
- identity policy
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
- candidate-universe determinism
- feature lineage completeness
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
outcome gene-assignment policy
historical novelty policy
matching rules
zero-event disease policy
primary/secondary metrics
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

If transparent models do not beat research-attention/evidence-count baselines on development data, investigate the scientific premise before adding complexity.

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

B-TGT-E1-v0 predicts disease–gene target-association prioritization and evaluates later independent human genetic support. It does **not** claim to validate intervention direction, clinical efficacy, or treatment success.

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
- E1-NOVEL requires an independent HistoricalNoveltyAudit;
- unresolved novelty or assignment becomes AMBIGUOUS, not a rescued positive.

Normative decision: [adr/ADR-006-outcome-gene-assignment.md](adr/ADR-006-outcome-gene-assignment.md).

---

## 31. Researcher-hindsight and adjudication contract

A sealed database does not erase modern biomedical knowledge from researchers.

Confirmatory studies therefore maintain BenchmarkDesignProvenance and, where feasible:

- separate ranking/model development from outcome adjudication;
- blind outcome adjudicators to model rank/order;
- record researcher exposure to sealed diseases and future outcomes;
- freeze feature families/algorithm/config before sealed outcome reveal;
- keep sealed disease identities hidden from the ranking methodology team for the strongest retrospective claim.

A technically sealed benchmark with outcome-aware design may be downgraded to exploratory evidence.

Normative decision: [adr/ADR-007-benchmark-design-provenance.md](adr/ADR-007-benchmark-design-provenance.md).

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
