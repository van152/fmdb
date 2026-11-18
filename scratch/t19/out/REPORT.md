# t19 — club/nation cursor_layout 重建（partial）

## 结论 / 状态

- `status=partial_cursor_club_frame_closed_nation_prefix_only`。按要求先拆结构；没有把未闭合的 reader 路径伪装成 E20 式全量字段序列。
- club 的 **行框架** 可复算并封口：84,259 行、3 个 compact body 未解；但 `mixed / dual RTTI` reader 的 41 个 transfer calls 含动态 helper/分支，未与完整 row cursor 对齐。表型证据分开记录：CLUB slot19 `0xe5a7a0`；LEAGUE_BODY_CLUB thunk 解包到 `0x43beba0`，另见 4B/1B 对象传输。无逐行 class selector。
- nation 复建出 t01g 的 25B 前缀（10 transfers，width sum=25）及 7 个字段；后续 count/helper 循环体线宽、每行边界仍未知。总 payload 包络能闭合，不等于逐行 loop closure。

## club 结构图

```text
row+0  db_id u32 | +4 parent/ref u32 | +8 duplicate/Cccn? u32 | +12 duplicate u32
+16  class split: CLUB 5B  OR  LEAGUE_BODY_CLUB 4B + separate +20 byte
+20/21 group/status u32 | +24/25 flag byte | (4B track only: +25 unassigned byte)
+26  full-name byte length u32 | +30 UTF-8 full name [N]
+30+N short-name byte length u32 | +34+N short name [M]
+34+N+M unresolved 3B | row_end-13 identity suffix 12B | row_end-1 marker
```

Standard row equation: `row_length = 50 + N + M`. Samples in `club_v2/output.json` satisfy it; all 84,256 standard rows and the 3 compact rows sum to 84,259. Parser footer: `0x69c66a + 8 = 6,932,082`; `footer_exact=true`. The contiguous class split is accepted in the upstream artifact but **not** chosen by a proven per-row discriminator. Compact rows 69706..69708 remain identity-framed only.

`Cccn@+8/4` is carried as `L3_inherited`, not a t19 discovery. The prior local reader bytes point at object `+0xf0`, width 4, getter cmp Cccn; however `codes_full.json` has only a `path_descend` record (no direct object_off read), the type-3 width trace has no object offset 240, and sample row 69709 has `row+8 == row+0`. Therefore Cccn is low-confidence and does not validate the reader/frame merge. The E20-like cumulative row layout is **not** an alignment of 41 C++ transfers.

## nation 结构图

```text
body+0..24: 1,4,4,4,4,1,1,4,1,1 = 25B
body+24: scratch/count byte (sample 3) -> helper item loop (wire width unknown)
then: u32 count -> loop body unresolved
separate arg8!=0 branch: u16 count -> repeated 4B transfer; client/server assignment unproven
```

The 40-call `reader_widths` trace aligns calls 15..23 to the first nine prefix steps (width and object offsets); call 24 is also 1B but writes to object+0x44 rather than t01g's stack scratch byte. Calls 0..14 belong to an unreconciled path; calls 25..39 follow count-driven blocks and have no safely assignable row offsets. t01g explicitly records `complete_rows_verified=0`; its 7 prefix fields are inherited as L3, not promoted to a complete row parser. Table envelope `14+24,710+8=24,732` is a payload boundary check only. The required loop-body step and count closure remain blocked.

## 命名率与台账

- club: t18 baseline 14/672 → t19 ledger 15/672 (2.23%). Difference is only carried `Cccn`; **0 new independent L3 mappings**. All old 14 entries retain their t18 grade/evidence and are marked not revalidated against the reconstructed cursor.
- nation: t18 baseline 0/441 → t19 7/441 (1.59%); the seven t01g prefix mappings are inherited. Remaining 434 fields stay `unnamed`.
- Full schema ledger entries include top-level and nested fields; `fields_*.json` are manifests and `.partNNN.json` are ≤100-field shards.

## 校验 / 未闭合项

`verify.py --selftest` validates formulas and instruction-byte decoding. Default verification checks club footer/sample closure, nation prefix sequence, schema baseline comparison and payload envelope. It returns code 1 because per-row nation loop closure and club reader-to-frame alignment are still unproven.

证伪/保留：不把 club 5B byte-walker aggregate 等同语义 5B 字段；不按 ordinal/marker/name 推断 class；不把 t01g 的 arg8 分支命名为 client/server；不把 251 行与全 payload envelope 当成 251 个 row-start 已恢复。

## 来源与冻结快照

- `scratch/t02/inbox/club_v2/output.json`, `scratch/t05/reader_widths.json`, `scratch/t05/schema_inventory.json`, `scratch/t12/out/codes_full.json`, `scratch/t18/out/fields_*`.
- `scratch/t01/inbox/t01g/output.json` 与 `scratch/t01/inbox/t01g/REPORT.md`; table_10 locator: `evidence/fm24/reports/dbdat_decode/client_table_10_nation_locator.json`.
- schema snapshot `evidence/fm24/reports/editor_schema/master.json`, SHA-256 `7d57477e144d5359ccde64bb24b3ba7c640ef41738ed196eba8a38e792776eda`; compared to `evidence/MANIFEST.json` (snapshot date 2026-11-18).
- 未联网，外部输入只读；所有新文件仅落于 `scratch/t19/out/` 与 `scripts/t19_build.py`。
