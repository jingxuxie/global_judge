from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


OUT_DIR = Path("paper/tables")


def fmt(value: float | int | None, digits: int = 3) -> str:
    if value is None or pd.isna(value):
        return ""
    return f"{float(value):.{digits}f}"


def metric(metrics: pd.DataFrame, language: str, dimension: str, protocol: str) -> pd.Series:
    rows = metrics[
        (metrics["language"] == language)
        & (metrics["dimension"] == dimension)
        & (metrics["protocol"] == protocol)
    ]
    if rows.empty:
        raise KeyError((language, dimension, protocol))
    return rows.iloc[0]


def pair(pairwise: pd.DataFrame, language: str, dimension: str, protocol_a: str, protocol_b: str) -> pd.Series:
    rows = pairwise[
        (pairwise["language"] == language)
        & (pairwise["dimension"] == dimension)
        & (pairwise["protocol_a"] == protocol_a)
        & (pairwise["protocol_b"] == protocol_b)
    ]
    if rows.empty:
        raise KeyError((language, dimension, protocol_a, protocol_b))
    return rows.iloc[0]


def sp_auc(metrics: pd.DataFrame, language: str, dimension: str, protocol: str) -> str:
    row = metric(metrics, language, dimension, protocol)
    return f"{fmt(row['spearman'])} / {fmt(row['auroc'])}"


def sp_auc_optional(metrics: pd.DataFrame, language: str, dimension: str, protocol: str) -> str:
    rows = metrics[
        (metrics["language"] == language)
        & (metrics["dimension"] == dimension)
        & (metrics["protocol"] == protocol)
    ]
    if rows.empty:
        return "n/a"
    row = rows.iloc[0]
    return f"{fmt(row['spearman'])} / {fmt(row['auroc'])}"


