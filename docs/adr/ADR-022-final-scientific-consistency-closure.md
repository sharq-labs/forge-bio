# ADR-022 — Final Scientific Consistency Closure (pre-BIG 0F)

**Status:** Accepted — closes the pre-code specification phase
**Normative summary:** [V0_FREEZE_STATEMENT.md](../V0_FREEZE_STATEMENT.md)
**Regression requirements:** [SEMANTIC_INVARIANTS.md](../SEMANTIC_INVARIANTS.md)
**Supersedes, where they conflict:** ADR-006 (threshold timing), ADR-020 §4 (nuisance family list), ADR-021 §2–§4 and §9 (sampling order, randomness, agreement, power input)

## 1. Context

An independent hostile review of `main` at `a1326e3` found the architecture sound but not freezable. The weaknesses fell into five groups:

1. **Undefined semantics.** The primary metric had no canonical definition, and neither did ties or family credit.
2. **Deferred choices that fed GO.** Subtype, metric, assignment thresholds, agreement statistic and power inputs were all "chosen after BIG 0F", yet they determined BIG 0F GO.
3. **A label-eligibility artifact in E1-NOVEL-STRICT.** It manufactures lift with no biology.
4. **Outcome-exposure and grinding channels.** These were the 16-pair enumeration, showcase cases, beacon chain and round choice, and frame variants.
5. **Stale status claims.** Documents claimed CLOSED or machine-enforced status for code and tests that no longer exist.

A second reviewer agreed with the findings, with one wording correction (§4, D10). That reviewer asked for **one bounded closure change**, followed by a targeted consistency attack only.

This ADR is that change. It records each decision, the alternative rejected, and the evidence.

## 2. Pre-seal versioning rule

Nothing in this repository has been externally sealed. Before the first seal:

- A config or schema is **versioned**: vN becomes vN+1 and the old file is removed. This happens whenever an instance that conformed to vN would still validate but would **mean something different**.
- A file is **amended in place** only when every change makes old instances fail validation, so no silent reinterpretation is possible.
- After S1 ([BIG_0F_SELECTION_CUSTODY.md](../BIG_0F_SELECTION_CUSTODY.md)), any change needs a new protocol version (INV-S6).

## 3. Decision register

