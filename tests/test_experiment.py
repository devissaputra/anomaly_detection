from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from src.run_experiment import (
    causal_features,
    event_metrics,
    operating_metrics,
    point_labels,
    robust_history_score,
    temporal_partitions,
    threshold_from_scores,
)


def test_repository_is_research_bundle():
    root = Path(__file__).resolve().parents[1]
    for path in [
        "README.md", "RESEARCH_BUNDLE.md", "DATA.md", "REPRODUCIBILITY.md",
        "ETHICS.md", "src/run_experiment.py", "paper/paper.md",
        ".github/workflows/ci.yml", ".github/workflows/empirical.yml",
    ]:
        assert (root / path).exists(), path


def test_temporal_partitions_are_ordered_and_disjoint():
    a, b, c = temporal_partitions(100)
    assert a[-1] < b[0] < b[-1] < c[0]
    assert len(set(a) | set(b) | set(c)) == 100


def test_features_use_prior_history_for_rolling_statistics():
    X = causal_features([1, 2, 3, 10], window=2)
    assert np.isclose(X.loc[3, "history_mean"], 2.5)
    assert X.loc[3, "value"] == 10


def test_robust_score_flags_large_jump():
    scores = robust_history_score([1, 1.1, .9, 1.0, 1.1, 8.0], window=4)
    assert scores[-1] > scores[-2]


def test_window_to_point_labels():
    stamps = ["2020-01-01", "2020-01-02", "2020-01-03"]
    y = point_labels(stamps, [["2020-01-02", "2020-01-02"]])
    assert y.tolist() == [0, 1, 0]


def test_threshold_budget_ordering():
    scores = np.arange(100, dtype=float)
    t05 = threshold_from_scores(scores, .05)
    t15 = threshold_from_scores(scores, .15)
    assert t05 > t15
    with pytest.raises(ValueError):
        threshold_from_scores(scores, 0)


def test_operating_metrics_count_false_alarms():
    y = [0, 0, 1, 1]
    scores = [0.1, 0.9, 0.2, 0.8]
    m = operating_metrics(y, scores, 0.5)
    assert m["false_alarms"] == 1
    assert m["missed_anomaly_points"] == 1


def test_event_metrics_detects_one_window():
    ts = pd.date_range("2020-01-01", periods=6, freq="h", tz="UTC")
    scores = np.array([0, 0, 0.9, 0.1, 0, 0], dtype=float)
    windows = [["2020-01-01 02:00:00", "2020-01-01 03:00:00"]]
    m = event_metrics(ts, scores, 0.8, windows)
    assert m["events_in_test"] == 1
    assert m["events_detected"] == 1
    assert m["median_delay_seconds"] == 0
