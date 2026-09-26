# Plan Strength Audit — Pre-Code V1

**Status:** REVISED AFTER INDEPENDENT HOSTILE REVIEW  
**Current phase:** BIG 0F-0 critical-path hardening  
**Scope:** whether the B-TGT-E1 plan is strong enough to justify BIG 0F and later confirmatory implementation

## 1. Correction to the previous audit

The previous audit concluded that no major known architecture/specification gap remained.

That conclusion was too strong.

An independent hostile review identified claim-relevant gaps in the E1 critical path that broad architecture work had not closed:

- gene-label attention circularity;
- missing genomic-architecture / pleiotropy nuisance controls;
- use of the strongest single baseline instead of a combined nuisance comparator;
- no numeric confirmatory decision rule / MDE / power target;
- research-program multiplicity across repeated confirmatory generations;
- insufficient role independence for strongest-tier claims;
- schemas that enforced field presence but not key scientific cross-field invariants;
- incomplete BIG 0F sampling/adjudication/contamination protocol.

The prior "no known major gap" statement is therefore **withdrawn**.

## 2. Current score policy

Forge Bio will not self-award a higher scientific-plan score after self-authored fixes.

The latest independent hostile assessment is **Round 2** and is treated as the reference external assessment:

```text
Scientific plan strength: 5.5/10
Current empirical evidence strength: 0/10
Readiness to start BIG 0F: 4/10
```

Those values describe the exact pre-closure state reviewed in Round 2. The project does not self-award a higher score after implementing the Round 2 patch.

The project is re-scored only after:
1. BIG 0F-0 is complete;
2. hostile-review regression probes pass;
3. a fresh independent review examines the new state.

## 3. What determines scientific value

The core question is no longer phrased as:

> Can Forge Bio beat attention?

The stronger question is:

> Does pre-T biological information add reproducible predictive value over a combined as-of-T nuisance model containing research attention, genomic architecture, cross-trait pleiotropy, historical observability, and measurement/discoverability opportunity?

A positive result against random or a single popularity baseline is insufficient.

## 4. Critical-path audit

| Domain | Current status | Required evidence |
|---|---|---|
| Research question / falsifiability | STRONG DESIGN | frozen endpoint + confirmatory rule |
| Historical temporal semantics | STRONG POLICY | hostile watermark tests + provider audit |
| Primary future outcome | HARDENING | high-specificity assignment or locus redesign |
| Gene-label attention circularity | BIG 0F-0 POLICY FIXED / EMPIRICAL OPEN | assignment-attention audit |
| Genomic architecture nuisance | BIG 0F-0 POLICY FIXED / DATA OPEN | historical nuisance features |
| Cross-trait pleiotropy nuisance | BIG 0F-0 POLICY FIXED / DATA OPEN | historical pleiotropy feature |
| Primary comparator | FIXED IN POLICY | Combined Nuisance Model |
| Confirmatory statistics | BIG 0F-0 HARDENING | alpha/MDE/power after pilot counts |
| Research-program multiplicity | BIG 0F-0 HARDENING | ConfirmatoryProgramBudget |
| Disease sampling hindsight | POLICY FIXED / SEAL OPEN | deterministic T/H ordering + sealed frame/random seed |
| Independent adjudication | OPERATIONAL OPEN | second reviewer |
| Lockbox custody independence | OPERATIONAL OPEN | dual-seal mechanism identified; independent custodian + dry run still required |
| Schema scientific invariants | PASS-TEST | hostile regression suite passes in CI |
| Historical provider availability | EMPIRICAL OPEN | mini provider audit |
| Ground-truth ambiguity | EMPIRICAL OPEN | BIG 0F |
| Nuisance-model headroom | EMPIRICAL OPEN | development-only pilot analysis |
| Confirmatory power | EMPIRICAL OPEN | simulation-based analysis |
| Branch protection | OPERATIONAL OPEN | GitHub Issue #2 |
| Scientific result | NOT TESTED | no model benchmark result exists |

## 5. BIG 0F-0 completion criteria

BIG 0F cannot begin until all of the following are true:

