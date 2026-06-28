# Pilot Summary

Responses: 640
Parsed responses: 640
Estimated API cost from returned usage: $0.0395

## Best protocol correlations

```text
judge_model language         dimension          protocol          protocol_name  n  n_parsed  parse_rate  human_positive_rate  mean_judge_score  spearman  spearman_ci_low  spearman_ci_high  auroc  estimated_cost_usd
gpt-4o-mini    es-ES comprehensibility      P3_bilingual       Bilingual rubric 20        20         1.0                  0.5              2.70  0.898027         0.801456          0.930474  1.000            0.001351
gpt-4o-mini       tr comprehensibility P0_direct_english  Direct English rubric 20        20         1.0                  0.5              3.10  0.885116         0.750880          0.953463  0.985            0.001194
gpt-4o-mini    es-ES comprehensibility P0_direct_english  Direct English rubric 20        20         1.0                  0.5              2.80  0.868986         0.765167          0.925250  0.985            0.001166
gpt-4o-mini    es-ES comprehensibility P2_explicit_pivot Explicit English pivot 20        20         1.0                  0.5              3.10  0.815562         0.633318          0.914026  0.955            0.001181
gpt-4o-mini    en-US comprehensibility P2_explicit_pivot Explicit English pivot 20        20         1.0                  0.5              3.10  0.783966         0.578579          0.895433  0.940            0.001170
gpt-4o-mini    en-US comprehensibility P0_direct_english  Direct English rubric 20        20         1.0                  0.5              2.80  0.781181         0.571863          0.896144  0.940            0.001107
gpt-4o-mini    es-ES comprehensibility  P1_target_rubric Target-language rubric 20        20         1.0                  0.5              2.25  0.755191         0.580280          0.897077  0.910            0.001193
gpt-4o-mini    en-US comprehensibility  P1_target_rubric Target-language rubric 20        20         1.0                  0.5              2.45  0.738170         0.528850          0.884332  0.910            0.001029
gpt-4o-mini    en-US           grammar      P3_bilingual       Bilingual rubric 20        20         1.0                  0.5              3.85  0.716217         0.532309          0.879125  0.880            0.001223
gpt-4o-mini    en-US           grammar P2_explicit_pivot Explicit English pivot 20        20         1.0                  0.5              4.20  0.710096         0.388516          0.917891  0.870            0.001176
```

## Largest protocol shifts

```text
judge_model language         dimension        protocol_a        protocol_b  mean_abs_shift  median_abs_shift  n
gpt-4o-mini       tr comprehensibility  P1_target_rubric P2_explicit_pivot            1.50               1.5 20
gpt-4o-mini       tr           grammar  P1_target_rubric P2_explicit_pivot            1.40               1.0 20
gpt-4o-mini       vi           grammar  P1_target_rubric P2_explicit_pivot            1.35               1.0 20
gpt-4o-mini       tr           grammar P2_explicit_pivot      P3_bilingual            1.10               1.0 20
gpt-4o-mini       vi comprehensibility  P1_target_rubric P2_explicit_pivot            1.05               1.0 20
gpt-4o-mini       tr comprehensibility P2_explicit_pivot      P3_bilingual            1.00               1.0 20
gpt-4o-mini       tr           grammar P0_direct_english P2_explicit_pivot            0.95               1.0 20
gpt-4o-mini    en-US           grammar  P1_target_rubric P2_explicit_pivot            0.95               1.0 20
gpt-4o-mini    es-ES           grammar  P1_target_rubric P2_explicit_pivot            0.90               1.0 20
gpt-4o-mini       tr comprehensibility P0_direct_english P2_explicit_pivot            0.90               1.0 20
gpt-4o-mini       vi comprehensibility P0_direct_english P2_explicit_pivot            0.90               1.0 20
gpt-4o-mini    es-ES comprehensibility  P1_target_rubric P2_explicit_pivot            0.85               1.0 20
```
