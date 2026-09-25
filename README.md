# Label-Blind Streaming Anomaly Detection on NAB

[![CI](https://github.com/devissaputra/anomaly_detection/actions/workflows/ci.yml/badge.svg)](https://github.com/devissaputra/anomaly_detection/actions/workflows/ci.yml)
[![Empirical Study](https://github.com/devissaputra/anomaly_detection/actions/workflows/empirical.yml/badge.svg)](https://github.com/devissaputra/anomaly_detection/actions/workflows/empirical.yml)

**Research Bundle · AI Engineering · time-series anomaly detection**

This repository is a reproducible empirical study on selected **Numenta Anomaly Benchmark (NAB)** real-world streams. Its primary protocol is deliberately label-blind: NAB annotations are not used to fit Isolation Forest or to choose the primary alert threshold. Labels are reserved for final evaluation. Annotation-cleaned alternatives are reported only as oracle sensitivity analyses.

## Research question

> How well do a multivariate Isolation Forest detector and a transparent robust-history baseline rank and detect NAB anomaly events when model fitting, threshold calibration and final evaluation are chronologically separated and primary training is label-blind?

The study separates three questions that are often mixed together: anomaly ranking, alert-budget threshold selection, and event detection/timeliness.

## Real data

The frozen default subset is:

- \`realKnownCause/ambient_temperature_system_failure.csv\`
- \`realKnownCause/cpu_utilization_asg_misconfiguration.csv\`
- \`realKnownCause/ec2_request_latency_system_failure.csv\`
- \`realKnownCause/machine_temperature_system_failure.csv\`

The runner fetches the streams and \`labels/combined_windows.json\` from the upstream NAB repository, caches them outside version control, and records SHA-256 hashes of the source files used.

## Primary design

For every series:

1. Order observations by timestamp.
2. Construct causal features from the current value and **prior-history** lags/rolling statistics.
3. Use the first 50% as label-blind model-fit data.
4. Use the next 20% for label-blind threshold calibration.
5. Evaluate only on the final 30% chronological holdout.
6. Compare Isolation Forest with a transparent robust historical-deviation score.
7. Report alert-budget operating points for 5%, 10% and 15% validation alert rates.
8. Report point-level ROC-AUC/AP and precision/recall/F1/balanced accuracy.
9. Report event-level recall and detection delay for NAB windows intersecting the test period.

## Robustness and sensitivity

- Isolation Forest seeds: 13, 29, 42, 73, 101.
- Feature-history windows: 6, 12 and 24 observations.
- Label-blind threshold calibration is the primary result.
- A normal-only threshold is retained as an **oracle sensitivity analysis**, not as the unsupervised headline result.
- Label-blind model fitting is compared with annotation-cleaned fitting to expose how much benchmark-label access changes the result.

The four selected streams were checked before freezing the design; each has annotated anomaly points in the final 30% test segment.

## Run

\`\`\`bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. pytest -q
PYTHONPATH=. python src/run_experiment.py
\`\`\`

A faster networked smoke run is available with:

\`\`\`bash
PYTHONPATH=. python src/run_experiment.py --quick
\`\`\`

The full experiment generates \`results/metrics.json\`, \`results/summary.md\`, per-series score figures under \`results/figures/\`, and \`paper/results.md\`.

## Why this is a Research Bundle

The repository now contains a real external benchmark, data hashing, chronological holdouts, multiple detector baselines, repeated stochastic runs, alert-budget sensitivity, label-access ablation, feature-window sensitivity, point and event metrics, false-alarm/missed-point counts, offline tests, CI, an empirical workflow, ethics/limitations, and a paper-facing scaffold.

## Interpretation boundary

NAB annotations are benchmark windows, not universal definitions of operational failure. Point-wise metrics can misrepresent a detector that alerts early or late within an event, so event-level metrics are also reported. Results on four streams do not establish production readiness or transfer to another monitoring environment.

## Professor review path

1. \`README.md\`
2. \`DATA.md\`
3. \`src/run_experiment.py\`
4. \`results/summary.md\`
5. \`results/metrics.json\`
6. \`RESEARCH_BUNDLE.md\`
7. \`REPRODUCIBILITY.md\`
8. \`ETHICS.md\`
9. \`paper/paper.md\`
10. \`paper/results.md\`
