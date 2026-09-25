# Ethics, Operational Limits and Responsible Use

This project studies anomaly detection on public operational time series. An anomaly score indicates unusual behavior relative to a model and reference period; it does **not** establish that an observation is harmful, fraudulent, unsafe or caused by a particular failure.

## Alert costs

False alarms consume operator attention and can produce alert fatigue. Missed anomalies can delay investigation. For that reason the repository exposes multiple alert budgets and reports realized test false-positive rates instead of hiding threshold choice behind a single default.

## Annotation access

The primary protocol is label-blind before test evaluation. NAB labels are used for scoring. Conditions that use labels to remove fit points or to calibrate thresholds on known-normal validation points are explicitly marked as oracle sensitivity analyses and must not be presented as unsupervised primary evidence.

## Temporal and domain shift

A threshold calibrated on one historical period can fail after workload, seasonality, hardware, software or operational practices change. A production system would require drift monitoring, threshold review, event deduplication, incident-cost modeling and human escalation rules.

## Human impact

Although the selected NAB streams do not directly make decisions about people, anomaly systems can influence operators and downstream automated actions. High-stakes deployment would require documented intervention rules, auditability, rollback paths and review of false-alarm consequences.

This repository is a benchmark study, not a production monitoring certification.
