# t01-h 任务书:factory 跳表全普查 —— 32 实体逐一分类(直线 vs 变长)

> 交给 pi gpt-6-luna max。这是 stage-2 的战术普查:t01f/t01g 已分别打通 comp(直线型)与 nation(变长型),现在要**一次性判定所有实体属于哪一类**,为后续逐实体攻坚排序。
> 规则不变:只读输入、不启动游戏本体/FM 编辑器(IDA 静态分析允许)、不 pip install、Python `py -V:3.12 -I -B`、每个 claim 带 file offset + 字节证据。

## 已知锚点(勿重复发现,直接引用)

- type-id 工厂跳表:基址推导见 t01g——`0xf48b45` 推出跳表基址 `0xf49d38`;type-10 项 `0xf49d60: ef f1 ff ff` → handler `0xf48f27`(alloc 0x1d8 → ctor `0x103ebf0`);type-25 项 `0xf49d9c: f1 f3 ff ff` → `0xf49129`(alloc 0x1b0 → COMP 构造器 `0xeb5dd5`)
- 记录类模式:`.?AV<NAME>@db@@` RTTI;构造器写 vptr;slot7 型查询函数 `mov eax,<type_id>; ret`;slot19=读主体/slot21=写主体(vtable +0x98/+0xA8,参照 COMP 0x187d350/0x187d360 与 nation 0x1888a50/0x1888a60)
- 直线型判据(COMP 样例):reader 主体为固定指令序列,`mov r8d,N`(41 b8 N..)宽度即时数直线排列,无 inc/cmp/jl 计数循环
- 变长型判据(nation 样例):param 分支 + 计数驱动循环(`fe c3` inc bl / `3a 5c 24 44` cmp / `7c cc` jl 等 inc/cmp/jcc 模式)或 2B/4B count + 循环体重复读
- t01g 产物:`scratch/t01/inbox/t01g/output.json`(nation 全链 + 判据);t01f 产物:`scratch/t01/inbox/t01f/output.json`(COMP 全链)
- 32 实体清单与码表:`evidence/fm24/reports/editor_schema/master.json`(entities/entity_summary);t01e 虚表映射 12/32:`scratch/t01/t01e_vtables.json`

## 任务

对工厂跳表的**每一项**(从基址 `0xf49d38` 起逐项枚举 rel32,直到跳表结束——先确定项数,可能是 32 或接近):
1. 解析 handler VA → alloc size(`mov ecx,N`)→ 构造器 → RTTI 名(`.?AV...`)→ vptr → type-id 查询函数返回值
2. 定位 slot19 reader 入口(vtable +0x98)
3. **分类**:读 reader 入口后 ~0x800 字节,按上述判据分类:`straight-line` / `count-loop` / `mixed(前缀直线+后续循环)` / `unclear(给出现状)`
4. 与 t01e 的 12/32 虚表映射交叉核对(一致则标 cross-checked,不一致逐字节裁决)
5. 与 master.json 的实体语义对齐(RTTI 名 → entity),与旧库 TABLE_HINTS(table 8/10/21/25/41/56)对齐已知项

## 验收判据

- 跳表项数 + 每项 {type_id, handler, alloc, ctor, rtti, entity, reader, mode} 全清单(L3,逐项字节证据);
- 分类一致性:comp=straight-line、nation=count-loop 必须复现(负对照);
- 跳表项数与 master.json 实体数的关系要说清(缺谁、多谁)。

## 交付

`scratch/t01/inbox/t01h/`:`output.json`(census 数组 + summary)、`REPORT.md` ≤100 行、`verify.py --selftest`(含 comp/nation 负对照)。

## 纪律

深度优先;每实体判据看 ~0x800 字节即够,不追全函数;unclear 允许但要给字节现状;勿改既有账本。
