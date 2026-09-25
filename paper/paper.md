# Threshold-Aware Unsupervised Anomaly Detection on Real Operational Time Series

## Status
Research-bundle manuscript scaffold. Results are generated from the current NAB runner and are not hard-coded before execution.

## Question
How well does an Isolation Forest rank labeled anomalies and support explicit false-positive budgets when fitting, threshold calibration and final evaluation are chronologically separated?

## Data
Selected `realKnownCause` streams from the Numenta Anomaly Benchmark.

## Method
Causal rolling features feed an Isolation Forest. Model fitting uses a normal-only early segment; threshold calibration uses a separate normal-only segment; the final chronological segment is untouched until evaluation.

## Metrics
ROC-AUC and average precision assess ranking. Precision, recall, F1, balanced accuracy and realized false-positive rate assess explicit threshold policies.

## Threats to validity
NAB windows are benchmark annotations. Point metrics can reward or penalize detections differently from event-level scoring. Results on these selected streams do not establish production transfer.
