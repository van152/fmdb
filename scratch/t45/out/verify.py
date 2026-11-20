#!/usr/bin/env python3
"""Independent verifier for the t45 schema v3 consolidation."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
OUT_JSON = ROOT / "reports" / "club_nation_subtable_schema.json"
OUT_MD = ROOT / "reports" / "club_nation_subtable_schema.md"
OUT_DIR = Path(__file__).resolve().parent
V2_JSON = OUT_DIR / "club_nation_subtable_schema.v2.json"
V2_MD = OUT_DIR / "club_nation_subtable_schema.v2.md"
V2_JSON_SHA256 = "a08b013a060724bef6e0c8ea1e0c4b16e57a7438a8fa53d7ed519c6f77611ab7"
V2_MD_SHA256 = "da02f1062172d0ca9ae5f44ee3061cb06962a2255c95af0b76617156bf700dbd"
FIELDS_PATH = "scratch/t41/out/fields_csme.json"
CURSOR_PATH = "scratch/t41/out/cursor_csme.json"
T41_REPORT_PATH = "scratch/t41/out/REPORT.md"
LEDGER_PATH = "scratch/t45/out/LEDGER.E82.json"
EXPECTED_SOURCE_HASHES = {
    "scratch/t24/out/subtables.part001.json": "6ba93636161d924ebf2648cb4be254d864b773bc30b28bd9c4fdf3349a44b829",
    "scratch/t33/out/profiles/table_server_59.profile.json": "3c4ee8efdb057ad21b020d67a6d08c174ffe42309bb2d3fc28e0fea11922ecf9",
    "scratch/t33/out/profiles/table_server_59.rows.jsonl": "b06e7e468f6d9e1c3cb8b8b36533b667ae87a74b2338fe8c24e91f7a34abcc49",
    "scratch/t33/out/REPORT.md": "07572015f6f2455bd0787e7d0303ef3782eee386e40829e2b723963ada23e7e5",
    FIELDS_PATH: "f08c5ca7d0b51779f4708ae77c3a4bc15b37e5d6633879ca1ca78654d5ba1a50",
    CURSOR_PATH: "967cca2843388b00bb2335e5d67de7cb6a6074fbe3fe444851b5808770cc8306",
    T41_REPORT_PATH: "2013d798716f4f740e0009d4b051e86caac256f4105fe444cbffdcfb579ba3bf",
    "scratch/t41/out/instructions.part001.json": "6dc495f393dd8d4c3370fb171b6a2544f49640faed8d0d1c52a84e9091de6a59",
    "scratch/t41/out/instructions.part002.json": "81bc5d477c11cf1ec7400376dbf1ede5dc1b74d465498794bbb31d8e6513f47f",
    "scratch/t41/out/instructions.part003.json": "bd5e97b77380f1a8778a31a68bdcada4f6e011aa27a4df5bd48ae9f2797d5aa0",
    "scratch/t41/out/instructions.part004.json": "3e9e903d0bfaa3453230192f027e3b63578ebc3db0142f8d39a6aae0e62cc4ed",
    "scratch/t41/out/instructions.part005.json": "cbe84c936ef617f71bc310d8dc626576bdbd6818fbf6fb1d40962b51acc1a89a",
    "scratch/t41/out/instructions.part006.json": "92b1cf51326fc1e7d5cf5f9f53e89f3e06f35f9c0ab358eddf50db4a384b689e",
    "scratch/t41/out/instructions.part007.json": "9ecb7facebd594dacd70932f0e9641b9f6259d10fd5454ed18cb2404e7e78c53",
    "scratch/t41/out/instructions.part008.json": "840d0e5bfff4ffe11cdbd664657995b731a596ac82976d7bf5bf37578675f43f",
    "scratch/t41/out/branches.part001.json": "645a2b28856286895d8fd283d06f9286f00dc400baebaa150c532e76d1fd47a4",
    "scratch/t41/out/branches.part002.json": "42817fbfec105774d1fd8849c94a43ec57e61e79f2ebb23be6afadfa7b97098e",
    LEDGER_PATH: "20fb4a99a955b800a49078ede30700221ca7a9b32fd98db49b8a2fed981af749",
}
BINARY_SHA256 = "b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4"


class VerifyFailure(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerifyFailure(message)


def path_for(path: str) -> Path:
    return ROOT / Path(path)


def load_json(path: Path | str) -> Any:
    target = path if isinstance(path, Path) else path_for(path)
    return json.loads(target.read_text(encoding="utf-8"))


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_digest(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return digest(raw)


def integer(value: Any) -> int | None:
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        try:
            return int(value, 0)
        except ValueError:
            return None
    return None


def hex_offset(value: Any) -> str:
    number = integer(value)
    require(number is not None, f"invalid source offset {value!r}")
    return f"0x{number:x}"


def instruction_index(cursor: dict[str, Any]) -> dict[int, dict[str, Any]]:
    result: dict[int, dict[str, Any]] = {}
    for name in cursor["instruction_shards"]:
        shard = load_json(path_for(f"scratch/t41/out/{name}"))
        for item in shard["instructions"]:
            offset = integer(item.get("file_offset"))
            if offset is not None:
                require(offset not in result or result[offset] == item, f"conflicting instruction index at {item.get('file_offset')}")
                result[offset] = item
    return result


def check_source_files(fields: dict[str, Any], cursor: dict[str, Any], table: dict[str, Any]) -> list[str]:
    t33 = cursor["t33_differential"]
    expected_paths = [
        fields["occurrences_source"], FIELDS_PATH, CURSOR_PATH, T41_REPORT_PATH,
        *[f"scratch/t41/out/{name}" for name in cursor["instruction_shards"]],
        *[f"scratch/t41/out/{name}" for name in cursor["branch_shards"]],
        t33["path"], t33["rows_file"], t33["historical_negative"]["path"], LEDGER_PATH,
    ]
    require(len(expected_paths) == len(set(expected_paths)), "duplicate expected t41 artifact path")
    require(set(expected_paths) == set(EXPECTED_SOURCE_HASHES), "source artifact inventory differs from frozen E82 evidence")
    for path, expected_hash in EXPECTED_SOURCE_HASHES.items():
        target = path_for(path)
        require(target.is_file(), f"missing source artifact: {path}")
        actual_hash = digest(target.read_bytes())
        require(actual_hash == expected_hash, f"source artifact SHA-256 mismatch: {path}")

    listed = table["source_artifacts"]
    require(listed == expected_paths, "Csme source artifact path list/order mismatch")
    all_artifacts = {item["path"]: item for item in load_json(OUT_JSON)["source_artifacts"]}
    for path in expected_paths:
        item = all_artifacts.get(path)
        require(item is not None, f"schema source_artifacts missing {path}")
        raw = path_for(path).read_bytes()
        require(item.get("sha256") == digest(raw) and item.get("bytes") == len(raw), f"schema artifact digest/size mismatch: {path}")
    return expected_paths


def check_provenance(field: dict[str, Any], record: dict[str, Any], category: str,
                     expected_paths: list[str], extent: dict[str, Any], index: dict[int, dict[str, Any]]) -> None:
    provenance = field["provenance"]
    require(provenance.get("task") == "t41" and provenance.get("field_ledger") == FIELDS_PATH, f"{field['code']} source ledger mismatch")
    require(provenance.get("source_files") == expected_paths, f"{field['code']} provenance file list mismatch")
    require(provenance.get("source_record") == record, f"{field['code']} source record was altered")
    require(provenance.get("source_record_sha256") == canonical_digest(record), f"{field['code']} source-record digest mismatch")
    require(provenance.get("binary") == "editor.exe" and provenance.get("binary_sha256") == BINARY_SHA256, f"{field['code']} binary provenance mismatch")
    require(provenance.get("reader_extent") == extent, f"{field['code']} reader extent mismatch")

    sink = record.get("sink") or record.get("candidate_sink")
    offset = integer(sink["site"])
    reader = index[offset]
    reader_site = provenance["reader_transfer_sites"]
    require(len(reader_site) == 1, f"{field['code']} should have exactly one reader transfer site")
    site = reader_site[0]
    require(site.get("role") == "row_reader_transfer", f"{field['code']} reader-site role mismatch")
    require(site.get("file_offset") == hex_offset(sink["site"]) and site.get("VA") == reader["VA"], f"{field['code']} reader-site address mismatch")
    require(site.get("width_bytes") == sink["width"] and site.get("legacy_offset") == sink["legacy"] and site.get("wire_offset") == sink["wire"], f"{field['code']} reader sink coordinates mismatch")
    require(site.get("condition") == sink["when"] and site.get("instruction") == reader["instruction"], f"{field['code']} reader instruction/condition mismatch")

    expected_getter_offsets: list[int] = []
    getter = record["getter"]
    if getter.get("compare") is not None:
        expected_getter_offsets.append(integer(getter["compare"]))
    if getter.get("box_call") is not None:
        expected_getter_offsets.append(integer(getter["box_call"]))
    if getter.get("member_load") is not None:
        expected_getter_offsets.append(integer(getter["member_load"]))
    expected_getter_offsets.extend(integer(value) for value in getter.get("lane_loads", []))
    actual_getter = provenance.get("getter_accesses", [])
    require([integer(item["file_offset"]) for item in actual_getter] == expected_getter_offsets, f"{field['code']} getter evidence sites mismatch")
    for item in actual_getter:
        source = index[integer(item["file_offset"])]
        require(item.get("VA") == source["VA"] and item.get("instruction") == source["instruction"], f"{field['code']} getter instruction mismatch")

    expected_writers = list(record.get("write_sites", []))
    if sink.get("writer_site") is not None:
        expected_writers.append(sink["writer_site"])
    actual_writers = provenance.get("writer_sites", [])
    require([integer(item["file_offset"]) for item in actual_writers] == expected_writers, f"{field['code']} writer-site list mismatch")
    for item in actual_writers:
        source = index[integer(item["file_offset"])]
        require(item.get("VA") == source["VA"] and item.get("instruction") == source["instruction"], f"{field['code']} writer instruction mismatch")

    require(field.get("schema", {}).get("idx") == int(record["occurrence"][2]), f"{field['code']} schema occurrence index mismatch")
    expected_schema = dict(record["schema"])
    expected_schema["idx"] = int(record["occurrence"][2])
    require(field.get("schema") == expected_schema, f"{field['code']} schema metadata mismatch")
    require(field.get("profile") == record["profile"] and field.get("domain") == record.get("domain"), f"{field['code']} profile/domain changed")
    require(field.get("status") == category and field.get("grade") == record["grade"], f"{field['code']} evidence category/grade mismatch")


def verify_all() -> dict[str, Any]:
    require(V2_JSON.is_file() and digest(V2_JSON.read_bytes()) == V2_JSON_SHA256, "frozen v2 JSON snapshot missing or hash mismatch")
    require(V2_MD.is_file() and digest(V2_MD.read_bytes()) == V2_MD_SHA256, "frozen v2 Markdown snapshot missing or hash mismatch")
    baseline = load_json(V2_JSON)
    baseline_md = V2_MD.read_text(encoding="utf-8")
    schema = load_json(OUT_JSON)
    report = OUT_MD.read_text(encoding="utf-8")
    fields = load_json(FIELDS_PATH)
    cursor = load_json(CURSOR_PATH)
    ledger = load_json(LEDGER_PATH)

    require(baseline.get("schema_version") == 2 and baseline.get("generated_by") == "t42", "frozen baseline identity mismatch")
    require(schema.get("schema_version") == 3 and schema.get("generated_by") == "t45", "public schema is not t45 v3")
    require(schema.get("tables", [])[:7] == baseline.get("tables"), "v2 seven-table content changed")
    require(schema.get("negative_regressions") == baseline.get("negative_regressions") and len(schema["negative_regressions"]) == 4, "original four negative regressions changed")
    require(schema.get("binary_provenance") == baseline.get("binary_provenance"), "v2 binary provenance changed")
    require(schema.get("source_artifacts", [])[:len(baseline["source_artifacts"])] == baseline["source_artifacts"], "v2 source artifact records were not preserved verbatim")
    require(schema.get("schema_provenance", {}).get("acceptance_ledger", {}).get("csme_acceptance_entry") == "E82", "schema E82 cross-reference missing")

    tables = schema.get("tables", [])
    require(len(tables) == 8 and [item.get("parent_code") for item in tables] == [item["parent_code"] for item in baseline["tables"]] + ["Csme"], "table order/count mismatch")
    l3_count = sum(len(item.get("fields", [])) for item in tables)
    held_count = sum(len(item.get("held_fields", [])) for item in tables)
    require((l3_count, held_count) == (52, 16), f"actual field counts are {l3_count} L3 / {held_count} held")
    coverage = schema["coverage"]
    require((coverage.get("club_tables"), coverage.get("club_L3_fields"), coverage.get("held_fields"), coverage.get("negative_regressions"), coverage.get("L4")) == (8, 52, 16, 4, 0), "coverage counters mismatch")
    require(coverage.get("nation_side", {}).get("summary") == baseline["coverage"]["nation_side"]["summary"], "nation summary changed")
    require(coverage.get("nation_side", {}).get("summary", {}).get("new_L3_claims") == 0, "nation-side L3 claims must remain zero")
    require(len(tables[0].get("excluded_non_business_records", [])) == 2, "Cstc non-business records changed")

    table = tables[7]
    require((table.get("table_type"), table.get("parent_xml"), table.get("parent_code"), table.get("rtti_class"), table.get("source_task"), table.get("schema_scope")) == (
        59, "club.xml", "Csme", "STARTING_MEDIA_EXPECTATIONS", "t41", ["club.xml", "Csme"]
    ), "Csme identity/scope mismatch")
    require(table.get("source_ledger_summary") == {
        "status": "accepted_by_E82", "fields_named": 2, "L3": 1, "held": 1,
        "club_exclusive_L3": 0, "L4": 0,
        "offset_origin": "Melf is item-indexed; row_offset/wire_offset denote j=0 only and exist only when count n > 0.",
    }, "Csme source-ledger summary mismatch")

    server = cursor["archives"]["server"]
    client = cursor["archives"]["client"]
    frame = server["selected_frame"]
    histogram = {"22": int(server["stride_histogram"]["22"]), "32": int(server["stride_histogram"]["32"])}
    payload = table["server_payload"]
    computed_payload = 13 + histogram["22"] * 22 + histogram["32"] * 32 + 9
    require(computed_payload == 224880 == server["payload_bytes"] == payload["payload_len"], "Csme variable-length closure arithmetic mismatch")
    require(payload.get("closure_formula") == "13 + 6567 * 22 + 2512 * 32 + 9 = 224880" and payload.get("closure_ok") is True, "Csme closure expression/status mismatch")
    require(payload.get("payload_sha256") == "7eee0ecc59ee306aefc52eb7a7f7095d439748f3e06ac9d36d3ddc1568c8b1a7" == frame["sha256"], "Csme payload SHA mismatch")
    require((payload.get("row_count"), payload.get("stride_histogram_bytes"), payload.get("row_length_formula"), payload.get("count_wire_offset")) == (9079, histogram, "22 + 10*n", 6), "Csme row count/stride/count formula mismatch")
    require(payload.get("wire_footer_start") == 224871 and payload.get("footer_bytes") == 9, "Csme footer coordinate mismatch")
    header = bytes.fromhex(server["header_hex"])
    require(payload.get("header_record_count") == int.from_bytes(header[8:12], "little") == 9079, "Csme header row count mismatch")
    require(table.get("client_observation") == {
        "archive": "client", "present": False, "directory_entry_count": client["directory_entry_count"], "table_entry_absent": True,
    } and client.get("present") is False and client.get("entry") is None, "client table59 absence mismatch")

    owner = fields["unscoped_owner"]
    owner_scope = table["owner_scope"]
    require(owner_scope.get("source_record") == owner, "Csme owner source record changed")
    require((owner_scope.get("target_table_type"), owner_scope.get("owner_rows"), owner_scope.get("distinct_owner_ordinals"), owner_scope.get("selector_histogram")) == (24, 9079, 9079, {"10": 8941, "11": 138}), "Csme owner selector counts mismatch")
    require(owner_scope.get("selector_classes") == {"10": "TEAM", "11": "NATIONAL_TEAM"}, "Csme Team-family selector classes mismatch")
    require(owner_scope.get("club_exclusive_L3") == 0 and owner_scope.get("first_non_club_exclusive_witness") == owner["scope_counterexample"], "Csme club-exclusivity witness missing")
    require(owner_scope.get("scope_caveat") == fields["scope_caveat"], "Csme scope caveat changed")

    records = {item["code"]: item for item in fields["fields"]}
    require(set(records) == {"Msid", "Melf"}, "t41 fields_csme record set changed")
    melf = table.get("fields", [None])[0]
    msid = table.get("held_fields", [None])[0]
    require(melf is not None and msid is not None, "Csme Melf or Msid record missing")
    require(table["fields"] == [melf] and table["held_fields"] == [msid], "unexpected Csme L3/held fields")
    require((melf.get("grade"), melf.get("row_offset"), melf.get("wire_offset"), melf.get("width_bytes")) == ("L3_table59_conditional_named_coordinate", 18, 19, 1), "Melf coordinate/grade mismatch")
    require(melf.get("coordinates") == [{
        "row_offset": "18+10*j", "wire_offset": "19+10*j", "width_bytes": 1,
        "index": "j", "count": "n", "condition": "0 <= j < count",
    }], "Melf item-indexed coordinate mismatch")
    melf_note = melf.get("coordinate_note", "")
    require("only on count=1 rows (2,512 rows)" in melf_note and "count=0 row has no Melf value" in melf_note and "default is not asserted" in melf_note, "Melf absence/default caveat missing")
    require(msid.get("grade") == "held_no_live_media_reference" and msid.get("status") == "held", "Msid was incorrectly promoted")
    require(msid.get("held_reason") == records["Msid"]["reason"], "Msid held reason changed")
    require(msid.get("row_offset") is None and msid.get("wire_offset") is None and msid.get("coordinates") == [], "held Msid acquired a promoted coordinate")
    require(msid.get("candidate_coordinates") == [{
        "row_offset": "10+10*j", "wire_offset": "11+10*j", "width_bytes": 8,
        "index": "j", "count": "n", "condition": "0 <= j < count", "disposition": "held; static sink binding only",
    }], "Msid static candidate binding changed")
    require("no live media-source reference" in msid.get("coordinate_note", ""), "Msid live-reference caveat missing")
    require(table.get("unscoped_evidence") == {
        "outer_non_schema_byte": fields["outer_non_schema_byte"], "inner_tag": fields["inner_tag"],
    }, "unscoped non-schema evidence changed")
    require(table.get("supplemental_evidence", {}).get("historical_t33_differential") == cursor["t33_differential"], "t33 negative/differential was altered")
    require(table["supplemental_evidence"].get("historical_t33_negative") == cursor["t33_differential"]["historical_negative"], "historical t33 negative wording/source changed")

    reader = cursor["reader"]
    expected_extent = {
        "start_file_offset": hex_offset(reader["entry"]),
        "end_file_offset_exclusive": hex_offset(reader["end_exclusive"]),
        "start_VA": reader["entry_VA"],
        "end_VA_exclusive": reader["end_VA"],
        "extent_source": reader["extent_source"],
    }
    require(table.get("reader_extent") == expected_extent, "Csme reader extent does not match t41 cursor")
    require(expected_extent["start_VA"] == "0x141583ba0" and expected_extent["end_VA_exclusive"] == "0x141583f80", "Csme reader VA extent mismatch")
    paths = check_source_files(fields, cursor, table)
    instructions = instruction_index(cursor)
    check_provenance(melf, records["Melf"], "L3", paths, expected_extent, instructions)
    check_provenance(msid, records["Msid"], "held", paths, expected_extent, instructions)

    entries = [item for item in ledger.get("entries", []) if item.get("id") == "E82"]
    require(len(entries) == 1, "E82 is missing from the frozen acceptance ledger")
    accepted = entries[0]
    require(accepted.get("kind") == "acceptance" and accepted.get("level") == "L3", "E82 is not an L3 acceptance")
    require(table.get("source_acceptance", {}).get("claim") == accepted.get("claim"), "Csme source acceptance claim differs from E82")
    require(table.get("source_acceptance", {}).get("ledger_path") == LEDGER_PATH, "Csme acceptance should use the t45 E82 ledger snapshot")

    md_checks = [
        "Generated by t45:", "Club tables: 8", "Accepted L3 business fields: 52", "Held fields: 16",
        "Original negative regressions retained separately: 4", "L4: 0", "client entries for the other seven tables",
        "13 + 6567×22 + 2512×32 + 9 = 224880", "## Csme", "0x141583ba0..0x141583f80",
        "count=0 rows have no Melf value", "Club-exclusive L3 is 0", "tail id pair in every row equals 0x01000000",
        "The four t20 linear-coordinate negatives are retained as source labels",
    ]
    for marker in md_checks:
        require(marker in report, f"public Markdown missing required marker: {marker}")
    require("Generated by t42:" in baseline_md and "Accepted L3 business fields: 51" in baseline_md, "v2 Markdown snapshot content mismatch")

    return {
        "tables": len(tables), "L3": l3_count, "held": held_count,
        "negative_regressions": len(schema["negative_regressions"]), "L4": coverage.get("L4"),
        "source_artifacts": len(schema["source_artifacts"]), "Csme_payload_bytes": payload["payload_len"],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Independently verify t45 schema v3 against frozen v2 and t41 evidence.")
    parser.add_argument("--selftest", action="store_true", help="run the full independent validation without writing files")
    args = parser.parse_args(argv)
    try:
        result = verify_all()
        label = "SELFTEST PASS" if args.selftest else "VERIFY PASS"
        print(f"{label}: {result['tables']} tables, {result['L3']} L3, {result['held']} held, {result['negative_regressions']} negatives, L4={result['L4']}; Csme {result['Csme_payload_bytes']} B; {result['source_artifacts']} artifacts")
        return 0
    except VerifyFailure as exc:
        print(f"VERIFY FAILED: {exc}", file=sys.stderr)
        return 1
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"FATAL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
