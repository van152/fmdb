#!/usr/bin/env python3
"""t85-fix1 — 集合字段清单骨架(只装配 t75/t78 冻结工件,不新扫描)。

输入(只读):
  scratch/t75/out/xref_reverse.json  negative_evidence.nation.r2_held_verbatim
  scratch/t75/out/xref_reverse.json  nation_escalations(集合 grammar 台账)
  scratch/t78/out/buckets.json       entity=comp 的 held / unresolved_wire_slot
  evidence/fm24/reports/editor_schema/master.json  (字段 type / list_item_fields)

分类(显式):
  collection_object_proven     gate source 含 [this+0x108] 或 t75 nation_escalations
  object_pointer_string_member gate source 含 this+0x20/0x28/0x30(同对象字符串指针)
  list_schema_field            schema type=list 或带 list_item_fields
  scalar_getter_out_of_scope   其余标量 getter

输出: scratch/t85/out2/collection_fields.json
退出码 0 成功 / 1 自检未过 / 2 用法或致命错误。
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

OUT = "scratch/t85/out2/collection_fields.json"
COLL_PAT = re.compile(r"\[this\+0x108\]")
PTR_PAT = re.compile(r"this\+0x(20|28|30)\b")
LIST_TYPES = ("list", "database_record_list")


def _load(rel: str):
    root = pathlib.Path(__file__).resolve().parents[1]
    return json.loads((root / rel).read_text(encoding="utf-8"))


def _classify(src: str, schema: dict) -> str:
    src = src or ""
    if COLL_PAT.search(src):
        return "collection_object_proven"
    if PTR_PAT.search(src):
        return "object_pointer_string_member"
    if str(schema.get("type") or "") in LIST_TYPES or schema.get("list_item_fields"):
        return "list_schema_field"
    return "scalar_getter_out_of_scope"


def build() -> dict:
    xref = _load("scratch/t75/out/xref_reverse.json")
    master = _load("evidence/fm24/reports/editor_schema/master.json")
    buckets = _load("scratch/t78/out/buckets.json")
    nation_fields = master["entities"]["nation.xml"][0]["fields"]
    other_records = master["entities"]["nation.xml"][0].get("other_records") or []

    nation = []
    for it in xref["negative_evidence"]["nation"]["r2_held_verbatim"]:
        if it.get("status") != "getter_proven_but_no_main_row_sink":
            continue
        idx = it.get("xml_index")
        schema = dict(nation_fields[idx]) if isinstance(idx, int) and idx < len(nation_fields) else {}
        fce = it.get("first_counterexample") or {}
        nation.append({
            "entity": "nation", "table_id": 10, "xml_index": idx,
            "code": it.get("code"),
            "schema_type": schema.get("type"),
            "schema_name": schema.get("name"),
            "list_item_fields": [x.get("field") for x in (schema.get("list_item_fields") or [])],
            "t75_status": it.get("status"),
            "slot": it.get("slot"),
            "projection_gate": it.get("projection_gate"),
            "gate": fce.get("gate"),
            "gate_source_verbatim": fce.get("source"),
            "class": _classify(fce.get("source") or "", schema),
            "verdict": "held",
            "wire_binding": None,
        })

    inserted = [{
        "entity": "nation", "table_id": 10, "code": rec.get("insert_fields"),
        "source": "master.json entities/nation.xml[0].other_records",
        "class": "list_schema_field", "verdict": "held", "wire_binding": None,
        "note": "nation.xml 无同名字段;独立实体插入,主行 reader 未见",
    } for rec in other_records]

    # t75 自己声明的 nation 集合 escalation(extra_128 等)
    escal = [{
        "entity": "nation", "table_id": 10,
        "slot": e["escalation"].get("slot"),
        "collection": e["escalation"].get("collection"),
        "kind": e["escalation"].get("kind"),
        "why_verbatim": e["escalation"].get("why"),
        "grammar": e["escalation"].get("grammar"),
        "count_format": e["escalation"].get("count_format"),
        "gate_helper_cursor": e["escalation"].get("gate_helper_cursor"),
        "reader_site": e["escalation"].get("reader_site"),
        "object_displacement": e["escalation"].get("object_displacement"),
        "grade": e["escalation"].get("grade"),
        "prior_ids": e["escalation"].get("prior_ids"),
        "class": "collection_object_proven", "verdict": "held_no_items",
        "wire_binding": None,
    } for e in xref.get("nation_escalations", [])]

    comp = []
    for o in buckets["occurrences"]:
        if o.get("entity") != "comp" or o.get("bucket") not in ("held", "unresolved_wire_slot"):
            continue
        comp.append({
            "entity": "comp", "table_id": 25,
            "occurrence_id": o.get("id"), "code": o.get("code"),
            "bucket": o.get("bucket"), "evidence_ref": o.get("evidence_ref"),
            "note_verbatim": o.get("note"),
            "class": "held_no_getter_ledger", "verdict": "held", "wire_binding": None,
        })

    counts: dict[str, int] = {}
    for it in nation + inserted + escal + comp:
        counts[it["class"]] = counts.get(it["class"], 0) + 1
    counts["total"] = len(nation) + len(inserted) + len(escal) + len(comp)

    return {
        "schema": "t85.collection_fields.v1",
        "task": "t85-fix1",
        "stage": "skeleton_then_profile",
        "inputs": {
            "t75_xref_reverse": "scratch/t75/out/xref_reverse.json",
            "t78_buckets": "scratch/t78/out/buckets.json",
            "master": "evidence/fm24/reports/editor_schema/master.json",
        },
        "rule": {
            "collection_object_proven": "gate source 明写 [this+0x108] 或 t75 nation_escalations",
            "object_pointer_string_member": "gate source 明写 this+0x20/0x28/0x30 指针成员(字符串,非集合)",
            "list_schema_field": "schema type∈{list,database_record_list} 或带 list_item_fields",
            "scalar_getter_out_of_scope": "标量 getter(string/colour/boolean)",
        },
        "counts": counts,
        "nation": {"getter_ledger": nation, "schema_inserted_lists": inserted,
                   "t75_collection_escalations": escal},
        "comp": {"held_or_unresolved": comp},
        "negative_preserved": [
            "t75 原文不改:所有条目 verdict 保持 held,wire_binding=null",
            "comp 侧 t78 只给分类与 evidence_ref,无 gate 地址",
        ],
    }


def selftest() -> int:
    res = build()
    ok = True
    proven = [x for x in res["nation"]["getter_ledger"] if x["class"] == "collection_object_proven"]
    if [x["code"] for x in proven] != ["nhrl"]:
        print("FAIL: [this+0x108] 应唯一命中 nhrl,实得", [x["code"] for x in proven]); ok = False
    cand = [x["code"] for x in res["nation"]["getter_ledger"]
            if x["class"] == "object_pointer_string_member"]
    if cand != ["Nsnm", "N3ln", "Nnty"]:
        print("FAIL: 字符串指针成员应为 Nsnm/N3ln/Nnty,实得", cand); ok = False
    if len(res["comp"]["held_or_unresolved"]) < 20:
        print("FAIL: comp held/unresolved 少于 20"); ok = False
    if not res["nation"]["t75_collection_escalations"]:
        print("FAIL: nation 集合 escalation 空"); ok = False
    if ok:
        print("PASS selftest:", res["counts"])
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="t85-fix1 任务1:集合字段清单骨架")
    ap.add_argument("--build", action="store_true", help="写 scratch/t85/out2/collection_fields.json")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    try:
        res = build()
    except Exception as exc:  # noqa: BLE001
        print("FATAL:", exc, file=sys.stderr); return 2
    if a.build:
        p = pathlib.Path(__file__).resolve().parents[1] / OUT
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print("wrote", OUT)
    print(json.dumps(res["counts"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
