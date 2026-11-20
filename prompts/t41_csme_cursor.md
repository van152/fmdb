# t41 — Csme 媒体预期子表 变长 stride cursor(t39 方法复制 + 变长扩展)

你是受指挥官委派的子代理。club 子表 branch-aware cursor 法已 **7 次证实**(t27/t30/t31/t32/t34/t36/t39,累计 51 L3)。本任务复制到 **Csme(媒体预期),table_type=59**,首次攻 **变长 stride**(前 7 次均定长)。静态攻坚,晋级 L3。

## 必读
- D:\tmp2b\fm24-db\AGENTS.md(硬约束)
- D:\tmp2b\fm24-db\scratch\t39\out\REPORT.md + scripts\t39_tchl_cursor.py + scratch\t39\out\verify.py(**最新范例,7/9 L3**;leaf thunk→真 reader+identity tail、双 mode fork、shared 排他闸门、footer 末 u32 不妄断、**多帧按 entry.size 选**)
- D:\tmp2b\fm24-db\scratch\t27\out\replication.md(方法模板)
- D:\tmp2b\fm24-db\scratch\t33\out\profiles\table_server_59.profile.json + .rows.jsonl(**数据侧画像,直接消费不重 dump**)
- D:\tmp2b\fm24-db\scratch\t24\out\subtables.part001.json(Csme nested schema occurrence)
- evidence/fm24/reports/editor_schema/master.json(club.xml Csme.list_item_fields,冻结 SHA 7d57477e 对照 MANIFEST)

## 已知锚点(t33 实测)
- Parent `Csme`,table_type **59**,RTTI `STARTING_MEDIA_EXPECTATIONS`,club.xml "Starting Media Expectations",**2 字段**:`Msid`(Media Source,database_record_unique_id→media_source 表)、`Melf`(Predicted League Finish,integer)。
- handler_off `0xf49950`,vtable VA `0x141882fa8`(t14 census;追 slot19 真 reader,可能 leaf thunk)。
- server payload **224880 B**,SHA `7eee0ecc59ee306aefc52eb7a7f7095d439748f3e06ac9d36d3ddc1568c8b1a7`,packed_offset 38661659,packed_size 62202,count **9079**,**model=variable**。
- closure `14 + Σrow_lens(224858) + 8 = 224880`;**identity 13B @ row_end-13**,grammar `ordinal|id|id|marker`,tail13_hits=9079、id_pair_hits=9079(变长行可用 identity 尾锚定,类 lcrg_tail)。
- entity_tag=**play**(club/play 共用,**排他闸门须验实际 owner 指向**,不沿用 entity_tag 作独占结论,参 t39 national-team 教训)。
- **多帧/E66**:若 load_payload 返回空/异常短,查成员是否含 stub 首帧;**权威选帧子=entry["size"]==224880**(E78:entry["sha256"] 可能是成员/压缩 SHA 而非解压 payload SHA,payload SHA 另行计算验证)。client 有无 table59 如实记。

## 任务(同 t39 + 变长)
1. 两 archive 目录+payload:table59 client/server count/stride 分布/SHA;client 无成员如实记。
2. factory→RTTI/vtable→slot19→真 reader(+identity tail),PE runtime-function extent 建可达 CFG(t21b_control_flow.ReaderCFG),追 thunk,保存 bytes+VA。
3. 分支五分类(wire_data/runtime-external/IO-result/context-lifecycle/dead)逐条证据+首行反例;**变长关键:找出决定每行长度的是哪些 wire_data 分支**(计数循环/可选块),逐行 replay 求 row_len;有 caller mode 条件则 fork 全表跑。
4. walk 逐行闭合 `header+Σrow_len+footer==payload_len`(每行 row_len 由 reader 语义决定,非固定 stride);双坐标(legacy14/wire13);identity 后置校验(lane0=ordinal,后两 lane 相等非零,marker);selector 全表观察。
5. 三重闸门:唯一 scoped occurrence→getter 4CC 分发+object 成员→实际 wire sink;全表独立画像(Msid ordinal 引用走 media_source 目标表实际 ordinal 集,Melf integer 有符号/sentinel -1/0 区别,bool 掩码)。2 字段可证实者 L3,域冲突 held 保留首反例。
6. 独立 verify.py(不 import builder)+ builder scripts/t41_csme_cursor.py;--help/--selftest;退出码 0/1/2。

## 边界
- 只 Csme/table59;不碰已闭 Cstc/Clhs/CSrs/Cmti/CNtp/Cdbt/Tchl;Cafl/Cvfl 另案。
- 候选不写结论;negative/held 反例保留;L4=0;不启动游戏/编辑器/IDA,不联网,不读写 Z:。
- 消费 t33 画像;预算内无法闭合则诚实 partial+已绑定子集+剩余+首反例(变长首次,允许 partial)。

## 交付 scratch/t41/out/
- cursor_csme.json、fields_csme.json(2 字段台账+grade)、instructions.part*.json、branches.part*.json、verify.py、REPORT.md、DONE.md
- scripts/t41_csme_cursor.py

Python `py -V:3.12 -I -B`;FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data;只写 scratch/t41/ 与 scripts/t41_*.py;完成跑 verify + t01_anchors.py(7/7)。