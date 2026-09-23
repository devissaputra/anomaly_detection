# Reproducing the Experiment

Run:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/run_experiment.py
```

The train/test split uses `random_state=42` and is stratified on the novelty label. Digit 0 is excluded from the training data.

The Isolation Forest uses 350 trees, `contamination=0.10`, and `random_state=42`.

The script writes ROC-AUC, F1, the novelty digit, and test-set size to `results/metrics.json`.

Because anomaly thresholds can be sensitive to library changes, record your scikit-learn version if you are comparing exact numbers.
