# Concrete Research Plan: Multilingual LLM-as-a-Judge Is Not a Global Judge

**Target venue:** Generative AI for the World: Workshop on Globalizing Tasks, Evaluations, and Systems at COLM 2026  
**Recommended submission type:** 2-page extended abstract if submitting immediately; 5-page short paper if you can spend 1–2 more weeks strengthening experiments  
**Compute assumption:** no local LLMs; limited API budget around $100  
**Core paper type:** evaluation/protocol paper, not model-training paper

---

## 0. One-sentence paper idea

> **LLM-as-a-judge results can change substantially depending on the language of the task, the language of the rubric, whether examples are translated into English, and whether a small human calibration set is used; therefore, global benchmarks should report judge-protocol sensitivity instead of a single judge score.**

---

## 1. Recommended working title

Use one of these:

1. **Do Not Let English Judge the World: Protocol Sensitivity in Multilingual LLM-as-a-Judge Evaluation**
2. **Same Answer, Different Language, Different Grade: Multilingual Instability in LLM-as-a-Judge Evaluation**
3. **GlobalJudge Protocols: Calibrating LLM Judges for Multilingual Evaluation**
4. **When the Judge Is Not Global: Measuring and Calibrating Multilingual LLM-as-a-Judge Failures**

My favorite is:

> **Do Not Let English Judge the World: Protocol Sensitivity in Multilingual LLM-as-a-Judge Evaluation**

It is memorable, workshop-aligned, and clearly signals the contribution.

---

## 2. Why this can be a high-impact workshop paper

The workshop asks for work on:

- globalizing tasks;
- evaluation beyond performance;
- annotation standards across languages and cultures;
- global users’ vulnerabilities and workarounds;
- systems not bound to a single language or culture.

This topic fits because many papers and products now rely on LLM-as-a-judge, but a single English-centered judge can distort multilingual evaluation. Prior work already shows LLM-as-a-judge is useful but biased, and recent multilingual work finds weak cross-language consistency. Your opportunity is to make the next step practical:

> **Not just “LLM judges are unreliable,” but “here is how benchmark builders should test, report, and calibrate multilingual judge reliability under a small budget.”**

That practical protocol angle is what can make the paper stand out.

---

## 3. Core research questions

### RQ1. Does judge reliability change by language?

For the same evaluation task, do LLM judges correlate less with human labels in some languages than others?

### RQ2. Does the evaluation protocol change the result?

Compare these protocols:

1. **Direct multilingual judging:** original task text and candidate output are judged directly.
2. **English-pivot judging:** non-English inputs/outputs are translated into English, then judged.
3. **Target-language rubric:** the rubric is translated into the task language.
4. **Bilingual rubric:** the rubric contains both English and the task language.
5. **Calibrated judging:** a small human-labeled calibration split is used to correct judge scores or thresholds.

### RQ3. Are some protocols better for some quality dimensions?

Hypothesis:

- English-pivot judging may work better for semantic dimensions such as “main idea captured.”
- Direct or target-language judging may be necessary for grammar, fluency, politeness, register, and target-language appropriateness.
- Bilingual rubrics may improve robustness but not eliminate language-specific failures.

### RQ4. How much human calibration is enough?

Can 25, 50, or 100 human-labeled examples per language substantially reduce wrong conclusions?

You can use existing human-labeled datasets for this, so you do not need to pay annotators.

---

## 4. Main contribution package

Aim to contribute four things.

### Contribution 1: A protocol comparison benchmark

Create a small, clean benchmark called something like:

> **GlobalJudge-ProtocolBench**

It does not need to be huge. A high-quality small benchmark is better than a large noisy one.

Recommended size for a first submission:

| Version | Items | Languages | Tasks | Judge models | Protocols |
|---|---:|---:|---:|---:|---:|
| 2-page emergency version | 300–500 | 3–4 | 1–2 | 2 | 3 |
| Strong short paper | 800–1,500 | 4–6 | 2 | 2–3 | 4–5 |
| Ambitious long paper | 2,000–5,000 | 6+ | 2–3 | 3–5 | 5+ |

### Contribution 2: Protocol-sensitivity metrics

Report not just correlation with human labels, but:

- by-language correlation;
- by-protocol correlation;
- cross-protocol score shifts;
- language gap;
- calibration improvement;
- invalid JSON / malformed judge-output rate;
- cost per 1,000 judgments.

### Contribution 3: A small calibration recipe

Show that a small human-labeled calibration set can make LLM judge reporting more honest. You can do this with existing human labels by pretending that only a small calibration split is labeled.

### Contribution 4: A “Global Judge Reporting Card”

End the paper with a concrete checklist for future benchmark papers:

- Which judge model?
- Which language was the rubric written in?
- Was the judged answer translated?
- Was correlation reported separately by language?
- Was a calibration set used?
- Were confidence intervals reported?
- Were target-language quality dimensions judged in the target language?
- Was position bias tested for pairwise judgments?
- Were costs reported?

This checklist is likely to be appreciated by workshop reviewers because it turns your findings into a reusable evaluation practice.

---

## 5. Recommended datasets

Use existing datasets with human judgments. This avoids annotation cost and makes the paper credible.

### Dataset A: SEAHORSE — multilingual summarization evaluation

**Why use it:** It has human ratings for multilingual summaries across multiple quality dimensions.

Useful dimensions:

- comprehensibility;
- repetition;
- grammar;
- attribution;
- main ideas;
- conciseness.

Use it to test whether judge protocols behave differently for semantic versus language-form dimensions.

Suggested languages from the dataset:

- English (`en-US`) as anchor;
- Spanish (`es-ES`) as high-resource non-English;
- German (`de`) or Russian (`ru`) as another high-resource language;
- Turkish (`tr`) or Vietnamese (`vi`) as a typologically different / underrepresented option.

Recommended subset:

- 4 languages × 100 examples × 3 dimensions = 1,200 judge units.
- For a faster version: 3 languages × 50 examples × 2 dimensions = 300 judge units.

Source: SEAHORSE paper and repository.

### Dataset B: WMT Metrics Shared Task / MT Metrics Eval

**Why use it:** It has source sentences, machine translation outputs, references, and human ratings/MQM annotations. It is a natural fit for evaluating whether LLM-as-a-judge can replace human translation quality evaluation.

Good language pairs:

- English→German;
- Chinese→English;
- Hebrew→English;
- any WMT pair available with MQM/human scores.

Recommended subset:

- 3 language pairs × 100 segments × 2 candidate systems = 600 judge units.
- For a faster version: 2 pairs × 50 segments × 2 systems = 200 judge units.

Use both:

1. **reference-based judging:** source + candidate + reference;
2. **reference-free judging:** source + candidate only.

### Optional Dataset C: Native/cultural mini-set

Only do this if you have native-speaker expertise or collaborators.

Create 60–120 examples in one language where an answer is semantically correct but culturally/register inappropriate.

Example categories:

- too informal for a professor/elder/official;
- wrong honorifics;
- overly direct English-style request;
- wrong locale assumption;
- inappropriate translation of proper nouns;
- incorrect local administrative format.

This mini-set can make the paper more workshop-specific, but do not do it unless labels are trustworthy.

---

## 6. Minimal viable experiment design

### 6.1 Recommended minimal version

Use:

- **SEAHORSE only**
- 4 languages: `en-US`, `es-ES`, `tr`, `vi`
- 2 dimensions:
  - `main ideas` = semantic/content dimension
  - `grammar` or `comprehensibility` = language-form dimension
- 100 examples per language
- 2 judge models
- 4 protocols:
  - direct;
  - English pivot;
  - target-language rubric;
  - bilingual rubric.

This gives:

```text
4 languages × 100 examples × 2 dimensions × 2 judge models × 4 protocols
= 6,400 judge calls
```

That sounds large, but each call can be short. You can halve it by using 50 examples per language:

```text
4 × 50 × 2 × 2 × 4 = 3,200 judge calls
```

This should fit within a $100 API budget if you use mostly cheap models and reserve strong models for a subset.

### 6.2 Stronger version

Use both SEAHORSE and WMT:

```text
SEAHORSE:
4 languages × 100 examples × 2 dimensions = 800 base units

WMT:
3 language pairs × 100 segments × 2 systems = 600 base units

Total base units = 1,400
```

Run:

```text
1,400 base units × 4 protocols × 2 judge models = 11,200 judge calls
```

If this is too expensive or slow, run the full protocol suite on one judge model and a smaller subset on the stronger judge model.

---

## 7. Judge protocols to compare

This is the heart of the paper.

### Protocol P0: Direct multilingual judging

Input is kept in its original language. The rubric is in English.

**Example structure:**

```text
You are evaluating a candidate summary.

Dimension: Main ideas.
Question: Does the summary capture the main idea(s) of the source text?

Source text:
{source_text_in_original_language}

Candidate summary:
{candidate_summary_in_original_language}

Give a score from 1 to 5.
Return JSON only.
```

This tests the common lazy practice: use an English evaluation prompt for everything.

### Protocol P1: Target-language rubric

Translate the rubric into the task language.

For Spanish:

```text
Eres un evaluador de resúmenes.

Dimensión: Ideas principales.
Pregunta: ¿El resumen captura las ideas principales del texto fuente?

Texto fuente:
{source_text_spanish}

Resumen candidato:
{candidate_summary_spanish}

Da una puntuación de 1 a 5.
Devuelve solo JSON.
```

This tests whether judges improve when the evaluation frame matches the task language.

### Protocol P2: English-pivot judging

