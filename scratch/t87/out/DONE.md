DONE type=t87 status=complete

# t87 — Schema v11.1 增量:E121(t82)补录

- schema:`reports/club_nation_subtable_schema.json` **v11 → v11.1**(29,893,769 B,SHA-256 `f811a216a8d1f72ea98dd86995924a3f55e952bc52b2b23466005dd7a7d4efed`)
- markdown:`reports/club_nation_subtable_schema.md` 89,265 B,SHA-256 `a95a150edee2608ab36aa701d63e4bc045f9208693bb83c95517822c6182db03`(v11 字节为严格前缀 + t87 附录)
- 新根节 `club_extra3_l3_e121`:35 新 L3 / 39 held / 131 负证 / 117 项 `CBW*`·`CBD*` → `server_db/table_45.dat` 正名
- coverage:`club_main_row_L3` 43 → **78**(+35,E121);L4 = 0
- 只增不改:v11 的 32 个非 mutable 根节逐字节不变(摘要护栏 + 原文切片双证)

## 三档

| 档位 | 结果 |
|---|---|
| `scripts/t87_v11_patch.py --selftest` | 9/9,exit 0 |
| `scripts/t87_v11_patch.py --build` | 27/27,exit 0 |
| `scripts/t87_v11_patch.py --verify` | **59/59**,exit 0 |

回归:`scripts/t01_anchors.py` 7/7;`scripts/baseline_coverage.py --check` CHECK OK。

## 交付清单

| 文件 | 说明 |
|---|---|
| `scripts/t87_v11_patch.py` | 补丁器:`--build/--verify/--selftest`,退出码 0/1/2 |
| `reports/club_nation_subtable_schema.json` | v11.1 主 schema |
| `reports/club_nation_subtable_schema.md` | v11.1 主 schema(附录) |
| `scratch/t87/out/REPORT.md` | 任务报告 |
| `scratch/t87/out/verify_log.md` | 校验日志(哈希、计数、失败白名单) |
| `scratch/t87/out/v11_section_digests.json` | 32 节摘要护栏(机读) |
| `scratch/t87/out/DONE.md` | 本文件 |
| `scratch/t87/out/{verify,selftest,anchors,baseline}_raw.txt` | 三档与回归原始输出 |
| `README.md` / `docs/REPO_STATUS.md` | 各追加 v11.1 状态行 |

## 遗留(未在本任务范围)

- `table_45` 的 117 项 `STARTING_RECORD` 字段仍无 wire 槽位扫描。
- `reports/xml_denominator_coverage.json` 的 E116 分桶未重发(117 项 carve-out 仅注记)。
- `scripts/t77_schema_v11.py --verify` 现 59/63,4 项失败是把已发布文件钉在 v11 的终态断言,已由 t87 白名单断言显式记录。
