from __future__ import annotations

import argparse
import hashlib
import json
import platform
from pathlib import Path
from urllib.request import urlopen

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn
from sklearn.ensemble import IsolationForest
from sklearn.metrics import (
    average_precision_score,
    balanced_accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

PRIMARY_SEED = 42
REPEATED_SEEDS = (13, 29, 42, 73, 101)
NAB_REVISION = "ea702d75cc2258d9d7dd35ca8e5e2539d71f3140"
BASE = f"https://raw.githubusercontent.com/numenta/NAB/{NAB_REVISION}"
UPSTREAM = "https://github.com/numenta/NAB"
NAB_DOI = "10.5281/zenodo.1040335"
NAB_LICENSE = "MIT"
EXPECTED_WINDOWS_SHA256 = "1e1fbc4601321aad8d0f8b3784c8134299379f68f6c1f7777565f8ffd57ab6b1"
SERIES = (
    "realKnownCause/ambient_temperature_system_failure.csv",
    "realKnownCause/cpu_utilization_asg_misconfiguration.csv",
    "realKnownCause/ec2_request_latency_system_failure.csv",
    "realKnownCause/machine_temperature_system_failure.csv",
)
EXPECTED_SERIES_SHA256 = {
    "realKnownCause/ambient_temperature_system_failure.csv": "230b68ccca20f59d562afd5d24ad52939c9b784386bed0054018358bf9120581",
    "realKnownCause/cpu_utilization_asg_misconfiguration.csv": "58ba65dc0737cfbac11b51514476d50c438d44011232144bb8d93f392df58f9f",
    "realKnownCause/ec2_request_latency_system_failure.csv": "98378580aa80157e057c61d59d81daddccc6c65a2c0c800e3f01f603b8215c3f",
    "realKnownCause/machine_temperature_system_failure.csv": "92bf5b87fc7f9bba8ca0b7ec63ccaac8cb4a1371a258e8c29a10ae9c018d82a4",
}
ALERT_BUDGETS = (0.05, 0.10, 0.15)
ROLLING_WINDOW = 12
N_ESTIMATORS = 200


def _download_bytes(url: str) -> bytes:
    with urlopen(url, timeout=60) as response:
        return response.read()


def validate_source_hash(name: str, payload: bytes, expected_sha256: str) -> str:
    actual = hashlib.sha256(payload).hexdigest()
    if actual != expected_sha256:
        raise ValueError(
            f"Unexpected SHA-256 for {name}: {actual}; expected {expected_sha256}. "
            "The frozen research protocol requires the exact validated NAB bytes."
        )
    return actual


def load_windows(cache_dir: str | Path = "data/cache") -> tuple[dict, str]:
    cache = Path(cache_dir)
    cache.mkdir(parents=True, exist_ok=True)
    path = cache / "combined_windows.json"
    payload = path.read_bytes() if path.exists() else _download_bytes(f"{BASE}/labels/combined_windows.json")
    windows_sha = validate_source_hash("labels/combined_windows.json", payload, EXPECTED_WINDOWS_SHA256)
    if not path.exists():
        path.write_bytes(payload)
    return json.loads(payload.decode("utf-8")), windows_sha


def load_series(path: str, cache_dir: str | Path = "data/cache") -> tuple[pd.DataFrame, str]:
    cache = Path(cache_dir) / Path(path).parent
    cache.mkdir(parents=True, exist_ok=True)
    local = cache / Path(path).name
    payload = local.read_bytes() if local.exists() else _download_bytes(f"{BASE}/data/{path}")
    series_sha = validate_source_hash(path, payload, EXPECTED_SERIES_SHA256[path])
    if not local.exists():
        local.write_bytes(payload)
    frame = pd.read_csv(pd.io.common.BytesIO(payload))
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    frame["value"] = pd.to_numeric(frame["value"], errors="raise")
    frame = frame.sort_values("timestamp").reset_index(drop=True)
    return frame, series_sha


def point_labels(timestamps, windows) -> np.ndarray:
    ts = pd.to_datetime(pd.Series(timestamps), utc=True)
    labels = np.zeros(len(ts), dtype=int)
    for start, end in windows:
        lo = pd.to_datetime(start, utc=True)
        hi = pd.to_datetime(end, utc=True)
        labels[(ts >= lo) & (ts <= hi)] = 1
    return labels


def causal_features(values, window: int = ROLLING_WINDOW) -> pd.DataFrame:
    if window < 2:
        raise ValueError("window must be at least 2")
    s = pd.Series(values, dtype=float)
    lag1 = s.shift(1)
    history_mean = lag1.rolling(window, min_periods=2).mean()
    history_std = lag1.rolling(window, min_periods=2).std()
    frame = pd.DataFrame({
        "value": s,
        "diff_1": s.diff(),
        "lag_1": lag1,
        "history_mean": history_mean,
        "history_std": history_std,
    })
    # Missing warm-up values are filled with a fixed neutral value. Never back-fill:
    # back-filling would import information from future timestamps into earlier rows.
    return frame.replace([np.inf, -np.inf], np.nan).fillna(0.0)


def robust_history_score(values, window: int = ROLLING_WINDOW) -> np.ndarray:
    s = pd.Series(values, dtype=float)
    hist = s.shift(1)
    med = hist.rolling(window, min_periods=3).median()
    mad = hist.rolling(window, min_periods=3).apply(
        lambda x: float(np.median(np.abs(x - np.median(x)))), raw=True
    )
    scale = 1.4826 * mad
    # A causal scale floor keeps constant-history windows numerically defined without
    # borrowing any future observation. Warm-up rows remain neutral at score zero.
    scale_floor = 1e-6 * med.abs().clip(lower=1.0)
    scale = scale.where(scale > scale_floor, scale_floor)
    score = (s - med).abs() / scale
    return score.replace([np.inf, -np.inf], np.nan).fillna(0.0).to_numpy(float)


def temporal_partitions(n: int):
    if n < 20:
        raise ValueError("series too short for the frozen temporal protocol")
    fit_end = int(n * 0.50)
    validation_end = int(n * 0.70)
    return np.arange(0, fit_end), np.arange(fit_end, validation_end), np.arange(validation_end, n)


def threshold_from_scores(scores, budget: float) -> float:
    if not 0 < budget < 1:
        raise ValueError("budget must lie in (0, 1)")
    scores = np.asarray(scores, dtype=float)
    if scores.size == 0 or not np.isfinite(scores).all():
        raise ValueError("validation scores must be nonempty and finite")
    return float(np.quantile(scores, 1.0 - budget))


def ranking_metrics(y_true, scores) -> dict:
    y = np.asarray(y_true, dtype=int)
    s = np.asarray(scores, dtype=float)
    return {
        "roc_auc": float(roc_auc_score(y, s)) if len(np.unique(y)) == 2 else None,
        "average_precision": float(average_precision_score(y, s)) if y.sum() else None,
    }


def operating_metrics(y_true, scores, threshold) -> dict:
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
        "alerts": int(prediction.sum()),
        "false_alarms": int(((prediction == 1) & normal).sum()),
        "missed_anomaly_points": int(((prediction == 0) & (y == 1)).sum()),
    }


