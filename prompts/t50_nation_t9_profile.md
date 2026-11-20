# t50 — t9 NATIONAL_TEAM_CONTAINER 数据侧独立画像(L1/L2,纯数据,不碰静态)

你是受指挥官委派的子代理,做**数据侧批量画像**(cheap batch)。t47(sol,E87)已静态发现 nation 8 parent 内嵌于 t9 NATIONAL_TEAM_CONTAINER;t49(sol)正做静态+wire 验收。本任务**独立从数据侧**重建 t9 两成员的 row framing/identity census,作为 t49 的 **L2 交叉验证**。**只做数据侧:不读 editor.exe、不追 reader/VA、不命名语义字段、不做 ordinal join**(那是 t49 的事)。

## 必读
- D:\tmp2b\fm24-db\AGENTS.md(硬约束;negative 原样保留;候选不写结论;L4=0)
- scratch/t46/out/REPORT.md + profiles/table_server_10.profile.json + profiles/table_server_10.rows.jsonl(**数据侧画像范例**:row/offset/body_offset/len/raw_hex/identity/prefix_probe)
- scratch/t47/out/cursor_nation_tax.json(**仅对照 row framing 结果,不拷其静态结论**;archives 成员起点/size/SHA)
- scripts/fm24_dump.py(load_payload,E80 已修:member start=data_base+offset,按 entry.size 选帧)

## 已知锚点(E80)
- 成员绝对起点=`data_base(34)+entry.offset`;按 `entry.size` 选帧;`entry.sha256`=压缩区 SHA(另存 payload SHA)。
- `table_9.dat`:client 31956 B / server 307564 B;`table_extra_9.dat`:client 83927 B / server 105228 B。
- tad shell `03017461642ef10d`(8B)+ u32 count@8=251(两成员两档均 251)。`table_extra_10.dat` 两档缺失。
- 编号表 wire 格式参考:t10 为 `13 + Σrow_len + 9`(selector 前置 13B 头,9B footer=count0/flag1/maxid)。**t9 是否同构须由数据自证,不可假定**。

## 任务(纯数据侧)
1. 独立解码 4 个 payload(client/server × table_9/table_extra_9),记 entry.offset/packed_size/size、member_start、payload SHA、压缩区 SHA。验证 tad shell + u32 count@8==251。
2. **row framing 尝试**:从数据侧推每行边界(selector 前置游标)。若变长无法唯一闭合,诚实记 partial + 已确定前缀/首行 + 剩余未知段(**不强行猜**)。对能闭合者验 `header + Σrow_len + footer == payload_len`。
3. **identity census**:扫 12B identity tail(ordinal|row_id|repeated|00 结构,参考 t46/t10),逐行记 ordinal/identity,验 ordinal 序列 0..250、repeated lanes 相等、唯一性。若 t9 identity 结构不同,如实记差异+首反例。
4. **row-length 直方图** + 每行 raw_hex 样本(首/末/最长/最短行)。prefix_probe(行首 i32le 候选 count/selector)。
5. 双档对比:client vs server row grammar 是否同构(参考 t46 grammar_diff),count/stride/identity 差异如实记。
6. 独立 verify.py(**不 import 任何 builder/t49**)+ builder scripts/t50_nation_t9_profile.py;--help/--selftest;退出码 0/1/2。

## 边界
- **只数据侧**:不读 exe/IDA、不追静态 reader、不命名语义字段、不做 target ordinal join、不晋级 L3。
- 不碰 t49 产物(scratch/t49/)、不碰 t37/t47 baseline。候选不写结论;negative 原样保留;L4=0。
- 不启动游戏/编辑器/IDA,不联网,不读写 Z:。变长无法闭合则诚实 partial。
- 只写 scratch/t50/ 与 scripts/t50_*.py。

## 交付 scratch/t50/out/
- profile_t9.json(4 成员 anchors+shell+count+closure 判定)、profiles/table_{client,server}_{9,extra_9}.rows.jsonl(row framing+identity)、grammar_diff_t9.json(双档对比)、verify.py、REPORT.md、DONE.md
- scripts/t50_nation_t9_profile.py

Python `py -V:3.12 -I -B`;FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data;完成跑 verify + t01_anchors.py(7/7)。