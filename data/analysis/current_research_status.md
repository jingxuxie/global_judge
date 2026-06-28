# Current Research Status

Date: 2026-06-28

## Main completed result: SEAHORSE candidate-quality n=50

Dataset: SEAHORSE test split.

Scope:
- 4 languages: `en-US`, `es-ES`, `tr`, `vi`
- 2 candidate-only dimensions: `comprehensibility`, `grammar`
- 50 balanced examples per language/dimension, with 25 positive and 25 negative human labels
- 400 base items
- 4 protocols: direct English rubric, target-language rubric, explicit English pivot, bilingual rubric
- judge model: `gpt-4o-mini`

Artifacts:
- Items: `data/processed/candidate_n50_items.jsonl`
- Base prompts/responses: `data/prompts/candidate_n50_base_prompts.jsonl`, `data/responses/candidate_n50_base_responses.jsonl`
- Explicit-pivot translations: `data/processed/candidate_n50_english_translations.jsonl`
- Explicit-pivot prompts/responses: `data/prompts/candidate_n50_explicit_pivot_prompts.jsonl`, `data/responses/candidate_n50_explicit_pivot_responses.jsonl`
- Combined responses: `data/responses/candidate_n50_combined_explicit_responses.jsonl`
- Metrics: `data/analysis/candidate_n50_combined_explicit_metrics.csv`
- Protocol shifts: `data/analysis/candidate_n50_combined_explicit_protocol_shifts.csv`
- Paired bootstrap comparisons: `data/analysis/candidate_n50_combined_explicit_metrics_pairwise_bootstrap.csv`
- Language gaps: `data/analysis/candidate_n50_combined_explicit_metrics_language_gaps.csv`
- Summaries: `data/analysis/candidate_n50_combined_explicit_summary.md`, `data/analysis/candidate_n50_combined_explicit_metrics_protocol_comparison_summary.md`
- Calibration: `data/analysis/candidate_n50_combined_explicit_calibration.csv`, `data/analysis/candidate_n50_combined_explicit_calibration_summary.md`
- Figures: `paper/figures/candidate_n50_combined_explicit_heatmap.png`, `paper/figures/candidate_n50_combined_explicit_shifts.png`

Approximate incremental API spend for the n=50 run:
- Base judge calls: `$0.0739`
- Explicit-pivot translations: `$0.0134`
- Explicit-pivot judge calls: `$0.0240`
- Incremental n=50 total: about `$0.1114`

The selected paper-facing components cost about `$0.3927` in returned usage estimates: `$0.1114` for the n=50 candidate-quality run, `$0.1431` for the n=25 audit, `$0.0659` for the source-grounded semantic n=30 run, `$0.0295` for the WMT MQM reference-based extension, `$0.0206` for the WMT MQM reference-free extension, and `$0.0221` for the targeted WMT reference-free stronger-judge audit. Including earlier pilots, observed non-duplicated API spend remains about `$0.60`. The combined response files duplicate costs from their component files and should not be counted again.

## Main n=50 signal

This is now strong enough to write as a bounded empirical result, while still framing it as one judge model and one dataset family.

1. Protocol-induced score shifts are large on the same items.
   - `vi / grammar`: target-language rubric vs explicit English pivot mean absolute shift = `1.20` on a 1-5 scale; 82% of paired items changed score and 34% shifted by at least 2 points.
   - `tr / grammar`: target-language rubric vs explicit English pivot shift = `0.96`.
   - `en-US / grammar`: target-language rubric vs explicit English pivot shift = `0.94`.
   - `vi / comprehensibility`: direct English rubric vs explicit English pivot shift = `0.88`; target-language rubric vs explicit English pivot shift = `0.90`.

2. English-pivot judging is not a universal fix and can hurt human alignment.
   - `tr / comprehensibility`: direct English rubric Spearman `0.603`, AUROC `0.836`; explicit English pivot Spearman `0.331`, AUROC `0.686`.
   - Paired bootstrap for `tr / comprehensibility`, explicit pivot minus direct: AUROC delta `-0.1496`, 95% CI `[-0.2565, -0.0550]`; Spearman delta `-0.2719`, 95% CI `[-0.4650, -0.0970]`.
   - `vi / comprehensibility`: explicit pivot is weakest among protocols, with Spearman `0.086`, AUROC `0.548`. Bilingual rubric is better, with Spearman `0.399`, AUROC `0.714`.
   - Paired bootstrap for `vi / comprehensibility`, bilingual minus explicit pivot: AUROC delta `+0.1656`, 95% CI `[0.0088, 0.3168]`.

3. Grammar/form evaluation remains much weaker than comprehensibility.
   - `tr / grammar`: all protocols are near chance or worse by AUROC (`0.454` to `0.488`) and have negative Spearman correlations.
   - `vi / grammar`: explicit pivot AUROC is `0.509` and Spearman is `0.016`, despite a high mean score of `3.68`.
   - This supports the core caveat: translating into English can remove or smooth the target-language form evidence needed to judge grammar.

4. Bilingual rubric is not always best, but it reduces the largest language gap for comprehensibility.
   - Comprehensibility Spearman language gap by protocol:
     - explicit English pivot: `0.625`
     - target-language rubric: `0.535`
     - direct English rubric: `0.382`
     - bilingual rubric: `0.302`
   - This is a promising reporting-card result: protocol choice changes both absolute alignment and cross-language disparity.

