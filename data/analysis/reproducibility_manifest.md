# Reproducibility Manifest

Paper-facing reproducibility manifest for GlobalJudge protocol-sensitivity experiments.

## Section Summary

| Section | Files | Bytes | Records |
| --- | ---: | ---: | ---: |
| analysis | 76 | 4652314 | 29220 |
| configs | 19 | 24766 | 0 |
| paper | 53 | 2854416 | 0 |
| plan_and_docs | 7 | 144261 | 0 |
| processed_items | 4 | 832515 | 780 |
| prompts | 7 | 5688346 | 3480 |
| raw_data_archives | 5 | 164618758 | 0 |
| responses | 7 | 3309642 | 3480 |
| source_code | 31 | 313138 | 0 |
| translations | 4 | 929511 | 785 |

## Validation Commands

- `/home/eston/anaconda3/envs/global_judge/bin/python -m compileall src`
- `/home/eston/anaconda3/envs/global_judge/bin/python src/validate_paper_claims.py`
- `/home/eston/anaconda3/envs/global_judge/bin/python src/run_release_checks.py`
- `make -C paper`
- `pdfinfo paper/extended_abstract.pdf`
- `rg -n '(T[O]DO|T[B]D|F[I]XME|p[l]aceholder|0\\.3706|0\\.3499|0\\.3403|significant pivot dr[o]p|including a signific[a]nt|single global w[i]nner)' README.md paper data/analysis/current_research_status.md src configs`
- `rg -n '(undefined|Undefined|Citation|Reference|Overfull|Underfull|Warning|Error|Rerun)' paper/main.log`

## Key Paper-Facing Files

