from __future__ import annotations

import argparse
import hashlib
import json
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "scratch/t25/out"
SCHEMA = ROOT / "evidence/fm24/reports/editor_schema/master.json"
MANIFEST = ROOT / "evidence/MANIFEST.json"
PREFIX_EVIDENCE = ROOT / "scratch/t01/inbox/t01g/output.json"
FRAMEWORK = ROOT / "scratch/t02/inbox/nati/OUTBOX/framework.json"
PAYLOAD = ROOT / "scratch/t02/inbox/nati/client_db_t10.bin"
CAPITAL_REPORT = ROOT / "reports/t22_nation_capital.json"
SCHEMA_SHA256 = "7d57477e144d5359ccde64bb24b3ba7c640ef41738ed196eba8a38e792776eda"
PAYLOAD_SHA256 = "7e9d740b9ee6900965d8616a136ea4bc54a0f7207f9727eac72badfb727f6c34"
EXPECTED_ROWS = 251
HEADER_SIZE = 14
FOOTER_SIZE = 8
SHARD_SIZE = 100


def load(path: Path):
    with path.open("r", encoding="utf-8") as stream:
        return json.load(stream)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_file(path: Path) -> str:
    return sha256(path.read_bytes())


def dump_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=True, indent=1) + "\n", encoding="utf-8")


def flatten_schema() -> list[dict]:
    entity = load(SCHEMA)["entities"]["nation.xml"][0]
    result = []
    for top_index, parent in enumerate(entity["fields"]):
        result.append({
            "schema_index": len(result), "top_level_index": top_index,
            "code": parent["field"], "name": parent.get("name"), "type": parent.get("type"),
            "parent": None, "is_client_field": parent.get("is_client_field"),
            "is_language_field": parent.get("is_language_field"),
            "schema_properties": {k: parent[k] for k in (
                "is_optional", "is_read_only", "database_table_type", "is_language_field"
            ) if k in parent},
        })
        for child_index, child in enumerate(parent.get("list_item_fields", [])):
            result.append({
                "schema_index": len(result), "top_level_index": top_index,
                "list_item_index": child_index, "code": child["field"],
                "name": child.get("name"), "type": child.get("type"),
                "parent": parent["field"], "is_client_field": child.get("is_client_field"),
                "is_language_field": child.get("is_language_field"),
                "schema_properties": {k: child[k] for k in (
                    "is_optional", "is_read_only", "database_table_type", "is_language_field"
                ) if k in child},
            })
    return result


def classify_schema(fields: list[dict]) -> dict:
    by_code = {f["code"]: f for f in fields if f["parent"] is None}
    direct, inherited, explicit_server, unknown = [], [], [], []
    for field in fields:
        flag = field.get("is_client_field")
        if flag == "true":
            field["schema_classification"] = "client_direct"
            field["classification_basis"] = "is_client_field=true"
            direct.append(field["code"])
        elif flag == "false":
            field["schema_classification"] = "server_only_explicit"
            field["classification_basis"] = "is_client_field=false"
            explicit_server.append(field["code"])
        elif field["parent"] and by_code[field["parent"]].get("is_client_field") == "true":
            field["schema_classification"] = "client_inherited_list_item"
            field["classification_basis"] = f"parent {field['parent']} has is_client_field=true"
            inherited.append(field["code"])
        else:
            field["schema_classification"] = "unknown_unmarked"
            field["classification_basis"] = "no is_client_field flag on field or client-marked parent"
            unknown.append(field["code"])
    return {
        "counts": {
            "active_schema_fields": len(fields), "client_direct": len(direct),
            "client_inherited_list_items": len(inherited),
            "client_scoped_total_including_list_items": len(direct) + len(inherited),
            "server_only_explicit": len(explicit_server), "unknown_unmarked": len(unknown),
        },
        "client_direct_codes": direct,
        "client_inherited_list_item_codes": inherited,
        "server_only_explicit_codes": explicit_server,
        "unknown_unmarked_codes": unknown,
        "language_marked_client_codes": [
            f["code"] for f in fields
            if f.get("is_language_field") == "true" and f["schema_classification"].startswith("client_")
        ],
        "classified_fields": {
            "client_direct": [f for f in fields if f["schema_classification"] == "client_direct"],
            "client_inherited_list_items": [
                f for f in fields if f["schema_classification"] == "client_inherited_list_item"
            ],
            "server_only_explicit": [
                f for f in fields if f["schema_classification"] == "server_only_explicit"
            ],
            "unknown_unmarked": [f for f in fields if f["schema_classification"] == "unknown_unmarked"],
        },
    }


