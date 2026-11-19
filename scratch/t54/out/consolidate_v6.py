#!/usr/bin/env python3
"""Incrementally merge accepted t53 TCrs evidence into the frozen v5 schema."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = Path(__file__).resolve().parent
PUBLIC_JSON = ROOT / "reports" / "club_nation_subtable_schema.json"
PUBLIC_MD = ROOT / "reports" / "club_nation_subtable_schema.md"
LEDGER_PATH = ROOT / "scratch" / "t01" / "LEDGER.json"
V5_JSON_SNAPSHOT = OUT_DIR / "club_nation_subtable_schema.v5.json"
V5_MD_SNAPSHOT = OUT_DIR / "club_nation_subtable_schema.v5.md"
V5_JSON_SHA256 = "03967c9157fe0ca46d741e5bd74f9cd4d8df592045ca2dd6c38827f99eb36184"
V5_MD_SHA256 = "4e40595cb7734df534c4ab145b96855fada9da38f711454f27d3cfedf5e6c009"
INTERIM_V6_JSON_SHA256 = "33f503e3e4bed9025c3811af686ce8646cda7140b4e431a0bc5029e86768393b"
INTERIM_V6_MD_SHA256 = "9883372dba314004464e0ff77d13827f5e9835e439786df9425836da91cea39a"
LEDGER_ENTRY_IDS = ("E87", "E89", "E90", "E91", "E92", "E93")
E93_CLAIM_SHA256 = "a889360cc8ac6a2eca46190000b28d8dcadee8a79705c2f30283f90b1542e30c"
# Historical build snapshot metadata only; live validation is entry-scoped.
HISTORICAL_LEDGER_SNAPSHOT = {
    "path": "scratch/t54/out/ledger_snapshot.json",
    "live_source_path": "scratch/t01/LEDGER.json",
    "sha256": "1ff0c2d2893300ac74fdd1c16103f5d8445c0ab718fd6df25b47154991f5b340",
    "bytes": 201293,
    "entries_used": ["E87", "E89", "E90", "E91", "E92", "E93"],
    "t50_acceptance_entry": "E91",
    "t50_acceptance_level": "L2",
    "t52_acceptance_entry": "E92",
    "t52_acceptance_level": "L2",
    "t53_acceptance_entry": "E93",
    "t53_acceptance_level": "L2",
}
FIX1_ROOT_CAUSE = "- Root cause: commander recorded E94 (t55 acceptance) after the t54 build, so the 93-entry full-ledger hash/size no longer matched the 94-entry live ledger."
FIX1_REMEDY = "- Fix: builder and verifier now pin only E87/E89/E90/E91/E92/E93 by ID, canonical claim SHA-256, kind, and level; the full-file snapshot remains historical and is not compared with the live ledger."

T53_PATHS = (
    "scratch/t53/out/discovery_crs_wire.json",
    "scratch/t53/out/cursor_crs_main_client.json",
    "scratch/t53/out/cursor_crs_main_server.json",
    "scratch/t53/out/cursor_crs_extra_client.json",
    "scratch/t53/out/cursor_crs_extra_server.json",
    "scratch/t53/out/fields_PUnI.json",
    "scratch/t53/out/fields_PUnT.json",
    "scratch/t53/out/fields_PUnP.json",
    "scratch/t53/out/fields_PUnJ.json",
    "scratch/t53/out/REPORT.md",
    "scratch/t53/out/DONE.md",
)
T53_SHA256 = {
    "scratch/t53/out/discovery_crs_wire.json": "6383063973c0b16ebd06f304b7aec4f3b46649324f93345b8e1cd879a07e66a5",
    "scratch/t53/out/cursor_crs_main_client.json": "52e043f612a95efca28b04ef87c04eecc580e8711cfe7a7088c4616cc4326cac",
    "scratch/t53/out/cursor_crs_main_server.json": "99fd9ad8cc53ce3c2c1911487ef4300b1847b622a0bb3d5d95768ef28f90c49d",
    "scratch/t53/out/cursor_crs_extra_client.json": "5fb9fcffe735063dc12f575e5b69b5f5bf534990e2d20bd8daca7afd9082f3d9",
    "scratch/t53/out/cursor_crs_extra_server.json": "b00c6fd0f6fe3732f9aa6045a338fc037d00545591478aa3c4807e924dd8cdea",
    "scratch/t53/out/fields_PUnI.json": "b0ecbba661c1633fcd7ce937a26b920cf23d0418301f450f953c24b862702b6e",
    "scratch/t53/out/fields_PUnT.json": "589bc4bf61bc2bf26c5d3b160adc7a34a885b6f9601a054bf2a385fc9040ff31",
    "scratch/t53/out/fields_PUnP.json": "994e4a11e01e10c7735275dca81fc44beac05d47a5a9bca83f9d782c8d5af37c",
    "scratch/t53/out/fields_PUnJ.json": "17124f10abaa07d83c76d097c7bc2dcfeaac7d03bfd176c9599b0a16a3a2dd4f",
    "scratch/t53/out/REPORT.md": "e4c07bed43d2d2c569f1aaa9ec9acd607a9cad315390c3d8762c0ebb7c5eddac",
    "scratch/t53/out/DONE.md": "46b6a65aef2a91fd38027e8ce39cd0c90ba410ab8af95339fba46f0885f5ab79",
}
FIELD_CODES = ("PUnI", "PUnT", "PUnP", "PUnJ")
PROTECTED_KEYS = ("tables", "negative_regressions", "v3_baseline", "club_auxiliary_sources", "nation_static_side")
EXPECTED_TRIAL_GROUPS = (
    "main_client",
    "extra_as_slot19_client",
    "extra_named_client",
    "extra_named_without_object_name_arm_client",
    "main_server",
    "extra_as_slot19_server",
    "extra_named_server",
    "extra_named_without_object_name_arm_server",
)
T50_NO_WINNER_APPENDIX = (
    "t53 E93 cross-result: the sequential table_extra_9 reader consumes the row-1 version-2/count-0 bytes through @875, "
    "selecting the server row-2 block at @875 rather than the t50 @867 alternative; for row 82 it consumes the earlier "
    "@39439 candidate as part of the preceding block and reaches the next block at @39533. This resolves only the "
    "table_extra_9 block-internal ambiguity; the table_9 t49/t50 row-boundary adjudication remains NO WINNER."
)


class CheckFailure(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckFailure(message)


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_sha256(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256_bytes(raw)


def read_json(path: Path) -> Any:
    require(path.is_file(), f"missing JSON input: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def root_path(relative: str) -> Path:
    return ROOT / Path(relative)


def load_v5() -> tuple[dict[str, Any], bytes, bytes]:
    have_json_snapshot = V5_JSON_SNAPSHOT.is_file()
    have_md_snapshot = V5_MD_SNAPSHOT.is_file()
    require(have_json_snapshot == have_md_snapshot, "only one frozen v5 snapshot exists")
    if have_json_snapshot:
        json_raw, md_raw = V5_JSON_SNAPSHOT.read_bytes(), V5_MD_SNAPSHOT.read_bytes()
    else:
        require(PUBLIC_JSON.is_file() and PUBLIC_MD.is_file(), "public v5 schema pair is missing")
        json_raw, md_raw = PUBLIC_JSON.read_bytes(), PUBLIC_MD.read_bytes()
    require(sha256_bytes(json_raw) == V5_JSON_SHA256, "v5 JSON snapshot SHA-256 mismatch")
    require(sha256_bytes(md_raw) == V5_MD_SHA256, "v5 Markdown snapshot SHA-256 mismatch")
    schema = json.loads(json_raw.decode("utf-8"))
    require((schema.get("schema_version"), schema.get("generated_by")) == (5, "t52"),
            "expected the current t52/fix1 schema v5")
    require(len(schema.get("tables", [])) == 8 and len(schema.get("negative_regressions", [])) == 4,
            "v5 base table/regression counts changed")
    return schema, json_raw, md_raw


def artifact_record(relative: str) -> dict[str, Any]:
    path = root_path(relative)
    require(path.is_file(), f"missing t53 source artifact: {relative}")
    raw = path.read_bytes()
    digest = sha256_bytes(raw)
    require(digest == T53_SHA256[relative], f"t53 source SHA-256 changed: {relative}")
    return {"path": relative, "sha256": digest, "bytes": len(raw)}


def validate_main_cursor(cursor: dict[str, Any], expected_side: str) -> dict[str, Any]:
    rows = cursor["rows"]
    require(cursor["member"] == "table_9.dat" and cursor["side"] == expected_side and
            cursor["mode"] == (0 if expected_side == "client" else 1) and len(rows) == 251,
            f"main cursor identity/mode/row count mismatch: {expected_side}")
    require(cursor["header"] == 13, f"main {expected_side}: header mismatch")
    require(rows[0]["start"] == cursor["header"], f"main {expected_side}: first row offset mismatch")
    require(all(a["end"] == b["start"] for a, b in zip(rows, rows[1:])),
            f"main {expected_side}: row spans are not contiguous")
    spans = sum(row["end"] - row["start"] for row in rows)
    require(cursor["end"] == rows[-1]["end"] and cursor["end"] == cursor["header"] + spans,
            f"main {expected_side}: EOF cursor mismatch")
    footer_bytes = len(bytes.fromhex(cursor["footer"]))
    total = cursor["end"] + footer_bytes
    expected_total = 31956 if expected_side == "client" else 307564
    require(footer_bytes == 9 and total == expected_total,
            f"main {expected_side}: footer/EOF mismatch")
    if expected_side == "client":
        require(cursor["summary"]["skipped"] == 251 and cursor["summary"]["items"] == 0 and
                all(row["presence"] is None and row["vector"] is None for row in rows),
                "main client mode-0 skip summary mismatch")
        return {"mode": 0, "rows": 251, "skipped": 251, "presence_reads": 0,
                "span_bytes": spans, "footer_bytes": footer_bytes, "payload_bytes": total,
                "closure_formula": f"13 + {spans} + 9 = {total}",
                "payload_sha256": cursor["payload_sha256"]}

    presence = Counter(str(row["presence"]) for row in rows)
    vectors = [row["vector"] for row in rows if row.get("vector") is not None]
    nonempty = [vector for vector in vectors if vector["count"] > 0]
    item_count = sum(vector["count"] for vector in vectors)
    versions = Counter(str(vector["version"]) for vector in vectors)
    tags = Counter(str(item["tag"]) for vector in vectors for item in vector["items"])
    require(dict(presence) == {"0": 166, "1": 85} and len(vectors) == 85 and len(nonempty) == 85 and
            item_count == 2219 and dict(versions) == {"2": 85} and dict(tags) == {"3": 2219},
            "main server presence/vector/version/tag counts mismatch")
    require(cursor["summary"]["items"] == item_count, "main server summary item count mismatch")
    for vector in vectors:
        require(vector["version"] == 2 and vector["count"] == len(vector["items"]),
                "main server vector count/version mismatch")
        for item in vector["items"]:
            raw = bytes.fromhex(item["raw"])
            require(len(raw) == 12 and item["tag"] == 3 and raw[:2] == b"\x03\x00" and
                    int.from_bytes(raw[2:6], "little", signed=True) == -1,
                    "main server item tag/width/PUnP sentinel mismatch")
    return {"mode": 1, "rows": 251, "presence": {"0": 166, "1": 85},
            "present_vectors": 85, "nonempty_vectors": 85, "items": 2219,
            "versions": {"2": 85}, "tags": {"3": 2219}, "PUnP_signed_values": {"-1": 2219},
            "span_bytes": spans, "footer_bytes": footer_bytes, "payload_bytes": total,
            "closure_formula": f"13 + {spans} + 9 = {total}",
            "every_nonempty_vector_closed_to_next_transfer": True,
            "payload_sha256": cursor["payload_sha256"]}


def validate_extra_cursor(cursor: dict[str, Any], expected_side: str) -> dict[str, Any]:
    rows = cursor["rows"]
    require(cursor["member"] == "table_extra_9.dat" and cursor["side"] == expected_side and
            cursor["mode"] == (0 if expected_side == "client" else 1) and len(rows) == 251,
            f"extra cursor identity/mode/row count mismatch: {expected_side}")
    require(cursor["header"] == 12 and rows[0]["start"] == 12,
            f"extra {expected_side}: header mismatch")
    require(all(a["end"] == b["start"] for a, b in zip(rows, rows[1:])),
            f"extra {expected_side}: row spans are not contiguous")
    spans = sum(row["end"] - row["start"] for row in rows)
    total = cursor["end"]
    expected_total = 83927 if expected_side == "client" else 105228
    require(cursor["end"] == rows[-1]["end"] and total == 12 + spans and total == expected_total and
            cursor["footer"] == "", f"extra {expected_side}: EOF closure/footer mismatch")
    if expected_side == "client":
        require(cursor["summary"]["skipped"] == 251 and cursor["summary"]["items"] == 0 and
                all(row["presence"] is None and row["vector"] is None for row in rows),
                "extra client mode-0 skip summary mismatch")
        return {"mode": 0, "rows": 251, "skipped": 251, "presence_reads": 0,
                "span_bytes": spans, "payload_bytes": total,
                "closure_formula": f"12 + sum(spans={spans}) = {total}",
                "payload_sha256": cursor["payload_sha256"]}

    presence = Counter(str(row["presence"]) for row in rows)
    vectors = [row["vector"] for row in rows if row.get("vector") is not None]
    nonempty = [vector for vector in vectors if vector["count"] > 0]
    items = [item for vector in vectors for item in vector["items"]]
    versions = Counter(str(vector["version"]) for vector in vectors)
    tags = Counter(str(item["tag"]) for item in items)
    require(dict(presence) == {"0": 179, "1": 72} and len(vectors) == 72 and
            sum(vector["count"] == 0 for vector in vectors) == 39 and len(nonempty) == 33 and
            len(items) == 76 and dict(versions) == {"2": 72} and dict(tags) == {"3": 76},
            "extra server presence/vector/version/tag counts mismatch")
    require(cursor["summary"]["items"] == 76, "extra server summary item count mismatch")
    for vector in vectors:
        require(vector["version"] == 2 and vector["count"] == len(vector["items"]),
                "extra server vector count/version mismatch")
    return {"mode": 1, "rows": 251, "presence": {"0": 179, "1": 72},
            "present_vectors": 72, "zero_count_vectors": 39, "nonempty_vectors": 33,
            "items": 76, "versions": {"2": 72}, "tags": {"3": 76},
            "span_bytes": spans, "payload_bytes": total,
            "closure_formula": f"12 + sum(spans={spans}) = {total}",
            "every_nonempty_vector_closed_to_next_transfer": True,
            "payload_sha256": cursor["payload_sha256"]}


def load_sources(v5: dict[str, Any]) -> dict[str, Any]:
    artifacts = [artifact_record(path) for path in T53_PATHS]
    source = {record["path"]: read_json(root_path(record["path"]))
              for record in artifacts if record["path"].endswith(".json")}
    source["REPORT.md"] = root_path("scratch/t53/out/REPORT.md").read_text(encoding="utf-8")
    source["DONE.md"] = root_path("scratch/t53/out/DONE.md").read_text(encoding="utf-8")
    discovery = source["scratch/t53/out/discovery_crs_wire.json"]
    require(discovery["L3_fields"] == 0 and discovery["L4"] == 0,
            "t53 field-grade/L4 boundary changed")
    require(discovery["TCrs"]["main_wire"] == "table_9.dat" and
            discovery["TCrs"]["getter_backing"] == "table_extra_9.dat" and
            discovery["TCrs"]["distinct_slots"] is True,
            "t53 TCrs dual-member adjudication changed")
    require(tuple(discovery["trials"]) == EXPECTED_TRIAL_GROUPS,
            "t53 negative trial-group set/order changed")
    main = {
        side: validate_main_cursor(source[f"scratch/t53/out/cursor_crs_main_{side}.json"], side)
        for side in ("client", "server")
    }
    extra = {
        side: validate_extra_cursor(source[f"scratch/t53/out/cursor_crs_extra_{side}.json"], side)
        for side in ("client", "server")
    }
    summaries = discovery["summaries"]
    require(summaries["main_server"]["presence"] == {"0": 166, "1": 85} and
            summaries["main_server"]["items"] == 2219 and
            summaries["extra_server"]["presence"] == {"0": 179, "1": 72} and
            summaries["extra_server"]["counts"]["0"] == 39 and
            summaries["extra_server"]["items"] == 76,
            "discovery summaries disagree with cursor-derived counts")
    fields = {code: source[f"scratch/t53/out/fields_{code}.json"] for code in FIELD_CODES}
    require(all(record["grade"] == "held" for record in fields.values()),
            "one or more t53 PUn* field grades are not held")
    require(fields["PUnP"]["archives"]["main_server"]["histogram"] == {"-1": 2219} and
            fields["PUnP"]["archives"]["extra_server"]["checks"] ==
            {"ordinal_miss": 64, "UID_probe_hit": 74, "ordinal_hit": 12, "UID_probe_miss": 2},
            "PUnP held evidence changed")
    require(fields["PUnJ"]["archives"]["extra_server"]["first_by_check"]["ftjn_miss"]["value"] == 109 and
            fields["PUnJ"]["archives"]["extra_server"]["first_by_check"]["ftjn_miss"]["row"] == 129,
            "PUnJ held counterexample changed")
    require(discovery["EDfx"]["status"] == "editor_only_generated_output_on_traced_route" and
            "Upstream imported" in discovery["EDfx"]["persistence_scope"] and
            discovery["EDsc"]["status"] == "negative_strengthened_no_verified_call_chain",
            "t53 EDfx/EDsc scope changed")
    t50_extra = v5["nation_t9_wire"]["table_extra_9"]["t50_data_side_candidate_profile"]["server"]
    ambiguity = t50_extra["ambiguity"]["ambiguous"]
    require([(item["row"], item["candidates"]) for item in ambiguity] ==
            [(2, [867, 875]), (82, [39439, 39533])],
            "v5 t50 server ambiguity baseline changed")
    extra_server_rows = source["scratch/t53/out/cursor_crs_extra_server.json"]["rows"]
    require(extra_server_rows[2]["start"] == 875 and extra_server_rows[81]["end"] == 39533 and
            extra_server_rows[82]["start"] == 39533 and
            extra_server_rows[81]["end"] - 39439 == 94,
            "t53 sequential reader no longer resolves t50 row-2/row-82 alternatives")
    ledger = read_json(LEDGER_PATH)
    by_id: dict[str, dict[str, Any]] = {}
    for entry in ledger.get("entries", []):
        entry_id = entry.get("id")
        if entry_id in LEDGER_ENTRY_IDS:
            require(entry_id not in by_id, f"duplicate referenced ledger entry: {entry_id}")
            by_id[entry_id] = entry
    require(set(by_id) == set(LEDGER_ENTRY_IDS), "one or more referenced ledger entries are missing")
    prov = v5["incremental_provenance"]
    expected_entries = prov["acceptance_ledger_entries"]
    for entry_id in LEDGER_ENTRY_IDS:
        expected = expected_entries.get(entry_id) if entry_id != "E93" else {
            "kind": "acceptance", "level": "L2", "claim_sha256": E93_CLAIM_SHA256,
        }
        actual = by_id[entry_id]
        require(expected is not None and expected.get("kind") == actual.get("kind") and
                expected.get("level") == actual.get("level") and
                expected.get("claim_sha256") == canonical_sha256(actual["claim"]),
                f"referenced ledger entry mismatch: {entry_id}")
    require(all((by_id[entry_id]["kind"], by_id[entry_id]["level"]) == ("acceptance", "L2")
                for entry_id in ("E91", "E92", "E93")),
            "E91/E92/E93 acceptance grades must remain L2")
    task50 = prov["tasks"]["t50"]
    t50_node = v5["nation_t9_wire"]["t50_L2_cross_validation"]
    require(task50["acceptance_ledger_entry"] == "E91" and
            task50["ledger_status"].startswith("E91 accepts L2 data-side profile only; no L3") and
            t50_node["acceptance_ledger_entry"] == "E91" and
            t50_node["acceptance_ledger_level"] == "L2" and t50_node["evidence_level"]["L3"] == 0 and
            prov["acceptance_ledger_entries"]["E91"]["level"] == "L2" and
            prov["acceptance_ledger_entries"]["E92"]["level"] == "L2",
            "t52 fix1 E91@L2-only provenance guard failed")
    require(prov["t52_ledger_snapshot"]["t52_acceptance_entry"] == "E92" and
            prov["t52_ledger_snapshot"]["t52_acceptance_level"] == "L2",
            "v5 fix1 E92 ledger snapshot guard changed")
    return {"artifacts": artifacts, "discovery": discovery, "fields": fields,
            "main": main, "extra": extra,
            "ledger_entries": by_id, "t50_ambiguity": ambiguity,
            "t53_source": source}


def build_t53_adjudication(data: dict[str, Any]) -> dict[str, Any]:
    discovery = data["discovery"]
    cursor_rows = data["t53_source"]["scratch/t53/out/cursor_crs_extra_server.json"]["rows"]
    trial_groups = [{"id": key, "source_record": copy.deepcopy(discovery["trials"][key])}
                    for key in EXPECTED_TRIAL_GROUPS]
    field_records = {
        code: {
            "grade": data["fields"][code]["grade"],
            "domain_result": data["fields"][code]["gates"]["domain_result"],
            "source_artifact": f"scratch/t53/out/fields_{code}.json",
            "source_record_verbatim": copy.deepcopy(data["fields"][code]),
        }
        for code in FIELD_CODES
    }
    return {
        "source_task": "t53",
        "acceptance_ledger_entry": "E93",
        "acceptance_ledger_level": "L2",
        "acceptance_ledger_claim_sha256": canonical_sha256(data["ledger_entries"]["E93"]["claim"]),
        "status": discovery["status"],
        "scope": "nation.xml#nation[64].TCrs",
        "evidence_level": {"accepted_level": "L2", "L3_fields": 0, "L4": 0},
        "distinct_vector_slots": discovery["TCrs"]["distinct_slots"],
        "main_vector": {
            "member": "table_9.dat",
            "slot": "this+0x188",
            "archive_modes": {"client": data["main"]["client"], "server": data["main"]["server"]},
        },
        "getter_vector": {
            "member": "table_extra_9.dat",
            "slot": "[this+0xb0]+0x48",
            "region": "typed suffix after the t50 name-block portion",
            "typed_selector": 9,
            "archive_modes": {"client": data["extra"]["client"], "server": data["extra"]["server"]},
        },
        "double_eof_closure": {
            "main_table_9": {
                "client": data["main"]["client"]["closure_formula"],
                "server": data["main"]["server"]["closure_formula"],
            },
            "getter_table_extra_9_suffix": {
                "client": data["extra"]["client"]["closure_formula"],
                "server": data["extra"]["server"]["closure_formula"],
            },
            "all_four_archives_reach_eof": True,
            "extra_9_has_separable_footer": False,
        },
        "field_dispositions": field_records,
        "wrong_mode_trial_groups": trial_groups,
        "no_alias_assertion_scope": {
            "distinct_slots": True,
            "recorded_claim": discovery["TCrs"]["no_alias_claim"],
            "scope_limit": "No alias or migration was found in the examined routes; universal absence is not asserted.",
            "universal_absence_asserted": False,
            "accounting": "held_scope_boundary; not an additional failed trial or field occurrence",
        },
        "t50_block_internal_cross_result": {
            "source_acceptance": "E93/L2",
            "scope": "table_extra_9 block-internal ambiguity only",
            "server_row_2": {
                "t50_candidate_offsets": [867, 875],
                "t53_selected_block_start": cursor_rows[2]["start"],
                "t53_prior_row1_version_at": cursor_rows[1]["vector"]["version_at"],
                "t53_prior_row1_count_at": cursor_rows[1]["vector"]["count_at"],
                "t53_prior_row1_count": cursor_rows[1]["vector"]["count"],
            },
            "server_row_82": {
                "t50_candidate_offsets": [39439, 39533],
                "t53_previous_block_end": cursor_rows[81]["end"],
                "t53_selected_block_start": cursor_rows[82]["start"],
                "bytes_consumed_after_earlier_candidate": cursor_rows[81]["end"] - 39439,
                "t50_dual_candidate_columns_retained": True,
            },
            "t9_table_9_no_winner_unchanged": True,
        },
        "EDfx": {
            "status": discovery["EDfx"]["status"],
            "persistence_scope": discovery["EDfx"]["persistence_scope"],
            "conclusion_scope": "editor-only generated output path; upstream input persistence is outside this conclusion",
        },
        "EDsc": {
            "status": discovery["EDsc"]["status"],
            "limits": discovery["EDsc"]["limits"],
            "conclusion": "still no verified call chain; not an absence-of-persistence claim",
        },
        "source_artifacts": copy.deepcopy(data["artifacts"]),
        "source_records_verbatim": {
            "REPORT.md": data["t53_source"]["REPORT.md"],
            "DONE.md": data["t53_source"]["DONE.md"],
            "discovery_crs_wire.json": copy.deepcopy(discovery),
        },
    }


def build_schema(v5: dict[str, Any], data: dict[str, Any]) -> dict[str, Any]:
    schema = copy.deepcopy(v5)
    schema["schema_version"], schema["generated_by"] = 6, "t54"
    wire = schema["nation_t9_wire"]
    adjudication = build_t53_adjudication(data)
    wire["t53_crs_adjudication"] = adjudication

    extra = wire["table_extra_9"]
    old_rejections = copy.deepcopy(v5["nation_t9_wire"]["table_extra_9"]["rejection_records"])
    extra["status"] = "TCrs_getter_typed_suffix_bound; t50_name_block_portion_remains_L2_scoped"
    extra["reader"] = {
        "source_task": "t53",
        "getter_slot": "[this+0xb0]+0x48",
        "region": "typed suffix after the t50 name-block portion",
    }
    extra["mode"] = {"client": 0, "server": 1}
    extra["target_parent_assignment"] = ["nation.xml#nation[64].TCrs getter vector (typed suffix only)"]
    extra["source_discovery_binding_scope"] = (
        "The original t49 slot19 discovery binding and rejected attempts remain verbatim; "
        "the accepted t53 binding is limited to the typed suffix."
    )
    extra["t53_typed_suffix_adjudication"] = {
        "source_task": "t53",
        "source_acceptance": "E93/L2",
        "binding": "TCrs getter vector [this+0xb0]+0x48",
        "region": "typed suffix after the t50 name-block portion",
        "name_block_scope": "t50 L2 name-table basis retained; t53 does not reassign the name prefix",
        "cursor_eof_closure": copy.deepcopy(adjudication["double_eof_closure"]["getter_table_extra_9_suffix"]),
        "rejected_t49_member_mode_attempts_preserved": True,
    }
    require(extra["rejection_records"] == old_rejections and
            extra["rejected_member_mode_attempts_total"] == 6 and
            extra["rejected_member_mode_attempts_for_extra_9"] == 4,
            "v5 table_extra_9 rejected slot19 trials were modified")

    t50_node = wire["t50_L2_cross_validation"]
    old_adjudication = v5["nation_t9_wire"]["t50_L2_cross_validation"]["adjudication"]
    require(old_adjudication.startswith("NO WINNER."), "v5 t50 adjudication no longer starts NO WINNER")
    t50_node["adjudication"] = old_adjudication + " " + T50_NO_WINNER_APPENDIX
    t50_node["t53_block_internal_cross_result"] = copy.deepcopy(adjudication["t50_block_internal_cross_result"])
    require(t50_node["source_records_verbatim"] == v5["nation_t9_wire"]["t50_L2_cross_validation"]["source_records_verbatim"],
            "t50 source records changed during v6 build")

    coverage = schema["coverage"]
    require((coverage["nation_L3_occurrences"], coverage["nation_L3_unique_wire_fields"],
             coverage["nation_held_occurrences"], coverage["nation_negative_records"]) == (30, 30, 20, 7),
            "v5 nation coverage baseline changed")
    coverage["nation_negative_records"] = 7 + len(adjudication["wrong_mode_trial_groups"])
    coverage["nation_t53_negative_trial_groups"] = len(adjudication["wrong_mode_trial_groups"])
    breakdown = coverage["nation_negative_record_breakdown"]
    breakdown["t53_wrong_mode_trial_groups"] = len(adjudication["wrong_mode_trial_groups"])
    breakdown["t53_wrong_mode_trial_ids"] = [item["id"] for item in adjudication["wrong_mode_trial_groups"]]
    breakdown["t53_no_alias_scope_limit_counted_as_failed_trial"] = False
    coverage["nation_coverage_policy"] += (
        " t53 adds eight individually retained negative trial groups to the bounded record total; "
        "the no-alias assertion limit is recorded as a held scope boundary, not a failed trial."
    )

    provenance = schema["incremental_provenance"]
    ledger_entries = provenance.setdefault("acceptance_ledger_entries", {})
    e93 = data["ledger_entries"]["E93"]
    ledger_entries["E93"] = {
        "kind": e93["kind"], "level": e93["level"], "date": e93.get("date"),
        "claim_sha256": canonical_sha256(e93["claim"]),
    }
    tasks = provenance.setdefault("tasks", {})
    payloads = {
        "client_table_9": data["main"]["client"]["payload_sha256"],
        "server_table_9": data["main"]["server"]["payload_sha256"],
        "client_table_extra_9": data["extra"]["client"]["payload_sha256"],
        "server_table_extra_9": data["extra"]["server"]["payload_sha256"],
    }
    tasks["t53"] = {
        "status": "accepted_L2_TCrs_dual_wire_closure_fields_held",
        "acceptance_ledger_entry": "E93",
        "acceptance_ledger_level": "L2",
        "ledger_status": "E93 accepts the dual-wire TCrs adjudication at L2; no schema field is promoted to L3.",
        "evidence_level": {"accepted_level": "L2", "L3_fields": 0, "L4": 0},
        "payload_sha256": payloads,
        "source_artifacts": copy.deepcopy(data["artifacts"]),
        "ledger_claim_sha256": canonical_sha256(e93["claim"]),
    }
    provenance["t54_ledger_snapshot"] = copy.deepcopy(HISTORICAL_LEDGER_SNAPSHOT)
    validate_schema(schema, v5, data)
    return schema


def validate_schema(schema: dict[str, Any], v5: dict[str, Any], data: dict[str, Any]) -> None:
    require((schema.get("schema_version"), schema.get("generated_by")) == (6, "t54"),
            "output is not schema v6")
    for key in PROTECTED_KEYS:
        require(schema.get(key) == v5.get(key), f"v5 protected block changed: {key}")
    for key, value in v5["coverage"].items():
        if not key.startswith("nation_"):
            require(schema["coverage"].get(key) == value, f"v5 non-nation coverage changed: {key}")
    require(len(schema["tables"]) == 8 and len(schema["negative_regressions"]) == 4,
            "v5 table/negative regression counts changed")
    require(schema["nation_static_side"] == v5["nation_static_side"], "nation_static_side changed")
    require(schema["nation_t9_wire"]["table_9"] == v5["nation_t9_wire"]["table_9"],
            "existing table_9 accepted records changed")
    require(schema["nation_t9_wire"]["t50_L2_cross_validation"]["adjudication"].startswith(
                v5["nation_t9_wire"]["t50_L2_cross_validation"]["adjudication"]),
            "v5 NO WINNER adjudication text was not retained as prefix")
    extra_before = v5["nation_t9_wire"]["table_extra_9"]
    extra_after = schema["nation_t9_wire"]["table_extra_9"]
    for key in ("rejection_records", "rejected_member_mode_attempts_total",
                "rejected_member_mode_attempts_for_extra_9", "source_discovery_binding",
                "t50_data_side_candidate_profile", "t50_L2_shape_assessment", "t50_not_a_parent_assignment"):
        require(extra_after[key] == extra_before[key], f"v5 table_extra_9 negative/source record changed: {key}")
    coverage = schema["coverage"]
    require((coverage["nation_L3_occurrences"], coverage["nation_L3_unique_wire_fields"],
             coverage["nation_held_occurrences"], coverage["nation_negative_records"]) == (30, 30, 20, 15),
            "v6 nation totals mismatch")
    t53 = schema["nation_t9_wire"]["t53_crs_adjudication"]
    require(t53["acceptance_ledger_entry"] == "E93" and t53["acceptance_ledger_level"] == "L2" and
            t53["evidence_level"] == {"accepted_level": "L2", "L3_fields": 0, "L4": 0} and
            len(t53["wrong_mode_trial_groups"]) == 8 and
            all(value["grade"] == "held" for value in t53["field_dispositions"].values()),
            "t53 field grade or acceptance-level boundary changed")
    require(schema["nation_t9_wire"]["table_extra_9"]["target_parent_assignment"] ==
            ["nation.xml#nation[64].TCrs getter vector (typed suffix only)"],
            "table_extra_9 binding scope mismatch")
    require(schema["coverage"]["L4"] == schema["nation_t9_wire"]["L4"] == 0,
            "L4 must remain zero")


def summarize_trial(record: dict[str, Any]) -> str:
    def describe(outcome: dict[str, Any]) -> str:
        if outcome["closed"]:
            return f"closed ({outcome['rows']} rows)"
        failure = outcome["first_failure"]
        return f"first failure @{failure['absolute']} ({failure['kind']})"

    if "0" in record or "1" in record:
        return "; ".join(f"mode {mode}: {describe(record[mode])}" for mode in ("0", "1") if mode in record)
    return describe(record)


def render_markdown(v5_md: bytes, schema: dict[str, Any]) -> str:
    t53 = schema["nation_t9_wire"]["t53_crs_adjudication"]
    coverage = schema["coverage"]
    fields = t53["field_dispositions"]
    lines = [
        "## t53 Incremental Addendum", "",
        "This addendum records the E93-accepted TCrs adjudication at L2. It adds wire/backing scope and cursor closure only; no PUn* schema field is promoted to L3. All preceding v5 Markdown bytes are retained as the exact prefix.", "",
        "### TCrs Dual Closure", "",
        "The main TCrs vector is read from `table_9.dat` at `this+0x188`; the getter vector `[this+0xb0]+0x48` is backed by the typed suffix of `table_extra_9.dat`, after the t50 name-block portion. These are distinct vector destinations; the no-alias statement is bounded to examined routes.", "",
        f"- Main server presence: 166 absent / 85 present; 85 nonempty vectors, 2,219 items, all version 2 and tag 3; PUnP is -1 for all 2,219 main items.",
        f"- Getter suffix server presence: 179 absent / 72 present; 39 present zero-count vectors, 33 nonempty vectors, 76 items, all version 2 and tag 3.",
        f"- Main EOF closures: client `{t53['double_eof_closure']['main_table_9']['client']}`; server `{t53['double_eof_closure']['main_table_9']['server']}`.",
        f"- Getter-suffix EOF closures: client `{t53['double_eof_closure']['getter_table_extra_9_suffix']['client']}`; server `{t53['double_eof_closure']['getter_table_extra_9_suffix']['server']}`. No separate extra_9 footer is asserted.", "",
        "### table_extra_9 and t50", "",
        "`table_extra_9.dat` is no longer recorded as wholly unbound: t53 verifies its typed suffix as the TCrs getter backing. The name-block portion remains under t50's L2 name-table profile. The six pre-existing t49 slot19/member-mode rejection records and their original failure details remain unchanged.", "",
        "The v5 t9 framing adjudication remains **NO WINNER**. t53 appends a separate within-block result: server row 2 starts at `@875` after row 1's version-2/count-0 bytes (t50 also retained `@867`); for row 82, the sequential reader consumes 94 bytes beyond the earlier `@39439` candidate and reaches the next block at `@39533`. The t50 source's two candidate columns remain retained.", "",
        "### Held and Negative", "",
        f"All four fields remain held; L3 field promotions = {t53['evidence_level']['L3_fields']}. The aggregate held count remains {coverage['nation_held_occurrences']} (unchanged from v5).", "",
        "| Field | Grade | Preserved domain result |", "|---|---|---|",
    ]
    for code in FIELD_CODES:
        lines.append(f"| `{code}` | `{fields[code]['grade']}` | {fields[code]['domain_result']} |")
    lines += ["", f"The bounded nation negative-record count is {coverage['nation_negative_records']}: seven existing records plus eight individually retained t53 trial groups. The no-alias assertion limit is recorded as a held scope boundary, not a ninth failed trial.", ""]
    for trial in t53["wrong_mode_trial_groups"]:
        result = summarize_trial(trial["source_record"])
        lines.append(f"- `{trial['id']}`: {result}; full source record retained verbatim in `nation_t9_wire.t53_crs_adjudication.wrong_mode_trial_groups`.")
    lines += [
        "", "### EDfx and EDsc", "",
        "EDfx is narrowed to the editor-only generated-output path that was traced; whether its upstream inputs are persisted is outside this conclusion. EDsc remains `negative_strengthened_no_verified_call_chain`; this is not an absence-of-persistence claim.", "",
        "### Provenance", "",
        "E93 is recorded as an `acceptance` / `L2` entry. The t53 discovery sections, field ledgers, REPORT, and DONE are preserved verbatim in the JSON addendum; source hashes and sizes are recorded below. L3 fields = 0; L4 = 0.", "",
        "| t53 source artifact | SHA-256 | Bytes |", "|---|---|---:|",
    ]
    for record in t53["source_artifacts"]:
        lines.append(f"| `{record['path']}` | `{record['sha256']}` | {record['bytes']} |")
    lines += ["", f"Ledger snapshot SHA-256: `{schema['incremental_provenance']['t54_ledger_snapshot']['sha256']}`. L4 remains 0.", ""]
    return v5_md.decode("utf-8") + "\n" + "\n".join(lines)


def render_report(schema: dict[str, Any]) -> str:
    coverage = schema["coverage"]
    t53 = schema["nation_t9_wire"]["t53_crs_adjudication"]
    base = "\n".join([
        "# t54 v6 Merge Report", "",
        "Status: schema v6 generated additively from the SHA-pinned v5/fix1 pair; t53 E93 is accepted at L2.", "",
        "## Result", "",
        "- TCrs main vector: `table_9.dat` / `this+0x188`; getter vector: typed suffix of `table_extra_9.dat` / `[this+0xb0]+0x48`.",
        "- Main server closure: 166/85 presence and 2,219 items; getter suffix: 179/72 presence, 39 zero-count vectors, 76 items. Both members close at EOF in both archives.",
        "- PUnI/PUnT/PUnP/PUnJ remain held; no L3 field mapping is attributed to E93.",
        "- The six v5 slot19 rejection records remain intact. Eight t53 negative trial groups are itemized; nation negative records are 15, held count remains 20.",
        "- The t50 `NO WINNER` t9 framing decision remains intact. t53 only resolves the table_extra_9 internal block candidates and appends that result.",
        "- EDfx scope is editor-only generated output on the traced route; upstream input persistence is outside scope. EDsc remains without a verified call chain.",
        "- Protected v5 tables, regressions, v3 baseline, club auxiliary source, club coverage, and nation_static_side are unchanged.",
        "- L4=0; no game/editor/IDA, network, or Z: access.", "",
        "## Outputs", "",
        "- `reports/club_nation_subtable_schema.json` and `.md`: v6 pair.",
        "- `scratch/t54/out/club_nation_subtable_schema.v5.json` and `.md`: SHA-pinned v5 input snapshots.",
        "- `scratch/t54/out/ledger_snapshot.json`: exact ledger bytes used for E93 provenance.",
        "- `scratch/t54/out/consolidate_v6.py`: deterministic guarded builder with `--help` / `--selftest` / `--build`.",
        "- `scratch/t54/out/verify.py`: independent verifier; it does not import the builder.",
        "- `scripts/t54_spot_v6.py`: independent spot script; it does not import the builder.",
        "- `scratch/t54/out/spot_*.log`: command outputs and anchor regression.", "",
        f"Coverage check: {coverage['nation_L3_occurrences']} L3 / {coverage['nation_L3_unique_wire_fields']} unique / {coverage['nation_held_occurrences']} held / {coverage['nation_negative_records']} negative; t53 groups={len(t53['wrong_mode_trial_groups'])}.", "",
        "## Audit", "",
        f"v5 JSON SHA-256 `{V5_JSON_SHA256}`; v5 Markdown SHA-256 `{V5_MD_SHA256}`. E93 claim SHA-256 `{t53['acceptance_ledger_claim_sha256']}`. Verification commands and results are in `spot_*.log`.", "",
    ])
    return f"{base}\n## fix1\n{FIX1_ROOT_CAUSE}\n{FIX1_REMEDY}\n"


def verification_logs_passed() -> bool:
    expected = {
        "spot_builder_help.log": ("usage:",),
        "spot_builder_selftest.log": ("SELFTEST PASS",),
        "spot_build.log": ("t54 schema v6 build complete",),
        "spot_verify_help.log": ("usage:",),
        "spot_verify_selftest.log": ("selftest PASS",),
        "spot_verify.log": ("t54 independent verification PASS",),
        "spot_spotcheck_help.log": ("usage:",),
        "spot_spotcheck_selftest.log": ("selftest PASS",),
        "spot_schema.log": ("t54 independent spot check PASS",),
        "spot_t01_anchors.log": ("7/7",),
        "spot_fix1.log": ("ENTRY-SCOPED PASS", "E94 excluded"),
    }
    for name, markers in expected.items():
        path = OUT_DIR / name
        if not path.is_file():
            return False
        text = path.read_text(encoding="utf-8")
        if any(marker not in text for marker in markers):
            return False
    return True


def render_done(schema: dict[str, Any], verified: bool | None = None) -> str:
    if verified is None:
        verified = verification_logs_passed()
    checked = "[x]" if verified else "[ ]"
    base = "\n".join([
        "# t54 DONE", "",
        "- [x] v5/fix1 JSON and Markdown hashes pinned and snapshotted.",
        "- [x] t53 E93 validated as acceptance/L2; no L3 field promotion; L4=0.",
        "- [x] TCrs main and getter vectors recorded as separate EOF-closed members.",
        "- [x] table_extra_9 typed-suffix binding added while preserving t49's six rejection records and t50 source profile.",
        "- [x] t50 NO WINNER string retained as prefix with a separate t53 block-internal note.",
        "- [x] Four PUn* fields remain held; held count stays at 20; eight t53 negative trial groups are listed; negative count is 15.",
        "- [x] Protected v5 sections and all club counters compare equal to the v5 snapshot.",
        f"- {checked} Builder, verifier, spot script, and t01 anchors passed; see `spot_*.log`.", "",
        "No game/editor/IDA was launched; no network or Z: access was used.", "",
    ])
    return f"{base}\n## fix1\n{FIX1_ROOT_CAUSE}\n{FIX1_REMEDY}\n"


def build_all() -> tuple[dict[str, Any], str, str, str, dict[str, Any], bytes, bytes]:
    v5, v5_json_raw, v5_md_raw = load_v5()
    data = load_sources(v5)
    schema = build_schema(v5, data)
    markdown = render_markdown(v5_md_raw, schema)
    report = render_report(schema)
    done = render_done(schema)
    return schema, markdown, report, done, data, v5_json_raw, v5_md_raw


def guarded_write(path: Path, content: bytes, allowed: tuple[bytes, ...]) -> None:
    if path.exists():
        current = path.read_bytes()
        require(current in allowed or current == content,
                f"refusing to overwrite unexpected existing output: {path.relative_to(ROOT)}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)


def write_outputs(schema: dict[str, Any], markdown: str, report: str, done: str,
                  data: dict[str, Any], v5_json_raw: bytes, v5_md_raw: bytes) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    public_json = (json.dumps(schema, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    public_md = markdown.encode("utf-8")
    pending_done = render_done(schema, verified=False).encode("utf-8")
    guarded_write(V5_JSON_SNAPSHOT, v5_json_raw, (v5_json_raw,))
    guarded_write(V5_MD_SNAPSHOT, v5_md_raw, (v5_md_raw,))
    allowed_json_inputs = [v5_json_raw]
    if PUBLIC_JSON.is_file():
        prior_json = PUBLIC_JSON.read_bytes()
        if sha256_bytes(prior_json) == INTERIM_V6_JSON_SHA256:
            allowed_json_inputs.append(prior_json)
    guarded_write(PUBLIC_JSON, public_json, tuple(allowed_json_inputs))
    allowed_md_inputs = [v5_md_raw]
    if PUBLIC_MD.is_file():
        prior_md = PUBLIC_MD.read_bytes()
        if sha256_bytes(prior_md) == INTERIM_V6_MD_SHA256:
            allowed_md_inputs.append(prior_md)
    guarded_write(PUBLIC_MD, public_md, tuple(allowed_md_inputs))
    guarded_write(OUT_DIR / "REPORT.md", report.encode("utf-8"), ())
    guarded_write(OUT_DIR / "DONE.md", done.encode("utf-8"), (pending_done,))
    print(f"WROTE {PUBLIC_JSON.relative_to(ROOT)}")
    print(f"WROTE {PUBLIC_MD.relative_to(ROOT)}")
    print(f"FROZEN {V5_JSON_SNAPSHOT.relative_to(ROOT)}")
    print(f"FROZEN {V5_MD_SNAPSHOT.relative_to(ROOT)}")
    print("t54 schema v6 build complete")


def selftest() -> None:
    require(sha256_bytes(b"") == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "empty SHA-256 selftest failed")
    sample = {"schema_version": 5, "coverage": {"held": 20}}
    copied = copy.deepcopy(sample)
    copied["schema_version"] = 6
    require(sample["schema_version"] == 5 and copied["coverage"] == sample["coverage"],
            "copy-on-increment selftest failed")
    require(len(EXPECTED_TRIAL_GROUPS) == 8 and len(FIELD_CODES) == 4 and
            len(LEDGER_ENTRY_IDS) == 6, "t53 group/held-field/ledger-entry constants selftest failed")
    print("SELFTEST PASS: v5 guarded increment, eight trial groups, four held fields, L2 provenance boundary")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Merge t53 E93/L2 TCrs dual-wire evidence into schema v6 without changing v5 protected blocks.")
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--selftest", action="store_true", help="validate pinned sources and merge invariants without writing")
    modes.add_argument("--build", action="store_true", help="write the v6 public schema pair and t54 outputs")
    args = parser.parse_args(argv)
    try:
        if args.selftest:
            schema, _, _, _, _, _, _ = build_all()
            require(schema["coverage"]["nation_negative_records"] == 15, "selftest nation negative total")
            print("SELFTEST PASS: v5 SHA pinned; protected blocks unchanged; E87/E89/E90/E91/E92/E93 entry-level guards; E94 excluded; TCrs dual EOF closure; 8 negative trial groups; 4 fields held; L4=0")
            return 0
        schema, markdown, report, done, data, v5_json_raw, v5_md_raw = build_all()
        write_outputs(schema, markdown, report, done, data, v5_json_raw, v5_md_raw)
        return 0
    except CheckFailure as exc:
        print(f"CHECK FAILED: {exc}", file=sys.stderr)
        return 1
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"FATAL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
