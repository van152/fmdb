# t16 任务书:类序列化器字段提取引擎 —— E20 手法从 2 个实体泛化到全部类

先读 [AGENTS.md](../AGENTS.md)。

## 前置条件

`scratch/t14/out/stage2_map.json` 必须已存在(t14 交付)。先校验它 `"status"` 是 complete_,否则直接落盘 `"status":"blocked_waiting_t14"` 收工,不要自己抢跑 t14 的活。

## 一句话目标

E20/E21 已证明:**行内字段偏移 = 类序列化器逐字段固定指令顺序 + 显式宽度立即数**——但至今只手工做过 comp(t01f)与 nation(t01g)。本任务把它做成引擎:对每个 db 类,从它的序列化函数批量抽出 `{4CC 码, 对象内偏移, 宽度, 指令地址}`,与 schema 4CC 字段集对齐命名,生成实体级字段表。

## 已验证机制(当输入,不要重推导)

- factory 构造块:`handler_off(t) = 0xF49D38 + rel32@0xF49D38+4t`(.rdata 文件偏移口径,**file_off + 0xA00 = RVA**,VA = RVA + 0x140000000);块尾 `jmp 0x140f4a6a9`。
- 块内 `call <init>` → 序列化/初始化函数;行对象字段访问:`mov/movsx/movzx reg, [reg + off]` / `lea rdx,[reg + off]`(t05_reader_widths.py 的 W/O 提取已是这个路数,只读复用)。
- 4CC 比较链:`scratch/t08/out/chains.json`(226 条链);码实例全表:`scratch/t12/out/codes_full.json`(4,278 条,含 shape/object_off/instruction)。
- schema:entity → 4CC 字段集见 `scratch/t05/schema_inventory.json`;已命名槽:`reports/t12_field_names.json`(132/240,E55 口径)。
- reader→槽:`scratch/t05/reader_widths.json`。

## 引擎设计要求(`scripts/t16_serializer_walk.py`,新增;不改任何既有脚本)

1. 输入:类名列表(默认全量;`--entity club` 可单跑)。
2. 定位序列化函数:factory 块 → call 目标(BFS 深度 ≤4,防循环);跳过 alloc/free 这类公共函数(用调用扇出判断:被 >50 个类共用的 call 是运行时函数)。
3. 逐指令提取字段访问序列;`--golden city|weather|comp` 跑黄金集。
4. 对齐命名:walk 序列(offset+width+类型)↔ schema 4CC(类型+宽度)做单射分配;与 t12 已命名槽一致性必须 ≥98%,冲突列冲突清单**不许静默覆盖**。
5. 退出码 0/1/2;`--help`/`--selftest`(selftest 至少:黄金集 weather 89 字段中 spot 抽 10 个偏移与 E27 工件一致)。

## 黄金集验收(引擎没资格放量,除非先过这个)

- **city**:E42 的三个引用字段定名 + 56,293 行框架不破坏。
- **weather**:E27 的 89 个 L3 字段(88 季节字段 + wnam)偏移全部复现。
- **comp**:E20 的 18 个行偏移全部复现。
黄金集任何一条复现失败 → 引擎判 1,不许带伤放量。

## 批量执行

黄金集过了之后按优先级跑:club(433 字段,tier1)→ nation(346,tier1)→ team → stad → injury → 其余。每类落盘一个 `fields_<tag>.json`,进度写 `ledger.json`(`{"entity","fields_total","fields_named","fields_unnamed","conflicts","evidence_grade"}`)。

club 是 mixed 实体(t04 只闭合过 1 个字段)——若 walk 到 club 序列化器成功,这是阶段三最大突破;若它有多个序列化器分支,先报结构再逐分支。

## 纪律

- 只写 `scratch/t16/out/` + 新增 `scripts/t16_*.py`;scratch/t05..t14、reports/、docs/、evidence/ 只读。
- 不联网、不启动游戏/编辑器/IDA。
- 45 分钟做不完就分批落盘标 `"status":"partial_<限定词>"`。
- 数据侧需要 CSV 时:`FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data`(已设),用 `scripts/fm24_dump.py` 本地导出。

## 交付(scratch/t16/out/)

1. `fields_<tag>.json` × N —— 每实体字段表:`{"field":"CMWE","offset":68,"width":4,"type":"...","evidence":{"inst_off":"0x...","instruction":"...","4CC_chain":"chain_0145"},"grade":"L3"}`
2. `ledger.json` + `ledger.md` —— 覆盖率汇总。
3. `verify.py` —— 独立复算黄金集 + 抽样实体。
4. `REPORT.md` —— 引擎方法、黄金集结果、冲突清单、未闭合项。

## 验收线

1. 黄金集三实体 100% 复现(这是硬门)。
2. ≥10 个实体的字段表交付,club/nation 必须在内(哪怕 partial)。
3. 所有命名字段带 L3 证据(指令地址),verify.py 复算通过。
4. 未命名/冲突字段如实保留,负结果不删。
