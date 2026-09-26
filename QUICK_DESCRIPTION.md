# Label-Blind Threshold-Aware Anomaly Detection on NAB

This study compares feature-based Isolation Forest with a transparent robust-history baseline on four real NAB streams. The primary pipeline stays label-blind during fitting and alert-budget calibration, then evaluates event detection separately so threshold tuning does not quietly leak benchmark labels into the detector.

At the 5% validation alert budget, the primary Isolation Forest test false-positive rate ranges from 0.0300 to 0.2338 across the four streams. This variation is central to the finding: a fixed calibration budget does not guarantee a stable operating point after temporal change. Repeated seeds and history-window checks describe robustness on these streams, not independent replications.

See [CALCULATIONS.md](CALCULATIONS.md) for evidence and verification scope.