def event_metrics(timestamps, scores, threshold, windows) -> dict:
    ts = pd.to_datetime(pd.Series(timestamps), utc=True)
    pred = np.asarray(scores) >= threshold
    if len(ts) == 0:
        return {"events_in_test": 0, "events_detected": 0, "event_recall": None, "median_delay_seconds": None}
    lo_test, hi_test = ts.iloc[0], ts.iloc[-1]
    delays, events, detected = [], 0, 0
    for start, end in windows:
        lo = max(pd.to_datetime(start, utc=True), lo_test)
        hi = min(pd.to_datetime(end, utc=True), hi_test)
        if lo > hi:
            continue
        events += 1
        mask = (ts >= lo) & (ts <= hi)
        positions = np.flatnonzero(mask.to_numpy() & pred)
        if positions.size:
            detected += 1
            delays.append((ts.iloc[positions[0]] - lo).total_seconds())
    return {
        "events_in_test": int(events),
        "events_detected": int(detected),
        "event_recall": float(detected / events) if events else None,
        "median_delay_seconds": float(np.median(delays)) if delays else None,
    }


def fit_isolation_forest(X: pd.DataFrame, fit_idx, seed: int):
    model = IsolationForest(
        n_estimators=N_ESTIMATORS,
        contamination="auto",
        random_state=seed,
        n_jobs=-1,
    )
    model.fit(X.iloc[fit_idx])
    return model


def score_isolation_forest(model, X: pd.DataFrame, idx) -> np.ndarray:
    return -model.score_samples(X.iloc[idx])


