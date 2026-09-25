# Label-Blind Threshold-Aware Anomaly Detection on NAB

[![CI](https://github.com/devissaputra/anomaly_detection/actions/workflows/ci.yml/badge.svg)](https://github.com/devissaputra/anomaly_detection/actions/workflows/ci.yml)
[![Empirical Study](https://github.com/devissaputra/anomaly_detection/actions/workflows/empirical.yml/badge.svg)](https://github.com/devissaputra/anomaly_detection/actions/workflows/empirical.yml)

**Research Bundle · AI Engineering · time-series anomaly detection**

This repository is a reproducible empirical study on four real-world streams from the **Numenta Anomaly Benchmark (NAB)**. The primary protocol is deliberately label-blind: NAB annotations are not used to fit Isolation Forest or to choose the primary alert threshold. Labels are reserved for evaluation. Annotation-cleaned fitting and normal-only threshold calibration are retained only as clearly named oracle sensitivity analyses.

## Research question

> How well do a feature-based Isolation Forest detector and a transparent robust-history baseline rank and detect NAB anomaly events when fitting, alert-budget calibration and final evaluation are chronologically separated and the primary pipeline remains label-blind?

## Frozen external data

The study uses:

- `realKnownCause/ambient_temperature_system_failure.csv`
- `realKnownCause/cpu_utilization_asg_misconfiguration.csv`
- `realKnownCause/ec2_request_latency_system_failure.csv`
- `realKnownCause/machine_temperature_system_failure.csv`
- `labels/combined_windows.json`

The executable source is pinned to NAB Git revision `ea702d75cc2258d9d7dd35ca8e5e2539d71f3140`, not mutable `master`. Every selected CSV and the annotation file are checked against frozen SHA-256 values before analysis. NAB identifies the benchmark as version 1.1 and provides DOI `10.5281/zenodo.1040335`; the pinned repository revision uses the MIT license.

## Primary design

For every series:

1. Order observations by timestamp.
2. Construct features from the current observation plus strictly prior-history lag and rolling statistics.
3. Fill warm-up history with fixed neutral values only; never backward-fill from future timestamps.
4. Use the first 50% as label-blind model-fit data.
5. Use the next 20% for label-blind threshold calibration.
6. Evaluate only on the final 30% chronological holdout.
7. Compare Isolation Forest with a transparent rolling median/MAD historical-deviation baseline.
8. Report 5%, 10% and 15% **validation alert-budget** operating points.
9. Report point-level ROC-AUC/AP, precision, recall, F1, balanced accuracy and realized test false-positive rate.
10. Report event-level recall and detection delay for NAB windows intersecting the test period.

A validation alert budget is not a guaranteed future false-positive rate. Realized test FPR is measured separately because the stream can shift over time.

## Robustness and sensitivity

- Isolation Forest seeds: 13, 29, 42, 73, 101.
- History windows: 6, 12 and 24 observations.
- Label-blind threshold calibration is the primary result.
- A normal-only threshold is an oracle sensitivity analysis.
- Label-blind fitting is compared with annotation-cleaned fitting to expose the effect of benchmark-label access.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. pytest -q
PYTHONPATH=. python src/run_experiment.py
```

A faster networked smoke run is available with `--quick`.

The full study generates:

- `results/metrics.json`
- `results/summary.md`
- one score/alert figure per selected series under `results/figures/`
- `paper/results.md`
- `paper/results.tex`

## Research-bundle boundary

This repository uses NAB data and anomaly windows but **does not reproduce the official NAB scoring profile or leaderboard score**. Its reported ROC-AUC, AP, F1, false-alarm and event metrics are specific to this transparent protocol and must not be presented as official NAB scores.

NAB annotations are benchmark windows, not universal definitions of failure. Results on four streams do not establish production readiness or transfer to another monitoring environment.

## Professor review path

`README.md` → `DATA.md` → `src/run_experiment.py` → `results/summary.md` → `results/metrics.json` → `RESEARCH_BUNDLE.md` → `REPRODUCIBILITY.md` → `ETHICS.md` → `paper/paper.md`.
