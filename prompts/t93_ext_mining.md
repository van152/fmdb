# t93 — 外部语料挖矿:三仓格式知识→JSON 资产(只读外源,禁执行)

你是受指挥官委派的子代理,**全新会话**。指挥官已完成外部侦察与锚交叉验证(E140):三个社区仓已克隆到本地,**纯参考资料,一律禁止执行、禁 pip install、禁 import 运行**——只许 Read/grep 读源码。

## 输入(只读;provenance 均已冻结)

- `scratch/ext/fmsave` @755fe9c(MIT,纯 Python):FM26/27 存档解析器,zstd 分节+块序列化。核心 `src/fmsave/_save.py`(3090 行)、`src/fmsave/readers/*`(31 表)、`src/fmsave/models/*`(字段语义)、`src/fmsave/_version.py`(per-build 布局门控)
- `scratch/ext/fm-editor` @ba605f4(GPL):FM24/26/27 内存布局。`docs/fm24/memory-layout.md`(我方版本!实体数组 RVA/stride/字段偏移:UID@0x284、FmString@0x2C0 等)、`src/fields/fm24/`
- `scratch/ext/FMLibreEditor` @fb76023(GPL):FM27 recon 20+ 篇(`docs/recon/`:object-pools/contracts/loans/transfers/names…)

## 任务(顺序;每步落盘;全部写 `scratch/t93/out/` 新文件;单次写 ≤120 行)

1. **10 分钟内**:写 `out/README.md` 骨架 + 三仓 provenance(commithash)
2. **fmsave 文法摘录**(核心):读 `_save.py` 的 section/header/table/record 文法与 zstd 用法、`_version.py` 布局门控机制 → `out/save_grammar.json`(每条带 file:line 溯源;摘录文法,不跑代码)
3. **字段字典**:`models/*` + `readers/*` 的字段名/类型/覆盖 → `out/field_dictionary.json`(表→字段→语义;players/staff/clubs/nations 优先)
4. **fm-editor FM24 摘录**:`docs/fm24/memory-layout.md` 全文 + `src/fields/fm24/` → `out/fm24_memory_layout.json`(实体数组/stride/对象字段偏移;注明"内存布局非 wire 格式")
5. **FMLibreEditor recon 摘录**:20+ 篇每篇 3-8 行要点 → `out/fm27_recon_digest.json`
6. **交叉对照**(held 级):我方冻结资产(E132 三列、E138 访问器模型、34 L3 slots、table_9 文法) vs 外部字典——命名接近/结构相似处逐条列 `out/crosswalk.json`,grade=held,**外部标签永不升级我方分级**
7. `out/verify.py`(独立,≥5 项:三仓 provenance 核对、摘录条目 file:line 存在性、字段字典计数、crosswalk 全 held、无执行外源代码的 grep 自证)+ `REPORT.md` + `DONE.md`(complete/partial)

## 避坑纪律

1. 只写 `scratch/t93/out/` 与 `scripts/t93_*.py`;不碰 reports/、LEDGER、scratch/cmd/、scratch/ext/(只读)
2. **外源代码零执行**:不许 python -m / import fmsave / 运行任何仓内脚本;摘录靠读
3. >20KB 不进会话;print ≤30 行;每节完成立即落盘;时间不够→partial DONE 列剩余
4. 候选不写成结论;外部内容与 CLI 输出均标 provenance=ext/<repo>@<hash>
5. `py -V:3.12 -I -B`(仅用于 verify.py 自检)

## 交付 scratch/t93/out/

`README.md`、`save_grammar.json`、`field_dictionary.json`、`fm24_memory_layout.json`、`fm27_recon_digest.json`、`crosswalk.json`、`verify.py`、`REPORT.md`、`DONE.md`。
