#!/usr/bin/env python3
"""t85_collect_fields — 任务1:集合字段清单(getter_proven_but_no_main_row_sink)。

来源(只读):
  scratch/t75/out/xref_reverse.json  -> negative_evidence.nation.r2_held_verbatim
                                         .status == getter_proven_but_no_main_row_sink
  scratch/t78/out/buckets.json       -> entity=comp/held|unresolved_wire_slot 明细
  evidence/fm24/reports/editor_schema/master.json -> 字段 type/list_item_fields

分类规则(显式、可复核):
  * gate_source 含 "[this+0x108]"        -> collection_object_proven   (t75 已证:集合对象)
  * gate_source 含 "this+0x20/0x28/0x30" -> collection_object_candidate (指针成员,同一 NATION 对象)
  * schema type 为 list/database_record_list,或 master 里 nation.xml
    other_records 的 insert_fields(alnm/ntts) -> list_schema_field
  * 其余(string/colour/boolean 标量 getter)  -> scalar_getter_out_of_scope

输出: scratch/t85/out/collection_fields.json
退出码 0 成功 / 1 检查未过 / 2 用法或致命错误。
"""
from __future__ import annotations

import argparse
import json
import re
import sys

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import t85_common as C  # noqa: E402

OUT = "scratch/t85/out/collection_fields.json"
COLL_PAT = re.compile(r"\[this\+0x108\]")
PTR_PAT = re.compile(r"this\+0x(20|28|30)\b")
LIST_TYPES = ("list", "database_record_list")


def _classify(src: str | None, schema: dict) -> str:
    src = src or ""
    if COLL_PAT.search(src):
        return "collection_object_proven"
    if PTR_PAT.search(src):
        return "collection_object_candidate"
    if str(schema.get("type") or "") in LIST_TYPES or schema.get("list_item_fields"):
        return "list_schema_field"
    return "scalar_getter_out_of_scope"


