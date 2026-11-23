# b46 交接 — client_db 小表业务字段普查

## 交付物

- `scripts/b46_tables_small.py`：只读 scoped-FMF 扫描器，提供 `--help`、`--table N`、`--json PATH`、`--selftest`。
- `reports/dbdat_decode/db_tables_small.json`：16 张表、名称池、simple_vars、old-save 辅助项的完整机读字段/槽位统计。
- `reports/dbdat_decode/SMALL_TABLES.md`：逐表边界模型、槽位、身份映射档位、L2/负结果与证据边界。
- `tmp_b46/PROGRESS.md`：P0–P2 检查点与风险记录。

## 关键数字与验收

- 目标 16 表总计 **10,716 行**；任务书 count **16/16 相符**；边界模型 **16/16** 到 footer 闭合。固定步长表覆盖 table_47 的 11 B 扩展头；变长表覆盖 7/8/9/10/18/27/41。
- table_9 / table_10 identity 顺序相同 **251/251**；简中 table_9 名称更新覆盖 **250/251**，未覆盖 identity 为 `217945`。
- table_7 English 名称更新 **3/3** key/name 对上；table_18 English 更新 **25/25** key/name 对上；table_0 **38/38**、table_6 **1/1** English 更新 key 对上对应 identity。
- `name_table_{0,1,2}` 分别 245,981 / 542,060 / 85,668 行；main `u32@+2` 与同序 `name_table_extra_*` string_id 全匹配。client/server 六份成员均字节相同；ID 是 pool-local ordinal，未证明 16 张小表有指向这些 pool 的字段引用。
- simple_vars 解压 payload **34 B**，所有字节分片记录但语义未命名；`table_for_old_save_23` 与 table_23 相同；`table_for_old_save_25` 为 **7,047×123 B** 结构，仅清点 auxiliary，不读取主 table_25。
- scanner 的实读成员审计 `db_tables_small.json.meta.decompressed_entry_paths_by_archive` 显示，**没有解压 table_2/3/21/25 或 table_extra_3**；prohibited list 为空。
- `py -V:3.12 -I scripts/b46_tables_small.py --selftest`：**13/13 true**；16 次 `--table N --json ...`：**16/16 exit 0**。
- 最终全量回归：`py -V:3.12 -I scripts/run_regression.py` → **12 PASS / 0 FAIL / 0 SKIP（176.3s）**。
  - 第一次在稀疏 worktree 原地运行时，因 `.gitignore` 留盘输入未映射，出现 4 PASS / 2 FAIL / 6 SKIP；两个 FAIL 都是缺 `1 1-大连人.fm` / `Stadium improvements.json` 的 `FileNotFoundError`。没有据此归咎代码。
  - 最终运行前，在 worktree 临时创建 3 个 junction，仅供回归只读访问主树的 `dbc_decoded/`、`decrypted/`、`save_decode/samples/`。最终回归后逐个 `rmdir` 移除链接；主树源文件未复制/修改。恢复了回归工具改写的基线和跟踪内索引/自检产物，未提交时间戳抖动。

## 表映射结论与证据等级

- **L1（自家结构字节记账）**：16 张行边界、stride/row walk、重复-u32/rdui/ordinal 槽、table_9/10 identity sequence、table_41 4 字符串/历史项/trailer、name_table main↔extra ordinal 关系、旧存档辅助项边界。L1 只说明本工具结构闭合，不提升为外部验证。
- **L2（公开名称/事实）**：table_0 公开奖项名称、table_6 Plantar Fasciitis、table_7 媒体名称/URL、table_8 语言名、table_9/10 Singapore 等国家事实、table_18 Oulu/Melbourne 等地名、table_27 climate-name 候选、table_41 Euro/USD/JPY/GBP 名称与符号。语言更新 key 与基础表 identity 的逐字节 join 单独仍是 L1。
- entity 档位：**确认** award(0)、injury(6)、media source(7)、language(8)、nation name/key companion(9)、nation(10)、city-associated secondary-name data(18)、currency(41)；**候选** continent(5)、weather profile(27)；**未知** 19/22/23/35/47/56。
- 明确无 L2 字段的表：5/19/22/23/35/47/56。table_47 44-byte fixed-row 候选虽已精确记账，但 repeated-u32 identity offset 不稳定，拒绝命名字段。
- **L3=0**（本任务未做 exe 静态分析）；**L4=0**（未启动游戏/editor）。

## 未解项 / 不可超读范围

1. table_0/5/6/19/22/23/35/47/56 的大部分业务槽位仍只有字节/数值分布，未做一字段一 Schema 的完整绑定；table_5 的 continent 仅为候选。
2. table_7 nested list/enum/URL role 未全解；177/208 个首 URL-slot 候选可解析，`Murl` 仍只标候选。
3. table_9/10 仅解身份边界；table_10 scalar body 未逐字段映射。
4. table_18 中间变长 48–134 B 区、table_27 99 B 数值区未映射到具体 city/weather Schema codes；table_27 entity 仍候选。
5. table_41 的四个字符串角色和 history kind 语义未完全定型；不把 rates 外推为某个报告日期。
6. name_table pool 的人名分类、metadata 其余 u16 字段、业务字段如何指向三个 pool 均未解；不能把 local string ordinal 当 DBID。
7. simple_vars 字段语义未知；old-save25 只得 123 B stride，不读取主 table_25。

## 提交记录

- 阶段 P1（工具、全量 JSON、逐表报告、安全审计）：`a458bb474f43f25284630dd7ffdbd253bc9c05dd` — `feat(dbdat): 普查client_db小表业务字段`。
- 阶段 P2（HANDOFF 与最终回归记录）：`9bd3c9df9cb6e53d007618b143fcc23edf659613` — `docs(dbdat): 补充b46交接与回归结果`。
- 后续仅为将上述 P2 hash 回填到本 HANDOFF 的元数据提交；当前最终 HEAD hash 由收尾消息给出。
