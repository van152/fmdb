# t147 立即收口落盘指令（停止继续探索！）

你已在本次会话中完成了大量 `nation`（table_9 / table_10 / table_extra_9 / lang_db）26 个缺口的深入调研。**现在立即停止任何新的探索、反编译或仿真实验**，马上把你已经掌握并验证过的全部结论落盘为正式交付物：

1. 编写 `scripts/t147_nation_gaps_v5.py`（必须 `import fm24_config`，零硬编码路径，支持 `--help` 和 `--selftest`，退出码 0/1/2）。
2. 运行脚本生成：
   - `${OUTDIR}/nation_gaps_v5.json`（含 `"status": "complete"` 或 `"partial"`，26 条 nation 缺口逐条裁决：新闭合 L3 / 确证非持久化排除 / 仍保留并写精确阻断点，总数严格守恒 = 26）
   - `${OUTDIR}/REPORT.md`
   - `${OUTDIR}/DONE.md`（首行含 `DONE type=nation_gaps_v5`）
3. 运行 `py -V:3.12 -B scripts/t147_nation_gaps_v5.py --selftest` 与 `py -V:3.12 -B scripts/check_repo.py` 确认全部通过后立即结束并打印交付清单！
4. 严禁修改 `reports/`、`scratch/t01/LEDGER.json` 及既有脚本。
