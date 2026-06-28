from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

import pandas as pd


OUT_GROUPS_CSV = Path("data/analysis/score_threshold_diagnostic_groups.csv")
OUT_SUMMARY_CSV = Path("data/analysis/score_threshold_diagnostic_summary.csv")
OUT_MD = Path("data/analysis/score_threshold_diagnostic.md")
OUT_TEX = Path("paper/tables/score_threshold_diagnostic.tex")


RUN_SPECS = [
    {
        "run": "candidate n50",
        "items": "data/processed/candidate_n50_items.jsonl",
        "responses": "data/responses/candidate_n50_combined_explicit_responses.jsonl",
    },
    {
        "run": "semantic n30",
        "items": "data/processed/semantic_xlsum_n30_items.jsonl",
        "responses": "data/responses/semantic_xlsum_n30_responses.jsonl",
    },
    {
        "run": "wmt reference n30",
        "items": "data/processed/wmt_mqm_n30_items.jsonl",
        "responses": "data/responses/wmt_mqm_n30_responses.jsonl",
    },
    {
        "run": "wmt ref-free n30",
        "items": "data/processed/wmt_mqm_n30_items.jsonl",
        "responses": "data/responses/wmt_mqm_ref_free_n30_responses.jsonl",
    },
    {
        "run": "candidate audit n25",
        "items": "data/processed/audit_gpt41mini_n25_items.jsonl",
        "responses": "data/responses/audit_gpt41mini_n25_combined_explicit_responses.jsonl",
    },
]


