# Protocol Comparison Summary

## Largest score shifts

```text
language         dimension        protocol_a        protocol_b  n  mean_abs_score_shift  score_disagreement_rate  large_shift_rate_abs_ge_2  mean_score_delta_b_minus_a
      tr comprehensibility P2_explicit_pivot      P3_bilingual 12              1.500000                 0.833333                   0.333333                   -0.166667
      tr comprehensibility P0_direct_english P2_explicit_pivot 12              1.416667                 0.666667                   0.416667                   -0.083333
      tr comprehensibility  P1_target_rubric P2_explicit_pivot 12              1.416667                 0.833333                   0.333333                    0.250000
   es-ES           grammar P0_direct_english P2_explicit_pivot 12              1.333333                 0.833333                   0.416667                   -1.166667
   es-ES           grammar P2_explicit_pivot      P3_bilingual 12              1.250000                 0.833333                   0.333333                    1.083333
      vi comprehensibility P0_direct_english P2_explicit_pivot 12              0.750000                 0.583333                   0.083333                   -0.416667
   es-ES           grammar P0_direct_english  P1_target_rubric 12              0.750000                 0.416667                   0.333333                   -0.750000
      vi           grammar  P1_target_rubric P2_explicit_pivot 12              0.750000                 0.500000                   0.250000                    0.583333
      vi           grammar P0_direct_english P2_explicit_pivot 12              0.666667                 0.500000                   0.166667                    0.166667
   es-ES           grammar  P1_target_rubric      P3_bilingual 12              0.666667                 0.500000                   0.166667                    0.666667
      vi           grammar P2_explicit_pivot      P3_bilingual 12              0.666667                 0.500000                   0.166667                   -0.333333
      vi           grammar P0_direct_english  P1_target_rubric 12              0.583333                 0.500000                   0.083333                   -0.416667
```

## Largest paired AUROC deltas

```text
language         dimension        protocol_a        protocol_b  n  auroc_delta_b_minus_a  auroc_delta_ci_low  auroc_delta_ci_high  auroc_prob_delta_gt_0
      tr comprehensibility  P1_target_rubric P2_explicit_pivot 12              -0.527778           -0.777778            -0.240741               0.000000
      tr comprehensibility P2_explicit_pivot      P3_bilingual 12               0.527778            0.249821             0.785714               1.000000
      tr comprehensibility P0_direct_english P2_explicit_pivot 12              -0.500000           -0.765625            -0.214137               0.000000
   es-ES           grammar P2_explicit_pivot      P3_bilingual 12               0.208333           -0.085714             0.457143               0.913000
      vi           grammar P2_explicit_pivot      P3_bilingual 12               0.194444           -0.085714             0.537183               0.898000
      vi           grammar P0_direct_english P2_explicit_pivot 12              -0.180556           -0.513889             0.140737               0.119119
      vi           grammar  P1_target_rubric P2_explicit_pivot 12              -0.180556           -0.472454             0.085844               0.076000
   en-US           grammar P2_explicit_pivot      P3_bilingual 12               0.166667           -0.047132             0.400156               0.922000
   es-ES           grammar  P1_target_rubric      P3_bilingual 12               0.166667            0.000000             0.342857               0.972000
   es-ES comprehensibility  P1_target_rubric P2_explicit_pivot 12              -0.166667           -0.406392             0.000000               0.000000
   es-ES           grammar P0_direct_english      P3_bilingual 12               0.138889            0.000000             0.333333               0.953954
   es-ES comprehensibility P2_explicit_pivot      P3_bilingual 12               0.138889            0.000000             0.375000               0.871000
```

## Largest language gaps

```text
        dimension          protocol  mean_spearman min_spearman_language  min_spearman max_spearman_language  max_spearman  spearman_language_gap  auroc_language_gap
comprehensibility P2_explicit_pivot       0.360043                    tr     -0.201389                 en-US      0.724547               0.925937            0.513889
          grammar P2_explicit_pivot       0.325501                    vi      0.151330                    tr      0.617213               0.465883            0.250000
comprehensibility P0_direct_english       0.682290                 es-ES      0.426334                    vi      0.849469               0.423135            0.236111
          grammar P0_direct_english       0.509852                 es-ES      0.380188                    tr      0.778962               0.398774            0.208333
comprehensibility      P3_bilingual       0.697904                 es-ES      0.453126                    vi      0.810191               0.357065            0.194444
          grammar  P1_target_rubric       0.454454                 es-ES      0.314270                    tr      0.666667               0.352397            0.166667
          grammar      P3_bilingual       0.612453                    vi      0.506370                    tr      0.778962               0.272593            0.125000
comprehensibility  P1_target_rubric       0.689837                 es-ES      0.517434                    tr      0.758098               0.240664            0.138889
```
