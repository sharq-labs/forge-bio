# BIG 0F Power Input Derivation Contract

**Status:** FROZEN PRE-CODE CONTRACT  
**Artifact:** `config/big0f-power-input-derivation.v1.json`

## Purpose

BIG 0F cannot observe the future paired biological-model lift because the pilot is NUISANCE_ONLY. Therefore a nuisance-rank standard deviation is not accepted as an empirical estimate of the variance of the confirmatory biological increment.

## Primary rule

A GO-capable power conclusion requires variance evidence from at least one **independent DEVELOPMENT dataset or prior development benchmark that measures the same estimand and the same primary metric**.

The variance source must:
- be identified and content-addressed;
- be disjoint from the untouched confirmatory disease/event pool;
- use the same disease-level estimand and primary metric;
- not use BIG 0F biological-arm results;
- expose enough disease-level values to reproduce the variance estimate.

## Conservative planning SD

For each eligible independent source:
1. compute the disease-level sample SD for the same estimand;
2. compute the preregistered bootstrap 95% upper confidence bound for that SD;
3. apply the frozen dependence/cluster adjustment when the source contains materially dependent disease/event groups.

The primary planning SD is the most conservative eligible adjusted upper-bound SD across the frozen eligible sources.

## Pilot nuisance proxy

`PILOT_NUISANCE_DISEASE_MEAN_RANK_SD_PROXY_V1` remains useful only as a planning/sensitivity diagnostic.

It is **not GO-eligible variance evidence**.

If no eligible independent same-estimand variance source exists, the power gate is `INCONCLUSIVE`; the study may not convert the nuisance proxy into a favorable GO.

## Scenario requirements

The power artifact must report:
- the primary conservative scenario;
- every eligible source-specific scenario;
- dependence/cluster sensitivity;
- nuisance-proxy sensitivity;
- required untouched disease count and achieved/estimated power for each scenario.

If scientifically plausible frozen scenarios change the feasibility conclusion, BIG 0F returns `REDESIGN`.

If the primary conservative scenario is below target power even using the feasible untouched pool, BIG 0F returns `NO_GO`.

## Zero-event diseases

Zero-event diseases remain in the study frame. No fabricated rank score is assigned. Power reporting must distinguish the event-bearing disease estimand from the all-frame observed-event utility analysis.

## Leakage prohibition

No Forge Bio biological-model ranking, lift, biological feature selection, biological hyperparameter tuning, or post-result threshold choice may enter BIG 0F power-input derivation.
