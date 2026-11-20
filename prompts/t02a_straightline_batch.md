# t02-a 任务书:straight-line 小实体批量字段映射(8 实体)

> 交给 pi devseek(deepseek-v4.1-flash-free)。方法论已四场景验证,本任务是纯执行:**8 个 straight-line 实体,`--thinking max`,一次扫干净**。
> 规则:只读输入、不启动游戏/编辑器/IDA、不 pip install、Python `py -V:3.12 -I -B`、每个 claim 带 file offset + 字节证据。

## 方法论(照抄,勿重新发明)

完整模板读这两份,它们是同一套方法的成功样本:
1. `scratch/t01/inbox/t01l/REPORT.md` —— weat/table_27,89 字段。行框架(变长名)+ 固定四季循环 + 4CC 范围跳表
2. `scratch/t01/inbox/t01m/REPORT.md` —— stad/table_21,16 字段。server/client 双行宽 + 旧库 L1 双源互证

核心五步:
1. **行框架**:解压 client_db.dat(或 server_db.dat)中 `table_<ID>.dat` 成员(payload 头 `03 01 74 61 64 2e f1 0d`);恢复 count、行起、stride 或变长公式;**总量必须封口**(行字节 + 9B 尾 == payload 长度)
2. **reader 宽度累加**:从工厂跳表拿 reader 入口,沿 `mov r8d,N` 宽度指令 + `lea reg,[rbx+disp]` 目的地址,按指令顺序累加 → 行偏移。**区分字面直线 vs 固定次数循环**(循环无害,只要次数确定)
3. **4CC 对齐**:定位该实体的 getter 窗口,扫**全寄存器** `cmp r32,imm32`(81 f8..ff)+ `3d`(EAX);4CC 以**小端**写成 imm32(如 `Scti` → `69 74 63 53`)。getter 里的对象成员访问 `[rbx+disp]` 与 reader 的目的地址对齐
4. **抽验**:5+ 行逐字节对照原始 payload
5. **身份块**:行末 12B 通常是 `u32 ordinal | u32 ID | 重复 u32 ID`(已在 comp/nation/basic_people/weather/stadium 五张表证实);若成立就记录,不成立如实说

## 本批 8 个实体(census 已确认 straight-line,建议按此顺序,从易到难)

| type | 实体标签 | 字段数 | 说明 |
|---:|---|---:|---|
| 19 | regi | 6 | 最小,先热身 |
| 41 | curr | 7 | 小 |
| 23 | stgn(阶段名) | 8 | 小 |
| 8 | lang | 12 | 小 |
| 2 | city | 15 | **高价值**,旧库有 table_2 锚(56,293 行;`rdui@+30`=行序号,**E20 勘误:该处是行序号非 rdui**) |
| 18 | drbr(德比) | 22 | 中 |
| 24 | team | 25 | 中 |
| 6 | inju(伤病) | 27 | 中 |

**每张表独立成节**,不要混。若某张表 20 分钟内无进展,记录现状(哪一步卡住、已拿到什么字节)跳到下一张——**宁可 6 张完整,不要 8 张半成品**。

## 已知输入

- 工厂跳表基址 `0xf49d38`,编码 `target = base + rel32`(小端);type-id → handler。74 项全 census 在 `scratch/t01/inbox/t01h/output.json`(每项含 handler/allocation/constructor_classes/reader/slot19 入口)
- archive:client 20 表、server 59 表(全 ID 列表在 `scratch/t01/inbox/t01i/output.json`)
- 码表:`evidence/fm24/reports/editor_schema/master.json`(entity_summary 有每实体码表)
- 旧库 L1 参考:`evidence/fm24/reports/dbdat_decode/DB_TABLES_BIG.md`(只引 `evidence/fm24/` 快照,勿改)
- 已证伪,勿重做:行偏移不在描述符槽(E20);`rdui@+114/+30` 是行序号(E20);switch/getter 区是实体特异的(E21);getter 比较寄存器不唯一(E26)

## 验收判据(本批总判据)

- **至少 6 个实体**各给出 ≥5 个字段的行内偏移 L3(带 getter cmp + reader 目的/宽度/流调用三元组字节证据)+ ≥3 行抽验 + 行框架封口
- 每实体单独报告:行框架(count/行起/stride)、字段表、身份块是否成立
- 负结果可接受,但必须给出卡在哪一步 + 已获取的字节

## 交付

`scratch/t02/inbox/a/`:
- `output.json` —— 按 type-id 分键,每实体含 `{row_framework, row_offset_map, identity_block, samples, unclosed}`
- `REPORT.md` ≤200 行(每实体一节,≤20 行)
- `verify.py --selftest` —— 只读,重跑行框架封口 + 抽验 + 静态字节;含负对照

## 纪律

- **不要修改任何已有文件**(账本、晨报、t01 产物一律不动)
- 深度优先;每实体 20 分钟上限;候选不写成结论;未证实的填 `unclosed`
- 完成后打印:每个实体拿到几个字段、卡在哪的清单
