# Dataset Sampling Audit

Generated from processed item JSONL files. WMT audit rows are selected by the item IDs that appear in the targeted audit response caches.

## Run Summary

| Run | Items | Langs | Dims | Pos | Neg | Source Rate | Reference Rate | Mean Candidate Chars |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| candidate n50 | 400 | 4 | 2 | 200 | 200 | 0.0% | 0.0% | 162.8 |
| candidate audit n25 | 200 | 4 | 2 | 96 | 104 | 0.0% | 0.0% | 178.0 |
| semantic n30 | 90 | 3 | 1 | 45 | 45 | 100.0% | 100.0% | 131.5 |
| wmt n30 shared items | 90 | 3 | 1 | 45 | 45 | 100.0% | 100.0% | 116.2 |
| wmt ref-free audit zh-en | 30 | 1 | 1 | 15 | 15 | 100.0% | 100.0% | 120.9 |
| wmt ref-free audit en-de | 30 | 1 | 1 | 15 | 15 | 100.0% | 100.0% | 102.2 |

## Group Summary

| Run | Language | Dimension | N | Pos | Neg | Pos Rate | Mean Candidate Chars | Source Rate | Reference Rate |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| candidate n50 | en-US | comprehensibility | 50 | 25 | 25 | 50.0% | 143.2 | 0.0% | 0.0% |
| candidate n50 | en-US | grammar | 50 | 25 | 25 | 50.0% | 133.5 | 0.0% | 0.0% |
| candidate n50 | es-ES | comprehensibility | 50 | 25 | 25 | 50.0% | 172.1 | 0.0% | 0.0% |
| candidate n50 | es-ES | grammar | 50 | 25 | 25 | 50.0% | 136.4 | 0.0% | 0.0% |
| candidate n50 | tr | comprehensibility | 50 | 25 | 25 | 50.0% | 273.6 | 0.0% | 0.0% |
| candidate n50 | tr | grammar | 50 | 25 | 25 | 50.0% | 150.8 | 0.0% | 0.0% |
| candidate n50 | vi | comprehensibility | 50 | 25 | 25 | 50.0% | 152.7 | 0.0% | 0.0% |
| candidate n50 | vi | grammar | 50 | 25 | 25 | 50.0% | 140.4 | 0.0% | 0.0% |
| candidate audit n25 | en-US | comprehensibility | 25 | 12 | 13 | 48.0% | 99.8 | 0.0% | 0.0% |
| candidate audit n25 | en-US | grammar | 25 | 12 | 13 | 48.0% | 120.6 | 0.0% | 0.0% |
| candidate audit n25 | es-ES | comprehensibility | 25 | 12 | 13 | 48.0% | 171.7 | 0.0% | 0.0% |
| candidate audit n25 | es-ES | grammar | 25 | 12 | 13 | 48.0% | 162.0 | 0.0% | 0.0% |
| candidate audit n25 | tr | comprehensibility | 25 | 12 | 13 | 48.0% | 262.2 | 0.0% | 0.0% |
| candidate audit n25 | tr | grammar | 25 | 12 | 13 | 48.0% | 144.0 | 0.0% | 0.0% |
| candidate audit n25 | vi | comprehensibility | 25 | 12 | 13 | 48.0% | 281.1 | 0.0% | 0.0% |
| candidate audit n25 | vi | grammar | 25 | 12 | 13 | 48.0% | 182.5 | 0.0% | 0.0% |
| semantic n30 | es-ES | main_ideas | 30 | 15 | 15 | 50.0% | 130.1 | 100.0% | 100.0% |
| semantic n30 | tr | main_ideas | 30 | 15 | 15 | 50.0% | 121.0 | 100.0% | 100.0% |
| semantic n30 | vi | main_ideas | 30 | 15 | 15 | 50.0% | 143.4 | 100.0% | 100.0% |
| wmt n30 shared items | en-de | translation_quality | 30 | 15 | 15 | 50.0% | 102.2 | 100.0% | 100.0% |
| wmt n30 shared items | en-ru | translation_quality | 30 | 15 | 15 | 50.0% | 125.4 | 100.0% | 100.0% |
| wmt n30 shared items | zh-en | translation_quality | 30 | 15 | 15 | 50.0% | 120.9 | 100.0% | 100.0% |
| wmt ref-free audit zh-en | zh-en | translation_quality | 30 | 15 | 15 | 50.0% | 120.9 | 100.0% | 100.0% |
| wmt ref-free audit en-de | en-de | translation_quality | 30 | 15 | 15 | 50.0% | 102.2 | 100.0% | 100.0% |
