# Repeatability Control

This no-new-API control uses overlapping pilot and main-run response caches.

| Control | Scored Pairs | Identical Prompts | Exact Agreement | Mean Abs Delta | Max Abs Delta | Interpretation |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| exact original-text prompt repeat | 42 | 100.0% | 92.9% | 0.071 | 1 | Same prompt text repeated across independent pilot/main caches; measures ordinary judge run-to-run noise. |
| explicit-pivot pipeline repeat | 14 | 0.0% | 57.1% | 0.643 | 4 | Prompt text changed because the English-pivot pipeline was regenerated; measures pivot-pipeline volatility. |

The exact original-text prompt repeats are the clean judge repeatability control.
The explicit-pivot repeat is a pipeline-repeat control because the prompt text changed between the historical pilot and main run.
