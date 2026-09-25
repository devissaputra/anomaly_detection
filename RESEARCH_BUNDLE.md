# Research Bundle Evidence Contract

## Identity

**Area:** AI Engineering  
**Study:** label-blind threshold-aware time-series anomaly detection  
**Dataset:** Numenta Anomaly Benchmark (NAB), four selected `realKnownCause` streams  
**Frozen revision:** `ea702d75cc2258d9d7dd35ca8e5e2539d71f3140`

## Evidence required for a valid full result

A valid run must record or generate:

1. exact pinned upstream Git revision, DOI/license, selected series and source-file SHA-256 hashes;
2. validated anomaly-window SHA-256;
3. chronological fit/validation/test boundaries and anomaly counts;
4. forward-only feature definition and history window;
5. Isolation Forest seed and estimator count;
6. transparent robust-history baseline;
7. label-blind primary threshold policy for 5%, 10% and 15% validation alert budgets;
8. oracle normal-only threshold sensitivity;
9. label-blind versus annotation-cleaned fitting sensitivity;
10. repeated Isolation Forest seeds;
11. history-window sensitivity;
12. ROC-AUC and average precision;
13. precision, recall, F1, balanced accuracy, realized test FPR, alert count, false alarms and missed anomaly points;
14. event recall and detection delay;
15. software environment and generated figures;
16. generated Markdown and LaTeX result artifacts.

## Label-use contract

NAB annotations score primary test results. They are not used to remove fit observations or calibrate the primary threshold. Any condition using labels before final evaluation must be explicitly marked oracle/sensitivity.

## Temporal leakage contract

No feature or baseline score may use a future observation to construct an earlier timestamp. Missing warm-up lag/rolling values must never be backward-filled. Tests compare identical prefixes with different future tails to enforce this property.

## Benchmark-score boundary

This bundle does not implement the official NAB scoring profile. Its reported metrics are not NAB leaderboard scores. A 5%, 10% or 15% label-blind validation alert budget is also not a guaranteed future false-positive rate.

## Non-claims

The bundle does not claim production readiness, universal anomaly semantics, independence of time-series observations, causal failure diagnosis, or that point-level F1 alone captures operational utility.
