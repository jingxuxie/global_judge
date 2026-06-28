from __future__ import annotations

from pathlib import Path

import pandas as pd

from globaljudge_common import PROTOCOL_NAMES


OUT_DIR = Path("data/analysis")

RUN_SPECS = [
    {
        "run": "candidate n50",
        "metrics": "data/analysis/candidate_n50_combined_explicit_metrics.csv",
        "pairwise": "data/analysis/candidate_n50_combined_explicit_metrics_pairwise_bootstrap.csv",
    },
    {
        "run": "semantic n30",
        "metrics": "data/analysis/semantic_xlsum_n30_metrics.csv",
        "pairwise": "data/analysis/semantic_xlsum_n30_metrics_pairwise_bootstrap.csv",
    },
    {
        "run": "wmt reference n30",
        "metrics": "data/analysis/wmt_mqm_n30_metrics.csv",
        "pairwise": "data/analysis/wmt_mqm_n30_metrics_pairwise_bootstrap.csv",
    },
    {
        "run": "wmt ref-free n30",
        "metrics": "data/analysis/wmt_mqm_ref_free_n30_metrics.csv",
        "pairwise": "data/analysis/wmt_mqm_ref_free_n30_metrics_pairwise_bootstrap.csv",
    },
    {
        "run": "candidate audit n25",
        "metrics": "data/analysis/audit_gpt41mini_n25_combined_explicit_metrics.csv",
        "pairwise": "data/analysis/audit_gpt41mini_n25_combined_explicit_metrics_pairwise_bootstrap.csv",
    },
    {
        "run": "wmt ref-free audit",
        "metrics": "data/analysis/wmt_mqm_ref_free_audit_zh_en_gpt41mini_metrics.csv",
        "pairwise": "data/analysis/wmt_mqm_ref_free_audit_zh_en_gpt41mini_metrics_pairwise_bootstrap.csv",
    },
    {
        "run": "wmt ref-free audit",
        "metrics": "data/analysis/wmt_mqm_ref_free_audit_en_de_gpt41mini_metrics.csv",
        "pairwise": "data/analysis/wmt_mqm_ref_free_audit_en_de_gpt41mini_metrics_pairwise_bootstrap.csv",
    },
]


def protocol_label(protocol: str | None) -> str:
    if protocol is None or pd.isna(protocol):
        return ""
    return PROTOCOL_NAMES.get(str(protocol), str(protocol))


def significant_auroc_pairs(pairwise: pd.DataFrame) -> pd.Series:
    if pairwise.empty:
        return pd.Series(dtype=bool)
    return (pairwise["auroc_delta_ci_low"] > 0) | (pairwise["auroc_delta_ci_high"] < 0)


def summarize_cells() -> pd.DataFrame:
    rows = []
    for spec in RUN_SPECS:
        metrics = pd.read_csv(spec["metrics"])
        pairwise = pd.read_csv(spec["pairwise"])
        for (judge_model, language, dimension), group in metrics.groupby(["judge_model", "language", "dimension"]):
            clean = group.dropna(subset=["auroc", "spearman"]).copy()
            if len(clean) < 2:
                continue
            best = clean.sort_values(["auroc", "spearman"], ascending=False).iloc[0]
            worst = clean.sort_values(["auroc", "spearman"], ascending=True).iloc[0]
            paired = pairwise[
                (pairwise["judge_model"] == judge_model)
                & (pairwise["language"] == language)
                & (pairwise["dimension"] == dimension)
            ].copy()
            if paired.empty:
                largest_delta = None
                largest_abs_delta = None
                largest_delta_pair = ""
                max_shift = None
                sig_count = 0
            else:
                idx = paired["auroc_delta_b_minus_a"].abs().idxmax()
                largest = paired.loc[idx]
                largest_delta = largest["auroc_delta_b_minus_a"]
                largest_abs_delta = abs(largest_delta)
                largest_delta_pair = f"{largest['protocol_b']} minus {largest['protocol_a']}"
                max_shift = paired["mean_abs_score_shift"].max()
                sig_count = int(significant_auroc_pairs(paired).sum())
            rows.append(
                {
                    "run": spec["run"],
                    "judge_model": judge_model,
                    "language": language,
                    "dimension": dimension,
                    "n_protocols": len(clean),
                    "best_protocol": best["protocol"],
                    "best_protocol_name": protocol_label(best["protocol"]),
                    "best_auroc": best["auroc"],
                    "best_spearman": best["spearman"],
                    "worst_protocol": worst["protocol"],
                    "worst_protocol_name": protocol_label(worst["protocol"]),
                    "worst_auroc": worst["auroc"],
                    "worst_spearman": worst["spearman"],
                    "auroc_range": best["auroc"] - worst["auroc"],
                    "spearman_range": clean["spearman"].max() - clean["spearman"].min(),
                    "max_mean_abs_score_shift": max_shift,
                    "n_significant_auroc_pairs": sig_count,
                    "has_significant_auroc_pair": sig_count > 0,
                    "largest_abs_auroc_delta": largest_abs_delta,
                    "largest_auroc_delta_b_minus_a": largest_delta,
                    "largest_auroc_delta_pair": largest_delta_pair,
                    "best_is_direct": best["protocol"] == "P0_direct_english",
                    "best_is_pivot": best["protocol"] == "P2_explicit_pivot",
                    "pivot_is_worst": worst["protocol"] == "P2_explicit_pivot",
                    "has_pivot": bool((clean["protocol"] == "P2_explicit_pivot").any()),
                }
            )
    return pd.DataFrame(rows)


