# Pilot Summary

Responses: 384
Parsed responses: 384
Estimated API cost from returned usage: $0.0636

## Best protocol correlations

```text
 judge_model language         dimension          protocol          protocol_name  n  n_parsed  parse_rate  human_positive_rate  mean_judge_score  spearman  spearman_ci_low  spearman_ci_high    auroc  estimated_cost_usd
gpt-4.1-mini       vi comprehensibility P0_direct_english  Direct English rubric 12        12         1.0                  0.5          3.333333  0.849469         0.651534          0.948683 0.972222            0.001812
gpt-4.1-mini       vi comprehensibility      P3_bilingual       Bilingual rubric 12        12         1.0                  0.5          2.916667  0.810191         0.531381          0.935692 0.944444            0.002258
gpt-4.1-mini       tr           grammar P0_direct_english  Direct English rubric 12        12         1.0                  0.5          3.416667  0.778962         0.344414          1.000000 0.902778            0.001824
gpt-4.1-mini       tr           grammar      P3_bilingual       Bilingual rubric 12        12         1.0                  0.5          3.583333  0.778962         0.343372          1.000000 0.902778            0.002216
gpt-4.1-mini    en-US comprehensibility      P3_bilingual       Bilingual rubric 12        12         1.0                  0.5          3.000000  0.770201         0.474178          0.922937 0.930556            0.002038
gpt-4.1-mini       tr comprehensibility  P1_target_rubric Target-language rubric 12        12         1.0                  0.5          2.416667  0.758098         0.506478          0.903663 0.916667            0.002262
gpt-4.1-mini       tr comprehensibility      P3_bilingual       Bilingual rubric 12        12         1.0                  0.5          2.500000  0.758098         0.506478          0.904534 0.916667            0.002360
gpt-4.1-mini    en-US comprehensibility  P1_target_rubric Target-language rubric 12        12         1.0                  0.5          2.833333  0.753778         0.445113          0.972096 0.916667            0.001702
gpt-4.1-mini       vi comprehensibility  P1_target_rubric Target-language rubric 12        12         1.0                  0.5          2.916667  0.730036         0.315474          0.923047 0.902778            0.002060
gpt-4.1-mini       tr comprehensibility P0_direct_english  Direct English rubric 12        12         1.0                  0.5          2.750000  0.728811         0.471940          0.923936 0.888889            0.001990
```

## Largest protocol shifts

```text
 judge_model language         dimension        protocol_a        protocol_b  mean_abs_shift  median_abs_shift  n
gpt-4.1-mini       tr comprehensibility P2_explicit_pivot      P3_bilingual        1.500000               1.0 12
gpt-4.1-mini       tr comprehensibility P0_direct_english P2_explicit_pivot        1.416667               1.0 12
gpt-4.1-mini       tr comprehensibility  P1_target_rubric P2_explicit_pivot        1.416667               1.0 12
gpt-4.1-mini    es-ES           grammar P0_direct_english P2_explicit_pivot        1.333333               1.0 12
gpt-4.1-mini    es-ES           grammar P2_explicit_pivot      P3_bilingual        1.250000               1.0 12
gpt-4.1-mini       vi           grammar  P1_target_rubric P2_explicit_pivot        0.750000               0.5 12
gpt-4.1-mini    es-ES           grammar P0_direct_english  P1_target_rubric        0.750000               0.0 12
gpt-4.1-mini       vi comprehensibility P0_direct_english P2_explicit_pivot        0.750000               1.0 12
gpt-4.1-mini       vi           grammar P0_direct_english P2_explicit_pivot        0.666667               0.5 12
gpt-4.1-mini       vi           grammar P2_explicit_pivot      P3_bilingual        0.666667               0.5 12
gpt-4.1-mini    es-ES           grammar  P1_target_rubric      P3_bilingual        0.666667               0.5 12
gpt-4.1-mini    es-ES           grammar  P1_target_rubric P2_explicit_pivot        0.583333               0.0 12
```
