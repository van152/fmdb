#!/usr/bin/env python3
"""Append accepted t41 Csme evidence to the frozen t42 schema v2."""
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
V2_JSON = OUT_DIR / "club_nation_subtable_schema.v2.json"
V2_MD = OUT_DIR / "club_nation_subtable_schema.v2.md"
V2_JSON_SHA256 = "a08b013a060724bef6e0c8ea1e0c4b16e57a7438a8fa53d7ed519c6f77611ab7"
V2_MD_SHA256 = "da02f1062172d0ca9ae5f44ee3061cb06962a2255c95af0b76617156bf700dbd"
FIELDS_PATH = "scratch/t41/out/fields_csme.json"
CURSOR_PATH = "scratch/t41/out/cursor_csme.json"
T41_REPORT_PATH = "scratch/t41/out/REPORT.md"
LEDGER_LIVE_PATH = "scratch/t01/LEDGER.json"
LEDGER_PATH = "scratch/t45/out/LEDGER.E82.json"
BINARY_SHA256 = "b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4"
EXPECTED_SOURCE_HASHES = {
    "scratch/t24/out/subtables.part001.json": "6ba93636161d924ebf2648cb4be254d864b773bc30b28bd9c4fdf3349a44b829",
    "scratch/t33/out/profiles/table_server_59.profile.json": "3c4ee8efdb057ad21b020d67a6d08c174ffe42309bb2d3fc28e0fea11922ecf9",
    "scratch/t33/out/profiles/table_server_59.rows.jsonl": "b06e7e468f6d9e1c3cb8b8b36533b667ae87a74b2338fe8c24e91f7a34abcc49",
    "scratch/t33/out/REPORT.md": "07572015f6f2455bd0787e7d0303ef3782eee386e40829e2b723963ada23e7e5",
    FIELDS_PATH: "f08c5ca7d0b51779f4708ae77c3a4bc15b37e5d6633879ca1ca78654d5ba1a50",
    CURSOR_PATH: "967cca2843388b00bb2335e5d67de7cb6a6074fbe3fe444851b5808770cc8306",
    T41_REPORT_PATH: "2013d798716f4f740e0009d4b051e86caac256f4105fe444cbffdcfb579ba3bf",
    LEDGER_PATH: "20fb4a99a955b800a49078ede30700221ca7a9b32fd98db49b8a2fed981af749",
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
}


class CheckFailure(Exception):
    pass


def rel(path: str) -> Path:
    return ROOT / Path(path)


def source_file(path: str) -> Path:
    target = rel(path)
    if path == LEDGER_PATH and not target.is_file():
        return rel(LEDGER_LIVE_PATH)
    return target


def read_json(path: Path | str) -> Any:
    target = path if isinstance(path, Path) else source_file(path)
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


def hex_offset(value: Any) -> str:
    number = as_int(value)
    if number is None:
        raise CheckFailure(f"invalid file offset {value!r}")
    return f"0x{number:x}"


def load_v2_json() -> tuple[dict[str, Any], bytes]:
    source = V2_JSON if V2_JSON.is_file() else OUT_JSON
    raw = source.read_bytes()
    if sha256_bytes(raw) != V2_JSON_SHA256:
        raise CheckFailure("t42 v2 JSON snapshot/input SHA-256 mismatch")
    baseline = json.loads(raw.decode("utf-8"))
    if baseline.get("schema_version") != 2 or baseline.get("generated_by") != "t42":
        raise CheckFailure("expected the accepted t42 schema v2 baseline")
    return baseline, raw


def load_v2_markdown() -> tuple[str, bytes]:
    source = V2_MD if V2_MD.is_file() else OUT_MD
    raw = source.read_bytes()
    if sha256_bytes(raw) != V2_MD_SHA256:
        raise CheckFailure("t42 v2 Markdown snapshot/input SHA-256 mismatch")
    text = raw.decode("utf-8")
    if "Generated by t42:" not in text or "Accepted L3 business fields: 51" not in text:
        raise CheckFailure("expected the accepted t42 v2 Markdown baseline")
    return text, raw


def verify_source_hashes(cursor: dict[str, Any], fields: dict[str, Any]) -> list[str]:
    dynamic = [f"scratch/t41/out/{name}" for name in cursor.get("instruction_shards", [])]
    dynamic += [f"scratch/t41/out/{name}" for name in cursor.get("branch_shards", [])]
    t33 = cursor.get("t33_differential", {})
    historical_negative = t33.get("historical_negative", {})
    paths = [
        fields.get("occurrences_source"), FIELDS_PATH, CURSOR_PATH, T41_REPORT_PATH,
        *dynamic, t33.get("path"), t33.get("rows_file"), historical_negative.get("path"), LEDGER_PATH,
    ]
    if any(not isinstance(path, str) for path in paths) or len(paths) != len(set(paths)):
        raise CheckFailure("t41 source artifact paths are missing or duplicated")
    if set(paths) != set(EXPECTED_SOURCE_HASHES):
        raise CheckFailure("t41 source artifact inventory differs from the frozen E82 inputs")
    for path, expected in EXPECTED_SOURCE_HASHES.items():
        target = source_file(path)
        if not target.is_file() or sha256_file(target) != expected:
            raise CheckFailure(f"t41 source artifact hash mismatch: {path}")
    if fields.get("occurrences_sha256") != EXPECTED_SOURCE_HASHES.get(fields.get("occurrences_source")):
        raise CheckFailure("Csme schema occurrence source hash differs from fields_csme.json")
    return paths


