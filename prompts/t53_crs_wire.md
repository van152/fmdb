# t53 — TCrs t9 主档 wire 闭合 + EDfx/EDsc 收尾(t51/t50 后继)

你是受指挥官委派的子代理,负责**最难**的收尾任务。t51(sol,E90)已把 TCrs 追到 getter 所用集合(`[this+0xb0]+0x48`)、12B 分配池与 `0x11d3200` 填充路径,但 **member/mode 未绑**;其 sidecar 候选 `table_extra_9.dat` 被 t50(E91)**数据侧**判明为 nation 名称表形态(251 块 `ordinal|name_len|name`,server block0=(0,11,"Les Fennecs"))——TCrs 的 PUn* item 数据**不可能**以该形态存在于块首结构已闭合的部分,sidecar 假设须正面处置。t51 同时记录了关键反例:已绑定的 t9 主 reader 在 `0x105dd63` 也调用同一 item reader,但 `0x105dd56` 写 **`this+0x188`**;server presence 0/1 = **166/85 行**,row 1 `@1726:01` 后确实消费 308 B。本任务裁决 TCrs 的持久化归属并闭合 wire,顺带收尾 EDfx/EDsc。

## 必读
- <WORKSPACE>\AGENTS.md(硬约束;negative 原样保留;候选不写结论;L4=0)
- scratch/t51/out/discovery_unknown2.json(**TCrs 真源**:getter/setter/projection/read_chain sites、object_pointer_path [176,72]、item_allocation_width 12、allocation_pool_VA、archive_candidate_context、main_table_context_comparison;REPORT.md 的 TCrs 段与 Nftb 三重闸门范例)
- scratch/t49/out/cursor_t9_{client,server}.json + REPORT.md(**已接受的 t9 主档行界**,251×2;未命名变长站点只消费不命名——你的 TCrs walk 必须落在这些行界内并与之相容)
- scratch/t50/out/profiles/table_{client,server}_extra_9.rows.jsonl + profile_t9.json(**extra_9 名称表形态 L1 证据**,块首已闭/块内未解)
- scratch/t47/out/REPORT.md(Ntxr 三重闸门+枚举 held 口径)、scratch/t49/out/REPORT.md(pers→people_db 658,011 ordinal walk 先例;@291 side/perm 同 byte bitmask 先例)
- evidence/fm24/reports/editor_schema/master.json(nation.xml#nation parent idx 64,冻结 SHA 7d57477e)

## 任务
1. **TCrs 归属裁决(优先)**:对 `[+0xb0]+0x48`(getter 集)与 `+0x188`(t9 主 reader 写)两条路径建完整证据表——写点/读点/分配池/fill 链是否同一 vector;`0x105dd56` 写 `+0x188` 后 `0x105dd63` 调 item reader 的调用上下文版本与 mode 分叉(t21b_control_flow.ReaderCFG 法);server/client 双档试 mode 0/1,错 mode 记首反例(invalid count@offset)。**以 wire 闭合裁决**:在 t49 已接受行界内,对 presence=1 的 85 个 server 行(row 1 @1726 起 308 B 等)逐行 walk TCrs items(tag 闸门、12B item、EOF),闭合则绑 `+0x188`@t9 主表;闭合不了如实 partial。`table_extra_9` 名称表证据写进裁决书:块内未解部分**不作为 TCrs 容器**(除非你给出 item 级闭合证据)。
2. **逐 item 三重闸门 + ordinal join**:PUnP→person 走 people_db 658,011 实际 ordinal(t49 法,raw 当 UID 的 miss 率如实记);PUnI/PUnT/PUnJ 枚举域无 scoped enum_ref 则 held 不猜标签;bool 位验 bitmask(t49 side/perm 同 byte 先例)。可证实者 L3,冲突/无域 held 留首反例。
3. **EDfx 上游持久化**:从 UI 结果构造链(`0x29c80→0x907f0`、`0x9082e`、`0x909d9→0x103f9f0`、`0x90a24`)追产物去向:是否有 archive opener/record sink 接收生成记录;证 editor-only 或找到 backing member,二选一给静态证据链(现在的"UI 路径已证"不够裁决持久化)。
4. **EDsc**:双字节序零命中已记;试 computed/resource 路线(冻结 schema `allow_add/remove=false`、同 code 另见 advanced/database test/comp test.xml#cpts);无法闭合则加固 negative(指明"未找到调用链"与"证不持久化"的区别)。
5. 独立 verify.py(**不 import builder/ReaderCFG/fm24_dump**)+ builder scripts/t53_crs_wire.py;--help/--selftest;退出码 0/1/2。

## 边界
- 不重做 t49 的 8 parent、t51 的 Nrvn/Calt/Nftb、t47 的 Ntxr;不推翻已接受结论,若发现**真冲突**则 dual-list 记录+首反例,不裁决改写。
- t37/t47/t49/t50/t51 negative/held/baseline 原样保留;候选不写结论;L4=0;不启动游戏/编辑器/IDA,不联网,不读写 Z:。
- 预算内无法全闭则诚实 partial。**优先级:TCrs 裁决+wire > EDfx > EDsc。**

## 交付 scratch/t53/out/
- discovery_crs_wire.json(TCrs 归属裁决+EDfx/EDsc 处置)、cursor_crs_*.json(闭合者)、fields_PUn*.json(逐字段三重闸门+ordinal join+grades)、instructions.part*.json、branches.part*.json、verify.py、REPORT.md、DONE.md
- scripts/t53_crs_wire.py

Python `py -V:3.12 -I -B`;FM24_DB_DIR=<WORKSPACE>/scratch/data;只写 scratch/t53/ 与 scripts/t53_*.py;完成跑 verify + t01_anchors.py(7/7)。
