#!/usr/bin/env python3
"""Incrementally append accepted t39 Tchl evidence to the t40 schema."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
OUT_JSON = ROOT / "reports" / "club_nation_subtable_schema.json"
OUT_MD = ROOT / "reports" / "club_nation_subtable_schema.md"
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
TCHL_FIELDS_PATH = "scratch/t39/out/fields_tchl.json"
TCHL_CURSOR_PATH = "scratch/t39/out/cursor_tchl.json"
TCHL_REPORT_PATH = "scratch/t39/out/REPORT.md"


class CheckFailure(Exception):
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


def load_v1_baseline() -> tuple[dict[str, Any], str]:
    if V1_JSON_SNAPSHOT.exists():
        raw = V1_JSON_SNAPSHOT.read_bytes()
    else:
        raw = OUT_JSON.read_bytes()
    if sha256_bytes(raw) != V1_JSON_SHA256:
        raise CheckFailure("t40 schema baseline SHA-256 differs from the accepted v1 input")
    baseline = json.loads(raw.decode("utf-8"))
    if baseline.get("schema_version") != 1 or baseline.get("generated_by") != "t40":
        raise CheckFailure("expected the accepted t40 schema v1 baseline")
    return baseline, raw.decode("utf-8")


def load_v1_markdown() -> str:
    raw = V1_MD_SNAPSHOT.read_bytes() if V1_MD_SNAPSHOT.exists() else OUT_MD.read_bytes()
    if sha256_bytes(raw) != V1_MD_SHA256:
        raise CheckFailure("t40 Markdown baseline SHA-256 differs from the accepted v1 input")
    return raw.decode("utf-8")


def t39_paths(cursor: dict[str, Any]) -> list[str]:
    paths = [TCHL_FIELDS_PATH, TCHL_CURSOR_PATH, TCHL_REPORT_PATH]
    paths.extend(f"scratch/t39/out/{name}" for name in cursor.get("instruction_shards", []))
    paths.extend(f"scratch/t39/out/{name}" for name in cursor.get("branch_shards", []))
    if len(paths) != len(set(paths)):
        raise CheckFailure("duplicate t39 source artifact path")
    for path in paths:
        if not rel(path).is_file():
            raise CheckFailure(f"missing t39 source artifact {path}")
    return paths


def load_instruction_index(cursor: dict[str, Any]) -> dict[int, dict[str, Any]]:
    result: dict[int, dict[str, Any]] = {}
    for name in cursor.get("instruction_shards", []):
        shard = read_json(rel(f"scratch/t39/out/{name}"))
        for instruction in shard.get("instructions", []):
            offset = as_int(instruction.get("file_offset"))
            if offset is None:
                continue
            previous = result.get(offset)
            if previous is not None and previous.get("VA") != instruction.get("VA"):
                raise CheckFailure(f"conflicting instruction VA at {name}:{instruction.get('file_offset')}")
            result[offset] = instruction
    return result


def schema_index(record: dict[str, Any]) -> int:
    for occurrence in record.get("scoped_occurrences", []):
        if len(occurrence) >= 3 and occurrence[0] == "club.xml" and occurrence[1] == "Tchl":
            return int(occurrence[2])
    raise CheckFailure(f"missing club.xml/Tchl schema index for {record.get('code')}")


def make_reader_sites(record: dict[str, Any], instruction_index: dict[int, dict[str, Any]]) -> list[dict[str, Any]]:
    result = []
    for sink in record.get("sinks", []):
        offset = as_int(sink.get("site"))
        instruction = instruction_index.get(offset) if offset is not None else None
        if instruction is None or not instruction.get("VA"):
            raise CheckFailure(f"missing reader instruction VA for {record.get('code')} sink {sink.get('site')}")
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


def make_getter_sites(record: dict[str, Any], instruction_index: dict[int, dict[str, Any]]) -> list[dict[str, Any]]:
    getter = record.get("getter") or {}
    object_offsets = getter.get("object_offsets", [])
    selected: dict[int, tuple[int, dict[str, Any]]] = {}
    for offset in getter.get("evidence", []):
        instruction = instruction_index.get(offset)
        if not instruction:
            continue
        text = instruction.get("instruction", "")
        for object_offset in object_offsets:
            pattern = rf"\[rcx \+ 0x{int(object_offset):x}\]"
            if re.search(pattern, text, re.IGNORECASE):
                selected.setdefault(int(object_offset), (offset, instruction))
    if not selected and getter.get("load") is not None:
        offset = as_int(getter.get("load"))
        instruction = instruction_index.get(offset) if offset is not None else None
        if instruction:
            object_offset = object_offsets[0] if object_offsets else None
            selected[object_offset if object_offset is not None else -1] = (offset, instruction)
    if object_offsets and set(selected) != {int(value) for value in object_offsets}:
        raise CheckFailure(f"getter object offsets lack explicit access instructions for {record.get('code')}")
    return [{
        "role": "static_getter_access",
        "file_offset": hex_offset(offset),
        "VA": instruction.get("VA"),
        "instruction": instruction.get("instruction"),
        "object_offset": object_offset if object_offset >= 0 else None,
    } for object_offset, (offset, instruction) in sorted(selected.items())]


def held_reason(record: dict[str, Any]) -> str:
    profile = record.get("profile", {})
    domain = record.get("domain", {})
    violation = profile.get("first_violation", {})
    coordinates = violation.get("coordinates", [])
    coordinate = coordinates[0] if coordinates else {}
    code = record.get("code")
    if code not in {"styr", "edyr"}:
        raise CheckFailure(f"unexpected held Tchl field {code}")
    return (
        f"u16_year_integer; {profile.get('zero_count')} zero values conflict with frozen XML "
        f"{domain.get('xml_bounds')}; first counterexample row {violation.get('row')} "
        f"@{coordinate.get('offset')}: {coordinate.get('hex')}"
    )


def make_tchl_field(
    record: dict[str, Any], category: str, source_paths: list[str],
    instruction_index: dict[int, dict[str, Any]], reader_extent: dict[str, Any],
) -> dict[str, Any]:
    coordinates = [{
        "row_offset": sink.get("legacy_offset"),
        "wire_offset": sink.get("wire_offset"),
        "width_bytes": sink.get("width"),
    } for sink in record.get("sinks", [])]
    widths = [item["width_bytes"] for item in coordinates if isinstance(item.get("width_bytes"), int)]
    width_bytes = sum(widths) if widths else None
    schema = deepcopy(record.get("schema", {}))
    schema["idx"] = schema_index(record)
    name = record.get("name") or schema.get("name")
    # T39 stores the static reader transfer sites as file offsets in sinks[].site.
    return {
        "code": record.get("code"),
        "name": name,
        "status": category,
        "grade": record.get("grade"),
        "row_offset": record.get("row_offset"),
        "wire_offset": record.get("wire_offset"),
        "coordinates": coordinates,
        "coordinate_note": "t39 row_offset is body-relative; wire_offset includes the one-byte selector (wire_offset = row_offset + 1). Compound dbrt retains both one-byte lanes; held year fields retain candidate coordinates without promotion.",
        "width_bytes": width_bytes,
        "interpretation": record.get("interpretation"),
        "schema": schema,
        "domain": deepcopy(record.get("domain")),
        "profile": deepcopy(record.get("profile")),
        "held_reason": held_reason(record) if category == "held" else None,
        "provenance": {
            "task": "t39",
            "field_ledger": TCHL_FIELDS_PATH,
            "source_files": list(source_paths),
            "source_record_sha256": canonical_sha256(record),
            "binary": "editor.exe",
            "binary_sha256": BINARY_SHA256,
            "reader_extent": deepcopy(reader_extent),
            "reader_transfer_sites": make_reader_sites(record, instruction_index),
            "getter_accesses": make_getter_sites(record, instruction_index),
            "source_record": deepcopy(record),
        },
    }


def make_tchl_table(ledger: dict[str, Any], cursor: dict[str, Any], source_paths: list[str]) -> dict[str, Any]:
    server = cursor["archives"]["server"]
    entry = server["entry"]
    selected = server["selected_frame"]
    reader = cursor["reader"]
    instruction_index = load_instruction_index(cursor)
    reader_extent = {
        "start_file_offset": hex_offset(reader["entry"]),
        "end_file_offset_exclusive": hex_offset(reader["end_exclusive"]),
        "start_VA": reader["entry_VA"],
        "end_VA_exclusive": reader["end_VA"],
        "extent_source": reader["extent_source"],
    }
    count = int(server["row_count"])
    stride = int(server["stride"])
    payload_len = int(server["payload_bytes"])
    footer_start = int(server["wire_footer_offset"])
    footer_bytes = payload_len - footer_start
    prefix = footer_start - count * stride
    header_hex = server["header_hex"]
    header = bytes.fromhex(header_hex)
    header_count = int.from_bytes(header[8:12], "little")
    closure_ok = prefix + count * stride + footer_bytes == payload_len
    if not closure_ok or prefix != 13 or footer_bytes != 9 or header_count != count:
        raise CheckFailure("t39 Tchl server framing/header does not close")
    if selected.get("sha256") != server.get("payload_sha256"):
        raise CheckFailure("selected Tchl frame payload SHA differs from cursor payload SHA")

    fields = []
    held = []
    for record in ledger.get("fields", []):
        if record.get("grade") == "L3_table34_named_coordinate":
            fields.append(make_tchl_field(record, "L3", source_paths, instruction_index, reader_extent))
        elif record.get("grade") == "L3_table34_named_compound_coordinate":
            fields.append(make_tchl_field(record, "L3", source_paths, instruction_index, reader_extent))
        elif record.get("grade") == "held_domain_conflict":
            held.append(make_tchl_field(record, "held", source_paths, instruction_index, reader_extent))
        else:
            raise CheckFailure(f"unclassified t39 field {record.get('code')} grade {record.get('grade')}")

    owner = deepcopy(ledger["unscoped_owner"])
    owner_profile = owner["profile"]
    reference_domains = {
        "ordinal_target_domains": deepcopy(ledger["target_domains"]),
        "shared_owner_domain": {
            "source": TCHL_FIELDS_PATH,
            "source_record": owner,
            "target_table_type": owner["domain"]["target_table"],
            "owner_encoding": owner["interpretation"],
            "nonnull_owner_count": owner_profile["matches"],
            "null_owner_count": owner_profile["null_count"],
            "target_selector_counts": owner_profile["target_selector_histogram"],
            "nonempty_owner_target": "table24 selector11 NATIONAL_TEAM",
            "club_exclusive_L3": ledger["club_exclusive_L3"],
            "exclusivity_basis": "owner ordinal lookup joined to table24 selector and NATIONAL_TEAM factory arm; entity_tag is not used as an exclusivity criterion",
            "scope_note": "Tchl dispatch is shared by club/nation; this table is not a club-exclusive field claim.",
        },
    }
    def coordinate_order(field: dict[str, Any]) -> tuple[int, str]:
        offsets = [item.get("row_offset") for item in field.get("coordinates", []) if isinstance(item.get("row_offset"), int)]
        return (min(offsets) if offsets else 10**9, field.get("code") or "")

    return {
        "entity": "club_nation_shared",
        "parent_xml": "club.xml + nation.xml",
        "parent_code": "Tchl",
        "table_type": int(cursor["table_type"]),
        "rtti_class": cursor["rtti"]["class"],
        "source_task": "t39",
        "schema_scope": deepcopy(ledger["scope"]),
        "source_ledger_summary": {
            "status": "accepted_by_E78",
            "occurrences": ledger.get("occurrences"),
            "fields_named": len(ledger.get("fields", [])),
            "L3": ledger.get("L3"),
            "held": sum(item["status"] == "held" for item in held),
            "club_exclusive_L3": ledger.get("club_exclusive_L3"),
            "L4": ledger.get("L4"),
            "offset_origin": "row_offset is body-relative; wire_offset includes the selector byte",
        },
        "server_payload": {
            "archive": "server",
            "present": True,
            "path": entry["path"],
            "row_count": count,
            "stride_bytes": stride,
            "payload_len": payload_len,
            "payload_sha256": server["payload_sha256"],
            "header_hex": header_hex,
            "header_record_count": header_count,
            "row_stream_prefix_bytes": prefix,
            "selector_bytes_per_row": 1,
            "row_body_bytes": stride - 1,
            "wire_footer_start": footer_start,
            "footer_hex": server["wire_footer_hex"],
            "footer_bytes": footer_bytes,
            "closure_formula": f"{prefix} + {count} * {stride} + {footer_bytes} = {payload_len}",
            "closure_ok": closure_ok,
            "legacy_row_origin": server["legacy_origin"],
            "wire_row_origin": server["wire_origin"],
            "legacy_footer_start": server["legacy_footer_offset"],
            "legacy_footer_hex": server["legacy_footer_hex"],
            "archive_member_offset": entry["offset"],
            "archive_member_packed_size": entry["packed_size"],
            "selected_frame_offset": selected["offset"],
            "selected_frame_packed_size": selected["compressed_bytes"],
        },
        "client_observation": {
            "archive": "client",
            "present": False,
            "directory_entry_count": cursor["archives"]["client"]["directory_entry_count"],
            "table_entry_absent": True,
        },
        "coordinate_policy": "Tchl t39 row_offset is body-relative; wire_offset includes the one-byte selector (wire_offset = row_offset + 1). Candidate/held coordinates are kept distinct from promoted row_offset; dbrt has two one-byte lanes.",
        "reference_domains": reference_domains,
        "reader_extent": reader_extent,
        "source_acceptance": {"ledger_path": LEDGER_PATH, "entry_id": "E78", "level": "L3", "kind": "acceptance"},
        "fields": sorted(fields, key=coordinate_order),
        "held_fields": sorted(held, key=coordinate_order),
        "excluded_non_business_records": [],
        "source_artifacts": list(source_paths),
        "supplemental_evidence": {
            "shared_dispatch_and_owner_scope": "t39 REPORT.md; 7,084 nonempty owner ordinals resolve to table24 selector11 NATIONAL_TEAM; 31 owners are null; club-exclusive L3=0.",
            "target_domains": "t39 fields_tchl.json; ordinal target witnesses for table types 23, 24, and 25 are retained under reference_domains.ordinal_target_domains.",
        },
    }


def schema_provenance() -> dict[str, Any]:
    master = rel(MASTER_PATH)
    manifest_path = rel(MANIFEST_PATH)
    manifest = read_json(manifest_path)
    entries = [item for item in manifest.get("files", []) if item.get("path") == MASTER_PATH]
    if len(entries) != 1:
        raise CheckFailure(f"expected one MANIFEST entry for {MASTER_PATH}, found {len(entries)}")
    entry = entries[0]
    master_sha = sha256_file(master)
    manifest_sha = sha256_file(manifest_path)
    if master_sha != MASTER_SHA256 or entry.get("sha256") != master_sha or entry.get("bytes") != master.stat().st_size:
        raise CheckFailure("master.json does not match its frozen MANIFEST entry")
    ledger = read_json(LEDGER_PATH)
    accepted = {item.get("id"): item for item in ledger.get("entries", []) if item.get("id") in {"E78", "E79"}}
    if set(accepted) != {"E78", "E79"}:
        raise CheckFailure("expected t39 E78 and t40 E79 acceptance records")
    if accepted["E78"].get("kind") != "acceptance" or accepted["E79"].get("kind") != "acceptance_with_note":
        raise CheckFailure("task acceptance ledger kinds differ from E78/E79")
    return {
        "master_json_path": MASTER_PATH,
        "master_json_sha256": master_sha,
        "master_json_bytes": master.stat().st_size,
        "manifest_path": MANIFEST_PATH,
        "manifest_sha256": manifest_sha,
        "manifest_entry_sha256": entry["sha256"],
        "manifest_entry_bytes": entry["bytes"],
        "manifest_match": True,
        "snapshot_date": manifest.get("snapshot_date"),
        "acceptance_ledger": {
            "path": LEDGER_PATH,
            "v1_acceptance_entry": "E79",
            "tchl_acceptance_entry": "E78",
        },
    }


def build_schema(baseline: dict[str, Any]) -> dict[str, Any]:
    ledger = read_json(TCHL_FIELDS_PATH)
    cursor = read_json(TCHL_CURSOR_PATH)
    paths = t39_paths(cursor)
    table = make_tchl_table(ledger, cursor, paths)
    schema = deepcopy(baseline)
    schema["schema_version"] = 2
    schema["generated_by"] = "t42"
    schema["schema_provenance"] = schema_provenance()
    artifacts = list(schema["source_artifacts"])
    known = {item["path"] for item in artifacts}
    additions = [*paths, MASTER_PATH, LEDGER_PATH]
    for path in additions:
        if path not in known:
            source = rel(path)
            artifacts.append({"path": path, "sha256": sha256_file(source), "bytes": source.stat().st_size})
            known.add(path)
    schema["source_artifacts"] = artifacts
    schema["tables"].append(table)
    coverage = schema["coverage"]
    coverage.update({
        "club_tables": 7,
        "club_L3_fields": 51,
        "held_fields": 15,
        "negative_regressions": 4,
        "L4": 0,
        "cross_archive_offset_inference": "not performed; accepted business-field sink evidence remains server-side. Cstc client table 22 carries identity only; the other six client table entries, including shared Tchl table 34, are absent. Tchl table ordinals retain separate t39 target-domain witnesses.",
    })
    coverage["nation_side"]["conclusion"] = (
        "The t37 nation inventory remains partial with zero new nation-exclusive L3 claims. "
        "Accepted shared Tchl/table 34 fields are recorded separately and are not promoted as nation-only or club-only claims."
    )
    schema["inventory_reconciliation"]["tchl_shared_scope"] = (
        "t39 E78 establishes shared club/nation dispatch and table24 selector11 NATIONAL_TEAM ownership for all 7,084 nonempty owners; club-exclusive L3=0. The entity_tag label is not used as an exclusivity test."
    )
    return schema


def tchl_markdown(table: dict[str, Any]) -> str:
    payload = table["server_payload"]
    lines = [
        "## Tchl",
        "",
        f"Source task `{table['source_task']}`; `table_type={table['table_type']}`; RTTI `{table['rtti_class']}`. Shared club/nation editor scope; this is not a club-exclusive field claim.",
        "",
        table["coordinate_policy"],
        "",
        f"Server payload: `{payload['row_count']}` rows x `{payload['stride_bytes']}` B; `{payload['payload_len']}` B; SHA-256 `{payload['payload_sha256']}`; closure `{payload['closure_formula']}`. Client table 34 is absent (31 client directory entries).",
        "",
        "Reader extent: file offsets `0x43a6890..0x43a6a6f` (end exclusive), VA `0x144511e90..0x14451206f` (end exclusive). Per-field reader transfer VAs and getter accesses are in JSON provenance.",
        "",
        "Owner scope: all 7,084 nonempty owner ordinals resolve to table 24 selector 11 `NATIONAL_TEAM`; 31 owner values are null. Club-exclusive L3 is 0. This conclusion uses the owner ordinal/selector and factory-arm evidence, not `entity_tag`.",
        "",
        "Target ordinal domains consumed by Tchl are retained in JSON `reference_domains`: competition/table 25, stage_name/table 23, and team/table 24. These are t39 empirical identity witnesses, not UID reinterpretations.",
        "",
        "| Field | Name | Offset | Width | Type/interpretation | Data/domain evidence | Grade | Reader VA | Getter VA |",
        "|---|---|---|---:|---|---|---|---|---|",
    ]
    summaries = {
        "tchc": "table 25 ordinal; 7,084 joins, 31 null; row 0 raw 637 resolves to target identity 1,301,390",
        "mstn": "stage_name/table 23 ordinal; 6,956 joins, 159 null; raw 274 at row 1,439 is outside nation main-table ordinals but inside stage_name domain",
        "sstn": "stage_name/table 23 ordinal; 3,441 joins, 3,674 null; zero at row 3,830 is a valid ordinal",
        "dbrt": "two lanes: u8 flag + i8 state; not a one-byte enum; no enum_ref/UI labels asserted",
        "posi": "i8; -1 is native missing value (2,650 rows); live values 1..16 fit XML [0,50]",
        "cquf": "table 25 ordinal; 1,022 joins, 6,093 null",
        "tcop": "table 24 team ordinal; 2,629 joins, 4,486 null; all live targets use selector 11",
    }
    for field in table["fields"]:
        coords = field["coordinates"]
        if len(coords) == 1:
            coord = f"row {coords[0]['row_offset']} / wire {coords[0]['wire_offset']}"
        else:
            coord = "; ".join(f"row {item['row_offset']} / wire {item['wire_offset']}" for item in coords)
        reader_vas = ", ".join(site["VA"] for site in field["provenance"]["reader_transfer_sites"])
        getter_vas = ", ".join(site["VA"] for site in field["provenance"]["getter_accesses"])
        lines.append("| " + " | ".join([
            f"`Tchl.{field['code']}`",
            str(field.get("name", "-")).replace("|", "\\|"),
            coord,
            str(field.get("width_bytes")),
            str(field.get("interpretation", "-")).replace("|", "\\|"),
            summaries[field["code"]],
            str(field.get("grade")),
            reader_vas,
            getter_vas,
        ]) + " |")
    lines.extend([
        "",
        "### Held in Tchl",
        "",
        "| Field | Grade | Candidate coordinate | Preserved reason / first counterexample |",
        "|---|---|---|---|",
    ])
    for field in table["held_fields"]:
        coord = "; ".join(
            f"row {item['row_offset']} / wire {item['wire_offset']} / width {item['width_bytes']}"
            for item in field["coordinates"]
        )
        lines.append("| " + " | ".join([
            f"`{field['code']}`", str(field["grade"]), coord,
            str(field["held_reason"]).replace("|", "\\|"),
        ]) + " |")
    lines.extend([
        "",
        "`styr` and `edyr` remain held: both are u16 year integers with zero values outside frozen XML [1900,2100]; no zero sentinel is inferred. The first counterexamples remain row 28 @1254 and row 2695 @118604.",
        "",
    ])
    return "\n".join(lines)


def markdown_report(baseline_md: str, schema: dict[str, Any]) -> str:
    replacements = {
        "Generated by t40 from six accepted field ledgers.": "Generated by t42: the six accepted t40 tables are retained verbatim and accepted t39 Tchl evidence is appended.",
        "- Club tables: 6": "- Club tables: 7 (including shared club/nation Tchl)",
        "- Accepted L3 business fields: 44": "- Accepted L3 business fields: 51",
        "- Held fields: 13": "- Held fields: 15",
        "client entries for the other five tables are absent.": "client entries for the other six tables, including Tchl/table 34, are absent.",
        "the source cursors report a 13-byte prefix and 9-byte footer for all six tables.": "the source cursors report a 13-byte prefix and 9-byte footer for all seven tables.",
    }
    text = baseline_md
    for old, new in replacements.items():
        if text.count(old) != 1:
            raise CheckFailure(f"expected one Markdown baseline phrase: {old}")
        text = text.replace(old, new, 1)
    table_row = "| `club.xml/nation.xml:Tchl` | 34 | STARTING_TEAM_CUP_HISTORY | 7115 | 44 | 313082 | `a07b2bb76fb8796bcbc39dde659610d5257a8801004b6608e4be34beb9a84812` | `13 + 7115 * 44 + 9 = 313082` |"
    marker = "| `club.xml:Cdbt` | 33 | STARTING_CLUB_DEBT | 32409 | 79 | 2560333 | `b2bf8e2f1db6d73bc0080e4fd9a2666fa6bbdd7d053cd386e19590d557e987c3` | `13 + 32409 * 79 + 9 = 2560333` |"
    if text.count(marker) != 1:
        raise CheckFailure("could not identify the end of the accepted v1 table list")
    text = text.replace(marker, marker + "\n" + table_row, 1)
    tchl_section = tchl_markdown(schema["tables"][-1]).rstrip() + "\n\n"
    section_marker = "## Negative Regressions\n"
    if text.count(section_marker) != 1:
        raise CheckFailure("could not locate the Markdown negative-regressions section")
    text = text.replace(section_marker, tchl_section + section_marker, 1)
    text = text.replace(
        "- Binary provenance is tied to the manifested `evidence/fm24` IDA provenance snapshot; the external executable was not read.",
        "- Binary provenance is tied to the manifested `evidence/fm24` IDA provenance snapshot; the external executable was not read. Schema provenance additionally records the frozen `master.json` SHA-256 and its matching MANIFEST entry.",
        1,
    )
    for marker in ("Club tables: 7", "Accepted L3 business fields: 51", "Held fields: 15", "L4: 0", "Negative Regressions", "## Tchl", "master.json"):
        if marker not in text:
            raise CheckFailure(f"Markdown report missing marker: {marker}")
    return text


def validate_schema(schema: dict[str, Any], baseline: dict[str, Any], report: str) -> None:
    tables = schema.get("tables", [])
    if schema.get("schema_version") != 2 or schema.get("generated_by") != "t42":
        raise CheckFailure("schema version/generator is not t42 v2")
    if len(tables) != 7 or [item["parent_code"] for item in tables[:6]] != [item["parent_code"] for item in baseline["tables"]]:
        raise CheckFailure("v1 table order or seven-table total changed")
    if tables[:6] != baseline["tables"]:
        raise CheckFailure("one or more accepted v1 tables were modified")
    if schema.get("negative_regressions") != baseline.get("negative_regressions"):
        raise CheckFailure("v1 negative regressions were modified")
    if len(schema["negative_regressions"]) != 4:
        raise CheckFailure("expected four negative regressions")
    if len(tables[0].get("excluded_non_business_records", [])) != 2:
        raise CheckFailure("the two accepted Cstc non-business slots were modified")
    l3_count = sum(len(table.get("fields", [])) for table in tables)
    held_count = sum(len(table.get("held_fields", [])) for table in tables)
    if (l3_count, held_count) != (51, 15):
        raise CheckFailure(f"expected 51 L3 and 15 held, got {l3_count}/{held_count}")
    if schema.get("coverage", {}).get("club_tables") != 7 or schema.get("coverage", {}).get("club_L3_fields") != 51:
        raise CheckFailure("coverage table/L3 counts are inconsistent")
    if schema.get("coverage", {}).get("held_fields") != 15 or schema.get("coverage", {}).get("negative_regressions") != 4:
        raise CheckFailure("coverage held/negative counts are inconsistent")
    if schema.get("coverage", {}).get("L4") != 0:
        raise CheckFailure("L4 must remain zero")
    if schema.get("coverage", {}).get("nation_side", {}).get("summary", {}).get("new_L3_claims") != 0:
        raise CheckFailure("t37 nation context must retain zero new nation-exclusive L3 claims")
    if schema.get("binary_provenance") != baseline.get("binary_provenance"):
        raise CheckFailure("accepted v1 binary provenance was changed")
    if not schema.get("schema_provenance", {}).get("manifest_match"):
        raise CheckFailure("master.json manifest match is missing")
    tchl = tables[-1]
    if tchl.get("parent_code") != "Tchl" or tchl.get("table_type") != 34 or tchl.get("rtti_class") != "STARTING_TEAM_CUP_HISTORY":
        raise CheckFailure("Tchl table identity mismatch")
    if {field["code"] for field in tchl["fields"]} != {"tchc", "mstn", "sstn", "dbrt", "posi", "cquf", "tcop"}:
        raise CheckFailure("Tchl L3 field set mismatch")
    if {field["code"] for field in tchl["held_fields"]} != {"styr", "edyr"}:
        raise CheckFailure("Tchl held field set mismatch")
    if tchl.get("reference_domains", {}).get("shared_owner_domain", {}).get("club_exclusive_L3") != 0:
        raise CheckFailure("Tchl club-exclusive L3 must remain zero")
    if tchl["reference_domains"]["shared_owner_domain"].get("nonnull_owner_count") != 7084:
        raise CheckFailure("Tchl nonempty owner count differs")
    if tchl["reference_domains"]["shared_owner_domain"].get("target_selector_counts") != {"11": 7084}:
        raise CheckFailure("Tchl owner selector evidence differs")
    if not re.search(r"not used as an exclusivity criterion", tchl["reference_domains"]["shared_owner_domain"].get("exclusivity_basis", "")):
        raise CheckFailure("entity_tag exclusivity caveat is missing")
    layout = tchl.get("server_payload", {})
    if (layout.get("payload_sha256") != "a07b2bb76fb8796bcbc39dde659610d5257a8801004b6608e4be34beb9a84812"
            or layout.get("row_count") != 7115 or layout.get("stride_bytes") != 44
            or layout.get("payload_len") != 313082 or not layout.get("closure_ok")
            or layout.get("closure_formula") != "13 + 7115 * 44 + 9 = 313082"):
        raise CheckFailure("Tchl server payload identity/closure mismatch")
    if tchl.get("reader_extent", {}).get("start_VA") != "0x144511e90" or tchl.get("reader_extent", {}).get("end_VA_exclusive") != "0x14451206f":
        raise CheckFailure("Tchl reader VA extent mismatch")
    for field in tchl["fields"] + tchl["held_fields"]:
        for coordinate in field.get("coordinates", []):
            if coordinate["row_offset"] is None or coordinate["wire_offset"] != coordinate["row_offset"] + 1:
                raise CheckFailure(f"Tchl coordinate origin mismatch for {field['code']}")
        if not field.get("provenance", {}).get("reader_transfer_sites"):
            raise CheckFailure(f"missing reader transfer provenance for Tchl.{field['code']}")
        if not field.get("provenance", {}).get("getter_accesses"):
            raise CheckFailure(f"missing getter provenance for Tchl.{field['code']}")
    if len(next(item for item in tchl["fields"] if item["code"] == "dbrt")["coordinates"]) != 2:
        raise CheckFailure("dbrt's two physical lanes were collapsed")
    if "## Tchl" not in report or "first counterexample row 28 @1254" not in report or "row 2695 @118604" not in report:
        raise CheckFailure("Tchl Markdown section or held counterexamples are incomplete")


def selftest() -> tuple[dict[str, Any], str]:
    baseline, _ = load_v1_baseline()
    baseline_md = load_v1_markdown()
    schema = build_schema(baseline)
    report = markdown_report(baseline_md, schema)
    validate_schema(schema, baseline, report)
    return schema, report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Append accepted t39 Tchl evidence to the frozen t40 club/nation schema v1.")
    parser.add_argument("--selftest", action="store_true", help="build in memory and validate counts, preservation, provenance, and closure")
    parser.add_argument("--force", action="store_true", help="write v2 reports and preserve the exact accepted v1 inputs on first run")
    args = parser.parse_args(argv)
    try:
        schema, report = selftest()
        if args.selftest:
            print("SELFTEST PASS: 7 tables, 51 L3, 15 held, 4 negatives, 2 Cstc non-business, L4=0; v1 tables verbatim; master SHA matched")
            return 0
        if (OUT_JSON.exists() or OUT_MD.exists()) and not args.force:
            raise CheckFailure("report outputs exist; pass --force to perform the requested in-place v2 upgrade")
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        if not V1_JSON_SNAPSHOT.exists():
            current = OUT_JSON.read_bytes()
            if sha256_bytes(current) != V1_JSON_SHA256:
                raise CheckFailure("refusing to snapshot a non-v1 schema as the accepted baseline")
            V1_JSON_SNAPSHOT.write_bytes(current)
        if not V1_MD_SNAPSHOT.exists():
            current_md = OUT_MD.read_bytes()
            if sha256_bytes(current_md) != V1_MD_SHA256:
                raise CheckFailure("refusing to snapshot a non-v1 Markdown report as the accepted baseline")
            V1_MD_SNAPSHOT.write_bytes(current_md)
        OUT_JSON.write_text(json.dumps(schema, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        OUT_MD.write_text(report, encoding="utf-8", newline="\n")
        print(f"WROTE {OUT_JSON.relative_to(ROOT)}")
        print(f"WROTE {OUT_MD.relative_to(ROOT)}")
        print(f"SNAPSHOT {V1_JSON_SNAPSHOT.relative_to(ROOT)}")
        print(f"SNAPSHOT {V1_MD_SNAPSHOT.relative_to(ROOT)}")
        return 0
    except CheckFailure as exc:
        print(f"CHECK FAILED: {exc}", file=sys.stderr)
        return 1
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"FATAL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
