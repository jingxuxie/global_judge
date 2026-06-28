from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


OUT_CSV = Path("data/analysis/claim_evidence_matrix.csv")
OUT_MD = Path("data/analysis/claim_evidence_matrix.md")
OUT_TEX = Path("paper/tables/claim_evidence_matrix.tex")


def fmt(value: float, digits: int = 3) -> str:
    return f"{float(value):.{digits}f}"


def latex_escape(value: object) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(char, char) for char in str(value))


def metric(df: pd.DataFrame, language: str, dimension: str, protocol: str) -> pd.Series:
    rows = df[(df["language"] == language) & (df["dimension"] == dimension) & (df["protocol"] == protocol)]
    if rows.empty:
        raise KeyError((language, dimension, protocol))
    return rows.iloc[0]


def pair(df: pd.DataFrame, language: str, dimension: str, protocol_a: str, protocol_b: str) -> pd.Series:
    rows = df[
        (df["language"] == language)
        & (df["dimension"] == dimension)
        & (df["protocol_a"] == protocol_a)
        & (df["protocol_b"] == protocol_b)
    ]
    if rows.empty:
        raise KeyError((language, dimension, protocol_a, protocol_b))
    return rows.iloc[0]


def make_rows() -> list[dict[str, Any]]:
    candidate = pd.read_csv("data/analysis/candidate_n50_combined_explicit_metrics.csv")
    candidate_pair = pd.read_csv("data/analysis/candidate_n50_combined_explicit_metrics_pairwise_bootstrap.csv")
    audit_pair = pd.read_csv("data/analysis/audit_gpt41mini_n25_combined_explicit_metrics_pairwise_bootstrap.csv")
    semantic = pd.read_csv("data/analysis/semantic_xlsum_n30_metrics.csv")
    semantic_pair = pd.read_csv("data/analysis/semantic_xlsum_n30_metrics_pairwise_bootstrap.csv")
    wmt_pair = pd.read_csv("data/analysis/wmt_mqm_n30_metrics_pairwise_bootstrap.csv")
    wmt_ref_free_pair = pd.read_csv("data/analysis/wmt_mqm_ref_free_n30_metrics_pairwise_bootstrap.csv")
    wmt_audit_zh_pair = pd.read_csv(
        "data/analysis/wmt_mqm_ref_free_audit_zh_en_gpt41mini_metrics_pairwise_bootstrap.csv"
    )
    wmt_audit_de_pair = pd.read_csv(
        "data/analysis/wmt_mqm_ref_free_audit_en_de_gpt41mini_metrics_pairwise_bootstrap.csv"
    )
    instability = pd.read_csv("data/analysis/protocol_instability_summary.csv")
    calibration_curve = pd.read_csv("data/analysis/calibration_learning_curve_summary.csv")
    score_threshold = pd.read_csv("data/analysis/score_threshold_diagnostic_summary.csv")
    repeatability = pd.read_csv("data/analysis/repeatability_control_summary.csv")
    run_inventory = pd.read_csv("data/analysis/run_inventory.csv")
    sampling = pd.read_csv("data/analysis/dataset_sampling_summary.csv")
    prompt_inventory = pd.read_csv("data/analysis/prompt_inventory_summary.csv")

    vi_shift = pair(candidate_pair, "vi", "grammar", "P1_target_rubric", "P2_explicit_pivot")
    tr_direct = metric(candidate, "tr", "comprehensibility", "P0_direct_english")
    tr_pivot = metric(candidate, "tr", "comprehensibility", "P2_explicit_pivot")
    tr_delta = pair(candidate_pair, "tr", "comprehensibility", "P0_direct_english", "P2_explicit_pivot")
    audit_tr_direct = pair(audit_pair, "tr", "comprehensibility", "P0_direct_english", "P2_explicit_pivot")
    audit_tr_bi = pair(audit_pair, "tr", "comprehensibility", "P2_explicit_pivot", "P3_bilingual")
    semantic_tr = pair(semantic_pair, "tr", "main_ideas", "P2_explicit_pivot", "P3_bilingual")
    semantic_vi = pair(semantic_pair, "vi", "main_ideas", "P2_explicit_pivot", "P3_bilingual")
    semantic_vi_pivot = metric(semantic, "vi", "main_ideas", "P2_explicit_pivot")
    wmt_ref_zh = pair(wmt_pair, "zh-en", "translation_quality", "P0_direct_english", "P2_explicit_pivot")
    wmt_ref_free_zh = pair(
        wmt_ref_free_pair,
        "zh-en",
        "translation_quality_ref_free",
        "P0_direct_english",
        "P2_explicit_pivot",
    )
    wmt_audit_zh = pair(
        wmt_audit_zh_pair,
        "zh-en",
        "translation_quality_ref_free",
        "P0_direct_english",
        "P2_explicit_pivot",
    )
    wmt_audit_de = pair(
        wmt_audit_de_pair,
        "en-de",
        "translation_quality_ref_free",
        "P2_explicit_pivot",
        "P3_bilingual",
    )
    main_instability = instability[~instability["run"].str.contains("audit")]
    semantic_curve = calibration_curve[
        (calibration_curve["run"] == "semantic n30") & (calibration_curve["n_calibration"] == 24)
    ].iloc[0]
    candidate_curve = calibration_curve[
        (calibration_curve["run"] == "candidate n50") & (calibration_curve["n_calibration"] == 24)
    ].iloc[0]
    semantic_threshold = score_threshold[score_threshold["run"] == "semantic n30"].iloc[0]
    wmt_threshold = score_threshold[score_threshold["run"] == "wmt ref-free n30"].iloc[0]
    exact_repeat = repeatability[repeatability["control"] == "exact original-text prompt repeat"].iloc[0]
    candidate_inventory = run_inventory[run_inventory["run"] == "candidate n50"].iloc[0]
    sampling_candidate = sampling[sampling["run"] == "candidate n50"].iloc[0]
    prompt_candidate = prompt_inventory[prompt_inventory["run"] == "candidate n50"].iloc[0]

    rows = [
        {
            "claim": "Same-item scores change materially across judge protocols.",
            "evidence": (
                "vi/grammar target-vs-pivot mean absolute shift "
                f"{fmt(vi_shift['mean_abs_score_shift'], 2)}; "
                f"{100 * vi_shift['large_shift_rate_abs_ge_2']:.1f}% shift by at least 2."
            ),
            "artifact": "data/analysis/candidate_n50_combined_explicit_metrics_pairwise_bootstrap.csv",
            "validator_coverage": "vi grammar shift and large-shift checks",
        },
        {
            "claim": "English pivot is not a safe default for candidate-quality judging.",
            "evidence": (
                "tr/comprehensibility direct AUROC "
                f"{fmt(tr_direct['auroc'])} vs pivot {fmt(tr_pivot['auroc'])}; "
                f"pivot-direct delta {fmt(tr_delta['auroc_delta_b_minus_a'])} "
                f"CI [{fmt(tr_delta['auroc_delta_ci_low'])}, {fmt(tr_delta['auroc_delta_ci_high'])}]."
            ),
            "artifact": "data/analysis/candidate_n50_combined_explicit_metrics.csv; data/analysis/candidate_n50_combined_explicit_metrics_pairwise_bootstrap.csv",
            "validator_coverage": "tr direct/pivot Spearman, AUROC, and delta checks",
        },
        {
            "claim": "The main pivot failure survives a stronger OpenAI judge audit.",
            "evidence": (
                "gpt-4.1-mini tr/comprehensibility pivot-direct AUROC delta "
                f"{fmt(audit_tr_direct['auroc_delta_b_minus_a'])}; "
                f"bilingual-pivot delta {fmt(audit_tr_bi['auroc_delta_b_minus_a'])}."
            ),
            "artifact": "data/analysis/audit_gpt41mini_n25_combined_explicit_metrics_pairwise_bootstrap.csv",
            "validator_coverage": "stronger audit tr bilingual-pivot delta check",
        },
        {
            "claim": "Source-grounded semantic judging is also protocol-sensitive and language-dependent.",
            "evidence": (
                "tr bilingual-pivot AUROC delta "
                f"{fmt(semantic_tr['auroc_delta_b_minus_a'])}; "
                f"vi bilingual-pivot delta {fmt(semantic_vi['auroc_delta_b_minus_a'])}; "
                f"vi pivot AUROC {fmt(semantic_vi_pivot['auroc'])}."
            ),
            "artifact": "data/analysis/semantic_xlsum_n30_metrics.csv; data/analysis/semantic_xlsum_n30_metrics_pairwise_bootstrap.csv",
            "validator_coverage": "semantic tr bilingual-pivot delta check",
        },
        {
            "claim": "WMT is contrast evidence, not a stable global protocol ranking.",
            "evidence": (
                "reference zh-en pivot-direct delta "
                f"{fmt(wmt_ref_zh['auroc_delta_b_minus_a'])}; "
                f"ref-free zh-en delta {fmt(wmt_ref_free_zh['auroc_delta_b_minus_a'])}; "
                f"stronger audit zh-en delta {fmt(wmt_audit_zh['auroc_delta_b_minus_a'])}; "
                f"stronger audit en-de bilingual-pivot delta {fmt(wmt_audit_de['auroc_delta_b_minus_a'])}."
            ),
            "artifact": "data/analysis/wmt_mqm_n30_metrics_pairwise_bootstrap.csv; data/analysis/wmt_mqm_ref_free_n30_metrics_pairwise_bootstrap.csv; data/analysis/wmt_mqm_ref_free_audit_*_metrics_pairwise_bootstrap.csv",
            "validator_coverage": "WMT ref-free zh-en delta check plus required audit artifacts",
        },
        {
            "claim": "No single protocol dominates across cells.",
            "evidence": (
                f"{int(main_instability['n_cells'].sum())} non-audit cells; "
                f"best protocol not direct in {int(main_instability['cells_best_not_direct'].sum())}; "
                f"pivot worst in {int(main_instability['cells_pivot_worst'].sum())}; "
                f"significant AUROC pair in {int(main_instability['cells_with_significant_auroc_pair'].sum())}."
            ),
            "artifact": "data/analysis/protocol_instability_summary.csv",
            "validator_coverage": "aggregate instability count checks",
        },
        {
            "claim": "Calibration is a diagnostic, not a universal fix.",
            "evidence": (
                "semantic largest-budget balanced-accuracy delta "
                f"{fmt(semantic_curve['mean_delta_balanced_accuracy'])}; "
                f"candidate n50 delta {fmt(candidate_curve['mean_delta_balanced_accuracy'])}; "
                f"semantic score>=4 good-rate {100 * semantic_threshold['predicted_good_rate_threshold_4']:.1f}%; "
                f"WMT ref-free score>=4 good-rate {100 * wmt_threshold['predicted_good_rate_threshold_4']:.1f}%."
            ),
            "artifact": "data/analysis/calibration_learning_curve_summary.csv; data/analysis/score_threshold_diagnostic_summary.csv",
            "validator_coverage": "calibration curve and score-threshold checks",
        },
        {
            "claim": "Large protocol shifts exceed ordinary exact-prompt repeat variation.",
            "evidence": (
                f"{int(exact_repeat['n_scored_pairs'])} exact repeated prompts; "
                f"exact agreement {100 * exact_repeat['exact_score_agreement']:.1f}%; "
                f"mean absolute score delta {fmt(exact_repeat['mean_abs_score_delta'])}."
            ),
            "artifact": "data/analysis/repeatability_control_summary.csv",
            "validator_coverage": "repeatability count, agreement, and mean-delta checks",
        },
        {
            "claim": "The run package is auditable for sampling, prompts, parse rate, usage, and cost.",
            "evidence": (
                f"candidate n50 sampling {int(sampling_candidate['human_positive'])}/"
                f"{int(sampling_candidate['human_negative'])} pos/neg; "
                f"{int(prompt_candidate['prompts'])} candidate prompts; "
                f"{100 * candidate_inventory['parse_rate']:.1f}% parse rate; "
                f"{int(candidate_inventory['total_tokens'])} candidate total tokens."
            ),
            "artifact": "data/analysis/dataset_sampling_summary.csv; data/analysis/prompt_inventory_summary.csv; data/analysis/run_inventory.csv; data/analysis/reproducibility_manifest.json",
            "validator_coverage": "sampling, prompt inventory, parse-rate, token, and manifest checks",
        },
    ]
    return rows


