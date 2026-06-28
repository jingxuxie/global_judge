from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any


OUT_JSON = Path("data/analysis/reproducibility_manifest.json")
OUT_MD = Path("data/analysis/reproducibility_manifest.md")

SECTIONS = [
    (
        "plan_and_docs",
        [
            "globaljudge_protocol_paper_plan.md",
            "README.md",
            "paper/reporting_card.md",
            "paper/globaljudge_short_paper_draft.md",
            "paper/results_brief.md",
            "paper/globaljudge_protocolbench_datacard.md",
            "data/analysis/current_research_status.md",
        ],
    ),
    ("configs", ["configs/*.yaml"]),
    ("source_code", ["src/*.py"]),
    (
        "raw_data_archives",
        [
            "data/raw/seahorse_data.zip",
            "data/raw/xlsum/*.tar.bz2",
            "data/raw/hf_datasets/RicardoRei___wmt-mqm-human-evaluation/**/dataset_info.json",
        ],
    ),
    (
        "processed_items",
        [
            "data/processed/candidate_n50_items.jsonl",
            "data/processed/audit_gpt41mini_n25_items.jsonl",
            "data/processed/semantic_xlsum_n30_items.jsonl",
            "data/processed/wmt_mqm_n30_items.jsonl",
        ],
    ),
    (
        "prompts",
        [
            "data/prompts/candidate_n50_combined_explicit_prompts.jsonl",
            "data/prompts/audit_gpt41mini_n25_combined_explicit_prompts.jsonl",
            "data/prompts/semantic_xlsum_n30_prompts.jsonl",
            "data/prompts/wmt_mqm_n30_prompts.jsonl",
            "data/prompts/wmt_mqm_ref_free_n30_prompts.jsonl",
            "data/prompts/wmt_mqm_ref_free_audit_zh_en_gpt41mini_prompts.jsonl",
            "data/prompts/wmt_mqm_ref_free_audit_en_de_gpt41mini_prompts.jsonl",
        ],
    ),
    (
        "translations",
        [
            "data/processed/candidate_n50_english_translations.jsonl",
            "data/processed/audit_gpt41mini_n25_english_translations.jsonl",
            "data/processed/semantic_xlsum_n30_english_translations.jsonl",
            "data/processed/wmt_mqm_n30_english_translations.jsonl",
        ],
    ),
    (
        "responses",
        [
            "data/responses/candidate_n50_combined_explicit_responses.jsonl",
            "data/responses/audit_gpt41mini_n25_combined_explicit_responses.jsonl",
            "data/responses/semantic_xlsum_n30_responses.jsonl",
            "data/responses/wmt_mqm_n30_responses.jsonl",
            "data/responses/wmt_mqm_ref_free_n30_responses.jsonl",
            "data/responses/wmt_mqm_ref_free_audit_zh_en_gpt41mini_responses.jsonl",
            "data/responses/wmt_mqm_ref_free_audit_en_de_gpt41mini_responses.jsonl",
        ],
    ),
    (
        "analysis",
        [
            "data/analysis/*_metrics.csv",
            "data/analysis/*_metrics_pairwise_bootstrap.csv",
            "data/analysis/*_metrics_language_gaps.csv",
            "data/analysis/*_protocol_shifts.csv",
            "data/analysis/*_calibration.csv",
            "data/analysis/*_summary.csv",
            "data/analysis/dataset_sampling_items.csv",
            "data/analysis/dataset_sampling_groups.csv",
            "data/analysis/dataset_sampling_summary.csv",
            "data/analysis/dataset_sampling_audit.md",
            "data/analysis/protocol_instability_cells.csv",
            "data/analysis/qualitative_protocol_examples.csv",
            "data/analysis/prompt_inventory.csv",
            "data/analysis/prompt_inventory_summary.csv",
            "data/analysis/prompt_inventory.md",
            "data/analysis/prompt_representatives.csv",
            "data/analysis/claim_evidence_matrix.csv",
            "data/analysis/claim_evidence_matrix.md",
            "data/analysis/rq_contribution_matrix.csv",
            "data/analysis/rq_contribution_matrix.md",
            "data/analysis/calibration_learning_curve_raw.csv",
            "data/analysis/score_threshold_diagnostic_groups.csv",
            "data/analysis/repeatability_control_details.csv",
            "data/analysis/run_inventory.csv",
            "data/analysis/release_validation_report.json",
            "data/analysis/release_validation_report.md",
            "data/analysis/completion_audit.json",
            "data/analysis/completion_audit.md",
        ],
    ),
    (
        "paper",
        [
            "paper/Makefile",
            "paper/colm2026_conference.sty",
            "paper/colm2026_conference.bst",
            "paper/fancyhdr.sty",
            "paper/natbib.sty",
            "paper/main.tex",
            "paper/main.pdf",
            "paper/extended_abstract.tex",
            "paper/extended_abstract.pdf",
            "paper/submission_packet.md",
            "paper/references.bib",
            "paper/tables/*.tex",
            "paper/figures/*.png",
        ],
    ),
]

