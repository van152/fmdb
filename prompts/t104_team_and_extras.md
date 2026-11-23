# t104 — `TEAM` (`tt=24`) / `NATIONAL_TEAM` / `TEAM_CONTAINER` 与 `table_extra_{3,9,24}.dat` 结构解析

> 交付目录：`OUTDIR`（`scratch/t104/out`）
> 脚本路径：`scripts/t104_team_and_extras.py`（Python 3.12 `-I -B`，须含 `--help` 和 `--selftest`，退出码 0/1/2）
> 输入源（全部只读）：`scratch/t95/vtable_index.json`、`scratch/t95/funcs/*.c`、`scratch/data/server_db.dat`、`scratch/data/client_db.dat`、`scripts/t38_multiframe.py`。不要修改 `reports/` 或 `LEDGER.json`。

## 背景与输入
`scratch/t95/funcs/` 已完整反编译：
- `TEAM` (`0x14188e2d8`): `slot19=1411a1280.c`, `slot20=1411a1640.c`, `slot02=1411b01b0.c` (1803L), `slot03=1411b5630.c` (820L)
- `NATIONAL_TEAM` (`0x141889618`): `slot19=141053680.c`, `slot20`, `slot02`, `slot03`
- `TEAM_CONTAINER` (`0x14188e548`, CLUB 与 NATIONAL_TEAM_CONTAINER 共同基类！): `slot19=1411d1730.c` (1296L), `slot20=1411d2f80.c` (315L), `slot02=1411f1090.c` (1646L, 205 4CCs!), `slot03=1411f4f70.c` (1219L)

## 任务要求
1. **完整解析 `TEAM` (`tt=24`) 与 `NATIONAL_TEAM`**：
   - 从 Hex-Rays 提取 `server` + `client` wire 顺序与 `4CC ↔ mem_off ↔ wire_off` L3 映射。
   - 在真实 `server_db/table_24.dat` (84,507 行) 与 `client_db/table_24.dat` (84,507 行) 上验证逐行解码与 9B footer 闭合（注意 `tt=24` 按行型标志区分普通 `TEAM` 与 `NATIONAL_TEAM`！）。
2. **完整解析基类 `TEAM_CONTAINER`**：
   - 提取 `1411d1730.c` (server) 与 `1411d2f80.c` (client) 读入的全部字段 + `1411f1090.c` / `1411f4f70.c` 的 205 个 4CC → `mem_off` 映射！这会同时解锁 `CLUB` (`tt=3`) 和 `NATIONAL_TEAM_CONTAINER` (`tt=9`) 继承自基类的一大片未映射字段！
3. **盘点 `table_extra_3.dat` (35 MB)、`table_extra_9.dat` (105 KB)、`table_extra_24.dat` (6.9 MB)**：
   - 解压查看头部魔数、版本、记录帧格式，结合 `CLUB`/`NATIONAL_TEAM_CONTAINER`/`TEAM` 反编译代码中对 extra 数据的引用，定位三者的结构摘要与前 5 条样本记录。

## 交付物（写入 `OUTDIR`）
1. `team_and_extras_schema.json`：含 `"status": "complete"`，`TEAM`、`NATIONAL_TEAM`、`TEAM_CONTAINER` L3 映射 + `table_24` 实数校验 + `table_extra_{3,9,24}` 结构摘要。
2. `REPORT.md`：清晰报告。
3. `DONE.md`：含 `DONE type=t104` 与核心统计数字。
