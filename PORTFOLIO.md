# Portfolio Summary

## Novelty Detection on Handwritten Digits

I train an Isolation Forest only on digits 1 through 9 and treat digit 0 as unseen novelty.

The project shows why anomaly ranking and the final thresholded decision should be evaluated separately.

### Images

![Project overview](assets/01_cover.svg)

![Novelty detection pipeline](assets/02_data_pipeline.svg)

![Anomaly score view](assets/03_data_or_model.svg)

![Evaluation summary](assets/04_evaluation_or_results.svg)

**Key result:** ROC-AUC reached 0.8119, while thresholded F1 was only 0.2927.
