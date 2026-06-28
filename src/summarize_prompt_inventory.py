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
        "prompt_files": ["data/prompts/candidate_n50_combined_explicit_prompts.jsonl"],
    },
    {
        "run": "candidate audit n25",
        "prompt_files": ["data/prompts/audit_gpt41mini_n25_combined_explicit_prompts.jsonl"],
    },
    {
        "run": "semantic n30",
        "prompt_files": ["data/prompts/semantic_xlsum_n30_prompts.jsonl"],
    },
    {
        "run": "wmt reference n30",
        "prompt_files": ["data/prompts/wmt_mqm_n30_prompts.jsonl"],
    },
    {
        "run": "wmt ref-free n30",
        "prompt_files": ["data/prompts/wmt_mqm_ref_free_n30_prompts.jsonl"],
    },
    {
        "run": "wmt ref-free audit",
        "prompt_files": [
            "data/prompts/wmt_mqm_ref_free_audit_zh_en_gpt41mini_prompts.jsonl",
            "data/prompts/wmt_mqm_ref_free_audit_en_de_gpt41mini_prompts.jsonl",
        ],
    },
]

TEXT_BLOCK_LABELS = {
    "source text",
    "reference text",
    "reference translation",
    "candidate summary",
    "candidate translation",
    "english translation of source",
    "english translation of source text",
    "english translation of reference",
    "english translation of candidate summary",
    "english translation of candidate translation",
    "english translation of candidate",
    "translated source text",
    "translated reference translation",
    "translated candidate translation",
    "texto fuente",
    "resumen candidato",
    "kaynak metin",
    "aday ozet",
    "van ban nguon",
    "ban tom tat ung vien",
    "ausgangstext",
    "referenzuebersetzung",
    "kandidatenuebersetzung",
    "исходный текст",
    "эталонный перевод",
    "перевод-кандидат",
}


def is_text_block_label(stripped: str) -> bool:
    if not stripped.endswith(":"):
        return False
    label = stripped[:-1].strip().lower()
    parts = [part.strip() for part in label.split("/")]
    return any(part in TEXT_BLOCK_LABELS for part in parts)


