# Do Not Let English Judge the World: Protocol Sensitivity in Multilingual LLM-as-a-Judge Evaluation

## Abstract

LLM-as-a-judge evaluation is increasingly used to score open-ended model outputs, but multilingual benchmarks often hide an implementation choice that can change conclusions: which language the judge sees, which language the rubric uses, and whether non-English examples are translated into English before judging. We study this protocol sensitivity on multilingual summarization evaluation using SEAHORSE human labels and source-grounded XLSum examples, with a small WMT MQM translation-quality contrast. Across 400 candidate-quality examples in English, Spanish, Turkish, and Vietnamese, the same `gpt-4o-mini` judge assigns materially different scores under direct English rubrics, target-language rubrics, explicit English-pivot judging, and bilingual rubrics. The largest shifts appear in target-language form dimensions: for Vietnamese grammar, target-language rubric and English-pivot scores differ by 1.20 points on a 1-5 scale on average. English pivot is not a safe default: on Turkish comprehensibility it significantly underperforms direct judging, and a stronger `gpt-4.1-mini` audit reproduces the same failure mode. In source-grounded XLSum `main_ideas`, protocol shifts are smaller but remain language-dependent. In WMT MQM translation quality, reference-based direct-vs-pivot deltas are smaller, while reference-free judging exposes larger `gpt-4o-mini` protocol effects and a targeted stronger-judge audit shows which effects are directional versus model-dependent. Across 17 non-audit task/language cells, the best protocol is not direct in 11 cells and explicit pivot is worst in 10. We argue that multilingual benchmarks should report protocol sensitivity, language gaps, calibration behavior, parse rates, and cost instead of a single aggregate judge score.

## 1. Introduction

LLM judges are attractive because they make open-ended evaluation cheap, fast, and easy to scale. Recent work has shown that LLM judges can correlate with human preferences and with task-specific human ratings in settings such as chatbot evaluation, summarization, and machine translation [@zheng2023judging; @liu2023geval; @kocmi2023large]. This has made LLM-as-a-judge a common evaluation component in both research and product pipelines.

However, multilingual evaluation adds a protocol choice that is often treated as incidental. A benchmark builder can ask an English prompt to judge a non-English answer directly, translate the answer into English first, translate the rubric into the target language, or provide bilingual instructions. These choices are not equivalent. An English-pivot protocol may make semantic content easier for an English-dominant model to process, but it can erase target-language form evidence such as grammar, fluency, register, morphology, and repetition. A target-language rubric may better match the task surface, but it depends on rubric translation quality. A bilingual rubric may provide redundancy but can also introduce conflicting cues.

This paper asks a practical question:

> When a multilingual benchmark reports an LLM judge score, how sensitive is that score to the judge protocol?

We study this question using existing human-labeled summarization evaluation data and a compact reference-based machine translation contrast. SEAHORSE provides multilingual human ratings for candidate summaries across several quality dimensions [@clark2023seahorse]. XLSum provides source documents and summaries for many languages [@hasan2021xlsum]. We use SEAHORSE candidate-quality dimensions for grammar and comprehensibility, recover source-grounded XLSum examples for `main_ideas` by matching SEAHORSE reference summaries to raw XLSum source records, and add WMT MQM human-evaluation rows for translation-quality judging.

Our contribution is a small but reusable protocol comparison package:

1. A benchmark scaffold, GlobalJudge-ProtocolBench, covering 580 main base examples across candidate-quality, source-grounded semantic, and reference-based translation-quality settings, plus a 200-item stronger-judge audit.
2. A direct comparison of four multilingual judge protocols for summarization, plus reference-based and reference-free WMT MQM translation-quality extensions.
3. Protocol-sensitivity metrics: by-language human alignment, paired score shifts, language gaps, calibration behavior, parse rate, and cost.
4. A Global Judge Reporting Card for future multilingual LLM-as-a-judge papers.

Our main finding is not that one protocol is universally best. The key result is that protocol choice can change both scores and human alignment, and the direction depends on language and quality dimension. Therefore a single aggregate multilingual judge score is under-specified unless the judge protocol and its sensitivity are reported.

## 2. Related Work and Positioning

LLM judges are now widely studied as scalable evaluators for open-ended generation, including chatbot response quality, summarization, and machine translation [@zheng2023judging; @liu2023geval; @kocmi2023large]. This line of work establishes that prompted LLM evaluators can align with human judgments in some settings, but it also raises concerns about prompt sensitivity and evaluator bias. Our focus is narrower: we treat the judge protocol itself as an experimental factor in multilingual evaluation.

