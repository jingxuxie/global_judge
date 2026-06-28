# Global Judge Reporting Card

Use this checklist when reporting multilingual LLM-as-a-judge results.

## Judge Configuration

- Judge model and exact API/model identifier.
- Decoding settings.
- Response format and parse-failure handling.
- Date of API run.

## Protocol Surface

- Language of the task input.
- Language of the candidate output.
- Language of the rubric.
- Whether the source text, candidate output, reference, or rubric was translated.
- Whether translations were produced by the same model family as the judge.
- Whether the judge saw original target-language text for grammar, fluency, politeness, register, or other form-sensitive dimensions.

## Human Alignment

- Per-language alignment with human labels.
- Per-dimension alignment with human labels.
- Confidence intervals or bootstrap intervals.
- AUROC/accuracy threshold definition if binary labels are used.

## Protocol Sensitivity

- Same-item score shifts between protocols.
- Largest score-shift cells.
- Whether the best protocol differs by language or dimension.
- Language gap for each protocol.

## Calibration

- Calibration split size.
- Calibration method.
- Held-out calibration improvement or degradation.
- Whether calibration changes the main conclusion.

## Reproducibility and Cost

- Dataset split and sampling seed.
- Number of base items and number of judge calls.
- Prompt templates or prompt-generation code.
- Parse rate and invalid-output policy.
- Approximate cost per run and cost per 1,000 judgments.
