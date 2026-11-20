#!/usr/bin/env python3
"""Independent verifier for the t40 club/nation subtable schema."""
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
EXPECTED_BINARY_SHA256 = "b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4"
EXPECTED_L3 = {
    "Cstc": {"Slea", "Scap", "Salt", "Scpm", "Sscp", "Snxa", "Snmn", "Snmx", "Stks", "Slmd", "Slhm", "ScTL", "ScYL", "Sceb"},
    "Clhs": {"orde", "divi", "play", "wins", "draw", "lost", "gfor", "gaga"},
    "CSrs": {"Ttyp", "Tdvi", "tmno", "tmnv", "Tsti", "Twhm", "Tmhm", "Catd", "Cmna", "Cmxa"},
    "Cmti": {"play", "club", "cash", "mths", "pyiv"},
    "CNtp": {"nati", "rati"},
    "Cdbt": {"cash", "sour", "stdt", "endt", "inrt"},
}
EXPECTED_HELD = {
    "Cstc": {"Sold", "Snew", "Ssta", "Styp", "Scam", "Scns"},
    "Clhs": {"year", "posi", "mxtm", "poin"},
    "CSrs": set(),
    "Cmti": {"icom"},
    "CNtp": {"mina", "maxa"},
    "Cdbt": set(),
}
TASKS = {
    "Cstc": ("t27", "fields_t22.json", "cursor_t22.json", 22),
    "Clhs": ("t30", "fields_clhs.json", "cursor_clhs.json", 37),
    "CSrs": ("t31", "fields_csrs.json", "cursor_csrs.json", 62),
    "Cmti": ("t32", "fields_cmti.json", "cursor_cmti.json", 43),
    "CNtp": ("t34", "fields_cntp.json", "cursor_cntp.json", 66),
    "Cdbt": ("t36", "fields_cdbt.json", "cursor_cdbt.json", 33),
}

class VerificationFailure(Exception):
    pass


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha256(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def number(value: Any) -> int | None:
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


def task_inputs(code: str) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]], list[str]]:
    task, field_name, cursor_name, _table_type = TASKS[code]
    root = ROOT / "scratch" / task / "out"
    ledger = read_json(root / field_name)
    if task == "t27":
        records: list[dict[str, Any]] = []
        paths = [f"scratch/t27/out/{field_name}"]
        for part in ledger.get("fields", []):
            path = root / part
            records.extend(read_json(path).get("fields", []))
            paths.append(f"scratch/t27/out/{part}")
    else:
        records = ledger.get("fields", [])
        paths = [f"scratch/{task}/out/{field_name}"]
    cursor = read_json(root / cursor_name)
    instruction_paths = [f"scratch/{task}/out/{name}" for name in cursor.get("instruction_shards", [])]
    paths.extend([f"scratch/{task}/out/{cursor_name}", *instruction_paths])
    return ledger, cursor, records, paths


def build_instruction_map(task: str, cursor: dict[str, Any]) -> dict[int, dict[str, Any]]:
    result: dict[int, dict[str, Any]] = {}
    for shard_name in cursor.get("instruction_shards", []):
        shard = read_json(ROOT / "scratch" / task / "out" / shard_name)
        for instruction in shard.get("instructions", []):
            offset = number(instruction.get("file_offset"))
            if offset is not None:
                result[offset] = instruction
    return result


def record_code(record: dict[str, Any]) -> str | None:
    return record.get("code") or record.get("candidate_code")


def ledgers_by_category(code: str, ledger: dict[str, Any], records: list[dict[str, Any]]) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    accepted: dict[str, dict[str, Any]] = {}
    held: dict[str, dict[str, Any]] = {}
    for record in records:
        field_code = record_code(record)
        grade = record.get("grade", "")
        if code == "Cstc":
            if field_code in ledger.get("promoted_codes", []):
                accepted[field_code] = record
            elif grade in {"L3_code_row_only", "L3_coordinate_profile_conflict"}:
                held[field_code] = record
        elif grade in {"L3_named_row_coordinate", "L3_contextual_row_coordinates"}:
            accepted[field_code] = record
        elif str(grade).startswith("held"):
            held[field_code] = record
    return accepted, held