def write_markdown(df: pd.DataFrame) -> None:
    lines = [
        "# Claim Evidence Matrix",
        "",
        "Each row maps a paper-facing claim to concrete evidence artifacts and validator coverage.",
        "",
        "| Claim | Evidence | Artifact | Validator Coverage |",
        "| --- | --- | --- | --- |",
    ]
    for _, row in df.iterrows():
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["claim"]),
                    str(row["evidence"]),
                    str(row["artifact"]),
                    str(row["validator_coverage"]),
                ]
            )
            + " |"
        )
    lines.append("")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def write_latex(df: pd.DataFrame) -> None:
    OUT_TEX.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "\\begin{table}[t]",
        "\\centering",
        "\\caption{Claim evidence matrix. Full artifact paths are provided in \\texttt{data/analysis/claim\\_evidence\\_matrix.md}.}",
        "\\label{tab:claim_evidence_matrix}",
        "\\resizebox{\\linewidth}{!}{%",
        "\\begin{tabular}{lll}",
        "\\toprule",
        "Claim & Evidence summary & Validator coverage \\\\",
        "\\midrule",
    ]
    for _, row in df.iterrows():
        lines.append(
            " & ".join(
                [
                    latex_escape(row["claim"]),
                    latex_escape(row["evidence"]),
                    latex_escape(row["validator_coverage"]),
                ]
            )
            + " \\\\"
        )
    lines.extend(["\\bottomrule", "\\end{tabular}%", "}", "\\end{table}", ""])
    OUT_TEX.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(make_rows())
    df.to_csv(OUT_CSV, index=False)
    write_markdown(df)
    write_latex(df)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    print(f"Wrote {OUT_TEX}")


if __name__ == "__main__":
    main()
