# t02-g2:nati 变长行边界恢复(转派 luna;logfare 限流失败后接手)

## 使命

FM24 `.dat` 语义解析:恢复 nati(type 10)行框架/行边界。**只读输入,不启动游戏本体/FM 编辑器(IDA 静态分析允许),不 pip install,`py -V:3.12 -I -B`。**

## 背景(别重新发现)

- logfare 渠道 5 次全部限流失败,但已把解压好的 payload 落盘,直接用:
  - `scratch/t02/inbox/nati/client_db_t10.bin`(24,732B,count=251,SHA `7e9d740b9ee6`,头 `03 01 74 61 64 2e f1 0d`)
  - `scratch/t02/inbox/nati/server_db_t10.bin`(422,345B,SHA `19337841e40d`)
  - 两个 bin 从 payload+0 起就是数据(含 14B 头:magic 7B + count u32 @+8 + 3B),**行数据从 offset 14 开始**。先读 logfare 留下的 `explore*.py`/`extract.py` 看它怎么解的。
- t01-g(E21)已验收:client table_10 = 251 行、payload 0x609c=24732、nation 是**计数驱动集合循环变长型**(直线累加法不适用),7 个前缀字段(Ngct@0/Ncti@1/Nrgi@5/Ncur@13/Nsod@17/Necf@18/Nygn@23,宽度序列 1,4,4,4,4,1,1,4,1,1)、duni 锚点 `payload+0x1046 = 6e 00 00 00 6e 00 00 00`。
- 你之前做 weat(E27)成功恢复过"固定 4 季循环"的变长行;nation 的计数循环比它复杂(有变长集合),但方法论相通:找循环计数、每项宽度、段数。

## 任务(先落盘再深入)

1. **第一步(必做)**:在 OUTBOX 创建 `framework.json` 骨架 `{"type_id":10,"entity":"nati","status":"in_progress"}`,每拿到结果就重写。
2. **恢复行长度公式**:分析 nation 行的计数循环结构——哪些段是计数驱动的集合、计数在哪、每项宽度、如何判定一段结束。给出能走查全部 251 行的行边界算法。
3. **closure 必须成立**:`14 + sum(row_len) + 8 == 24732`,全部 251 行精确封口(footer 8B)。
4. 验证身份块(行末 12B ordinal|ID|重复ID)是否成立;对照 duni 锚点 0x1046。
5. 若能恢复行边界,追加 ≥5 个字段行偏移;若走不通,给明确负结果 + 卡点 offset + 已排除假设(负结果同样验收,不要编造)。

## 方法论

- `scratch/t01/inbox/t01g/REPORT.md`(nation 已知前缀与负结果)、`scratch/t01/inbox/t01l/REPORT.md`(weat 循环行成功范式)。
- 勘误:rdui@+114/+30 是行序号非字段;4CC 比较寄存器不唯一(全寄存器 81 f8..ff)。

## 硬约束

只读;claim 带 file offset + 字节;负结果保留;候选不写成结论;只写 OUTBOX。

## 交付

`OUTBOX/framework.json` + `OUTBOX/REPORT.md`。打印:行边界算法是否恢复 + 251 行是否封口 + 字段数 + 卡在哪。
