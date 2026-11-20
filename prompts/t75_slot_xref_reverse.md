# t75 — club/nation/comp 剩余槽位 Wire-First 反查收尾(sol)

你是受指挥官委派的子代理。第 1 波 t72 已交付三主表的**未命名物理槽位清单 + 值域指纹**(数据侧,L2 口径)。本任务用静态 exe 反查把其中能闭合的最后一批槽位转正:对每个未命名槽位,按"槽位 → 成员偏移 → reader extent 内的 getter/xref → 4CC → 全档域"反向链,补齐 club/nation/comp 主行剩余真实槽位。

## 必读

- AGENTS.md;`scratch/t72/out/inventory.json` + `fingerprints.json`(**本任务的主输入**:unnamed/held 槽位分类、逐槽宽度候选/min-max/cardinality/all-zero/全一占比/外键命中/wrong-UID 控制/first-last 样例/xref_hint)
- `scratch/t57/out/field_slots.json`、`scratch/t59/out/field_slots.json`、`scratch/t55/out/field_slots.json`(槽位→object_displacement/execution_index 的坐标来源)
- 既有静态台账(不得推翻,只能补充):t57/t59/t55 REPORT + instructions/branches 分片;t63/t64/t65 field_map_r2(negative/held 原文保留);`scratch/t62/out/` EDsc 分发;schema v10 `reports/club_nation_subtable_schema.json`
- t66 REPORT(引用 lane 的 ordinal-vs-UID 纪律)
- 静态来源:只读 `D:/tmp2b/fm24/input/editor.exe`,SHA `b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4`;file offset/VA 口径沿用 t57

## 任务

1. **优先级队列**(指挥官 2026-11-21 指令:先 nation 段内文法,后 club/comp 特色槽):
   - **第一优先:t72 的 10 项 `escalations`(nation 段内变长文法,slot_2/slot_3/slot_4/... 的 A/B/C/D 段、Nftb 等内项文法)**——t72 数据侧明确上交的,配合 t46 profiles / t55 field_slots 的段坐标,把每段的 item 文法钉到字节级并给段内标量/引用槽命名;这是 nation 主行 318 unmapped 的最大空白。
   - 第二优先:club/comp 的 unnamed 槽里**数据特征最强**的(小枚举子集命中 scoped enum、外键命中高且 wrong-UID 控制例干净、非全零全一),按 t72 指纹排序逐个反查。
   - 第三优先:held 邻接槽(t63/t64/t65 held 但指纹显示有活值的;t71 已闭的 24 项不在其列,勿重做)。
   - 全零/全一且无 xref 的放最后(可能就没 wire)。
2. **反查链**:每个目标槽位给:数据侧槽位坐标(archive+行内偏移+宽度候选)→ 对应 reader 位移(t57/t59/t55 slots 的 object_displacement/transfer)→ 在 CLUB/NATION/COMP reader extent 及 helper 区内找读该位移的指令(精确比较/bit-test gate、helper rel32、vtable 调用)→ case-sensitive 4CC 匹配 master.json `field_codes`(3,009 个,含 locations)→ 全档域验证。nation 段内文法另需:段循环的静态读取点(t46 server table_10 reader 链)→ 段内 item 边界文法 → 全档 item 重放闭包。
3. **nation 特记**:t65 第二轮 forward 普查 0 新 L3(收益递减已量化);本任务是**反向**角度,若指纹显示某槽是干净引用 lane 而 forward 4CC 搜漏了,允许转正,但每条必须有完整四件套(gate/helper/cursor/域)。nation A_B_C_D 段内文法若 t72 重放成功,可顺带闭合段内标量槽;失败项沿用 t46/t55 边界。
4. **过闸 L3 / 不过 held+首反例**;与既有 negative 冲突时不翻案,除非给出推翻旧条目的明确证据并引用原条目 id。
5. **独立 verify.py**(不 import builder/ReaderCFG/fm24_dump)+ builder `scripts/t75_slot_xref_reverse.py`;`--help`/`--selftest`;退出码 0/1/2;t01 anchors 7/7。

## 边界

- 只做三主行 unnamed/held 槽位的反查;不碰 8 个 club 子表、CLUB_LINK、t71 的 +0x100 链、集合层(t66 已闭)、person/PDxx。
- 不启动游戏/编辑器/IDA,不联网,不读写 Z:;全档验证向量化,不得抽样代替。

## 交付 scratch/t75/out/

- `xref_reverse.json`(逐槽反查台账:槽位坐标→指令链→4CC→grade,含 escalate/负结果原文)、`field_map_r3.json`(club/comp/nation 增量 grades,引用既有 id)、`verify.py`、`REPORT.md`、`DONE.md`(首行 `DONE type=t75 status=complete`);builder `scripts/t75_slot_xref_reverse.py`。

Python `py -V:3.12 -I -B`;`FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data`。
