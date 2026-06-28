# Run Inventory

Generated from current JSONL artifacts. Costs are returned usage estimates and are incremental for each run. Token counts are from returned API usage metadata and do not depend on a current pricing table.

```text
                run  base_items  judge_calls  parsed_calls  parse_rate  unique_judged_items  observed_cost_usd  cost_per_1000_judge_calls  api_calls_including_translations  input_tokens  output_tokens  total_tokens  avg_total_tokens_per_api_call
      candidate n50         400         1600          1600         1.0                  400           0.111354                   0.069596                              2000        382769          89897        472666                     236.333000
candidate audit n25         200          800           800         1.0                  200           0.143124                   0.178906                              1005        198162          48377        246539                     245.312438
       semantic n30          90          360           360         1.0                   90           0.065928                   0.183135                               450        252403          46780        299183                     664.851111
  wmt reference n30          90          300           300         1.0                   90           0.029530                   0.098433                               390        108238          22157        130395                     334.346154
   wmt ref-free n30          90          300           300         1.0                   90           0.020639                   0.068796                               300         84237          13339         97576                     325.253333
 wmt ref-free audit          60          120           120         1.0                   60           0.022102                   0.184183                               120         32659           5649         38308                     319.233333
```
