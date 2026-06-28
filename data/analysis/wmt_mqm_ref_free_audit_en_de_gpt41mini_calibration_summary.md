# Calibration Summary

Eligible test groups: 2
Mean test balanced-accuracy delta: 0.000
Median test balanced-accuracy delta: 0.000

## Largest Test Improvements

```text
 judge_model language                    dimension          protocol          protocol_name split  n  calibration_fraction  baseline_threshold  calibrated_threshold  calibration_balanced_accuracy  baseline_accuracy  calibrated_accuracy  delta_accuracy  baseline_balanced_accuracy  calibrated_balanced_accuracy  delta_balanced_accuracy  baseline_f1  calibrated_f1  delta_f1
gpt-4.1-mini    en-de translation_quality_ref_free P2_explicit_pivot Explicit English pivot  test 22                   0.3                   4                     4                          0.625           0.636364             0.636364             0.0                    0.636364                      0.636364                      0.0     0.733333       0.733333  0.000000
gpt-4.1-mini    en-de translation_quality_ref_free      P3_bilingual       Bilingual rubric  test 22                   0.3                   4                     5                          0.750           0.727273             0.727273             0.0                    0.727273                      0.727273                      0.0     0.785714       0.750000 -0.035714
```

## Largest Test Degradations

```text
 judge_model language                    dimension          protocol          protocol_name split  n  calibration_fraction  baseline_threshold  calibrated_threshold  calibration_balanced_accuracy  baseline_accuracy  calibrated_accuracy  delta_accuracy  baseline_balanced_accuracy  calibrated_balanced_accuracy  delta_balanced_accuracy  baseline_f1  calibrated_f1  delta_f1
gpt-4.1-mini    en-de translation_quality_ref_free P2_explicit_pivot Explicit English pivot  test 22                   0.3                   4                     4                          0.625           0.636364             0.636364             0.0                    0.636364                      0.636364                      0.0     0.733333       0.733333  0.000000
gpt-4.1-mini    en-de translation_quality_ref_free      P3_bilingual       Bilingual rubric  test 22                   0.3                   4                     5                          0.750           0.727273             0.727273             0.0                    0.727273                      0.727273                      0.0     0.785714       0.750000 -0.035714
```
