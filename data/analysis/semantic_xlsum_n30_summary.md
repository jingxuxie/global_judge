# Pilot Summary

Responses: 360
Parsed responses: 360
Estimated API cost from returned usage: $0.0426

## Best protocol correlations

```text
judge_model language  dimension          protocol          protocol_name  n  n_parsed  parse_rate  human_positive_rate  mean_judge_score  spearman  spearman_ci_low  spearman_ci_high    auroc  estimated_cost_usd
gpt-4o-mini       tr main_ideas      P3_bilingual       Bilingual rubric 30        30         1.0                  0.5          1.766667  0.587887         0.320458          0.790239 0.793333            0.003804
gpt-4o-mini    es-ES main_ideas P2_explicit_pivot Explicit English pivot 30        30         1.0                  0.5          1.733333  0.514260         0.220539          0.764590 0.771111            0.002919
gpt-4o-mini       tr main_ideas  P1_target_rubric Target-language rubric 30        30         1.0                  0.5          1.933333  0.495457         0.301968          0.678590 0.711111            0.004133
gpt-4o-mini    es-ES main_ideas P0_direct_english  Direct English rubric 30        30         1.0                  0.5          1.900000  0.487870         0.163693          0.735749 0.762222            0.003006
gpt-4o-mini       tr main_ideas P0_direct_english  Direct English rubric 30        30         1.0                  0.5          1.866667  0.463360         0.156556          0.698046 0.737778            0.003410
gpt-4o-mini    es-ES main_ideas      P3_bilingual       Bilingual rubric 30        30         1.0                  0.5          1.666667  0.431766         0.115331          0.723178 0.724444            0.003310
gpt-4o-mini    es-ES main_ideas  P1_target_rubric Target-language rubric 30        30         1.0                  0.5          1.566667  0.423493         0.112707          0.718319 0.717778            0.003398
gpt-4o-mini       tr main_ideas P2_explicit_pivot Explicit English pivot 30        30         1.0                  0.5          1.733333  0.338531         0.009678          0.623481 0.668889            0.003025
gpt-4o-mini       vi main_ideas      P3_bilingual       Bilingual rubric 30        30         1.0                  0.5          2.433333  0.194722        -0.145527          0.538329 0.606667            0.004208
gpt-4o-mini       vi main_ideas P0_direct_english  Direct English rubric 30        30         1.0                  0.5          2.433333  0.143242        -0.227031          0.460915 0.575556            0.003846
```

## Largest protocol shifts

```text
judge_model language  dimension        protocol_a        protocol_b  mean_abs_shift  median_abs_shift  n
gpt-4o-mini       vi main_ideas  P1_target_rubric P2_explicit_pivot        0.700000               1.0 30
gpt-4o-mini       vi main_ideas  P1_target_rubric      P3_bilingual        0.666667               1.0 30
gpt-4o-mini       vi main_ideas P0_direct_english  P1_target_rubric        0.466667               0.0 30
gpt-4o-mini    es-ES main_ideas P0_direct_english  P1_target_rubric        0.400000               0.0 30
gpt-4o-mini       tr main_ideas  P1_target_rubric P2_explicit_pivot        0.400000               0.0 30
gpt-4o-mini       tr main_ideas P0_direct_english P2_explicit_pivot        0.333333               0.0 30
gpt-4o-mini       vi main_ideas P2_explicit_pivot      P3_bilingual        0.300000               0.0 30
gpt-4o-mini       tr main_ideas P0_direct_english  P1_target_rubric        0.266667               0.0 30
gpt-4o-mini    es-ES main_ideas P0_direct_english P2_explicit_pivot        0.233333               0.0 30
gpt-4o-mini       vi main_ideas P0_direct_english P2_explicit_pivot        0.233333               0.0 30
gpt-4o-mini       tr main_ideas P2_explicit_pivot      P3_bilingual        0.233333               0.0 30
gpt-4o-mini    es-ES main_ideas  P1_target_rubric P2_explicit_pivot        0.233333               0.0 30
```
