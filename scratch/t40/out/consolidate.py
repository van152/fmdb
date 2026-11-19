#!/usr/bin/env python3
"""Consolidate accepted club/nation subtable L3 ledgers for t40."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
OUT_JSON = ROOT / "reports" / "club_nation_subtable_schema.json"
OUT_MD = ROOT / "reports" / "club_nation_subtable_schema.md"
BINARY_SHA256 = "b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4"
PROVENANCE_DOC = "evidence/fm24/reports/qa/IDA_PROVENANCE.md"
MANIFEST_PATH = "evidence/MANIFEST.json"

TASKS = [
    {
        "task": "t27", "code": "Cstc", "table_type": 22,
        "ledger": "scratch/t27/out/fields_t22.json",
        "cursor": "scratch/t27/out/cursor_t22.json",
        "expected_l3": 14, "expected_held": 6,
        "coordinates": "t27 coordinates remain body-relative. The selector is part of each 79-byte stride; do not shift these accepted row offsets.",
    },
    {
        "task": "t30", "code": "Clhs", "table_type": 37,
        "ledger": "scratch/t30/out/fields_clhs.json",
        "cursor": "scratch/t30/out/cursor_clhs.json",
        "expected_l3": 8, "expected_held": 4,
        "coordinates": "row_offset is body-relative; recorded wire_offset includes the one-byte selector (wire_offset = row_offset + 1).",
    },
    {
        "task": "t31", "code": "CSrs", "table_type": 62,
        "ledger": "scratch/t31/out/fields_csrs.json",
        "cursor": "scratch/t31/out/cursor_csrs.json",
        "expected_l3": 10, "expected_held": 0,
        "coordinates": "row_offset is body-relative; recorded wire_offset includes the one-byte selector (wire_offset = row_offset + 1).",
    },
    {
        "task": "t32", "code": "Cmti", "table_type": 43,
        "ledger": "scratch/t32/out/fields_cmti.json",
        "cursor": "scratch/t32/out/cursor_cmti.json",
        "expected_l3": 5, "expected_held": 1,
        "coordinates": "row_offset is body-relative; recorded wire_offset includes the one-byte selector (wire_offset = row_offset + 1). Contextual fields retain all sink coordinates and have no single row_offset.",
    },
    {
        "task": "t34", "code": "CNtp", "table_type": 66,
        "ledger": "scratch/t34/out/fields_cntp.json",
        "cursor": "scratch/t34/out/cursor_cntp.json",
        "expected_l3": 2, "expected_held": 2,
        "coordinates": "row_offset is body-relative; recorded wire_offset includes the one-byte selector (wire_offset = row_offset + 1).",
    },
    {
        "task": "t36", "code": "Cdbt", "table_type": 33,
        "ledger": "scratch/t36/out/fields_cdbt.json",
        "cursor": "scratch/t36/out/cursor_cdbt.json",
        "expected_l3": 5, "expected_held": 0,
        "coordinates": "row_offset is body-relative; recorded wire_offset includes the one-byte selector (wire_offset = row_offset + 1).",
    },
]

class CheckFailure(Exception):
    pass


def rel(path: str) -> Path:
    return ROOT / Path(path)


def read_json(path: str) -> Any:
    return json.loads(rel(path).read_text(encoding="utf-8"))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_sha256(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256_bytes(payload)


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


def file_offset(value: Any) -> str | None:
    number = as_int(value)
    return None if number is None else f"0x{number:x}"


def load_source_rows(spec: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]], list[str]]:
    ledger = read_json(spec["ledger"])
    if spec["task"] == "t27":
        rows: list[dict[str, Any]] = []
        parts = ledger.get("fields", [])
        for part in parts:
            part_path = f"scratch/t27/out/{part}"
            rows.extend(read_json(part_path).get("fields", []))
        field_paths = [spec["ledger"], *[f"scratch/t27/out/{part}" for part in parts]]
    else:
        rows = ledger.get("fields", [])
        field_paths = [spec["ledger"]]
    if not rows:
        raise CheckFailure(f"no field rows in {spec['ledger']}")
    return ledger, rows, field_paths


def load_instruction_index(spec: dict[str, Any], cursor: dict[str, Any]) -> tuple[dict[int, dict[str, Any]], list[str]]:
    paths = [f"scratch/{spec['task']}/out/{name}" for name in cursor.get("instruction_shards", [])]
    index: dict[int, dict[str, Any]] = {}
    for path in paths:
        shard = read_json(path)
        for insn in shard.get("instructions", []):
            offset = as_int(insn.get("file_offset"))
            if offset is None:
                continue
            prior = index.get(offset)
            if prior is not None and prior.get("VA") != insn.get("VA"):
                raise CheckFailure(f"conflicting instruction VA at {path}:{insn.get('file_offset')}")
            index[offset] = insn
    return index, paths


def source_sites(record: dict[str, Any], task: str) -> list[dict[str, Any]]:
    if task == "t27":
        if not record.get("file_offset") and record.get("file_offset") != "0x0":
            return []
        return [{
            "role": "row_reader_transfer",
            "file_offset": record.get("file_offset"),
            "VA": record.get("VA"),
            "width_bytes": record.get("width"),
            "wire_offset": record.get("wire_offset"),
            "instruction": record.get("instruction"),
        }]
    sinks = record.get("candidate_sink") or record.get("sink") or record.get("sinks") or []
    if isinstance(sinks, dict):
        sinks = [sinks]
    result = []
    for sink in sinks:
        site = sink.get("reader_site", sink.get("site"))
        if site is None:
            continue
        result.append({
            "role": "row_reader_transfer",
            "file_offset": file_offset(site),
            "VA": None,
            "width_bytes": sink.get("width"),
            "row_offset": sink.get("legacy_offset", record.get("row_offset")),
            "wire_offset": sink.get("wire_offset", record.get("wire_offset")),
            "object_offset": sink.get("object_offset"),
        })
    return result


def getter_sites(record: dict[str, Any], instruction_index: dict[int, dict[str, Any]]) -> list[dict[str, Any]]:
    getter = record.get("getter")
    entries = getter if isinstance(getter, list) else ([getter] if isinstance(getter, dict) else [])
    result: list[dict[str, Any]] = []
    for entry in entries:
        access = entry.get("access") if isinstance(entry, dict) else None
        if isinstance(access, dict):
            offset = as_int(access.get("file_offset"))
            result.append({
                "role": "static_getter_access",
                "file_offset": file_offset(offset),
                "VA": access.get("VA"),
                "instruction": access.get("instruction"),
                "object_offset": entry.get("object_off", entry.get("object_offset")),
            })
            continue
        if isinstance(access, list):
            for item in access:
                if isinstance(item, dict):
                    offset = as_int(item.get("file_offset"))
                    result.append({
                        "role": "static_getter_access",
                        "file_offset": file_offset(offset),
                        "VA": item.get("VA"),
                        "instruction": item.get("instruction"),
                        "object_offset": entry.get("object_off", entry.get("object_offset")),
                    })
            continue
        chosen_key = next((key for key in ("load", "access", "arm") if as_int(entry.get(key)) is not None), None)
        if chosen_key is None:
            continue
        offset = as_int(entry[chosen_key])
        insn = instruction_index.get(offset) if offset is not None else None
        result.append({
            "role": "static_getter_access",
            "file_offset": file_offset(offset),
            "VA": insn.get("VA") if insn else None,
            "instruction": insn.get("instruction") if insn else None,
            "object_offset": entry.get("object_offset", entry.get("object_off")),
        })
    return result


def classify(spec: dict[str, Any], ledger: dict[str, Any], record: dict[str, Any]) -> str:
    grade = record.get("grade", "")
    code = record.get("code") or record.get("candidate_code")
    if spec["task"] == "t27":
        if code in ledger.get("promoted_codes", []):
            return "L3"
        if grade in {"L3_code_row_only", "L3_coordinate_profile_conflict"}:
            return "held"
        if grade == "unnamed":
            return "non_business"
        raise CheckFailure(f"unclassified t27 field record: {code!r} grade={grade!r}")
    if grade in {"L3_named_row_coordinate", "L3_contextual_row_coordinates"}:
        return "L3"
    if str(grade).startswith("held"):
        return "held"
    raise CheckFailure(f"unclassified field record in {spec['task']}: {code!r} grade={grade!r}")


def schema_info(record: dict[str, Any]) -> dict[str, Any]:
    schema = record.get("schema")
    if isinstance(schema, dict):
        return schema
    occurrences = record.get("schema_occurrences") or []
    return occurrences[0] if occurrences else {}


def width_of(record: dict[str, Any]) -> int | None:
    if isinstance(record.get("width"), int):
        return record["width"]
    sinks = record.get("candidate_sink") or record.get("sink") or record.get("sinks") or []
    if isinstance(sinks, dict):
        sinks = [sinks]
    widths = [s.get("width") for s in sinks if isinstance(s.get("width"), int)]
    if widths and len(set(widths)) == 1:
        return widths[0]
    return None


def held_reason(record: dict[str, Any]) -> str:
    direct = record.get("disposition") or record.get("blocker") or record.get("reason")
    profile = record.get("profile", record.get("data_profile"))
    if isinstance(profile, list):
        profile = profile[0] if profile else {}
    profile = profile if isinstance(profile, dict) else {}
    violations = profile.get("violations")
    if violations is None and profile.get("matches") is not None:
        count = profile.get("count", profile.get("n"))
        if count is not None:
            violations = count - profile["matches"]
    bounds = profile.get("bounds")
    schema = schema_info(record)
    if bounds is None and schema.get("min_value") is not None and schema.get("max_value") is not None:
        bounds = [schema.get("min_value"), schema.get("max_value")]
    first = profile.get("first_violation")
    if first is None:
        samples = profile.get("first_violations") or profile.get("mismatch_samples") or []
        first = samples[0] if samples else None
    details = []
    if violations:
        details.append(f"{violations} profile violations")
    if bounds is not None:
        details.append(f"frozen domain {bounds}")
    if first is not None:
        details.append(f"first counterexample {first}")
    if direct:
        return str(direct) + ("; " + "; ".join(details) if details else "")
    return "; ".join(details) if details else f"held by source grade {record.get('grade', 'unknown')}"


def make_field(spec: dict[str, Any], category: str, record: dict[str, Any], instruction_index: dict[int, dict[str, Any]], source_paths: list[str]) -> dict[str, Any]:
    code = record.get("code") or record.get("candidate_code")
    sites = source_sites(record, spec["task"])
    for site in sites:
        if site.get("VA") is None and site.get("file_offset"):
            insn = instruction_index.get(as_int(site["file_offset"]))
            if insn:
                site["VA"] = insn.get("VA")
                site["instruction"] = insn.get("instruction")
    getters = getter_sites(record, instruction_index)
    schema = schema_info(record)
    coordinates = []
    sinks = record.get("candidate_sink") or record.get("sink") or record.get("sinks") or []
    if isinstance(sinks, dict):
        sinks = [sinks]
    for sink in sinks:
        coordinates.append({
            "row_offset": sink.get("legacy_offset", record.get("row_offset")),
            "wire_offset": sink.get("wire_offset", record.get("wire_offset")),
            "width_bytes": sink.get("width", record.get("width")),
        })
    if not coordinates and record.get("row_offset") is not None:
        coordinates.append({
            "row_offset": record.get("row_offset"),
            "wire_offset": record.get("wire_offset"),
            "width_bytes": record.get("width"),
        })
    elif not coordinates and record.get("wire_offset") is not None:
        coordinates.append({
            "row_offset": None,
            "wire_offset": record.get("wire_offset"),
            "width_bytes": record.get("width"),
        })
    field = {
        "code": code,
        "name": record.get("name") or schema.get("name"),
        "status": category,
        "grade": record.get("grade"),
        "row_offset": record.get("row_offset"),
        "wire_offset": record.get("wire_offset"),
        "coordinates": coordinates,
        "coordinate_note": spec["coordinates"],
        "width_bytes": width_of(record),
        "interpretation": record.get("interpretation") or schema.get("type"),
        "schema": schema,
        "domain": record.get("domain"),
        "profile": record.get("data_profile", record.get("profile", record.get("profiles"))),
        "held_reason": held_reason(record) if category == "held" else None,
        "provenance": {
            "task": spec["task"],
            "field_ledger": spec["ledger"],
            "source_files": source_paths,
            "source_record_sha256": canonical_sha256(record),
            "binary": "editor.exe",
            "binary_sha256": BINARY_SHA256,
            "reader_transfer_sites": sites,
            "getter_accesses": getters,
            "source_record": record,
        },
    }
    return field


def cursor_archive(cursor: dict[str, Any], archive_name: str, table_type: int) -> dict[str, Any]:
    item = cursor.get("archives", {}).get(archive_name, {})
    if not item:
        return {"archive": archive_name, "present": False}
    member = item.get("archive_member") or {}
    entries = item.get(f"table{table_type}_entries") or []
    entry = entries[0] if entries else {}
    present = bool(item.get("present", item.get("status") == "complete_observed_walk" or member or entry))
    if not present:
        return {
            "archive": archive_name,
            "present": False,
            "archive_sha256": item.get("archive_sha256"),
            "directory_entry_count": item.get("directory_entry_count"),
        }
    count = item.get("row_count", member.get("record_count_header", entry.get("record_count_header")))
    stride = item.get("stride")
    payload_len = item.get("payload_len", member.get("size", entry.get("size")))
    footer_start = item.get("wire_footer_start")
    if footer_start is None and payload_len is not None and item.get("wire_footer_hex"):
        footer_start = payload_len - len(bytes.fromhex(item["wire_footer_hex"]))
    header_hex = item.get("header_hex", member.get("payload_magic"))
    if header_hex and len(header_hex) % 2:
        header_hex = None
    prefix = footer_start - count * stride if None not in (footer_start, count, stride) else None
    footer_bytes = payload_len - footer_start if None not in (payload_len, footer_start) else None
    closure_ok = prefix is not None and footer_bytes is not None and prefix + count * stride + footer_bytes == payload_len
    header_bytes = bytes.fromhex(header_hex) if header_hex else b""
    header_count = int.from_bytes(header_bytes[8:12], "little") if len(header_bytes) >= 12 else None
    return {
        "archive": archive_name,
        "present": True,
        "path": member.get("path", entry.get("path")),
        "row_count": count,
        "stride_bytes": stride,
        "payload_len": payload_len,
        "payload_sha256": item.get("payload_sha256"),
        "header_hex": header_hex,
        "header_record_count": header_count,
        "row_stream_prefix_bytes": prefix,
        "selector_bytes_per_row": 1,
        "row_body_bytes": stride - 1 if isinstance(stride, int) else None,
        "wire_footer_start": footer_start,
        "footer_hex": item.get("wire_footer_hex"),
        "footer_bytes": footer_bytes,
        "closure_formula": f"{prefix} + {count} * {stride} + {footer_bytes} = {payload_len}" if closure_ok else None,
        "closure_ok": closure_ok,
        "legacy_row_origin": item.get("legacy_row_origin", item.get("legacy_origin")),
        "wire_row_origin": item.get("wire_row_origin", item.get("wire_origin")),
        "legacy_footer_start": item.get("legacy_footer_start"),
        "legacy_footer_hex": item.get("legacy_footer_hex"),
        "archive_member_sha256": member.get("sha256", entry.get("sha256")),
        "archive_member_offset": member.get("offset", entry.get("offset")),
        "archive_member_packed_size": member.get("packed_size", entry.get("packed_size")),
        "mode": item.get("mode"),
        "swapped_mode_rejection": item.get("swapped_mode_rejection"),
    }


def all_source_artifact_paths() -> tuple[dict[str, list[str]], list[str]]:
    per_task: dict[str, list[str]] = {}
    paths: set[str] = {PROVENANCE_DOC, MANIFEST_PATH, "scratch/t29/out/subtable_inventory.json", "scratch/t37/out/nation_subtable_inventory.json"}
    for spec in TASKS:
        ledger, _, field_paths = load_source_rows(spec)
        cursor = read_json(spec["cursor"])
        instruction_paths = [f"scratch/{spec['task']}/out/{name}" for name in cursor.get("instruction_shards", [])]
        task_paths = list(dict.fromkeys([*field_paths, spec["cursor"], *instruction_paths]))
        per_task[spec["task"]] = task_paths
        paths.update(task_paths)
    return per_task, sorted(paths)


def binary_provenance() -> dict[str, Any]:
    provenance_path = rel(PROVENANCE_DOC)
    manifest = read_json(MANIFEST_PATH)
    entries = [entry for entry in manifest.get("files", []) if entry.get("path") == PROVENANCE_DOC]
    if len(entries) != 1:
        raise CheckFailure(f"expected one MANIFEST entry for {PROVENANCE_DOC}, found {len(entries)}")
    doc_sha = sha256_file(provenance_path)
    entry = entries[0]
    if entry.get("sha256") != doc_sha or entry.get("bytes") != provenance_path.stat().st_size:
        raise CheckFailure("IDA_PROVENANCE.md does not match evidence/MANIFEST.json")
    text = provenance_path.read_text(encoding="utf-8")
    if BINARY_SHA256 not in text:
        raise CheckFailure("editor.exe SHA-256 is not present in the manifested provenance snapshot")
    return {
        "binary": "editor.exe",
        "sha256": BINARY_SHA256,
        "image_base": "0x140000000",
        "hash_basis": PROVENANCE_DOC,
        "hash_basis_sha256": doc_sha,
        "manifest_path": MANIFEST_PATH,
        "manifest_sha256": sha256_file(rel(MANIFEST_PATH)),
        "manifest_entry_sha256": entry["sha256"],
        "snapshot_date": manifest.get("snapshot_date"),
        "external_binary_read": False,
    }


def build_schema() -> dict[str, Any]:
    binary = binary_provenance()
    per_task_paths, artifact_paths = all_source_artifact_paths()
    artifacts = []
    for path in artifact_paths:
        file_path = rel(path)
        artifacts.append({"path": path, "sha256": sha256_file(file_path), "bytes": file_path.stat().st_size})
    artifact_by_path = {entry["path"]: entry for entry in artifacts}
    tables = []
    negatives: list[dict[str, Any]] = []
    for spec in TASKS:
        ledger, records, field_paths = load_source_rows(spec)
        cursor = read_json(spec["cursor"])
        instruction_index, instruction_paths = load_instruction_index(spec, cursor)
        table_paths = list(dict.fromkeys([*field_paths, spec["cursor"], *instruction_paths]))
        l3_fields: list[dict[str, Any]] = []
        held_fields: list[dict[str, Any]] = []
        non_business: list[dict[str, Any]] = []
        for record in records:
            category = classify(spec, ledger, record)
            if category == "non_business":
                non_business.append({
                    "grade": record.get("grade"),
                    "wire_offset": record.get("wire_offset"),
                    "width_bytes": record.get("width"),
                    "disposition": record.get("disposition"),
                    "source_record_sha256": canonical_sha256(record),
                    "source_record": record,
                })
                continue
            field = make_field(spec, category, record, instruction_index, table_paths)
            if category == "L3":
                l3_fields.append(field)
            else:
                held_fields.append(field)
        server = cursor_archive(cursor, "server", spec["table_type"])
        client = cursor_archive(cursor, "client", spec["table_type"])
        reader = cursor.get("reader", {})
        table_identity = cursor.get("table_identity", {})
        rtti = cursor.get("rtti", {})
        rtti_class = table_identity.get("RTTI") or rtti.get("class") or rtti.get("RTTI")
        if not server.get("present"):
            raise CheckFailure(f"server archive observation missing for {spec['code']}")
        if len(l3_fields) != spec["expected_l3"] or len(held_fields) != spec["expected_held"]:
            raise CheckFailure(f"{spec['code']} field counts differ: L3={len(l3_fields)}, held={len(held_fields)}")
        if server["row_count"] != server["header_record_count"]:
            raise CheckFailure(f"{spec['code']} row count does not match its cursor header")
        if not server["closure_ok"] or server["row_stream_prefix_bytes"] != 13 or server["footer_bytes"] != 9:
            raise CheckFailure(f"{spec['code']} server payload closure failed")
        if spec["task"] == "t27" and (not client.get("closure_ok") or client.get("row_count") != server.get("row_count")):
            raise CheckFailure("Cstc client identity archive closure failed")
        if spec["task"] != "t27" and client.get("present"):
            raise CheckFailure(f"unexpected client table for {spec['code']}")
        source_summary_keys = ["status", "baseline_L3", "L3", "L4", "occurrences", "fields_named", "schema_occurrences", "unpromoted_count_by_grade", "offset_origin", "negative_policy"]
        source_summary = {key: ledger[key] for key in source_summary_keys if key in ledger}
        if int(ledger.get("L4", 0) or 0) != 0:
            raise CheckFailure(f"unexpected L4 evidence in {spec['task']}")
        table = {
            "entity": "club",
            "parent_xml": "club.xml",
            "parent_code": spec["code"],
            "table_type": spec["table_type"],
            "rtti_class": rtti_class,
            "source_task": spec["task"],
            "schema_scope": ledger.get("scope", ["club.xml", spec["code"]]),
            "source_ledger_summary": source_summary,
            "server_payload": server,
            "client_observation": client,
            "coordinate_policy": spec["coordinates"],
            "reference_domains": ledger.get("reference_domains", ledger.get("reference_domain")),
            "fields": sorted(l3_fields, key=lambda f: (f["row_offset"] is None, f["row_offset"] if f["row_offset"] is not None else 10**9, f["code"] or "")),
            "held_fields": sorted(held_fields, key=lambda f: (f["code"] or "")),
            "excluded_non_business_records": non_business,
            "source_artifacts": table_paths,
            "supplemental_evidence": {
                key: ledger[key] for key in ("age_relationship", "rejected_record_pair", "unscoped_references", "unscoped_properties_bytes", "negative_policy") if key in ledger
            },
        }
        if spec["task"] == "t27":
            table["identity_transfer"] = cursor.get("bulk")
            negatives.extend(ledger.get("negative_regressions", []))
        tables.append(table)
    nation_inventory = read_json("scratch/t37/out/nation_subtable_inventory.json")
    nation_summary = nation_inventory.get("summary", {})
    nation_coverage = {
        "inventory_path": "scratch/t37/out/nation_subtable_inventory.json",
        "inventory_status": nation_inventory.get("status"),
        "summary": nation_summary,
        "conclusion": "No accepted nation-child L3 field ledger is included. The partial t37 inventory is retained as context, not promoted into schema claims.",
    }
    schema = {
        "schema_id": "fm24.club_nation_subtable_schema",
        "schema_version": 1,
        "generated_by": "t40",
        "evidence_grade_policy": "Only accepted source-ledger L3 rows are in fields. Held rows, exclusions, and negative regressions remain separate. L4=0.",
        "binary_provenance": binary,
        "coverage": {
            "club_tables": len(tables),
            "club_L3_fields": sum(len(table["fields"]) for table in tables),
            "held_fields": sum(len(table["held_fields"]) for table in tables),
            "negative_regressions": len(negatives),
            "L4": 0,
            "nation_side": nation_coverage,
            "cross_archive_offset_inference": "not performed; all business-field sink evidence in this consolidation is server-side. Cstc client table 22 carries identity only; the other five client table entries are absent.",
        },
        "inventory_reconciliation": {
            "club_inventory": "scratch/t29/out/subtable_inventory.json is context only. Where t29 lists Cmti/CNtp/Cdbt item candidates at candidate/L2, the accepted t32/t34/t36 L3 ledgers take precedence for this consolidation.",
            "nation_inventory": "t37 is partial and reports zero new L3 claims; no nation child fields are promoted here.",
        },
        "source_artifacts": artifacts,
        "tables": tables,
        "negative_regressions": negatives,
    }
    return schema


def sentinel_reference(field: dict[str, Any]) -> str:
    raw = field["provenance"]["source_record"]
    domain = field.get("domain") if isinstance(field.get("domain"), dict) else {}
    schema = field.get("schema") if isinstance(field.get("schema"), dict) else {}
    profile = field.get("profile")
    if isinstance(profile, list):
        profile = profile[0] if profile else {}
    profile = profile if isinstance(profile, dict) else {}
    ref = domain.get("target") or domain.get("target_ordinal") or schema.get("database_table_type")
    if not ref:
        occurrences = raw.get("schema_occurrences") or []
        if occurrences:
            ref = occurrences[0].get("database_table_type")
    sentinels: list[str] = []
    if domain.get("native_null") is not None:
        sentinels.append(f"native null {domain['native_null']}")
    if domain.get("constructor_default") is not None:
        sentinels.append(f"default {domain['constructor_default']}")
    if domain.get("zero_sentinel"):
        sentinels.append(str(domain["zero_sentinel"]))
    specials = domain.get("native_specials")
    if isinstance(specials, dict):
        sentinels.extend(f"{key}: {value}" for key, value in specials.items())
    sentinel_count = profile.get("sentinel_count", 0) or 0
    if profile.get("sentinel") is not None:
        sentinels.append(f"{profile['sentinel']} ({sentinel_count} rows)")
    elif profile.get("sentinel_ff", 0) > 0:
        sentinels.append(f"-1 ({profile['sentinel_ff']} rows)")
    parts = []
    if ref:
        parts.append(f"schema target {ref}")
    if sentinels:
        parts.append("sentinel/special: " + "; ".join(sentinels))
    return "; ".join(parts) if parts else "no sentinel recorded"


def domain_profile_summary(field: dict[str, Any]) -> str:
    raw = field["provenance"]["source_record"]
    domain = field.get("domain") if isinstance(field.get("domain"), dict) else {}
    schema = field.get("schema") if isinstance(field.get("schema"), dict) else {}
    profile = field.get("profile")
    if isinstance(profile, list):
        profile = profile[0] if profile else {}
    profile = profile if isinstance(profile, dict) else {}
    parts = [sentinel_reference(field)]
    bounds = domain.get("xml_bounds") or domain.get("bounds")
    if bounds is None and schema.get("min_value") is not None and schema.get("max_value") is not None:
        bounds = [schema.get("min_value"), schema.get("max_value")]
    if bounds is not None:
        parts.append(f"declared {bounds}")
    if domain.get("frozen_enum"):
        parts.append(f"enum {domain['frozen_enum']} values {domain.get('values', [])}")
    if domain.get("native_signed_bounds") is not None:
        parts.append(f"native signed bounds {domain['native_signed_bounds']}")
    if domain.get("list_excluded_for_R8D_zero") is not None:
        parts.append(f"collection excludes R8D zero {domain['list_excluded_for_R8D_zero']}")
    if domain.get("mask") is not None:
        parts.append(f"bit mask {domain['mask']}")
    if domain.get("key_basis"):
        parts.append(f"key basis: {domain['key_basis']}")
    low = profile.get("min_signed", profile.get("min"))
    high = profile.get("max_signed", profile.get("max"))
    if low is not None and high is not None:
        distinct = profile.get("distinct")
        suffix = f", {distinct} distinct" if distinct is not None else ""
        label = "packed value observed" if profile.get("packed") or field.get("interpretation") == "packed_u16_day_year" else "observed"
        parts.append(f"{label} {low}..{high}{suffix}")
    packed = profile.get("packed") if isinstance(profile.get("packed"), dict) else profile
    if packed.get("year_min") is not None and packed.get("year_max") is not None:
        year_distinct = packed.get("year_distinct")
        suffix = f", {year_distinct} distinct years" if year_distinct is not None else ""
        parts.append(f"packed years {packed['year_min']}..{packed['year_max']}{suffix}")
    if packed.get("day_min") is not None and packed.get("day_max") is not None:
        parts.append(f"days {packed['day_min']}..{packed['day_max']}")
    elif packed.get("day_max") is not None:
        parts.append(f"maximum day {packed['day_max']}")
    histogram = profile.get("histogram")
    if isinstance(histogram, dict) and len(histogram) <= 24:
        parts.append("observed values " + ", ".join(sorted(histogram, key=lambda x: int(x))))
    frequency = profile.get("top_signed_freq")
    if isinstance(frequency, list) and frequency and len(frequency) <= 12:
        parts.append("top raw value counts " + ", ".join(f"{value}={count}" for value, count in frequency))
    live_bounds = profile.get("live_bounds_from_UI")
    if live_bounds is not None:
        parts.append(f"UI-derived live bounds {live_bounds}")
    decoded = raw.get("data_profile", {}).get("decoded_counts") if isinstance(raw.get("data_profile"), dict) else None
    if decoded:
        parts.append(f"decoded counts {decoded}")
    caveat = profile.get("ui_dependency_caveat") or (raw.get("data_profile") or {}).get("ui_dependency_caveat")
    if isinstance(caveat, dict):
        parts.append(f"UI caveat: schema type {caveat.get('schema_type')} -> non-null type {caveat.get('observed_type_with_non_null_values')}; storage only, no UI equivalence")
    elif caveat:
        parts.append(f"UI caveat {caveat}")
    return "; ".join(dict.fromkeys(parts))


def md_escape(value: Any) -> str:
    if value is None:
        return "-"
    text = str(value).replace("|", "\\|").replace("\n", " ")
    return text


def field_table_rows(table: dict[str, Any]) -> list[str]:
    rows = []
    for field in table["fields"]:
        coords = field.get("coordinates", [])
        if field.get("row_offset") is not None:
            offset = f"row {field['row_offset']} / wire {field.get('wire_offset')}"
        elif coords:
            offset = "; ".join(f"row {c.get('row_offset') if c.get('row_offset') is not None else 'n/a'} / wire {c.get('wire_offset')}" for c in coords)
        else:
            offset = "contextual"
        sinks = ", ".join(s.get("VA") or "VA missing" for s in field["provenance"]["reader_transfer_sites"]) or "-"
        getters = ", ".join(s.get("VA") or "VA missing" for s in field["provenance"]["getter_accesses"]) or "-"
        rows.append("| " + " | ".join([
            f"`{table['parent_code']}.{field['code']}`",
            md_escape(field.get("name")),
            md_escape(offset),
            md_escape(field.get("width_bytes")),
            md_escape(field.get("interpretation")),
            md_escape(domain_profile_summary(field)),
            md_escape(field.get("grade")),
            md_escape(sinks),
            md_escape(getters),
        ]) + " |")
    return rows


def markdown_report(schema: dict[str, Any]) -> str:
    lines = [
        "# Club/Nation Subtable Schema",
        "",
        "Generated by t40 from six accepted field ledgers. This is a consolidation of existing evidence; cursor extraction and payload/EXE parsing were not rerun.",
        "",
        "## Coverage",
        "",
        f"- Club tables: {schema['coverage']['club_tables']}",
        f"- Accepted L3 business fields: {schema['coverage']['club_L3_fields']}",
        f"- Held fields: {schema['coverage']['held_fields']}",
        f"- Original negative regressions retained separately: {schema['coverage']['negative_regressions']}",
        "- L4: 0",
        "- Nation side: partial t37 inventory only; no accepted nation-child L3 field ledger is included.",
        "- All business-field sink evidence is server-side. No cross-archive offset inference is made. Cstc client table 22 is identity-only; client entries for the other five tables are absent.",
        "",
        "Business identity lanes are not promoted as foreign keys. In particular, the Cstc identity transfer is retained as transport evidence and does not establish a stadium/club relation.",
        "",
        "## Tables",
        "",
        "| Parent/table | Type | RTTI | Rows | Stride | Payload bytes | Payload SHA-256 | Closure |",
        "|---|---:|---|---:|---:|---:|---|---|",
    ]
    for table in schema["tables"]:
        payload = table["server_payload"]
        lines.append("| " + " | ".join([
            f"`{table['parent_xml']}:{table['parent_code']}`",
            str(table["table_type"]),
            md_escape(table.get("rtti_class")),
            str(payload["row_count"]),
            str(payload["stride_bytes"]),
            str(payload["payload_len"]),
            f"`{payload['payload_sha256']}`",
            f"`{payload['closure_formula']}`",
        ]) + " |")
    lines.extend(["", "Every server row stream closes as `prefix + count * stride + footer = payload_len`; the source cursors report a 13-byte prefix and 9-byte footer for all six tables.", ""])
    for table in schema["tables"]:
        lines.extend([
            f"## {table['parent_code']}",
            "",
            f"Source task `{table['source_task']}`; `table_type={table['table_type']}`; RTTI `{table.get('rtti_class')}`.",
            "",
            table["coordinate_policy"],
            "",
            "| Field | Name | Offset | Width | Type/interpretation | Domain, reference, sentinel, profile | Grade | Reader VA | Getter VA |",
            "|---|---|---|---:|---|---|---|---|---|",
            *field_table_rows(table),
            "",
        ])
        if table["held_fields"]:
            lines.extend([
                f"### Held in {table['parent_code']}",
                "",
                "| Field | Grade | Candidate coordinate | Preserved reason / first counterexample |",
                "|---|---|---|---|",
            ])
            for field in table["held_fields"]:
                coords = field.get("coordinates", [])
                coord = "; ".join(f"row {c.get('row_offset') if c.get('row_offset') is not None else 'n/a'} / wire {c.get('wire_offset')}" for c in coords) or "not promoted"
                lines.append("| " + " | ".join([
                    f"`{field['code']}`",
                    md_escape(field.get("grade")),
                    md_escape(coord),
                    md_escape(field.get("held_reason")),
                ]) + " |")
            lines.append("")
        if table.get("excluded_non_business_records"):
            lines.extend(["Non-business slots are preserved separately and excluded from L3/held counts:", ""])
            for record in table["excluded_non_business_records"]:
                lines.append(f"- wire offset `{record['wire_offset']}`, width `{record['width_bytes']}`: {md_escape(record.get('disposition'))}")
            lines.append("")
        if table.get("identity_transfer"):
            ident = table["identity_transfer"]
            lines.extend([
                "Cstc identity transport: server row offset `66` to client row offset `0`, width `12`, exact matches `449/449`; it is not counted as a nested business field and does not establish a foreign key.",
                "",
            ])
        if table.get("reference_domains"):
            lines.extend(["Reference-domain evidence is preserved verbatim in the JSON `reference_domains` member; schema-declared targets are not extended beyond that evidence.", ""])
    lines.extend([
        "## Negative Regressions",
        "",
        "The four t20 linear-coordinate negatives are retained as source labels; they are not additional fields and are not rewritten as positive claims.",
        "",
        "| Code | t20 row offset | Original status |",
        "|---|---:|---|",
    ])
    for item in schema["negative_regressions"]:
        lines.append(f"| `{item['code']}` | {item['t20_row_offset']} | `{item['status']}` |")
    lines.extend([
        "",
        "## Method and Limits",
        "",
        "- L3 means the accepted source task tied the named schema field to an executable row coordinate/getter and retained its value profile. It does not imply a user-interface edit was tested.",
        "- Table framing is copied from the accepted cursor records and checked arithmetically; this consolidation does not decode payload bytes.",
        "- t29 inventory is context only. For Cmti, CNtp, and Cdbt, accepted t32/t34/t36 field-ledger findings take precedence over earlier candidate/L2 labels.",
        "- Held rows remain held, including Cstc code-row-only/profile-conflict records, Clhs and CNtp profile conflicts, and Cmti `icom` without an independent wire sink.",
        "- Binary provenance is tied to the manifested `evidence/fm24` IDA provenance snapshot; the external executable was not read.",
        "",
        f"Source editor.exe SHA-256: `{BINARY_SHA256}`. L4 evidence: `0`.",
        "",
    ])
    return "\n".join(lines)


def validate_schema(schema: dict[str, Any]) -> None:
    tables = schema.get("tables", [])
    if len(tables) != 6:
        raise CheckFailure(f"expected 6 tables, got {len(tables)}")
    l3_count = sum(len(table.get("fields", [])) for table in tables)
    held_count = sum(len(table.get("held_fields", [])) for table in tables)
    if l3_count != 44:
        raise CheckFailure(f"expected 44 L3 fields, got {l3_count}")
    if held_count != 13:
        raise CheckFailure(f"expected 13 held fields, got {held_count}")
    if len(schema.get("negative_regressions", [])) != 4:
        raise CheckFailure("expected the four original t27 negative regressions")
    if schema.get("coverage", {}).get("L4") != 0:
        raise CheckFailure("L4 must remain zero")
    known_artifacts = {artifact.get("path") for artifact in schema.get("source_artifacts", [])}
    for table in tables:
        layout = table.get("server_payload", {})
        if not layout.get("closure_ok") or layout.get("closure_formula") is None:
            raise CheckFailure(f"{table.get('parent_code')} closure is not self-consistent")
        if not re.fullmatch(r"[0-9a-f]{64}", layout.get("payload_sha256", "")):
            raise CheckFailure(f"{table.get('parent_code')} has no payload SHA-256")
        for field in table.get("fields", []) + table.get("held_fields", []):
            provenance = field.get("provenance", {})
            if provenance.get("binary_sha256") != BINARY_SHA256 or not provenance.get("source_record_sha256"):
                raise CheckFailure(f"incomplete source provenance for {table['parent_code']}.{field.get('code')}")
            if any(path not in known_artifacts for path in provenance.get("source_files", [])):
                raise CheckFailure(f"unregistered source artifact for {table['parent_code']}.{field.get('code')}")
            if field.get("status") == "L3":
                sinks = provenance.get("reader_transfer_sites", [])
                getters = provenance.get("getter_accesses", [])
                if not sinks or not all(site.get("VA") for site in sinks):
                    raise CheckFailure(f"missing reader VA for L3 {table['parent_code']}.{field.get('code')}")
                if not getters or not all(site.get("VA") for site in getters):
                    raise CheckFailure(f"missing getter VA for L3 {table['parent_code']}.{field.get('code')}")
    client = next(table for table in tables if table["parent_code"] == "Cstc")["client_observation"]
    if not client.get("closure_ok") or client.get("stride_bytes") != 13:
        raise CheckFailure("Cstc client identity-only archive closure failed")


def selftest() -> dict[str, Any]:
    schema = build_schema()
    validate_schema(schema)
    report = markdown_report(schema)
    for table in schema["tables"]:
        for field in table["fields"]:
            marker = f"`{table['parent_code']}.{field['code']}`"
            if marker not in report:
                raise CheckFailure(f"markdown field missing: {marker}")
    if "Held in Cstc" not in report or "Negative Regressions" not in report:
        raise CheckFailure("markdown held/negative sections are missing")
    return schema


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Consolidate accepted t27/t30/t31/t32/t34/t36 club-subtable L3 ledgers.")
    parser.add_argument("--selftest", action="store_true", help="build in memory and check counts, provenance, and closure arithmetic")
    parser.add_argument("--force", action="store_true", help="replace the two generated reports if they already exist")
    args = parser.parse_args(argv)
    try:
        schema = selftest()
        if args.selftest:
            print("SELFTEST PASS: 6 tables, 44 L3, 13 held, 4 negatives, L4=0; provenance and closures complete")
            return 0
        if not args.force and (OUT_JSON.exists() or OUT_MD.exists()):
            raise CheckFailure("report output already exists; pass --force only to replace these generated files")
        json_text = json.dumps(schema, ensure_ascii=False, indent=2) + "\n"
        md_text = markdown_report(schema)
        OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
        OUT_JSON.write_text(json_text, encoding="utf-8", newline="\n")
        OUT_MD.write_text(md_text, encoding="utf-8", newline="\n")
        print(f"WROTE {OUT_JSON.relative_to(ROOT)}")
        print(f"WROTE {OUT_MD.relative_to(ROOT)}")
        return 0
    except CheckFailure as exc:
        print(f"CHECK FAILED: {exc}", file=sys.stderr)
        return 1
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"FATAL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
