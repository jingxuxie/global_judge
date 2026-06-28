from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

from globaljudge_common import PROTOCOL_NAMES, read_jsonl


OUT_DIR = Path("data/analysis")

ITEMS_PATH = Path("data/processed/candidate_n50_items.jsonl")
TRANSLATIONS_PATH = Path("data/processed/candidate_n50_english_translations.jsonl")
RESPONSES_PATH = Path("data/responses/candidate_n50_combined_explicit_responses.jsonl")


def clean_text(text: str | None, limit: int = 210) -> str:
    if text is None or pd.isna(text):
        return ""
    compact = re.sub(r"\s+", " ", str(text)).strip()
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3].rstrip() + "..."


def score_cell(row: pd.Series, protocol: str) -> str:
    score = row.get(protocol)
    if pd.isna(score):
        return ""
    return str(int(score))


def rationale_cell(row: pd.Series, protocol: str) -> str:
    return clean_text(row.get(f"{protocol}_rationale"), 140)


def load_joined() -> pd.DataFrame:
    items = pd.DataFrame(read_jsonl(ITEMS_PATH))
    translations = pd.DataFrame(read_jsonl(TRANSLATIONS_PATH))
    responses = pd.DataFrame(read_jsonl(RESPONSES_PATH))

    score_wide = responses.pivot_table(
        index="item_id",
        columns="protocol",
        values="score",
        aggfunc="first",
    ).reset_index()

    rationale_rows = []
    for _, row in responses.iterrows():
        parsed = row.get("parsed_response") or {}
        rationale_rows.append(
            {
                "item_id": row["item_id"],
                "protocol": row["protocol"],
                "rationale": parsed.get("rationale_brief", ""),
            }
        )
    rationale_wide = (
        pd.DataFrame(rationale_rows)
        .pivot_table(index="item_id", columns="protocol", values="rationale", aggfunc="first")
        .add_suffix("_rationale")
        .reset_index()
    )

    joined = (
        items.merge(translations[["item_id", "english_translation"]], on="item_id", how="left")
        .merge(score_wide, on="item_id", how="left")
        .merge(rationale_wide, on="item_id", how="left")
    )
    for protocol in PROTOCOL_NAMES:
        if protocol in joined.columns:
            joined[protocol] = pd.to_numeric(joined[protocol], errors="coerce")
    joined = joined[joined["language"] != "en-US"].copy()
    protocol_cols = ["P0_direct_english", "P1_target_rubric", "P2_explicit_pivot", "P3_bilingual"]
    joined["min_nonpivot"] = joined[["P0_direct_english", "P1_target_rubric", "P3_bilingual"]].min(axis=1)
    joined["max_nonpivot"] = joined[["P0_direct_english", "P1_target_rubric", "P3_bilingual"]].max(axis=1)
    joined["pivot_minus_min_nonpivot"] = joined["P2_explicit_pivot"] - joined["min_nonpivot"]
    joined["max_nonpivot_minus_pivot"] = joined["max_nonpivot"] - joined["P2_explicit_pivot"]
    joined["score_pattern"] = joined.apply(
        lambda r: " / ".join(f"{p.replace('P', '')}:{score_cell(r, p)}" for p in protocol_cols),
        axis=1,
    )
    return joined


def select_examples(df: pd.DataFrame) -> pd.DataFrame:
    clean_mask = ~df["candidate_output"].fillna("").str.contains("smallUrl|bigUrl|https?://|mw-parser-output")
    inflated = df[
        (df["human_label"] == 0)
        & (df["P2_explicit_pivot"] >= 4)
        & (df["pivot_minus_min_nonpivot"] >= 2)
        & clean_mask
    ].copy()
    inflated["failure_mode"] = "Pivot inflates human-negative item"
    inflated["effect_size"] = inflated["pivot_minus_min_nonpivot"]

    deflated = df[
        (df["human_label"] == 1)
        & (df["P2_explicit_pivot"] <= 2)
        & (df["max_nonpivot_minus_pivot"] >= 2)
    ].copy()
    deflated["failure_mode"] = "Pivot deflates human-positive item"
    deflated["effect_size"] = deflated["max_nonpivot_minus_pivot"]

    selected = pd.concat(
        [
            inflated.sort_values(["effect_size", "P2_explicit_pivot"], ascending=False).head(8),
            deflated.sort_values(["effect_size", "max_nonpivot"], ascending=False).head(8),
        ],
        ignore_index=True,
    )
    return selected


def write_csv(selected: pd.DataFrame, path: Path) -> None:
    columns = [
        "failure_mode",
        "language",
        "dimension",
        "human_label",
        "item_id",
        "P0_direct_english",
        "P1_target_rubric",
        "P2_explicit_pivot",
        "P3_bilingual",
        "effect_size",
        "candidate_output",
        "english_translation",
        "P1_target_rubric_rationale",
        "P2_explicit_pivot_rationale",
        "P3_bilingual_rationale",
    ]
    selected[columns].to_csv(path, index=False)


def write_markdown(selected: pd.DataFrame, path: Path) -> None:
    lines = [
        "# Qualitative Protocol Examples",
        "",
        "Generated from the main candidate-quality n=50 run. Scores use the 1-5 judge scale.",
        "",
        "Protocol score columns are direct, target-language rubric, explicit English pivot, and bilingual rubric.",
        "",
    ]
    for mode, group in selected.groupby("failure_mode", sort=False):
        lines.extend([f"## {mode}", ""])
        for _, row in group.iterrows():
            lines.extend(
                [
                    f"### {row['language']} / {row['dimension']} / human label {int(row['human_label'])}",
                    "",
                    f"- Item: `{row['item_id']}`",
                    (
                        "- Scores: "
                        f"direct={score_cell(row, 'P0_direct_english')}, "
                        f"target={score_cell(row, 'P1_target_rubric')}, "
                        f"pivot={score_cell(row, 'P2_explicit_pivot')}, "
                        f"bilingual={score_cell(row, 'P3_bilingual')}"
                    ),
                    f"- Original summary: {clean_text(row['candidate_output'])}",
                    f"- English pivot: {clean_text(row['english_translation'])}",
                    f"- Target-rubric rationale: {rationale_cell(row, 'P1_target_rubric')}",
                    f"- Pivot rationale: {rationale_cell(row, 'P2_explicit_pivot')}",
                    f"- Bilingual rationale: {rationale_cell(row, 'P3_bilingual')}",
                    "",
                ]
            )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    joined = load_joined()
    selected = select_examples(joined)
    write_csv(selected, OUT_DIR / "qualitative_protocol_examples.csv")
    write_markdown(selected, OUT_DIR / "qualitative_protocol_examples.md")
    print(f"Wrote {OUT_DIR / 'qualitative_protocol_examples.csv'}")
    print(f"Wrote {OUT_DIR / 'qualitative_protocol_examples.md'}")


if __name__ == "__main__":
    main()
