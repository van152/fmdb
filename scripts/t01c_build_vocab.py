#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""t01-c: schema vocabulary tabularization (task brief: prompts/t01c_vocab_tables.md).

Reads (read-only):
  * evidence/fm24/reports/editor_schema/master.json  (entities / entity_summary /
    field_codes / enums ...)
  * evidence/fm24/reports/editor_gen/PROPERTY_MAP.md (section 3: database_table_type
    -> entity mapping table)

Writes (task products, generated - never hand-edited):
  * scratch/t01/inbox/t01c/vocab.json        {entities, field_codes, code_conflicts, meta}
  * scratch/t01/inbox/t01c/property_map.json {source, rows}
  * scratch/t01/inbox/t01c/REPORT.md         (<=40 lines)

Run:  py -V:3.12 -I scripts/t01c_build_vocab.py [--help]
Pure stdlib; deterministic; no network, no installs.

Transcription policy (documented in REPORT.md):
  * vocab.entities[codes]     = master.entity_summary[..]["codes"] verbatim
                                (order + duplicates preserved, verified against
                                entities[..]["fields"]).
  * client_codes              = top-level fields with is_client_field=="true"
                                (same scope as entity_summary codes; dedup).
  * readonly_codes            = top-level fields with is_read_only=="true" or the
                                one non-standard read_only=="true" (MYpc); dedup.
  * vocab.field_codes         = all 3009 codes of master.field_codes (verbatim keys).
                                  entity        : derived from a full walk of the 32
                                                  entities (incl. list_item_fields);
                                                  1 -> "file.xml#id", >1 -> sorted
                                                  list, none -> null.
                                  type          : master field_codes[code]["type"]
                                                  as-is.
                                  is_client_field: true if any field occurrence sets
                                                  it "true", false if all occurrences
                                                  that specify it say "false",
                                                  null if never specified.
                                  enum_ref      : master attr enum_ref; 1 -> str,
                                                  >1 -> sorted list, none -> null.
  * code_conflicts            = codes present in more than one entity.
  * property_map rows         = every row of PROPERTY_MAP.md section 3
                                (database_table_type <-> entity), fields
                                table_type(int) / entity / property / source(raw md
                                line); "property" = the row's dbts enum-name column
                                (null for table 10 which has none); the entity short
                                name from the md is normalized to "file.xml#id".
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(r"D:\tmp2b\fm24-db")
DEFAULT_MASTER = REPO / "evidence/fm24/reports/editor_schema/master.json"
DEFAULT_PMAP = REPO / "evidence/fm24/reports/editor_gen/PROPERTY_MAP.md"
DEFAULT_OUT = REPO / "scratch/t01/inbox/t01c"

# Commander-known self-check anchors for comp.xml#comp.  cnsm/cl3n are NOT present
# in master.json under any casing (verified) - the script fails hard only on the
# codes that DO exist there, and reports the two missing ones as findings.
COMP_ANCHORS_PRESENT = ["ccti", "cnti", "cpcm", "cnam", "PLgn", "crep", "cext"]
COMP_ANCHORS_REPORTED_MISSING = ["cnsm", "cl3n"]
FOUR_CC = re.compile(r"[A-Za-z0-9]{4}\Z")
DB_LOC = re.compile(r"database/database/(.+?\.xml)#")


def is_field(obj) -> bool:
    """A schema field dict: has both 'field' (code) and 'type'."""
    return isinstance(obj, dict) and "field" in obj and "type" in obj


