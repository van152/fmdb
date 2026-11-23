DONE type=t96

状态：partial（未达到验收标准，不代表全量闭合）。

- `scripts/t96_unicorn_all_tables.py --selftest`：通过（STARTING_RECORD，消费 3918 B）。
- 交付记录：79 个 archive/table 组合；footer 闭合 2 个；`wire_traces.json` 状态为 `partial`。
- `table_9`：server 仅追踪到 5/251 行后发生 unmapped read（row 0 为 57 B）；client row 0 即 unmapped read。均未闭合至 footer，未验证 307,564 / 31,956 B 目标。
- 尚未实现字符串/动态数组长度字段与完整父调用链归因；未解决 table_10 等异常。
- 详见 `REPORT.md` 与 `table9_251_closure.json`。失败均如实保留，未生成 complete 状态。
