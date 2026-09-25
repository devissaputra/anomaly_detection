# Research Bundle Evidence Contract

## Identity
**Area:** AI Engineering  
**Study:** threshold-aware streaming anomaly detection  
**Dataset:** Numenta Anomaly Benchmark (NAB) realKnownCause series

## Evidence required for an empirical result
- exact upstream series names;
- retrieval URLs and run timestamp;
- chronological split boundaries;
- number of normal/anomalous test points;
- feature-window definition;
- Isolation Forest specification;
- validation false-positive budgets;
- ranking and operating-point metrics;
- software environment.

## Non-claims
This bundle does not claim production readiness, universal anomaly semantics, or that point-wise F1 is the only appropriate benchmark objective.

## Review path
1. `README.md`
2. `DATA.md`
3. `src/run_experiment.py`
4. `tests/test_experiment.py`
5. `REPRODUCIBILITY.md`
6. `paper/paper.md`
7. generated `results/metrics.json`