def read_jsonl(path: str | Path) -> list[dict[str, Any]]:
    with Path(path).open("r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def balanced_accuracy(pos_scores: pd.Series, neg_scores: pd.Series, threshold: int) -> float:
    if pos_scores.empty or neg_scores.empty:
        return float("nan")
    true_positive_rate = float((pos_scores >= threshold).mean())
    true_negative_rate = float((neg_scores < threshold).mean())
    return 0.5 * (true_positive_rate + true_negative_rate)


def group_rows(run: str, items_path: str, responses_path: str) -> list[dict[str, Any]]:
    items = pd.DataFrame(read_jsonl(items_path))[["item_id", "human_label"]]
    responses = pd.DataFrame(read_jsonl(responses_path))
    df = responses.merge(items, on="item_id", how="left")
    clean = df[df["parse_success"] & df["score"].notna() & df["human_label"].notna()].copy()
    rows = []
    for (language, dimension, protocol), group in clean.groupby(["language", "dimension", "protocol"]):
        pos_scores = group[group["human_label"] == 1]["score"]
        neg_scores = group[group["human_label"] == 0]["score"]
        if pos_scores.empty or neg_scores.empty:
            continue
        threshold_scores = {
            threshold: balanced_accuracy(pos_scores, neg_scores, threshold) for threshold in [2, 3, 4, 5]
        }
        best_threshold = max(threshold_scores, key=lambda threshold: (threshold_scores[threshold], -threshold))
        rows.append(
            {
                "run": run,
                "language": language,
                "dimension": dimension,
                "protocol": protocol,
                "n": len(group),
                "mean_score": float(group["score"].mean()),
                "mean_score_human_positive": float(pos_scores.mean()),
                "mean_score_human_negative": float(neg_scores.mean()),
                "score_separation_pos_minus_neg": float(pos_scores.mean() - neg_scores.mean()),
                "predicted_good_rate_threshold_4": float((group["score"] >= 4).mean()),
                "positive_good_rate_threshold_4": float((pos_scores >= 4).mean()),
                "negative_good_rate_threshold_4": float((neg_scores >= 4).mean()),
                "balanced_accuracy_threshold_4": threshold_scores[4],
                "best_in_group_threshold": best_threshold,
                "best_in_group_balanced_accuracy": threshold_scores[best_threshold],
            }
        )
    return rows


def mode(values: pd.Series) -> int:
    counts = Counter(int(value) for value in values)
    return min((-count, value) for value, count in counts.items())[1]


def summarize(groups: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for run, group in groups.groupby("run", sort=False):
        rows.append(
            {
                "run": run,
                "groups": len(group),
                "mean_score": group["mean_score"].mean(),
                "mean_score_human_positive": group["mean_score_human_positive"].mean(),
                "mean_score_human_negative": group["mean_score_human_negative"].mean(),
                "score_separation_pos_minus_neg": group["score_separation_pos_minus_neg"].mean(),
                "predicted_good_rate_threshold_4": group["predicted_good_rate_threshold_4"].mean(),
                "positive_good_rate_threshold_4": group["positive_good_rate_threshold_4"].mean(),
                "negative_good_rate_threshold_4": group["negative_good_rate_threshold_4"].mean(),
                "balanced_accuracy_threshold_4": group["balanced_accuracy_threshold_4"].mean(),
                "mode_best_in_group_threshold": mode(group["best_in_group_threshold"]),
                "mean_best_in_group_balanced_accuracy": group["best_in_group_balanced_accuracy"].mean(),
            }
        )
    return pd.DataFrame(rows)


def write_markdown(summary: pd.DataFrame) -> None:
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Score Threshold Diagnostic",
        "",
        "This no-new-API diagnostic summarizes how raw 1-5 judge scores interact with the fixed score >= 4 baseline threshold used by the calibration analyses.",
        "",
        "| Run | Groups | Mean Pos Score | Mean Neg Score | Pred Good @4 | Pos Good @4 | Neg Good @4 | BalAcc @4 | Mode Best Threshold |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for _, row in summary.iterrows():
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["run"]),
                    str(int(row["groups"])),
                    f"{row['mean_score_human_positive']:.3f}",
                    f"{row['mean_score_human_negative']:.3f}",
                    f"{100.0 * row['predicted_good_rate_threshold_4']:.1f}%",
                    f"{100.0 * row['positive_good_rate_threshold_4']:.1f}%",
                    f"{100.0 * row['negative_good_rate_threshold_4']:.1f}%",
                    f"{row['balanced_accuracy_threshold_4']:.3f}",
                    str(int(row["mode_best_in_group_threshold"])),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "Interpretation:",
            "- Source-grounded semantic `main_ideas` scores are compressed low: score >= 4 marks only a small fraction of balanced examples as good, and the modal best in-group threshold is 2.",
            "- WMT reference-free scores are compressed high: score >= 4 marks most examples as good, and the modal best in-group threshold is 5.",
            "- These diagnostics explain why threshold calibration helps semantic `main_ideas`, is mixed for WMT reference-free, and is not a universal repair for protocol sensitivity.",
            "",
        ]
    )
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def write_latex(summary: pd.DataFrame) -> None:
    OUT_TEX.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "\\begin{table}[t]",
        "\\centering",
        "\\caption{Score-threshold diagnostic. Rates use the fixed score $\\geq 4$ baseline threshold.}",
        "\\label{tab:score_threshold_diagnostic}",
        "\\resizebox{\\linewidth}{!}{%",
        "\\begin{tabular}{lrrrrrrr}",
        "\\toprule",
        "Run & Groups & Pos score & Neg score & Pred good & Pos good & Neg good & Mode best $t$ \\\\",
        "\\midrule",
    ]
    for _, row in summary.iterrows():
        lines.append(
            " & ".join(
                [
                    str(row["run"]).replace("_", "\\_"),
                    str(int(row["groups"])),
                    f"{row['mean_score_human_positive']:.2f}",
                    f"{row['mean_score_human_negative']:.2f}",
                    f"{100.0 * row['predicted_good_rate_threshold_4']:.1f}\\%",
                    f"{100.0 * row['positive_good_rate_threshold_4']:.1f}\\%",
                    f"{100.0 * row['negative_good_rate_threshold_4']:.1f}\\%",
                    str(int(row["mode_best_in_group_threshold"])),
                ]
            )
            + " \\\\"
        )
    lines.extend(["\\bottomrule", "\\end{tabular}%", "}", "\\end{table}", ""])
    OUT_TEX.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    rows: list[dict[str, Any]] = []
    for spec in RUN_SPECS:
        rows.extend(group_rows(spec["run"], spec["items"], spec["responses"]))
    groups = pd.DataFrame(rows)
    summary = summarize(groups)

    OUT_GROUPS_CSV.parent.mkdir(parents=True, exist_ok=True)
    groups.to_csv(OUT_GROUPS_CSV, index=False)
    summary.to_csv(OUT_SUMMARY_CSV, index=False)
    write_markdown(summary)
    write_latex(summary)
    print(f"Wrote {OUT_GROUPS_CSV}")
    print(f"Wrote {OUT_SUMMARY_CSV}")
    print(f"Wrote {OUT_MD}")
    print(f"Wrote {OUT_TEX}")


if __name__ == "__main__":
    main()
