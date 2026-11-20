# t71 — CLUB+0x100 跨对象读链打通 + 22 cnst 契约字段批量转正 L3(sol)

你是受指挥官委派的子代理,承担本轮最硬的一环。t63(E106)把 club 主行 399 个 unmapped 复查后,留下 **22 个 `cnst` 契约状态字段 held**:静态侧已证明每个 4CC 的精确 gate→helper→逐 byte `movsx` 位置,字节落在 **`*(CLUB+0x100)` 所指的另一个对象**内(`+0xe0..0xe6` 7 个、`+0xe7..0xf5` 15 个),但**缺 wire 游标**——即哪个归档成员、什么行文法、哪些字节位喂进这个对象,没有闭合。本任务打通这条跨对象读链,把 22 个字段批量转正 L3。

## 已冻结的静态证据(必须复用,不重推)

- **22 个 4CC 与对象内字节**(t63 held,`scratch/t63/out/field_map_r2.json` 每条含 gate/helper/wire 证据):
  - A 块 7 个(`+0xe0..0xe6`):`Ccsp Ccsk Ccsf Ccsr Ccsb Ccsh Ccsy`
  - B 块 15 个(`+0xe7..0xf5`):`Ccjm Ccja Ccjc Ccji Ccjg Ccpc Ccjy Ccjs Ccjp Ccjd Ccjt Ccjh Ccda Ccss Ccdr`
- **两条 getter 链**(t63 REPORT):玩家态 `0xe89be8 → 0xe89bea → 0xe89c13 → 0x151d9b0`;职员态 `0xe89fd3 bit-test → 0xe89fdc → 0xe8a005 → 0x151e500`;首断点 `0xe89bef` / `0xe89fe1` 都是加载额外对象指针(即 CLUB+0x100 的 qword load)。
- **同对象的旁证**(t57/t63 held):`Cebd` 走 `+0x100 → extra+0x78`(election 对象);`Cyfn` getter `0xe8e6a9/e8e6b1` 是 `CLUB+0x100 → extra+0xd8`。
- 静态来源:只读 `D:/tmp2b/fm24/input/editor.exe`,SHA-256 `b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4`;下文 file offset 不得混淆 VA。CLUB slot 19 `0xe5a7a0`(extent `0xe5a7a0..0xe5bfca`)、slot 2 `0xe89a00`。
- 对照范本:t64 已在 comp 侧转正过 22 个同名范式的 cnst(Pcsp/Pcsk/...),但其对象是 `COMP+0x198` 本地——**club 是跨对象,不得照抄 comp 的 wire 顺序或偏移**。

## 任务

1. **证明 CLUB+0x100 的 wire 来源**:从 club 构造/reader 路径(工厂 `0xf48b30` case 3、slot 19 `0xe5a7a0`、slot 2 `0xe89a00`)找出写 `*(CLUB+0x100)` 的反序列化器,链到具体归档成员。强候选(必须证明,不许假设):`table_extra_3.dat`(client 13,053,908 B / server 35,009,248 B,两档都有;t57 的成立年 fixture 就来自 client extra_3;t63/t57 held 的 `Cebd/Cyfn` 都把 `+0x100` 对象叫 "extra")。排除其余成员(club_links.dat、8 个编号子表、name_table_*)要给证据。
2. **成员行文法独立闭合**:对 `table_extra_3` 两档做 t57 式数据侧行框闭合(四对齐 identity triple DP、ordinal 分层、footer 敏感性、每档行数);identity 宽度按本表自证,不得照抄 club 主行 12B 或上游 13B/14B 约定。行数若 ≠ 84,259,说明行与 club 的配对方式(按 ordinal/UID join)要给证据。
3. **对象内游标**:从反序列化器证明 wire 字节 → 对象成员 `+0x78 / +0xd8 / +0xe0..0xf5` 的映射(含跳过/条件分支);给出每行内 22 个字节的绝对坐标规则。
4. **全档域检验**:两档全量行(向量化):22 字段值直方图 vs `evidence/fm24/reports/editor_schema/master.json` 的 `enums['cnst']`(scoped enum,冻结);跨档按 UID 逐行配对核对;`0xffffffff` 与合法 0 分列;与 comp 侧 t64 观测子集 `{0,1,2,4,6}` 对照(仅对照,不搬结论)。t01 夹具回归(Liverpool/Bernabéu/成立年 14 条 client extra_3 witness)必须复洽。
5. **转正与顺带收割**:22 个 cnst 逐字段过闸 → L3(gate+helper+cursor+全档域四件套齐);同一游标若同时闭合 `Cebd(+0x78)`、`Cyfn(+0xd8)`,按同样标准转正(它们是 t57/t63 的 held,不是本轮新发现);过不了的给 held+首反例,negative 原样保留。
6. **独立 verify.py**(不 import builder/ReaderCFG/fm24_dump)+ builder `scripts/t71_club100_cnst.py`;`--help`/`--selftest`;退出码 0/1/2。

## 边界

- 只做 CLUB+0x100 链与上述 24 个 held 字段;不重做 club 主行其余 350 unmapped、8 子表、CLUB_LINK、`+0x150` tag0(t63 已闭)、nation/comp、person/PDxx。
- 不启动游戏/编辑器/IDA,不联网,不读写 Z:;只读外部数据。
- 全档统计可向量化,L3 判定不得抽样代替全档。

## 交付 scratch/t71/out/

- `chain.json`(静态链:成员绑定 + 对象内游标,含 VA/file offset/原字节)、`field_map_r3.json`(24 个字段的增量 grades,引用 t63/t57 held id)、`rows_extra3.json`(行框 + 坐标摘要)、`verify.py`、`REPORT.md`、`DONE.md`(首行 `DONE type=t71 status=complete`);builder `scripts/t71_club100_cnst.py`。

Python `py -V:3.12 -I -B`;`FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data`;完成跑 verify + `scripts/t01_anchors.py`(7/7)。
