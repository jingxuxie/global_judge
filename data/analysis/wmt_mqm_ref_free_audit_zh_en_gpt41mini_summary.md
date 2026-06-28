# Pilot Summary

Responses: 60
Parsed responses: 60
Estimated API cost from returned usage: $0.0105

## Best protocol correlations

```text
 judge_model language                    dimension          protocol          protocol_name  n  n_parsed  parse_rate  human_positive_rate  mean_judge_score  spearman  spearman_ci_low  spearman_ci_high    auroc  estimated_cost_usd
gpt-4.1-mini    zh-en translation_quality_ref_free P0_direct_english  Direct English rubric 30        30         1.0                  0.5               3.8  0.502711         0.227394          0.743141 0.773333            0.005320
gpt-4.1-mini    zh-en translation_quality_ref_free P2_explicit_pivot Explicit English pivot 30        30         1.0                  0.5               4.2  0.254498        -0.068136          0.537084 0.635556            0.005204
```

## Largest protocol shifts

```text
 judge_model language                    dimension        protocol_a        protocol_b  mean_abs_shift  median_abs_shift  n
gpt-4.1-mini    zh-en translation_quality_ref_free P0_direct_english P2_explicit_pivot        0.666667               0.5 30
```