def validate_source_artifacts(schema: dict[str, Any]) -> None:
    artifacts = schema.get("source_artifacts", [])
    indexed = {item.get("path"): item for item in artifacts}
    if len(indexed) != len(artifacts):
        raise VerificationFailure("duplicate source artifact paths")
    for path, item in indexed.items():
        target = ROOT / Path(path)
        if not target.is_file():
            raise VerificationFailure(f"missing source artifact {path}")
        if sha256(target) != item.get("sha256") or target.stat().st_size != item.get("bytes"):
            raise VerificationFailure(f"source artifact digest/size changed: {path}")
    provenance_path = ROOT / "evidence/fm24/reports/qa/IDA_PROVENANCE.md"
    manifest_path = ROOT / "evidence/MANIFEST.json"
    manifest = read_json(manifest_path)
    entry = next((x for x in manifest.get("files", []) if x.get("path") == "evidence/fm24/reports/qa/IDA_PROVENANCE.md"), None)
    binary = schema.get("binary_provenance", {})
    if entry is None or sha256(provenance_path) != entry.get("sha256"):
        raise VerificationFailure("static binary provenance snapshot is not matched by MANIFEST")
    if (binary.get("sha256") != EXPECTED_BINARY_SHA256
            or binary.get("hash_basis_sha256") != entry.get("sha256")
            or binary.get("manifest_entry_sha256") != entry.get("sha256")
            or binary.get("manifest_sha256") != sha256(manifest_path)):
        raise VerificationFailure("editor.exe provenance does not match snapshot/manifest")


def expected_va_evidence(code: str, record: dict[str, Any], index: dict[int, dict[str, Any]]) -> tuple[list[str], list[str]]:
    sinks: list[str] = []
    getters: list[str] = []
    if code == "Cstc":
        if record.get("VA"):
            sinks.append(record["VA"])
        getter = record.get("getter") or []
        if isinstance(getter, dict):
            getter = [getter]
        for item in getter:
            access = item.get("access") if isinstance(item, dict) else None
            if isinstance(access, dict) and access.get("VA"):
                getters.append(access["VA"])
    else:
        candidates = record.get("candidate_sink") or record.get("sink") or record.get("sinks") or []
        if isinstance(candidates, dict):
            candidates = [candidates]
        for sink in candidates:
            site = sink.get("reader_site", sink.get("site"))
            instruction = index.get(number(site)) if site is not None else None
            if instruction and instruction.get("VA"):
                sinks.append(instruction["VA"])
        getter = record.get("getter") or {}
        if isinstance(getter, list):
            getter_list = getter
        elif isinstance(getter, dict):
            getter_list = [getter]
        else:
            getter_list = []
        for item in getter_list:
            access = item.get("access") if isinstance(item, dict) else None
            if isinstance(access, dict) and access.get("VA"):
                getters.append(access["VA"])
                continue
            if isinstance(access, list):
                getters.extend(x["VA"] for x in access if isinstance(x, dict) and x.get("VA"))
                continue
            offset = next((number(item.get(k)) for k in ("load", "access", "arm") if number(item.get(k)) is not None), None)
            instruction = index.get(offset) if offset is not None else None
            if instruction and instruction.get("VA"):
                getters.append(instruction["VA"])
    return sinks, getters


