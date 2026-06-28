from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


OUT_CSV = Path("data/analysis/rq_contribution_matrix.csv")
OUT_MD = Path("data/analysis/rq_contribution_matrix.md")
OUT_TEX = Path("paper/tables/rq_contribution_matrix.tex")


def fmt(value: float | int, digits: int = 3) -> str:
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


def row_by(df: pd.DataFrame, column: str, value: str) -> pd.Series:
    rows = df[df[column] == value]
    if rows.empty:
        raise KeyError((column, value))
    return rows.iloc[0]


def gap(df: pd.DataFrame, dimension: str, protocol: str) -> pd.Series:
    rows = df[(df["dimension"] == dimension) & (df["protocol"] == protocol)]
    if rows.empty:
        raise KeyError((dimension, protocol))
    return rows.iloc[0]


def calibration_row(df: pd.DataFrame, run: str, n_calibration: int = 24) -> pd.Series:
    rows = df[(df["run"] == run) & (df["n_calibration"] == n_calibration)]
    if rows.empty:
        raise KeyError((run, n_calibration))
    return rows.iloc[0]


def make_rows() -> list[dict[str, Any]]:
    sampling = pd.read_csv("data/analysis/dataset_sampling_summary.csv")
    prompt_inventory = pd.read_csv("data/analysis/prompt_inventory_summary.csv")
    instability = pd.read_csv("data/analysis/protocol_instability_summary.csv")
    candidate_gaps = pd.read_csv("data/analysis/candidate_n50_combined_explicit_metrics_language_gaps.csv")
    semantic_gaps = pd.read_csv("data/analysis/semantic_xlsum_n30_metrics_language_gaps.csv")
    wmt_ref_free_gaps = pd.read_csv("data/analysis/wmt_mqm_ref_free_n30_metrics_language_gaps.csv")
    calibration = pd.read_csv("data/analysis/calibration_learning_curve_summary.csv")
    repeatability = pd.read_csv("data/analysis/repeatability_control_summary.csv")
    run_inventory = pd.read_csv("data/analysis/run_inventory.csv")

    candidate_items = int(row_by(sampling, "run", "candidate n50")["items"])
    semantic_items = int(row_by(sampling, "run", "semantic n30")["items"])
    wmt_items = int(row_by(sampling, "run", "wmt n30 shared items")["items"])
    audit_items = int(row_by(sampling, "run", "candidate audit n25")["items"])
    wmt_audit_items = int(
        row_by(sampling, "run", "wmt ref-free audit zh-en")["items"]
        + row_by(sampling, "run", "wmt ref-free audit en-de")["items"]
    )
    main_items = candidate_items + semantic_items + wmt_items
    total_prompts = int(prompt_inventory["prompts"].sum())
    judge_models = ", ".join(sorted({model for models in prompt_inventory["judge_models"] for model in models.split(", ")}))

    main_instability = instability[~instability["run"].str.contains("audit")]
    non_audit_cells = int(main_instability["n_cells"].sum())
    best_not_direct = int(main_instability["cells_best_not_direct"].sum())
    pivot_worst = int(main_instability["cells_pivot_worst"].sum())
    significant_cells = int(main_instability["cells_with_significant_auroc_pair"].sum())
    max_main_shift = float(main_instability["max_mean_abs_score_shift"].max())

    candidate_pivot_gap = gap(candidate_gaps, "comprehensibility", "P2_explicit_pivot")
    semantic_pivot_gap = gap(semantic_gaps, "main_ideas", "P2_explicit_pivot")
    wmt_direct_gap = gap(wmt_ref_free_gaps, "translation_quality_ref_free", "P0_direct_english")

    candidate_instability = row_by(instability, "run", "candidate n50")
    semantic_instability = row_by(instability, "run", "semantic n30")
    wmt_reference_instability = row_by(instability, "run", "wmt reference n30")
    wmt_ref_free_instability = row_by(instability, "run", "wmt ref-free n30")

    candidate_cal = calibration_row(calibration, "candidate n50")
    semantic_cal = calibration_row(calibration, "semantic n30")
    wmt_ref_free_cal = calibration_row(calibration, "wmt ref-free n30")

    exact_repeat = row_by(repeatability, "control", "exact original-text prompt repeat")
    pivot_repeat = row_by(repeatability, "control", "explicit-pivot pipeline repeat")

    total_judge_calls = int(run_inventory["judge_calls"].sum())
    total_tokens = int(run_inventory["total_tokens"].sum())
    all_parse = float(run_inventory["parse_rate"].min())
    selected_cost = float(run_inventory["observed_cost_usd"].sum())

    return [
        {
            "plan_item": "RQ1: judge reliability changes by language",
            "coverage": "covered",
            "evidence": (
                "Language gaps are reported per protocol: candidate comprehensibility pivot Spearman gap "
                f"{fmt(candidate_pivot_gap['spearman_language_gap'])}; semantic pivot gap "
                f"{fmt(semantic_pivot_gap['spearman_language_gap'])}; WMT ref-free direct gap "
                f"{fmt(wmt_direct_gap['spearman_language_gap'])}."
            ),
            "primary_artifacts": "language-gap CSVs; paper/tables/language_gaps.tex",
            "claim_boundary": "Per-language evidence is strong for current sampled languages, not a universal language ranking.",
        },
        {
            "plan_item": "RQ2: evaluation protocol changes the result",
            "coverage": "covered",
            "evidence": (
                f"Across {non_audit_cells} non-audit cells, best protocol is not direct in {best_not_direct}, "
                f"pivot is worst in {pivot_worst}, {significant_cells} cells have a significant AUROC pair, "
                f"and max same-item shift is {fmt(max_main_shift, 2)}."
            ),
            "primary_artifacts": "data/analysis/protocol_instability_summary.csv; paired-bootstrap CSVs",
            "claim_boundary": "Protocol sensitivity is the central claim; no single protocol is claimed globally optimal.",
        },
        {
            "plan_item": "RQ3: protocol effects differ by quality dimension/task",
            "coverage": "covered with contrast evidence",
            "evidence": (
                "Max same-item shifts differ by setting: candidate-quality "
                f"{fmt(candidate_instability['max_mean_abs_score_shift'], 2)}, semantic "
                f"{fmt(semantic_instability['max_mean_abs_score_shift'], 2)}, WMT reference "
                f"{fmt(wmt_reference_instability['max_mean_abs_score_shift'], 2)}, WMT ref-free "
                f"{fmt(wmt_ref_free_instability['max_mean_abs_score_shift'], 2)}."
            ),
            "primary_artifacts": "candidate, semantic, and WMT protocol-shift and metrics CSVs",
            "claim_boundary": "Dimension story is empirical and bounded; native form-sensitive dimensions remain the clearest risk case.",
        },
        {
            "plan_item": "RQ4: small human calibration set",
            "coverage": "covered as diagnostic",
            "evidence": (
                "At 24 calibration examples, balanced-accuracy deltas are candidate "
                f"{fmt(candidate_cal['mean_delta_balanced_accuracy'])}, semantic "
                f"{fmt(semantic_cal['mean_delta_balanced_accuracy'])}, and WMT ref-free "
                f"{fmt(wmt_ref_free_cal['mean_delta_balanced_accuracy'])}."
            ),
            "primary_artifacts": "data/analysis/calibration_learning_curve_summary.csv; score-threshold diagnostic",
            "claim_boundary": "Calibration is framed as score-distribution diagnosis, not a universal repair.",
        },
        {
            "plan_item": "Contribution 1: GlobalJudge-ProtocolBench scaffold",
            "coverage": "covered for workshop scale",
            "evidence": (
                f"{main_items} main base items plus {audit_items} candidate audit items and "
                f"{wmt_audit_items} targeted WMT audit subset rows; {total_prompts} prompts across "
                f"{judge_models}."
            ),
            "primary_artifacts": "processed item JSONLs; prompt inventory; reproducibility manifest",
            "claim_boundary": "Scope is compact and intentionally bounded; larger model-family coverage is future work.",
        },
        {
            "plan_item": "Contribution 2: protocol-sensitivity metrics",
            "coverage": "covered",
            "evidence": (
                "Tables report Spearman/AUROC, paired AUROC deltas, same-item shifts, language gaps, "
                "parse rate, token usage, and cost-per-1k judgments."
            ),
            "primary_artifacts": "paper/tables/*.tex; data/analysis/run_inventory.csv",
            "claim_boundary": "Kendall, Pearson, Brier score, and pairwise position-bias tests are not claimed.",
        },
        {
            "plan_item": "Contribution 3: calibration recipe",
            "coverage": "covered with caveat",
            "evidence": (
                "Repeated stratified threshold calibration uses 50 trials per eligible group and budgets from "
                "2 to 24 calibration examples; threshold diagnostic explains low semantic scores and high WMT ref-free scores."
            ),
            "primary_artifacts": "calibration learning curve; score-threshold diagnostic; calibration tables",
            "claim_boundary": "Post-hoc threshold calibration is included; few-shot calibrated prompting is not run.",
        },
        {
            "plan_item": "Contribution 4: Global Judge Reporting Card",
            "coverage": "covered",
            "evidence": "Reporting card lists judge configuration, protocol surface, human alignment, protocol sensitivity, calibration, reproducibility, and cost fields.",
            "primary_artifacts": "paper/reporting_card.md; paper/main.tex reporting-card section",
            "claim_boundary": "Checklist is a recommended reporting practice, not a validated standard.",
        },
        {
            "plan_item": "Stability and rerun control",
            "coverage": "covered",
            "evidence": (
                f"{int(exact_repeat['n_scored_pairs'])} exact repeated prompts have "
                f"{100 * exact_repeat['exact_score_agreement']:.1f}% exact agreement and mean delta "
                f"{fmt(exact_repeat['mean_abs_score_delta'])}; {int(pivot_repeat['n_scored_pairs'])} "
                "pivot-pipeline repeats expose regenerated-translation volatility."
            ),
            "primary_artifacts": "data/analysis/repeatability_control_summary.csv; paper/tables/repeatability_control.tex",
            "claim_boundary": "The pivot repeat is not a pure stochasticity control because prompt text changed.",
        },
        {
            "plan_item": "Cost, parsing, and release auditability",
            "coverage": "covered",
            "evidence": (
                f"{total_judge_calls} judge calls, {100 * all_parse:.1f}% minimum parse rate, "
                f"{total_tokens} total returned tokens across paper-facing runs, and ${selected_cost:.4f} "
                "observed local cost estimate."
            ),
            "primary_artifacts": "run inventory; prompt inventory; sampling audit; reproducibility manifest",
            "claim_boundary": "Token usage is stable; dollar costs should be refreshed against provider pricing before submission.",
        },
    ]


