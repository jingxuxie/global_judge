# Protocol Comparison Summary

## Largest score shifts

```text
language           dimension        protocol_a        protocol_b  n  mean_abs_score_shift  score_disagreement_rate  large_shift_rate_abs_ge_2  mean_score_delta_b_minus_a
   zh-en translation_quality P0_direct_english P2_explicit_pivot 30              0.533333                 0.433333                   0.066667                    0.000000
   en-de translation_quality P0_direct_english      P3_bilingual 30              0.200000                 0.200000                   0.000000                   -0.200000
   en-de translation_quality P0_direct_english P2_explicit_pivot 30              0.200000                 0.200000                   0.000000                   -0.200000
   en-de translation_quality  P1_target_rubric P2_explicit_pivot 30              0.166667                 0.166667                   0.000000                   -0.100000
   en-de translation_quality P0_direct_english  P1_target_rubric 30              0.166667                 0.166667                   0.000000                   -0.100000
   en-ru translation_quality  P1_target_rubric      P3_bilingual 30              0.166667                 0.166667                   0.000000                   -0.166667
   en-ru translation_quality P0_direct_english  P1_target_rubric 30              0.166667                 0.166667                   0.000000                    0.100000
   en-de translation_quality P2_explicit_pivot      P3_bilingual 30              0.133333                 0.133333                   0.000000                    0.000000
   en-de translation_quality  P1_target_rubric      P3_bilingual 30              0.100000                 0.100000                   0.000000                   -0.100000
   en-ru translation_quality  P1_target_rubric P2_explicit_pivot 30              0.100000                 0.100000                   0.000000                   -0.100000
   en-ru translation_quality P0_direct_english P2_explicit_pivot 30              0.066667                 0.066667                   0.000000                    0.000000
   en-ru translation_quality P0_direct_english      P3_bilingual 30              0.066667                 0.066667                   0.000000                   -0.066667
```

## Largest paired AUROC deltas

```text
language           dimension        protocol_a        protocol_b  n  auroc_delta_b_minus_a  auroc_delta_ci_low  auroc_delta_ci_high  auroc_prob_delta_gt_0
   en-de translation_quality  P1_target_rubric      P3_bilingual 30               0.093333            0.000000             0.200022                  0.959
   en-ru translation_quality  P1_target_rubric P2_explicit_pivot 30              -0.084444           -0.185187             0.000000                  0.000
   en-de translation_quality  P1_target_rubric P2_explicit_pivot 30               0.082222           -0.042427             0.212512                  0.896
   en-de translation_quality P0_direct_english  P1_target_rubric 30              -0.077778           -0.199095             0.037037                  0.109
   en-ru translation_quality P0_direct_english  P1_target_rubric 30               0.075556           -0.043062             0.196482                  0.866
   en-ru translation_quality  P1_target_rubric      P3_bilingual 30              -0.073333           -0.192171             0.035726                  0.092
   zh-en translation_quality P0_direct_english P2_explicit_pivot 30              -0.024444           -0.226671             0.177286                  0.377
   en-de translation_quality P0_direct_english      P3_bilingual 30               0.015556           -0.107242             0.142534                  0.585
   en-ru translation_quality P2_explicit_pivot      P3_bilingual 30               0.011111           -0.060000             0.093750                  0.528
   en-de translation_quality P2_explicit_pivot      P3_bilingual 30               0.011111           -0.102234             0.133929                  0.540
   en-ru translation_quality P0_direct_english P2_explicit_pivot 30              -0.008889           -0.095813             0.061121                  0.302
   en-de translation_quality P0_direct_english P2_explicit_pivot 30               0.004444           -0.125000             0.136171                  0.521
```

## Largest language gaps

```text
          dimension          protocol  mean_spearman min_spearman_language  min_spearman max_spearman_language  max_spearman  spearman_language_gap  auroc_language_gap
translation_quality      P3_bilingual       0.314840                 en-ru      0.159089                 en-de      0.470591               0.311502            0.113333
translation_quality P2_explicit_pivot       0.278941                 en-ru      0.134898                 en-de      0.398410               0.263511            0.113333
translation_quality P0_direct_english       0.302234                 en-ru      0.164959                 en-de      0.387585               0.222626            0.120000
translation_quality  P1_target_rubric       0.319160                 en-de      0.318126                 en-ru      0.320193               0.002067            0.053333
```
