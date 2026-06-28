from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pandas as pd


OUT_PATH = Path("paper/submission_packet.md")


def fmt(value: float | int, digits: int = 3) -> str:
    return f"{float(value):.{digits}f}"


def pdf_pages(path: str) -> int:
    result = subprocess.run(["pdfinfo", path], check=True, capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if line.startswith("Pages:"):
            return int(line.split(":", 1)[1].strip())
    raise RuntimeError(f"Could not read page count from {path}")


def load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> None:
    claim_matrix = pd.read_csv("data/analysis/claim_evidence_matrix.csv")
    rq_matrix = pd.read_csv("data/analysis/rq_contribution_matrix.csv")
    run_inventory = pd.read_csv("data/analysis/run_inventory.csv")
    manifest = load_json("data/analysis/reproducibility_manifest.json")

    main_pdf_pages = pdf_pages("paper/main.pdf")
    extended_pdf_pages = pdf_pages("paper/extended_abstract.pdf")
    total_calls = int(run_inventory["judge_calls"].sum())
    total_tokens = int(run_inventory["total_tokens"].sum())
    min_parse_rate = float(run_inventory["parse_rate"].min())
    total_cost = float(run_inventory["observed_cost_usd"].sum())

    claim_rows = [
        {
            "claim": row["claim"],
            "evidence": row["evidence"],
            "coverage": row["validator_coverage"],
        }
        for _, row in claim_matrix.iterrows()
    ]
    rq_rows = [
        {
            "item": row["plan_item"],
            "coverage": row["coverage"],
            "boundary": row["claim_boundary"],
        }
        for _, row in rq_matrix.iterrows()
    ]

    risk_rows = [
        {
            "risk": "Only OpenAI judges are tested.",
            "answer": "State this directly. The main claim is protocol sensitivity within realistic API judge workflows, not model-family universality. The gpt-4.1-mini audits show the failure mode survives a stronger OpenAI judge.",
            "artifact": "paper/main.tex limitations; data/analysis/rq_contribution_matrix.md",
        },
        {
            "risk": "Target-language rubrics are not native-speaker validated.",
            "answer": "Frame target-rubric results as pilot protocol evidence. The strongest pivot-failure claim does not depend on target-language rubric superiority because direct-vs-pivot and bilingual-vs-pivot comparisons carry the key signal.",
            "artifact": "paper/main.tex limitations; data/analysis/claim_evidence_matrix.md",
        },
        {
            "risk": "WMT results look mixed.",
            "answer": "Use WMT as a boundary condition. Reference-based MT has smaller shifts; reference-free MT exposes larger gpt-4o-mini effects; the stronger audit narrows the claim to protocol/model sensitivity rather than a global ranking.",
            "artifact": "paper/tables/wmt_translation_quality.tex; paper/tables/wmt_ref_free_stronger_audit.tex",
        },
        {
            "risk": "Calibration is not a positive universal contribution.",
            "answer": "Do not sell calibration as a repair. Present it as a score-threshold diagnostic that helps semantic main-ideas but remains mixed or negative in other settings.",
            "artifact": "data/analysis/calibration_learning_curve_summary.csv; paper/tables/score_threshold_diagnostic.tex",
        },
        {
            "risk": "A single aggregate score may hide small cells.",
            "answer": "Lean on per-language tables, paired bootstrap intervals, same-item shifts, language gaps, sampling audit, and the claim-evidence matrix instead of aggregate-only claims.",
            "artifact": "paper/tables/language_gaps.tex; data/analysis/dataset_sampling_audit.md",
        },
        {
            "risk": "Cost estimates may change before submission.",
            "answer": "Report returned token usage as stable accounting. Treat dollar amounts as local run-time estimates and refresh provider pricing before camera-ready release.",
            "artifact": "data/analysis/run_inventory.csv; paper/tables/api_usage_inventory.tex",
        },
        {
            "risk": "Prompt examples might leak copyrighted or benchmark item text.",
            "answer": "Use the redacted prompt inventory for public appendix text. The validator checks representative prompt redaction markers and known leaked strings.",
            "artifact": "data/analysis/prompt_inventory.md; src/validate_paper_claims.py",
        },
    ]

    def md_table(rows: list[dict[str, str]], columns: list[tuple[str, str]]) -> list[str]:
        lines = [
            "| " + " | ".join(header for _, header in columns) + " |",
            "| " + " | ".join(["---"] * len(columns)) + " |",
        ]
        for row in rows:
            lines.append("| " + " | ".join(str(row.get(key, "")) for key, _ in columns) + " |")
        return lines

    lines = [
        "# Submission Packet",
        "",
        "This packet turns the current evidence package into submission-facing claims, claim boundaries, reviewer-risk responses, and final pre-submission checks.",
        "",
        "## Writing Surfaces",
        "",
        f"- Immediate extended abstract: `paper/extended_abstract.pdf` ({extended_pdf_pages} pages).",
        f"- Full supporting manuscript: `paper/main.pdf` ({main_pdf_pages} pages).",
        "- Results and response source of truth: `paper/results_brief.md`, `data/analysis/claim_evidence_matrix.md`, and `data/analysis/rq_contribution_matrix.md`.",
        "- Benchmark/data-card source of truth: `paper/globaljudge_protocolbench_datacard.md`.",
        "- Completion audit: `data/analysis/completion_audit.md`.",
        "",
        "## One-Sentence Pitch",
        "",
        "Multilingual LLM-as-a-judge scores are under-specified unless the paper reports which language the judge saw, which language the rubric used, whether examples were translated, and how sensitive conclusions are to those protocol choices.",
        "",
        "## Submission-Ready Claim Boundary",
        "",
        "- Claim: multilingual judge conclusions are protocol-sensitive across the current SEAHORSE, source-grounded XLSum, and WMT MQM stress tests.",
        "- Claim: English pivoting is not a safe default; it can hurt human alignment and hide target-language form evidence.",
        "- Claim: reporting should include protocol shifts, language gaps, calibration behavior, parse rate, returned token usage, and cost.",
        "- Do not claim: a universal best protocol, model-family generality beyond current OpenAI judges, native-validated target-language rubrics, or a definitive WMT protocol ranking.",
        "",
        "## Key Claim Evidence",
        "",
    ]
    lines.extend(md_table(claim_rows, [("claim", "Claim"), ("evidence", "Evidence"), ("coverage", "Validator Coverage")]))
    lines.extend(
        [
            "",
            "## RQ and Contribution Coverage",
            "",
        ]
    )
    lines.extend(md_table(rq_rows, [("item", "Plan Item"), ("coverage", "Coverage"), ("boundary", "Claim Boundary")]))
    lines.extend(
        [
            "",
            "## Reviewer Risk Responses",
            "",
        ]
    )
    lines.extend(md_table(risk_rows, [("risk", "Reviewer Risk"), ("answer", "Response Strategy"), ("artifact", "Evidence Artifact")]))
    lines.extend(
        [
            "",
            "## Audit Snapshot",
            "",
            f"- Manifest files recorded: {len(manifest['files'])}.",
            f"- Paper-facing judge calls: {total_calls}.",
            f"- Minimum parse rate across paper-facing runs: {100 * min_parse_rate:.1f}%.",
            f"- Returned total tokens across paper-facing runs: {total_tokens}.",
            f"- Observed local cost estimate across paper-facing runs: ${total_cost:.4f}.",
            "",
            "## Final Pre-Submission Checks",
            "",
            "- Apply the target venue template if required; the current extended abstract is template-neutral.",
            "- Refresh dollar-cost estimates against current provider pricing; keep token counts unchanged unless rerunning calls.",
            "- Native-check target-language rubric translations before making strong claims about target-language prompting.",
            "- Include or link the benchmark data card when sharing the artifact package.",
            "- If time and budget allow, add a non-OpenAI judge-family audit; otherwise keep the current model-family limitation prominent.",
            "- Run `make -C paper`, `/home/eston/anaconda3/envs/global_judge/bin/python src/validate_paper_claims.py`, and `/home/eston/anaconda3/envs/global_judge/bin/python src/run_release_checks.py` immediately before submission.",
            "",
        ]
    )
    OUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