5. Simple post-hoc threshold calibration is not yet a positive result.
   - Across 32 eligible test groups, mean test balanced-accuracy delta is `-0.017`, median `0.000`.
   - Some individual groups improve, but degradations are comparable. In the paper, calibration should be framed as an uncertainty/reporting analysis unless a stronger calibration method or larger split improves it.

## Stronger-judge audit: gpt-4.1-mini n=25

This is a bounded audit, not a replacement for the n=50 main run, but it is now large enough to use as the main stronger-judge robustness check.

Scope:
- Same 4 languages and 2 dimensions as the n=50 candidate-quality benchmark.
- 25 balanced examples per language/dimension, with 12 positive and 13 negative human labels.
- 200 base items and 800 judge responses across the same 4 protocols.
- Judge model: `gpt-4.1-mini`.
- Explicit-pivot translations used `gpt-4o-mini` to keep translation cost low.
- The translation cache has 200 unique successful translations. One pathological Turkish repetitive summary required a documented manual repair row after repeated `gpt-4o-mini` truncation; failed attempts remain in the JSONL cache for auditability.

Artifacts:
- Configs: `configs/audit_gpt41mini_n25.yaml`, `configs/audit_gpt41mini_n25_explicit_pivot.yaml`, `configs/audit_gpt41mini_n25_combined_explicit.yaml`
- Items: `data/processed/audit_gpt41mini_n25_items.jsonl`
- Translations: `data/processed/audit_gpt41mini_n25_english_translations.jsonl`
- Combined responses: `data/responses/audit_gpt41mini_n25_combined_explicit_responses.jsonl`
- Metrics: `data/analysis/audit_gpt41mini_n25_combined_explicit_metrics.csv`
- Protocol shifts: `data/analysis/audit_gpt41mini_n25_combined_explicit_protocol_shifts.csv`
- Paired bootstrap comparisons: `data/analysis/audit_gpt41mini_n25_combined_explicit_metrics_pairwise_bootstrap.csv`
- Language gaps: `data/analysis/audit_gpt41mini_n25_combined_explicit_metrics_language_gaps.csv`
- Summary: `data/analysis/audit_gpt41mini_n25_combined_explicit_summary.md`
- Comparison summary: `data/analysis/audit_gpt41mini_n25_combined_explicit_metrics_protocol_comparison_summary.md`
- Figures: `paper/figures/audit_gpt41mini_n25_combined_explicit_heatmap.png`, `paper/figures/audit_gpt41mini_n25_combined_explicit_shifts.png`

Approximate audit spend:
- Base audit judge calls: `$0.1024`
- Audit explicit-pivot translations: `$0.0081`
- Audit explicit-pivot judge calls: `$0.0326`
- Audit total: about `$0.1431`

Audit signal:

1. Protocol sensitivity survives the stronger judge.
   - `tr / comprehensibility`: explicit pivot vs bilingual mean absolute shift = `1.16`; direct English rubric vs explicit pivot = `1.04`; target-language rubric vs explicit pivot = `1.04`.
   - `vi / comprehensibility`: direct English rubric vs explicit pivot shift = `0.96`; explicit pivot vs bilingual = `0.96`.
   - `es-ES / grammar`: direct English rubric vs explicit pivot shift = `0.92`.

2. Explicit English pivot fails sharply even for the stronger audit judge.
   - `tr / comprehensibility`: direct English rubric Spearman `0.729`, AUROC `0.910`; explicit pivot Spearman `0.168`, AUROC `0.593`; bilingual rubric Spearman `0.796`, AUROC `0.946`.
   - Paired bootstrap for `tr / comprehensibility`, explicit pivot minus direct: AUROC delta `-0.317`, 95% CI `[-0.510, -0.150]`.
   - Paired bootstrap for `tr / comprehensibility`, bilingual minus explicit pivot: AUROC delta `+0.353`, 95% CI `[0.182, 0.544]`.
   - `vi / grammar`: direct English rubric Spearman `0.564`, AUROC `0.814`; explicit pivot Spearman `-0.052`, AUROC `0.471`; bilingual rubric Spearman `0.491`, AUROC `0.769`.
   - Paired bootstrap for `vi / grammar`, explicit pivot minus direct: AUROC delta `-0.343`, 95% CI `[-0.540, -0.175]`.
   - Paired bootstrap for `vi / grammar`, bilingual minus explicit pivot: AUROC delta `+0.298`, 95% CI `[0.125, 0.494]`.

3. Treat audit estimates cautiously but use them as stronger robustness evidence.
   - The n=25 cells are still smaller than the n=50 main run, but the failure mode is no longer just a tiny audit check.
   - The robust point is not that one prompt is globally optimal; it is that a stronger judge still shows large protocol-dependent score shifts and explicit-pivot failures.

4. Calibration remains negative in the audit.
   - Mean test balanced-accuracy delta is `-0.029`, median `-0.003`.
   - This reinforces that simple per-cell threshold tuning is not yet a positive contribution.

## Source-grounded semantic result: XLSum main-ideas n=30

SEAHORSE raw TSVs do not include source documents, so source-grounded `main_ideas` required matching SEAHORSE reference summaries back to raw XLSum summaries. The matching pipeline uses raw XLSum JSONL files and does not execute remote dataset code.

Recovered source matches:
- Spanish: 151/151 reference rows matched.
- Turkish: 243/244 reference rows matched.
- Vietnamese: 252/252 reference rows matched.

