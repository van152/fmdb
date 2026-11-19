#!/usr/bin/env python3
"""Independent verifier for the t42 v2 schema; does not import its builder."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
SCHEMA_PATH = ROOT / "reports" / "club_nation_subtable_schema.json"
MARKDOWN_PATH = ROOT / "reports" / "club_nation_subtable_schema.md"
OUT_DIR = Path(__file__).resolve().parent
V1_JSON_SNAPSHOT = OUT_DIR / "club_nation_subtable_schema.v1.json"
V1_MD_SNAPSHOT = OUT_DIR / "club_nation_subtable_schema.v1.md"
V1_JSON_SHA256 = "963bfec0ee13ecff23fe05cb1a622841eaff46735fbda2a5dcbda72f9fdc5a7c"
V1_MD_SHA256 = "3e713d47daecc05e72bf077e719ef41e71525456af91edf97b70ae01949ea163"
BINARY_SHA256 = "b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4"
MASTER_PATH = "evidence/fm24/reports/editor_schema/master.json"
MASTER_SHA256 = "7d57477e144d5359ccde64bb24b3ba7c640ef41738ed196eba8a38e792776eda"
MANIFEST_PATH = "evidence/MANIFEST.json"
LEDGER_PATH = "scratch/t01/LEDGER.json"
FIELDS_PATH = "scratch/t39/out/fields_tchl.json"
CURSOR_PATH = "scratch/t39/out/cursor_tchl.json"
REPORT_PATH = "scratch/t39/out/REPORT.md"
EXPECTED_L3 = {"tchc", "mstn", "sstn", "dbrt", "posi", "cquf", "tcop"}
EXPECTED_HELD = {"styr", "edyr"}
EXPECTED_TABLES = ["Cstc", "Clhs", "CSrs", "Cmti", "CNtp", "Cdbt", "Tchl"]


class VerificationFailure(Exception):
    pass


def rel(path: str) -> Path:
    return ROOT / Path(path)


def read_json(path: Path | str) -> Any:
    target = path if isinstance(path, Path) else rel(path)
    return json.loads(target.read_text(encoding="utf-8"))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_sha256(value: Any) -> str:
    data = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256_bytes(data)


def as_int(value: Any) -> int | None:
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


def hex_offset(value: Any) -> str | None:
    number = as_int(value)
    return None if number is None else f"0x{number:x}"


def fail(message: str) -> None:
    raise VerificationFailure(message)


def load_frozen_v1() -> tuple[dict[str, Any], str]:
    if not V1_JSON_SNAPSHOT.is_file() or not V1_MD_SNAPSHOT.is_file():
        fail("frozen t40 v1 JSON/Markdown snapshots are missing")
    raw_json = V1_JSON_SNAPSHOT.read_bytes()
    raw_md = V1_MD_SNAPSHOT.read_bytes()
    if sha256_bytes(raw_json) != V1_JSON_SHA256 or sha256_bytes(raw_md) != V1_MD_SHA256:
        fail("frozen v1 baseline SHA-256 mismatch")
    baseline = json.loads(raw_json.decode("utf-8"))
    if baseline.get("schema_version") != 1 or baseline.get("generated_by") != "t40":
        fail("v1 baseline is not the accepted t40 schema")
    return baseline, raw_md.decode("utf-8")


def source_paths(cursor: dict[str, Any]) -> list[str]:
    paths = [FIELDS_PATH, CURSOR_PATH, REPORT_PATH]
    paths.extend(f"scratch/t39/out/{name}" for name in cursor.get("instruction_shards", []))
    paths.extend(f"scratch/t39/out/{name}" for name in cursor.get("branch_shards", []))
    if len(paths) != len(set(paths)):
        fail("duplicate t39 source paths")
    return paths


def instruction_map(cursor: dict[str, Any]) -> dict[int, dict[str, Any]]:
    result: dict[int, dict[str, Any]] = {}
    for name in cursor.get("instruction_shards", []):
        shard = read_json(rel(f"scratch/t39/out/{name}"))
        for instruction in shard.get("instructions", []):
            offset = as_int(instruction.get("file_offset"))
            if offset is None:
                continue
            if offset in result and result[offset].get("VA") != instruction.get("VA"):
                fail(f"conflicting instruction VA at {name}:{instruction.get('file_offset')}")
            result[offset] = instruction
    return result


def expected_schema_index(record: dict[str, Any]) -> int:
    for item in record.get("scoped_occurrences", []):
        if len(item) >= 3 and item[0:2] == ["club.xml", "Tchl"]:
            return int(item[2])
    fail(f"no club/Tchl schema index for {record.get('code')}")
    raise AssertionError


def expected_reader_sites(record: dict[str, Any], index: dict[int, dict[str, Any]]) -> list[dict[str, Any]]:
    result = []
    for sink in record.get("sinks", []):
        offset = as_int(sink.get("site"))
        instruction = index.get(offset) if offset is not None else None
        if not instruction or not instruction.get("VA"):
            fail(f"missing t39 reader VA for {record.get('code')} sink")
        result.append({
            "role": "row_reader_transfer",
            "file_offset": hex_offset(offset),
            "VA": instruction["VA"],
            "width_bytes": sink.get("width"),
            "row_offset": sink.get("legacy_offset"),
            "wire_offset": sink.get("wire_offset"),
            "object_offset": sink.get("object_offset"),
            "instruction": instruction.get("instruction"),
        })
    return result


def expected_getter_sites(record: dict[str, Any], index: dict[int, dict[str, Any]]) -> list[dict[str, Any]]:
    getter = record.get("getter") or {}
    object_offsets = [int(value) for value in getter.get("object_offsets", [])]
    selected: dict[int, tuple[int, dict[str, Any]]] = {}
    for offset in getter.get("evidence", []):
        instruction = index.get(offset)
        if not instruction:
            continue
        text = instruction.get("instruction", "")
        for object_offset in object_offsets:
            if re.search(rf"\[rcx \+ 0x{object_offset:x}\]", text, re.IGNORECASE):
                selected.setdefault(object_offset, (offset, instruction))
    if not selected and getter.get("load") is not None:
        offset = as_int(getter.get("load"))
        instruction = index.get(offset) if offset is not None else None
        if instruction:
            selected[object_offsets[0] if object_offsets else -1] = (offset, instruction)
    if object_offsets and set(selected) != set(object_offsets):
        fail(f"getter access list does not cover Tchl.{record.get('code')} object offsets")
    return [{
        "role": "static_getter_access",
        "file_offset": hex_offset(offset),
        "VA": instruction.get("VA"),
        "instruction": instruction.get("instruction"),
        "object_offset": object_offset if object_offset >= 0 else None,
    } for object_offset, (offset, instruction) in sorted(selected.items())]


def expected_held_reason(record: dict[str, Any]) -> str:
    profile = record["profile"]
    domain = record["domain"]
    violation = profile["first_violation"]
    coordinate = violation["coordinates"][0]
    return (
        f"u16_year_integer; {profile['zero_count']} zero values conflict with frozen XML "
        f"{domain['xml_bounds']}; first counterexample row {violation['row']} "
        f"@{coordinate['offset']}: {coordinate['hex']}"
    )


def validate_master_and_acceptance(schema: dict[str, Any]) -> None:
    master = rel(MASTER_PATH)
    manifest_file = rel(MANIFEST_PATH)
    manifest = read_json(manifest_file)
    entries = [entry for entry in manifest.get("files", []) if entry.get("path") == MASTER_PATH]
    if len(entries) != 1:
        fail("MANIFEST must contain exactly one frozen master.json entry")
    entry = entries[0]
    master_hash = sha256_file(master)
    manifest_hash = sha256_file(manifest_file)
    if master_hash != MASTER_SHA256 or entry.get("sha256") != master_hash or entry.get("bytes") != master.stat().st_size:
        fail("master.json SHA/size does not match frozen MANIFEST entry")
    metadata = schema.get("schema_provenance", {})
    expected = {
        "master_json_path": MASTER_PATH,
        "master_json_sha256": MASTER_SHA256,
        "master_json_bytes": master.stat().st_size,
        "manifest_path": MANIFEST_PATH,
        "manifest_sha256": manifest_hash,
        "manifest_entry_sha256": entry.get("sha256"),
        "manifest_entry_bytes": entry.get("bytes"),
        "manifest_match": True,
        "snapshot_date": manifest.get("snapshot_date"),
    }
    for key, value in expected.items():
        if metadata.get(key) != value:
            fail(f"schema_provenance.{key} differs from frozen source")
    ledger = read_json(LEDGER_PATH)
    acceptance = {item.get("id"): item for item in ledger.get("entries", []) if item.get("id") in {"E78", "E79"}}
    if set(acceptance) != {"E78", "E79"}:
        fail("t01 ledger is missing E78/E79 acceptance entries")
    if acceptance["E78"].get("kind") != "acceptance" or acceptance["E79"].get("kind") != "acceptance_with_note":
        fail("t01 ledger E78/E79 acceptance kinds differ")
    if metadata.get("acceptance_ledger") != {
        "path": LEDGER_PATH,
        "v1_acceptance_entry": "E79",
        "tchl_acceptance_entry": "E78",
    }:
        fail("schema acceptance cross-reference differs from t01 ledger")


def validate_artifacts(schema: dict[str, Any], baseline: dict[str, Any], expected_t39_paths: list[str]) -> None:
    artifacts = schema.get("source_artifacts", [])
    by_path = {item.get("path"): item for item in artifacts}
    if len(by_path) != len(artifacts):
        fail("duplicate source artifact paths")
    old = {item["path"]: item for item in baseline.get("source_artifacts", [])}
    for path, item in old.items():
        if by_path.get(path) != item:
            fail(f"accepted v1 source artifact changed: {path}")
    additions = set(expected_t39_paths) | {MASTER_PATH, LEDGER_PATH}
    if not additions <= set(by_path):
        fail(f"schema source artifacts omit required t39/master/ledger paths: {sorted(additions - set(by_path))}")
    for path, item in by_path.items():
        target = rel(path)
        if not target.is_file():
            fail(f"missing source artifact {path}")
        if target.stat().st_size != item.get("bytes") or sha256_file(target) != item.get("sha256"):
            fail(f"source artifact hash/size mismatch: {path}")


def validate_tchl_field(
    field: dict[str, Any], record: dict[str, Any], category: str,
    source_list: list[str], index: dict[int, dict[str, Any]], reader_extent: dict[str, Any],
) -> None:
    code = record.get("code")
    if field.get("code") != code or field.get("status") != category or field.get("grade") != record.get("grade"):
        fail(f"Tchl.{code} identity/status differs from t39 source")
    schema = dict(record.get("schema", {}))
    schema["idx"] = expected_schema_index(record)
    if field.get("schema") != schema:
        fail(f"Tchl.{code} schema fields/index differ from t39 source")
    for key in ("row_offset", "wire_offset", "interpretation", "domain", "profile"):
        if field.get(key) != record.get(key):
            fail(f"Tchl.{code} {key} differs from t39 source")
    expected_coordinates = [{
        "row_offset": sink.get("legacy_offset"),
        "wire_offset": sink.get("wire_offset"),
        "width_bytes": sink.get("width"),
    } for sink in record.get("sinks", [])]
    if field.get("coordinates") != expected_coordinates:
        fail(f"Tchl.{code} candidate/accepted coordinates differ from sink records")
    expected_width = sum(item["width_bytes"] for item in expected_coordinates)
    if field.get("width_bytes") != expected_width:
        fail(f"Tchl.{code} aggregate width differs from physical sinks")
    if field.get("name") != record.get("schema", {}).get("name"):
        fail(f"Tchl.{code} schema display name differs")
    if category == "held":
        if field.get("held_reason") != expected_held_reason(record):
            fail(f"Tchl.{code} held reason/first counterexample changed")
    elif field.get("held_reason") is not None:
        fail(f"Tchl.{code} L3 field has a held reason")
    provenance = field.get("provenance", {})
    if provenance.get("task") != "t39" or provenance.get("field_ledger") != FIELDS_PATH:
        fail(f"Tchl.{code} source task/ledger mismatch")
    if provenance.get("source_files") != source_list:
        fail(f"Tchl.{code} source file list mismatch")
    if provenance.get("source_record") != record or provenance.get("source_record_sha256") != canonical_sha256(record):
        fail(f"Tchl.{code} original t39 record/digest changed")
    if provenance.get("binary_sha256") != BINARY_SHA256:
        fail(f"Tchl.{code} editor binary provenance mismatch")
    if provenance.get("reader_extent") != reader_extent:
        fail(f"Tchl.{code} reader extent mismatch")
    if provenance.get("reader_transfer_sites") != expected_reader_sites(record, index):
        fail(f"Tchl.{code} reader transfer VA provenance mismatch")
    if provenance.get("getter_accesses") != expected_getter_sites(record, index):
        fail(f"Tchl.{code} getter access VA provenance mismatch")
    for coordinate in expected_coordinates:
        if coordinate["wire_offset"] != coordinate["row_offset"] + 1:
            fail(f"Tchl.{code} row/wire coordinate origin is inconsistent")


def validate_tchl_table(table: dict[str, Any], ledger: dict[str, Any], cursor: dict[str, Any], paths: list[str]) -> None:
    if table.get("parent_code") != "Tchl" or table.get("table_type") != 34 or table.get("rtti_class") != "STARTING_TEAM_CUP_HISTORY":
        fail("Tchl table identity/RTTI mismatch")
    if table.get("source_task") != "t39" or table.get("entity") != "club_nation_shared":
        fail("Tchl source task/shared entity scope mismatch")
    if table.get("schema_scope") != ledger.get("scope") or table.get("source_artifacts") != paths:
        fail("Tchl scope or source artifact paths differ")
    if table.get("source_acceptance") != {"ledger_path": LEDGER_PATH, "entry_id": "E78", "level": "L3", "kind": "acceptance"}:
        fail("Tchl acceptance marker differs from E78")
    source_records = {item.get("code"): item for item in ledger.get("fields", [])}
    accepted = {code: item for code, item in source_records.items() if item.get("grade") in {"L3_table34_named_coordinate", "L3_table34_named_compound_coordinate"}}
    held = {code: item for code, item in source_records.items() if item.get("grade") == "held_domain_conflict"}
    fields = {item.get("code"): item for item in table.get("fields", [])}
    held_fields = {item.get("code"): item for item in table.get("held_fields", [])}
    if set(accepted) != EXPECTED_L3 or set(fields) != EXPECTED_L3:
        fail("Tchl accepted L3 field set differs from t39")
    if set(held) != EXPECTED_HELD or set(held_fields) != EXPECTED_HELD:
        fail("Tchl held field set differs from t39")
    instruction_index = instruction_map(cursor)
    reader = cursor["reader"]
    reader_extent = {
        "start_file_offset": hex_offset(reader["entry"]),
        "end_file_offset_exclusive": hex_offset(reader["end_exclusive"]),
        "start_VA": reader["entry_VA"],
        "end_VA_exclusive": reader["end_VA"],
        "extent_source": reader["extent_source"],
    }
    if table.get("reader_extent") != reader_extent:
        fail("Tchl table-level reader extent differs from cursor")
    for code, record in accepted.items():
        validate_tchl_field(fields[code], record, "L3", paths, instruction_index, reader_extent)
    for code, record in held.items():
        validate_tchl_field(held_fields[code], record, "held", paths, instruction_index, reader_extent)

    archives = cursor["archives"]
    server = archives["server"]
    entry = server["entry"]
    selected = server["selected_frame"]
    payload = table.get("server_payload", {})
    count, stride, size = int(server["row_count"]), int(server["stride"]), int(server["payload_bytes"])
    footer = int(server["wire_footer_offset"])
    prefix, suffix = footer - count * stride, size - footer
    header = bytes.fromhex(server["header_hex"])
    expected_layout = {
        "archive": "server", "present": True, "path": entry["path"],
        "row_count": count, "stride_bytes": stride, "payload_len": size,
        "payload_sha256": server["payload_sha256"], "header_hex": server["header_hex"],
        "header_record_count": int.from_bytes(header[8:12], "little"),
        "row_stream_prefix_bytes": prefix, "selector_bytes_per_row": 1,
        "row_body_bytes": stride - 1, "wire_footer_start": footer,
        "footer_hex": server["wire_footer_hex"], "footer_bytes": suffix,
        "closure_formula": f"{prefix} + {count} * {stride} + {suffix} = {size}",
        "closure_ok": prefix == 13 and suffix == 9 and prefix + count * stride + suffix == size,
        "legacy_row_origin": server["legacy_origin"], "wire_row_origin": server["wire_origin"],
        "legacy_footer_start": server["legacy_footer_offset"], "legacy_footer_hex": server["legacy_footer_hex"],
        "archive_member_offset": entry["offset"], "archive_member_packed_size": entry["packed_size"],
        "selected_frame_offset": selected["offset"], "selected_frame_packed_size": selected["compressed_bytes"],
    }
    if payload != expected_layout:
        fail("Tchl server payload metadata differs from t39 cursor")
    if (count, stride, size, payload.get("payload_sha256")) != (
            7115, 44, 313082, "a07b2bb76fb8796bcbc39dde659610d5257a8801004b6608e4be34beb9a84812"):
        fail("Tchl server count/stride/payload SHA differ from accepted t39 evidence")
    client = table.get("client_observation", {})
    if client != {
        "archive": "client", "present": False,
        "directory_entry_count": archives["client"]["directory_entry_count"],
        "table_entry_absent": True,
    }:
        fail("Tchl client absence must not be represented as an empty table")

    domains = table.get("reference_domains", {})
    owner = ledger["unscoped_owner"]
    owner_profile = owner["profile"]
    if domains.get("ordinal_target_domains") != ledger.get("target_domains"):
        fail("Tchl table 23/24/25 ordinal target-domain evidence differs")
    shared_owner = domains.get("shared_owner_domain", {})
    if shared_owner.get("source_record") != owner or shared_owner.get("target_table_type") != 24:
        fail("Tchl shared owner source/target table mismatch")
    if shared_owner.get("nonnull_owner_count") != 7084 or shared_owner.get("null_owner_count") != 31:
        fail("Tchl shared owner count/null count mismatch")
    if shared_owner.get("target_selector_counts") != {"11": 7084} or owner_profile.get("target_selector_histogram") != {"11": 7084}:
        fail("Tchl nonempty owner selector evidence differs")
    if shared_owner.get("club_exclusive_L3") != 0 or ledger.get("club_exclusive_L3") != 0:
        fail("Tchl club-exclusive L3 must remain zero")
    basis = shared_owner.get("exclusivity_basis", "")
    if "entity_tag is not used" not in basis or "selector" not in basis:
        fail("Tchl owner exclusivity note is incomplete")
    field_targets = {
        "tchc": 25, "cquf": 25, "mstn": 23, "sstn": 23, "tcop": 24,
    }
    for code, target in field_targets.items():
        if fields[code].get("domain", {}).get("target_table") != target:
            fail(f"Tchl.{code} reference target does not match table {target}")
    if len(fields["dbrt"].get("coordinates", [])) != 2:
        fail("dbrt double-slot field was collapsed")


def verify_markdown(text: str, baseline_md: str, baseline: dict[str, Any], schema: dict[str, Any]) -> None:
    markers = [
        "Club tables: 7", "Accepted L3 business fields: 51", "Held fields: 15",
        "Original negative regressions retained separately: 4", "L4: 0", "## Tchl",
        "0x144511e90..0x14451206f", "7,084 nonempty owner ordinals",
        "first counterexample row 28 @1254", "row 2695 @118604", "Negative Regressions",
    ]
    for marker in markers:
        if marker not in text:
            fail(f"Markdown report missing required marker: {marker}")
    for table in baseline["tables"]:
        for field in table.get("fields", []):
            marker = f"`{table['parent_code']}.{field['code']}`"
            if marker not in text:
                fail(f"Markdown omitted preserved v1 field {marker}")
        for field in table.get("held_fields", []):
            if f"`{field['code']}`" not in text:
                fail(f"Markdown omitted held v1 field {table['parent_code']}.{field['code']}")
    for item in baseline.get("negative_regressions", []):
        if f"`{item['code']}`" not in text or item["status"] not in text:
            fail(f"Markdown omitted original negative regression {item.get('code')}")
    for field in schema["tables"][-1]["fields"]:
        if f"`Tchl.{field['code']}`" not in text:
            fail(f"Markdown omitted Tchl.{field['code']}")
    # The v1 report's accepted rows and negative table remain byte-for-byte substrings.
    for line in baseline_md.splitlines():
        if line.startswith("| `") and ("L3_named" in line or "L3_contextual" in line):
            if line not in text:
                fail("a v1 accepted Markdown field row was rewritten")


def verify() -> tuple[int, int, int]:
    if not SCHEMA_PATH.is_file() or not MARKDOWN_PATH.is_file():
        fail("v2 schema JSON/Markdown output is missing")
    baseline, baseline_md = load_frozen_v1()
    schema = read_json(SCHEMA_PATH)
    if schema.get("schema_id") != "fm24.club_nation_subtable_schema" or schema.get("schema_version") != 2 or schema.get("generated_by") != "t42":
        fail("schema identity/version/generator mismatch")
    if [table.get("parent_code") for table in schema.get("tables", [])] != EXPECTED_TABLES:
        fail("schema table sequence differs from v1 plus Tchl")
    if schema["tables"][:6] != baseline["tables"]:
        fail("one or more v1 table structures/44 fields/13 held/two Cstc slots changed")
    if schema.get("negative_regressions") != baseline.get("negative_regressions") or len(schema.get("negative_regressions", [])) != 4:
        fail("the four original negative regression records were modified")
    if schema.get("binary_provenance") != baseline.get("binary_provenance"):
        fail("accepted v1 binary provenance changed")
    if schema.get("coverage", {}).get("L4") != 0:
        fail("L4 must remain zero")
    coverage = schema.get("coverage", {})
    if (coverage.get("club_tables"), coverage.get("club_L3_fields"), coverage.get("held_fields"), coverage.get("negative_regressions")) != (7, 51, 15, 4):
        fail("coverage counts must be 7/51/15/4")
    nation_summary = coverage.get("nation_side", {}).get("summary", {})
    if nation_summary != baseline["coverage"]["nation_side"]["summary"] or nation_summary.get("new_L3_claims") != 0:
        fail("t37 partial nation inventory context was promoted or changed")
    validate_master_and_acceptance(schema)

    ledger = read_json(FIELDS_PATH)
    cursor = read_json(CURSOR_PATH)
    paths = source_paths(cursor)
    validate_artifacts(schema, baseline, paths)
    validate_tchl_table(schema["tables"][-1], ledger, cursor, paths)
    total_l3 = sum(len(table.get("fields", [])) for table in schema["tables"])
    total_held = sum(len(table.get("held_fields", [])) for table in schema["tables"])
    if total_l3 != 51 or total_held != 15:
        fail(f"aggregate field counts differ: L3={total_l3} held={total_held}")
    markdown = MARKDOWN_PATH.read_text(encoding="utf-8")
    verify_markdown(markdown, baseline_md, baseline, schema)
    return len(schema["tables"]), total_l3, total_held


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Independently verify t42 v2 while comparing against the frozen t40 v1 snapshot.")
    parser.add_argument("--selftest", action="store_true", help="run full preservation, source, provenance, and closure verification")
    args = parser.parse_args(argv)
    try:
        table_count, l3_count, held_count = verify()
        label = "SELFTEST PASS" if args.selftest else "VERIFY PASS"
        print(f"{label}: tables={table_count} L3={l3_count} held={held_count} negatives=4 Cstc_non_business=2 L4=0; v1 verbatim; Tchl source/VA/closure; master SHA/MANIFEST")
        return 0
    except VerificationFailure as exc:
        print(f"VERIFY FAILED: {exc}", file=sys.stderr)
        return 1
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"FATAL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