def write_latex(df: pd.DataFrame, path: Path, caption: str, label: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    align = "l" * len(df.columns)
    lines = [
        "\\begin{table}[t]",
        "\\centering",
        f"\\caption{{{caption}}}",
        f"\\label{{{label}}}",
        "\\resizebox{\\linewidth}{!}{%",
        f"\\begin{{tabular}}{{{align}}}",
        "\\toprule",
        " & ".join(df.columns) + " \\\\",
        "\\midrule",
    ]
    for _, row in df.iterrows():
        lines.append(" & ".join(str(row[col]).replace("_", "\\_") for col in df.columns) + " \\\\")
    lines.extend(["\\bottomrule", "\\end{tabular}%", "}", "\\end{table}", ""])
    tex = "\n".join(lines)
    path.write_text(tex, encoding="utf-8")


def cost(paths: list[str]) -> float:
    total = 0.0
    for path in paths:
        with Path(path).open("r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    total += json.loads(line).get("api_cost_estimate_usd") or 0.0
    return total


def frac(n: int | float, d: int | float) -> str:
    return f"{int(n)}/{int(d)}"


def main() -> None:
    candidate = pd.read_csv("data/analysis/candidate_n50_combined_explicit_metrics.csv")
    candidate_pair = pd.read_csv("data/analysis/candidate_n50_combined_explicit_metrics_pairwise_bootstrap.csv")
    semantic = pd.read_csv("data/analysis/semantic_xlsum_n30_metrics.csv")
    semantic_pair = pd.read_csv("data/analysis/semantic_xlsum_n30_metrics_pairwise_bootstrap.csv")
    audit = pd.read_csv("data/analysis/audit_gpt41mini_n25_combined_explicit_metrics.csv")
    audit_pair = pd.read_csv("data/analysis/audit_gpt41mini_n25_combined_explicit_metrics_pairwise_bootstrap.csv")
    wmt = pd.read_csv("data/analysis/wmt_mqm_n30_metrics.csv")
    wmt_pair = pd.read_csv("data/analysis/wmt_mqm_n30_metrics_pairwise_bootstrap.csv")
    wmt_ref_free = pd.read_csv("data/analysis/wmt_mqm_ref_free_n30_metrics.csv")
    wmt_ref_free_pair = pd.read_csv("data/analysis/wmt_mqm_ref_free_n30_metrics_pairwise_bootstrap.csv")
    wmt_zh_audit = pd.read_csv("data/analysis/wmt_mqm_ref_free_audit_zh_en_gpt41mini_metrics.csv")
    wmt_zh_audit_pair = pd.read_csv(
        "data/analysis/wmt_mqm_ref_free_audit_zh_en_gpt41mini_metrics_pairwise_bootstrap.csv"
    )
    wmt_de_audit = pd.read_csv("data/analysis/wmt_mqm_ref_free_audit_en_de_gpt41mini_metrics.csv")
    wmt_de_audit_pair = pd.read_csv(
        "data/analysis/wmt_mqm_ref_free_audit_en_de_gpt41mini_metrics_pairwise_bootstrap.csv"
    )
    candidate_gaps = pd.read_csv("data/analysis/candidate_n50_combined_explicit_metrics_language_gaps.csv")
    semantic_gaps = pd.read_csv("data/analysis/semantic_xlsum_n30_metrics_language_gaps.csv")
    wmt_gaps = pd.read_csv("data/analysis/wmt_mqm_n30_metrics_language_gaps.csv")
    wmt_ref_free_gaps = pd.read_csv("data/analysis/wmt_mqm_ref_free_n30_metrics_language_gaps.csv")
    instability = pd.read_csv("data/analysis/protocol_instability_summary.csv")
    calibration_curve = pd.read_csv("data/analysis/calibration_learning_curve_summary.csv")
    run_inventory = pd.read_csv("data/analysis/run_inventory.csv")

    candidate_rows = []
    for language, dimension, protocol_a, protocol_b, comparison in [
        ("tr", "comprehensibility", "P0_direct_english", "P2_explicit_pivot", "Pivot - direct"),
        ("vi", "comprehensibility", "P2_explicit_pivot", "P3_bilingual", "Bilingual - pivot"),
        ("vi", "grammar", "P1_target_rubric", "P2_explicit_pivot", "Pivot - target"),
    ]:
        delta = pair(candidate_pair, language, dimension, protocol_a, protocol_b)
        candidate_rows.append(
            {
                "Cell": f"{language} / {dimension}",
                "Direct": sp_auc(candidate, language, dimension, "P0_direct_english"),
                "Target": sp_auc(candidate, language, dimension, "P1_target_rubric"),
                "Pivot": sp_auc(candidate, language, dimension, "P2_explicit_pivot"),
                "Bilingual": sp_auc(candidate, language, dimension, "P3_bilingual"),
                "Comparison": comparison,
                "$\\Delta$AUROC": fmt(delta["auroc_delta_b_minus_a"]),
                "95\\% CI": f"[{fmt(delta['auroc_delta_ci_low'])}, {fmt(delta['auroc_delta_ci_high'])}]",
                "Shift": fmt(delta["mean_abs_score_shift"]),
            }
        )
    write_latex(
        pd.DataFrame(candidate_rows),
        OUT_DIR / "candidate_protocol_sensitivity.tex",
        "Candidate-quality protocol sensitivity. Protocol columns report Spearman / AUROC.",
        "tab:candidate_protocol_sensitivity",
    )

    semantic_rows = []
    for language in ["es-ES", "tr", "vi"]:
        sub = semantic[(semantic["language"] == language) & (semantic["dimension"] == "main_ideas")]
        best = sub.sort_values("auroc", ascending=False).iloc[0]
        semantic_rows.append(
            {
                "Language": language,
                "Best": best["protocol"],
                "Best Sp/AUROC": f"{fmt(best['spearman'])} / {fmt(best['auroc'])}",
                "Direct": sp_auc(semantic, language, "main_ideas", "P0_direct_english"),
                "Pivot": sp_auc(semantic, language, "main_ideas", "P2_explicit_pivot"),
                "Bilingual": sp_auc(semantic, language, "main_ideas", "P3_bilingual"),
            }
        )
    write_latex(
        pd.DataFrame(semantic_rows),
        OUT_DIR / "semantic_main_ideas.tex",
        "Source-grounded XLSum main-ideas alignment by protocol. Values are Spearman / AUROC.",
        "tab:semantic_main_ideas",
    )

    audit_rows = []
    for language, dimension in [("tr", "comprehensibility"), ("vi", "grammar")]:
        audit_delta_direct = pair(
            audit_pair,
            language,
            dimension,
            "P0_direct_english",
            "P2_explicit_pivot",
        )
        audit_delta_bilingual = pair(
            audit_pair,
            language,
            dimension,
            "P2_explicit_pivot",
            "P3_bilingual",
        )
        audit_rows.append(
            {
                "Cell": f"{language} / {dimension}",
                "Direct": sp_auc(audit, language, dimension, "P0_direct_english"),
                "Pivot": sp_auc(audit, language, dimension, "P2_explicit_pivot"),
                "Bilingual": sp_auc(audit, language, dimension, "P3_bilingual"),
                "Pivot-Direct $\\Delta$AUROC": fmt(audit_delta_direct["auroc_delta_b_minus_a"]),
                "Bilingual-Pivot $\\Delta$AUROC": fmt(audit_delta_bilingual["auroc_delta_b_minus_a"]),
            }
        )
    write_latex(
        pd.DataFrame(audit_rows),
        OUT_DIR / "stronger_judge_audit.tex",
        "Stronger-judge audit on a stratified n=25-per-cell subset.",
        "tab:stronger_judge_audit",
    )

    wmt_rows = []
    for setting, metrics_df, pair_df, dimension in [
        ("Reference", wmt, wmt_pair, "translation_quality"),
        ("Ref-free", wmt_ref_free, wmt_ref_free_pair, "translation_quality_ref_free"),
    ]:
        for language in ["en-de", "en-ru", "zh-en"]:
            sub = metrics_df[(metrics_df["language"] == language) & (metrics_df["dimension"] == dimension)]
            if sub.empty:
                continue
            best = sub.sort_values("auroc", ascending=False).iloc[0]
            delta = pair(
                pair_df,
                language,
                dimension,
                "P0_direct_english",
                "P2_explicit_pivot",
            )
            wmt_rows.append(
                {
                    "Setting": setting,
                    "Pair": language,
                    "Best": best["protocol"],
                    "Best Sp/AUROC": f"{fmt(best['spearman'])} / {fmt(best['auroc'])}",
                    "Direct": sp_auc(metrics_df, language, dimension, "P0_direct_english"),
                    "Target": sp_auc_optional(metrics_df, language, dimension, "P1_target_rubric"),
                    "Pivot": sp_auc(metrics_df, language, dimension, "P2_explicit_pivot"),
                    "Bilingual": sp_auc_optional(metrics_df, language, dimension, "P3_bilingual"),
                    "Pivot-Direct $\\Delta$AUROC": fmt(delta["auroc_delta_b_minus_a"]),
                }
            )
    write_latex(
        pd.DataFrame(wmt_rows),
        OUT_DIR / "wmt_translation_quality.tex",
        "WMT MQM translation-quality protocol extension. Values are Spearman / AUROC.",
        "tab:wmt_translation_quality",
    )

    wmt_audit_specs = [
        (
            "zh-en ref-free",
            wmt_zh_audit,
            wmt_zh_audit_pair,
            "zh-en",
            "P0_direct_english",
            "P2_explicit_pivot",
            "Pivot - direct",
            "Direct",
            "Pivot",
        ),
        (
            "en-de ref-free",
            wmt_de_audit,
            wmt_de_audit_pair,
            "en-de",
            "P2_explicit_pivot",
            "P3_bilingual",
            "Bilingual - pivot",
            "Pivot",
            "Bilingual",
        ),
    ]
    wmt_audit_rows = []
    for cell, metrics_df, pair_df, language, protocol_a, protocol_b, comparison, a_name, b_name in wmt_audit_specs:
        delta = pair(
            pair_df,
            language,
            "translation_quality_ref_free",
            protocol_a,
            protocol_b,
        )
        wmt_audit_rows.append(
            {
                "Cell": cell,
                "Comparison": comparison,
                "Protocol A": a_name,
                "A Sp/AUROC": sp_auc(metrics_df, language, "translation_quality_ref_free", protocol_a),
                "Protocol B": b_name,
                "B Sp/AUROC": sp_auc(metrics_df, language, "translation_quality_ref_free", protocol_b),
                "$\\Delta$AUROC": fmt(delta["auroc_delta_b_minus_a"]),
                "95\\% CI": f"[{fmt(delta['auroc_delta_ci_low'])}, {fmt(delta['auroc_delta_ci_high'])}]",
                "Shift": fmt(delta["mean_abs_score_shift"]),
            }
        )
    write_latex(
        pd.DataFrame(wmt_audit_rows),
        OUT_DIR / "wmt_ref_free_stronger_audit.tex",
        "Targeted WMT reference-free stronger-judge audit with \\texttt{gpt-4.1-mini}. Values are Spearman / AUROC.",
        "tab:wmt_ref_free_stronger_audit",
    )

    instability_rows = []
    for _, row in instability.iterrows():
        n_cells = row["n_cells"]
        instability_rows.append(
            {
                "Run": row["run"],
                "Cells": int(n_cells),
                "Median range": fmt(row["median_auroc_range"]),
                "Max range": fmt(row["max_auroc_range"]),
                "Range $\\geq$ .10": frac(row["cells_auroc_range_ge_0_10"], n_cells),
                "Best $\\neq$ direct": frac(row["cells_best_not_direct"], n_cells),
                "Pivot worst": frac(row["cells_pivot_worst"], n_cells),
                "Sig. cells": frac(row["cells_with_significant_auroc_pair"], n_cells),
                "Max shift": fmt(row["max_mean_abs_score_shift"]),
            }
        )
    write_latex(
        pd.DataFrame(instability_rows),
        OUT_DIR / "protocol_instability_summary.tex",
        "Protocol-instability summary by run. AUROC range is best minus worst protocol within a language/dimension cell.",
        "tab:protocol_instability_summary",
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
                    "Run": run,
                    "Dimension": row["dimension"],
                    "Protocol": row["protocol"],
                    "Gap": fmt(row["spearman_language_gap"]),
                    "Min": f"{row['min_spearman_language']} ({fmt(row['min_spearman'])})",
                    "Max": f"{row['max_spearman_language']} ({fmt(row['max_spearman'])})",
                }
            )
    write_latex(
        pd.DataFrame(gap_rows),
        OUT_DIR / "language_gaps.tex",
        "Largest cross-language Spearman gaps.",
        "tab:language_gaps",
    )

    calibration_rows = []
    for name, path in [
        ("candidate n50", "data/analysis/candidate_n50_combined_explicit_calibration.csv"),
        ("audit n25", "data/analysis/audit_gpt41mini_n25_combined_explicit_calibration.csv"),
        ("semantic n30", "data/analysis/semantic_xlsum_n30_calibration.csv"),
        ("wmt n30", "data/analysis/wmt_mqm_n30_calibration.csv"),
        ("wmt ref-free n30", "data/analysis/wmt_mqm_ref_free_n30_calibration.csv"),
        ("wmt audit zh-en", "data/analysis/wmt_mqm_ref_free_audit_zh_en_gpt41mini_calibration.csv"),
        ("wmt audit en-de", "data/analysis/wmt_mqm_ref_free_audit_en_de_gpt41mini_calibration.csv"),
    ]:
        df = pd.read_csv(path)
        test = df[df["split"] == "test"]
        calibration_rows.append(
            {
                "Run": name,
                "Groups": len(test),
                "Mean $\\Delta$BalAcc": fmt(test["delta_balanced_accuracy"].mean()),
                "Median $\\Delta$BalAcc": fmt(test["delta_balanced_accuracy"].median()),
            }
        )
    write_latex(
        pd.DataFrame(calibration_rows),
        OUT_DIR / "calibration_summary.tex",
        "Held-out threshold calibration effects.",
        "tab:calibration_summary",
    )

    inventory_rows = []
    for _, row in run_inventory.iterrows():
        inventory_rows.append(
            {
                "Run": row["run"],
                "Base": int(row["base_items"]),
                "Calls": int(row["judge_calls"]),
                "Parse": f"{100.0 * row['parse_rate']:.1f}\\%",
                "Cost": fmt(row["observed_cost_usd"], 4),
                "Cost/1k": fmt(row["cost_per_1000_judge_calls"], 3),
            }
        )
    write_latex(
        pd.DataFrame(inventory_rows),
        OUT_DIR / "run_inventory.tex",
        "Run inventory, parse rate, and observed incremental API cost.",
        "tab:run_inventory",
    )

    usage_rows = []
    for _, row in run_inventory.iterrows():
        usage_rows.append(
            {
                "Run": row["run"],
                "API calls": int(row["api_calls_including_translations"]),
                "Input tok.": int(row["input_tokens"]),
                "Output tok.": int(row["output_tokens"]),
                "Total tok.": int(row["total_tokens"]),
                "Tok./call": fmt(row["avg_total_tokens_per_api_call"], 1),
            }
        )
    write_latex(
        pd.DataFrame(usage_rows),
        OUT_DIR / "api_usage_inventory.tex",
        "Price-independent API usage inventory from returned token metadata. API calls include translation calls and retries recorded in the run cost paths.",
        "tab:api_usage_inventory",
    )

    curve_rows = []
    curve_runs = [
        "candidate n50",
        "semantic n30",
        "wmt reference n30",
        "wmt ref-free n30",
        "candidate audit n25",
    ]
    for run in curve_runs:
        sub = calibration_curve[calibration_curve["run"] == run].set_index("n_calibration")
        if sub.empty:
            continue
        largest = sub.loc[sub.index.max()]
        curve_rows.append(
            {
                "Run": run,
                "$n_{cal}=2$": fmt(sub.loc[2, "mean_delta_balanced_accuracy"]) if 2 in sub.index else "",
                "$n_{cal}=8$": fmt(sub.loc[8, "mean_delta_balanced_accuracy"]) if 8 in sub.index else "",
                "Largest $n_{cal}$": int(largest.name),
                "Largest $\\Delta$": fmt(largest["mean_delta_balanced_accuracy"]),
                "P(improve)": fmt(largest["prob_improves"]),
                "P(degrade)": fmt(largest["prob_degrades"]),
            }
        )
    write_latex(
        pd.DataFrame(curve_rows),
        OUT_DIR / "calibration_learning_curve.tex",
        "Repeated threshold-calibration learning curve. Entries are mean held-out balanced-accuracy deltas over repeated stratified calibration samples.",
        "tab:calibration_learning_curve",
    )

    cost_rows = [
        {
            "Run": "candidate n50",
            "Approx. cost": fmt(
                cost(
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
            "Run": "audit n25",
            "Approx. cost": fmt(
                cost(
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
            "Run": "semantic n30",
            "Approx. cost": fmt(
                cost(
                    [
                        "data/processed/semantic_xlsum_n30_english_translations.jsonl",
                        "data/responses/semantic_xlsum_n30_responses.jsonl",
                    ]
                ),
                4,
            ),
        },
        {
            "Run": "wmt n30",
            "Approx. cost": fmt(
                cost(
                    [
                        "data/processed/wmt_mqm_n30_english_translations.jsonl",
                        "data/responses/wmt_mqm_n30_responses.jsonl",
                    ]
                ),
                4,
            ),
        },
        {
            "Run": "wmt ref-free n30",
            "Approx. cost": fmt(
                cost(
                    [
                        "data/responses/wmt_mqm_ref_free_n30_responses.jsonl",
                    ]
                ),
                4,
            ),
        },
        {
            "Run": "wmt ref-free audit",
            "Approx. cost": fmt(
                cost(
                    [
                        "data/responses/wmt_mqm_ref_free_audit_zh_en_gpt41mini_responses.jsonl",
                        "data/responses/wmt_mqm_ref_free_audit_en_de_gpt41mini_responses.jsonl",
                    ]
                ),
                4,
            ),
        },
    ]
    write_latex(
        pd.DataFrame(cost_rows),
        OUT_DIR / "api_costs.tex",
        "Observed API cost estimates from returned usage metadata.",
        "tab:api_costs",
    )

    print(f"Wrote tables to {OUT_DIR}")


if __name__ == "__main__":
    main()
