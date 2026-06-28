from __future__ import annotations

import argparse

from globaljudge_common import (
    LANGUAGE_NAMES,
    PROTOCOL_NAMES,
    QUESTION_METADATA,
    TARGET_LANGUAGE_TEXT,
    load_config,
    read_jsonl,
    write_jsonl,
)


def json_contract() -> str:
    return (
        'Return JSON only:\n'
        '{\n'
        '  "score": integer from 1 to 5,\n'
        '  "label": "bad" | "borderline" | "good",\n'
        '  "confidence": number from 0 to 1,\n'
        '  "rationale_brief": string of at most 18 words\n'
        '}'
    )


def direct_prompt(item: dict) -> list[dict[str, str]]:
    lang = item["language_name"]
    meta = QUESTION_METADATA[item["dimension"]]
    source_block = ""
    if item.get("source_text"):
        source_block = f"\nSource text:\n{item['source_text']}\n"
    no_source_instruction = (
        "Judge only the candidate summary. Do not infer facts from an unavailable source article."
        if not item.get("source_text")
        else "Judge the candidate summary against the source text."
    )
    user = f"""Task: summarization quality evaluation
Language of candidate summary: {lang}

Evaluation dimension: {meta["display"]}
Rubric:
1 = very poor
2 = poor
3 = acceptable
4 = good
5 = excellent

Question:
{meta["question_en"]}
{source_block}
Candidate summary:
{item["candidate_output"]}

{no_source_instruction}

{json_contract()}"""
    return [
        {"role": "system", "content": "You are a careful evaluator. Return valid JSON only."},
        {"role": "user", "content": user},
    ]


def target_prompt(item: dict) -> list[dict[str, str]]:
    language = item["language"]
    text = TARGET_LANGUAGE_TEXT.get(language, TARGET_LANGUAGE_TEXT["en-US"])
    dimension = item["dimension"]
    question = text["questions"].get(dimension, QUESTION_METADATA[dimension]["question_en"])
    source_block = ""
    if item.get("source_text"):
        source_block = f"\n{text['source_label']}:\n{item['source_text']}\n"
    user = f"""{text["task"]}
{text["dimension_label"]}: {QUESTION_METADATA[dimension]["display"]}

{text["question_label"]}:
{question}

{text["rubric"]}
{source_block}
{text["summary_label"]}:
{item["candidate_output"]}

{text["json_instruction"]}"""
    return [
        {"role": "system", "content": text["system"]},
        {"role": "user", "content": user},
    ]


def pivot_prompt(item: dict) -> list[dict[str, str]]:
    lang = item["language_name"]
    meta = QUESTION_METADATA[item["dimension"]]
    user = f"""Task: summarization quality evaluation through an English pivot
Original language of candidate summary: {lang}

First, internally translate the candidate summary into English. Then evaluate only the English translation.

Evaluation dimension: {meta["display"]}
Question:
{meta["question_en"]}

Important:
For grammar, fluency, or language-form dimensions, judge what remains visible after English translation.
Do not score target-language grammar directly in this protocol.

Candidate summary in original language:
{item["candidate_output"]}

{json_contract()}"""
    return [
        {"role": "system", "content": "You are a careful evaluator. Return valid JSON only."},
        {"role": "user", "content": user},
    ]


def explicit_pivot_prompt(item: dict, translation_record: dict | str) -> list[dict[str, str]]:
    lang = item["language_name"]
    meta = QUESTION_METADATA[item["dimension"]]
    if isinstance(translation_record, str):
        candidate_translation = translation_record
        source_translation = None
    else:
        candidate_translation = translation_record.get("english_translation")
        source_translation = translation_record.get("english_source_text")
    source_block = ""
    if source_translation:
        source_block = f"\nEnglish translation of source text:\n{source_translation}\n"
    user = f"""Task: summarization quality evaluation through an explicit English pivot
Original language of candidate summary: {lang}

The source and candidate summary have been translated into English for evaluation when a source is available.

Evaluation dimension: {meta["display"]}
Question:
{meta["question_en"]}

Important:
For grammar, fluency, or language-form dimensions, judge only what remains visible in the English translation.
Do not infer or directly score target-language grammar because the original wording is not shown in this protocol.
{source_block}
English translation of candidate summary:
{candidate_translation}

{json_contract()}"""
    return [
        {"role": "system", "content": "You are a careful evaluator. Return valid JSON only."},
        {"role": "user", "content": user},
    ]


def bilingual_prompt(item: dict) -> list[dict[str, str]]:
    language = item["language"]
    target = TARGET_LANGUAGE_TEXT.get(language, TARGET_LANGUAGE_TEXT["en-US"])
    meta = QUESTION_METADATA[item["dimension"]]
    target_question = target["questions"].get(item["dimension"], meta["question_en"])
    lang = LANGUAGE_NAMES.get(language, language)
    source_block = ""
    if item.get("source_text"):
        source_block = f"\nSource text / {target['source_label']}:\n{item['source_text']}\n"
    user = f"""Task / Task in target language: summarization quality evaluation / {target["task"]}
Language / Target language: {lang} / {language}

Evaluation dimension / {target["dimension_label"]}:
{meta["display"]}

Question:
{meta["question_en"]}
{target["question_label"]}:
{target_question}

Rubric:
1 = very poor
2 = poor
3 = acceptable
4 = good
5 = excellent

{target["rubric"]}
{source_block}
Candidate summary / {target["summary_label"]}:
{item["candidate_output"]}

{json_contract()}"""
    return [
        {"role": "system", "content": "You are a careful bilingual evaluator. Return valid JSON only."},
        {"role": "user", "content": user},
    ]


PROMPT_BUILDERS = {
    "P0_direct_english": direct_prompt,
    "P1_target_rubric": target_prompt,
    "P2_pivot_in_prompt": pivot_prompt,
    "P3_bilingual": bilingual_prompt,
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/pilot_seahorse.yaml")
    args = parser.parse_args()
    config = load_config(args.config)
    items = read_jsonl(config["paths"]["items_jsonl"])
    judge_model = config["judge"]["model"]
    translations = {}
    if "english_translations_jsonl" in config["paths"]:
        translations = {
            row["item_id"]: row
            for row in read_jsonl(config["paths"]["english_translations_jsonl"])
            if row.get("parse_success", True)
        }
    prompts = []
    for item in items:
        for protocol in config["protocols"]:
            if protocol == "P2_explicit_pivot":
                if item["item_id"] not in translations:
                    raise KeyError(f"Missing English translation for {item['item_id']}")
                messages = explicit_pivot_prompt(item, translations[item["item_id"]])
            else:
                messages = PROMPT_BUILDERS[protocol](item)
            prompt_id = f"{item['item_id']}__{protocol}__{judge_model}"
            prompts.append(
                {
                    "prompt_id": prompt_id,
                    "item_id": item["item_id"],
                    "dataset": item["dataset"],
                    "language": item["language"],
                    "dimension": item["dimension"],
                    "protocol": protocol,
                    "protocol_name": PROTOCOL_NAMES[protocol],
                    "judge_model": judge_model,
                    "messages": messages,
                    "metadata": {
                        "pivot_is_diagnostic": protocol == "P2_pivot_in_prompt",
                        "candidate_only_dimension": item["metadata"]["candidate_only_dimension"],
                    },
                }
            )
    write_jsonl(config["paths"]["prompts_jsonl"], prompts)
    print(f"Wrote {len(prompts)} prompts to {config['paths']['prompts_jsonl']}")


if __name__ == "__main__":
    main()