def load_master(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def build_entities(master: dict) -> tuple[dict, dict]:
    """Return (vocab.entities, code_attr_index) built from master entities."""
    summaries = master["entity_summary"]
    entities: dict = {}
    # code -> {"client": set("true"/"false"), "ro": bool, "enum": set(refs)}
    attrs: dict = defaultdict(lambda: {"client": set(), "ro": set(), "enum": set()})

    def walk(obj, ent):
        if isinstance(obj, dict):
            if is_field(obj):
                a = attrs[obj["field"]]
                if "is_client_field" in obj:
                    a["client"].add(str(obj["is_client_field"]))
                if "is_read_only" in obj:
                    a["ro"].add(str(obj["is_read_only"]))
                if "read_only" in obj:  # one non-standard occurrence (MYpc)
                    a["ro"].add(str(obj["read_only"]))
                if "enum_ref" in obj:
                    a["enum"].add(obj["enum_ref"])
            for v in obj.values():
                walk(v, ent)
        elif isinstance(obj, list):
            for v in obj:
                walk(v, ent)

    for fname, groups in master["entities"].items():
        for g in groups:
            key = f"{fname}#{g['id']}"
            fields = g.get("fields", [])
            summ = summaries.get(key)
            if summ is None:
                sys.exit(f"entity {key}: no entity_summary entry")
            if summ["field_count"] != len(fields):
                sys.exit(f"entity {key}: field_count {summ['field_count']} != {len(fields)} fields")
            if summ["codes"] != [f["field"] for f in fields]:
                sys.exit(f"entity {key}: entity_summary codes != entities fields order")
            client, ro = [], []
            for f in fields:
                code = f["field"]
                if f.get("is_client_field") == "true" and code not in client:
                    client.append(code)
                if ("is_read_only" in f and f["is_read_only"] == "true") or f.get("read_only") == "true":
                    if code not in ro:
                        ro.append(code)
            entities[key] = {
                "field_count": summ["field_count"],
                "codes": list(summ["codes"]),  # verbatim, duplicates kept
                "client_codes": client,
                "readonly_codes": ro,
            }
            walk(g, key)
    return entities, attrs


def build_field_codes(master: dict, attrs: dict) -> tuple[dict, dict]:
    """Return (vocab.field_codes, code_conflicts)."""
    ents_by_code: dict = defaultdict(set)
    for fname, groups in master["entities"].items():
        for g in groups:
            key = f"{fname}#{g['id']}"

            def walk(obj):
                if isinstance(obj, dict):
                    if is_field(obj):
                        ents_by_code[obj["field"]].add(key)
                    for v in obj.values():
                        walk(v)
                elif isinstance(obj, list):
                    for v in obj:
                        walk(v)

            walk(g)

    unknown = sorted(set(ents_by_code) - set(master["field_codes"]))
    if unknown:
        sys.exit(f"entity codes absent from master.field_codes: {unknown[:10]}")

    field_codes: dict = {}
    for code, entry in master["field_codes"].items():
        ents = ents_by_code.get(code)
        client_vals = attrs[code]["client"]
        if "true" in client_vals:
            client = True
        elif "false" in client_vals:
            client = False
        else:
            client = None
        enums = sorted(attrs[code]["enum"])
        entity: object
        if ents is None:
            entity = None
        elif len(ents) == 1:
            entity = next(iter(ents))
        else:
            entity = sorted(ents)
        field_codes[code] = {
            "entity": entity,
            "type": entry["type"],
            "is_client_field": client,
            "enum_ref": enums[0] if len(enums) == 1 else (enums if enums else None),
        }

    conflicts = {
        code: sorted(ents)
        for code, ents in sorted(ents_by_code.items())
        if len(ents) > 1
    }
    return field_codes, conflicts


def norm_entity_key(name: str, master: dict) -> str:
    """Map PROPERTY_MAP.md entity short name -> "<file.xml>#<record id>"."""
    files = list(master["entities"].keys())
    lowered = name.strip().lower()
    stems = {f: f[:-4].lower() for f in files if f.lower().endswith(".xml")}
    exact = [f for f, s in stems.items() if s == lowered]
    if len(exact) > 1:
        sys.exit(f"entity short name {name!r}: ambiguous exact matches {exact}")
    if not exact:
        # whole md name contains exactly one file stem (e.g. "derby name" -> derby)
        partial = [f for f, s in stems.items() if s in lowered]
        if len(partial) != 1:
            sys.exit(f"entity short name {name!r}: {len(partial)} file matches {partial}")
        exact = partial
    fname = exact[0]
    return f"{fname}#{master['entities'][fname][0]['id']}"


def parse_property_map(path: Path, master: dict) -> dict:
    """Transcribe every mapping row of PROPERTY_MAP.md section 3."""
    lines = path.read_text(encoding="utf-8").splitlines()
    sec3 = next(i for i, ln in enumerate(lines) if ln.startswith("## 3."))
    sec4 = next(i for i, ln in enumerate(lines) if ln.startswith("## 4."))
    dbts = {v["enum"]: v["name"] for v in master["enums"].get("dbts", {}).get("values", [])}
    rows, notes = [], []
    for ln in lines[sec3 + 1:sec4]:
        if not ln.startswith("|"):
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if not cells[0].isdigit():
            continue  # header / separator rows
        table = int(cells[0])
        short, dbts_name = cells[1], cells[3]
        prop = None if dbts_name in ("-", "—", "") else dbts_name
        if prop is not None and dbts.get(str(table)) != prop:
            notes.append(f"table {table}: dbts name {prop!r} != master enums.dbts "
                         f"{dbts.get(str(table))!r}")
        rows.append({
            "table_type": table,
            "entity": norm_entity_key(short, master),
            "property": prop,
            "source": ln,
        })
    return {"source": str(path), "rows": rows, "dbts_crosscheck_notes": notes}


def anchor_check(vocab: dict) -> dict:
    comp = vocab["entities"].get("comp.xml#comp", {}).get("codes", [])
    low = {c.lower() for c in vocab["field_codes"]}
    return {
        "present": [c for c in COMP_ANCHORS_PRESENT if c in comp],
        "missing": [c for c in COMP_ANCHORS_PRESENT if c not in comp],
        "absent_everywhere_case_insensitive": [c for c in COMP_ANCHORS_REPORTED_MISSING
                                               if c.lower() not in low],
        "near_matches": {c: [k for k in vocab["field_codes"] if k.lower() == c.lower()
                             or (c.lower() in ("cnsm", "cl3n") and
                                 k.lower() in ("csnm", "c3ln", "cl3n"))]
                         for c in COMP_ANCHORS_REPORTED_MISSING},
    }


def write_json(path: Path, obj) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def build_report(master: dict, vocab: dict, pmap: dict, anchors: dict, args) -> list[str]:
    fc = vocab["field_codes"]
    n_all = len(fc)
    n4 = sum(1 for k in fc if FOUR_CC.fullmatch(k))
    ent_codes = set()
    top_union = set()
    top_sum = 0
    for key, e in vocab["entities"].items():
        ent_codes.update(e["codes"])
        top_union.update(e["codes"])
        top_sum += e["field_count"]
    n_ent_walk = sum(1 for v in fc.values() if v["entity"] is not None)
    conflicts = vocab["code_conflicts"]
    top_conf = max(conflicts.items(), key=lambda kv: len(kv[1])) if conflicts else ("", [])
    meta = master["meta"]
    L = []
    a = L.append
    a("# t01-c REPORT:schema 词汇表机读化")
    a("")
    a(f"- 输入: master.json(editor_schema, {meta['game_version']}, parse_errors={meta['parse_errors']}) + PROPERTY_MAP.md")
    a(f"- 产物: 本目录 vocab.json / property_map.json / REPORT.md;脚本 scripts/{Path(__file__).name} 可复跑")
    a("")
    a("## 对账")
    a(f"- 实体数 {len(vocab['entities'])}(32 个 xml 均单 record 组,key=<file>#<id>;field_count 与字段数逐一核对一致)")
    a(f"- vocab.field_codes = {n_all} = master.field_codes ✓(键与 master 完全一致)")
    a(f"- 码长分布:4 字符码 {n4},其它 {n_all - n4}")
    a(f"- 属于 32 实体的码 {n_ent_walk}(含嵌套 list_item_fields);非实体来源 {n_all - n_ent_walk}"
      f"(rule_group/format/extractor)→ entity=null")
    a(f"- 实体顶层码合计 {top_sum}(= sum field_count),顶层并集 {len(top_union)};"
      f"codes 列表按 master 原样保留重复(如 comp 的 duni 出现 2 次)")
    a(f"- code_conflicts:{len(conflicts)} 个码出现在 >1 实体(机读全清单在 vocab.json);"
      f"最大:{top_conf[0]} 出现于 {len(top_conf[1])} 实体")
    a("")
    a("## 锚点自检(comp.xml#comp)")
    a(f"- 通过 {len(anchors['present'])}/9:{'/'.join(anchors['present'])}")
    a("- cnsm:master 全库(3009 码,大小写不敏感)无此码;comp 的是 csnm(Short Name)与 c3ln(Three Letter Name)")
    a("- cl3n:无此码;club.xml 有 Cl3n,comp.xml#comp 有 c3ln")
    a("- → 两个锚码与证据不符(疑拼写偏差),解析经 3 重核对(entities/summary/field_codes)无误")
    a("")
    a("## 结构与预期不符(如实记录)")
    a("- 属性名:枚举引用为 enum_ref(非 enum);只读为 is_read_only(174 处)+ 1 处非标 read_only(MYpc,已计入 readonly_codes)")
    a("- master field_codes[].locations 对 52 个实体码漏记 database 位置(如 PLgn/Cnti 只记 rule_group)"
      "→ vocab 的 entity 以 entities 树全量遍历为准")
    a("- is_client_field 顶层 true=192 / false=3(CSrs/Cfvp/CRtm);另有 2 个嵌套 list_item_field 为 true,"
      "不计入 client_codes(与 codes 同为顶层范围)")
    a("- 一码多枚举:enum_ref 冲突 Ttyp、PFjo → vocab 用 list;75 个码有多个 type 变体,type 按 master 原文转录")
    a("- vocab.field_codes 的 entity 字段:单实体→str,多实体→list,非实体→null(is_client_field/enum_ref 同理)")
    a("")
    a(f"## property_map.json({len(pmap['rows'])} 行)")
    a("- 转录 §3「database_table_type 数值 → 实体」全部映射行;property=该行 dbts 枚举名(表 10 无 → null);"
      "投票/一致/备注保留在 source 原文行")
    a("- entity 已归一化为 <file>#<id>(md 的 derby name → derby.xml#drbr,唯一子串匹配);"
      f"dbts 枚举名与 master#enums.dbts 交叉验证:{'一致' if not pmap['dbts_crosscheck_notes'] else pmap['dbts_crosscheck_notes']}")
    a("- §4 字段映射行未转录:其表号列含多值(如 10,9)不满足 table_type(int),内容已由 vocab.json 承载")
    return L


def main() -> None:
    ap = argparse.ArgumentParser(
        description="t01-c: build vocab.json / property_map.json / REPORT.md from "
                    "master.json and PROPERTY_MAP.md (read-only inputs).")
    ap.add_argument("--master", type=Path, default=DEFAULT_MASTER,
                    help=f"master.json path (default: {DEFAULT_MASTER})")
    ap.add_argument("--property-map", type=Path, default=DEFAULT_PMAP,
                    help=f"PROPERTY_MAP.md path (default: {DEFAULT_PMAP})")
    ap.add_argument("--outdir", type=Path, default=DEFAULT_OUT,
                    help=f"output directory (default: {DEFAULT_OUT})")
    ap.add_argument("--indent", type=int, default=2, help="JSON indent (default: 2)")
    args = ap.parse_args()

    master = load_master(args.master)
    entities, attrs = build_entities(master)
    field_codes, conflicts = build_field_codes(master, attrs)

    n4 = sum(1 for k in field_codes if FOUR_CC.fullmatch(k))
    n_entity = sum(1 for v in field_codes.values() if v["entity"] is not None)
    vocab = {
        "entities": entities,
        "field_codes": field_codes,
        "code_conflicts": conflicts,
        "meta": {
            "master": str(args.master),
            "game_version": master["meta"]["game_version"],
            "counts": {
                "entities": len(entities),
                "field_codes_total": len(field_codes),
                "master_field_codes_total": len(master["field_codes"]),
                "four_char_codes": n4,
                "non_four_char_codes": len(field_codes) - n4,
                "codes_with_entity": n_entity,
                "codes_without_entity": len(field_codes) - n_entity,
                "entity_top_level_codes_sum": sum(e["field_count"] for e in entities.values()),
                "entity_top_level_union": len({c for e in entities.values() for c in e["codes"]}),
                "codes_in_multiple_entities": len(conflicts),
            },
            "policies": {
                "entities.codes": "master.entity_summary codes verbatim (duplicates kept)",
                "client_codes": "top-level fields is_client_field=true (scope of codes)",
                "readonly_codes": "top-level fields is_read_only/read_only=true",
                "field_codes.entity": "full walk of entities (incl. list_item_fields); str|list|null",
                "field_codes.type": "master field_codes type verbatim",
                "property_map.property": "dbts enum-name column of PROPERTY_MAP.md sec.3",
            },
        },
    }
    # hard reconciliation gates
    if len(field_codes) != len(master["field_codes"]):
        sys.exit("reconciliation failed: field_codes count mismatch")
    anchors = anchor_check(vocab)
    if anchors["missing"]:
        sys.exit(f"anchor check failed: comp.xml#comp lacks {anchors['missing']} - parsing is wrong, fix first")
    vocab["meta"]["anchor_check"] = anchors

    pmap = parse_property_map(args.property_map, master)

    args.outdir.mkdir(parents=True, exist_ok=True)
    write_json(args.outdir / "vocab.json", vocab)
    write_json(args.outdir / "property_map.json", pmap)
    report = build_report(master, vocab, pmap, anchors, args)
    (args.outdir / "REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8", newline="\n")

    print(f"entities={len(entities)} field_codes={len(field_codes)} "
          f"four_char={n4} conflicts={len(conflicts)} property_map_rows={len(pmap['rows'])}")
    print(f"out: {args.outdir / 'vocab.json'}")
    print(f"out: {args.outdir / 'property_map.json'}")
    print(f"out: {args.outdir / 'REPORT.md'} ({len(report)} lines)")


if __name__ == "__main__":
    main()
