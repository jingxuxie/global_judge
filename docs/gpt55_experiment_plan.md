# Additional Experiment Plan for the Global Judge Paper

**Paper:** *Do Not Let English Judge the World: Protocol Sensitivity in Multilingual LLM-as-a-Judge Evaluation*  
**Goal:** Strengthen the paper without local LLMs or large compute by adding a modern frontier-judge audit, a cost/quality model comparison, and one mitigation protocol.

---

## 1. Current paper status

The current draft already has a strong core result: multilingual LLM-as-a-judge scores depend on the judge protocol, especially when the evaluation dimension depends on target-language form.

The current experimental package appears to contain:

- Main candidate-quality run: 400 base examples, 1,600 judge responses, four protocols, `gpt-4o-mini`.
- Source-grounded semantic run: 90 base examples, 360 judge responses, four protocols, `gpt-4o-mini`.
- WMT MQM reference and reference-free runs: 90 base examples each, 600 combined judge responses, mostly `gpt-4o-mini`.
- Stronger audit: 200 base candidate-quality examples, 800 judge responses, `gpt-4.1-mini`.
- Targeted WMT reference-free audit: 60 base examples, 120 judge responses, `gpt-4.1-mini`.

The main weakness is not the number of examples. The main weakness is that the judge-model story is dated and narrow: most results are from one older low-cost judge, with a limited `gpt-4.1-mini` audit. The highest-impact next step is therefore **not** to add many more datasets. It is to show whether the central protocol-sensitivity claim survives with a current frontier judge and a current cheap judge.

---

## 2. Recommended headline addition

Add a new section to the paper:

> **Modern-Judge Audit: Protocol Sensitivity Persists Under GPT-5.5**

Run a focused or full rerun using:

1. `gpt-5.5` as the frontier modern judge.
2. `gpt-5.4-mini` as the current cheap judge.
3. Optional: `gpt-5.5-pro` on only the highest-sensitivity cells if you have enough budget.

The strongest possible claim is:

> “Protocol sensitivity is not an artifact of `gpt-4o-mini` or `gpt-4.1-mini`: the same English-pivot failure mode appears under GPT-5.5 on target-language form dimensions.”

A more cautious but still publishable result is:

> “Modern judges reduce some protocol gaps but do not eliminate the need to report protocol sensitivity; model choice changes which protocol appears best.”

Either outcome strengthens the paper.

---

## 3. Budget estimate

Using the token inventory currently reported in the repo, a full rerun of the existing paper-facing calls is surprisingly affordable with current OpenAI pricing.

Approximate standard short-context costs using the current token counts:

| Run | Input tokens | Output tokens | `gpt-5.5` est. | `gpt-5.4-mini` est. | `gpt-5.5-pro` est. |
|---|---:|---:|---:|---:|---:|
| Candidate n50 | 382,769 | 89,897 | $4.61 | $0.69 | $27.66 |
| Candidate audit n25 | 198,162 | 48,377 | $2.44 | $0.37 | $14.65 |
| Semantic n30 | 252,403 | 46,780 | $2.67 | $0.40 | $15.99 |
| WMT reference n30 | 108,238 | 22,157 | $1.21 | $0.18 | $7.24 |
| WMT ref-free n30 | 84,237 | 13,339 | $0.82 | $0.12 | $4.93 |
| WMT ref-free audit | 32,659 | 5,649 | $0.33 | $0.05 | $2.00 |
| **Full existing suite** | **1,058,468** | **226,199** | **$12.08** | **$1.81** | **$72.47** |

These estimates use the standard short-context price table available in the OpenAI API docs on June 28, 2026: `gpt-5.5` at $5/M input and $30/M output, `gpt-5.4-mini` at $0.75/M input and $4.50/M output, and `gpt-5.5-pro` at $30/M input and $180/M output. Refresh the numbers before final submission.

**Practical recommendation:** Run the full existing suite with `gpt-5.5` and `gpt-5.4-mini`. Run `gpt-5.5-pro` only on the high-sensitivity subset.

---

## 4. Experiment priority list

### Priority A — Full modern-judge rerun

**Purpose:** Upgrade the paper from “older OpenAI mini judge shows protocol sensitivity” to “current frontier and current cheap judges still require protocol reporting.”

**Run:**

- Same items.
- Same protocols.
- Same prompts except model name and any model-specific API settings.
- Same structured JSON output.
- Temperature 0 or lowest available deterministic setting.
- Record exact model ID, API date, prompt file hash, response cache hash, and usage metadata.

**Minimum:**