Recent multilingual judge work finds that LLM judges can be inconsistent across languages and that disagreement can be exploited or corrected by more elaborate multilingual judging procedures [@fu2025reliable; @fu2026languages]. Our contribution is complementary. Rather than proposing a new judge model or adjudication algorithm, we evaluate low-cost reporting choices available to benchmark builders: judging original text, translating into English, translating the rubric, using bilingual instructions, and calibrating score thresholds against small human-labeled splits.

## 3. Experimental Setup

### 3.1 Data

We use two SEAHORSE-derived settings.

Candidate-quality setting. We sample from the SEAHORSE test split. The main run uses four languages: English (`en-US`), Spanish (`es-ES`), Turkish (`tr`), and Vietnamese (`vi`). We evaluate two candidate-visible dimensions:

- `comprehensibility`: whether the candidate summary is easy to understand as written.
- `grammar`: whether the candidate summary is grammatical and fluent in its language.

For each language and dimension, we sample 50 balanced examples, with 25 positive and 25 negative human labels. This gives 400 base examples and 1,600 judge responses across four protocols.

Source-grounded semantic setting. SEAHORSE raw TSV files do not include source documents. To recover source-grounded examples, we match SEAHORSE reference summaries to raw XLSum test summaries. Matching recovers 151/151 Spanish, 243/244 Turkish, and 252/252 Vietnamese reference rows. We then sample 30 balanced `main_ideas` examples per language, giving 90 base examples and 360 judge responses.

WMT MQM translation-quality contrast. To test whether protocol sensitivity is equally severe for machine translation evaluation, we sample 30 balanced examples per language pair from WMT MQM human-evaluation rows: `en-de`, `en-ru`, and `zh-en`. We use year-2022 rows and derive high/low labels from within-pair MQM-score quantiles. This gives 90 base examples. We run both reference-based judging (source, candidate, reference) and reference-free judging (source, candidate only). Each condition uses direct judging and explicit English-pivot judging for all pairs, plus target-language and bilingual rubrics for the two non-English target pairs, giving 600 WMT judge responses total.

Stronger-judge audit. To check whether the observed protocol sensitivity is only a cheap-judge artifact, we run `gpt-4.1-mini` on a stratified candidate-quality subset: 25 examples per language/dimension, 200 base examples, and 800 judge responses.

Sampling audit. The processed item sets used by the paper-facing runs are summarized in `paper/tables/dataset_sampling_audit.tex`. The main candidate-quality, semantic, and WMT item pools are balanced by construction, while the candidate audit intentionally has 12 positive and 13 negative examples per language/dimension cell.

### 3.2 Judge Protocols

We compare four protocols.

P0, direct English rubric. The original candidate summary is shown in its original language, but the instruction and rubric are written in English.

P1, target-language rubric. The original candidate summary is shown in its original language, and the rubric/question are translated into the task language.

P2, explicit English pivot. The source text or reference text, when present, and candidate summary are translated into English first. The judge sees only the English translation. For grammar and form dimensions, the prompt explicitly says to judge only what remains visible after translation.

P3, bilingual rubric. The original candidate summary is shown in its original language, and the prompt includes both English and target-language rubric wording.

The summarization settings use all four protocols. The WMT MQM contrast uses P0 and P2 for all pairs, and P1/P3 for non-English target pairs where target-language rubric wording is meaningful. All judge calls request strict JSON with a 1-5 score, a coarse label, confidence, and a short rationale. The main judge is `gpt-4o-mini`; the audit judge is `gpt-4.1-mini`.

Prompt auditability. The release package includes a prompt inventory with counts for each paper-facing prompt file and a redacted prompt appendix that preserves system messages, rubric wording, protocol instructions, and JSON contracts while replacing item-specific source, reference, and candidate text with redaction markers.

### 3.3 Metrics

We report:

- Spearman correlation between judge score and binary human label.
- AUROC for human positive vs. negative labels using judge score.
- Mean absolute paired score shift between protocols on the same items.
- Language gap: max minus min by-language Spearman for a protocol.
- Post-hoc calibration: threshold selection on a calibration split, evaluated on held-out examples.
- Parse rate and approximate API cost from returned usage metadata.

For paired protocol comparisons, we bootstrap item-level differences to estimate confidence intervals for AUROC deltas.

## 4. Results

### 4.1 Protocol Choice Changes Candidate-Quality Scores

