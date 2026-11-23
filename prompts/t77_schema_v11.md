# t77 — Schema v11 模块化合并 + 仓库治理(deepseek #1;唯一允许碰 reports/ 的车道)

你是受指挥官委派的子代理。E111–E119 验收包已入账(E119=指挥官负结果探测:t80 枚举增补前提证伪,见 LEDGER;E120=t76a stadium/team)(t76b 三连墙零落盘已弃,其 award/language/media 由 t83 吸收,本版不涉),公共 schema 停在 v10。本任务把九包成果**模块化合入 v11** 并做仓库治理。**你是本轮唯一被授权写 `reports/` 的车道**;`scratch/t01/LEDGER.json` 仍由指挥官记账,你不碰。

## 合并输入(E111–E119,全部已验收)

| E | 任务 | 成果 | 并入 v11 的节名(建议) |
|---|---|---|---|
| E111 | t71 | CLUB+0x100 链=table_extra_3 双档行框;22 cnst+Cebd+Cyfn 转正(club L3 21→43) | `club_extra_object_row`(t71 field_map_r3 + rows_extra3 摘要) |
| E112 | t72 | 三主表未命名槽位清单+指纹(partial) | `slot_fingerprints`(引 scratch/t72/out/,只放计数与键表) |
| E113 | t73 | 通用映射器+city/cont/regi/curr 四表闭环;alias group 否定结果 | `simple_tables`(t73 slots 摘要+方法边界) |
| E114 | t75 | nation 10 段文法闭合+99 槽裁决(新具名 L3=0) | `nation_segment_grammars`、`xref_reverse_adjudication` |
| E115 | t74 | 9 表双档行框+identity 自证 | `row_frames9`(表→(archive,header,footer,count,model,identity) 紧凑表) |
| E116 | t78 | 分母账本 110/1034=10.6% | **单拆文件** `reports/xml_denominator_coverage.json`(主 schema 只留指针) |
| E120 | t76a | stadium/team L2 槽位(t76a2 新会话交付) | `scan_tables` |
| E118 | t76c | derby/weather/lcrg/agreement L2 槽位 + derby 6B 差=3 字段、weather 95B=3+4×23 结构发现 | `scan_tables` |
| — | t76b | **弃**award/language/media(三连墙零落盘)→ 本版 `scan_tables` 节不含它们 | `pending:t76b(由 t83 接收)` |

## 任务

1. **builder** `scripts/t77_schema_v11.py`(`--build/--verify/--selftest`,退出码 0/1/2):
   - 读 `reports/club_nation_subtable_schema.json`(v10)→ 逐节 additive 合并(不改动既有节内容;upgrade 新节如上表)
   - `schema_version: 11`;`incremental_provenance` 追加 E111–E119;`coverage` 数字更新(club 主行 L3 43;t75 后不变;t78 分母指针)
   - **体积治理**:v11 主 JSON 只保留三主表+8 编号子表+CLUB_LINK+各 r2/r3 节;把 t73/t76 的 13 张非主表槽位结论写到 **`reports/other_tables_schema.json`**(独立文件,主 schema 里放路径指针+SHA-256);分母写 **`reports/xml_denominator_coverage.json`**
   - `--verify`:重读全部输入,校验每个新节的条目数与 LEDGER claim 一致(E111 24 项、E113 8 帧 17 L2、E115 9 表×2 档、E118 t76c 8 档 slots、E119 t76a stadium/team 等)
2. **治理杂项**:
   - 根目录若有 `nul` 文件(Windows 保留名事故产物)→ 删除
   - `README.md`/`docs/REPO_STATUS.md`/`docs/BASELINE.md` 增量段同步 v11 状态(数字引用 E 号,不改历史段落)
   - **merge-to-main 评估**:只写一节评估(REPO_STATUS 内:34 分支线性链、L4=0、快照远端差异),给出建议(建议/不建议+理由),**不执行 merge**
3. **回归**:t01 anchors 7/7;`baseline_coverage.py --check` 数字不变(分母单拆不影响冻结快照)
4. **文件写单次 ≤120 行**(分段写/append;t73 教训);大 JSON 由 builder 生成,不手写

## 避坑纪律

1. 只写:`reports/club_nation_subtable_schema.{json,md}`、`reports/other_tables_schema.json`、`reports/xml_denominator_coverage.json`、`README.md`、`docs/REPO_STATUS.md`、`docs/BASELINE.md`、`scratch/t77/`、`scripts/t77_*.py`;**其余 reports/docs 文件与 LEDGER 一律不碰**。
2. 既有节内容逐字节保留(只增不改);negative/held 原样;candidate 不写成结论。
3. 若某输入包缺文件(如 t76 车道未落盘项),对应节标 `pending:<E>`,不算失败,继续其余节。

## 交付 scratch/t77/out/

`verify_log.md`(build/verify 输出摘要)、`v11_diff_summary.json`(各节条目数前后对照)、`REPORT.md`、`DONE.md`(首行 `DONE type=t77 status=complete`)。

Python `py -V:3.12 -I -B`;不需要 FM24_DB_DIR。
