from __future__ import annotations

import argparse
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path("logs/matplotlib").resolve()))

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import spearmanr

from globaljudge_common import PROTOCOL_NAMES, load_config, read_jsonl


def auroc_binary(y_true: np.ndarray, y_score: np.ndarray) -> float:
    y_true = np.asarray(y_true).astype(int)
    y_score = np.asarray(y_score).astype(float)
    pos = y_score[y_true == 1]
    neg = y_score[y_true == 0]
    if len(pos) == 0 or len(neg) == 0:
        return np.nan
    wins = 0.0
    total = len(pos) * len(neg)
    for score in pos:
        wins += np.sum(score > neg)
        wins += 0.5 * np.sum(score == neg)
    return float(wins / total)


def bootstrap_spearman(y_true: np.ndarray, y_score: np.ndarray, seed: int, n: int = 500) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    vals = []
    if len(np.unique(y_true)) < 2 or len(np.unique(y_score)) < 2:
        return np.nan, np.nan
    for _ in range(n):
        idx = rng.integers(0, len(y_true), len(y_true))
        if len(np.unique(y_true[idx])) < 2 or len(np.unique(y_score[idx])) < 2:
            continue
        vals.append(spearmanr(y_true[idx], y_score[idx]).correlation)
    if not vals:
        return np.nan, np.nan
    return tuple(np.percentile(vals, [2.5, 97.5]))


def build_metrics(df: pd.DataFrame, seed: int) -> pd.DataFrame:
    rows = []
    group_cols = ["judge_model", "language", "dimension", "protocol"]
    for key, group in df.groupby(group_cols):
        clean = group[group["parse_success"] & group["score"].notna() & group["human_label"].notna()]
        y_true = clean["human_label"].to_numpy()
        y_score = clean["score"].to_numpy()
        if len(clean) >= 2 and len(np.unique(y_true)) >= 2 and len(np.unique(y_score)) >= 2:
            spearman = float(spearmanr(y_true, y_score).correlation)
            ci_low, ci_high = bootstrap_spearman(y_true, y_score, seed)
        else:
            spearman = np.nan
            ci_low = np.nan
            ci_high = np.nan
        rows.append(
            {
                "judge_model": key[0],
                "language": key[1],
                "dimension": key[2],
                "protocol": key[3],
                "protocol_name": PROTOCOL_NAMES.get(key[3], key[3]),
                "n": len(group),
                "n_parsed": len(clean),
                "parse_rate": len(clean) / len(group) if len(group) else np.nan,
                "human_positive_rate": clean["human_label"].mean() if len(clean) else np.nan,
                "mean_judge_score": clean["score"].mean() if len(clean) else np.nan,
                "spearman": spearman,
                "spearman_ci_low": ci_low,
                "spearman_ci_high": ci_high,
                "auroc": auroc_binary(y_true, y_score) if len(clean) else np.nan,
                "estimated_cost_usd": group["api_cost_estimate_usd"].sum(min_count=1),
            }
        )
    return pd.DataFrame(rows)


def build_shifts(df: pd.DataFrame) -> pd.DataFrame:
    clean = df[df["parse_success"] & df["score"].notna()].copy()
    if clean.empty:
        return pd.DataFrame()
    index_cols = ["judge_model", "language", "dimension", "item_id"]
    wide = clean.pivot_table(index=index_cols, columns="protocol", values="score", aggfunc="first")
    rows = []
    protocols = [col for col in wide.columns if isinstance(col, str)]
    for i, left in enumerate(protocols):
        for right in protocols[i + 1 :]:
            delta = (wide[left] - wide[right]).abs().dropna()
            if delta.empty:
                continue
            for key, values in delta.groupby(level=["judge_model", "language", "dimension"]):
                rows.append(
                    {
                        "judge_model": key[0],
                        "language": key[1],
                        "dimension": key[2],
                        "protocol_a": left,
                        "protocol_b": right,
                        "mean_abs_shift": values.mean(),
                        "median_abs_shift": values.median(),
                        "n": len(values),
                    }
                )
    return pd.DataFrame(rows)


