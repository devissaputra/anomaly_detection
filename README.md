# 05. Novelty / Anomaly Detection on Real Digits ★★★

![Cover](assets/01_cover.svg)

> **Quick description:** Treat handwritten digit `0` as a held-out novelty class and test Isolation Forest scoring on real digit images.

## Why this project matters
This AI Engineering project demonstrates a genuine **novelty-detection** setup rather than ordinary supervised classification. The model is trained only on examples considered normal, while the held-out digit `0` is treated as unseen novelty during evaluation.

The project uses the real **Optical Recognition of Handwritten Digits** dataset from scikit-learn and evaluates both anomaly-score ranking and thresholded novelty decisions.

## Dataset
- **Dataset:** Optical Recognition of Handwritten Digits
- **Source:** scikit-learn `load_digits`
- **Image representation:** 8×8 grayscale images flattened to 64 numerical features
- **Novel class:** digit `0`
- **Data provenance and usage:** [DATA.md](DATA.md)

## Research pipeline
![Novelty detection pipeline](assets/02_data_pipeline.svg)

### Processing steps
1. Load the real handwritten-digit dataset.
2. Mark digit `0` as the novelty class and digits `1–9` as normal.
3. Create a stratified 65/35 train-test split.
4. Remove all digit-`0` examples from the training subset.
5. Fit an **Isolation Forest** with 350 trees and contamination set to 0.10.
6. Score every test observation for anomalousness.
7. Evaluate ranking with ROC-AUC and thresholded detection with F1.

## Anomaly-score view
![Anomaly score separation](assets/03_data_or_model.svg)

Isolation Forest does not learn a digit classifier. Instead, it isolates observations through random partitioning. Examples that are isolated unusually quickly receive stronger anomaly scores.

The score distributions can overlap, so a model may rank novelty reasonably well while still making weak thresholded decisions.

## Evaluation results
![Evaluation results](assets/04_evaluation_or_results.svg)

Generated metrics from the included experiment:

```json
{
  "roc_auc": 0.8119132957842635,
  "f1": 0.2926829268292683,
  "novel_digit": 0,
  "n_test": 629
}
```

### Interpretation
- **ROC-AUC = 0.8119** indicates useful separation between normal digits and the held-out digit `0`.
- **F1 = 0.2927** is much weaker, showing that the model's default anomaly threshold is not well aligned with the novelty-detection objective.
- This difference is important: **ranking quality and threshold quality are not the same thing**.
- The result should not be interpreted as evidence that Isolation Forest is universally effective for image novelty detection.

## Reproduce
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python src/run_experiment.py
```

Metrics are written to `results/metrics.json`.

## Research documentation
- [Scientific-style technical report](paper/paper.md)
- [Quick description](QUICK_DESCRIPTION.md)
- [Website-ready portfolio entry](PORTFOLIO.md)
- [Data provenance](DATA.md)
- [Reproducibility notes](REPRODUCIBILITY.md)
- [Ethics and responsible use](ETHICS.md)
- [Citation metadata](CITATION.cff)

## Difficulty
**★★★ — intermediate**

## Academic integrity
This repository is a research portfolio artifact, not a peer-reviewed publication. Reported metrics are generated from the included code on the stated real dataset.

## Stronger research extension
A publication-oriented extension would tune the decision threshold on a validation set, compare Isolation Forest with One-Class SVM and autoencoder baselines, evaluate multiple held-out digits, report precision-recall curves, study contamination sensitivity, and test whether learned image representations improve novelty detection.
