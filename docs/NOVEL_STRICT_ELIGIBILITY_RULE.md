# NOVEL-STRICT Eligibility Rule

**Status:** NORMATIVE — V0 ranking universe ([V0_FREEZE_STATEMENT.md](V0_FREEZE_STATEMENT.md))

## 1. The problem this closes

A gene can become an E1-NOVEL-STRICT positive only if it had no pre-T disease-specific genetic signal. Previously, genes that *did* have a pre-T signal stayed in the ranking universe as competitors, but could never be positives.

A biology arm that sees pre-T genetics can therefore learn "known → push down" and gain rank percentile without predicting anything new. This is label-eligibility exploitation.

## 2. Rule

The primary ranking universe for disease *d* at cutoff T is:

```text
U_d = { g in the as-of-T identity-valid CandidateUniverse : ScreenSignal(g, d, T) = NONE }
```

`ScreenSignal` is computed identically for **every** candidate of **both** arms. It is fixed before any post-T outcome is opened, and it uses only the **ranker-visible** historical snapshot (KNOWN_TO_RANKER_AT_T):

- **SUGGESTIVE_OR_QUALIFYING** if any pre-T disease-specific association in the ranker-visible snapshot has p ≤ the suggestive threshold, and its lead variant lies within the frozen gene window of *g*. The threshold, the gene window and the candidate-gene replication clause are those in `config/big0f-adjudication-policy.v2.json` → `pre_t_genetic_state`.
- **Disease-specific** means the same term set as outcome discovery: concept, synonyms and narrower descendants ([OUTCOME_DISCOVERY_SPEC_V1.md](OUTCOME_DISCOVERY_SPEC_V1.md) §2). The novelty audit uses the same term set.
- **Ranker-visible snapshot** means the union of the pre-T genetic-association inputs available to **any** arm. A signal visible to one arm is screened for both.
- **NONE** otherwise.

## 3. Relation to the positives' audit

- A positive additionally needs the evaluation-side HistoricalNoveltyAudit to return NOVEL_CONFIRMED, with PreTGeneticState = NO_SIGNAL_OBSERVED.
- The audit may find a signal the ranker could not see (KNOWN_PUBLICLY_AT_T only). That event is a provider-coverage failure and is excluded from P_d. Its gene stays in U_d, because it is not screened out. As an assigned post-T event gene it belongs to X_d, so it is not a competitor for other positives ([METRIC_EVENT_RANK_PERCENTILE_V1.md](METRIC_EVENT_RANK_PERCENTILE_V1.md) §1–§2). Because that signal is invisible to both arms, it cannot be exploited.
- Because the screen uses exactly the data the biology arm can see, the exploitation channel is closed. The universe is not made to depend on outcomes.

## 4. Mandatory sensitivity

The **symmetric-indicator universe** is also reported:

- U_d = all identity-valid candidates;
- the `ScreenSignal` indicator is added to the **nuisance block of both arms**.

The primary claim is labelled eligibility-fragile if the two analyses disagree in sign, or in significance at α = 0.05 (SENS-SYMMETRIC in [V0_FREEZE_STATEMENT.md](V0_FREEZE_STATEMENT.md) §3a). This is a label, not a veto.

## 5. Evidence (synthetic, recorded in ADR-022)

Lift = combined − nuisance. There were 40 training and 40 test diseases, 3,000 genes per disease, and 12 worlds; values are mean (SE).

| World | Learner | Current design | Filtered universe (primary) | Symmetric indicator (sensitivity) |
|---|---|---|---|---|
| No biology, 8.9% pre-T signal genes | logistic | **+0.0129** (0.0006) | −0.0001 (0.0002) | −0.0002 (0.0002) |
| No biology, 8.9% | gradient boosting | **+0.0170** (0.0049) | +0.0039 (0.0048) | −0.0029 (0.0061) |
| Real biology, 8.9% | logistic | +0.0659 (0.0035) | +0.0525 (0.0033) | +0.0528 (0.0034) |
| No biology, 2.2% pre-T signal genes | logistic | +0.0040 (0.0002) | −0.0001 (0.0001) | +0.0003 (0.0002) |

**What the evidence shows:**

- The current design manufactures lift when there is no biology. The artifact is about a quarter of the 0.05 planning effect when pre-T signal is dense, as at later cutoffs.
- Both fixes remove the artifact.
- The filtered universe is primary because it does not depend on the learner learning to use the indicator. It also preserved real signal as well as or better than the indicator design with gradient boosting (0.0428 vs 0.0405 in the sparse world).
