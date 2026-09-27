# Plan Strength Audit — Pre-Code V1

**Status:** REVISED AFTER INDEPENDENT HOSTILE REVIEW; aligned with ADR-022  
**Current phase:** 0. SPEC FREEZE ([ADR-022](adr/ADR-022-final-scientific-consistency-closure.md) §6: SPEC FREEZE → minimal pre-BIG 0F verification harness → BIG 0F → core)  
**Scope:** whether the B-TGT-E1 plan is strong enough to justify BIG 0F and later confirmatory implementation  
**Precedence:** [V0_FREEZE_STATEMENT.md](V0_FREEZE_STATEMENT.md) wins where this audit disagrees with it. Status labels follow ADR-022 D15: SPEC-CLOSED / IMPLEMENTATION-PENDING; no check is machine-enforced until the harness exists.

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
2. hostile-review regression probes pass in the minimal pre-BIG 0F verification harness (INV-* checks; ADR-022 §6, phase 1);
3. an independent reviewer examines the new state. After ADR-022 that examination is the targeted consistency attack on D1–D19, not a new open review (ADR-022 §9).

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
| Primary future outcome | SPEC-CLOSED (ADR-022 D7) / EMPIRICAL OPEN | high-specificity assignment under adjudication policy v2; locus-level primary credit is a V1 redesign only (Freeze Statement §4) |
| Gene-label attention circularity | BIG 0F-0 POLICY FIXED / EMPIRICAL OPEN | assignment-attention audit |
| Genomic architecture nuisance | BIG 0F-0 POLICY FIXED / DATA OPEN | historical nuisance features |
| Cross-trait pleiotropy nuisance | BIG 0F-0 POLICY FIXED / DATA OPEN | historical pleiotropy feature |
| Primary comparator | FIXED IN POLICY | Combined Nuisance Model |
| Confirmatory statistics | SPEC-CLOSED (ADR-022 D18) | α, planning effect, power, test and success rule fixed now (Freeze Statement §1, §3); not "after pilot counts" |
| Research-program multiplicity | SPEC-CLOSED (ADR-022 D16) / IMPLEMENTATION-PENDING | ConfirmatoryProgramBudget; ledger invariants INV-L1–L9 in the harness |
| Disease sampling hindsight | SPEC-CLOSED (ADR-022 D6, D12, D13) / SEAL OPEN | mechanical frame rule, custodian T/H predicates, pinned drand round pre-declared in S4; S1/S4/S6 seals |
| Independent adjudication | OPERATIONAL OPEN | second reviewer |
| Lockbox custody independence | OPERATIONAL OPEN | dual-seal mechanism identified; independent selection custodian (ADR-022 D12) + external-seal dry run still required |
| Schema scientific invariants | SPEC-CLOSED / IMPLEMENTATION-PENDING | SEMANTIC_INVARIANTS.md checks implemented in the verification harness (ADR-022 §6, phase 1); no code, test suite or CI exists (D15) |
| Historical provider availability | EMPIRICAL OPEN | mini provider audit |
| Ground-truth ambiguity | EMPIRICAL OPEN | BIG 0F |
| Nuisance-model headroom | EMPIRICAL OPEN | development-only pilot analysis |
| Confirmatory power | EMPIRICAL OPEN (method SPEC-CLOSED, ADR-022 D10) | Stage A pool-sufficiency screen in BIG 0F; Stage B DLVS before the confirmatory seal |
| Branch protection | OPERATIONAL OPEN | GitHub Issue #2 |
| Scientific result | NOT TESTED | no model benchmark result exists |

## 5. BIG 0F-0 completion criteria

BIG 0F cannot begin until all of the following are true. The binding entry gate is ADR-022 §6 and §9; this list must agree with it.

