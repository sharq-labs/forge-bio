# Benchmark and Source Lifecycle Policy

**Status:** NORMATIVE PRE-CODE V1

## 1. Source lifecycle

Scientific source state is time-dependent.

```text
SourceArtifact
    ↓
SourceLifecycleEvent*
```

Historical admission resolves lifecycle state as-of-T.

Later retractions/corrections are evaluation/current knowledge only and may trigger fragility sensitivity.

## 2. Benchmark exposure budget

Every validation/benchmark generation has an exposure ledger.

Exposure includes:
- aggregate metric reveal;
- subgroup reveal;
- per-case reveal;
- label reveal;
- adjudication discussion;
- methodological changes caused by evaluation feedback.

The benchmark-generation status is not inferred only from access count; disclosure granularity and downstream adaptation matter.

## 3. Exhaustion rule

A benchmark generation cannot remain "untouched" after adaptive feedback.

Possible states:

```text
ACTIVE_CONFIRMATORY
DEVELOPMENT_EXPOSED
EXHAUSTED
RETIRED
```

A new strongest confirmatory claim requires an ACTIVE_CONFIRMATORY generation or a genuinely independent external/prospective evaluation.

## 4. Research-program multiplicity

Repeated benchmark generations, endpoints, horizons, disease subsets, and model families are recorded in a ResearchProgramAttemptLedger.

```text
ResearchProgramAttempt
    attempt_id
    benchmark_family
    benchmark_generation
    endpoint
    horizon
    primary_metric
    model_family
    result_status
    public_or_internal
    relationship_to_prior_attempts
```

Selective reporting of only favorable attempts is prohibited.

## 5. External seal

For strongest confirmatory/prospective work freeze and externally attest:
- MAP digest;
- code/environment digest;
- candidate-universe digest;
- ranking/prediction digest;
- outcome-discovery snapshot/ledger digest where applicable.

External attestation complements, but does not replace, role separation and analyst-hindsight controls.

## 6. Prospective independence

Prediction exposure is recorded before prospective interpretation.

Prospective evidence is stratified by exposure risk.

Publicly released predictions may still be scientifically useful, but are not automatically counted as unexposed independent confirmation if they could have changed research attention.

## 7. Source correction sensitivity

If a later retraction/correction affects a source that materially contributed to a historical prediction:
- retain the original historical run;
- do not rewrite history;
- run a current fragility analysis excluding/correcting the source;
- report whether the prediction depended materially on now-invalidated evidence.

## 8. Drift/migration

Provider/schema/ontology migrations are immutable derivation artifacts.

Never overwrite a historical snapshot to make it conform to a newer ontology/provider representation.

## 9. Stop rule

Do not label a result strongest-confirmatory if:
- its benchmark generation is DEVELOPMENT_EXPOSED or EXHAUSTED;
- adaptive attempts are not fully logged;
- required external seal/attestation is missing;
- prospective target exposure is materially confounded and unreported;
- source lifecycle state is unresolved for outcome-defining evidence.