def build() -> dict:
    xref = C.jload("scratch/t75/out/xref_reverse.json")
    master = C.jload("evidence/fm24/reports/editor_schema/master.json")
    nation_fields = master["entities"]["nation.xml"][0]["fields"]
    other_records = master["entities"]["nation.xml"][0].get("other_records") or []
    buckets = C.jload("scratch/t78/out/buckets.json")

    # --- nation 侧: t75 held 台账逐条 ---
    held = xref["negative_evidence"]["nation"]["r2_held_verbatim"]
    nation_items = []
    for it in held:
        if it.get("status") != "getter_proven_but_no_main_row_sink":
            continue
        idx = it.get("xml_index")
        schema = dict(nation_fields[idx]) if isinstance(idx, int) and idx < len(nation_fields) else {}
        fce = it.get("first_counterexample") or {}
        src = fce.get("source")
        nation_items.append({
            "entity": "nation",
            "table_id": 10,
            "xml_index": idx,
            "code": it.get("code"),
            "schema_type": schema.get("type"),
            "schema_name": schema.get("name"),
            "schema_flags": {k: v for k, v in schema.items() if k.startswith("is_")},
            "t75_status": it.get("status"),
            "t75_grade": it.get("grade"),
            "slot": it.get("slot"),
            "projection_gate": it.get("projection_gate"),
            "gate": fce.get("gate"),
            "gate_source_verbatim": src,
            "first_evidence": fce.get("first_evidence"),
            "class": _classify(src, schema),
            "verdict": "held",
            "wire_binding": None,
        })

    # --- nation 侧: schema other_records 的 list 插入项(无独立 getter 台账) ---
    inserted = []
    for rec in other_records:
        code = rec.get("insert_fields")
        inserted.append({
            "entity": "nation",
            "table_id": 10,
            "code": code,
            "source": "master.json entities/nation.xml[0].other_records",
            "hide_if_field_not_found": rec.get("hide_if_field_not_found"),
            "class": "list_schema_field",
            "verdict": "held",
            "wire_binding": None,
            "note": "nation.xml 无同名字段;由 alnm/ntts 独立实体插入,主行 reader 未见",
        })

    # --- comp 侧: t78 held + unresolved_wire_slot 明细 ---
    comp_items = []
    for o in buckets["occurrences"]:
        if o.get("entity") != "comp":
            continue
        if o.get("bucket") not in ("held", "unresolved_wire_slot"):
            continue
        comp_items.append({
            "entity": "comp",
            "table_id": 25,
            "occurrence_id": o.get("id"),
            "code": o.get("code"),
            "bucket": o.get("bucket"),
            "evidence_ref": o.get("evidence_ref"),
            "note_verbatim": o.get("note"),
            "class": "held_no_getter_ledger",
            "verdict": "held",
            "wire_binding": None,
        })

    counts: dict[str, int] = {}
    for it in nation_items + inserted + comp_items:
        counts[it["class"]] = counts.get(it["class"], 0) + 1

    return {
        "schema": "t85.collection_fields.v1",
        "task": "t85",
        "inputs": {
            "t75_xref_reverse": "scratch/t75/out/xref_reverse.json",
            "t78_buckets": "scratch/t78/out/buckets.json",
            "master": "evidence/fm24/reports/editor_schema/master.json",
        },
        "rule": {
            "source": "t75 negative_evidence.nation.r2_held_verbatim[].first_counterexample.source",
            "collection_object_proven": "gate source 明写 [this+0x108]",
            "collection_object_candidate": "gate source 明写 this+0x20/0x28/0x30 指针成员",
            "list_schema_field": "schema type ∈ {list,database_record_list} 或 other_records 插入项",
            "scalar_getter_out_of_scope": "标量 getter(string/colour/boolean),非集合",
        },
        "counts": counts,
        "nation": {"getter_ledger": nation_items, "schema_inserted_lists": inserted},
        "comp": {"held_or_unresolved": comp_items},
        "negative_preserved": [
            "t75 原文不改:所有条目 verdict=held,wire_binding=null",
            "comp 侧 t78 只有分类与 evidence_ref,无 gate 地址,故不生成 collection_object_* 类",
        ],
    }


def selftest() -> int:
    res = build()
    ok = True
    proven = [x for x in res["nation"]["getter_ledger"] if x["class"] == "collection_object_proven"]
    if [x["code"] for x in proven] != ["nhrl"]:
        print("FAIL: [this+0x108] 应唯一命中 nhrl,实得", [x["code"] for x in proven])
        ok = False
    if not any(x["code"] == "dbnm" for x in res["nation"]["getter_ledger"]):
        print("FAIL: dbnm 未入账")
        ok = False
    if len(res["comp"]["held_or_unresolved"]) < 20:
        print("FAIL: comp held/unresolved 少于 20:", len(res["comp"]["held_or_unresolved"]))
        ok = False
    if all(x["verdict"] == "held" for x in res["nation"]["getter_ledger"] + res["comp"]["held_or_unresolved"]):
        print("PASS selftest: 分类闭合,全部 held 原样")
    else:
        print("FAIL: 出现非 held verdict")
        ok = False
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="t85 任务1:集合字段清单")
    ap.add_argument("--build", action="store_true", help="写 scratch/t85/out/collection_fields.json")
    ap.add_argument("--selftest", action="store_true", help="不落盘自检")
    ap.add_argument("--print", action="store_true", help="打印摘要")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    try:
        res = build()
    except Exception as exc:  # noqa: BLE001
        print("FATAL:", exc, file=sys.stderr)
        return 2
    if args.print or not args.build:
        print(json.dumps(res["counts"], ensure_ascii=False, indent=1))
        for x in res["nation"]["getter_ledger"]:
            print(f'  {x["code"]:5s} idx={x["xml_index"]:<4d} {x["schema_type"]:10s} {x["class"]}')
        print(f'  comp held/unresolved = {len(res["comp"]["held_or_unresolved"])}')
    if args.build:
        p = C.jdump(OUT, res)
        print("wrote", p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
