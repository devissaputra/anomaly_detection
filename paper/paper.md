# Label-Blind Threshold-Aware Anomaly Detection on Operational Time Series

## Abstract

Anomaly-detection benchmarks often blur unsupervised model fitting with label-informed threshold selection. This study separates those stages on selected Numenta Anomaly Benchmark streams. The primary protocol fits Isolation Forest without consulting anomaly annotations, calibrates alert thresholds on a later label-blind validation segment, and evaluates only on the final chronological holdout. A robust historical-deviation baseline, repeated random seeds, feature-window sensitivity, label-access ablations, point-level metrics and event-level detection/delay metrics are included to test whether conclusions survive reasonable methodological choices.

## Research question

How well do Isolation Forest and a transparent robust-history detector identify annotated NAB anomalies when fitting, alert-budget calibration and evaluation are chronologically separated and the primary pipeline is label-blind?

## Data

Four \`realKnownCause\` streams and \`labels/combined_windows.json\` are fetched from the upstream NAB repository. Exact source hashes are recorded in the generated result manifest.

## Methods

### Temporal protocol

The first 50% of each ordered stream is used for model fitting, the next 20% for threshold calibration, and the last 30% for evaluation.

### Primary detector

Isolation Forest uses causal features formed from the current value plus prior-history lag and rolling statistics. NAB labels are not used to remove points from the primary fit region.

### Baseline

A robust historical-deviation score measures absolute deviation from a prior rolling median scaled by rolling median absolute deviation.

### Operating thresholds

The primary threshold is an empirical validation-score quantile corresponding to 5%, 10% or 15% validation alert budgets. A normal-only threshold is reported separately as an oracle sensitivity condition.

### Robustness analyses

Isolation Forest is repeated at seeds 13, 29, 42, 73 and 101. Feature-history windows 6, 12 and 24 are compared at the primary seed. Annotation-cleaned fitting is compared against the label-blind primary fit.

### Metrics

Ranking uses ROC-AUC and average precision. Operating points report realized false-positive rate, precision, recall, F1, balanced accuracy, alerts, false alarms and missed anomaly points. Event evaluation reports the proportion of test-intersecting NAB windows detected and the delay to first alert.

## Results

Numerical results are generated to [results.md](results.md). They are intentionally not typed into this methods file by hand.

## Threats to validity

NAB labels are benchmark windows, not universal anomaly definitions. The selected subset is small and heterogeneous. Temporal dependence violates iid assumptions, repeated seeds are not independent replications, and event utility depends on domain-specific alert cost and timing.

## Reproducibility

The executable protocol is \`src/run_experiment.py\`; full machine-readable evidence is written to \`results/metrics.json\`.
