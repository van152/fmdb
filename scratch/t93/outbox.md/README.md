# t93 — 外部语料挖矿:三仓格式知识 → JSON 资产

只读外源。**外源代码零执行**(不 import、不 `python -m`、不跑仓内脚本、不 pip install);
本目录全部内容由 Read/grep 摘录 + 人工归纳产生。

## 三仓 provenance(commithash 已冻结)

| 仓 | commit | 日期 | 许可 | 本任务用途 |
|---|---|---|---|---|
| `scratch/ext/fmsave` | `755fe9c566bb0497d4ad6ef6e1ac1fd2fde7351b` | 2026-11-21 | MIT | FM26/27 存档(zstd 分节 + 块序列化)文法、字段字典 |
| `scratch/ext/fm-editor` | `ba605f4b64137dfc18940a69ecb2f523007f3ea8` | 2026-11-21 | GPL | FM24 **内存**布局(实体数组 RVA/stride/字段偏移) |
| `scratch/ext/FMLibreEditor` | `fb76023fc28c53ddc851ad1afdaf9879d3534d5c` | 2026-11-22 | GPL | FM27 recon 22 篇(`docs/recon/`) |

引用格式统一:`provenance=ext/<repo>@<hash>`。**外部标签永不升级我方分级**;
本目录 `crosswalk.json` 全部条目 grade = `held`。

## 交付

| 文件 | 内容 | 步 |
|---|---|---|
| `save_grammar.json` | 容器/分节/表/记录文法 + zstd 用法 + per-build 布局门控(每条 file:line) | 2 |
| `field_dictionary.json` | fmsave 表→字段→语义(players/staff/clubs/nations 优先) | 3 |
| `fm24_memory_layout.json` | FM24 实体数组/stride/对象字段偏移(**内存布局,非 wire 格式**) | 4 |
| `fm27_recon_digest.json` | FMLibreEditor 22 篇 recon 每篇 3–8 条要点 | 5 |
| `crosswalk.json` | 我方冻结资产 vs 外部字典,逐条 held 级对照 | 6 |
| `verify.py` | 独立校验(provenance / file:line 存在性 / 计数 / 全 held / 零执行自证) | 7 |
| `REPORT.md` / `DONE.md` | 结论与完成状态 | 7 |

## 边界

- 只写 `scratch/t93/outbox.md/` 与 `scripts/t93_*.py`;不碰 `reports/`、`LEDGER`、
  `scratch/cmd/`、`scratch/ext/`(只读)。
- 本目录**不产生新证据等级**:外部内容一律候选/参考,不写成结论。
- 我方基线引用自 `scratch/t92/out/schema_v113.json`(E132 三列 / E138 访问器模型 /
  34 L3 slots / table_9 文法),只读不改。
