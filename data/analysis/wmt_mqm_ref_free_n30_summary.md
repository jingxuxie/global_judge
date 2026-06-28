# Pilot Summary

Responses: 300
Parsed responses: 300
Estimated API cost from returned usage: $0.0206

## Best protocol correlations

```text
judge_model language                    dimension          protocol          protocol_name  n  n_parsed  parse_rate  human_positive_rate  mean_judge_score  spearman  spearman_ci_low  spearman_ci_high    auroc  estimated_cost_usd
gpt-4o-mini    en-de translation_quality_ref_free      P3_bilingual       Bilingual rubric 30        30         1.0                  0.5          4.533333  0.677062         0.416907          0.867914 0.837778            0.002332
gpt-4o-mini    zh-en translation_quality_ref_free P0_direct_english  Direct English rubric 30        30         1.0                  0.5          4.166667  0.595367         0.318586          0.843909 0.820000            0.001961
gpt-4o-mini    en-de translation_quality_ref_free P0_direct_english  Direct English rubric 30        30         1.0                  0.5          4.666667  0.510791         0.229729          0.776642 0.735556            0.001917
gpt-4o-mini    en-de translation_quality_ref_free  P1_target_rubric Target-language rubric 30        30         1.0                  0.5          4.533333  0.478725         0.204127          0.784677 0.740000            0.002234
gpt-4o-mini    en-de translation_quality_ref_free P2_explicit_pivot Explicit English pivot 30        30         1.0                  0.5          4.600000  0.437328         0.141225          0.720739 0.708889            0.001879
gpt-4o-mini    en-ru translation_quality_ref_free  P1_target_rubric Target-language rubric 30        30         1.0                  0.5          4.433333  0.199117        -0.110264          0.533021 0.600000            0.002128
gpt-4o-mini    zh-en translation_quality_ref_free P2_explicit_pivot Explicit English pivot 30        30         1.0                  0.5          4.133333  0.187500        -0.149276          0.483974 0.600000            0.001921
gpt-4o-mini    en-ru translation_quality_ref_free      P3_bilingual       Bilingual rubric 30        30         1.0                  0.5          4.466667  0.178148        -0.164860          0.530540 0.588889            0.002354
gpt-4o-mini    en-ru translation_quality_ref_free P2_explicit_pivot Explicit English pivot 30        30         1.0                  0.5          4.366667  0.035116        -0.301698          0.386223 0.517778            0.001941
gpt-4o-mini    en-ru translation_quality_ref_free P0_direct_english  Direct English rubric 30        30         1.0                  0.5          4.566667  0.023395        -0.281868          0.379805 0.511111            0.001972
```

## Largest protocol shifts

```text
judge_model language                    dimension        protocol_a        protocol_b  mean_abs_shift  median_abs_shift  n
gpt-4o-mini    zh-en translation_quality_ref_free P0_direct_english P2_explicit_pivot        0.700000               1.0 30
gpt-4o-mini    en-ru translation_quality_ref_free P0_direct_english P2_explicit_pivot        0.266667               0.0 30
gpt-4o-mini    en-ru translation_quality_ref_free  P1_target_rubric P2_explicit_pivot        0.266667               0.0 30
gpt-4o-mini    en-ru translation_quality_ref_free P2_explicit_pivot      P3_bilingual        0.233333               0.0 30
gpt-4o-mini    en-de translation_quality_ref_free P0_direct_english  P1_target_rubric        0.133333               0.0 30
gpt-4o-mini    en-ru translation_quality_ref_free P0_direct_english  P1_target_rubric        0.133333               0.0 30
gpt-4o-mini    en-de translation_quality_ref_free P0_direct_english P2_explicit_pivot        0.133333               0.0 30
gpt-4o-mini    en-de translation_quality_ref_free  P1_target_rubric P2_explicit_pivot        0.133333               0.0 30
gpt-4o-mini    en-de translation_quality_ref_free P0_direct_english      P3_bilingual        0.133333               0.0 30
gpt-4o-mini    en-de translation_quality_ref_free P2_explicit_pivot      P3_bilingual        0.133333               0.0 30
gpt-4o-mini    en-de translation_quality_ref_free  P1_target_rubric      P3_bilingual        0.133333               0.0 30
gpt-4o-mini    en-ru translation_quality_ref_free P0_direct_english      P3_bilingual        0.100000               0.0 30
```
