# t77-fix1 — Schema v11 合版(全新会话;严禁整读大 JSON,交付先行)

你是受指挥官委派的子代理,**全新会话**。前一轮 40 分钟撞墙零落盘——把 v10 schema(数百 KB)与九个任务包往会话里整读烧光了窗口。本会话铁律:

## 铁律(违反即任务失败)

1. **任何 >20KB 的文件不进会话上下文**:`reports/club_nation_subtable_schema.json`(v10)、各任务大 JSON、LEDGER 全部用脚本 `json.load` 程序化处理,只 print 摘要(节数、条目数、差集大小),print 每次 ≤30 行。
2. **10 分钟内先落盘**:`scratch/t77/out/v11_diff_summary.json` 骨架 + builder 骨架;再逐步充。单次文件写 ≤120 行,分块追加。
3. 合并只做 **additive**:读 v10 的节键列表(程序化 print),新节全部由 builder 构造,不手写大 JSON。

## 任务(顺序)

1. `scripts/t77_schema_v11.py`(`--build/--verify/--selftest`,退出码 0/1/2):
   - 读 v10 → `schema_version: 11`;`incremental_provenance` 追加 E111–E120(程序化读 `scratch/t01/LEDGER.json` 取每条 id+claim.scope,**不复制全文**)
   - 新节(每节由 builder 从对应包构造,主 schema 只存摘要+指针):
     - `club_extra_object_row`(t71:24 项转正摘要+行框指针)
     - `slot_fingerprints`(t72:计数与键表)
     - `simple_tables`(t73:四表闭环摘要+alias 否定)
     - `nation_segment_grammars`+`xref_reverse_adjudication`(t75:99 槽裁决摘要)
     - `row_frames9`(t74:9 表×双档紧凑表)
     - `scan_tables`(t76a stadium 12/47 槽 + t76c derby/weather/lcrg/agreement;**t76b 已弃**,节内标 `pending:t76b(由 t83 接收)`)
     - `club_base18_forwarded_6`(t79:六字段转发双链摘要)
     - 指针节:`xml_denominator_coverage` → `reports/xml_denominator_coverage.json`(由 t78 buckets.json 生成独立文件,主 schema 存路径+SHA-256)
     - 指针节:`other_tables_schema` → `reports/other_tables_schema.json`(t73/t76 的 13 张非主表槽位结论)
   - **体积治理**:v11 主 JSON 只留三主表+8 编号子表+CLUB_LINK+各 r2/r3 节+上述新节;两个指针文件单独生成
2. 治理:根目录若有 `nul` 文件→删除;`README.md`/`docs/REPO_STATUS.md`/`docs/BASELINE.md` 增量段同步 v11(数字引用 E 号,不改历史段);merge-to-main 评估一节(REPO_STATUS 内,不执行 merge)
3. 回归:`scripts/t01_anchors.py` 7/7;`baseline_coverage.py --check` 数字不变
4. `REPORT.md` + `DONE.md`(首行 `DONE type=t77 status=complete`)+ `scratch/t77/out/verify_log.md` + `v11_diff_summary.json`

## 避坑纪律

1. 只写:`reports/club_nation_subtable_schema.{json,md}`、`reports/other_tables_schema.json`、`reports/xml_denominator_coverage.json`、`README.md`、`docs/REPO_STATUS.md`、`docs/BASELINE.md`、`scratch/t77/`、`scripts/t77_*.py`;其余 reports/docs 与 LEDGER 不碰
2. 既有节逐字节保留;negative/held 原样;candidate 不写成结论
3. 输入包缺文件→对应节标 `pending:<E>`,继续其余节
4. `py -V:3.12 -I -B`;不需要 FM24_DB_DIR
