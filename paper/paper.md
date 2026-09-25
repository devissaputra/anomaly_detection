# Label-Blind Threshold-Aware Anomaly Detection on Operational Time Series

## Abstract

Anomaly-detection benchmarks can inadvertently blur unsupervised fitting with label-informed threshold selection. This study separates those stages on four real-world Numenta Anomaly Benchmark streams. Isolation Forest is fitted without consulting annotations, primary alert thresholds are calibrated on a later label-blind validation period, and final evaluation uses only the chronological test segment. A robust historical-deviation baseline, repeated random seeds, history-window sensitivity, label-access ablations, point metrics and event detection/delay are included to test whether conclusions survive reasonable methodological choices.

## Research question

How well do Isolation Forest and a transparent robust-history detector identify annotated NAB anomalies when fitting, alert-budget calibration and evaluation are chronologically separated and the primary pipeline remains label-blind?

## Data

Four `realKnownCause` streams and `labels/combined_windows.json` are retrieved from frozen NAB revision `ea702d75cc2258d9d7dd35ca8e5e2539d71f3140`. The runner verifies exact SHA-256 identities before analysis and records them in the generated result manifest.

## Related work

NAB provides real and artificial time-series streams with labeled anomaly windows and a timing-aware benchmark design. This study uses the NAB corpus but does not reproduce its official leaderboard scoring function. Isolation Forest is used as the primary detector because it provides an unsupervised partition-based anomaly score without requiring anomaly labels during fitting.

## Methods

### Temporal protocol

The first 50% of each ordered stream is used for model fitting, the next 20% for threshold calibration, and the last 30% for evaluation.

### Primary detector and temporal features

Isolation Forest uses the current value plus strictly prior-history first-difference, lag and rolling statistics. Missing warm-up features use fixed neutral values. Backward filling from future observations is explicitly prohibited and tested.

### Baseline

A robust historical-deviation score measures absolute deviation from a prior rolling median scaled by prior rolling median absolute deviation with a small causal numerical floor.

### Operating thresholds

Primary thresholds are empirical validation-score quantiles corresponding to 5%, 10% and 15% validation alert budgets. Because annotations are deliberately ignored during calibration, these are not guaranteed false-positive rates. A normal-only validation threshold is an oracle sensitivity condition only.

### Robustness analyses

Isolation Forest is repeated at seeds 13, 29, 42, 73 and 101. History windows 6, 12 and 24 are compared at the primary seed. Annotation-cleaned fitting is compared with the label-blind primary fit.

### Metrics

Ranking uses ROC-AUC and average precision. Operating points report realized false-positive rate, precision, recall, F1, balanced accuracy, alerts, false alarms and missed anomaly points. Event evaluation reports the proportion of test-intersecting anomaly windows detected and delay to first alert.

## Results

Numerical results are generated to `paper/results.md` and `paper/results.tex`. The LaTeX manuscript imports the generated table rather than duplicating values manually. Stream-to-stream performance varies substantially, including realized test false-positive rates, demonstrating that a fixed validation alert budget does not guarantee stable operating behavior after temporal shift.

## Threats to validity

NAB labels are benchmark windows, not universal anomaly definitions. The subset is small and heterogeneous. Temporal dependence violates iid assumptions, repeated seeds are not independent replications, and event utility depends on domain-specific alert cost and timing. The study does not implement the official NAB scoring profile, so its results should not be compared directly with NAB leaderboard scores.

## Reproducibility

The executable protocol is `src/run_experiment.py`; full machine-readable evidence is written to `results/metrics.json`.

## References

- Ahmad, S., Lavin, A., Purdy, S., & Agha, Z. (2017). Unsupervised real-time anomaly detection for streaming data. *Neurocomputing*, 262, 134–147. DOI: 10.1016/j.neucom.2017.04.070.
- Liu, F. T., Ting, K. M., & Zhou, Z.-H. (2008). Isolation Forest. *2008 Eighth IEEE International Conference on Data Mining*, 413–422. DOI: 10.1109/ICDM.2008.17.
