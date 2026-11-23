# t144 Wave 13+14 Regression Audit

Python: 3.12  |  timeout: 120s per script  |  cwd: `D:\tmp2b\fm24-db`

## 1. Regression checks (Wave 13+14 scripts)

| # | script | args | exit_code | elapsed_s | pass | timeout | stdout last 3 lines |
|---|--------|------|-----------|-----------|------|---------|---------------------|
| 1 | scripts/t01_anchors.py | - | 0 | 0.649 | YES | no | PASS A7_ledger_erratum_applied  ['PLgn', 'cnam', 'csnm', 'c3ln', 'cnti', 'ccti', |
| 2 | scripts/t97_extract_4cc_mem.py | --selftest | 0 | 0.4472 | YES | no | PASS CLUB get_prop yields >100 branches :: 513 / PASS CLUB dispatch alias v4 det |
| 3 | scripts/t98_table45_closure.py | --selftest | 0 | 6.355 | YES | no |   D:\tmp2b\fm24-db\scratch\t98\out\REPORT.md /   D:\tmp2b\fm24-db\scratch\t98\ou |
| 4 | scripts/t106_special_members.py | --selftest | 0 | 0.2907 | YES | no |   PASS  sha256 stable /   PASS  all members registered / selftest: 37/37 pass |
| 5 | scripts/t108_extract_4cc_v2.py | --selftest | 0 | 0.3723 | YES | no | PASS 18 accepted L3 items checked :: 18 / PASS triage row Cnti -> 0xd8 :: 0xd8 / |
| 6 | scripts/t109_big3_l3_join.py | --selftest | 0 | 1.6518 | YES | no |   net coverage          : 379/673 = 56.3% /   accepted-L3 crosscheck: {'agree_ex |
| 7 | scripts/t110_master_l3_schema.py | --selftest | 0 | 1.3208 | YES | no | selftest PASS |
| 8 | scripts/t112_fm24_reader.py | --selftest | 0 | 0.7951 | YES | no | [PASS] live client/41 closed: None / [PASS] live server/45 500 rows: None / ---  |
| 9 | scripts/t115_basic_people_full.py | --selftest | 1 | 0.3291 | NO | no |  |
| 10 | scripts/t119_unicorn_last5.py | --selftest | 0 | 24.368 | YES | no |   server/t72 (STARTING_PAST_TRADE): status=sample_ok rows_ok=10/10 (hdr=138) clo |
| 11 | scripts/t120_people_unicorn.py | --selftest | 0 | 1.1086 | YES | no | t120 selftest PASS: rows_ok=1210 stats={'2': {'class': 'PLAYER', 'rows_ok': 17,  |
| 12 | scripts/t121_master_79of79.py | --selftest | 0 | 0.9338 | YES | no | selftest PASS — 79/79, joined 56/67, L3=1104 |
| 13 | scripts/t122_people_l3_schema.py | --selftest | 0 | 0.3316 | YES | no | t122 selftest: PASS |
| 14 | scripts/t123_basic_people_l3.py | --selftest | 0 | 12.5881 | YES | no | byte_maps=83/83/83/34/22 / anchors=3 names=Harry Kane,Cristiano Ronaldo,Lionel M |
| 15 | scripts/t125_big3_gap_closure.py | --selftest | 0 | 7.0749 | YES | no | t125 --selftest PASS / gross 512/1034 (49.5%); net 512/672 (76.2%); gaps 294 ->  |
| 16 | scripts/t126_player_attributes_l3.py | --selftest | 0 | 1.4078 | YES | no | t126 selftest PASS: 54/54 PDxx GET==SET, 69B mapped, 5-class L3=374, cards=['Mil |
| 17 | scripts/t133_fm24_reader_v2.py | --selftest | 0 | 9.3674 | YES | no | [PASS] server/72 row0 trace {'reads': 30, 'canonical_fields': 17, 'trace_end': 9 |
| 18 | scripts/t135_star_player_cards.py | --selftest | 0 | 4.8737 | YES | no | t135 selftest PASS (4.39s): Harry Kane: OK (CA/PA 184/185) \| Lionel Messi: OK ( |

- scripts run: 18
- passed: 17
- failed: 1

## 2. Protected-path clean check

- paths: reports/, scratch/t01/LEDGER.json
- clean: YES

## 3. Completed task catalog (scratch/t95..t143/out/DONE.md)

| task | has DONE.md | first line | deliverables |
|------|-------------|------------|--------------|
| t95 | no | - | 0 |
| t96 | YES | DONE type=t96 | 4 |
| t97 | YES | DONE type=t97 | 5 |
| t98 | YES | # t98 done | 4 |
| t99 | no | - | 0 |
| t100 | no | - | 0 |
| t101 | no | - | 1 |
| t102 | no | - | 0 |
| t103 | no | - | 0 |
| t104 | no | - | 0 |
| t105 | YES | DONE type=t105 | 5 |
| t106 | YES | DONE type=t106 | 3 |
| t107 | no | - | 1 |
| t108 | YES | DONE type=t108b | 5 |
| t109 | YES | DONE type=t109c | 5 |
| t110 | YES | DONE type=t110 | 4 |
| t111 | YES | DONE type=t111 | 4 |
| t112 | YES | DONE type=t112 | 3 |
| t113 | YES | # t113 delivery status: PARTIAL | 5 |
| t114 | YES | DONE type=t114 | 4 |
| t115 | YES | DONE type=t115 | 3 |
| t116 | YES | DONE type=t116 | 4 |
| t117 | YES | # DONE type=t117 | 5 |
| t118 | YES | DONE type=t118 | 5 |
| t119 | YES | DONE type=t119 | 3 |
| t120 | YES | DONE type=t120 | 4 |
| t121 | YES | DONE type=t121 | 4 |
| t122 | YES | DONE type=t122 | 3 |
| t123 | YES | DONE type=t123 | 3 |
| t124 | no | - | 1 |
| t125 | YES | DONE type=t125 | 5 |
| t126 | YES | DONE type=t126 | 7 |
| t127 | no | - | 3 |
| t128 | no | - | 0 |
| t129 | no | - | 0 |
| t130 | no | - | 0 |
| t131 | no | - | 0 |
| t132 | no | - | 1 |
| t133 | YES | DONE type=t133 | 4 |
| t134 | dir missing | - | - |
| t135 | YES | DONE type=t135 | 5 |
| t136 | no | - | 6 |
| t137 | no | - | 0 |
| t138 | no | - | 1 |
| t139 | dir missing | - | - |
| t140 | dir missing | - | - |
| t141 | dir missing | - | - |
| t142 | dir missing | - | - |
| t143 | dir missing | - | - |

- tasks with DONE.md: 25 / 49

## 4. SHA-256 deliverable manifest

See `regression_matrix.json` for per-file SHA-256 + byte size of every `.json`/`.md` under each `scratch/t*/out/` (t95..t143). Oversized `.bin`/`.pkl`/`.sqlite` (> 50 MB) are skipped.
