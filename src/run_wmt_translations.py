from __future__ import annotations

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from openai import OpenAI

from globaljudge_common import APPROX_OPENAI_PRICES_PER_MILLION, append_jsonl, load_config, read_jsonl


def approximate_cost(model: str, input_tokens: int, output_tokens: int) -> float | None:
    prices = APPROX_OPENAI_PRICES_PER_MILLION.get(model)
    if not prices:
        return None
    return (input_tokens / 1_000_000) * prices["input"] + (output_tokens / 1_000_000) * prices["output"]


def parse_translation(raw: str) -> tuple[dict[str, str] | None, str | None]:
    text = raw.strip()
    if text.startswith("```"):
        lines = [line for line in text.splitlines() if not line.strip().startswith("```")]
        text = "\n".join(lines).strip()
    try:
        obj = json.loads(text)
    except json.JSONDecodeError as exc:
        return None, f"json_error:{exc.msg}"
    required = ["source_translation", "candidate_translation", "reference_translation"]
    if not isinstance(obj, dict):
        return None, "json_not_object"
    for key in required:
        if not isinstance(obj.get(key), str) or not obj[key].strip():
            return None, f"missing_{key}"
    return {
        "english_source_text": obj["source_translation"].strip(),
        "english_translation": obj["candidate_translation"].strip(),
        "english_reference": obj["reference_translation"].strip(),
    }, None


def existing_success_ids(path: Path) -> set[str]:
    if not path.exists():
        return set()
    return {row["item_id"] for row in read_jsonl(path) if row.get("parse_success") and "item_id" in row}


def messages(item: dict) -> list[dict[str, str]]:
    meta = item["metadata"]
    return [
        {
            "role": "system",
            "content": "You translate machine-translation evaluation inputs into English. Return valid JSON only.",
        },
        {
            "role": "user",
            "content": (
                "Translate each field into natural English while preserving meaning, errors, omissions, "
                "awkward wording, and mistranslations as much as possible. Do not judge quality.\n\n"
                f"Language pair: {item['language_name']}\n"
                f"Source language: {meta['source_language_name']}\n"
                f"Target language: {meta['target_language_name']}\n\n"
                f"Source text:\n{item['source_text']}\n\n"
                f"Candidate translation:\n{item['candidate_output']}\n\n"
                f"Reference translation:\n{item['reference']}\n\n"
                'Return JSON only: {"source_translation": string, '
                '"candidate_translation": string, "reference_translation": string}'
            ),
        },
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/wmt_mqm_n30.yaml")
    parser.add_argument("--api-key-file", default="apikey.txt")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()
    config = load_config(args.config)
    items = read_jsonl(config["paths"]["items_jsonl"])
    output_path = Path(config["paths"]["english_translations_jsonl"])
    done = existing_success_ids(output_path)
    pending = [item for item in items if item["item_id"] not in done]
    if args.limit is not None:
        pending = pending[: args.limit]
    print(f"Items total={len(items)} done={len(done)} pending_this_run={len(pending)}")
    if args.dry_run:
        for item in pending[:3]:
            print("=" * 80)
            print(item["item_id"])
            print(messages(item)[1]["content"][:1200])
        return

    model = config.get("translation", {}).get("model", config["judge"]["model"])
    max_tokens = int(config.get("translation", {}).get("max_output_tokens", 700))
    temperature = float(config.get("translation", {}).get("temperature", 0))
    client = OpenAI(api_key=Path(args.api_key_file).read_text(encoding="utf-8").strip())
    for index, item in enumerate(pending, start=1):
        started = time.time()
        raw = ""
        usage: dict[str, Any] = {}
        parsed = None
        parse_error = None
        api_error = None
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages(item),
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
            parsed, parse_error = parse_translation(raw)
        except Exception as exc:  # noqa: BLE001 - preserve API failure details in cache.
            api_error = repr(exc)
        parsed = parsed or {}
        input_tokens = int(usage.get("prompt_tokens", 0) or 0)
        output_tokens = int(usage.get("completion_tokens", 0) or 0)
        record = {
            "item_id": item["item_id"],
            "language": item["language"],
            "translation_model": model,
            "raw_response": raw,
            "english_source_text": parsed.get("english_source_text"),
            "english_translation": parsed.get("english_translation"),
            "english_reference": parsed.get("english_reference"),
            "parse_success": all(parsed.get(k) for k in ["english_source_text", "english_translation", "english_reference"]),
            "parse_error": parse_error,
            "api_error": api_error,
            "usage": usage,
            "api_cost_estimate_usd": approximate_cost(model, input_tokens, output_tokens),
            "elapsed_seconds": round(time.time() - started, 3),
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        }
        append_jsonl(output_path, record)
        status = "ok" if record["parse_success"] and not api_error else "fail"
        print(f"[{index}/{len(pending)}] {status} {item['item_id']} cost={record['api_cost_estimate_usd']}")


if __name__ == "__main__":
    main()