def verify_layout(code: str, table: dict[str, Any], cursor: dict[str, Any], table_type: int) -> None:
    archive = cursor.get("archives", {}).get("server", {})
    payload = table.get("server_payload", {})
    member = archive.get("archive_member") or {}
    entries = archive.get(f"table{table_type}_entries") or []
    entry = entries[0] if entries else {}
    count = archive.get("row_count", member.get("record_count_header", entry.get("record_count_header")))
    stride = archive.get("stride")
    size = archive.get("payload_len", member.get("size", entry.get("size")))
    footer = archive.get("wire_footer_start")
    if footer is None and archive.get("wire_footer_hex"):
        footer = size - len(bytes.fromhex(archive["wire_footer_hex"]))
    prefix = footer - count * stride if None not in (footer, count, stride) else None
    suffix = size - footer if None not in (size, footer) else None
    if payload.get("row_count") != count or payload.get("stride_bytes") != stride or payload.get("payload_len") != size:
        raise VerificationFailure(f"{code} count/stride/payload length differs from source cursor")
    if payload.get("payload_sha256") != archive.get("payload_sha256"):
        raise VerificationFailure(f"{code} payload SHA differs from source cursor")
    if prefix != 13 or suffix != 9 or prefix + count * stride + suffix != size:
        raise VerificationFailure(f"{code} source cursor framing does not close")
    if payload.get("row_stream_prefix_bytes") != prefix or payload.get("footer_bytes") != suffix or not payload.get("closure_ok"):
        raise VerificationFailure(f"{code} serialized closure is inconsistent")


def verify_client_layout(code: str, table: dict[str, Any], cursor: dict[str, Any], table_type: int) -> None:
    archive = cursor.get("archives", {}).get("client", {})
    observed = table.get("client_observation", {})
    if code != "Cstc":
        if archive.get("present") or observed.get("present"):
            raise VerificationFailure(f"{code} unexpectedly has a client table")
        return
    member = archive.get("archive_member") or {}
    entries = archive.get(f"table{table_type}_entries") or []
    entry = entries[0] if entries else {}
    count = archive.get("row_count", member.get("record_count_header", entry.get("record_count_header")))
    stride = archive.get("stride")
    size = member.get("size", entry.get("size"))
    footer = archive.get("wire_footer_start")
    if footer is None and archive.get("wire_footer_hex"):
        footer = size - len(bytes.fromhex(archive["wire_footer_hex"]))
    prefix = footer - count * stride if None not in (footer, count, stride) else None
    suffix = size - footer if None not in (size, footer) else None
    if (not observed.get("present") or observed.get("row_count") != count
            or observed.get("stride_bytes") != stride or observed.get("payload_len") != size
            or observed.get("payload_sha256") != archive.get("payload_sha256")):
        raise VerificationFailure("Cstc client identity table differs from cursor")
    if prefix != 13 or suffix != 9 or prefix + count * stride + suffix != size or not observed.get("closure_ok"):
        raise VerificationFailure("Cstc client identity payload closure failed")


