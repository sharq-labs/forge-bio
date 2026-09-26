# BIG 0F False-GO Closure Plan

**Status:** PRE-CODE NORMATIVE PLAN  
**Scope:** close the Round 2 false-GO attack surface before any runtime implementation or BIG 0F adjudication  
**Implementation rule:** this document defines contracts and scientific decision semantics only. It does not authorize implementation code.

---

## 1. Purpose

BIG 0F may start only when a future implementation can make every claim-valid decision from sealed, reconstructable evidence rather than from study-authored summary claims.

The design must fail closed whenever a required provenance chain, selection reconstruction, external authority check, nuisance execution binding, or power-input derivation cannot be independently reconstructed.

This plan closes the currently known false-GO classes without opening another unrestricted architecture round.

---

## 2. Closure principles

1. **No self-attested GO-critical fact.** A scalar such as LOW provider coupling, ADEQUATE ancestry metadata, VERIFIED external seal, or a favorable power SD cannot be sufficient by itself.
2. **Selection must be reconstructable.** Cutoff/horizon, disease expansion, and capped-event selection must be derivable from frozen inputs and deterministic rules.
3. **Pilot biological performance stays hidden.** BIG 0F remains NUISANCE_ONLY. No biological-arm lift may be used to choose thresholds, variance assumptions, endpoint subtype, disease sample, or comparator.
4. **Power uncertainty is explicit.** A single analyst-supplied disease-level SD is prohibited.
5. **Comparator identity is executable in principle.** The eventual fitted nuisance model must be bound to the exact frozen nuisance manifest, source releases, transforms, preprocessing, tuning budget, and output ranks.
6. **External trust must actually be external.** A JSON field saying VERIFIED is not sufficient evidence of a timestamp, public registration, or randomness beacon.
7. **Program history is monotonic.** Failed or spent confirmatory attempts cannot disappear by creating a fresh ledger.
8. **One normative rule per scientific decision.** Duplicate endpoint/decision implementations may not define competing semantics.

---

## 3. P0 — Event-bearing disease diversity

### Problem

A pilot can meet the total event-count threshold while nearly all events come from a very small number of diseases. That can create a false impression that the benchmark is broadly constructible.

### Frozen rule

The pilot result must report:

- total selected disease count;
- event-bearing disease count;
- event-bearing disease fraction;
- per-disease event counts.

The event-bearing disease fraction is:

```text
event_bearing_disease_count / disease_count
```

A claim-valid GO requires the fraction to meet the sealed `min_event_bearing_disease_fraction` threshold.

Threshold-sensitivity variants must vary this gate together with the other frozen thresholds. If the final decision changes under a sealed plausible variant, the outcome is REDESIGN rather than selective threshold choice.

### Failure semantics

- missing/inconsistent per-disease counts -> INCONCLUSIVE;
- fraction below the base GO requirement -> REDESIGN;
- decision instability across sealed sensitivity variants -> REDESIGN.

---

## 4. P0 — Cutoff/horizon first-passing rule

### Problem

A later cutoff/horizon pair can be chosen because it produces a more favorable pilot even though an earlier pair already passed the preregistered feasibility criteria.

### Required selection-provenance artifact

For every candidate cutoff/horizon pair in the frozen lexicographic order, record only the preregistered feasibility inputs:

- provider-availability pass/fail;
- observation-window pass/fail;
- raw candidate-event feasibility count;
- overall feasibility pass/fail;
- immutable evidence/provenance references.

The chosen pair must equal the **first passing pair** in that ledger.

No ambiguity rate, nuisance performance, biological rank, assignment quality, or downstream result may participate in pair selection.

### Failure semantics

- chosen pair is not the first passing pair -> INVALID pilot / REDESIGN;
- earlier pair evidence missing -> INCONCLUSIVE;
- pair feasibility was recomputed after outcome inspection under changed rules -> protocol spent; new pilot version required.

---

## 5. P0 — Disease sample expansion 12 -> 15

### Problem

The study can expand beyond the first 12 sampled diseases in a favorable direction unless the expansion trigger is reconstructable.

### Frozen rule

Disease order is immutable after the externally sealed frame and randomness event.

The first 12 diseases are always the initial pilot sample.

Expansion to disease 13, 14, or 15 is permitted only while the cumulative raw candidate-event count from the already included prefix remains below the frozen minimum event count.

Expansion stops at the earliest prefix that reaches the minimum, or at 15 diseases.

The decision uses event availability only. It must not inspect ambiguity, assignment class, nuisance rank, biological rank, curation difficulty, or downstream agreement.