def _operating_grid(y_test, test_scores, validation_scores, validation_labels, test_ts, windows):
    out = {"label_blind": {}, "oracle_normal_only": {}}
    normal_validation_scores = validation_scores[np.asarray(validation_labels) == 0]
    for budget in ALERT_BUDGETS:
        key = f"{budget:.2f}"
        blind_threshold = threshold_from_scores(validation_scores, budget)
        oracle_threshold = threshold_from_scores(normal_validation_scores, budget)
        blind = operating_metrics(y_test, test_scores, blind_threshold)
        blind["event_metrics"] = event_metrics(test_ts, test_scores, blind_threshold, windows)
        oracle = operating_metrics(y_test, test_scores, oracle_threshold)
        oracle["event_metrics"] = event_metrics(test_ts, test_scores, oracle_threshold, windows)
        out["label_blind"][key] = blind
        out["oracle_normal_only"][key] = oracle
    return out


def evaluate_one(path: str, windows_by_path: dict, seed: int = PRIMARY_SEED, window: int = ROLLING_WINDOW):
    frame, series_sha = load_series(path)
    windows = windows_by_path.get(path, [])
    labels = point_labels(frame["timestamp"], windows)
    X = causal_features(frame["value"], window=window)
    fit_idx, validation_idx, test_idx = temporal_partitions(len(frame))
    y_test = labels[test_idx]

    model = fit_isolation_forest(X, fit_idx, seed)
    validation_scores = score_isolation_forest(model, X, validation_idx)
    test_scores = score_isolation_forest(model, X, test_idx)

    z_scores = robust_history_score(frame["value"], window=window)
    z_validation = z_scores[validation_idx]
    z_test = z_scores[test_idx]

    clean_fit_idx = fit_idx[labels[fit_idx] == 0]
    clean_model = fit_isolation_forest(X, clean_fit_idx, seed)
    clean_test_scores = score_isolation_forest(clean_model, X, test_idx)

    return {
        "data_sha256": series_sha,
        "n": int(len(frame)),
        "split": {
            "fit_n": int(len(fit_idx)),
            "fit_anomalies": int(labels[fit_idx].sum()),
            "validation_n": int(len(validation_idx)),
            "validation_anomalies": int(labels[validation_idx].sum()),
            "test_n": int(len(test_idx)),
            "test_anomalies": int(y_test.sum()),
        },
        "isolation_forest": {
            "ranking": ranking_metrics(y_test, test_scores),
            "operating_points": _operating_grid(
                y_test, test_scores, validation_scores, labels[validation_idx],
                frame["timestamp"].iloc[test_idx].reset_index(drop=True), windows
            ),
        },
        "robust_history_z": {
            "ranking": ranking_metrics(y_test, z_test),
            "operating_points": _operating_grid(
                y_test, z_test, z_validation, labels[validation_idx],
                frame["timestamp"].iloc[test_idx].reset_index(drop=True), windows
            ),
        },
        "label_cleaning_sensitivity": {
            "primary_label_blind_fit": ranking_metrics(y_test, test_scores),
            "annotation_cleaned_fit": ranking_metrics(y_test, clean_test_scores),
            "fit_points_removed_as_annotated_anomalies": int(labels[fit_idx].sum()),
        },
        "plot": {
            "timestamp": frame["timestamp"].iloc[test_idx].astype(str).tolist(),
            "labels": y_test.astype(int).tolist(),
            "if_scores": test_scores.astype(float).tolist(),
            "if_threshold_0_05": float(threshold_from_scores(validation_scores, 0.05)),
        },
    }


def summarize_repeated(per_seed: dict) -> dict:
    out = {}
    for path in SERIES:
        values = {"roc_auc": [], "average_precision": [], "f1_at_0.05": [], "test_fpr_at_0.05": []}
        for seed in per_seed:
            row = per_seed[seed][path]
            values["roc_auc"].append(row["isolation_forest"]["ranking"]["roc_auc"])
            values["average_precision"].append(row["isolation_forest"]["ranking"]["average_precision"])
            op = row["isolation_forest"]["operating_points"]["label_blind"]["0.05"]
            values["f1_at_0.05"].append(op["f1"])
            values["test_fpr_at_0.05"].append(op["test_fpr"])
        out[path] = {}
        for metric, vals in values.items():
            arr = np.asarray([v for v in vals if v is not None], dtype=float)
            out[path][metric] = {
                "mean": float(arr.mean()) if arr.size else None,
                "std": float(arr.std(ddof=1)) if arr.size > 1 else 0.0 if arr.size else None,
                "min": float(arr.min()) if arr.size else None,
                "max": float(arr.max()) if arr.size else None,
            }
    return out


