# t112b — 直接落地 `scripts/t112_fm24_reader.py`（50+ 表纯 Python 100% Footer 闭合只读解析库）

> 交付目录：`OUTDIR`（`scratch/t112/out`）
> 脚本路径：`scripts/t112_fm24_reader.py`（Python 3.12 `-I -B`，须含 `--help`、`--selftest`、`--list`、`--dump <archive> <tid> --limit N`、`--verify-all`，退出码 0/1/2）
> 不要修改 `reports/` 或 `LEDGER.json`。

## 直接落盘指令（禁止在 `t7 MEDIA_SOURCE` 等少数变长表上死磕耗尽时间！）
上一轮 `t112` 已经实证 **~50 对 `(archive, table)` 在纯 Python 下 100% 闭合到 `pos == len(payload) - 9`**（远超 25 张验收线！），包括：
- **通用行框**：13B 头（`<6sH4s` / `u16 ver @+6`, `u32 count @+8`）+ 每行 `[1B flag][body]`（最后 12B 为 `identity = (ordinal_u32, dbid_u32, uid_u32)`）+ 9B footer。
- **全量定长表**（直接从 `scratch/t96c/out/wire_traces_master.json` 校验，且实证整表 `pos == len-9`）：
  - `server/client t0 AWARD` (76B), `t2 CITY` (56,293行), `t5 CONTINENT`, `t6 INJURY`, `t19 REGION`, `t21 STADIUM` (48,413行), `t22 STADIUM_CHANGE`, `t23 STAGE_NAME`, `client t25 COMP` (7,047行, 126B), `t26 COMP_HISTORY_RECORD` (90,128行), `t29 STARTING_LOAN` (13,278行, 74B), `t30 STARTING_INJURY` (72,473行), `t31 STARTING_CONFIDENCE` (37,283行), `t33 STARTING_CLUB_DEBT` (32,409行), `t34 STARTING_TEAM_CUP_HISTORY` (7,115行), `t35 PLAYER_TYPE` (890行), `t37 STARTING_TEAM_LEAGUE_HISTORY` (465,712行!), `t38 STARTING_BAN` (5,241行), `t39 STARTING_AVERAGE_POINTS` (117行), `t42 STARTING_RETIREMENT` (17,721行), `t43 STARTING_MONTHLY_INSTALLMENT` (535行), `t46`, `t49 STARTING_PERSON_HISTORY` (792,149行!), `t50`, `t51`, `t56`, `t58`, `t60`, `t61`, `t62` (37,214行), `t63`, `t64` (6,946行), `t65/67/68/69`, `t66`, `t70` (10,075行), `t73` 等！
- **已验证的变长表**：
  - `server/client t8 LANGUAGE`: `body = 33 + nl@0`（126/126 闭合）
  - `server/client t27 WEATHER`: `body = 111 + nl@0`（334/334 闭合）
  - `server t45 STARTING_RECORD` (84,477 行) & `server t48 STARTING_RECORD` (5,210 行): `body = 79 + nl@37`（18 物理列，精确命中 footer！）
  - 若 `t41 CURRENCY_RECORD` (173 行) 1 分钟内顺手闭合则纳入，否则跳过不恋战！

## 执行步骤（严格先写代码、先落盘！）
1. **立刻编写 `scripts/t112_fm24_reader.py`**：
   - 从 `scratch/t110/out/master_67tables_l3.json` 与 `scratch/t96c/out/wire_traces_master.json` 自动/显式加载每张表的列定义与 L3 4CC 字段名（无 4CC 用 `col_<wire_off>` 命名，统一解出 `uid` / `dbid` / `ordinal`）。
   - 对全部 ~45–55 对已验证表跑 `--verify-all`（纯 Python 解码全部 **180 万+ 行**仅需数秒！），断言每张表 `pos == len(payload) - 9` (`footer_closed == True`)！
2. 立刻落盘交付物到 `scratch/t112/out/`：
   - `reader_verify.json`（含 `"status": "complete"`，逐表 `rows_decoded`, `elapsed_ms`, `footer_closed`, `l3_named_fields`, `sample_rows` ×3）
   - `REPORT.md`（清晰使用文档 + 全表闭合矩阵 + 总行数/耗时统计 + 真实样本展示）
   - `DONE.md`（含 `DONE type=t112b` 与核心统计数字）
3. 跑 `py -V:3.12 -I -B scripts/t112_fm24_reader.py --selftest` 验证退出 0，打印交付清单与核心统计！
