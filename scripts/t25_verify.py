from __future__ import annotations

import argparse
import hashlib
import json
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "scratch/t25/out"
PAYLOAD = ROOT / "scratch/t02/inbox/nati/client_db_t10.bin"
SCHEMA = ROOT / "evidence/fm24/reports/editor_schema/master.json"
MANIFEST = ROOT / "evidence/MANIFEST.json"
PREFIX_EVIDENCE = ROOT / "scratch/t01/inbox/t01g/output.json"
PAYLOAD_SHA256 = "7e9d740b9ee6900965d8616a136ea4bc54a0f7207f9727eac72badfb727f6c34"
SCHEMA_SHA256 = "7d57477e144d5359ccde64bb24b3ba7c640ef41738ed196eba8a38e792776eda"
HEADER = 14
FOOTER = 8
EXPECTED_COUNT = 251
EXPECTED_CODES = {"Ngct", "Ncti", "Nrgi", "Ncur", "Nsod", "Necf", "Nygn"}


def load(path: Path):
    with path.open("r", encoding="utf-8") as stream:
        return json.load(stream)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def signed_count(raw: bytes, offset: int, width: int) -> int:
    if offset < 0 or offset + width > len(raw):
        raise ValueError(f"count outside payload at {offset:#x}")
    count = struct.unpack_from("<b" if width == 1 else "<i", raw, offset)[0]
    if count < 0:
        raise ValueError(f"negative count {count} at {offset:#x}")
    return count


def parse_rows(raw: bytes) -> dict:
    if len(raw) != 24732 or raw[:8] != bytes.fromhex("03 01 74 61 64 2e f1 0d"):
        raise ValueError("payload size/header mismatch")
    if struct.unpack_from("<I", raw, 8)[0] != EXPECTED_COUNT or raw[12:14] != b"\0\0":
        raise ValueError("payload row count/header trailer mismatch")
    body_end = len(raw) - FOOTER
    body = raw[HEADER:body_end]
    cursor = 0
    rows = []
    totals = [0, 0, 0, 0]
    for index in range(EXPECTED_COUNT):
        start = cursor
        if start + 25 > len(body):
            raise ValueError(f"row {index} fixed prefix truncated")
        a = signed_count(body, start + 24, 1)
        counts = [a]
        count_body = [start + 24]
        item_body = [start + 25]
        cursor = start + 25 + 5 * a
        for item_size in (28, 28, 12):
            count_body.append(cursor)
            count = signed_count(body, cursor, 4)
            counts.append(count)
            item_body.append(cursor + 4)
            cursor += 4 + count * item_size
            if cursor > len(body):
                raise ValueError(f"row {index} collection overruns body")
        identity = cursor
        if identity + 13 > len(body):
            raise ValueError(f"row {index} identity truncated")
        ordinal, rid, repeated = struct.unpack_from("<III", body, identity)
        marker = body[identity + 12]
        if ordinal != index or rid != repeated or marker != 0:
            raise ValueError(f"row {index} identity/marker mismatch")
        span = identity + 13 - start
        if span != 50 + 5 * counts[0] + 28 * counts[1] + 28 * counts[2] + 12 * counts[3]:
            raise ValueError(f"row {index} span formula mismatch")
        rows.append({
            "row_index": index, "row_start_body": start,
            "row_start_payload": HEADER + start, "row_span": span,
            "row_end_body_exclusive": start + span,
            "counts": {k: counts[n] for n, k in enumerate("ABCD")},
            "count_offsets_body": {k: count_body[n] for n, k in enumerate("ABCD")},
            "count_offsets_payload": {k: HEADER + count_body[n] for n, k in enumerate("ABCD")},
            "items_start_body": {k: item_body[n] for n, k in enumerate("ABCD")},
            "item_wire_bytes": {"A": 5, "B": 28, "C": 28, "D": 12},
            "identity_body": identity, "identity_payload": HEADER + identity,
            "ordinal": ordinal, "row_id": rid, "repeated_id": repeated,
            "marker_payload": HEADER + identity + 12,
        })
        totals = [x + y for x, y in zip(totals, counts)]
        cursor = start + span
    if cursor != len(body) or totals != [492, 214, 63, 162]:
        raise ValueError(f"row closure/count totals mismatch: cursor={cursor}, totals={totals}")
    if raw[0x1046:0x104e] != bytes.fromhex("6e 00 00 00 6e 00 00 00"):
        raise ValueError("duni anchor mismatch")
    return {"rows": rows, "body_bytes": len(body), "footer_start": body_end,
            "footer_hex": raw[body_end:].hex(" "), "totals": totals, "span_sum": cursor}


