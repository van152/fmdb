#!/usr/bin/env python3
"""t60 指挥官独立抽查 — schema v8→v9 合并验收(不 import worker 代码)。

checks:
  1. reports/ v9 JSON/MD SHA == REPORT 宣称
  2. out/ v8 快照 == git HEAD reports/(E98 时点)
  3. 保护节 v8→v9 逐值不动(含 club_main_row_fields;generated_by=t58→t60 预期增量)
  4. club/nation 计数不动(94/59/21;35 L3;13 L3)
  5. comp_main_row_fields 数字断言(894991/1533972/7047/12B/9B footer/837+114/82+2/49 L3/26 新 4CC/818 倒置/54 aligned)
  6. coverage comp_main_row_* 新分项
  7. provenance t59/E99/L3 + 条目级守卫 E84–E99 canonical claim SHA 复算
  8. markdown v9 = v8 前缀
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
SNAP_JSON = ROOT / "scratch/t60/out/club_nation_subtable_schema.v8.json"
SNAP_MD = ROOT / "scratch/t60/out/club_nation_subtable_schema.v8.md"
LEDGER = ROOT / "scratch/t01/LEDGER.json"

EXPECT_JSON_SHA = "703df30ea34fbee3b555ccf4233d4fe012bcb614435381efb68a3224e5ae64ee"
EXPECT_MD_SHA = "ded0da91af36098b2648af769ed258fd39d903e86f0494b5b2f8fab3a98c5757"
V8_JSON_SHA = "76da94d4376613a9e649a32d3bfc415f19596d4c7fb1c7c861d60b5951770cbf"
V8_MD_SHA = "5067502eadd489fac0e9842c6ece45e8402ff656e43d41e721522714308737f6"
GUARD_IDS = ["E84", "E85", "E86", "E87", "E88", "E89", "E90", "E91", "E92", "E93", "E94", "E95", "E96", "E97", "E98", "E99"]

PROTECTED_TOP = [
    "tables", "negative_regressions", "v3_baseline", "club_auxiliary_sources",
    "nation_static_side", "nation_t9_wire", "nation_main_row_fields",
    "nation_data_side_status", "evidence_grade_policy", "schema_id",
    "schema_provenance", "binary_provenance", "inventory_reconciliation",
    "source_artifacts", "club_main_row_fields",
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
    v9_raw = SCHEMA.read_bytes()
    v9_md_raw = SCHEMA_MD.read_bytes()
    check("1a.v9.json.sha", sha(v9_raw) == EXPECT_JSON_SHA, sha(v9_raw))
    check("1b.v9.md.sha", sha(v9_md_raw) == EXPECT_MD_SHA, sha(v9_md_raw))

    v8 = json.loads(SNAP_JSON.read_bytes())
    v8_md = SNAP_MD.read_bytes()
    check("2a.v8snap.json==HEAD", sha(SNAP_JSON.read_bytes()) == sha(git_blob("reports/club_nation_subtable_schema.json")))
    check("2b.v8snap.md==HEAD", sha(v8_md) == sha(git_blob("reports/club_nation_subtable_schema.md")))
    check("2c.v8snap.json.sha", sha(SNAP_JSON.read_bytes()) == V8_JSON_SHA)
    check("2d.v8snap.md.sha", sha(v8_md) == V8_MD_SHA)

    v9 = json.loads(v9_raw)
    check("3a.v9.version", v9["schema_version"] == 9, str(v9["schema_version"]))
    check("3b.generated_by_fold_delta", v8.get("generated_by") == "t58" and v9.get("generated_by") == "t60",
          f"{v8.get('generated_by')}->{v9.get('generated_by')}")
    for key in PROTECTED_TOP:
        check(f"3.{key}", key in v8 and key in v9 and v8[key] == v9[key])
    cov8, cov9 = v8["coverage"], v9["coverage"]
    for key in set(cov8) & set(cov9):
        check(f"4.cov.{key}", cov8[key] == cov9[key])
    check("4a.club_L3_occurrences94", cov9.get("club_L3_occurrences") == 94, str(cov9.get("club_L3_occurrences")))
    check("4b.club_L3_unique59", cov9.get("club_L3_unique_wire_fields") == 59)
    check("4c.club_main_L3_13", cov9.get("club_main_row_L3") == 13, str(cov9.get("club_main_row_L3")))
    check("4c2.club_main_newL3_5", cov9.get("club_main_row_new_L3") == 5, str(cov9.get("club_main_row_new_L3")))
    check("4d.club_main_occ433", cov9.get("club_main_row_occurrences") == 433)
    nmf = v9.get("nation_main_row_fields", {}).get("field_census", {})
    check("4e.nation_main_L3_5", nmf.get("grade_counts", {}).get("L3") == 5, str(nmf.get("grade_counts")))

    cmr = v9["comp_main_row_fields"]
    check("5a.cmr.task", cmr.get("source_task") == "t59", str(cmr.get("source_task")))
    check("5b.cmr.ledger", cmr.get("acceptance_ledger_entry") == "E99"
          and cmr.get("acceptance_ledger_level") == "L3",
          f"{cmr.get('acceptance_ledger_entry')}/{cmr.get('acceptance_ledger_level')}")
    census = cmr.get("field_census", {})
    check("5c.occ255", census.get("occurrences") == 255, str(census.get("occurrences")))
    gc = census.get("grade_counts", {})
    check("5d.grades", gc.get("L3") == 49 and gc.get("held") == 10 and gc.get("unmapped") == 196,
          str(gc))
    check("5e.aligned54", census.get("aligned") == 54, str(census.get("aligned")))
    check("5f.new4CC_26", census.get("new_4CC_count") == 26 and len(census.get("new_4CC", [])) == 26
          and "LAUC" in census.get("new_4CC", []),
          f"{census.get('new_4CC_count')}/{len(census.get('new_4CC', []))}")
    check("5f2.L3_fields_len49", len(cmr.get("L3_fields", [])) == 49, str(len(cmr.get("L3_fields", []))))
    order = cmr.get("order", {})
    check("5g.inversions818", order.get("inversions") == 818, str(order.get("inversions")))
    check("5h.first_inv", order.get("first_counterexample") is not None
          and "duni" in json.dumps(order.get("first_counterexample"), ensure_ascii=False)
          and "cfcl" in json.dumps(order.get("first_counterexample"), ensure_ascii=False),
          str(order.get("first_counterexample")))
    osc = cmr.get("outer_sequence_closure", {})
    check("5i.reader837_114_slot19", cmr.get("reader_and_factory", {}).get("reachable_instructions") == 837
          and cmr.get("reader_and_factory", {}).get("conditional_branches") == 114
          and cmr.get("reader_and_factory", {}).get("vtable_slot") == 19,
          str({k: cmr.get("reader_and_factory", {}).get(k) for k in ("reachable_instructions", "conditional_branches", "vtable_slot")}))
    check("5i2.dual_vtables", cmr.get("reader_and_factory", {}).get("comp_object_vtable") == "0x14187dcb8"
          and cmr.get("reader_and_factory", {}).get("database_table_comp_vtable") == "0x14187f6d8",
          str({k: cmr.get("reader_and_factory", {}).get(k) for k in ("comp_object_vtable", "database_table_comp_vtable")}))
    rf = cmr.get("row_framing", {})
    arch = rf.get("archives", {})
    cli, srv = arch.get("client", {}), arch.get("server", {})
    check("5j.client894991", cli.get("payload") == 894991 and cli.get("rows") == 894969
          and cli.get("header") == 13 and cli.get("footer") == 9 and cli.get("count") == 7047, str(cli)[:120])
    check("5k.server1533972", srv.get("payload") == 1533972 and srv.get("rows") == 1533950
          and srv.get("footer") == 9 and srv.get("count") == 7047, str(srv)[:120])
    check("5m.identity12B_footer9B", rf.get("identity_width") == 12 and rf.get("footer_width") == 9
          and str(rf.get("footer_hex", "")).endswith("4ec43a77"),
          str({k: rf.get(k) for k in ("identity_width", "footer_width", "footer_hex")}))
    check("5m2.width_policy_note", "12-byte identity and 9-byte footer" in
          (cov9.get("comp_identity_footer_width_note") or "") or
          "do not copy widths" in (cov9.get("comp_identity_footer_width_note") or ""),
          str(cov9.get("comp_identity_footer_width_note"))[:120])
    check("5n.sites82_plus2", osc.get("observed_positions") == 82
          and sorted(osc.get("static_untriggered_positions", [])) == ["obj_a8", "obj_e0"]
          and osc.get("field_slot_records") == 84
          and osc.get("client_templates") == 1 and osc.get("server_templates") == 25,
          str({k: osc.get(k) for k in ("observed_positions", "static_untriggered_positions", "field_slot_records", "client_templates", "server_templates")}))

    check("6a.cov.comp_occ255", cov9.get("comp_main_row_occurrences") == 255, str(cov9.get("comp_main_row_occurrences")))
    check("6b.cov.comp_L3_49", cov9.get("comp_main_row_L3", cov9.get("comp_main_row_new_L3")) == 49,
          str({k: v for k, v in cov9.items() if "comp_main" in str(k)}))
    check("6c.cov.comp_unmapped196", cov9.get("comp_main_row_unmapped") == 196)
    check("6d.cov.comp_inv818", cov9.get("comp_main_row_order_inversions") == 818,
          str(cov9.get("comp_main_row_order_inversions")))

    led = json.loads(LEDGER.read_bytes())
    entries = {e["id"]: e for e in led["entries"]}
    check("7a.last_E99", led["entries"][-1]["id"] == "E99", led["entries"][-1]["id"])
    t59_task = v9["incremental_provenance"]["tasks"].get("t59")
    check("7b.prov.t59_E99_L3", bool(t59_task) and t59_task.get("acceptance_ledger_entry") == "E99"
          and t59_task.get("acceptance_ledger_level") == "L3",
          str(t59_task)[:160] if t59_task else "missing")
    e99 = entries.get("E99")
    check("7c.t59_claim_sha", bool(t59_task) and e99 is not None
          and t59_task.get("ledger_claim_sha256") == canon(e99["claim"]),
          f"{t59_task.get('ledger_claim_sha256') if t59_task else None} vs {canon(e99['claim']) if e99 else None}")
    ale = v9["incremental_provenance"]["acceptance_ledger_entries"]
    check("7d.guard_ids", sorted(ale.keys()) == GUARD_IDS, str(sorted(ale.keys())))
    for eid in GUARD_IDS:
        g, e = ale.get(eid), entries.get(eid)
        ok = (g is not None and e is not None
              and g.get("claim_sha256") == canon(e["claim"])
              and g.get("kind") == e.get("kind") and g.get("level") == e.get("level"))
        check(f"7.{eid}", ok, json.dumps(g, ensure_ascii=False)[:100] if g else "missing")
    check("7e.E100_not_guarded", "E100" not in ale)

    check("8.md_prefix", v9_md_raw.startswith(v8_md), "v9 md 不以 v8 md 为前缀")

    t59_el = (t59_task or {}).get("evidence_level", {})
    check("9.L4_0", cov9.get("L4") == 0 and t59_el.get("L4") == 0,
          f"cov={cov9.get('L4')} task={t59_el}")

    print(f"\n{len(fails)} FAIL / spot t60 done")
    return 0 if not fails else 1


if __name__ == "__main__":
    if "--help" in sys.argv:
        print(__doc__)
        sys.exit(0)
    if "--selftest" in sys.argv:
        print("selftest: structural spot, imports ok")
        sys.exit(0)
    sys.exit(main())
