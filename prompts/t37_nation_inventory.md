# t37 — nation 子表广度 inventory(luna 数据侧侦察,补 t29b club)

先读 D:\tmp2b\fm24-db\AGENTS.md。你是受指挥官委派的子代理。club 侧 t29b inventory 已交付(38 父码),sol 静态 cursor 已闭 6 子表 44 L3,但 **sol openai-codex 额度暂受限**,静态线暂停。本任务做 **nation 侧互补广度数据侧侦察**:把 nation list 父码的子表找出来、画像、生成 L2 候选,为 sol 恢复后静态闭合备料。**不做静态 cursor、不晋级 L3**。

## 已确认基线
- **nation schema**:evidence/fm24/reports/editor_schema/master.json#entities.nation.xml[0].fields(346 字段,冻结 SHA 7d57477e 对照 MANIFEST)。**29 个 list 父码**,从 `list_item_fields` 取 item 字段名+类型。有 item 的父码(子表候选):Nagr(3)/TCrs(4)/Nrvn(2)/Nefr(7)/Nnfr(7)/Nntp(6)/Nctp(5)/Nrtp(5)/Nlns(2)/NTRv(2)/NWGv(2)/NSps(2)/NCro(2)/Ntxr(9)/Nfmp(6)/Nftb(7)/Calt(2);0 item 的(Nchi/Nphi/Tko1/Tkg1/Tko2/Tkg2/Tko3/Tkg3)多为 ref-only list,可能嵌主行或共享表,如实标注。
- **t28 已闭 nation client tail**(E64):Nlns/Nefr/Nnfr/Nagr 四字段 L3(A/B/C/D 坐标,getter selector 0/1 区分 B/C)。**这些已闭父码标 linked_by_t28,不重复画像为 unknown**。
- **子表身份源**:scratch/t14/out/census.json(74 表 table_type/handler_off/vtables.class/primary_class/entity_tag)+ scratch/t14/out/stage2_map.json + reports/stage2_table_identity.json。
- **t33 batch II 画像**(E75,直接消费):scratch/t33/out/profiles/(t12 AWARD_HISTORY/t39 AVERAGE_POINTS/t45,t48 RECORD/t58 WEEKLY_WAGE_CONTRIBUTION/t59 MEDIA_EXPECTATIONS/t73 ITALIAN_SERIE_A)+ subtable_candidates.json(候选 t12->AWsh/t39->csap/t45,t48->Plhs/Pnph/Pacl/t58->Cwcl/t59->Csme)。
- **club 方法范例**:scratch/t29/out/subtable_inventory.json + build_inventory.json(**复用其 inventory 结构与方法**;注意其 verify.py ROOT parents[3] bug,你用 parents[2])。
- 数据导出 scripts/fm24_dump.py,FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data;**多帧成员注意 E66**(load_payload 取首帧,空 stub 时取真实第二帧;client table3 有 28 帧)。

## 任务(数据侧,候选不晋级)
对每个 nation list 父码(优先有 item 字段的):
1. **定子表**:RTTI 语义匹配(如 Nntp→NATION_TRANSFER_PREFERENCE 类、Ntxr→TAX_RULE 类、Nfmp→FAMOUS_PLAYER 类)+ t14 primary_class/entity_tag + stage2 身份 + schema item database_table_type(若有)。匹配不确定标 unknown,**不猜**。nation 父表是 table_type=10(client t25 已闭 251 行;server 未独立解析行布局)。
2. **画像**:dump 候选子表全行(多帧感知),报 count/stride/行封口方程;逐列画像(值域/distinct/哨兵 0xFFFFFFFF 率/packed day/year 日期/nation ID 域落界/cash 样金额/enum 值集/bool 掩码)。
3. **L2 候选列映射**:item schema 字段按类型语义对候选列(date 落 packed day/year、ref 落 nation/club ID 域或 t32/E69 record-key pair 模型、cash 落金额),标 candidate 绝不 L3;附全量统计证据。
4. **复制就绪清单**:每父码 {parent_4cc, table_type, archive, rtti_class, reader_va(若 t14 有), count, stride, item_field_candidates, confidence, blockers}。已闭 t28 父码标 linked_by_t28。

## 纪律
- 只读 scratch/data/ + 仓内证据 + 只读 editor.exe(VA 对照用 scripts/t05_pe.py);只写 scratch/t37/out/ 与 scripts/t37_*.py;不覆盖 t24/t28/t29/t33 产物。
- 候选不写结论;无独立证据不赋列名;负结果/反例保留;匹配不到如实 unknown。
- 卡壳写 partial 再做下一个;新脚本 --help/--selftest,退出码 0/1/2;单次打印 ≤400 行;大 JSON 分片;状态词 complete_*/partial_*/negative_*。
- 不启动游戏/编辑器/IDA,不联网,不读写 Z:。

## 交付 scratch/t37/out/
- nation_subtable_inventory.json(每父码发现+画像+候选+confidence+blockers,可分片)
- profiles/(候选子表逐列画像机读)
- REPORT.md(已定子表数/候选字段数/unknown 清单/与 t28 已闭父码衔接/与 sol 静态衔接)
- verify.py(独立复算行封口+候选列统计抽样;**ROOT=Path(__file__).resolve().parents[2] 指向 fm24-db**)
- DONE.md

Python `py -V:3.12 -I -B`;完成跑自己的 verify(须 PASS)+ t01_anchors.py(7/7)。打印交付清单:每父码拿到什么、卡在哪。