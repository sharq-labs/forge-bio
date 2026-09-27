# BIG 0F Power and Variance Policy

**Status:** NORMATIVE — machine-readable source: `config/big0f-power-policy.v2.json`
**Replaces:** the v1 Power Input Derivation Contract

## 1. Why power is split into two stages

BIG 0F is NUISANCE_ONLY, so the variance of the biological increment cannot be observed in the pilot.

v1 made BIG 0F GO depend on an "independent same-estimand development source". That route is logically possible, but no such source exists. None can be produced under the roadmap before core code exists. And a loosely judged "same estimand" could be cherry-picked.

v2 therefore separates:

- **Stage A — BIG 0F pool-sufficiency screen.** GO-eligible and model-free. It asks whether the untouched pool is large enough under a conservative, frozen variance family.
- **Stage B — confirmatory power gate.** A P1 item, required before the confirmatory seal. It measures the variance in a Development Lift & Variance Study (DLVS).

The confirmatory test is fixed in [V0_FREEZE_STATEMENT.md](V0_FREEZE_STATEMENT.md) §3. Both stages simulate **that** test.

## 2. Stage A — pool-sufficiency screen (BIG 0F)

**Inputs.** All come from committed BIG 0F artifacts:

- m_d: the number of primary-positive event families in each event-bearing pilot disease.
- s_e: the pooled within-disease SD of nuisance-arm event percentiles, using out-of-fold ranks from the frozen nuisance run.
- p_eb: the fraction of pilot diseases that are event-bearing (primary positives).

**Planning quantities.**

- s_e,up = max(chi-square upper 95% bound with df = Σ(m_d − 1), disease-cluster BCa bootstrap upper 95% bound). The bootstrap uses B = 10,000 and seed domain `power-sd`. A percentile bootstrap alone is not allowed: on normal data with 8 sources it covers the true SD only 69% of the time.
- σ_e(ρ) = √(2(1 − ρ)) · s_e,up. This assumes the combined arm has the same event-level dispersion as the nuisance arm, with correlation ρ between arms.
- Disease-level variance: v(m) = τ² + σ_e(ρ)² / m.

**Simulation.** For each candidate n:

- R = 10,000 datasets. Each has n event-bearing diseases with m_d resampled from the pilot.
- Δ_d = δ + √v(m_d) · Z_d, where Z_d is a standardized Student-t with 5 df. This gives heavier tails than Normal, for skew and outliers. Δ_d is clipped to [−1, 1].
- δ = 0.05.
- The frozen sign-flip test uses 2,000 Monte Carlo flips per dataset, seed domain `power-sim`.

**Required sizes.**

- N_req = smallest n with (power − 2·MCSE) ≥ 0.80.
- F_req = ⌈N_req / p_eb,lower⌉, where p_eb,lower is the Wilson lower 95% bound.

The closed-form Normal approximation is reported as a secondary check. It never decides.

**Frozen scenario family.**

| Scenario | ρ | τ | Role |
|---|---|---|---|
| OPTIMISTIC | 0.8 | 0.05 | NO_GO boundary |
| PLANNING | 0.5 | 0.05 | GO boundary |
| HETEROGENEOUS | 0.5 | 0.10 | Reported |
| PESSIMISTIC | 0.0 | 0.05 | Reported |

**DLVS reservation.** Stage B will draw its additional development diseases from U (§3). Stage A therefore reserves them in advance:

N_DLVS = max(0, ⌈(20 − E_pilot) / p_eb,lower⌉)

Here E_pilot is the number of event-bearing pilot diseases.

**Decision.** U is the untouched pool computed in [BIG_0F_SELECTION_CUSTODY.md](BIG_0F_SELECTION_CUSTODY.md) §5. Two threshold-manifest gates implement the decision:

| Gate | Value | Pass | Fail |
|---|---|---|---|
| `POWER_POOL_SUFFICIENCY` | U − N_DLVS − F_req(PLANNING) | ≥ 0 | REDESIGN |
| `POWER_POOL_OPTIMISTIC_FLOOR` | U − N_DLVS − F_req(OPTIMISTIC) | ≥ 0 | NO_GO |

So:

- the power screen passes if U − N_DLVS ≥ F_req(PLANNING);
- **REDESIGN** if F_req(OPTIMISTIC) ≤ U − N_DLVS < F_req(PLANNING);
- **NO_GO** if U − N_DLVS < F_req(OPTIMISTIC).

**Why ρ = 0.5 for planning (judgement).** Nested arms share the entire nuisance block, so their event percentiles are expected to be positively and strongly correlated. 0.5 is deliberately below that expectation. Stage B does not use ρ; it measures the paired-difference SD directly (§3).

## 3. Stage B — confirmatory power gate (before the confirmatory seal; P1)

| Element | Rule |
|---|---|
| Data | The DLVS runs the intended confirmatory model family and version, and the nuisance comparator, at (T\*, H\*) on DEVELOPMENT_EXPOSED diseases only. These are the BIG 0F pilot diseases plus additional development diseases. |
| Additional diseases | The custodian draws them from U in ascending HMAC(key, `dlvs` ‖ disease UI) order, one at a time, until the development set has ≥ 20 event-bearing diseases. Nobody chooses them. Each drawn disease becomes DEVELOPMENT_EXPOSED and leaves U. U is frozen by digest at the BIG 0F result registration, and this draw is the only permitted removal: any other exposure of a U disease spends the V0 allocation (Freeze Statement §4). The untouched pool for the Stage B gate is U_B = U − every DLVS disease. |
| Minimum size | ≥ 20 event-bearing development diseases |
| Estimands | σ_e is the within-disease SD of event-level paired differences, measured directly. τ is the between-disease SD of true lift, by method of moments with a floor of 0.02. ρ is the between-arm correlation of event percentiles. |
| Planning values | σ_e: max(chi-square upper 95%, disease-family cluster BCa upper 95%). τ: bootstrap upper 95%. ρ: reported only. B = 10,000 with a keyed seed (domain `power-sd`). |
| Simulation | Same machinery as Stage A, using the pooled DLVS and pilot events-per-disease distribution, with one difference. Stage B uses the **directly measured** paired-difference σ_e planning value in v(m) = τ² + σ_e²/m; the Stage A transform √(2(1 − ρ))·s_e is not used. ρ is reported only. Bootstrap seeds use domain `power-sd`. |
| External sources | Optional, only through the variance-source registry with its frozen search protocol, and only if each covers ≥ 20 diseases. They can **only raise** the planning SD (max rule), never lower it. |
| Gate | The confirmatory seal is allowed only if U_B ≥ F_req at the Stage B planning values. Otherwise the result is REDESIGN, meaning V1 or a larger frame under a new version. (T\*, H\*) is never re-selected inside V0. |
| Finality | The Stage B result is registered under the public-seal rule (INV-S8) before the MAP seal, together with the U_B digest and the variance-source registry (or an explicit null). It is final: external sources cannot be added and the gate cannot be re-evaluated afterwards. |
| Tier | The DLVS is development evidence. If its results influence the model, its diseases are SPENT_FOR_MODEL_SELECTION. It never supports a confirmatory claim. |

## 4. Prohibitions

- No caller-supplied SD.
- No BIG 0F biological-arm run.
- No seed chosen by an analyst: every seed is derived from the sealed key with a named domain.
- No scenario chosen after results.

## 5. Zero-event diseases

Zero-event diseases stay in the frame. Power is computed for the event-bearing conditional estimand; frame requirements are converted through p_eb,lower.