| ID | Decision | Rejected alternative | Normative source |
|---|---|---|---|
| D1 | Status vocabulary `SEAL_CANDIDATE` / `SEALED`, plus `sealed_by_attestation_id`. The self-reported `frozen_at` is removed. | Keep `frozen_at` dates. These were backdated assertions with no evidence. | Freeze Statement §5; INV-S1–S5 |
| D2 | The primary subtype `E1-NOVEL-STRICT` and the primary metric `EVENT_RANK_PERCENTILE_V1` are **fixed now**. | Choose them after BIG 0F. This was a forking path, and it was circular with GO. | Freeze Statement §1 |
| D3 | Canonical metric: per-positive AUC against a filtered competitor set, mid-rank ties, family credit = mean over assigned genes, disease-macro mean | Best-ranked gene per family; ties unspecified | [METRIC_EVENT_RANK_PERCENTILE_V1.md](../METRIC_EVENT_RANK_PERCENTILE_V1.md) |
| D4 | NOVEL-STRICT ranking universe = candidates with ScreenSignal = NONE on the ranker-visible snapshot. The symmetric-indicator universe is a mandatory sensitivity. | Keep pre-T-signal genes as never-positive competitors; indicator-only design | [NOVEL_STRICT_ELIGIBILITY_RULE.md](../NOVEL_STRICT_ELIGIBILITY_RULE.md) |
| D5 | Outcome discovery v1: pinned sources, candidate predicate, date rule, 500 kb families, recall audit, a single execution by the custodian | Unspecified "all qualifying candidate events" | [OUTCOME_DISCOVERY_SPEC_V1.md](../OUTCOME_DISCOVERY_SPEC_V1.md) |
| D6 | Mechanical MeSH disease frame with no manual additions | Frame built "from frozen vocabulary/regime rules" left undefined | [BIG_0F_FRAME_RULE.md](../BIG_0F_FRAME_RULE.md) |
| D7 | Assignment, phenotype, novelty and coverage definitions (adjudication policy v2) are frozen **before** BIG 0F. The later endpoint-quality rule may only be equal or stricter. | Freeze thresholds after BIG 0F while they already gate GO | [BIG_0F_ADJUDICATION_DEFINITIONS.md](../BIG_0F_ADJUDICATION_DEFINITIONS.md); INV-T8 |
| D8 | Agreement = Gwet AC1 for each gated task, with a lower one-sided 90% BCa bound. The duplicate selection is **salted**: the custodian salt is committed at S6 and revealed after the first-review labels are registered. At most one clarification-only revision, retested on ≥ 30 fresh cases. | Statistic chosen after prevalence is seen; analyst-chosen subsets | Adjudication definitions §4 |
| D9 | Threshold manifest v2: every gate has an ID, direction, source artifact, GO/NO-GO bounds, stricter/looser bounds and a rationale type. GO requires a pass at the stricter bound. | Unlabelled numbers; a sensitivity rule whose consequence was unstated | `config/big0f-thresholds.v2.json`; INV-T1–T7 |
| D10 | Power in two stages. **Stage A** (BIG 0F) is a model-free pool-sufficiency screen that reserves N_DLVS diseases. Its REDESIGN and NO_GO boundaries are two separate gates. **Stage B** (before the confirmatory seal, P1) is a Development Lift & Variance Study with ≥ 20 event-bearing diseases, whose extra diseases the custodian draws from U by key order. | Keep v1: BIG 0F GO depends on an "independent same-estimand development source" | [BIG_0F_POWER_AND_VARIANCE_POLICY.md](../BIG_0F_POWER_AND_VARIANCE_POLICY.md) |
| D11 | Nuisance manifest v2: 14 families including global attention volume and momentum. The learner is fully specified (objective, negatives, missing handling) and **immutable after pilot labels**. Out-of-fold ranks, an adequacy check (failure → REDESIGN), and a K = 19 permuted-biology placebo guard with a defined permutation scope. | 12 families; a learner that is recorded but not frozen | `config/big0f-nuisance-manifest.v2.json`; [BIG_0F_NUISANCE_EXECUTION_CONTRACT.md](../BIG_0F_NUISANCE_EXECUTION_CONTRACT.md) |
| D12 | T/H custody: an independent custodian computes five frozen predicates and runs discovery once; the study team sees aggregates only; every exposure is in the ledger. U excludes every non-role-separated exposure. Loci of **any** development-exposed disease at (T\*, H\*) are excluded from confirmatory positives. | Study team enumerates per-event universes for all 16 pairs | [BIG_0F_SELECTION_CUSTODY.md](../BIG_0F_SELECTION_CUSTODY.md) §2–§6 |
| D13 | Randomness: the drand **quicknet** chain is pinned, round R is **pre-declared** in a public registration, and there is **one authoritative timestamp** (§5). Validity is decided publicly before R and cannot be voided afterwards. Byte encodings are fixed. Confirmatory randomness uses a new pre-declared round and key. | "First verified round after frame seal" on an unpinned chain, embargo allowed | Custody §7; INV-C6–C11 |
| D14 | Phase order is SPEC FREEZE → minimal verification harness → BIG 0F → core. The manual pilot **is** BIG 0F; there is no separate manual pilot. | Parallel manual pilot; core before BIG 0F | §6 below |
| D15 | Closure labels come from the INV-D2 vocabulary (SPEC-CLOSED, IMPLEMENTATION-PENDING, EMPIRICAL-OPEN, OPERATIONAL-OPEN, SUPERSEDED). No document may claim machine enforcement that no code provides. | CLOSED-ENGINE / CLOSED-TEST labels after code removal | INV-D2 |
| D16 | Research-program ledger invariants (sequence, hash chain, Σα, transitions, anchoring, fork rule, budget carryover). V0 holds the full α = 0.05, and every test uses its generation's allocated α. | Schema-only structure with no semantic rules | [SEMANTIC_INVARIANTS.md](../SEMANTIC_INVARIANTS.md) §INV-L |
| D17 | Endpoint-quality applicability matrix: every dimension is REQUIRED or NOT_APPLICABLE for each subtype, and every applicable criterion has `required: true` | Freely chosen `required` flags; REPLICATION and HETEROGENEITY undefined | [ENDPOINT_QUALITY_RULE.md](../ENDPOINT_QUALITY_RULE.md) |
| D18 | One confirmatory cutoff (T\*, H\*) and a paired sign-flip test on Δ̄. A **closed** sensitivity list: BLOCKING (placebo guard, leave-one-disease-out) and LABEL (all others). The 0.05 effect is for planning only. An INVALID run still spends its α. | Pooled cutoffs; the effect size used as a success threshold; open-ended "required sensitivities pass" | Freeze Statement §3, §3a, §4 |
| D19 | MAP-level parameters that are not in §1 get a phase: set in the MAP on development data before the confirmatory seal, and unable to touch any §1 item | Unassigned values settled whenever convenient | Freeze Statement §2 |

