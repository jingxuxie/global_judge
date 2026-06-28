# GlobalJudge Results Brief

This brief is generated from the current analysis CSV/JSONL artifacts. Values are Spearman / AUROC unless noted.

## Claim Boundary

- Strongest claim: multilingual LLM-as-judge conclusions are protocol-sensitive; reporting one aggregate score hides language, dimension, and protocol effects.
- Strong evidence: n=50 candidate-quality SEAHORSE run, n=30 source-grounded XLSum `main_ideas` run, and n=25 `gpt-4.1-mini` audit all show protocol-dependent score or alignment changes.
- Contrast evidence: WMT MQM n=30 per language pair shows smaller direct-vs-pivot shifts for reference-based translation quality, while reference-free MT judging has larger `gpt-4o-mini` protocol effects.
- WMT audit boundary: a targeted `gpt-4.1-mini` audit preserves the `zh-en` pivot-drop direction but not significance at n=30, and does not reproduce the `en-de` bilingual-over-pivot gain.
- Aggregate instability: across 17 non-audit task/language cells, the best AUROC protocol is not direct in 11 cells, explicit pivot is worst in 10 cells, and 6 cells have at least one paired AUROC delta with a bootstrap CI excluding zero.
- Conservative caveat: all current runs use OpenAI judges; target-language rubrics are pilot translations and should be native-checked before final publication claims.

## Dataset Sampling Audit

| Run | Items | Langs | Dims | Pos | Neg | Source Rate | Reference Rate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| candidate n50 | 400 | 4 | 2 | 200 | 200 | 0.0% | 0.0% |
| candidate audit n25 | 200 | 4 | 2 | 96 | 104 | 0.0% | 0.0% |
| semantic n30 | 90 | 3 | 1 | 45 | 45 | 100.0% | 100.0% |
| wmt n30 shared items | 90 | 3 | 1 | 45 | 45 | 100.0% | 100.0% |
| wmt ref-free audit zh-en | 30 | 1 | 1 | 15 | 15 | 100.0% | 100.0% |
| wmt ref-free audit en-de | 30 | 1 | 1 | 15 | 15 | 100.0% | 100.0% |

## Candidate-Quality N=50

| Cell | Direct | Target | Pivot | Bilingual | Paired AUROC Delta | Delta | 95% CI | Mean Abs Shift |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| tr / comprehensibility | 0.603 / 0.836 | 0.556 / 0.810 | 0.331 / 0.686 | 0.575 / 0.822 | pivot - direct | -0.150 | [-0.257, -0.055] | 0.620 |
| vi / comprehensibility | 0.349 / 0.690 | 0.164 / 0.590 | 0.086 / 0.548 | 0.399 / 0.714 | bilingual - pivot | 0.166 | [0.009, 0.317] | 0.960 |
| tr / grammar | -0.022 / 0.488 | -0.088 / 0.454 | -0.076 / 0.458 | -0.072 / 0.462 | pivot - direct | -0.030 | [-0.182, 0.117] | 0.840 |
| vi / grammar | 0.231 / 0.622 | 0.254 / 0.628 | 0.016 / 0.509 | 0.098 / 0.550 | pivot - target | -0.119 | [-0.268, 0.025] | 1.200 |

## Source-Grounded Semantic N=30

| Language | Best Protocol | Best | Direct | Pivot | Bilingual |
| --- | --- | --- | --- | --- | --- |
| es-ES | P2_explicit_pivot | 0.514 / 0.771 | 0.488 / 0.762 | 0.514 / 0.771 | 0.432 / 0.724 |
| tr | P3_bilingual | 0.588 / 0.793 | 0.463 / 0.738 | 0.339 / 0.669 | 0.588 / 0.793 |
| vi | P3_bilingual | 0.195 / 0.607 | 0.143 / 0.576 | 0.000 / 0.500 | 0.195 / 0.607 |