- Run `gpt-5.5` on the 200-item candidate audit subset.
- Run `gpt-5.5` on the WMT reference-free audit subset.

**Best:**

- Run `gpt-5.5` on the full existing suite.
- Run `gpt-5.4-mini` on the full existing suite.
- Run `gpt-5.5-pro` on only these four cells:
  - Turkish comprehensibility: direct, pivot, bilingual.
  - Vietnamese grammar: direct, target, pivot, bilingual.
  - Vietnamese comprehensibility: direct, pivot, bilingual.
  - WMT `zh-en` reference-free: direct vs pivot.

**Main metrics:**

- Spearman and AUROC by language/dimension/protocol/model.
- Pivot-minus-direct paired AUROC delta.
- Bilingual-minus-pivot paired AUROC delta.
- Mean absolute same-item score shift.
- Cross-language Spearman gap.
- Cost per 1,000 judgments.

**Main table to add:**

| Cell | Judge | Direct | Pivot | Bilingual | Pivot - Direct AUROC | Bilingual - Pivot AUROC | Shift |
|---|---|---:|---:|---:|---:|---:|---:|
| tr / comprehensibility | gpt-4.1-mini | existing | existing | existing | existing | existing | existing |
| tr / comprehensibility | gpt-5.5 | new | new | new | new | new | new |
| vi / grammar | gpt-4.1-mini | existing | existing | existing | existing | existing | existing |
| vi / grammar | gpt-5.5 | new | new | new | new | new | new |
| zh-en ref-free | gpt-4.1-mini | existing | existing | n/a | existing | n/a | existing |
| zh-en ref-free | gpt-5.5 | new | new | n/a | new | n/a | new |

**Interpretation rules:**

- If `gpt-5.5` still fails on pivot for Turkish/Vietnamese form dimensions, make this a headline result.
- If `gpt-5.5` fixes some cells but not others, frame protocol sensitivity as model-dependent and therefore reportable.
- If `gpt-5.5` fixes all high-sensitivity cells, the paper is still strong: “frontier judges mitigate but do not justify hidden protocols; older cheap judges remain widely used, and model version materially changes conclusions.”

---

### Priority B — Add one mitigation protocol: evidence-preserving bilingual judge

The paper currently diagnoses a problem. Add a small mitigation so reviewers see a constructive contribution.

**New protocol:** `P4_evidence_preserving_bilingual`

**Prompt idea:**

1. Tell the judge that target-language form evidence must be evaluated in the original text, not from an English translation.
2. Ask the judge to quote the exact original-language evidence before scoring.
3. Ask the judge to separate semantic adequacy from target-language form.
4. Require JSON fields:
   - `target_language_evidence`
   - `semantic_evidence`
   - `score`
   - `label`
   - `confidence`
   - `rationale`

**Run only on high-sensitivity cells:**

- Turkish comprehensibility.
- Vietnamese grammar.
- Vietnamese comprehensibility.
- Optional: source-grounded Vietnamese main ideas.

**Expected contribution:**

This can become a new table:

| Cell | Best old protocol | Pivot AUROC | Bilingual AUROC | P4 AUROC | P4 gain over pivot | P4 shift vs pivot |
|---|---:|---:|---:|---:|---:|---:|

**How to describe it:**

> “A simple evidence-preserving bilingual prompt reduces the worst pivot failures, suggesting that the problem is not only judge capability but also missing protocol specification.”

This turns the paper from purely diagnostic into actionable evaluation guidance.

---

### Priority C — Translation-pipeline ablation

The current results show that explicit pivot can fail, but reviewers may ask whether the problem is the judge or the translation.

Add a small ablation:

1. Use the current pivot translations already cached.
2. Generate new pivot translations with `gpt-5.5` for only the high-sensitivity subset.
3. Judge both versions with the same judge model.

**Minimal cells:**

- Turkish comprehensibility: 25 or 50 examples.
- Vietnamese grammar: 25 or 50 examples.

**Report:**

- Translation version agreement.
- Pivot-score difference between old translation and `gpt-5.5` translation.
- Whether pivot remains worse than original-text judging.

**Interpretation:**

- If better translations fix pivot, the paper can say “translation quality is part of judge protocol and must be reported.”
- If better translations do not fix pivot, the paper can say “even high-quality pivoting can remove target-language evidence.”

---

### Priority D — Native-speaker validation of rubrics and qualitative examples

This is not compute-heavy and will make the paper much more credible.

**Do this for 20–40 examples total:**

