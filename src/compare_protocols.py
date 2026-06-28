from __future__ import annotations

import argparse
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path("logs/matplotlib").resolve()))

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

from analyze_results import auroc_binary
from globaljudge_common import PROTOCOL_NAMES, load_config, read_jsonl


def spearman_safe(y_true: np.ndarray, y_score: np.ndarray) -> float:
    if len(y_true) < 2 or len(np.unique(y_true)) < 2 or len(np.unique(y_score)) < 2:
        return np.nan
    return float(spearmanr(y_true, y_score).correlation)


def bootstrap_delta(
    values: pd.DataFrame,
    left: str,
    right: str,
    metric: str,
    seed: int,
    n_bootstrap: int,
) -> tuple[float, float, float, float]:
    rng = np.random.default_rng(seed)
    y_true = values["human_label"].to_numpy()
    left_score = values[left].to_numpy()
    right_score = values[right].to_numpy()

    def score_delta(indices: np.ndarray) -> float:
        y = y_true[indices]
        lhs = left_score[indices]
        rhs = right_score[indices]
        if metric == "spearman":
            return spearman_safe(y, rhs) - spearman_safe(y, lhs)
        if metric == "auroc":
            return auroc_binary(y, rhs) - auroc_binary(y, lhs)
        raise ValueError(f"Unknown metric: {metric}")

    point = score_delta(np.arange(len(values)))
    samples = []
    for _ in range(n_bootstrap):
        idx = rng.integers(0, len(values), len(values))
        delta = score_delta(idx)
        if not np.isnan(delta):
            samples.append(delta)
    if not samples:
        return point, np.nan, np.nan, np.nan
    ci_low, ci_high = np.percentile(samples, [2.5, 97.5])
    prob_gt_zero = float(np.mean(np.asarray(samples) > 0))
    return point, float(ci_low), float(ci_high), prob_gt_zero


def build_pairwise(df: pd.DataFrame, seed: int, n_bootstrap: int) -> pd.DataFrame:
    clean = df[df["parse_success"] & df["score"].notna() & df["human_label"].notna()].copy()
    index_cols = ["judge_model", "language", "dimension", "item_id", "human_label"]
    wide = clean.pivot_table(index=index_cols, columns="protocol", values="score", aggfunc="first").reset_index()
    protocols = [col for col in wide.columns if isinstance(col, str) and col.startswith("P")]
    rows = []
    for group_key, group in wide.groupby(["judge_model", "language", "dimension"]):
        for left_idx, left in enumerate(protocols):
            for right in protocols[left_idx + 1 :]:
                paired = group[["human_label", left, right]].dropna()
                if len(paired) < 8:
                    continue
                score_delta = paired[right] - paired[left]
                sp_delta, sp_low, sp_high, sp_prob = bootstrap_delta(
                    paired,
                    left,
                    right,
                    metric="spearman",
                    seed=seed + len(rows) * 17,
                    n_bootstrap=n_bootstrap,
                )
                auroc_delta, auroc_low, auroc_high, auroc_prob = bootstrap_delta(
                    paired,
                    left,
                    right,
                    metric="auroc",
                    seed=seed + len(rows) * 17 + 1,
                    n_bootstrap=n_bootstrap,
                )
                rows.append(
                    {
                        "judge_model": group_key[0],
                        "language": group_key[1],
                        "dimension": group_key[2],
                        "protocol_a": left,
                        "protocol_a_name": PROTOCOL_NAMES.get(left, left),
                        "protocol_b": right,
                        "protocol_b_name": PROTOCOL_NAMES.get(right, right),
                        "n": len(paired),
                        "mean_score_a": paired[left].mean(),
                        "mean_score_b": paired[right].mean(),
                        "mean_score_delta_b_minus_a": score_delta.mean(),
                        "mean_abs_score_shift": score_delta.abs().mean(),
                        "score_disagreement_rate": float((score_delta != 0).mean()),
                        "large_shift_rate_abs_ge_2": float((score_delta.abs() >= 2).mean()),
                        "spearman_delta_b_minus_a": sp_delta,
                        "spearman_delta_ci_low": sp_low,
                        "spearman_delta_ci_high": sp_high,
                        "spearman_prob_delta_gt_0": sp_prob,
                        "auroc_delta_b_minus_a": auroc_delta,
                        "auroc_delta_ci_low": auroc_low,
                        "auroc_delta_ci_high": auroc_high,
                        "auroc_prob_delta_gt_0": auroc_prob,
                    }
                )
    return pd.DataFrame(rows)


