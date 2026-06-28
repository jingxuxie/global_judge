from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


OUT_SUMMARY_CSV = Path("data/analysis/repeatability_control_summary.csv")
OUT_DETAILS_CSV = Path("data/analysis/repeatability_control_details.csv")
OUT_MD = Path("data/analysis/repeatability_control.md")
OUT_TEX = Path("paper/tables/repeatability_control.tex")


def read_jsonl(path: str | Path) -> list[dict[str, Any]]:
    with Path(path).open("r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def load_by_prompt_id(path: str | Path) -> dict[str, dict[str, Any]]:
    return {row["prompt_id"]: row for row in read_jsonl(path)}


def prompt_text(row: dict[str, Any]) -> str:
    return "\n\n".join(f"{message['role']}:{message['content']}" for message in row["messages"])


def score_delta(left: dict[str, Any], right: dict[str, Any]) -> float | None:
    if not left.get("parse_success") or not right.get("parse_success"):
        return None
    if left.get("score") is None or right.get("score") is None:
        return None
    return abs(float(left["score"]) - float(right["score"]))


def summarize_pair(
    *,
    control_name: str,
    prompt_a: str,
    response_a: str,
    prompt_b: str,
    response_b: str,
    interpretation: str,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    prompts_a = load_by_prompt_id(prompt_a)
    prompts_b = load_by_prompt_id(prompt_b)
    responses_a = load_by_prompt_id(response_a)
    responses_b = load_by_prompt_id(response_b)

    common_ids = sorted(set(prompts_a) & set(prompts_b) & set(responses_a) & set(responses_b))
    details = []
    for prompt_id in common_ids:
        left = responses_a[prompt_id]
        right = responses_b[prompt_id]
        delta = score_delta(left, right)
        same_prompt_text = prompt_text(prompts_a[prompt_id]) == prompt_text(prompts_b[prompt_id])
        details.append(
            {
                "control": control_name,
                "prompt_id": prompt_id,
                "item_id": left["item_id"],
                "language": left["language"],
                "dimension": left["dimension"],
                "protocol": left["protocol"],
                "same_prompt_text": same_prompt_text,
                "score_a": left.get("score"),
                "score_b": right.get("score"),
                "abs_score_delta": delta,
                "same_raw_response": left.get("raw_response") == right.get("raw_response"),
                "timestamp_a": left.get("timestamp_utc"),
                "timestamp_b": right.get("timestamp_utc"),
                "response_file_a": response_a,
                "response_file_b": response_b,
            }
        )

    scored = [row for row in details if row["abs_score_delta"] is not None]
    deltas = pd.Series([row["abs_score_delta"] for row in scored], dtype=float)
    summary = {
        "control": control_name,
        "n_common_prompts": len(details),
        "n_scored_pairs": len(scored),
        "identical_prompt_rate": sum(row["same_prompt_text"] for row in details) / len(details) if details else 0.0,
        "exact_score_agreement": float((deltas == 0).mean()) if len(deltas) else 0.0,
        "changed_score_pairs": int((deltas != 0).sum()) if len(deltas) else 0,
        "mean_abs_score_delta": float(deltas.mean()) if len(deltas) else 0.0,
        "median_abs_score_delta": float(deltas.median()) if len(deltas) else 0.0,
        "max_abs_score_delta": float(deltas.max()) if len(deltas) else 0.0,
        "same_raw_response_rate": sum(row["same_raw_response"] for row in details) / len(details) if details else 0.0,
        "interpretation": interpretation,
    }
    return summary, details


def write_latex(summary: pd.DataFrame) -> None:
    OUT_TEX.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "\\begin{table}[t]",
        "\\centering",
        "\\caption{Repeatability control from overlapping pilot and main-run caches.}",
        "\\label{tab:repeatability_control}",
        "\\resizebox{\\linewidth}{!}{%",
        "\\begin{tabular}{lrrrrr}",
        "\\toprule",
        "Control & Pairs & Identical prompts & Exact agree & Mean $|\\Delta|$ & Max $|\\Delta|$ \\\\",
        "\\midrule",
    ]
    for _, row in summary.iterrows():
        lines.append(
            " & ".join(
                [
                    str(row["control"]).replace("_", "\\_"),
                    str(int(row["n_scored_pairs"])),
                    f"{100.0 * row['identical_prompt_rate']:.1f}\\%",
                    f"{100.0 * row['exact_score_agreement']:.1f}\\%",
                    f"{row['mean_abs_score_delta']:.3f}",
                    f"{row['max_abs_score_delta']:.0f}",
                ]
            )
            + " \\\\"
        )
    lines.extend(["\\bottomrule", "\\end{tabular}%", "}", "\\end{table}", ""])
    OUT_TEX.write_text("\n".join(lines), encoding="utf-8")


def write_markdown(summary: pd.DataFrame) -> None:
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Repeatability Control",
        "",
        "This no-new-API control uses overlapping pilot and main-run response caches.",
        "",
        "| Control | Scored Pairs | Identical Prompts | Exact Agreement | Mean Abs Delta | Max Abs Delta | Interpretation |",
        "| --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for _, row in summary.iterrows():
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["control"]),
                    str(int(row["n_scored_pairs"])),
                    f"{100.0 * row['identical_prompt_rate']:.1f}%",
                    f"{100.0 * row['exact_score_agreement']:.1f}%",
                    f"{row['mean_abs_score_delta']:.3f}",
                    f"{row['max_abs_score_delta']:.0f}",
                    str(row["interpretation"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "The exact original-text prompt repeats are the clean judge repeatability control.",
            "The explicit-pivot repeat is a pipeline-repeat control because the prompt text changed between the historical pilot and main run.",
            "",
        ]
    )
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    specs = [
        {
            "control_name": "exact original-text prompt repeat",
            "prompt_a": "data/prompts/pilot_n20_prompts.jsonl",
            "response_a": "data/responses/pilot_n20_openai_responses.jsonl",
            "prompt_b": "data/prompts/candidate_n50_base_prompts.jsonl",
            "response_b": "data/responses/candidate_n50_base_responses.jsonl",
            "interpretation": "Same prompt text repeated across independent pilot/main caches; measures ordinary judge run-to-run noise.",
        },
        {
            "control_name": "explicit-pivot pipeline repeat",
            "prompt_a": "data/prompts/pilot_n20_explicit_pivot_prompts.jsonl",
            "response_a": "data/responses/pilot_n20_explicit_pivot_responses.jsonl",
            "prompt_b": "data/prompts/candidate_n50_explicit_pivot_prompts.jsonl",
            "response_b": "data/responses/candidate_n50_explicit_pivot_responses.jsonl",
            "interpretation": "Prompt text changed because the English-pivot pipeline was regenerated; measures pivot-pipeline volatility.",
        },
    ]

    summary_rows: list[dict[str, Any]] = []
    detail_rows: list[dict[str, Any]] = []
    for spec in specs:
        summary, details = summarize_pair(**spec)
        summary_rows.append(summary)
        detail_rows.extend(details)

    summary_df = pd.DataFrame(summary_rows)
    details_df = pd.DataFrame(detail_rows)
    OUT_SUMMARY_CSV.parent.mkdir(parents=True, exist_ok=True)
    summary_df.to_csv(OUT_SUMMARY_CSV, index=False)
    details_df.to_csv(OUT_DETAILS_CSV, index=False)
    write_markdown(summary_df)
    write_latex(summary_df)
    print(f"Wrote {OUT_SUMMARY_CSV}")
    print(f"Wrote {OUT_DETAILS_CSV}")
    print(f"Wrote {OUT_MD}")
    print(f"Wrote {OUT_TEX}")


if __name__ == "__main__":
    main()
