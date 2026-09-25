# Dataset Card — Numenta Anomaly Benchmark

## Source

**Numenta Anomaly Benchmark (NAB), version 1.1**  
Repository: https://github.com/numenta/NAB  
Frozen Git revision: `ea702d75cc2258d9d7dd35ca8e5e2539d71f3140`  
DOI: `10.5281/zenodo.1040335`  
License at frozen revision: MIT  
Primary annotation file: `labels/combined_windows.json`

The empirical runner downloads from the exact revision above. Mutable `master` is not used as the scientific source.

## Frozen hashes

- `labels/combined_windows.json`: `1e1fbc4601321aad8d0f8b3784c8134299379f68f6c1f7777565f8ffd57ab6b1`
- `realKnownCause/ambient_temperature_system_failure.csv`: `230b68ccca20f59d562afd5d24ad52939c9b784386bed0054018358bf9120581`
- `realKnownCause/cpu_utilization_asg_misconfiguration.csv`: `58ba65dc0737cfbac11b51514476d50c438d44011232144bb8d93f392df58f9f`
- `realKnownCause/ec2_request_latency_system_failure.csv`: `98378580aa80157e057c61d59d81daddccc6c65a2c0c800e3f01f603b8215c3f`
- `realKnownCause/machine_temperature_system_failure.csv`: `92bf5b87fc7f9bba8ca0b7ec63ccaac8cb4a1371a258e8c29a10ae9c018d82a4`

The runner stops if any loaded source differs from these byte-level identities, including files already present in the local cache.

## Labels and label-use boundary

NAB supplies anomaly windows. The runner expands each window to point labels for final evaluation and for explicitly labelled oracle/sensitivity conditions.

The **primary** Isolation Forest fit includes every point in the first 50%, regardless of its annotation. The **primary** threshold is a quantile of all validation scores in the next 20%, without using labels to remove points.

## Chronological split

- first 50%: label-blind model fit;
- next 20%: label-blind alert-budget calibration;
- final 30%: untouched evaluation.

No random split mixes future and past observations.

## Temporal feature boundary

Feature rows contain the current value, first difference, lag-1 value, and rolling mean/std calculated from prior observations. Missing warm-up history is filled with fixed neutral values rather than backward-filled from future timestamps. The robust-history baseline follows the same one-way temporal rule.

## Cache and provenance

Raw NAB files are cached under `data/cache/`, which is gitignored. The generated result manifest records the pinned revision and the accepted hashes rather than redistributing the source data.

## Limitations

NAB windows are benchmark annotations rather than ground truth for every operational definition of failure. The four selected streams are heterogeneous, temporally dependent, and too small a subset to establish general production performance. This study does not implement the official NAB scoring profile.
