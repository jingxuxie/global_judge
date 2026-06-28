# Pilot Summary

Responses: 96
Parsed responses: 96
Estimated API cost from returned usage: $0.0114

## Best protocol correlations

```text
judge_model language  dimension          protocol          protocol_name  n  n_parsed  parse_rate  human_positive_rate  mean_judge_score  spearman  spearman_ci_low  spearman_ci_high   auroc  estimated_cost_usd
gpt-4o-mini       tr main_ideas P2_explicit_pivot Explicit English pivot  8         8         1.0                  0.5             2.500  0.670820         0.065847          0.956183 0.87500            0.000823
gpt-4o-mini       tr main_ideas      P3_bilingual       Bilingual rubric  8         8         1.0                  0.5             2.125  0.629941         0.218218          0.956183 0.81250            0.001031
gpt-4o-mini       tr main_ideas P0_direct_english  Direct English rubric  8         8         1.0                  0.5             2.250  0.577350         0.292770          1.000000 0.75000            0.000926
gpt-4o-mini       tr main_ideas  P1_target_rubric Target-language rubric  8         8         1.0                  0.5             2.250  0.577350         0.292770          1.000000 0.75000            0.001092
gpt-4o-mini       vi main_ideas  P1_target_rubric Target-language rubric  8         8         1.0                  0.5             2.875  0.377964         0.218218          0.774597 0.62500            0.001186
gpt-4o-mini    es-ES main_ideas  P1_target_rubric Target-language rubric  8         8         1.0                  0.5             1.375  0.258199        -0.461317          0.774597 0.62500            0.000918
gpt-4o-mini    es-ES main_ideas P0_direct_english  Direct English rubric  8         8         1.0                  0.5             1.875  0.251976        -0.745356          1.000000 0.62500            0.000825
gpt-4o-mini    es-ES main_ideas      P3_bilingual       Bilingual rubric  8         8         1.0                  0.5             1.750  0.059761        -0.751964          0.774597 0.53125            0.000915
gpt-4o-mini    es-ES main_ideas P2_explicit_pivot Explicit English pivot  8         8         1.0                  0.5             2.000  0.000000        -0.706702          0.707107 0.50000            0.000777
gpt-4o-mini       vi main_ideas      P3_bilingual       Bilingual rubric  8         8         1.0                  0.5             2.250 -0.250000        -0.776596          0.577350 0.37500            0.001108
```

## Largest protocol shifts

```text
judge_model language  dimension        protocol_a        protocol_b  mean_abs_shift  median_abs_shift  n
gpt-4o-mini       vi main_ideas  P1_target_rubric P2_explicit_pivot           1.125               1.0  8
gpt-4o-mini       vi main_ideas  P1_target_rubric      P3_bilingual           0.875               1.0  8
gpt-4o-mini       tr main_ideas  P1_target_rubric P2_explicit_pivot           0.750               1.0  8
gpt-4o-mini       tr main_ideas P0_direct_english P2_explicit_pivot           0.750               1.0  8
gpt-4o-mini       vi main_ideas P0_direct_english  P1_target_rubric           0.750               1.0  8
gpt-4o-mini       tr main_ideas P2_explicit_pivot      P3_bilingual           0.625               1.0  8
gpt-4o-mini    es-ES main_ideas  P1_target_rubric P2_explicit_pivot           0.625               1.0  8
gpt-4o-mini    es-ES main_ideas P0_direct_english  P1_target_rubric           0.500               0.5  8
gpt-4o-mini       vi main_ideas P2_explicit_pivot      P3_bilingual           0.500               0.5  8
gpt-4o-mini    es-ES main_ideas P0_direct_english P2_explicit_pivot           0.375               0.0  8
gpt-4o-mini       vi main_ideas P0_direct_english      P3_bilingual           0.375               0.0  8
gpt-4o-mini    es-ES main_ideas  P1_target_rubric      P3_bilingual           0.375               0.0  8
```
