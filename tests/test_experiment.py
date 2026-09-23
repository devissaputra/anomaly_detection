from pathlib import Path

from src.run_experiment import (
    FALSE_POSITIVE_BUDGETS,
    make_splits,
    run_experiment,
)


def test_novel_digit_never_enters_fit_or_validation():
    _, novelty, train_idx, validation_idx, _ = make_splits()
    assert novelty[train_idx].sum() == 0
    assert novelty[validation_idx].sum() == 0


def test_thresholds_decrease_as_false_positive_budget_increases(tmp_path):
    result = run_experiment(tmp_path, make_plots=False)
    thresholds = [
        result["operating_points"][f"{budget:.2f}"]["threshold"]
        for budget in FALSE_POSITIVE_BUDGETS
    ]
    assert thresholds == sorted(thresholds, reverse=True)


def test_metrics_are_bounded(tmp_path):
    result = run_experiment(tmp_path, make_plots=False)
    assert 0.0 <= result["ranking"]["roc_auc"] <= 1.0
    assert 0.0 <= result["ranking"]["average_precision"] <= 1.0
    for point in result["operating_points"].values():
        for key in ["test_fpr", "precision", "recall", "f1", "balanced_accuracy"]:
            assert 0.0 <= point[key] <= 1.0


def test_repository_structure():
    root = Path(__file__).resolve().parents[1]
    assert (root / ".github/workflows/ci.yml").exists()
    assert (root / "src/run_experiment.py").exists()
    assert (root / "paper/paper.md").exists()
