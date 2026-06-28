from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

import yaml


LANGUAGE_NAMES = {
    "en-US": "English",
    "es-ES": "Spanish",
    "de": "German",
    "ru": "Russian",
    "tr": "Turkish",
    "vi": "Vietnamese",
}


QUESTION_METADATA = {
    "comprehensibility": {
        "column": "question1",
        "display": "Comprehensibility",
        "candidate_only": True,
        "question_en": "Is the summary easy to understand as written?",
        "positive_label": "understandable",
    },
    "non_repetition": {
        "column": "question2",
        "display": "No unnecessary repetition",
        "candidate_only": True,
        "question_en": "Is the summary free of unnecessary repetition?",
        "positive_label": "not_repetitive",
    },
    "grammar": {
        "column": "question3",
        "display": "Grammar",
        "candidate_only": True,
        "question_en": "Is the summary grammatical and fluent in its language?",
        "positive_label": "grammatical",
    },
    "attribution": {
        "column": "question4",
        "display": "Attribution",
        "candidate_only": False,
        "question_en": "Is the summary fully supported by the source article?",
        "positive_label": "attributed",
    },
    "main_ideas": {
        "column": "question5",
        "display": "Main ideas",
        "candidate_only": False,
        "question_en": "Does the summary capture the main idea or ideas of the source article?",
        "positive_label": "captures_main_ideas",
    },
    "conciseness": {
        "column": "question6",
        "display": "Conciseness",
        "candidate_only": True,
        "question_en": "Is the summary concise without unnecessary detail?",
        "positive_label": "concise",
    },
}


TARGET_LANGUAGE_TEXT = {
    "en-US": {
        "system": "You are a careful evaluator. Return valid JSON only.",
        "task": "Task: summarization quality evaluation",
        "dimension_label": "Evaluation dimension",
        "question_label": "Question",
        "rubric": (
            "Rubric:\n"
            "1 = very poor\n"
            "2 = poor\n"
            "3 = acceptable\n"
            "4 = good\n"
            "5 = excellent"
        ),
        "summary_label": "Candidate summary",
        "source_label": "Source text",
        "json_instruction": (
            "Return JSON only with keys score, label, confidence, rationale_brief. "
            "Use label bad, borderline, or good."
        ),
        "questions": {
            "comprehensibility": "Is the summary easy to understand as written?",
            "grammar": "Is the summary grammatical and fluent in English?",
            "non_repetition": "Is the summary free of unnecessary repetition?",
            "conciseness": "Is the summary concise without unnecessary detail?",
            "main_ideas": "Does the summary capture the main idea or ideas of the source text?",
        },
    },
    "es-ES": {
        "system": "Eres un evaluador cuidadoso. Devuelve solo JSON valido.",
        "task": "Tarea: evaluacion de la calidad de un resumen",
        "dimension_label": "Dimension de evaluacion",
        "question_label": "Pregunta",
        "rubric": (
            "Rubrica:\n"
            "1 = muy deficiente\n"
            "2 = deficiente\n"
            "3 = aceptable\n"
            "4 = bueno\n"
            "5 = excelente"
        ),
        "summary_label": "Resumen candidato",
        "source_label": "Texto fuente",
        "json_instruction": (
            "Devuelve solo JSON con las claves score, label, confidence, rationale_brief. "
            "Usa label bad, borderline o good."
        ),
        "questions": {
            "comprehensibility": "El resumen es facil de entender tal como esta escrito?",
            "grammar": "El resumen es gramatical y fluido en espanol?",
            "non_repetition": "El resumen esta libre de repeticion innecesaria?",
            "conciseness": "El resumen es conciso y no incluye detalles innecesarios?",
            "main_ideas": "El resumen captura la idea principal o las ideas principales del texto fuente?",
        },
    },
    "tr": {
        "system": "Dikkatli bir degerlendiricisin. Yalnizca gecerli JSON dondur.",
        "task": "Gorev: ozet kalitesi degerlendirmesi",
        "dimension_label": "Degerlendirme boyutu",
        "question_label": "Soru",
        "rubric": (
            "Olcek:\n"
            "1 = cok zayif\n"
            "2 = zayif\n"
            "3 = kabul edilebilir\n"
            "4 = iyi\n"
            "5 = mukemmel"
        ),
        "summary_label": "Aday ozet",
        "source_label": "Kaynak metin",
        "json_instruction": (
            "Yalnizca score, label, confidence, rationale_brief anahtarlarini iceren JSON dondur. "
            "label icin bad, borderline veya good kullan."
        ),
        "questions": {
            "comprehensibility": "Ozet yazildigi haliyle kolay anlasiliyor mu?",
            "grammar": "Ozet Turkce dilbilgisi acisindan dogru ve akici mi?",
            "non_repetition": "Ozet gereksiz tekrardan arinmis mi?",
            "conciseness": "Ozet gereksiz ayrinti olmadan kisa ve oz mu?",
            "main_ideas": "Ozet kaynak metnin ana fikrini veya ana fikirlerini yakaliyor mu?",
        },
    },
    "vi": {
        "system": "Ban la nguoi danh gia can than. Chi tra ve JSON hop le.",
        "task": "Nhiem vu: danh gia chat luong ban tom tat",
        "dimension_label": "Tieu chi danh gia",
        "question_label": "Cau hoi",
        "rubric": (
            "Thang diem:\n"
            "1 = rat kem\n"
            "2 = kem\n"
            "3 = chap nhan duoc\n"
            "4 = tot\n"
            "5 = xuat sac"
        ),
        "summary_label": "Ban tom tat ung vien",
        "source_label": "Van ban nguon",
        "json_instruction": (
            "Chi tra ve JSON voi cac khoa score, label, confidence, rationale_brief. "
            "Dung label bad, borderline, hoac good."
        ),
        "questions": {
            "comprehensibility": "Ban tom tat co de hieu nhu duoc viet khong?",
            "grammar": "Ban tom tat co dung ngu phap va troi chay trong tieng Viet khong?",
            "non_repetition": "Ban tom tat co tranh lap lai khong can thiet khong?",
            "conciseness": "Ban tom tat co ngan gon va khong co chi tiet thua khong?",
            "main_ideas": "Ban tom tat co nam bat y chinh cua van ban nguon khong?",
        },
    },
}


PROTOCOL_NAMES = {
    "P0_direct_english": "Direct English rubric",
    "P1_target_rubric": "Target-language rubric",
    "P2_pivot_in_prompt": "English-pivot diagnostic",
    "P2_explicit_pivot": "Explicit English pivot",
    "P3_bilingual": "Bilingual rubric",
}


APPROX_OPENAI_PRICES_PER_MILLION = {
    # Keep these as approximate run metadata only. Use official pricing pages
    # for paper-ready cost tables because hosted API prices can change.
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4.1-nano": {"input": 0.10, "output": 0.40},
    "gpt-4.1-mini": {"input": 0.40, "output": 1.60},
}


def load_config(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def read_jsonl(path: str | Path) -> list[dict[str, Any]]:
    records = []
    with Path(path).open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def write_jsonl(path: str | Path, records: Iterable[dict[str, Any]]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def append_jsonl(path: str | Path, record: dict[str, Any]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def yes_no_to_int(value: Any) -> int | None:
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized == "yes":
            return 1
        if normalized == "no":
            return 0
    return None


def label_from_score(score: float | int | None) -> str | None:
    if score is None:
        return None
    if score <= 2:
        return "bad"
    if score == 3:
        return "borderline"
    return "good"
