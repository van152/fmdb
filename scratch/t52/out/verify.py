#!/usr/bin/env python3
"""Independent verifier for the t52 schema v5 merge."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
V4_JSON = OUT / "club_nation_subtable_schema.v4.json"
V4_MD = OUT / "club_nation_subtable_schema.v4.md"
V5_JSON = ROOT / "reports" / "club_nation_subtable_schema.json"
V5_MD = ROOT / "reports" / "club_nation_subtable_schema.md"
V4_JSON_SHA256 = "7567606c8082f53296caf9c07088489614c364d214e25ba3d4f6390e17d25932"
V4_MD_SHA256 = "ee47e88a4f7d82ecb996022dc7465975eff51bb153869f99adb987dc46ee3c0c"
LEDGER_SNAPSHOT = OUT / "ledger_snapshot.json"
LEDGER_SOURCE = "scratch/t01/LEDGER.json"

ARTIFACTS = {
    "t47": ["scratch/t47/out/discovery_nation_unknown.json", "scratch/t47/out/fields_nation_tax.json",
            "scratch/t47/out/cursor_nation_tax.json", "scratch/t47/out/REPORT.md"],
    "t49": ["scratch/t49/out/discovery_t9_wire.json", "scratch/t49/out/REPORT.md",
            "scratch/t49/out/cursor_t9_client.json", "scratch/t49/out/cursor_t9_server.json",
            *[f"scratch/t49/out/fields_{name}.json" for name in ("Nntp", "Nctp", "Nrtp", "NTRv", "NWGv", "NSps", "Nfmp", "NCro")]],
    "t50": ["scratch/t50/out/REPORT.md", "scratch/t50/out/profile_t9.json", "scratch/t50/out/grammar_diff_t9.json",
            "scratch/t50/out/verify.py", "scratch/t50/out/DONE.md", "scratch/t50/out/profiles/table_client_9.rows.jsonl",
            "scratch/t50/out/profiles/table_client_extra_9.rows.jsonl",
            "scratch/t50/out/profiles/table_server_9.rows.jsonl",
            "scratch/t50/out/profiles/table_server_extra_9.rows.jsonl"],
    "t51": ["scratch/t51/out/discovery_unknown2.json", "scratch/t51/out/REPORT.md",
            "scratch/t51/out/cursor_table_9_client.json", "scratch/t51/out/cursor_table_9_server.json",
            "scratch/t51/out/cursor_table_10_server.json",
            "scratch/t51/out/fields_Nrvn.json", "scratch/t51/out/fields_Nftb.json", "scratch/t51/out/fields_Calt.json"],
}

EXPECTED_SHA256 = {
    "scratch/t47/out/discovery_nation_unknown.json": "2c0a5b535fd280c1c1c46825b5e1b8ea7206ff5d5be40d13c7ed8d241b05b5d3",
    "scratch/t47/out/fields_nation_tax.json": "b7b57595a3b8e4d60458f14f1e923b660e751304fdab1feff7c85b035a4af9b7",
    "scratch/t47/out/cursor_nation_tax.json": "42b3e88db86c725221a23cd7b2bdd6e3d4c1b089d758ed844a56f84e103f2ea9",
    "scratch/t47/out/REPORT.md": "c0742c66ad5ed0819b222983c046c1b7ec83db02fdcbe67bd7063ea0eab563f8",
    "scratch/t49/out/discovery_t9_wire.json": "f3b9f06535bbdca2876f86caaf3f0c592969028281600b0e678c3912f6f50b9a",
    "scratch/t49/out/REPORT.md": "0c0b1129c1edb5758d49403351950238383b5369d089097c9bfb8b0fe6d23974",
    "scratch/t49/out/cursor_t9_client.json": "82a733f8157b1518d38dadafcc33249a34fa3d563ec2a37c4d60740bf1f6b004",
    "scratch/t49/out/cursor_t9_server.json": "ccf78eba3d1d845b530550987b093b120ca20dd9e4a079da3970ca590259e69b",
    "scratch/t49/out/fields_NCro.json": "d3f1f0479587071389718005b12ce5820d0991ec7230db136f71d3efb1ada144",
    "scratch/t49/out/fields_NSps.json": "c4c420461c3de270d9168af06719d54b5885cffed540680629ff0ec588febbae",
    "scratch/t49/out/fields_NTRv.json": "c4afdc411be456f418dd854e407a491738d235d73777c78055fdff53c4c6c15a",
    "scratch/t49/out/fields_NWGv.json": "681db4ba1d42c480b86fa587cab1c8b459e8ea5e15890828e189061b6f5896ae",
    "scratch/t49/out/fields_Nctp.json": "75f983bfa703bdde1cab4b642404ea07f2251d806d6e67aa230d78331f682562",
    "scratch/t49/out/fields_Nfmp.json": "d1b8e84be431991682bb6a347b085a4c2d41241be757251a7234b656a42ecd14",
    "scratch/t49/out/fields_Nntp.json": "21a342822440328f3c9515d2208556306455262a486d3708d0d56771237de22a",
    "scratch/t49/out/fields_Nrtp.json": "d93a94262d035fe5e5f4938125b7879b9d5f80b8fad232fa1302dc6e5b9e5e22",
    "scratch/t50/out/REPORT.md": "8994cc39ce7b67227f9f372c18ef997a173ade3e88ca583f6e4bb4870770b0ba",
    "scratch/t50/out/profile_t9.json": "95a413310116af0b123128f7e819a47e94aa01556000fef0ab60bfc6d8c1fa06",
    "scratch/t50/out/grammar_diff_t9.json": "31f1fb7628d0f5d81acfea89e82b77f610942af188b20bc31bb9225148f81477",
    "scratch/t50/out/verify.py": "179b9c8fdacbff94c2ae6150ec7c08fdf48781c9c462d28b51c2e1617242486c",
    "scratch/t50/out/DONE.md": "fae026b837e96e59645fbb3effdf3e59c1b1fd1532bb4a3e69545c40ab82f3f2",
    "scripts/t50_nation_t9_profile.py": "659de87f7799ee81242ac75f036068fd910c8fdcbf78ff231cdf438261de7b80",
    "scratch/cmd/t50_spot.py": "aa5ee28b5421cdee0afc36079738cbd400288b1c8305a043ca75549da6efff16",
    "scratch/t50/out/profiles/table_client_9.rows.jsonl": "5c5d18c112813371e2b9fcee42046a481b7467337db3d21d0143ac539d6b0d1a",
    "scratch/t50/out/profiles/table_client_extra_9.rows.jsonl": "98817ff54bdfc6e4695ca415299a63f0e5985a0ddd039bbcee4e8dca4a583249",
    "scratch/t50/out/profiles/table_server_9.rows.jsonl": "2d8b7b92c350b287e1cc1525e1cb1f98899fda2881cd7c33e22d655902b031db",
    "scratch/t50/out/profiles/table_server_extra_9.rows.jsonl": "188c68e607b034caa0ce1283edd185780bbb0511b574e88810cd3d1caab09fd4",
    "scratch/t51/out/discovery_unknown2.json": "3b384f82cab9417a1bc41b0dfded0f15b96f79e354928c87235993045fe538f6",
    "scratch/t51/out/REPORT.md": "3821c9a3e9da24a8e2c1fbd49929a4a425d5be39e9bcaa28dc594fb1bacc517b",
    "scratch/t51/out/cursor_table_9_client.json": "4f70c334ab30763e5ece062f493dfb9378d40ecd42d41aecdea3ce302b75a3e7",
    "scratch/t51/out/cursor_table_9_server.json": "6bff39851db865fec2fb18808ccfc3220bbbb367acc642a7328d459e26b0e670",
    "scratch/t51/out/cursor_table_10_server.json": "8236f250af16a120a23fb241755df9d66e7f741fcc6baf2c3cc8e1a61f61bf40",
    "scratch/t51/out/fields_Nrvn.json": "c663f14aed3a1cceccff3adfad55b7f0a23a15b63e3f58c0a8db0273e1191537",
    "scratch/t51/out/fields_Nftb.json": "69f83b15f3143e2305846967d36d6afc340b6626222527a04232fc90da1fa7b0",
    "scratch/t51/out/fields_Calt.json": "91a3ad1da9f738038660288071732c4e90f6590485c6e3def2ce40e5789e89d2",
}

PROTECTED_KEYS = ("tables", "negative_regressions", "v3_baseline", "club_auxiliary_sources", "nation_data_side_status")
T9_PARENTS = ("Nntp", "Nctp", "Nrtp", "NTRv", "NWGv", "NSps", "Nfmp", "NCro")


class VerifyFailure(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerifyFailure(message)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_sha256(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256_bytes(raw)


def read_json(path: Path) -> Any:
    require(path.is_file(), f"missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def read_root_json(path: str) -> Any:
    return read_json(ROOT / path)


def read_jsonl(path: str) -> list[dict[str, Any]]:
    full = ROOT / path
    require(full.is_file(), f"missing JSONL: {path}")
    return [json.loads(line) for line in full.read_text(encoding="ascii").splitlines() if line]


def verify_artifact_hashes(schema: dict[str, Any]) -> int:
    groups = schema["incremental_provenance"]["tasks"]
    checks = 0
    for task, paths in ARTIFACTS.items():
        records = groups[task]["source_artifacts"]
        by_path = {record["path"]: record for record in records}
        require(set(by_path) == set(paths), f"{task}: provenance source artifact set mismatch")
        for path in paths:
            raw = (ROOT / path).read_bytes()
            digest = sha256_bytes(raw)
            require(digest == EXPECTED_SHA256[path], f"source SHA mismatch: {path}")
            require(by_path[path]["sha256"] == digest and by_path[path]["bytes"] == len(raw),
                    f"provenance hash/size mismatch: {path}")
            checks += 1
    task50 = groups["t50"]
    evidence_paths = {item["path"]: item for item in task50["acceptance_evidence"]}
    expected_evidence_paths = ("scripts/t50_nation_t9_profile.py", "scratch/cmd/t50_spot.py")
    require(set(evidence_paths) == set(expected_evidence_paths), "t50 E91 acceptance evidence set mismatch")
    for path in expected_evidence_paths:
        raw = (ROOT / path).read_bytes()
        digest = sha256_bytes(raw)
        require(digest == EXPECTED_SHA256[path] and evidence_paths[path]["sha256"] == digest and
                evidence_paths[path]["bytes"] == len(raw), f"t50 acceptance evidence hash/size mismatch: {path}")
        checks += 1
    ledger_prov = schema["incremental_provenance"]
    snapshot_meta = ledger_prov["t52_ledger_snapshot"]
    snapshot_raw = LEDGER_SNAPSHOT.read_bytes()
    require(snapshot_meta["path"] == "scratch/t52/out/ledger_snapshot.json" and
            snapshot_meta["live_source_path"] == LEDGER_SOURCE and
            sha256_bytes(snapshot_raw) == snapshot_meta["sha256"] and
            len(snapshot_raw) == snapshot_meta["bytes"],
            "t52 frozen ledger snapshot SHA/size mismatch")
    snapshot = json.loads(snapshot_raw.decode("utf-8"))
    live = read_root_json(LEDGER_SOURCE)
    used_ids = ["E87", "E89", "E90", "E91", "E92"]
    require(snapshot_meta["entries_used"] == used_ids and
            snapshot_meta["t50_acceptance_entry"] == "E91" and snapshot_meta["t50_acceptance_level"] == "L2" and
            snapshot_meta["t52_acceptance_entry"] == "E92" and snapshot_meta["t52_acceptance_level"] == "L2",
            "v5 ledger provenance snapshot scope mismatch")
    snapshot_entries = {entry.get("id"): entry for entry in snapshot.get("entries", [])}
    live_entries = {entry.get("id"): entry for entry in live.get("entries", [])}
    for entry_id in used_ids:
        require(entry_id in snapshot_entries and live_entries.get(entry_id) == snapshot_entries[entry_id],
                f"live ledger entry changed or is missing: {entry_id}")
        expected_level = "L2" if entry_id in ("E91", "E92") else "L3"
        require((snapshot_entries[entry_id].get("kind"), snapshot_entries[entry_id].get("level")) ==
                ("acceptance", expected_level), f"ledger entry grade mismatch: {entry_id}")
        record = ledger_prov["acceptance_ledger_entries"][entry_id]
        require(record["kind"] == "acceptance" and record["level"] == expected_level and
                record["claim_sha256"] == canonical_sha256(snapshot_entries[entry_id]["claim"]),
                f"v5 ledger acceptance provenance mismatch: {entry_id}")
        checks += 1
    return checks + 1


def verify_field_ledgers(schema: dict[str, Any]) -> int:
    static = schema["nation_static_side"]
    t47 = read_root_json("scratch/t47/out/fields_nation_tax.json")
    t47_out = static["Ntxr"]
    require(t47_out["source_field_ledger"] == t47, "t47 source ledger changed in v5")
    require(len(t47_out["fields"]) == 9, "Ntxr field count")
    checks = 0
    for code, source in t47["fields"].items():
        field = next(item for item in t47_out["fields"] if item["code"] == code)
        require(field["source_record"] == source, f"Ntxr/{code}: source record differs")
        require(field["grade"] == source["status"], f"Ntxr/{code}: grade differs")
        if source["status"] == "L3":
            require(field["item_relative_offset"] == source["accepted_item_offset"], f"Ntxr/{code}: L3 offset differs")
        else:
            require(field["candidate_item_relative_offset"] == source["static_item_offset"], f"Ntxr/{code}: held candidate offset differs")
        checks += 1

    for parent in T9_PARENTS:
        source = read_root_json(f"scratch/t49/out/fields_{parent}.json")
        output = schema["nation_t9_wire"]["table_9"]["parents"][parent]
        require(output["source_field_ledger"] == source, f"t49/{parent}: field ledger changed")
        require(len(output["fields"]) == len(source["fields"]), f"t49/{parent}: field count")
        for code, source_record in source["fields"].items():
            field = next(item for item in output["fields"] if item["code"] == code)
            require(field["source_record"] == source_record, f"t49/{parent}/{code}: source record differs")
            require(field["grade"] == source_record["grade"], f"t49/{parent}/{code}: grade changed")
            require(field["accepted_item_offset"] == source_record.get("accepted_item_offset"),
                    f"t49/{parent}/{code}: accepted offset changed")
            require(field["static_item_offset"] == source_record.get("static_item_offset"),
                    f"t49/{parent}/{code}: candidate offset changed")
            checks += 1

    for parent in ("Nrvn", "Nftb", "Calt"):
        source = read_root_json(f"scratch/t51/out/fields_{parent}.json")
        require(static["t51_followup"]["field_ledgers"][parent] == source, f"t51/{parent}: source ledger changed")
        checks += len(source["fields"])
    require((schema["coverage"]["nation_L3_occurrences"], schema["coverage"]["nation_L3_unique_wire_fields"],
             schema["coverage"]["nation_held_occurrences"]) == (30, 30, 20), "nation field coverage counts")
    require((schema["nation_t9_wire"]["table_9"]["grade_totals"]["L3"],
             schema["nation_t9_wire"]["table_9"]["grade_totals"]["held"]) == (17, 13), "t49 summary totals")
    return checks + 2


def verify_crosswalk_and_conflict(schema: dict[str, Any]) -> int:
    t9_wire = schema["nation_t9_wire"]
    c = t9_wire["t51_t47_t49_cross_walk"]
    source_pairs = [
        ("t9_client_t49_to_t51", "scratch/t49/out/cursor_t9_client.json", "scratch/t51/out/cursor_table_9_client.json"),
        ("t9_server_t49_to_t51", "scratch/t49/out/cursor_t9_server.json", "scratch/t51/out/cursor_table_9_server.json"),
        ("t10_server_t47_to_t51", "scratch/t47/out/cursor_nation_tax.json", "scratch/t51/out/cursor_table_10_server.json"),
    ]
    checks = 0
    keys = ("row", "wire13", "legacy14", "end", "identity_at", "length", "identity", "wire_sha256")
    for name, left_path, right_path in source_pairs:
        left, right = read_root_json(left_path), read_root_json(right_path)
        if "nation_tax" in left_path:
            left = left["server"]
        left_rows, right_rows = left["rows"], right["rows"]
        require(len(left_rows) == len(right_rows) == 251, f"{name}: row counts")
        require(all(all(a.get(key) == b.get(key) for key in keys) for a, b in zip(left_rows, right_rows)),
                f"{name}: row-level cross-walk mismatch")
        stored = c[name]
        require(stored["full_row_record_matches"] is True and stored["rows_left"] == 251 and stored["rows_right"] == 251,
                f"{name}: stored cross-walk status")
        checks += 1

    t49 = {side: read_root_json(f"scratch/t49/out/cursor_t9_{side}.json")["rows"] for side in ("client", "server")}
    t50 = {side: read_jsonl(f"scratch/t50/out/profiles/table_{side}_9.rows.jsonl") for side in ("client", "server")}
    stored_conflict = t9_wire["t50_L2_cross_validation"]["row_boundary_conflict"]
    stored_tail_crosswalk = t9_wire["t50_identity_tail_crosswalk"]
    for side in ("client", "server"):
        old, new = t49[side], t50[side]
        require(len(old) == len(new) == 251, f"t50 {side}: row counts")
        offset_deltas = [b["offset"] - a["wire13"] for a, b in zip(old, new)]
        length_deltas = [b["len"] - a["length"] for a, b in zip(old, new)]
        identity_equal = [b["identity"]["ordinal"] == a["identity"][0] and
                          b["identity"]["row_id"] == a["identity"][1] and
                          b["identity"]["repeated_id"] == a["identity"][2]
                          for a, b in zip(old, new)]
        identity_tail_start_equal = [b["offset"] + b["identity"]["tail_offset_in_row"] == a["identity_at"]
                                     for a, b in zip(old, new)]
        hash_equal = [sha256_bytes(bytes.fromhex(b["raw_hex"])) == a["wire_sha256"]
                      for a, b in zip(old, new)]
        require(offset_deltas == [0] + [1] * 250, f"t50 {side}: offset delta pattern")
        require(length_deltas == [1] + [0] * 250, f"t50 {side}: length delta pattern")
        require(all(identity_equal) and all(identity_tail_start_equal) and not any(hash_equal),
                f"t50 {side}: identity-tail/hash conflict pattern")
        record = stored_conflict[side]
        require(record["start_offset_delta_t50_minus_t49"] == {"row_0": 0, "rows_1_to_250": 1},
                f"t50 {side}: stored offset conflict")
        require(record["row_length_delta_t50_minus_t49"] == {"row_0": 1, "rows_1_to_250": 0},
                f"t50 {side}: stored length conflict")
        require(record["identity_ladder_matches"] == 251 and record["t50_raw_row_sha_matches_t49_wire_sha"] == 0 and
                record["full_row_spans_match"] == 0 and record["conflict"] is True,
                f"t50 {side}: stored conflict summary")
        require(stored_tail_crosswalk[side]["rows_compared"] == 251 and
                stored_tail_crosswalk[side]["absolute_identity_tail_starts_match"] == 251,
                f"t50 {side}: separate absolute identity-tail cross-walk")
        checks += 1
    adjudication = t9_wire["t50_L2_cross_validation"]["adjudication"]
    require(adjudication == "NO WINNER. Preserve both framings as source-specific alternatives. The t49 E89 accepted field ledger remains unchanged; t50 is an L1/L2 candidate profile, not the winning cursor and not a field-grade promotion.",
            "t49/t50 NO WINNER record changed")
    require(t9_wire["table_9"]["field_locator_preservation"].startswith("All 17 t49 accepted L3 field locators"),
            "t49 field locators were not explicitly preserved")
    return checks + 2


def verify_t50_delivery(schema: dict[str, Any]) -> int:
    node = schema["nation_t9_wire"]["t50_L2_cross_validation"]
    profile = read_root_json("scratch/t50/out/profile_t9.json")
    diff = read_root_json("scratch/t50/out/grammar_diff_t9.json")
    report = (ROOT / "scratch/t50/out/REPORT.md").read_text(encoding="utf-8")
    done = (ROOT / "scratch/t50/out/DONE.md").read_text(encoding="utf-8")
    embedded = node["source_records_verbatim"]
    require(embedded["REPORT.md"] == report and embedded["DONE.md"] == done,
            "t50 report/DONE text is not preserved verbatim")
    require(embedded["profile_t9.json"] == profile and embedded["grammar_diff_t9.json"] == diff,
            "t50 machine-readable source records changed")
    require(node["evidence_level"] == profile["evidence_level"] and profile["evidence_level"]["L3"] == 0 and
            profile["evidence_level"]["L4"] == 0, "t50 grade discipline changed")
    require(node["fields_named"] is False and node["target_ordinals_joined"] is False,
            "t50 scope was promoted")
    extra = schema["nation_t9_wire"]["table_extra_9"]["t50_data_side_candidate_profile"]
    require(extra["client"]["candidate_block_walks"] == 1 and extra["server"]["candidate_block_walks"] == 4,
            "t50 sidecar block-walk counts")
    require(extra["server"]["ambiguity"]["ambiguous_block_count"] == 2 and
            [item["row"] for item in extra["server"]["ambiguity"]["ambiguous"]] == [2, 82],
            "t50 sidecar ambiguity findings")
    require(schema["nation_t9_wire"]["table_extra_9"]["target_parent_assignment"] == [] and
            schema["nation_t9_wire"]["table_extra_9"]["t50_not_a_parent_assignment"] is True,
            "table_extra_9 must remain unassigned")
    section = report.split("## 6. 明确的负结果与未解项", 1)[1].split("## 7. 边界与合规", 1)[0]
    report_items = re.findall(r"(?m)^\s*[1-7]\.\s", section)
    require(len(report_items) == 7 and schema["coverage"]["nation_t50_negative_report_items"] == 7,
            "t50 numbered negative/unresolved findings count")
    require(schema["coverage"]["nation_negative_records"] == 7,
            "bounded nation negative record total changed")
    task50 = schema["incremental_provenance"]["tasks"]["t50"]
    ledger = read_root_json("scratch/t01/LEDGER.json")
    e91 = [entry for entry in ledger["entries"] if entry.get("id") == "E91"]
    require(len(e91) == 1 and (e91[0].get("kind"), e91[0].get("level")) == ("acceptance", "L2") and
            node["acceptance_ledger_entry"] == task50["acceptance_ledger_entry"] == "E91" and
            task50["ledger_status"].startswith("E91 accepts L2 data-side profile only; no L3"),
            "t50 E91 provenance does not match the live acceptance/L2 ledger record")
    require(node["acceptance_ledger_level"] == "L2" and node["evidence_level"]["L3"] == 0 and
            schema["incremental_provenance"]["t52_ledger_snapshot"]["t50_acceptance_level"] == "L2",
            "t50 acceptance must remain L2 with L3=0")
    shape = schema["nation_t9_wire"]["table_extra_9"]["t50_L2_shape_assessment"]
    require(shape["acceptance_ledger_entry"] == "E91" and shape["target_parent_assignment"] == [] and
            "ordinal|name_len|name" in shape["recorded_shape"], "t50 sidecar L2 shape/assignment scope")

    def reject_t50_field_attribution(value: Any, location: str) -> None:
        if isinstance(value, dict):
            require(value.get("source_task") != "t50" and value.get("field_source_task") != "t50" and
                    value.get("grade_source_task") != "t50" and value.get("acceptance_ledger_entry") != "E91",
                    f"t50 field-grade attribution found in {location}")
            for key, child in value.items():
                reject_t50_field_attribution(child, f"{location}.{key}")
        elif isinstance(value, list):
            for index, child in enumerate(value):
                reject_t50_field_attribution(child, f"{location}[{index}]")

    for label, value in (("nation_static_side", schema["nation_static_side"]),
                         ("nation_t9_wire.table_9", schema["nation_t9_wire"]["table_9"]),
                         ("tables", schema["tables"])):
        reject_t50_field_attribution(value, label)
    return 18


def verify_v4_preservation(schema: dict[str, Any], markdown: str) -> int:
    require(V4_JSON.is_file() and V4_MD.is_file(), "frozen v4 snapshots missing")
    v4_json_raw, v4_md_raw = V4_JSON.read_bytes(), V4_MD.read_bytes()
    require(sha256_bytes(v4_json_raw) == V4_JSON_SHA256, "frozen v4 JSON SHA mismatch")
    require(sha256_bytes(v4_md_raw) == V4_MD_SHA256, "frozen v4 Markdown SHA mismatch")
    baseline = json.loads(v4_json_raw.decode("utf-8"))
    for key in PROTECTED_KEYS:
        require(schema.get(key) == baseline.get(key), f"protected v4 block changed: {key}")
    require(len(schema["tables"]) == 8 and len(schema["negative_regressions"]) == 4,
            "v4 table/negative regression counts changed")
    for key, value in baseline["coverage"].items():
        require(schema["coverage"].get(key) == value, f"v4 coverage field changed: {key}")
    require(markdown.startswith(v4_md_raw.decode("utf-8").rstrip() + "\n\n## t52 Incremental Addendum"),
            "v4 Markdown was not retained verbatim as prefix")
    require((schema.get("schema_version"), schema.get("generated_by")) == (5, "t52"), "schema version metadata")
    require(schema["nation_t9_wire"]["L4"] == schema["nation_static_side"]["L4"] == 0,
            "nation L4 must be zero")
    return 1 + len(PROTECTED_KEYS) + len(baseline["coverage"]) + 4


def selftest() -> int:
    sample_left = [{"row": 0, "wire13": 13, "length": 5, "identity": [0, 7, 7]}]
    sample_right = [{"row": 0, "offset": 13, "len": 6, "identity": {"ordinal": 0, "row_id": 7, "repeated_id": 7}}]
    require(sample_right[0]["offset"] - sample_left[0]["wire13"] == 0, "selftest offset equality")
    require(sample_right[0]["len"] - sample_left[0]["length"] == 1, "selftest length conflict")
    require(sample_right[0]["identity"]["row_id"] == sample_left[0]["identity"][1], "selftest identity match")
    require(sha256_bytes(b"") == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "selftest SHA")
    return 0


def verify_all() -> int:
    schema = read_json(V5_JSON)
    markdown = V5_MD.read_text(encoding="utf-8")
    checks = verify_v4_preservation(schema, markdown)
    checks += verify_artifact_hashes(schema)
    checks += verify_field_ledgers(schema)
    checks += verify_t50_delivery(schema)
    checks += verify_crosswalk_and_conflict(schema)
    print(f"t52 independent verification PASS ({checks} check groups/items)")
    print("v4 protected sections: byte-exact source snapshots and structural equality verified")
    print("nation fields: t47 7 L3/2 held; t49 17 L3/13 held; t51 6 L3/5 held")
    print("t50: E91 accepts L2 data-side profile only; L3 field attribution stays zero and sidecar remains unassigned")
    print("t49/t50: absolute identity-tail starts cross-walk 251/251 per archive; full spans conflict; NO WINNER")
    print("t51 cross-walk: all three 251-row source pairs match; L4=0")
    return checks


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Independently verify t52-fix1 E91 provenance, source hashes, protected v4 blocks, field grades, and the unchanged t49/t50 NO WINNER record.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--selftest", action="store_true", help="run isolated verifier selftests")
    group.add_argument("--check", action="store_true", help="verify the v5 schema against frozen baseline and source artifacts")
    args = parser.parse_args(argv)
    try:
        if args.selftest:
            selftest()
            print("t52 verifier selftest PASS")
            return 0
        verify_all()
        return 0
    except VerifyFailure as exc:
        print(f"CHECK FAILED: {exc}", file=sys.stderr)
        return 1
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"FATAL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
