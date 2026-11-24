#!/usr/bin/env python3
"""Rebuild t22's server-row cursor and field ledger from frozen workspace evidence."""
from __future__ import annotations
import sys as _cfg_sys
from pathlib import Path as _cfg_pathlib
_cfg_sys.path.insert(0, str(_cfg_pathlib(__file__).resolve().parent))
import fm24_config as _cfg

import argparse
import csv
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "scratch" / "t20" / "out"
# FM24_DB_DIR points at the decoded data workspace; the static binary is the
# read-only editor.exe reference used by t14/t16, not under that data directory.
EDITOR = Path(str(_cfg.EDITOR_EXE))
CSV_T22 = ROOT / "scratch" / "t13d" / "out" / "t22.csv"
AUDIT = ROOT / "scratch" / "t13d" / "out" / "audit.json"
CENSUS = ROOT / "scratch" / "t14" / "out" / "census.json"
READER_WIDTHS = ROOT / "scratch" / "t05" / "reader_widths.json"
SCHEMA = ROOT / "scratch" / "t05" / "schema_inventory.json"
CODES = ROOT / "scratch" / "t12" / "out" / "codes_full.json"
IDENTITY = ROOT / "reports" / "stage2_table_identity.json"

EXPECTED_T22_WIDTHS = [4, 4, 4, 4, 1, 4, 1, 4, 4, 4, 4, 4, 1, 4, 1, 1, 1, 4, 12]
CODE_INSTANCE_REGION = (0x1538E00, 0x1539400)
E56_CODES = {"Salt", "Scam", "Scpm", "Slhm"}
LINEAR_CODE_CANDIDATE_OFFSETS = {"Salt": 17, "Scam": 43, "Scpm": 21, "Slhm": 42}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def write_compact_records(path: Path, doc: dict[str, Any], record_key: str) -> None:
    """Write nested metadata compactly and one compact JSON record per list item."""
    records = doc[record_key]
    lines = ["{"]
    items = [(k, v) for k, v in doc.items() if k != record_key]
    for key, value in items:
        lines.append("  " + json.dumps(key, ensure_ascii=False) + ": " +
                     json.dumps(value, ensure_ascii=False, separators=(",", ":")) + ",")
    lines.append("  " + json.dumps(record_key) + ": [")
    for i, item in enumerate(records):
        comma = "," if i + 1 < len(records) else ""
        lines.append("    " + json.dumps(item, ensure_ascii=False, separators=(",", ":")) + comma)
    lines.extend(["  ]", "}"])
    text = "\n".join(lines) + "\n"
    if len(lines) > 400 or len(text.encode("utf-8")) > 50_000:
        raise ValueError(f"output budget exceeded: {path.name} ({len(lines)} lines, {len(text)} bytes)")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
def import_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import helper: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
def selftest() -> bool:
    cursor = 0
    starts = []
    for width in EXPECTED_T22_WIDTHS:
        starts.append(cursor)
        cursor += width
    expected_candidates = {"Salt": starts[5], "Scam": starts[13],
                           "Scpm": starts[6], "Slhm": starts[12]}
    return (cursor == 66 and starts[5] == 17 and starts[12] == 42 and
            starts[13] == 43 and 66 + 13 == 79 and
            LINEAR_CODE_CANDIDATE_OFFSETS == expected_candidates and
            set(LINEAR_CODE_CANDIDATE_OFFSETS) == E56_CODES)
def row_profile(rows: list[bytes], offset: int, width: int) -> dict[str, Any]:
    cells = [row[offset:offset + width] for row in rows]
    values = [int.from_bytes(cell, "little") for cell in cells]
    full_ff = (1 << (8 * width)) - 1
    return {
        "distinct": len(set(cells)),
        "min_le": min(values),
        "max_le": max(values),
        "zero_count": sum(v == 0 for v in values),
        "all_ff_count": sum(v == full_ff for v in values),
        "sample_row0_hex": cells[0].hex(),
    }
def trace_t22(census_row: dict[str, Any]) -> tuple[Any, dict[str, Any]]:
    """Run t16's existing static class walk in-memory; it writes no artifacts."""
    walker_mod = import_module("_t16_t20", ROOT / "scripts" / "t16_serializer_walk.py")
    walker = walker_mod.Walker()
    trace = walker.class_trace(census_row)
    if trace.get("status") != "ok" or not trace.get("serializer_functions"):
        raise RuntimeError(f"t16 serializer walk failed for t22: {trace.get('status')}")
    return walker, trace