def load_instruction_index(cursor: dict[str, Any]) -> dict[int, dict[str, Any]]:
    result: dict[int, dict[str, Any]] = {}
    for name in cursor.get("instruction_shards", []):
        shard = read_json(rel(f"scratch/t41/out/{name}"))
        for instruction in shard.get("instructions", []):
            offset = as_int(instruction.get("file_offset"))
            if offset is None:
                continue
            previous = result.get(offset)
            if previous is not None and previous != instruction:
                raise CheckFailure(f"conflicting t41 instruction at {name}:{instruction.get('file_offset')}")
            result[offset] = instruction
    return result


def require_instruction(index: dict[int, dict[str, Any]], offset: Any, label: str) -> dict[str, Any]:
    number = as_int(offset)
    instruction = index.get(number) if number is not None else None
    if instruction is None or not instruction.get("VA"):
        raise CheckFailure(f"missing instruction provenance for {label} at {offset!r}")
    return instruction


def reader_extent(cursor: dict[str, Any]) -> dict[str, Any]:
    reader = cursor["reader"]
    return {
        "start_file_offset": hex_offset(reader["entry"]),
        "end_file_offset_exclusive": hex_offset(reader["end_exclusive"]),
        "start_VA": reader["entry_VA"],
        "end_VA_exclusive": reader["end_VA"],
        "extent_source": reader["extent_source"],
    }


def reader_site(record: dict[str, Any], sink: dict[str, Any], index: dict[int, dict[str, Any]]) -> dict[str, Any]:
    instruction = require_instruction(index, sink.get("site"), f"{record.get('code')} reader sink")
    return {
        "role": "row_reader_transfer",
        "file_offset": hex_offset(sink["site"]),
        "VA": instruction["VA"],
        "width_bytes": sink["width"],
        "legacy_offset": sink.get("legacy"),
        "wire_offset": sink.get("wire"),
        "index": "j",
        "condition": sink.get("when"),
        "instruction": instruction.get("instruction"),
    }


def getter_sites(record: dict[str, Any], index: dict[int, dict[str, Any]]) -> list[dict[str, Any]]:
    getter = record.get("getter", {})
    candidates: list[tuple[str, Any]] = []
    if getter.get("compare") is not None:
        candidates.append(("field_dispatch_compare", getter["compare"]))
    if getter.get("box_call") is not None:
        candidates.append(("tagged_box_helper_call", getter["box_call"]))
    if getter.get("member_load") is not None:
        candidates.append(("getter_member_load", getter["member_load"]))
    for offset in getter.get("lane_loads", []):
        candidates.append(("tagged_pair_lane_load", offset))
    result = []
    for role, offset in candidates:
        instruction = require_instruction(index, offset, f"{record.get('code')} {role}")
        result.append({
            "role": role,
            "file_offset": hex_offset(offset),
            "VA": instruction["VA"],
            "instruction": instruction.get("instruction"),
        })
    return result


def writer_sites(record: dict[str, Any], sink: dict[str, Any], index: dict[int, dict[str, Any]]) -> list[dict[str, Any]]:
    offsets = record.get("write_sites", [])
    if sink.get("writer_site") is not None:
        offsets = [*offsets, sink["writer_site"]]
    result = []
    for offset in offsets:
        instruction = require_instruction(index, offset, f"{record.get('code')} writer site")
        result.append({
            "file_offset": hex_offset(offset),
            "VA": instruction["VA"],
            "instruction": instruction.get("instruction"),
        })
    return result