def save_heatmap(metrics: pd.DataFrame, path: str) -> None:
    plot_df = metrics.copy()
    if plot_df.empty:
        return
    plot_df["cell"] = plot_df["language"] + " / " + plot_df["dimension"]
    for model, model_df in plot_df.groupby("judge_model"):
        pivot = model_df.pivot_table(index="cell", columns="protocol_name", values="spearman", aggfunc="first")
        plt.figure(figsize=(11, max(4, 0.45 * len(pivot))))
        sns.heatmap(pivot, annot=True, fmt=".2f", cmap="vlag", center=0, vmin=-1, vmax=1)
        plt.title(f"Judge-human Spearman by protocol ({model})")
        plt.tight_layout()
        out = Path(path)
        if len(plot_df["judge_model"].unique()) > 1:
            out = out.with_name(f"{out.stem}_{model}{out.suffix}")
        out.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(out, dpi=180)
        plt.close()


def save_shift_plot(shifts: pd.DataFrame, path: str) -> None:
    if shifts.empty:
        return
    plot_df = shifts.copy()
    plot_df["comparison"] = plot_df["protocol_a"] + " vs " + plot_df["protocol_b"]
    plot_df["language_dimension"] = plot_df["language"] + " / " + plot_df["dimension"]
    plt.figure(figsize=(12, max(4, 0.4 * plot_df["language_dimension"].nunique())))
    sns.barplot(data=plot_df, y="language_dimension", x="mean_abs_shift", hue="comparison")
    plt.xlabel("Mean absolute 1-5 score shift")
    plt.ylabel("")
    plt.legend(loc="best", fontsize="small")
    plt.tight_layout()
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out, dpi=180)
    plt.close()


def write_summary(metrics: pd.DataFrame, shifts: pd.DataFrame, df: pd.DataFrame, path: str) -> None:
    lines = [
        "# Pilot Summary",
        "",
        f"Responses: {len(df)}",
        f"Parsed responses: {int(df['parse_success'].sum()) if len(df) else 0}",
        f"Estimated API cost from returned usage: ${df['api_cost_estimate_usd'].sum(min_count=1):.4f}",
        "",
        "## Best protocol correlations",
        "",
    ]
    if not metrics.empty:
        best = metrics.sort_values("spearman", ascending=False).head(10)
        lines.append("```text")
        lines.append(best.to_string(index=False))
        lines.append("```")
    lines.extend(["", "## Largest protocol shifts", ""])
    if not shifts.empty:
        lines.append("```text")
        lines.append(shifts.sort_values("mean_abs_shift", ascending=False).head(12).to_string(index=False))
        lines.append("```")
    path_obj = Path(path)
    path_obj.parent.mkdir(parents=True, exist_ok=True)
    path_obj.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/pilot_seahorse.yaml")
    args = parser.parse_args()
    config = load_config(args.config)

    items = pd.DataFrame(read_jsonl(config["paths"]["items_jsonl"]))
    prompts = pd.DataFrame(read_jsonl(config["paths"]["prompts_jsonl"]))
    responses = pd.DataFrame(read_jsonl(config["paths"]["responses_jsonl"]))
    if responses.empty:
        raise ValueError("No responses found")

    df = responses.merge(prompts[["prompt_id", "protocol_name"]], on="prompt_id", how="left")
    df = df.merge(items[["item_id", "human_label", "human_label_text", "candidate_output", "metadata"]], on="item_id", how="left")
    metrics = build_metrics(df, int(config["seed"]))
    shifts = build_shifts(df)

    metrics.to_csv(config["paths"]["metrics_csv"], index=False)
    shifts.to_csv(config["paths"]["shifts_csv"], index=False)
    save_heatmap(metrics, config["paths"]["heatmap_png"])
    save_shift_plot(shifts, config["paths"]["shift_png"])
    write_summary(metrics, shifts, df, config["paths"]["summary_md"])
    print(f"Wrote metrics to {config['paths']['metrics_csv']}")
    print(f"Wrote shifts to {config['paths']['shifts_csv']}")
    print(f"Wrote summary to {config['paths']['summary_md']}")


if __name__ == "__main__":
    main()
