from __future__ import annotations

from pathlib import Path

import pandas as pd


OUT_PATH = Path("paper/globaljudge_protocolbench_datacard.md")


def fmt(value: float | int, digits: int = 3) -> str:
    return f"{float(value):.{digits}f}"


def md_table(rows: list[dict[str, object]], columns: list[tuple[str, str]]) -> list[str]:
    lines = [
        "| " + " | ".join(header for _, header in columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(key, "")) for key, _ in columns) + " |")
    return lines


def main() -> None:
    sampling = pd.read_csv("data/analysis/dataset_sampling_summary.csv")
    prompt_inventory = pd.read_csv("data/analysis/prompt_inventory_summary.csv")
    run_inventory = pd.read_csv("data/analysis/run_inventory.csv")
    rq_matrix = pd.read_csv("data/analysis/rq_contribution_matrix.csv")

    sampling_rows = []
    for _, row in sampling.iterrows():
        sampling_rows.append(
            {
                "run": row["run"],
                "items": int(row["items"]),
                "languages": int(row["languages"]),
                "dimensions": int(row["dimensions"]),
                "labels": f"{int(row['human_positive'])}/{int(row['human_negative'])}",
                "source": f"{100 * row['source_available_rate']:.1f}%",
                "reference": f"{100 * row['reference_available_rate']:.1f}%",
            }
        )

    prompt_rows = []
    for _, row in prompt_inventory.iterrows():
        prompt_rows.append(
            {
                "run": row["run"],
                "prompts": int(row["prompts"]),
                "protocols": int(row["n_protocols"]),
                "languages": row["languages"],
                "dimensions": row["dimensions"],
                "judge": row["judge_models"],
            }
        )

    run_rows = []
    for _, row in run_inventory.iterrows():
        run_rows.append(
            {
                "run": row["run"],
                "base": int(row["base_items"]),
                "calls": int(row["judge_calls"]),
                "parse": f"{100 * row['parse_rate']:.1f}%",
                "tokens": int(row["total_tokens"]),
                "cost": f"${row['observed_cost_usd']:.4f}",
            }
        )

    total_items = int(sampling["items"].sum())
    main_items = int(sampling[sampling["run"].isin(["candidate n50", "semantic n30", "wmt n30 shared items"])]["items"].sum())
    total_prompts = int(prompt_inventory["prompts"].sum())
    total_calls = int(run_inventory["judge_calls"].sum())
    total_tokens = int(run_inventory["total_tokens"].sum())
    total_cost = float(run_inventory["observed_cost_usd"].sum())
    min_parse = float(run_inventory["parse_rate"].min())
    protocols = sorted({protocol.strip() for value in prompt_inventory["protocols"] for protocol in str(value).split(",")})
    judges = sorted({model.strip() for value in prompt_inventory["judge_models"] for model in str(value).split(",")})
    coverage = "; ".join(
        f"{row['plan_item']}: {row['coverage']}" for _, row in rq_matrix.head(4).iterrows()
    )

    lines = [
        "# GlobalJudge-ProtocolBench Data Card",
        "",
        "This data card documents the compact benchmark package used by the GlobalJudge protocol-sensitivity paper artifacts.",
        "",
        "## Purpose",
        "",
        "GlobalJudge-ProtocolBench is designed to test whether multilingual LLM-as-a-judge conclusions change when the judge sees different protocol surfaces: original-language text with English instructions, target-language rubric wording, explicit English-pivot translations, or bilingual instructions.",
        "",
        "The benchmark is intended for protocol auditing and reporting practice. It is not intended to rank languages, to declare a universal best judge prompt, or to replace native-speaker evaluation.",
        "",
        "## Composition Snapshot",
        "",
        f"- Main paper-facing base items: {main_items}.",
        f"- Total audited item rows including stronger-judge subsets: {total_items}.",
        f"- Prompt surfaces: {', '.join(protocols)}.",
        f"- Judge models represented in paper-facing runs: {', '.join(judges)}.",
        f"- Paper-facing judge calls: {total_calls}; total prompts in prompt inventory: {total_prompts}.",
        f"- Minimum parse rate across paper-facing runs: {100 * min_parse:.1f}%.",
        f"- Returned total tokens: {total_tokens}; observed local cost estimate: ${total_cost:.4f}.",
        "",
        "## Item Sets",
        "",
    ]
    lines.extend(
        md_table(
            sampling_rows,
            [
                ("run", "Run"),
                ("items", "Items"),
                ("languages", "Langs"),
                ("dimensions", "Dims"),
                ("labels", "Pos/Neg"),
                ("source", "Source Rate"),
                ("reference", "Reference Rate"),
            ],
        )
    )
    lines.extend(["", "## Prompt and Judge Inventory", ""])
    lines.extend(
        md_table(
            prompt_rows,
            [
                ("run", "Run"),
                ("prompts", "Prompts"),
                ("protocols", "Protocols"),
                ("languages", "Languages"),
                ("dimensions", "Dimensions"),
                ("judge", "Judge"),
            ],
        )
    )
    lines.extend(["", "## Run and Cost Inventory", ""])
    lines.extend(
        md_table(
            run_rows,
            [
                ("run", "Run"),
                ("base", "Base Items"),
                ("calls", "Judge Calls"),
                ("parse", "Parse"),
                ("tokens", "Tokens"),
                ("cost", "Cost"),
            ],
        )
    )
    lines.extend(
        [
            "",
            "## Labels and Sampling",
            "",
            "- SEAHORSE candidate-quality labels are binary human yes/no labels for dimensions such as comprehensibility and grammar.",
            "- Source-grounded semantic examples are balanced `main_ideas` examples recovered by matching SEAHORSE reference summaries to raw XLSum records.",
            "- WMT examples use MQM-derived high/low labels from within-language-pair score quantiles; these are protocol stress-test labels, not new human annotations.",
            "- Main sampled cells are balanced by construction; the candidate audit uses 12 positive and 13 negative examples per language/dimension cell.",
            "",
            "## Protocols",
            "",
            "- `P0_direct_english`: original text with English rubric/instructions.",
            "- `P1_target_rubric`: original text with target-language rubric wording.",
            "- `P2_explicit_pivot`: English translations of the judged content, then English judging.",
            "- `P3_bilingual`: original text with English plus target-language rubric wording.",
            "",
            "## Intended Uses",
            "",
            "- Audit whether multilingual LLM judge conclusions are sensitive to protocol choices.",
            "- Report per-language and per-protocol alignment instead of a single aggregate judge score.",
            "- Stress-test English-pivot judging, especially for target-language form dimensions.",
            "- Teach or reproduce a compact reporting-card workflow with parse rate, token usage, and cost.",
            "",
            "## Out-of-Scope Uses",
            "",
            "- Ranking languages by model capability.",
            "- Claiming a universal best protocol across all multilingual evaluation tasks.",
            "- Treating target-language rubric translations as native-speaker validated.",
            "- Treating WMT reference-free labels as a new human annotation target.",
            "- Estimating current provider pricing without refreshing price tables.",
            "",
            "## Coverage Against Project Plan",
            "",
            coverage,
            "",
            "## Known Limitations",
            "",
            "- Main judge calls use OpenAI models; stronger audits use another OpenAI model rather than an independent model family.",
            "- The benchmark is compact and optimized for fast iteration, not broad task/language coverage.",
            "- Target-language rubric wording is pragmatic and should be native-checked before stronger claims about target-language prompting.",
            "- English-pivot translations are produced by the same model family as the judge, which mirrors many practical workflows but should be disclosed.",
            "- Approximate costs are local returned-usage estimates; token usage is the stable accounting quantity.",
            "",
            "## Reproducibility Pointers",
            "",
            "- Reproducibility manifest: `data/analysis/reproducibility_manifest.{json,md}`.",
            "- Prompt inventory with redacted representatives: `data/analysis/prompt_inventory.md`.",
            "- Sampling audit: `data/analysis/dataset_sampling_audit.md`.",
            "- Claim evidence matrix: `data/analysis/claim_evidence_matrix.md`.",
            "- Release validation report: `data/analysis/release_validation_report.md`.",
            "",
        ]
    )
    OUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
