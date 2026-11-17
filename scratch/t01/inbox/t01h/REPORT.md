# t01-h factory 跳表普查

## 结论

- `editor.exe` 只读静态扫描：factory dispatch 在 `0xf48b38: 83 f9 49`（`cmp ecx,0x49`），故有效 type-id 为 **0..73，共 74 项**；`0xf48b45: 48 8d 0d ec 11 00 00` 推出 rel32 表基址 `0xf49d38`。跳转用 `base + sign_extend(rel32)`，不是 `entry + rel32`。逐项入口、handler、分配/构造证据、RTTI/COL、slot 7/19 与 mode 见 `output.json`。
- 74 项落到 **60 个不同 handler**；11 个 type-id（11,13,15,16,17,20,28,40,53,54,55）共用 `0xf49ca9` 空结果路径。另有 handler 别名：45/48、65/67/68/69。故跳表项数不能等同 XML 实体数。
- mode 按 reader entry 后最多 0x800 字节及直接 serializer callee 分类：46 straight-line、7 count-loop、7 mixed、14 unclear（包含空返回/非记录类）。负对照复现：type-25 COMP = **straight-line**；type-10 NATION = **count-loop**。

## 代表字节链

- COMP：`0xf49d9c: f1 f3 ff ff` → handler `0xf49129`；`0xf49129: b9 b0 01 00 00` 请求 0x1b0，`0xf49139: e8 72 cc f6 ff` 调 ctor `0xeb5db0`。ctor `0xeb5dd5` 写 vptr `0x187d2b8`，RTTI `.?AVCOMP@db@@`。slot19 指针 `0x187d350: 40 14 ed 40 01 00 00 00` → reader thunk `0xed0a40` → body `0xeb7000`，直线宽度序列，无计数循环。完整 call/vptr/query/reader 字节在 JSON type 25。
- NATION：`0xf49d60: ef f1 ff ff` → handler `0xf48f27`；`0xf48f27: b9 d8 01 00 00` 请求 0x1d8，`0xf48f37: e8 b4 5c 0f 00` 调 ctor `0x103ebf0`。vptr `0x18889b8` 的 COL 指针在 `0x18889b0: b0 95 88 41 01 00 00 00`，RTTI 名在 `0x1aacac0`；slot7 `0x104e4b0: b8 0a 00 00 00 c3` 返回 10；slot19 `0x1888a50: c0 04 04 41 01 00 00 00` → reader `0x103fac0`，有循环。详见 JSON type 10。

## 32 个 master entity 对齐 / t01e 交叉核对

- RTTI 名精确映射 **18/32**；type-id 1 的 person-family 与 type-id 24 的 team-family 只能列候选，合并后候选覆盖 **29/32**。仍未关联（连候选也无）：`CntF`、`alnm`、`dscr`。JSON 保留每项的 RTTI→entity matched/candidates，未将候选提升为结论。
- t01e 报 12 个 confirmed entities。本次 RTTI/COL 字节精确吻合 8 个：`awar/club/comp/drbr/inju/mdso/stad/weat`；`agen/offc/jour` 的虚表与 type-id 1 是 family 候选，不是 handler 的 `BASIC_PERSON` vptr 等同证明。
- **t01e 的 nati 标签与 RTTI 不符，按 COL 字节裁决并保留负结果**：t01e 的 `table_off=0x1888ed0`（vptr `0x1888ed8`）COL 名为 `.?AVNATIONAL_TEAM_CONTAINER@db@@`，slot7 在 `0x10730d0: b8 09 00 00 00 c3` 返回 9；`table_off=0x188db40`（vptr `0x188db48`）COL 名为 `.?AVTEAM_CONTAINER@db@@`，slot7 在 `0x866f0: b8 ff ff ff ff c3` 返回 `0xffffffff`。两者均非 NATION/type 10。相对地，真正 NATION vptr 是 `0x18889b8`、slot7 返回10（上节）。JSON 同时保存 t01e 标注、COL/RTTI、slot7 原字节；不把 t01e 的 nati 标签写成已核实。

## 旧 TABLE_HINTS 与边界

- 冻结快照 SHA-256 已对照 `evidence/MANIFEST.json`。table 8/language、10/nation、21/stadium、25/competition、41/currency 与相应 RTTI/type-id 有候选或交叉支持；table 56 的旧快照明确语义 unknown。虽然 factory type-id 56 RTTI 为 AGREEMENT，**不据此断言 table 56 = agreement**。快照路径与哈希在 JSON `sources.verified_frozen_snapshots` / `old_table_hints`。
- 分配值是 allocator request size（wrapper `mov edx,N` 或调用者 `mov ecx,N` 字节证据）；非 allocator 形状者标 candidate/unclear。内部 `STARTING_*`、history、container 类不是 master schema entity 的直接映射。无游戏、Editor、IDA 执行；未装依赖；未改既有账本。

## 复验

```powershell
py -V:3.12 -I -B scratch/t01/inbox/t01h/verify.py --help
py -V:3.12 -I -B scratch/t01/inbox/t01h/verify.py --selftest
```

`--selftest` 重建 74 项并检查 COMP/NATION 分类负对照及 t01e 的 nati/RTTI 冲突；`--write` 只写同目录 `output.json`。
