# Protocol Comparison Summary

## Largest score shifts

```text
language                    dimension        protocol_a        protocol_b  n  mean_abs_score_shift  score_disagreement_rate  large_shift_rate_abs_ge_2  mean_score_delta_b_minus_a
   zh-en translation_quality_ref_free P0_direct_english P2_explicit_pivot 30              0.700000                 0.533333                   0.133333                   -0.033333
   en-ru translation_quality_ref_free P0_direct_english P2_explicit_pivot 30              0.266667                 0.266667                   0.000000                   -0.200000
   en-ru translation_quality_ref_free  P1_target_rubric P2_explicit_pivot 30              0.266667                 0.266667                   0.000000                   -0.066667
   en-ru translation_quality_ref_free P2_explicit_pivot      P3_bilingual 30              0.233333                 0.233333                   0.000000                    0.100000
   en-de translation_quality_ref_free P0_direct_english  P1_target_rubric 30              0.133333                 0.133333                   0.000000                   -0.133333
   en-de translation_quality_ref_free  P1_target_rubric      P3_bilingual 30              0.133333                 0.133333                   0.000000                    0.000000
   en-de translation_quality_ref_free  P1_target_rubric P2_explicit_pivot 30              0.133333                 0.133333                   0.000000                    0.066667
   en-de translation_quality_ref_free P0_direct_english      P3_bilingual 30              0.133333                 0.133333                   0.000000                   -0.133333
   en-de translation_quality_ref_free P0_direct_english P2_explicit_pivot 30              0.133333                 0.133333                   0.000000                   -0.066667
   en-de translation_quality_ref_free P2_explicit_pivot      P3_bilingual 30              0.133333                 0.133333                   0.000000                   -0.066667
   en-ru translation_quality_ref_free P0_direct_english  P1_target_rubric 30              0.133333                 0.133333                   0.000000                   -0.133333
   en-ru translation_quality_ref_free P0_direct_english      P3_bilingual 30              0.100000                 0.100000                   0.000000                   -0.100000
```

## Largest paired AUROC deltas

```text
language                    dimension        protocol_a        protocol_b  n  auroc_delta_b_minus_a  auroc_delta_ci_low  auroc_delta_ci_high  auroc_prob_delta_gt_0
   zh-en translation_quality_ref_free P0_direct_english P2_explicit_pivot 30              -0.220000           -0.440292            -0.006737                  0.022
   en-de translation_quality_ref_free P2_explicit_pivot      P3_bilingual 30               0.128889            0.024865             0.257781                  0.984
   en-de translation_quality_ref_free P0_direct_english      P3_bilingual 30               0.102222            0.002262             0.215368                  0.978
   en-de translation_quality_ref_free  P1_target_rubric      P3_bilingual 30               0.097778            0.000000             0.213012                  0.972
   en-ru translation_quality_ref_free P0_direct_english  P1_target_rubric 30               0.088889            0.009050             0.192026                  0.981
   en-ru translation_quality_ref_free  P1_target_rubric P2_explicit_pivot 30              -0.082222           -0.236860             0.062500                  0.135
   en-ru translation_quality_ref_free P0_direct_english      P3_bilingual 30               0.077778            0.000000             0.178571                  0.953
   en-ru translation_quality_ref_free P2_explicit_pivot      P3_bilingual 30               0.071111           -0.040179             0.202245                  0.868
   en-de translation_quality_ref_free  P1_target_rubric P2_explicit_pivot 30              -0.031111           -0.138889             0.067873                  0.274
   en-de translation_quality_ref_free P0_direct_english P2_explicit_pivot 30              -0.026667           -0.135869             0.074206                  0.294
   en-ru translation_quality_ref_free  P1_target_rubric      P3_bilingual 30              -0.011111           -0.102683             0.084660                  0.347
   en-ru translation_quality_ref_free P0_direct_english P2_explicit_pivot 30               0.006667           -0.100000             0.140639                  0.582
```

## Largest language gaps

```text
                   dimension          protocol  mean_spearman min_spearman_language  min_spearman max_spearman_language  max_spearman  spearman_language_gap  auroc_language_gap
translation_quality_ref_free P0_direct_english       0.376518                 en-ru      0.023395                 zh-en      0.595367               0.571971            0.308889
translation_quality_ref_free      P3_bilingual       0.427605                 en-ru      0.178148                 en-de      0.677062               0.498914            0.248889
translation_quality_ref_free P2_explicit_pivot       0.219981                 en-ru      0.035116                 en-de      0.437328               0.402211            0.191111
translation_quality_ref_free  P1_target_rubric       0.338921                 en-ru      0.199117                 en-de      0.478725               0.279608            0.140000
```
