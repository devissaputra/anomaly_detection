# Reproducibility

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
python src/run_experiment.py
```

## Frozen defaults
- NAB upstream branch: master
- four named `realKnownCause` streams
- chronological fractions: 0.50 fit / 0.20 validation / 0.30 test
- rolling window: 12 observations
- Isolation Forest estimators: 350
- seed: 42
- threshold validation FPR budgets: 0.05, 0.10, 0.15

## Network boundary
Tests operate on local fixtures and helper functions. The empirical runner requires internet access to the official NAB repository.

## Result integrity
Metrics from the retired handwritten-digits demonstration are not valid research-bundle evidence and have been removed from the results manifest.
