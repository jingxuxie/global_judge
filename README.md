# GlobalJudge Protocols

Fast experimental scaffold for `globaljudge_protocol_paper_plan.md`.

The current results cover SEAHORSE candidate-visible quality dimensions,
source-grounded XLSum `main_ideas` examples recovered by matching SEAHORSE
reference summaries to raw XLSum source records, and a small WMT MQM
translation-quality contrast:

- languages: `en-US`, `es-ES`, `tr`, `vi`
- candidate-quality dimensions: `comprehensibility`, `grammar`
- source-grounded dimension: `main_ideas` for `es-ES`, `tr`, `vi`
- WMT language pairs: `en-de`, `en-ru`, `zh-en`
- protocols: direct English rubric, target-language rubric, bilingual rubric,
  and an explicit English-pivot protocol with cached translations; the WMT
  extension uses direct and explicit-pivot for all pairs, and target-language
  plus bilingual rubrics for non-English target pairs, in both reference-based
  and reference-free MT judging modes
- judges: `gpt-4o-mini` for the main runs, plus a stratified n=25 candidate-quality `gpt-4.1-mini` audit and a targeted WMT reference-free `gpt-4.1-mini` audit

The first diagnostic run used an in-prompt pivot, but the cleaner current result
uses cached explicit translations. The source-grounded run uses local raw XLSum
archives and does not execute remote dataset code.
The WMT contrast uses the compact Hugging Face dataset
`RicardoRei/wmt-mqm-human-evaluation`; the official Google Research
`mt-metrics-eval` archive was inspected but not required for the runnable
pipeline because the full tarball is large.

## Setup

```bash
/home/eston/anaconda3/envs/global_judge/bin/python -m pip install -r requirements.txt
```

OpenAI API calls read from `apikey.txt` by default; that file is ignored by
Git. The pushed repository tracks processed paper-facing artifacts, prompts,
responses, analysis outputs, and manuscripts, but excludes `data/raw/` because
the raw dataset cache is large and can be recreated with the preparation
scripts.

## Reproduce the small pilot

```bash
/home/eston/anaconda3/envs/global_judge/bin/python src/prepare_seahorse.py \
  --config configs/pilot_seahorse.yaml

/home/eston/anaconda3/envs/global_judge/bin/python src/build_prompts.py \
  --config configs/pilot_seahorse.yaml

/home/eston/anaconda3/envs/global_judge/bin/python src/run_openai_judges.py \
  --config configs/pilot_seahorse.yaml \
  --api-key-file apikey.txt

/home/eston/anaconda3/envs/global_judge/bin/python src/analyze_results.py \
  --config configs/pilot_seahorse.yaml
```

Use `--dry-run` on `run_openai_judges.py` to inspect prompts and token estimates
without spending API budget.

## Reproduce the historical n=20 explicit-pivot pilot

```bash
/home/eston/anaconda3/envs/global_judge/bin/python src/prepare_seahorse.py \
  --config configs/pilot_seahorse_20.yaml

/home/eston/anaconda3/envs/global_judge/bin/python src/build_prompts.py \
  --config configs/pilot_seahorse_20.yaml

/home/eston/anaconda3/envs/global_judge/bin/python src/run_openai_judges.py \
  --config configs/pilot_seahorse_20.yaml \
  --api-key-file apikey.txt

/home/eston/anaconda3/envs/global_judge/bin/python src/run_openai_translations.py \
  --config configs/pilot_seahorse_20_explicit_pivot.yaml \
  --api-key-file apikey.txt

/home/eston/anaconda3/envs/global_judge/bin/python src/build_prompts.py \
  --config configs/pilot_seahorse_20_explicit_pivot.yaml

/home/eston/anaconda3/envs/global_judge/bin/python src/run_openai_judges.py \
  --config configs/pilot_seahorse_20_explicit_pivot.yaml \
  --api-key-file apikey.txt

/home/eston/anaconda3/envs/global_judge/bin/python src/combine_explicit_pivot.py

/home/eston/anaconda3/envs/global_judge/bin/python src/analyze_results.py \
  --config configs/pilot_seahorse_20_combined_explicit.yaml
```

