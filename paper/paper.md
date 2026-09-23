# Novelty Detection on Handwritten Digits

## Question

Can an Isolation Forest trained only on digits 1 through 9 identify digit 0 as something unusual?

## Data

I use scikit-learn's handwritten digits dataset. Each image is 8 × 8 pixels, giving 64 numerical input features.

Digit 0 is treated as the novelty class. The train/test split is stratified on that novelty label, and every digit-0 example is removed from the training set.

## Method

The Isolation Forest uses:

- 350 trees;
- `contamination=0.10`;
- `random_state=42`.

I use the negative model score as the anomaly score. ROC-AUC measures how well that score ranks novel examples, while F1 evaluates the model's built-in thresholded decision.

## Results

| Metric | Result |
|---|---:|
| ROC-AUC | 0.8119 |
| F1 | 0.2927 |
| Test examples | 629 |

## Interpretation

The anomaly score has useful ranking ability, but the thresholded predictions are much weaker.

That difference is the most useful result in this project. Detecting unusual examples is not only about learning a score. The threshold that turns the score into an action also has to be chosen and validated.

## Limitations

The experiment uses only one held-out digit. Isolation Forest also works on flattened pixels, so it does not use the spatial structure of the images.

A stronger version would test every digit as the novelty class, tune the threshold on a validation set, and compare Isolation Forest with One-Class SVM and representation-based methods.

## Reproduce

```bash
pip install -r requirements.txt
python src/run_experiment.py
```