def verify() -> tuple[int, int, int]:
    if not SCHEMA_PATH.is_file():
        raise VerificationFailure(f"missing schema {SCHEMA_PATH}")
    schema = read_json(SCHEMA_PATH)
    validate_source_artifacts(schema)
    tables = {table.get("parent_code"): table for table in schema.get("tables", [])}
    if set(tables) != set(TASKS):
        raise VerificationFailure("schema table set differs from six accepted sources")
    if len(schema.get("negative_regressions", [])) != 4:
        raise VerificationFailure("the four t27 negative regressions are not preserved")
    t27_ledger = read_json(ROOT / "scratch/t27/out/fields_t22.json")
    if schema.get("negative_regressions") != t27_ledger.get("negative_regressions"):
        raise VerificationFailure("t27 negative regressions differ from their source ledger")
    if schema.get("coverage", {}).get("L4") != 0:
        raise VerificationFailure("L4 must remain zero")
    if schema.get("coverage", {}).get("club_L3_fields") != 44 or schema.get("coverage", {}).get("held_fields") != 13:
        raise VerificationFailure("schema coverage totals are inconsistent")
    if schema.get("coverage", {}).get("nation_side", {}).get("summary", {}).get("new_L3_claims") != 0:
        raise VerificationFailure("nation inventory no longer supports the recorded zero-new-L3 scope")
    total_l3 = 0
    total_held = 0
    for code, (task, _field_name, _cursor_name, table_type) in TASKS.items():
        ledger, cursor, records, source_paths = task_inputs(code)
        table = tables[code]
        accepted, held = ledgers_by_category(code, ledger, records)
        output_fields = {field.get("code"): field for field in table.get("fields", [])}
        output_held = {field.get("code"): field for field in table.get("held_fields", [])}
        if set(output_fields) != EXPECTED_L3[code] or set(output_fields) != set(accepted):
            raise VerificationFailure(f"{code} L3 field set differs from source ledger")
        if set(output_held) != EXPECTED_HELD[code] or set(output_held) != set(held):
            raise VerificationFailure(f"{code} held field set differs from source ledger")
        index = build_instruction_map(task, cursor)
        for field_code, raw in accepted.items():
            field = output_fields[field_code]
            provenance = field.get("provenance", {})
            if provenance.get("source_record_sha256") != canonical_sha256(raw):
                raise VerificationFailure(f"{code}.{field_code} source record digest mismatch")
            if provenance.get("source_record") != raw:
                raise VerificationFailure(f"{code}.{field_code} source record changed")
            if provenance.get("binary_sha256") != EXPECTED_BINARY_SHA256:
                raise VerificationFailure(f"{code}.{field_code} binary hash mismatch")
            expected_sinks, expected_getters = expected_va_evidence(code, raw, index)
            actual_sinks = [item.get("VA") for item in provenance.get("reader_transfer_sites", [])]
            actual_getters = [item.get("VA") for item in provenance.get("getter_accesses", [])]
            if sorted(actual_sinks) != sorted(expected_sinks) or not expected_sinks:
                raise VerificationFailure(f"{code}.{field_code} reader VA provenance mismatch")
            if sorted(actual_getters) != sorted(expected_getters) or not expected_getters:
                raise VerificationFailure(f"{code}.{field_code} getter VA provenance mismatch")
            if any(path not in source_paths for path in provenance.get("source_files", [])):
                raise VerificationFailure(f"{code}.{field_code} source-file list mismatch")
        for field_code, raw in held.items():
            field = output_held[field_code]
            if field.get("provenance", {}).get("source_record_sha256") != canonical_sha256(raw):
                raise VerificationFailure(f"{code}.{field_code} held source record digest mismatch")
            if field.get("provenance", {}).get("source_record") != raw:
                raise VerificationFailure(f"{code}.{field_code} held source record changed")
        verify_layout(code, table, cursor, table_type)
        verify_client_layout(code, table, cursor, table_type)
        total_l3 += len(output_fields)
        total_held += len(output_held)
    if total_l3 != 44 or total_held != 13:
        raise VerificationFailure(f"wrong aggregate counts: L3={total_l3} held={total_held}")
    if not MARKDOWN_PATH.is_file():
        raise VerificationFailure(f"missing markdown report {MARKDOWN_PATH}")
    text = MARKDOWN_PATH.read_text(encoding="utf-8")
    for marker in ("Accepted L3 business fields: 44", "Held fields: 13", "L4: 0", "Negative Regressions"):
        if marker not in text:
            raise VerificationFailure(f"markdown report missing marker: {marker}")
    return len(tables), total_l3, total_held


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Independently verify the generated t40 club/nation subtable schema.")
    parser.add_argument("--selftest", action="store_true", help="run the full independent verification suite")
    args = parser.parse_args(argv)
    try:
        table_count, l3_count, held_count = verify()
        if args.selftest:
            print(f"SELFTEST PASS: tables={table_count} L3={l3_count} held={held_count} negatives=4 L4=0")
        else:
            print(f"VERIFY PASS: tables={table_count} L3={l3_count} held={held_count} negatives=4 L4=0; source hashes, field sets, VA provenance, and closures match")
        return 0
    except VerificationFailure as exc:
        print(f"VERIFY FAILED: {exc}", file=sys.stderr)
        return 1
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"FATAL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