Scope:
- 3 languages: `es-ES`, `tr`, `vi`
- dimension: `main_ideas`
- 30 balanced examples per language, with 15 positive and 15 negative human labels
- 90 base items
- 4 protocols: direct English rubric, target-language rubric, explicit English pivot, bilingual rubric
- judge model: `gpt-4o-mini`
- source text excerpts truncated to 1400 characters

Artifacts:
- Config: `configs/semantic_xlsum_n30.yaml`
- Source-grounded items: `data/processed/semantic_xlsum_n30_items.jsonl`
- Source/candidate translations: `data/processed/semantic_xlsum_n30_english_translations.jsonl`
- Prompts: `data/prompts/semantic_xlsum_n30_prompts.jsonl`
- Responses: `data/responses/semantic_xlsum_n30_responses.jsonl`
- Metrics: `data/analysis/semantic_xlsum_n30_metrics.csv`
- Protocol shifts: `data/analysis/semantic_xlsum_n30_protocol_shifts.csv`
- Paired bootstrap comparisons: `data/analysis/semantic_xlsum_n30_metrics_pairwise_bootstrap.csv`
- Language gaps: `data/analysis/semantic_xlsum_n30_metrics_language_gaps.csv`
- Summaries: `data/analysis/semantic_xlsum_n30_summary.md`, `data/analysis/semantic_xlsum_n30_metrics_protocol_comparison_summary.md`
- Calibration: `data/analysis/semantic_xlsum_n30_calibration.csv`, `data/analysis/semantic_xlsum_n30_calibration_summary.md`
- Figures: `paper/figures/semantic_xlsum_n30_heatmap.png`, `paper/figures/semantic_xlsum_n30_shifts.png`

Approximate n=30 semantic spend:
- Source/candidate translation cache: `$0.0233`
- Judge calls: `$0.0426`
- Total: about `$0.0659`

Main semantic signal:

1. Source-grounded semantic judging shows smaller score shifts than grammar/form, but still meaningful protocol sensitivity.
   - Largest mean absolute shift is `vi / main_ideas`, target-language rubric vs explicit pivot = `0.70`.
   - `vi / main_ideas`, target-language rubric vs bilingual = `0.67`.
   - These are smaller than the 0.9-1.2 shifts seen for grammar/form in the n=50 candidate-quality result, supporting a dimension-dependent protocol-sensitivity story.

2. Explicit English pivot is not uniformly better for semantic `main_ideas`.
   - `es-ES / main_ideas`: explicit pivot is best, Spearman `0.514`, AUROC `0.771`.
   - `tr / main_ideas`: bilingual is best, Spearman `0.588`, AUROC `0.793`; explicit pivot is weaker, Spearman `0.339`, AUROC `0.669`.
   - `vi / main_ideas`: explicit pivot is worst, Spearman `0.000`, AUROC `0.500`; bilingual is best among weak protocols, Spearman `0.195`, AUROC `0.607`.

3. Paired bootstrap gives cautious but useful pairwise evidence.
   - `tr / main_ideas`, bilingual minus explicit pivot: AUROC delta `+0.124`, 95% CI `[0.000, 0.275]`.
   - `vi / main_ideas`, bilingual minus explicit pivot: AUROC delta `+0.107`, 95% CI `[0.013, 0.220]`.
   - `es-ES / main_ideas`, explicit pivot is stronger than bilingual by AUROC delta `+0.047`; the comparison summary reports bilingual minus explicit pivot as `-0.047`, 95% CI `[-0.119, 0.000]`.

4. Explicit pivot creates the largest language gap for source-grounded semantic judging.
   - Spearman language gap by protocol:
     - explicit English pivot: `0.514`
     - bilingual rubric: `0.393`
     - target-language rubric: `0.357`
     - direct English rubric: `0.345`
   - This reinforces the paper’s reporting-card angle: a single aggregate judge score hides cross-language disparity.

5. Calibration is positive for this source-grounded semantic run, unlike candidate-quality and audit runs.
   - Across 12 eligible groups, mean test balanced-accuracy delta is `+0.136`, median `+0.136`.
   - The main mechanism is that raw judge scores are compressed low for `main_ideas`, so a fixed threshold of 4 is poorly calibrated and a threshold of 2 often performs better.
   - This should be framed carefully: calibration is dimension- and score-distribution-dependent, not a universal fix.

## WMT MQM protocol extension: translation quality n=30

This is a small second-task-family contrast result. It uses WMT MQM human-evaluation rows from `RicardoRei/wmt-mqm-human-evaluation`, sampled from year 2022. It includes both reference-based judging (source + candidate + reference) and reference-free judging (source + candidate only). It started as a direct-vs-pivot contrast, then was extended with target-language and bilingual rubrics for non-English target pairs (`en-de`, `en-ru`). For `zh-en`, target-language and bilingual rubrics are intentionally skipped because the target language is English and the protocol would collapse back toward English instructions.

Scope:
- 3 language pairs: `en-de`, `en-ru`, `zh-en`
- dimensions: `translation_quality` and `translation_quality_ref_free`
- 30 balanced examples per language pair, with 15 high-quality and 15 low-quality human MQM-derived labels
- 90 base items
- 2 protocols for all pairs: direct English rubric and explicit English pivot
- 2 additional protocols for non-English target pairs: target-language rubric and bilingual rubric
- judge model: `gpt-4o-mini`