## Reproduce the current n=50 candidate-quality result

```bash
/home/eston/anaconda3/envs/global_judge/bin/python src/prepare_seahorse.py \
  --config configs/candidate_quality_n50.yaml

/home/eston/anaconda3/envs/global_judge/bin/python src/build_prompts.py \
  --config configs/candidate_quality_n50.yaml

/home/eston/anaconda3/envs/global_judge/bin/python src/run_openai_judges.py \
  --config configs/candidate_quality_n50.yaml \
  --api-key-file apikey.txt

/home/eston/anaconda3/envs/global_judge/bin/python src/run_openai_translations.py \
  --config configs/candidate_quality_n50_explicit_pivot.yaml \
  --api-key-file apikey.txt

/home/eston/anaconda3/envs/global_judge/bin/python src/build_prompts.py \
  --config configs/candidate_quality_n50_explicit_pivot.yaml

/home/eston/anaconda3/envs/global_judge/bin/python src/run_openai_judges.py \
  --config configs/candidate_quality_n50_explicit_pivot.yaml \
  --api-key-file apikey.txt

/home/eston/anaconda3/envs/global_judge/bin/python src/combine_explicit_pivot.py \
  --base-config configs/candidate_quality_n50.yaml \
  --pivot-config configs/candidate_quality_n50_explicit_pivot.yaml \
  --out-config configs/candidate_quality_n50_combined_explicit.yaml

/home/eston/anaconda3/envs/global_judge/bin/python src/analyze_results.py \
  --config configs/candidate_quality_n50_combined_explicit.yaml

/home/eston/anaconda3/envs/global_judge/bin/python src/calibrate_thresholds.py \
  --config configs/candidate_quality_n50_combined_explicit.yaml

/home/eston/anaconda3/envs/global_judge/bin/python src/compare_protocols.py \
  --config configs/candidate_quality_n50_combined_explicit.yaml
```

The current paper-facing status note is
`data/analysis/current_research_status.md`.

Regenerate the aggregate protocol-instability summary with:

```bash
/home/eston/anaconda3/envs/global_judge/bin/python src/summarize_protocol_instability.py
```

Regenerate qualitative protocol examples with:

```bash
/home/eston/anaconda3/envs/global_judge/bin/python src/extract_qualitative_examples.py
```

Regenerate the prompt/protocol inventory with redacted representative prompts:

```bash
/home/eston/anaconda3/envs/global_judge/bin/python src/summarize_prompt_inventory.py
```

Regenerate the dataset/sampling audit with item counts and label balance:

```bash
/home/eston/anaconda3/envs/global_judge/bin/python src/summarize_dataset_sampling.py
```

Regenerate the claim-to-evidence matrix:

```bash
/home/eston/anaconda3/envs/global_judge/bin/python src/build_claim_evidence_matrix.py
```

Regenerate the research-question/contribution coverage matrix:

```bash
/home/eston/anaconda3/envs/global_judge/bin/python src/build_rq_contribution_matrix.py
```

Regenerate the calibration learning curve with:

```bash
/home/eston/anaconda3/envs/global_judge/bin/python src/summarize_calibration_learning_curve.py
```

Regenerate the score-threshold diagnostic with:

```bash
/home/eston/anaconda3/envs/global_judge/bin/python src/summarize_score_threshold_diagnostic.py
```

Regenerate the run inventory, parse-rate summary, cost estimates, and token-usage counts with:

```bash
/home/eston/anaconda3/envs/global_judge/bin/python src/summarize_run_inventory.py
```

Regenerate the repeatability-control summary with:

```bash
/home/eston/anaconda3/envs/global_judge/bin/python src/summarize_repeatability_control.py
```

Regenerate the paper-facing results brief with:

```bash
/home/eston/anaconda3/envs/global_judge/bin/python src/make_results_brief.py
```

The generated brief is `paper/results_brief.md`.

