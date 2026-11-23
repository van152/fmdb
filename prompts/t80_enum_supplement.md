# t80 — 枚举增补字典:解冻 t61/t75 的旧债(deepseek)

你是受指挥官委派的子代理。t61(67 条无源 held)和 t75(6 条未冻结 4CC:Ccre/cosr/Npop/Ncpi/CICF)卡在"scoped enum 缺少冻结域"上。旧证据库里现成有枚举字典,指挥官已快照入库。本任务:产一份**增补字典**(不动冻结 master.json),自动重扫这两笔旧债,零反汇编成本解锁。

## 指挥官已完成的证据治理(你只管读)

以下文件已从旧库快照入 `evidence/fm24/reports/editor_schema/` 并登记 `evidence/MANIFEST.json`(SHA-256 对照):
- `enum_extras.json`(92 KB)
- `enums.json`(308 KB)
- `database_ui.json`(32 KB)
- `EXE_ENUMS.md`(仓内既有)
- 另有 `rule_groups.json`、`entities.json`、`enum_crrp_static.json`、`enum_crrp_unicorn.json` 一并快照,可用但引用须给 MANIFEST 指针。

只读快照路径;**不修改冻结的 `evidence/fm24/reports/editor_schema/master.json`**(v10 的 schema_basis 引用它)。

## 必读

- AGENTS.md(证据分级:增补字典给的是 L2/L3 静态来源对照,引用须带 MANIFEST SHA-256)
- `scratch/t61/out/`(t61 enum_ref sweep 的 67 条无源 held 台账)
- `scratch/t75/out/xref_reverse.json`(6 条未冻结 4CC 的 gate/sink 证据:Ccre/cosr 等)
- `scratch/t73/out/slots_*.json`、`scratch/t76*/out/`(若已落盘:新扫表的 enum 候选也可用增补字典复核)

## 任务

1. **增补字典** `scripts/t80_enum_supplement.py` → `scratch/t80/out/enum_supplement.json`:
   - 合并 enum_extras.json + enums.json(+EXE_ENUMS.md 机器可读部分),键=scoped enum 名,值=值域+值名+来源文件+MANIFEST SHA-256
   - 与 master.json `enums`(304 个)求差集/交集:master 已有的不覆盖,只补缺;每条带 `provenance`
2. **自动重扫 t61**:67 条无源 held 逐条查增补字典,命中且域自洽 → 候选升级表(grade 建议 L3,注明"enum_ref 现已 scoped,静态槽不变");仍无源 → 保持 held,给"字典未含"标记
3. **自动重扫 t75 六条未冻结 4CC**:Ccre/cosr/Npop/Ncpi/CICF(+xref_reverse.json 里同类的)逐条:4CC 在 field_codes/增补字典里的 locations、值域 vs 增补枚举域,给裁决候选
4. **交叉复核**:t73/t76 的 enum 类槽(如 continent DBvw 的空名枚举——master 数据缺陷,增补字典若能补上值名,单独列一节)
5. `verify.py`:抽样 20 条增补条目反查源文件原字节/键名对拍
6. `--help`/`--selftest`;退出码 0/1/2;负结果原样保留

## 避坑纪律

1. 只写 `scratch/t80/` 和 `scripts/t80_*.py`;不碰 reports/、LEDGER、evidence/(快照是指挥官做的,你只读)。
2. 增补字典不覆盖 master.json 已有条目;冲突条目单列 `conflicts` 不裁决。
3. 文件写单次 ≤120 行(t73 教训)。

## 交付 scratch/t80/out/

`enum_supplement.json`、`rescan_t61.json`、`rescan_t75.json`、`REPORT.md`、`DONE.md`(首行 `DONE type=t80 status=complete`)、`verify.py`。

Python `py -V:3.12 -I -B`;不需要 FM24_DB_DIR(不读 .dat)。