Artifacts:
- Config: `configs/wmt_mqm_n30.yaml`
- Preparation script: `src/prepare_wmt_mqm.py`
- Translation script: `src/run_wmt_translations.py`
- Prompt builder: `src/build_wmt_prompts.py`
- Items: `data/processed/wmt_mqm_n30_items.jsonl`
- Explicit-pivot translations: `data/processed/wmt_mqm_n30_english_translations.jsonl`
- Prompts: `data/prompts/wmt_mqm_n30_prompts.jsonl`
- Responses: `data/responses/wmt_mqm_n30_responses.jsonl`
- Metrics: `data/analysis/wmt_mqm_n30_metrics.csv`
- Reference-free metrics: `data/analysis/wmt_mqm_ref_free_n30_metrics.csv`
- Stronger-judge audit configs: `configs/wmt_mqm_ref_free_audit_zh_en_gpt41mini.yaml`, `configs/wmt_mqm_ref_free_audit_en_de_gpt41mini.yaml`
- Stronger-judge audit responses: `data/responses/wmt_mqm_ref_free_audit_zh_en_gpt41mini_responses.jsonl`, `data/responses/wmt_mqm_ref_free_audit_en_de_gpt41mini_responses.jsonl`
- Stronger-judge audit metrics: `data/analysis/wmt_mqm_ref_free_audit_zh_en_gpt41mini_metrics.csv`, `data/analysis/wmt_mqm_ref_free_audit_en_de_gpt41mini_metrics.csv`
- Stronger-judge audit paired comparisons: `data/analysis/wmt_mqm_ref_free_audit_zh_en_gpt41mini_metrics_pairwise_bootstrap.csv`, `data/analysis/wmt_mqm_ref_free_audit_en_de_gpt41mini_metrics_pairwise_bootstrap.csv`
- Protocol shifts: `data/analysis/wmt_mqm_n30_protocol_shifts.csv`
- Reference-free protocol shifts: `data/analysis/wmt_mqm_ref_free_n30_protocol_shifts.csv`
- Paired bootstrap comparisons: `data/analysis/wmt_mqm_n30_metrics_pairwise_bootstrap.csv`
- Reference-free paired bootstrap comparisons: `data/analysis/wmt_mqm_ref_free_n30_metrics_pairwise_bootstrap.csv`
- Language gaps: `data/analysis/wmt_mqm_n30_metrics_language_gaps.csv`
- Reference-free language gaps: `data/analysis/wmt_mqm_ref_free_n30_metrics_language_gaps.csv`
- Summaries: `data/analysis/wmt_mqm_n30_summary.md`, `data/analysis/wmt_mqm_n30_metrics_protocol_comparison_summary.md`
- Calibration: `data/analysis/wmt_mqm_n30_calibration.csv`, `data/analysis/wmt_mqm_n30_calibration_summary.md`
- Reference-free calibration: `data/analysis/wmt_mqm_ref_free_n30_calibration.csv`, `data/analysis/wmt_mqm_ref_free_n30_calibration_summary.md`
- Figures: `paper/figures/wmt_mqm_n30_heatmap.png`, `paper/figures/wmt_mqm_n30_shifts.png`
- Reference-free figures: `paper/figures/wmt_mqm_ref_free_n30_heatmap.png`, `paper/figures/wmt_mqm_ref_free_n30_shifts.png`

Approximate WMT spend:
- Explicit-pivot translation cache: `$0.0076`
- Reference-based judge calls: `$0.0219`
- Reference-free judge calls: `$0.0206`
- Targeted reference-free stronger-judge audit: `$0.0221`
- WMT total: about `$0.0723`

Main WMT signal:

1. Translation-quality judging has much smaller direct-vs-pivot shifts than target-language form evaluation.
   - `zh-en / translation_quality`: mean absolute shift = `0.53`, 43% disagreement, 6.7% shifts by at least 2 points.
   - `en-de / translation_quality`: mean absolute shift = `0.20`.
   - `en-ru / translation_quality`: mean absolute shift = `0.07`.

2. Direct and explicit-pivot alignment are similar in this reference-based MT setting.
   - `en-de`: direct Spearman/AUROC `0.388/0.673`; pivot `0.398/0.678`; pivot-direct AUROC delta `+0.004`, CI `[-0.127, 0.134]`.
   - `en-ru`: direct `0.165/0.573`; pivot `0.135/0.564`; delta `-0.009`, CI `[-0.093, 0.067]`.
   - `zh-en`: direct `0.354/0.693`; pivot `0.304/0.669`; delta `-0.024`, CI `[-0.227, 0.177]`.

3. Target-language and bilingual MT rubrics change alignment on non-English target pairs.
   - `en-de`: bilingual is best, Spearman/AUROC `0.471/0.689`; direct is `0.388/0.673`; target-language rubric is lower at `0.318/0.596`.
   - `en-ru`: target-language rubric is best, `0.320/0.649`; direct is `0.165/0.573`; bilingual remains weak at `0.159/0.576`.
   - Paired AUROC deltas are still small at n=30, but the best protocol differs by pair: bilingual for `en-de`, target-language for `en-ru`, direct for `zh-en`.

