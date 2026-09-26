# BIG 0F Nuisance Execution Contract

**Status:** FROZEN PRE-CODE CONTRACT  
**Artifact schema:** `schemas/big0f-nuisance-run.v1.schema.json`

## Purpose

The Combined Nuisance comparator used in BIG 0F must be the comparator that was actually frozen, not a weaker model reported under the same name.

## Required execution identity

Every future nuisance-run artifact must bind:
- the frozen nuisance-manifest digest;
- the exact mandatory feature-family set;
- per-family feature-family records binding each family to source releases, feature artifact digest, and transform digest;
- historical source/release IDs;
- candidate-universe digest;
- full rank-output digest;
- feature-transform digest;
- preprocessing digest;
- learner/model-family identity;
- hyperparameter-search-space digest;
- tuning-budget identity;
- early-stopping-rule identity;
- random-seed-policy identity;
- fitted-model artifact digest.

BIG 0F remains `NUISANCE_ONLY`; semantic biological-evidence features are forbidden.

## Rank reconstruction

Headline nuisance metrics are not accepted as free summary numbers.

The eligible positive-event set is committed by digest before nuisance headroom summaries are accepted. The nuisance run must contain exactly that complete eligible positive set—no omission of poorly ranked positives and no addition of favorable cases.

For every positive event used in the headroom analysis, record:
- disease ID;
- event ID;
- rank position;
- candidate-universe size;
- rank fraction.

The future evaluator must verify the event against the committed candidate universe and full rank output, then recompute median rank, top-1%, and top-5% metrics.

If the candidate universe, full rank output, or complete eligible positive-event set cannot be recovered and cross-checked from the committed digests, the result is `INCONCLUSIVE`.

## Manifest parity

The actual feature-family set must equal the frozen mandatory feature-family set for the headline comparator. Missing mandatory families or silent substitutions force `INCONCLUSIVE`; post-result comparator changes force `REDESIGN`.

Diagnostic ablations may remove attention variables only as labelled sensitivity analyses. They never replace the headline Combined Nuisance comparator.
