# FM24 二进制数据库全量破译与双向读写引擎 (`fm24-db`)

> **最新里程碑（2026-11-23 Wave 14 收官）**：FM24 (`24.3.0`, DB version `0x0DF1`) 发行目录下全部 **13 / 13 个 `.dat` 二进制数据库档案**（解压后超 **`1.1 GB`**、承载超过 **`2,340 万` 条记录与多语言词条**）已实现 **100.0% 纯 Python 零字节误差（`diff == 0`）解码闭合**，并完成 **S+ 级位级双向回写与官方 `editor.exe` 真机机器码回读验收**（24 / 24 核心回归脚本 `--selftest` 全绿通过）。

## 📖 项目长篇纪实报告（推荐先读）

- **[《从“免费 AI 的五日浩劫”到大一统理论：我们如何在一夜之间破译 FM24 的二进制宇宙》](scratch/t145/out/WAVE14_MORNING_REPORT.md)**  
  完整还原本项目如何从最初五天“被降智免费模型立下错误祖制、手写上百个盲猜小脚本仅解出 6/74 表（10.6%）”的炼金术泥潭，通过掀开 `editor.exe` / `fm.exe` 底板、架设 Unicorn x86_64 粒子对撞机与多模型 AI 军团协同，在一夜之间打穿全部 13 个 `.dat` 档案并造出双向回写引擎的全过程。

---

## 🏆 13 / 13 `.dat` 全库零误差闭合总览

| # | 档案文件 | 规模与记录数 | 状态 | 核心脚本与报告 |
|---:|---|---|---:|---|
| 1–2 | `server_db.dat` + `client_db.dat` | **79 / 79 张编号表**（2,846,936 行）+ **13 个特殊成员**（1,858,739 行）+ `table_extra_9/24` | **`diff = 0`** | [`t133_fm24_reader_v2.py`](scripts/t133_fm24_reader_v2.py) · [`t106_special_members.py`](scripts/t106_special_members.py) · [`t136_big3_final_closure.py`](scripts/t136_big3_final_closure.py) |
| 3 | `summary.dat` | 54,087 条目 + 11,004 B 尾段 | **`diff = 0`** | [`t106_special_members.py`](scripts/t106_special_members.py) |
| 4 | `basic_people_db.dat` | **658,011 行**（5 类人物定宽 `83/83/83/34/22 B`） | **`diff = 0`** | [`t123_basic_people_l3.py`](scripts/t123_basic_people_l3.py) |
| 5 | `people_db.dat` | **400.4 MB** / **658,011 名足坛人物**（纯 Python 16.84s 全量闭合，含球员 54/54 `PDxx` 属性与教练 34 项执教属性） | **`diff = 0`** | [`t138_people_pure_py.py`](scripts/t138_people_pure_py.py) · [`t126_player_attributes_l3.py`](scripts/t126_player_attributes_l3.py) · [`t137d_manager_cards_full.py`](scripts/t137d_manager_cards_full.py) |
| 6–7 | `lang_db_2400.dat` + `lang_update_db.dat` | **704 / 704 语言包成员**（22 种语言、**10,290,726 条** UTF-8 本地化词条，含 196.4 万简体中文） | **`diff = 0`** | [`t143_lang_db.py`](scripts/t143_lang_db.py) |
| 8–10 | `pl_hist_{index,id,dt}.dat` | **515,581 名球员** / **4,515,803 条**赛季履历（198.7 MB，48,510 个 4 KiB zstd 帧） | **`diff = 0`** | [`t127_pl_hist.py`](scripts/t127_pl_hist.py) |
| 11–13 | `non_pl_hist_{index,id,dt}.dat` | **746,543 名职员** / **3,212,443 条**任职履历（77.1 MB，18,823 个 4 KiB zstd 帧） | **`diff = 0`** | [`t128_non_pl_hist.py`](scripts/t128_non_pl_hist.py) |

---

## 🛠️ 核心工程与分析交付物