def read_count(data: bytes, offset: int, width: int, label: str) -> int:
    if offset < 0 or offset + width > len(data):
        raise ValueError(f"{label}: count outside row body at {offset:#x}")
    value = struct.unpack_from("<b" if width == 1 else "<i", data, offset)[0]
    if value < 0:
        raise ValueError(f"{label}: negative signed collection count {value}")
    return value


def parse_client_payload(raw: bytes) -> dict:
    if len(raw) < HEADER_SIZE + FOOTER_SIZE or raw[:8] != bytes.fromhex("03 01 74 61 64 2e f1 0d"):
        raise ValueError("client nation payload header or size is invalid")
    if struct.unpack_from("<I", raw, 8)[0] != EXPECTED_ROWS or raw[12:14] != b"\0\0":
        raise ValueError("client nation payload row count/header differs")
    footer_start = len(raw) - FOOTER_SIZE
    body = raw[HEADER_SIZE:footer_start]
    rows = []
    pos = 0
    totals = [0, 0, 0, 0]
    maxima = [0, 0, 0, 0]
    for index in range(EXPECTED_ROWS):
        start = pos
        if start + 25 > len(body):
            raise ValueError(f"row {index}: truncated fixed prefix")
        counts = [read_count(body, start + 24, 1, f"row {index} A")]
        items = [start + 25]
        pos = start + 25 + counts[0] * 5
        count_offsets = [start + 24]
        for j, item_size in ((1, 28), (2, 28), (3, 12)):
            count_offsets.append(pos)
            count = read_count(body, pos, 4, f"row {index} {'BCD'[j-1]}")
            counts.append(count)
            items.append(pos + 4)
            pos += 4 + count * item_size
            if pos > len(body):
                raise ValueError(f"row {index}: collection {'BCD'[j-1]} exceeds payload")
        identity = pos
        if identity + 13 > len(body):
            raise ValueError(f"row {index}: identity/marker exceeds payload")
        ordinal, row_id, repeat_id = struct.unpack_from("<III", body, identity)
        marker = body[identity + 12]
        if (ordinal, repeat_id, marker) != (index, row_id, 0):
            raise ValueError(f"row {index}: identity or marker mismatch")
        span = identity + 13 - start
        if span != 50 + 5 * counts[0] + 28 * counts[1] + 28 * counts[2] + 12 * counts[3]:
            raise ValueError(f"row {index}: span formula mismatch")
        totals = [a + b for a, b in zip(totals, counts)]
        maxima = [max(a, b) for a, b in zip(maxima, counts)]
        rows.append({
            "row_index": index, "row_start_body": start,
            "row_start_payload": HEADER_SIZE + start, "row_span": span,
            "row_end_body_exclusive": start + span,
            "counts": {k: counts[n] for n, k in enumerate("ABCD")},
            "count_offsets_body": {k: count_offsets[n] for n, k in enumerate("ABCD")},
            "count_offsets_payload": {k: HEADER_SIZE + count_offsets[n] for n, k in enumerate("ABCD")},
            "items_start_body": {k: items[n] for n, k in enumerate("ABCD")},
            "item_wire_bytes": {"A": 5, "B": 28, "C": 28, "D": 12},
            "identity_body": identity, "identity_payload": HEADER_SIZE + identity,
            "ordinal": ordinal, "row_id": row_id, "repeated_id": repeat_id,
            "marker_payload": HEADER_SIZE + identity + 12,
        })
        pos = start + span
    if pos != len(body) or HEADER_SIZE + pos + FOOTER_SIZE != len(raw):
        raise ValueError("251-row parse did not close exactly at the footer")
    if totals != [492, 214, 63, 162] or maxima != [7, 40, 21, 2]:
        raise ValueError(f"client collection summary changed: totals={totals}, maxima={maxima}")
    if raw[0x1046:0x104e] != bytes.fromhex("6e 00 00 00 6e 00 00 00"):
        raise ValueError("row 55 duni anchor bytes changed")
    if rows[55]["identity_payload"] != 0x1042 or rows[55]["row_id"] != 110:
        raise ValueError("row 55 identity/duni anchor changed")
    return {
        "rows": rows, "body_bytes": len(body), "footer_start_payload": footer_start,
        "footer_hex": raw[footer_start:].hex(" "), "count_totals": totals,
        "count_maxima": maxima, "sum_row_spans": pos,
    }


