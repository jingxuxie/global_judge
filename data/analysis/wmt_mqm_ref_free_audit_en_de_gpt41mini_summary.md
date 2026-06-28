# Pilot Summary

Responses: 60
Parsed responses: 60
Estimated API cost from returned usage: $0.0116

## Best protocol correlations

```text
 judge_model language                    dimension          protocol          protocol_name  n  n_parsed  parse_rate  human_positive_rate  mean_judge_score  spearman  spearman_ci_low  spearman_ci_high    auroc  estimated_cost_usd
gpt-4.1-mini    en-de translation_quality_ref_free P2_explicit_pivot Explicit English pivot 30        30         1.0                  0.5          4.400000  0.563489         0.309591          0.796691 0.784444            0.005128
gpt-4.1-mini    en-de translation_quality_ref_free      P3_bilingual       Bilingual rubric 30        30         1.0                  0.5          4.266667  0.503278         0.207657          0.743032 0.760000            0.006450
```

## Largest protocol shifts

```text
 judge_model language                    dimension        protocol_a   protocol_b  mean_abs_shift  median_abs_shift  n
gpt-4.1-mini    en-de translation_quality_ref_free P2_explicit_pivot P3_bilingual             0.2               0.0 30
```
