# Protocol Comparison Summary

## Largest score shifts

```text
language         dimension        protocol_a        protocol_b  n  mean_abs_score_shift  score_disagreement_rate  large_shift_rate_abs_ge_2  mean_score_delta_b_minus_a
      vi           grammar  P1_target_rubric P2_explicit_pivot 50                  1.20                     0.82                       0.34                        0.84
      tr           grammar  P1_target_rubric P2_explicit_pivot 50                  0.96                     0.74                       0.16                        0.72
      vi comprehensibility P2_explicit_pivot      P3_bilingual 50                  0.96                     0.68                       0.18                        0.24
   en-US           grammar  P1_target_rubric P2_explicit_pivot 50                  0.94                     0.84                       0.10                        0.90
      tr           grammar P2_explicit_pivot      P3_bilingual 50                  0.90                     0.66                       0.18                       -0.50
      vi comprehensibility  P1_target_rubric P2_explicit_pivot 50                  0.90                     0.64                       0.20                        0.22
      vi comprehensibility P0_direct_english P2_explicit_pivot 50                  0.88                     0.66                       0.14                       -0.20
   en-US comprehensibility  P1_target_rubric P2_explicit_pivot 50                  0.88                     0.62                       0.24                        0.80
      tr           grammar P0_direct_english P2_explicit_pivot 50                  0.84                     0.64                       0.16                        0.32
   es-ES           grammar  P1_target_rubric P2_explicit_pivot 50                  0.84                     0.64                       0.18                        0.16
   es-ES           grammar P0_direct_english P2_explicit_pivot 50                  0.80                     0.54                       0.18                       -0.36
      tr comprehensibility  P1_target_rubric P2_explicit_pivot 50                  0.80                     0.56                       0.14                        0.44
```

## Largest paired AUROC deltas

```text
language         dimension        protocol_a        protocol_b  n  auroc_delta_b_minus_a  auroc_delta_ci_low  auroc_delta_ci_high  auroc_prob_delta_gt_0
      vi comprehensibility P2_explicit_pivot      P3_bilingual 50                 0.1656            0.008781             0.316811                  0.980
      tr comprehensibility P0_direct_english P2_explicit_pivot 50                -0.1496           -0.256526            -0.054993                  0.000
      vi comprehensibility P0_direct_english P2_explicit_pivot 50                -0.1424           -0.300828             0.028648                  0.046
      tr comprehensibility P2_explicit_pivot      P3_bilingual 50                 0.1360            0.036636             0.249262                  1.000
      vi comprehensibility  P1_target_rubric      P3_bilingual 50                 0.1240            0.018493             0.230087                  0.988
      tr comprehensibility  P1_target_rubric P2_explicit_pivot 50                -0.1240           -0.245141            -0.017823                  0.012
      vi           grammar  P1_target_rubric P2_explicit_pivot 50                -0.1192           -0.267536             0.024848                  0.073
      vi           grammar P0_direct_english P2_explicit_pivot 50                -0.1128           -0.252405             0.025701                  0.044
      vi comprehensibility P0_direct_english  P1_target_rubric 50                -0.1008           -0.223217             0.013622                  0.045
      vi           grammar  P1_target_rubric      P3_bilingual 50                -0.0776           -0.186689             0.027247                  0.067
   es-ES           grammar  P1_target_rubric P2_explicit_pivot 50                 0.0768           -0.061204             0.219022                  0.858
   es-ES comprehensibility P0_direct_english P2_explicit_pivot 50                -0.0712           -0.172887             0.032061                  0.095
```

## Largest language gaps

```text
        dimension          protocol  mean_spearman min_spearman_language  min_spearman max_spearman_language  max_spearman  spearman_language_gap  auroc_language_gap
comprehensibility P2_explicit_pivot       0.413597                    vi      0.085546                 en-US      0.710816               0.625270              0.3496
comprehensibility  P1_target_rubric       0.502007                    vi      0.164377                 en-US      0.699263               0.534886              0.2912
          grammar      P3_bilingual       0.151589                    tr     -0.071507                 en-US      0.384920               0.456426              0.2496
          grammar  P1_target_rubric       0.174472                    tr     -0.088359                 en-US      0.366391               0.454750              0.2384
          grammar P2_explicit_pivot       0.148348                    tr     -0.075697                 en-US      0.364527               0.440224              0.2248
comprehensibility P0_direct_english       0.583880                    vi      0.349114                 en-US      0.731180               0.382066              0.2200
          grammar P0_direct_english       0.181400                    tr     -0.021613                 en-US      0.327433               0.349046              0.1928
comprehensibility      P3_bilingual       0.559355                    vi      0.399354                 en-US      0.701414               0.302061              0.1768
```
