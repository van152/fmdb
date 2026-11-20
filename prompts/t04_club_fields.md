# t04:club 字段级 L3 映射(半自动,交给 luna)

## 使命

FM24 `.dat` 的 club 表(type 3,433 字段)做字段级行偏移映射。**只读输入,不启动游戏/编辑器/IDA,不 pip install,`py -V:3.12 -I -B`。**

## 这是全库最大空位

club 有 433 个 schema 字段,当前 L3=0。攻下它是全解析覆盖率的最大单笔跃升。

## 已有底稿(别从零开始,直接用)

1. **行框架已解**:`scratch/t02/inbox/club_v2/output.json` —— 84,259 行全封口,每行结构已明(4B db_id + 4B parent + 8B 重复 + 变长 id-block + group + flag + u32len名 + u32len短名 + 3B + 12B身份 + 1B)。
2. **传输点半自动底稿**:`scratch/t02/field_mapper/club_substrate.json` —— field_mapper 脚本扫出的 **74 个 transfer_events**,每个含 file offset + 宽度 + 行偏移候选。前 5 个事件 row=[0,4,8,12,16] 已确证(db_id/parent/ref/ref/id-block),之后游标分裂为多候选(如 [0,20]、[0,1,20,21]),这些是你要消歧的。
3. **完整候选证据**:`scratch/t02/field_mapper/out/fixtures_result.json` 里 source=t02c 的 analysis(74 事件全字节)。

## 任务(先落盘,边做边存)

1. **第一步**:创建 `OUTBOX/output.json` 骨架 `{"type_id":3,"entity":"club","status":"in_progress","row_offset_map":[],"unclosed":[]}`,每解一个字段就重写。
2. **reader 定位**:club slot19 reader `0xe5a7a0`(census),但注意可能有多读主体(mixed 模式,两个 RTTI:CLUB / LEAGUE_BODY_CLUB)。getters 从 COMP 同款 vtable slot2 扫 `cmp r32,imm32`(全寄存器 81 f8..ff,4CC 小端)。
3. **逐段消歧**:用底稿的 74 事件 + club 84,259 行真实字节,逐段确定每个传输的行偏移。分支游标多候选时,用真实行字节 + 身份块位置反推哪个候选正确(参考 t01f/t01m 的数据抽验法)。
4. **4CC 对齐**:getter 的 `[rbx+disp]` 成员偏移 ↔ reader 写同一 disp 的传输点 → 字段命名。目标 ≥30 个 L3 字段(如果 433 字段里能稳定映射的就这么多个,诚实报告实际上限)。
5. 未闭合的放 `unclosed`,不猜。

## 方法论

- `scratch/t01/inbox/t01f/REPORT.md`(comp 18 字段,直线型宽度累加范式)。
- `scratch/t01/inbox/t01m/REPORT.md`(stad 16 字段,server/client 双源互证)。
- 勘误:rdui@+114/+30 是行序号;4CC 比较寄存器不唯一;identity 块惯例(行末 ordinal|ID|重复ID)。
- 数据抽验:club client_db.dat table_3 可从 `scratch/t02/inbox/club_v2/` 的脚本解出原始行字节。

## 硬约束

只读;claim 带 file offset + 字节;负结果保留;候选不写成结论;只写 OUTBOX。

## 交付

`OUTBOX/output.json` + `OUTBOX/REPORT.md`。打印:L3 字段数 + 逐字段 row 偏移 + 卡在哪一段。
