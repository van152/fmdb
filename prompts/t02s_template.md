# t02-s:单实体快速扫描任务(模板)

> 交给 pi devseek。**极小任务**:一张表,一个交付文件,**最先写 output.json**。
> 规则:只读输入、不启动游戏本体/FM 编辑器(IDA 静态分析允许)、不 pip install、Python `py -V:3.12 -I -B`、每个 claim 带 file offset + 字节证据。

## 铁律(先读,这条最重要)

**先写骨架,再填内容,边做边存。** 按此顺序:

1. **第一步(必须最先做)**:立刻创建 `OUTDIR/output.json`,内容是骨架:
   ```json
   {"type_id": TID, "entity": "TAG", "status": "in_progress", "row_framework": null, "row_offset_map": [], "samples": [], "unclosed": []}
   ```
   并写 `OUTDIR/REPORT.md` 一行摘要。
2. 每解出**一个字段**,立刻追加进 `row_offset_map` 并重写 `output.json`(不要攒)。
3. 每解出**行框架**,立刻填 `row_framework` 并重写。
4. 全部完成后把 `status` 改成 `"complete"` 或 `"partial"`。

**理由**:上一个任务因上游频繁断流(2-4 分钟一次)在写成果前被截断,17 个探索脚本全部白费。**只要有落盘,断流也能验收**。

## 少想多做

- 不要花时间做全局设计、不要写大型 helper 库、不要反复重扫。**直接奔向答案**
- 每步只跑一个小脚本,看结果,记下来,下一条
- 目标在 **15 分钟内交第一版**(哪怕只有 3 个字段),然后继续加深

## 方法论(照抄 t01l/t01m,勿重新发明)

- 模板:`scratch/t01/inbox/t01l/REPORT.md`(weat 89 字段)、`scratch/t01/inbox/t01m/REPORT.md`(stad 16 字段)
- census:`scratch/t01/inbox/t01h/output.json`(找 `type_id == TID` 的项:handler / allocation / constructor_classes / reader.slot19_readers[0].entry_file_offset)
- **行框架**:解压 archive 里 `table_<TID>.dat` 成员(头 `03 01 74 61 64 2e f1 0d`);count @+8;行起/stride 恢复;**总量必须封口**(行字节+9B 尾 == payload 长)
- **reader 宽度累加**:从 reader 入口沿 `mov r8d,N` + `lea reg,[rbx+disp]` 顺序累加 → 行偏移
- **4CC 对齐**:该实体 getter 窗口内扫全寄存器 `cmp r32,imm32`(81 f8..ff)+ `3d`;4CC 小端作 imm32(如 `Cnam` → `6d 61 6e 43`)。getter 的对象成员 `[rbx+disp]` 与 reader 目的地址对应
- **身份块**:行末 12B 常为 `ordinal|ID|重复ID`(5 张表已验证)
- 已证伪勿重做:行偏移不在描述符槽;`rdui@+114/+30` 是行序号;getter 寄存器不唯一

## 本任务参数

- **TID / 实体 / 字段数 / 输出目录**:见下方"本次任务"
- 码表(若有):`evidence/fm24/reports/editor_schema/master.json` 的 `entity_summary`
- 旧库参考:`evidence/fm24/reports/dbdat_decode/DB_TABLES_BIG.md`(只读引用)

## 验收判据

- ≥5 个字段的行内偏移 + 行框架封口 + ≥3 行抽验;字段少的表要求全字段
- 未闭合的放 `unclosed`,不猜

## 纪律

不改任何目录外文件;不做全局设计;边做边存。
