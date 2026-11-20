# t79 — stadium(21)+team(24)+extra_24 静态 L3 收割 + CLUB+0x18 转发链(neon 攻坚)

你是受指挥官委派的攻坚车道(接替 sol 位)。分母账本(E116)已确认:三主表主行静态收益已见底,当前静态 ROI 最高的是 **stadium/team 两条主表 + table_extra_24** 和 **club 经 CLUB+0x18 转发的 6 个 held 字段**。t74 已把行框钉死,t76a 会给出 L2 指纹,你做静态三重闸门收割。

## 必读

- AGENTS.md;`scratch/t74/out/frames.json`(行框真源:stadium client 38B/server 181B×48,413;team server-only 变长或 extra_24 82B——以 frames.json 为准)+ `row_widths_21/24_*.csv`
- `scratch/t76a/out/`(t76a 的 L2 槽位指纹;若尚未落盘,自己跑 t74 帧上的槽位 profiling,不等待)
- `evidence/fm24/reports/editor_schema/master.json`:`entities['stadium.xml']`(约 60 字段)、`entities['team.xml']`(约 25 字段)+ `field_codes`(3,009)+ `enums`
- 静态范式与既有台账:`scratch/t57/out/REPORT.md`(三重闸门)、`scratch/t63/out/REPORT.md`(club held 的转发描述:Cldi/Cndi/Codi 转发第一 Team;Csti 接 stadium fixup;Crep/Cdvi getter 走首 Team 间接对象)、`scratch/t59/out/REPORT.md`(cnst 投影范式)、`scratch/t66/out/REPORT.md`(t24 ordinal→UID 84,507;table_extra_24.dat 只取过 ordinal)
- 静态来源:只读 `D:/tmp2b/fm24/input/editor.exe`,SHA-256 `b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4`;file offset/VA 口径沿用 t57;STADIUM/TEAM 的工厂 case(21/24)与 reader extent 自行定位(参照 t57 对 CLUB 的做法:factory `0xf48b30` rel32 表)

## 任务

1. **stadium(21) 静态 L3**:定位 STADIUM slot 19 reader extent,4CC gate→cursor→同位移 sink 三重闸门,对齐 stadium.xml 字段;client 38B 定长 + server 181B 定长差异要静态解释(server 多出的段对应哪些对象成员);全档 48,413 行值域双档验证。client 锚点 `Scti@3/Slat@17/Slon@21/rdui@25/duni@29` 必须复洽。
2. **team(24) 静态 L3**:TEAM reader extent;84,507 行(t66 已证 ordinal→UID);t74 行框;team.xml 字段逐个过闸;`WpBn/dbty` 等 t59/t75 侧的 team 邻接结论只引用不重判。
3. **extra_24 静态绑定**:证明 `table_extra_24.dat`(server 6,929,586B)装载到哪个对象(预计 TEAM 侧伴生流,类比 t71 的 table_extra_3→CLUB+0x100);行框自证(用户先验:82B 定长——必须自证);若文法闭合,给 extra_24 的字段槽位,不改 t66 "只取 ordinal" 的旧边界(那是当时任务范围声明,不是行框结论)。
4. **CLUB+0x18 转发链**:从 CLUB reader 定位 `+0x18`(首 Team 对象)的装载与 getter 分发,证明 `Crep/Cdvi/Cldi/Cndi/Codi/Csti` 六个 held 的完整链路 CLUB→Team→team.xml 字段(4CC 用 team.xml 的 T* 名),全档域验证后把 club.xml 六个 occurrence 升 L3(标注"经 +0x18 转发的投影");setter 入口也要找(用户要求:写入路径同步入账)。
5. **独立 verify.py**(不 import builder/ReaderCFG/fm24_dump)+ builder `scripts/t79_*.py`;`--help`/`--selftest`;退出码 0/1/2;t01 anchors 7/7。

## 边界

- 只做 stadium/team/extra_24/CLUB+0x18 六字段;不碰三主表其余 unmapped(已见底)、person/PDxx、t76 各车道目标表(award 等)。
- 不启动游戏/编辑器/IDA,不联网,不读写 Z:;全档验证向量化。
- **防冲突**:只写 `scratch/t79/` 和 `scripts/t79_*.py`。

## 交付 scratch/t79/out/

`xref_stad_team.json`(静态链台账)、`field_map.json`(stadium/team/extra_24/club 六字段的 grades)、`verify.py`、`REPORT.md`、`DONE.md`(首行 `DONE type=t79 status=complete`)。

Python `py -V:3.12 -I -B`;`FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data`。
