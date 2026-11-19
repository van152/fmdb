#!/usr/bin/env python3
"""t58 指挥官独立抽查 — schema v7→v8 合并验收(不 import worker 代码)。

checks:
  1. reports/ v8 JSON/MD SHA == DONE 宣称
  2. out/ v7 快照 == git HEAD reports/(E96 时点)且 SHA 与 REPORT 宣称一致
  3. 保护节 v7→v8 逐值不动(深层相等;generated_by=t56→t58 为预期 fold 增量,不保护)
  4. club 子表口径不动(L3_occurrences 94 等)
  5. club_main_row_fields 数字断言(6932082/16595312/84259/12B/13 L3/72 倒置/69705/E60)
  6. coverage club_main_row_* 分项 + aligned 18
  7. provenance t57/E97/L3 + 条目级守卫 E84,E85,E87,E89–E97 canonical claim SHA 复算
  8. markdown v8 = v7 前缀 + 增量
  9. L4=0
退出码 0=全过 1=失败 2=用法错。
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path("D:/tmp2b/fm24-db")
SCHEMA = ROOT / "reports/club_nation_subtable_schema.json"
SCHEMA_MD = ROOT / "reports/club_nation_subtable_schema.md"
SNAP_JSON = ROOT / "scratch/t58/out/club_nation_subtable_schema.v7.json"
SNAP_MD = ROOT / "scratch/t58/out/club_nation_subtable_schema.v7.md"
LEDGER = ROOT / "scratch/t01/LEDGER.json"

EXPECT_JSON_SHA = "76da94d4376613a9e649a32d3bfc415f19596d4c7fb1c7c861d60b5951770cbf"
EXPECT_MD_SHA = "5067502eadd489fac0e9842c6ece45e8402ff656e43d41e721522714308737f6"
V7_JSON_SHA = "d93a5070489c737e5d70fa2b8ffb135f9d4135d70df7ae4b6e2d27a4379ded10"
V7_MD_SHA = "f84d265c2ca067794bd98f8ddb15cda026dc2b63bd185bd3db0eab43bd6b83bc"
GUARD_IDS = ["E84", "E85", "E87", "E89", "E90", "E91", "E92", "E93", "E94", "E95", "E96", "E97"]

PROTECTED_TOP = [
    "tables", "negative_regressions", "v3_baseline", "club_auxiliary_sources",
    "nation_static_side", "nation_t9_wire", "nation_main_row_fields",
    "nation_data_side_status", "evidence_grade_policy", "schema_id",
    "schema_provenance", "binary_provenance", "inventory_reconciliation",
    "source_artifacts",
]

fails: list[str] = []


def check(name: str, ok: bool, why: str = "") -> None:
    print(("PASS " if ok else "FAIL ") + name + (f"  ({why})" if why and not ok else ""))
    if not ok:
        fails.append(name)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canon(value) -> str:
    return sha(json.dumps(value, ensure_ascii=False, sort_keys=True,
                          separators=(",", ":")).encode("utf-8"))


def git_blob(path: str) -> bytes:
    return subprocess.run(["git", "-C", str(ROOT), "show", f"HEAD:{path}"],
                          capture_output=True, check=True).stdout


def main() -> int:
    v8_raw = SCHEMA.read_bytes()
    v8_md_raw = SCHEMA_MD.read_bytes()
    check("1a.v8.json.sha", sha(v8_raw) == EXPECT_JSON_SHA, sha(v8_raw))
    check("1b.v8.md.sha", sha(v8_md_raw) == EXPECT_MD_SHA, sha(v8_md_raw))

    v7 = json.loads(SNAP_JSON.read_bytes())
    v7_md = SNAP_MD.read_bytes()
    check("2a.v7snap.json==HEAD", sha(SNAP_JSON.read_bytes()) == sha(git_blob("reports/club_nation_subtable_schema.json")))
    check("2b.v7snap.md==HEAD", sha(v7_md) == sha(git_blob("reports/club_nation_subtable_schema.md")))
    check("2c.v7snap.json.sha", sha(SNAP_JSON.read_bytes()) == V7_JSON_SHA)
    check("2d.v7snap.md.sha", sha(v7_md) == V7_MD_SHA)

    v8 = json.loads(v8_raw)
    check("3a.v8.version", v8["schema_version"] == 8, str(v8["schema_version"]))
    check("3b.generated_by_fold_delta", v7.get("generated_by") == "t56" and v8.get("generated_by") == "t58",
          f"{v7.get('generated_by')}->{v8.get('generated_by')}")
    for key in PROTECTED_TOP:
        check(f"3.{key}", key in v7 and key in v8 and v7[key] == v8[key])
    cov7, cov8 = v7["coverage"], v8["coverage"]
    new_main_keys = {k for k in cov8 if k.startswith("club_main_row_")} - {k for k in cov7 if k.startswith("club_main_row_")}
    for key in sorted(set(cov7) & set(cov8)):
        check(f"4.cov.{key}", cov7[key] == cov8[key])
    check("4a.club_L3_occurrences94", cov8.get("club_L3_occurrences") == 94, str(cov8.get("club_L3_occurrences")))
    check("4b.club_L3_unique59", cov8.get("club_L3_unique_wire_fields") == 59, str(cov8.get("club_L3_unique_wire_fields")))
    check("4c.club_tables8", cov8.get("club_tables") == 8, str(cov8.get("club_tables")))
    print(f"    [i] v8 新增 coverage 主行分项: {sorted(new_main_keys)}")

    cmr = v8["club_main_row_fields"]
    check("5a.cmr.task", cmr.get("source_task") == "t57", str(cmr.get("source_task")))
    check("5b.cmr.ledger", cmr.get("acceptance_ledger_entry") == "E97"
          and cmr.get("acceptance_ledger_level") == "L3",
          f"{cmr.get('acceptance_ledger_entry')}/{cmr.get('acceptance_ledger_level')}")
    census = cmr.get("field_census", {})
    check("5c.census.fields_total433", census.get("fields_total") == 433, str(census.get("fields_total")))
    check("5c2.census.aligned18", census.get("fields_with_unique_XML_alignment") == 18,
          str(census.get("fields_with_unique_XML_alignment")))
    check("5d.census.l3_13", census.get("grade_counts", {}).get("L3") == 13, str(census.get("grade_counts")))
    check("5e.census.held11", census.get("grade_counts", {}).get("held") == 11)
    check("5f.census.skipped10", census.get("grade_counts", {}).get("skipped_separate_member") == 10)
    check("5g.census.unmapped399", census.get("grade_counts", {}).get("unmapped") == 399)
    check("5h.L3_fields_len13", len(cmr.get("L3_fields", [])) == 13, str(len(cmr.get("L3_fields", []))))
    order = cmr.get("order", {})
    check("5i.inversions72", order.get("inversions") == 72, str(order.get("inversions")))
    check("5i2.first_inv_Cext_Cnam", order.get("first_counterexample") == [[3, 13, "Cext"], [10, 6, "Cnam"]],
          str(order.get("first_counterexample")))
    osc = cmr.get("outer_sequence_closure", {})
    check("5j.positions34", osc.get("positions") == 34, str(osc.get("positions")))
    reader = osc.get("reader", {})
    check("5k.reader1412_167_slot19", reader.get("reachable_instructions") == 1412
          and reader.get("conditional_branches") == 167 and reader.get("vtable_slot") == 19,
          str({k: reader.get(k) for k in ("reachable_instructions", "conditional_branches", "vtable_slot")}))
    modes = osc.get("archive_modes", {})
    mode_txt = json.dumps(modes, ensure_ascii=False)
    check("5l.client6932082", "6932082" in mode_txt, mode_txt[:120])
    check("5m.server16595312", "16595312" in mode_txt, mode_txt[:120])
    ident = cmr.get("identity_framing", {})
    check("5n.identity12B", ident.get("native_tail_width") == 12 and ident.get("layout") == "ordinal | UID | UID"
          and str(ident.get("footer_hex", "")).endswith("e3c03a77"),
          str({k: ident.get(k) for k in ("native_tail_width", "layout", "footer_hex")}))
    check("5n2.rows84259", ident.get("selector_counts", {}).get("0") == 84256
          and ident.get("selector_counts", {}).get("12") == 3, str(ident.get("selector_counts")))
    cmr_txt = json.dumps(cmr, ensure_ascii=False)
    check("5o.neg69705_in_cmr", "69705" in cmr_txt, "69705 不在 club_main_row_fields 子树")
    neg = cmr.get("negative_regressions_preserved", {})
    check("5p.E60_verbatim", "E60_original_Cccn_negative" in neg and "true_binding_note" in neg
          and "low-confidence candidate" in neg.get("E60_original_Cccn_negative", ""),
          str(sorted(neg.keys())))

    check("6a.cov.newL3_13", cov8.get("club_main_row_new_L3") == 13 or cov8.get("club_main_row_L3") == 13,
          f"new={cov8.get('club_main_row_new_L3')} L3={cov8.get('club_main_row_L3')}")
    check("6b.cov.occ433", cov8.get("club_main_row_occurrences") == 433, str(cov8.get("club_main_row_occurrences")))
    check("6c.cov.unmapped399", cov8.get("club_main_row_unmapped") == 399)
    check("6d.cov.aligned18", cov8.get("club_main_row_aligned") == 18, str(cov8.get("club_main_row_aligned")))
    check("6e.cov.inversions72", cov8.get("club_main_row_order_inversions") == 72,
          str(cov8.get("club_main_row_order_inversions")))

    led = json.loads(LEDGER.read_bytes())
    entries = {e["id"]: e for e in led["entries"]}
    check("7a.last_E97", led["entries"][-1]["id"] == "E97", led["entries"][-1]["id"])
    t57_task = v8["incremental_provenance"]["tasks"].get("t57")
    check("7b.prov.t57_E97_L3", bool(t57_task) and t57_task.get("acceptance_ledger_entry") == "E97"
          and t57_task.get("acceptance_ledger_level") == "L3",
          str(t57_task)[:160] if t57_task else "missing")
    e97 = entries.get("E97")
    check("7c.t57_claim_sha", bool(t57_task) and e97 is not None
          and t57_task.get("ledger_claim_sha256") == canon(e97["claim"]),
          f"{t57_task.get('ledger_claim_sha256') if t57_task else None} vs {canon(e97['claim']) if e97 else None}")
    ale = v8["incremental_provenance"]["acceptance_ledger_entries"]
    check("7d.guard_ids", sorted(ale.keys()) == GUARD_IDS, str(sorted(ale.keys())))
    for eid in GUARD_IDS:
        g, e = ale.get(eid), entries.get(eid)
        ok = (g is not None and e is not None
              and g.get("claim_sha256") == canon(e["claim"])
              and g.get("kind") == e.get("kind") and g.get("level") == e.get("level"))
        check(f"7.{eid}", ok, json.dumps(g, ensure_ascii=False)[:100] if g else "missing")
    check("7e.E98_not_guarded", "E98" not in ale)

    check("8.md_prefix", v8_md_raw.startswith(v7_md), "v8 md 不以 v7 md 为前缀")

    check("9.L4_0", cov8.get("L4") == 0 and t57_task.get("evidence_level", {}).get("L4") == 0,
          f"cov={cov8.get('L4')} task={t57_task.get('evidence_level')}")

    total = len(fails)
    print(f"\n{total} FAIL / spot t58 done")
    return 0 if total == 0 else 1


if __name__ == "__main__":
    if "--help" in sys.argv:
        print(__doc__)
        sys.exit(0)
    if "--selftest" in sys.argv:
        print("selftest: fixture-free structural spot; imports+keys only")
        sys.exit(0)
    sys.exit(main())
