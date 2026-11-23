# t114 — `basic_people_db.dat`（658,011 人）全量纯 Python 解码闭合与 `people_db.dat`（400 MB）锚点验证

> 交付目录：`OUTDIR`（`scratch/t114/out`）
> 脚本路径：`scripts/t114_people_decoder.py`（Python 3.12 `-I -B`，须含 `--help`、`--selftest`，退出码 0/1/2）
> 输入源（全部只读）：
> - `scratch/t113/out/people_archives_inventory.json`
> - `scratch/t113/out/people_vtables_full.json`、`scratch/t113/out/funcs/*.c`（含 `1410992c0.c` 人物工厂、`PERSON` 8,980L、`CONTRACT` 1,564L、`BASIC_PERSON` 960L）
> - `scratch/t95/funcs/140e4fd70.c`（`BASIC_PERSON::slot19` 175L）和 `140e50cd0.c`（`BASIC_PERSON::slot02`）
> - `scratch/data/basic_people_db.dat`（解压 54,060,043 B，658,011 行）与 `scratch/data/people_db.dat`（解压 400,443,970 B）
> - `scripts/t38_multiframe.py`
> 不要修改 `reports/` 或 `LEDGER.json`。

## 任务目标
1. **精读 `BASIC_PERSON::slot19` (`140e4fd70.c`) 与 `slot02` (`140e50cd0.c`)**：
   - 完整抽出 `BASIC_PERSON` 的精确二进制列布局（`wire_off`, `width`, `mem_off`, `4CC`），并说明它与 5 个子类计数（`166,064 / 476,158 / 4,757 / 9,839 / 1,193`）的对应关系（对照 `1410992c0.c` 的 `case 1..6`：`NON_PLAYER / PLAYER / PLAYER_AND_NON_PLAYER / OFFICIAL / JOURNALIST`）。
2. **实现纯 Python 高速 `basic_people_db.dat` 全量解码器**：
   - 跑完 **`basic_people_db.dat` 全部 658,011 行**，校验精确闭合到末尾 footer（`pos == len - 9`）！
   - 按 UID 锚点实查已知球星（如 Harry Kane `28049320`、Cristiano Ronaldo `735216`、Messi `7458500` 等），打印他们的 `basic_people` 解码字段（出生日期、姓名 ID、国籍、身高/体重/人物类型等）并与现实事实核对（L2+L3 双证！）。
3. **精读 `PERSON::slot19` 与 `ACTUAL_PLAYER::slot19`（在 `scratch/t113/out/funcs/`），解码 `people_db.dat` (400 MB) 头部与前 100 行**：
   - 确认 `people_db.dat` 内部成员结构与每行首字节 `person_type` 分发规则，尽量解出前 20 行结构摘要（若含复杂嵌套子类块如 `PLAYER_DATA` 未反编译，如实标注缺漏 helper VA 清单）。

## 交付物（写入 `OUTDIR = scratch/t114/out`）
1. `basic_people_schema.json`：含 `"status": "complete"`，`BASIC_PERSON` 完整 L3 列定义、658,011 行全量闭合验证、5 子类统计与球星 UID 实测锚点记录。
2. `people_db_probe.json`：`people_db.dat` 400 MB 头部/行首类型分析与待补反编译 helper 清单。
3. `REPORT.md`：人类可读汇总与球星解码样例表。
4. `DONE.md`：含 `DONE type=t114` 与核心统计数字。

## 验收标准
- `py -V:3.12 -I -B scripts/t114_people_decoder.py --selftest` 退出 0。
- `basic_people_db.dat` **全部 658,011 行**必须通过纯 Python 字节精确闭合验证，且至少命中 2 个知名球星 UID 锚点！
