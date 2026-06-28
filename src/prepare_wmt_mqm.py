from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from datasets import load_dataset

from globaljudge_common import load_config, write_jsonl


LANGUAGE_NAMES = {
    "en": "English",
    "de": "German",
    "ru": "Russian",
    "zh": "Chinese",
}


def truncate(text: str, limit: int) -> str:
    text = str(text)
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + "..."


def sample_pair(frame: pd.DataFrame, n: int, rng: np.random.Generator) -> pd.DataFrame:
    # WMT MQM scores in this dataset are higher-is-better. For 2022, perfect
    # translations are commonly 0 and worse translations have negative scores.
    high_cut = frame["score"].quantile(0.75)
    low_cut = frame["score"].quantile(0.25)
    high = frame[frame["score"] >= high_cut]
    low = frame[frame["score"] <= low_cut]
    pos_n = n // 2
    neg_n = n - pos_n
    if len(high) < pos_n or len(low) < neg_n:
        raise ValueError(
            f"Not enough high/low rows for {frame.iloc[0]['lp']}: "
            f"high={len(high)} low={len(low)} requested={n}"
        )
    pos = high.sample(n=pos_n, random_state=int(rng.integers(1_000_000_000))).copy()
    neg = low.sample(n=neg_n, random_state=int(rng.integers(1_000_000_000))).copy()
    pos["human_label"] = 1
    neg["human_label"] = 0
    sampled = pd.concat([pos, neg], ignore_index=False)
    return sampled.sample(frac=1, random_state=int(rng.integers(1_000_000_000)))


def build_items(config: dict) -> list[dict]:
    dataset_cfg = config["dataset"]
    ds = load_dataset(
        dataset_cfg["hf_dataset"],
        split=dataset_cfg.get("split", "train"),
        cache_dir=config["paths"].get("hf_cache_dir"),
    )
    df = ds.to_pandas()
    df = df[df["year"] == int(dataset_cfg["year"])].copy()
    rng = np.random.default_rng(int(config["seed"]))
    records: list[dict] = []
    for lp in dataset_cfg["language_pairs"]:
        lp_df = df[df["lp"] == lp].copy()
        if lp_df.empty:
            raise ValueError(f"No WMT MQM rows for language pair {lp}")
        sampled = sample_pair(lp_df, int(dataset_cfg["samples_per_language_pair"]), rng)
        src_lang, tgt_lang = lp.split("-")
        for row_index, row in sampled.iterrows():
            item_id = f"wmtmqm_{int(row['year'])}_{lp}_{int(row_index):06d}_{row['system']}"
            records.append(
                {
                    "item_id": item_id,
                    "dataset": "wmt_mqm_human_evaluation",
                    "split": str(dataset_cfg.get("split", "train")),
                    "language": lp,
                    "language_name": f"{LANGUAGE_NAMES.get(src_lang, src_lang)} to {LANGUAGE_NAMES.get(tgt_lang, tgt_lang)}",
                    "task": "machine_translation_quality",
                    "dimension": "translation_quality",
                    "dimension_display": "Translation quality",
                    "dimension_question_en": (
                        "Is the candidate translation accurate, fluent, and adequate "
                        "with respect to the source and reference?"
                    ),
                    "source_text": truncate(row["src"], int(dataset_cfg["max_source_chars"])),
                    "candidate_output": truncate(row["mt"], int(dataset_cfg["max_candidate_chars"])),
                    "reference": truncate(row["ref"], int(dataset_cfg["max_reference_chars"])),
                    "human_label": int(row["human_label"]),
                    "human_label_text": "high_quality" if int(row["human_label"]) == 1 else "low_quality",
                    "metadata": {
                        "source_language": src_lang,
                        "target_language": tgt_lang,
                        "source_language_name": LANGUAGE_NAMES.get(src_lang, src_lang),
                        "target_language_name": LANGUAGE_NAMES.get(tgt_lang, tgt_lang),
                        "human_score": float(row["score"]),
                        "system": row["system"],
                        "annotators": int(row["annotators"]),
                        "domain": row["domain"],
                        "year": int(row["year"]),
                        "candidate_only_dimension": False,
                    },
                }
            )
    return records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/wmt_mqm_n30.yaml")
    args = parser.parse_args()
    config = load_config(args.config)
    records = build_items(config)
    write_jsonl(config["paths"]["items_jsonl"], records)
    counts: dict[tuple[str, int], int] = {}
    for record in records:
        key = (record["language"], record["human_label"])
        counts[key] = counts.get(key, 0) + 1
    print(f"Wrote {len(records)} WMT MQM items to {config['paths']['items_jsonl']}")
    for key, count in sorted(counts.items()):
        print(f"{key}: {count}")


if __name__ == "__main__":
    main()
