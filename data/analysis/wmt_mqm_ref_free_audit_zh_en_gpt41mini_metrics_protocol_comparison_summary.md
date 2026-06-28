# Protocol Comparison Summary

## Largest score shifts

```text
language                    dimension        protocol_a        protocol_b  n  mean_abs_score_shift  score_disagreement_rate  large_shift_rate_abs_ge_2  mean_score_delta_b_minus_a
   zh-en translation_quality_ref_free P0_direct_english P2_explicit_pivot 30              0.666667                      0.5                   0.166667                         0.4
```

## Largest paired AUROC deltas

```text
language                    dimension        protocol_a        protocol_b  n  auroc_delta_b_minus_a  auroc_delta_ci_low  auroc_delta_ci_high  auroc_prob_delta_gt_0
   zh-en translation_quality_ref_free P0_direct_english P2_explicit_pivot 30              -0.137778           -0.346172             0.067181                  0.097
```

## Largest language gaps

```text
                   dimension          protocol  mean_spearman min_spearman_language  min_spearman max_spearman_language  max_spearman  spearman_language_gap  auroc_language_gap
translation_quality_ref_free P0_direct_english       0.502711                 zh-en      0.502711                 zh-en      0.502711                    0.0                 0.0
translation_quality_ref_free P2_explicit_pivot       0.254498                 zh-en      0.254498                 zh-en      0.254498                    0.0                 0.0
```
