# Pilot Summary

Responses: 192
Parsed responses: 192
Estimated API cost from returned usage: $0.0121

## Best protocol correlations

```text
judge_model language         dimension           protocol            protocol_name  n  n_parsed  parse_rate  human_positive_rate  mean_judge_score  spearman  spearman_ci_low  spearman_ci_high    auroc  estimated_cost_usd
gpt-4o-mini    en-US comprehensibility   P1_target_rubric   Target-language rubric  6         6         1.0                  0.5          2.833333  0.948683         0.707107               1.0 1.000000            0.000303
gpt-4o-mini    en-US comprehensibility P2_pivot_in_prompt English-pivot diagnostic  6         6         1.0                  0.5          3.666667  0.948683         0.707107               1.0 1.000000            0.000345
gpt-4o-mini       tr comprehensibility  P0_direct_english    Direct English rubric  6         6         1.0                  0.5          2.666667  0.948683         0.707107               1.0 1.000000            0.000413
gpt-4o-mini       tr comprehensibility       P3_bilingual         Bilingual rubric  6         6         1.0                  0.5          2.666667  0.948683         0.707107               1.0 1.000000            0.000485
gpt-4o-mini       tr comprehensibility   P1_target_rubric   Target-language rubric  6         6         1.0                  0.5          2.500000  0.904534         0.707107               1.0 1.000000            0.000470
gpt-4o-mini       tr comprehensibility P2_pivot_in_prompt English-pivot diagnostic  6         6         1.0                  0.5          3.000000  0.904534         0.707107               1.0 1.000000            0.000426
gpt-4o-mini    en-US comprehensibility       P3_bilingual         Bilingual rubric  6         6         1.0                  0.5          3.000000  0.904534         0.707107               1.0 1.000000            0.000367
gpt-4o-mini    en-US comprehensibility  P0_direct_english    Direct English rubric  6         6         1.0                  0.5          3.333333  0.891133         0.674200               1.0 1.000000            0.000334
gpt-4o-mini    es-ES comprehensibility P2_pivot_in_prompt English-pivot diagnostic  6         6         1.0                  0.5          2.666667  0.816497         0.316228               1.0 0.944444            0.000347
gpt-4o-mini    es-ES comprehensibility  P0_direct_english    Direct English rubric  6         6         1.0                  0.5          2.833333  0.804030         0.316228               1.0 0.944444            0.000334
```

## Largest protocol shifts

```text
judge_model language         dimension         protocol_a         protocol_b  mean_abs_shift  median_abs_shift  n
gpt-4o-mini    en-US           grammar   P1_target_rubric P2_pivot_in_prompt        1.333333               1.0  6
gpt-4o-mini    en-US           grammar  P0_direct_english P2_pivot_in_prompt        1.000000               0.5  6
gpt-4o-mini       vi           grammar   P1_target_rubric P2_pivot_in_prompt        1.000000               1.0  6
gpt-4o-mini    es-ES           grammar   P1_target_rubric P2_pivot_in_prompt        1.000000               1.0  6
gpt-4o-mini       vi comprehensibility   P1_target_rubric P2_pivot_in_prompt        1.000000               1.0  6
gpt-4o-mini    es-ES           grammar  P0_direct_english P2_pivot_in_prompt        0.833333               0.5  6
gpt-4o-mini    es-ES comprehensibility   P1_target_rubric P2_pivot_in_prompt        0.833333               1.0  6
gpt-4o-mini    en-US comprehensibility   P1_target_rubric P2_pivot_in_prompt        0.833333               1.0  6
gpt-4o-mini       vi           grammar   P1_target_rubric       P3_bilingual        0.833333               1.0  6
gpt-4o-mini    en-US           grammar P2_pivot_in_prompt       P3_bilingual        0.833333               0.5  6
gpt-4o-mini    en-US           grammar  P0_direct_english   P1_target_rubric        0.666667               1.0  6
gpt-4o-mini    es-ES comprehensibility  P0_direct_english   P1_target_rubric        0.666667               1.0  6
```
