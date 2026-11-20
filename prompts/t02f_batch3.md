# t02-f:批量行框架 ×3(交给 devseek,断流可重跑)

## 使命

FM24 `.dat` 语义解析:恢复行框架。**只读输入,不启动游戏/编辑器/IDA,不 pip install,`py -V:3.12 -I -B`。**

## 铁律:先落盘

对每张表,第一步就写 `OUTDIR/fw<TID>.json` 骨架 `{"type_id":TID,"status":"in_progress"}`,拿到结果就重写。**上游 2-14 分钟会断流,没落盘=白费。**

## 本次三张表(都是 client_db.dat 里的未解表)

按此顺序做,做完一张立刻落盘再做下一张:

| TID | 说明 | census 模式 |
|---|---|---|
| 7 | client 表,类型 mdso | count-loop |
| 9 | client 表,国家队容器(NATIONAL_TEAM_CONTAINER,E23 裁决) | mixed |
| 22 | client 表,实体未匹配 | straight-line |

## 每张表的任务(只求框架,不求字段)

1. 从 `client_db.dat` 解出 `table_<TID>.dat` 成员:头 `03 01 74 61 64 2e f1 0d`,count @ payload+8(u32le)。
2. 恢复行起、stride(定长)或变长行长度公式。
3. **closure 必须成立**:`14 + count*stride + 8 == payload_len`(变长则 `14 + sum(row_len) + 8 == payload_len`),走查全部行精确封口。
4. 身份块:行末 12B 常为 `ordinal|ID|重复ID`——抽样验证是否成立。
5. 写 `fw<TID>.json`,字段:type_id/status/count/stride或variable/row_shape/closure/member/payload_len。完成后 status="complete"。

## 只写这些文件

只在 `OUTDIR/` 下写 `fw7.json`/`fw9.json`/`fw22.json` + `REPORT.md`。不改目录外任何文件。做完打印三行 `DONE type=N ...`。
