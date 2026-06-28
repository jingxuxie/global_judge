# Protocol Comparison Summary

## Largest score shifts

```text
language                    dimension        protocol_a   protocol_b  n  mean_abs_score_shift  score_disagreement_rate  large_shift_rate_abs_ge_2  mean_score_delta_b_minus_a
   en-de translation_quality_ref_free P2_explicit_pivot P3_bilingual 30                   0.2                      0.2                        0.0                   -0.133333
```

## Largest paired AUROC deltas

```text
language                    dimension        protocol_a   protocol_b  n  auroc_delta_b_minus_a  auroc_delta_ci_low  auroc_delta_ci_high  auroc_prob_delta_gt_0
   en-de translation_quality_ref_free P2_explicit_pivot P3_bilingual 30              -0.024444           -0.085656             0.015625                  0.145
```

## Largest language gaps

```text
                   dimension          protocol  mean_spearman min_spearman_language  min_spearman max_spearman_language  max_spearman  spearman_language_gap  auroc_language_gap
translation_quality_ref_free P2_explicit_pivot       0.563489                 en-de      0.563489                 en-de      0.563489                    0.0                 0.0
translation_quality_ref_free      P3_bilingual       0.503278                 en-de      0.503278                 en-de      0.503278                    0.0                 0.0
```