- primary gene-assignment eligibility is frozen for the pilot;
- author-named/nearest-gene labels are non-primary unless independently high-specificity;
- Combined Nuisance families are frozen;
- pilot disease/event sampling rule is frozen;
- pilot target N rule is frozen;
- second-adjudication plan is frozen or the reduced claim ceiling is accepted;
- pilot cases are permanently DEVELOPMENT_EXPOSED;
- symmetric non-event audit sampling is frozen;
- mini provider-availability audit procedure is frozen;
- numeric GO / REDESIGN / NO-GO threshold categories are sealed before adjudication;
- confirmatory alpha / MDE / power workflow is defined;
- confirmatory-generation multiplicity budget is defined;
- hostile schema/invariant probes all fail as intended.

## 6. BIG 0F must answer

BIG 0F is successful only if it establishes that a confirmatory benchmark appears constructible.

It must quantify:

- event count per disease/subtype;
- high-specificity gene-assignment yield;
- author-named / nearest-gene dependence;
- attention correlation by assignment class;
- phenotype ambiguity;
- novelty ambiguity;
- historical-search coverage;
- pre-T cohort reuse in post-T events;
- variant/liftover/allele ambiguity;
- event-family duplication;
- locus-to-many-gene sensitivity;
- provider coupling;
- cohort/sample-overlap ambiguity;
- retrospective-curation burden;
- ancestry metadata coverage;
- independent adjudicator agreement;
- symmetric non-event audit burden;
- archived provider field availability;
- Combined Nuisance headroom;
- inputs for simulation-based confirmatory power.

## 7. What "100%" means

There is no defensible claim that a research plan is literally 100% complete or free from unknown unknowns.

The strongest acceptable pre-code statement is:

> all currently known claim-invalidating design risks have been either closed by enforceable protocol/invariants or converted into explicit BIG 0F empirical gates, and an independent reviewer finds no unresolved P0 design defect.

That statement has **not yet been earned**.

## 8. Current conclusion

Forge Bio remains scientifically interesting and potentially high-value, but is not yet ready for BIG 0F.

The project is currently in **critical-path repair**, not final architecture completion.

Do not add more Digital Twin / pathogen / therapeutic complexity until the B-TGT-E1 critical path passes BIG 0F and demonstrates that biological signal could exist beyond the Combined Nuisance Model.

The next score must come from an independent re-review, not from the project author.


## 9. Sharp consistency pass after BIG 0F-0

A post-hardening consistency pass found four additional degrees of freedom and closed them at policy level:

1. **Cutoff/horizon selection order** — candidate T/H ordering is now deterministic and sealed; no post-hoc choice from the 2005–2014 / 3–10y grid.
2. **Pilot threshold semantics** — field-availability denominator, critical-field behavior, agreement-statistic choice, and threshold sensitivity are explicit.
3. **Comparator-capacity confounding** — nuisance-only and nuisance+evidence arms use the same learner/tuning/search budget in the primary nested comparison.
4. **External seal ambiguity** — the operational candidate is a dual seal using an independent timestamp proof plus an OSF research registration; dry-run verification and independent custody remain open.

These closures do not raise the project score automatically. They reduce known design degrees of freedom before independent re-review.


## 10. Operational-prep closure

After critical-path design hardening, the remaining transition risk was that BIG 0F execution could still be manual and mutable.

The operational-prep layer therefore adds:
- a machine-readable structure-frozen estimand distinct from the final confirmatory instance;
- a machine-readable endpoint-quality rule whose values remain empirical-open until provider audit;
- deterministic seal-bundle hashing and seed commitment;
- one-byte tamper detection;
- a machine-readable pilot-result artifact;
- deterministic GO / REDESIGN / NO_GO evaluation.

These tools do not close human-independence or external-registration gates.

The following remain genuinely external/empirical:
- independent second adjudicator;
- independent custodian;
- external OpenTimestamps/OSF dry run and real seal;
- manual provider/outcome pilot;
- final endpoint-quality values;
- exact confirmatory estimand instance;
- BIG 0F empirical measurements and decision.


## 11. Round 2 bounded closure

Round 2 did **not** justify another architecture phase. It identified a bounded enforcement/specification patch before empirical work.

The closure patch therefore focuses only on:
- mandatory disease-specific content-free attention volume/momentum;
- fail-closed BIG 0F decision evaluation;
- sealing decision-critical code/schema/manifests;
- post-frame-seal public randomness;
- frozen hypothesis-free primary ascertainment;
- nuisance-only pilot diagnostics;
- one canonical research-program alpha budget;
- executable endpoint-quality rules.

Advanced Digital Twin / Pathogen / Therapeutic work remains frozen/deferred.

The next independent score must come from a fresh hostile re-review of the merged state, not from this document.