- 10 Turkish comprehensibility cases.
- 10 Vietnamese grammar/comprehensibility cases.
- Optional: 10 Spanish main-ideas cases.

Ask a native speaker or fluent annotator to answer:

1. Is the human label plausible?
2. Does the target-language rubric translation preserve the intended criterion?
3. Did the pivot translation remove or introduce the relevant error?
4. Which protocol rationale is most faithful to the original text?

**Add to paper:**

- One paragraph in Methods: “rubric and qualitative validation.”
- One table with 3–4 examples.
- One sentence in Limitations clarifying the validation scale.

This will reduce reviewer concern that the target-language rubric translations are ad hoc.

---

### Priority E — Pairwise judging as a robustness baseline

Scalar 1–5 scores can be poorly calibrated across languages. Add a small pairwise judge condition.

**Task:** Given two candidate summaries for the same source/language, ask which is better under the dimension.

**Construction:**

- Pair one human-positive and one human-negative item within the same language/dimension when possible.
- Run direct, pivot, and bilingual pairwise protocols.
- Evaluate accuracy against the human-positive item.

**Run size:**

- 25 pairs per high-sensitivity cell.
- 3 cells × 3 protocols × 2 judges = 450 calls if using two judges.

**Why it helps:**

If pairwise judging is less protocol-sensitive, you can recommend pairwise comparisons for multilingual evaluation. If it is also protocol-sensitive, your core claim becomes stronger.

---

## 5. Proposed final experiment matrix

Use this as the final scope if time and budget allow.

| Experiment | Models | Data | Calls | Priority | Paper value |
|---|---|---:|---:|---|---|
| Full modern rerun | `gpt-5.5`, `gpt-5.4-mini` | existing full suite | about 5,000–5,200 each including translation calls | Must do | Upgrades model story |
| Frontier-pro audit | `gpt-5.5-pro` | 3–4 high-sensitivity cells | about 300–600 | Optional | Strongest robustness check |
| Evidence-preserving P4 | `gpt-5.5` | 3 high-sensitivity cells | about 300–600 | Must do if possible | Adds mitigation |
| Translation-pipeline ablation | `gpt-5.5` translator + judge | 2 cells | about 200–400 | Good | Separates translation vs judging |
| Native validation | humans | 20–40 examples | no API | High value | Improves credibility |
| Pairwise judging | `gpt-5.5` and/or `gpt-5.4-mini` | 3 cells | about 225–450 | Optional | Alternative protocol |

---

## 6. Concrete implementation checklist

### Step 1 — Freeze current artifacts

Create a manifest row for every current run:

- item file path
- prompt file path
- response cache path
- analysis table path
- model ID
- run date
- temperature/settings
- prompt hash
- response hash
- token usage

Do this before running new models so the paper can claim reproducibility.

### Step 2 — Add model argument to the run scripts

The scripts should support:

```bash
python src/run_judge.py \
  --items data/processed/candidate_n50.jsonl \
  --protocols P0_direct_english P1_target_rubric P2_explicit_pivot P3_bilingual \
  --model gpt-5.5 \
  --output runs/candidate_n50_gpt55.jsonl
```

Use the equivalent existing script names in the repo.

### Step 3 — Preserve prompt identity

For the modern rerun, do not edit the old prompts except for unavoidable model/API formatting. You want a clean model comparison:

- same items
- same protocol definitions
- same output schema
- same analysis code
- different judge model

For P4, create new prompt files and label them explicitly as mitigation prompts.

### Step 4 — Run smoke tests

For each model and protocol:

- run 5 examples
- check JSON parse rate
- check scores are in [1, 5]
- check labels are valid
- check language-specific fields are not empty
- check token usage is logged

### Step 5 — Run full or focused batch

Recommended order:

1. `gpt-5.4-mini` full suite.
2. `gpt-5.5` candidate n50.
3. `gpt-5.5` semantic n30.
4. `gpt-5.5` WMT ref-free n30.
5. `gpt-5.5` WMT reference n30.
6. P4 mitigation on high-sensitivity cells.
7. Optional `gpt-5.5-pro` high-sensitivity audit.

### Step 6 — Regenerate tables

Add these tables:

1. `modern_judge_audit.tex`
2. `model_sensitivity_summary.tex`
3. `p4_mitigation.tex`
4. updated `api_usage_inventory.tex`
5. updated `api_costs.tex`

### Step 7 — Update manuscript claims

Add or revise:

- Abstract: mention `gpt-5.5` audit if run.
- Methods: add “Modern-judge audit” and “Mitigation protocol.”
- Results: add one subsection after the current stronger-judge audit.
- Analysis: update recommendations based on P4 and model comparison.
- Limitations: if still only OpenAI models, say so clearly.

---

## 7. New paper subsection templates

### Modern-judge audit subsection

```latex
\subsection{Modern Judges Reduce Some Gaps but Do Not Eliminate Protocol Sensitivity}

To test whether the observed protocol effects are artifacts of older low-cost judges, we rerun the existing protocol comparison with \texttt{gpt-5.5} and \texttt{gpt-5.4-mini}. The audit preserves the original items, rubric surfaces, output schema, and analysis code. [Insert result summary.] On the highest-sensitivity target-language form cells, explicit English pivot remains worse than original-text or bilingual judging under [model], with [delta] AUROC on [cell]. [If fixed, say: the direction changes under GPT-5.5, showing that reported conclusions depend on judge version as well as protocol.] These results strengthen the central recommendation: multilingual judge papers should report the judge model/version and protocol-sensitivity diagnostics rather than a single aggregate score.
```

### P4 mitigation subsection

```latex
\subsection{Evidence-Preserving Bilingual Judging as a Lightweight Mitigation}

We test a simple mitigation protocol that requires the judge to cite original-language evidence before assigning a score. This protocol is designed for form-sensitive dimensions, where English pivoting can remove the very evidence needed for evaluation. On [cells], P4 improves over explicit pivot by [delta] AUROC and reduces same-item score shifts by [amount]. This does not make P4 universally optimal, but it shows that protocol design can reduce failures without training a new judge.
```

---

## 8. Decision tree for final claims

### Case 1: GPT-5.5 reproduces pivot failure

Use the strongest framing:

> “Even current frontier judges are protocol-sensitive. English pivoting remains unsafe for target-language form dimensions.”

### Case 2: GPT-5.5 fixes target-language form but GPT-5.4-mini does not

Use the practical deployment framing:

> “Protocol sensitivity is model-dependent. Because many evaluation pipelines use cheaper judges, benchmark papers must report model/version and protocol sensitivity.”

### Case 3: GPT-5.5 and GPT-5.4-mini both reduce most failures

Use the historical and reporting framing:

> “Modern judges mitigate some failures, but the paper’s main point remains: protocol choice and judge version can change conclusions, so they must be reported.”

### Case 4: P4 beats existing protocols

Make P4 a contribution:

> “A lightweight evidence-preserving bilingual protocol reduces target-language form failures.”

### Case 5: P4 does not help

Still useful:

> “Prompt-level mitigation alone is insufficient; protocol reporting remains necessary.”

---

## 9. What not to do

Do not spend time on:

- training local LLMs;
- expanding to many more languages without validation;
- adding more figures before stabilizing the table layout;
- running GPT-5.5 on new data before rerunning the exact existing suite;
- claiming GPT-5.5 results in the paper before the cache, token usage, and analysis tables are committed.

---

## 10. Submission-ready contribution after these experiments

After the recommended experiments, the paper can claim four things:

1. **Diagnosis:** multilingual LLM-as-a-judge evaluation is protocol-sensitive.
2. **Boundary:** the effect is strongest for target-language form, smaller for some semantic/reference-based settings, and model-dependent for WMT.
3. **Robustness:** modern judges still require protocol reporting, or at minimum change the protocol ranking enough that judge version must be reported.
4. **Mitigation:** evidence-preserving bilingual judging is a cheap protocol-level mitigation for high-risk cells.

This would make the paper substantially stronger for a GenAI-for-the-world workshop because it moves from “here is an artifact in one model” to “here is an auditable evaluation practice for multilingual benchmarks.”

---

## 11. Minimal final table set for the paper

To keep formatting clean, use only these tables in the main paper:

1. Dataset/run summary.
2. Candidate-quality protocol sensitivity.
3. Modern-judge audit.
4. Semantic + WMT boundary results.
5. Protocol-instability summary.
6. Optional P4 mitigation table.

Move everything else to appendix:

- prompt inventory;
- repeatability control;
- language gaps;
- calibration summary;
- calibration learning curve;
- score-threshold diagnostics;
- run inventory;
- API usage and cost.

Do not include all heatmaps in the main TeX. Keep them as repo artifacts or include only one if the page budget allows.

---

## 12. Source notes

- OpenAI API model/pricing docs accessed June 28, 2026: https://platform.openai.com/docs/models and https://platform.openai.com/docs/pricing
- The cost estimates above are approximate and should be recomputed from actual returned token usage after each run.
