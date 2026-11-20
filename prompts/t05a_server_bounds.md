# t05a — server_db 变长表行边界收官(独立复算 + 补齐 18 张未解表)

## 角色与硬约束

你是数据逆向工程师。工作区 `<WORKSPACE>`,Python 固定 `py -V:3.12 -I -B`(必须带 `-I -B`)。

**只读边界(不可违反)**:
- 游戏数据 `<GAME_DATA>\data\database\db\2430\2430_fm\server_db.dat` **只读**。
- 上游工作区 `<OLD_REPO>\` **全目录只读**(它的 AGENTS.md 禁止写入;你只能读它的 reports 和 scripts)。
- 你的**唯一可写目录**是本任务的 OUTDIR。不要写 `scratch/t01`、不要改 `scratch/t02` 的任何既有文件。

**纪律**:
- 不用 `--selftest` 之外的花哨东西;每个断言必须能被 `py -V:3.12 -I -B verify.py --selftest` 复现。
- **closure 必须精确算术相等**,不允许"约等于""基本吻合"。变长表必须给出最后一行结束位置 + footer 长度 == payload 长度的等式。
- 允许并鼓励**诚实负结果**:某张表解不出就写 `status: partial_negative` + 明确卡点,不要编造 stride。
- **边做边落盘**:第一步就先把 `boundaries.json` 骨架写出来(所有表 status=in_progress),之后每解一张就更新一次。这样中途被掐断也有产出。

## 目标

`server_db.dat` 目录里 **59 张数值主表**。上游普查(`<OLD_REPO>\reports\dbdat_decode\server_tables_census.json`)给出:37 张 `fixed_stride`、18 张 `variable_or_nonstandard`、少量 empty/auxiliary。

你的任务:
1. **对全部 59 张数值表独立复算闭包**(不信任上游结论,自己解压自己算):定长表验 `14 + count*stride + 8 == payload_len`;变长表必须真正走完整表。
2. **攻下 18 张 `variable_or_nonstandard`**,恢复其行边界文法。
3. 给出每张表的身份槽(identity slot)位置与类型。

## 输入

| 用途 | 路径 |
|---|---|
| archive 读取/解压 | `<OLD_REPO>\scripts\modding_read_dbdat.py`(用 `runpy.run_path` 加载;函数 `list_tables()`、`_resolve_table(tid, ents, 'server_db.dat')`、`_stream_decompress(buf, maxlen)`) |
| 容器格式说明 | `<OLD_REPO>\reports\CONTAINER_SPEC.md`、`<OLD_REPO>\reports\DBDAT_FORMAT.md` |
| 上游普查(仅作假设) | `<OLD_REPO>\reports\dbdat_decode\server_tables_census.json`(每条含 `table_id / record_count_header / payload_size / payload_sha256 / row_model / row_boundary`) |
| 变长行范例(已解) | `<WORKSPACE>\scratch\t02\inbox\nati\OUTBOX\framework.json`(4 段计数循环 `row_len=50+5A+28B+28C+12D`) |
| 变长行走范例(已解) | `<WORKSPACE>\scratch\t02\inbox\club_v2\solve.py`(84,259 行全封口的 walker,注意 `load_raw()`) |

**已知陷阱(务必先解决)**:
`_resolve_table()` 返回的 `offset` **不是 zstd 帧起点**。正确做法二选一:
- (a) 从 `offset` 起向后扫描 zstd magic `28 b5 2f fd`(限定前 64 字节内),从 magic 起解压;
- (b) 直接读 `CONTAINER_SPEC.md`/`DBDAT_FORMAT.md` 里成员头长度定义,精确计算帧起点。
不管用哪种,在 verify.py 里断言解压后 `payload_size` 与上游 `payload_size` 相等、`sha256` 相等——这是你的解压正确性护栏。

**payload 头格式(已验证)**:前 8 字节 `03 01 74 61 64 2e f1 0d`,+8 是 2 字节(通常 `0000`),+10 是 u32 record_count,行区从 **+14** 开始,末尾 **8 字节 footer**。

## 方法建议

1. 先写 `common.py`:`load_payload(archive, table_id) -> bytes`(带上面两个护栏断言)。
2. 定长表:解 `count` 后对 `payload_len-22` 做整除,并验证身份槽(找 `rdui == row_index` 的 u32 偏移 + `重复 u32` 的 8 字节槽)。**只有当身份槽也成立时**才标 `verified: true`;只整除不算。
3. 变长表:从 payload 尾部反推。多数变长表最后一行的尾部结构固定(如 `duni_u32 + duni_u32 + 00`)。用"尾部锚点 + count 递减"的倒序走查往往比正序容易:
   - 先在 payload 里扫所有 `重复 u32 + 00` 候选尾锚,取其中 **严格递增/递减的长序列**(长度应接近 count);
   - 用相邻锚点差值反推行长分布,再验证"每行起始处结构一致性";
   - 若行长由计数段驱动(像 nati),用行长 = 固定前缀 + Σ段计数×项宽 反解每段的计数字段偏移。
4. 对每张表同时尝试正序与倒序,取能精确封口的那一种。

## 交付

写进 OUTDIR:

1. `boundaries.json` — 顶层:
```json
{"status": "complete_all|complete_partial|partial_negative",
 "archive": "...server_db.dat",
 "payload_sha256_ok": true,
 "tables": [
   {"table_id": 19, "count": 28, "payload_len": 1310,
    "model": "fixed|variable|empty|unresolved",
    "stride": 46, "closure": "14+28*46+8 == 1310",
    "identity": {"offset": 34, "kind": "rdui|repeated_u32|none", "verified_rows": "28/28"},
    "boundary_grammar": "仅 variable 需要: 分行描述",
    "verified": true, "evidence": "..."}
 ]}
```
2. `verify.py` — 必须支持 `--selftest`(纯离线自检)与默认模式(重新从 archive 复算全部 59 表并打印 PASS/FAIL)。**不得复用 boundaries.json 里的数字来"验证"自己**——必须从原始字节重算。
3. `REPORT.md` — 表格式总结 + 未解表的具体卡点(哪一步不成立)+ 你推翻/修正的上游结论。
4. `common.py` 若单独成文件也一起交付。

## 验收标准

- `verify.py --selftest` 全 true。
- 59 张数值表中,**≥52 张** `verified: true` 且 closure 精确;其中原先 18 张 `variable_or_nonstandard` **至少攻下 10 张**。
- 未解表必须有明确卡点说明,不得用 `stride` 猜测充数。
- 所有解压后 payload 的 sha256 与上游普查一致(若不一致,如实报告差异)。

## 完成后

打印交付清单(文件名 + 字节数 + 关键数字:verified 表数 / 攻下的变长表编号 / 未解表编号)。
