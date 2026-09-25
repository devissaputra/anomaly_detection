# Reproducibility

\`\`\`bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. pytest -q
PYTHONPATH=. python src/run_experiment.py
\`\`\`

## Frozen defaults

- NAB upstream branch: \`master\`
- four named \`realKnownCause\` streams
- chronology: 0.50 fit / 0.20 validation / 0.30 test
- primary training: label-blind
- primary threshold calibration: label-blind validation quantile
- robust-history baseline: rolling median/MAD deviation
- history window: 12
- history-window sensitivity: 6, 12, 24
- Isolation Forest estimators: 200
- primary seed: 42
- repeated seeds: 13, 29, 42, 73, 101
- validation alert budgets: 0.05, 0.10, 0.15

## Outputs

The full empirical runner writes:

- \`results/metrics.json\`
- \`results/summary.md\`
- one score/alert figure per selected series under \`results/figures/\`
- \`paper/results.md\`

## Network boundary

Unit tests are offline and exercise temporal splitting, causal features, robust scoring, threshold behavior, point error accounting and event detection. The empirical workflow is separately allowed to contact the official NAB repository.

## Result integrity

The empirical workflow commits regenerated outputs after material changes to the runner. Numerical claims must come from generated artifacts, not from the retired handwritten-digit demonstration or manually entered values.

## Statistical interpretation

Repeated seeds measure stochastic sensitivity of Isolation Forest on the same chronological split. They are not independent datasets and should not be treated as independent replications for inferential p-values.
