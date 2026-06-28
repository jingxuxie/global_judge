# Pilot Summary

Responses: 800
Parsed responses: 800
Estimated API cost from returned usage: $0.1350

## Best protocol correlations

```text
 judge_model language         dimension          protocol          protocol_name  n  n_parsed  parse_rate  human_positive_rate  mean_judge_score  spearman  spearman_ci_low  spearman_ci_high    auroc  estimated_cost_usd
gpt-4.1-mini       tr comprehensibility      P3_bilingual       Bilingual rubric 25        25         1.0                 0.48              2.68  0.796060         0.623707          0.896659 0.945513            0.005051
gpt-4.1-mini    es-ES comprehensibility P0_direct_english  Direct English rubric 25        25         1.0                 0.48              3.40  0.738452         0.504197          0.912318 0.907051            0.003776
gpt-4.1-mini       tr comprehensibility P0_direct_english  Direct English rubric 25        25         1.0                 0.48              2.88  0.729340         0.491376          0.866912 0.910256            0.004257
gpt-4.1-mini       tr comprehensibility  P1_target_rubric Target-language rubric 25        25         1.0                 0.48              2.64  0.718527         0.403883          0.881815 0.903846            0.004694
gpt-4.1-mini    es-ES comprehensibility      P3_bilingual       Bilingual rubric 25        25         1.0                 0.48              3.20  0.690504         0.403461          0.909081 0.884615            0.004458
gpt-4.1-mini    es-ES comprehensibility  P1_target_rubric Target-language rubric 25        25         1.0                 0.48              2.92  0.675478         0.419781          0.894429 0.875000            0.003873
gpt-4.1-mini    en-US comprehensibility P2_explicit_pivot Explicit English pivot 25        25         1.0                 0.48              3.52  0.649019         0.383668          0.853837 0.862179            0.003972
gpt-4.1-mini    en-US           grammar P0_direct_english  Direct English rubric 25        25         1.0                 0.48              4.12  0.644503         0.322318          0.889327 0.846154            0.003657
gpt-4.1-mini    en-US           grammar P2_explicit_pivot Explicit English pivot 25        25         1.0                 0.48              4.16  0.631970         0.328973          0.852732 0.833333            0.003970
gpt-4.1-mini    en-US comprehensibility P0_direct_english  Direct English rubric 25        25         1.0                 0.48              3.24  0.610425         0.325361          0.841138 0.842949            0.003620
```

## Largest protocol shifts

```text
 judge_model language         dimension        protocol_a        protocol_b  mean_abs_shift  median_abs_shift  n
gpt-4.1-mini       tr comprehensibility P2_explicit_pivot      P3_bilingual            1.16               1.0 25
gpt-4.1-mini       tr comprehensibility P0_direct_english P2_explicit_pivot            1.04               1.0 25
gpt-4.1-mini       tr comprehensibility  P1_target_rubric P2_explicit_pivot            1.04               1.0 25
gpt-4.1-mini       vi comprehensibility P0_direct_english P2_explicit_pivot            0.96               1.0 25
gpt-4.1-mini       vi comprehensibility P2_explicit_pivot      P3_bilingual            0.96               1.0 25
gpt-4.1-mini    es-ES           grammar P0_direct_english P2_explicit_pivot            0.92               1.0 25
gpt-4.1-mini    es-ES           grammar P2_explicit_pivot      P3_bilingual            0.88               0.0 25
gpt-4.1-mini       tr           grammar P0_direct_english P2_explicit_pivot            0.84               1.0 25
gpt-4.1-mini       vi           grammar P0_direct_english P2_explicit_pivot            0.84               1.0 25
gpt-4.1-mini       vi           grammar P2_explicit_pivot      P3_bilingual            0.84               1.0 25
gpt-4.1-mini       tr           grammar  P1_target_rubric P2_explicit_pivot            0.84               1.0 25
gpt-4.1-mini       vi           grammar  P1_target_rubric P2_explicit_pivot            0.80               1.0 25
```
