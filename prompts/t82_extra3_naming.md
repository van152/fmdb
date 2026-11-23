# t82 — table_extra_3 剩余载荷命名:CBW*/CBD* 与尾段虚分派(neon 攻坚 #2)

你是受指挥官委派的攻坚车道(neon xhigh,agy CLI)。t71(E111)已把 `table_extra_3.dat` 双档行游标逐字节闭合,并收割了 `+0x78(Cebd)/+0xd8(Cyfn)/+0xe0..0xf5(22 cnst)`。分母账本(E116)显示 club 还有 **20 个未命名物理槽挂 239 个字段**——其中一大簇就在 extra_3 对象里。本任务命名 extra_3 剩余成员。

## 已冻结的地基(直接用,不重做)

- `scratch/t71/out/chain.json`(静态链:成员绑定/对象游标/各 tag rel32 格与 vtable reader)、`rows_extra3.json`(行框+坐标)、`REPORT.md`(t71 对 B 后载荷的完整消费顺序描述)
- `scratch/t63/out/field_map_r2.json` 的 399 条 club unmapped 中 **CBW\*/CBD\* 族**(CBWa/CBWc/CBWd/CBWf/CBWo、CBDa/CBDc/CBDd/CBDf/CBDo 等)与 `1sbc/1scl/2sbc/2scl/2tbc/2tcl/3sbc/3scl/3tbc/3tcl/C1sq/C2pf` 等疑似 extra_3 后台的 occurrence 清单
- `evidence/fm24/reports/editor_schema/master.json`:`entities['club.xml']` 字段清单+type+dependencies;`enums`;`field_codes`
- 静态来源:只读 `D:/tmp2b/fm24/input/editor.exe`,SHA-256 `b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4`;t71 已证 0x151d2e0/0x151d710/0x15211a0/0x4339e80/0x433bbc0/0x4342940 等 helper 区可复用

## 任务

1. **对象成员反查**:对 extra_3 对象的未命名成员(+0x28/+0x48/+0x68/+0x98/+0xac/+0xf8 之后的族,以及 t71 证到的 `i8 count ×22`、`u8 count ×10`、四类条件段 +48/+30/+38/+70、+50 u32、+68 u16 tag2 item、+40、+dc、公共尾 +ac/+98/+78/8B scalar、server 尾 i16×20/i8×6/16B/8 种 base 虚分派)逐个:对象位移 → getter(和 setter,沿 t79 的双链范式)→ 4CC gate → club.xml occurrence 对齐。
2. **三重闸门**照旧:frozen 唯一 occurrence → getter 4CC 精确分发 → 同位移 sink + 全档域(84,259 行双档,向量化)。CBW*/CBD* 若确系"俱乐部历史/荣誉/董事会书写"类,只按静态证据给 4CC 与槽位,**业务名不发明**。
3. **server-only 段**(t71 记载 client 无此载荷的)与 client-only 段分开记账;`0xffffffff` 与合法 0 分列;默认值(构造 0x3aabb18..30 的 default 6 类)与持久化值分开。
4. **过闸 L3 / 不过 held+首反例**;t63/t57 的 negative 不翻案(除非新链证据明确推翻并引用原条目);t71 已转正的 24 项不在范围。
5. **独立 verify.py**(不 import builder/fm24_dump)+ builder `scripts/t82_*.py`;`--help`/`--selftest`;退出码 0/1/2;t01 anchors 7/7。

## 边界

- 只做 extra_3 对象;不碰 club 主行其余槽(见 t75 裁决)、8 子表、CLUB_LINK、person/PDxx、stadium/team(t79 已收)。
- **防冲突**:只写 `scratch/t82/` 和 `scripts/t82_*.py`。
- 不启动游戏本体/FM 编辑器(IDA 静态分析允许),不联网,不读写 Z:;全档验证向量化,不得抽样代替。

## 交付 scratch/t82/out/

`xref_extra3.json`(静态链+成员台账)、`field_map.json`(增量 grades,引用 t63/t71 既有 id)、`domain_stats.json`(全档域)、`verify.py`、`REPORT.md`、`DONE.md`(首行 `DONE type=t82 status=complete`)。

Python `py -V:3.12 -I -B`;`FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data`。
