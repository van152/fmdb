# t62 — EDfx 上游持久化来源 + EDsc 调用链(v3 基线最老悬案,sol)

你是受指挥官委派的子代理,负责**最难**的静态逆向悬案:v3 基线集合 `EDfx` 的上游持久化来源与 `EDsc` 的调用链。既有口径:EDfx/EDsc/AXML/Tchl 属 club/nation 容器集合(v3 snapshot);EDsc 曾判 no_main_wire_slot(t55);EDfx 上游"持久化来源"未定。目标:**把"哪个 reader/writer 持久化 EDfx 内容、EDsc 被谁消费"闭合到可引用证据**;无法闭合则给出可证伪的排除清单(也是进展)。

## 必读
- AGENTS.md(候选不写结论;negative 原样保留;L4=0)
- reports/club_nation_subtable_schema.json(v8):`v3_baseline` 节 AXML/EDfx/EDsc/Tchl 原文、`negative_regressions` 中 EDsc/EDfx 相关条目、`nation_main_row_fields` EDsc 行(no_main_wire_slot)
- scratch/t55/out/REPORT.md(EDsc no_main_wire_slot 的证据与口径)
- scratch/t27/out/replication.md、scratch/t39/t44 REPORT(club 集合 helper `0x15e9830→0x44d7bf0`、全局 VA `0x141b60158`、CLUB slot2 `0xe89a00` 精确分发)
- evidence/fm24/reports/editor_schema/master.json(冻结;club/nation XML 中 EDfx/EDsc 关联字段)
- <OLD_REPO>/input/editor.exe(只读;SHA-256 b82ebe8e…da4,见 t59 REPORT)

## 任务
1. **交叉引用普查**:editor.exe 内 EDfx/EDsc 4CC 全量引用点(字符串/立即数/比较器),逐点分类:collection 打开器/容器构造/序列化 sink/纯比较。
2. **EDfx 上游**:确定 EDfx 内容的持久化路径——reader(从 .dat 载入?)与 writer(编辑器写回?)两侧;若是间接层(经别的集合映射),给出映射链逐跳证据(PE offset + 指令);候选不入结论。
3. **EDsc 调用链**:谁打开/消费 EDsc(与 t55 no_main_wire_slot 结论对齐或推翻——推翻需新证据,旧 negative 不删);client/server 差异如实。
4. **数据侧对证**:若结论指向某 .dat 成员/区域,用独立解码交叉核验(不改写 reports/)。
5. 独立 verify.py + builder scripts/t62_edfx_edsc.py;--help/--selftest;退出码 0/1/2;partial 诚实(排除清单也算交付)。

## 边界
- 只 EDfx/EDsc(AXML/Tchl 顺带引用点可记,不展开);不碰已闭 L3 层;不启动游戏/编辑器/IDA,不联网,不读写 Z:;PE extent 法照 t21b/t59 口径,不可达边不写成死边。
- 交付 scratch/t62/out/:xref.json(引用点台账)、chain.json(逐跳)、exclusions.json(证伪清单)、verify.py、REPORT.md、DONE.md;scripts/t62_edfx_edsc.py

Python `py -V:3.12 -I -B`;FM24_DB_DIR=<WORKSPACE>/scratch/data;完成跑 verify + scripts/t01_anchors.py(7/7)。
