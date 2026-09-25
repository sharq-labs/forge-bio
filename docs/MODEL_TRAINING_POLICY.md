# Model Training Policy

**Status:** PRE-CODE CANDIDATE

## 1. Problem

"Do not train on future labels" does **not** mean historical supervised learning is impossible.

It means a model evaluated at cutoff T_eval must not use labels that were unknowable at T_eval.

## 2. Nested temporal training

For each training anchor t_i:

1. build features only from a HistoricalKnowledgeView as-of t_i;
2. construct the candidate universe as-of t_i;
3. derive the training endpoint from events in (t_i, t_i + H];
4. require t_i + H <= T_eval for strict training of a model evaluated at T_eval;
5. exclude or censor examples whose outcome window is incomplete.

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

## 5. Hyperparameter tuning

Hyperparameters may be tuned only using development/validation challenges whose labels are permitted by the training policy.

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
- endpoint/horizon;
- split policy;
- seeds;
- knowledge watermark;
- environment digest.

## 10. Failure condition

If any training example uses a label whose qualifying event is after T_eval, the strict confirmatory model is contaminated and the run must fail closed.