VALIDATION_COMMANDS = [
    "/home/eston/anaconda3/envs/global_judge/bin/python -m compileall src",
    "/home/eston/anaconda3/envs/global_judge/bin/python src/validate_paper_claims.py",
    "/home/eston/anaconda3/envs/global_judge/bin/python src/run_release_checks.py",
    "make -C paper",
    "pdfinfo paper/extended_abstract.pdf",
    "rg -n '(T[O]DO|T[B]D|F[I]XME|p[l]aceholder|0\\\\.3706|0\\\\.3499|0\\\\.3403|significant pivot dr[o]p|including a signific[a]nt|single global w[i]nner)' README.md paper data/analysis/current_research_status.md src configs",
    "rg -n '(undefined|Undefined|Citation|Reference|Overfull|Underfull|Warning|Error|Rerun)' paper/main.log",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def count_jsonl(path: Path) -> int:
    with path.open("r", encoding="utf-8") as f:
        return sum(1 for line in f if line.strip())


def count_csv_rows(path: Path) -> int:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)
    return max(0, len(rows) - 1)


def record_for(path: Path, section: str) -> dict[str, Any]:
    record: dict[str, Any] = {
        "section": section,
        "path": path.as_posix(),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }
    if path.suffix == ".jsonl":
        record["records"] = count_jsonl(path)
    elif path.suffix == ".csv":
        record["records"] = count_csv_rows(path)
    return record


def resolve_patterns(patterns: list[str]) -> list[Path]:
    paths: set[Path] = set()
    for pattern in patterns:
        matched = sorted(Path(".").glob(pattern))
        paths.update(path for path in matched if path.is_file())
    return sorted(paths, key=lambda path: path.as_posix())


def build_manifest() -> dict[str, Any]:
    files = []
    for section, patterns in SECTIONS:
        for path in resolve_patterns(patterns):
            files.append(record_for(path, section))
    return {
        "manifest_version": 1,
        "purpose": "Paper-facing reproducibility manifest for GlobalJudge protocol-sensitivity experiments.",
        "validation_commands": VALIDATION_COMMANDS,
        "files": files,
    }


def summarize_sections(files: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    sections = sorted({record["section"] for record in files})
    for section in sections:
        subset = [record for record in files if record["section"] == section]
        rows.append(
            {
                "section": section,
                "files": len(subset),
                "bytes": sum(int(record["bytes"]) for record in subset),
                "records": sum(int(record.get("records", 0)) for record in subset),
            }
        )
    return rows


def write_markdown(manifest: dict[str, Any]) -> None:
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    section_rows = summarize_sections(manifest["files"])
    lines = [
        "# Reproducibility Manifest",
        "",
        manifest["purpose"],
        "",
        "## Section Summary",
        "",
        "| Section | Files | Bytes | Records |",
        "| --- | ---: | ---: | ---: |",
    ]
    for row in section_rows:
        lines.append(f"| {row['section']} | {row['files']} | {row['bytes']} | {row['records']} |")
    lines.extend(["", "## Validation Commands", ""])
    for command in manifest["validation_commands"]:
        lines.append(f"- `{command}`")
    lines.extend(
        [
            "",
            "## Key Paper-Facing Files",
            "",
            "| Section | Path | Records | SHA256 |",
            "| --- | --- | ---: | --- |",
        ]
    )
    key_sections = {"processed_items", "prompts", "responses", "analysis", "paper"}
    for record in manifest["files"]:
        if record["section"] not in key_sections:
            continue
        records = record.get("records", "")
        lines.append(f"| {record['section']} | `{record['path']}` | {records} | `{record['sha256']}` |")
    lines.append("")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    manifest = build_manifest()
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(manifest)
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")
    print(f"Recorded {len(manifest['files'])} files")


if __name__ == "__main__":
    main()
