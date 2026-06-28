from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from globaljudge_common import LANGUAGE_NAMES, QUESTION_METADATA, load_config, write_jsonl, yes_no_to_int


def sample_balanced(
    frame: pd.DataFrame,
    label_column: str,
    n: int,
    rng: np.random.Generator,
) -> pd.DataFrame:
    positives = frame[frame[label_column] == 1]
    negatives = frame[frame[label_column] == 0]
    pos_target = n // 2
    neg_target = n - pos_target

    parts = []
    if len(positives):
        parts.append(positives.sample(n=min(pos_target, len(positives)), random_state=int(rng.integers(1e9))))
    if len(negatives):
        parts.append(negatives.sample(n=min(neg_target, len(negatives)), random_state=int(rng.integers(1e9))))

    sampled = pd.concat(parts, ignore_index=False) if parts else frame.iloc[0:0]
    if len(sampled) < n:
        remaining = frame.drop(index=sampled.index, errors="ignore")
        if len(remaining):
            topup = remaining.sample(n=min(n - len(sampled), len(remaining)), random_state=int(rng.integers(1e9)))
            sampled = pd.concat([sampled, topup], ignore_index=False)
    return sampled.sample(frac=1, random_state=int(rng.integers(1e9)))


def build_items(config: dict) -> list[dict]:
    rng = np.random.default_rng(config["seed"])
    raw_dir = Path(config["paths"]["seahorse_raw_dir"])
    split = config["dataset"]["split"]
    path = raw_dir / f"{split}.tsv"
    if not path.exists():
        raise FileNotFoundError(f"Missing SEAHORSE split: {path}")

    df = pd.read_csv(path, sep="\t")
    df = df.reset_index(names="seahorse_row")
    max_chars = int(config["dataset"].get("max_summary_chars", 1200))
    records: list[dict] = []

    for language in config["dataset"]["languages"]:
        lang_df = df[df["worker_lang"] == language].copy()
        if lang_df.empty:
            raise ValueError(f"No rows found for language {language}")

        for dimension in config["dataset"]["dimensions"]:
            meta = QUESTION_METADATA[dimension]
            column = meta["column"]
            dim_df = lang_df.copy()
            dim_df["human_label"] = dim_df[column].map(yes_no_to_int)
            dim_df = dim_df[dim_df["human_label"].notna()].copy()
            if column != "question1":
                # Per the SEAHORSE README, later question ratings are only
                # meaningful when the summary is comprehensible.
                dim_df = dim_df[dim_df["question1"].astype(str).str.lower() == "yes"]
            if dim_df.empty:
                raise ValueError(f"No rows for {language}/{dimension}")

            sampled = sample_balanced(
                dim_df,
                "human_label",
                int(config["dataset"]["samples_per_language_dimension"]),
                rng,
            )
            for _, row in sampled.iterrows():
                item_id = (
                    f"seahorse_{split}_{language}_{dimension}_"
                    f"{int(row['seahorse_row']):06d}_{row['model']}"
                )
                summary = str(row["summary"])
                if len(summary) > max_chars:
                    summary = summary[:max_chars].rstrip() + "..."
                records.append(
                    {
                        "item_id": item_id,
                        "dataset": "seahorse",
                        "split": split,
                        "language": language,
                        "language_name": LANGUAGE_NAMES.get(language, language),
                        "task": "summarization_candidate_quality",
                        "dimension": dimension,
                        "dimension_display": meta["display"],
                        "dimension_column": column,
                        "dimension_question_en": meta["question_en"],
                        "candidate_output": summary,
                        "source_text": None,
                        "reference": None,
                        "human_label": int(row["human_label"]),
                        "human_label_text": "yes" if int(row["human_label"]) == 1 else "no",
                        "metadata": {
                            "gem_id": row["gem_id"],
                            "summary_model": row["model"],
                            "seahorse_row": int(row["seahorse_row"]),
                            "candidate_only_dimension": bool(meta["candidate_only"]),
                        },
                    }
                )
    return records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/pilot_seahorse.yaml")
    args = parser.parse_args()
    config = load_config(args.config)
    records = build_items(config)
    write_jsonl(config["paths"]["items_jsonl"], records)
    by_key: dict[tuple[str, str, int], int] = {}
    for record in records:
        key = (record["language"], record["dimension"], record["human_label"])
        by_key[key] = by_key.get(key, 0) + 1
    print(f"Wrote {len(records)} items to {config['paths']['items_jsonl']}")
    for key, count in sorted(by_key.items()):
        print(f"{key}: {count}")


if __name__ == "__main__":
    main()
