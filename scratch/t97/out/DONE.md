DONE type=t97

# t97 — 全量 67 表 Hex-Rays 4CC ↔ 内存偏移抽取 + XML 1,034 分母分诊

status: complete
outputs: scratch/t97/out

## 摘要数字

- tables_covered: 67/67
- unique_fourcc: 2219
- table_fourcc_pairs: 6219
- pairs_with_byte_offset: 1808
- access_kind: direct_field=1255, bitfield=125, subobj_deref=89, helper_computed=2525, delegated_or_empty=2225
- missing_subcalls: 135

## 1,034 分母分诊

- denominator: 1034
- unresolved_wire_slot (160): direct_mem_off=41, helper_computed=85, absent_everywhere=9
- held (59): direct_mem_off=24, helper_computed=20, absent_everywhere=1
- no_wire_evidence (564): direct_mem_off=46, helper_computed=217, absent_everywhere=267
- total_direct_mem_off_hits: 152
- total_absent_everywhere: 320

## 静态 read 交叉

- fourccs_with_offset: 1808
- hit_read_server: 724
- hit_read_client: 250
- hit_any_read: 802

## 回归验证（对已验收 L3）

- checked: 18
- exact: 12
- within_slot: 3
- no_static_hit: 2
- mismatch: 1

## 验收

- `py -V:3.12 -I -B scripts/t97_extract_4cc_mem.py --selftest` → exit 0 (25 assertions,
  incl. STARTING_RECORD `1415446a0.c`: 1869899892('otht')->0x28, 1918989417('rati')->0x5a, 1920099681('rrea')->0x5c)
- 67/67 tables covered; all JSON deliverables parse cleanly
- `reports/` and `LEDGER.json` untouched (read-only inputs)

## 交付物

| 文件 | 字节 | sha256[:16] |
|---|---|---|
| `fourcc_mem_map.json` | 7505256 | `b9a7dfc7148bb848` |
| `xml_triage.json` | 752031 | `3ac817cd5bc6d682` |
| `static_read_join.json` | 2244123 | `b0acc949316fb53d` |
| `REPORT.md` | 17342 | `8f451ec91a5d5262` |
| `DONE.md` | 1661 | `2b4290d739d3bd0e` |

