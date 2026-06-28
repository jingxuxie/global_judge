# Submission Packet

This packet turns the current evidence package into submission-facing claims, claim boundaries, reviewer-risk responses, and final pre-submission checks.

## Writing Surfaces

- Immediate extended abstract: `paper/extended_abstract.pdf` (2 pages).
- Full supporting manuscript: `paper/main.pdf` (11 pages).
- Results and response source of truth: `paper/results_brief.md`, `data/analysis/claim_evidence_matrix.md`, and `data/analysis/rq_contribution_matrix.md`.
- Benchmark/data-card source of truth: `paper/globaljudge_protocolbench_datacard.md`.
- Completion audit: `data/analysis/completion_audit.md`.

## One-Sentence Pitch

Multilingual LLM-as-a-judge scores are under-specified unless the paper reports which language the judge saw, which language the rubric used, whether examples were translated, and how sensitive conclusions are to those protocol choices.

## Submission-Ready Claim Boundary

- Claim: multilingual judge conclusions are protocol-sensitive across the current SEAHORSE, source-grounded XLSum, and WMT MQM stress tests.
- Claim: English pivoting is not a safe default; it can hurt human alignment and hide target-language form evidence.
- Claim: reporting should include protocol shifts, language gaps, calibration behavior, parse rate, returned token usage, and cost.
- Do not claim: a universal best protocol, model-family generality beyond current OpenAI judges, native-validated target-language rubrics, or a definitive WMT protocol ranking.

## Key Claim Evidence

| Claim | Evidence | Validator Coverage |
| --- | --- | --- |
| Same-item scores change materially across judge protocols. | vi/grammar target-vs-pivot mean absolute shift 1.20; 34.0% shift by at least 2. | vi grammar shift and large-shift checks |
| English pivot is not a safe default for candidate-quality judging. | tr/comprehensibility direct AUROC 0.836 vs pivot 0.686; pivot-direct delta -0.150 CI [-0.257, -0.055]. | tr direct/pivot Spearman, AUROC, and delta checks |
| The main pivot failure survives a stronger OpenAI judge audit. | gpt-4.1-mini tr/comprehensibility pivot-direct AUROC delta -0.317; bilingual-pivot delta 0.353. | stronger audit tr bilingual-pivot delta check |
| Source-grounded semantic judging is also protocol-sensitive and language-dependent. | tr bilingual-pivot AUROC delta 0.124; vi bilingual-pivot delta 0.107; vi pivot AUROC 0.500. | semantic tr bilingual-pivot delta check |
| WMT is contrast evidence, not a stable global protocol ranking. | reference zh-en pivot-direct delta -0.024; ref-free zh-en delta -0.220; stronger audit zh-en delta -0.138; stronger audit en-de bilingual-pivot delta -0.024. | WMT ref-free zh-en delta check plus required audit artifacts |
| No single protocol dominates across cells. | 17 non-audit cells; best protocol not direct in 11; pivot worst in 10; significant AUROC pair in 6. | aggregate instability count checks |
| Calibration is a diagnostic, not a universal fix. | semantic largest-budget balanced-accuracy delta 0.136; candidate n50 delta -0.009; semantic score>=4 good-rate 8.3%; WMT ref-free score>=4 good-rate 90.0%. | calibration curve and score-threshold checks |
| Large protocol shifts exceed ordinary exact-prompt repeat variation. | 42 exact repeated prompts; exact agreement 92.9%; mean absolute score delta 0.071. | repeatability count, agreement, and mean-delta checks |
| The run package is auditable for sampling, prompts, parse rate, usage, and cost. | candidate n50 sampling 200/200 pos/neg; 1600 candidate prompts; 100.0% parse rate; 472666 candidate total tokens. | sampling, prompt inventory, parse-rate, token, and manifest checks |

## RQ and Contribution Coverage

