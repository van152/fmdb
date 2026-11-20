# t70 — public club/nation schema v9→v10

- v9 snapshot: JSON SHA-256 `703df30ea34fbee3b555ccf4233d4fe012bcb614435381efb68a3224e5ae64ee`; Markdown SHA-256 `ded0da91af36098b2648af769ed258fd39d903e86f0494b5b2f8fab3a98c5757`. v10 Markdown preserves the full v9 bytes as prefix.
- Additive sections: `club_main_row_fields_r2`, `comp_main_row_fields_r2`, `nation_main_row_fields_r2`, `comp_collections`, `edfx_edsc_dispatch`, `tail_ledger`.
- Club round 2: 8 new L3; coverage cumulative club main-row L3=21; 41 held and 350 unmapped in this round. R1 and R2 counts are separately labeled in coverage.
- COMP round 2: 196 reviewed, 0 new L3; baseline 49/10/196 and 818 inversions unchanged. Nation round 2: 327 reviewed, 9 held, 318 unmapped, 0 new L3.
- Collections: 7 physical grammars and 4 reference lanes at L3; corrected nonempty row counts 315/366/121/51. EDsc dispatch closed, EDfx upstream open. Tail ledger 18/18, unresolved club skips 0.
- All accepted task JSON records plus REPORT/DONE documents (and t69 SUMMARY) are embedded; source SHA-256 and byte counts are pinned.
- Protected sections and old provenance/task records are value-identical to v9. Ledger claim guards span E84–E109. L4=0.
- Builder/verifier `--help`, `--selftest`, `--check`, exit-code 1/2 probes passed; t01 anchors 7/7. Logs are in `scratch/t70/out/spot_*.log`.
- v10 JSON SHA-256 `7c35160827875c5ce295701950747482c61dd0c9862658459e6a3765e0882515` (29511808 bytes); Markdown SHA-256 `b9ba0bb3efc2d43baac697bdec76d548243ef9c5da094377eacfc46799b5c051` (77028 bytes).
