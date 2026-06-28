# Protocol Comparison Summary

## Largest score shifts

```text
language  dimension        protocol_a        protocol_b  n  mean_abs_score_shift  score_disagreement_rate  large_shift_rate_abs_ge_2  mean_score_delta_b_minus_a
      vi main_ideas  P1_target_rubric P2_explicit_pivot 30              0.700000                 0.533333                   0.133333                   -0.500000
      vi main_ideas  P1_target_rubric      P3_bilingual 30              0.666667                 0.566667                   0.100000                   -0.266667
      vi main_ideas P0_direct_english  P1_target_rubric 30              0.466667                 0.366667                   0.100000                    0.266667
   es-ES main_ideas P0_direct_english  P1_target_rubric 30              0.400000                 0.366667                   0.033333                   -0.333333
      tr main_ideas  P1_target_rubric P2_explicit_pivot 30              0.400000                 0.400000                   0.000000                   -0.200000
      tr main_ideas P0_direct_english P2_explicit_pivot 30              0.333333                 0.333333                   0.000000                   -0.133333
      vi main_ideas P2_explicit_pivot      P3_bilingual 30              0.300000                 0.266667                   0.033333                    0.233333
      tr main_ideas P0_direct_english  P1_target_rubric 30              0.266667                 0.266667                   0.000000                    0.066667
   es-ES main_ideas P0_direct_english P2_explicit_pivot 30              0.233333                 0.233333                   0.000000                   -0.166667
   es-ES main_ideas P0_direct_english      P3_bilingual 30              0.233333                 0.233333                   0.000000                   -0.233333
      vi main_ideas P0_direct_english P2_explicit_pivot 30              0.233333                 0.233333                   0.000000                   -0.233333
      tr main_ideas P2_explicit_pivot      P3_bilingual 30              0.233333                 0.233333                   0.000000                    0.033333
```

## Largest paired AUROC deltas

```text
language  dimension        protocol_a        protocol_b  n  auroc_delta_b_minus_a  auroc_delta_ci_low  auroc_delta_ci_high  auroc_prob_delta_gt_0
      tr main_ideas P2_explicit_pivot      P3_bilingual 30               0.124444            0.000000             0.275186                  0.957
      vi main_ideas P2_explicit_pivot      P3_bilingual 30               0.106667            0.013283             0.219514                  0.987
      tr main_ideas  P1_target_rubric      P3_bilingual 30               0.082222           -0.041667             0.219460                  0.907
      vi main_ideas P0_direct_english P2_explicit_pivot 30              -0.075556           -0.181828             0.017874                  0.046
      vi main_ideas  P1_target_rubric P2_explicit_pivot 30              -0.073333           -0.291866             0.111645                  0.207
      tr main_ideas P0_direct_english P2_explicit_pivot 30              -0.068889           -0.227525             0.084854                  0.150
      tr main_ideas P0_direct_english      P3_bilingual 30               0.055556           -0.069458             0.187832                  0.768
   es-ES main_ideas  P1_target_rubric P2_explicit_pivot 30               0.053333           -0.060324             0.160714                  0.830
   es-ES main_ideas P2_explicit_pivot      P3_bilingual 30              -0.046667           -0.119349             0.000000                  0.000
   es-ES main_ideas P0_direct_english  P1_target_rubric 30              -0.044444           -0.178249             0.095056                  0.264
      tr main_ideas  P1_target_rubric P2_explicit_pivot 30              -0.042222           -0.222247             0.124458                  0.348
   es-ES main_ideas P0_direct_english      P3_bilingual 30              -0.037778           -0.144796             0.057418                  0.228
```

## Largest language gaps

```text
 dimension          protocol  mean_spearman min_spearman_language  min_spearman max_spearman_language  max_spearman  spearman_language_gap  auroc_language_gap
main_ideas P2_explicit_pivot       0.284264                    vi      0.000000                 es-ES      0.514260               0.514260            0.271111
main_ideas      P3_bilingual       0.404792                    vi      0.194722                    tr      0.587887               0.393165            0.186667
main_ideas  P1_target_rubric       0.352391                    vi      0.138222                    tr      0.495457               0.357236            0.144444
main_ideas P0_direct_english       0.364824                    vi      0.143242                 es-ES      0.487870               0.344628            0.186667
```