def reader_evidence() -> dict:
    prefix = load(PREFIX_EVIDENCE)
    frame = load(FRAMEWORK)
    static = frame["reader_static_evidence"]
    ordinary = prefix["row_codec"]["ordinary_path_counted_collections"]
    return {
        "exe_sha256": frame["sources"]["reader_binary"]["sha256"],
        "reader_entry_file_offset": frame["sources"]["reader_binary"]["reader_file_offset"],
        "reader_entry_va": frame["sources"]["reader_binary"]["reader_va"],
        "coordinate_source": "t02-g2 independently verified client row frame; coordinates recomputed from payload bytes",
        "prefix_reader_transfers": prefix["row_codec"]["cursor_layout"],
        "counted_path": {
            "A": {k: ordinary[k] for k in ("count_source", "helper_call", "count_test", "per_item_helper", "loop_back_edge")},
            "B": {"count_width": static["count_B_read_width"], "stream_call": static["count_B_stream_call"], "item_helper": static["item_B_call"]},
            "C": {"count_width": static["count_C_read_width"], "stream_call": static["count_C_stream_call"], "item_helper": static["item_C_call"]},
            "D": {"count_width": static["count_D_read_width"], "stream_call": static["count_D_stream_call"], "item_helper": static["item_D_call"]},
        },
        "coordinate_binding_status": "data_frame_complete; reader call 24-39 to row-tail fields and list-item schema fields are not reconciled",
        "arg8_nonzero_path": "excluded; its u16-count/4-byte-item reader is not assigned to client or server",
    }