4. Reference-free MT judging surfaces stronger protocol effects than reference-based MT.
   - `zh-en / translation_quality_ref_free`: direct Spearman/AUROC `0.595/0.820`; explicit pivot `0.187/0.600`; pivot-direct AUROC delta `-0.220`, CI `[-0.440, -0.007]`.
   - `en-de / translation_quality_ref_free`: bilingual is best, `0.677/0.838`; bilingual minus pivot AUROC delta `+0.129`, CI `[0.025, 0.258]`.
   - `en-ru / translation_quality_ref_free`: target-language rubric is best by AUROC (`0.600`) and improves over direct by `+0.089`, CI `[0.009, 0.192]`; all `en-ru` correlations remain low.

5. The targeted `gpt-4.1-mini` WMT audit supports only a conservative WMT claim boundary.
   - `zh-en / translation_quality_ref_free`: direct `0.503/0.773`; explicit pivot `0.254/0.636`; pivot-direct AUROC delta `-0.138`, CI `[-0.346, 0.067]`. The direction persists, but n=30 significance does not.
   - `en-de / translation_quality_ref_free`: explicit pivot `0.563/0.784`; bilingual `0.503/0.760`; bilingual-pivot AUROC delta `-0.024`, CI `[-0.086, 0.016]`. The `gpt-4o-mini` bilingual advantage does not reproduce under the stronger judge.
   - Paper framing: WMT reference-free is evidence of protocol/model sensitivity and a stress test for reporting, not a stable global protocol ranking.

6. This should be framed as contrast and boundary evidence, not a main positive benchmark.
   - It supports a dimension-dependent story: pivot risk is large for target-language form and some summarization semantics, smaller for reference-based MT quality on this sample, and reappears for reference-free MT.
   - The WMT extension also reinforces the paper's reporting-card recommendation: even when pivot is not clearly harmful, non-English target rubrics can alter alignment, so protocol choice should still be reported.
   - The WMT run is intentionally small and covers one year, three language pairs, and only two additional protocols for the non-English target pairs. The stronger audit covers only two reference-free cells.

## Aggregate protocol-instability summary

This is a no-new-API synthesis over the current metrics and paired-bootstrap files. It is generated by `src/summarize_protocol_instability.py`.

Artifacts:
- Cell-level CSV: `data/analysis/protocol_instability_cells.csv`
- Run-level CSV: `data/analysis/protocol_instability_summary.csv`
- Markdown summary: `data/analysis/protocol_instability_summary.md`
- Paper table: `paper/tables/protocol_instability_summary.tex`

Main aggregate signal:
- Across 17 non-audit task/language cells, the best AUROC protocol is not direct in 11 cells.
- Explicit English pivot is the worst protocol in 10 of those 17 cells.
- 6 of the 17 non-audit cells have at least one paired AUROC delta with a bootstrap CI excluding zero.
- The candidate-quality `gpt-4.1-mini` audit is even more unstable: 7 of 8 cells have AUROC range at least 0.10 across protocols, and the maximum within-cell AUROC range is 0.353.
- This strengthens the reporting-card claim: protocol choice is an experimental factor that changes conclusions, not a prompt implementation detail.

## Calibration learning curve

This is a no-new-API RQ4 analysis over cached judge scores. It is generated by `src/summarize_calibration_learning_curve.py` with 50 repeated stratified samples per eligible group and calibration budgets of 1, 2, 4, 8, and 12 examples per class when enough items are available. The baseline threshold is score >= 4, matching the existing calibration summaries.

Artifacts:
- Raw repeated-sample results: `data/analysis/calibration_learning_curve_raw.csv`
- Run-level summary: `data/analysis/calibration_learning_curve_summary.csv`
- Markdown summary: `data/analysis/calibration_learning_curve_summary.md`
- Paper table: `paper/tables/calibration_learning_curve.tex`

Main calibration signal:
- Candidate-quality n=50 does not benefit reliably from threshold calibration. Mean held-out balanced-accuracy deltas remain slightly negative as calibration grows from 2 examples (`-0.054`) to 24 examples (`-0.009`), with median 0 at larger budgets.
- Source-grounded semantic `main_ideas` does benefit: mean deltas stay around `+0.12` to `+0.14`, with improvement probability above 0.61 at every tested budget.
- WMT reference-based judging is negative on average, while WMT reference-free judging improves on average as the calibration budget grows (`+0.076` at 24 calibration examples) but remains mixed by cell.
- Paper framing: calibration is useful as a diagnostic for score-threshold mismatch, especially when scores are compressed, but it is not a universal repair for protocol sensitivity.

## Score-threshold diagnostic

This is a no-new-API calibration-mechanism analysis over cached judge scores. It is generated by `src/summarize_score_threshold_diagnostic.py`.

Artifacts:
- Group-level CSV: `data/analysis/score_threshold_diagnostic_groups.csv`
- Run-level CSV: `data/analysis/score_threshold_diagnostic_summary.csv`
- Markdown summary: `data/analysis/score_threshold_diagnostic.md`
- Paper table: `paper/tables/score_threshold_diagnostic.tex`

Main threshold signal:
- Source-grounded semantic `main_ideas` scores are compressed low. Across 12 groups, human-positive examples average score `2.23`, human-negative examples average `1.76`, and the fixed score >= 4 threshold marks only `8.3%` of balanced examples as good. The modal best in-group threshold is `2`.
- WMT reference-free scores are compressed high. Across 10 groups, human-positive examples average `4.70`, human-negative examples average `4.19`, and score >= 4 marks `90.0%` of balanced examples as good. The modal best in-group threshold is `5`.
- Paper framing: this gives the mechanism behind the calibration learning curve. Calibration helps source-grounded semantics by lowering an overly strict cutoff, is mixed for WMT reference-free because scores are inflated, and is not a universal repair for protocol sensitivity.

