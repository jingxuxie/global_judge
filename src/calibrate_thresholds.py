from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import numpy as np
import pandas as pd

from globaljudge_common import PROTOCOL_NAMES, load_config, read_jsonl


def binary_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    y_true = np.asarray(y_true).astype(int)
    y_pred = np.asarray(y_pred).astype(int)
    tp = int(((y_true == 1) & (y_pred == 1)).sum())
    tn = int(((y_true == 0) & (y_pred == 0)).sum())
    fp = int(((y_true == 0) & (y_pred == 1)).sum())
    fn = int(((y_true == 1) & (y_pred == 0)).sum())
    total = len(y_true)
    accuracy = (tp + tn) / total if total else np.nan
    sensitivity = tp / (tp + fn) if tp + fn else np.nan
    specificity = tn / (tn + fp) if tn + fp else np.nan
    precision = tp / (tp + fp) if tp + fp else np.nan
    recall = sensitivity
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else np.nan
    balanced_accuracy = np.nanmean([sensitivity, specificity])
    return {
        "accuracy": accuracy,
        "balanced_accuracy": balanced_accuracy,
        "f1": f1,
        "sensitivity": sensitivity,
        "specificity": specificity,
        "tp": tp,
        "tn": tn,
        "fp": fp,
        "fn": fn,
    }


def stratified_split(group: pd.DataFrame, fraction: float, rng: np.random.Generator) -> tuple[pd.DataFrame, pd.DataFrame]:
    calibration_parts = []
    test_parts = []
    for _, label_group in group.groupby("human_label"):
        idx = np.array(label_group.index)
        rng.shuffle(idx)
        if len(idx) <= 2:
            n_cal = 1
        else:
            n_cal = int(round(len(idx) * fraction))
            n_cal = min(max(1, n_cal), len(idx) - 1)
        calibration_parts.append(group.loc[idx[:n_cal]])
        test_parts.append(group.loc[idx[n_cal:]])
    calibration = pd.concat(calibration_parts).sample(frac=1, random_state=int(rng.integers(1_000_000_000)))
    test = pd.concat(test_parts).sample(frac=1, random_state=int(rng.integers(1_000_000_000)))
    return calibration, test


def choose_threshold(calibration: pd.DataFrame, candidates: list[int]) -> tuple[int, dict[str, float]]:
    best_threshold = candidates[0]
    best_metrics: dict[str, float] | None = None
    best_key = (-np.inf, -np.inf, -np.inf, np.inf)
    for threshold in candidates:
        pred = (calibration["score"].to_numpy() >= threshold).astype(int)
        metrics = binary_metrics(calibration["human_label"].to_numpy(), pred)
        key = (
            metrics["balanced_accuracy"],
            metrics["f1"] if not np.isnan(metrics["f1"]) else -np.inf,
            metrics["accuracy"],
            -threshold,
        )
        if key > best_key:
            best_key = key
            best_threshold = threshold
            best_metrics = metrics
    return best_threshold, best_metrics or {}


def build_joined_frame(config: dict) -> pd.DataFrame:
    items = pd.DataFrame(read_jsonl(config["paths"]["items_jsonl"]))
    prompts = pd.DataFrame(read_jsonl(config["paths"]["prompts_jsonl"]))
    responses = pd.DataFrame(read_jsonl(config["paths"]["responses_jsonl"]))
    df = responses.merge(prompts[["prompt_id", "protocol_name"]], on="prompt_id", how="left")
    df = df.merge(
        items[["item_id", "human_label", "human_label_text", "candidate_output", "metadata"]],
        on="item_id",
        how="left",
    )
    return df[df["parse_success"] & df["score"].notna() & df["human_label"].notna()].copy()


