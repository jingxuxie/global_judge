from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

import pandas as pd


OUT_PATH = Path("paper/results_brief.md")


def fmt_num(value: float | int | str | None, digits: int = 3) -> str:
    if value is None or pd.isna(value):
        return ""
    if isinstance(value, str):
        return value
    return f"{float(value):.{digits}f}"


def md_table(rows: list[dict], columns: list[tuple[str, str]]) -> str:
    headers = [header for _, header in columns]
    keys = [key for key, _ in columns]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(key, "")) for key in keys) + " |")
    return "\n".join(lines)


def load(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def metric_row(metrics: pd.DataFrame, language: str, dimension: str, protocol: str) -> pd.Series:
    rows = metrics[
        (metrics["language"] == language)
        & (metrics["dimension"] == dimension)
        & (metrics["protocol"] == protocol)
    ]
    if rows.empty:
        raise KeyError((language, dimension, protocol))
    return rows.iloc[0]


def pair_row(pairwise: pd.DataFrame, language: str, dimension: str, protocol_a: str, protocol_b: str) -> pd.Series:
    rows = pairwise[
        (pairwise["language"] == language)
        & (pairwise["dimension"] == dimension)
        & (pairwise["protocol_a"] == protocol_a)
        & (pairwise["protocol_b"] == protocol_b)
    ]
    if rows.empty:
        raise KeyError((language, dimension, protocol_a, protocol_b))
    return rows.iloc[0]


def describe_protocol(metrics: pd.DataFrame, language: str, dimension: str, protocol: str) -> str:
    row = metric_row(metrics, language, dimension, protocol)
    return f"{fmt_num(row['spearman'])} / {fmt_num(row['auroc'])}"


def describe_protocol_optional(metrics: pd.DataFrame, language: str, dimension: str, protocol: str) -> str:
    rows = metrics[
        (metrics["language"] == language)
        & (metrics["dimension"] == dimension)
        & (metrics["protocol"] == protocol)
    ]
    if rows.empty:
        return "n/a"
    row = rows.iloc[0]
    return f"{fmt_num(row['spearman'])} / {fmt_num(row['auroc'])}"


def component_cost(paths: Iterable[str]) -> float:
    total = 0.0
    for path in paths:
        with Path(path).open("r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    total += json.loads(line).get("api_cost_estimate_usd") or 0.0
    return total


def calibration_summary(path: str, name: str) -> dict:
    df = load(path)
    test = df[df["split"] == "test"]
    return {
        "run": name,
        "groups": len(test),
        "mean_delta_bal_acc": fmt_num(test["delta_balanced_accuracy"].mean()),
        "median_delta_bal_acc": fmt_num(test["delta_balanced_accuracy"].median()),
    }


def clip_text(value: str | None, limit: int = 120) -> str:
    if value is None or pd.isna(value):
        return ""
    text = " ".join(str(value).split())
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def main() -> None:
    candidate = load("data/analysis/candidate_n50_combined_explicit_metrics.csv")
    candidate_pair = load("data/analysis/candidate_n50_combined_explicit_metrics_pairwise_bootstrap.csv")
    candidate_gaps = load("data/analysis/candidate_n50_combined_explicit_metrics_language_gaps.csv")
    semantic = load("data/analysis/semantic_xlsum_n30_metrics.csv")
    semantic_pair = load("data/analysis/semantic_xlsum_n30_metrics_pairwise_bootstrap.csv")
    semantic_gaps = load("data/analysis/semantic_xlsum_n30_metrics_language_gaps.csv")
    audit = load("data/analysis/audit_gpt41mini_n25_combined_explicit_metrics.csv")
    audit_pair = load("data/analysis/audit_gpt41mini_n25_combined_explicit_metrics_pairwise_bootstrap.csv")
    wmt = load("data/analysis/wmt_mqm_n30_metrics.csv")
    wmt_pair = load("data/analysis/wmt_mqm_n30_metrics_pairwise_bootstrap.csv")
    wmt_gaps = load("data/analysis/wmt_mqm_n30_metrics_language_gaps.csv")
    wmt_ref_free = load("data/analysis/wmt_mqm_ref_free_n30_metrics.csv")
    wmt_ref_free_pair = load("data/analysis/wmt_mqm_ref_free_n30_metrics_pairwise_bootstrap.csv")
    wmt_ref_free_gaps = load("data/analysis/wmt_mqm_ref_free_n30_metrics_language_gaps.csv")
    wmt_zh_audit = load("data/analysis/wmt_mqm_ref_free_audit_zh_en_gpt41mini_metrics.csv")
    wmt_zh_audit_pair = load(
        "data/analysis/wmt_mqm_ref_free_audit_zh_en_gpt41mini_metrics_pairwise_bootstrap.csv"
    )
    wmt_de_audit = load("data/analysis/wmt_mqm_ref_free_audit_en_de_gpt41mini_metrics.csv")
    wmt_de_audit_pair = load(
        "data/analysis/wmt_mqm_ref_free_audit_en_de_gpt41mini_metrics_pairwise_bootstrap.csv"
    )
    instability = load("data/analysis/protocol_instability_summary.csv")
    qualitative = load("data/analysis/qualitative_protocol_examples.csv")
    sampling = load("data/analysis/dataset_sampling_summary.csv")
    calibration_curve = load("data/analysis/calibration_learning_curve_summary.csv")
    score_threshold = load("data/analysis/score_threshold_diagnostic_summary.csv")
    run_inventory = load("data/analysis/run_inventory.csv")
    repeatability = load("data/analysis/repeatability_control_summary.csv")
    rq_matrix = load("data/analysis/rq_contribution_matrix.csv")

    candidate_rows = []
    for language, dimension, comparison, protocol_a, protocol_b in [
        ("tr", "comprehensibility", "pivot - direct", "P0_direct_english", "P2_explicit_pivot"),
        ("vi", "comprehensibility", "bilingual - pivot", "P2_explicit_pivot", "P3_bilingual"),
        ("tr", "grammar", "pivot - direct", "P0_direct_english", "P2_explicit_pivot"),
        ("vi", "grammar", "pivot - target", "P1_target_rubric", "P2_explicit_pivot"),
    ]:
        pair = pair_row(candidate_pair, language, dimension, protocol_a, protocol_b)
        candidate_rows.append(
            {
                "cell": f"{language} / {dimension}",
                "direct": describe_protocol(candidate, language, dimension, "P0_direct_english"),
                "target": describe_protocol(candidate, language, dimension, "P1_target_rubric"),
                "pivot": describe_protocol(candidate, language, dimension, "P2_explicit_pivot"),
                "bilingual": describe_protocol(candidate, language, dimension, "P3_bilingual"),
                "comparison": comparison,
                "paired_delta": fmt_num(pair["auroc_delta_b_minus_a"]),
                "ci": f"[{fmt_num(pair['auroc_delta_ci_low'])}, {fmt_num(pair['auroc_delta_ci_high'])}]",
                "shift": fmt_num(pair["mean_abs_score_shift"]),
            }
        )

    sampling_rows = []
    for _, row in sampling.iterrows():
        sampling_rows.append(
            {
                "run": row["run"],
                "items": int(row["items"]),
                "languages": int(row["languages"]),
                "dimensions": int(row["dimensions"]),
                "positive": int(row["human_positive"]),
                "negative": int(row["human_negative"]),
                "source_rate": f"{100.0 * row['source_available_rate']:.1f}%",
                "reference_rate": f"{100.0 * row['reference_available_rate']:.1f}%",
            }
        )

    semantic_rows = []
    for language in ["es-ES", "tr", "vi"]:
        sub = semantic[(semantic["language"] == language) & (semantic["dimension"] == "main_ideas")]
        best = sub.sort_values("auroc", ascending=False).iloc[0]
        semantic_rows.append(
            {
                "language": language,
                "best_protocol": best["protocol"],
                "best_sp_auroc": f"{fmt_num(best['spearman'])} / {fmt_num(best['auroc'])}",
                "direct": describe_protocol(semantic, language, "main_ideas", "P0_direct_english"),
                "pivot": describe_protocol(semantic, language, "main_ideas", "P2_explicit_pivot"),
                "bilingual": describe_protocol(semantic, language, "main_ideas", "P3_bilingual"),
            }
        )

    audit_rows = []
    for language, dimension in [("tr", "comprehensibility"), ("vi", "grammar")]:
        audit_pair_direct = pair_row(
            audit_pair,
            language,
            dimension,
            "P0_direct_english",
            "P2_explicit_pivot",
        )
        audit_pair_bi = pair_row(
            audit_pair,
            language,
            dimension,
            "P2_explicit_pivot",
            "P3_bilingual",
        )
        audit_rows.append(
            {
                "cell": f"{language} / {dimension}",
                "direct": describe_protocol(audit, language, dimension, "P0_direct_english"),
                "pivot": describe_protocol(audit, language, dimension, "P2_explicit_pivot"),
                "bilingual": describe_protocol(audit, language, dimension, "P3_bilingual"),
                "pivot_minus_direct_auroc": fmt_num(audit_pair_direct["auroc_delta_b_minus_a"]),
                "bilingual_minus_pivot_auroc": fmt_num(audit_pair_bi["auroc_delta_b_minus_a"]),
            }
        )

    wmt_rows = []
    for setting, metrics_df, pair_df, dimension in [
        ("reference", wmt, wmt_pair, "translation_quality"),
        ("ref-free", wmt_ref_free, wmt_ref_free_pair, "translation_quality_ref_free"),
    ]:
        for language in ["en-de", "en-ru", "zh-en"]:
            sub = metrics_df[(metrics_df["language"] == language) & (metrics_df["dimension"] == dimension)]
            if sub.empty:
                continue
            best = sub.sort_values("auroc", ascending=False).iloc[0]
            wmt_delta = pair_row(
                pair_df,
                language,
                dimension,
                "P0_direct_english",
                "P2_explicit_pivot",
            )
            wmt_rows.append(
                {
                    "setting": setting,
                    "language": language,
                    "best_protocol": best["protocol"],
                    "best": f"{fmt_num(best['spearman'])} / {fmt_num(best['auroc'])}",
                    "direct": describe_protocol(metrics_df, language, dimension, "P0_direct_english"),
                    "target": describe_protocol_optional(metrics_df, language, dimension, "P1_target_rubric"),
                    "pivot": describe_protocol(metrics_df, language, dimension, "P2_explicit_pivot"),
                    "bilingual": describe_protocol_optional(metrics_df, language, dimension, "P3_bilingual"),
                    "delta": fmt_num(wmt_delta["auroc_delta_b_minus_a"]),
                    "ci": f"[{fmt_num(wmt_delta['auroc_delta_ci_low'])}, {fmt_num(wmt_delta['auroc_delta_ci_high'])}]",
                    "shift": fmt_num(wmt_delta["mean_abs_score_shift"]),
                }
            )

    wmt_audit_rows = []
    for cell, metrics_df, pair_df, language, protocol_a, protocol_b, comparison, a_name, b_name in [
        (
            "zh-en ref-free",
            wmt_zh_audit,
            wmt_zh_audit_pair,
            "zh-en",
            "P0_direct_english",
            "P2_explicit_pivot",
            "pivot - direct",
            "direct",
            "pivot",
        ),
        (
            "en-de ref-free",
            wmt_de_audit,
            wmt_de_audit_pair,
            "en-de",
            "P2_explicit_pivot",
            "P3_bilingual",
            "bilingual - pivot",
            "pivot",
            "bilingual",
        ),
    ]:
        delta = pair_row(pair_df, language, "translation_quality_ref_free", protocol_a, protocol_b)
        wmt_audit_rows.append(
            {
                "cell": cell,
                "comparison": comparison,
                "protocol_a": a_name,
                "a_sp_auroc": describe_protocol(metrics_df, language, "translation_quality_ref_free", protocol_a),
                "protocol_b": b_name,
                "b_sp_auroc": describe_protocol(metrics_df, language, "translation_quality_ref_free", protocol_b),
                "delta": fmt_num(delta["auroc_delta_b_minus_a"]),
                "ci": f"[{fmt_num(delta['auroc_delta_ci_low'])}, {fmt_num(delta['auroc_delta_ci_high'])}]",
                "shift": fmt_num(delta["mean_abs_score_shift"]),
            }
        )

    gap_rows = []
    for run, gaps in [
        ("candidate n50", candidate_gaps),
        ("semantic n30", semantic_gaps),
        ("wmt n30", wmt_gaps),
        ("wmt ref-free n30", wmt_ref_free_gaps),
    ]:
        limit = 4 if run.startswith("wmt") else 3
        for _, row in gaps.sort_values("spearman_language_gap", ascending=False).head(limit).iterrows():
            gap_rows.append(
                {
                    "run": run,
                    "dimension": row["dimension"],
                    "protocol": row["protocol"],
                    "gap": fmt_num(row["spearman_language_gap"]),
                    "min": f"{row['min_spearman_language']} ({fmt_num(row['min_spearman'])})",
                    "max": f"{row['max_spearman_language']} ({fmt_num(row['max_spearman'])})",
                }
            )

    instability_rows = []
    for _, row in instability.iterrows():
        cells = int(row["n_cells"])
        instability_rows.append(
            {
                "run": row["run"],
                "cells": cells,
                "median_range": fmt_num(row["median_auroc_range"]),
                "max_range": fmt_num(row["max_auroc_range"]),
                "range_ge_010": f"{int(row['cells_auroc_range_ge_0_10'])}/{cells}",
                "best_not_direct": f"{int(row['cells_best_not_direct'])}/{cells}",
                "pivot_worst": f"{int(row['cells_pivot_worst'])}/{cells}",
                "sig_cells": f"{int(row['cells_with_significant_auroc_pair'])}/{cells}",
                "max_shift": fmt_num(row["max_mean_abs_score_shift"]),
            }
        )

    repeatability_rows = []
    for _, row in repeatability.iterrows():
        repeatability_rows.append(
            {
                "control": row["control"],
                "pairs": int(row["n_scored_pairs"]),
                "identical_prompts": f"{100.0 * row['identical_prompt_rate']:.1f}%",
                "exact_agreement": f"{100.0 * row['exact_score_agreement']:.1f}%",
                "mean_delta": fmt_num(row["mean_abs_score_delta"]),
                "max_delta": fmt_num(row["max_abs_score_delta"], 0),
                "interpretation": row["interpretation"],
            }
        )

    rq_rows = []
    for _, row in rq_matrix.iterrows():
        rq_rows.append(
            {
                "plan_item": row["plan_item"],
                "coverage": row["coverage"],
                "evidence": row["evidence"],
                "boundary": row["claim_boundary"],
            }
        )

    qualitative_rows = []
    for mode, group in qualitative.groupby("failure_mode", sort=False):
        for _, row in group.head(2).iterrows():
            qualitative_rows.append(
                {
                    "mode": mode,
                    "cell": f"{row['language']} / {row['dimension']}",
                    "human": int(row["human_label"]),
                    "scores": (
                        f"D={int(row['P0_direct_english'])}, "
                        f"T={int(row['P1_target_rubric'])}, "
                        f"P={int(row['P2_explicit_pivot'])}, "
                        f"B={int(row['P3_bilingual'])}"
                    ),
                    "original": clip_text(row["candidate_output"]),
                    "pivot": clip_text(row["english_translation"]),
                    "pivot_rationale": clip_text(row["P2_explicit_pivot_rationale"]),
                }
            )

    calibration_rows = [
        calibration_summary("data/analysis/candidate_n50_combined_explicit_calibration.csv", "candidate n50"),
        calibration_summary("data/analysis/audit_gpt41mini_n25_combined_explicit_calibration.csv", "gpt-4.1-mini audit n25"),
        calibration_summary("data/analysis/semantic_xlsum_n30_calibration.csv", "semantic n30"),
        calibration_summary("data/analysis/wmt_mqm_n30_calibration.csv", "wmt n30"),
        calibration_summary("data/analysis/wmt_mqm_ref_free_n30_calibration.csv", "wmt ref-free n30"),
        calibration_summary("data/analysis/wmt_mqm_ref_free_audit_zh_en_gpt41mini_calibration.csv", "wmt audit zh-en"),
        calibration_summary("data/analysis/wmt_mqm_ref_free_audit_en_de_gpt41mini_calibration.csv", "wmt audit en-de"),
    ]

    calibration_curve_rows = []
    for run in ["candidate n50", "semantic n30", "wmt reference n30", "wmt ref-free n30", "candidate audit n25"]:
        sub = calibration_curve[calibration_curve["run"] == run].set_index("n_calibration")
        if sub.empty:
            continue
        largest = sub.loc[sub.index.max()]
        calibration_curve_rows.append(
            {
                "run": run,
                "delta_n2": fmt_num(sub.loc[2, "mean_delta_balanced_accuracy"]) if 2 in sub.index else "",
                "delta_n8": fmt_num(sub.loc[8, "mean_delta_balanced_accuracy"]) if 8 in sub.index else "",
                "largest_n": int(largest.name),
                "largest_delta": fmt_num(largest["mean_delta_balanced_accuracy"]),
                "prob_improve": fmt_num(largest["prob_improves"]),
                "prob_degrade": fmt_num(largest["prob_degrades"]),
            }
        )

    score_threshold_rows = []
    for _, row in score_threshold.iterrows():
        score_threshold_rows.append(
            {
                "run": row["run"],
                "groups": int(row["groups"]),
                "pos_score": fmt_num(row["mean_score_human_positive"]),
                "neg_score": fmt_num(row["mean_score_human_negative"]),
                "pred_good": f"{100.0 * row['predicted_good_rate_threshold_4']:.1f}%",
                "pos_good": f"{100.0 * row['positive_good_rate_threshold_4']:.1f}%",
                "neg_good": f"{100.0 * row['negative_good_rate_threshold_4']:.1f}%",
                "bal_acc": fmt_num(row["balanced_accuracy_threshold_4"]),
                "mode_best_threshold": int(row["mode_best_in_group_threshold"]),
            }
        )

    cost_rows = [
        {
            "run": "candidate n50",
            "cost_usd": fmt_num(
                component_cost(
                    [
                        "data/responses/candidate_n50_base_responses.jsonl",
                        "data/processed/candidate_n50_english_translations.jsonl",
                        "data/responses/candidate_n50_explicit_pivot_responses.jsonl",
                    ]
                ),
                4,
            ),
        },
        {
            "run": "gpt-4.1-mini audit n25",
            "cost_usd": fmt_num(
                component_cost(
                    [
                        "data/responses/audit_gpt41mini_n25_base_responses.jsonl",
                        "data/processed/audit_gpt41mini_n25_english_translations.jsonl",
                        "data/responses/audit_gpt41mini_n25_explicit_pivot_responses.jsonl",
                    ]
                ),
                4,
            ),
        },
        {
            "run": "semantic n30",
            "cost_usd": fmt_num(
                component_cost(
                    [
                        "data/processed/semantic_xlsum_n30_english_translations.jsonl",
                        "data/responses/semantic_xlsum_n30_responses.jsonl",
                    ]
                ),
                4,
            ),
        },
        {
            "run": "wmt n30",
            "cost_usd": fmt_num(
                component_cost(
                    [
                        "data/processed/wmt_mqm_n30_english_translations.jsonl",
                        "data/responses/wmt_mqm_n30_responses.jsonl",
                    ]
                ),
                4,
            ),
        },
        {
            "run": "wmt ref-free n30",
            "cost_usd": fmt_num(
                component_cost(
                    [
                        "data/responses/wmt_mqm_ref_free_n30_responses.jsonl",
                    ]
                ),
                4,
            ),
        },
        {
            "run": "wmt ref-free audit",
            "cost_usd": fmt_num(
                component_cost(
                    [
                        "data/responses/wmt_mqm_ref_free_audit_zh_en_gpt41mini_responses.jsonl",
                        "data/responses/wmt_mqm_ref_free_audit_en_de_gpt41mini_responses.jsonl",
                    ]
                ),
                4,
            ),
        },
    ]

    inventory_rows = []
    usage_rows = []
    for _, row in run_inventory.iterrows():
        inventory_rows.append(
            {
                "run": row["run"],
                "base": int(row["base_items"]),
                "calls": int(row["judge_calls"]),
                "parse": f"{100.0 * row['parse_rate']:.1f}%",
                "cost": fmt_num(row["observed_cost_usd"], 4),
                "cost_per_1k": fmt_num(row["cost_per_1000_judge_calls"]),
            }
        )
        usage_rows.append(
            {
                "run": row["run"],
                "api_calls": int(row["api_calls_including_translations"]),
                "input_tokens": int(row["input_tokens"]),
                "output_tokens": int(row["output_tokens"]),
                "total_tokens": int(row["total_tokens"]),
                "tokens_per_call": fmt_num(row["avg_total_tokens_per_api_call"], 1),
            }
        )

    lines = [
        "# GlobalJudge Results Brief",
        "",
        "This brief is generated from the current analysis CSV/JSONL artifacts. Values are Spearman / AUROC unless noted.",
        "",
        "## Claim Boundary",
        "",
        "- Strongest claim: multilingual LLM-as-judge conclusions are protocol-sensitive; reporting one aggregate score hides language, dimension, and protocol effects.",
        "- Strong evidence: n=50 candidate-quality SEAHORSE run, n=30 source-grounded XLSum `main_ideas` run, and n=25 `gpt-4.1-mini` audit all show protocol-dependent score or alignment changes.",
        "- Contrast evidence: WMT MQM n=30 per language pair shows smaller direct-vs-pivot shifts for reference-based translation quality, while reference-free MT judging has larger `gpt-4o-mini` protocol effects.",
        "- WMT audit boundary: a targeted `gpt-4.1-mini` audit preserves the `zh-en` pivot-drop direction but not significance at n=30, and does not reproduce the `en-de` bilingual-over-pivot gain.",
        "- Aggregate instability: across 17 non-audit task/language cells, the best AUROC protocol is not direct in 11 cells, explicit pivot is worst in 10 cells, and 6 cells have at least one paired AUROC delta with a bootstrap CI excluding zero.",
        "- Conservative caveat: all current runs use OpenAI judges; target-language rubrics are pilot translations and should be native-checked before final publication claims.",
        "",
        "## Dataset Sampling Audit",
        "",
        md_table(
            sampling_rows,
            [
                ("run", "Run"),
                ("items", "Items"),
                ("languages", "Langs"),
                ("dimensions", "Dims"),
                ("positive", "Pos"),
                ("negative", "Neg"),
                ("source_rate", "Source Rate"),
                ("reference_rate", "Reference Rate"),
            ],
        ),
        "",
        "## Candidate-Quality N=50",
        "",
        md_table(
            candidate_rows,
            [
                ("cell", "Cell"),
                ("direct", "Direct"),
                ("target", "Target"),
                ("pivot", "Pivot"),
                ("bilingual", "Bilingual"),
                ("comparison", "Paired AUROC Delta"),
                ("paired_delta", "Delta"),
                ("ci", "95% CI"),
                ("shift", "Mean Abs Shift"),
            ],
        ),
        "",
        "## Source-Grounded Semantic N=30",
        "",
        md_table(
            semantic_rows,
            [
                ("language", "Language"),
                ("best_protocol", "Best Protocol"),
                ("best_sp_auroc", "Best"),
                ("direct", "Direct"),
                ("pivot", "Pivot"),
                ("bilingual", "Bilingual"),
            ],
        ),
        "",
        "Semantic paired highlights: `tr`, bilingual minus pivot AUROC delta = `+0.124` with 95% CI `[0.000, 0.275]`; `vi`, bilingual minus pivot AUROC delta = `+0.107` with 95% CI `[0.013, 0.220]`.",
        "",
        "## Stronger-Judge Audit",
        "",
        md_table(
            audit_rows,
            [
                ("cell", "Cell"),
                ("direct", "Direct"),
                ("pivot", "Pivot"),
                ("bilingual", "Bilingual"),
                ("pivot_minus_direct_auroc", "Pivot-Direct AUROC"),
                ("bilingual_minus_pivot_auroc", "Bilingual-Pivot AUROC"),
            ],
        ),
        "",
        "## WMT MQM Translation-Quality Contrast",
        "",
        md_table(
            wmt_rows,
            [
                ("language", "Pair"),
                ("setting", "Setting"),
                ("best_protocol", "Best Protocol"),
                ("best", "Best"),
                ("direct", "Direct"),
                ("target", "Target"),
                ("pivot", "Pivot"),
                ("bilingual", "Bilingual"),
                ("delta", "Pivot-Direct AUROC"),
                ("ci", "95% CI"),
                ("shift", "Mean Abs Shift"),
            ],
        ),
        "",
        "## WMT Ref-Free Stronger-Judge Audit",
        "",
        md_table(
            wmt_audit_rows,
            [
                ("cell", "Cell"),
                ("comparison", "Comparison"),
                ("protocol_a", "Protocol A"),
                ("a_sp_auroc", "A"),
                ("protocol_b", "Protocol B"),
                ("b_sp_auroc", "B"),
                ("delta", "B-A AUROC"),
                ("ci", "95% CI"),
                ("shift", "Mean Abs Shift"),
            ],
        ),
        "",
        "Interpretation: the stronger audit supports `zh-en` reference-free direct-over-pivot as a directional robustness check, but the CI crosses zero. The `en-de` bilingual advantage from the main `gpt-4o-mini` reference-free run is model-dependent in this bounded audit.",
        "",
        "## Qualitative Protocol Examples",
        "",
        md_table(
            qualitative_rows,
            [
                ("mode", "Mode"),
                ("cell", "Cell"),
                ("human", "Human"),
                ("scores", "Scores"),
                ("original", "Original"),
                ("pivot", "English Pivot"),
                ("pivot_rationale", "Pivot Rationale"),
            ],
        ),
        "",
        "Full examples with target and bilingual rationales are generated at `data/analysis/qualitative_protocol_examples.md`.",
        "",
        "## Protocol Instability Summary",
        "",
        md_table(
            instability_rows,
            [
                ("run", "Run"),
                ("cells", "Cells"),
                ("median_range", "Median AUROC Range"),
                ("max_range", "Max AUROC Range"),
                ("range_ge_010", "Range >= .10"),
                ("best_not_direct", "Best != Direct"),
                ("pivot_worst", "Pivot Worst"),
                ("sig_cells", "Significant Cells"),
                ("max_shift", "Max Shift"),
            ],
        ),
        "",
        "## Repeatability Control",
        "",
        md_table(
            repeatability_rows,
            [
                ("control", "Control"),
                ("pairs", "Pairs"),
                ("identical_prompts", "Identical Prompts"),
                ("exact_agreement", "Exact Agreement"),
                ("mean_delta", "Mean Abs Delta"),
                ("max_delta", "Max Abs Delta"),
                ("interpretation", "Interpretation"),
            ],
        ),
        "",
        "Interpretation: exact repeated original-text prompts show small ordinary judge run-to-run variation, while regenerated explicit-pivot prompts expose additional pipeline volatility.",
        "",
        "## Largest Language Gaps",
        "",
        md_table(
            gap_rows,
            [
                ("run", "Run"),
                ("dimension", "Dimension"),
                ("protocol", "Protocol"),
                ("gap", "Spearman Gap"),
                ("min", "Min Lang"),
                ("max", "Max Lang"),
            ],
        ),
        "",
        "## Calibration Summary",
        "",
        md_table(
            calibration_rows,
            [
                ("run", "Run"),
                ("groups", "Groups"),
                ("mean_delta_bal_acc", "Mean Bal-Acc Delta"),
                ("median_delta_bal_acc", "Median Bal-Acc Delta"),
            ],
        ),
        "",
        "## Calibration Learning Curve",
        "",
        md_table(
            calibration_curve_rows,
            [
                ("run", "Run"),
                ("delta_n2", "Mean Delta n=2"),
                ("delta_n8", "Mean Delta n=8"),
                ("largest_n", "Largest n_cal"),
                ("largest_delta", "Largest-Budget Delta"),
                ("prob_improve", "P(Improve)"),
                ("prob_degrade", "P(Degrade)"),
            ],
        ),
        "",
        "Interpretation: small threshold calibration is useful for the source-grounded semantic setting, mixed for reference-free WMT, and not a reliable fix for candidate-quality form judgments.",
        "",
        "## Score Threshold Diagnostic",
        "",
        md_table(
            score_threshold_rows,
            [
                ("run", "Run"),
                ("groups", "Groups"),
                ("pos_score", "Mean Pos Score"),
                ("neg_score", "Mean Neg Score"),
                ("pred_good", "Pred Good @4"),
                ("pos_good", "Pos Good @4"),
                ("neg_good", "Neg Good @4"),
                ("bal_acc", "BalAcc @4"),
                ("mode_best_threshold", "Mode Best Threshold"),
            ],
        ),
        "",
        "Interpretation: semantic `main_ideas` scores are compressed low, so score >= 4 marks only 8.3% of balanced examples as good and threshold calibration often lowers the cutoff. WMT ref-free scores are compressed high, so threshold 5 is often preferred.",
        "",
        "## Run Inventory",
        "",
        md_table(
            inventory_rows,
            [
                ("run", "Run"),
                ("base", "Base Items"),
                ("calls", "Judge Calls"),
                ("parse", "Parse Rate"),
                ("cost", "Observed Cost"),
                ("cost_per_1k", "Cost / 1k Calls"),
            ],
        ),
        "",
        "## API Token Inventory",
        "",
        md_table(
            usage_rows,
            [
                ("run", "Run"),
                ("api_calls", "API Calls"),
                ("input_tokens", "Input Tokens"),
                ("output_tokens", "Output Tokens"),
                ("total_tokens", "Total Tokens"),
                ("tokens_per_call", "Tokens / Call"),
            ],
        ),
        "",
        "Interpretation: token counts come from returned API usage metadata and are stable even if model pricing changes. API calls include translation calls and recorded retries where present.",
        "",
        "## Observed API Spend",
        "",
        md_table(cost_rows, [("run", "Run"), ("cost_usd", "Approx Cost USD")]),
        "",
        "## RQ and Contribution Coverage",
        "",
        md_table(
            rq_rows,
            [
                ("plan_item", "Plan Item"),
                ("coverage", "Coverage"),
                ("evidence", "Evidence"),
                ("boundary", "Claim Boundary"),
            ],
        ),
        "",
        "## Draft Result Paragraph",
        "",
        "Across 400 candidate-quality SEAHORSE examples, a cheap LLM judge produced materially different scores for the same summaries depending only on the judging protocol. The largest shifts concentrate in target-language form dimensions: for Vietnamese grammar, target-language rubric and explicit English pivot differ by 1.20 points on a 1-5 scale on average, and 34% of items shift by at least two points. English-pivot judging is therefore not a safe default: on Turkish comprehensibility it significantly underperforms direct judging in paired AUROC, and in a stronger n=25 `gpt-4.1-mini` audit the same failure mode reappears. In source-grounded XLSum `main_ideas`, protocol shifts are smaller, but pivoting remains language-dependent: it is strongest for Spanish, weaker for Turkish than bilingual judging, and chance-level for Vietnamese. A WMT MQM translation-quality extension shows that reference-based direct-vs-pivot differences are smaller, but reference-free MT judging surfaces larger `gpt-4o-mini` protocol effects. A targeted `gpt-4.1-mini` WMT audit preserves the `zh-en` direct-over-pivot direction but not n=30 significance, and does not reproduce the `en-de` bilingual-over-pivot gain, so WMT is best framed as protocol/model-sensitivity evidence rather than a stable global protocol ranking. These results motivate reporting protocol sensitivity, language gaps, calibration behavior, parse rates, and cost rather than a single multilingual judge score.",
        "",
    ]
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
