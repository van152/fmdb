#!/usr/bin/env python3
"""Build t19's offline cursor-layout and field-ledger artifacts from frozen workspace evidence."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "scratch" / "t19" / "out"


def load(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def render_json(data, depth: int = 0) -> str:
    pad = "  " * depth
    child = "  " * (depth + 1)
    if isinstance(data, dict):
        if not data:
            return "{}"
        lines = ["{"]
        items = list(data.items())
        for i, (key, value) in enumerate(items):
            rendered = render_json(value, depth + 1)
            comma = "," if i + 1 < len(items) else ""
            if "\n" in rendered:
                lines.append(f"{child}{json.dumps(key, ensure_ascii=False)}: {rendered.replace(chr(10), chr(10) + child)}{comma}")
            else:
                lines.append(f"{child}{json.dumps(key, ensure_ascii=False)}: {rendered}{comma}")
        lines.append(pad + "}")
        return "\n".join(lines)
    if isinstance(data, list):
        if not data:
            return "[]"
        if all(isinstance(item, dict) for item in data):
            lines = ["["]
            for i, item in enumerate(data):
                comma = "," if i + 1 < len(data) else ""
                lines.append(child + json.dumps(item, ensure_ascii=False, separators=(",", ":")) + comma)
            lines.append(pad + "]")
            return "\n".join(lines)
        if all(not isinstance(item, (dict, list)) for item in data):
            return json.dumps(data, ensure_ascii=False, separators=(",", ":"))
        lines = ["["]
        for i, item in enumerate(data):
            comma = "," if i + 1 < len(data) else ""
            lines.append(child + render_json(item, depth + 1) + comma)
        lines.append(pad + "]")
        return "\n".join(lines)
    return json.dumps(data, ensure_ascii=False)


def dump(rel: str, data, pretty: bool = True):
    path = OUT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    text = (render_json(data) if pretty else json.dumps(data, ensure_ascii=False, separators=(",", ":"))) + "\n"
    if len(text.splitlines()) > 400:
        raise ValueError(f"single output exceeds 400 lines: {rel}")
    path.write_text(text, encoding="utf-8")


def dump_field_part(rel: str, entity: str, tag: str, part: int, parts: int, fields: list[dict]):
    path = OUT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["{", f'  "entity": {json.dumps(entity)},', f'  "entity_tag": {json.dumps(tag)},',
             f'  "offset_space": "dat_row",', f'  "part": {part},', f'  "parts": {parts},', '  "fields": [']
    for i, field in enumerate(fields):
        comma = "," if i + 1 < len(fields) else ""
        lines.append("    " + json.dumps(field, ensure_ascii=False, separators=(",", ":")) + comma)
    lines.extend(["  ]", "}"])
    text = "\n".join(lines) + "\n"
    if len(lines) > 400 or len(text.encode("utf-8")) > 50_000:
        raise ValueError(f"field shard exceeds budget: {rel}, {len(lines)} lines, {len(text)} bytes")
    path.write_text(text, encoding="utf-8")


def hex_off(value):
    return None if value is None else f"0x{int(value):x}"


def build_fields(entity: str, tag: str, top_level: dict[str, dict], named_entries: list[dict], extra: dict[str, dict]):
    inventory = load("scratch/t05/schema_inventory.json")["entities"][entity]["fields"]
    named_by_code: dict[str, dict] = {}
    for entry in named_entries:
        code = entry.get("field")
        if entry.get("grade") != "unnamed":
            if code in named_by_code:
                raise ValueError(f"duplicate named ledger code in {entity}: {code}")
            named_by_code[code] = entry
    result = []
    for schema_field in inventory:
        code = schema_field["code"]
        idx = schema_field["idx"]
        prior = named_by_code.get(code) if schema_field.get("parent") is None else None
        rec = {"field": code, "row_offset": None, "width": None, "grade": "unnamed",
               "evidence": {"reason": "No row coordinate promoted by t19; retain unnamed until cursor path is reconciled."},
               "schema_index": idx, "parent": schema_field.get("parent"), "type": schema_field.get("type")}
        if prior is not None:
            rec.update({"row_offset": prior.get("offset"), "width": prior.get("width"), "grade": prior["grade"],
                        "evidence": {"carried_from": f"scratch/t18/out/fields_{tag}.part*.json",
                                     "prior_source": prior.get("source"), "prior_evidence": prior.get("evidence"),
                                     "t19_disposition": "preserved; not independently revalidated against the rebuilt cursor"}})
        if schema_field.get("parent") is None and code in extra:
            rec.update(extra[code])
        result.append(rec)
    return result


def main_build():
    OUT.mkdir(parents=True, exist_ok=True)
    inv = load("scratch/t05/schema_inventory.json")
    widths = load("scratch/t05/reader_widths.json")
    coverage = load("scratch/t05/COVERAGE.json")
    club_src = load("scratch/t02/inbox/club_v2/output.json")
    club_t18 = load("scratch/t18/out/fields_club.json")
    nation_src = load("scratch/t01/inbox/t01g/output.json")
    codes = load("scratch/t12/out/codes_full.json")
    manifest = load("evidence/MANIFEST.json")
    schema_path = ROOT / "evidence" / "fm24" / "reports" / "editor_schema" / "master.json"
    schema_sha = hashlib.sha256(schema_path.read_bytes()).hexdigest()
    expected = next(x["sha256"] for x in manifest["files"]
                    if x["path"] == "evidence/fm24/reports/editor_schema/master.json")
    if schema_sha != expected:
        raise ValueError("frozen master schema hash differs from evidence/MANIFEST.json")

    reader3 = next(x for x in widths["results"] if x["type_id"] == 3)
    reader10 = next(x for x in widths["results"] if x["type_id"] == 10)
    prefix = nation_src["row_codec"]["cursor_layout"]
    prefix_widths = [x["width"] for x in prefix]
    prefix_objs = [int(x["object_offset"], 16) if isinstance(x.get("object_offset"), str) else None for x in prefix]
    if reader10["seq"][15:25] != prefix_widths or reader10["obj_seq"][15:24] != prefix_objs[:9]:
        raise ValueError("nation prefix cursor does not align to reader_widths entries 15..23")
    if prefix_objs[9] is not None or reader10["obj_seq"][24] != 68:
        raise ValueError("expected the t01g scratch byte vs reader-width object+0x44 sink discrepancy")

    club_class_tracks = [
        {"id": "CLUB_5B_block", "status": "row-frame-observed; class discriminator not independently established",
         "id_block": {"row_offset": 16, "width": 5}, "group_status": {"row_offset": 21, "width": 4},
         "flag": {"row_offset": 25, "width": 1}, "name_length": {"row_offset": 26, "width": 4}},
        {"id": "LEAGUE_BODY_CLUB_4B_block", "status": "row-frame-observed; accepted split is not a per-row class byte",
         "id_block": {"row_offset": 16, "width": 4}, "group_status": {"row_offset": 20, "width": 4},
         "flag": {"row_offset": 24, "width": 1}, "unassigned_byte": {"row_offset": 25, "width": 1},
         "name_length": {"row_offset": 26, "width": 4}},
    ]
    club_layout = [
        {"step": "db_id", "row_offset": 0, "width": 4, "grade": "L1_structural_only", "formula": "fixed"},
        {"step": "parent_ref_candidate", "row_offset": 4, "width": 4, "grade": "L1_structural_only", "formula": "fixed"},
        {"step": "Cccn_candidate_duplicate_id", "row_offset": 8, "width": 4, "grade": "L3_inherited", "formula": "fixed; low-confidence inherited anchor"},
        {"step": "duplicate_u32", "row_offset": 12, "width": 4, "grade": "L1_structural_only", "formula": "fixed"},
        {"step": "class_id_block", "row_offset": 16, "width": {"CLUB": 5, "LEAGUE_BODY_CLUB": 4}, "grade": "L1_structural_only", "formula": "selected by unresolved class track"},
        {"step": "group_status", "row_offset": {"CLUB": 21, "LEAGUE_BODY_CLUB": 20}, "width": 4, "grade": "L1_structural_only", "formula": "class-specific"},
        {"step": "flag_candidate", "row_offset": {"CLUB": 25, "LEAGUE_BODY_CLUB": 24}, "width": 1, "grade": "L1_structural_only", "formula": "class-specific"},
        {"step": "LEAGUE_BODY_CLUB_unassigned", "row_offset": 25, "width": 1, "grade": "unnamed", "formula": "only 4B class track"},
        {"step": "full_name_length", "row_offset": 26, "width": 4, "grade": "L1_structural_only", "formula": "fixed"},
        {"step": "full_name_bytes", "row_offset": 30, "width": "full_name_len", "grade": "unnamed", "formula": "row+30, then advance by UTF-8 byte length"},
        {"step": "short_name_length", "row_offset": "30+full_name_len", "width": 4, "grade": "L1_structural_only", "formula": "variable"},
        {"step": "short_name_bytes", "row_offset": "34+full_name_len", "width": "short_name_len", "grade": "unnamed", "formula": "variable"},
        {"step": "unresolved_3B_block", "row_offset": "34+full_name_len+short_name_len", "width": 3, "grade": "unnamed", "formula": "fixed after names"},
        {"step": "identity_suffix", "row_offset": "row_end-13", "width": 12, "grade": "L1_structural_only", "formula": "identity/ordinal framing; semantics not assigned"},
        {"step": "row_marker", "row_offset": "row_end-1", "width": 1, "grade": "L1_structural_only", "formula": "row trailer"},
    ]
    cccn = codes["codes"].get("Cccn", [])
    cccn_desc = next((x for x in cccn if x.get("shape") == "path_descend"), None)
    club_summary = {
        "task": "t19", "entity": "club", "table_id": 3,
        "status": "partial_frame_closed_reader_unreconciled",
        "row_coordinate_space": "client_db.dat table_3 row-relative bytes",
        "structure_first": True,
        "block_structure": club_class_tracks,
        "cursor_layout": club_layout,
        "row_frame_formula": {
            "standard": "row_length = 50 + full_name_utf8_bytes + short_name_utf8_bytes",
            "name_cursor": "26:u32(full_len), 30:full_name, 30+full_len:u32(short_len), 34+full_len:short_name",
            "tail": "3B unresolved block + 12B identity suffix + 1B marker",
            "compact_rows": {"count": 3, "span": 55, "identity_relative_offset": 42, "body_semantics": "unparsed"},
        },
        "class_partition": {"accepted_rows": club_src["class_partition"]["rows"],
                            "rule": club_src["class_partition"]["rule"],
                            "class_byte_or_flag_found": False,
                            "warning": "contiguous ordinal split is not used to promote field names"},
        "serializer_branch_structure": {
            "mode": "mixed / dual RTTI", "table_type": 3,
            "walk_summary": next(x for x in club_t18["walk_summary"]["class_branches"] if x.get("table_type") == 3),
            "class_reader_evidence": club_src["class_reader_evidence"],
            "interpretation": "CLUB slot19 reader and LEAGUE_BODY_CLUB thunk/reader are distinct tracks; no row class selector was established",
        },
        "reader_models": [{
            "reader": reader3["reader"], "mode": reader3["mode"], "calls": reader3["calls"],
            "cursor_layout": [{"call_index": i, "width": w, "object_offset": reader3["obj_seq"][i],
                               "row_offset": None, "status": "unplaced; mixed branch/helper cursor not reconciled"}
                              for i, w in enumerate(reader3["seq"])],
            "widths": reader3["seq"], "object_offsets": reader3["obj_seq"],
        }, {
            "reader_track": "Cccn local sink candidate", "reader_file_offset": "0xe5a7a0",
            "object_offset_candidate": "0xf0", "transfer_width": 4,
            "reader_destination": {"file_offset": "0xe5a864", "bytes": "49 8d be f0 00 00 00"},
            "width_instruction": {"file_offset": "0xe5a86e", "bytes": "41 b8 04 00 00 00"},
            "getter_cmp": {"file_offset": "0xe8b7bf", "bytes": "81 fb 6e 63 63 43"},
            "codes_full_crosscheck": cccn_desc,
            "status": "inherited low-confidence; not aligned to complete row cursor",
        }],
        "boundary_evidence": {"count": club_src["count"], "walked_rows": club_src["walked_rows"],
                              "member_length": club_src["member_length"],
                              "row_body_end_member_offset": club_src["row_body_end_member_offset"],
                              "footer_offset": club_src["footer_offset"], "footer_hex": club_src["footer_hex"],
                              "footer_exact": club_src["footer_exact"],
                              "standard_layout_rows": club_src["standard_layout_rows"],
                              "compact_rows": len(club_src["class_partition"]["compact_rows_inside_LEAGUE_BODY_CLUB_segment"])},
        "sources": ["scratch/t02/inbox/club_v2/output.json", "scratch/t05/reader_widths.json",
                    "scratch/t12/out/codes_full.json", "scratch/t18/out/fields_club.part*.json"],
    }
    dump("cursor_club.json", club_summary)

    nation_calls = []
    # The first nine object sinks align; call 24 is same-width but object+0x44, not t01g's stack scratch byte.
    prefix_by_call = {15 + i: step for i, step in enumerate(prefix[:9])}
    for i, (w, obj) in enumerate(zip(reader10["seq"], reader10["obj_seq"])):
        step = prefix_by_call.get(i)
        if step:
            entry = {"step": step["step"], "reader_call_index": i,
                     "row_offset": step["row_offset_in_body"], "width": w,
                     "object_offset": step.get("object_offset"),
                     "offset_formula": "linear prefix; cumulatively verified from body start",
                     "evidence": step["reader"]}
        else:
            if i < 15:
                track = "pre_prefix_unreconciled_branch"
            elif i == 24:
                track = "same_width_different_object_sink_vs_t01g_scratch_byte"
            else:
                track = "post_prefix_after_counted_collections"
            entry = {"step": f"reader_transfer_{i:02d}", "reader_call_index": i,
                     "row_offset": None, "width": w, "object_offset": hex_off(obj),
                     "offset_formula": "unresolved; reader has 11 conditional branches and counted collections",
                     "track": track,
                     "evidence": {"reader": reader10["reader"], "width_sequence_source": "scratch/t05/reader_widths.json"}}
        nation_calls.append(entry)
    nation_summary = {
        "task": "t19", "entity": "nation", "table_id": 10,
        "status": "partial_prefix_cursor_tail_and_loops_unresolved",
        "row_coordinate_space": "client_db.dat table_10 body-relative candidate; complete row starts not recovered",
        "reader": reader10["reader"], "reader_call_count": reader10["calls"],
        "conditional_branch_count": 11,
        "cursor_layout": nation_calls,
        "verified_prefix": {"status": "L3 cursor chain + L1 one-prefix byte spot-check; not all 251 row starts",
                            "steps": [{"step": x["step"], "row_offset": x["row_offset_in_body"],
                                       "width": x["width"], "object_offset": x["object_offset"],
                                       "evidence": x["reader"],
                                       "payload_spotcheck": x.get("client_payload_prefix_spotcheck")}
                                      for x in prefix],
                            "widths": prefix_widths, "body_bytes": sum(prefix_widths),
                            "reader_widths_crosscheck": "calls 15..23 match widths+object offsets; call 24 is 1B but sinks to object+0x44 rather than t01g stack scratch byte"},
        "counted_blocks": [
            {"id": "arg8_nonzero_conditional_count", "count_width": 2,
             "element_width": 4, "loop_count_source": "u16 count read under arg8!=0",
             "evidence": nation_src["row_codec"]["variable_collection_path"],
             "client_server_assignment": "unproven"},
            {"id": "ordinary_path_byte_counted_helper_list", "count_offset": 24,
             "count_width": 1, "sample_count": 3, "element_width": None,
             "body_step": "helper per item; wire width/cursor advance not recovered",
             "evidence": nation_src["row_codec"]["ordinary_path_counted_collections"]},
            {"id": "ordinary_path_following_dword_count_loop", "count_width": 4,
             "element_width": None, "body_step": "loop body cursor width not recovered",
             "evidence": nation_src["row_codec"]["ordinary_path_counted_collections"]},
        ],
        "payload_envelope": {"payload_size": 24732, "record_count": 251, "header_bytes": 14,
                             "data_bytes": 24710, "footer_bytes": 8,
                             "equation": "14 + 24710 + 8 = 24732",
                             "scope": "global payload envelope only; not a per-record cursor/loop closure"},
        "sources": ["scratch/t01/inbox/t01g/output.json", "scratch/t05/reader_widths.json",
                    "scratch/t05/COVERAGE.json", "evidence/fm24/reports/dbdat_decode/client_table_10_nation_locator.json"],
    }
    dump("cursor_nation.json", nation_summary)

    old_club = []
    for p in sorted((ROOT / "scratch" / "t18" / "out").glob("fields_club.part*.json")):
        old_club.extend(load(str(p.relative_to(ROOT)))["fields"])
    if sum(x.get("grade") != "unnamed" for x in old_club) != 14:
        raise ValueError("t18 club field baseline differs from expected 14/672")
    old_nation = []
    for p in sorted((ROOT / "scratch" / "t18" / "out").glob("fields_nati.part*.json")):
        old_nation.extend(load(str(p.relative_to(ROOT)))["fields"])
    if sum(x.get("grade") != "unnamed" for x in old_nation) != 0:
        raise ValueError("t18 nation named-field baseline is not 0/441")

    # Carry the 14 existing t18 named rows without upgrading them; Cccn remains inherited low-confidence.
    club_extra = {"Cccn": {"row_offset": 8, "width": 4, "grade": "L3_inherited",
        "evidence": {"source": "scratch/t05/club_align2/club_fields.json + REPORT.md",
                     "status": "inherited_low_confidence_candidate_not_revalidated",
                     "reader_destination": "editor.exe+0xe5a864: 49 8d be f0 00 00 00",
                     "width_instruction": "editor.exe+0xe5a86e: 41 b8 04 00 00 00",
                     "getter_cmp": "editor.exe+0xe8b7bf: 81 fb 6e 63 63 43",
                     "codes_full_shape": cccn_desc,
                     "counterevidence": "reader_widths type 3 has no object_off=240 entry; codes_full retains only path_descend, not a direct read; row 69709 +8 duplicates +0 in the LEAGUE_BODY_CLUB sample",
                     "not_a_t19_new_mapping": True}}}
    club_fields = build_fields("club", "club", {}, old_club, club_extra)

    nation_map = nation_src["row_offset_map"]
    nation_extra = {}
    for code, mapping in nation_map.items():
        if code not in {"Ngct", "Ncti", "Nrgi", "Ncur", "Nsod", "Necf", "Nygn"}:
            continue
        nation_extra[code] = {"row_offset": mapping["row_offset"], "width": mapping["width"],
                              "grade": "L3_inherited",
                              "evidence": {"source": "scratch/t01/inbox/t01g/output.json",
                                           "evidence_level": mapping["evidence_level"],
                                           "object_offset": mapping["object_offset"],
                                           "serializer": mapping["serializer"],
                                           "field_getter_link": mapping.get("field_getter_link"),
                                           "prefix_spotcheck": next((x.get("client_payload_prefix_spotcheck")
                                               for x in prefix if x["step"] == code), None),
                                           "t19_disposition": "inherited prefix; not expanded to later row fields"}}
    nation_fields = build_fields("nation", "nati", {}, old_nation, nation_extra)

    for entity, tag, fields in (("club", "club", club_fields), ("nation", "nati", nation_fields)):
        parts = [fields[i:i + 100] for i in range(0, len(fields), 100)]
        shard_names = []
        for part_no, chunk in enumerate(parts, 1):
            name = f"fields_{entity}.part{part_no:03d}.json"
            dump_field_part(name, entity, tag, part_no, len(parts), chunk)
            shard_names.append(name)
        grade_counts = dict(Counter(x["grade"] for x in fields))
        summary = {"entity": entity, "entity_tag": tag, "status": "partial_cursor_reconciliation",
                   "offset_space": "dat_row", "fields_total": len(fields),
                   "top_level_fields": sum(x.get("parent") is None for x in fields),
                   "nested_fields": sum(x.get("parent") is not None for x in fields),
                   "grade_counts": grade_counts, "named_fields": len(fields) - grade_counts.get("unnamed", 0),
                   "shards": shard_names, "shard_limit_fields": 100,
                   "schema_snapshot_sha256": schema_sha}
        dump(f"fields_{entity}.json", summary)

    report = """# t19 — club/nation cursor_layout 重建（partial）\n\n## 结论 / 状态\n\n- `status=partial_cursor_club_frame_closed_nation_prefix_only`。按要求先拆结构；没有把未闭合的 reader 路径伪装成 E20 式全量字段序列。\n- club 的 **行框架** 可复算并封口：84,259 行、3 个 compact body 未解；但 `mixed / dual RTTI` reader 的 41 个 transfer calls 含动态 helper/分支，未与完整 row cursor 对齐。表型证据分开记录：CLUB slot19 `0xe5a7a0`；LEAGUE_BODY_CLUB thunk 解包到 `0x43beba0`，另见 4B/1B 对象传输。无逐行 class selector。\n- nation 复建出 t01g 的 25B 前缀（10 transfers，width sum=25）及 7 个字段；后续 count/helper 循环体线宽、每行边界仍未知。总 payload 包络能闭合，不等于逐行 loop closure。\n\n## club 结构图\n\n```text\nrow+0  db_id u32 | +4 parent/ref u32 | +8 duplicate/Cccn? u32 | +12 duplicate u32\n+16  class split: CLUB 5B  OR  LEAGUE_BODY_CLUB 4B + separate +20 byte\n+20/21 group/status u32 | +24/25 flag byte | (4B track only: +25 unassigned byte)\n+26  full-name byte length u32 | +30 UTF-8 full name [N]\n+30+N short-name byte length u32 | +34+N short name [M]\n+34+N+M unresolved 3B | row_end-13 identity suffix 12B | row_end-1 marker\n```\n\nStandard row equation: `row_length = 50 + N + M`. Samples in `club_v2/output.json` satisfy it; all 84,256 standard rows and the 3 compact rows sum to 84,259. Parser footer: `0x69c66a + 8 = 6,932,082`; `footer_exact=true`. The contiguous class split is accepted in the upstream artifact but **not** chosen by a proven per-row discriminator. Compact rows 69706..69708 remain identity-framed only.\n\n`Cccn@+8/4` is carried as `L3_inherited`, not a t19 discovery. The prior local reader bytes point at object `+0xf0`, width 4, getter cmp Cccn; however `codes_full.json` has only a `path_descend` record (no direct object_off read), the type-3 width trace has no object offset 240, and sample row 69709 has `row+8 == row+0`. Therefore Cccn is low-confidence and does not validate the reader/frame merge. The E20-like cumulative row layout is **not** an alignment of 41 C++ transfers.\n\n## nation 结构图\n\n```text\nbody+0..24: 1,4,4,4,4,1,1,4,1,1 = 25B\nbody+24: scratch/count byte (sample 3) -> helper item loop (wire width unknown)\nthen: u32 count -> loop body unresolved\nseparate arg8!=0 branch: u16 count -> repeated 4B transfer; client/server assignment unproven\n```\n\nThe 40-call `reader_widths` trace aligns calls 15..23 to the first nine prefix steps (width and object offsets); call 24 is also 1B but writes to object+0x44 rather than t01g's stack scratch byte. Calls 0..14 belong to an unreconciled path; calls 25..39 follow count-driven blocks and have no safely assignable row offsets. t01g explicitly records `complete_rows_verified=0`; its 7 prefix fields are inherited as L3, not promoted to a complete row parser. Table envelope `14+24,710+8=24,732` is a payload boundary check only. The required loop-body step and count closure remain blocked.\n\n## 命名率与台账\n\n- club: t18 baseline 14/672 → t19 ledger 15/672 (2.23%). Difference is only carried `Cccn`; **0 new independent L3 mappings**. All old 14 entries retain their t18 grade/evidence and are marked not revalidated against the reconstructed cursor.\n- nation: t18 baseline 0/441 → t19 7/441 (1.59%); the seven t01g prefix mappings are inherited. Remaining 434 fields stay `unnamed`.\n- Full schema ledger entries include top-level and nested fields; `fields_*.json` are manifests and `.partNNN.json` are ≤100-field shards.\n\n## 校验 / 未闭合项\n\n`verify.py --selftest` validates formulas and instruction-byte decoding. Default verification checks club footer/sample closure, nation prefix sequence, schema baseline comparison and payload envelope. It returns code 1 because per-row nation loop closure and club reader-to-frame alignment are still unproven.\n\n证伪/保留：不把 club 5B byte-walker aggregate 等同语义 5B 字段；不按 ordinal/marker/name 推断 class；不把 t01g 的 arg8 分支命名为 client/server；不把 251 行与全 payload envelope 当成 251 个 row-start 已恢复。\n\n## 来源与冻结快照\n\n- `scratch/t02/inbox/club_v2/output.json`, `scratch/t05/reader_widths.json`, `scratch/t05/schema_inventory.json`, `scratch/t12/out/codes_full.json`, `scratch/t18/out/fields_*`.\n- `scratch/t01/inbox/t01g/output.json` 与 `scratch/t01/inbox/t01g/REPORT.md`; table_10 locator: `evidence/fm24/reports/dbdat_decode/client_table_10_nation_locator.json`.\n- schema snapshot `evidence/fm24/reports/editor_schema/master.json`, SHA-256 `""" + schema_sha + """`; compared to `evidence/MANIFEST.json` (snapshot date 2026-11-18).\n- 未联网，外部输入只读；所有新文件仅落于 `scratch/t19/out/` 与 `scripts/t19_build.py`。\n"""
    report_path = OUT / "REPORT.md"
    report_path.write_text(report, encoding="utf-8")
    if len(report.splitlines()) > 400:
        raise ValueError("REPORT.md exceeds 400 lines")
    print(f"built {OUT}; club={len(club_fields)} fields/{sum(x['grade'] != 'unnamed' for x in club_fields)} named; "
          f"nation={len(nation_fields)} fields/{sum(x['grade'] != 'unnamed' for x in nation_fields)} named")


def selftest():
    assert 16 + 5 + 4 + 1 + 4 + 33 + 4 + 12 + 3 + 12 + 1 == 95
    assert 50 + 33 + 12 == 95
    assert sum([1, 4, 4, 4, 4, 1, 1, 4, 1, 1]) == 25
    assert 14 + 24710 + 8 == 24732
    assert bytes.fromhex("81 fb 6e 63 63 43")[2:6][::-1].decode("ascii") == "Cccn"
    print("t19_build selftest: PASS")


def cli():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selftest", action="store_true", help="run internal formula checks without writing")
    parser.add_argument("--build", action="store_true", help="build outputs (default action)")
    args = parser.parse_args()
    try:
        if args.selftest:
            selftest()
            return 0
        main_build()
        return 0
    except (OSError, ValueError, KeyError, StopIteration, AssertionError) as exc:
        print(f"fatal: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(cli())