def write_markdown(df: pd.DataFrame) -> None:
    lines = [
        "# RQ and Contribution Coverage Matrix",
        "",
        "This matrix maps the original project plan's research questions and contribution package to current evidence.",
        "",
        "| Plan Item | Coverage | Evidence | Primary Artifacts | Claim Boundary |",
        "| --- | --- | --- | --- | --- |",
    ]
    for _, row in df.iterrows():
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["plan_item"]),
                    str(row["coverage"]),
                    str(row["evidence"]),
                    str(row["primary_artifacts"]),
                    str(row["claim_boundary"]),
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
        "\\caption{Research-question and contribution coverage matrix. Full artifact paths are provided in \\texttt{data/analysis/rq\\_contribution\\_matrix.md}.}",
        "\\label{tab:rq_contribution_matrix}",
        "\\resizebox{\\linewidth}{!}{%",
        "\\begin{tabular}{llll}",
        "\\toprule",
        "Plan item & Coverage & Evidence summary & Claim boundary \\\\",
        "\\midrule",
    ]
    for _, row in df.iterrows():
        lines.append(
            " & ".join(
                [
                    latex_escape(row["plan_item"]),
                    latex_escape(row["coverage"]),
                    latex_escape(row["evidence"]),
                    latex_escape(row["claim_boundary"]),
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