## Run inventory and cost-per-call reporting

This is a no-new-API reporting-card artifact generated by `src/summarize_run_inventory.py`.

Artifacts:
- CSV: `data/analysis/run_inventory.csv`
- Markdown: `data/analysis/run_inventory.md`
- Paper table: `paper/tables/run_inventory.tex`
- API usage paper table: `paper/tables/api_usage_inventory.tex`

Main inventory signal:
- All selected paper-facing runs have 100% parse rate.
- Candidate n=50: 400 base items, 1,600 judge calls, `$0.1114` incremental cost, about `$0.070` per 1,000 judge calls.
- Candidate n=50 price-independent usage: 2,000 API calls including translations, 382,769 input tokens, 89,897 output tokens, and 472,666 total tokens.
- Source-grounded semantic n=30: 90 base items, 360 judge calls, `$0.0659`, about `$0.183` per 1,000 judge calls.
- Source-grounded semantic n=30 usage: 450 API calls including translations, 252,403 input tokens, 46,780 output tokens, and 299,183 total tokens.
- WMT reference-free n=30: 90 base items, 300 judge calls, `$0.0206`, about `$0.069` per 1,000 judge calls.
- WMT reference-free n=30 usage: 300 API calls, 84,237 input tokens, 13,339 output tokens, and 97,576 total tokens.
- This directly supports the paper's recommendation to report parse rate, token usage, and cost rather than only aggregate judge scores. Token usage is price-independent; dollar costs are local returned-usage estimates and should be refreshed against current official pricing before camera-ready release.

## Repeatability control

This is a no-new-API control over overlapping pilot and main-run response caches. It is generated by `src/summarize_repeatability_control.py`.

Artifacts:
- Summary CSV: `data/analysis/repeatability_control_summary.csv`
- Detail CSV: `data/analysis/repeatability_control_details.csv`
- Markdown summary: `data/analysis/repeatability_control.md`
- Paper table: `paper/tables/repeatability_control.tex`

Main repeatability signal:
- Exact original-text prompt repeats: 42 scored prompt pairs with identical prompt text across the historical n=20 pilot and n=50 main run; exact score agreement is 92.9%, mean absolute score delta is 0.071, and the maximum delta is 1.
- Explicit-pivot pipeline repeats: 14 scored prompt pairs with the same prompt IDs but regenerated English-pivot prompt text; exact score agreement is 57.1%, mean absolute score delta is 0.643, and the maximum delta is 4.
- Paper framing: the exact-prompt control shows that ordinary repeated-call variation is much smaller than the headline protocol shifts, while regenerated English-pivot workflows can add translation/prompt-pipeline volatility. The pivot repeat should not be described as a pure judge-stochasticity control because the prompt text changed.

## Claim evidence matrix

This is a no-new-API release-readiness artifact generated by `src/build_claim_evidence_matrix.py`.

Artifacts:
- CSV: `data/analysis/claim_evidence_matrix.csv`
- Markdown: `data/analysis/claim_evidence_matrix.md`
- LaTeX table: `paper/tables/claim_evidence_matrix.tex`

Main matrix contents:
- Maps 9 headline paper claims to concrete metrics, paired-bootstrap outputs, sampling/prompt audits, run inventory, and validator coverage.
- Covers the main score-shift claim, the explicit-pivot failure claim, stronger-judge audit evidence, semantic and WMT claim boundaries, aggregate protocol instability, calibration diagnostics, repeatability control, and release-package auditability.
- Intended as a paper-support artifact rather than a main manuscript table because the full paths and validator notes are too wide for the short-paper body.

## RQ and contribution coverage matrix

This is a no-new-API plan-coverage artifact generated by `src/build_rq_contribution_matrix.py`.

Artifacts:
- CSV: `data/analysis/rq_contribution_matrix.csv`
- Markdown: `data/analysis/rq_contribution_matrix.md`
- LaTeX table: `paper/tables/rq_contribution_matrix.tex`

Main matrix contents:
- Maps RQ1--RQ4 and the four planned contribution areas to current evidence, primary artifacts, and conservative claim boundaries.
- Marks calibration as a diagnostic rather than a universal repair, the WMT extension as contrast evidence, and model-family coverage as a remaining limitation rather than a hidden claim.
- Intended for writing, reviewer response, and completion auditing against `globaljudge_protocol_paper_plan.md`.

## Reproducibility manifest

This is a no-new-API release-readiness artifact generated by `src/build_reproducibility_manifest.py`.

Artifacts:
- JSON manifest: `data/analysis/reproducibility_manifest.json`
- Markdown manifest: `data/analysis/reproducibility_manifest.md`

Main manifest contents:
- Records 208 files across docs, configs, source code, raw data archives, processed items, translations, response caches, analysis outputs, and paper outputs.
- Captures SHA256 hashes and file sizes for all recorded files.
- Captures row counts for CSV and JSONL artifacts; the paper-facing response caches total 3,480 judge responses, and the processed paper-facing item files total 780 base items.
- Lists the validation commands used for the claim package: source compile, claim validator, paper build, stale-claim scan, and LaTeX log scan.

## Prior supporting pilots

### n=20 candidate-quality pilot

