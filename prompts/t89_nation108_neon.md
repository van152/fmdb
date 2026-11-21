# t89 — [NATION+0x108] 静态读链追源 + table_9(NATION_T9)文法定型(neon 攻坚 #4)

你是受指挥官委派的攻坚车道(neon xhigh,agy CLI)。E127 已把 t85 的遗留问题升级:table_9(NATION_T9,251 行,13B 头+变长体+12B identity 尾+9B 脚)严格闭包成立,但其**条目文法 held_no_item_grammar**,且 [NATION+0x108] 集合是否就是 table_9 的 wire 家**未证**。t83(E126)已证 DATABASE 构造器把 t9 注册在 `db+0x60`(紧邻 nation `db+0x28`)。本任务用静态链一锤定音。

## 已冻结地基(直接用,不重做)

- `scratch/t85/out2/profile_nation.json`:table_9 结构+行 0 body_head_hex(首反例)+逐偏移 lane 域;`wire_candidates.json`:双档闭包+t51 冻结游标对拍;`collection_fields.json`:t75 的 getter_proven_but_no_main_row_sink 清单(nhrl 实例:gate 17048862 "compares bounds at [this+0x108]+0x4a0/0x4a8")
- `scratch/t83/out/xref_*.json`:五表工厂/vtable/RTTI/`DATABASE` 构造器 0xf026c0 的 16 个 db+offset 绑定(含 **+0x60: t9 (NATION_T9, 251)**、+0x28: t10)
- 静态:只读 `D:/tmp2b/fm24/input/editor.exe`(SHA-256 `b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4`);t79/t83 的 getter+setter 双链范式
- schema:`evidence/fm24/reports/editor_schema/master.json`(程序化查)+ `scratch/t75/out/xref_reverse.json` 的 nation_escalations 与 slots

## 任务

1. **NATION+0x108 读链追源**:从 t75 的 gate(如 17048862)向上回溯——[NATION+0x108] 的类型、它的 reader/write 路径、它读的是哪个 DATABASE 表(假设 table_9 @ db+0x60):给 VA/fo/指令字节三件套;若证实,即"集合字段 wire 家=table_9"L3 裁决
2. **table_9 条目文法静态定型**:从 t9 的 read handler(t83 的工厂/RTTI 方法可复用:找 NATION_T9 类的 vtable slot 19/20/21)逐字节给出条目网格,解释 body 46..449B 变长与 92 种长度;与 t85 行 0 反例(00 ff ff ff ff 01 01 01 00 00 00 0a 00 00 00 00 00 01 5c 05 00 00 00 00)对账
3. **held 集合字段回填**:nhrl 等 getter_proven_but_no_main_row_sink 字段逐个对到 table_9 条目内偏移(或证伪);过闸 L2/L3,不过闸 held+首反例
4. **双档对拍**:table_9 client 31,956B / server 307,555B 差额(server body0=1086 vs client 46)的静态解释
5. 独立 `verify.py`(不 import builder/fm24_dump)+ builder `scripts/t89_*.py`;`--help`/`--selftest`;退出码 0/1/2;t01 anchors 7/7

## 边界

- 只做 [NATION+0x108]/table_9 及其直接关联字段;不碰 club/comp 主行、t45(见 t88-fix1 车道)、五表(t83 已收)
- **防冲突**:只写 `scratch/t89/` 和 `scripts/t89_*.py`
- 不启动游戏/编辑器/IDA,不联网,不读写 Z:;数据侧验证向量化

## 交付 scratch/t89/out/

`xref_nation108.json`(读链)、`table9_grammar.json`(条目文法+行 0 对账)、`field_map.json`(held 回填增量)、`domain_stats.json`、`verify.py`、`REPORT.md`、`DONE.md`(首行 `DONE type=t89 status=complete`)。

Python `py -V:3.12 -I -B`;`FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data`。
