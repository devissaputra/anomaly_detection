# Novelty Detection and Threshold Calibration

[![CI](https://github.com/devissaputra/anomaly_detection/actions/workflows/ci.yml/badge.svg)](https://github.com/devissaputra/anomaly_detection/actions/workflows/ci.yml)

![Project overview](assets/01_cover.svg)

A novelty-detection experiment that separates **ranking anomalies** from **choosing an operating threshold**.

Digit `0` is treated as an unseen class. The Isolation Forest is fitted only on digits `1-9`.

## Why this version is stricter

A common anomaly-detection mistake is to accept the estimator's default threshold and report one F1 score. This project instead creates:

- a normal-only training set;
- a separate normal-only validation set for threshold calibration;
- an untouched mixed test set containing normal and novel examples.

No digit-0 example is used to fit the model or calibrate the threshold.

## Data split

- 1,797 handwritten digit images
- 64 pixel features
- digit 0 = novelty class
- 35% mixed test set
- remaining normal examples split 80/20 into model-fit and threshold-validation sets

Recorded sizes:

| Partition | Samples |
|---|---:|
| Normal training | 841 |
| Normal validation | 211 |
| Mixed test | 629 |

## Ranking quality

![Novelty detection pipeline](assets/02_data_pipeline.svg)

Before applying any threshold, the continuous anomaly score achieves:

| Metric | Result |
|---|---:|
| ROC-AUC | **0.8071** |
| Average Precision | **0.2458** |

This says the score contains useful ranking information, but ranking alone does not tell us where to trigger an alert.

## Threshold calibration

![Anomaly score view](assets/03_data_or_model.svg)

Thresholds are selected from **normal validation scores only**. I evaluate three target false-positive budgets:

| Validation FPR budget | Test FPR | Precision | Recall | F1 | Balanced Acc. |
|---|---:|---:|---:|---:|---:|
| 5% | 0.0511 | 0.2750 | 0.1774 | 0.2157 | 0.5631 |
| 10% | 0.1129 | 0.2644 | 0.3710 | 0.3087 | 0.6290 |
| 15% | 0.1834 | 0.2571 | 0.5806 | **0.3564** | **0.6986** |

![Evaluation summary](assets/04_evaluation_or_results.svg)

The trade-off is the point: allowing more false positives raises novelty recall substantially. There is no universally correct operating point. The acceptable false-positive budget depends on the downstream cost of review.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/run_experiment.py
```

## Test

```bash
pip install pytest
pytest
```

Tests verify that digit 0 never leaks into fitting or threshold calibration, threshold ordering is sensible, and all reported operating-point metrics are bounded.

## Limitations

Digit 0 is only a convenient benchmark novelty, not a realistic open-world anomaly distribution. A stronger system would evaluate multiple unseen classes, contamination shifts, threshold uncertainty, streaming drift, and out-of-distribution datasets.
