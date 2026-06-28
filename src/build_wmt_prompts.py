from __future__ import annotations

import argparse

from globaljudge_common import PROTOCOL_NAMES, load_config, read_jsonl, write_jsonl


TARGET_RUBRICS = {
    "de": {
        "system": "Sie sind ein sorgfaeltiger Evaluator fuer maschinelle Uebersetzung. Geben Sie nur gueltiges JSON zurueck.",
        "task": "Aufgabe: Bewertung der Qualitaet maschineller Uebersetzung",
        "question": (
            "Ist die Kandidatenuebersetzung im Vergleich zu Quelle und Referenz "
            "genau, fluessig und angemessen?"
        ),
        "question_ref_free": "Ist die Kandidatenuebersetzung im Vergleich zur Quelle genau, fluessig und angemessen?",
        "rubric": (
            "Bewertungsskala:\n"
            "1 = sehr schlechte Uebersetzung mit schwerem Bedeutungsverlust oder unbrauchbarer Sprache\n"
            "2 = schlechte Uebersetzung mit groben Fehlern\n"
            "3 = akzeptable Uebersetzung mit erkennbaren Fehlern\n"
            "4 = gute Uebersetzung mit kleinen Fehlern\n"
            "5 = ausgezeichnete Uebersetzung"
        ),
        "source": "Ausgangstext",
        "reference": "Referenzuebersetzung",
        "candidate": "Kandidatenuebersetzung",
        "judge_note": "Bewerten Sie die Kandidatenuebersetzung, nicht die Referenz.",
        "judge_note_ref_free": "Bewerten Sie die Kandidatenuebersetzung.",
    },
    "ru": {
        "system": "You are a careful machine translation evaluator. Return valid JSON only.",
        "task": "Задача: оценка качества машинного перевода",
        "question": (
            "Является ли перевод-кандидат точным, беглым и адекватным относительно "
            "исходного текста и эталонного перевода?"
        ),
        "question_ref_free": "Является ли перевод-кандидат точным, беглым и адекватным относительно исходного текста?",
        "rubric": (
            "Шкала:\n"
            "1 = очень плохой перевод с серьезной потерей смысла или непригодным языком\n"
            "2 = плохой перевод с крупными ошибками\n"
            "3 = приемлемый перевод с заметными ошибками\n"
            "4 = хороший перевод с небольшими ошибками\n"
            "5 = отличный перевод"
        ),
        "source": "Исходный текст",
        "reference": "Эталонный перевод",
        "candidate": "Перевод-кандидат",
        "judge_note": "Оценивайте перевод-кандидат, а не эталон.",
        "judge_note_ref_free": "Оценивайте перевод-кандидат.",
    },
}


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


def direct_prompt(item: dict, include_reference: bool) -> list[dict[str, str]]:
    meta = item["metadata"]
    question = (
        "Is the candidate translation accurate, fluent, and adequate with respect to the source and reference?"
        if include_reference
        else "Is the candidate translation accurate, fluent, and adequate with respect to the source text?"
    )
    judge_note = "Judge the candidate translation, not the reference." if include_reference else "Judge the candidate translation."
    reference_block = (
        f"\nReference translation:\n{item['reference']}\n"
        if include_reference
        else "\nNo reference translation is provided. Judge against the source text only.\n"
    )
    user = f"""Task: machine translation quality evaluation
Language pair: {item['language_name']}
Source language: {meta['source_language_name']}
Target language: {meta['target_language_name']}

Evaluation dimension: Translation quality
Question:
{question}

Rubric:
1 = very poor translation with severe meaning loss or unusable language
2 = poor translation with major errors
3 = acceptable translation with noticeable errors
4 = good translation with minor errors
5 = excellent translation

Source text:
{item['source_text']}
{reference_block}

Candidate translation:
{item['candidate_output']}

{judge_note}

{json_contract()}"""
    return [
        {"role": "system", "content": "You are a careful machine translation evaluator. Return valid JSON only."},
        {"role": "user", "content": user},
    ]


def target_prompt(item: dict, include_reference: bool) -> list[dict[str, str]]:
    meta = item["metadata"]
    rubric = TARGET_RUBRICS[meta["target_language"]]
    question = rubric["question"] if include_reference else rubric["question_ref_free"]
    judge_note = rubric["judge_note"] if include_reference else rubric["judge_note_ref_free"]
    reference_block = (
        f"\n{rubric['reference']}:\n{item['reference']}\n"
        if include_reference
        else "\nNo reference translation is provided. Judge against the source text only.\n"
    )
    user = f"""{rubric['task']}
Language pair: {item['language_name']}
Source language: {meta['source_language_name']}
Target language: {meta['target_language_name']}

Evaluation dimension: Translation quality
Question:
{question}

{rubric['rubric']}

{rubric['source']}:
{item['source_text']}
{reference_block}

{rubric['candidate']}:
{item['candidate_output']}

{judge_note}

{json_contract()}"""
    return [
        {"role": "system", "content": rubric["system"]},
        {"role": "user", "content": user},
    ]


