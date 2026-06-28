from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


OUT_DIR = Path("data/analysis")
TABLE_DIR = Path("paper/tables")


RUN_SPECS = [
    {
        "run": "candidate n50",
        "items": "data/processed/candidate_n50_items.jsonl",
        "selection_response_paths": [],
    },
    {
        "run": "candidate audit n25",
        "items": "data/processed/audit_gpt41mini_n25_items.jsonl",
        "selection_response_paths": [],
    },
    {
        "run": "semantic n30",
        "items": "data/processed/semantic_xlsum_n30_items.jsonl",
        "selection_response_paths": [],
    },
    {
        "run": "wmt n30 shared items",
        "items": "data/processed/wmt_mqm_n30_items.jsonl",
        "selection_response_paths": [],
    },
    {
        "run": "wmt ref-free audit zh-en",
        "items": "data/processed/wmt_mqm_n30_items.jsonl",
        "selection_response_paths": ["data/responses/wmt_mqm_ref_free_audit_zh_en_gpt41mini_responses.jsonl"],
    },
    {
        "run": "wmt ref-free audit en-de",
        "items": "data/processed/wmt_mqm_n30_items.jsonl",
        "selection_response_paths": ["data/responses/wmt_mqm_ref_free_audit_en_de_gpt41mini_responses.jsonl"],
    },
]


def read_jsonl(path: str | Path) -> list[dict[str, Any]]:
    with Path(path).open("r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def selected_item_ids(paths: list[str]) -> set[str] | None:
    if not paths:
        return None
    ids: set[str] = set()
    for path in paths:
        ids.update(record["item_id"] for record in read_jsonl(path))
    return ids


def text_len(value: Any) -> int:
    if value is None:
        return 0
    if pd.isna(value):
        return 0
    return len(str(value))


def item_rows() -> pd.DataFrame:
    rows = []
    for spec in RUN_SPECS:
        keep_ids = selected_item_ids(spec["selection_response_paths"])
        for item in read_jsonl(spec["items"]):
            if keep_ids is not None and item["item_id"] not in keep_ids:
                continue
            metadata = item.get("metadata") or {}
            rows.append(
                {
                    "run": spec["run"],
                    "dataset": item.get("dataset", ""),
                    "task": item.get("task", ""),
                    "split": item.get("split", ""),
                    "item_id": item["item_id"],
                    "language": item.get("language", ""),
                    "language_name": item.get("language_name", ""),
                    "dimension": item.get("dimension", ""),
                    "human_label": int(item["human_label"]),
                    "human_label_text": item.get("human_label_text", ""),
                    "candidate_chars": text_len(item.get("candidate_output")),
                    "source_chars": text_len(item.get("source_text")),
                    "reference_chars": text_len(item.get("reference")),
                    "has_source": bool(item.get("source_text")),
                    "has_reference": bool(item.get("reference")),
                    "summary_model": metadata.get("summary_model", ""),
                    "wmt_system": metadata.get("system", ""),
                    "wmt_year": metadata.get("year", ""),
                    "wmt_human_score": metadata.get("human_score"),
                }
            )
    return pd.DataFrame(rows)


def summarize_groups(items: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (run, language, dimension), group in items.groupby(["run", "language", "dimension"], sort=False):
        pos = int(group["human_label"].sum())
        n = len(group)
        rows.append(
            {
                "run": run,
                "language": language,
                "dimension": dimension,
                "n": n,
                "human_positive": pos,
                "human_negative": n - pos,
                "positive_rate": pos / n if n else 0.0,
                "mean_candidate_chars": group["candidate_chars"].mean(),
                "max_candidate_chars": int(group["candidate_chars"].max()),
                "source_available_rate": group["has_source"].mean(),
                "reference_available_rate": group["has_reference"].mean(),
                "mean_source_chars": group["source_chars"].mean(),
                "mean_reference_chars": group["reference_chars"].mean(),
                "mean_wmt_human_score": pd.to_numeric(group["wmt_human_score"], errors="coerce").mean(),
                "min_wmt_human_score": pd.to_numeric(group["wmt_human_score"], errors="coerce").min(),
                "max_wmt_human_score": pd.to_numeric(group["wmt_human_score"], errors="coerce").max(),
            }
        )
    return pd.DataFrame(rows)


def summarize_runs(items: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for run, group in items.groupby("run", sort=False):
        rows.append(
            {
                "run": run,
                "items": len(group),
                "languages": group["language"].nunique(),
                "dimensions": group["dimension"].nunique(),
                "human_positive": int(group["human_label"].sum()),
                "human_negative": int(len(group) - group["human_label"].sum()),
                "positive_rate": group["human_label"].mean(),
                "mean_candidate_chars": group["candidate_chars"].mean(),
                "max_candidate_chars": int(group["candidate_chars"].max()),
                "source_available_rate": group["has_source"].mean(),
                "reference_available_rate": group["has_reference"].mean(),
            }
        )
    return pd.DataFrame(rows)


def write_markdown(run_summary: pd.DataFrame, group_summary: pd.DataFrame) -> None:
    lines = [
        "# Dataset Sampling Audit",
        "",
        "Generated from processed item JSONL files. WMT audit rows are selected by the item IDs that appear in the targeted audit response caches.",
        "",
        "## Run Summary",
        "",
        "| Run | Items | Langs | Dims | Pos | Neg | Source Rate | Reference Rate | Mean Candidate Chars |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for _, row in run_summary.iterrows():
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["run"]),
                    str(int(row["items"])),
                    str(int(row["languages"])),
                    str(int(row["dimensions"])),
                    str(int(row["human_positive"])),
                    str(int(row["human_negative"])),
                    f"{100.0 * row['source_available_rate']:.1f}%",
                    f"{100.0 * row['reference_available_rate']:.1f}%",
                    f"{row['mean_candidate_chars']:.1f}",
                ]
            )
            + " |"
        )
    lines.extend(["", "## Group Summary", ""])
    lines.append(
        "| Run | Language | Dimension | N | Pos | Neg | Pos Rate | Mean Candidate Chars | Source Rate | Reference Rate |"
    )
    lines.append("| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for _, row in group_summary.iterrows():
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["run"]),
                    str(row["language"]),
                    str(row["dimension"]),
                    str(int(row["n"])),
                    str(int(row["human_positive"])),
                    str(int(row["human_negative"])),
                    f"{100.0 * row['positive_rate']:.1f}%",
                    f"{row['mean_candidate_chars']:.1f}",
                    f"{100.0 * row['source_available_rate']:.1f}%",
                    f"{100.0 * row['reference_available_rate']:.1f}%",
                ]
            )
            + " |"
        )
    lines.append("")
    (OUT_DIR / "dataset_sampling_audit.md").write_text("\n".join(lines), encoding="utf-8")