def make_field(
    record: dict[str, Any], category: str, source_paths: list[str],
    index: dict[int, dict[str, Any]], extent: dict[str, Any],
) -> dict[str, Any]:
    code = record["code"]
    occurrence = record["occurrence"]
    schema = deepcopy(record["schema"])
    schema["idx"] = int(occurrence[2])
    sink = record.get("sink") or record.get("candidate_sink")
    if not isinstance(sink, dict):
        raise CheckFailure(f"missing sink record for Csme.{code}")
    coordinates = []
    candidate_coordinates = []
    if category == "L3":
        coordinates = [{
            "row_offset": sink["legacy"],
            "wire_offset": sink["wire"],
            "width_bytes": sink["width"],
            "index": "j",
            "count": "n",
            "condition": sink["when"],
        }]
    else:
        candidate_coordinates = [{
            "row_offset": sink["legacy"],
            "wire_offset": sink["wire"],
            "width_bytes": sink["width"],
            "index": "j",
            "count": "n",
            "condition": sink["when"],
            "disposition": "held; static sink binding only",
        }]
    coordinate_note = (
        "t41 row_offset=18 and wire_offset=19 identify item j=0 only; the conditional coordinate is "
        "legacy 18+10*j / wire 19+10*j for 0 <= j < n, where n is the u32 count at wire+6. "
        "In the observed payload n is 0 or 1, so Melf is present only on count=1 rows (2,512 rows). "
        "A count=0 row has no Melf value; the XML default is not asserted as a stored row value."
        if category == "L3" else
        "Static binding only: candidate legacy 10+10*j / wire 11+10*j, width 8, for 0 <= j < n. "
        "The coordinate is not promoted because every materialized pair is null and no live media-source reference is available."
    )
    provenance = {
        "task": "t41",
        "field_ledger": FIELDS_PATH,
        "source_files": list(source_paths),
        "source_record_sha256": canonical_sha256(record),
        "binary": "editor.exe",
        "binary_sha256": BINARY_SHA256,
        "reader_extent": deepcopy(extent),
        "reader_transfer_sites": [reader_site(record, sink, index)],
        "getter_accesses": getter_sites(record, index),
        "writer_sites": writer_sites(record, sink, index),
        "source_record": deepcopy(record),
    }
    return {
        "code": code,
        "name": record["schema"]["name"],
        "status": category,
        "grade": record["grade"],
        "row_offset": record.get("row_offset") if category == "L3" else None,
        "wire_offset": record.get("wire_offset") if category == "L3" else None,
        "coordinates": coordinates,
        "candidate_coordinates": candidate_coordinates,
        "coordinate_note": coordinate_note,
        "width_bytes": sink["width"],
        "interpretation": record.get("profile", {}).get("interpretation") if category == "L3" else "tagged two-lane identity pair; live target resolution not observed",
        "schema": schema,
        "domain": deepcopy(record.get("domain")),
        "profile": deepcopy(record["profile"]),
        "held_reason": record.get("reason") if category == "held" else None,
        "provenance": provenance,
    }


def acceptance_record(ledger: dict[str, Any]) -> dict[str, Any]:
    matches = [item for item in ledger.get("entries", []) if item.get("id") == "E82"]
    if len(matches) != 1:
        raise CheckFailure("expected exactly one t01 E82 acceptance entry")
    entry = matches[0]
    if entry.get("kind") != "acceptance" or entry.get("level") != "L3":
        raise CheckFailure("E82 is not an accepted L3 record")
    claim = entry.get("claim", "")
    if "Melf" not in claim or "Msid held" not in claim or "224880" not in claim:
        raise CheckFailure("E82 claim does not contain the accepted Csme scope")
    return entry


