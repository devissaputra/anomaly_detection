# Streaming Anomaly Detection Research Bundle

[![CI](https://github.com/devissaputra/anomaly_detection/actions/workflows/ci.yml/badge.svg)](https://github.com/devissaputra/anomaly_detection/actions/workflows/ci.yml)

**Research Bundle · AI Engineering · real-world time-series anomaly detection**

This repository is an empirical anomaly-detection study built on the **Numenta Anomaly Benchmark (NAB)**. The earlier handwritten-digit novelty demonstration has been retired from the research narrative.

## Research question

> How well does an unsupervised Isolation Forest rank and detect labeled anomalies in real operational time series when its alert threshold is calibrated only from a normal validation segment?

The central methodological issue is the separation of **anomaly ranking** from **operating-threshold selection**.

## Real dataset

The default study downloads selected real-world series and the official anomaly windows from the public NAB repository.

Default series:

- `realKnownCause/ambient_temperature_system_failure.csv`
- `realKnownCause/cpu_utilization_asg_misconfiguration.csv`
- `realKnownCause/ec2_request_latency_system_failure.csv`
- `realKnownCause/machine_temperature_system_failure.csv`

NAB contains labeled streaming time series from operational domains. Dataset and benchmark terms remain those of the upstream NAB project.

## Frozen study design

For each series:

1. Download the timestamp/value stream and official NAB anomaly windows.
2. Convert windows to point labels only for evaluation.
3. Build causal features from present/past values: level, first difference, rolling mean and rolling standard deviation.
4. Use the first 50% of the stream as the model-fit region, excluding labeled anomaly points.
5. Use the next 20% as a threshold-calibration region, again using only labeled-normal points for calibration.
6. Evaluate ranking and operating points on the final 30% chronological holdout.
7. Calibrate thresholds for 5%, 10% and 15% validation false-positive budgets.
8. Report ROC-AUC, average precision, test FPR, precision, recall, F1 and balanced accuracy.

The labels are never used as model targets. They are used to construct clean benchmark fit/calibration regions and to score the final holdout.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/run_experiment.py
```

The runner writes one aggregate JSON report under `results/metrics.json`.

## Research-bundle requirements

See [RESEARCH_BUNDLE.md](RESEARCH_BUNDLE.md). A professor can trace the project from dataset provenance through temporal split, threshold policy, code, tests and threats to validity.

## Why threshold policy matters

A detector can rank abnormal points well while still being unusable at a particular alert budget. This bundle therefore refuses to present one default threshold as universally correct. Operating points are explicit policy choices.

## Interpretation boundary

NAB labels are benchmark annotations, not proof that the same detector will transfer to a production system. The selected series are heterogeneous, and point-wise metrics do not fully capture alert timeliness or operational cost. This study is a benchmark of a transparent method, not a production monitoring certification.

## Repository map

```text
README.md
RESEARCH_BUNDLE.md
DATA.md
REPRODUCIBILITY.md
ETHICS.md
src/run_experiment.py
tests/
results/
paper/
CITATION.cff
```