Regenerate the reviewer/submission packet with:

```bash
/home/eston/anaconda3/envs/global_judge/bin/python src/build_submission_packet.py
```

Regenerate the benchmark data card with:

```bash
/home/eston/anaconda3/envs/global_judge/bin/python src/build_benchmark_datacard.py
```

Regenerate LaTeX-ready result tables with:

```bash
/home/eston/anaconda3/envs/global_judge/bin/python src/export_paper_tables.py
```

Regenerate the reproducibility manifest with file hashes and record counts:

```bash
/home/eston/anaconda3/envs/global_judge/bin/python src/build_reproducibility_manifest.py
```

Validate the paper-facing claim package with:

```bash
/home/eston/anaconda3/envs/global_judge/bin/python src/validate_paper_claims.py
```

Run the full no-API release validation suite with:

```bash
/home/eston/anaconda3/envs/global_judge/bin/python src/run_release_checks.py
```

Paper-facing writing artifacts:

- `paper/globaljudge_short_paper_draft.md`
- `paper/extended_abstract.tex`
- `paper/extended_abstract.pdf`
- `paper/submission_packet.md`
- `paper/globaljudge_protocolbench_datacard.md`
- `paper/main.tex`
- `paper/main.pdf`
- `paper/reporting_card.md`
- `paper/references.bib`
- `paper/tables/*.tex`
- `data/analysis/release_validation_report.{json,md}`
- `data/analysis/completion_audit.{json,md}`
- `data/analysis/claim_evidence_matrix.{csv,md}`
- `data/analysis/rq_contribution_matrix.{csv,md}`
- `data/analysis/reproducibility_manifest.{json,md}`

Compile the LaTeX manuscript with:

```bash
make -C paper
```

## Reproduce the current source-grounded semantic result

```bash
/home/eston/anaconda3/envs/global_judge/bin/python src/prepare_xlsum_semantic.py \
  --config configs/semantic_xlsum_n30.yaml

/home/eston/anaconda3/envs/global_judge/bin/python src/run_openai_translations.py \
  --config configs/semantic_xlsum_n30.yaml \
  --api-key-file apikey.txt

/home/eston/anaconda3/envs/global_judge/bin/python src/build_prompts.py \
  --config configs/semantic_xlsum_n30.yaml

/home/eston/anaconda3/envs/global_judge/bin/python src/run_openai_judges.py \
  --config configs/semantic_xlsum_n30.yaml \
  --api-key-file apikey.txt

/home/eston/anaconda3/envs/global_judge/bin/python src/analyze_results.py \
  --config configs/semantic_xlsum_n30.yaml

/home/eston/anaconda3/envs/global_judge/bin/python src/calibrate_thresholds.py \
  --config configs/semantic_xlsum_n30.yaml

/home/eston/anaconda3/envs/global_judge/bin/python src/compare_protocols.py \
  --config configs/semantic_xlsum_n30.yaml
```

## Reproduce the n=25 stronger-judge audit

```bash
/home/eston/anaconda3/envs/global_judge/bin/python src/prepare_seahorse.py \
  --config configs/audit_gpt41mini_n25.yaml

/home/eston/anaconda3/envs/global_judge/bin/python src/build_prompts.py \
  --config configs/audit_gpt41mini_n25.yaml

/home/eston/anaconda3/envs/global_judge/bin/python src/run_openai_judges.py \
  --config configs/audit_gpt41mini_n25.yaml \
  --api-key-file apikey.txt

/home/eston/anaconda3/envs/global_judge/bin/python src/run_openai_translations.py \
  --config configs/audit_gpt41mini_n25_explicit_pivot.yaml \
  --api-key-file apikey.txt

/home/eston/anaconda3/envs/global_judge/bin/python src/build_prompts.py \
  --config configs/audit_gpt41mini_n25_explicit_pivot.yaml

/home/eston/anaconda3/envs/global_judge/bin/python src/run_openai_judges.py \
  --config configs/audit_gpt41mini_n25_explicit_pivot.yaml \
  --api-key-file apikey.txt

/home/eston/anaconda3/envs/global_judge/bin/python src/combine_explicit_pivot.py \
  --base-config configs/audit_gpt41mini_n25.yaml \
  --pivot-config configs/audit_gpt41mini_n25_explicit_pivot.yaml \
  --out-config configs/audit_gpt41mini_n25_combined_explicit.yaml

/home/eston/anaconda3/envs/global_judge/bin/python src/analyze_results.py \
  --config configs/audit_gpt41mini_n25_combined_explicit.yaml

/home/eston/anaconda3/envs/global_judge/bin/python src/calibrate_thresholds.py \
  --config configs/audit_gpt41mini_n25_combined_explicit.yaml

/home/eston/anaconda3/envs/global_judge/bin/python src/compare_protocols.py \
  --config configs/audit_gpt41mini_n25_combined_explicit.yaml
```

