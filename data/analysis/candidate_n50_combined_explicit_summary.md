# Pilot Summary

Responses: 1600
Parsed responses: 1600
Estimated API cost from returned usage: $0.0979

## Best protocol correlations

```text
judge_model language         dimension          protocol          protocol_name  n  n_parsed  parse_rate  human_positive_rate  mean_judge_score  spearman  spearman_ci_low  spearman_ci_high  auroc  estimated_cost_usd
gpt-4o-mini    en-US comprehensibility P0_direct_english  Direct English rubric 50        50         1.0                  0.5              3.00  0.731180         0.566474          0.839329 0.9104            0.002769
gpt-4o-mini    en-US comprehensibility P2_explicit_pivot Explicit English pivot 50        50         1.0                  0.5              3.30  0.710816         0.552842          0.829626 0.8976            0.002991
gpt-4o-mini    en-US comprehensibility      P3_bilingual       Bilingual rubric 50        50         1.0                  0.5              2.92  0.701414         0.528253          0.826468 0.8904            0.003054
gpt-4o-mini    en-US comprehensibility  P1_target_rubric Target-language rubric 50        50         1.0                  0.5              2.50  0.699263         0.516298          0.836066 0.8808            0.002606
gpt-4o-mini    es-ES comprehensibility P0_direct_english  Direct English rubric 50        50         1.0                  0.5              2.78  0.652250         0.432667          0.807256 0.8640            0.002837
gpt-4o-mini       tr comprehensibility P0_direct_english  Direct English rubric 50        50         1.0                  0.5              2.78  0.602976         0.359949          0.776845 0.8360            0.003100
gpt-4o-mini    es-ES comprehensibility  P1_target_rubric Target-language rubric 50        50         1.0                  0.5              2.28  0.588809         0.362938          0.754993 0.8272            0.002892
gpt-4o-mini       tr comprehensibility      P3_bilingual       Bilingual rubric 50        50         1.0                  0.5              2.60  0.574806         0.337855          0.772686 0.8224            0.003701
gpt-4o-mini    es-ES comprehensibility      P3_bilingual       Bilingual rubric 50        50         1.0                  0.5              2.56  0.561845         0.312887          0.756013 0.8088            0.003284
gpt-4o-mini       tr comprehensibility  P1_target_rubric Target-language rubric 50        50         1.0                  0.5              2.44  0.555577         0.316375          0.751323 0.8104            0.003561
```

## Largest protocol shifts

```text
judge_model language         dimension        protocol_a        protocol_b  mean_abs_shift  median_abs_shift  n
gpt-4o-mini       vi           grammar  P1_target_rubric P2_explicit_pivot            1.20               1.0 50
gpt-4o-mini       tr           grammar  P1_target_rubric P2_explicit_pivot            0.96               1.0 50
gpt-4o-mini       vi comprehensibility P2_explicit_pivot      P3_bilingual            0.96               1.0 50
gpt-4o-mini    en-US           grammar  P1_target_rubric P2_explicit_pivot            0.94               1.0 50
gpt-4o-mini       vi comprehensibility  P1_target_rubric P2_explicit_pivot            0.90               1.0 50
gpt-4o-mini       tr           grammar P2_explicit_pivot      P3_bilingual            0.90               1.0 50
gpt-4o-mini       vi comprehensibility P0_direct_english P2_explicit_pivot            0.88               1.0 50
gpt-4o-mini    en-US comprehensibility  P1_target_rubric P2_explicit_pivot            0.88               1.0 50
gpt-4o-mini    es-ES           grammar  P1_target_rubric P2_explicit_pivot            0.84               1.0 50
gpt-4o-mini       tr           grammar P0_direct_english P2_explicit_pivot            0.84               1.0 50
gpt-4o-mini    es-ES           grammar P0_direct_english P2_explicit_pivot            0.80               1.0 50
gpt-4o-mini       tr comprehensibility  P1_target_rubric P2_explicit_pivot            0.80               1.0 50
```
