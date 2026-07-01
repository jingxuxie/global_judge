# GlobalJudge Results Brief

This brief is generated from the current analysis CSV/JSONL artifacts. Values are Spearman / AUROC unless noted.

## Claim Boundary

- Strongest claim: multilingual LLM-as-judge conclusions are protocol-sensitive; reporting one aggregate score hides language, dimension, and protocol effects.
- Strong evidence: n=50 candidate-quality SEAHORSE run, n=30 source-grounded XLSum `main_ideas` run, and n=25 `gpt-4.1-mini` experiment all show protocol-dependent score or alignment changes.
- Contrast evidence: WMT MQM n=30 per language pair shows smaller direct-vs-pivot shifts for reference-based translation quality, while reference-free MT judging has larger `gpt-4o-mini` protocol effects.
- WMT experiment boundary: a targeted `gpt-4.1-mini` experiment preserves the `zh-en` pivot-drop direction but not significance at n=30, and does not reproduce the `en-de` bilingual-over-pivot gain.
- Aggregate instability: across 17 main-experiment task/language cells, the best AUROC protocol is not direct in 11 cells, explicit pivot is worst in 10 cells, and 6 cells have at least one strongly supported paired AUROC change.
- Conservative caveat: all current runs use OpenAI judges; target-language rubrics are pilot translations and should be native-checked before final publication claims.

## Dataset Sampling Summary

| Run | Items | Langs | Dims | Pos | Neg | Source Rate | Reference Rate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| candidate n50 | 400 | 4 | 2 | 200 | 200 | 0.0% | 0.0% |
| candidate experiment n25 | 200 | 4 | 2 | 96 | 104 | 0.0% | 0.0% |
| semantic n30 | 90 | 3 | 1 | 45 | 45 | 100.0% | 100.0% |
| wmt n30 shared items | 90 | 3 | 1 | 45 | 45 | 100.0% | 100.0% |
| wmt ref-free experiment zh-en | 30 | 1 | 1 | 15 | 15 | 100.0% | 100.0% |
| wmt ref-free experiment en-de | 30 | 1 | 1 | 15 | 15 | 100.0% | 100.0% |

## Candidate-Quality N=50

| Cell | Direct | Target | Pivot | Bilingual | Paired AUROC Delta | Delta | Mean Abs Shift |
| --- | --- | --- | --- | --- | --- | --- | --- |
| tr / comprehensibility | 0.60 / 0.84 | 0.56 / 0.81 | 0.33 / 0.69 | 0.57 / 0.82 | pivot - direct | -0.15 | 0.62 |
| vi / comprehensibility | 0.35 / 0.69 | 0.16 / 0.59 | 0.09 / 0.55 | 0.40 / 0.71 | bilingual - pivot | 0.17 | 0.96 |
| tr / grammar | -0.02 / 0.49 | -0.09 / 0.45 | -0.08 / 0.46 | -0.07 / 0.46 | pivot - direct | -0.03 | 0.84 |
| vi / grammar | 0.23 / 0.62 | 0.25 / 0.63 | 0.02 / 0.51 | 0.10 / 0.55 | pivot - target | -0.12 | 1.20 |

## Source-Grounded Semantic N=30

| Language | Best Protocol | Best | Direct | Pivot | Bilingual |
| --- | --- | --- | --- | --- | --- |
| es-ES | P2_explicit_pivot | 0.51 / 0.77 | 0.49 / 0.76 | 0.51 / 0.77 | 0.43 / 0.72 |
| tr | P3_bilingual | 0.59 / 0.79 | 0.46 / 0.74 | 0.34 / 0.67 | 0.59 / 0.79 |
| vi | P3_bilingual | 0.19 / 0.61 | 0.14 / 0.58 | 0.00 / 0.50 | 0.19 / 0.61 |

Semantic paired highlights: `tr`, bilingual minus pivot AUROC delta = `+0.12`; `vi`, bilingual minus pivot AUROC delta = `+0.11`.

## Stronger-Judge Experiment

| Cell | Direct | Pivot | Bilingual | Pivot-Direct AUROC | Bilingual-Pivot AUROC |
| --- | --- | --- | --- | --- | --- |
| tr / comprehensibility | 0.73 / 0.91 | 0.17 / 0.59 | 0.80 / 0.95 | -0.32 | 0.35 |
| vi / grammar | 0.56 / 0.81 | -0.05 / 0.47 | 0.49 / 0.77 | -0.34 | 0.30 |

