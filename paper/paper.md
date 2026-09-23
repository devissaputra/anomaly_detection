# Novelty / Anomaly Detection on Real Digits: Scientific-Style Technical Report

**Status:** reproducible portfolio report, not peer reviewed.  
**Difficulty:** ★★★  
**Dataset:** Optical Recognition of Handwritten Digits dataset

## Abstract
This project studies a concrete AI Engineering problem using a real public dataset and a fully inspectable pipeline. The project focuses on anomaly detection, novelty detection, Isolation Forest, ROC-AUC. Its central engineering goal is to make data preparation, model fitting, evaluation, and limitations reproducible rather than treating the model as a black box.

## 1. Research objective
Treat one handwritten digit as a held-out novelty class and test Isolation Forest scoring on real images.

## 2. Data
The dataset is **Optical Recognition of Handwritten Digits dataset**. Provenance and the original reference are documented in [`DATA.md`](../DATA.md).

## 3. Method
The implemented pipeline is:
1. Load real images
2. Define novelty class
3. Train on normal classes
4. Score samples
5. Threshold audit

## 4. Evaluation
**Primary metric(s):** ROC-AUC / F1.  
**Validation design:** novel class held out from fit.  
The experiment saves machine-readable metrics and visual diagnostics so claims can be traced to an executable run.

## 5. Results
Generated metrics:
```json
{
  "roc_auc": 0.8119132957842635,
  "f1": 0.2926829268292683,
  "novel_digit": 0,
  "n_test": 629
}
```

## 6. Limitations and validity
Key concern: anomaly-definition dependence. Benchmark performance on one dataset does not imply universal performance. The project is intended to demonstrate research engineering discipline and to provide a base for stronger comparative studies.

## 7. Reproducibility
Run `python src/run_experiment.py` from the repository root after installing `requirements.txt`.

## 8. Next research extension
Add repeated cross-validation or temporal/external validation, stronger baselines, hyperparameter sensitivity, confidence intervals, and a domain-specific error analysis.

## References
- Dataset/reference page: https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_digits.html