def make_csme_table(fields: dict[str, Any], cursor: dict[str, Any], source_paths: list[str], ledger: dict[str, Any]) -> dict[str, Any]:
    if fields.get("table_type") != 59 or fields.get("parent") != "Csme" or fields.get("scope") != ["club.xml", "Csme"]:
        raise CheckFailure("fields_csme table identity/scope mismatch")
    if cursor.get("table_type") != 59 or cursor.get("parent") != "Csme":
        raise CheckFailure("cursor_csme table identity mismatch")
    source_records = {item.get("code"): item for item in fields.get("fields", [])}
    if set(source_records) != {"Melf", "Msid"}:
        raise CheckFailure("expected exactly the t41 Melf and Msid records")
    if (source_records["Melf"].get("grade"), source_records["Msid"].get("grade")) != (
        "L3_table59_conditional_named_coordinate", "held_no_live_media_reference"
    ):
        raise CheckFailure("t41 Csme source grades differ from E82")
    if fields.get("L3") != 1 or fields.get("club_exclusive_L3") != 0 or fields.get("L4") != 0:
        raise CheckFailure("t41 Csme accepted counts differ from E82")
    if fields.get("scope_caveat") != "not club-exclusive: actual owners include selector 11; play label is not a PLAYER pointer or dispatch proof":
        raise CheckFailure("t41 Csme scope caveat changed")

    archives = cursor["archives"]
    server = archives["server"]
    client = archives["client"]
    frame = server["selected_frame"]
    entry = server["entry"]
    count = int(server["row_count"])
    payload_len = int(server["payload_bytes"])
    payload_hash = server["payload_sha256"]
    histogram = server["stride_histogram"]
    footer = server["wire_footer"]
    n0, n1 = int(histogram["22"]), int(histogram["32"])
    closure_ok = 13 + n0 * 22 + n1 * 32 + 9 == payload_len
    if (count, n0, n1, payload_len, payload_hash) != (
        9079, 6567, 2512, 224880,
        "7eee0ecc59ee306aefc52eb7a7f7095d439748f3e06ac9d36d3ddc1568c8b1a7",
    ) or not closure_ok or frame.get("sha256") != payload_hash:
        raise CheckFailure("t41 Csme variable server payload does not match the accepted closure")
    header = bytes.fromhex(server["header_hex"])
    header_count = int.from_bytes(header[8:12], "little")
    if header_count != count or footer.get("offset") != 224871 or payload_len - footer["offset"] != 9:
        raise CheckFailure("t41 Csme header/footer framing mismatch")
    if client.get("present") is not False or client.get("entry") is not None:
        raise CheckFailure("client table 59 must remain absent, not empty")

    owner = deepcopy(fields["unscoped_owner"])
    selectors = owner.get("selector_histogram", {})
    if owner.get("matches") != 9079 or owner.get("distinct") != 9079 or selectors != {"10": 8941, "11": 138}:
        raise CheckFailure("Csme table24 owner selector profile differs from t41")
    if owner.get("scope_counterexample", {}).get("row") != 0 or owner.get("scope_counterexample", {}).get("target_selector") != 11:
        raise CheckFailure("Csme club-exclusivity counterexample differs from t41")

    index = load_instruction_index(cursor)
    extent = reader_extent(cursor)
    melf = make_field(source_records["Melf"], "L3", source_paths, index, extent)
    msid = make_field(source_records["Msid"], "held", source_paths, index, extent)
    accepted = acceptance_record(ledger)
    table = {
        "entity": "club_editor_team_owned",
        "parent_xml": "club.xml",
        "parent_code": "Csme",
        "table_type": 59,
        "rtti_class": cursor["rtti"]["class"],
        "source_task": "t41",
        "schema_scope": deepcopy(fields["scope"]),
        "source_ledger_summary": {
            "status": "accepted_by_E82",
            "fields_named": len(source_records),
            "L3": 1,
            "held": 1,
            "club_exclusive_L3": 0,
            "L4": 0,
            "offset_origin": "Melf is item-indexed; row_offset/wire_offset denote j=0 only and exist only when count n > 0.",
        },
        "server_payload": {
            "archive": "server",
            "present": True,
            "path": entry["path"],
            "row_count": count,
            "stride_bytes": None,
            "stride_histogram_bytes": {"22": n0, "32": n1},
            "payload_len": payload_len,
            "payload_sha256": payload_hash,
            "header_hex": server["header_hex"],
            "header_record_count": header_count,
            "row_stream_prefix_bytes": 13,
            "selector_bytes_per_row": 1,
            "row_body_length_formula": "21 + 10*n",
            "row_length_formula": "22 + 10*n",
            "count_wire_offset": 6,
            "wire_footer_start": footer["offset"],
            "footer_hex": footer["hex"],
            "footer_bytes": 9,
            "closure_formula": "13 + 6567 * 22 + 2512 * 32 + 9 = 224880",
            "closure_ok": closure_ok,
            "legacy_row_origin": server["legacy_origin"],
            "wire_row_origin": server["wire_origin"],
            "legacy_footer_start": server["legacy_footer_offset"],
            "legacy_footer_hex": server["legacy_footer_hex"],
            "archive_member_offset": entry["offset"],
            "archive_member_packed_size": entry["packed_size"],
            "selected_frame_offset": frame["offset"],
            "selected_frame_packed_size": frame["compressed_bytes"],
        },
        "client_observation": {
            "archive": "client",
            "present": False,
            "directory_entry_count": client["directory_entry_count"],
            "table_entry_absent": True,
        },
        "coordinate_policy": (
            "t41 coordinates are item-indexed. For Melf, row_offset 18 / wire_offset 19 is j=0 only; "
            "the byte coordinate is legacy 18+10*j / wire 19+10*j for 0 <= j < n. The observed rows "
            "have n=0 or 1, so only count=1 rows contain Melf; no default is inferred for count=0 rows."
        ),
        "reader_extent": extent,
        "owner_scope": {
            "source_record": owner,
            "target_table_type": 24,
            "owner_rows": owner["matches"],
            "distinct_owner_ordinals": owner["distinct"],
            "selector_histogram": selectors,
            "selector_classes": {"10": "TEAM", "11": "NATIONAL_TEAM"},
            "club_exclusive_L3": 0,
            "exclusivity_basis": "All owner ordinals resolve in the table24 Team family; selectors 10/11 include TEAM and NATIONAL_TEAM. The row-0 selector-11 witness disproves club exclusivity.",
            "first_non_club_exclusive_witness": deepcopy(owner["scope_counterexample"]),
            "scope_caveat": fields["scope_caveat"],
        },
        "source_acceptance": {
            "ledger_path": LEDGER_PATH,
            "entry_id": "E82",
            "level": "L3",
            "kind": "acceptance",
            "claim": accepted["claim"],
        },
        "fields": [melf],
        "held_fields": [msid],
        "unscoped_evidence": {
            "outer_non_schema_byte": deepcopy(fields["outer_non_schema_byte"]),
            "inner_tag": deepcopy(fields["inner_tag"]),
        },
        "supplemental_evidence": {
            "historical_t33_differential": deepcopy(cursor["t33_differential"]),
            "historical_t33_negative": deepcopy(cursor["t33_differential"]["historical_negative"]),
            "t33_negative_clarification": cursor["t33_differential"]["historical_negative"]["clarification"],
            "scope_note": "The t41 report retains the t33 false-tail negative; it is not added to the four original t20 negative regressions.",
        },
        "source_artifacts": list(source_paths),
    }
    return table


