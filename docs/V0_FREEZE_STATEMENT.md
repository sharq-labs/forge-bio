# B-TGT-E1-v0 Freeze Statement

**Status:** NORMATIVE — single source of truth for what is fixed in V0
**Decision record:** [ADR-022](adr/ADR-022-final-scientific-consistency-closure.md)
**Precedence:** where any other document disagrees with this page, this page wins and the other document is a defect to be corrected.

## 1. Fixed now (before BIG 0F)

| Item | V0 value | Normative source |
|---|---|---|
| Regime | Common-complex germline disease/trait genetics | [BENCHMARK_ESTIMAND_V0.md](BENCHMARK_ESTIMAND_V0.md) §2 |
| Primary subtype | `E1-NOVEL-STRICT` | this page |
| Ranking universe | Eligibility-filtered NOVEL-STRICT universe | [NOVEL_STRICT_ELIGIBILITY_RULE.md](NOVEL_STRICT_ELIGIBILITY_RULE.md) |
| Primary metric | `EVENT_RANK_PERCENTILE_V1` | [METRIC_EVENT_RANK_PERCENTILE_V1.md](METRIC_EVENT_RANK_PERCENTILE_V1.md) |
| Primary contrast | (Nuisance + biology) − (Nuisance only), nested, capacity-matched, with a permuted-biology placebo guard | [ADR-020](adr/ADR-020-e1-primary-comparator-confirmatory-rule.md) §5; §3 below |
| Nuisance comparator | 14 mandatory families, frozen definitions | `config/big0f-nuisance-manifest.v2.json` |
| Outcome discovery | Frozen sources, candidate-event predicate, date rule, grouping, custody | [OUTCOME_DISCOVERY_SPEC_V1.md](OUTCOME_DISCOVERY_SPEC_V1.md), `config/outcome-discovery.v1.json` |
| Assignment, phenotype, novelty definitions | Adjudication policy v2 (`BIG0F-ADJUDICATION-V2`) | `config/big0f-adjudication-policy.v2.json` |
| Agreement policy | Gwet AC1 per task with a lower-bound rule | `config/big0f-adjudication-policy.v2.json` |
| BIG 0F thresholds | Threshold manifest v2 (direction, rationale, sensitivity per gate) | `config/big0f-thresholds.v2.json` |
| Cutoff/horizon rule | First passing pair under frozen custodian predicates | [BIG_0F_SELECTION_CUSTODY.md](BIG_0F_SELECTION_CUSTODY.md) |
| Confirmatory cutoff and horizon | The BIG 0F-selected pair (T\*, H\*); one cutoff, no pooling across cutoffs in V0 | this page |
| α | 0.05, one-sided. This is the program's family-wise α, and the V0 confirmatory generation is allocated all of it (FIXED_SPLIT). Every confirmatory test uses its generation's allocated α as the p-value threshold (INV-L11). | this page |
| Minimum scientifically meaningful effect | 0.05 percentile units (planning effect, not a success threshold) | this page |
| Target power | 0.80 | this page |
| Confirmatory test and success rule | §3 below | this page |
| Power sequencing | BIG 0F: pool-sufficiency screen. Before the confirmatory seal: Development Lift & Variance Study | [BIG_0F_POWER_AND_VARIANCE_POLICY.md](BIG_0F_POWER_AND_VARIANCE_POLICY.md) |

## 2. Instantiated later by frozen rules (values measured, rules fixed)

| Item | When | Constraint |
|---|---|---|
| T\*, H\* values | Stage 3, before sampling | Produced by the custodian predicates; not chosen |
| Endpoint-quality rule values | After BIG 0F, and sealed **before the custodian releases any DLVS label** (seal_time before the release-log entry, so no DLVS combined-arm result can exist) | May only be equal to or stricter than adjudication policy v2. They are never tuned to model lift. |
| Planning variance for confirmation | Development Lift & Variance Study | Methodology frozen in the power policy |
| Untouched confirmatory pool | After BIG 0F exposure accounting | Computed by [BIG_0F_SELECTION_CUSTODY.md](BIG_0F_SELECTION_CUSTODY.md) §5 |
| Confirmatory disease sample | After the MAP seal and after rankings of every U_B disease are sealed, at time(R_c); before the confirmatory seal bundle | The first F_req (Stage B planning) diseases of U_B, in ascending HMAC(key_c, `confirmatory-draw` ‖ disease UI) order. No other size is allowed. There is one draw per program version ([BIG_0F_SELECTION_CUSTODY.md](BIG_0F_SELECTION_CUSTODY.md) §7; INV-C12). |
| DLVS development diseases | After BIG 0F, before Stage B | Drawn by the custodian from U in `dlvs` key order until ≥ 20 event-bearing ([BIG_0F_POWER_AND_VARIANCE_POLICY.md](BIG_0F_POWER_AND_VARIANCE_POLICY.md) §3) |
| MAP-level parameters: coverage-gate fractions, confirmatory learner family and capacity protocol, K of the Recall@K companion, observability-sensitivity details | In the MAP, before the confirmatory seal | Set on DEVELOPMENT data only. The data-quality items (coverage-gate fractions, observability-sensitivity details) are sealed before the custodian releases any DLVS label. None of them can change the primary metric, universe, test, α, effect, nuisance families or §3a. |

