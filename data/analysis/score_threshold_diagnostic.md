# Score Threshold Diagnostic

This no-new-API diagnostic summarizes how raw 1-5 judge scores interact with the fixed score >= 4 baseline threshold used by the calibration analyses.

| Run | Groups | Mean Pos Score | Mean Neg Score | Pred Good @4 | Pos Good @4 | Neg Good @4 | BalAcc @4 | Mode Best Threshold |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| candidate n50 | 32 | 3.555 | 2.780 | 48.3% | 62.6% | 33.9% | 0.644 | 4 |
| semantic n30 | 12 | 2.228 | 1.761 | 8.3% | 10.0% | 6.7% | 0.517 | 2 |
| wmt reference n30 | 10 | 3.953 | 3.553 | 73.3% | 84.0% | 62.7% | 0.607 | 4 |
| wmt ref-free n30 | 10 | 4.700 | 4.193 | 90.0% | 96.0% | 84.0% | 0.560 | 5 |
| candidate audit n25 | 32 | 4.148 | 3.026 | 58.0% | 76.8% | 40.6% | 0.681 | 4 |

Interpretation:
- Source-grounded semantic `main_ideas` scores are compressed low: score >= 4 marks only a small fraction of balanced examples as good, and the modal best in-group threshold is 2.
- WMT reference-free scores are compressed high: score >= 4 marks most examples as good, and the modal best in-group threshold is 5.
- These diagnostics explain why threshold calibration helps semantic `main_ideas`, is mixed for WMT reference-free, and is not a universal repair for protocol sensitivity.
