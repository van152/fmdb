# t99 — 全库归档清单、11 张 default 表确认与 `lang_update_db.dat` 解析

> 交付目录：`OUTDIR`（`scratch/t99/out`）
> 脚本路径：`scripts/t99_lang_and_inventory.py`（Python 3.12 `-I -B`，须含 `--help` 和 `--selftest`，退出码 0/1/2）
> 输入源（全部只读）：`scratch/data/*.dat`（全部 12 个 `.dat` 归档）、`scratch/t14/out/census.json`、`scratch/t95/vtable_index.json`、`scratch/t93/outbox.md/field_dictionary.json`。不要修改 `reports/` 或 `LEDGER.json`。

## 任务目标

### 1. 全库 12 个 `.dat` 归档的完整成员普查
扫描 `scratch/data/` 下全部 `.dat` 文件（`server_db.dat`, `client_db.dat`, `lang_update_db.dat`, `people_db.dat`, `basic_people_db.dat`, `summary.dat`, `pl_hist_*.dat`, `non_pl_hist_*.dat`）：
- 用 `scripts/t38_multiframe.py`（遵循 E80 规则）列出每个归档的全部成员：`path`, `size`, `packed_size`, `payload_magic`, `version`, `record_count_header`, `table_id`（若有）。
- **11 张 `default` handler 表最终裁决**：逐一检查 `table_type` ∈ `{11, 13, 15, 16, 17, 20, 28, 40, 53, 54, 55}` 在全部 12 个 `.dat` 归档中是否出现、是否存在任何非空成员。若全库 0 出现，给出可复现的 L1/L2 终判（可从有效表分母中正式划出！）。
- **盘点所有非编号成员**（如 `simple_vars.dat`, `club_links.dat`, `table_extra_3/9/24.dat`, `name_table_0/1/2.dat`, `name_table_extra_0/1/2.dat`, `common_name_links.dat`, `table_for_old_save_23/25.dat`, `fantasy_draft_future_regens.dat` 等）：统计其体积、头部魔数、记录数与结构特征。

### 2. 解析 `lang_update_db.dat` (2.3 MB)
- 完整解包 `lang_update_db.dat` 内部所有成员，识别其格式（容器头、字符串表 / 键值对 / 本地化条目结构）。
- 提取其统计概览（成员数、语言/记录条数、前 30 条样本、字段/表关联线索），评估它对数据库字段语义命名的贡献。

### 3. 全库 74 表覆盖总账基线
结合 `scratch/t14/out/census.json`（74 表）与本次 12 归档扫描结果，生成一张清晰的总表清单：
- 哪些表存在于 `server_db.dat` / `client_db.dat` / `people_db.dat` / `basic_people_db.dat` / `pl_hist_*` / `non_pl_hist_*`
- 每张表的行数、解压体积、对应 C++ 类名、vtable VA、`t95` 反编译状态（已全量反编译 vs 缺漏）。

## 交付物（写入 `OUTDIR`）
1. `db_inventory.json`：含 `"status": "complete"`，12 归档全成员 + 74 表存在矩阵 + 11 张 default 表裁决 + 非编号成员清单。
2. `lang_db_summary.json`：`lang_update_db.dat` 解包结构与统计样本。
3. `REPORT.md`：人类可读汇总报告。
4. `verify.py`：独立校验脚本。
5. `DONE.md`：含 `DONE type=t99` 与关键统计数字。

## 验收标准
- `py -V:3.12 -I -B scripts/t99_lang_and_inventory.py --selftest` 退出 0。
- `py -V:3.12 -I -B scratch/t99/out/verify.py` 退出 0。
- 分块写盘（避免超长单次输出超时），完成后打印交付清单。
