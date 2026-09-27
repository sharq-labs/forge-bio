# EVENT_RANK_PERCENTILE_V1 — Canonical Definition

**Status:** NORMATIVE — V0 primary metric ([V0_FREEZE_STATEMENT.md](V0_FREEZE_STATEMENT.md))

## 1. Objects

For disease *d* and one model arm:

- **U_d** — the ranking universe: the eligibility-filtered NOVEL-STRICT universe ([NOVEL_STRICT_ELIGIBILITY_RULE.md](NOVEL_STRICT_ELIGIBILITY_RULE.md)), fixed before outcomes are opened and identical for both arms.
- **s(g)** — the arm's score for gene *g* ∈ U_d. A higher score means a higher priority. Every gene in U_d must be scored. If any score is missing or non-finite, the run is `INVALID`; genes are never silently dropped.
- **P_d** — the NOVEL-STRICT primary positives of *d*: genes in U_d that carry an adjudicated primary-eligible assignment of a qualifying E1-NOVEL-STRICT event family.
- **X_d** — every gene in U_d that is **assigned, under any assignment class** (primary or secondary), to any adjudicated post-T event family of *d* in (T, T+H], whatever the family's status (positive, AMBIGUOUS, secondary-only, excluded). LOCUS_ONLY families and families that were not adjudicated contribute no genes. Families that were not adjudicated include capped-out families and PRE_T_LOCUS families. The definition is identical for both arms.
- **F_d** — the qualifying GeneticDiscoveryEventFamilies of *d*. Each family *f* has its assigned primary genes A_f ⊆ P_d.

## 2. Per-gene score (filtered, mid-rank)

For a positive gene *p*, the competitor set is C_p = U_d \ X_d. It excludes all post-T event genes except *p* itself, and is applied identically to both arms.

```latex
\mathrm{pct}(p) = \frac{\#\{c \in C_p : s(c) < s(p)\} + \tfrac{1}{2}\,\#\{c \in C_p : s(c) = s(p)\}}{|C_p|}
```

This is the AUC of *p* against its competitors. A value of 1 is best, 0 is worst, and ties count one half. If |C_p| = 0, the run is `INVALID`.

## 3. Per-family and per-disease values

- **Family credit.** pct(f) = mean of pct(g) over g ∈ A_f. One family gives one credit, and the credit is never the best-ranked gene.
- **Gene deduplication.** A gene that is assigned to several families of *d* counts once. It is attached to the earliest family by first public availability. A family whose A_f becomes empty after deduplication is dropped from F_d, and the drop is reported.
- **Disease value.** M_d = mean of pct(f) over f ∈ F_d, defined only when |F_d| ≥ 1.

## 4. Aggregate

Over event-bearing diseases: M = (1/n) Σ_d M_d, with equal disease weights. Zero-event diseases are retained in the frame and reported in the all-frame utility. They receive no fabricated value.

## 5. Exclusions reported, never silent

The following are excluded from P_d. Each exclusion is counted per disease and reported:

- an event gene absent from U_d (no as-of-T identity, or screened out as pre-T signal);
- a positive whose event lies in a development-exposed locus: within 500 kb of an adjudicated family of any DEVELOPMENT_EXPOSED disease at (T\*, H\*) ([BIG_0F_SELECTION_CUSTODY.md](BIG_0F_SELECTION_CUSTODY.md) §6);
- an event with AMBIGUOUS or UNRESOLVED status.

## 6. Placebo guard (mandatory)

The combined arm is refit with the biology block permuted within each disease (K = 19; see [V0_FREEZE_STATEMENT.md](V0_FREEZE_STATEMENT.md) §3).

**Why it is needed.** On synthetic data with no biological signal, a gradient-boosting learner gave a mean "lift" of +0.0039 (SE 0.0048, per-world SD ≈ 0.017 over 12 worlds) from the extra feature columns alone ([ADR-022](adr/ADR-022-final-scientific-consistency-closure.md) §4). The mean is not distinguishable from zero, but a single world can show a spurious lift of a third of the planning effect. Capacity parity by configuration does not remove this; a permutation placebo does.

## 7. Why mid-rank and filtering

**Ties.** Attention counts are massively tied at zero. On synthetic data with no signal, adding a pure-noise column produced a spurious lift of **+0.253** when positives were ranked last within ties, and **+0.0015** with mid-ranks. Tie handling other than mid-rank is therefore prohibited.

**Filtering.** Removing other post-T event genes from C_p prevents one discovery from penalizing another. It applies identically to both arms and depends only on the committed outcome ledger, never on ranks.

## 8. Companion metrics (secondary)

- Recall@1% of |U_d| and Recall@K, computed on the same U_d and C_p rules.
- They never replace M as the primary metric in V0.