Table \ref{tab:candidate_protocol_sensitivity} summarizes the strongest candidate-quality findings. Protocol shifts are large on the same item, especially for target-language form dimensions. For Vietnamese grammar, target-language rubric and English-pivot scores differ by 1.20 points on a 1-5 scale on average. For Vietnamese comprehensibility, bilingual and English-pivot scores differ by 0.96 points on average.

These shifts matter because they are not merely score-scale differences. In Turkish comprehensibility, direct judging reaches Spearman 0.603 and AUROC 0.836, while explicit English pivot drops to Spearman 0.331 and AUROC 0.686. The paired AUROC delta for pivot minus direct is -0.150, with 95% bootstrap CI [-0.257, -0.055]. Thus a common workaround, translating into English before judging, can significantly reduce alignment with human labels.

Qualitative examples suggest two concrete mechanisms. In one Vietnamese human-negative comprehensibility item, target-language judging scores the original summary 2, while the English pivot "Prepare materials." is scored 5 because the translation is clear but has removed the target-language error signal. Conversely, in a Turkish human-positive comprehensibility item, direct, target-language, and bilingual protocols all score 5, but the pivot translation repeats the sentence and the pivot judge assigns 1. These cases illustrate why translation can both clean away errors and introduce new artifacts.

Vietnamese shows a similar pattern. For Vietnamese comprehensibility, explicit pivot is weaker than bilingual judging: bilingual minus pivot AUROC delta is +0.166, with 95% CI [0.009, 0.317]. For Vietnamese grammar, explicit pivot has Spearman 0.016 and AUROC 0.509 despite a high mean judge score, consistent with the concern that translation can hide form errors.

### 4.2 A Stronger Judge Does Not Remove the Failure Mode

The `gpt-4.1-mini` audit is still bounded, so we do not treat its exact correlations as final. It is useful as a stronger-model failure-mode check. On Turkish comprehensibility, the stronger judge gives direct judging Spearman 0.729 / AUROC 0.910 and bilingual judging 0.796 / 0.946, but explicit pivot falls to 0.168 / 0.593. The paired AUROC delta for pivot minus direct is -0.317, and bilingual minus pivot is +0.353. The same pattern appears for Vietnamese grammar: direct judging reaches 0.564 / 0.814, explicit pivot drops to -0.052 / 0.471, and bilingual judging recovers to 0.491 / 0.769.

This audit supports the main interpretation: protocol sensitivity is not only a property of a weak judge. Stronger models can still react sharply to whether they see original target-language text or an English pivot.

### 4.3 Source-Grounded Semantics Are Also Protocol-Sensitive

The source-grounded `main_ideas` setting gives a different but complementary pattern. Protocol shifts are smaller than for grammar/form dimensions, which is expected: semantic content can often survive translation better than grammar or fluency. Still, explicit pivot is not uniformly best.

For Spanish `main_ideas`, explicit pivot performs best: Spearman 0.514 / AUROC 0.771. For Turkish, bilingual judging is best: Spearman 0.588 / AUROC 0.793, while explicit pivot is weaker at 0.339 / 0.669. For Vietnamese, all protocols are weak, but explicit pivot is chance-level: Spearman 0.000 / AUROC 0.500, while bilingual reaches 0.195 / 0.607.

Paired comparisons reinforce this language dependence. For Turkish `main_ideas`, bilingual minus pivot AUROC delta is +0.124 with 95% CI [0.000, 0.275]. For Vietnamese, bilingual minus pivot AUROC delta is +0.107 with 95% CI [0.013, 0.220]. Therefore the appropriate conclusion is not "never pivot." It is that pivoting is a protocol choice whose effect must be measured and reported.

### 4.4 Reference-Based MT Is a Useful Contrast

The WMT MQM contrast is intentionally smaller and narrower than the summarization runs, but it is important for claim boundaries. Reference-based translation-quality judging shows smaller direct-vs-pivot shifts and no significant paired AUROC deltas. For `en-de`, direct and pivot judging are nearly identical: direct Spearman/AUROC is 0.388 / 0.673 and pivot is 0.398 / 0.678. For `en-ru`, both direct and pivot are weak. For `zh-en`, pivot shifts more scores than the other pairs, with mean absolute shift 0.53, but the paired AUROC delta remains small at -0.024 with 95% CI [-0.227, 0.177].