def pivot_prompt(item: dict, translation: dict, include_reference: bool) -> list[dict[str, str]]:
    question = (
        "Is the candidate translation accurate, fluent, and adequate with respect to the source and reference?"
        if include_reference
        else "Is the candidate translation accurate, fluent, and adequate with respect to the source text?"
    )
    reference_intro = (
        "The source, candidate translation, and reference translation have been translated into English for evaluation."
        if include_reference
        else "The source and candidate translation have been translated into English for reference-free evaluation."
    )
    reference_block = (
        f"\nEnglish translation of reference:\n{translation['english_reference']}\n"
        if include_reference
        else "\nNo reference translation is provided. Judge against the English source text only.\n"
    )
    user = f"""Task: machine translation quality evaluation through an explicit English pivot
Original language pair: {item['language_name']}

{reference_intro}

Evaluation dimension: Translation quality
Question:
{question}

Important:
Judge only what remains visible in the English translations. Do not infer target-language fluency errors that are not visible after translation.

English translation of source text:
{translation['english_source_text']}
{reference_block}

English translation of candidate:
{translation['english_translation']}

{json_contract()}"""
    return [
        {"role": "system", "content": "You are a careful machine translation evaluator. Return valid JSON only."},
        {"role": "user", "content": user},
    ]


def bilingual_prompt(item: dict, include_reference: bool) -> list[dict[str, str]]:
    meta = item["metadata"]
    rubric = TARGET_RUBRICS[meta["target_language"]]
    english_question = (
        "Is the candidate translation accurate, fluent, and adequate with respect to the source and reference?"
        if include_reference
        else "Is the candidate translation accurate, fluent, and adequate with respect to the source text?"
    )
    target_question = rubric["question"] if include_reference else rubric["question_ref_free"]
    judge_note = (
        "Judge the candidate translation, not the reference. Use both rubric versions when helpful."
        if include_reference
        else "Judge the candidate translation. Use both rubric versions when helpful."
    )
    reference_block = (
        f"\nReference translation:\n{item['reference']}\n"
        if include_reference
        else "\nNo reference translation is provided. Judge against the source text only.\n"
    )
    user = f"""Task: machine translation quality evaluation
Language pair: {item['language_name']}
Source language: {meta['source_language_name']}
Target language: {meta['target_language_name']}

English rubric:
{english_question}
1 = very poor translation with severe meaning loss or unusable language
2 = poor translation with major errors
3 = acceptable translation with noticeable errors
4 = good translation with minor errors
5 = excellent translation

Target-language rubric:
{target_question}
{rubric['rubric']}

Source text:
{item['source_text']}
{reference_block}

Candidate translation:
{item['candidate_output']}

{judge_note}

{json_contract()}"""
    return [
        {"role": "system", "content": "You are a careful machine translation evaluator. Return valid JSON only."},
        {"role": "user", "content": user},
    ]


def supports_target_protocol(item: dict) -> bool:
    return item["metadata"]["target_language"] in TARGET_RUBRICS


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/wmt_mqm_n30.yaml")
    args = parser.parse_args()
    config = load_config(args.config)
    evaluation = config.get("evaluation", {})
    include_reference = evaluation.get("reference_mode", "reference_based") != "reference_free"
    dimension = evaluation.get("dimension", "translation_quality_ref_free" if not include_reference else None)
    prompt_id_suffix = evaluation.get("prompt_id_suffix")
    items = read_jsonl(config["paths"]["items_jsonl"])
    selected_pairs = set(config.get("dataset", {}).get("language_pairs", []))
    if selected_pairs:
        items = [item for item in items if item["language"] in selected_pairs]
    translations = {
        row["item_id"]: row
        for row in read_jsonl(config["paths"]["english_translations_jsonl"])
        if row.get("parse_success")
    }
    judge_model = config["judge"]["model"]
    prompts = []
    skipped = 0
    for item in items:
        for protocol in config["protocols"]:
            if protocol == "P0_direct_english":
                messages = direct_prompt(item, include_reference=include_reference)
            elif protocol == "P1_target_rubric":
                if not supports_target_protocol(item):
                    skipped += 1
                    continue
                messages = target_prompt(item, include_reference=include_reference)
            elif protocol == "P2_explicit_pivot":
                if item["item_id"] not in translations:
                    raise KeyError(f"Missing English translation for {item['item_id']}")
                messages = pivot_prompt(item, translations[item["item_id"]], include_reference=include_reference)
            elif protocol == "P3_bilingual":
                if not supports_target_protocol(item):
                    skipped += 1
                    continue
                messages = bilingual_prompt(item, include_reference=include_reference)
            else:
                raise ValueError(f"Unsupported WMT protocol: {protocol}")
            prompt_id_parts = [item["item_id"], protocol]
            if prompt_id_suffix:
                prompt_id_parts.append(str(prompt_id_suffix))
            prompt_id_parts.append(judge_model)
            prompt_id = "__".join(prompt_id_parts)
            prompts.append(
                {
                    "prompt_id": prompt_id,
                    "item_id": item["item_id"],
                    "dataset": item["dataset"],
                    "language": item["language"],
                    "dimension": dimension or item["dimension"],
                    "protocol": protocol,
                    "protocol_name": PROTOCOL_NAMES.get(protocol, protocol),
                    "judge_model": judge_model,
                    "messages": messages,
                    "metadata": {
                        "task": item["task"],
                        "source_language": item["metadata"]["source_language"],
                        "target_language": item["metadata"]["target_language"],
                    },
                }
            )
    write_jsonl(config["paths"]["prompts_jsonl"], prompts)
    print(f"Wrote {len(prompts)} WMT prompts to {config['paths']['prompts_jsonl']}")
    if skipped:
        print(f"Skipped {skipped} target-language WMT prompts without non-English target rubric.")


if __name__ == "__main__":
    main()
