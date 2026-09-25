# Research Bundle Evidence Contract

## Identity

**Area:** AI Engineering  
**Study:** label-blind threshold-aware streaming anomaly detection  
**Dataset:** Numenta Anomaly Benchmark, selected \`realKnownCause\` series

## Evidence required for a valid result

A full run must record:

1. exact upstream series names and source-file SHA-256 hashes;
2. anomaly-window file SHA-256;
3. chronological fit/validation/test boundaries and anomaly counts in each segment;
4. causal feature definition and history window;
5. Isolation Forest seed and estimator count;
6. transparent robust-history baseline;
7. label-blind primary threshold policy for 5%, 10% and 15% alert budgets;
8. oracle normal-only threshold sensitivity;
9. label-blind versus annotation-cleaned fit sensitivity;
10. repeated Isolation Forest seeds;
11. history-window sensitivity;
12. ROC-AUC and average precision;
13. precision, recall, F1, balanced accuracy, realized FPR, alert count, false alarms and missed anomaly points;
14. event recall and detection delay;
15. software environment and generated figures.

## Label-use contract

NAB annotations are used to score the primary test results. They are **not** used to remove fit observations or calibrate the primary threshold. Any condition that uses labels before test evaluation must be explicitly named as an oracle or sensitivity condition.

## Non-claims

This bundle does not claim production readiness, universal anomaly semantics, independence of time-series observations, or that point-level F1 alone captures operational utility.

## Review path

1. \`README.md\`
2. \`DATA.md\`
3. \`src/run_experiment.py\`
4. \`results/summary.md\`
5. \`results/metrics.json\`
6. \`tests/test_experiment.py\`
7. \`REPRODUCIBILITY.md\`
8. \`ETHICS.md\`
9. \`paper/paper.md\`
10. \`paper/results.md\`
