# b51 — `summary.dat` 字段语义调查

目标：在 v4 已确定的 editor database-summary 身份/布局上，拆出记录字段并尝试定语义。结论是**原始字段位置可复现，字段语义仍未解**；本轮没有把“数值看起来像年份/DBID”升级成命名字段。机读映射与字节 profile：`reports/dbdat_decode/summary_field_map.json`；脚本：`scripts/b51_summary_fields.py`。

## 证据口径与结论

- **L1**：读取 db 2430 `summary.dat`（1,648,018 B，SHA-256 `966eea20bf8d261c08c78e8783eeee400b3c18c594bc952b26d4f2d2ccf87d94`）；头、分段字节总账、分隔符与标准体字段宽度均复核。
- **L3**：对只读 `input/editor.exe` 的静态 IDALIB 分析证明 `database_summary.cpp` 写侧及其调用关系；函数地址/来源见 §L3。L3 只说明静态写路径，不等于运行时验证，也不等于字段的业务语义。
- **L2：0 个字段命名**。已知 ID、俱乐部/联赛候选值和 `pl_hist` ID 集的交叉未形成唯一关系；没有独立史料支撑 b0…b5/u16 的含义。旧版三个假设（表行数汇总、schema 罗塞塔、与存档 summary 同族）已在 `DBDAT_FORMAT.md` v4 证伪。
- **L4：0**，没有启动 Editor/Game。

因此，验收走“穷尽负结果”分支：可复现的字段槽位逐一列出；所有字段均命名为 `raw/unresolved`，不伪称 ≥5 个 L2 语义字段。

## 候选 17-byte body 字段表

下表 offset 均相对观察到的 `ff ff ff ff 03` 分隔符之后、候选 body 的第一个字节；不是文件固定绝对偏移。标准体只指 **恰为 17 B 的 53,742 个 body**。证据等级是槽位/宽度（L1），不是语义名称的证据等级。

| body offset | 宽度 | 机读名 | 观测/语义 | 等级 |
|---:|---:|---|---|---|
| 0 | 4 | `record_id_raw_u32le` | 53,742 个互异值，57–2,000,339,170；与 pl_hist ID 的重叠不足以 join；实体/主键含义未定 | L1 槽位；L2 未解 |
| 4 | 1 | `payload_b0_raw_u8` | 6 个值，主要 1/2/3；未定 | L1；L2 未解 |
| 5 | 1 | `payload_b1_raw_u8` | 4–7；4 占 50,559/53,742；未定 | L1；L2 未解 |
| 6 | 1 | `payload_b2_raw_u8` | 1–56，宽离散值域；未定 | L1；L2 未解 |
| 7 | 1 | `payload_b3_raw_u8` | 11–19；与 b4 强相关，看似年序号但没有独立锚点，**不命名为年份** | L1；L2 未解 |
| 8 | 1 | `payload_b4_raw_u8` | 11–20；常等于 b3 或 b3+1；未定 | L1；L2 未解 |
| 9 | 1 | `payload_b5_raw_u8` | 1–6；未定 | L1；L2 未解 |
| 10 | 2 | `payload_u16_6_raw` | LE u16，0–32,767；常见 212/32767/28672/32704/346/1057/518；未定 | L1；L2 未解 |
| 12 | 2 | `payload_u16_8_raw` | LE u16，0–32,767；常见 32767/1057/28672/32704/346；未定 | L1；L2 未解 |
| 14 | 2 | `payload_u16_10_raw` | LE u16，0–32,767；常见 32767/0/1057/28672/32704/346；未定 | L1；L2 未解 |
| 16 | 1 | `payload_b12_raw_u8` | 53,742/53,742 为 0；恒定值不等于已知语义 | L1；L2 未解 |

上述为 11 个可指认的**原始槽位**，L2 命名数为 0。`summary_field_map.json` 有每槽 unique/min/max/top-frequency profile。

## 变长 body、前置段、收尾段

