# t115 — `basic_people_db.dat`（658,011 人）完整 L3 语义解码 + 姓名表 Join + 球星 Top 50 实测验证

> 交付目录：`OUTDIR`（`scratch/t115/out`）
> 脚本路径：`scripts/t115_basic_people_full.py`（Python 3.12 `-I -B`，须含 `--help`、`--selftest`、`--uid <uid>`、`--top <N>`，退出码 0/1/2）
> 输入源（全部只读）：
> - `scratch/data/basic_people_db.dat`（zstd 解压后 54,060,043 B，头部 `<I` = 658,011 行，全量闭合到 `len-9`）
> - `scratch/data/server_db.dat`（含 `name_table_0/1/2.dat` 姓名池，`scripts/t38_multiframe.py` 加载）
> - `scratch/t95/funcs/140e4fd70.c`（`BASIC_PERSON::slot19` 174 行，**极其清晰，逐字段必读！**）
> - `scratch/t95/funcs/140e50cd0.c`（`BASIC_PERSON::slot02` 960 行，20 个 4CC）
> - `scratch/t113/out/funcs/1410992c0.c`（人物子类工厂：`1=NON_PLAYER, 2=PLAYER, 3=PLAYER_AND_NON_PLAYER, 4=OFFICIAL, 6=JOURNALIST`）
> 不要修改 `reports/` 或 `LEDGER.json`。

## 指挥官刚刚实测命中的 3 个铁证球星锚点（直接复用验证！）
在 `basic_people_db.dat` 解压 payload 中已实测定位：
- **Harry Kane (`uid = 28049320`, `0x01abffa8`)**：offset `13,650,120`，前 32B 含 `CA=184 (0x00b8)`, `PA=185 (0x00b9)`, 出生年 `1993 (0x07c9)`！
- **Cristiano Ronaldo (`uid = 735216`, `0x000b37f0`)**：offset `1,594,042`，前 32B 含 `CA=160 (0x00a0)`, `PA=200 (0x00c8)`, 出生年 `1985 (0x07c1)`！
- **Lionel Messi (`uid = 7458500`, `0x0071cec4`)**：offset `4,317,787`，前 32B 含 `CA=185/200`, `PA=200 (0x00c8)`, 出生年 `1987 (0x07c3)`！

## 任务目标
1. **逐行精读 `140e4fd70.c` (`BASIC_PERSON::slot19`) + `140e50cd0.c` (`slot02`)**：
   - 把 `BASIC_PERSON` 每一字节的二进制布局（按 `person_type` 分支：完整型 vs `OFFICIAL=4` 短型）与 `this+0xNN` 和 4CC 一一对应，给出严格 L3 列定义表（带精确 `file:line` 溯源）！
   - 核实 `140e4fd70.c` 末尾调用的 `sub_141084540`（`PERSON` 基础段：姓名 ID、出生日期、国籍、12B identity 等）。
2. **纯 Python 高速解码全部 658,011 行并精确闭合到 `len - 9`**：
   - 解出全部 658,011 人的 `person_type`, `uid`, `dbid`, `ordinal`, `first_name_id`, `surname_id`, `common_name_id`, `dob_year/doy`, `nation_id`, `club_id`, `ca`, `pa`, `home_rep`, `current_rep`, `world_rep` 等全部列！
   - 校验每行 `ordinal == row_index` 且最终位置精确命中 `len(payload) - 9` (`diff == 0`)！
3. **尝试关联 `name_table_0/1/2` 给出真实姓名（若可解出则附加，否则诚实标注 ID）并验证 5+ 位知名球星锚点**：
   - 必查：Harry Kane (`28049320`)、Cristiano Ronaldo (`735216`)、Lionel Messi (`7458500`)，并按 `CA` 降序输出 FM24 **Top 30 最高 CA 球员清单**（含 `uid`, `person_type`, `CA`, `PA`, `birth_year`, `nation_id`, `club_id` 及姓名若已解出）！

## 交付物（写入 `OUTDIR = scratch/t115/out`）
1. `basic_people_l3_schema.json`：含 `"status": "complete"`，`BASIC_PERSON` 全字段 L3 定义（带 C 行号）、658,011 行闭合验证统计、5 子类计数、锚点球星实测校验与 FM24 Top 30 CA 球员榜单。
2. `REPORT.md`：清晰字段表、球星锚点核对表、Top 30 CA 榜单。
3. `DONE.md`：含 `DONE type=t115` 与核心统计数字。

## 验收标准
- `py -V:3.12 -I -B scripts/t115_basic_people_full.py --selftest` 退出 0（须断言 658,011 行闭合 `diff == 0` 且 Kane `CA=184, PA=185, year=1993`、Ronaldo `CA=160, PA=200, year=1985`、Messi `PA=200, year=1987` 全部精确命中！）。
