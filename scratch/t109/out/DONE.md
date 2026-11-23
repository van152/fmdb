DONE type=t109c

完成 `t109_big3_l3_join.py` 收尾并重生成三份 JSON。自检通过（退出码 0）；三份机读结果均 `status=complete`，分母 1,034 严格守恒（club 433 + nation 346 + comp 255）。

- 旧覆盖：110/1,034 = 10.6%
- 新总覆盖：379/1,034 = 36.7%（105 L3 static + 274 routed）
- 净持久化覆盖：379/673 = 56.3%
- 其余：361 excluded non-DB；294 gap；accepted-L3 crosscheck 尚有 10 个静态未闭合项，逐条解释见 `REPORT.md` 与 JSON。

交付：
1. `scratch/t109/out/big3_l3_join.json`
2. `scratch/t109/out/coverage_summary.json`
3. `scratch/t109/out/remaining_gaps.json`
4. `scratch/t109/out/REPORT.md`
5. `scratch/t109/out/DONE.md`
6. `scripts/t109_big3_l3_join.py`（accepted persistence 优先处理、误排除防护与逐项 gap reason）
