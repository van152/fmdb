# t54 — Schema v5→v6 合并:t53 TCrs 双闭合裁决并入(luna)

你是受指挥官委派的子代理,做**谨慎的合并**任务。当前公共 schema 为 **v5**(E92,含 fix1)。t53(E93)完成 TCrs 双闭合裁决,本任务把其并入为 **v6**,全部保留 v5 既有内容 verbatim,只做增量:

1. **TCrs 裁决**(t53):主档 wire = `table_9.dat` `this+0x188`(server 166/85 presence、85 段 2,219 项、tag3/version2、PUnP 全 -1);getter 槽 `[this+0xb0]+0x48` back 到 **table_extra_9.dat 类型化后缀**(t50 名称块之后;server 179/72、33 非空向量 76 项;12+Σspans=105228/client 83927 EOF 闭合)。**这修正 v5 中 `nation_t9_wire.table_extra_9.target_parent_assignment=[]` 的表述**:extra_9 不再是"未绑"——其类型化后缀现在是 TCrs getter 的已验 backing(名称块部分仍属 t50 名称表口径);同时主档 TCrs 向量按 t9 主表记。4 个 PUn* 字段 **held**(v5 已如此,保持)。
2. **t50 块内歧义消解口径**:t53 的 reader 逐块消费把 t50 保留的 server 4 候选铺法消解为实际 wire(row2 @867 vs @875、row82 双列);v5 的 `adjudication: NO WINNER` 记法**保留**并追加 t53 交叉结果(不删旧文,加注)。
3. **EDfx**:结论收窄为 editor-only 输出路径(上游输入持久化不在结论内);EDsc:仍未找到调用链(v5 原样保留)。
4. t53 的 8 组错-mode trials 与"无别名断言限已查路线"按 negative/held 口径入账。

## 必读
- AGENTS.md(硬约束;候选不写结论;negative/held 原样保留;L4=0)
- reports/club_nation_subtable_schema.json + .md(**v5 基线**,E92/fix1 后状态)
- scratch/t53/out/discovery_crs_wire.json + cursor_crs_*.json + fields_PUn*.json + REPORT.md + DONE.md(指挥官补写版)
- scratch/t52/out/consolidate_v5.py + verify.py(**方法复刻**;v5 builder 有 E91@L2-only 守卫先例)
- scratch/t01/LEDGER.json(E87–E93)

## 任务
1. `schema_version: 6`;nation_t9_wire 增 `t53_crs_adjudication` 节(主档计数/后缀计数/双档闭合公式/8 trials/no-alias 边界);`table_extra_9` 节按裁决改写(加注不改写旧负例:slot19 强套负例 6 拒绝保留);coverage nation 计数如实更新(held 计数不变——4 PUn* 已 held;negative 记录数按实际新增 trials 调整并逐条列出);`incremental_provenance.tasks` 增 t53(E93,level L2——**注意 E93 是 L2 验收,勿写成 L3 映射**;复用 t52 fix1 的 E91@L2-only 守卫模式)。
2. `tables` 8 表、`negative_regressions` 4 条、`v3_baseline`、`club_auxiliary_sources`、club 计数、`nation_static_side`(t47/t51)**verbatim 不动**。
3. markdown 同步重生成(v5 md 为底+新增节);json/md 同名成对,数字自洽。
4. 独立 spot 脚本(**不 import 合并逻辑**):断言 v5 快照 SHA、保护节 verbatim、t53 关键数字(2219/76/166-85/179-72/39/EOF 公式)与 t53 out 文件一致、t50 原文未动;t01_anchors 7/7;verify 独立;--help/--selftest;退出码 0/1/2。
5. 候选不写结论;凡 t53 held/partial/negative 原样进 v6。

## 边界
- 只改 reports/ 两文件与 scratch/t54/、scripts/t54_*.py;**不改** scratch/t47/t49/t50/t51/t53;不改 BASELINE.md(指挥官另行)。
- 不启动游戏/编辑器/IDA,不联网,不读写 Z:;L4=0。

## 交付 scratch/t54/out/
- consolidate_v6.py、verify.py、spot_*.log、REPORT.md、DONE.md;reports/ 两文件升 v6(指挥官验收后提交)

Python `py -V:3.12 -I -B`;FM24_DB_DIR=<WORKSPACE>/scratch/data;完成跑 verify + t01_anchors.py(7/7)。
