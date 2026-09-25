# Reproducibility

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. pytest -q
PYTHONPATH=. python src/run_experiment.py
```

## Frozen defaults

- NAB Git revision: `ea702d75cc2258d9d7dd35ca8e5e2539d71f3140`
- NAB DOI: `10.5281/zenodo.1040335`
- NAB license at frozen revision: MIT
- four named `realKnownCause` streams
- chronology: 0.50 fit / 0.20 validation / 0.30 test
- primary training: label-blind
- primary threshold calibration: label-blind validation-score quantile
- robust-history baseline: prior rolling median/MAD deviation with a causal numerical floor
- history window: 12
- history-window sensitivity: 6, 12, 24
- Isolation Forest estimators: 200
- primary seed: 42
- repeated seeds: 13, 29, 42, 73, 101
- validation alert budgets: 0.05, 0.10, 0.15

## Frozen source verification

The runner validates the annotation file and each selected series against the SHA-256 values documented in `DATA.md`. Cached files are subject to the same verification. A source mismatch stops the study and requires an explicit protocol revision.

## Outputs

A full run writes:

- `results/metrics.json`
- `results/summary.md`
- one score/alert figure per selected series under `results/figures/`
- `paper/results.md`
- `paper/results.tex`

## Network and CI boundary

Unit tests are offline and check temporal partitioning, forward-only feature construction, robust scoring, hash validation, threshold behavior, point error accounting and event detection. The empirical workflow separately contacts the frozen NAB source and regenerates evidence.

Repeated seeds measure stochastic sensitivity of Isolation Forest on the same chronological split. They are not independent datasets and are not used as independent replications for inferential p-values.

## Manuscript build

After a successful empirical run:

```bash
cd paper
pdflatex paper.tex
bibtex paper
pdflatex paper.tex
pdflatex paper.tex
```

The LaTeX manuscript imports generated `results.tex`; numerical results should never be manually copied into it.