Translate source and candidate into English first, then judge in English.

```text
Original language: Turkish

English translation of source:
{translated_source}

English translation of candidate summary:
{translated_summary}

Evaluate whether the candidate captures the main ideas of the source.
Give a score from 1 to 5.
Return JSON only.
```

This tests a common workaround: translate everything into English because the judge is assumed to be better in English.

Important caveat: English-pivot judging may destroy evidence about grammar, fluency, register, and target-language appropriateness. That is not a bug in your experiment; it is one of your main points.

### Protocol P3: Bilingual rubric

Rubric includes both English and target-language wording.

```text
You are evaluating a candidate summary in Vietnamese.

Evaluation dimension / Tiêu chí đánh giá:
Main ideas / Ý chính

Question / Câu hỏi:
Does the summary capture the main idea(s) of the source text?
Bản tóm tắt có nắm bắt được các ý chính của văn bản nguồn không?

Source text:
{source_text_vietnamese}

Candidate summary:
{candidate_summary_vietnamese}

Score from 1 to 5.
Return JSON only.
```

This tests whether bilingual instructions reduce ambiguity.

### Protocol P4: Calibrated judging

Use a small labeled calibration set per language and dimension.

Two variants:

#### P4a. Post-hoc calibration

1. Run judge normally.
2. On a small calibration split, fit a mapping from judge scores to human labels.
3. Apply the mapping to the test split.
4. Report corrected estimates and confidence intervals.

This is cleaner than putting labeled examples in the prompt because it avoids prompt-length cost and makes the statistical procedure explicit.

#### P4b. Few-shot calibrated prompt

Put 3–5 labeled examples in the prompt before the test item.

This can work but is more expensive and may overfit to examples. Use it only as a secondary experiment if time allows.

---

## 8. Judge-output format

Use strict JSON to simplify analysis.

### Scalar score format

```json
{
  "score": 1,
  "label": "bad",
  "confidence": 0.64,
  "rationale_brief": "The summary omits the main event and adds unsupported details."
}
```

### Pairwise format

```json
{
  "winner": "A",
  "confidence": 0.72,
  "rationale_brief": "A preserves the main claim while B contradicts the source."
}
```

Keep rationales short. Do not request long chain-of-thought. Long rationales increase cost and can introduce verbosity bias.

---

## 9. Recommended judge models

Because you do not have local models, use API models.

### Minimal model set

Use two judge models:

1. **Cheap/main judge:** a low-cost model you can run over the full benchmark.
2. **Strong/audit judge:** a stronger model run on a subset.

This lets you say:

> “We evaluate whether the protocol effect appears both for an economical judge and for a stronger judge.”

### Better model set

Use three judge models:

1. low-cost OpenAI judge;
2. strong OpenAI judge;
3. non-OpenAI judge, such as Claude or Gemini, if you have access.

This helps avoid making a claim about only one model family.

### Model-selection principle

Do **not** over-focus on which model is best. The paper is about **protocol sensitivity**. Your main message is:

> “Even if a judge model is strong, benchmark conclusions depend on the judging protocol.”

---

## 10. API budget plan

### 10.1 Cost formula

Use this spreadsheet-style formula:

```text
total_calls = num_items × num_protocols × num_judges × num_repeats
input_tokens = total_calls × avg_input_tokens_per_call
output_tokens = total_calls × avg_output_tokens_per_call
cost = input_tokens/1e6 × input_price + output_tokens/1e6 × output_price
```

### 10.2 Example budget

Assume:

```text
num_items = 800
num_protocols = 4
num_judges = 2
num_repeats = 1
avg_input_tokens = 900
avg_output_tokens = 60
```

Then:

```text
total_calls = 800 × 4 × 2 = 6,400
input_tokens ≈ 5.76M
output_tokens ≈ 0.384M
```

Even with a moderately expensive model, this is usually feasible under $100. If you use one cheap model for the full run and one stronger model for a 25–50% subset, you should have room for reruns and translation.

### 10.3 Cost controls

- Truncate long source documents to the minimum needed.
- Run a 50-example pilot before full evaluation.
- Cache all API responses.
- Use deterministic settings.
- Do not ask for long rationales.
- Use batch APIs if available.
- Run the strongest judge only on the subset used for your main statistical claims.

---

## 11. Sampling strategy

Your paper will be stronger if you sample intentionally.

### SEAHORSE sampling

For each language and dimension:

1. Sort examples by human rating.
2. Sample:
   - low-quality examples;
   - medium-quality examples;
   - high-quality examples.
3. Avoid a dataset dominated by obvious good/bad examples.

Recommended per language:

```text
25 low + 25 medium + 25 high = 75 examples
```

For 4 languages:

```text
4 × 75 = 300 examples per dimension
```

For 2 dimensions:

```text
600 base examples
```

### WMT sampling

