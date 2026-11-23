# t87 — Schema v11.1 增量:E121(t82)补录(15 分钟轻任务,deepseek)

你是受指挥官委派的子代理。v11(t77 车道产物)停在 E120;E121(t82)交付在发车之后,需要一次 **additive-only** 增量合入。这是 15 分钟轻任务,**严禁整读大文件**——一切用脚本程序化处理,单次文件写 ≤120 行。

## 输入(全部已验收落账)

- `reports/club_nation_subtable_schema.json`(v11,t77 车道刚生成;若尚不存在则本任务标 `pending:t77` 收尾退出,不算失败)
- `scratch/t01/LEDGER.json` 的 E121 条目(程序化读,取 claim/evidence)
- `scratch/t82/out/field_map.json`(35 新 L3 + 39 held 计数)与 `REPORT.md`(只读头部摘要,程序化 grep)

## 任务

1. `scripts/t87_v11_patch.py`(`--build/--verify/--selftest`,退出码 0/1/2):
   - `schema_version: 11` → `11.1`;`incremental_provenance` 追加 E121(引用 LEDGER 条目,不复制全文)
   - 新节 `club_extra3_l3_e121`:35 新 L3 的 4CC 列表 + 39 held 计数 + CBW*/CBD*→table_45 正名结论(引用 `scratch/t82/out/field_map.json` 路径,不复制大对象)
   - `coverage` 增量:club 主行+extra_3 对象 L3 计数 43→78;分母注记:club.xml[211..327] 117 项记录族 wire 家=server table_45(E116 账本的 239 未解 club occurrence 相应缩小)
   - **既有节内容逐字节不动**(只增不改);negative/held 原样
2. `--verify`:重读 v11 与 t82 产物,校验条目数(35/39/131)与 LEDGER claim 一致
3. `README.md`/`docs/REPO_STATUS.md` 若 t77 已更新到 v11,只追加一行 v11.1 状态(引用 E121);未更新则跳过

## 避坑纪律

1. 只写:`reports/club_nation_subtable_schema.json`(及 .md 若需同步)、`scratch/t87/`、`scripts/t87_*.py`、上述两文档的一行追加;**其余 reports/docs 与 LEDGER 一律不碰**
2. v11 主 JSON 体积大(>20KB),用 `json.load` 程序化改,禁止人读整文件
3. `py -V:3.12 -I -B`;不需要 FM24_DB_DIR

## 交付 scratch/t87/out/

`verify_log.md`、`REPORT.md`、`DONE.md`(首行 `DONE type=t87 status=complete`)。