Artifacts:
- Items: `data/processed/pilot_n20_items.jsonl`
- Explicit translations: `data/processed/pilot_n20_english_translations.jsonl`
- Combined responses: `data/responses/pilot_n20_combined_explicit_responses.jsonl`
- Metrics: `data/analysis/pilot_n20_combined_explicit_metrics.csv`
- Protocol shifts: `data/analysis/pilot_n20_combined_explicit_protocol_shifts.csv`
- Summary: `data/analysis/pilot_n20_combined_explicit_summary.md`
- Figures: `paper/figures/pilot_n20_combined_explicit_heatmap.png`, `paper/figures/pilot_n20_combined_explicit_shifts.png`

The n=20 run found the same direction as n=50 but with noisier estimates. Largest shifts were `tr / comprehensibility` target vs explicit pivot `1.50`, `tr / grammar` `1.40`, and `vi / grammar` `1.35`.

### Source-grounded semantic XLSum pilot n=8

Pilot scope:
- 3 languages: `es-ES`, `tr`, `vi`
- dimension: `main_ideas`
- 8 balanced examples per language
- 24 base items
- same four protocols
- source text excerpts truncated to 1400 characters

Artifacts:
- Raw XLSum archives: `data/raw/xlsum/`
- Source-grounded items: `data/processed/semantic_xlsum_pilot_items.jsonl`
- Source/candidate translations: `data/processed/semantic_xlsum_pilot_english_translations.jsonl`
- Responses: `data/responses/semantic_xlsum_pilot_responses.jsonl`
- Metrics: `data/analysis/semantic_xlsum_pilot_metrics.csv`
- Summary: `data/analysis/semantic_xlsum_pilot_summary.md`
- Figures: `paper/figures/semantic_xlsum_pilot_heatmap.png`, `paper/figures/semantic_xlsum_pilot_shifts.png`

Main semantic-pilot signal:
- Protocol shifts persist for source-grounded semantic judging.
- `tr / main_ideas`: explicit pivot was best in the tiny pilot, Spearman `0.671`.
- `vi / main_ideas`: explicit pivot was harmful, Spearman `-0.354`, while target-language rubric reached `0.378`.
- This supports a cautious hypothesis: pivoting can help semantic judgments in some languages but harm others, while it is especially suspect for target-language form dimensions.

## Qualitative examples

The main n=50 qualitative examples are now generated by `src/extract_qualitative_examples.py`.

Artifacts:
- CSV: `data/analysis/qualitative_protocol_examples.csv`
- Markdown: `data/analysis/qualitative_protocol_examples.md`

Main mechanisms:
- Pivot can clean away target-language error signals. Example: a Vietnamese human-negative comprehensibility item is scored 2 by target-language judging, but its English pivot `Prepare materials.` is scored 5.
- Pivot can introduce translation artifacts. Example: a Turkish human-positive comprehensibility item is scored 5 by direct, target-language, and bilingual protocols, but the English pivot repeats the sentence and the pivot judge assigns 1.

Older grammar examples where explicit English pivot inflated scores in the n=20 pilot:

| Language | Human grammar label | Target rubric score | Explicit pivot score | Original summary | English pivot text |
|---|---:|---:|---:|---|---|
| `tr` | 0 | 2 | 5 | `Facebook İnternet sitesini "Keşfet" sekmesinin altında Daha Fazla'ya tıkla. Tarihte Bugün Anıların arasında aşğı kaydır.` | `Click on 'More' under the 'Discover' tab on the Facebook website. Scroll down among the memories for 'On This Day'.` |
| `tr` | 0 | 2 | 5 | `Yunanistan'da Öğretmenler ve Öğretmenler greve başladı.` | `Teachers and educators in Greece have started a strike.` |
| `vi` | 0 | 2 | 5 | `Cựu Chủ tịch Đà Nẵng Phan Văn Anh Vũ bị đề nghị tổng cộng vào ngày 11/11 tại Hà Nội, theo truyền thông Việt Nam.` | `Former Chairman of Da Nang, Phan Van Anh Vu, was proposed on November 11 in Hanoi, according to Vietnamese media.` |

These examples support the conservative claim that translation-pivot evaluation can hide target-language form errors because the judge sees a cleaned English rendering.

## Prompt and protocol inventory

This is a no-new-API prompt-auditability artifact generated by `src/summarize_prompt_inventory.py`.

Artifacts:
- Prompt-level CSV: `data/analysis/prompt_inventory.csv`
- Run-level CSV: `data/analysis/prompt_inventory_summary.csv`
- Representative redacted prompt CSV: `data/analysis/prompt_representatives.csv`
- Markdown prompt appendix: `data/analysis/prompt_inventory.md`
- Paper table: `paper/tables/prompt_inventory.tex`

Main prompt-inventory signal:
- Candidate n50 has 1,600 prompts across 4 protocols, 4 languages, 2 dimensions, and `gpt-4o-mini`.
- Candidate audit n25 has 800 prompts across the same protocol/language/dimension grid and `gpt-4.1-mini`.
- Semantic n30 has 360 prompts across 4 protocols, 3 languages, one `main_ideas` dimension, and `gpt-4o-mini`.
- WMT reference and reference-free n30 each have 300 prompts; the targeted WMT audit has 120 prompts across 2 language pairs and 3 protocols.
- Representative prompts redact item-specific source/reference/candidate text while preserving system messages, rubric wording, protocol instructions, and JSON output contracts.

