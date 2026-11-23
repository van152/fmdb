# t02-g:nati 变长行框架(交给 logfare,1M 上下文)

## 使命

FM24 `.dat` 语义解析:恢复 nati(type 10)行框架。**只读输入,不启动游戏本体/FM 编辑器(IDA 静态分析允许),不 pip install,`py -V:3.12 -I -B`。**

## 背景(t01-g E21 已验收的负结果,别重新发现)

- `client_db/table_10.dat`:251 行,payload 0x609c,SHA `7e9d740b9ee6`。
- nation 序列化 **不是直线型**:存在计数驱动集合循环(变长记录),直线累加法不适用。
- 已复现锚点:payload `0x1046 = 6e 00 00 00 6e 00 00 00`(=472446402670,duni 类锚点)。
- 7 个前缀字段已知(Ngct@0/Ncti@1/Nrgi@5/Ncur@13/Nsod@17/Necf@18/Nygn@23),但**行边界未恢复**。

## 任务

1. **第一步(必做)**:创建 `OUTDIR/framework.json` 骨架 `{"type_id":10,"entity":"nati","status":"in_progress"}`,拿到结果就重写。
2. 恢复 nation 的**行长度公式**:分析计数驱动循环的结构(计数在哪、每项宽度、有几段集合),给出能走查全部 251 行的行边界算法。
3. **closure 必须成立**:`14 + sum(row_len) + 8 == payload_len`,全部 251 行精确封口。
4. 验证身份块惯例(行末 12B ordinal|ID|重复ID)是否成立。
5. 若走不通,给出明确的负结果 + 卡点 file offset + 已排除的假设(负结果同样验收)。

## 只写这些文件

只在 `OUTDIR/` 下写 `framework.json` + `REPORT.md`。不改目录外任何文件。做完打印 `DONE type=10 ...`。