def read_jsonl(path: str | Path) -> list[dict[str, Any]]:
    with Path(path).open("r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def message_content(prompt: dict[str, Any], role: str) -> str:
    for message in prompt["messages"]:
        if message["role"] == role:
            return message["content"]
    return ""


def redact_item_text(user_text: str) -> str:
    lines = user_text.splitlines()
    out: list[str] = []
    skip_block = False
    for line in lines:
        stripped = line.strip()
        if skip_block:
            if stripped == "":
                out.append(line)
                skip_block = False
            continue
        if is_text_block_label(stripped):
            out.append(line)
            out.append("<item text redacted>")
            skip_block = True
            continue
        out.append(line)
    return "\n".join(out).strip()


def inventory_rows() -> list[dict[str, Any]]:
    rows = []
    for spec in RUN_SPECS:
        for prompt_file in spec["prompt_files"]:
            for prompt in read_jsonl(prompt_file):
                system = message_content(prompt, "system")
                user = message_content(prompt, "user")
                rows.append(
                    {
                        "run": spec["run"],
                        "prompt_file": prompt_file,
                        "prompt_id": prompt["prompt_id"],
                        "dataset": prompt.get("dataset", ""),
                        "judge_model": prompt.get("judge_model", ""),
                        "language": prompt.get("language", ""),
                        "dimension": prompt.get("dimension", ""),
                        "protocol": prompt.get("protocol", ""),
                        "protocol_name": prompt.get("protocol_name", prompt.get("protocol", "")),
                        "system_chars": len(system),
                        "user_chars": len(user),
                        "messages": len(prompt.get("messages", [])),
                    }
                )
    return rows


def join_values(values: pd.Series) -> str:
    return ", ".join(sorted(str(value) for value in values.dropna().unique()))


def summarize(inventory: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for run, group in inventory.groupby("run", sort=False):
        rows.append(
            {
                "run": run,
                "prompt_files": len(group["prompt_file"].unique()),
                "prompts": len(group),
                "protocols": join_values(group["protocol"]),
                "n_protocols": group["protocol"].nunique(),
                "languages": join_values(group["language"]),
                "n_languages": group["language"].nunique(),
                "dimensions": join_values(group["dimension"]),
                "n_dimensions": group["dimension"].nunique(),
                "judge_models": join_values(group["judge_model"]),
                "mean_user_chars": group["user_chars"].mean(),
                "max_user_chars": group["user_chars"].max(),
            }
        )
    return pd.DataFrame(rows)


def representative_rows(inventory: pd.DataFrame) -> list[dict[str, Any]]:
    rows = []
    for (run, protocol), group in inventory.groupby(["run", "protocol"], sort=False):
        # Prefer a non-English example when possible, because protocol differences are clearer there.
        ordered = group.assign(non_english=group["language"].ne("en-US")).sort_values(
            ["non_english", "language", "dimension"], ascending=[False, True, True]
        )
        row = ordered.iloc[0]
        prompt = None
        for record in read_jsonl(row["prompt_file"]):
            if record["prompt_id"] == row["prompt_id"]:
                prompt = record
                break
        if prompt is None:
            continue
        rows.append(
            {
                "run": run,
                "protocol": protocol,
                "language": row["language"],
                "dimension": row["dimension"],
                "judge_model": row["judge_model"],
                "system": message_content(prompt, "system"),
                "user_template": redact_item_text(message_content(prompt, "user")),
            }
        )
    return rows


def write_markdown(summary: pd.DataFrame, representatives: list[dict[str, Any]]) -> None:
    lines = [
        "# Prompt Inventory",
        "",
        "Generated from the current prompt JSONL artifacts. Representative prompts redact item-specific source, reference, and candidate text while preserving instructions, rubric wording, protocol surface, and JSON output contract.",
        "",
        "## Summary",
        "",
        "| Run | Prompts | Protocols | Languages | Dimensions | Judge Models | Mean User Chars | Max User Chars |",
        "| --- | ---: | --- | --- | --- | --- | ---: | ---: |",
    ]
    for _, row in summary.iterrows():
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["run"]),
                    str(int(row["prompts"])),
                    str(row["protocols"]),
                    str(row["languages"]),
                    str(row["dimensions"]),
                    str(row["judge_models"]),
                    f"{row['mean_user_chars']:.1f}",
                    str(int(row["max_user_chars"])),
                ]
            )
            + " |"
        )
    lines.extend(["", "## Representative Redacted Prompt Surfaces", ""])
    for row in representatives:
        lines.extend(
            [
                f"### {row['run']} / {row['protocol']} / {row['language']} / {row['dimension']}",
                "",
                f"System: `{row['system']}`",
                "",
                "```text",
                row["user_template"],
                "```",
                "",
            ]
        )
    (OUT_DIR / "prompt_inventory.md").write_text("\n".join(lines), encoding="utf-8")


def write_latex(summary: pd.DataFrame) -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    lines = [
        "\\begin{table}[t]",
        "\\centering",
        "\\caption{Prompt inventory for paper-facing runs.}",
        "\\label{tab:prompt_inventory}",
        "\\resizebox{\\linewidth}{!}{%",
        "\\begin{tabular}{lrrrrl}",
        "\\toprule",
        "Run & Prompts & Protocols & Langs & Dims & Judge \\\\",
        "\\midrule",
    ]
    for _, row in summary.iterrows():
        lines.append(
            " & ".join(
                [
                    str(row["run"]).replace("_", "\\_"),
                    str(int(row["prompts"])),
                    str(int(row["n_protocols"])),
                    str(int(row["n_languages"])),
                    str(int(row["n_dimensions"])),
                    str(row["judge_models"]).replace("_", "\\_"),
                ]
            )
            + " \\\\"
        )
    lines.extend(["\\bottomrule", "\\end{tabular}%", "}", "\\end{table}", ""])
    (TABLE_DIR / "prompt_inventory.tex").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    inventory = pd.DataFrame(inventory_rows())
    summary = summarize(inventory)
    representatives = representative_rows(inventory)
    inventory.to_csv(OUT_DIR / "prompt_inventory.csv", index=False)
    summary.to_csv(OUT_DIR / "prompt_inventory_summary.csv", index=False)
    pd.DataFrame(representatives).to_csv(OUT_DIR / "prompt_representatives.csv", index=False)
    write_markdown(summary, representatives)
    write_latex(summary)
    print(f"Wrote {OUT_DIR / 'prompt_inventory.csv'}")
    print(f"Wrote {OUT_DIR / 'prompt_inventory_summary.csv'}")
    print(f"Wrote {OUT_DIR / 'prompt_representatives.csv'}")
    print(f"Wrote {OUT_DIR / 'prompt_inventory.md'}")
    print(f"Wrote {TABLE_DIR / 'prompt_inventory.tex'}")


if __name__ == "__main__":
    main()