## 3. Confirmatory test and success rule (V0)

1. **Unit.** Event-bearing confirmatory diseases *d* = 1..*n*, i.e. diseases with at least one adjudicated NOVEL-STRICT primary positive.
2. **Disease contrast.** Δ_d = M_d(combined) − M_d(nuisance), with M_d as defined in the metric specification.
3. **Statistic.** The equal-weight mean Δ̄ = (1/n) Σ Δ_d.
4. **Test.** One-sided sign-flip randomization test of H0: Δ_d symmetric about 0, against H1: E[Δ] > 0.
    - The test is exact when n ≤ 20: p = #{s ∈ {−1, +1}ⁿ : mean(s_d·Δ_d) ≥ Δ̄} / 2ⁿ, where the identity vector is included.
    - Otherwise it uses B = 100,000 Monte Carlo sign flips, with p = (1 + #{flipped Δ̄ ≥ observed Δ̄}) / (1 + B).
    - The seeds come from the **confirmatory key** key_c, with domain `confirmatory-signflip`. key_c is derived from a new drand round pre-declared in the single confirmatory draw registration ([BIG_0F_SELECTION_CUSTODY.md](BIG_0F_SELECTION_CUSTODY.md) §7). The public BIG 0F key is never used.
5. **Placebo guard.** Refit the combined arm K = 19 times with the biology block permuted within each disease.
    - Each permutation shuffles gene identities within each disease, for **both** the training anchors and the scored confirmatory diseases.
    - One permutation is applied jointly to all biology columns.
    - Each refit is a full refit with the same learner, search space and budget.
    - Seeds come from key_c with domain `placebo`.
    - Observed Δ̄ must exceed every placebo Δ̄, which is a one-sided permutation level of 0.05.
6. **Success** requires all of the following:
    - p < α_g, the generation's allocated α. In V0 α_g = 0.05 (INV-L11);
    - every BLOCKING analysis in §3a passes;
    - every integrity precondition in [BENCHMARK_V0_SPEC.md](BENCHMARK_V0_SPEC.md) §28 items 1–11 holds. A failed precondition makes the run INVALID; it is not a negative result (§4).
7. **Reported regardless of outcome:**
    - Δ̄ with a disease-level BCa bootstrap 95% CI;
    - the disease-family block bootstrap CI;
    - every analysis in §3a, with its label.
8. **The 0.05 effect is for power planning only.** Magnitude claims use the CI.

### 3a. Sensitivity analyses (closed list)

No other analysis can grant or veto success. Every analysis reuses the frozen test, learner, search space, budget and keyed seeds.

| ID | Analysis | Role | Pass criterion | Label if not passed |
|---|---|---|---|---|
| SENS-PLACEBO | Permuted-biology placebo guard (item 5) | BLOCKING | Observed Δ̄ exceeds all 19 placebo Δ̄ | — |
| SENS-LODO | Leave one event-bearing disease out, for every disease | BLOCKING | min over d of Δ̄(−d) > 0 | — |
| SENS-FAMILY | Sign-flip at the disease-family level | LABEL | p < 0.05 | dependence-fragile |
| SENS-SYMMETRIC | Symmetric-indicator universe ([NOVEL_STRICT_ELIGIBILITY_RULE.md](NOVEL_STRICT_ELIGIBILITY_RULE.md) §4) | LABEL | Same sign as the primary and p < 0.05 | eligibility-fragile |
| SENS-COVERAGE-HIGH | Diseases with HIGH coverage only | LABEL | Δ̄ > 0 | coverage-fragile |
| SENS-CANDIDATE-GENE | Candidate-gene clause of the pre-T screen removed (adjudication policy v2) | LABEL | Δ̄ > 0 and p < 0.05 | novelty-fragile |
| SENS-COUPLING | Events with label–feature method coupling excluded | LABEL | Δ̄ > 0 and p < 0.05 | coupling-fragile |
| SENS-PROVIDER | Events from sources coupled to an input provider excluded (provider audit) | LABEL | Δ̄ > 0 | provider-fragile |
| SENS-ATTENTION | Δ̄ within each tercile of pre-T disease-specific attention of the positives | LABEL | Δ̄ > 0 in at least 2 of 3 terciles | attention-concentrated |
| SENS-DEV-LOCUS | Development-exposed loci included: pilot, DLVS and showcase ([BIG_0F_SELECTION_CUSTODY.md](BIG_0F_SELECTION_CUSTODY.md) §6) | REPORT | — | — |

- BLOCKING analyses are intersection–union conditions on the primary success, so they need no α adjustment.
- LABEL analyses never change the decision. They attach their label to the claim.

## 4. Failure semantics

- A GO/REDESIGN/NO-GO outcome never changes the subtype, metric, α, effect, test or nuisance families inside V0.
- If E1-NOVEL-STRICT is not constructible, the outcome is **REDESIGN → a new version (V1)** with a new pilot on untouched diseases. The research-program α budget carries over (see [SEMANTIC_INVARIANTS.md](SEMANTIC_INVARIANTS.md) INV-L7). Because V0 holds the full 0.05, V1 can receive α **only** if V0 ended in a **mechanical REDESIGN or NO_GO whose result was registered, under the public-seal rule (INV-S8), before the MAP seal**. The qualifying results are the BIG 0F decision, the Stage B power gate and the BIG 1 fidelity verdict, and only then is the V0 allocation RETIRED unspent.
    - Each of these results is final once registered. For example, the Stage B result binds its variance-source registry, or an explicit null, and is never re-evaluated.
    - Any other withdrawal or abandonment, at any time, spends the allocation.
    - The MAP seal itself obeys the public-seal rule and precedes the CDR. Once a CDR with a verified seal exists, any later defect in the MAP or the rankings spends α and never voids the CDR.

- Once the MAP is sealed, the V0 allocation is spent by any of these, whether or not the test ran:
    - a voluntary withdrawal;
    - an exposure of a U_B disease;
    - an abandonment.
- U is frozen by digest when the BIG 0F result is registered. After that, the only permitted removal is the custodian's keyed DLVS draw, so U_B = U − DLVS is fully mechanical. Any other exposure of a U disease to an audience that is not role-separated spends the V0 allocation; it does not shrink the pool. The pool cannot be pruned selectively.
- If a later stage shows that the selected (T\*, H\*) or the untouched pool cannot support confirmation, the outcome is **REDESIGN → V1**. Such stages include the BIG 1 fidelity check and the Stage B power gate. (T\*, H\*) is never re-selected inside V0.
- A confirmatory run that is INVALID because a §28 precondition failed still **spends** its α allocation once outcomes have been unsealed for that generation (INV-L10). A failed procedure is never retried on the same generation.
- Locus-level primary credit is the preferred V1 redesign; it is not a V0 option.

## 5. What "frozen" means

`status: SEAL_CANDIDATE` means the text is final pending external sealing. An artifact is `SEALED` only when a verified public-registry attestation and a timestamp attestation cover its digest.

**Public-seal rule (INV-S8).** A registration that gates a later step counts only if two things exist **before that dependent step begins**: its upgraded OTS proof is attached to the public registry record, and a public web-archive capture exists. This covers S1, S4, S6, every BIG 0F result, the Stage B result, the BIG 1 verdict, the endpoint-quality rule, the MAP data-quality values, the MAP, the ranking commitment, the CDR, the §3a refit registration, the confirmatory seal bundle and every label-set registration. Each has exactly one registration per generation.

- A registration that fails the rule is void and must be redone before the dependent step.
- Once the dependent step has happened, the registration can no longer be voided or re-presented.
- A later defect means REDESIGN if it arises before the MAP seal. That REDESIGN retires α only if it is one of the qualifying mechanical results in §4; otherwise α is spent. A defect after the MAP seal spends α.

- Only `SEALED` supports a claim about **when** something was fixed.
- Self-reported `frozen_at` dates are not evidence and are no longer used.
- In prose, "frozen" or "fixed" describes a rule that is decided at specification level (SPEC-CLOSED). It never implies a seal.

## 6. Superseded statements

These statements are superseded by this page and were corrected in the same change:

- BENCHMARK_ESTIMAND_V0 §8, §9 and §11 (primary metric and subtype "selected after BIG 0F"; Recall@K promotion; smallest-H rule);
- BENCHMARK_V0_SPEC §5–§7 (cutoff, horizon and subtype selection);
- ADR-006 "thresholds frozen after BIG 0F";
- README "exact confirmatory estimand instance (H, subtype, metric) after feasibility evidence";
- PRE_CODE_CHECKLIST items that treated subtype, metric, α or effect as open.
