# t03 通用字段映射器 — 交付与回归

## 结论

脚本与逐字段证据已落盘，但**验收未达标**：独立复跑应有 2/7 夹具 ≥80%，低于要求的 5/7；`--selfcheck` 因此返回 **1**。不将候选或未闭合游标写成成功。

| 夹具 | 模式 | 候选字段/夹具字段 | 偏移吻合 | 说明 |
|---|---|---:|---:|---|
| t01f COMP | straight-line | 3/26 | 3/26 (11.5%) | 可靠闭合 `levl@15`、`Ccre@17`、`CTty@18`；其后 reader 分支/辅助读取使游标不闭合 |
| t01l WEAT | straight-line | 0/89 | 0/89 (0%) | 周期字段重复访问同一对象成员，helper/循环布局未闭合；保留负结果 |
| t01m STAD | straight-line | 12/18 | 12/18 (66.7%) | 12 个吻合；6 个字段需解析 reader 条件臂/成员复用 |
| t01g NATION | count-loop | 7/7 | 7/7 (100%) | 仅首轮最早传输位置；不是循环边界/全循环公式的闭合 |
| t02p PERSON | straight-line | 1/15 | 0/15 (0%) | `Ptyp` 候选为 reader-relative +0，行帧偏移未闭合；其余 4/8B 分支未解决 |
| t02g2 NATION | count-loop | 7/7 | 7/7 (100%) | 与 t01g 同一 type 10，使用相同首轮前缀口径 |
| t02c CLUB | mixed | 0/11 | 0/11 (0%) | 双 reader、混合模式；夹具字段为语义描述，未伪造 4CC 对齐 |

平均逐字段吻合率 **39.74%**；达到 80% 的夹具 **2/7**。通过的仅是 `count-loop` 夹具的首轮前缀口径；`straight-line` 与 `mixed` 未通过。两个 NATION 夹具是同一 type_id 的重复回归，不能视为两个独立实体成果。

## 实现与证据边界

- 只读 `editor.exe`（SHA-256 `b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4`）、t01h census 与本地 fixtures；无安装依赖、游戏/Editor/IDA 启动或外部写入。脚本依赖已装 Capstone 5.0.7。
- reader 从 census `entry_file_offset` 开始，沿直接 `jmp` 与有限层 `call` 追踪高密度流传输主体。COMP 链实证：`editor.exe+0xed0a40: e9 8b 92 dd 02` → 中间环 `+0x3b3f0d0`；`+0x3b3f101: e8 fa d2 20 fd` → 主体 `+0xeb7000`。字节链、主体偏移、宽度/传输点都在 JSON 中保留。
- 用 `mov r8d,N` 配对 `call [rax+0x28]`，并识别带宽度的 `call rax`；前向 CFG 合并分支游标。能闭合的直接 helper 宽度纳入游标；含未闭合 helper 的后续游标标记 unknown，不继续猜。计数循环不展开，只报告首轮候选；循环边界公式仍未实现。
- 从构造器 RTTI 的 vtable slot 2 扫 4CC 比较和等值路径成员读，按 reader 写入相同成员 displacement 对齐。例：COMP `levl` getter 比较 `+0xec1781: 81 fe 6c 76 65 6c`，成员读取 `+0xec4672: 41 0f be b4 24 a2 01 00 00`；reader 宽度 `+0xeb70ab: 41 b8 01 00 00 00`、成员目的 `+0xeb70a1: 4c 8d bb a2 01 00 00`、传输 `+0xeb70b7: ff 50 28`，闭合为 row+15。STAD `Scpy` 的比较/成员读取与 reader 宽度/传输也逐条保存在 `fixtures_result.json`。
- NATION 首轮示例：`+0x10405be: 41 b8 01 00 00 00` → `+0x10405c7: ff 50 28`，同一传输的 cursor 候选为 `[0,58,70,83,95]`；脚本仅取首轮最早位置 0，并在字段证据中标注 `earliest-first-iteration-prefix`。其余循环位置保留，不能据此声称已解出循环计数或全布局。

## 复跑

```powershell
py -V:3.12 -I -B scratch/t02/field_mapper/out/field_mapper.py --help
py -V:3.12 -I -B scratch/t02/field_mapper/out/field_mapper.py --selfcheck
```

`--selfcheck` 重建 `fixtures_result.json` 并打印 7 项比对；当前预期退出码 **1**（未达到 5/7）。JSON 中逐字段记录 expected/actual、缺失/错配、reader body、thunk/call-hop、4CC 比较、宽度指令和传输字节证据。