### Required provenance

Record cumulative event counts for prefixes 12, 13, 14, and 15 as applicable, with the immutable ordered disease IDs and source evidence.

### Failure semantics

Any non-prefix disease inclusion, unnecessary expansion after the threshold was already reached, or outcome-aware expansion invalidates the pilot selection.

---

## 6. P0 — More than 150 candidate events

### Problem

A favorable subset of 150 events can be selected from a larger raw event universe.

### Frozen rule

The complete pre-cap event universe is first serialized and committed.

If the raw count is <=150, retain all events.

If the raw count is >150:

1. preserve at least one event from each event-bearing disease where mathematically feasible;
2. select remaining slots by deterministic keyed ordering from the same sealed randomness domain;
3. never use assignment quality, ambiguity, rank, effect direction, publication prestige, or curation difficulty in event selection;
4. record the raw-universe digest, selected-event IDs, per-disease raw counts, and per-disease selected counts.

A future evaluator must be able to reconstruct the exact 150 IDs from the committed raw universe and frozen rule.

### Failure semantics

Unreconstructable or outcome-aware capped-event selection -> INVALID pilot / REDESIGN.

---

## 7. P0 — Power-input provenance and variance uncertainty

### Problem

A freely supplied disease-level SD can make a weak design appear adequately powered.

BIG 0F also cannot legitimately estimate the variance of biological incremental lift by secretly running the biological arm, because the pilot is NUISANCE_ONLY.

### Frozen design

A single analyst-entered SD is prohibited.

Before adjudication, a **Power Input Derivation Contract** must define:

- which pilot-safe quantities may enter power planning;
- which independent external/development quantities may enter;
- the deterministic transforms applied to them;
- the allowed variance/dependence scenario family;
- the conservative primary planning scenario;
- the sensitivity scenarios;
- the rule for clustered/dependent events;
- the rule for zero-event diseases;
- how many untouched confirmatory diseases are actually available.

The contract may use nuisance-only and structural pilot outputs, but it may not use observed biological-model lift.

The primary confirmatory design must achieve target power under the sealed conservative planning scenario. If scientifically plausible sealed variance/dependence scenarios produce materially different feasibility conclusions, BIG 0F returns REDESIGN or INCONCLUSIVE rather than selecting the favorable scenario.

### Required future artifact

A power-analysis artifact must bind:

- derivation-contract digest;
- raw input artifact digests;
- derived planning quantities;
- dependence assumptions;
- scenario family;
- target effect and alpha;
- required disease count under every sealed scenario.

### Failure semantics

Free scalar SD, missing derivation provenance, or post-result scenario choice -> INCONCLUSIVE/REDESIGN and no GO.

---

## 8. P1 — Bind actual nuisance execution to the frozen manifest

### Problem

A nuisance manifest can name a strong comparator while the model actually executed uses fewer/weaker nuisance features.

### Required Nuisance Execution Artifact

The eventual nuisance run must bind:

- nuisance-manifest digest;
- exact mandatory feature-family IDs;
- source/provider release IDs;
- historical cutoff and admissibility status;
- feature construction/transformation definitions;
- preprocessing identity;
- learner/model-family identity;
- hyperparameter search space;
- tuning budget;
- early-stopping rule;
- random-seed policy;
- candidate-universe digest;
- fitted-model artifact digest;
- per-candidate rank-output digest;
- pilot summary metrics derived from those exact ranks.

All mandatory families in the frozen manifest must be present. Extra semantic biological evidence is prohibited in BIG 0F.

Reported nuisance headroom metrics must be reproducible from the committed rank output.

### Failure semantics

Missing mandatory family, mismatched model/output digest, or unreconstructable summary metric -> INCONCLUSIVE; intentional substitution after seeing results -> REDESIGN.

---

## 9. P0/P1 — External seal and randomness trust root

### Problem

A study-authored artifact can claim that an external timestamp, public registration, or beacon was VERIFIED without independently proving it.

### Frozen trust rule

Claim-valid verification must use evidence that is independently retrievable or cryptographically verifiable outside the study repository.

For OpenTimestamps:
- preserve the exact proof artifact;
- verify the proof against the exact committed bytes/digest using the official/protocol-compatible verification path;
- record the independently verified timestamp result.

For public preregistration:
- independently retrieve the registry record;
- verify the exact committed digest/content identity and registration time;
- preserve the registry identifier and retrieval evidence.

For DRAND or equivalent public randomness:
- independently retrieve the stated round;
- verify round identity, publication time, randomness, and the service's authenticity/signature mechanism;
- verify that it is the first eligible round after the frame seal under the frozen rule.

