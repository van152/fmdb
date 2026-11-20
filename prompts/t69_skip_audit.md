# t69 — Skipped/static-untriggered 账目审计(t57/t59 尾账,sol;L2 文档任务)

你是受指挥官委派的子代理,做**小而精**的账目审计,把 t57/t59 留下的"跳过/未触发"尾账逐项闭环到证据引用:

1. **club skipped_separate_member 10 项**(t57 grade_counts):逐项给出"哪个已闭子表/独立成员承接"的证据表(schema v8/v9 的 club 8 表+CLUB_LINK 条目级引用);任何一项找不到承接者 → 升级为悬案条目(候选不入结论)。
2. **comp 2 个静态未触发 payload**(+0xa8/+0xe0,t59):静态分支谓词摘录 + 数据侧双档全 0 复核。
3. **comp vec30 全 0** 与 `+0x100` i16 count×5 的现状台账:值分布 + 是否在 t66 已定性(若 t66 已交付,引用其条目;未交付则只做数据侧台账)。
4. **nation held 4(Necf/Nygn/Ngct/Nsod)与 t61 交叉**:若 t61 已交付,引用其判定;未交付则台账现状(不重判)。
5. 产出一份 **三表尾账总表**(skipped/held/static-zero/edge-pending × 证据引用 × 承接任务),供 schema 折叠与晨报引用。

## 必读
- AGENTS.md;reports/club_nation_subtable_schema.json(最新版);scratch/t57/out/field_map.json;scratch/t59/out/field_map.json + field_slots.json;scratch/t50/out/REPORT.md(账目口径)
- scratch/t61/t66/t68 的 out/(存在则引用,不存在则如实记 pending)

## 交付 scratch/t69/out/
- tail_ledger.json(逐项:id/table/kind/evidence_refs/grade/承接)、SUMMARY.md、REPORT.md、DONE.md;verify.py(--help/--selftest,退出码 0/1/2)

边界:只读已交付产物+数据侧复核,不重做任何普查;不启动游戏/编辑器/IDA,不联网,不读写 Z:。Python `py -V:3.12 -I -B`;FM24_DB_DIR=<WORKSPACE>/scratch/data。
