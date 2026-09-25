# Dataset Card — Numenta Anomaly Benchmark

## Source
Numenta Anomaly Benchmark (NAB)  
Repository: https://github.com/numenta/NAB  
Paper: Ahmad et al., *Unsupervised real-time anomaly detection for streaming data*, Neurocomputing (2017), DOI 10.1016/j.neucom.2017.04.070.

## Study subset
The default experiment uses four files under `data/realKnownCause/`. Their timestamps, values and anomaly-window annotations are fetched directly from the upstream GitHub repository at run time.

## Labels
NAB supplies anomaly windows in `labels/combined_windows.json`. This research bundle expands those windows to point-level labels solely to support transparent ranking and threshold evaluation.

## Split
Each series is ordered by timestamp and split chronologically:
- first 50%: candidate model-fit region;
- next 20%: candidate threshold-validation region;
- final 30%: untouched test region.

Known anomaly points are excluded from fit and validation sets. The final test segment retains all labels.

## Leakage boundary
Features are causal rolling features computed from present/past values only. Future values are not used to form a feature row.

## Limitations
Benchmark windows are annotations, not universal definitions of operational failure. Time-series dependence also means ordinary iid interpretations of metrics are inappropriate.
