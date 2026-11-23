# t02-p:BASIC_PERSON 宽度选择器 W 静态溯源(交给 sol,最强模型,一次性投入)

## 使命

FM24 `.dat` 语义解析:把 schema 字段映射到行内偏移。**只读输入,不启动游戏本体/FM 编辑器(IDA 静态分析允许),不 pip install,`py -V:3.12 -I -B`。**

## 背景(t01-k 已验收的卡点,别重新发现)

这是全项目最大、最高价值的未解卡点:person 家族 271 字段。

- `basic_people_db.dat` = 直接单帧 Zstd(file+8 起),payload 54,060,043B,count=658,011,5 类变长行(1/2/3=83B、4=34B、5=22B),全量封口已通过(t01-j E25)。
- **唯一卡点**:BASIC_PERSON slot-19 reader(`editor.exe` off `0xe4f370`)读 class-4 时,两个 2B 字段的行偏移依赖前置宽度 W:
  - `W=4` → `row+6`/`row+8`
  - `W=8` → `row+10`/`row+12`
  - W 由两处全局状态字节决定:`0xe4f4d5: 80 3d 77 04 d1 00 00` 与 `0xe4f4ed: 80 3d 38 fd d0 00 00`;随后 `0xe4f4f6: 41 b8 08...` 或 `0xe4f4fe: 41 b8 04...` 二选一,`0xe4f4eb: 74 11`/`0xe4f4f4: 75 08` 分流(互斥,不相加)。
- t01-k 因"不运行程序取运行时值"(L4=0)停在 1 个固定字段(Ptyp@row+1)。**本任务允许并鼓励静态溯源**:找出这两个全局字节在 editor.exe 里何时被写、写什么值;或从 PDB/RTTI/初始化路径证明其默认值。

## 任务(按价值排序,先落盘再深入)

1. **第一步(必做)**:创建 `OUTDIR/output.json` 骨架:
   `{"type_id":1,"entity":"pers","status":"in_progress","selector_resolution":null,"row_offset_map":[],"unclosed":[]}`
   每拿到一个结果就重写。
2. **静态溯源选择器**:对 `0xe4f4d5`/`0xe4f4ed` 的 `cmp byte [rip+disp],0` 算出目标 VA(注意 rip-relative),在 editor.exe 全文件找对该地址的 `mov byte ptr [...]` 写入点,追踪初始化值。若能证明 W 恒定(比如恒 4 或恒 8),直接锁定 class-4 两个 2B 字段的行偏移。
3. **数据侧反推(辅助证据)**:用已知的 658,011 行字节,对 class-4 的 9,839 行统计 `row+2..5`/`+6..9`/`+10..13` 三个候选跨度,看哪个位置的字节模式全量自洽(如 Pdob 日期范围、Ptyp 值域)。这是 L1 数据证据,与 L3 静态证据交叉。
4. **闭合 helper 游标**:`0xe4f5a3: e8 f8 2b 16 00` → `0xfb21a0: e9 5b 6b e2 02`(jmp 进 .reloc 明文区),按 E20 的 helperB 解析法(rip-relative 重算)追下去,看能否闭合剩余 5 个字段(PCJO/PSJO/PNJO/Piap 等)。
5. **目标**:达到 ≥10 个固定行偏移字段(阶段验收线),或诚实给出"W 确为运行时依赖、静态不可解"的负结果 + 完整证据链(负结果同样有价值,必须保留)。

## 参考文件

- `scratch/t01/inbox/t01k/REPORT.md` + `output.json`(卡点全细节,getter 10 条链)。
- `scratch/t01/inbox/t01j/REPORT.md`(行框架全量封口)。
- `scratch/t01/inbox/t01h/output.json` 里 type_id==1 项(ctor/RTTI/slot19)。
- 勘误:E20 证明 helperB 非墙(jmp 目标在 .reloc 明文);VA=fileoff+0xA00(.rdata)或 off+0x16B600(.reloc)。

## 硬约束

- 只读外部数据;L4=0(不做真机加载;L3 静态分析允许);每 claim 带 file offset + 字节;负结果保留。
- 只写 `OUTDIR/`。

## 交付

`OUTDIR/output.json` + `OUTDIR/REPORT.md`。打印:W 是否静态可解 + 锁定字段数 + 关键 file offset。
