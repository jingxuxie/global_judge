from __future__ import annotations

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from openai import OpenAI

from globaljudge_common import APPROX_OPENAI_PRICES_PER_MILLION, append_jsonl, load_config, read_jsonl


def parse_translation(raw: str, has_source: bool = False) -> tuple[dict[str, str] | None, str | None]:
    text = raw.strip()
    if text.startswith("```"):
        lines = [line for line in text.splitlines() if not line.strip().startswith("```")]
        text = "\n".join(lines).strip()
    try:
        obj = json.loads(text)
    except json.JSONDecodeError as exc:
        return None, f"json_error:{exc.msg}"
    if not isinstance(obj, dict):
        return None, "json_not_object"
    if has_source:
        source_translation = obj.get("source_translation")
        candidate_translation = obj.get("candidate_translation")
        if not isinstance(source_translation, str) or not source_translation.strip():
            return None, "missing_source_translation"
        if not isinstance(candidate_translation, str) or not candidate_translation.strip():
            return None, "missing_candidate_translation"
        return {
            "english_source_text": source_translation.strip(),
            "english_translation": candidate_translation.strip(),
        }, None
    translation = obj.get("translation")
    if not isinstance(translation, str) or not translation.strip():
        return None, "missing_translation"
    return {"english_translation": translation.strip()}, None


def approximate_cost(model: str, input_tokens: int, output_tokens: int) -> float | None:
    prices = APPROX_OPENAI_PRICES_PER_MILLION.get(model)
    if not prices:
        return None
    return (input_tokens / 1_000_000) * prices["input"] + (output_tokens / 1_000_000) * prices["output"]


def existing_item_ids(path: Path) -> set[str]:
    if not path.exists():
        return set()
    return {
        row["item_id"]
        for row in read_jsonl(path)
        if "item_id" in row and row.get("parse_success", False)
    }


def translation_messages(item: dict) -> list[dict[str, str]]:
    if item.get("source_text"):
        return [
            {
                "role": "system",
                "content": "You translate evaluation inputs into English. Return valid JSON only.",
            },
            {
                "role": "user",
                "content": (
                    f"Translate the following {item['language_name']} source text excerpt and candidate summary "
                    "into natural English. Preserve meaning. If a phrase repeats many times, translate it once "
                    "or twice and add [repetition continues]. Keep the source translation under 240 words and "
                    "the candidate translation under 90 words. Do not judge quality.\n\n"
                    f"Source text excerpt:\n{item['source_text']}\n\n"
                    f"Candidate summary:\n{item['candidate_output']}\n\n"
                    'Return JSON only: {"source_translation": string, "candidate_translation": string}'
                ),
            },
        ]
    return [
        {
            "role": "system",
            "content": "You translate summaries into English. Return valid JSON only.",
        },
        {
            "role": "user",
            "content": (
                f"Translate the following {item['language_name']} candidate summary into natural English. "
                "Preserve meaning and obvious repetition, but if a phrase repeats many times, translate it once "
                "or twice and add [repetition continues] instead of continuing the loop. Keep the translation "
                "under 90 words. Do not judge quality.\n\n"
                f"Candidate summary:\n{item['candidate_output']}\n\n"
                'Return JSON only: {"translation": string}'
            ),
        },
    ]


def copy_english_record(item: dict, model: str) -> dict[str, Any]:
    return {
        "item_id": item["item_id"],
        "language": item["language"],
        "translation_model": model,
        "raw_response": None,
        "english_translation": item["candidate_output"],
        "english_source_text": item.get("source_text"),
        "parse_success": True,
        "parse_error": None,
        "api_error": None,
        "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
        "api_cost_estimate_usd": 0.0,
        "elapsed_seconds": 0.0,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "metadata": {"copied_original_english": True},
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/pilot_seahorse_20_explicit_pivot.yaml")
    parser.add_argument("--api-key-file", default="apikey.txt")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    config = load_config(args.config)
    items = read_jsonl(config["paths"]["items_jsonl"])
    output_path = Path(config["paths"]["english_translations_jsonl"])
    done = existing_item_ids(output_path)
    pending = [item for item in items if item["item_id"] not in done]
    if args.limit is not None:
        pending = pending[: args.limit]
    print(f"Items total={len(items)} done={len(done)} pending_this_run={len(pending)}")
    if args.dry_run:
        for item in pending[:3]:
            print("=" * 80)
            print(item["item_id"])
            print(translation_messages(item)[1]["content"][:1000])
        return

    model = config.get("translation", {}).get("model", config["judge"]["model"])
    max_tokens = int(config.get("translation", {}).get("max_output_tokens", 180))
    temperature = float(config.get("translation", {}).get("temperature", 0))
    client = OpenAI(api_key=Path(args.api_key_file).read_text(encoding="utf-8").strip())

    for index, item in enumerate(pending, start=1):
        if item["language"] == "en-US":
            append_jsonl(output_path, copy_english_record(item, model))
            print(f"[{index}/{len(pending)}] copied {item['item_id']}")
            continue

        started = time.time()
        raw = ""
        usage = {}
        translation_fields = None
        parse_error = None
        api_error = None
        try:
            response = client.chat.completions.create(
                model=model,
                messages=translation_messages(item),
                temperature=temperature,
                max_tokens=max_tokens,
                response_format={"type": "json_object"},
            )
            raw = response.choices[0].message.content or ""
            usage = {
                "prompt_tokens": getattr(response.usage, "prompt_tokens", 0) if response.usage else 0,
                "completion_tokens": getattr(response.usage, "completion_tokens", 0) if response.usage else 0,
                "total_tokens": getattr(response.usage, "total_tokens", 0) if response.usage else 0,
            }
            translation_fields, parse_error = parse_translation(raw, has_source=bool(item.get("source_text")))
        except Exception as exc:  # noqa: BLE001 - cache API failures for audit.
            api_error = repr(exc)

        translation_fields = translation_fields or {}
        record = {
            "item_id": item["item_id"],
            "language": item["language"],
            "translation_model": model,
            "raw_response": raw,
            "english_translation": translation_fields.get("english_translation"),
            "english_source_text": translation_fields.get("english_source_text"),
            "parse_success": bool(translation_fields.get("english_translation"))
            and (not item.get("source_text") or bool(translation_fields.get("english_source_text"))),
            "parse_error": parse_error,
            "api_error": api_error,
            "usage": usage,
            "api_cost_estimate_usd": approximate_cost(
                model,
                int(usage.get("prompt_tokens", 0) or 0),
                int(usage.get("completion_tokens", 0) or 0),
            ),
            "elapsed_seconds": round(time.time() - started, 3),
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "metadata": {"copied_original_english": False},
        }
        append_jsonl(output_path, record)
        status = "ok" if record["parse_success"] else "fail"
        print(f"[{index}/{len(pending)}] {status} {item['item_id']} cost={record['api_cost_estimate_usd']}")


if __name__ == "__main__":
    main()