A local `verification_status=VERIFIED` field is metadata only and cannot establish trust.

### Failure semantics

If independent verification cannot be performed, the artifact remains UNVERIFIED and cannot support BIG 0F GO.

---

## 10. P1 — Provider, ancestry, curation, and adjudicator evidence binding

### Problem

GO-critical states can collapse rich evidence into self-declared scalars or IDs.

### Provider Audit Artifact

Must contain the frozen source-family/field matrix with, per cell:

- historical release obtainable;
- version/release identity;
- field existed at T;
- retrospective-curation flag;
- mapping requirement;
- access/license constraint;
- coverage state;
- criticality;
- evidence/provenance reference.

The required-field availability fraction must be recomputable from this matrix.

### Applicability Artifact

Ancestry/population adequacy must bind to:
- coverage numerator/denominator;
- population metadata source;
- unknown/missing rate;
- predefined adequacy rule;
- evidence digest.

### Curation Burden Artifact

Must bind event and non-event case-level timing/audit records used to derive burden summaries.

### Second-adjudicator Independence Artifact

Must bind:
- adjudicator role identity;
- role-registry snapshot;
- conflict/independence evidence;
- blinding commitments;
- assignment time;
- artifact digest.

### Failure semantics

A summary state that cannot be regenerated from its evidence artifact is INCONCLUSIVE and cannot be GO.

---

## 11. P1 — Append-only confirmatory program history

### Problem

A fresh ledger could omit earlier failed/spent attempts and recreate an apparently unused alpha budget.

### Frozen ledger rule

Every ResearchProgramAttempt ledger revision must contain:

- monotonic sequence number;
- previous-ledger digest;
- complete cumulative attempt IDs;
- cumulative alpha spent;
- generation state transitions;
- timestamp/registration reference.

A new ledger head must extend the previous externally anchored head. It may correct metadata through an explicit correction event, but may not delete or renumber prior attempts.

At material milestones, the current ledger-head digest is externally timestamped/registered.

Renaming benchmark, endpoint, model, or generation does not create a new research-program budget.

### Failure semantics

Broken chain, missing prior head, or unexplained attempt disappearance -> confirmatory claim invalid until reconciled.

---

## 12. P2 — One canonical endpoint decision source

### Problem

Multiple endpoint validators can silently diverge on field names or allowed states.

### Frozen rule

There is one normative endpoint-quality contract and one canonical decision semantics definition.

Future code may have adapters/wrappers, but every adapter must call the same normative implementation and may not redefine field semantics.

Any material change to endpoint criteria creates a versioned endpoint rule and spends the affected sealed design when required by the lifecycle policy.

---

## 13. P2 — Threshold provenance and digest hygiene

Every GO-critical numeric threshold must have:

- threshold ID;
- exact metric definition;
- direction;
- value;
- scientific/operational rationale;
- sensitivity range;
- decision consequence;
- freeze time/version.

Zero/self-placeholder digests are not claim-valid evidence. Claim-valid artifact digests are computed externally over the exact serialized artifact and committed by the seal bundle/registry process.

---

## 14. P2 — Gene-level robustness

Primary high-specificity gene labels remain the V0 design, but every confirmatory analysis must preserve a locus-level one-credit sensitivity where gene assignment can be method- or attention-dependent.

If the headline conclusion materially changes under the preregistered locus-level sensitivity or under removal of attention-sensitive assignment classes, the result is reported as fragile and cannot be presented as robust gene-level discovery value.

---

## 15. BIG 0F start gate after this planning round

Architecture hardening stops after the contracts above are frozen.

Before actual BIG 0F adjudication, all of the following must be true:

- selection provenance contract frozen;
- event-bearing disease gate frozen;
- Power Input Derivation Contract frozen;
- Nuisance Execution Artifact contract frozen;
- external timestamp/registry/beacon verification procedure frozen and dry-run successfully;
- provider/applicability/curation/adjudicator evidence artifacts frozen;
- append-only research-program ledger contract frozen;
- canonical endpoint decision semantics identified;
- hostile false-GO cases are preserved as mandatory future regression-test requirements;
- independent second adjudicator and external seal process are operationally available.

No runtime implementation is authorized by this document. Implementation begins only after the pre-code gate is explicitly passed.

---

## 16. Stop rule

After these closures receive one final hostile scientific review, do not open another broad architecture round unless that review identifies a new P0 threat capable of producing a false confirmatory claim.

The next phase is then implementation of the frozen contracts, followed by BIG 0F empirical work.
