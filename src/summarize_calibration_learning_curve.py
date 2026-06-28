from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np
import pandas as pd

from calibrate_thresholds import build_joined_frame, choose_threshold, binary_metrics
from globaljudge_common import load_config


OUT_DIR = Path("data/analysis")
N_REPEATS = 50
K_PER_CLASS = [1, 2, 4, 8, 12]

RUN_SPECS = [
    ("candidate n50", "configs/candidate_quality_n50_combined_explicit.yaml"),
    ("semantic n30", "configs/semantic_xlsum_n30.yaml"),
    ("wmt reference n30", "configs/wmt_mqm_n30.yaml"),
    ("wmt ref-free n30", "configs/wmt_mqm_ref_free_n30.yaml"),
    ("candidate audit n25", "configs/audit_gpt41mini_n25_combined_explicit.yaml"),
    ("wmt ref-free audit zh-en", "configs/wmt_mqm_ref_free_audit_zh_en_gpt41mini.yaml"),
    ("wmt ref-free audit en-de", "configs/wmt_mqm_ref_free_audit_en_de_gpt41mini.yaml"),
]


def balanced_accuracy_at_threshold(y_true: np.ndarray, y_score: np.ndarray, threshold: int) -> float:
    pred = (y_score >= threshold).astype(int)
    return binary_metrics(y_true, pred)["balanced_accuracy"]


def group_seed(*parts: object) -> int:
    material = repr(parts).encode("utf-8")
    return int(hashlib.sha256(material).hexdigest()[:8], 16)


def evaluate_run(run_name: str, config_path: str) -> list[dict]:
    config = load_config(config_path)
    df = build_joined_frame(config)
    candidates = list(config.get("calibration", {}).get("threshold_candidates", [2, 3, 4, 5]))
    baseline_threshold = int(config.get("calibration", {}).get("baseline_threshold", 4))
    rows = []

    for group_key, group in df.groupby(["judge_model", "language", "dimension", "protocol"]):
        group = group.reset_index(drop=True)
        if len(group) < 10 or group["human_label"].nunique() < 2:
            continue
        y_true = group["human_label"].to_numpy(dtype=int)
        y_score = group["score"].to_numpy(dtype=float)
        label_indices = {label: np.where(y_true == label)[0] for label in [0, 1]}
        max_k = min(len(label_indices[0]), len(label_indices[1])) - 2
        if max_k < 1:
            continue
        base_group_bal = balanced_accuracy_at_threshold(y_true, y_score, baseline_threshold)

        for k in K_PER_CLASS:
            if k > max_k:
                continue
            for repeat in range(N_REPEATS):
                rng = np.random.default_rng(group_seed(run_name, group_key, k, repeat))
                calibration_indices = []
                for label in [0, 1]:
                    shuffled = label_indices[label].copy()
                    rng.shuffle(shuffled)
                    calibration_indices.extend(shuffled[:k])
                calibration_indices = np.asarray(calibration_indices, dtype=int)
                calibration = group.iloc[calibration_indices]
                threshold, _ = choose_threshold(calibration, candidates)
                test_mask = np.ones(len(group), dtype=bool)
                test_mask[calibration_indices] = False
                baseline_bal = balanced_accuracy_at_threshold(
                    y_true[test_mask],
                    y_score[test_mask],
                    baseline_threshold,
                )
                calibrated_bal = balanced_accuracy_at_threshold(
                    y_true[test_mask],
                    y_score[test_mask],
                    threshold,
                )
                rows.append(
                    {
                        "run": run_name,
                        "judge_model": group_key[0],
                        "language": group_key[1],
                        "dimension": group_key[2],
                        "protocol": group_key[3],
                        "k_per_class": k,
                        "n_calibration": 2 * k,
                        "n_test": int(test_mask.sum()),
                        "repeat": repeat,
                        "baseline_threshold": baseline_threshold,
                        "selected_threshold": threshold,
                        "full_group_baseline_balanced_accuracy": base_group_bal,
                        "test_baseline_balanced_accuracy": baseline_bal,
                        "test_calibrated_balanced_accuracy": calibrated_bal,
                        "delta_balanced_accuracy": calibrated_bal - baseline_bal,
                    }
                )
    return rows


def summarize(raw: pd.DataFrame) -> pd.DataFrame:
    grouped = raw.groupby(["run", "k_per_class"], sort=False)
    rows = []
    for key, group in grouped:
        deltas = group["delta_balanced_accuracy"]
        rows.append(
            {
                "run": key[0],
                "k_per_class": key[1],
                "n_calibration": int(2 * key[1]),
                "n_groups": group[["judge_model", "language", "dimension", "protocol"]].drop_duplicates().shape[0],
                "n_trials": len(group),
                "mean_delta_balanced_accuracy": deltas.mean(),
                "median_delta_balanced_accuracy": deltas.median(),
                "delta_ci_low": deltas.quantile(0.025),
                "delta_ci_high": deltas.quantile(0.975),
                "prob_improves": float((deltas > 0).mean()),
                "prob_degrades": float((deltas < 0).mean()),
                "mean_selected_threshold": group["selected_threshold"].mean(),
            }
        )
    return pd.DataFrame(rows)


def write_markdown(summary: pd.DataFrame, path: Path) -> None:
    main = summary[~summary["run"].str.contains("audit")]
    best_by_run = (
        main.sort_values(["run", "mean_delta_balanced_accuracy"], ascending=[True, False])
        .groupby("run")
        .head(1)
    )
    lines = [
        "# Calibration Learning Curve",
        "",
        (
            f"Generated with {N_REPEATS} repeated stratified samples per eligible group and k-per-class "
            "calibration budgets. The fixed baseline threshold is 4."
        ),
        "",
        "## Best Main-Run Calibration Budgets",
        "",
        "```text",
        best_by_run[
            [
                "run",
                "k_per_class",
                "n_calibration",
                "n_groups",
                "mean_delta_balanced_accuracy",
                "median_delta_balanced_accuracy",
                "prob_improves",
                "prob_degrades",
            ]
        ].to_string(index=False),
        "```",
        "",
        "## Full Summary",
        "",
        "```text",
        summary.to_string(index=False),
        "```",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    for run_name, config_path in RUN_SPECS:
        rows.extend(evaluate_run(run_name, config_path))
    raw = pd.DataFrame(rows)
    summary = summarize(raw)
    raw.to_csv(OUT_DIR / "calibration_learning_curve_raw.csv", index=False)
    summary.to_csv(OUT_DIR / "calibration_learning_curve_summary.csv", index=False)
    write_markdown(summary, OUT_DIR / "calibration_learning_curve_summary.md")
    print(f"Wrote {OUT_DIR / 'calibration_learning_curve_raw.csv'}")
    print(f"Wrote {OUT_DIR / 'calibration_learning_curve_summary.csv'}")
    print(f"Wrote {OUT_DIR / 'calibration_learning_curve_summary.md'}")


if __name__ == "__main__":
    main()