## WMT MQM Translation-Quality Contrast

| Pair | Setting | Best Protocol | Best | Direct | Target | Pivot | Bilingual | Pivot-Direct AUROC | Mean Abs Shift |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| en-de | reference | P3_bilingual | 0.47 / 0.69 | 0.39 / 0.67 | 0.32 / 0.60 | 0.40 / 0.68 | 0.47 / 0.69 | 0.00 | 0.20 |
| en-ru | reference | P1_target_rubric | 0.32 / 0.65 | 0.16 / 0.57 | 0.32 / 0.65 | 0.13 / 0.56 | 0.16 / 0.58 | -0.01 | 0.07 |
| zh-en | reference | P0_direct_english | 0.35 / 0.69 | 0.35 / 0.69 | n/a | 0.30 / 0.67 | n/a | -0.02 | 0.53 |
| en-de | ref-free | P3_bilingual | 0.68 / 0.84 | 0.51 / 0.74 | 0.48 / 0.74 | 0.44 / 0.71 | 0.68 / 0.84 | -0.03 | 0.13 |
| en-ru | ref-free | P1_target_rubric | 0.20 / 0.60 | 0.02 / 0.51 | 0.20 / 0.60 | 0.04 / 0.52 | 0.18 / 0.59 | 0.01 | 0.27 |
| zh-en | ref-free | P0_direct_english | 0.60 / 0.82 | 0.60 / 0.82 | n/a | 0.19 / 0.60 | n/a | -0.22 | 0.70 |

## WMT Ref-Free Stronger-Judge Experiment

| Cell | Comparison | Protocol A | A | Protocol B | B | B-A AUROC | Mean Abs Shift |
| --- | --- | --- | --- | --- | --- | --- | --- |
| zh-en ref-free | pivot - direct | direct | 0.50 / 0.77 | pivot | 0.25 / 0.64 | -0.14 | 0.67 |
| en-de ref-free | bilingual - pivot | pivot | 0.56 / 0.78 | bilingual | 0.50 / 0.76 | -0.02 | 0.20 |

Interpretation: the stronger experiment supports `zh-en` reference-free direct-over-pivot as a directional robustness check. The `en-de` bilingual advantage from the main `gpt-4o-mini` reference-free run is model-dependent in this bounded experiment.

## Qualitative Protocol Examples

| Mode | Cell | Human | Scores | Original | English Pivot | Pivot Rationale |
| --- | --- | --- | --- | --- | --- | --- |
| Pivot inflates human-negative item | vi / comprehensibility | 0 | D=2, T=2, P=5, B=1 | Chuẩn bị vật liệu,. | Prepare materials. | The summary is clear and straightforward, conveying a simple action. |
| Pivot inflates human-negative item | tr / grammar | 0 | D=2, T=3, P=5, B=2 | Kuzey Kore lideri Kim Jong-nam'ın kardeşi Kim Jong-nam'ın, bir kamera şakası yaptığını iddia eden bir kişi gözaltına... | A person claiming to be a prankster of Kim Jong-nam, the brother of North Korean leader Kim Jong-un, has been detained. | The summary is grammatical and fluent in English. |
| Pivot deflates human-positive item | tr / comprehensibility | 1 | D=5, T=5, P=1, B=5 | Kâğıdı kare şeklinde katla. | Fold the paper into a square shape. Fold the paper into a square shape. [repetition continues] | Repetition makes the summary unclear and difficult to understand. |
| Pivot deflates human-positive item | es-ES / comprehensibility | 1 | D=5, T=4, P=2, B=4 | La Comisión Europea detecta otros 12 sospechosos de haber combatido en las filas del Estado Islámico | The European Commission identifies another 12 suspects of having fought in the ranks of the Islamic State. The Europe... | Repetition affects clarity and makes it harder to understand. |

Full examples with target and bilingual rationales are generated at `data/analysis/qualitative_protocol_examples.md`.

## Protocol Instability Summary