For each language pair:

1. Select 50–100 source segments.
2. For each segment, include candidate translations from two systems:
   - one high-scoring system;
   - one lower-scoring system.
3. Keep references when testing reference-based mode.
4. Hide system identity from the judge.

---

## 12. Metrics

### 12.1 Human-alignment metrics

For each dataset, language, dimension, judge model, and protocol, compute:

- Spearman correlation with human score;
- Kendall correlation with human score;
- Pearson correlation if scores are approximately interval-scaled;
- AUROC if converted to binary good/bad;
- accuracy/F1 after thresholding;
- Brier score if using confidence.

### 12.2 Protocol-sensitivity metrics

Define:

```text
ProtocolShift(Pa, Pb) = mean_i | score_i,Pa - score_i,Pb|
```

Also compute:

```text
LanguageGap(P) = max_lang corr(P, lang) - min_lang corr(P, lang)
```

And:

```text
PivotGain(lang, dimension) = corr(EnglishPivot, lang, dimension) - corr(Direct, lang, dimension)
```

These metrics let you make concrete claims like:

> “English-pivot judging improves main-idea correlation in Turkish by X but reduces grammar correlation by Y.”

### 12.3 Calibration metrics

Split labeled data into:

```text
calibration split: 20%
test split: 80%
```

Use the calibration split to estimate:

- per-language thresholds;
- per-dimension thresholds;
- sensitivity/specificity if binary;
- score normalization parameters if scalar.

Report:

- uncalibrated correlation/accuracy;
- calibrated correlation/accuracy;
- confidence intervals using bootstrap.

### 12.4 Stability metrics

Run a small subset twice with the same model and protocol.

Compute:

- exact-score agreement;
- mean absolute difference;
- rank stability;
- invalid-output rate.

This is optional but useful.

---

## 13. Main figures and tables

A high-quality workshop paper can be built around 3–4 strong visuals.

### Figure 1: Protocol × language heatmap

Rows: languages  
Columns: judge protocols  
Cell: correlation with human labels

This is likely your main figure.

### Figure 2: Dimension-specific protocol effect

Bar plot showing English-pivot gain/loss by dimension:

- main ideas;
- grammar;
- comprehensibility;
- conciseness.

Expected story:

- English pivot may help semantic judgments.
- English pivot may harm language-form judgments.

### Figure 3: Calibration effect

Before/after calibration:

- uncalibrated judge;
- calibrated judge with 25 examples;
- calibrated judge with 50 examples;
- calibrated judge with 100 examples.

Metric: error or confidence interval width.

### Figure 4: Qualitative failure cases

Show 3–5 examples:

1. direct judge underrates a good non-English summary;
2. English-pivot hides a grammar/fluency problem;
3. target-language rubric changes score;
4. bilingual rubric resolves ambiguity;
5. calibration changes a wrong benchmark conclusion.

### Table 1: Experimental setup

Include languages, datasets, dimensions, model names, protocols, number of examples, and approximate API cost.

### Table 2: Global Judge Reporting Card

A checklist for future papers.

---

## 14. Statistical testing

Do not overcomplicate this, but include enough rigor.

### Recommended tests

1. **Bootstrap confidence intervals**
   - Resample items within language.
   - Compute correlation for each resample.
   - Report 95% CI.

2. **Paired bootstrap for protocol differences**
   - Compare protocol A and B on the same items.
   - Report whether the difference excludes zero.

3. **Multiple comparisons**
   - You do not need heavy correction for a workshop paper.
   - State that the study is exploratory.
   - Emphasize effect sizes and confidence intervals.

### Practical implementation

Use Python:

```python
from scipy.stats import spearmanr, kendalltau
import numpy as np

def bootstrap_corr(y_true, y_pred, n=1000, seed=0):
    rng = np.random.default_rng(seed)
    vals = []
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    for _ in range(n):
        idx = rng.integers(0, len(y_true), len(y_true))
        vals.append(spearmanr(y_true[idx], y_pred[idx]).correlation)
    return np.percentile(vals, [2.5, 50, 97.5])
```

---

## 15. Concrete repository structure

Set up your project like this:

```text
globaljudge-protocols/
  README.md
  data/
    raw/
    processed/
    prompts/
    responses/
    analysis/
  src/
    download_seahorse.py
    download_wmt.py
    sample_items.py
    build_prompts.py
    run_judges.py
    parse_responses.py
    calibrate.py
    analyze.py
    plot_figures.py
  paper/
    main.tex
    references.bib
    figures/
    tables/
  configs/
    experiment_small.yaml
    experiment_full.yaml
  logs/
```

### Standard data schema

Use JSONL.