| Section | Path | Records | SHA256 |
| --- | --- | ---: | --- |
| processed_items | `data/processed/audit_gpt41mini_n25_items.jsonl` | 200 | `b146e9ca2f5c68c013851e088685125fda5600965bf4c61ab36565e37cd5baa9` |
| processed_items | `data/processed/candidate_n50_items.jsonl` | 400 | `8b4467ce77769f16c9301b0a3d060d279a8a34ec70a363bec5ff2a9a9e38329a` |
| processed_items | `data/processed/semantic_xlsum_n30_items.jsonl` | 90 | `1f1dd4ec43143bd4521588a32dc296fc3ba8c6a90ab9ee18ac9ea0d991a1112a` |
| processed_items | `data/processed/wmt_mqm_n30_items.jsonl` | 90 | `9e6bf2e2cb0b6caa7834e9cbec2e6a3b091ba8291f39ac4a869f9dce92ad2669` |
| prompts | `data/prompts/audit_gpt41mini_n25_combined_explicit_prompts.jsonl` | 800 | `9f4d60d77687cd9a2c82fd03b5033bb8cdcefb757ec39d615fa04334c9b6001a` |
| prompts | `data/prompts/candidate_n50_combined_explicit_prompts.jsonl` | 1600 | `2664cb6228d00222c0a346ad9eac873512fe2a5174901d327d4cccb0ffc51b15` |
| prompts | `data/prompts/semantic_xlsum_n30_prompts.jsonl` | 360 | `0d301808382edb13ad0bb7cb2bcefbdaaf213a05960e01f06893593aa0adc98f` |
| prompts | `data/prompts/wmt_mqm_n30_prompts.jsonl` | 300 | `797b6d5182ad306c641352bdb15225b05337883cfe1dc32ee2db2d48fa8f9c6d` |
| prompts | `data/prompts/wmt_mqm_ref_free_audit_en_de_gpt41mini_prompts.jsonl` | 60 | `7e87e98e08e18cad0ba20ebfcd6596846895fd6bb5f27efcebc831104aa1c336` |
| prompts | `data/prompts/wmt_mqm_ref_free_audit_zh_en_gpt41mini_prompts.jsonl` | 60 | `87cade5f851cca45b277e8ebd622b0a59f3316ba86226cc3f2ce80cc7ca504f9` |
| prompts | `data/prompts/wmt_mqm_ref_free_n30_prompts.jsonl` | 300 | `0731d8b4add7fa50b4aa08695f376fb61ff87112e573141acae3780a3b977971` |
| responses | `data/responses/audit_gpt41mini_n25_combined_explicit_responses.jsonl` | 800 | `f300517122e0b2caec66970449199c7d5bd3b58497d440a8481ce67fff049b57` |
| responses | `data/responses/candidate_n50_combined_explicit_responses.jsonl` | 1600 | `623030b98f78b5157edbdd623703fad9cc75452844b13767a737c8a0eded4eda` |
| responses | `data/responses/semantic_xlsum_n30_responses.jsonl` | 360 | `a9a0193721978679533fdbd144d677ff14f307ba2454c8c61dc14f410c6ed2e0` |
| responses | `data/responses/wmt_mqm_n30_responses.jsonl` | 300 | `2f39df13994ca0fe49fc9a0185233864bba1fff3f4f192d50a69d40c6abab0a1` |
| responses | `data/responses/wmt_mqm_ref_free_audit_en_de_gpt41mini_responses.jsonl` | 60 | `d145a85c29284510740c87ba88f6d08a0ce74d8ec08a74c17d778a5383a076d1` |
| responses | `data/responses/wmt_mqm_ref_free_audit_zh_en_gpt41mini_responses.jsonl` | 60 | `584514794ecdd4fc3588b56b1d483ad309fa283d77a0993dc89ac375d31c1585` |
| responses | `data/responses/wmt_mqm_ref_free_n30_responses.jsonl` | 300 | `fa3fb1842fbeb65c923660faa04c5cad8af44197d376a962bd3aab2642d9b7e9` |
| analysis | `data/analysis/audit_gpt41mini_n12_combined_explicit_calibration.csv` | 64 | `d691e62e4d677be7c7554eb69a92a1403cec05d05fcd6df644ac5ee9b4f91891` |
| analysis | `data/analysis/audit_gpt41mini_n12_combined_explicit_metrics.csv` | 32 | `a286e2ab3bf41e389ca1ba6acf524e90bd4017ddebe59b703e230a5b7b9f7175` |
| analysis | `data/analysis/audit_gpt41mini_n12_combined_explicit_metrics_language_gaps.csv` | 8 | `306b92f7d869c2af5619043506010bbc4080c7d43ca526e821c390802faa846c` |
| analysis | `data/analysis/audit_gpt41mini_n12_combined_explicit_metrics_pairwise_bootstrap.csv` | 48 | `5b68eda997a955ef6c20e497f50c977e4290439e4dfa703d6ca1aff6c035c238` |
| analysis | `data/analysis/audit_gpt41mini_n12_combined_explicit_protocol_shifts.csv` | 48 | `23bf3c48795644850613e7de43546b57c17ea21d513110b38be38139d55ff503` |
| analysis | `data/analysis/audit_gpt41mini_n25_combined_explicit_calibration.csv` | 64 | `be229e4d901de60883c0ea2ff78236e6f927f2947d458c46f6646df1b77ae437` |
| analysis | `data/analysis/audit_gpt41mini_n25_combined_explicit_metrics.csv` | 32 | `cbf8dc4e65bbe43ea3b2f3867f2dc22c2a15864a105397572f159b01403122f6` |
| analysis | `data/analysis/audit_gpt41mini_n25_combined_explicit_metrics_language_gaps.csv` | 8 | `69cffa251ed47bd8e40f29ec111cb9110e1f049872928325c08e6141fe7e6162` |
| analysis | `data/analysis/audit_gpt41mini_n25_combined_explicit_metrics_pairwise_bootstrap.csv` | 48 | `ad8b4a5684c8a3ea4ef793f87710afeec8629904219de5b7b2e8a1747da1bfef` |
| analysis | `data/analysis/audit_gpt41mini_n25_combined_explicit_protocol_shifts.csv` | 48 | `70d669de4fa729724fc555a323803cfaf8ee1c62c557a43a412039ef0b35eaa9` |
| analysis | `data/analysis/calibration_learning_curve_raw.csv` | 23400 | `0bfe22853e78aa2590174cc353248a4e99bc269c7cb8c895db95b5e869ea492a` |
| analysis | `data/analysis/calibration_learning_curve_summary.csv` | 34 | `ba78f2b3ede39264b1225d1b57aaa3439a2329c993859710c280deffe44bffe5` |
| analysis | `data/analysis/candidate_n50_combined_explicit_calibration.csv` | 64 | `a2959bf451514affb240e7a5a47e728bd1994516cac208146f26875697edc751` |
| analysis | `data/analysis/candidate_n50_combined_explicit_metrics.csv` | 32 | `53a331f3e84a5d014dce094fb113dbf8b3ea226d8284d2070eb40784bfe6d994` |
| analysis | `data/analysis/candidate_n50_combined_explicit_metrics_language_gaps.csv` | 8 | `60fa32629563944c6622cc46d5de19faf0754c6e91529a2eeb69ce6b924cfd5b` |
| analysis | `data/analysis/candidate_n50_combined_explicit_metrics_pairwise_bootstrap.csv` | 48 | `6028bc71c3c63f3612c9ddcf59fee1843dc14e823ae348839232ef722be4e4f2` |
| analysis | `data/analysis/candidate_n50_combined_explicit_protocol_shifts.csv` | 48 | `9af50044f60382c072be0aa55cc0613e6cd538d4c433e96d1ffebeb8c5d247ce` |
| analysis | `data/analysis/claim_evidence_matrix.csv` | 9 | `88cdfef41f699363e045124f4f7565731a79471d6f063e50cb9b289a13aaa9d1` |
| analysis | `data/analysis/claim_evidence_matrix.md` |  | `a2a110e7b96ae6938fa467309f37c0f860e4057567f8410bd096b3941dbe1dc1` |
| analysis | `data/analysis/completion_audit.json` |  | `ef15dd08c448902fa9fdeb6c8ad7c863bc6d68b7fa026a429083b9e11d35cba7` |
| analysis | `data/analysis/completion_audit.md` |  | `2202afa0151734cecd631bedb5a6486aa2125161078354a30565abb51decc417` |
| analysis | `data/analysis/dataset_sampling_audit.md` |  | `0bfe47281b0aa31fe1544eadcd621173ef6a7cac7c52529a2a629b861bd2dad9` |
| analysis | `data/analysis/dataset_sampling_groups.csv` | 24 | `c908538ce7147d82097515200c94b588486c6d18829f9d0b0363f4f9b6fb0006` |
| analysis | `data/analysis/dataset_sampling_items.csv` | 840 | `89218a7abcab6e89bb5ee6dc80287e6c3f639943e5506a9faed9b5245f38d5c6` |
| analysis | `data/analysis/dataset_sampling_summary.csv` | 6 | `3957d0ea552cd11c9ab4d74d5afb2180eeeb49bf9a2d6ee098b55754eb7fcff3` |
| analysis | `data/analysis/pilot_metrics.csv` | 32 | `f5dcc7a0e5a78658a2cb857cc349c5605ab3c193d7c142b256fb866b8102bdaa` |
| analysis | `data/analysis/pilot_n20_combined_explicit_calibration.csv` | 64 | `22dd17c3aa534e19379e71aa1a2044a584d1d1328efaaccf497b34a63f04f33d` |
| analysis | `data/analysis/pilot_n20_combined_explicit_metrics.csv` | 32 | `41c840a6571b64658b3adf308f660f9495cd8cc917c641f1747ec22e9bdb53e6` |
| analysis | `data/analysis/pilot_n20_combined_explicit_protocol_shifts.csv` | 48 | `e24c3345f5f36375e96f5777a7e645ca3a8f4e967c9784824130f1c05561012a` |
| analysis | `data/analysis/pilot_n20_metrics.csv` | 32 | `b8fb772ed8b93cc4d357f363f60acaada5908007ed59e6299308fa3d2fec25dc` |
| analysis | `data/analysis/pilot_n20_protocol_shifts.csv` | 48 | `98f1c17b4ae5a81bfe8e773409eb8488259adfc54a1f5e37d9e5931758f05757` |
| analysis | `data/analysis/pilot_protocol_shifts.csv` | 48 | `37a887ebb98a7beaee1193c46eac77c5a06361742d794d98931badcd832a1a03` |
| analysis | `data/analysis/prompt_inventory.csv` | 3480 | `4a3d7debbf2ff84ff80cb5bf39df03342a4698ed33115db36f0ef50257c3b155` |
| analysis | `data/analysis/prompt_inventory.md` |  | `7b7086a011575a6ff0bb9d176a976fa23e858b06f8b23a91b88b2efdfb018b1c` |
| analysis | `data/analysis/prompt_inventory_summary.csv` | 6 | `78985a33370098d7bb1341c39f1323b588282e1b84c2ab32c2542d786ff7ceb8` |
| analysis | `data/analysis/prompt_representatives.csv` | 23 | `00457ae1396cbebeab413b7ada119c7c0bf95e1eb1e7c0090ebb3744b7707bc1` |
| analysis | `data/analysis/protocol_instability_cells.csv` | 27 | `4e24a94693e3e60d059b2bfebd3dc0b7bda255909b60f2a8099d29dcc7487476` |
| analysis | `data/analysis/protocol_instability_summary.csv` | 6 | `03ba91b933b9437de10418021a0f02bc69dccf796c9e23eb7c921f8d65a174fb` |
| analysis | `data/analysis/qualitative_protocol_examples.csv` | 16 | `7aa846578990d2e9eecb48cab85ad6fcfcaef6249b4ce67dd253a3e47c2a8a76` |
| analysis | `data/analysis/release_validation_report.json` |  | `1f1e83f80e9d81cd0b457ad6f69afd608fab755ec4ef78849f4140d61aa93c1f` |
| analysis | `data/analysis/release_validation_report.md` |  | `067142f2a5d7368bd58f9372e6546203adefd018e5408a7acfa43ab498e2a7b3` |
| analysis | `data/analysis/repeatability_control_details.csv` | 56 | `f5c159def6e440048b65855e3a4a50de5b676a54824bb92ede67fd4c187cf409` |
| analysis | `data/analysis/repeatability_control_summary.csv` | 2 | `1db3d29ddda2d782dc7f2978cdca15f8e6273978d87ba538d7e6638eb64b5e03` |
| analysis | `data/analysis/rq_contribution_matrix.csv` | 10 | `ed5ce53531ffd296e5638b63cd92c6e9a67949e7ec825a3bee87a9ce4102af65` |
| analysis | `data/analysis/rq_contribution_matrix.md` |  | `f8ef294d021faa3cb63d5017bb25639e122351a24f441bc79aca9998890cea0d` |
| analysis | `data/analysis/run_inventory.csv` | 6 | `160e13633bf544f99a5d9919ead8b6c0418c2587d76694afc19e6d5aace1f6a6` |
| analysis | `data/analysis/score_threshold_diagnostic_groups.csv` | 96 | `2f1912af5bdfdd30f327b6dcd100405bafa11ec8e01404748427e67316ca94c2` |
| analysis | `data/analysis/score_threshold_diagnostic_summary.csv` | 5 | `68352746a6a90ac75271693588542606e718742c28b53e6cc4bec4a5f92372e4` |
| analysis | `data/analysis/semantic_xlsum_n30_calibration.csv` | 24 | `647436e3df2dbba34ed3eb025ca40e93f1030f59f2e6404eaee95a94878e90b0` |
| analysis | `data/analysis/semantic_xlsum_n30_metrics.csv` | 12 | `8d1807badc8812bd7a05215ea2f6300cde6ede77cca03f7df0730e05e9727c07` |
| analysis | `data/analysis/semantic_xlsum_n30_metrics_language_gaps.csv` | 4 | `e58ed02a6630aba600abf2116b14b30882c626dbe5807a7f1338a3a0a9efabb9` |
| analysis | `data/analysis/semantic_xlsum_n30_metrics_pairwise_bootstrap.csv` | 18 | `6a5448e9effbb91001576dfad699ab7979a8f4e762f0655d2d254e3767d5c0c2` |
| analysis | `data/analysis/semantic_xlsum_n30_protocol_shifts.csv` | 18 | `2c5a014ddd079d75d83c87355bdc280cd8a00db7fb0497cceaacf5bb942473b6` |
| analysis | `data/analysis/semantic_xlsum_pilot_calibration.csv` | 24 | `713b9c7eaaef20f7daaad3f71a477dfbd851b3431604d9101dffd4e6b1e9b2a3` |
| analysis | `data/analysis/semantic_xlsum_pilot_metrics.csv` | 12 | `3406dd1a38669052127fab4a97277a3ddf475dee3689216db16079ebd766b3d1` |
| analysis | `data/analysis/semantic_xlsum_pilot_protocol_shifts.csv` | 18 | `31d6f997a7b202c51ca120cd5d4d98fb174c11273defca7b9e535a5dbec80c11` |
| analysis | `data/analysis/wmt_mqm_n30_calibration.csv` | 20 | `60602b148af17b5f9ce873843eca989f100b234ede2c7ff7a0205cbda7cf4f7e` |
| analysis | `data/analysis/wmt_mqm_n30_metrics.csv` | 10 | `d9c5621a74a86b162ea2a8438ba6681383c21dc342da3618ffdcae55664aaa51` |
| analysis | `data/analysis/wmt_mqm_n30_metrics_language_gaps.csv` | 4 | `6c7d43b9da92d9375b8675c8f11c7779628366867ceb52b5996bf095c0a03364` |
| analysis | `data/analysis/wmt_mqm_n30_metrics_pairwise_bootstrap.csv` | 13 | `ce4284c61971ae0fb9388b9124486c77dd42fcdfb4785eaa29623f9b7d1fc228` |
| analysis | `data/analysis/wmt_mqm_n30_protocol_shifts.csv` | 13 | `702be0751d550123668adfbd11495a9d08a0c049c56bf02f3de96bb9d3705161` |
| analysis | `data/analysis/wmt_mqm_ref_free_audit_en_de_gpt41mini_calibration.csv` | 4 | `631e780ae3ea55b717747ca5f007ebb26939b03772826ecc2f7d778330a59d2f` |
| analysis | `data/analysis/wmt_mqm_ref_free_audit_en_de_gpt41mini_metrics.csv` | 2 | `b984d0cf1f08b3c837a1f897a724424cf53697d338b24e087b9e7f7a3df7140d` |
| analysis | `data/analysis/wmt_mqm_ref_free_audit_en_de_gpt41mini_metrics_language_gaps.csv` | 2 | `560265aba0969512dfb7e4df65d0c5d7c14a0907629cd64ccfbc3ba94b80ebd4` |
| analysis | `data/analysis/wmt_mqm_ref_free_audit_en_de_gpt41mini_metrics_pairwise_bootstrap.csv` | 1 | `5a86012cd0b586d7b9083b80f5650af37cbf66b3ab067fdbe4685d1a282af77a` |
| analysis | `data/analysis/wmt_mqm_ref_free_audit_en_de_gpt41mini_protocol_shifts.csv` | 1 | `2496e1b12476205a682bb163446102877eee7991836eab57287a18b0a60347d4` |
| analysis | `data/analysis/wmt_mqm_ref_free_audit_zh_en_gpt41mini_calibration.csv` | 4 | `f6e386f80cb0a5a3706727d6229efd7756f8fff540525fad93b045c40087d46b` |
| analysis | `data/analysis/wmt_mqm_ref_free_audit_zh_en_gpt41mini_metrics.csv` | 2 | `857f9fae6378f895e9cd6217fd0b3639ad4ae6d9e0f474e5ec262b098e3ea66b` |
| analysis | `data/analysis/wmt_mqm_ref_free_audit_zh_en_gpt41mini_metrics_language_gaps.csv` | 2 | `a0b14021844336811578789e4ffa6cbf387be5b2814986958695e8ff4f224831` |
| analysis | `data/analysis/wmt_mqm_ref_free_audit_zh_en_gpt41mini_metrics_pairwise_bootstrap.csv` | 1 | `b0f2af912d1ae730e9432cc542c90bc46b0a1c99ab10671f992bf270af8560b7` |
| analysis | `data/analysis/wmt_mqm_ref_free_audit_zh_en_gpt41mini_protocol_shifts.csv` | 1 | `283ff112cb1e6bb0591f1697fdd7ecb580d70d4ee2d3d00596617cdd0e2bd0f3` |
| analysis | `data/analysis/wmt_mqm_ref_free_n30_calibration.csv` | 20 | `1dbc8e86eff9ae5066ae2b864e6b8832ffacbfa7a3672fc0d832a913f01870fc` |
| analysis | `data/analysis/wmt_mqm_ref_free_n30_metrics.csv` | 10 | `b56d5b4711116d736a8f10ab6ec4250f2d5743adf81a3cb667c6f8aa61fe23f3` |
| analysis | `data/analysis/wmt_mqm_ref_free_n30_metrics_language_gaps.csv` | 4 | `161e9207403d437e244c4cfbdcdf028d08cd6ecad04c41a0e58e223f9072e076` |
| analysis | `data/analysis/wmt_mqm_ref_free_n30_metrics_pairwise_bootstrap.csv` | 13 | `cfca35cd719535f3e399fd4836235562005abb72ba56652dcf51738dc333667c` |
| analysis | `data/analysis/wmt_mqm_ref_free_n30_protocol_shifts.csv` | 13 | `a2f39cfcb083df78b91ac3fa40ba758b523c35d255c1ab22914f2c1c198a3c6d` |
| paper | `paper/Makefile` |  | `65b360a7348472fd6bb8b9c59caacb98f61f026959b3324bb962e3ccf3e00335` |
| paper | `paper/colm2026_conference.bst` |  | `2d67552db7ed38ccfccb5957b52f95656e25c249724761d3cf5f7922ad1844c5` |
| paper | `paper/colm2026_conference.sty` |  | `55962ae80c25a50335825c85d23eb5f1cd9015aa8e77f7af32b483b646c7483e` |
| paper | `paper/extended_abstract.pdf` |  | `b6adcb1502792dff152169d3ad17043f27aa332bf32aa63b2a25b7f957ea25be` |
| paper | `paper/extended_abstract.tex` |  | `a986cefaefcf5ef3a38860ee67f9a188ad75749730d2f71c7b859bc0246088e1` |
| paper | `paper/fancyhdr.sty` |  | `b56ec4434b9f4607529a4b23dc68ad8d4b94f1f631c8cddaf7da78140d53a5ea` |
| paper | `paper/figures/audit_gpt41mini_n12_combined_explicit_heatmap.png` |  | `5b3b30fa4283a8b4522eaab4337a6df10b81333ded904d9de625b01af02fdd9c` |
| paper | `paper/figures/audit_gpt41mini_n12_combined_explicit_shifts.png` |  | `867cff66307e8bb8286ca4f7cc2896828f3aa903c0ba9d5d00d8f8e38ae43bfd` |
| paper | `paper/figures/audit_gpt41mini_n25_combined_explicit_heatmap.png` |  | `bd81b3a7e035892065424c2decb0aa3c908bfbc2863d20456921993d17af8f1b` |
| paper | `paper/figures/audit_gpt41mini_n25_combined_explicit_shifts.png` |  | `1dbb09a400ddf05d76fbbeea7b2458d04101b60c520fc1aeb4292c93259481f2` |
| paper | `paper/figures/candidate_n50_combined_explicit_heatmap.png` |  | `5ad8258f32005e3fbc7a276793764531b196dbcd42312e6c3d3d81dca5abe540` |
| paper | `paper/figures/candidate_n50_combined_explicit_shifts.png` |  | `98250c26909f9d5beabf00bd61e77dee986e76f0b08bab14bb4e325375c8377d` |
| paper | `paper/figures/pilot_n20_combined_explicit_heatmap.png` |  | `6af0dfd0635c7184e7ee8acc93bf0fd7db39b752adfda52821deaa3bce338954` |
| paper | `paper/figures/pilot_n20_combined_explicit_shifts.png` |  | `04bc270d4fea941edafce36b717950089f7bcd1651d6a73bc3268996e95cf6d3` |
| paper | `paper/figures/pilot_n20_protocol_heatmap.png` |  | `6407e562671d7fb14a40d55c53222466addef526617263e19d4035351ba27ba7` |
| paper | `paper/figures/pilot_n20_protocol_shifts.png` |  | `b7935bee3bc4420778f9e50a4c116d596f2611ee47787478ba3c26ef68d5a4d5` |
| paper | `paper/figures/pilot_protocol_heatmap.png` |  | `feb23b2c9e504a8e02e1db0fbb19317ef45ddd95828688feecdaaeeeb4119768` |
| paper | `paper/figures/pilot_protocol_shifts.png` |  | `9aee057914c088c22cd08f75e9c20f739cad1bf1492a1d97c551763b094f510a` |
| paper | `paper/figures/semantic_xlsum_n30_heatmap.png` |  | `baf35512c51f5d68511d573d3e30b845283f15779a6796c0d9e5add9f5b12cd4` |
| paper | `paper/figures/semantic_xlsum_n30_shifts.png` |  | `b1dbc1beab2abadf45eb69522855918bc2150cf9a607c953505b004d1c86fc2b` |
| paper | `paper/figures/semantic_xlsum_pilot_heatmap.png` |  | `99c5aa642d929559af657817e53a4335e6df16b4854f05debbc5813a1264aaee` |
| paper | `paper/figures/semantic_xlsum_pilot_shifts.png` |  | `772994a3afbe7a76480e403481c73e45fdde5a1249ff029cae2562bfc5e0595e` |
| paper | `paper/figures/wmt_mqm_n30_heatmap.png` |  | `8ca40c23f764bdad97cf43f46f85d13b58d96d015b44bcc5caee26fbda4dc9e4` |
| paper | `paper/figures/wmt_mqm_n30_shifts.png` |  | `aaa671766d05d073c8b58529419a23723d1c5367f70e306006ac5699100d1281` |
| paper | `paper/figures/wmt_mqm_ref_free_audit_en_de_gpt41mini_heatmap.png` |  | `8114549b9a9fa9eece0760bdc207efbf5f920a591dd9ab6c0793b473e3bbdbb2` |
| paper | `paper/figures/wmt_mqm_ref_free_audit_en_de_gpt41mini_shifts.png` |  | `a2e0b943edac8eb3da6168c48f240ee9b7b85993c7a7aaccd666b56b7a3820d6` |
| paper | `paper/figures/wmt_mqm_ref_free_audit_zh_en_gpt41mini_heatmap.png` |  | `82f546ea5e0035a16279be0c47d6a174578ff84b0f643b747dea0a12875670dc` |
| paper | `paper/figures/wmt_mqm_ref_free_audit_zh_en_gpt41mini_shifts.png` |  | `53283d0068ae5cfe67398a046b826833c739c2d81ac6e7105cb9042b19f51324` |
| paper | `paper/figures/wmt_mqm_ref_free_n30_heatmap.png` |  | `8b1c873e1895082fb8640ceb0ff6bab9d7015b6b70b19da9e922459d6325d913` |
| paper | `paper/figures/wmt_mqm_ref_free_n30_shifts.png` |  | `7381d064424a0333b7e687e6128b52eb4ec86f4d1274ed4800b12a040138e2ae` |
| paper | `paper/main.pdf` |  | `f3f43a8f81f617abf51e560d0d6a1f640b60229c9e6ebe0e372c2cdf5b5af238` |
| paper | `paper/main.tex` |  | `597cd2f6d3b88cbb6e6240bc388ad38faedd69c8109652139413f506a18a7025` |
| paper | `paper/natbib.sty` |  | `88bc70c0e48461934cab5b2accef06b74a8b3ac45ad03ccd3f2a6b7e0d6d530d` |
| paper | `paper/references.bib` |  | `13d51291f6c11bacf5c7c763b1cfa8cc652423149f6bfdd3c3f930de37425bc8` |
| paper | `paper/submission_packet.md` |  | `55762ce9cc81bc830fd42ffe8215d5ee6906b226c23235b7b5eb949838549897` |
| paper | `paper/tables/api_costs.tex` |  | `4e1dc2d26a0d271eed8cd7c44b5154106cb99cc91fda8eb832a116064e4c107f` |
| paper | `paper/tables/api_usage_inventory.tex` |  | `25a38c67f8e87a7aead4a28d3c62b4b3bd81bab27bae70a744a4dcc1bbaf5ad7` |
| paper | `paper/tables/calibration_learning_curve.tex` |  | `7a435346ba726499f95f23c709b512a07f77e0533b78ac7ee8ecefefd1fdeb9f` |
| paper | `paper/tables/calibration_summary.tex` |  | `cfddb10f071f2f7ab631ad7024e15a4802ac7c337ed86e89a784df4b5a3b7df6` |
| paper | `paper/tables/candidate_protocol_sensitivity.tex` |  | `42a9ae6a10227566f1d4492cd389e2d06bc9c05f80d8da6b613517b7c27000a8` |
| paper | `paper/tables/claim_evidence_matrix.tex` |  | `8c2d9df776011c380e48aebc0f4fbc163ff28e02bef918fb73b6d1c99085f70c` |
| paper | `paper/tables/dataset_sampling_audit.tex` |  | `be735832e418b72c18c2815b2819a99e104b15c523bb516122fd7b3ca642c512` |
| paper | `paper/tables/language_gaps.tex` |  | `c4554baad050959f2ed95069b245225a12ee2bc9846f4eaba97f56bd306efea4` |
| paper | `paper/tables/prompt_inventory.tex` |  | `770f99a1acb4f482f8a705f7886e10cbf27007dd7fa6ccfcf8bcc1356bb0d610` |
| paper | `paper/tables/protocol_instability_summary.tex` |  | `80de1c8444a4b56a827e9950ab259c9b1faaef4b0b9a622494df4dcbb3314579` |
| paper | `paper/tables/repeatability_control.tex` |  | `1dba430fba62019a48e069e961f822b95c18bcc962104b0a3563b5c3ea94f9be` |
| paper | `paper/tables/rq_contribution_matrix.tex` |  | `70d6bebd8c50aaf602b6bbe743b8676b0406edc00856750f058bc74bda0a9f67` |
| paper | `paper/tables/run_inventory.tex` |  | `6158466b6e227498704d5ebb6986b56831b559b683f3a92ff70bfc6666ebca21` |
| paper | `paper/tables/score_threshold_diagnostic.tex` |  | `8cd1dd41eedabb5fe2d5781e10493289e13b05f58e5d592134fb7a6987843917` |
| paper | `paper/tables/semantic_main_ideas.tex` |  | `ebae16ddedc0284d903510c85231700f08c717b48bd070679d20372510010342` |
| paper | `paper/tables/stronger_judge_audit.tex` |  | `194c8e6f98d38908d91b7df38a847920b2f920fcb34dad42c370bf49b85ce08b` |
| paper | `paper/tables/wmt_ref_free_stronger_audit.tex` |  | `3d49aae8572917116366ae8ee84fb1e3730446428d959e009274d7124117a803` |
| paper | `paper/tables/wmt_translation_quality.tex` |  | `ea2ec4dd59c499b8ae00eb0520dc3d0ed464770ecd761596ea5f31ebaaad1cfc` |