def build() -> tuple[dict[str, Any], dict[str, Any]]:
    required = (EDITOR, CSV_T22, AUDIT, CENSUS, READER_WIDTHS, SCHEMA, CODES, IDENTITY)
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError("missing inputs: " + ", ".join(missing))
    census_doc = load_json(CENSUS)
    census_row = next(x for x in census_doc["tables"] if int(x["table_type"]) == 22)
    identity = next(x for x in load_json(IDENTITY)["rows"] if int(x["table_type"]) == 22)
    reader_doc = load_json(READER_WIDTHS)
    reader = next(x for x in reader_doc["results"] if int(x["type_id"]) == 22)
    schema = load_json(SCHEMA)
    codes_doc = load_json(CODES)
    codes = codes_doc["codes"]
    audit = next(x for x in load_json(AUDIT)["tables"] if int(x["table_type"]) == 22)

    with CSV_T22.open("r", encoding="utf-8", newline="") as handle:
        csv_rows = list(csv.DictReader(handle))
    rows = [bytes.fromhex(row["raw_hex"]) for row in csv_rows]
    if len(rows) != 449 or any(len(row) != 79 for row in rows):
        raise ValueError("t22 CSV is not the expected 449 x 79-byte row set")
    for index, row in enumerate(csv_rows):
        if int(row["row"]) != index or int(row["offset"]) != 14 + index * 79 or int(row["len"]) != 79:
            raise ValueError(f"t22 row coordinate mismatch at row {index}")
    if audit.get("rows_dumped") != 449 or audit.get("stride") != 79:
        raise ValueError("t13d audit does not corroborate t22 dimensions")
    walker, class_trace = trace_t22(census_row)
    writer = class_trace["serializer_functions"][0]
    writer_events = writer["events"]
    reader_widths = [int(x) for x in reader["seq"][:19]]
    reader_objects = reader["obj_seq"][:19]
    if reader_widths != EXPECTED_T22_WIDTHS or sum(reader_widths) != 66:
        raise ValueError("type 22 reader's leading cursor window no longer closes at 66 B")
    if len(writer_events) != 18 or [int(e["width"]) for e in writer_events] != reader_widths[:18]:
        raise ValueError("t16 serializer events disagree with the first 18 type 22 reader slots")
    if [e.get("object_off") for e in writer_events] != reader_objects[:18] or reader_objects[18] is not None:
        raise ValueError("t16 serializer object sinks disagree with type 22 reader evidence")

    reader_mod = import_module("_t05_widths_t20", ROOT / "scripts" / "t05_reader_widths.py")
    scan = reader_mod.scan_reader(walker.md, walker.raw, int(reader["reader"], 16))
    scan_calls = scan["calls"][:19]
    if [int(c["width"]) for c in scan_calls] != reader_widths:
        raise ValueError("fresh reader scan disagrees with frozen t05 widths")
    club_fields = [x for x in schema["entities"]["club"]["fields"] if x.get("parent") == "Cstc"]
    club_by_code: dict[str, list[dict[str, Any]]] = {}
    for field in club_fields:
        club_by_code.setdefault(field["code"], []).append(field)
    entities_by_code: dict[str, set[str]] = {}
    for entity_name, entity in schema["entities"].items():
        for field in entity.get("fields", []):
            entities_by_code.setdefault(field["code"], set()).add(entity_name)
    steps: list[dict[str, Any]] = []
    cursor = 0
    candidate_name_count = 0
    ambiguous_count = 0
    for i, width in enumerate(reader_widths):
        event = writer_events[i] if i < len(writer_events) else None
        object_off = event.get("object_off") if event else None
        # Call details are from a fresh scan of the same slot-19 reader.
        call_info = scan_calls[i]
        code_instances = []
        if object_off is not None:
            for tag, instances in codes.items():
                for inst in instances:
                    try:
                        file_off = int(inst.get("file_off", "-1"), 16)
                    except (TypeError, ValueError):
                        continue
                    if (CODE_INSTANCE_REGION[0] <= file_off <= CODE_INSTANCE_REGION[1] and
                            inst.get("shape") in ("read", "ref_ptr") and
                            inst.get("object_off") == object_off and inst.get("size") == width and
                            tag in club_by_code):
                        code_instances.append({"code": tag, "shape": inst["shape"],
                                               "file_off": inst["file_off"],
                                               "access_va": inst.get("access_va"),
                                               "instruction": inst.get("instruction")})
        candidate_codes = sorted({x["code"] for x in code_instances})
        field_code = candidate_codes[0] if len(candidate_codes) == 1 else None
        schema_candidates = club_by_code.get(field_code, []) if field_code else []
        field = None
        field_name = None
        field_name_candidate = None
        grade = "unnamed"
        disposition = "no_unique_Cstc_code_match"
        if len(candidate_codes) == 1 and len(schema_candidates) == 1:
            field_name_candidate = schema_candidates[0].get("name")
            grade = "L3_object_code_candidate_unplaced"
            disposition = "unique_within_club_Cstc_but_branch_cursor_unreconciled"
            candidate_name_count += 1
        elif len(candidate_codes) == 1 and len(schema_candidates) > 1:
            grade = "L3_code_only"
            disposition = "repeated_schema_occurrence_and_unplaced_cursor"
            ambiguous_count += 1

        if event:
            event_inst_off = event.get("inst_off")
            event_call_off = event.get("call_off")
            event_inst_va = walker.pe.f2va(int(event_inst_off, 16)) if event_inst_off else None
            event_call_va = walker.pe.f2va(int(event_call_off, 16)) if event_call_off else None
            serializer_evidence = {
                "source": "t16_slot19_walk_in_memory",
                "function_file_off": writer["function_off"],
                "event_inst_file_off": event_inst_off,
                "event_inst_va": hex(event_inst_va) if event_inst_va else None,
                "call_file_off": event_call_off,
                "call_va": hex(event_call_va) if event_call_va else None,
                "instruction": event.get("instruction"),
                "object_off": object_off,
            }
        else:
            call_va = int(call_info["call_va"], 16)
            call_file_off = walker.pe.va2f(call_va)
            # The final 12-byte bulk transfer is present in the reader trace but
            # t16 cannot assign its RDX source to a record-member offset.
            reader_insns = list(walker.md.disasm(walker.raw[int(reader["reader"], 16):
                                                          int(reader["reader"], 16) + 0x2000],
                                                 walker.pe.f2va(int(reader["reader"], 16))))
            call_index = next((j for j, ins in enumerate(reader_insns) if ins.address == call_va), None)
            width_inst = None
            if call_index is not None:
                for ins in reversed(reader_insns[max(0, call_index - 8):call_index]):
                    if ins.mnemonic == "mov" and ins.op_str.replace(" ", "") == "r8d,0xc":
                        width_inst = ins
                        break
            serializer_evidence = {
                "source": "t05_reader_width_trace; t16 object sink unresolved",
                "reader_call_va": hex(call_va),
                "reader_call_file_off": hex(call_file_off) if call_file_off is not None else None,
                "width_inst_va": hex(width_inst.address) if width_inst else None,
                "width_inst_file_off": hex(walker.pe.va2f(width_inst.address)) if width_inst else None,
                "width_instruction": width_inst.mnemonic + " " + width_inst.op_str if width_inst else None,
                "object_off": None,
            }
            if not width_inst:
                raise ValueError("could not independently locate t22's 12-byte bulk transfer")

        steps.append({
            "slot": i,
            "row_offset": None,
            "row_offset_candidate": cursor,
            "width": width,
            "row_end_exclusive_candidate": cursor + width,
            "object_off": object_off,
            "field": field,
            "field_name": field_name,
            "field_name_candidate": field_name_candidate,
            "field_code_candidate": field_code,
            "candidate_codes": candidate_codes,
            "schema_candidates": [{"schema_index": f["idx"], "name": f.get("name"),
                                   "type": f.get("type"), "parent": f.get("parent")}
                                  for f in schema_candidates],
            "code_entity_df": len(entities_by_code.get(field_code, set())) if field_code else None,
            "grade": grade,
            "disposition": disposition,
            "evidence": {
                "serializer": serializer_evidence,
                "code_instances": code_instances,
                "reader_call_width": width,
                "reader_call_va": call_info.get("call_va"),
            },
            "data_profile": row_profile(rows, cursor, width),
        })
        cursor += width

    if cursor != 66:
        raise ValueError(f"t22 business-byte budget changed: {cursor} != 66")
    anchors = {}
    for code in sorted(E56_CODES):
        item = next((s for s in steps if s.get("field_code_candidate") == code), None)
        anchors[code] = {"linear_cursor_offset_candidate": item.get("row_offset_candidate") if item else None,
                         "row_offset_promoted": None,
                         "E56_status": "A-level club field identity; row cursor not reconciled"}
    live_c0 = [int.from_bytes(row[:4], "little") for row in rows if row[:4] != b"\xff\xff\xff\xff"]
    if not live_c0 or min(live_c0) != 86 or max(live_c0) != 82403:
        raise ValueError("t22 c0 club-domain side-check changed")
    sha = hashlib.sha256(EDITOR.read_bytes()).hexdigest()
    if codes_doc.get("exe_sha256") and sha != codes_doc["exe_sha256"]:
        raise ValueError("editor.exe SHA-256 differs from codes_full static evidence")
    cursor_doc = {
        "task": "t20",
        "entity": "club",
        "entity_tag": "club",
        "table_type": 22,
        "role": identity.get("role"),
        "status": "partial_cursor_t22_branch_paths_unreconciled",
        "row_coordinate_space": "server_db.dat table_22 row-relative bytes",
        "table_identity": {"grade": identity.get("level"), "source": identity.get("source"),
                           "anchors": identity.get("anchors"),
                           "runtime_class": census_row.get("primary_class"),
                           "class_note": "RTTI class STADIUM_CHANGE; does not override E56 parent-entity adjudication club"},
        "serializer_locator": {
            "factory_handler_file_off": census_row.get("handler_off"),
            "vtable_va": census_row.get("vtables", [{}])[0].get("vtable_va"),
            "class_type_descriptor": census_row.get("vtables", [{}])[0].get("class"),
            "census_rtti_depth": census_row.get("vtables", [{}])[0].get("depth"),
            "census_fm_cross": census_row.get("vtables", [{}])[0].get("fm_cross"),
            "t16_handler_vtable_assignment_found": class_trace.get("vtable_assignment_found"),
            "slot19_reader_va": hex(int(class_trace["reader_va"], 16)),
            "slot19_reader_file_off": hex(int(class_trace["reader_off"], 16)),
            "slot19_walk_function_file_off": writer.get("function_off"),
            "serializer_depth": writer.get("depth"),
            "slot19_events_with_member_sink": len(writer_events),
            "branch_count": writer.get("branch_count"),
            "exe": str(EDITOR),
            "exe_sha256": sha,
            "static_source": "editor.exe; factory census + slot19 + t16 direct-call serializer walk",
        },
        "cursor_method": {
            "width_trace": "scratch/t05/reader_widths.json type_id=22; fresh scan confirms calls 0..18",
            "static_walk_crosscheck": "t16 slot19 walk captures 18 member-sink events and the reader scan captures a 12B call; 23 branches and per-call barriers mean this is not a proven executed field order",
            "linear_candidate_width_sum": cursor,
            "static_reader_calls_scanned": reader.get("calls"),
            "event_count_including_bulk": len(reader_widths),
            "unresolved_bulk_sink": {"slot": 18, "width": 12, "row_offset_candidate": 54,
                                   "row_offset_promoted": None,
                                   "note": "width is statically observed; member/object origin and selected path remain unresolved"},
            "branch_path_closed": False,
        },
        "stride_closure": {
            "row_count": len(rows),
            "stride": 79,
            "business_width_candidate": cursor,
            "trailer_width": 13,
            "byte_budget_equation": "66 candidate business bytes + 13 trailer bytes = 79 stride",
            "payload_equation": "14 + 449*79 + 8 = 35493",
            "csv_rows_contiguous_from_offset": 14,
            "payload_boundary_source": "scratch/t13d/out/quick_audit.md + audit.json; closed fixed-stride export",
            "byte_budget_pass": cursor + 13 == 79 and len(rows) == 449,
            "field_cursor_closed": False,
            "closure_blocker": "linear reader window crosses branch barriers; row data at +12/+16/+50 independently looks date-packed and contradicts candidate Scap@+12, Styp@+16, Sceb@+50",
            "data_shape_date_offsets": audit.get("date_cols", []),
            "data_shape_conflicts": [
                {"candidate_row_offset": 12, "candidate_code": "Scap", "schema_name_candidate": "New Capacity",
                 "observed_shape": "u32 packed day/year; t13d audit year 2000..2030"},
                {"candidate_row_offset": 16, "candidate_code": "Styp", "schema_name_candidate": "Type",
                 "observed_shape": "u32 packed day/year; t13d audit year 2017..2030; one-byte slot would split the observed date"},
                {"candidate_row_offset": 17, "candidate_code": "Salt", "schema_name_candidate": "Alternative Stadium",
                 "observed_shape": "candidate begins inside packed date at +16; cannot promote"},
                {"candidate_row_offset": 50, "candidate_code": "Sceb", "schema_name_candidate": "Future Stadium Development Fund",
                 "observed_shape": "u32 packed day/year; t13d audit year 1900..2030"}
            ],
            "trailer_semantics": "unassigned framing; not promoted to business fields",
        },
        "crosschecks": {
            "E56_unique_club_fields": anchors,
            "c0_reference_range": {"non_null_rows": len(live_c0), "distinct": len(set(live_c0)),
                                    "min": min(live_c0), "max": max(live_c0),
                                    "source": "t13d audit + t22 CSV; domain is club-ID compatible, not by itself table-identity proof"},
            "t13d_audit_count_stride": {"rows_dumped": audit.get("rows_dumped"), "stride": audit.get("stride")},
        },
        "evidence_grade": "L3_static_width_candidates_plus_L1_stride_and_E56_A_identity; row_cursor_partial",
        "sources": ["scratch/t14/out/census.json", "scratch/t05/reader_widths.json",
                    "scratch/t12/out/codes_full.json", "scratch/t13d/out/t22.csv",
                    "scratch/t13d/out/audit.json", "reports/stage2_table_identity.json"],
        "steps": steps,
    }
    field_doc = {
        "entity": "club",
        "entity_tag": "club",
        "table_type": 22,
        "runtime_class": "STADIUM_CHANGE",
        "role": identity.get("role"),
        "offset_space": "server_db.dat table_22 row-relative bytes",
        "status": "partial_row_cursor_with_branch_ambiguity",
        "row_count": len(rows),
        "stride": 79,
        "business_width": 66,
        "trailer": {"row_offset": 66, "width": 13, "grade": "unnamed_framing"},
        "fields_named": 0,
        "candidate_names_unique_within_club_Cstc": candidate_name_count,
        "code_only_ambiguous": ambiguous_count,
        "unnamed_or_unmatched": len(steps) - candidate_name_count - ambiguous_count,
        "field_basis": "static object_off/4CC candidates + club.Cstc schema scope; no row coordinate promoted because selected branch path is unresolved",
        "scope_caveat": "Unique within club.Cstc is a candidate only; duplicated Snew/Sold and data-shape contradictions block promotion.",
        "fields": steps,
    }
    return cursor_doc, field_doc
def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selftest", action="store_true", help="run deterministic cursor arithmetic self-test")
    parser.add_argument("--outdir", default=str(OUT), help="artifact directory (default: scratch/t20/out)")
    args = parser.parse_args()
    if args.selftest:
        ok = selftest()
        print("t20_build selftest: " + ("PASS" if ok else "FAIL"))
        return 0 if ok else 1
    outdir = Path(args.outdir)
    if outdir.resolve() != OUT.resolve():
        print("refusing output outside scratch/t20/out", file=sys.stderr)
        return 2
    try:
        cursor_doc, field_doc = build()
        write_compact_records(outdir / "cursor_t22.json", cursor_doc, "steps")
        write_compact_records(outdir / "fields_t22.json", field_doc, "fields")
        print(f"wrote {outdir / 'cursor_t22.json'}")
        print(f"wrote {outdir / 'fields_t22.json'}")
        print(f"status={cursor_doc['status']} named={field_doc['fields_named']}/{len(field_doc['fields'])}")
        return 0
    except (OSError, ValueError, KeyError, RuntimeError, StopIteration, ImportError, TypeError) as exc:
        print(f"t20_build: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
