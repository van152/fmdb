# t93 DONE — status: **complete**

外部语料挖矿三仓(fmsave / fm-editor / FMLibreEditor)全部按序完成,**零执行外源代码**,
交付 9 个文件,`verify.py` 9/9 全绿。

## 交付清单

| # | 文件 | 大小 | 状态 |
|---|---|---|---|
| 1 | `README.md` | 2.0 KB | ✅ 骨架 + 三仓 provenance + 边界 |
| 2 | `save_grammar.json` | 15.1 KB | ✅ 30 条文法 G01–G30 / 65 锚点 / 9 源文件 |
| 3 | `field_dictionary.json` | 192 KB | ✅ 58 实体 / 720 字段 / 34 readers |
| 4 | `fm24_memory_layout.json` | 72.8 KB | ✅ 270 字段 + 15 子记录 + 30 curated fact |
| — | `fm24_fields.json` | 63.9 KB | 中间产物(同 270 字段,无 curated fact),非交付物 |
| 5 | `fm27_recon_digest.json` | 23.3 KB | ✅ 22 篇 / 102 行锚要点 |
| 6 | `crosswalk.json` | 29.2 KB | ✅ 20 条,**全 held**,0 分级变动 |
| 7 | `verify.py` | 11.6 KB | ✅ 9 项校验,9/9 PASS |
| 8 | `REPORT.md` | — | ✅ 结果与结论 |
| 9 | `DONE.md` | — | ✅ 本文件 |

生成脚本(只读,不 import 外源):`scripts/t93_fields.py`、`scripts/t93_fm24.py`、
`scripts/t93_recon.py`、`scripts/t93_crosswalk.py`。

## verify.py 结果

```
PASS  1 three repos at the frozen commits
PASS  2 provenance strings name the frozen commits
PASS  3 internal baseline artifacts unchanged (read-only respected)
PASS  4 save_grammar evidence lines exist (30 entries, 65 anchors)
PASS  5 fm24_memory_layout lines exist (300 anchors) and declares memory!=wire
PASS  6 recon digest: 22 docs, 102 line-anchored points
PASS  7 field_dictionary self-consistent (58 entities, 720 fields)
PASS  8 crosswalk fully held (20 entries, 0 grade moves)
PASS  9 no external execution; 4 t93 scripts + outbox contents
```

## 纪律核对

- **零执行**:未 `import fmsave`、未 `python -m`、未跑任何仓内脚本、未 `pip install`;
  `verify.py` 第 9 项对 4 个脚本 + 自身做禁用模式扫描,并对 `scratch/ext` 只允许 `read_text`。
- **只写两处**:`scratch/t93/outbox.md/` 与 `scripts/t93_*.py`。`reports/`、`LEDGER`、
  `scratch/cmd/`、`scratch/ext/` 未动(第 3 项以 sha256 侧证三份基线未漂移)。
- **provenance 全覆盖**:每个外部条目带 `ext/<repo>@<40 hex>`,与三仓 HEAD 逐一核对(第 1、2 项)。
- **外部标签不升级**:`crosswalk.json` 20/20 `held`,`grade_moves: 0`;`our_side.grade` 白名单
  `L1|L2|L3|held|n/a`,并显式禁止 `verified` / `unconfirmed` / `ext_status` 这类外部词(第 8 项)。
- **候选不写成结论**:外部冲突原样保留(fmsave 命名 18 = Continental Cup Goalkeeper vs
  FMLibre 记为 18 从未出现;`0x22` shutout vs 34 clean sheet),不裁不并。

## 已知限制

1. `save_grammar.json` 覆盖容器/分节/表/记录/zstd/门控;**未摘** `cli.py`、`export.py`(与格式无关)。
2. `fm24_memory_layout.json` 只取 FM24;fm-editor 的 `src/fields/fm26*`、`fm27*` 未摘。
3. FMLibre 只摘 `docs/recon/` 22 篇,非 recon 文档未摘。
4. stadium 数组根在 fm-editor 中未定位(`rva_stadium_base=0`),我方 JSON 照实记录该缺口,
   未做任何推断。
5. `field_dictionary.json` 中 `PlayerSeasonStats` 的登记表含 14 个非字段名(计算/派生列),
   已单列在 `status_names_not_a_field`,不计入 `verified_count`。

以上 5 条均为**范围裁剪**,不是未完成项;三项交付物在各自声明范围内完整。
