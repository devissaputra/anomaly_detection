from pathlib import Path
import numpy as np

from src.run_experiment import causal_features, point_labels, temporal_partitions, threshold_from_normal_scores

def test_repository_is_research_bundle():
    root = Path(__file__).resolve().parents[1]
    for path in ["README.md","RESEARCH_BUNDLE.md","DATA.md","REPRODUCIBILITY.md",
                 "src/run_experiment.py","paper/paper.md",".github/workflows/ci.yml"]:
        assert (root / path).exists(), path

def test_temporal_partitions_are_ordered_and_disjoint():
    a, b, c = temporal_partitions(100)
    assert a[-1] < b[0] < b[-1] < c[0]
    assert len(set(a) | set(b) | set(c)) == 100

def test_features_are_causal_prefix_statistics():
    X = causal_features([1,2,3], window=2)
    assert X.loc[1, "rolling_mean"] == 1.5
    assert X.loc[2, "rolling_mean"] == 2.5

def test_window_to_point_labels():
    stamps = ["2020-01-01","2020-01-02","2020-01-03"]
    y = point_labels(stamps, [["2020-01-02","2020-01-02"]])
    assert y.tolist() == [0,1,0]

def test_threshold_budget_ordering():
    scores = np.arange(100, dtype=float)
    t05 = threshold_from_normal_scores(scores, .05)
    t15 = threshold_from_normal_scores(scores, .15)
    assert t05 > t15
