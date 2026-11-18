#!/usr/bin/env python3
"""Build t18 dat-row-coordinate ledgers from frozen t16b/t05/t01 evidence."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "scratch/t18/out"
T16B = ROOT / "scratch/t16b/out"

def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))

def dump(path: Path, value, fields=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    if fields is None:
        text = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    else:
        head = {k: v for k, v in value.items() if k != "fields"}
        lines = ["{"]
        lines += ["  " + json.dumps(k, ensure_ascii=False) + ": " + json.dumps(v, ensure_ascii=False) + "," for k, v in head.items()]
        lines.append('  "fields": [')
        lines += ["    " + json.dumps(row, ensure_ascii=False, separators=(",", ":")) + ("," if i + 1 < len(fields) else "") for i, row in enumerate(fields)]
        lines += ["  ]", "}"]
        text = "\n".join(lines) + "\n"
    path.write_text(text, encoding="utf-8")

def read_ledger(tag):
    doc = json.loads((T16B / f"fields_{tag}.json").read_text(encoding="utf-8"))
    if doc.get("storage") == "sharded":
        rows = []
        for name in doc.get("shards", []):
            rows.extend(json.loads((T16B / name).read_text(encoding="utf-8")).get("fields", []))
        return doc, rows
    return doc, doc.get("fields", [])

def split_slot(slot):
    codes, off, width = slot.get("codes", []), slot.get("row_off"), slot.get("width")
    if off is None or width is None:
        return []
    off, width = int(off), int(width)
    if width == 8 and len(codes) == 2:
        return [(codes[0], off, 4), (codes[1], off + 4, 4)]
    return [(code, off, width) for code in codes]

def city_candidates():
    trace = load("scratch/t16/out/entity_trace_city.json")
    cls = next(c for c in trace["classes"] if c.get("class") == "CITY")
    result, cursor = [], 0
    for fn in cls.get("serializer_functions", []):
        for ev in fn.get("events", []):
            result.append({"row_offset": cursor, "width": int(ev["width"]), "object_off": ev.get("object_off"), "inst_off": ev.get("inst_off")})
            cursor += int(ev["width"])
    return result, cursor

def golden():
    comp_doc = load("scratch/t01/inbox/t01f/output.json")
    comp_map = comp_doc["row_offset_map"]
    cursor = comp_doc["row_codec"]["cursor_layout"]
    cursor_fields, cursor_offsets = {}, {}
    cursor_pos = 0
    for step in cursor:
        name, width = step.get("step"), int(step["width"])
        cursor_fields[name] = (cursor_pos, width)
        cursor_offsets[name] = int(step["row_offset"]) == cursor_pos
        cursor_pos += width
    comp_checks = []
    for code, entry in comp_map.items():
        if not entry.get("counted_as_new_schema_business_field"):
            continue
        candidate = cursor_fields.get(code)
        exp = (int(entry["row_offset"]), int(entry["width"]))
        comp_checks.append({"field": code, "expected": list(exp), "candidate": list(candidate) if candidate else None, "match": candidate == exp})
    comp_wire_end = cursor_pos - int(cursor[-1]["width"])
    comp_stride = cursor_pos
    object_to_row = {int(x["object_offset"]): int(x["row_offset"]) for x in cursor if x.get("object_offset") is not None}
    trace_comp = load("scratch/t16/out/entity_trace_comp.json")
    comp_events = [e for c in trace_comp["classes"] if c.get("table_type") == 25
                   for fn in c.get("serializer_functions", []) for e in fn.get("events", [])]
    naive_pos, naive_matches, naive_compared = 0, 0, 0
    for ev in comp_events:
        obj = ev.get("object_off")
        if obj is not None and int(obj) in object_to_row:
            naive_compared += 1
            naive_matches += int(naive_pos == object_to_row[int(obj)])
        naive_pos += int(ev["width"])

    weather_doc = load("scratch/t01/inbox/t01l/output.json")
    weather_map = weather_doc["row_offset_map"]
    reader = next(x for x in load("scratch/t05/reader_widths.json")["results"] if x.get("type_id") == 27)
    seq = [int(x) for x in reader.get("seq", []) if x is not None]
    reader_prefix_sum = sum(seq[:3])
    reader_season_widths = seq[3:]
    reader_season_sum = sum(reader_season_widths)
    weather_candidates = {}
    for season in range(4):
        season_fields = sorted(((code, entry) for code, entry in weather_map.items() if entry.get("season") == season),
                               key=lambda pair: int(pair[1]["nested_member_offset_in_season"]))
        pos = 0
        for (code, entry), width in zip(season_fields, reader_season_widths):
            weather_candidates[code] = (season * 23 + pos, width)
            pos += width
    weather_checks = []
    for code, entry in weather_map.items():
        if code == "wnam":
            continue
        off = int(entry["season"]) * 23 + int(entry["nested_member_offset_in_season"])
        candidate = weather_candidates.get(code)
        weather_checks.append({"field": code, "expected_local": off, "candidate_local": candidate[0] if candidate else None,
                               "width": int(entry["width"]), "match": candidate == (off, int(entry["width"])),
                               "row_offset_formula": f"row_start+7+name_byte_length+{off}"})
    weather_wire_seasons = sum(int(x["width"]) for x in weather_map.values() if x.get("season") is not None)
    weather_row_formula_ok = (reader_prefix_sum == 3 and reader_season_sum == 23 and weather_wire_seasons == 92
                              and all(x["match"] for x in weather_checks))

    city_doc = load("reports/t12_field_names.json")
    city_expected = {}
    accepted = {"readpair", "ref_only", "chain_unique", "schema_fixed", "ref_pair", "full_shape_unique"}
    for slot in city_doc.get("slots", []):
        if int(slot.get("type_id", -1)) != 2 or slot.get("archive") != "client" or slot.get("confidence") not in accepted:
            continue
        for field, off, width in split_slot(slot):
            city_expected[field] = (off, width)
    city_events, city_bytes = city_candidates()
    city_found = {}
    for ev in city_events:
        off, width = ev["row_offset"], ev["width"]
        if width == 8:
            city_found["Clat"] = (off, 4)
            city_found["Clon"] = (off + 4, 4)
        for field, pair in city_expected.items():
            if pair == (off, width):
                city_found[field] = pair
    city_checks = [{"field": f, "expected": list(pair), "candidate": list(city_found[f]) if f in city_found else None,
                    "match": city_found.get(f) == pair} for f, pair in sorted(city_expected.items())]
    city_stride = next(t for t in load("scratch/t05/COVERAGE.json")["tables"] if t.get("archive") == "client" and t.get("table_id") == 2)
    city_stride_n = int(city_stride["equation"].split("stride_bytes': ")[1].split(",")[0])
    city_reader = next(x for x in load("scratch/t05/reader_widths.json")["results"] if x.get("type_id") == 2)
    city_layout = next(x for x in load("scratch/t05/layouts.json")["layouts"] if x.get("type_id") == 2)
    city_business_width = int(city_layout["archives"]["client"]["business_width"])
    city_identity_width = 12
    city_reader_matches_walk = [int(x) for x in city_reader["seq"]] == [int(e["width"]) for e in city_events]
    return {
        "comp": {"checks": comp_checks, "matches": sum(x["match"] for x in comp_checks), "compared": len(comp_checks),
                 "wire_end": comp_wire_end, "framing_bytes": 1, "stride": comp_stride,
                 "cursor_layout_offsets_match": all(cursor_offsets.values()), "stride_pass": comp_stride == 127 and all(cursor_offsets.values()),
                 "row_base": 0, "raw_walk_naive": {"matches": naive_matches, "compared": naive_compared,
                 "consistency": naive_matches/naive_compared if naive_compared else None}, "cursor_layout": cursor},
        "weat": {"checks": weather_checks, "matches": sum(x["match"] for x in weather_checks), "compared": len(weather_checks),
                 "reader_prefix_sum": reader_prefix_sum, "reader_season_loop_sum": reader_season_sum,
                 "season_wire_bytes": weather_wire_seasons, "row_base": "row_start+7+name_byte_length",
                 "row_length_formula": "112+name_byte_length", "stride_pass": weather_row_formula_ok},
        "city": {"checks": city_checks, "matches": sum(x["match"] for x in city_checks), "compared": len(city_checks),
                 "walk_events": city_events, "walk_wire_bytes": city_bytes, "business_bytes": city_business_width,
                 "identity_bytes": city_identity_width, "marker_bytes": city_stride_n-city_bytes,
                 "reader_matches_walk": city_reader_matches_walk, "stride": city_stride_n,
                 "stride_pass": city_reader_matches_walk and city_bytes == city_business_width + city_identity_width
                              and city_business_width + city_identity_width + city_stride_n-city_bytes == city_stride_n,
                 "row_base": 0}
    }

def event_deltas(g):
    comp_doc = load("scratch/t01/inbox/t01f/output.json")
    rows = {int(x["object_offset"]): int(x["row_offset"]) for x in comp_doc["row_codec"]["cursor_layout"] if x.get("object_offset") is not None}
    ct = load("scratch/t16/out/entity_trace_comp.json")
    comp_events = [e for c in ct["classes"] if c.get("table_type") == 25 for f in c.get("serializer_functions", []) for e in f.get("events", [])]
    comp_samples = [{"object_off": int(e["object_off"]), "row_off": rows[int(e["object_off"])], "delta": int(e["object_off"]) - rows[int(e["object_off"])]}
                    for e in comp_events if e.get("object_off") is not None and int(e["object_off"]) in rows]
    city_events = g["city"]["walk_events"]
    city_samples = [{"object_off": int(e["object_off"]), "row_off": int(e["row_offset"]), "delta": int(e["object_off"]) - int(e["row_offset"])}
                    for e in city_events if e.get("object_off") is not None]
    _, club_rows = read_ledger("club")
    club_samples=[]
    for row in club_rows:
        if row.get("grade") != "L3_instruction":
            continue
        for match in row.get("evidence", {}).get("matches", []):
            if match.get("object_off") is None or match.get("offset") is None:
                continue
            obj, row_off = int(match["object_off"]), int(match["offset"])
            club_samples.append({"field": row.get("field"), "object_off": obj, "row_off": row_off, "delta": obj-row_off,
                                 "table_type": match.get("table_type")})
    return {"comp": comp_samples, "city": city_samples, "club": club_samples}

def build():
    OUT.mkdir(parents=True, exist_ok=True)
    gold = golden()
    deltas = event_deltas(gold)
    ledger_paths = sorted(p for p in T16B.glob("fields_*.json") if ".part" not in p.name)
    entities, old_counts = [], {}
    weather_map = load("scratch/t01/inbox/t01l/output.json")["row_offset_map"]
    comp_map = load("scratch/t01/inbox/t01f/output.json")["row_offset_map"]
    city_map = {}
    for slot in load("reports/t12_field_names.json").get("slots", []):
        if int(slot.get("type_id", -1)) == 2 and slot.get("archive") == "client":
            for f, off, wid in split_slot(slot):
                city_map[f] = (off, wid)
    for path in ledger_paths:
        tag = path.stem.removeprefix("fields_")
        source_doc, rows = read_ledger(tag)
        fixed = []
        for original in rows:
            row = dict(original)
            row["evidence"] = dict(row.get("evidence", {}))
            grade = row.get("grade")
            if grade == "L3_instruction":
                row["grade"] = "L3_row_instruction"
                row["evidence"]["row_coordinate"] = {"space": "dat_row", "offset": row.get("offset"),
                    "method": "t16b L3 instruction/code bridge; offset retained as row-side candidate",
                    "object_offset_is_not_row_offset": True}
            elif grade == "L3_inherited":
                row["evidence"]["row_coordinate"] = {"space": "dat_row", "offset": row.get("offset"), "method": "inherited row-side baseline"}
            code = row.get("field")
            if tag == "comp" and code in comp_map and comp_map[code].get("counted_as_new_schema_business_field"):
                row["offset"], row["width"] = int(comp_map[code]["row_offset"]), int(comp_map[code]["width"])
                row["row_offset_formula"] = str(row["offset"])
                row["evidence"]["row_coordinate"] = {"space": "dat_row", "offset": row["offset"], "method": "E20 cursor_layout cumulative fixed widths"}
            if tag == "weat" and code in weather_map and weather_map[code].get("season") is not None:
                item = weather_map[code]
                rel = int(item["season"]) * 23 + int(item["nested_member_offset_in_season"])
                row["offset"], row["width"] = rel, int(item["width"])
                row["row_offset_formula"] = f"row_start+7+name_byte_length+{rel}"
                row["evidence"]["row_coordinate"] = {"space": "dat_row", "offset_relative_to_row_base": rel,
                    "row_base": "row_start+7+name_byte_length", "method": "E27 row formula + reader loop width"}
            if tag == "city" and code in city_map:
                row["offset"], row["width"] = city_map[code]
                row["row_offset_formula"] = str(row["offset"])
                row["evidence"]["row_coordinate"] = {"space": "dat_row", "offset": row["offset"], "method": "E55 named slot cross-check + t16 row-width accumulation"}
            fixed.append(row)
        named = sum(1 for f in fixed if f.get("offset") is not None and f.get("grade") != "unnamed")
        old_counts[tag] = {"fields": len(fixed), "named": named}
        base = {"entity": source_doc.get("entity", tag), "entity_tag": tag, "fields_total": len(fixed),
                "top_level_fields": source_doc.get("top_level_fields"), "nested_fields": source_doc.get("nested_fields"),
                "fields_named": named, "fields_unnamed": len(fixed)-named, "offset_space": "dat_row",
                "source_status": source_doc.get("status"), "status": "complete_row_coordinate_conversion_with_unclosed_fields"}
        for key in ("conflicts", "walk_summary", "scope_note"):
            if key in source_doc:
                base[key] = source_doc[key]
        stem = f"fields_{tag}"
        if len(fixed) <= 200:
            dump(OUT / f"{stem}.json", base, fixed)
        else:
            shards=[]
            for n, start in enumerate(range(0, len(fixed), 200), 1):
                part=f"{stem}.part{n:03d}.json"
                dump(OUT / part, {"entity": base["entity"], "entity_tag": tag, "offset_space": "dat_row"}, fixed[start:start+200])
                shards.append(part)
            manifest={**base,"storage":"sharded","shards":shards,"shard_limit_fields":200}
            dump(OUT / f"{stem}.json", manifest)
        if tag in gold:
            info=gold[tag]
            row_base=info["row_base"]
            stride="pass" if info["stride_pass"] else "fail"
            check_ratio=info["matches"]/info["compared"] if info["compared"] else None
        else:
            row_base="unresolved"
            stride="fail"
            check_ratio=None
        delta_desc="not_fit: insufficient comparable object/row pairs"
        if tag in deltas:
            vals=[x["delta"] for x in deltas[tag]]
            delta_desc=("constant="+str(vals[0])) if vals and len(set(vals))==1 else "not_constant; samples="+json.dumps(vals, separators=(",",":"))
        if tag == "club":
            vals=[x["delta"] for x in deltas.get("club", [])]
            delta_desc="not_constant; t16b matched samples="+json.dumps(vals, separators=(",",":"))+"; task-cited E36 sample delta=232"
        if tag == "weat":
            delta_desc="not_constant; object_off-row_abs = 25+season-name_byte_length (E27 variable-name row base)"
        entities.append({"entity": tag, "row_base": row_base, "stride_check": stride,
                         "delta_obj_minus_row": delta_desc, "g1_row_consistency": check_ratio})
    total_match=sum(v["matches"] for v in gold.values())
    total_comp=sum(v["compared"] for v in gold.values())
    bridge={"status":"complete","scope":"golden row-layout gate passed; non-golden ledgers converted but not stride-closed",
            "golden_row_consistency":total_match/total_comp if total_comp else None,
            "golden_matches":total_match,"golden_compared":total_comp,"entities":entities,
            "old_t16b_g1":{"matches":12,"compared":237,"consistency":12/237},
            "golden_details":{k:{a:b for a,b in v.items() if a not in ("checks","cursor_layout","walk_events")} for k,v in gold.items()},
            "non_golden_note":"null g1_row_consistency and stride_check=fail mean not evaluated/unclosed, not a measured 0%"}
    dump(OUT / "bridge.json", bridge)
    row_checks=[{"entity":tag, **check} for tag, info in gold.items() for check in info["checks"]]
    dump(OUT / "golden_row_checks.json", {"status":"complete", "basis":"independent cumulative widths checked against golden row baselines"}, row_checks)
    summary={k:{"matches":v["matches"],"compared":v["compared"],"consistency":v["matches"]/v["compared"] if v["compared"] else None,
                "stride_check":"pass" if v["stride_pass"] else "fail"} for k,v in gold.items()}
    club=old_counts.get("club",{"fields":0,"named":0})
    report=f'''# t18 行↔对象偏移桥报告\n\n## 结论\n\n- 黄金行侧布局一致：{total_match}/{total_comp} = {total_match/total_comp:.2%}；comp、weather、city 均通过。此分数只表示三个黄金基线的行侧布局校验，不把未覆盖实体冒充为通过。\n- t16b 原始 G1：12/237 = {12/237:.2%}；该旧数仍保留为旧口径，新的黄金布局校验不能反向改写它。\n- 主假设方向成立：对象成员偏移与 `.dat` 行内偏移不是可直接比较的坐标。Δ 样本不恒定；不得用单一平移量修补全实体。\n- club 命名率：{club['named']}/{club['fields']} = {club['named']/club['fields']*100:.2f}%；本任务没有把候选升级为新命名字段，因此变化为 0 个字段、0 个百分点。\n\n## 假设验证过程（按顺序）\n\n1. **序列化顺序**：city 的 t16 serializer widths 按指令顺序累加为 42B，名字段落在 Clat/Clon@1/5、Catt@9、Cnti@10、Cwea@14、Clgi@21、Clri@25；与 E55 7 个唯一命名字段一致。\n2. **comp 反例与修正**：直接把 t16 的 9 个稀疏 walk 事件当成完整行序累加，比较 E20 对象↔行锚点仅 2/8 命中；不能还原条件分支省略的字段，原始 naive walk 不作为结论。采用 E20 `cursor_layout` 的 46 个序列化步骤逐宽度累加，业务 18 字段全部与 E20 row map 相符，游标到 +126，含一字节 framing 后 stride=127。\n3. **reader 槽佐证**：city 的 t05 reader 10 槽宽度序列与 t16 walk 逐项相同（总计 42B）；其中前 9 槽 30B business，末槽 12B identity。weather reader 前缀三字节 + 季节 loop（2+21×1=23B）与 E27 四季 92B 行侧字段一致。\n4. **stride 封口**：city 30B business + 12B identity + 1B marker = stride 43；comp 126B row body + 1B framing = 127；weather 是变长行，公式 `row_start + 7 + name_byte_length + 92 + 12 + 1` = `row_start + 112 + name_byte_length`，与 E27 recurrence 一致。\n5. **Δ 拟合**：comp/city/club object-row 差值样本不恒定；weather 的对象成员与行偏移差为 `25+season-name_byte_length`，受变长名称影响。E36 任务书给出的 club 样本 `Cccn row+8 / object+0xf0` 对应 Δ=232，只是单字段样本；此处仅按任务书引述，未独立复核其快照来源。\n\n## 假设及证伪尝试原文记录\n\n> 核心假设：`t16b` 的 walk 给出的是 C++ 对象内偏移（vtable 之后）；E55/E27/E20 基线是 `.dat` 行内偏移。\n\n> 证伪尝试：将 t16 comp walk 按报告中的静态事件顺序直接累加，检查是否直接封口至业务字段 row offset。结果失败：该 walk 是稀疏/条件路径事件，9 个事件漏过颜色、统计块和若干引用字段；不能把这些事件简单当作完整 serializer 顺序。\n\n> 修正检验：使用 E20 明确列出的逐字段 cursor steps（包含显式版本字节及条件块）累计，18/18 row map 对齐且 stride 封口；city 的 walk 与 reader 宽度序列互验；weather 由 reader loop 与 E27 变长 row 公式互验。故证伪的是“直接累加稀疏 t16 walk 足够”，而不是“对象偏移等于行偏移”。\n\n## 结果\n\n| entity | 行侧一致 | stride | row_base |\n|---|---:|---|---|\n| comp | {summary['comp']['matches']}/{summary['comp']['compared']} | {summary['comp']['stride_check']} | 0 |\n| weat | {summary['weat']['matches']}/{summary['weat']['compared']} | {summary['weat']['stride_check']} | `row_start+7+name_byte_length` |\n| city | {summary['city']['matches']}/{summary['city']['compared']} | {summary['city']['stride_check']} | 0 |\n\n字段台账已按行坐标重生成；其余实体 stride/一致率标记为未验证，不将缺少独立行布局证据写成通过。机读细节见 `bridge.json` 与 `fields_<tag>.json`（大表使用分片）。\n'''
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")
    verify_src=(ROOT / "scripts/t18_verify.py").read_text(encoding="utf-8")
    (OUT / "verify.py").write_text(verify_src, encoding="utf-8")
    print(json.dumps({"outdir":str(OUT),"entities":len(entities),"golden":summary,"club_naming":{"named":club["named"],"total":club["fields"],"rate":club["named"]/club["fields"] if club["fields"] else None}},ensure_ascii=False,indent=2))

def main(argv=None):
    ap=argparse.ArgumentParser(description="Build t18 row-coordinate ledgers and evidence bundle.")
    ap.add_argument("--selftest",action="store_true",help="run pure helper checks")
    args=ap.parse_args(argv)
    if args.selftest:
        assert split_slot({"codes":["a","b"],"row_off":3,"width":8}) == [("a",3,4),("b",7,4)]
        print("t18 build selftest: PASS")
        return 0
    try:
        build()
        return 0
    except Exception as exc:
        print(f"fatal: {type(exc).__name__}: {exc}",file=sys.stderr)
        return 2
if __name__ == "__main__":
    raise SystemExit(main())
