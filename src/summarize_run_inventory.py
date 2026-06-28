from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


OUT_DIR = Path("data/analysis")

RUN_SPECS = [
    {
        "run": "candidate n50",
        "base_items": "data/processed/candidate_n50_items.jsonl",
        "responses": ["data/responses/candidate_n50_combined_explicit_responses.jsonl"],
        "cost_paths": [
            "data/responses/candidate_n50_base_responses.jsonl",
            "data/processed/candidate_n50_english_translations.jsonl",
            "data/responses/candidate_n50_explicit_pivot_responses.jsonl",
        ],
    },
    {
        "run": "candidate audit n25",
        "base_items": "data/processed/audit_gpt41mini_n25_items.jsonl",
        "responses": ["data/responses/audit_gpt41mini_n25_combined_explicit_responses.jsonl"],
        "cost_paths": [
            "data/responses/audit_gpt41mini_n25_base_responses.jsonl",
            "data/processed/audit_gpt41mini_n25_english_translations.jsonl",
            "data/responses/audit_gpt41mini_n25_explicit_pivot_responses.jsonl",
        ],
    },
    {
        "run": "semantic n30",
        "base_items": "data/processed/semantic_xlsum_n30_items.jsonl",
        "responses": ["data/responses/semantic_xlsum_n30_responses.jsonl"],
        "cost_paths": [
            "data/processed/semantic_xlsum_n30_english_translations.jsonl",
            "data/responses/semantic_xlsum_n30_responses.jsonl",
        ],
    },
    {
        "run": "wmt reference n30",
        "base_items": "data/processed/wmt_mqm_n30_items.jsonl",
        "responses": ["data/responses/wmt_mqm_n30_responses.jsonl"],
        "cost_paths": [
            "data/processed/wmt_mqm_n30_english_translations.jsonl",
            "data/responses/wmt_mqm_n30_responses.jsonl",
        ],
    },
    {
        "run": "wmt ref-free n30",
        "base_items": "data/processed/wmt_mqm_n30_items.jsonl",
        "responses": ["data/responses/wmt_mqm_ref_free_n30_responses.jsonl"],
        "cost_paths": ["data/responses/wmt_mqm_ref_free_n30_responses.jsonl"],
    },
    {
        "run": "wmt ref-free audit",
        "base_items": None,
        "responses": [
            "data/responses/wmt_mqm_ref_free_audit_zh_en_gpt41mini_responses.jsonl",
            "data/responses/wmt_mqm_ref_free_audit_en_de_gpt41mini_responses.jsonl",
        ],
        "cost_paths": [
            "data/responses/wmt_mqm_ref_free_audit_zh_en_gpt41mini_responses.jsonl",
            "data/responses/wmt_mqm_ref_free_audit_en_de_gpt41mini_responses.jsonl",
        ],
    },
]


def read_jsonl(path: str | Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def sum_cost(paths: list[str]) -> float:
    total = 0.0
    for path in paths:
        for record in read_jsonl(path):
            total += record.get("api_cost_estimate_usd") or 0.0
    return total


def usage_summary(paths: list[str]) -> dict[str, int]:
    api_calls = 0
    input_tokens = 0
    output_tokens = 0
    total_tokens = 0
    for path in paths:
        for record in read_jsonl(path):
            usage = record.get("usage") or {}
            api_calls += 1
            input_tokens += int(usage.get("prompt_tokens") or 0)
            output_tokens += int(usage.get("completion_tokens") or 0)
            total_tokens += int(usage.get("total_tokens") or 0)
    if total_tokens == 0:
        total_tokens = input_tokens + output_tokens
    return {
        "api_calls_including_translations": api_calls,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
    }


def summarize() -> pd.DataFrame:
    rows = []
    for spec in RUN_SPECS:
        response_records = []
        for path in spec["responses"]:
            response_records.extend(read_jsonl(path))
        judge_calls = len(response_records)
        parsed = sum(1 for record in response_records if record.get("parse_success") is True)
        unique_items = len({record.get("item_id") for record in response_records})
        if spec["base_items"] is None:
            base_items = unique_items
        else:
            base_items = len(read_jsonl(spec["base_items"]))
        cost = sum_cost(spec["cost_paths"])
        usage = usage_summary(spec["cost_paths"])
        rows.append(
            {
                "run": spec["run"],
                "base_items": base_items,
                "judge_calls": judge_calls,
                "parsed_calls": parsed,
                "parse_rate": parsed / judge_calls if judge_calls else 0.0,
                "unique_judged_items": unique_items,
                "observed_cost_usd": cost,
                "cost_per_1000_judge_calls": 1000.0 * cost / judge_calls if judge_calls else 0.0,
                **usage,
                "avg_total_tokens_per_api_call": (
                    usage["total_tokens"] / usage["api_calls_including_translations"]
                    if usage["api_calls_including_translations"]
                    else 0.0
                ),
            }
        )
    return pd.DataFrame(rows)


def write_markdown(df: pd.DataFrame, path: Path) -> None:
    lines = [
        "# Run Inventory",
        "",
        "Generated from current JSONL artifacts. Costs are returned usage estimates and are incremental for each run. Token counts are from returned API usage metadata and do not depend on a current pricing table.",
        "",
        "```text",
        df.to_string(index=False),
        "```",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df = summarize()
    df.to_csv(OUT_DIR / "run_inventory.csv", index=False)
    write_markdown(df, OUT_DIR / "run_inventory.md")
    print(f"Wrote {OUT_DIR / 'run_inventory.csv'}")
    print(f"Wrote {OUT_DIR / 'run_inventory.md'}")


if __name__ == "__main__":
    main()
