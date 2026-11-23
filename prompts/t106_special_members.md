# t106 — 非编号特殊表（`name_table_*` / `common_name_links` / `club_links` / `simple_vars` / `summary.dat`）格式解析与验证

> 交付目录：`OUTDIR`（`scratch/t106/out`）
> 脚本路径：`scripts/t106_special_members.py`（Python 3.12 `-I -B`，须含 `--help` 和 `--selftest`，退出码 0/1/2）
> 输入源（全部只读）：`scratch/data/server_db.dat`、`scratch/data/client_db.dat`、`scratch/data/summary.dat`、`scripts/t38_multiframe.py`。不要修改 `reports/` 或 `LEDGER.json`。

## 任务目标
除 `table_<N>.dat`（编号表，由 t96–t105 处理）外，FM24 数据库还包含若干关键的非编号成员，承担姓名池、俱乐部关联、全局变量与库摘要：
1. `name_table_0.dat` (2.95 MB)、`name_table_1.dat` (6.50 MB)、`name_table_2.dat` (1.03 MB)（first name / surname / common name）
2. `name_table_extra_0/1/2.dat` (3.84 MB / 8.71 MB / 1.64 MB)
3. `common_name_links.dat` (120 KB)
4. `club_links.dat` (435 KB)
5. `simple_vars.dat` (82 KB)
6. `summary.dat` (1.65 MB，独立归档)
7. `table_for_old_save_23.dat`、`table_for_old_save_25.dat`、`fantasy_draft_future_regens.dat`

请编写 `scripts/t106_special_members.py` 完成：
- 使用 `scripts/t38_multiframe.py`（E80 规则）解包上述全部成员，解析每个成员的二进制头、记录结构、字段宽度、字符串/UID 编码。
- 实现每个成员的逐行解码器，校验**字节精确闭合**（是否全部消费至末尾 9B footer / 文件尾）。
- 对每个成员输出前 10 条解码样本（例如 `name_table_0/1/2` 的真实姓名+UID+国籍/频率字段、`club_links` 的关联俱乐部 UID 对、`simple_vars` 的键值对）。

## 交付物（写入 `OUTDIR`）
1. `special_members_schema.json`：含 `"status": "complete"`，全部 13 个特殊成员的二进制格式定义、记录数、footer 闭合验证结果与前 10 条样本。
2. `REPORT.md`：清晰格式说明与闭合汇总表。
3. `DONE.md`：含 `DONE type=t106` 与核心统计数字。
