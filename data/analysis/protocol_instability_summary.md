# Protocol Instability Summary

This file is generated from existing metrics and paired-bootstrap outputs.

## Aggregate Main-Run Claim

Across 17 non-audit task/language cells, the best AUROC protocol is not direct in 11 cells, explicit pivot is the worst protocol in 10 cells, and 6 cells have at least one paired AUROC delta with a bootstrap CI excluding zero.

## Run-Level Summary

```text
                run  n_cells  median_auroc_range  max_auroc_range  median_spearman_range  max_spearman_range  cells_auroc_range_ge_0_10  cells_auroc_range_ge_0_15  cells_best_not_direct  cells_best_not_pivot  cells_pivot_worst  cells_with_significant_auroc_pair  max_mean_abs_score_shift
      candidate n50        8            0.074000         0.165600               0.124175            0.313807                          3                          1                      4                     7                  4                                  2                  1.200000
       semantic n30        3            0.106667         0.124444               0.194722            0.249356                          2                          0                      3                     2                  2                                  1                  0.700000
  wmt reference n30        3            0.084444         0.093333               0.152465            0.185295                          0                          0                      2                     3                  2                                  0                  0.533333
   wmt ref-free n30        3            0.128889         0.220000               0.239734            0.407867                          2                          1                      2                     3                  2                                  3                  0.700000
candidate audit n25        8            0.161859         0.352564               0.287337            0.627615                          7                          5                      5                     6                  4                                  4                  1.160000
 wmt ref-free audit        2            0.081111         0.137778               0.154212            0.248213                          1                          0                      1                     1                  1                                  0                  0.666667
```

## Largest Cell-Level AUROC Ranges

```text
                run language                    dimension     best_protocol    worst_protocol  auroc_range  max_mean_abs_score_shift  n_significant_auroc_pairs
candidate audit n25       tr            comprehensibility      P3_bilingual P2_explicit_pivot     0.352564                  1.160000                          3
candidate audit n25       vi                      grammar P0_direct_english P2_explicit_pivot     0.342949                  0.840000                          3
   wmt ref-free n30    zh-en translation_quality_ref_free P0_direct_english P2_explicit_pivot     0.220000                  0.700000                          1
candidate audit n25       vi            comprehensibility  P1_target_rubric P2_explicit_pivot     0.192308                  0.960000                          0
candidate audit n25    en-US                      grammar P0_direct_english      P3_bilingual     0.169872                  0.280000                          3
      candidate n50       vi            comprehensibility      P3_bilingual P2_explicit_pivot     0.165600                  0.960000                          2
candidate audit n25    es-ES            comprehensibility P0_direct_english P2_explicit_pivot     0.153846                  0.800000                          0
      candidate n50       tr            comprehensibility P0_direct_english P2_explicit_pivot     0.149600                  0.800000                          3
 wmt ref-free audit    zh-en translation_quality_ref_free P0_direct_english P2_explicit_pivot     0.137778                  0.666667                          0
   wmt ref-free n30    en-de translation_quality_ref_free      P3_bilingual P2_explicit_pivot     0.128889                  0.133333                          2
       semantic n30       tr                   main_ideas      P3_bilingual P2_explicit_pivot     0.124444                  0.400000                          0
      candidate n50       vi                      grammar  P1_target_rubric P2_explicit_pivot     0.119200                  1.200000                          0
```
