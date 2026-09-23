# Novelty Detection and Threshold Calibration

**Focus:** separating anomaly ranking from operating-threshold selection.

I train an Isolation Forest only on digits 1 through 9 and treat digit 0 as unseen novelty. A normal-only validation set is used to calibrate thresholds at 5%, 10%, and 15% false-positive budgets; digit 0 never enters model fitting or threshold selection.

The held-out anomaly score reaches ROC-AUC 0.8071 and Average Precision 0.2458. As the false-positive budget rises, recall increases from 0.1774 to 0.5806, making the operational trade-off explicit instead of accepting the estimator's default threshold.

The repository includes no-leakage tests, CI, reproducibility documentation, and generated threshold-trade-off diagnostics.