def schema_inventory() -> tuple[list[dict], dict]:
    master = load(SCHEMA)
    source = master["entities"]["nation.xml"][0]["fields"]
    flat = []
    direct, inherited, server, unknown, language = [], [], [], [], []
    parents = {}
    for top_index, field in enumerate(source):
        parent_code = field["field"]
        parents[parent_code] = field
        flat.append((field, None, top_index, None))
        flat.extend((child, parent_code, top_index, child_index)
                    for child_index, child in enumerate(field.get("list_item_fields", [])))
    for field, parent, _, _ in flat:
        flag = field.get("is_client_field")
        if flag == "true":
            direct.append(field["field"])
        elif flag == "false":
            server.append(field["field"])
        elif parent and parents[parent].get("is_client_field") == "true":
            inherited.append(field["field"])
        else:
            unknown.append(field["field"])
        if field.get("is_language_field") == "true" and (
            flag == "true" or (parent and parents[parent].get("is_client_field") == "true")
        ):
            language.append(field["field"])
    return flat, {"direct": direct, "inherited": inherited, "server": server,
                  "unknown": unknown, "language": language}


def verify() -> tuple[int, list[str]]:
    errors = []
    def check(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    raw = PAYLOAD.read_bytes()
    payload_hash = digest(raw)
    check(payload_hash == PAYLOAD_SHA256, "client payload SHA-256 differs from baseline")
    parsed = parse_rows(raw)
    split = load(OUT / "schema_split.json")
    cursor = load(OUT / "cursor_nation.json")
    field_index = load(OUT / "fields_nation.json")
    check(digest(SCHEMA.read_bytes()) == SCHEMA_SHA256, "frozen schema SHA-256 differs from baseline")
    manifest = load(MANIFEST)
    entry = next((item for item in manifest["files"] if item["path"] == "evidence/fm24/reports/editor_schema/master.json"), None)
    check(entry is not None and entry.get("sha256") == SCHEMA_SHA256, "schema MANIFEST entry missing/mismatched")
    flat, groups = schema_inventory()
    check(len(flat) == 441, f"flattened schema field count={len(flat)}, expected 441")
    counts = split.get("counts", {})
    check(counts.get("active_schema_fields") == 441, "schema_split active field count mismatch")
    check(split.get("client_direct_codes") == groups["direct"], "direct client field classification/order mismatch")
    check(split.get("client_inherited_list_item_codes") == groups["inherited"], "inherited list item classification/order mismatch")
    check(split.get("server_only_explicit_codes") == groups["server"], "explicit server classification/order mismatch")
    check(split.get("unknown_unmarked_codes") == groups["unknown"], "unknown classification/order mismatch")
    check(split.get("language_marked_client_codes") == groups["language"], "language-marked field list mismatch")
    check(counts.get("client_direct") == 21 and counts.get("client_inherited_list_items") == 28
          and counts.get("server_only_explicit") == 0 and counts.get("unknown_unmarked") == 392,
          "schema classification totals mismatch")
    check({item.get("code") for item in split.get("mapped_unmarked_reader_candidates", [])}
          == {"Ngct", "Nrgi", "Nsod", "Necf", "Nygn"},
          "unmarked reader candidate list mismatch")

    check(cursor.get("source_payload", {}).get("sha256") == payload_hash, "cursor source payload hash mismatch")
    check(cursor.get("row_count") == EXPECTED_COUNT, "cursor row count mismatch")
    check(cursor.get("rows") == parsed["rows"], "cursor coordinates differ from independent payload parse")
    check(cursor.get("sum_row_spans") == parsed["span_sum"] == 24710, "cursor span sum mismatch")
    check(cursor.get("closure_equation") == "14 + 24710 + 8 = 24732", "cursor closure equation mismatch")
    check(cursor.get("footer", {}).get("start_payload") == parsed["footer_start"], "cursor footer start mismatch")
    check(cursor.get("footer", {}).get("hex") == parsed["footer_hex"], "cursor footer bytes mismatch")
    check(cursor.get("collection_totals") == dict(zip("ABCD", parsed["totals"])), "cursor collection totals mismatch")

    shard_fields = []
    for shard in field_index.get("shards", []):
        path = OUT / shard["path"]
        check(path.is_file(), f"missing field shard {path.name}")
        if not path.is_file():
            continue
        check(digest(path.read_bytes()) == shard.get("sha256"), f"field shard hash mismatch: {path.name}")
        contents = load(path)
        shard_fields.extend(contents.get("fields", []))
    check(len(shard_fields) == 441, f"field shard count={len(shard_fields)}, expected 441")
    check([field.get("schema_index") for field in shard_fields] == list(range(441)), "field shard indices do not cover 0..440")
    check([field.get("code") for field in shard_fields] == [item[0]["field"] for item in flat], "field shard schema ordering/content mismatch")
    mappings = [field for field in shard_fields if field.get("mapping", {}).get("status") == "mapped_prefix_L3_and_251_row_data_checked"]
    check({field["code"] for field in mappings} == EXPECTED_CODES and len(mappings) == 7, "mapped field set differs from t01g prefix baseline")
    prefix = load(PREFIX_EVIDENCE)
    check(digest(PREFIX_EVIDENCE.read_bytes()) == field_index.get("mapping_evidence", {}).get("source_sha256"), "t01g source hash mismatch")
    for field in mappings:
        code = field["code"]
        proof = prefix["row_offset_map"][code]
        mapping = field["mapping"]
        check(mapping.get("row_offset") == proof["row_offset"] and mapping.get("width") == proof["width"], f"{code}: mapped offset/width mismatch")
        stat = mapping.get("value_check", {})
        check(stat.get("rows_checked") == EXPECTED_COUNT and stat.get("all_rows_decoded") is True, f"{code}: no full-row value scan")
        fmt = "<b" if proof["width"] == 1 else "<I"
        values = [struct.unpack_from(fmt, raw, row["row_start_payload"] + proof["row_offset"])[0] for row in parsed["rows"]]
        check(stat.get("unique_values") == len(set(values)) and stat.get("minimum") == min(values)
              and stat.get("maximum") == max(values), f"{code}: field value summary mismatch")
    supplemental = load(OUT / field_index.get("supplemental_path", "fields_nation_supplemental.json"))
    supplemental_field = supplemental.get("fields", [{}])[0]
    check(supplemental_field.get("code") == "Ncpi", "Ncpi supplemental record missing")
    check(supplemental_field.get("mapping", {}).get("row_offset") == 9, "Ncpi t22 offset mismatch")
    ncpi_data = supplemental_field.get("data_side_check", {})
    check(ncpi_data.get("nation_rows") == 251 and ncpi_data.get("nulls") == 20
          and ncpi_data.get("ordinal_hits") == 231 and ncpi_data.get("same_nation_row_hits") == 226,
          "Ncpi t22 data-side summary mismatch")
    check(len(ncpi_data.get("cross_nation_records", [])) == 5
          and len(ncpi_data.get("holdout_rows", [])) == 6,
          "Ncpi cross-nation/holdout record count mismatch")
    check((OUT / "REPORT.md").is_file(), "REPORT.md missing")
    check((OUT / "verify.py").is_file(), "generated verify.py missing")
    return (1 if errors else 0), errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Independently verify t25 schema, cursor and mapping artifacts")
    parser.add_argument("--selftest", action="store_true", help="run the full read-only artifact verification")
    args = parser.parse_args()
    try:
        code, errors = verify()
    except (OSError, ValueError, KeyError, TypeError, struct.error) as error:
        print(f"FATAL: {type(error).__name__}: {error}", file=sys.stderr)
        return 2
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        print(f"{len(errors)} verification failure(s)")
        return code
    print("PASS: schema classification 441 fields; 251 client row coordinates close; 7 prefix mappings checked across all rows; Ncpi supplemental evidence present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
