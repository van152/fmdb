# t80-fix1 — 枚举增补字典(全新会话;严禁整读大 JSON)

你是受指挥官委派的子代理,**全新会话**。前一轮 40 分钟撞墙零落盘——死因是把 308KB 的 enums.json 往会话里整读,烧光了窗口。本会话铁律:

## 铁律(违反即任务失败)

1. **任何 >20KB 的文件不进会话上下文**(enums.json 308KB、enum_extras.json 92KB、master.json、LEDGER.json 全部在此列)。要合并/求差/查键,写 `scripts/t80_enum_supplement.py` 用 `json.load` 程序化处理,只 print 摘要(条数、键样本、差集大小)。
2. **10 分钟内先落盘**:写 `scratch/t80/out/enum_supplement.json` 骨架(meta+counts+前几条),再逐步充。任何单次文件写 ≤120 行,分块追加。
3. builder 先行:脚本只读以下文件(全部程序化):
   - `evidence/fm24/reports/editor_schema/enum_extras.json`、`enums.json`、`database_ui.json`(SHA-256 查 `evidence/MANIFEST.json`,也是程序化读)
   - `evidence/fm24/reports/editor_schema/master.json` 的 `enums`(304 个,求差集用脚本,不要人读)
4. 输出打印控制在每次 ≤30 行。

## 任务(顺序)

1. `scripts/t80_enum_supplement.py`(`--build/--verify/--selftest`,退出码 0/1/2):
   - 合并 enum_extras + enums(+EXE_ENUMS.md 机器可读行),键=scoped enum 名,值=值域+值名+来源+MANIFEST SHA-256;master 已有的不覆盖只补缺,每条带 provenance
   - 产出 `scratch/t80/out/enum_supplement.json`(大文件由脚本生成,不手写)
2. **自动重扫 t61**:程序化读 `scratch/t61/out/` 的 67 条无源 held 台账,逐条查增补字典,命中且域自洽→候选升级表(建议 L3,注明静态槽不变);仍无源→保持 held+`字典未含` 标记。产出 `scratch/t80/out/rescan_t61.json`
3. **自动重扫 t75**:程序化读 `scratch/t75/out/xref_reverse.json`,对 Ccre/cosr/Npop/Ncpi/CICF 等未冻结 4CC:field_codes/增补字典里的 locations、值域 vs 枚举域,给裁决候选。产出 `scratch/t80/out/rescan_t75.json`
4. 交叉复核:master enum 缺口(如 continent DBvw 空名枚举)若增补字典能补值名,单独一节
5. `REPORT.md` + `DONE.md`(首行 `DONE type=t80 status=complete`);`--verify` 重跑计数对拍

## 避坑纪律

1. 只写 `scratch/t80/` 和 `scripts/t80_*.py`;不碰冻结 master.json、reports/、LEDGER。
2. 负结果原样保留;候选不写成结论;enum 值域不自洽的降 candidate。
3. `py -V:3.12 -I -B`;不需要 FM24_DB_DIR。

## 交付 scratch/t80/out/

`enum_supplement.json`、`rescan_t61.json`、`rescan_t75.json`、`REPORT.md`、`DONE.md`、`verify.py`。