## Dataset sampling audit

This is a no-new-API item-set audit generated by `src/summarize_dataset_sampling.py`.

Artifacts:
- Item-level CSV: `data/analysis/dataset_sampling_items.csv`
- Group-level CSV: `data/analysis/dataset_sampling_groups.csv`
- Run-level CSV: `data/analysis/dataset_sampling_summary.csv`
- Markdown audit: `data/analysis/dataset_sampling_audit.md`
- Paper table: `paper/tables/dataset_sampling_audit.tex`

Main sampling signal:
- Candidate n50: 400 items, 4 languages, 2 dimensions, 200 positive and 200 negative labels; candidate-only, so source/reference availability is 0%.
- Candidate audit n25: 200 items, 96 positive and 104 negative labels because each language/dimension cell has 12 positive and 13 negative examples.
- Semantic n30: 90 source-grounded items, 3 languages, one `main_ideas` dimension, 45 positive and 45 negative labels; source and reference availability are both 100%.
- WMT n30 shared items: 90 items, 3 language pairs, 45 high-quality and 45 low-quality MQM-derived labels; source and reference availability are both 100%.
- Targeted WMT reference-free audits use balanced 30-item subsets for `zh-en` and `en-de`, each with 15 positive and 15 negative labels.

## Current limitations

- The main n=50 result uses only one judge model. The `gpt-4.1-mini` n=25 audit shows that the protocol-sensitivity signal survives a stronger judge, but model-general claims still require a second model family.
- The source-grounded semantic run covers only `main_ideas`, three non-English languages, one dataset family, and one judge model.
- The WMT MQM contrast/extension run is small, covers only year 2022 and three language pairs, adds target/bilingual rubrics only for the two non-English target pairs, and uses quantile-derived binary labels from continuous MQM scores. The reference-free condition reuses the same MQM-derived labels, so it is a stress test of judge protocol rather than a new human annotation target.
- Target-language rubric translations are pragmatic pilot translations, not native-speaker validated.
- English-pivot translations are produced by the same model family as the judge, which is realistic for low-cost workflows but should be disclosed.
- Approximate cost accounting uses local price constants; final paper tables should prioritize returned token usage and refresh dollar costs against current official pricing.

## Recommended next steps

1. Tighten the short-paper draft into the target venue format.
2. If budget and time allow, add a non-OpenAI judge family or another OpenAI family not used for translation.
3. Native-check the Spanish, Turkish, and Vietnamese rubric translations before final claims about target-language prompting.
4. If time allows, scale the WMT MQM extension beyond n=30, especially the reference-free condition where protocol effects are larger.
5. Keep the central claim conservative and practical: multilingual LLM-as-judge papers should report protocol sensitivity, language gaps, calibration behavior, parse rates, and cost instead of a single aggregate judge score.

## Paper-facing writing artifacts

- Results brief: `paper/results_brief.md`
- Reviewer/submission packet: `paper/submission_packet.md`
- Benchmark data card: `paper/globaljudge_protocolbench_datacard.md`
- Release validation report: `data/analysis/release_validation_report.{json,md}`
- Completion audit: `data/analysis/completion_audit.{json,md}`
- Short-paper draft: `paper/globaljudge_short_paper_draft.md`
- Compact extended abstract: `paper/extended_abstract.tex`, `paper/extended_abstract.pdf` (2 pages)
- Compiled LaTeX manuscript: `paper/main.tex`, `paper/main.pdf`
- Paper build entry point: `paper/Makefile` (`make -C paper`)
- Reporting card: `paper/reporting_card.md`
- Bibliography: `paper/references.bib` now includes closest multilingual LLM-judge positioning citations in addition to SEAHORSE, XLSum, G-Eval, MT-Bench/Chatbot Arena, and WMT LLM evaluator work.
- LaTeX tables: `paper/tables/*.tex`
- Protocol-instability summarizer: `src/summarize_protocol_instability.py`
- Claim-evidence matrix builder: `src/build_claim_evidence_matrix.py`
- RQ/contribution matrix builder: `src/build_rq_contribution_matrix.py`
- Submission packet builder: `src/build_submission_packet.py`
- Benchmark data-card builder: `src/build_benchmark_datacard.py`
- Completion audit builder: `src/build_completion_audit.py`
- Calibration learning-curve summarizer: `src/summarize_calibration_learning_curve.py`
- Score-threshold diagnostic: `src/summarize_score_threshold_diagnostic.py`
- Run-inventory summarizer: `src/summarize_run_inventory.py`
- Repeatability-control summarizer: `src/summarize_repeatability_control.py`
- Reproducibility manifest builder: `src/build_reproducibility_manifest.py`
- Prompt-inventory summarizer: `src/summarize_prompt_inventory.py`
- Dataset-sampling audit: `src/summarize_dataset_sampling.py`
- Qualitative example extractor: `src/extract_qualitative_examples.py`
- Paper claim validator: `src/validate_paper_claims.py`
- Table exporter: `src/export_paper_tables.py`
- Brief generator: `src/make_results_brief.py`
- Release validation runner: `src/run_release_checks.py`

Current validation gate:
- `/home/eston/anaconda3/envs/global_judge/bin/python src/validate_paper_claims.py`
- `make -C paper`
- `/home/eston/anaconda3/envs/global_judge/bin/python src/run_release_checks.py`