- primary gene-assignment eligibility is frozen for the pilot (adjudication policy v2, ADR-022 D7);
- author-named/nearest-gene labels are non-primary unless independently high-specificity;
- Combined Nuisance families are frozen (14 families, manifest v2, ADR-022 D11);
- pilot disease/event sampling rule is frozen (BIG_0F_SELECTION_CUSTODY.md §7–§8);
- pilot target N rule is frozen;
- an independent second adjudicator is in place (ADR-022 §9). Superseded: the former "or the reduced claim ceiling is accepted" alternative;
- an independent selection custodian is in place (ADR-022 D12, §9);
- pilot cases are permanently DEVELOPMENT_EXPOSED, as scoped by BIG_0F_SELECTION_CUSTODY.md §4–§5;
- symmetric non-event audit sampling is frozen;
- mini provider-availability audit procedure is frozen;
- numeric GO / REDESIGN / NO-GO thresholds (threshold manifest v2) are sealed at S1 before adjudication;
- confirmatory α, planning effect and power are fixed and the power workflow is defined (Freeze Statement §1; ADR-022 D10);
- confirmatory-generation multiplicity budget is defined;
- the minimal pre-BIG 0F verification harness is complete, and the hostile schema/invariant probes all fail as intended in it (ADR-022 §6, phase 1);
- an external-seal dry run has succeeded (ADR-022 §9).

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
- the Stage A pool-sufficiency screen inputs ([BIG_0F_POWER_AND_VARIANCE_POLICY.md](BIG_0F_POWER_AND_VARIANCE_POLICY.md) §2). The Stage B planning variance comes from the DLVS, not from BIG 0F.

## 7. What "100%" means

There is no defensible claim that a research plan is literally 100% complete or free from unknown unknowns.

The strongest acceptable pre-code statement is:

> all currently known claim-invalidating design risks have been either closed by enforceable protocol/invariants or converted into explicit BIG 0F empirical gates, and an independent reviewer finds no unresolved P0 design defect.

That statement has **not yet been earned**.

## 8. Current conclusion

Forge Bio remains scientifically interesting and potentially high-value, but is not yet ready for BIG 0F.

The project is currently in **critical-path repair**, not final architecture completion.

Do not add more Digital Twin / pathogen / therapeutic complexity until the B-TGT-E1 critical path passes BIG 0F and demonstrates that biological signal could exist beyond the Combined Nuisance Model.

The next score must come from an independent re-review, not from the project author. After ADR-022 that re-review is the targeted consistency attack on D1–D19 (ADR-022 §9).


## 9. Sharp consistency pass after BIG 0F-0

A post-hardening consistency pass found four additional degrees of freedom and closed them at policy level:

1. **Cutoff/horizon selection order** — candidate T/H ordering is now deterministic and sealed; no post-hoc choice from the 2005–2014 / 3–10y grid. The independent selection custodian now computes the frozen predicates (ADR-022 D12).
2. **Pilot threshold semantics** — field-availability denominator, critical-field behavior, agreement-statistic choice, and threshold sensitivity are explicit. The agreement statistic is Gwet AC1 (ADR-022 D8); thresholds are in manifest v2 (D9).
3. **Comparator-capacity confounding** — nuisance-only and nuisance+evidence arms use the same learner/tuning/search budget in the primary nested comparison, plus the K = 19 permuted-biology placebo guard (ADR-022 D11).
4. **External seal ambiguity** — the operational candidate is a dual seal using an independent timestamp proof plus an OSF research registration, with one authoritative seal_time (ADR-022 §5, D13); dry-run verification and independent custody remain open.

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

Status after ADR-022: each item above is SPEC-CLOSED / IMPLEMENTATION-PENDING. The code and tests that implemented them were removed, and they are rebuilt in the minimal pre-BIG 0F verification harness (ADR-022 D15, §6).

The following remain genuinely external/empirical:
- independent second adjudicator;
- independent selection custodian (ADR-022 D12);
- external OpenTimestamps/OSF dry run and real seal;
- BIG 0F provider/outcome adjudication (the manual pilot is BIG 0F, ADR-022 D14);
- final endpoint-quality values (equal to or stricter than adjudication policy v2, ADR-022 D7);
- (T\*, H\*) values, produced by the custodian's first-passing-pair rule; subtype and metric are already fixed (Freeze Statement §1–§2);
- BIG 0F empirical measurements and decision.


## 11. Round 2 bounded closure

Round 2 did **not** justify another architecture phase. It identified a bounded enforcement/specification patch before empirical work.

The closure patch therefore focuses only on:
- mandatory disease-specific content-free attention volume/momentum;
- fail-closed BIG 0F decision evaluation;
- sealing decision-critical code/schema/manifests;
- post-frame-seal public randomness (superseded by ADR-022 D13: pinned drand quicknet, round pre-declared in S4);
- frozen hypothesis-free primary ascertainment;
- nuisance-only pilot diagnostics;
- one canonical research-program alpha budget;
- executable endpoint-quality rules.

Advanced Digital Twin / Pathogen / Therapeutic work remains frozen/deferred.

The next independent score must come from a fresh hostile re-review of the merged state, not from this document.

ADR-022 is the bounded closure change that followed the review of `a1326e3`. After it, that re-review is limited to a targeted consistency attack on D1–D19 (ADR-022 §9).
