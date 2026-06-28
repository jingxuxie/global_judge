from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

from globaljudge_common import LANGUAGE_NAMES, QUESTION_METADATA, load_config, write_jsonl, yes_no_to_int
from prepare_seahorse import sample_balanced


LANG_TO_XLSUM = {
    "es-ES": "spanish",
    "tr": "turkish",
    "vi": "vietnamese",
}


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", str(value)).strip().lower()


def load_xlsum_by_summary(raw_dir: Path, xlsum_language: str) -> dict[str, dict]:
    path = raw_dir / f"{xlsum_language}_test.jsonl"
    if not path.exists():
        raise FileNotFoundError(f"Missing XLSum test file: {path}")
    by_summary = {}
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            by_summary[normalize_text(row["summary"])] = row
    return by_summary


def build_source_map(seahorse: pd.DataFrame, xlsum_raw_dir: Path, languages: list[str]) -> dict[str, dict]:
    source_map: dict[str, dict] = {}
    for language in languages:
        xlsum_language = LANG_TO_XLSUM[language]
        raw_by_summary = load_xlsum_by_summary(xlsum_raw_dir, xlsum_language)
        refs = seahorse[
            (seahorse["worker_lang"] == language)
            & (seahorse["model"] == "reference")
            & (seahorse["gem_id"].str.startswith(f"xlsum_{xlsum_language}-test-"))
        ]
        for _, row in refs.iterrows():
            raw = raw_by_summary.get(normalize_text(row["summary"]))
            if raw:
                source_map[row["gem_id"]] = raw
    return source_map


def truncate_text(text: str, max_chars: int) -> str:
    text = re.sub(r"\s+", " ", str(text)).strip()
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rsplit(" ", 1)[0].rstrip() + "..."


def build_items(config: dict) -> list[dict]:
    rng = np.random.default_rng(config["seed"])
    raw_dir = Path(config["paths"]["seahorse_raw_dir"])
    xlsum_raw_dir = Path(config["paths"]["xlsum_raw_dir"])
    split = config["dataset"]["split"]
    df = pd.read_csv(raw_dir / f"{split}.tsv", sep="\t").reset_index(names="seahorse_row")
    languages = config["dataset"]["languages"]
    source_map = build_source_map(df, xlsum_raw_dir, languages)
    max_source_chars = int(config["dataset"].get("max_source_chars", 1400))
    max_summary_chars = int(config["dataset"].get("max_summary_chars", 700))

    records = []
    for language in languages:
        xlsum_language = LANG_TO_XLSUM[language]
        lang_df = df[
            (df["worker_lang"] == language)
            & (df["gem_id"].str.startswith(f"xlsum_{xlsum_language}-test-"))
            & (df["gem_id"].isin(source_map))
            & (df["model"] != "reference")
            & (df["question1"].astype(str).str.lower() == "yes")
        ].copy()
        for dimension in config["dataset"]["dimensions"]:
            meta = QUESTION_METADATA[dimension]
            lang_df["human_label"] = lang_df[meta["column"]].map(yes_no_to_int)
            dim_df = lang_df[lang_df["human_label"].notna()].copy()
            sampled = sample_balanced(
                dim_df,
                "human_label",
                int(config["dataset"]["samples_per_language_dimension"]),
                rng,
            )
            for _, row in sampled.iterrows():
                source = source_map[row["gem_id"]]
                item_id = (
                    f"seahorse_xlsum_{split}_{language}_{dimension}_"
                    f"{int(row['seahorse_row']):06d}_{row['model']}"
                )
                records.append(
                    {
                        "item_id": item_id,
                        "dataset": "seahorse_xlsum",
                        "split": split,
                        "language": language,
                        "language_name": LANGUAGE_NAMES.get(language, language),
                        "task": "summarization_source_grounded_quality",
                        "dimension": dimension,
                        "dimension_display": meta["display"],
                        "dimension_column": meta["column"],
                        "dimension_question_en": meta["question_en"],
                        "source_text": truncate_text(source["text"], max_source_chars),
                        "candidate_output": truncate_text(row["summary"], max_summary_chars),
                        "reference": truncate_text(source["summary"], max_summary_chars),
                        "human_label": int(row["human_label"]),
                        "human_label_text": "yes" if int(row["human_label"]) == 1 else "no",
                        "metadata": {
                            "gem_id": row["gem_id"],
                            "summary_model": row["model"],
                            "seahorse_row": int(row["seahorse_row"]),
                            "xlsum_id": source.get("id"),
                            "xlsum_url": source.get("url"),
                            "candidate_only_dimension": False,
                        },
                    }
                )
    return records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/semantic_xlsum_pilot.yaml")
    args = parser.parse_args()
    config = load_config(args.config)
    records = build_items(config)
    write_jsonl(config["paths"]["items_jsonl"], records)
    print(f"Wrote {len(records)} items to {config['paths']['items_jsonl']}")
    counts = {}
    for record in records:
        key = (record["language"], record["dimension"], record["human_label"])
        counts[key] = counts.get(key, 0) + 1
    for key, count in sorted(counts.items()):
        print(f"{key}: {count}")


if __name__ == "__main__":
    main()