def calibrate(config: dict) -> pd.DataFrame:
    df = build_joined_frame(config)
    calibration_config = config.get("calibration", {})
    fraction = float(calibration_config.get("fraction", 0.3))
    candidates = list(calibration_config.get("threshold_candidates", [2, 3, 4, 5]))
    baseline_threshold = int(calibration_config.get("baseline_threshold", 4))
    seed = int(config["seed"])
    rows = []

    group_cols = ["judge_model", "language", "dimension", "protocol"]
    for key, group in df.groupby(group_cols):
        group = group.copy()
        if len(group) < 6 or group["human_label"].nunique() < 2:
            continue
        seed_material = repr((seed, key)).encode("utf-8")
        group_seed = int(hashlib.sha256(seed_material).hexdigest()[:8], 16)
        rng = np.random.default_rng(group_seed)
        calibration_split, test_split = stratified_split(group, fraction, rng)
        threshold, calibration_metrics = choose_threshold(calibration_split, candidates)

        for split_name, split_df in [("calibration", calibration_split), ("test", test_split)]:
            baseline_pred = (split_df["score"].to_numpy() >= baseline_threshold).astype(int)
            calibrated_pred = (split_df["score"].to_numpy() >= threshold).astype(int)
            baseline_metrics = binary_metrics(split_df["human_label"].to_numpy(), baseline_pred)
            calibrated_metrics = binary_metrics(split_df["human_label"].to_numpy(), calibrated_pred)
            row = {
                "judge_model": key[0],
                "language": key[1],
                "dimension": key[2],
                "protocol": key[3],
                "protocol_name": PROTOCOL_NAMES.get(key[3], key[3]),
                "split": split_name,
                "n": len(split_df),
                "calibration_fraction": fraction,
                "baseline_threshold": baseline_threshold,
                "calibrated_threshold": threshold,
                "calibration_balanced_accuracy": calibration_metrics.get("balanced_accuracy"),
                "baseline_accuracy": baseline_metrics["accuracy"],
                "calibrated_accuracy": calibrated_metrics["accuracy"],
                "delta_accuracy": calibrated_metrics["accuracy"] - baseline_metrics["accuracy"],
                "baseline_balanced_accuracy": baseline_metrics["balanced_accuracy"],
                "calibrated_balanced_accuracy": calibrated_metrics["balanced_accuracy"],
                "delta_balanced_accuracy": calibrated_metrics["balanced_accuracy"]
                - baseline_metrics["balanced_accuracy"],
                "baseline_f1": baseline_metrics["f1"],
                "calibrated_f1": calibrated_metrics["f1"],
                "delta_f1": calibrated_metrics["f1"] - baseline_metrics["f1"],
            }
            rows.append(row)
    return pd.DataFrame(rows)


def write_summary(results: pd.DataFrame, path: str) -> None:
    lines = ["# Calibration Summary", ""]
    if results.empty:
        lines.append("No eligible groups.")
    else:
        test = results[results["split"] == "test"].copy()
        lines.extend(
            [
                f"Eligible test groups: {len(test)}",
                (
                    "Mean test balanced-accuracy delta: "
                    f"{test['delta_balanced_accuracy'].mean():.3f}"
                ),
                (
                    "Median test balanced-accuracy delta: "
                    f"{test['delta_balanced_accuracy'].median():.3f}"
                ),
                "",
                "## Largest Test Improvements",
                "",
                "```text",
                test.sort_values("delta_balanced_accuracy", ascending=False)
                .head(12)
                .to_string(index=False),
                "```",
                "",
                "## Largest Test Degradations",
                "",
                "```text",
                test.sort_values("delta_balanced_accuracy", ascending=True)
                .head(12)
                .to_string(index=False),
                "```",
            ]
        )
    path_obj = Path(path)
    path_obj.parent.mkdir(parents=True, exist_ok=True)
    path_obj.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/pilot_seahorse_20_combined_explicit.yaml")
    args = parser.parse_args()
    config = load_config(args.config)
    results = calibrate(config)
    output_csv = config["paths"].get(
        "calibration_csv",
        str(Path(config["paths"]["metrics_csv"]).with_name("calibration_thresholds.csv")),
    )
    output_summary = config["paths"].get(
        "calibration_summary_md",
        str(Path(config["paths"]["summary_md"]).with_name("calibration_summary.md")),
    )
    Path(output_csv).parent.mkdir(parents=True, exist_ok=True)
    results.to_csv(output_csv, index=False)
    write_summary(results, output_summary)
    print(f"Wrote calibration results to {output_csv}")
    print(f"Wrote calibration summary to {output_summary}")


if __name__ == "__main__":
    main()