def build_language_gaps(metrics: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for key, group in metrics.groupby(["judge_model", "dimension", "protocol"]):
        clean = group.dropna(subset=["spearman", "auroc"])
        if clean.empty:
            continue
        sp_min_idx = clean["spearman"].idxmin()
        sp_max_idx = clean["spearman"].idxmax()
        auroc_min_idx = clean["auroc"].idxmin()
        auroc_max_idx = clean["auroc"].idxmax()
        rows.append(
            {
                "judge_model": key[0],
                "dimension": key[1],
                "protocol": key[2],
                "protocol_name": PROTOCOL_NAMES.get(key[2], key[2]),
                "n_languages": clean["language"].nunique(),
                "mean_spearman": clean["spearman"].mean(),
                "min_spearman": clean.loc[sp_min_idx, "spearman"],
                "min_spearman_language": clean.loc[sp_min_idx, "language"],
                "max_spearman": clean.loc[sp_max_idx, "spearman"],
                "max_spearman_language": clean.loc[sp_max_idx, "language"],
                "spearman_language_gap": clean.loc[sp_max_idx, "spearman"] - clean.loc[sp_min_idx, "spearman"],
                "mean_auroc": clean["auroc"].mean(),
                "min_auroc": clean.loc[auroc_min_idx, "auroc"],
                "min_auroc_language": clean.loc[auroc_min_idx, "language"],
                "max_auroc": clean.loc[auroc_max_idx, "auroc"],
                "max_auroc_language": clean.loc[auroc_max_idx, "language"],
                "auroc_language_gap": clean.loc[auroc_max_idx, "auroc"] - clean.loc[auroc_min_idx, "auroc"],
            }
        )
    return pd.DataFrame(rows)


def write_summary(pairwise: pd.DataFrame, gaps: pd.DataFrame, path: Path) -> None:
    lines = [
        "# Protocol Comparison Summary",
        "",
        "## Largest score shifts",
        "",
    ]
    if not pairwise.empty:
        cols = [
            "language",
            "dimension",
            "protocol_a",
            "protocol_b",
            "n",
            "mean_abs_score_shift",
            "score_disagreement_rate",
            "large_shift_rate_abs_ge_2",
            "mean_score_delta_b_minus_a",
        ]
        lines.append("```text")
        lines.append(
            pairwise.sort_values("mean_abs_score_shift", ascending=False)
            .head(12)[cols]
            .to_string(index=False)
        )
        lines.append("```")
        lines.extend(["", "## Largest paired AUROC deltas", ""])
        cols = [
            "language",
            "dimension",
            "protocol_a",
            "protocol_b",
            "n",
            "auroc_delta_b_minus_a",
            "auroc_delta_ci_low",
            "auroc_delta_ci_high",
            "auroc_prob_delta_gt_0",
        ]
        lines.append("```text")
        lines.append(
            pairwise.reindex(pairwise["auroc_delta_b_minus_a"].abs().sort_values(ascending=False).index)
            .head(12)[cols]
            .to_string(index=False)
        )
        lines.append("```")
    lines.extend(["", "## Largest language gaps", ""])
    if not gaps.empty:
        cols = [
            "dimension",
            "protocol",
            "mean_spearman",
            "min_spearman_language",
            "min_spearman",
            "max_spearman_language",
            "max_spearman",
            "spearman_language_gap",
            "auroc_language_gap",
        ]
        lines.append("```text")
        lines.append(gaps.sort_values("spearman_language_gap", ascending=False).head(12)[cols].to_string(index=False))
        lines.append("```")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/pilot_seahorse_20_combined_explicit.yaml")
    parser.add_argument("--n-bootstrap", type=int, default=1000)
    args = parser.parse_args()

    config = load_config(args.config)
    items = pd.DataFrame(read_jsonl(config["paths"]["items_jsonl"]))
    prompts = pd.DataFrame(read_jsonl(config["paths"]["prompts_jsonl"]))
    responses = pd.DataFrame(read_jsonl(config["paths"]["responses_jsonl"]))
    metrics = pd.read_csv(config["paths"]["metrics_csv"])

    df = responses.merge(prompts[["prompt_id", "protocol_name"]], on="prompt_id", how="left")
    df = df.merge(items[["item_id", "human_label"]], on="item_id", how="left")

    pairwise = build_pairwise(df, int(config["seed"]), args.n_bootstrap)
    gaps = build_language_gaps(metrics)

    metrics_path = Path(config["paths"]["metrics_csv"])
    pairwise_path = metrics_path.with_name(f"{metrics_path.stem}_pairwise_bootstrap.csv")
    gaps_path = metrics_path.with_name(f"{metrics_path.stem}_language_gaps.csv")
    summary_path = metrics_path.with_name(f"{metrics_path.stem}_protocol_comparison_summary.md")

    pairwise.to_csv(pairwise_path, index=False)
    gaps.to_csv(gaps_path, index=False)
    write_summary(pairwise, gaps, summary_path)
    print(f"Wrote pairwise bootstrap results to {pairwise_path}")
    print(f"Wrote language gaps to {gaps_path}")
    print(f"Wrote comparison summary to {summary_path}")


if __name__ == "__main__":
    main()