def build_schema(baseline: dict[str, Any]) -> dict[str, Any]:
    fields = read_json(FIELDS_PATH)
    cursor = read_json(CURSOR_PATH)
    source_paths = verify_source_hashes(cursor, fields)
    ledger = read_json(LEDGER_PATH)
    table = make_csme_table(fields, cursor, source_paths, ledger)
    schema = deepcopy(baseline)
    schema["schema_version"] = 3
    schema["generated_by"] = "t45"
    schema["schema_provenance"]["acceptance_ledger"]["csme_acceptance_entry"] = "E82"

    artifacts = list(schema["source_artifacts"])
    known = {item["path"]: item for item in artifacts}
    for path in source_paths:
        target = source_file(path)
        item = {"path": path, "sha256": sha256_file(target), "bytes": target.stat().st_size}
        if path in known:
            if known[path] != item:
                raise CheckFailure(f"existing source artifact record differs for {path}")
        else:
            artifacts.append(item)
            known[path] = item
    schema["source_artifacts"] = artifacts
    schema["tables"].append(table)

    coverage = schema["coverage"]
    coverage.update({
        "club_tables": 8,
        "club_L3_fields": 52,
        "held_fields": 16,
        "negative_regressions": 4,
        "L4": 0,
        "cross_archive_offset_inference": (
            "not performed; accepted business-field sink evidence remains server-side. Cstc client table 22 carries identity only; "
            "client table entries for the other seven tables, including Tchl/table 34 and Csme/table 59, are absent. "
            "Tchl ordinal targets and Csme item-indexed coordinates remain separately scoped."
        ),
    })
    coverage["nation_side"]["conclusion"] = (
        "The t37 nation inventory remains partial with zero new nation-exclusive L3 claims. Accepted shared Tchl/table 34 fields "
        "remain separate from club-only claims; Csme/table 59 Melf is item-conditional and club-exclusive L3 remains zero."
    )
    schema["inventory_reconciliation"]["csme_scope"] = (
        "t41 E82 accepts Csme/table 59 Melf as an item-conditional L3 field. All 9,079 owner ordinals resolve within the table24 "
        "Team family (selectors 10 and 11); the selector-11 witness prevents a club-exclusive claim, so club-exclusive L3=0."
    )
    return schema


