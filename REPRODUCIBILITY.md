# Reproducing the experiment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/run_experiment.py
```

Seed 42 controls the mixed hold-out split, the normal-only train/validation split, and Isolation Forest.

Digit 0 is excluded from both model fitting and threshold calibration. Thresholds are selected only from normal validation scores at nominal false-positive budgets of 5%, 10%, and 15%, then frozen before evaluation on the mixed test set.

Outputs are written to `results/metrics.json` and `results/figures/`.

Run `pytest` to verify the no-leakage split and threshold behaviour. GitHub Actions runs those tests automatically.