def window_sensitivity(windows_by_path: dict) -> dict:
    out = {}
    for window in (6, 12, 24):
        out[str(window)] = {}
        for path in SERIES:
            result = evaluate_one(path, windows_by_path, seed=PRIMARY_SEED, window=window)
            out[str(window)][path] = result["isolation_forest"]["ranking"]
    return out


def write_figures(primary: dict, results_dir: Path) -> None:
    figures = results_dir / "figures"
    figures.mkdir(parents=True, exist_ok=True)
    for path, result in primary.items():
        plot = result["plot"]
        ts = pd.to_datetime(plot["timestamp"], utc=True)
        scores = np.asarray(plot["if_scores"], dtype=float)
        labels = np.asarray(plot["labels"], dtype=int)
        threshold = plot["if_threshold_0_05"]
        alerts = scores >= threshold
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(ts, scores, linewidth=1, label="Isolation Forest score")
        ax.axhline(threshold, linestyle="--", label="5% validation alert-budget threshold")
        if labels.any():
            ax.scatter(ts[labels == 1], scores[labels == 1], s=12, label="NAB anomaly-window points")
        if alerts.any():
            ax.scatter(ts[alerts], scores[alerts], s=8, marker="x", label="alerts")
        ax.set_title(path)
        ax.set_ylabel("Anomaly score")
        ax.legend(fontsize=7)
        fig.tight_layout()
        fig.savefig(figures / f"{Path(path).stem}_scores.png", dpi=170)
        plt.close(fig)