Semantic paired highlights: `tr`, bilingual minus pivot AUROC delta = `+0.124` with 95% CI `[0.000, 0.275]`; `vi`, bilingual minus pivot AUROC delta = `+0.107` with 95% CI `[0.013, 0.220]`.

## Stronger-Judge Audit

| Cell | Direct | Pivot | Bilingual | Pivot-Direct AUROC | Bilingual-Pivot AUROC |
| --- | --- | --- | --- | --- | --- |
| tr / comprehensibility | 0.729 / 0.910 | 0.168 / 0.593 | 0.796 / 0.946 | -0.317 | 0.353 |
| vi / grammar | 0.564 / 0.814 | -0.052 / 0.471 | 0.491 / 0.769 | -0.343 | 0.298 |

## WMT MQM Translation-Quality Contrast

| Pair | Setting | Best Protocol | Best | Direct | Target | Pivot | Bilingual | Pivot-Direct AUROC | 95% CI | Mean Abs Shift |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| en-de | reference | P3_bilingual | 0.471 / 0.689 | 0.388 / 0.673 | 0.318 / 0.596 | 0.398 / 0.678 | 0.471 / 0.689 | 0.004 | [-0.125, 0.136] | 0.200 |
| en-ru | reference | P1_target_rubric | 0.320 / 0.649 | 0.165 / 0.573 | 0.320 / 0.649 | 0.135 / 0.564 | 0.159 / 0.576 | -0.009 | [-0.096, 0.061] | 0.067 |
| zh-en | reference | P0_direct_english | 0.354 / 0.693 | 0.354 / 0.693 | n/a | 0.304 / 0.669 | n/a | -0.024 | [-0.227, 0.177] | 0.533 |
| en-de | ref-free | P3_bilingual | 0.677 / 0.838 | 0.511 / 0.736 | 0.479 / 0.740 | 0.437 / 0.709 | 0.677 / 0.838 | -0.027 | [-0.136, 0.074] | 0.133 |
| en-ru | ref-free | P1_target_rubric | 0.199 / 0.600 | 0.023 / 0.511 | 0.199 / 0.600 | 0.035 / 0.518 | 0.178 / 0.589 | 0.007 | [-0.100, 0.141] | 0.267 |
| zh-en | ref-free | P0_direct_english | 0.595 / 0.820 | 0.595 / 0.820 | n/a | 0.187 / 0.600 | n/a | -0.220 | [-0.440, -0.007] | 0.700 |

## WMT Ref-Free Stronger-Judge Audit

| Cell | Comparison | Protocol A | A | Protocol B | B | B-A AUROC | 95% CI | Mean Abs Shift |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| zh-en ref-free | pivot - direct | direct | 0.503 / 0.773 | pivot | 0.254 / 0.636 | -0.138 | [-0.346, 0.067] | 0.667 |
| en-de ref-free | bilingual - pivot | pivot | 0.563 / 0.784 | bilingual | 0.503 / 0.760 | -0.024 | [-0.086, 0.016] | 0.200 |

Interpretation: the stronger audit supports `zh-en` reference-free direct-over-pivot as a directional robustness check, but the CI crosses zero. The `en-de` bilingual advantage from the main `gpt-4o-mini` reference-free run is model-dependent in this bounded audit.

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
| candidate n50 | 8 | 0.074 | 0.166 | 3/8 | 4/8 | 4/8 | 2/8 | 1.200 |
| semantic n30 | 3 | 0.107 | 0.124 | 2/3 | 3/3 | 2/3 | 1/3 | 0.700 |
| wmt reference n30 | 3 | 0.084 | 0.093 | 0/3 | 2/3 | 2/3 | 0/3 | 0.533 |
| wmt ref-free n30 | 3 | 0.129 | 0.220 | 2/3 | 2/3 | 2/3 | 3/3 | 0.700 |
| candidate audit n25 | 8 | 0.162 | 0.353 | 7/8 | 5/8 | 4/8 | 4/8 | 1.160 |
| wmt ref-free audit | 2 | 0.081 | 0.138 | 1/2 | 1/2 | 1/2 | 0/2 | 0.667 |