## 4. Evidence

All simulations are synthetic, use fixed seeds, and were run outside the repository (numpy/scipy). The repository stays specification-only. The simulation scripts will enter the verification harness as regression fixtures (INV-D4).

### D4 — label-eligibility artifact

Lift = combined − nuisance. There were 40 training and 40 test diseases, 3,000 genes per disease, and 12 worlds; values are mean (SE).

| World | Learner | Current design | Filtered universe | Symmetric indicator |
|---|---|---|---|---|
| No biology, 8.9% pre-T signal | logistic | **+0.0129** (0.0006) | −0.0001 (0.0002) | −0.0002 (0.0002) |
| No biology, 8.9% | gradient boosting | **+0.0170** (0.0049) | +0.0039 (0.0048) | −0.0029 (0.0061) |
| Real biology, 8.9% | logistic | +0.0659 (0.0035) | +0.0525 (0.0033) | +0.0528 (0.0034) |
| No biology, 2.2% | logistic | +0.0040 (0.0002) | −0.0001 (0.0001) | +0.0003 (0.0002) |

**Conclusion.** With no biology, the current design manufactures +0.013 to +0.017, which is a quarter to a third of the 0.05 planning effect. Both fixes remove the artifact. The filtered universe is primary because it does not rely on the learner using an indicator.

### D3 — ties

On null data, adding a pure-noise attention column gave a spurious lift of **+0.253** when positives were ranked last within ties, and **+0.0015** with mid-ranks.

### D8 — agreement statistic shopping

The simulation used two independent raters, each 90% accurate, with n = 30 and prevalence 0.9:

- median κ = 0.37 and median AC1 = 0.75;
- P(κ ≥ 0.70) = 0.07 and P(AC1 ≥ 0.70) = 0.67.

Choosing the statistic after prevalence is seen is therefore a GO lever. AC1 is fixed now, and κ is reported.

### D10 — variance bound

With 8 variance sources on normal data, a percentile-bootstrap upper 95% bound covered the true SD only **69%** of the time. Stage A therefore takes the maximum of the chi-square and cluster-BCa bounds.

### D11 — flexible-learner null lift

In the no-biology world under the filtered universe, gradient boosting gave +0.0039 (SE 0.0048; per-world SD ≈ 0.017 over 12 worlds). That is not distinguishable from zero, but the spread across worlds is large relative to the effect. A flexible learner's capacity to fit noise is therefore controlled by the placebo guard rather than assumed away: success requires beating permuted biology under the same learner and budget.

## 5. Randomness and the authoritative timestamp (D13)

- **Chain.** drand quicknet, chain hash `52db9ba70e0cc0f6eaf7803dd07447a1f5477735fd3f661792ba94600c84e971`. The default chain and the other public chains are not accepted.
- **Round.** R is written into the S4 selection registration, about 7 days after submission; only the ordering rule below is binding. The team never "takes the first round after" anything.
- **Authoritative seal time** of any artifact: seal_time = max(earliest Bitcoin block time in the verified OpenTimestamps proof, public-registry registration time). Both attestations are required. A single attestation, a self-reported `sealed_at`, or an embargoed registry record gives no seal time.
- **Ordering rule.** seal_time(S4) ≤ time(R) − 24 h. The 24-hour margin absorbs Bitcoin block-time imprecision (up to 2 h) and registry processing delay.
- **No voiding after the fact.** The upgraded OTS proof must be attached to the public S4 record before time(R) − 24 h, so validity is settled publicly before R's randomness exists.
    - If the rule fails before that point, S4 is void and is re-registered with a new R; the void record stays public.
    - A public web-archive capture taken before that point is authoritative.
    - An invalidation after that point leads to REDESIGN, with the S5 prefix treated as DEVELOPMENT_EXPOSED.