def write_latex(run_summary: pd.DataFrame) -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    lines = [
        "\\begin{table}[t]",
        "\\centering",
        "\\caption{Dataset sampling audit for paper-facing item sets.}",
        "\\label{tab:dataset_sampling_audit}",
        "\\resizebox{\\linewidth}{!}{%",
        "\\begin{tabular}{lrrrrrr}",
        "\\toprule",
        "Run & Items & Langs & Dims & Pos & Neg & Source \\\\",
        "\\midrule",
    ]
    for _, row in run_summary.iterrows():
        lines.append(
            " & ".join(
                [
                    str(row["run"]).replace("_", "\\_"),
                    str(int(row["items"])),
                    str(int(row["languages"])),
                    str(int(row["dimensions"])),
                    str(int(row["human_positive"])),
                    str(int(row["human_negative"])),
                    f"{100.0 * row['source_available_rate']:.0f}\\%",
                ]
            )
            + " \\\\"
        )
    lines.extend(["\\bottomrule", "\\end{tabular}%", "}", "\\end{table}", ""])
    (TABLE_DIR / "dataset_sampling_audit.tex").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    items = item_rows()
    group_summary = summarize_groups(items)
    run_summary = summarize_runs(items)
    items.to_csv(OUT_DIR / "dataset_sampling_items.csv", index=False)
    group_summary.to_csv(OUT_DIR / "dataset_sampling_groups.csv", index=False)
    run_summary.to_csv(OUT_DIR / "dataset_sampling_summary.csv", index=False)
    write_markdown(run_summary, group_summary)
    write_latex(run_summary)
    print(f"Wrote {OUT_DIR / 'dataset_sampling_items.csv'}")
    print(f"Wrote {OUT_DIR / 'dataset_sampling_groups.csv'}")
    print(f"Wrote {OUT_DIR / 'dataset_sampling_summary.csv'}")
    print(f"Wrote {OUT_DIR / 'dataset_sampling_audit.md'}")
    print(f"Wrote {TABLE_DIR / 'dataset_sampling_audit.tex'}")


if __name__ == "__main__":
    main()
