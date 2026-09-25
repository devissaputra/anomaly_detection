# Dataset Card — Numenta Anomaly Benchmark

## Source

Numenta Anomaly Benchmark (NAB)  
Repository: https://github.com/numenta/NAB  
Primary annotation file: \`labels/combined_windows.json\`

The runner uses the upstream \`master\` branch URLs and records SHA-256 hashes for the annotation JSON and every selected CSV, so the exact bytes used by a result are auditable.

## Frozen study subset

- \`realKnownCause/ambient_temperature_system_failure.csv\`
- \`realKnownCause/cpu_utilization_asg_misconfiguration.csv\`
- \`realKnownCause/ec2_request_latency_system_failure.csv\`
- \`realKnownCause/machine_temperature_system_failure.csv\`

Before freezing the protocol, the split was checked against the official window annotations. All four selected streams have annotated anomaly points in the final 30% chronological test region.

## Labels

NAB supplies anomaly windows. The runner expands each window to point labels only for evaluation and for clearly named oracle/sensitivity analyses.

The **primary** Isolation Forest fit includes every point in the first 50%, regardless of its annotation. The **primary** threshold is the requested quantile of all scores in the next 20%, without removing annotated points.

## Chronological split

- first 50%: label-blind model fit;
- next 20%: label-blind threshold calibration;
- final 30%: untouched evaluation.

This fixed chronology avoids random mixing of future and past observations.

## Causal feature boundary

Feature rows contain the current value, first difference, lag-1 value, and rolling mean/std calculated from **prior observations**. Future samples are never used to construct a feature row.

## Cache and provenance

Downloaded files are cached under \`data/cache/\`, which is gitignored. Generated results record hashes instead of committing raw upstream data.

## Limitations

NAB windows are benchmark annotations rather than ground truth for every possible operational definition of failure. The selected series are heterogeneous, temporally dependent, and too small a subset to establish general production performance.