## Repeatability Control

| Control | Pairs | Identical Prompts | Exact Agreement | Mean Abs Delta | Max Abs Delta | Interpretation |
| --- | --- | --- | --- | --- | --- | --- |
| exact original-text prompt repeat | 42 | 100.0% | 92.9% | 0.071 | 1 | Same prompt text repeated across independent pilot/main caches; measures ordinary judge run-to-run noise. |
| explicit-pivot pipeline repeat | 14 | 0.0% | 57.1% | 0.643 | 4 | Prompt text changed because the English-pivot pipeline was regenerated; measures pivot-pipeline volatility. |

Interpretation: exact repeated original-text prompts show small ordinary judge run-to-run variation, while regenerated explicit-pivot prompts expose additional pipeline volatility.

## Largest Language Gaps

| Run | Dimension | Protocol | Spearman Gap | Min Lang | Max Lang |
| --- | --- | --- | --- | --- | --- |
| candidate n50 | comprehensibility | P2_explicit_pivot | 0.625 | vi (0.086) | en-US (0.711) |
| candidate n50 | comprehensibility | P1_target_rubric | 0.535 | vi (0.164) | en-US (0.699) |
| candidate n50 | grammar | P3_bilingual | 0.456 | tr (-0.072) | en-US (0.385) |
| semantic n30 | main_ideas | P2_explicit_pivot | 0.514 | vi (0.000) | es-ES (0.514) |
| semantic n30 | main_ideas | P3_bilingual | 0.393 | vi (0.195) | tr (0.588) |
| semantic n30 | main_ideas | P1_target_rubric | 0.357 | vi (0.138) | tr (0.495) |
| wmt n30 | translation_quality | P3_bilingual | 0.312 | en-ru (0.159) | en-de (0.471) |
| wmt n30 | translation_quality | P2_explicit_pivot | 0.264 | en-ru (0.135) | en-de (0.398) |
| wmt n30 | translation_quality | P0_direct_english | 0.223 | en-ru (0.165) | en-de (0.388) |
| wmt n30 | translation_quality | P1_target_rubric | 0.002 | en-de (0.318) | en-ru (0.320) |
| wmt ref-free n30 | translation_quality_ref_free | P0_direct_english | 0.572 | en-ru (0.023) | zh-en (0.595) |
| wmt ref-free n30 | translation_quality_ref_free | P3_bilingual | 0.499 | en-ru (0.178) | en-de (0.677) |
| wmt ref-free n30 | translation_quality_ref_free | P2_explicit_pivot | 0.402 | en-ru (0.035) | en-de (0.437) |
| wmt ref-free n30 | translation_quality_ref_free | P1_target_rubric | 0.280 | en-ru (0.199) | en-de (0.479) |

## Calibration Summary

| Run | Groups | Mean Bal-Acc Delta | Median Bal-Acc Delta |
| --- | --- | --- | --- |
| candidate n50 | 32 | -0.017 | 0.000 |
| gpt-4.1-mini audit n25 | 32 | -0.029 | -0.003 |
| semantic n30 | 12 | 0.136 | 0.136 |
| wmt n30 | 10 | -0.036 | 0.000 |
| wmt ref-free n30 | 10 | 0.059 | 0.000 |
| wmt audit zh-en | 2 | -0.045 | -0.045 |
| wmt audit en-de | 2 | 0.000 | 0.000 |

## Calibration Learning Curve

| Run | Mean Delta n=2 | Mean Delta n=8 | Largest n_cal | Largest-Budget Delta | P(Improve) | P(Degrade) |
| --- | --- | --- | --- | --- | --- | --- |
| candidate n50 | -0.054 | -0.022 | 24 | -0.009 | 0.198 | 0.331 |
| semantic n30 | 0.127 | 0.120 | 24 | 0.136 | 0.612 | 0.112 |
| wmt reference n30 | -0.067 | -0.047 | 24 | -0.041 | 0.000 | 0.180 |
| wmt ref-free n30 | 0.013 | 0.055 | 24 | 0.076 | 0.404 | 0.136 |
| candidate audit n25 | -0.066 | -0.032 | 16 | -0.024 | 0.232 | 0.351 |

