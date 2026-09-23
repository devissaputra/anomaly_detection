# Novelty Detection and Threshold Calibration

## Abstract

This project treats digit 0 from the scikit-learn handwritten-digits benchmark as an unseen class. Isolation Forest is fitted only on digits 1 through 9. A separate normal-only validation set calibrates operating thresholds at several false-positive budgets, and a mixed held-out test set evaluates both ranking and thresholded decisions.

## Method

The mixed test set contains 629 examples. The remaining normal examples are divided into 841 training and 211 validation cases. No digit-0 observation is used for fitting or threshold calibration.

The continuous anomaly score reaches ROC-AUC 0.8071 and Average Precision 0.2458. Thresholds are selected from normal validation-score quantiles corresponding to nominal false-positive budgets of 5%, 10%, and 15%.

## Interpretation

Higher false-positive budgets increase novelty recall and F1 in this run, illustrating that ranking quality and operating-point selection are separate engineering decisions. There is no universally optimal threshold without a downstream cost model.

## Limitations

Digit 0 is a convenient benchmark novelty rather than a realistic open-world anomaly distribution. External out-of-distribution datasets, temporal drift, repeated splits, and uncertainty around thresholds are natural extensions.