```json
{
  "item_id": "seahorse-es-000123",
  "dataset": "seahorse",
  "language": "es-ES",
  "task": "summarization_eval",
  "dimension": "main_ideas",
  "source_text": "...",
  "candidate_output": "...",
  "reference": null,
  "human_score": 0.82,
  "human_label": "good",
  "metadata": {
    "model_that_generated_candidate": "...",
    "split": "test"
  }
}
```

### Prompt schema

```json
{
  "prompt_id": "seahorse-es-000123__main_ideas__P3_bilingual",
  "item_id": "seahorse-es-000123",
  "protocol": "P3_bilingual",
  "judge_model": "JUDGE_MODEL_NAME",
  "messages": [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."}
  ]
}
```

### Response schema

```json
{
  "prompt_id": "seahorse-es-000123__main_ideas__P3_bilingual",
  "judge_model": "JUDGE_MODEL_NAME",
  "raw_response": "...",
  "score": 4,
  "label": "good",
  "confidence": 0.71,
  "parse_success": true,
  "api_cost_estimate": 0.00042,
  "timestamp": "..."
}
```

---

## 16. Prompt templates

### 16.1 Direct English-rubric prompt

```text
System:
You are a careful evaluator. You must judge only the candidate output using the provided rubric. Return valid JSON only.

User:
Task: multilingual summarization evaluation
Language of source and candidate: {language}

Evaluation dimension: {dimension}
Rubric:
1 = very poor
2 = poor
3 = acceptable
4 = good
5 = excellent

Question:
{dimension_question}

Source text:
{source_text}

Candidate output:
{candidate_output}

Return JSON only:
{
  "score": integer from 1 to 5,
  "label": "bad" | "borderline" | "good",
  "confidence": number from 0 to 1,
  "rationale_brief": string of at most 25 words
}
```

### 16.2 English-pivot prompt

```text
System:
You are a careful evaluator. You must judge only the candidate output using the provided rubric. Return valid JSON only.

User:
The original language is {language}. The text below has been translated into English for evaluation.

Evaluation dimension: {dimension}
Rubric:
1 = very poor
2 = poor
3 = acceptable
4 = good
5 = excellent

Question:
{dimension_question}

English translation of source text:
{source_text_english_translation}

English translation of candidate output:
{candidate_output_english_translation}

Important:
You are evaluating meaning preservation in the English translations. Do not evaluate target-language grammar or style because it is not visible after translation.

Return JSON only:
{
  "score": integer from 1 to 5,
  "label": "bad" | "borderline" | "good",
  "confidence": number from 0 to 1,
  "rationale_brief": string of at most 25 words
}
```

### 16.3 Target-language rubric prompt

Use this for languages where you trust the rubric translation.

```text
System:
{target_language_system_instruction}

User:
{target_language_task_description}

{target_language_rubric}

{target_language_question}

{target_language_source_label}:
{source_text}

{target_language_candidate_label}:
{candidate_output}

{target_language_json_instruction}
```

### 16.4 Bilingual rubric prompt

```text
System:
You are a careful bilingual evaluator. Return valid JSON only.

User:
Task / Tarea: multilingual summarization evaluation / evaluación multilingüe de resúmenes
Language / Idioma: {language}

Evaluation dimension / Dimensión de evaluación:
{dimension_english} / {dimension_target_language}

Question / Pregunta:
{question_english}
{question_target_language}

Rubric / Rúbrica:
1 = very poor / muy deficiente
2 = poor / deficiente
3 = acceptable / aceptable
4 = good / bueno
5 = excellent / excelente

Source text:
{source_text}

Candidate output:
{candidate_output}

Return JSON only:
{
  "score": integer from 1 to 5,
  "label": "bad" | "borderline" | "good",
  "confidence": number from 0 to 1,
  "rationale_brief": string of at most 25 words
}
```

---

## 17. Calibration method

### 17.1 Simple scalar calibration

For each language and dimension:

1. Use calibration split.
2. Fit linear mapping:

```text
human_score ≈ a_lang,dim × judge_score + b_lang,dim
```

3. Apply to test split.
4. Clip to valid range.

This is easy and works for scalar labels.

### 17.2 Threshold calibration

If using binary labels:

1. Convert human labels:
   - good if human score ≥ threshold;
   - bad otherwise.
2. On calibration split, choose judge-score threshold that maximizes F1 or balanced accuracy.
3. Apply threshold to test split.

### 17.3 Sensitivity/specificity correction

For binary labels, estimate on calibration split:

```text
sensitivity = P(judge says good | human good)
specificity = P(judge says bad | human bad)
```

Then use these to correct aggregate good-rate estimates. This is especially useful if you want to say:

> “A naive LLM-judge score would rank language A above language B, but after calibration the confidence intervals overlap.”

### 17.4 Bootstrap CIs

For every key number, report a confidence interval.

For example:

```text
Spanish, direct protocol, main-ideas dimension:
Spearman ρ = 0.42 [0.31, 0.54]
```