Interpretation: small threshold calibration is useful for the source-grounded semantic setting, mixed for reference-free WMT, and not a reliable fix for candidate-quality form judgments.

## Score Threshold Diagnostic

| Run | Groups | Mean Pos Score | Mean Neg Score | Pred Good @4 | Pos Good @4 | Neg Good @4 | BalAcc @4 | Mode Best Threshold |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| candidate n50 | 32 | 3.555 | 2.780 | 48.2% | 62.6% | 33.9% | 0.644 | 4 |
| semantic n30 | 12 | 2.228 | 1.761 | 8.3% | 10.0% | 6.7% | 0.517 | 2 |
| wmt reference n30 | 10 | 3.953 | 3.553 | 73.3% | 84.0% | 62.7% | 0.607 | 4 |
| wmt ref-free n30 | 10 | 4.700 | 4.193 | 90.0% | 96.0% | 84.0% | 0.560 | 5 |
| candidate audit n25 | 32 | 4.148 | 3.026 | 58.0% | 76.8% | 40.6% | 0.681 | 4 |

Interpretation: semantic `main_ideas` scores are compressed low, so score >= 4 marks only 8.3% of balanced examples as good and threshold calibration often lowers the cutoff. WMT ref-free scores are compressed high, so threshold 5 is often preferred.

## Run Inventory

| Run | Base Items | Judge Calls | Parse Rate | Observed Cost | Cost / 1k Calls |
| --- | --- | --- | --- | --- | --- |
| candidate n50 | 400 | 1600 | 100.0% | 0.1114 | 0.070 |
| candidate audit n25 | 200 | 800 | 100.0% | 0.1431 | 0.179 |
| semantic n30 | 90 | 360 | 100.0% | 0.0659 | 0.183 |
| wmt reference n30 | 90 | 300 | 100.0% | 0.0295 | 0.098 |
| wmt ref-free n30 | 90 | 300 | 100.0% | 0.0206 | 0.069 |
| wmt ref-free audit | 60 | 120 | 100.0% | 0.0221 | 0.184 |

## API Token Inventory

| Run | API Calls | Input Tokens | Output Tokens | Total Tokens | Tokens / Call |
| --- | --- | --- | --- | --- | --- |
| candidate n50 | 2000 | 382769 | 89897 | 472666 | 236.3 |
| candidate audit n25 | 1005 | 198162 | 48377 | 246539 | 245.3 |
| semantic n30 | 450 | 252403 | 46780 | 299183 | 664.9 |
| wmt reference n30 | 390 | 108238 | 22157 | 130395 | 334.3 |
| wmt ref-free n30 | 300 | 84237 | 13339 | 97576 | 325.3 |
| wmt ref-free audit | 120 | 32659 | 5649 | 38308 | 319.2 |

Interpretation: token counts come from returned API usage metadata and are stable even if model pricing changes. API calls include translation calls and recorded retries where present.

## Observed API Spend

| Run | Approx Cost USD |
| --- | --- |
| candidate n50 | 0.1114 |
| gpt-4.1-mini audit n25 | 0.1431 |
| semantic n30 | 0.0659 |
| wmt n30 | 0.0295 |
| wmt ref-free n30 | 0.0206 |
| wmt ref-free audit | 0.0221 |

## RQ and Contribution Coverage

