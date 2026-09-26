# Calculation guide

## Question and evidence

When do label-blind detectors produce useful alerts?

Four realKnownCause NAB streams; pinned data and annotation hashes.

**Status:** RECORDED EXTERNAL-DATA STUDY | full experiment not rerun in this review.

## Design

Fit on first 50%; calibrate on next 20%; evaluate on final 30%. Compare Isolation Forest with prior-history median/MAD deviations.

## Calculation and interpretation

`Threshold = quantile(validation scores, 1 - budget); FPR = FP / (FP + TN).`

A validation alert budget is the fraction of validation scores above a quantile, not the probability of a false alarm. Event recall and first-alert delay complement point-level metrics. These are not official NAB leaderboard scores.

## Evidence table

Selected recorded values (units and context shown). Full precision below is for traceability, not a claim of measurement precision.

| Quantity | Value | Unit / meaning | JSON path |
|---|---:|---|---|
| ambient_temperature | 0.23377337733773376 | test FPR @ 5% budget | `primary.realKnownCause/ambient_temperature_system_failure.csv.isolation_forest.operating_points.label_blind.0.05.test_fpr` |
| cpu_utilization | 0.10699693564862105 | test FPR @ 5% budget | `primary.realKnownCause/cpu_utilization_asg_misconfiguration.csv.isolation_forest.operating_points.label_blind.0.05.test_fpr` |
| request latency | 0.03003003003003003 | test FPR @ 5% budget | `primary.realKnownCause/ec2_request_latency_system_failure.csv.isolation_forest.operating_points.label_blind.0.05.test_fpr` |
| machine_temperature | 0.09480176211453745 | test FPR @ 5% budget | `primary.realKnownCause/machine_temperature_system_failure.csv.isolation_forest.operating_points.label_blind.0.05.test_fpr` |

Source: [results/metrics.json](results/metrics.json). Values resolve directly from this file when figures are regenerated.

At the 5% validation alert budget, the primary Isolation Forest test false-positive rate ranges from 0.0300 to 0.2338 across the four streams. This variation is central to the finding: a fixed calibration budget does not guarantee a stable operating point after temporal change. Repeated seeds and history-window checks describe robustness on these streams, not independent replications.

## Verification performed in this review

The existing suite requires unavailable dependencies; no full-suite pass is claimed. The complete data/model experiment was not rerun in this review. Stored empirical results were inspected, not independently reproduced from raw data.

The figure-generation check verifies agreement between the selected source values and SVGs. It does not validate the raw dataset, fitted model, identification assumptions, or external generalization.

```bash
python scripts/build_review_figures.py
python scripts/build_review_figures.py --check
```

## Implementation map

Follow these functions to inspect each transformation. Validation helpers and private functions remain visible in the linked modules.

| Function | Purpose / documented behavior |
|---|---|
| [`validate_source_hash`](src/run_experiment.py#L59) | Inspect the explicit implementation and its callers. |
| [`load_windows`](src/run_experiment.py#L69) | Inspect the explicit implementation and its callers. |
| [`load_series`](src/run_experiment.py#L80) | Inspect the explicit implementation and its callers. |
| [`point_labels`](src/run_experiment.py#L95) | Inspect the explicit implementation and its callers. |
| [`causal_features`](src/run_experiment.py#L105) | Inspect the explicit implementation and its callers. |
| [`robust_history_score`](src/run_experiment.py#L124) | Inspect the explicit implementation and its callers. |
| [`temporal_partitions`](src/run_experiment.py#L140) | Inspect the explicit implementation and its callers. |
| [`threshold_from_scores`](src/run_experiment.py#L148) | Inspect the explicit implementation and its callers. |
| [`ranking_metrics`](src/run_experiment.py#L157) | Inspect the explicit implementation and its callers. |
| [`operating_metrics`](src/run_experiment.py#L166) | Inspect the explicit implementation and its callers. |
| [`event_metrics`](src/run_experiment.py#L183) | Inspect the explicit implementation and its callers. |
| [`fit_isolation_forest`](src/run_experiment.py#L209) | Inspect the explicit implementation and its callers. |
| [`score_isolation_forest`](src/run_experiment.py#L220) | Inspect the explicit implementation and its callers. |
| [`evaluate_one`](src/run_experiment.py#L240) | Inspect the explicit implementation and its callers. |
| [`summarize_repeated`](src/run_experiment.py#L299) | Inspect the explicit implementation and its callers. |
| [`window_sensitivity`](src/run_experiment.py#L322) | Inspect the explicit implementation and its callers. |
| [`write_figures`](src/run_experiment.py#L332) | Inspect the explicit implementation and its callers. |
| [`write_summary`](src/run_experiment.py#L357) | Inspect the explicit implementation and its callers. |
| [`build_results_latex`](src/run_experiment.py#L403) | Inspect the explicit implementation and its callers. |
| [`run_experiment`](src/run_experiment.py#L448) | Inspect the explicit implementation and its callers. |
| [`main`](src/run_experiment.py#L520) | Inspect the explicit implementation and its callers. |

## What remains before a stronger research claim

A validation alert budget is the fraction of validation scores above a quantile, not the probability of a false alarm. Event recall and first-alert delay complement point-level metrics. These are not official NAB leaderboard scores. A successful software test is not validation of a scientific construct. New experiments should state their split unit, comparator, outcome, uncertainty procedure and failure criteria before examining final test results.
