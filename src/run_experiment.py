from __future__ import annotations

import json
from pathlib import Path
from urllib.request import urlopen

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import (
    average_precision_score,
    balanced_accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

SEED = 42
BASE = "https://raw.githubusercontent.com/numenta/NAB/master"
SERIES = (
    "realKnownCause/ambient_temperature_system_failure.csv",
    "realKnownCause/cpu_utilization_asg_misconfiguration.csv",
    "realKnownCause/ec2_request_latency_system_failure.csv",
    "realKnownCause/machine_temperature_system_failure.csv",
)
FALSE_POSITIVE_BUDGETS = (0.05, 0.10, 0.15)
ROLLING_WINDOW = 12

def load_windows() -> dict:
    with urlopen(f"{BASE}/labels/combined_windows.json", timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))

def load_series(path: str) -> pd.DataFrame:
    url = f"{BASE}/data/{path}"
    frame = pd.read_csv(url)
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    frame["value"] = pd.to_numeric(frame["value"], errors="raise")
    return frame.sort_values("timestamp").reset_index(drop=True)

def point_labels(timestamps, windows) -> np.ndarray:
    ts = pd.to_datetime(pd.Series(timestamps), utc=True)
    labels = np.zeros(len(ts), dtype=int)
    for start, end in windows:
        lo = pd.to_datetime(start, utc=True)
        hi = pd.to_datetime(end, utc=True)
        labels[(ts >= lo) & (ts <= hi)] = 1
    return labels

def causal_features(values, window: int = ROLLING_WINDOW) -> pd.DataFrame:
    s = pd.Series(values, dtype=float)
    frame = pd.DataFrame({
        "value": s,
        "diff_1": s.diff().fillna(0.0),
        "rolling_mean": s.rolling(window, min_periods=1).mean(),
        "rolling_std": s.rolling(window, min_periods=2).std().fillna(0.0),
    })
    return frame

def temporal_partitions(n: int):
    if n < 20:
        raise ValueError("series too short for the frozen temporal protocol")
    fit_end = int(n * 0.50)
    validation_end = int(n * 0.70)
    return np.arange(0, fit_end), np.arange(fit_end, validation_end), np.arange(validation_end, n)

def threshold_from_normal_scores(scores, budget: float) -> float:
    if not 0 < budget < 1:
        raise ValueError("budget must lie in (0, 1)")
    scores = np.asarray(scores, dtype=float)
    if scores.size == 0:
        raise ValueError("normal validation scores are empty")
    return float(np.quantile(scores, 1.0 - budget))

def operating_metrics(y_true, scores, threshold):
    y = np.asarray(y_true, dtype=int)
    prediction = (np.asarray(scores) >= threshold).astype(int)
    normal = y == 0
    return {
        "threshold": float(threshold),
        "test_fpr": float(((prediction == 1) & normal).sum() / max(1, normal.sum())),
        "precision": float(precision_score(y, prediction, zero_division=0)),
        "recall": float(recall_score(y, prediction, zero_division=0)),
        "f1": float(f1_score(y, prediction, zero_division=0)),
        "balanced_accuracy": float(balanced_accuracy_score(y, prediction)),
    }

def evaluate_one(path: str, windows: dict, seed: int = SEED):
    frame = load_series(path)
    labels = point_labels(frame["timestamp"], windows.get(path, []))
    X = causal_features(frame["value"])
    fit_idx, validation_idx, test_idx = temporal_partitions(len(frame))

    fit_normal = fit_idx[labels[fit_idx] == 0]
    validation_normal = validation_idx[labels[validation_idx] == 0]
    if len(fit_normal) < 20 or len(validation_normal) < 10:
        raise ValueError(f"insufficient normal fit/validation data for {path}")

    model = IsolationForest(n_estimators=350, contamination="auto", random_state=seed)
    model.fit(X.iloc[fit_normal])
    validation_scores = -model.score_samples(X.iloc[validation_normal])
    test_scores = -model.score_samples(X.iloc[test_idx])
    y_test = labels[test_idx]

    ranking = {
        "roc_auc": float(roc_auc_score(y_test, test_scores)) if len(np.unique(y_test)) == 2 else None,
        "average_precision": float(average_precision_score(y_test, test_scores)) if y_test.sum() else None,
    }
    operating = {}
    for budget in FALSE_POSITIVE_BUDGETS:
        threshold = threshold_from_normal_scores(validation_scores, budget)
        operating[f"{budget:.2f}"] = operating_metrics(y_test, test_scores, threshold)

    return {
        "n": int(len(frame)),
        "fit_normal": int(len(fit_normal)),
        "validation_normal": int(len(validation_normal)),
        "test_n": int(len(test_idx)),
        "test_anomalies": int(y_test.sum()),
        "ranking": ranking,
        "operating_points": operating,
    }

def run_experiment(results_dir: str | Path = "results", seed: int = SEED):
    windows = load_windows()
    results = {
        "research_bundle": True,
        "dataset": "Numenta Anomaly Benchmark",
        "upstream": "https://github.com/numenta/NAB",
        "seed": int(seed),
        "rolling_window": ROLLING_WINDOW,
        "series": {},
    }
    for path in SERIES:
        results["series"][path] = evaluate_one(path, windows, seed)

    out = Path(results_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "metrics.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    return results

if __name__ == "__main__":
    print(json.dumps(run_experiment(), indent=2))
