"""Stage-2 core artifact: merge table_type <-> entity <-> registration_fn (+ serialization mode).

Sources (all read-only):
- scratch/t01/inbox/t01c/property_map.json   (t01c: table_type <-> entity xml#tag)
- scratch/t01/t01e_vtables.json              (t01e E17: entity tag <-> vtable/slot6 regfn, 12 unique)
- evidence/fm24/reports/editor_schema/master.json (entity field counts)
- commander verified chains E20 (comp, straight-line) / E21 (nation, count-loop)
- old repo TABLE_HINTS (types 8/10/21/25/41/56)

Output: scratch/t01/stage2_three_way.json + .md
Run: py -V:3.12 -I scripts/t01_stage2_three_way.py
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

pm = json.load(open(ROOT / "scratch/t01/inbox/t01c/property_map.json", encoding="utf-8"))
t01e = json.load(open(ROOT / "scratch/t01/t01e_vtables.json", encoding="utf-8"))
master = json.load(open(ROOT / "evidence/fm24/reports/editor_schema/master.json", encoding="utf-8"))

# entity tag -> list of t01e vtable rows
vt_by_tag: dict[str, list[dict]] = {}
for v in t01e["vtables"]:
    vt_by_tag.setdefault(v["entity"], []).append(v)

# commander-verified rows (E20/E21)
commander = {
    25: {"entity_tag": "comp", "entity_xml": "comp.xml#comp", "record_ctor_off": "0xeb5dd5",
         "ctor_vptr_off": "0x187d2b8", "reader_off": "0xeb7000", "writer_off": "0xeb8920",
         "mode": "straight-line", "alloc": "0x1b0", "sources": ["E20", "t01f"]},
    10: {"entity_tag": "nati", "entity_xml": "nation.xml#nati", "record_ctor_off": "0x103ebf0",
         "ctor_vptr_off": "0x18889B8", "reader_off": "0x103fac0", "writer_off": "0x1041460",
         "mode": "count-loop", "alloc": "0x1d8", "sources": ["E21", "t01g"],
         "note": "RTTI .?AVNATION@db@@; t01e 的 'nati' 双虚表与 t01g 链交叉"},
}

OLD_HINTS = {
    8: "language (candidate, readable names)",
    10: "nation (strong candidate; L1 duni anchor; t01g/E21 confirmed entity)",
    21: "stadium (high; rdui@+30=行序号误标勘误适用)",
    25: "competition (high; E20 收口)",
    41: "currency (high candidate)",
    56: "structural triples",
}

es = master["entity_summary"]
def field_count_for(xml: str):
    if xml in es:
        return es[xml]["field_count"]
    for k, v in es.items():
        if k.split("#")[-1] == xml.split("#")[-1]:
            return v["field_count"]
    return None

rows = []
for r in pm["rows"]:
    xml = r["entity"]
    tag = xml.split("#")[-1]
    vts = vt_by_tag.get(tag, [])
    row = {
        "table_type": r["table_type"],
        "entity_xml": xml,
        "entity_tag": tag,
        "field_count": field_count_for(xml),
        "vtable_offs": [v["table_off"] for v in vts],
        "regfn_slot6_va": [v["slot6_va"] for v in vts],
        "regfn_block_offs": [v["reg_block_off"] for v in vts],
        "mode": "-",
        "sources": ["t01c/property_map"],
        "old_hint": OLD_HINTS.get(r["table_type"], ""),
    }
    if r["table_type"] in commander:
        c = commander[r["table_type"]]
        row.update({k: v for k, v in c.items() if k not in ("entity_tag", "sources")})
        row["mode"] = c["mode"]
        row["sources"] = sorted(set(row["sources"] + c["sources"]))
    elif vts:
        row["sources"].append("t01e/E17")
    rows.append(row)

# table types without a property_map row (0..58 per old repo's 59 numeric tables)
seen = {r["table_type"] for r in rows}
unknown = [t for t in range(59) if t not in seen]

# tags mapped by t01e but absent from property_map rows
pm_tags = {r["entity"].split("#")[-1] for r in pm["rows"]}
t01e_only = sorted(set(vt_by_tag) - pm_tags)

out = {
    "task": "stage2 three-way table: table_type <-> entity <-> registration_fn (+ serialization mode)",
    "date": "2026-11-18 05:2x",
    "author": "commander",
    "sources": ["t01c property_map (21 rows)", "t01e E17 (12 unique entities)",
                "E20 comp chain", "E21 nation chain", "master.json entity_summary", "old TABLE_HINTS"],
    "rows": sorted(rows, key=lambda r: r["table_type"]),
    "table_types_without_row": unknown,
    "t01e_tags_not_in_property_map": t01e_only,
    "notes": [
        "mode 列:straight-line(comp,E20)/ count-loop(nation,E21);其余实体待 t01h factory 跳表普查分类",
        "vtable/regfn 来自 t01e 的 slot6 计数口径;E20 已修正为 0-based slot5(字节不变)",
        "unknown 表共 %d 个(0..58 减去 property_map 已覆盖)" % len(unknown),
        "疑点:table_type 9 与 10 的 property_map 实体都是 nation.xml#nati —— 两个表型对应同一实体?可能 t01c 来源行有误或 nation 确有双表(如 client/server 双记录);待 t01h 跳表普查裁决(看 type 9/10 是否都有独立工厂项)",
        "t01e 独有 tag(agen/jour/offc)是 unknown 表型的候选实体",
    ],
}
json.dump(out, open(ROOT / "scratch/t01/stage2_three_way.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

# compact markdown
md = ["# stage2 三向表(table_type ↔ entity ↔ registration_fn)+ 序列化模式", "",
      "| type | entity | tag | fields | vtable(s) | regfn block off | mode | 来源 |",
      "|---|---|---|---:|---|---|---|---|"]
for r in out["rows"]:
    md.append("| {} | {} | {} | {} | {} | {} | {} | {} |".format(
        r["table_type"], r["entity_xml"], r["entity_tag"], r["field_count"],
        ", ".join(r["vtable_offs"]) or "-", ", ".join(r["regfn_block_offs"]) or "-",
        r["mode"], "+".join(r["sources"])))
md += ["", f"无属性映射的表型(0..58):{unknown}", "",
       f"t01e 已映射但 property_map 缺的 tag:{t01e_only}", "",
       "已知模式:comp=直线(E20)、nation=计数循环(E21);其余待 t01h 普查(E22)"]
(ROOT / "scratch/t01/stage2_three_way.md").write_text("\n".join(md), encoding="utf-8")

print(f"rows: {len(out['rows'])}, unknown table types: {len(unknown)}, t01e-only tags: {t01e_only}")
print("mode known:", [(r["table_type"], r["mode"]) for r in out["rows"] if r["mode"] != "-"])
