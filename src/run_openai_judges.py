from __future__ import annotations

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from openai import OpenAI

from globaljudge_common import (
    APPROX_OPENAI_PRICES_PER_MILLION,
    append_jsonl,
    label_from_score,
    load_config,
    read_jsonl,
)


def parse_json_object(raw: str) -> tuple[dict[str, Any] | None, str | None]:
    text = raw.strip()
    if text.startswith("```"):
        lines = [line for line in text.splitlines() if not line.strip().startswith("```")]
        text = "\n".join(lines).strip()
    try:
        value = json.loads(text)
        if isinstance(value, dict):
            return value, None
        return None, "json_not_object"
    except json.JSONDecodeError as exc:
        start = text.find("{")
        end = text.rfind("}")
        if start >= 0 and end > start:
            try:
                value = json.loads(text[start : end + 1])
                if isinstance(value, dict):
                    return value, "repaired_substring"
            except json.JSONDecodeError:
                pass
        return None, f"json_error:{exc.msg}"


def normalize_score(value: Any) -> int | None:
    try:
        score = int(round(float(value)))
    except (TypeError, ValueError):
        return None
    if 1 <= score <= 5:
        return score
    return None


def normalize_confidence(value: Any) -> float | None:
    try:
        confidence = float(value)
    except (TypeError, ValueError):
        return None
    if 0 <= confidence <= 1:
        return confidence
    return None


def approximate_cost(model: str, input_tokens: int, output_tokens: int) -> float | None:
    prices = APPROX_OPENAI_PRICES_PER_MILLION.get(model)
    if not prices:
        return None
    return (input_tokens / 1_000_000) * prices["input"] + (output_tokens / 1_000_000) * prices["output"]


def existing_prompt_ids(path: Path) -> set[str]:
    if not path.exists():
        return set()
    return {row["prompt_id"] for row in read_jsonl(path) if "prompt_id" in row}


def prompt_preview(prompts: list[dict], limit: int) -> None:
    for prompt in prompts[:limit]:
        user = next(message["content"] for message in prompt["messages"] if message["role"] == "user")
        print("=" * 80)
        print(prompt["prompt_id"])
        print(user[:1200])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/pilot_seahorse.yaml")
    parser.add_argument("--api-key-file", default="apikey.txt")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--preview", type=int, default=3)
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    config = load_config(args.config)
    prompts = read_jsonl(config["paths"]["prompts_jsonl"])
    response_path = Path(config["paths"]["responses_jsonl"])
    done = existing_prompt_ids(response_path)
    pending = [prompt for prompt in prompts if prompt["prompt_id"] not in done]

    request_limit = args.limit if args.limit is not None else int(config["judge"].get("request_limit", len(pending)))
    pending = pending[:request_limit]
    print(f"Prompts total={len(prompts)} done={len(done)} pending_this_run={len(pending)}")

    if args.dry_run:
        prompt_preview(pending, args.preview)
        return

    api_key = Path(args.api_key_file).read_text(encoding="utf-8").strip()
    if not api_key:
        raise ValueError(f"API key file is empty: {args.api_key_file}")
    client = OpenAI(api_key=api_key)
    model = config["judge"]["model"]

    for index, prompt in enumerate(pending, start=1):
        started = time.time()
        parse_error = None
        parsed = None
        score = None
        confidence = None
        raw = ""
        usage = {}
        error = None
        try:
            response = client.chat.completions.create(
                model=model,
                messages=prompt["messages"],
                temperature=float(config["judge"].get("temperature", 0)),
                max_tokens=int(config["judge"].get("max_output_tokens", 120)),
                response_format={"type": "json_object"},
            )
            raw = response.choices[0].message.content or ""
            usage = {
                "prompt_tokens": getattr(response.usage, "prompt_tokens", 0) if response.usage else 0,
                "completion_tokens": getattr(response.usage, "completion_tokens", 0) if response.usage else 0,
                "total_tokens": getattr(response.usage, "total_tokens", 0) if response.usage else 0,
            }
            parsed, parse_error = parse_json_object(raw)
            if parsed:
                score = normalize_score(parsed.get("score"))
                confidence = normalize_confidence(parsed.get("confidence"))
                if not parsed.get("label") and score is not None:
                    parsed["label"] = label_from_score(score)
        except Exception as exc:  # noqa: BLE001 - preserve API failure details in cache.
            error = repr(exc)

        input_tokens = int(usage.get("prompt_tokens", 0) or 0)
        output_tokens = int(usage.get("completion_tokens", 0) or 0)
        record = {
            "prompt_id": prompt["prompt_id"],
            "item_id": prompt["item_id"],
            "language": prompt["language"],
            "dimension": prompt["dimension"],
            "protocol": prompt["protocol"],
            "judge_model": model,
            "raw_response": raw,
            "parsed_response": parsed,
            "score": score,
            "label": parsed.get("label") if parsed else None,
            "confidence": confidence,
            "parse_success": parsed is not None and score is not None,
            "parse_error": parse_error,
            "api_error": error,
            "usage": usage,
            "api_cost_estimate_usd": approximate_cost(model, input_tokens, output_tokens),
            "elapsed_seconds": round(time.time() - started, 3),
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        }
        append_jsonl(response_path, record)
        status = "ok" if record["parse_success"] and not error else "fail"
        print(f"[{index}/{len(pending)}] {status} {prompt['prompt_id']} cost={record['api_cost_estimate_usd']}")


if __name__ == "__main__":
    main()