This makes the paper look much more serious than a table of point estimates.

---

## 18. Main claims to test

Do not write the paper as if you already know the answers. Frame these as hypotheses.

### H1. Protocol sensitivity exists.

The same judge model gives meaningfully different scores depending on whether the item is judged directly, translated to English, or judged with a target-language/bilingual rubric.

### H2. Language gaps persist under strong judges.

Even stronger judge models have uneven reliability across languages.

### H3. English pivot is not universally better.

English-pivot judging may improve some semantic evaluations, but it is inappropriate for dimensions that depend on the target language itself.

### H4. Small calibration improves reporting.

A small calibration set can reduce misleading benchmark-level conclusions and produce better uncertainty estimates.

### H5. Single global judge scores are under-reported.

Most evaluation reports should not publish one aggregate LLM-judge score without language-level and protocol-level analysis.

---

## 19. What results would be publishable?

The paper is worth submitting if you find at least one of the following:

1. **Protocol gap:** A protocol changes human correlation by ≥0.10 Spearman for at least one language/dimension.
2. **Language gap:** Best-to-worst language gap ≥0.15 Spearman under the same judge/protocol.
3. **Dimension reversal:** English pivot helps semantic dimensions but hurts grammar/fluency dimensions.
4. **Calibration benefit:** 50–100 calibration examples reduce error or narrow uncertainty enough to change conclusions.
5. **Judge-family disagreement:** Two judges rank protocols differently, showing that protocol recommendations should be tested, not assumed.
6. **Qualitative failures:** Clear examples where English-centric judging makes an obviously wrong evaluation.

If your pilot finds no major effect, pivot to:

> “When are multilingual judges reliable? A negative result with a reporting protocol.”

A well-done negative result can still be useful, but you need strong statistical care.

---

## 20. 72-hour submission plan

Use this if the deadline is imminent.

### Day 1: Dataset and pilot

**Goal:** Prove the experiment works end to end.

Tasks:

- Download SEAHORSE.
- Select 3 languages.
- Select 50 examples per language.
- Select 2 dimensions: main ideas + grammar/comprehensibility.
- Build P0 direct, P2 English-pivot, P3 bilingual prompts.
- Run 1 cheap judge model.
- Parse JSON responses.
- Compute correlations with human labels.
- Make one heatmap.

Deliverable by end of Day 1:

```text
A table with language × protocol correlations.
```

### Day 2: Full run and analysis

**Goal:** Add strength and repeatability.

Tasks:

- Expand to 4 languages.
- Run second judge model on either all data or a 50% subset.
- Add bootstrap confidence intervals.
- Add qualitative failure cases.
- Add cost table.
- Start writing method and results.

Deliverable by end of Day 2:

```text
3 figures + 1 table + 3 qualitative examples.
```

### Day 3: Write submission

**Goal:** Submit a polished 2-page extended abstract.

Tasks:

- Write title, abstract, intro, method, results, discussion.
- Add limitations and broader-impact statement.
- Add appendix with prompts and dataset details.
- Prepare anonymized code/data release if possible.
- Check page limit and double-blind requirements.

Deliverable:

```text
2-page extended abstract + references + appendix + broader-impact statement.
```

---

## 21. Two-week stronger plan

### Days 1–2: Finalize protocol and data

- Decide languages.
- Download SEAHORSE and WMT data.
- Build clean JSONL.
- Run a 50-item pilot.
- Freeze prompt templates.

### Days 3–5: Main API runs

- Run cheap judge on all items.
- Run strong judge on subset.
- Run translations for English-pivot protocol.
- Cache all outputs.
- Start parsing and sanity checks.

### Days 6–8: Analysis

- Compute correlations.
- Compute protocol shifts.
- Compute language gaps.
- Run calibration experiments.
- Bootstrap CIs.
- Make figures.

### Days 9–10: Robustness

- Add pairwise judging for a subset.
- Add A/B swap to estimate position bias.
- Check invalid-output rate.
- Test if findings hold after truncation or different thresholds.

### Days 11–12: Writing

- Write full 5-page version.
- Add related work.
- Add limitations.
- Add Global Judge Reporting Card.

### Days 13–14: Polish

- Clean figures.
- Verify all claims.
- Anonymize repository.
- Ask one colleague/native speaker to sanity-check examples.
- Submit.

---

## 22. Paper outline

### Abstract

Structure:

1. LLM-as-a-judge is widely used for scalable evaluation.
2. Global benchmarks increasingly use it across languages.
3. We show that judge conclusions are sensitive to protocol choices.
4. We compare direct, English-pivot, target-language, bilingual, and calibrated protocols on multilingual human-labeled evaluation datasets.
5. We find language- and dimension-specific failures.
6. We recommend protocol-sensitivity reporting and small calibration sets.

### Introduction

Make the problem vivid:

> A benchmark builder evaluates Spanish, Turkish, Vietnamese, and English model outputs using the same English LLM-judge prompt. The resulting table looks objective. But is the score lower because the model output is worse, or because the judge/rubric protocol is worse for that language?

Then state your thesis:

> Global evaluation should treat the judging protocol as an experimental variable.

### Related work

Briefly cover:

- LLM-as-a-judge and known biases;
- multilingual LLM-as-a-judge consistency;
- multilingual summarization/translation evaluation datasets;
- calibration and uncertainty in LLM-judge reporting.

### Method

Describe:

- datasets;
- languages;
- quality dimensions;
- protocols;
- judge models;
- scoring;
- calibration;
- statistics.

### Results

Organize by research questions:

1. Protocol sensitivity.
2. Language gaps.
3. Dimension-specific pivot effects.
4. Calibration gains.
5. Qualitative failure cases.

### Discussion

Translate results into recommendations:

- Do not report only aggregate judge scores.
- Report per-language judge-human agreement.
- Do not use English pivot for target-language form/style dimensions.
- Use a calibration set.
- Include prompt/rubric language in benchmark cards.

### Limitations

Be explicit:

- Existing datasets do not represent all languages or communities.
- Human labels are themselves culturally situated.
- Translation-pivot results depend on translation quality.
- API models change over time.
- No local model evaluation due to compute constraints.
- Findings are about evaluation protocols, not absolute model quality.

### Broader impact / ethics

State:

- The work aims to reduce inequitable evaluation practices.
- Misuse risk: readers might over-trust calibrated LLM judges.
- Calibration is not a replacement for local human expertise.
- Global evaluation should involve speakers and stakeholders from evaluated communities.

---

## 23. Draft abstract

You can adapt this.

> **Abstract.** LLM-as-a-judge is increasingly used to evaluate open-ended model outputs, but global benchmarks often apply a single judge prompt across languages. We study whether multilingual LLM-judge conclusions are stable under realistic protocol choices: direct source-language judging, English-pivot judging, target-language rubrics, bilingual rubrics, and small-set calibration. Using multilingual human-labeled summarization and translation evaluation data, we measure judge-human agreement, language gaps, protocol-induced score shifts, and calibration effects across multiple languages and judge models. We find that judge reliability is not only model-dependent but protocol-dependent: English-pivot judging can improve semantic judgments while obscuring target-language quality dimensions, and direct English-rubric judging can produce uneven agreement across languages. Small calibration sets reduce some misleading aggregate conclusions but do not remove the need for language-level reporting. We propose a Global Judge Reporting Card for multilingual evaluation, arguing that global benchmarks should report judge protocol, rubric language, per-language agreement, and calibration uncertainty rather than a single aggregate LLM-judge score.

---

## 24. Recommended title/abstract/contribution phrasing

### Claim to avoid

Avoid:

> “LLM judges are bad for multilingual evaluation.”

Too broad and already partially known.

### Stronger claim

Use:

> “LLM-judge reliability is a joint property of model, language, quality dimension, and judging protocol. Global benchmarks should therefore report protocol sensitivity and calibration uncertainty.”

This is more nuanced and publishable.

### Contribution wording

Use:

> “We introduce a protocol-sensitivity evaluation for multilingual LLM-as-a-judge, comparing direct, pivoted, target-language, bilingual, and calibrated judging.”

Not:

> “We introduce a new large benchmark.”

Unless you actually release one.

---

## 25. Risk management

### Risk 1: API budget runs out

Reduce to:

```text
3 languages × 50 examples × 2 dimensions × 3 protocols × 1 judge
= 900 calls
```

This is enough for a pilot paper if the findings are clear.

### Risk 2: Dataset loading is painful

Use SEAHORSE only. It is simpler than WMT.

### Risk 3: Translation quality confounds English-pivot protocol

Treat this as part of the protocol. Say:

> “English-pivot judging evaluates a realistic workflow in which non-English evaluation is mediated by translation.”

Also include a small manual spot-check of 20 translations if possible.

### Risk 4: No native-speaker validation

Do not create new cultural/register labels. Stick to datasets with existing human labels. In limitations, state that future work should add community-led evaluation.

### Risk 5: Judge outputs malformed JSON

Run a repair parser, but track invalid-output rate. Invalid-output rate is itself a result.

### Risk 6: Results are noisy

Use bootstrap CIs and phrase claims carefully. A workshop paper can be exploratory if the method is clean.

---

## 26. What to submit for the workshop

### For a 2-page extended abstract

Include:

- motivation;
- one dataset;
- 3–4 languages;
- 2 judge models or 1 judge + strong subset;
- 3 protocols;
- one main heatmap;
- one protocol-shift figure;
- one calibration mini-result;
- Global Judge Reporting Card.

### For a 5-page short paper

Include:

- SEAHORSE + WMT;
- 4–6 languages/pairs;
- 2–3 judge models;
- 4–5 protocols;
- full calibration;
- qualitative examples;
- cost analysis.

### For a 9-page long paper

Add:

- native/cultural mini-set;
- pairwise vs scalar judging;
- position-bias swapping;
- multiple calibration sizes;
- release benchmark and code.

---

## 27. Recommended final paper contributions

Use this exact structure in the introduction:

> We make three contributions:
>
> 1. **Protocol-sensitivity benchmark.** We evaluate multilingual LLM-as-a-judge under direct, English-pivot, target-language, bilingual, and calibrated protocols using human-labeled multilingual evaluation data.
> 2. **Empirical analysis.** We show that judge-human agreement varies by language, quality dimension, and protocol; in particular, English-pivot judging is not uniformly better and can hide target-language quality failures.
> 3. **Reporting recommendation.** We propose a Global Judge Reporting Card requiring benchmark papers to disclose rubric language, translation use, per-language judge-human agreement, calibration size, uncertainty, and cost.

---

## 28. Suggested references to cite

Use these as starting references.

### Workshop

- Generative AI for the World: Workshop on Globalizing Tasks, Evaluations, and Systems at COLM 2026  
  https://sites.google.com/view/genai4world/
- Call for Papers  
  https://sites.google.com/view/genai4world/call-for-papers

### LLM-as-a-judge

- Zheng et al. 2023. *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena.* NeurIPS Datasets and Benchmarks.  
  https://papers.nips.cc/paper_files/paper/2023/hash/91f18a1287b398d378ef22505bf41832-Abstract-Datasets_and_Benchmarks.html
- Li et al. 2025. *From Generation to Judgment: Opportunities and Challenges of LLM-as-a-judge.*  
  https://llm-as-a-judge.github.io/
- Fu and Liu / Fu et al. 2025. *How Reliable is Multilingual LLM-as-a-Judge?*  
  https://arxiv.org/html/2505.12201v1
- Lee et al. 2026. *How to Correctly Report LLM-as-a-Judge Evaluations.*  
  https://arxiv.org/abs/2511.21140

### Datasets

- Clark et al. 2023. *SEAHORSE: A Multilingual, Multifaceted Dataset for Summarization Evaluation.*  
  https://arxiv.org/abs/2305.13194
- SEAHORSE repository  
  https://github.com/google-research-datasets/seahorse
- WMT Metrics Shared Task  
  https://wmt-metrics-task.github.io/
- MT Metrics Eval toolkit  
  https://github.com/google-research/mt-metrics-eval

### API pricing references

Use current official pricing pages when finalizing your budget:

- OpenAI API pricing  
  https://openai.com/api/pricing/
- Anthropic pricing  
  https://docs.anthropic.com/en/docs/about-claude/pricing
- Gemini API pricing  
  https://ai.google.dev/gemini-api/docs/pricing

---

## 29. Immediate next actions

Do these in order.

### Step 1: Choose scope

Pick one:

```text
Fast 2-page:
SEAHORSE only, 4 languages, 2 dimensions, 3 protocols, 1–2 judges.

Strong 5-page:
SEAHORSE + WMT, 4–6 languages/pairs, 4 protocols, 2–3 judges, calibration.
```

### Step 2: Build the data

Create `items.jsonl` with:

- item ID;
- dataset;
- language;
- source;
- candidate;
- human score;
- dimension;
- split.

### Step 3: Build prompts

Generate prompts for:

- P0 direct;
- P2 English pivot;
- P3 bilingual;
- P4 calibrated/post-hoc.

### Step 4: Run a 50-item pilot

Before full spending, check:

- responses parse correctly;
- scores vary;
- correlations are not all undefined;
- token counts are reasonable.

### Step 5: Run full experiment

Cache everything.

### Step 6: Analyze

Produce:

- heatmap;
- protocol-shift plot;
- calibration plot;
- failure examples.

### Step 7: Write the paper

Use the draft abstract and outline above.

---

## 30. My recommended final scope for you

Given your constraints, I recommend:

```text
Dataset: SEAHORSE only for the initial submission
Languages: en-US, es-ES, tr, vi
Dimensions: main ideas + grammar/comprehensibility
Examples: 75 per language
Judge models: cheap judge full run + strong judge 25–50% subset
Protocols: direct English rubric, English pivot, target-language rubric, bilingual rubric
Calibration: 20% calibration split, 80% test split
```

This gives a clean, credible paper with no local compute and no paid annotation.

Your central figure should be:

```text
Spearman correlation with human labels
by language × protocol × dimension
```

Your central takeaway should be:

> “The evaluation protocol is an unreported variable in multilingual LLM-as-a-judge evaluation. Global benchmarks should treat it as part of the experimental design, not as an implementation detail.”