def csme_markdown(table: dict[str, Any]) -> str:
    payload = table["server_payload"]
    melf = table["fields"][0]
    msid = table["held_fields"][0]
    melf_reader = ", ".join(site["VA"] for site in melf["provenance"]["reader_transfer_sites"])
    melf_getter = ", ".join(site["VA"] for site in melf["provenance"]["getter_accesses"])
    msid_reader = ", ".join(site["VA"] for site in msid["provenance"]["reader_transfer_sites"])
    msid_getter = ", ".join(site["VA"] for site in msid["provenance"]["getter_accesses"])
    owner = table["owner_scope"]
    source = table["supplemental_evidence"]["historical_t33_negative"]
    lines = [
        "## Csme",
        "",
        "Source task `t41`, accepted by t01 E82; `table_type=59`; RTTI `STARTING_MEDIA_EXPECTATIONS`. Schema parent is `club.xml:Csme`, but this is not a club-exclusive field claim.",
        "",
        table["coordinate_policy"],
        "",
        f"Server payload: `{payload['row_count']}` rows; row lengths `{payload['stride_histogram_bytes']['22']} x 22 B` and `{payload['stride_histogram_bytes']['32']} x 32 B`; `{payload['payload_len']}` B; SHA-256 `{payload['payload_sha256']}`.",
        f"Variable closure: `{payload['closure_formula']}`. The reader takes `n` from u32 wire+6 and consumes `row_len = 22 + 10*n`; client table 59 is absent (31 client directory entries).",
        "",
        f"Reader extent: file offsets `{table['reader_extent']['start_file_offset']}..{table['reader_extent']['end_file_offset_exclusive']}` (end exclusive), VA `{table['reader_extent']['start_VA']}..{table['reader_extent']['end_VA_exclusive']}` (end exclusive).",
        f"Owner scope: {owner['owner_rows']:,} distinct table24 owner ordinals; selectors 10/11 are `{owner['selector_histogram']['10']:,}` / `{owner['selector_histogram']['11']}` (`TEAM` / `NATIONAL_TEAM`). Club-exclusive L3 is 0; row 0 at wire+1 resolves to selector 11.",
        "",
        "| Field | Name | Offset | Width | Type/interpretation | Data/domain evidence | Grade | Reader VA | Getter VA |",
        "|---|---|---|---:|---|---|---|---|---|",
        "| `Csme.Melf` | Predicted League Finish | row `18+10*j` / wire `19+10*j`, `0 <= j < n` | 1 | u8 zero-extended integer | 2,512 entries; values 1..33; no 0 or 0xff; XML max 127 | L3_table59_conditional_named_coordinate | " + melf_reader + " | " + melf_getter + " |",
        "| `Csme.Msid` | Media Source | candidate row `10+10*j` / wire `11+10*j`, `0 <= j < n` | 8 | tagged two-lane identity pair | 6,567 rows have no entry; all 2,512 materialized pairs are `(-1,-1)`; no live reference; first counterexample row 2 @68 `ffffffffffffffff` | held_no_live_media_reference | " + msid_reader + " | " + msid_getter + " |",
        "",
        "`Melf.row_offset=18` and `wire_offset=19` are the first-item coordinates only. In the observed payload, only count=1 rows (2,512) contain Melf; count=0 rows have no Melf value. The XML default `1` is not asserted as a stored default. No zero rewrite or 0/0xff sentinel is inferred.",
        "",
        "`Msid` remains held: the 8-byte pair is statically bound, but there is no live media-source reference to adjudicate ordinal/UID semantics. The first null pair is row 2 at wire offset 68. Its exact source-record reason and profile remain in JSON provenance.",
        "",
        f"Historical t33 negative is retained separately, not counted among the four t20 regressions: `{source['quote']}`. t41 clarification: {source['clarification']}",
        "",
    ]
    return "\n".join(lines)


def markdown_report(baseline_md: str, schema: dict[str, Any]) -> str:
    replacements = {
        "Generated by t42: the six accepted t40 tables are retained verbatim and accepted t39 Tchl evidence is appended.":
            "Generated by t45: the seven accepted t42 tables are retained verbatim and accepted t41 Csme evidence is appended.",
        "- Club tables: 7 (including shared club/nation Tchl)":
            "- Club tables: 8 (including shared Tchl and Csme; club-exclusive L3 remains zero for Csme)",
        "- Accepted L3 business fields: 51": "- Accepted L3 business fields: 52",
        "- Held fields: 15": "- Held fields: 16",
        "client entries for the other six tables, including Tchl/table 34, are absent.":
            "client entries for the other seven tables, including Tchl/table 34 and Csme/table 59, are absent.",
        "Every server row stream closes as `prefix + count * stride + footer = payload_len`; the source cursors report a 13-byte prefix and 9-byte footer for all seven tables.":
            "All eight server row streams close with a 13-byte prefix and 9-byte footer. Csme/table 59 is variable-length: `13 + 6567 * 22 + 2512 * 32 + 9 = 224880`; the other seven tables retain their accepted framing.",
        "- Held rows remain held, including Cstc code-row-only/profile-conflict records, Clhs and CNtp profile conflicts, and Cmti `icom` without an independent wire sink.":
            "- Held rows remain held, including the original Cstc, Clhs, Cmti, and CNtp records and Csme `Msid` without a live media-source reference.",
        "Source editor.exe SHA-256: `b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4`. L4 evidence: `0`.":
            "Source editor.exe SHA-256: `b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4`. t41 reader VA extent: `0x141583ba0..0x141583f80` (end exclusive). L4 evidence: `0`.",
    }
    text = baseline_md
    for old, new in replacements.items():
        if text.count(old) != 1:
            raise CheckFailure(f"expected exactly one v2 Markdown phrase: {old}")
        text = text.replace(old, new, 1)
    tchl_row = "| `club.xml/nation.xml:Tchl` | 34 | STARTING_TEAM_CUP_HISTORY | 7115 | 44 | 313082 | `a07b2bb76fb8796bcbc39dde659610d5257a8801004b6608e4be34beb9a84812` | `13 + 7115 * 44 + 9 = 313082` |"
    csme_row = "| `club.xml:Csme` | 59 | STARTING_MEDIA_EXPECTATIONS | 9079 | variable (22/32) | 224880 | `7eee0ecc59ee306aefc52eb7a7f7095d439748f3e06ac9d36d3ddc1568c8b1a7` | `13 + 6567×22 + 2512×32 + 9 = 224880` |"
    if text.count(tchl_row) != 1:
        raise CheckFailure("could not locate the v2 Tchl table row")
    text = text.replace(tchl_row, tchl_row + "\n" + csme_row, 1)
    marker = "## Negative Regressions\n"
    if text.count(marker) != 1:
        raise CheckFailure("could not locate the negative-regressions section")
    text = text.replace(marker, csme_markdown(schema["tables"][-1]) + marker, 1)
    for marker_text in (
        "Club tables: 8", "Accepted L3 business fields: 52", "Held fields: 16",
        "Original negative regressions retained separately: 4", "L4: 0", "## Csme",
        "0x141583ba0..0x141583f80", "count=0 rows have no Melf value", "Club-exclusive L3 is 0",
    ):
        if marker_text not in text:
            raise CheckFailure(f"v3 Markdown missing required marker: {marker_text}")
    return text


