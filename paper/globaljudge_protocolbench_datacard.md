# GlobalJudge-ProtocolBench Data Card

This data card documents the compact benchmark package used by the GlobalJudge protocol-sensitivity paper artifacts.

## Purpose

GlobalJudge-ProtocolBench is designed to test whether multilingual LLM-as-a-judge conclusions change when the judge sees different protocol surfaces: original-language text with English instructions, target-language rubric wording, explicit English-pivot translations, or bilingual instructions.

The benchmark is intended for protocol auditing and reporting practice. It is not intended to rank languages, to declare a universal best judge prompt, or to replace native-speaker evaluation.

## Composition Snapshot

- Main paper-facing base items: 580.
- Total audited item rows including stronger-judge subsets: 840.
- Prompt surfaces: P0_direct_english, P1_target_rubric, P2_explicit_pivot, P3_bilingual.
- Judge models represented in paper-facing runs: gpt-4.1-mini, gpt-4o-mini.
- Paper-facing judge calls: 3480; total prompts in prompt inventory: 3480.
- Minimum parse rate across paper-facing runs: 100.0%.
- Returned total tokens: 1284667; observed local cost estimate: $0.39.

## Item Sets

| Run | Items | Langs | Dims | Pos/Neg | Source Rate | Reference Rate |
| --- | --- | --- | --- | --- | --- | --- |
| candidate n50 | 400 | 4 | 2 | 200/200 | 0.0% | 0.0% |
| candidate experiment n25 | 200 | 4 | 2 | 96/104 | 0.0% | 0.0% |
| semantic n30 | 90 | 3 | 1 | 45/45 | 100.0% | 100.0% |
| wmt n30 shared items | 90 | 3 | 1 | 45/45 | 100.0% | 100.0% |
| wmt ref-free experiment zh-en | 30 | 1 | 1 | 15/15 | 100.0% | 100.0% |
| wmt ref-free experiment en-de | 30 | 1 | 1 | 15/15 | 100.0% | 100.0% |

## Prompt and Judge Inventory

| Run | Prompts | Protocols | Languages | Dimensions | Judge |
| --- | --- | --- | --- | --- | --- |
| candidate n50 | 1600 | 4 | en-US, es-ES, tr, vi | comprehensibility, grammar | gpt-4o-mini |
| candidate experiment n25 | 800 | 4 | en-US, es-ES, tr, vi | comprehensibility, grammar | gpt-4.1-mini |
| semantic n30 | 360 | 4 | es-ES, tr, vi | main_ideas | gpt-4o-mini |
| wmt reference n30 | 300 | 4 | en-de, en-ru, zh-en | translation_quality | gpt-4o-mini |
| wmt ref-free n30 | 300 | 4 | en-de, en-ru, zh-en | translation_quality_ref_free | gpt-4o-mini |
| wmt ref-free experiment | 120 | 3 | en-de, zh-en | translation_quality_ref_free | gpt-4.1-mini |

## Run and Cost Inventory

| Run | Base Items | Judge Calls | Parse | Tokens | Cost |
| --- | --- | --- | --- | --- | --- |
| candidate n50 | 400 | 1600 | 100.0% | 472666 | $0.11 |
| candidate experiment n25 | 200 | 800 | 100.0% | 246539 | $0.14 |
| semantic n30 | 90 | 360 | 100.0% | 299183 | $0.07 |
| wmt reference n30 | 90 | 300 | 100.0% | 130395 | $0.03 |
| wmt ref-free n30 | 90 | 300 | 100.0% | 97576 | $0.02 |
| wmt ref-free experiment | 60 | 120 | 100.0% | 38308 | $0.02 |

## Labels and Sampling

- SEAHORSE candidate-quality labels are binary human yes/no labels for dimensions such as comprehensibility and grammar.
- Source-grounded semantic examples are balanced `main_ideas` examples recovered by matching SEAHORSE reference summaries to raw XLSum records.
- WMT examples use MQM-derived high/low labels from within-language-pair score quantiles; these are protocol stress-test labels, not new human annotations.
- Main sampled cells are balanced by construction; the candidate experiment uses 12 positive and 13 negative examples per language/dimension cell.

## Protocols

- `P0_direct_english`: original text with English rubric/instructions.
- `P1_target_rubric`: original text with target-language rubric wording.
- `P2_explicit_pivot`: English translations of the judged content, then English judging.
- `P3_bilingual`: original text with English plus target-language rubric wording.

## Intended Uses

- Test whether multilingual LLM judge conclusions are sensitive to protocol choices.
- Report per-language and per-protocol alignment instead of a single aggregate judge score.
- Stress-test English-pivot judging, especially for target-language form dimensions.
- Teach or reproduce a compact reporting-card workflow with parse rate, token usage, and cost.

## Out-of-Scope Uses

- Ranking languages by model capability.
- Claiming a universal best protocol across all multilingual evaluation tasks.
- Treating target-language rubric translations as native-speaker validated.
- Treating WMT reference-free labels as a new human annotation target.
- Estimating current provider pricing without refreshing price tables.

## Coverage Against Project Plan

RQ1: judge reliability changes by language: covered; RQ2: evaluation protocol changes the result: covered; RQ3: protocol effects differ by quality dimension/task: covered with contrast evidence; RQ4: small human calibration set: covered as diagnostic

## Known Limitations

- Main judge calls use OpenAI models; stronger experiments use another OpenAI model rather than an independent model family.
- The benchmark is compact and optimized for fast iteration, not broad task/language coverage.
- Target-language rubric wording is pragmatic and should be native-checked before stronger claims about target-language prompting.
- English-pivot translations are produced by the same model family as the judge, which mirrors many practical workflows but should be disclosed.
- Approximate costs are local returned-usage estimates; token usage is the stable accounting quantity.

## Reproducibility Pointers

- Reproducibility manifest: `data/analysis/reproducibility_manifest.{json,md}`.
- Prompt inventory with redacted representatives: `data/analysis/prompt_inventory.md`.
- Sampling summary: `data/analysis/dataset_sampling_audit.md`.
- Claim evidence matrix: `data/analysis/claim_evidence_matrix.md`.
- Release validation report: `data/analysis/release_validation_report.md`.
