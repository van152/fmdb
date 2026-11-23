# t105 — 三大主表（`CLUB` / `COMP` / `NATION` + `NAT_TEAM_CONT`）Hex-Rays 序列化器逐行审计

> 交付目录：`OUTDIR`（`scratch/t105/out`）
> 脚本路径：`scripts/t105_big3_serializers.py`（Python 3.12 `-I -B`，须含 `--help` 和 `--selftest`，退出码 0/1/2）
> 输入源（全部只读）：`scratch/t95/vtable_index.json`、`scratch/t95/funcs/*.c`（重点：`140e5b1a0.c`, `140e5cf50.c`, `140eb7a00.c`, `140eb9000.c`, `1410404c0.c`, `14105d510.c` 及它们对应的 `hop1` client 文件）。不要修改 `reports/` 或 `LEDGER.json`。

## 任务目标
三大主表（`CLUB` tt=3、`NATION` tt=10 + `NATIONAL_TEAM_CONTAINER` tt=9、`COMP` tt=25）合计承载 1,034 个 XML 字段，是此前项目卡在 10.6% 覆盖率的核心难点。现在它们的 Hex-Rays C 伪代码全部在 `scratch/t95/funcs/` 里！

请写一个结构化 C 伪代码序列化器解析脚本 `scripts/t105_big3_serializers.py`，对以下 6 个核心序列化函数做逐行精确抽取（带 C 行号与版本门控条件）：
1. `CLUB::read_server` (`140e5b1a0.c`, 945L) 与 `CLUB::read_client` (`140e5cf50.c`, 200L)
2. `COMP::read_server` (`140eb7a00.c`, 551L) 与 `COMP::read_client` (`140eb9000.c`, 90L)
3. `NATION::read_server` (`1410404c0.c`, 677L) 与 `NATION::read_client`（查 `vtable_index.json` 中 `tt=10 slot20` 及其 `hop1`）
4. `NATIONAL_TEAM_CONTAINER::read_server` (`14105d510.c`, 1589L) 与 `read_client`（查 `tt=9 slot20` 及其 `hop1`）

对每个函数按执行顺序提取**有序读取步骤清单**：
- `seq_idx`, `line_no`, `read_kind` (`stream_vcall_40` | `helper_call` | `loop_vector` | `base_class_call`)
- `dst_mem_off`（按 `a1` 指针宽度统一换算成字节偏移 `0xNN`，若是栈临时变量标 `stack:vNN` 并追踪其后续写入的 `a1+0xNN`！）
- `wire_width`（固定字节数 1/2/4/8/12 或 `varlen:<helper_va>`）
- `version_gate`（所在 `if` 块的 DB 版本判断如 `ver >= 0xDDD` 或 `a5 != 0` 等条件表达式）
- `helper_va`（调用的子函数 VA，并汇总所有高频未反编译 helper VA 清单 `needed_helpers`，供下一轮 5 秒 IDA 补反编译！）

## 交付物（写入 `OUTDIR`）
1. `big3_serializers.json`：含 `"status": "complete"`，上述 8 个函数的完整有序序列化步骤清单 + `needed_helpers` 高频子函数清单。
2. `REPORT.md`：三大主表每个序列化器的读取步骤数、固定字段 vs 变长容器分布、版本门控总结与 `needed_helpers` Top 30。
3. `DONE.md`：含 `DONE type=t105` 与核心统计数字。
