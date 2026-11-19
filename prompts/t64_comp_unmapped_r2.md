# t64 — Comp 主行 unmapped 第二轮深度普查(sol;t59 方法加深)

你是受指挥官委派的子代理。t59(E99)comp table_25 主行 255 occurrence 中 **196 unmapped**(含 VARt/HKEt 家族、RsL0/COPc 双 occurrence、cnam/csnm/c3ln 字符串槽、集合与未定标量)。本任务做第二轮:在**不推翻 t59 已闭 L3** 的前提下,对 196 个 unmapped 与 2 个静态未触发 payload 深挖。

## 必读
- AGENTS.md;scratch/t59/out/field_slots.json + field_map.json + REPORT.md(**行框/站点唯一来源**;82 观测+2 静态未触发;COMP slot19 0xeb7000 837/114)
- scratch/t59/out/REPORT.md 的 held 节(**不得重判**,但可补证据):cnam/csnm/c3ln 备选路径只读 +0x48/+0x40 不读 +0x50、VARt/HKEt 直接分发读 rules/context、rdui 全 7,047 抑制
- scratch/t63 brief 的范式(comp 本地 getter 投影先例即 t59 cnst;本次在 comp 自身继续扫剩余 helper)
- evidence/fm24/reports/editor_schema/master.json(comp.xml 255 字段冻结)

## 任务
1. **剩余 helper 扫描**:主 extent(0xeb7000..0xeb7e42)内未归因的直接 stream+0x28(54 个中 3 个未解释:0xeb7218/0xeb72f8/0xeb7332)与未归因 helper 调用,逐个定性:被哪个/哪些 XML occurrence 消费。
2. **VARt/HKEt 家族**:rules/context 分发链静态走查,判定其是否可能绑定 COMP 同对象(若不能,给证伪清单+首反链,保持 unmapped);若能,全档域检验过闸。
3. **字符串槽**:cnam/csnm/c3ln 在 inline tag4 路径之外找其余消费点;找不到则保持 unmapped+证伪记录(候选不入结论)。
4. **2 个静态未触发 payload**(+0xa8/+0xe0):给出"何时会进"的静态条件描述(分支谓词),数据侧确认双档全 0。
5. 全档域检验过闸 L3;否则 held/unmapped 原样+首反例;独立 verify.py + builder scripts/t64_comp_unmapped_r2.py;--help/--selftest;退出码 0/1/2。

## 边界
- 只 comp 主行;不碰 t59 已闭 L3(818 倒置口径不变);不碰 comp 派生集合(那是 t66 的活,若 t66 已交付可引用其结论);不启动游戏/编辑器/IDA,不联网,不读写 Z:。

## 交付 scratch/t64/out/
- helpers.json、field_map_r2.json、exclusions.json、verify.py、REPORT.md、DONE.md;scripts/t64_comp_unmapped_r2.py

Python `py -V:3.12 -I -B`;FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data;完成跑 verify + scripts/t01_anchors.py(7/7)。