def build_outputs(out: Path = OUT) -> dict:
    schema_bytes = SCHEMA.read_bytes()
    if sha256(schema_bytes) != SCHEMA_SHA256:
        raise ValueError("frozen schema hash differs from evidence baseline")
    manifest = load(MANIFEST)
    manifest_entry = next((f for f in manifest["files"] if f["path"] == "evidence/fm24/reports/editor_schema/master.json"), None)
    if not manifest_entry or manifest_entry["sha256"] != SCHEMA_SHA256:
        raise ValueError("schema is not backed by the expected evidence/MANIFEST.json entry")
    raw = PAYLOAD.read_bytes()
    if len(raw) != 24732 or sha256(raw) != PAYLOAD_SHA256:
        raise ValueError("client nation payload size/hash differs from t02-g2 baseline")
    parsed = parse_client_payload(raw)
    prefix = load(PREFIX_EVIDENCE)
    prefix_hash = sha_file(PREFIX_EVIDENCE)
    capital = load(CAPITAL_REPORT)
    fields = flatten_schema()
    classes = classify_schema(fields)
    mappings = prefix["row_offset_map"]
    if len(fields) != 441 or set(mappings) != {"Ngct", "Ncti", "Nrgi", "Ncur", "Nsod", "Necf", "Nygn"}:
        raise ValueError("schema count or inherited prefix field set differs from baseline")

    values = {}
    for code, rec in mappings.items():
        offset, width = rec["row_offset"], rec["width"]
        if offset + width > 25:
            raise ValueError(f"mapped prefix field {code} is not inside the fixed prefix")
        fmt = "<b" if width == 1 else "<I"
        column = [struct.unpack_from(fmt, raw, row["row_start_payload"] + offset)[0] for row in parsed["rows"]]
        values[code] = {
            "row_offset": offset, "width": width, "object_offset": rec["object_offset"],
            "rows_checked": len(column), "unique_values": len(set(column)),
            "minimum": min(column), "maximum": max(column),
            "null_0xffffffff_count": sum(v == 0xffffffff for v in column),
            "sample_first_12": column[:12],
            "all_rows_decoded": True,
        }
    framework = load(FRAMEWORK)
    mapping_meta = {
        "source": "scratch/t01/inbox/t01g/output.json#row_offset_map",
        "source_sha256": prefix_hash,
        "level": "L3 reader destination+width and getter 4CC/member chain; row coordinates are cross-checked against all 251 client rows",
        "exe_sha256": framework["sources"]["reader_binary"]["sha256"],
        "fields": {code: {"row_offset": r["row_offset"], "width": r["width"],
                           "object_offset": r["object_offset"], "reader": r["serializer"],
                           "getter": r["field_getter_link"], "client_data_check": values[code]}
                   for code, r in mappings.items()},
    }
    schema_split = {
        "status": "complete_schema_flag_classification",
        "scope": "frozen active nation.xml#nati records only; nested list items are retained and parent client flags are inherited only for classification",
        "schema_source": "evidence/fm24/reports/editor_schema/master.json#entities.nation.xml[0]",
        "schema_sha256": sha256(schema_bytes), "manifest_snapshot_date": manifest["snapshot_date"],
        **classes,
        "mapped_unmarked_reader_candidates": [
            {"code": code, "schema_classification": "unknown_unmarked",
             "row_offset": mappings[code]["row_offset"], "width": mappings[code]["width"],
             "evidence": "t01g L3 reader destination/width + matching getter member; checked across all 251 decoded client rows",
             "promotion": "candidate_only; not counted in schema-confirmed client coverage"}
            for code in ("Ngct", "Nrgi", "Nsod", "Necf", "Nygn")
        ],
        "commented_out_records": [{
            "code": "Ncpi", "classification": "separate_commented_record_not_in_active_441",
            "schema_evidence": "reports/t22_nation_capital.json#schema",
            "schema_report_sha256": sha_file(CAPITAL_REPORT),
            "schema_properties": capital["schema"]["properties"],
            "mapping_status": "L3; not counted in active 441-field denominator",
        }],
        "limits": [
            "unknown_unmarked is not equivalent to server-only",
            "client classification does not establish that a scalar field occupies table_10 row bytes",
            "commented-out Ncpi does not establish active UI editability",
        ],
    }
    cursor = {
        "status": "complete_client_payload_coordinates_reader_tail_binding_open",
        "scope": "client table_10 rows only; no formula extrapolation to server payload",
        "source_payload": {"path": "scratch/t02/inbox/nati/client_db_t10.bin", "bytes": len(raw), "sha256": sha256(raw)},
        "source_frame": "scratch/t02/inbox/nati/OUTBOX/framework.json#row_frame",
        "row_count": len(parsed["rows"]), "header_bytes": HEADER_SIZE,
        "footer": {"start_payload": parsed["footer_start_payload"], "bytes": FOOTER_SIZE, "hex": parsed["footer_hex"]},
        "row_grammar": {
            "prefix_bytes": 25,
            "A": {"count": "signed i8 at row+24", "items_start": "row+25", "item_bytes": 5},
            "B": {"count": "signed i32le after A items", "item_bytes": 28},
            "C": {"count": "signed i32le after B items", "item_bytes": 28},
            "D": {"count": "signed i32le after C items", "item_bytes": 12},
            "identity": "ordinal u32le | row ID u32le | repeated row ID u32le | zero marker byte",
            "span": "50 + 5*A + 28*B + 28*C + 12*D",
        },
        "collection_totals": {k: parsed["count_totals"][i] for i, k in enumerate("ABCD")},
        "collection_maxima": {k: parsed["count_maxima"][i] for i, k in enumerate("ABCD")},
        "sum_row_spans": parsed["sum_row_spans"],
        "closure_equation": f"14 + {parsed['sum_row_spans']} + 8 = {len(raw)}",
        "reader_evidence": reader_evidence(), "rows": parsed["rows"],
    }
    all_records = []
    for field in fields:
        record = dict(field)
        code = field["code"]
        if code in mappings:
            record["mapping"] = {
                "status": "mapped_prefix_L3_and_251_row_data_checked",
                "row_offset": mappings[code]["row_offset"], "width": mappings[code]["width"],
                "object_offset": mappings[code]["object_offset"],
                "value_check": values[code],
            }
        else:
            record["mapping"] = {"status": "unresolved_no_promoted_table_10_coordinate"}
        if code in classes["language_marked_client_codes"]:
            record["language_role_note"] = "schema marks this client field is_language_field=true; table_9/text reference hypothesis is not proven here"
        all_records.append(record)
    shard_meta = []
    for shard_index, offset in enumerate(range(0, len(all_records), SHARD_SIZE)):
        name = f"fields_nation_{shard_index:03d}.json"
        chunk = all_records[offset:offset + SHARD_SIZE]
        shard = {"status": "partial_shard", "shard_index": shard_index,
                 "schema_index_start": offset, "schema_index_end_exclusive": offset + len(chunk),
                 "fields": chunk}
        dump_json(out / name, shard)
        shard_meta.append({"path": name, "count": len(chunk), "sha256": sha_file(out / name),
                           "schema_index_start": offset, "schema_index_end_exclusive": offset + len(chunk)})
    supplement = {
        "status": "separate_commented_record_not_in_active_schema_441",
        "fields": [{
            "code": "Ncpi", "name": "Capital City", "type": "database_record_unique_id",
            "parent": None, "schema_classification": "commented_out_client_schema_record",
            "schema_properties": capital["schema"]["properties"],
            "mapping": {"status": "mapped_L3_data_validated_by_t22", "row_offset": 9,
                        "width": 4, "object_offset": "0xe8", "target": "client_db/table_2.dat row ordinal",
                        "null_u32": 0xffffffff},
            "data_side_check": {
                "nation_rows": capital["data"]["nation_rows"],
                "nulls": capital["data"]["nulls"],
                "ordinal_hits": capital["data"]["ordinal_hits"],
                "same_nation_row_hits": capital["data"]["same_nation_row_hits"],
                "cross_nation_records": capital["cross_nation"],
                "holdout_rows": capital["holdouts"],
            },
            "evidence": "reports/t22_nation_capital.json",
            "limits": capital["limits"],
        }],
    }
    dump_json(out / "fields_nation_supplemental.json", supplement)
    field_index = {
        "status": "partial_client_field_mapping_prefix_only",
        "schema_source": "evidence/fm24/reports/editor_schema/master.json#entities.nation.xml[0]",
        "schema_sha256": sha256(schema_bytes), "schema_field_count": len(all_records),
        "mapping_summary": {
            "active_schema_fields_mapped": len(mappings), "mapped_direct_client_marked": 2,
            "schema_confirmed_client_scope_including_nested_items": classes["counts"]["client_scoped_total_including_list_items"],
            "schema_confirmed_client_fields_mapped": 2,
            "schema_confirmed_client_mapping_rate": "2/49 (4.1%)",
            "mapped_but_schema_flag_unknown": 5,
            "unmapped_active_schema_fields": len(all_records) - len(mappings),
            "commented_out_supplemental_fields": 1,
        },
        "mapping_evidence": mapping_meta, "shards": shard_meta,
        "supplemental_path": "fields_nation_supplemental.json",
        "unresolved_scope": "schema flags are classification only; no row coordinates inferred for the other fields",
    }
    dump_json(out / "schema_split.json", schema_split)
    dump_json(out / "cursor_nation.json", cursor)
    dump_json(out / "fields_nation.json", field_index)
    write_report(out / "REPORT.md", schema_split, field_index, cursor)
    write_verifier_launcher(out / "verify.py")
    return {"schema_split": schema_split, "field_index": field_index, "cursor": cursor}