| Plan Item | Coverage | Claim Boundary |
| --- | --- | --- |
| RQ1: judge reliability changes by language | covered | Per-language evidence is strong for current sampled languages, not a universal language ranking. |
| RQ2: evaluation protocol changes the result | covered | Protocol sensitivity is the central claim; no single protocol is claimed globally optimal. |
| RQ3: protocol effects differ by quality dimension/task | covered with contrast evidence | Dimension story is empirical and bounded; native form-sensitive dimensions remain the clearest risk case. |
| RQ4: small human calibration set | covered as diagnostic | Calibration is framed as score-distribution diagnosis, not a universal repair. |
| Contribution 1: GlobalJudge-ProtocolBench scaffold | covered for workshop scale | Scope is compact and intentionally bounded; larger model-family coverage is future work. |
| Contribution 2: protocol-sensitivity metrics | covered | Kendall, Pearson, Brier score, and pairwise position-bias tests are not claimed. |
| Contribution 3: calibration recipe | covered with caveat | Post-hoc threshold calibration is included; few-shot calibrated prompting is not run. |
| Contribution 4: Global Judge Reporting Card | covered | Checklist is a recommended reporting practice, not a validated standard. |
| Stability and rerun control | covered | The pivot repeat is not a pure stochasticity control because prompt text changed. |
| Cost, parsing, and release auditability | covered | Token usage is stable; dollar costs should be refreshed against provider pricing before submission. |

## Reviewer Risk Responses

| Reviewer Risk | Response Strategy | Evidence Artifact |
| --- | --- | --- |
| Only OpenAI judges are tested. | State this directly. The main claim is protocol sensitivity within realistic API judge workflows, not model-family universality. The gpt-4.1-mini audits show the failure mode survives a stronger OpenAI judge. | paper/main.tex limitations; data/analysis/rq_contribution_matrix.md |
| Target-language rubrics are not native-speaker validated. | Frame target-rubric results as pilot protocol evidence. The strongest pivot-failure claim does not depend on target-language rubric superiority because direct-vs-pivot and bilingual-vs-pivot comparisons carry the key signal. | paper/main.tex limitations; data/analysis/claim_evidence_matrix.md |
| WMT results look mixed. | Use WMT as a boundary condition. Reference-based MT has smaller shifts; reference-free MT exposes larger gpt-4o-mini effects; the stronger audit narrows the claim to protocol/model sensitivity rather than a global ranking. | paper/tables/wmt_translation_quality.tex; paper/tables/wmt_ref_free_stronger_audit.tex |
| Calibration is not a positive universal contribution. | Do not sell calibration as a repair. Present it as a score-threshold diagnostic that helps semantic main-ideas but remains mixed or negative in other settings. | data/analysis/calibration_learning_curve_summary.csv; paper/tables/score_threshold_diagnostic.tex |
| A single aggregate score may hide small cells. | Lean on per-language tables, paired bootstrap intervals, same-item shifts, language gaps, sampling audit, and the claim-evidence matrix instead of aggregate-only claims. | paper/tables/language_gaps.tex; data/analysis/dataset_sampling_audit.md |
| Cost estimates may change before submission. | Report returned token usage as stable accounting. Treat dollar amounts as local run-time estimates and refresh provider pricing before camera-ready release. | data/analysis/run_inventory.csv; paper/tables/api_usage_inventory.tex |
| Prompt examples might leak copyrighted or benchmark item text. | Use the redacted prompt inventory for public appendix text. The validator checks representative prompt redaction markers and known leaked strings. | data/analysis/prompt_inventory.md; src/validate_paper_claims.py |

## Audit Snapshot

- Manifest files recorded: 213.
- Paper-facing judge calls: 3480.
- Minimum parse rate across paper-facing runs: 100.0%.
- Returned total tokens across paper-facing runs: 1284667.
- Observed local cost estimate across paper-facing runs: $0.3927.

## Final Pre-Submission Checks

- Apply the target venue template if required; the current extended abstract is template-neutral.
- Refresh dollar-cost estimates against current provider pricing; keep token counts unchanged unless rerunning calls.
- Native-check target-language rubric translations before making strong claims about target-language prompting.
- Include or link the benchmark data card when sharing the artifact package.
- If time and budget allow, add a non-OpenAI judge-family audit; otherwise keep the current model-family limitation prominent.
- Run `make -C paper`, `/home/eston/anaconda3/envs/global_judge/bin/python src/validate_paper_claims.py`, and `/home/eston/anaconda3/envs/global_judge/bin/python src/run_release_checks.py` immediately before submission.