## Reproduce the WMT MQM contrast result

```bash
/home/eston/anaconda3/envs/global_judge/bin/python src/prepare_wmt_mqm.py \
  --config configs/wmt_mqm_n30.yaml

/home/eston/anaconda3/envs/global_judge/bin/python src/run_wmt_translations.py \
  --config configs/wmt_mqm_n30.yaml \
  --api-key-file apikey.txt

/home/eston/anaconda3/envs/global_judge/bin/python src/build_wmt_prompts.py \
  --config configs/wmt_mqm_n30.yaml

/home/eston/anaconda3/envs/global_judge/bin/python src/run_openai_judges.py \
  --config configs/wmt_mqm_n30.yaml \
  --api-key-file apikey.txt

/home/eston/anaconda3/envs/global_judge/bin/python src/analyze_results.py \
  --config configs/wmt_mqm_n30.yaml

/home/eston/anaconda3/envs/global_judge/bin/python src/calibrate_thresholds.py \
  --config configs/wmt_mqm_n30.yaml

/home/eston/anaconda3/envs/global_judge/bin/python src/compare_protocols.py \
  --config configs/wmt_mqm_n30.yaml
```

The reference-free WMT condition reuses the same sampled items and translation
cache, but judges source + candidate without the reference:

```bash
/home/eston/anaconda3/envs/global_judge/bin/python src/build_wmt_prompts.py \
  --config configs/wmt_mqm_ref_free_n30.yaml

/home/eston/anaconda3/envs/global_judge/bin/python src/run_openai_judges.py \
  --config configs/wmt_mqm_ref_free_n30.yaml \
  --api-key-file apikey.txt

/home/eston/anaconda3/envs/global_judge/bin/python src/analyze_results.py \
  --config configs/wmt_mqm_ref_free_n30.yaml

/home/eston/anaconda3/envs/global_judge/bin/python src/calibrate_thresholds.py \
  --config configs/wmt_mqm_ref_free_n30.yaml

/home/eston/anaconda3/envs/global_judge/bin/python src/compare_protocols.py \
  --config configs/wmt_mqm_ref_free_n30.yaml
```

The targeted stronger-judge WMT audit reruns only the key reference-free cells:
`zh-en` direct versus pivot and `en-de` pivot versus bilingual.

```bash
for cfg in \
  configs/wmt_mqm_ref_free_audit_zh_en_gpt41mini.yaml \
  configs/wmt_mqm_ref_free_audit_en_de_gpt41mini.yaml
do
  /home/eston/anaconda3/envs/global_judge/bin/python src/build_wmt_prompts.py \
    --config "$cfg"

  /home/eston/anaconda3/envs/global_judge/bin/python src/run_openai_judges.py \
    --config "$cfg" \
    --api-key-file apikey.txt

  /home/eston/anaconda3/envs/global_judge/bin/python src/analyze_results.py \
    --config "$cfg"

  /home/eston/anaconda3/envs/global_judge/bin/python src/calibrate_thresholds.py \
    --config "$cfg"

  /home/eston/anaconda3/envs/global_judge/bin/python src/compare_protocols.py \
    --config "$cfg"
done
```
