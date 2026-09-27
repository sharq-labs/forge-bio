# BIG 0F Nuisance Execution Contract

**Status:** NORMATIVE PRE-CODE CONTRACT — SPEC-CLOSED / IMPLEMENTATION-PENDING
**Manifest:** `config/big0f-nuisance-manifest.v2.json`
**Artifact schema:** `schemas/big0f-nuisance-run.v2.schema.json`

## Purpose

The Combined Nuisance comparator used in BIG 0F must be the comparator that was frozen, and it must be **adequate**. A weaker model reported under the same name is not acceptable, and neither is an under-fitted one.

## 1. Frozen content (manifest v2)

- **Families.** 14 mandatory families, each with a frozen level, class, as-of-T definition and transform. These include global attention volume and global attention momentum (ADR-020 §4). A family that cannot be historically reconstructed forces REDESIGN; it is never silently dropped.
- **Disease-level families.** They are constant within a disease, so they enter only through the pre-specified interactions with gene-level opportunity and attention. The central one is the power-maturation pathway: variant opportunity × disease sample-size growth.
- **Literature features.** A feature derived only from publication metadata, counts or timing is attention and belongs in the nuisance block. A biology block may not carry recency-, citation- or title-weighted attention proxies.

## 2. BIG 0F learner (frozen, not merely recorded)

| Element | Value |
|---|---|
| Learner | L2-penalized logistic regression with natural splines (3 df per continuous family) plus the pre-specified interactions |
| Tuning | Penalty from {0.01, 0.1, 1, 10} by inner leave-one-disease-out |
| Ranks | **Out-of-fold only**, from outer leave-one-disease-out cross-fitting. In-sample ranks are prohibited. |
| Labels | Pilot NOVEL-STRICT primary positives |
| Universe | Eligibility-filtered ([NOVEL_STRICT_ELIGIBILITY_RULE.md](NOVEL_STRICT_ELIGIBILITY_RULE.md)) |
| Ties | Mid-rank ([METRIC_EVENT_RANK_PERCENTILE_V1.md](METRIC_EVENT_RANK_PERCENTILE_V1.md)) |
| Tuning objective | Inner leave-one-disease-out, disease-macro EVENT_RANK_PERCENTILE_V1; ties go to the larger penalty |
| Negatives | Every gene in U_d that is not a positive, excluding X_d (the other post-T event genes) |
| Missing features | Zero-filled, with a per-family missing indicator. Values are never imputed from post-T data. |
| Best single-family model | The same learner and tuning, with one family plus that family's pre-specified interactions |
| Headline aggregation | The mean is the disease-macro mean of M_d; the median and the top-1% fraction are taken over family credits pct(f) |
| Change after pilot labels | Prohibited |
| Code identity | The nuisance fitting code digest is bound at S4 and again in the S6 bundle |

## 3. Adequacy check

The adequacy value is (combined model's out-of-fold EVENT_RANK_PERCENTILE_V1) − (best single-family model's out-of-fold value). It must be ≥ the GO bound of gate `NUISANCE_ADEQUACY_MARGIN` in the threshold manifest, recorded as `adequacy.combined_minus_best_single` in the run. A comparator that is weaker than one of its own components is under-fitted. Failure → **REDESIGN**. The BIG 0F learner is never changed, re-tuned or re-specified after pilot labels exist, and a changed learner requires a new protocol version on untouched diseases (custody §9; INV-X6).

## 4. Required execution identity

Every nuisance-run artifact binds:

- the manifest digest;
- per-family source releases, feature-artifact digests and transform digests;
- the candidate-universe digest and screen digest;
- the full out-of-fold rank-output digest;
- the fold assignment;
- the penalty chosen per fold;
- the fitted-model digests;
- the eligible positive-event set digest.

## 5. Rank reconstruction

Headline nuisance metrics are recomputed from the committed ranks, never accepted as free numbers:

- median positive event percentile (higher is better);
- the fraction of positives in the top 1% and top 5%;
- adequacy results.

Every committed positive must appear exactly once. If the universe, ranks or positive set cannot be cross-checked → INCONCLUSIVE.

## 6. Diagnostics

Removing attention families is allowed only as a labelled diagnostic, never as the headline comparator.