- **Confirmatory randomness.** The confirmatory generation uses a new round R_c and its own key. R_c is pre-declared in a single confirmatory draw registration, made after the MAP and the rankings of every U_B disease are sealed. The key depends on the U_B digest and the ranking commitment, not on the MAP digest. There is exactly one draw per program version, and withdrawal after time(R_c) − 24 h spends α. The public BIG 0F key is never reused for the confirmatory draw, the placebo guard or the sign-flip test.
- **Release.** Adjudicators receive events only after seal_time(S6) has been established and independently verified. The custodian's release log is the evidence that adjudication started after the seal.

## 6. Phase sequencing (D14)

| Phase | Entry condition | Exit |
|---|---|---|
| 0. SPEC FREEZE | This ADR merged | The targeted consistency attack (§9) finds no new false-GO P0 → PLAN FROZEN |
| 1. Minimal pre-BIG 0F verification harness | PLAN FROZEN | Schema/config validation; INV-* checks; canonical hashing; OTS/OSF/drand verifiers; metric reference implementation; Stage A power engine; schemas for the discovery run, recall audit and release log; external-seal dry run passed |
| 2. BIG 0F | Harness complete; independent custodian and second adjudicator in place (start gates) | GO / REDESIGN / NO_GO / INCONCLUSIVE under threshold manifest v2 |
| 3. Core B-TGT-E1 | BIG 0F GO | DLVS (Stage B) → confirmatory seal → confirmatory generation |

**Manual pilot.** The manual pilot is BIG 0F: the same custodian, frame, beacon and thresholds. Any case reviewed outside that path is a showcase case, governed by custody §4.

## 7. Correction recorded from review

The first review stated that the v1 power GO gate "can never pass". That was too strong. The contract allowed GO through an independent, prior, same-estimand DEVELOPMENT source.

- No such source exists.
- None can be produced before core code under the roadmap.
- Judging "same estimand" left a cherry-picking channel.

The gate was therefore **unreachable in practice under the current roadmap**, not logically impossible. It remains a P0, and D10 resolves it.

## 8. Consequences

- BIG 0F GO no longer depends on any quantity chosen after outcomes are seen.
- Several v1 configs and schemas were removed and replaced by v2. [schemas/README.md](../../schemas/README.md) lists the replacements.
- Every closure item now has an invariant ID. The verification harness implements those invariants as regression tests before BIG 0F.
- Costs accepted:
  - BIG 0F needs an independent custodian in addition to the second adjudicator.
  - Confirmation needs a DLVS of ≥ 20 event-bearing development diseases.
  - V0 cannot switch to locus-level credit; that is a V1 redesign.

## 8a. Targeted consistency attack — round 1 (recorded)

An independent agent that had not seen how the change was produced ran the targeted attack. It checked D1–D19 and made 24 false-GO attempts: 15 were blocked and 9 were open. It found five P0 findings. All five are fixed in this change.

| Finding | Fix |
|---|---|
| P0-1 After an adequacy failure, the nuisance learner could be changed and re-evaluated on the same pilot | Adequacy failure → REDESIGN; learner immutable after pilot labels (D11; nuisance contract §3; manifest `change_after_pilot_labels`) |
| P0-2 The success threshold was hard-coded at 0.05, not tied to the allocated α | V0 holds the full 0.05, and p < α_g applies (D16; INV-L11; Freeze §1, §3) |
| P0-3 The first reviewer could predict the duplicate-review audit set | Salted selection, revealed after first-review labels are registered, stratified by disease only (D8; custody §7, S8; INV-A3) |
| P0-4 The §28 preconditions re-opened a veto outside the closed §3a list | §28 items 1 and 11 rewritten (BENCHMARK_V0_SPEC §28) |
| P0-5 DLVS loci could leak into confirmatory positives | Exclusion extended to every development-exposed disease at (T\*, H\*) (D12; custody §6; INV-X5; SENS-DEV-LOCUS) |

The P1 findings fixed in the same pass:

- gene–event linkage for X_d, and empty families after deduplication;
- ScreenSignal term-set and snapshot scope;
- nuisance learner specification and code digest bound at S4;
- the scope of a rule revision;
- mandatory second review for SAME_CONCEPT_DIFFERENT_DEFINITION;
- the PRE_T_LOCUS significance threshold;
- the recall-audit key domain and rounding;
- S5 reusing the S2 universe;
- P_prov limited to AS_OF_T fields;
- MeSH multi-tree and count rules, and the disease-family definition;
- U scoping covering OTHER and DESIGN_TEAM;
- round-rule, void-rule and byte-encoding precision;
- the confirmatory draw size and key;
- registration of INCONCLUSIVE evaluations;
- the split of the non-event gate (INV-T5a);
- a single Stage B σ_e definition;
- the placebo permutation scope;
- endpoint-rule and data-quality MAP values fixed before any DLVS lift exists;
- stray vetoes in other documents mapped to §3a.

Deferred to the harness phase as IMPLEMENTATION-PENDING: schemas for the discovery run, the recall audit and the release log.

**Round 2** re-checked only the round-1 fixes. Every round-1 finding was FIXED except P0-3, which was only partly fixed. Round 2 found two P0 findings, both now fixed:

| Finding | Fix |
|---|---|
| P0-A The per-MAP confirmatory key allowed the confirmatory draw to be re-rolled | Fixed order: MAP sealed, then rankings of every U_B disease sealed, then **one** confirmatory draw registration. key_c is derived from the U_B digest and the ranking commitment. A withdrawal after time(R_c) − 24 h spends α (D13; custody §7; INV-C12; INV-L9) |
| P0-B A rule revision after the salt reveal re-opened audit foreknowledge | A second salt s_ret: the post-revision label set is registered first, then the retest is drawn from all cases (D8; custody S9; INV-A5) |

Round-2 P1 findings fixed in the same pass:

- the mandatory SAME_CONCEPT review is mixed into the blinded batch and excluded from AC1;
- a public archive capture of S4 is authoritative, and a late invalidation means REDESIGN with the prefix exposed;
- the audience scoping of INV-X1 and INV-X3;
- confirmatory discovery reuses the S2 universes, with no re-pin.

Round-2 P2 findings were fixed as well.

**Round 3** confirmed that P0-B is FIXED. It found that P0-A was still reachable through α retirement: the team could withdraw after seeing the draw, or retire after proxy-scoring the public outcome window, and carry α to V1. The fix:

- α is RETIRED unspent **only** through a mechanical REDESIGN or NO_GO **before the MAP seal**. After the MAP seal, any withdrawal, abandonment or exposure spends it.
- U is frozen by digest at the BIG 0F result registration, and the custodian's DLVS draw is the only permitted removal.
- All §3a refits are registered before any confirmatory outcome release.
- The earliest verified CDR binds.
- Salts are used privately and published only after the labels they select for are registered.

These changes are in the Freeze Statement §4, INV-L9, INV-L11, INV-C12, INV-P7, custody §2 and §7, and the power policy §3.

**Round 4** confirmed that every route from round 3 was blocked. One route remained: the MAP seal was controlled by the team. A withheld MAP proof, plus a Stage B gate that could be re-evaluated, could still retire α after the draw was seen. The fix:

- A single **public-seal rule** (INV-S8; Freeze Statement §5) now governs every gating registration. The proof is attached publicly and archived before the dependent step, and the registration can never be voided or re-presented afterwards.
- The Stage B result and the BIG 1 verdict are final once registered.
- Every other withdrawal or abandonment spends α.

**Round 5** result: **NO NEW FALSE-GO P0 → PLAN FROZEN.** The round-4 P0 is closed and the custody §5 wording is fixed. Its hardening items were applied in the same pass:

- INV-S8 now names every gating registration, including the §3a refits, the endpoint-quality rule, the MAP data-quality values and the confirmatory seal bundle;
- each gating registration is registered exactly once;
- the §3a refits are recomputed deterministically;
- the earliest **valid** CDR binds;
- a defect-triggered REDESIGN before the MAP seal spends α unless it is a qualifying mechanical result.

## 9. Exit criterion

After this change there is **only a targeted consistency attack** on D1–D19, not an open review. Each round re-checked only the previous round's fixes (§8a). Round 5 returned **no new false-GO P0**. When this change is merged, the status therefore becomes:

> **PLAN FROZEN → BEGIN MINIMAL PRE-BIG0F VERIFICATION IMPLEMENTATION**

Any later change to a D1–D19 decision needs a new ADR and a new targeted attack on that change.

BIG 0F adjudication still waits for four things:

- the harness;
- a successful external-seal dry run;
- an independent second adjudicator;
- an independent selection custodian.