| Run | Cells | Median AUROC Range | Max AUROC Range | Range >= .10 | Best != Direct | Pivot Worst | Significant Cells | Max Shift |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| candidate n50 | 8 | 0.07 | 0.17 | 3/8 | 4/8 | 4/8 | 2/8 | 1.20 |
| semantic n30 | 3 | 0.11 | 0.12 | 2/3 | 3/3 | 2/3 | 1/3 | 0.70 |
| wmt reference n30 | 3 | 0.08 | 0.09 | 0/3 | 2/3 | 2/3 | 0/3 | 0.53 |
| wmt ref-free n30 | 3 | 0.13 | 0.22 | 2/3 | 2/3 | 2/3 | 3/3 | 0.70 |
| candidate experiment n25 | 8 | 0.16 | 0.35 | 7/8 | 5/8 | 4/8 | 4/8 | 1.16 |
| wmt ref-free experiment | 2 | 0.08 | 0.14 | 1/2 | 1/2 | 1/2 | 0/2 | 0.67 |

## Repeatability Control

| Control | Pairs | Identical Prompts | Exact Agreement | Mean Abs Delta | Max Abs Delta | Interpretation |
| --- | --- | --- | --- | --- | --- | --- |
| exact original-text prompt repeat | 42 | 100.0% | 92.9% | 0.07 | 1 | Same prompt text repeated across independent pilot/main caches; measures ordinary judge run-to-run noise. |
| explicit-pivot pipeline repeat | 14 | 0.0% | 57.1% | 0.64 | 4 | Prompt text changed because the English-pivot pipeline was regenerated; measures pivot-pipeline volatility. |

Interpretation: exact repeated original-text prompts show small ordinary judge run-to-run variation, while regenerated explicit-pivot prompts expose additional pipeline volatility.

## Largest Language Gaps

| Run | Dimension | Protocol | Spearman Gap | Min Lang | Max Lang |
| --- | --- | --- | --- | --- | --- |
| candidate n50 | comprehensibility | P2_explicit_pivot | 0.63 | vi (0.09) | en-US (0.71) |
| candidate n50 | comprehensibility | P1_target_rubric | 0.53 | vi (0.16) | en-US (0.70) |
| candidate n50 | grammar | P3_bilingual | 0.46 | tr (-0.07) | en-US (0.38) |
| semantic n30 | main_ideas | P2_explicit_pivot | 0.51 | vi (0.00) | es-ES (0.51) |
| semantic n30 | main_ideas | P3_bilingual | 0.39 | vi (0.19) | tr (0.59) |
| semantic n30 | main_ideas | P1_target_rubric | 0.36 | vi (0.14) | tr (0.50) |
| wmt n30 | translation_quality | P3_bilingual | 0.31 | en-ru (0.16) | en-de (0.47) |
| wmt n30 | translation_quality | P2_explicit_pivot | 0.26 | en-ru (0.13) | en-de (0.40) |
| wmt n30 | translation_quality | P0_direct_english | 0.22 | en-ru (0.16) | en-de (0.39) |
| wmt n30 | translation_quality | P1_target_rubric | 0.00 | en-de (0.32) | en-ru (0.32) |
| wmt ref-free n30 | translation_quality_ref_free | P0_direct_english | 0.57 | en-ru (0.02) | zh-en (0.60) |
| wmt ref-free n30 | translation_quality_ref_free | P3_bilingual | 0.50 | en-ru (0.18) | en-de (0.68) |
| wmt ref-free n30 | translation_quality_ref_free | P2_explicit_pivot | 0.40 | en-ru (0.04) | en-de (0.44) |
| wmt ref-free n30 | translation_quality_ref_free | P1_target_rubric | 0.28 | en-ru (0.20) | en-de (0.48) |

## Calibration Summary

| Run | Groups | Mean Bal-Acc Delta | Median Bal-Acc Delta |
| --- | --- | --- | --- |
| candidate n50 | 32 | -0.02 | 0.00 |
| gpt-4.1-mini experiment n25 | 32 | -0.03 | -0.00 |
| semantic n30 | 12 | 0.14 | 0.14 |
| wmt n30 | 10 | -0.04 | 0.00 |
| wmt ref-free n30 | 10 | 0.06 | 0.00 |
| wmt experiment zh-en | 2 | -0.05 | -0.05 |
| wmt experiment en-de | 2 | 0.00 | 0.00 |

