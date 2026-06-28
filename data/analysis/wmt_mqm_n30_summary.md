# Pilot Summary

Responses: 300
Parsed responses: 300
Estimated API cost from returned usage: $0.0219

## Best protocol correlations

```text
judge_model language           dimension          protocol          protocol_name  n  n_parsed  parse_rate  human_positive_rate  mean_judge_score  spearman  spearman_ci_low  spearman_ci_high    auroc  estimated_cost_usd
gpt-4o-mini    en-de translation_quality      P3_bilingual       Bilingual rubric 30        30         1.0                  0.5          3.866667  0.470591         0.298444          0.668289 0.688889            0.002450
gpt-4o-mini    en-de translation_quality P2_explicit_pivot Explicit English pivot 30        30         1.0                  0.5          3.866667  0.398410         0.126478          0.629983 0.677778            0.001988
gpt-4o-mini    en-de translation_quality P0_direct_english  Direct English rubric 30        30         1.0                  0.5          4.066667  0.387585         0.128089          0.610296 0.673333            0.002008
gpt-4o-mini    zh-en translation_quality P0_direct_english  Direct English rubric 30        30         1.0                  0.5          3.533333  0.354159         0.000000          0.689390 0.693333            0.002058
gpt-4o-mini    en-ru translation_quality  P1_target_rubric Target-language rubric 30        30         1.0                  0.5          3.766667  0.320193        -0.005365          0.573834 0.648889            0.002285
gpt-4o-mini    en-de translation_quality  P1_target_rubric Target-language rubric 30        30         1.0                  0.5          3.966667  0.318126         0.151620          0.465195 0.595556            0.002385
gpt-4o-mini    zh-en translation_quality P2_explicit_pivot Explicit English pivot 30        30         1.0                  0.5          3.533333  0.303515        -0.034882          0.642396 0.668889            0.002033
gpt-4o-mini    en-ru translation_quality P0_direct_english  Direct English rubric 30        30         1.0                  0.5          3.666667  0.164959        -0.223100          0.482368 0.573333            0.002100
gpt-4o-mini    en-ru translation_quality      P3_bilingual       Bilingual rubric 30        30         1.0                  0.5          3.600000  0.159089        -0.226215          0.489134 0.575556            0.002538
gpt-4o-mini    en-ru translation_quality P2_explicit_pivot Explicit English pivot 30        30         1.0                  0.5          3.666667  0.134898        -0.258070          0.478010 0.564444            0.002090
```

## Largest protocol shifts

```text
judge_model language           dimension        protocol_a        protocol_b  mean_abs_shift  median_abs_shift  n
gpt-4o-mini    zh-en translation_quality P0_direct_english P2_explicit_pivot        0.533333               0.0 30
gpt-4o-mini    en-de translation_quality P0_direct_english P2_explicit_pivot        0.200000               0.0 30
gpt-4o-mini    en-de translation_quality P0_direct_english      P3_bilingual        0.200000               0.0 30
gpt-4o-mini    en-ru translation_quality P0_direct_english  P1_target_rubric        0.166667               0.0 30
gpt-4o-mini    en-de translation_quality P0_direct_english  P1_target_rubric        0.166667               0.0 30
gpt-4o-mini    en-ru translation_quality  P1_target_rubric      P3_bilingual        0.166667               0.0 30
gpt-4o-mini    en-de translation_quality  P1_target_rubric P2_explicit_pivot        0.166667               0.0 30
gpt-4o-mini    en-de translation_quality P2_explicit_pivot      P3_bilingual        0.133333               0.0 30
gpt-4o-mini    en-de translation_quality  P1_target_rubric      P3_bilingual        0.100000               0.0 30
gpt-4o-mini    en-ru translation_quality  P1_target_rubric P2_explicit_pivot        0.100000               0.0 30
gpt-4o-mini    en-ru translation_quality P0_direct_english P2_explicit_pivot        0.066667               0.0 30
gpt-4o-mini    en-ru translation_quality P0_direct_english      P3_bilingual        0.066667               0.0 30
```
