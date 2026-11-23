# t02-c:club 变体段续解(交给 luna,稳定长任务)

## 使命

FM24 `.dat` 语义解析:把 schema 字段映射到行内偏移。**只读输入,不启动游戏本体/FM 编辑器(IDA 静态分析允许),不 pip install,`py -V:3.12 -I -B`。**

## 背景(已验收事实,别重新发现)

- `client_db/table_3.dat`:count=84,259,payload_len=6,932,082,变长行。
- **前 69,705 行已逐行验证通过**(ordinal==row_index、dup-ID 相等、边界标记 0x00 全过),解析器 `scripts/t02_club.py --selftest` 通过。
- 卡点:**第 69,705 行起出现字段宽度变体**——第 5 个字段(身份块前的 id block)在主分支是 5B(u32+尾 00),在第二类 `LEAGUE_BODY_CLUB` 分支是 4B。约 14,554 行未解。
- 已有部分结论在 `scratch/t02/club_partial.json`,先读它。

## 任务(按优先级,先落盘再深入)

1. **第一步(必做)**:创建 `OUTDIR/output.json` 骨架:
   `{"type_id":3,"entity":"club","status":"in_progress","variants":[],"row_offset_map":[],"unclosed":[]}`
   之后每拿到一个结果就重写一次(断流不白费)。
2. **恢复变体规则**:确定第 5 字段 5B vs 4B 的判定条件(是 class byte?某个 flag?字典序?)。用两类各 3 行原字节举证(file offset + hex)。
3. **续走查 69,705→84,259 行**:把 `scripts/t02_club.py` 的解析器扩展到变体段,目标是全 84,259 行封口精确(payload 余 8B footer)。记录每行跨度分布。
4. **字段级映射**:从 editor.exe 找 `db::CLUB` slot19 reader(`scratch/t01/inbox/t01h/output.json` 里 type_id==3 项),做宽度累加;把 4CC getter(`cmp r32,imm32`,全寄存器 81 f8..ff)对齐到 reader 目的地址。目标 ≥10 个固定行偏移字段。
5. 未闭合的诚实放进 `unclosed`,不猜。

## 方法论(照抄,勿重新发明)

- `scratch/t02/inbox/t01m/REPORT.md`(stad 范式)、`scratch/t02/inbox/t01l/REPORT.md`(weat 范式)。
- 身份块惯例:行末 12B = `ordinal(u32)|ID(u32)|重复ID(u32)`,已 8 张表验证。
- 勘误(勿踩):`rdui@+114/+30` 是行序号非字段;4CC 比较寄存器不唯一(EDX/ESI 都有);循环只要分支确定就无害。

## 硬约束

- 只读:`D:/tmp2b/fm24`、`Z:/SteamLibrary/...`、editor.exe 只读。
- 每 claim 带 file offset + 字节证据;候选不写成结论;负结果保留原文。
- 只写 `OUTDIR/`,不改目录外任何文件。

## 交付

`OUTDIR/output.json` + `OUTDIR/REPORT.md`。打印:变体规则一行 + 已走查行数 + 字段数 + 卡在哪。
