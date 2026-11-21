# t87 — Schema v11.1 增量：E121(t82)补录

## 0. 结论

E121(t82)已 **additive-only** 并入公共 schema:**v11 → v11.1**。三档全过 —— `--selftest` 9/9、`--build` 27/27、`--verify` **59/59**;`t01 anchors` 7/7;`baseline_coverage --check` OK;L4 = 0。

- 根键 36 → **37**,新增 `club_extra3_l3_e121`。
- `schema_version` `11` → `"11.1"`;`generated_by` `t77` → `t87`。
- 既有 32 个非 mutable 根节 **逐字节不变**(原文切片比对 + 摘要护栏双证)。
- 体量:JSON 29,884,088 → **29,893,769 B**(+9,681);MD 87,373 → **89,265 B**(+1,892,附录)。

## 1. 新增节 `club_extra3_l3_e121`

| 项 | 值 |
|---|---|
| 验收条目 | `E121` / `acceptance` / `L3` / 2026-11-21 |
| 源任务 | t82(`table_extra_3` 剩余载荷命名) |
| 指针 | `scratch/t82/out/field_map.json` SHA-256 `2a31c025…`,`260,540 B` |
| 新 L3 | **35**(31 标量 + 4 列表/多态)|
| held | **39**(仅计数 + 4CC,首反例留在 t82 产物)|
| 负证 | **131** = 117(`table_45` 记录族)+ 14(其它非 extra_3)|
| 排除 | t71 已转正 24 项(不重复计入)|

**35 个 4CC 按 E121 claim 分组**(组内计数来自 t82 的 `grade`/`wire_scope`,非人工抄录):

| 组 | 计数 | 代码 |
|---|---:|---|
| server-only 标量 | 6 | `Ctlv Cmle Cyim Cyfb Cytv Crcb` |
| 选举子对象 | 5 | `Cetl Cmtm Cect Cemn Cemx` |
| 球迷画像 | 6 | `Csly Csps Cspt Csaf Cste Cspe` |
| UEFA 系数环 | 10 | `Cuf1..Cuf9 Cf10` |
| server-only i32 | 3 | `Catd Cmna Cmxa` |
| 串/列表尾 | 5 | `TCht Cbbl Csoc pcpt CPsL` |

## 2. `CBW*`/`CBD*` → `server_db/table_45.dat` 正名

`club.xml[211..327]` 全部 **117** 项记录族字段(含 10 个 `CB*` 代码:`CBWa/CBWc/CBWd/CBWf/CBWo`、`CBDa/CBDc/CBDd/CBDf/CBDo`)的 wire 家在 **`server_db/table_45.dat`(`DATABASE_TABLE<STARTING_RECORD>`,type `0x2d`=45,84,477 记录)**,不在 `table_extra_3.dat`:

- `TC_RECORD_GET @ 0x3ebad50` 完全不访问 `CLUB+0x100` / `CLUB+0xb0`;写路径 `TC_RECORD_SET @ 0x3ebaf50`。
- 表号自证:`mov edx, 0x2d` @ `0xf06c70..0xf06c84` + RTTI `.?AV?$DATABASE_TABLE@VSTARTING_RECORD@db@@`。
- 上述静态见证以字符串形式在 `--verify` 中**对 `scratch/t82/out/REPORT.md` 实时抽查**(5/5 命中),不复制大对象。

**分母后果**:E116 台账中 club 的 239 个 `unresolved_wire_slot` occurrence 里,这 117 项被 re-route 出 extra_3 分母。`reports/xml_denominator_coverage.json` **本任务不改**;117 项 carve-out 以 `coverage.club_denominator_note_E121` 注记,桶重发为后续任务。

## 3. coverage 增量

| 键 | v11 | v11.1 |
|---|---:|---:|
| `club_main_row_L3` | 43 | **78** |
| `club_main_row_L3_prior_v11` | — | 43(新增) |
| `club_main_row_L3_delta_E121` | — | 35(新增) |
| `club_main_row_L3_note_E121` | — | 43+35=78 口径说明(新增) |
| `club_denominator_note_E121` | — | 117/239 re-route 说明(新增) |
| `xml_denominator_pointer_note_E121` | — | 指针仍带 E116 数字(新增) |
| `L4` | 0 | 0 |

coverage 的键**只追加**,既有键中只有 `club_main_row_L3` 数值改变(`--build` 显式断言 `{removed: [], changed: ['club_main_row_L3']}`)。

## 4. 只增不改的证据

1. **摘要护栏**:`scratch/t87/out/v11_section_digests.json` 记录 v11 的 32 个非 mutable 根节规范 JSON SHA-256;`--verify` 逐节重算,32/32 一致。
2. **原始字节切片**:构建前用与 `t77_common.json_bytes` 相同参数重排 v11 基线可**逐字节复现**发布文件,因此在同一坐标系下按节切原文比较,32 节切片完全一致,漂移列表为空。
3. **显式差分断言**:`adder_guard` 在 build 中拒绝任何非 mutable 根节被删/被改。
4. **二次构建保护**:`--build` 在已打补丁的文件上直接失败(退出码 1),不会叠加。

## 5. 已知遗留(记录,不在本任务范围)

- **t77 验证器现为 59/63**:4 个失败均为把已发布文件钉在 v11 的终态断言(`schema_version is 11`、`generated_by is t77`、root keys、`club_main_row_L3 = 43`),已被 v11.1 超集取代。t87 把这 4 项做成显式白名单断言,任何**其它** t77 回归都会让 t87 `--verify` 失败。
- `table_45` 的 117 项 `STARTING_RECORD` 字段仍**无 wire 槽位扫描**(本任务只做正名与分母归位),建议后续 lane 接。
- `xml_denominator_coverage.json` 的 E116 分桶未重发。
- t82 的 39 held 与 131 负证原文保留在 `scratch/t82/out/field_map.json`,未复制入 schema。

## 6. 触达面(严格)

| 类型 | 路径 |
|---|---|
| 写 | `scripts/t87_v11_patch.py` |
| 写 | `reports/club_nation_subtable_schema.json`、`reports/club_nation_subtable_schema.md` |
| 写 | `scratch/t87/out/{verify_log.md,REPORT.md,DONE.md,v11_section_digests.json,*_raw.txt}` |
| 写 | `README.md`、`docs/REPO_STATUS.md`(各只追加 v11.1 状态行/表行) |
| 只读 | `scratch/t01/LEDGER.json`、`scratch/t82/out/*`、`scratch/t77/out/*`、`scratch/data/t87/`(未入库基线快照,构建期临时) |
| 未碰 | `reports/xml_denominator_coverage.json`、`reports/other_tables_schema.json`、`scratch/t01/LEDGER.json`、其余 reports/docs |

## 7. 复现

```powershell
py -V:3.12 -I -B scripts/t87_v11_patch.py --selftest   # 9/9
py -V:3.12 -I -B scripts/t87_v11_patch.py --verify      # 59/59(只读,可重复)
py -V:3.12 -I -B scripts/t01_anchors.py                 # 7/7
py -V:3.12 -I -B scripts/baseline_coverage.py --check   # CHECK OK
```

`--build` 是一次性的(已打补丁后拒绝重跑);需要从 v11 重建时,先把 v11 基线还原到 `reports/club_nation_subtable_schema.{json,md}` 再 `--build`。