def summarize_runs(cells: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for run, group in cells.groupby("run", sort=False):
        rows.append(
            {
                "run": run,
                "n_cells": len(group),
                "median_auroc_range": group["auroc_range"].median(),
                "max_auroc_range": group["auroc_range"].max(),
                "median_spearman_range": group["spearman_range"].median(),
                "max_spearman_range": group["spearman_range"].max(),
                "cells_auroc_range_ge_0_10": int((group["auroc_range"] >= 0.10).sum()),
                "cells_auroc_range_ge_0_15": int((group["auroc_range"] >= 0.15).sum()),
                "cells_best_not_direct": int((~group["best_is_direct"]).sum()),
                "cells_best_not_pivot": int((~group["best_is_pivot"]).sum()),
                "cells_pivot_worst": int(group["pivot_is_worst"].sum()),
                "cells_with_significant_auroc_pair": int(group["has_significant_auroc_pair"].sum()),
                "max_mean_abs_score_shift": group["max_mean_abs_score_shift"].max(),
            }
        )
    return pd.DataFrame(rows)


def write_markdown(cells: pd.DataFrame, summary: pd.DataFrame, path: Path) -> None:
    main = cells[~cells["run"].str.contains("audit")]
    lines = [
        "# Protocol Instability Summary",
        "",
        "This file is generated from existing metrics and paired-bootstrap outputs.",
        "",
        "## Aggregate Main-Run Claim",
        "",
        (
            f"Across {len(main)} non-audit task/language cells, the best AUROC protocol is not direct in "
            f"{int((~main['best_is_direct']).sum())} cells, explicit pivot is the worst protocol in "
            f"{int(main['pivot_is_worst'].sum())} cells, and "
            f"{int(main['has_significant_auroc_pair'].sum())} cells have at least one paired AUROC delta "
            "with a bootstrap CI excluding zero."
        ),
        "",
        "## Run-Level Summary",
        "",
        "```text",
        summary.to_string(index=False),
        "```",
        "",
        "## Largest Cell-Level AUROC Ranges",
        "",
        "```text",
        cells.sort_values("auroc_range", ascending=False)
        .head(12)[
            [
                "run",
                "language",
                "dimension",
                "best_protocol",
                "worst_protocol",
                "auroc_range",
                "max_mean_abs_score_shift",
                "n_significant_auroc_pairs",
            ]
        ]
        .to_string(index=False),
        "```",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    cells = summarize_cells()
    summary = summarize_runs(cells)
    cells.to_csv(OUT_DIR / "protocol_instability_cells.csv", index=False)
    summary.to_csv(OUT_DIR / "protocol_instability_summary.csv", index=False)
    write_markdown(cells, summary, OUT_DIR / "protocol_instability_summary.md")
    print(f"Wrote {OUT_DIR / 'protocol_instability_cells.csv'}")
    print(f"Wrote {OUT_DIR / 'protocol_instability_summary.csv'}")
    print(f"Wrote {OUT_DIR / 'protocol_instability_summary.md'}")


if __name__ == "__main__":
    main()
