# t112 — FM24 只读多表数据库解析库原型（`scripts/t112_fm24_reader.py`）与真机数据端到端验证

> 交付目录：`OUTDIR`（`scratch/t112/out`）
> 脚本路径：`scripts/t112_fm24_reader.py`（Python 3.12 `-I -B`，须含 `--help` 和 `--selftest`，退出码 0/1/2）
> 输入源（全部只读）：
> - `scratch/t110/out/master_67tables_l3.json`（54 张表、1,036 条 L3 映射）
> - `scratch/t96c/out/wire_traces_master.json`（Unicorn 实测 41 张整表闭合 + 27 张大表 wire 序列）
> - `scratch/t95/funcs/*.c`（需要核对定长/变长字段读法时参考）
> - `scratch/data/server_db.dat`、`scratch/data/client_db.dat`、`scripts/t38_multiframe.py`
> 不要修改 `reports/` 或 `LEDGER.json`。

## 任务目标
前期所有逆向研究（IDA + Unicorn + 1,034 分母）最终都要落地成**真正能读出 FM24 数据库内容的实用代码**！
请构建一个干净、高速、纯 Python（只依赖标准库 + vendored `zstandard`）的只读数据库解析器 `scripts/t112_fm24_reader.py`：

1. **支持至少 25 张以上核心表和子表的真实行解码**（优先覆盖已 `CLOSED (diff=0)` 的全部定长与变长表 + 核心实体表）：
   - 核心实体：`table_5 CONTINENT`、`table_6 INJURY`、`table_7 MEDIA_SOURCE`、`table_8 LANGUAGE`、`table_19 REGION`、`table_22 STADIUM_CHANGE`、`table_23 STAGE_NAME`、`table_27 WEATHER`、`table_35 PLAYER_TYPE`、`table_41 CURRENCY_RECORD`、`table_56 AGREEMENT`
   - 核心大表：`table_2 CITY`、`table_21 STADIUM`、`table_45 STARTING_RECORD`（84,477 行，`rowlen == 80 + namelen` 全部 18 列！）、`table_48 STARTING_RECORD`（5,210 行）
   - 重要子表：`table_29 STARTING_LOAN`、`table_30 STARTING_INJURY`、`table_31 STARTING_CONFIDENCE`、`table_33 STARTING_CLUB_DEBT`、`table_34 STARTING_TEAM_CUP_HISTORY`、`table_37 STARTING_TEAM_LEAGUE_HISTORY`、`table_38 STARTING_BAN`、`table_39 STARTING_AVERAGE_POINTS`、`table_42 STARTING_RETIREMENT`、`table_43 STARTING_MONTHLY_INSTALLMENT`、`table_46 STARTING_DRAFT_TRANSFER`、`table_50`/`51`/`58`/`60`/`61`/`63`/`65`/`66`/`68`/`69`/`73` 等！
   - 若时间允许，也接入 `table_10 NATION` (client/server) 和 `table_25 COMP` (client)！
2. **字段名直接绑定 L3 4CC**：每张表解析出的 dict 键名直接使用 `t110` 的 L3 4CC（无 4CC 处用 `col_<wire_off>` 诚实命名），并自动解出 `identity`（`uid`, `dbid`）。
3. **全表 0 字节误差校验（Footer Closure）**：对每一张已接入的表，用纯 Python 解码器跑完**全部行**（百万行级大表也可毫秒/秒级跑完！）并验证最终位置 **`pos == len(payload) - 9`**（精确命中 9 字节 footer）！
4. **CLI 查询体验**：支持 `--list`（列出所有已支持表及校验状态）、`--dump <archive> <table_id> --limit 5`（输出 JSON 样例行）、`--verify-all`（全表跑完 footer 闭合校验并输出报告）。

## 交付物（写入 `OUTDIR = scratch/t112/out`）
1. `reader_verify.json`：含 `"status": "complete"`，每张接入表的 `rows_decoded`, `elapsed_ms`, `footer_closed`, `l3_named_fields`, `sample_rows`（前 3 行真实数据）。
2. `REPORT.md`：可读性极佳的使用说明、全表闭合矩阵（行数、耗时、命名列数）、真实样本展示（例如真实伤病、语言、大洲、球场改造、俱乐部债务、84,477 行 `STARTING_RECORD` 等）。
3. `DONE.md`：含 `DONE type=t112` 与核心统计数字。

## 验收标准
- `py -V:3.12 -I -B scripts/t112_fm24_reader.py --selftest` 退出 0。
- 至少 **25 张以上**表通过纯 Python 整表 100% `footer_closed == True` 验证！
