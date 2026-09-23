# Web Portfolio Card

## Novelty / Anomaly Detection on Real Digits

**Track:** AI Engineering  
**Difficulty:** ★★★  
**Dataset:** Optical Recognition of Handwritten Digits  
**Quick description:** Treat digit 0 as a held-out novelty class and test Isolation Forest scoring on real digit images.

### Suggested website image gallery

![Cover](assets/01_cover.svg)

![Novelty detection pipeline](assets/02_data_pipeline.svg)

![Anomaly score view](assets/03_data_or_model.svg)

![Evaluation results](assets/04_evaluation_or_results.svg)

### Suggested portfolio copy
This project tests novelty detection on real handwritten digits by training Isolation Forest only on normal classes and treating digit 0 as unseen novelty. It separates anomaly-score ranking from thresholded detection, reporting ROC-AUC and F1 to show why a useful anomaly ranking can still produce weak binary decisions. The repository includes executable code, real empirical metrics, reproducibility documentation, and a scientific-style technical report.
