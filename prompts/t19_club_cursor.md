# t19 任务书:club/nation cursor_layout 重建 —— E20 手法向 tier-1 全量复刻

先读 [AGENTS.md](../AGENTS.md)。t18 已证明:**行偏移 = 逐字段 cursor 步骤(含显式版本字节与条件块)累加**,comp 46 步全对齐、stride 封口。现在把这个手法复刻到两个 tier-1 实体上。

## 方法模板(已验证,直接复刻)

- `scratch/t01/inbox/t01f/output.json` —— E20 comp 的 `cursor_layout`(46 个序列化步骤,含版本字节与条件块):这是"正确粒度"的样板。t16 的稀疏 walk(9 事件)不够——**条件分支漏掉的字段必须从 reader_widths/stride 反推补齐**。
- 校验三件套:行侧累加 ↔ 基线字段偏移一致、stride 封口(COVERAGE.json)、reader 槽序互验(reader_widths.json)。

## club(主目标,433+ 字段)

- 现状:t18 台账 14/672 命名;已知锚 `Cccn@row+8`(t04,对象成员 +0xf0);club 行文法是 **mixed/club_block**(`scripts/fm24_dump.py` OVERRIDE:client t3 "mixed 双 RTTI + 5B block",边界工件 `scratch/t02/inbox/club_v2/output.json`)。
- 任务:重建 club 序列化器的 cursor_layout——**先把块结构(几个分支、各分支字段序)画出来**,再逐块累加;与 schema_inventory 的 club 4CC 字段集对齐命名,与 codes_full.json 的 club object_off 实例互验;与 `scratch/t15d/out/clubwords.npy`、`fk_hits.json`(t15d 现场数据)交叉。
- 交付每字段 `{"field","row_offset","width","grade":"L3_row_instruction|L3_inherited|L2_data|unnamed","evidence"}`。

## nation(次目标,441 字段)

- 现状:t01g(E21)已建 nation 类全链 L3 + 7 个前缀字段行偏移(工件 `scratch/t01/inbox/t01g/`,含计数循环文法);t18 台账 nation 0/441。
- 任务:用 t01g 的全链做 cursor 重建基线,把 E21 的 7 个字段扩展到 schema 全集(对齐方式同 club);nation 是计数循环文法,**循环体步长与循环次数封口是硬校验**。

## 纪律

- 只写 `scratch/t19/out/` + 新增 `scripts/t19_*.py`;其他只读;不联网;FM24_DB_DIR 已设(本地数据)。
- 输出预算:单次写盘 ≤400 行;fields_*.json 超 50KB 分片。
- **结构优先于命名**:块结构没画清就别硬填字段名;unnamed 合法。
- 55 分钟做不完分批落盘 partial;status 用 `complete_cursor_<限定词>` / `partial_<限定词>`。

## 交付(scratch/t19/out/)

1. `cursor_club.json` / `cursor_nation.json` —— 块结构 + 步骤序列(同 t01f 的 cursor_layout 格式)
2. `fields_club.json` / `fields_nation.json` —— 行坐标字段台账(分片允许)
3. `verify.py` —— club/nation 的 stride 封口 + 基线字段比对 + 抽样指令复算;--help/--selftest
4. `REPORT.md` —— 块结构图、命名率变化、证伪记录