## Calibration Learning Curve

| Run | Mean Delta n=2 | Mean Delta n=8 | Largest n_cal | Largest-Budget Delta | P(Improve) | P(Degrade) |
| --- | --- | --- | --- | --- | --- | --- |
| candidate n50 | -0.05 | -0.02 | 24 | -0.01 | 0.20 | 0.33 |
| semantic n30 | 0.13 | 0.12 | 24 | 0.14 | 0.61 | 0.11 |
| wmt reference n30 | -0.07 | -0.05 | 24 | -0.04 | 0.00 | 0.18 |
| wmt ref-free n30 | 0.01 | 0.06 | 24 | 0.08 | 0.40 | 0.14 |
| candidate experiment n25 | -0.07 | -0.03 | 16 | -0.02 | 0.23 | 0.35 |

Interpretation: small threshold calibration is useful for the source-grounded semantic setting, mixed for reference-free WMT, and not a reliable fix for candidate-quality form judgments.

## Score Threshold Diagnostic

| Run | Groups | Mean Pos Score | Mean Neg Score | Pred Good @4 | Pos Good @4 | Neg Good @4 | BalAcc @4 | Mode Best Threshold |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| candidate n50 | 32 | 3.56 | 2.78 | 48.2% | 62.6% | 33.9% | 0.64 | 4 |
| semantic n30 | 12 | 2.23 | 1.76 | 8.3% | 10.0% | 6.7% | 0.52 | 2 |
| wmt reference n30 | 10 | 3.95 | 3.55 | 73.3% | 84.0% | 62.7% | 0.61 | 4 |
| wmt ref-free n30 | 10 | 4.70 | 4.19 | 90.0% | 96.0% | 84.0% | 0.56 | 5 |
| candidate experiment n25 | 32 | 4.15 | 3.03 | 58.0% | 76.8% | 40.6% | 0.68 | 4 |

Interpretation: semantic `main_ideas` scores are compressed low, so score >= 4 marks only 8.3% of balanced examples as good and threshold calibration often lowers the cutoff. WMT ref-free scores are compressed high, so threshold 5 is often preferred.

## Run Inventory

| Run | Base Items | Judge Calls | Parse Rate | Observed Cost | Cost / 1k Calls |
| --- | --- | --- | --- | --- | --- |
| candidate n50 | 400 | 1600 | 100.0% | 0.11 | 0.07 |
| candidate experiment n25 | 200 | 800 | 100.0% | 0.14 | 0.18 |
| semantic n30 | 90 | 360 | 100.0% | 0.07 | 0.18 |
| wmt reference n30 | 90 | 300 | 100.0% | 0.03 | 0.10 |
| wmt ref-free n30 | 90 | 300 | 100.0% | 0.02 | 0.07 |
| wmt ref-free experiment | 60 | 120 | 100.0% | 0.02 | 0.18 |

## API Token Inventory

| Run | API Calls | Input Tokens | Output Tokens | Total Tokens | Tokens / Call |
| --- | --- | --- | --- | --- | --- |
| candidate n50 | 2000 | 382769 | 89897 | 472666 | 236.3 |
| candidate experiment n25 | 1005 | 198162 | 48377 | 246539 | 245.3 |
| semantic n30 | 450 | 252403 | 46780 | 299183 | 664.9 |
| wmt reference n30 | 390 | 108238 | 22157 | 130395 | 334.3 |
| wmt ref-free n30 | 300 | 84237 | 13339 | 97576 | 325.3 |
| wmt ref-free experiment | 120 | 32659 | 5649 | 38308 | 319.2 |

Interpretation: token counts come from returned API usage metadata and are stable even if model pricing changes. API calls include translation calls and recorded retries where present.

## Observed API Spend

| Run | Approx Cost USD |
| --- | --- |
| candidate n50 | 0.11 |
| gpt-4.1-mini experiment n25 | 0.14 |
| semantic n30 | 0.07 |
| wmt n30 | 0.03 |
| wmt ref-free n30 | 0.02 |
| wmt ref-free experiment | 0.02 |

## RQ and Contribution Coverage