Reference-free MT judging surfaces stronger `gpt-4o-mini` protocol effects. For `zh-en`, direct judging reaches 0.595 / 0.820, while explicit pivot drops to 0.187 / 0.600; the paired pivot-minus-direct AUROC delta is -0.220 with 95% CI [-0.440, -0.007]. For `en-de`, bilingual reference-free judging is best at 0.677 / 0.838 and improves over pivot by +0.129 AUROC with CI [0.025, 0.258]. For `en-ru`, the target-language rubric is best by AUROC, though all correlations remain low. However, a targeted `gpt-4.1-mini` WMT audit separates directional robustness from model dependence: it preserves the `zh-en` direct-over-pivot direction (0.503 / 0.773 vs. 0.254 / 0.636; delta -0.138, CI [-0.346, 0.067]) but does not reproduce the `en-de` bilingual-over-pivot gain (pivot 0.563 / 0.784 vs. bilingual 0.503 / 0.760). Thus English pivoting is risky for target-language form and some source-grounded semantic settings, but the WMT evidence is best treated as protocol/model-sensitivity evidence rather than a stable global protocol ranking.

### 4.5 No Single Protocol Dominates

Aggregating over task/language cells makes the reporting-card motivation sharper. Across 17 non-audit cells, the best AUROC protocol is not direct in 11 cells, explicit pivot is the worst protocol in 10 cells, and 6 cells have at least one paired AUROC delta with a bootstrap CI excluding zero. In the `gpt-4.1-mini` candidate audit, 7 of 8 cells have an AUROC range of at least 0.10 across protocols, and the maximum range is 0.353. Protocol choice is therefore an experimental factor to report, not a nuisance prompt detail to hide.

### 4.6 Aggregate Scores Hide Language Gaps

Protocol choice changes language disparity. In candidate-quality comprehensibility, explicit pivot has a Spearman language gap of 0.625, from Vietnamese 0.086 to English 0.711. Bilingual judging reduces the same gap to 0.302. In source-grounded `main_ideas`, explicit pivot again has the largest language gap, 0.514, from Vietnamese 0.000 to Spanish 0.514. In WMT, the reference-free direct protocol has a much larger gap than the reference-based direct protocol, 0.572 versus 0.223.

These gaps are central for global evaluation. If a paper reports a single average LLM judge score, it can obscure the languages for which the judge is weak or the protocol is harmful.

### 4.7 Repeatability Control

The large protocol shifts are not explained by ordinary run-to-run variation in exact repeated prompts. The historical n=20 pilot and n=50 main run overlap on 42 original-text prompt calls with identical prompt text. Across these repeated calls, exact score agreement is 92.9%, mean absolute score delta is 0.071, and the maximum score delta is 1. This is much smaller than the main protocol shifts, such as 0.96 for Vietnamese comprehensibility and 1.20 for Vietnamese grammar.

The explicit-pivot overlap is different. Fourteen repeated explicit-pivot prompt IDs have different prompt text because the English-pivot pipeline was regenerated. These have lower exact agreement, 57.1%, and mean absolute delta 0.643. This should be framed as pivot-pipeline volatility, not pure judge stochasticity.

### 4.8 Calibration Is Useful but Not Universal

Post-hoc threshold calibration behaves differently across settings. In candidate-quality n=50, mean held-out balanced-accuracy delta is -0.017, with median 0.000. In the stronger audit, it remains slightly negative: mean -0.029, median -0.003. In source-grounded `main_ideas`, calibration is positive: mean +0.136, median +0.136. In the WMT reference-based extension it is again negative, with mean -0.036 and median 0.000. A repeated learning-curve analysis gives the same boundary: with 50 stratified resamples, source-grounded semantics improves by about +0.12 to +0.14 balanced accuracy even with small calibration sets, while candidate-quality calibration remains slightly negative on average and reference-free WMT is mixed.

The score-threshold diagnostic makes the mechanism explicit. For source-grounded `main_ideas`, the fixed score >= 4 threshold marks only 8.3% of balanced examples as good, and the modal best in-group threshold is 2. For WMT reference-free judging, score >= 4 marks 90.0% of examples as good, and the modal best threshold is 5. This supports using calibration diagnostics, but not claiming calibration as a universal fix.

## 5. Global Judge Reporting Card

We recommend that multilingual LLM-as-a-judge papers report:

1. Judge model and version.
2. Prompt/rubric language.
3. Whether source, candidate, or reference texts were translated.
4. Whether target-language form dimensions were judged in the original language.
5. Per-language human alignment, not only aggregate alignment.
6. Protocol-shift metrics on the same items.
7. Language gaps for each protocol.
8. Calibration split size, calibration method, and held-out calibration effect.
9. JSON/parse failure rate.
10. Returned token usage and approximate cost per 1,000 judgments.

