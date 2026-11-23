# t111 — 攻克 Unicorn 剩余最后 11 张表（冲刺 79/79 全库闭合！）

> 交付目录：`OUTDIR`（`scratch/t111/out`）
> 脚本路径：`scripts/t111_unicorn_last11.py`（Python 3.12 `-B`，须含 `--help` 和 `--selftest`，退出码 0/1/2）
> 输入源（只读）：`scripts/t95_unicorn_trace.py`、`scripts/t96c_unicorn_master.py`、`scratch/t96c/out/REPORT.md`、`scratch/t95/funcs/*.c`、`scratch/data/server_db.dat`、`scratch/data/client_db.dat`。不要修改 `reports/` 或 `LEDGER.json`。

## 背景
`scripts/t96c_unicorn_master.py` 已在 208 秒内跑通 **68/79（86.1%）** 表对（含 41 张整表 `diff == 0` 精确闭合：`server/client t9` 251/251、`server/client t10` 251/251 等），目前只剩最后 **11 对表** 尚未跑通：
1. `server/t0` & `client/t0` (`AWARD`): row 1 `flag=0xc8`, `rip=0x140f92cc4`, `addr=0x80`
2. `server/t3` (`CLUB`): row 3 `consumed=62498`, `rip=0x14371be8d` (`huge_read`)；`client/t3` (`CLUB`): row 12 `flag=0x4d`
3. `server/t32` (`STARTING_FUTURE_TRANSFER`): row 1 `pos 19111 >= footer 19103` (`diff = -8`)
4. `server/t36` (`STARTING_MANAGER_HOF_RECORD`): row 1 `consumed=18`, `UC_ERR_READ_UNMAPPED`
5. `server/t41` (`CURRENCY_RECORD`): row 0 `consumed=16`, `UC_ERR_READ_UNMAPPED`（注意 `client/t41` 已 173/173 `diff=0` 闭合！）
6. `server/t45` & `server/t48` (`STARTING_RECORD`): `consumed=55`（注意不用工厂而用零初始化 `THIS_BASE` 时 `t95_unicorn_trace.py` 已经跑通过 10/10！原因是工厂把 `*(this+0x38)` 设了非零/哨兵，导致字符串读函数 `sub_140814B10` 异常释放旧字符串！）
7. `server/t71` (`STARTING_PAST_TRANSFER`): row 9 `consumed=29393`, `_Xlength_error`
8. `server/t72` (`STARTING_PAST_TRADE`): row 0 `consumed=25`, `rip=0x140f83b02`, `addr=0x80`

## 任务目标
逐一查明上述 11 对表失败的精确指令与原因（看 `scratch/t95/funcs/*.c` 中对应 `slot19` 源码 + 反汇编报错 `rip`），在 `scripts/t111_unicorn_last11.py` 中补齐对应 stub / 构造参数 / `a3` / `flag` 分派逻辑，重点攻克：
- **`server/t3` & `client/t3` (`CLUB`, 84,259 行)**：至少前 200 行零异常，产出完整 `CLUB` server+client `canonical_fields`！
- **`server/t45` (84,477 行) & `server/t48` (5,210 行)**：至少前 200 行零异常（`t48` 可全表 5,210 行或 200 行闭合检查）！
- **`server/t0` & `client/t0` (`AWARD`, 3,545 行)**：解决 `0x140f92cc4` `addr=0x80` 与 row 1 对齐问题！
- **`server/t32` (315 行)、`server/t41` (173 行)、`server/t72` (138 行)**：冲刺整表 `diff == 0` 闭合！
- **`server/t36` (6,535 行)、`server/t71` (616,665 行)**：至少前 50 行零异常！

## 交付物（写入 `OUTDIR = scratch/t111/out`）
1. `last11_traces.json`：含 `"status": "complete"`（或 `"partial"`），11 对表的逐表追踪结果、`canonical_fields`、`row0_reads` 与失败根因总结。
2. `REPORT.md`：11 对表修复前后对比表（含具体修掉的汇编根因、新增闭合表数、总闭合进度更新）。
3. `DONE.md`：含 `DONE type=t111` 与核心统计数字。
