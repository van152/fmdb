# t44 DONE

状态：`shared_named_auxiliary_closed`。`Cafl` 与 `Cvfl` 共用 `CLUB_LINK*` 集合，持久化在 `server_db/club_links.dat`；无数字 table_type、entry RTTI/vptr 或 slot 19。Server `12 + 9,261 × 47 = 435,279` B，全表闭合；client 无成员。Cvfl 的 `clfr` 由运行时生成，副本生成处不按校验成功过滤。

字段：Cafl 26/29 L3，Cvfl 16/19 L3（含共享 occurrence，不重复计独立 wire 槽），L4=0。`type=21`、`yfee=-1`、`msls` 全空及 `clfr` runtime-only 保留边界。t35 原 JSON 与 REPORT 原样保留，独立 verifier 核对 SHA。

交付：
- `scratch/t44/out/discovery_cafl_cvfl.json` — 静态链、两视图和归档归属判定。
- `scratch/t44/out/cursor_club_links.json` / `fields_cafl_cvfl.json` — 精确 wire 游标、域画像、分支引用、分级与首反例。
- `scratch/t44/out/instructions.part001.json`…`part007.json`；`branches.part001.json`…`part003.json` — 原指令/VA/bytes，49 条可达条件分支分类。
- `scratch/t44/out/verify.py`、`scratch/t44/out/REPORT.md`、`scratch/t44/out/DONE.md`。
- `scripts/t44_cafl_cvfl.py` — builder。

运行记录：Python 3.12 隔离模式 `-I -B`，`FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data`。Builder 与 verifier 实跑 PASS，各自 `--help` / `--selftest` PASS，`scripts/t01_anchors.py` **7/7 PASS**。未联网、未启动游戏/编辑器/IDA、未访问 Z:。
