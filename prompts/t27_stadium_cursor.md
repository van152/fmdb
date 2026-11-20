# t27 任务书:t22 球场/迁建子表 branch-resolved cursor 收尾(t20 卡点攻坚)

先读 `AGENTS.md`。t24 刚用"分支感知符号 walk"闭合了 club 主行 84,259 行(已验收 E61)。本任务把同一手法用到 **t20 卡住的子表 table_22(STADIUM_CHANGE)**:解掉 23 个分支,把候选偏移与数据侧日期画像对账,晋级 Cstc 嵌套字段。这是子表方法的模板战——成功后 luna 可复制到 Cafl/Cvfl 等其他 club 子表。

## 已确认基线(直接引用)

- **行框架已封口**(t20):table_22 = 449 行 × 79 B,`14 + 449*79 + 8 = 35493`;行起点 14。`scratch/t20/out/cursor_t22.json`。
- **reader 已定位**(t20):RTTI 类 `STADIUM_CHANGE`(运行时类名,≠stadium 主表实体,E56 裁定为 club 球场/迁建属性集);factory handler file offset `0xF49092`;slot-19 reader VA `0x141538200` / file offset `0x1537800`;t16 in-memory walk 得 18 个带 object sink 的传输 + 23 分支。
- **19 个宽度候选**(t20,和 66,`66+13=79` 只封字节预算不是 cursor):`4,4,4,4,1,4,1,4,4,4,4,4,1,4,1,1,1,4,12`;第 19 项 12B 宽度指令 foff `0x1537AA8`/VA `0x1415384A8`,call `0x1537AB4`,object sink 未解。`scratch/t05/reader_widths.json`。
- **数据侧日期画像**(t13d,关键对账真值):`scratch/t13d/out/audit.json` 对 +12/+16/+50 给出稳定 packed day/year 画像(年份范围 2000–2030 / 2017–2030 / 1900–2030);+0 有 361 个非哨兵值、310 distinct、live 范围 [86,82403] ⊂ club ID 域。**t20 的候选线性配对把 +12 叫 Scap、+16 叫 Styp、+50 叫 Sceb,与这些日期画像矛盾——这正是你要解决的。**
- **schema**:Cstc 父码下 28 个嵌套 occurrence(t24 `scratch/t24/out/subtables.part*.json`,含 Styp/Snew/Salt/Slea/Ssta/Slmd 等);`scratch/t12/out/codes_full.json`;E56 四唯一码 Salt/Scam/Scpm/Slhm 只确认字段身份不给 row offset。
- **成功手法**(t24,正典):`scripts/t24_club_cursor.py` 的分支感知 walker + `scratch/t21/out/control_flow.json` 的 CFG 建模法 + `scripts/t21b_control_flow.py`。核心:把 stream read 建模为"消费 width→产出值→值喂后续分支",对每个条件分支归类(数据驱动可执行 / 运行时外部状态须数据侧反推 / 死代码),用全表分布验证假设。

## 唯一目标

1. **建 CFG**:对 slot-19 reader `0x1537800` 建基本块/分支图(用 t21b 法),把 23 个分支逐条归类;18 个 object-sink 传输 + 第 19 个 12B bulk 全部定位(VA+bytes+file offset,PE 换算用 `scripts/t05_pe.py`)。
2. **分支感知 walk**:对 449 行逐行消费恰好 79 B,footer 封口;用已读字节值驱动分支判定。12B bulk 与 slot0 未命名块要给出字节级解释(可能是 identity/引用数组),不能猜成字段。
3. **对账晋级**:每个候选 row offset 必须同时满足 (a) getter 证据链(schema 名→object_off→行偏移)、(b) 449 行全量数据侧画像吻合(日期字段必须落在 t13d 的 packed day/year 画像、引用字段落 club ID 域)。**三者缺一不晋级**;t20 已证伪的 Scap@+12/Styp@+16/Sceb@+50 配对不得复活,除非新证据推翻日期画像。
4. **模板产出**:把解法写成可复制方法(分支归类表 + walk 模板 + 对账判据),供 luna 复制到 Cafl(29 字段)/Cvfl(19) 等子表;附其他 club 子表的侦察清单(table_id/RTTI 类/reader VA/字段数/stride,能查多少查多少,查不到标 unknown)。

## 边界与纪律

- 只读 `<OLD_REPO>\input\editor.exe`(SHA-256 对照 IDA_PROVENANCE);本地数据 `FM24_DB_DIR=<WORKSPACE>/scratch/data`;table_22 在 **server** archive(`load_payload(codec,'server',22)`)——先确认 client/server 哪个有该表并写明。
- 不启动游戏/编辑器/IDA,不联网,不读写 Z:;只写 `scratch/t27/out/` 与 `scripts/t27_*.py`;不覆盖 t20/t24 产物。
- 候选不写成结论;负结果保留;未解分支如实标 partial,**不以候选名计入命名率**。
- 新脚本 `--help`/`--selftest`,退出码 0/1/2;单次打印 ≤400 行;大 JSON 分片;状态词 `complete_*`/`partial_*`/`negative_*`。
- 卡壳落盘 partial。

## 交付

1. `scratch/t27/out/cursor_t22.json`:CFG/分支归类/逐行轨迹/12B bulk 解释。
2. `scratch/t27/out/fields_t22.json`(可分片):晋级台账 {name,code,row_offset,width,object_off,VA,bytes,grade,数据画像匹配统计}+ 未晋级候选保留。
3. `scratch/t27/out/replication.md`:可复制子表方法 + 其他 club 子表侦察清单。
4. `scratch/t27/out/verify.py` + `REPORT.md`:独立复算 449 行封口 + 字段抽样 + 命名增量 + 未闭合项。

完成后跑自己的 verify、`py -V:3.12 -I scratch/t20/out/verify.py`(确认不矛盾)、`py -V:3.12 -I scripts/t01_anchors.py`(7/7)。打印交付清单。