- **S+ 级双向回写与 Round-Trip 引擎**：[`scripts/t140_fm24_roundtrip.py`](scripts/t140_fm24_roundtrip.py)（[报告](scratch/t140/out/REPORT.md)）—— 79/79 表位级无损重编码（`sha256` 100% 一致）+ 跨表变长修改与球星属性改写 + FMF/zstd 重打包 + 纯 Python 与 `editor.exe` 真机机器码双重零误差回读（69/69 PASS）。
- **毫秒级 SQLite 数据仓库与 CLI**：[`scripts/t139_fm24_db_cli.py`](scripts/t139_fm24_db_cli.py)（[报告](scratch/t139/out/REPORT.md)）—— 一键导出 191.7 MB 索引化 SQLite 数据库（24 张核心表、195.2 万行、`0.041 ms` 查表延迟）。
- **世界巨星与传奇名帅原盘直读卡片**：[`scripts/t135_star_player_cards.py`](scripts/t135_star_player_cards.py)（[21 位巨星报告](scratch/t135/out/REPORT.md)）· [`scripts/t137d_manager_cards_full.py`](scripts/t137d_manager_cards_full.py)（[Top-20 名帅报告](scratch/t137d/out/REPORT.md)）。
- **全库 84 表外键图谱与官方数据体检**：[`scripts/t142_fk_graph_audit.py`](scripts/t142_fk_graph_audit.py)（[报告](scratch/t142/out/REPORT.md)）—— 确认 44 条外键边、破译 24 个匿名列、检出 SI 官方库 764 行真实悬空外键。
- **`fm.exe` vs `editor.exe` 数据库内核同源定理**：[`scripts/t141_fm_vs_editor_diff.py`](scripts/t141_fm_vs_editor_diff.py)（[报告](scratch/t141/out/REPORT.md)）—— 证明 293/293 `db::` 类与 33/33 `STARTING_*` 类 100% 同源共享。
- **24 / 24 终极自动化回归矩阵**：[`scripts/t145_final_regression.py`](scripts/t145_final_regression.py)（[矩阵 JSON](scratch/t145/out/regression_matrix.json)）。

---

## 🧭 历史导航与基线文档

- 使命与硬约束：[AGENTS.md](AGENTS.md)
- 早期仓库现状快照（2026-11-21 v11 同步）：[docs/REPO_STATUS.md](docs/REPO_STATUS.md)
- 早期覆盖率基线 + 增量台账：[docs/BASELINE.md](docs/BASELINE.md)
- 外部只读引用说明：[docs/refs.md](docs/refs.md)
- 证据快照：[evidence/fm24/](evidence/fm24/)（SHA-256 见 [evidence/MANIFEST.json](evidence/MANIFEST.json)）
- 公共 schema：`reports/club_nation_subtable_schema.{json,md}`、[reports/other_tables_schema.json](reports/other_tables_schema.json)、[reports/xml_denominator_coverage.json](reports/xml_denominator_coverage.json)

## ⚡ 常用验证命令

```powershell
# 运行 Wave 13-14 全部 24 个核心里程碑脚本的终极回归自检 (24/24 PASS)
py -V:3.12 -B scripts/t145_final_regression.py --selftest

# 纯 Python 读取 server_db / client_db 全部 79 张编号表 (51/51 PASS)
py -V:3.12 -B scripts/t133_fm24_reader_v2.py --selftest

# 纯 Python 解码 400 MB people_db.dat 全部 658,011 名人物
py -V:3.12 -B scripts/t138_people_pure_py.py --selftest

# S+ 级 79/79 表双向位级回写 + editor.exe 真机机器码双重验收 (69/69 PASS)
py -V:3.12 -B scripts/t140_fm24_roundtrip.py --selftest

# 多语言大库 (704/704 成员, 1,029 万词条) 与生涯历史库 (772.8 万行) 自检
py -V:3.12 -B scripts/t143_lang_db.py --selftest
py -V:3.12 -B scripts/t127_pl_hist.py --selftest
py -V:3.12 -B scripts/t128_non_pl_hist.py --selftest

# 早期冻结锚点与 schema 基线自检
py -V:3.12 -I -B scripts/t01_anchors.py
py -V:3.12 -I scripts/baseline_coverage.py --check
```
