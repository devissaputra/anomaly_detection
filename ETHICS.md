# Ethics, Operational Limits and Responsible Use

This project studies anomaly detection on public operational time series. An anomaly score indicates unusual behavior relative to a model and reference period; it does **not** establish that an observation is harmful, fraudulent, unsafe or caused by a particular failure.

## Alert costs

False alarms consume operator attention and can produce alert fatigue. Missed anomalies can delay investigation. The repository therefore exposes multiple validation alert budgets and reports realized test false-positive rates rather than implying that a validation budget transfers unchanged into the future.

## Annotation access

The primary protocol is label-blind before final evaluation. NAB labels are used for scoring. Conditions that remove annotated fit points or calibrate thresholds on known-normal validation points are explicitly marked as oracle sensitivity analyses.

## Temporal and domain shift

A threshold calibrated on one historical period can fail after workload, seasonality, hardware, software or operational practices change. Production use would require drift monitoring, threshold review, event deduplication, incident-cost modeling and human escalation rules.

## Human impact

Although these selected streams do not directly make decisions about people, anomaly systems can influence operators and downstream automated actions. High-stakes deployment would require documented intervention rules, auditability, rollback paths and review of false-alarm consequences.

## Benchmark-score boundary

Using NAB data does not mean this repository reproduces the official NAB scoring system or leaderboard. The study reports its own transparent ranking, alert-budget, point-error and event metrics; these must not be presented as official NAB scores.

This repository is a benchmark study, not a production monitoring certification.
