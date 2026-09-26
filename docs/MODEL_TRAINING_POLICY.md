# Model Training Policy

**Status:** PRE-CODE CANDIDATE

## 1. Problem

"Do not train on future labels" does **not** mean historical supervised learning is impossible.

It means a model evaluated at cutoff T_eval must not use labels that were unknowable at T_eval.

## 2. Nested temporal training

For each training anchor t_i:

1. build features only from a HistoricalKnowledgeView as-of t_i;
2. construct the candidate universe as-of t_i;
3. derive the training endpoint from events in (t_i, t_i + H] using the same governed endpoint subtype, PreTGeneticState, novelty, phenotype-match, gene-assignment, replication, and independence policies required by the benchmark;
4. require t_i + H <= T_eval for strict training of a model evaluated at T_eval;
5. exclude or censor examples whose outcome window is incomplete according to the frozen policy;
6. preserve zero-event disease/challenge cases according to the benchmark estimand rather than dropping them for convenience.

Conceptually:

~~~text
training challenge:
features <= t_i
labels in (t_i, t_i+H]
and t_i+H <= T_eval

evaluation challenge:
features <= T_eval
labels after T_eval are sealed
~~~

The model may learn from outcomes that occurred before T_eval. It may not learn from outcomes after T_eval.

## 3. Rolling-origin construction

Training may contain multiple historical anchors:

~~~text
t1 < t2 < t3 < ... < T_eval
~~~

Each anchor is a complete historical challenge with its own:
- historical snapshot;
- candidate universe;
- endpoint window;
- labels;
- provenance.

Do not create one present-day table and attach old timestamps after the fact.

## 4. Entity leakage

Group/split policy must account for dependence.

Depending on the benchmark, prevent inappropriate overlap through:
- disease-group splits;
- disease-family splits;
- target-family splits;
- chemical similarity splits for B-REP;
- temporal splits.

The MAP freezes the split policy.

Where the endpoint is vulnerable to research-opportunity bias, validation also stratifies or controls for historical research intensity/discoverability. Model performance must not be interpreted as biological generalization if it collapses outside high-attention strata.

## 5. Hyperparameter tuning

Hyperparameters may be tuned only using development/validation challenges whose labels are permitted by the training policy.

Validation data are versioned into generations. When validation results materially influence feature/model/endpoint/hyperparameter/threshold selection, the generation becomes SPENT_FOR_MODEL_SELECTION and may not be described later as untouched validation.

SEALED_LOCKBOX labels never participate in:
- feature selection;
- hyperparameter selection;
- early stopping;
- calibration fitting;
- threshold selection.

## 6. Calibration

Calibration for endpoint E/H uses only historical challenges whose endpoint windows are fully observed by the relevant calibration cutoff.

A probability output requires separate calibration evidence.

## 7. Feature selection

Feature definitions are knowledge-bearing when chosen using biomedical hindsight.

Confirmatory runs use:
- preregistered generic feature families; or
- feature sets frozen from development work before lockbox opening.

For E1-CROSSMODAL, the tested arm must exclude pre-T genetic features or isolate them through a preregistered ablation so the result cannot be explained by genetic-signal maturation.

Feature definitions and disease selections influenced by known future successes are documented in BenchmarkDesignProvenance.

## 8. Pretrained models

A pretrained artifact is strict-historical only if its training knowledge horizon is known and <= the anchor/cutoff required by the MAP.

Unknown training composition => historical_safe = UNKNOWN.

Modern-prior experiments are allowed only in the explicitly contaminated operating mode.

## 9. Training artifact

Every trained model records:
- model_id/version;
- code commit;
- config hash;
- training challenge IDs;
- training anchor dates;
- training dataset IDs;
- endpoint family/subtype and horizon;
- estimand/version;
- PreTGeneticState, novelty, phenotype-match, gene-assignment, and replication policy versions;
- validation-generation IDs/statuses used during selection;
- split policy;
- seeds;
- knowledge watermark;
- environment digest.

## 10. Failure condition

A strict confirmatory model fails closed if:
- any training example uses a qualifying event after T_eval;
- a gene-level label depends on an ungoverned modern assignment;
- a purported E1-NOVEL-STRICT label has a pre-T SUGGESTIVE/QUALIFYING/AMBIGUOUS state or bypasses HistoricalNoveltyAudit;
- a training label bypasses required phenotype-match or genetic-replication adjudication;
- future-conditioned filtering changes the training population outside the frozen estimand.
