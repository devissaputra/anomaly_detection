from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_digits
from sklearn.ensemble import IsolationForest
from sklearn.metrics import (
    average_precision_score,
    balanced_accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split


SEED = 42
NOVEL_DIGIT = 0
FALSE_POSITIVE_BUDGETS = (0.05, 0.10, 0.15)


def make_splits(seed: int = SEED):
    X, digits = load_digits(return_X_y=True)
    novelty = (digits == NOVEL_DIGIT).astype(int)
    indices = np.arange(len(digits))

    fit_pool, test_indices = train_test_split(
        indices,
        test_size=0.35,
        random_state=seed,
        stratify=novelty,
    )

    normal_fit_pool = fit_pool[novelty[fit_pool] == 0]
    train_indices, validation_indices = train_test_split(
        normal_fit_pool,
        test_size=0.20,
        random_state=seed,
    )

    return X, novelty, train_indices, validation_indices, test_indices


def threshold_from_normal_scores(
    normal_scores,
    false_positive_budget: float,
) -> float:
    if not 0.0 < false_positive_budget < 1.0:
        raise ValueError("false_positive_budget must be between 0 and 1")
    return float(
        np.quantile(normal_scores, 1.0 - false_positive_budget)
    )


def operating_metrics(y_true, scores, threshold: float):
    prediction = (np.asarray(scores) >= threshold).astype(int)
    normal_mask = np.asarray(y_true) == 0
    false_positive_rate = float(
        ((prediction == 1) & normal_mask).sum() / normal_mask.sum()
    )
    return {
        "threshold": float(threshold),
        "test_fpr": false_positive_rate,
        "precision": float(precision_score(y_true, prediction, zero_division=0)),
        "recall": float(recall_score(y_true, prediction)),
        "f1": float(f1_score(y_true, prediction)),
        "balanced_accuracy": float(
            balanced_accuracy_score(y_true, prediction)
        ),
    }


def run_experiment(
    results_dir: str | Path = "results",
    seed: int = SEED,
    make_plots: bool = True,
):
    X, novelty, train_idx, validation_idx, test_idx = make_splits(seed)

    model = IsolationForest(
        n_estimators=350,
        contamination="auto",
        random_state=seed,
    )
    model.fit(X[train_idx])

    validation_scores = -model.score_samples(X[validation_idx])
    test_scores = -model.score_samples(X[test_idx])
    y_test = novelty[test_idx]

    results = {
        "seed": int(seed),
        "novel_digit": int(NOVEL_DIGIT),
        "n_train_normal": int(len(train_idx)),
        "n_validation_normal": int(len(validation_idx)),
        "n_test": int(len(test_idx)),
        "ranking": {
            "roc_auc": float(roc_auc_score(y_test, test_scores)),
            "average_precision": float(
                average_precision_score(y_test, test_scores)
            ),
        },
        "operating_points": {},
    }

    for budget in FALSE_POSITIVE_BUDGETS:
        threshold = threshold_from_normal_scores(
            validation_scores,
            budget,
        )
        results["operating_points"][f"{budget:.2f}"] = operating_metrics(
            y_test,
            test_scores,
            threshold,
        )

    output = Path(results_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "metrics.json").write_text(
        json.dumps(results, indent=2),
        encoding="utf-8",
    )

    if make_plots:
        figures = output / "figures"
        figures.mkdir(parents=True, exist_ok=True)

        plt.figure(figsize=(7, 5))
        plt.hist(
            test_scores[y_test == 0],
            bins=30,
            alpha=0.7,
            label="normal digits",
        )
        plt.hist(
            test_scores[y_test == 1],
            bins=20,
            alpha=0.7,
            label="novel digit 0",
        )
        plt.xlabel("Anomaly score")
        plt.ylabel("Count")
        plt.title("Held-out novelty-score distributions")
        plt.legend()
        plt.tight_layout()
        plt.savefig(figures / "score_distributions.png", dpi=150)
        plt.close()

        budgets = list(FALSE_POSITIVE_BUDGETS)
        recalls = [
            results["operating_points"][f"{budget:.2f}"]["recall"]
            for budget in budgets
        ]
        f1_values = [
            results["operating_points"][f"{budget:.2f}"]["f1"]
            for budget in budgets
        ]
        plt.figure(figsize=(7, 5))
        plt.plot(budgets, recalls, marker="o", label="recall")
        plt.plot(budgets, f1_values, marker="o", label="F1")
        plt.xlabel("Validation false-positive budget")
        plt.ylabel("Score")
        plt.title("Threshold trade-off")
        plt.legend()
        plt.tight_layout()
        plt.savefig(figures / "threshold_tradeoff.png", dpi=150)
        plt.close()

    return results


def main() -> None:
    print(json.dumps(run_experiment(), indent=2))


if __name__ == "__main__":
    main()