def validate_schema(schema: dict[str, Any], baseline: dict[str, Any], report: str) -> None:
    expected_tables = [item["parent_code"] for item in baseline["tables"]] + ["Csme"]
    if schema.get("schema_version") != 3 or schema.get("generated_by") != "t45":
        raise CheckFailure("schema identity/version/generator is not t45 v3")
    if [item.get("parent_code") for item in schema.get("tables", [])] != expected_tables:
        raise CheckFailure("v2 table order changed or Csme is not the eighth table")
    if schema["tables"][:7] != baseline["tables"]:
        raise CheckFailure("one or more accepted v2 table objects changed")
    if schema.get("negative_regressions") != baseline.get("negative_regressions") or len(schema["negative_regressions"]) != 4:
        raise CheckFailure("the four accepted negative regressions changed")
    if schema.get("binary_provenance") != baseline.get("binary_provenance"):
        raise CheckFailure("accepted v2 binary provenance changed")
    if schema.get("coverage", {}).get("nation_side", {}).get("summary") != baseline["coverage"]["nation_side"]["summary"]:
        raise CheckFailure("nation-side summary changed")
    l3_count = sum(len(item.get("fields", [])) for item in schema["tables"])
    held_count = sum(len(item.get("held_fields", [])) for item in schema["tables"])
    if (l3_count, held_count) != (52, 16):
        raise CheckFailure(f"expected 52 L3 and 16 held fields, got {l3_count}/{held_count}")
    coverage = schema.get("coverage", {})
    if (coverage.get("club_tables"), coverage.get("club_L3_fields"), coverage.get("held_fields"),
            coverage.get("negative_regressions"), coverage.get("L4")) != (8, 52, 16, 4, 0):
        raise CheckFailure("v3 coverage counts are inconsistent")
    if coverage.get("nation_side", {}).get("summary", {}).get("new_L3_claims") != 0:
        raise CheckFailure("nation-side new L3 claims must remain zero")
    if schema.get("schema_provenance", {}).get("acceptance_ledger", {}).get("csme_acceptance_entry") != "E82":
        raise CheckFailure("E82 schema acceptance cross-reference is missing")
    if len(schema["tables"][0].get("excluded_non_business_records", [])) != 2:
        raise CheckFailure("the two Cstc non-business records changed")

    table = schema["tables"][-1]
    if (table.get("table_type"), table.get("rtti_class"), table.get("source_task"), table.get("schema_scope")) != (
        59, "STARTING_MEDIA_EXPECTATIONS", "t41", ["club.xml", "Csme"]
    ):
        raise CheckFailure("Csme table identity/provenance mismatch")
    if [item.get("code") for item in table.get("fields", [])] != ["Melf"]:
        raise CheckFailure("Csme must add only Melf as L3")
    if [item.get("code") for item in table.get("held_fields", [])] != ["Msid"]:
        raise CheckFailure("Csme Msid must remain the only held field")
    if table.get("owner_scope", {}).get("club_exclusive_L3") != 0:
        raise CheckFailure("Csme club-exclusive L3 must remain zero")
    payload = table.get("server_payload", {})
    if payload.get("closure_formula") != "13 + 6567 * 22 + 2512 * 32 + 9 = 224880" or not payload.get("closure_ok"):
        raise CheckFailure("Csme variable-length closure is missing or false")
    if (payload.get("payload_len"), payload.get("payload_sha256"), payload.get("row_count"),
            payload.get("stride_histogram_bytes")) != (
        224880, "7eee0ecc59ee306aefc52eb7a7f7095d439748f3e06ac9d36d3ddc1568c8b1a7", 9079, {"22": 6567, "32": 2512}
    ):
        raise CheckFailure("Csme payload identity/count/stride distribution mismatch")
    if table.get("client_observation", {}).get("present") is not False:
        raise CheckFailure("client table 59 must be absent")
    melf = table["fields"][0]
    if (melf.get("grade"), melf.get("row_offset"), melf.get("wire_offset"), melf.get("width_bytes")) != (
        "L3_table59_conditional_named_coordinate", 18, 19, 1
    ):
        raise CheckFailure("Melf conditional coordinate differs from t41")
    note = melf.get("coordinate_note", "")
    if "only on count=1 rows" not in note or "count=0 row has no Melf value" not in note or "default is not asserted" not in note:
        raise CheckFailure("Melf conditional/default caveat is incomplete")
    msid = table["held_fields"][0]
    if msid.get("grade") != "held_no_live_media_reference" or msid.get("held_reason") != "All materialized entries are null. No populated reference to adjudicate against actual media_source keys; no scalar ordinal coordinate.":
        raise CheckFailure("Msid held status/reason changed")
    if table.get("reader_extent", {}).get("start_VA") != "0x141583ba0" or table.get("reader_extent", {}).get("end_VA_exclusive") != "0x141583f80":
        raise CheckFailure("Csme reader VA extent mismatch")
    if "## Csme" not in report or "13 + 6567×22 + 2512×32 + 9 = 224880" not in report:
        raise CheckFailure("Csme Markdown section/closure is missing")


