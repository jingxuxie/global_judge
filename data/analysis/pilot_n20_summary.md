# Pilot Summary

Responses: 640
Parsed responses: 638
Estimated API cost from returned usage: $0.0396

## Best protocol correlations

```text
judge_model language         dimension           protocol            protocol_name  n  n_parsed  parse_rate  human_positive_rate  mean_judge_score  spearman  spearman_ci_low  spearman_ci_high  auroc  estimated_cost_usd
gpt-4o-mini    es-ES comprehensibility       P3_bilingual         Bilingual rubric 20        20         1.0             0.500000          2.700000  0.898027         0.801456          0.930474 1.0000            0.001351
gpt-4o-mini    es-ES comprehensibility P2_pivot_in_prompt English-pivot diagnostic 20        20         1.0             0.500000          3.200000  0.888406         0.792606          0.916458 1.0000            0.001219
gpt-4o-mini       tr comprehensibility  P0_direct_english    Direct English rubric 20        20         1.0             0.500000          3.100000  0.885116         0.750880          0.953463 0.9850            0.001194
gpt-4o-mini    es-ES comprehensibility  P0_direct_english    Direct English rubric 20        20         1.0             0.500000          2.800000  0.868986         0.765167          0.925250 0.9850            0.001166
gpt-4o-mini    en-US comprehensibility  P0_direct_english    Direct English rubric 20        20         1.0             0.500000          2.800000  0.781181         0.571863          0.896144 0.9400            0.001107
gpt-4o-mini       tr comprehensibility P2_pivot_in_prompt English-pivot diagnostic 20        18         0.9             0.555556          3.555556  0.763802         0.578685          0.907435 0.9125            0.001239
gpt-4o-mini    en-US comprehensibility P2_pivot_in_prompt English-pivot diagnostic 20        20         1.0             0.500000          3.250000  0.758747         0.528399          0.895815 0.9250            0.001148
gpt-4o-mini    es-ES comprehensibility   P1_target_rubric   Target-language rubric 20        20         1.0             0.500000          2.250000  0.755191         0.580280          0.897077 0.9100            0.001193
gpt-4o-mini    en-US comprehensibility   P1_target_rubric   Target-language rubric 20        20         1.0             0.500000          2.450000  0.738170         0.528850          0.884332 0.9100            0.001029
gpt-4o-mini    en-US           grammar P2_pivot_in_prompt English-pivot diagnostic 20        20         1.0             0.500000          4.350000  0.717430         0.462598          0.959535 0.8500            0.001145
```

## Largest protocol shifts

```text
judge_model language         dimension         protocol_a         protocol_b  mean_abs_shift  median_abs_shift  n
gpt-4o-mini       tr comprehensibility   P1_target_rubric P2_pivot_in_prompt        1.111111               1.0 18
gpt-4o-mini    en-US           grammar   P1_target_rubric P2_pivot_in_prompt        1.100000               1.0 20
gpt-4o-mini       vi comprehensibility   P1_target_rubric P2_pivot_in_prompt        1.050000               1.0 20
gpt-4o-mini    es-ES comprehensibility   P1_target_rubric P2_pivot_in_prompt        0.950000               1.0 20
gpt-4o-mini    es-ES           grammar   P1_target_rubric P2_pivot_in_prompt        0.950000               1.0 20
gpt-4o-mini       vi           grammar   P1_target_rubric P2_pivot_in_prompt        0.900000               1.0 20
gpt-4o-mini       vi           grammar   P1_target_rubric       P3_bilingual        0.800000               1.0 20
gpt-4o-mini    en-US comprehensibility   P1_target_rubric P2_pivot_in_prompt        0.800000               1.0 20
gpt-4o-mini       vi comprehensibility  P0_direct_english P2_pivot_in_prompt        0.700000               1.0 20
gpt-4o-mini    en-US           grammar   P1_target_rubric       P3_bilingual        0.700000               1.0 20
gpt-4o-mini       tr           grammar   P1_target_rubric P2_pivot_in_prompt        0.700000               1.0 20
gpt-4o-mini       tr comprehensibility P2_pivot_in_prompt       P3_bilingual        0.666667               1.0 18
```
