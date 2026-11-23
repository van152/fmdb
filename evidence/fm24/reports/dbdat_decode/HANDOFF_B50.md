# b50 server_db.dat 普查交接

## 结论

已完成 `server_db.dat` 的 77 项目录级普查：59 个数值表、18 个辅助项；其中 table_21 按 b47 范围排除，仅记录目录项 stub，未解压其 payload。其余 58 个数值表均有边界状态、槽位统计/线索、可用 schema inventory 和保守的业务命名结论。逐项结果见 [DB_SERVER_TABLES.md](DB_SERVER_TABLES.md)，机器可读索引见 [server_tables_census.json](server_tables_census.json)。

本次是**结构普查与有限字段命名**，不是对所有表完成 serializer/schema 解码。未知表保持未知；算术 stride、重复-u32 和字符串命中均未被单独提升为 schema 或加载验证。

## 主要产物

- `scripts/b50_serverdb_census.py`：目录 census、逐表分析、schema inventory、辅助项处理、table_extra_3 深分析、markdown/JSON 生成；支持 `--help`、`--selftest`、`--table N`、`--json`。
- `reports/dbdat_decode/DB_SERVER_TABLES.md`：77 项总览与逐项证据记录。
- `reports/dbdat_decode/server_tables_census.json`：同一 census 的结构化数据。
- `tmp_b50/PROGRESS.md`：阶段记录与验证/边界说明。

重生成示例（Python 3.12）：

```powershell
py -V:3.12 -I scripts/b50_serverdb_census.py --json
py -V:3.12 -I scripts/b50_serverdb_census.py --selftest
```

## 核心数字与实体映射

- 目录项：77（59 numeric + 18 auxiliary）；所有数值表头均为 `tad.` v3569。
- in-scope 数值表：58；其中 37 项符合 `14 + N×stride + 8` 的 L1 算术候选，18 项边界仍未解，2 项为空表，table_41 的变长行由现有解码器全量消费。stride 算术候选不等价于字段语义已证实。
- entity 映射：confirmed `[2 city, 3 club, 21 stadium (excluded), 24 team, 25 competition]`；candidate `[7 media_source, 8 language, 10 nation, 41 currency]`；其余数值表 unknown。不假设 server/client 表号对齐。
- L2 字段/实体值锚点涉及 table_2/3/7/8/24/41；严格区分“值语义锚点”和“schema 槽已映射”。例如 table_2 的坐标、table_7 publication 名称、table_8 language 名称及 table_41 currency 名称尚未全部对齐到具体字段槽。

## 重点结果与剩余限制

- **table_2 city**：43 B 固定行候选；row+1/+5 两个 f32 在全 56,293 行均落入合理纬度/经度范围，row+34 有重复-u32 唯一性；DUNI 5 对应 Ghent 坐标样例。仅将 `Clat/Clon` 记作坐标候选；DBID 1061/7618 未命中问题仍待解释，未解 city 名称序列化。
- **table_41 currency**：173 行、74,352 B 全量消费；结构为 4 个字符串槽、当前汇率、历史序列和 13 B 行尾。首字符串槽名称值有 L2 语义锚点，但 `dbnm/Cnam` 具体归属未证；历史率解析是 L1。
- **table_24 team**：仍无通用行边界；Team.Tsti→table_21 rdui 的知名俱乐部交叉有效，但不代表完整 Team serializer 已解。
- **table_extra_24**：`12 + 84,507×82` 精确，ordinal 全量连续；只有 +10/+11/+81 变化。穷尽当前可观察槽位，但未能为三处变化赋予可信业务语义。
- **table_extra_3**：84,259 个 ordinal 均与 row+20 模板锚点配对，得到 25..4,827 B 的 template-anchored variable-row **L1 candidate**；旧贪心 ordinal 扫描存在短跳反例。字段语义仍无可信命名，不能称独立验证。
- `table_for_old_save_23.dat` 与 `table_23.dat` SHA/字节完全相同；另有空表 52/57 payload 相同。其他未解辅助项和主表均在逐项报告中列出。

## 证据与安全边界

- 源 `server_db.dat` 来自只读游戏安装目录；本次仅读取文件，未启动游戏/编辑器，未 attach 进程，未写安装目录或用户 Documents。
- 本次结构分析是 **L1**（安装字节 + 工作区脚本）。个别已知名称/坐标/俱乐部关系有 **L2 样例锚点**；没有新增 L3 静态证据。**L4 全工作区仍为 0**，绝不声称产物已在游戏/编辑器加载。
- 回归所需大数据不在该 worktree；验证期间临时以只读 junction 引用主树输入，所有输出仍落在 b50 worktree；测试结束后删除 junction 并确认主树目标保留。生成的无关 QA/编码索引已还原。

## 验证与提交

- `py -V:3.12 -I scripts/b50_serverdb_census.py --selftest`：14/14 true。
- `py -V:3.12 -I scripts/run_regression.py`：12/12 PASS、0 FAIL、0 SKIP。
- 核心实现与 census 产物提交：`9a4c488`（`feat(dbdat): server 77项普查与边界探针`）。
- HANDOFF 文档提交在其后的独立提交中；当前分支为 `work/b50-serverdb-census`。

## 后续建议

1. 追查 table_2 的 DBID 1061/7618 反例，并尝试把坐标槽锚定到 city schema 字段。
2. 推进 table_7/8、table_24 行边界；table_24 的 B/U21 队名称可作为辅助锚点。
3. 按价值继续攻克其他 unresolved 中小表，再处理大表；对 table_extra_3 优先寻找独立行边界/字段参照。
4. 所有结论保持 L1/L2/L3/L4 口径；不把未知字段解释成无语义，也不把 L1 自家回环说成加载验证。