def write_summary(results: dict, path: Path) -> None:
    lines = [
        "# Empirical Results Summary", "",
        "Generated by \`src/run_experiment.py\`; numerical values should not be edited by hand.", "",
        "## Primary seed 42", "",
        "| Series | IF ROC-AUC | IF AP | Robust-z ROC-AUC | Robust-z AP | IF F1 @ 5% blind budget | IF test FPR |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for series, row in results["primary"].items():
        ir = row["isolation_forest"]["ranking"]
        zr = row["robust_history_z"]["ranking"]
        op = row["isolation_forest"]["operating_points"]["label_blind"]["0.05"]
        fmt = lambda x: "NA" if x is None else f"{x:.4f}"
        lines.append(
            f"| {series} | {fmt(ir['roc_auc'])} | {fmt(ir['average_precision'])} | "
            f"{fmt(zr['roc_auc'])} | {fmt(zr['average_precision'])} | {fmt(op['f1'])} | {fmt(op['test_fpr'])} |"
        )
    lines += [
        "", "## Methodological guardrails", "",
        "The primary fit and validation threshold are label-blind. NAB labels are used only for evaluation. An annotation-cleaned fit and normal-only threshold are retained as oracle sensitivity analyses and are not presented as the primary unsupervised result.", "",
        "Repeated Isolation Forest seeds quantify stochastic sensitivity. Window sizes 6, 12 and 24 quantify feature-window sensitivity. Point metrics are complemented by event detection and delay metrics at each operating point.", "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def _strip_plot(result: dict) -> dict:
    return {k: v for k, v in result.items() if k != "plot"}


def build_results_latex(results: dict) -> str:
    bs = "\\"
    row_end = bs + bs
    names = {
        "realKnownCause/ambient_temperature_system_failure.csv": "Ambient temperature",
        "realKnownCause/cpu_utilization_asg_misconfiguration.csv": "CPU utilization",
        "realKnownCause/ec2_request_latency_system_failure.csv": "EC2 request latency",
        "realKnownCause/machine_temperature_system_failure.csv": "Machine temperature",
    }
    lines = [
        f"{bs}section{{Generated empirical results}}",
        "This section is generated by \\texttt{src/run\_experiment.py}; numerical values should not be hand-edited.",
        "",
        f"NAB revision: \\texttt{{{results['dataset']['revision']}}}.",
        "",
        f"{bs}begin{{table}}[htbp]",
        f"{bs}centering",
        f"{bs}small",
        f"{bs}begin{{tabular}}{{lrrrrrr}}",
        f"{bs}toprule",
        "Series & IF AUC & IF AP & Robust AUC & Robust AP & IF F1 & Test FPR " + row_end,
        f"{bs}midrule",
    ]
    for series, row in results["primary"].items():
        ir = row["isolation_forest"]["ranking"]
        rr = row["robust_history_z"]["ranking"]
        op = row["isolation_forest"]["operating_points"]["label_blind"]["0.05"]
        lines.append(
            f"{names.get(series, series)} & {ir['roc_auc']:.4f} & {ir['average_precision']:.4f} & "
            f"{rr['roc_auc']:.4f} & {rr['average_precision']:.4f} & {op['f1']:.4f} & {op['test_fpr']:.4f} " + row_end
        )
    lines += [
        f"{bs}bottomrule",
        f"{bs}end{{tabular}}",
        f"{bs}caption{{Primary-seed results. Isolation Forest F1 and test false-positive rate use the 5\% label-blind validation alert-budget threshold.}}",
        f"{bs}label{{tab:primary-results}}",
        f"{bs}end{{table}}",
        "",
        f"{bs}paragraph{{Interpretation.}}",
        "Performance varies substantially by stream. The label-blind validation alert budget does not guarantee the same false-positive rate after temporal shift, so realized test false-positive rates are reported explicitly.",
        "",
    ]
    return "\n".join(lines)


def run_experiment(results_dir: str | Path = "results", quick: bool = False):
    windows, windows_sha = load_windows()
    seeds = (PRIMARY_SEED,) if quick else REPEATED_SEEDS
    per_seed, primary_with_plot = {}, None
    for seed in seeds:
        per_seed[str(seed)] = {}
        for path in SERIES:
            result = evaluate_one(path, windows, seed=seed, window=ROLLING_WINDOW)
            per_seed[str(seed)][path] = result
            if seed == PRIMARY_SEED:
                primary_with_plot = primary_with_plot or {}
                primary_with_plot[path] = result

    primary = {path: _strip_plot(result) for path, result in primary_with_plot.items()}
    serializable_per_seed = {
        seed: {path: _strip_plot(result) for path, result in rows.items()}
        for seed, rows in per_seed.items()
    }
    results = {
        "research_bundle": True,
        "status": "quick_smoke_run" if quick else "complete",
        "dataset": {
            "name": "Numenta Anomaly Benchmark",
            "upstream": UPSTREAM,
            "revision": NAB_REVISION,
            "doi": NAB_DOI,
            "license": NAB_LICENSE,
            "combined_windows_sha256": windows_sha,
            "series": list(SERIES),
            "series_sha256": {
                path: primary[path]["data_sha256"] for path in SERIES
            },
        },
        "protocol": {
            "fit_fraction": 0.50,
            "validation_fraction": 0.20,
            "test_fraction": 0.30,
            "primary_training": "label-blind",
            "primary_threshold_calibration": "label-blind validation quantile",
            "alert_budgets": list(ALERT_BUDGETS),
            "rolling_window": ROLLING_WINDOW,
            "isolation_forest_estimators": N_ESTIMATORS,
            "repeated_seeds": list(seeds),
        },
        "primary": primary,
        "repeated_runs": serializable_per_seed,
        "repeated_summary": summarize_repeated(per_seed),
        "window_sensitivity": {"status": "skipped_in_quick_mode"} if quick else window_sensitivity(windows),
        "environment": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "pandas": pd.__version__,
            "scikit_learn": sklearn.__version__,
            "matplotlib": matplotlib.__version__,
        },
    }

    out = Path(results_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "metrics.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    write_summary(results, out / "summary.md")
    write_figures(primary_with_plot, out)
    paper_results = Path("paper/results.md")
    paper_results.parent.mkdir(parents=True, exist_ok=True)
    paper_results.write_text(
        "# Results\n\n" + (out / "summary.md").read_text(encoding="utf-8").replace("# Empirical Results Summary\n\n", "", 1),
        encoding="utf-8",
    )
    Path("paper/results.tex").write_text(build_results_latex(results), encoding="utf-8")
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the NAB anomaly-detection research bundle")
    parser.add_argument("--quick", action="store_true", help="Primary seed only and skip window sensitivity")
    parser.add_argument("--results-dir", default="results")
    args = parser.parse_args()
    result = run_experiment(results_dir=args.results_dir, quick=args.quick)
    print(json.dumps({"status": result["status"], "series": result["dataset"]["series"]}, indent=2))


if __name__ == "__main__":
    main()
