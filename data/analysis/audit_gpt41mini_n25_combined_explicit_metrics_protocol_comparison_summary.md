# Protocol Comparison Summary

## Largest score shifts

```text
language         dimension        protocol_a        protocol_b  n  mean_abs_score_shift  score_disagreement_rate  large_shift_rate_abs_ge_2  mean_score_delta_b_minus_a
      tr comprehensibility P2_explicit_pivot      P3_bilingual 25                  1.16                     0.64                       0.36                       -0.28
      tr comprehensibility P0_direct_english P2_explicit_pivot 25                  1.04                     0.56                       0.32                        0.08
      tr comprehensibility  P1_target_rubric P2_explicit_pivot 25                  1.04                     0.60                       0.32                        0.32
      vi comprehensibility P0_direct_english P2_explicit_pivot 25                  0.96                     0.68                       0.24                       -0.08
      vi comprehensibility P2_explicit_pivot      P3_bilingual 25                  0.96                     0.68                       0.24                        0.08
   es-ES           grammar P0_direct_english P2_explicit_pivot 25                  0.92                     0.52                       0.20                       -0.68
   es-ES           grammar P2_explicit_pivot      P3_bilingual 25                  0.88                     0.48                       0.20                        0.80
      tr           grammar P0_direct_english P2_explicit_pivot 25                  0.84                     0.56                       0.20                       -0.04
      vi           grammar P0_direct_english P2_explicit_pivot 25                  0.84                     0.64                       0.20                       -0.12
      vi           grammar P2_explicit_pivot      P3_bilingual 25                  0.84                     0.60                       0.16                       -0.04
      tr           grammar  P1_target_rubric P2_explicit_pivot 25                  0.84                     0.60                       0.16                        0.28
   es-ES comprehensibility P0_direct_english P2_explicit_pivot 25                  0.80                     0.48                       0.16                       -0.32
```

## Largest paired AUROC deltas

```text
language         dimension        protocol_a        protocol_b  n  auroc_delta_b_minus_a  auroc_delta_ci_low  auroc_delta_ci_high  auroc_prob_delta_gt_0
      tr comprehensibility P2_explicit_pivot      P3_bilingual 25               0.352564            0.181773             0.544137                  1.000
      vi           grammar P0_direct_english P2_explicit_pivot 25              -0.342949           -0.540011            -0.175307                  0.000
      tr comprehensibility P0_direct_english P2_explicit_pivot 25              -0.317308           -0.509817            -0.149984                  0.000
      tr comprehensibility  P1_target_rubric P2_explicit_pivot 25              -0.310897           -0.516031            -0.131410                  0.000
      vi           grammar P2_explicit_pivot      P3_bilingual 25               0.298077            0.124958             0.493667                  1.000
      vi           grammar  P1_target_rubric P2_explicit_pivot 25              -0.253205           -0.444471            -0.064103                  0.003
      vi comprehensibility  P1_target_rubric P2_explicit_pivot 25              -0.192308           -0.397059             0.010071                  0.029
   en-US           grammar P0_direct_english      P3_bilingual 25              -0.169872           -0.308451            -0.045455                  0.000
      vi comprehensibility P0_direct_english P2_explicit_pivot 25              -0.169872           -0.371795             0.060897                  0.072
   en-US           grammar P2_explicit_pivot      P3_bilingual 25              -0.157051           -0.288474            -0.035714                  0.000
   es-ES comprehensibility P0_direct_english P2_explicit_pivot 25              -0.153846           -0.336542             0.003477                  0.027
      vi comprehensibility P2_explicit_pivot      P3_bilingual 25               0.134615           -0.089854             0.357189                  0.890
```

## Largest language gaps

```text
        dimension          protocol  mean_spearman min_spearman_language  min_spearman max_spearman_language  max_spearman  spearman_language_gap  auroc_language_gap
          grammar P0_direct_english       0.311306                    tr     -0.093508                 en-US      0.644503               0.738011            0.397436
          grammar P2_explicit_pivot       0.233301                    vi     -0.051766                 en-US      0.631970               0.683736            0.362179
          grammar      P3_bilingual       0.263252                    tr     -0.052498                    vi      0.491022               0.543519            0.298077
comprehensibility P2_explicit_pivot       0.371656                    tr      0.168445                 en-US      0.649019               0.480574            0.269231
          grammar  P1_target_rubric       0.326534                    tr      0.093950                 en-US      0.554093               0.460144            0.237179
comprehensibility      P3_bilingual       0.632519                    vi      0.446071                    tr      0.796060               0.349989            0.195513
comprehensibility  P1_target_rubric       0.596267                 en-US      0.436363                    tr      0.718527               0.282163            0.157051
comprehensibility P0_direct_english       0.646799                    vi      0.508979                 es-ES      0.738452               0.229473            0.125000
```