def write_report(path: Path, split: dict, index: dict, cursor: dict) -> None:
    counts = split["counts"]
    mappings = index["mapping_summary"]
    lines = [
        "# t25 Nation Client Field Expansion", "",
        "## Status", "",
        "Client table_10 cursor coordinates are complete for the verified 251-row payload. Static reader-tail binding and schema field coverage remain partial. The cursor is data-side only; it does not assign the arg8!=0 path or claim a server format.", "",
        "## Schema Classification", "",
        f"- Active schema fields: {counts['active_schema_fields']}",
        f"- Direct client-marked: {counts['client_direct']}",
        f"- Nested list items inheriting a client-marked parent: {counts['client_inherited_list_items']}",
        f"- Client-scoped total including inherited list items: {counts['client_scoped_total_including_list_items']}",
        f"- Explicit server-only: {counts['server_only_explicit']}",
        f"- Unmarked/unknown: {counts['unknown_unmarked']}",
        "- The 6 language-marked client fields are listed in `schema_split.json`; table_9/text-reference semantics remain a hypothesis.",
        "- `Ncpi` is separately recorded as a commented-out schema field from t22, not part of the active 441.", "",
        "## Cursor", "",
        f"- Rows: {cursor['row_count']}; row spans: {cursor['sum_row_spans']} bytes.",
        f"- Closure: `{cursor['closure_equation']}`; footer: `{cursor['footer']['hex']}`.",
        "- Per-row body/payload offsets, A/B/C/D count locations, item starts, identity and marker offsets are in `cursor_nation.json`.",
        "- Existing frame verifier's row 55 identity/duni anchor is rechecked; count totals are A/B/C/D = 492/214/63/162.", "",
        "## Field Mapping", "",
        f"- Active schema fields mapped: {mappings['active_schema_fields_mapped']}/441 (2 directly client-marked; 5 have no client flag).",
        f"- Schema-confirmed client-scope mapping rate: {mappings['schema_confirmed_client_mapping_rate']} (two mapped fields out of 49 client-marked top-level/list-item fields).",
        "- The seven prefix mappings retain t01g's L3 reader/getter chains. Their row coordinates were decoded across all 251 client rows; per-field ranges and samples are in the shards.",
        "- No other field received a row coordinate. Schema membership, client flags and list ownership alone are not treated as byte-offset evidence.",
        "- Field ledger: `fields_nation.json` index plus five hash-checked shards; `Ncpi` is in `fields_nation_supplemental.json`.", "",
        "## Open Items", "",
        "- Reconcile reader calls 24-39 and all counted-loop bodies to row-frame coordinates; the cursor artifact currently gives complete client data coordinates, not a complete static call-to-wire trace.",
        "- Map collection payload members to nested schema list-item fields; none are inferred from parent names.",
        "- Investigate the 392 unmarked fields without classifying them as server-only.",
        "- Verify all unmarked candidates against additional independent anchors before promotion; retain server table_10, arg8!=0, and XML-comment editability boundaries.", "",
        "## Verification", "",
        "```text",
        "py -V:3.12 -I -B scripts/t25_nation_fields.py --selftest",
        "py -V:3.12 -I -B scripts/t25_verify.py",
        "py -V:3.12 -I -B scripts/t01_anchors.py",
        "```", "",
        "Source schema SHA-256: `" + split["schema_sha256"] + "` (matched against `evidence/MANIFEST.json`).",
        "Client payload SHA-256: `" + cursor["source_payload"]["sha256"] + "`.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_verifier_launcher(path: Path) -> None:
    source = '''from pathlib import Path\nimport sys\n\nROOT = Path(__file__).resolve().parents[3]\nsys.path.insert(0, str(ROOT))\nfrom scripts.t25_verify import main\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'''
    path.write_text(source, encoding="ascii")


def selftest() -> int:
    try:
        fields = flatten_schema()
        result = classify_schema(fields)
        assert len(fields) == 441
        assert result["counts"] == {
            "active_schema_fields": 441, "client_direct": 21,
            "client_inherited_list_items": 28, "client_scoped_total_including_list_items": 49,
            "server_only_explicit": 0, "unknown_unmarked": 392,
        }
        parsed = parse_client_payload(PAYLOAD.read_bytes())
        assert len(parsed["rows"]) == 251 and parsed["sum_row_spans"] == 24710
        assert parsed["rows"][143]["row_span"] == 1199
    except Exception as error:
        print(f"FAIL: {type(error).__name__}: {error}")
        return 1
    print("PASS: schema 441 (21 direct client, 28 inherited list items, 392 unknown); client cursor 251 rows")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Build t25 nation client schema, cursor and field artifacts")
    parser.add_argument("--out", default=str(OUT), help="output directory (restricted by task to scratch/t25/out)")
    parser.add_argument("--selftest", action="store_true", help="run input and classification self-checks without writing")
    args = parser.parse_args()
    if args.selftest:
        return selftest()
    out = Path(args.out).resolve()
    allowed = (ROOT / "scratch/t25/out").resolve()
    if out != allowed:
        print(f"fatal: output must be {allowed}", file=sys.stderr)
        return 2
    try:
        result = build_outputs(out)
    except (OSError, ValueError, KeyError, AssertionError) as error:
        print(f"fatal: {type(error).__name__}: {error}", file=sys.stderr)
        return 2
    counts = result["schema_split"]["counts"]
    print(f"wrote {out}: rows={len(result['cursor']['rows'])}, schema_fields={counts['active_schema_fields']}, mapped={result['field_index']['mapping_summary']['active_schema_fields_mapped']}")
    print(f"classification direct_client={counts['client_direct']} inherited_list={counts['client_inherited_list_items']} explicit_server={counts['server_only_explicit']} unknown={counts['unknown_unmarked']}")
    print("deliverables: schema_split.json cursor_nation.json fields_nation.json + 5 shards + supplemental + verify.py REPORT.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
