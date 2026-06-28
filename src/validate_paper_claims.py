from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pandas as pd


TOL = 5e-4


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def approx(value: float, expected: float, tol: float = TOL) -> bool:
    return abs(float(value) - expected) <= tol


def count_jsonl(path: str | Path) -> int:
    with Path(path).open("r", encoding="utf-8") as f:
        return sum(1 for line in f if line.strip())


def sum_cost(paths: list[str]) -> float:
    total = 0.0
    for path in paths:
        with Path(path).open("r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    total += json.loads(line).get("api_cost_estimate_usd") or 0.0
    return total


def pdf_pages(path: str | Path) -> int:
    result = subprocess.run(
        ["pdfinfo", str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    for line in result.stdout.splitlines():
        if line.startswith("Pages:"):
            return int(line.split(":", 1)[1].strip())
    raise AssertionError(f"Could not determine PDF page count for {path}")


def metric(df: pd.DataFrame, language: str, dimension: str, protocol: str) -> pd.Series:
    rows = df[(df.language == language) & (df.dimension == dimension) & (df.protocol == protocol)]
    if rows.empty:
        raise AssertionError(f"Missing metric row: {language} / {dimension} / {protocol}")
    return rows.iloc[0]


def pair(df: pd.DataFrame, language: str, dimension: str, protocol_a: str, protocol_b: str) -> pd.Series:
    rows = df[
        (df.language == language)
        & (df.dimension == dimension)
        & (df.protocol_a == protocol_a)
        & (df.protocol_b == protocol_b)
    ]
    if rows.empty:
        raise AssertionError(f"Missing pair row: {language} / {dimension} / {protocol_a} -> {protocol_b}")
    return rows.iloc[0]


def validate() -> list[str]:
    failures: list[str] = []

    required_files = [
        "paper/main.pdf",
        "paper/extended_abstract.tex",
        "paper/extended_abstract.pdf",
        "paper/submission_packet.md",
        "paper/globaljudge_protocolbench_datacard.md",
        "paper/results_brief.md",
        "paper/tables/candidate_protocol_sensitivity.tex",
        "paper/tables/stronger_judge_audit.tex",
        "paper/tables/semantic_main_ideas.tex",
        "paper/tables/wmt_translation_quality.tex",
        "paper/tables/wmt_ref_free_stronger_audit.tex",
        "paper/tables/dataset_sampling_audit.tex",
        "paper/tables/prompt_inventory.tex",
        "paper/tables/protocol_instability_summary.tex",
        "paper/tables/language_gaps.tex",
        "paper/tables/calibration_summary.tex",
        "paper/tables/calibration_learning_curve.tex",
        "paper/tables/score_threshold_diagnostic.tex",
        "paper/tables/repeatability_control.tex",
        "paper/tables/run_inventory.tex",
        "paper/tables/api_usage_inventory.tex",
        "paper/tables/api_costs.tex",
        "paper/tables/claim_evidence_matrix.tex",
        "paper/tables/rq_contribution_matrix.tex",
        "data/analysis/qualitative_protocol_examples.csv",
        "data/analysis/dataset_sampling_items.csv",
        "data/analysis/dataset_sampling_groups.csv",
        "data/analysis/dataset_sampling_summary.csv",
        "data/analysis/dataset_sampling_audit.md",
        "data/analysis/prompt_inventory.csv",
        "data/analysis/prompt_inventory_summary.csv",
        "data/analysis/prompt_inventory.md",
        "data/analysis/prompt_representatives.csv",
        "data/analysis/claim_evidence_matrix.csv",
        "data/analysis/claim_evidence_matrix.md",
        "data/analysis/rq_contribution_matrix.csv",
        "data/analysis/rq_contribution_matrix.md",
        "data/analysis/protocol_instability_summary.csv",
        "data/analysis/calibration_learning_curve_summary.csv",
        "data/analysis/score_threshold_diagnostic_summary.csv",
        "data/analysis/repeatability_control_summary.csv",
        "data/analysis/reproducibility_manifest.json",
        "data/analysis/reproducibility_manifest.md",
        "data/analysis/release_validation_report.json",
        "data/analysis/release_validation_report.md",
        "data/analysis/completion_audit.json",
        "data/analysis/completion_audit.md",
        "data/analysis/run_inventory.csv",
    ]
    for path in required_files:
        p = Path(path)
        require(p.exists() and p.stat().st_size > 0, f"Missing or empty required artifact: {path}", failures)
    try:
        require(pdf_pages("paper/extended_abstract.pdf") == 2, "Extended abstract is not 2 pages", failures)
    except Exception as exc:
        failures.append(f"Could not validate extended abstract page count: {exc}")
    submission_packet = Path("paper/submission_packet.md").read_text(encoding="utf-8")
    for phrase in [
        "Do not claim: a universal best protocol",
        "Only OpenAI judges are tested.",
        "Target-language rubrics are not native-speaker validated.",
        "Run `make -C paper`",
    ]:
        require(phrase in submission_packet, f"Submission packet missing phrase: {phrase}", failures)
    datacard = Path("paper/globaljudge_protocolbench_datacard.md").read_text(encoding="utf-8")
    for phrase in [
        "GlobalJudge-ProtocolBench Data Card",
        "Main paper-facing base items: 580.",
        "Prompt surfaces: P0_direct_english, P1_target_rubric, P2_explicit_pivot, P3_bilingual.",
        "Out-of-Scope Uses",
    ]:
        require(phrase in datacard, f"Benchmark data card missing phrase: {phrase}", failures)
    release_report = json.loads(Path("data/analysis/release_validation_report.json").read_text(encoding="utf-8"))
    require(release_report.get("status") == "passed", "Release validation report is not passing", failures)
    completion_audit = json.loads(Path("data/analysis/completion_audit.json").read_text(encoding="utf-8"))
    require(completion_audit.get("status") == "complete", "Completion audit is not complete", failures)

    expected_counts = {
        "data/processed/candidate_n50_items.jsonl": 400,
        "data/responses/candidate_n50_combined_explicit_responses.jsonl": 1600,
        "data/processed/audit_gpt41mini_n25_items.jsonl": 200,
        "data/responses/audit_gpt41mini_n25_combined_explicit_responses.jsonl": 800,
        "data/processed/semantic_xlsum_n30_items.jsonl": 90,
        "data/responses/semantic_xlsum_n30_responses.jsonl": 360,
        "data/processed/wmt_mqm_n30_items.jsonl": 90,
        "data/responses/wmt_mqm_n30_responses.jsonl": 300,
        "data/responses/wmt_mqm_ref_free_n30_responses.jsonl": 300,
        "data/responses/wmt_mqm_ref_free_audit_zh_en_gpt41mini_responses.jsonl": 60,
        "data/responses/wmt_mqm_ref_free_audit_en_de_gpt41mini_responses.jsonl": 60,
    }
    for path, expected in expected_counts.items():
        require(count_jsonl(path) == expected, f"{path} expected {expected} JSONL rows", failures)

    candidate = pd.read_csv("data/analysis/candidate_n50_combined_explicit_metrics.csv")
    candidate_pair = pd.read_csv("data/analysis/candidate_n50_combined_explicit_metrics_pairwise_bootstrap.csv")
    audit = pd.read_csv("data/analysis/audit_gpt41mini_n25_combined_explicit_metrics.csv")
    audit_pair = pd.read_csv("data/analysis/audit_gpt41mini_n25_combined_explicit_metrics_pairwise_bootstrap.csv")
    semantic = pd.read_csv("data/analysis/semantic_xlsum_n30_metrics.csv")
    semantic_pair = pd.read_csv("data/analysis/semantic_xlsum_n30_metrics_pairwise_bootstrap.csv")
    wmt_ref_free = pd.read_csv("data/analysis/wmt_mqm_ref_free_n30_metrics.csv")
    wmt_ref_free_pair = pd.read_csv("data/analysis/wmt_mqm_ref_free_n30_metrics_pairwise_bootstrap.csv")
    sampling = pd.read_csv("data/analysis/dataset_sampling_summary.csv")
    prompt_inventory = pd.read_csv("data/analysis/prompt_inventory_summary.csv")
    claim_matrix = pd.read_csv("data/analysis/claim_evidence_matrix.csv")
    rq_matrix = pd.read_csv("data/analysis/rq_contribution_matrix.csv")
    instability = pd.read_csv("data/analysis/protocol_instability_summary.csv")
    calibration_curve = pd.read_csv("data/analysis/calibration_learning_curve_summary.csv")
    score_threshold = pd.read_csv("data/analysis/score_threshold_diagnostic_summary.csv")
    repeatability = pd.read_csv("data/analysis/repeatability_control_summary.csv")
    run_inventory = pd.read_csv("data/analysis/run_inventory.csv")
    manifest = json.loads(Path("data/analysis/reproducibility_manifest.json").read_text(encoding="utf-8"))

    require((candidate.parse_rate == 1.0).all(), "Candidate n50 parse rate is not 100%", failures)
    require((audit.parse_rate == 1.0).all(), "Audit n25 parse rate is not 100%", failures)
    require((semantic.parse_rate == 1.0).all(), "Semantic n30 parse rate is not 100%", failures)
    require((wmt_ref_free.parse_rate == 1.0).all(), "WMT ref-free parse rate is not 100%", failures)

    sampling_by_run = {row.run: row for _, row in sampling.iterrows()}
    for run, items, positives, negatives in [
        ("candidate n50", 400, 200, 200),
        ("candidate audit n25", 200, 96, 104),
        ("semantic n30", 90, 45, 45),
        ("wmt n30 shared items", 90, 45, 45),
        ("wmt ref-free audit zh-en", 30, 15, 15),
        ("wmt ref-free audit en-de", 30, 15, 15),
    ]:
        row = sampling_by_run.get(run)
        require(row is not None, f"Sampling audit missing run: {run}", failures)
        if row is not None:
            require(int(row["items"]) == items, f"Sampling audit item count drifted for {run}", failures)
            require(
                int(row["human_positive"]) == positives,
                f"Sampling audit positive count drifted for {run}",
                failures,
            )
            require(
                int(row["human_negative"]) == negatives,
                f"Sampling audit negative count drifted for {run}",
                failures,
            )
    require(
        approx(sampling_by_run["semantic n30"].source_available_rate, 1.0, 1e-12),
        "Semantic sampling source availability drifted",
        failures,
    )

    prompt_counts = dict(zip(prompt_inventory.run, prompt_inventory.prompts, strict=True))
    require(int(prompt_counts.get("candidate n50", -1)) == 1600, "Prompt inventory candidate count drifted", failures)
    require(
        int(prompt_counts.get("candidate audit n25", -1)) == 800,
        "Prompt inventory audit count drifted",
        failures,
    )
    require(int(prompt_counts.get("semantic n30", -1)) == 360, "Prompt inventory semantic count drifted", failures)
    require(
        int(prompt_counts.get("wmt reference n30", -1)) == 300,
        "Prompt inventory WMT reference count drifted",
        failures,
    )
    require(
        int(prompt_counts.get("wmt ref-free n30", -1)) == 300,
        "Prompt inventory WMT ref-free count drifted",
        failures,
    )
    prompt_md = Path("data/analysis/prompt_inventory.md").read_text(encoding="utf-8")
    for leaked in ["Miles de personas", "La Casa Rosada", "Assam Anti-CAA", "Open a wall"]:
        require(leaked not in prompt_md, f"Prompt inventory leaked item text: {leaked}", failures)
    require("<item text redacted>" in prompt_md, "Prompt inventory does not contain redaction markers", failures)

    expected_claims = [
        "Same-item scores change materially across judge protocols.",
        "English pivot is not a safe default for candidate-quality judging.",
        "The main pivot failure survives a stronger OpenAI judge audit.",
        "Source-grounded semantic judging is also protocol-sensitive and language-dependent.",
        "WMT is contrast evidence, not a stable global protocol ranking.",
        "No single protocol dominates across cells.",
        "Calibration is a diagnostic, not a universal fix.",
        "Large protocol shifts exceed ordinary exact-prompt repeat variation.",
        "The run package is auditable for sampling, prompts, parse rate, usage, and cost.",
    ]
    require(len(claim_matrix) == len(expected_claims), "Claim evidence matrix row count drifted", failures)
    claim_by_name = {row.claim: row for _, row in claim_matrix.iterrows()}
    for claim in expected_claims:
        require(claim in claim_by_name, f"Claim evidence matrix missing claim: {claim}", failures)
    pivot_claim = claim_by_name.get("English pivot is not a safe default for candidate-quality judging.")
    if pivot_claim is not None:
        evidence = str(pivot_claim.evidence)
        require("0.836" in evidence and "0.686" in evidence, "Claim matrix pivot AUROCs drifted", failures)
        require("-0.150" in evidence, "Claim matrix pivot delta drifted", failures)
    dominance_claim = claim_by_name.get("No single protocol dominates across cells.")
    if dominance_claim is not None:
        evidence = str(dominance_claim.evidence)
        for phrase in [
            "17 non-audit cells",
            "best protocol not direct in 11",
            "pivot worst in 10",
            "significant AUROC pair in 6",
        ]:
            require(phrase in evidence, f"Claim matrix dominance evidence drifted: {phrase}", failures)

    expected_plan_items = [
        "RQ1: judge reliability changes by language",
        "RQ2: evaluation protocol changes the result",
        "RQ3: protocol effects differ by quality dimension/task",
        "RQ4: small human calibration set",
        "Contribution 1: GlobalJudge-ProtocolBench scaffold",
        "Contribution 2: protocol-sensitivity metrics",
        "Contribution 3: calibration recipe",
        "Contribution 4: Global Judge Reporting Card",
        "Stability and rerun control",
        "Cost, parsing, and release auditability",
    ]
    require(len(rq_matrix) == len(expected_plan_items), "RQ/contribution matrix row count drifted", failures)
    rq_by_item = {row.plan_item: row for _, row in rq_matrix.iterrows()}
    for item in expected_plan_items:
        require(item in rq_by_item, f"RQ/contribution matrix missing item: {item}", failures)
    rq2 = rq_by_item.get("RQ2: evaluation protocol changes the result")
    if rq2 is not None:
        evidence = str(rq2.evidence)
        for phrase in ["17 non-audit cells", "best protocol is not direct in 11", "max same-item shift is 1.20"]:
            require(phrase in evidence, f"RQ2 coverage evidence drifted: {phrase}", failures)
    bench = rq_by_item.get("Contribution 1: GlobalJudge-ProtocolBench scaffold")
    if bench is not None:
        evidence = str(bench.evidence)
        for phrase in ["580 main base items", "3480 prompts", "gpt-4.1-mini", "gpt-4o-mini"]:
            require(phrase in evidence, f"Benchmark coverage evidence drifted: {phrase}", failures)

    tr_direct = metric(candidate, "tr", "comprehensibility", "P0_direct_english")
    tr_pivot = metric(candidate, "tr", "comprehensibility", "P2_explicit_pivot")
    tr_delta = pair(candidate_pair, "tr", "comprehensibility", "P0_direct_english", "P2_explicit_pivot")
    require(approx(tr_direct.spearman, 0.602976, 1e-3), "tr comprehensibility direct Spearman drifted", failures)
    require(approx(tr_direct.auroc, 0.836, 1e-3), "tr comprehensibility direct AUROC drifted", failures)
    require(approx(tr_pivot.spearman, 0.331080, 1e-3), "tr comprehensibility pivot Spearman drifted", failures)
    require(approx(tr_pivot.auroc, 0.6864, 1e-3), "tr comprehensibility pivot AUROC drifted", failures)
    require(
        approx(tr_delta.auroc_delta_b_minus_a, -0.1496, 1e-3),
        "tr comprehensibility pivot-direct AUROC delta drifted",
        failures,
    )

    vi_grammar_shift = pair(candidate_pair, "vi", "grammar", "P1_target_rubric", "P2_explicit_pivot")
    require(approx(vi_grammar_shift.mean_abs_score_shift, 1.2, 1e-6), "vi grammar shift drifted", failures)
    require(
        approx(vi_grammar_shift.large_shift_rate_abs_ge_2, 0.34, 1e-6),
        "vi grammar large-shift rate drifted",
        failures,
    )

    audit_tr = pair(audit_pair, "tr", "comprehensibility", "P2_explicit_pivot", "P3_bilingual")
    require(
        approx(audit_tr.auroc_delta_b_minus_a, 0.352564, 1e-3),
        "Stronger audit tr bilingual-pivot AUROC delta drifted",
        failures,
    )

    semantic_tr = pair(semantic_pair, "tr", "main_ideas", "P2_explicit_pivot", "P3_bilingual")
    require(approx(semantic_tr.auroc_delta_b_minus_a, 0.124444, 1e-3), "Semantic tr delta drifted", failures)

    wmt_zh = pair(wmt_ref_free_pair, "zh-en", "translation_quality_ref_free", "P0_direct_english", "P2_explicit_pivot")
    require(approx(wmt_zh.auroc_delta_b_minus_a, -0.22, 1e-3), "WMT ref-free zh-en delta drifted", failures)

    main_instability = instability[~instability.run.str.contains("audit")]
    require(int(main_instability.n_cells.sum()) == 17, "Non-audit instability cell count is not 17", failures)
    require(
        int(main_instability.cells_best_not_direct.sum()) == 11,
        "Non-audit best-not-direct count is not 11",
        failures,
    )
    require(
        int(main_instability.cells_pivot_worst.sum()) == 10,
        "Non-audit pivot-worst count is not 10",
        failures,
    )
    require(
        int(main_instability.cells_with_significant_auroc_pair.sum()) == 6,
        "Non-audit significant-cell count is not 6",
        failures,
    )

    exact_repeat = repeatability[repeatability.control == "exact original-text prompt repeat"].iloc[0]
    pivot_repeat = repeatability[repeatability.control == "explicit-pivot pipeline repeat"].iloc[0]
    require(int(exact_repeat.n_scored_pairs) == 42, "Exact repeatability pair count drifted", failures)
    require(
        approx(exact_repeat.exact_score_agreement, 0.928571, 1e-6),
        "Exact repeatability agreement drifted",
        failures,
    )
    require(
        approx(exact_repeat.mean_abs_score_delta, 0.071429, 1e-6),
        "Exact repeatability mean delta drifted",
        failures,
    )
    require(int(pivot_repeat.n_scored_pairs) == 14, "Pivot repeatability pair count drifted", failures)
    require(
        approx(pivot_repeat.mean_abs_score_delta, 0.642857, 1e-6),
        "Pivot repeatability mean delta drifted",
        failures,
    )

    semantic_curve = calibration_curve[
        (calibration_curve.run == "semantic n30") & (calibration_curve.n_calibration == 24)
    ].iloc[0]
    candidate_curve = calibration_curve[
        (calibration_curve.run == "candidate n50") & (calibration_curve.n_calibration == 24)
    ].iloc[0]
    require(
        approx(semantic_curve.mean_delta_balanced_accuracy, 0.135833, 1e-3),
        "Semantic calibration curve largest-budget delta drifted",
        failures,
    )
    require(
        approx(candidate_curve.mean_delta_balanced_accuracy, -0.009183, 1e-3),
        "Candidate calibration curve largest-budget delta drifted",
        failures,
    )

    semantic_threshold = score_threshold[score_threshold.run == "semantic n30"].iloc[0]
    wmt_ref_free_threshold = score_threshold[score_threshold.run == "wmt ref-free n30"].iloc[0]
    require(
        approx(semantic_threshold.predicted_good_rate_threshold_4, 0.083333, 1e-6),
        "Semantic score-threshold predicted-good rate drifted",
        failures,
    )
    require(
        int(semantic_threshold.mode_best_in_group_threshold) == 2,
        "Semantic score-threshold mode drifted",
        failures,
    )
    require(
        approx(wmt_ref_free_threshold.predicted_good_rate_threshold_4, 0.9, 1e-6),
        "WMT ref-free score-threshold predicted-good rate drifted",
        failures,
    )
    require(
        int(wmt_ref_free_threshold.mode_best_in_group_threshold) == 5,
        "WMT ref-free score-threshold mode drifted",
        failures,
    )

    qualitative = pd.read_csv("data/analysis/qualitative_protocol_examples.csv")
    vi_example = qualitative[qualitative.item_id == "seahorse_test_vi_comprehensibility_008948_reference"]
    require(not vi_example.empty, "Missing Vietnamese qualitative inflation example", failures)
    if not vi_example.empty:
        row = vi_example.iloc[0]
        require(
            int(row.P1_target_rubric) == 2 and int(row.P2_explicit_pivot) == 5,
            "Vietnamese qualitative example scores drifted",
            failures,
        )

    selected_cost = sum_cost(
        [
            "data/responses/candidate_n50_base_responses.jsonl",
            "data/processed/candidate_n50_english_translations.jsonl",
            "data/responses/candidate_n50_explicit_pivot_responses.jsonl",
            "data/responses/audit_gpt41mini_n25_base_responses.jsonl",
            "data/processed/audit_gpt41mini_n25_english_translations.jsonl",
            "data/responses/audit_gpt41mini_n25_explicit_pivot_responses.jsonl",
            "data/processed/semantic_xlsum_n30_english_translations.jsonl",
            "data/responses/semantic_xlsum_n30_responses.jsonl",
            "data/processed/wmt_mqm_n30_english_translations.jsonl",
            "data/responses/wmt_mqm_n30_responses.jsonl",
            "data/responses/wmt_mqm_ref_free_n30_responses.jsonl",
            "data/responses/wmt_mqm_ref_free_audit_zh_en_gpt41mini_responses.jsonl",
            "data/responses/wmt_mqm_ref_free_audit_en_de_gpt41mini_responses.jsonl",
        ]
    )
    require(approx(selected_cost, 0.392677, 1e-6), "Selected paper-facing cost drifted", failures)

    require((run_inventory.parse_rate == 1.0).all(), "Run inventory contains a parse rate below 100%", failures)
    candidate_inventory = run_inventory[run_inventory.run == "candidate n50"].iloc[0]
    semantic_inventory = run_inventory[run_inventory.run == "semantic n30"].iloc[0]
    require(int(candidate_inventory.base_items) == 400, "Run inventory candidate base count drifted", failures)
    require(int(candidate_inventory.judge_calls) == 1600, "Run inventory candidate call count drifted", failures)
    require(
        approx(candidate_inventory.cost_per_1000_judge_calls, 0.069596, 1e-6),
        "Run inventory candidate cost per 1k drifted",
        failures,
    )
    require(
        int(candidate_inventory.api_calls_including_translations) == 2000,
        "Run inventory candidate API call count drifted",
        failures,
    )
    require(int(candidate_inventory.total_tokens) == 472666, "Run inventory candidate token count drifted", failures)
    require(int(semantic_inventory.base_items) == 90, "Run inventory semantic base count drifted", failures)
    require(int(semantic_inventory.judge_calls) == 360, "Run inventory semantic call count drifted", failures)
    require(
        int(semantic_inventory.total_tokens) == 299183,
        "Run inventory semantic token count drifted",
        failures,
    )

    manifest_files = manifest.get("files", [])
    require(len(manifest_files) >= 160, "Reproducibility manifest records too few files", failures)
    manifest_by_path = {record["path"]: record for record in manifest_files}
    for path, expected_records in [
        ("data/processed/candidate_n50_items.jsonl", 400),
        ("data/processed/audit_gpt41mini_n25_items.jsonl", 200),
        ("data/processed/semantic_xlsum_n30_items.jsonl", 90),
        ("data/processed/wmt_mqm_n30_items.jsonl", 90),
        ("data/prompts/candidate_n50_combined_explicit_prompts.jsonl", 1600),
        ("data/prompts/audit_gpt41mini_n25_combined_explicit_prompts.jsonl", 800),
        ("data/prompts/semantic_xlsum_n30_prompts.jsonl", 360),
        ("data/prompts/wmt_mqm_n30_prompts.jsonl", 300),
        ("data/prompts/wmt_mqm_ref_free_n30_prompts.jsonl", 300),
        ("data/responses/candidate_n50_combined_explicit_responses.jsonl", 1600),
        ("data/responses/audit_gpt41mini_n25_combined_explicit_responses.jsonl", 800),
        ("data/responses/semantic_xlsum_n30_responses.jsonl", 360),
        ("data/responses/wmt_mqm_n30_responses.jsonl", 300),
        ("data/responses/wmt_mqm_ref_free_n30_responses.jsonl", 300),
        ("data/analysis/claim_evidence_matrix.csv", 9),
        ("data/analysis/rq_contribution_matrix.csv", 10),
    ]:
        record = manifest_by_path.get(path)
        require(record is not None, f"Manifest missing required file: {path}", failures)
        if record is not None:
            require(
                int(record.get("records", -1)) == expected_records,
                f"Manifest record count drifted for {path}",
                failures,
            )
            require(len(record.get("sha256", "")) == 64, f"Manifest SHA256 missing for {path}", failures)
    for path in [
        "data/analysis/claim_evidence_matrix.md",
        "paper/tables/claim_evidence_matrix.tex",
        "data/analysis/rq_contribution_matrix.md",
        "paper/tables/rq_contribution_matrix.tex",
        "paper/extended_abstract.tex",
        "paper/extended_abstract.pdf",
        "paper/submission_packet.md",
        "paper/globaljudge_protocolbench_datacard.md",
        "data/analysis/release_validation_report.json",
        "data/analysis/release_validation_report.md",
        "data/analysis/completion_audit.json",
        "data/analysis/completion_audit.md",
    ]:
        require(path in manifest_by_path, f"Manifest missing required file: {path}", failures)
    commands = set(manifest.get("validation_commands", []))
    require(
        "/home/eston/anaconda3/envs/global_judge/bin/python src/validate_paper_claims.py" in commands,
        "Manifest missing claim-validator command",
        failures,
    )
    require("make -C paper" in commands, "Manifest missing paper-build command", failures)

    return failures


def main() -> None:
    failures = validate()
    if failures:
        print("Paper claim validation failed:")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)
    print("Paper claim validation passed.")


if __name__ == "__main__":
    main()