| Plan Item | Coverage | Evidence | Claim Boundary |
| --- | --- | --- | --- |
| RQ1: judge reliability changes by language | covered | Language gaps are reported per protocol: candidate comprehensibility pivot Spearman gap 0.63; semantic pivot gap 0.51; WMT ref-free direct gap 0.57. | Per-language evidence is strong for current sampled languages, not a universal language ranking. |
| RQ2: evaluation protocol changes the result | covered | Across 17 main-experiment cells, best protocol is not direct in 11, pivot is worst in 10, 6 cells have a significant AUROC pair, and max same-item shift is 1.20. | Protocol sensitivity is the central claim; no single protocol is claimed globally optimal. |
| RQ3: protocol effects differ by quality dimension/task | covered with contrast evidence | Max same-item shifts differ by setting: candidate-quality 1.20, semantic 0.70, WMT reference 0.53, WMT ref-free 0.70. | Dimension story is empirical and bounded; native form-sensitive dimensions remain the clearest risk case. |
| RQ4: small human calibration set | covered as diagnostic | At 24 calibration examples, balanced-accuracy deltas are candidate -0.01, semantic 0.14, and WMT ref-free 0.08. | Calibration is framed as score-distribution diagnosis, not a universal repair. |
| Contribution 1: GlobalJudge-ProtocolBench scaffold | covered for workshop scale | 580 main base items plus 200 candidate experiment items and 60 targeted WMT experiment subset rows; 3480 core prompts across gpt-4.1-mini, gpt-4o-mini; plus 795 modern/P4 follow-up prompts. | Scope is compact and intentionally bounded; larger model-family coverage is future work. |
| Contribution 2: protocol-sensitivity metrics | covered | Tables report Spearman/AUROC, paired AUROC deltas, same-item shifts, language gaps, parse rate, token usage, and cost-per-1k judgments. | Kendall, Pearson, Brier score, and pairwise position-bias tests are not claimed. |
| Contribution 3: calibration recipe | covered with caveat | Repeated stratified threshold calibration uses 50 trials per eligible group and budgets from 2 to 24 calibration examples; threshold diagnostic explains low semantic scores and high WMT ref-free scores. | Post-hoc threshold calibration is included; few-shot calibrated prompting is not run. |
| Contribution 4: Global Judge Reporting Card | covered | Reporting card lists judge configuration, protocol surface, human alignment, protocol sensitivity, calibration, reproducibility, and cost fields. | Checklist is a recommended reporting practice, not a validated standard. |
| Stability and rerun control | covered | 42 exact repeated prompts have 92.9% exact agreement and mean delta 0.07; 14 pivot-pipeline repeats expose regenerated-translation volatility. | The pivot repeat is not a pure stochasticity control because prompt text changed. |
| Cost, parsing, and release traceability | covered | 3480 judge calls, 100.0% minimum parse rate, 1284667 total returned tokens across core paper-facing runs, $0.39 core observed local cost estimate, and 795 modern/P4 follow-up prompts. | Token usage is stable; dollar costs should be refreshed against provider pricing before submission. |

## Draft Result Paragraph

Across 400 candidate-quality SEAHORSE examples, a cheap LLM judge produced materially different scores for the same summaries depending only on the judging protocol. The largest shifts concentrate in target-language form dimensions: for Vietnamese grammar, target-language rubric and explicit English pivot differ by 1.20 points on a 1-5 scale on average, and 34% of items shift by at least two points. English-pivot judging is therefore not a safe default: on Turkish comprehensibility it significantly underperforms direct judging in paired AUROC, and in a stronger n=25 `gpt-4.1-mini` experiment the same failure mode reappears. In source-grounded XLSum `main_ideas`, protocol shifts are smaller, but pivoting remains language-dependent: it is strongest for Spanish, weaker for Turkish than bilingual judging, and chance-level for Vietnamese. A WMT MQM translation-quality extension shows that reference-based direct-vs-pivot differences are smaller, but reference-free MT judging surfaces larger `gpt-4o-mini` protocol effects. A targeted `gpt-4.1-mini` WMT experiment preserves the `zh-en` direct-over-pivot direction but not n=30 significance, and does not reproduce the `en-de` bilingual-over-pivot gain, so WMT is best framed as protocol/model-sensitivity evidence rather than a stable global protocol ranking. These results motivate reporting protocol sensitivity, language gaps, calibration behavior, parse rates, and cost rather than a single multilingual judge score.