def selftest() -> tuple[dict[str, Any], str, dict[str, Any]]:
    baseline, _ = load_v2_json()
    baseline_md, _ = load_v2_markdown()
    schema = build_schema(baseline)
    report = markdown_report(baseline_md, schema)
    validate_schema(schema, baseline, report)
    return schema, report, baseline


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Append accepted t41 Csme evidence to the frozen t42 club/nation schema v2.")
    parser.add_argument("--selftest", action="store_true", help="build in memory and validate preservation, provenance, closure, and counts")
    args = parser.parse_args(argv)
    try:
        schema, report, baseline = selftest()
        if args.selftest:
            print("SELFTEST PASS: 8 tables, 52 L3, 16 held, 4 negatives, L4=0; v2 tables verbatim; E82 Csme closure/provenance")
            return 0

        current_json = OUT_JSON.read_bytes()
        current_md = OUT_MD.read_bytes()
        v2_json_raw = V2_JSON.read_bytes() if V2_JSON.is_file() else current_json
        v2_md_raw = V2_MD.read_bytes() if V2_MD.is_file() else current_md
        if V2_JSON.is_file() and sha256_bytes(v2_json_raw) != V2_JSON_SHA256:
            raise CheckFailure("existing v2 JSON snapshot has an unexpected hash")
        if V2_MD.is_file() and sha256_bytes(v2_md_raw) != V2_MD_SHA256:
            raise CheckFailure("existing v2 Markdown snapshot has an unexpected hash")
        expected_json = (json.dumps(schema, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        expected_md = report.encode("utf-8")
        if current_json not in (v2_json_raw, expected_json):
            raise CheckFailure("public JSON is neither the frozen v2 input nor this deterministic v3 output")
        if current_md not in (v2_md_raw, expected_md):
            raise CheckFailure("public Markdown is neither the frozen v2 input nor this deterministic v3 output")

        OUT_DIR.mkdir(parents=True, exist_ok=True)
        ledger_snapshot = rel(LEDGER_PATH)
        live_ledger = rel(LEDGER_LIVE_PATH)
        if ledger_snapshot.exists():
            if sha256_file(ledger_snapshot) != EXPECTED_SOURCE_HASHES[LEDGER_PATH]:
                raise CheckFailure("existing E82 ledger snapshot has an unexpected hash")
        else:
            if sha256_file(live_ledger) != EXPECTED_SOURCE_HASHES[LEDGER_PATH]:
                raise CheckFailure("refusing to snapshot a changed E82 ledger")
            ledger_snapshot.write_bytes(live_ledger.read_bytes())
        if not V2_JSON.exists():
            if sha256_bytes(v2_json_raw) != V2_JSON_SHA256:
                raise CheckFailure("refusing to snapshot a non-v2 public schema")
            V2_JSON.write_bytes(v2_json_raw)
        if not V2_MD.exists():
            if sha256_bytes(v2_md_raw) != V2_MD_SHA256:
                raise CheckFailure("refusing to snapshot a non-v2 public Markdown report")
            V2_MD.write_bytes(v2_md_raw)
        OUT_JSON.write_bytes(expected_json)
        OUT_MD.write_bytes(expected_md)
        print(f"WROTE {OUT_JSON.relative_to(ROOT)}")
        print(f"WROTE {OUT_MD.relative_to(ROOT)}")
        print(f"SNAPSHOT {V2_JSON.relative_to(ROOT)}")
        print(f"SNAPSHOT {V2_MD.relative_to(ROOT)}")
        print(f"SNAPSHOT {ledger_snapshot.relative_to(ROOT)}")
        return 0
    except CheckFailure as exc:
        print(f"CHECK FAILED: {exc}", file=sys.stderr)
        return 1
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"FATAL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