- 记录体候选边界：`0x49`（73）；观测分隔字节 `ff ff ff ff 03` 共 54,087 次，对应 54,086 个 body。全文件字节总账精确覆盖 1,648,018 B（L1）。
- body 长度恰为 17 B：53,742 个；其他长度：344 个，长度分布完整列在机读映射。以 8 个零字节 + `count@+25` + `base@+29` + `<A,B>` pairs 的判据找到 **117 个 extended candidate**；`count` 与可读 pair 数量/链式尾部仍不能统一解释。其余 227 个非 17B body 和 extended 尾部维持 raw/unresolved，不填造字段意义。
- 可读候选扩展体相对 body：`+17..+24` 8×00；`u32@+25`（count-like）；`u32@+29`（103,000–110,000 的 base ordinal 候选）；`<u32 A,u32 B>` 从 `+33` 起、stride 8。A/B 都未映射到可验证实体键；B 虽升序，A 有 `-1` 与 12,040,2xx 块的形态，但仍只是 L1 分布。
- block2（offset 40、33 B）：u32 `[251,3,1280,156928,256]` + 13B 碎片，语义未解。
- 收尾段从 offset 1,637,014 起，11,004 B：40B head（250、82,082,540、余下 raw）；两条升序 u32 ID 列表（2,486 / 126）；63 组 `(u32 0..64,float32)`，末尾 -1。它们的业务语义均未定。逐字段位置/宽度见 JSON。
- 字节模式分隔符与上述解析描述的是当前 v4 候选语法；L1 字节总账本身不能证明任何相同字节模式都一定是逻辑 record 边界。因此，本报告只把标准 body 槽称为“候选结构”，不将 ID/byte slot 当成实体字段。

## L2 交叉与证伪结果

- 记录 ID 与 pl_hist ID 集：54,039 个 distinct IDs 中仅 403 个重叠；量级/重叠不足以做人物 join。
- 扩展 A 与一组 table_3 repeated-u32 候选：仅 55/1,379 弱重叠；其它已测 A/B 候选与 verified duni/DBID 集为负。不能命名为 club/person DBID。
- 试读 11 个标准槽的全量分布：b3/b4 有连续小值、三个 u16 有大量 `0x7fff/0x7000/0x7fc0` 一类值；这些都不构成俱乐部/联赛/赛季的独立锚点。没有把“疑似年份/枚举/年龄统计”写成字段语义。
- 机读结果的 `l2_cross_checks` 保留了先前交叉的计数和边界；当前结论不是“字段已验证”，而是“尝试后未建立独立语义 join”。

## L3 写侧函数证据路径

来源为本机 `input/editor.exe`（24.4.2，PE hash 登记于 `reports/qa/IDA_PROVENANCE.md`），从原始 PE 建临时 IDALIB 聚焦库；`ida/editor.i64` 和 `editor_merge_v2.i64` 未打开/未修改。

1. 源文件路径字串 `..\\..\\code\\database_summary.cpp`；写入函数 `sub_140FF3840`（VA `0x140ff3840..0x140ff3fd9`）现场拼 stem `summary`，打开 `tag='NULL'`, version 3569 的 tad wrapper；并写一个 count+u32 ID vector。
2. 调用链锚：`sub_140035F10`（`0x140035f10..0x140036ec2`）在 `0x140036b0b` 调用写入函数；`sub_14004AF40`（`0x14004af40..0x14004df5b`）关联 `Creating database summary for … people kept for …` 日志。
3. `sub_140FF3840` 的对象序列化路径读取源对象 `+4,+144,+136,+128,+148,+152`，并把 `+80,+32,+56,+104` 交给辅助序列化器；`sub_140FF4420`（`0x140ff4420..0x140ff47a1`）确认 `+80` 是 counted-vector writer。它们证明写入源路径存在，但没有把这些内存成员逐字节对到每个 17B candidate-body offset，也没有给出 schema 级字段名称。
4. 写侧质检分支：对象 `dword@+4 == 771` 且 `dword@+144 > 0` 时发出 `Germany should not be manageable`。这是**内存对象检查**的 L3 证据；不能把 +4/+144 直接说成文件 payload 的某两个具名字段。

**L3 止步点：**函数链已追到 summary 对象 writer、调用者及一个 nested vector writer；缺少类型信息/独立对象语义锚点，无法诚实地把 raw field slots 命名为统计量。函数证据支持“有专用 database-summary writer”，不支持虚构字段表。

## 自检与重跑

```powershell
py -V:3.12 -I scripts/b51_summary_fields.py --help
py -V:3.12 -I scripts/b51_summary_fields.py --selftest --json
py -V:3.12 -I scripts/b51_summary_fields.py --analyze --json
py -V:3.12 -I scripts/b51_summary_fields.py --analyze --output reports/dbdat_decode/summary_field_map.json
```

退出码：0 结构检查通过（不等于语义验证），1 数据不满足检查，2 用法/输入/致命错误。