| Plan Item | Coverage | Evidence | Claim Boundary |
| --- | --- | --- | --- |
| RQ1: judge reliability changes by language | covered | Language gaps are reported per protocol: candidate comprehensibility pivot Spearman gap 0.625; semantic pivot gap 0.514; WMT ref-free direct gap 0.572. | Per-language evidence is strong for current sampled languages, not a universal language ranking. |
| RQ2: evaluation protocol changes the result | covered | Across 17 non-audit cells, best protocol is not direct in 11, pivot is worst in 10, 6 cells have a significant AUROC pair, and max same-item shift is 1.20. | Protocol sensitivity is the central claim; no single protocol is claimed globally optimal. |
| RQ3: protocol effects differ by quality dimension/task | covered with contrast evidence | Max same-item shifts differ by setting: candidate-quality 1.20, semantic 0.70, WMT reference 0.53, WMT ref-free 0.70. | Dimension story is empirical and bounded; native form-sensitive dimensions remain the clearest risk case. |
| RQ4: small human calibration set | covered as diagnostic | At 24 calibration examples, balanced-accuracy deltas are candidate -0.009, semantic 0.136, and WMT ref-free 0.076. | Calibration is framed as score-distribution diagnosis, not a universal repair. |
| Contribution 1: GlobalJudge-ProtocolBench scaffold | covered for workshop scale | 580 main base items plus 200 candidate audit items and 60 targeted WMT audit subset rows; 3480 prompts across gpt-4.1-mini, gpt-4o-mini. | Scope is compact and intentionally bounded; larger model-family coverage is future work. |
| Contribution 2: protocol-sensitivity metrics | covered | Tables report Spearman/AUROC, paired AUROC deltas, same-item shifts, language gaps, parse rate, token usage, and cost-per-1k judgments. | Kendall, Pearson, Brier score, and pairwise position-bias tests are not claimed. |
| Contribution 3: calibration recipe | covered with caveat | Repeated stratified threshold calibration uses 50 trials per eligible group and budgets from 2 to 24 calibration examples; threshold diagnostic explains low semantic scores and high WMT ref-free scores. | Post-hoc threshold calibration is included; few-shot calibrated prompting is not run. |
| Contribution 4: Global Judge Reporting Card | covered | Reporting card lists judge configuration, protocol surface, human alignment, protocol sensitivity, calibration, reproducibility, and cost fields. | Checklist is a recommended reporting practice, not a validated standard. |
| Stability and rerun control | covered | 42 exact repeated prompts have 92.9% exact agreement and mean delta 0.071; 14 pivot-pipeline repeats expose regenerated-translation volatility. | The pivot repeat is not a pure stochasticity control because prompt text changed. |
| Cost, parsing, and release auditability | covered | 3480 judge calls, 100.0% minimum parse rate, 1284667 total returned tokens across paper-facing runs, and $0.3927 observed local cost estimate. | Token usage is stable; dollar costs should be refreshed against provider pricing before submission. |

## Draft Result Paragraph

Across 400 candidate-quality SEAHORSE examples, a cheap LLM judge produced materially different scores for the same summaries depending only on the judging protocol. The largest shifts concentrate in target-language form dimensions: for Vietnamese grammar, target-language rubric and explicit English pivot differ by 1.20 points on a 1-5 scale on average, and 34% of items shift by at least two points. English-pivot judging is therefore not a safe default: on Turkish comprehensibility it significantly underperforms direct judging in paired AUROC, and in a stronger n=25 `gpt-4.1-mini` audit the same failure mode reappears. In source-grounded XLSum `main_ideas`, protocol shifts are smaller, but pivoting remains language-dependent: it is strongest for Spanish, weaker for Turkish than bilingual judging, and chance-level for Vietnamese. A WMT MQM translation-quality extension shows that reference-based direct-vs-pivot differences are smaller, but reference-free MT judging surfaces larger `gpt-4o-mini` protocol effects. A targeted `gpt-4.1-mini` WMT audit preserves the `zh-en` direct-over-pivot direction but not n=30 significance, and does not reproduce the `en-de` bilingual-over-pivot gain, so WMT is best framed as protocol/model-sensitivity evidence rather than a stable global protocol ranking. These results motivate reporting protocol sensitivity, language gaps, calibration behavior, parse rates, and cost rather than a single multilingual judge score.
