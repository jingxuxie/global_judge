from __future__ import annotations

import argparse

from globaljudge_common import load_config, read_jsonl, write_jsonl


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-config", default="configs/pilot_seahorse_20.yaml")
    parser.add_argument("--pivot-config", default="configs/pilot_seahorse_20_explicit_pivot.yaml")
    parser.add_argument("--out-config", default="configs/pilot_seahorse_20_combined_explicit.yaml")
    args = parser.parse_args()

    base = load_config(args.base_config)
    pivot = load_config(args.pivot_config)
    out = load_config(args.out_config)

    base_prompts = [row for row in read_jsonl(base["paths"]["prompts_jsonl"]) if row["protocol"] != "P2_pivot_in_prompt"]
    base_responses = [row for row in read_jsonl(base["paths"]["responses_jsonl"]) if row["protocol"] != "P2_pivot_in_prompt"]
    pivot_prompts = read_jsonl(pivot["paths"]["prompts_jsonl"])
    pivot_responses = read_jsonl(pivot["paths"]["responses_jsonl"])

    write_jsonl(out["paths"]["prompts_jsonl"], base_prompts + pivot_prompts)
    write_jsonl(out["paths"]["responses_jsonl"], base_responses + pivot_responses)
    print(f"Wrote {len(base_prompts) + len(pivot_prompts)} prompts to {out['paths']['prompts_jsonl']}")
    print(f"Wrote {len(base_responses) + len(pivot_responses)} responses to {out['paths']['responses_jsonl']}")


if __name__ == "__main__":
    main()