This checklist makes judge-protocol choices visible and makes multilingual evaluation easier to audit.

For this study, token usage is the stable accounting quantity. Dollar values are returned usage estimates computed with the run-time local price map and should be refreshed against current provider pricing before camera-ready release. The release package includes a reproducibility manifest with file hashes, record counts, and validation commands for the processed items, response caches, analysis tables, figures, and manuscript artifacts. It also includes claim-evidence and RQ-coverage matrices that map each headline claim and planned contribution to concrete artifacts and validator checks.

## 6. Limitations

The current evidence is deliberately bounded. All main judge calls use OpenAI models, and the stronger audits use another OpenAI model rather than an independent model family. Target-language rubric translations are pragmatic pilot translations, not native-speaker validated. The source-grounded setting covers one semantic dimension and three non-English languages. The WMT MQM contrast is small, covers one year and three language pairs, adds target/bilingual rubrics only for the two non-English target pairs, and uses quantile-derived binary labels from continuous MQM scores. The targeted WMT stronger-judge audit covers only two reference-free cells at n=30, so it is a robustness check rather than a definitive model-family comparison. The reference-free WMT condition reuses the same MQM-derived labels, so it is a protocol stress test rather than a new human annotation target. The SEAHORSE labels are binary yes/no labels for each dimension, while LLM judges produce 1-5 scores; thresholding and calibration are therefore part of the evaluation design. Finally, approximate cost accounting uses a local price map and returned usage metadata; final camera-ready cost tables should be recomputed against current official API pricing.

These limitations do not weaken the central protocol-sensitivity claim. They define its boundary: the current work is a practical stress test and reporting recipe, not a claim that any one prompt is globally optimal.

## 7. Conclusion

Multilingual LLM-as-a-judge evaluation is under-specified without the judge protocol. The same item can receive different scores depending on whether the judge sees original text, translated text, target-language instructions, or bilingual instructions. English-pivot judging can help in some semantic and reference-based settings, but it can also erase target-language evidence and increase language gaps. We recommend that global benchmark builders report protocol sensitivity as a first-class evaluation result.

## Table and Figure Plan

- Table \ref{tab:candidate_protocol_sensitivity}: generated at `paper/tables/candidate_protocol_sensitivity.tex`.
- Table \ref{tab:semantic_main_ideas}: generated at `paper/tables/semantic_main_ideas.tex`.
- Table \ref{tab:stronger_judge_audit}: generated at `paper/tables/stronger_judge_audit.tex`.
- Table \ref{tab:wmt_translation_quality}: generated at `paper/tables/wmt_translation_quality.tex`.
- Table \ref{tab:wmt_ref_free_stronger_audit}: generated at `paper/tables/wmt_ref_free_stronger_audit.tex`.
- Table \ref{tab:dataset_sampling_audit}: generated at `paper/tables/dataset_sampling_audit.tex`.
- Table \ref{tab:prompt_inventory}: generated at `paper/tables/prompt_inventory.tex`.
- Table \ref{tab:protocol_instability_summary}: generated at `paper/tables/protocol_instability_summary.tex`.
- Table \ref{tab:repeatability_control}: generated at `paper/tables/repeatability_control.tex`.
- Table \ref{tab:language_gaps}: generated at `paper/tables/language_gaps.tex`.
- Table \ref{tab:calibration_summary}: generated at `paper/tables/calibration_summary.tex`.
- Table \ref{tab:calibration_learning_curve}: generated at `paper/tables/calibration_learning_curve.tex`.
- Table \ref{tab:score_threshold_diagnostic}: generated at `paper/tables/score_threshold_diagnostic.tex`.
- Table \ref{tab:run_inventory}: generated at `paper/tables/run_inventory.tex`.
- Table \ref{tab:api_usage_inventory}: generated at `paper/tables/api_usage_inventory.tex`.
- Figure 1: candidate n=50 heatmap, `paper/figures/candidate_n50_combined_explicit_heatmap.png`.
- Figure 2: candidate n=50 protocol shifts, `paper/figures/candidate_n50_combined_explicit_shifts.png`.
- Figure 3: semantic n=30 heatmap, `paper/figures/semantic_xlsum_n30_heatmap.png`.
- Figure 4: WMT MQM n=30 heatmap, `paper/figures/wmt_mqm_n30_heatmap.png`.

## References

Use `paper/references.bib`.
