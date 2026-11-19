#!/usr/bin/env python3
"""Independent verifier for the t54 schema v6 merge; does not import the builder."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
PUBLIC_JSON = ROOT / "reports" / "club_nation_subtable_schema.json"
PUBLIC_MD = ROOT / "reports" / "club_nation_subtable_schema.md"
V5_JSON = OUT / "club_nation_subtable_schema.v5.json"
V5_MD = OUT / "club_nation_subtable_schema.v5.md"
V5_JSON_SHA256 = "03967c9157fe0ca46d741e5bd74f9cd4d8df592045ca2dd6c38827f99eb36184"
V5_MD_SHA256 = "4e40595cb7734df534c4ab145b96855fada9da38f711454f27d3cfedf5e6c009"
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
PROTECTED_KEYS = ("tables", "negative_regressions", "v3_baseline", "club_auxiliary_sources", "nation_static_side")
TRIAL_IDS = (
    "main_client", "extra_as_slot19_client", "extra_named_client",
    "extra_named_without_object_name_arm_client", "main_server", "extra_as_slot19_server",
    "extra_named_server", "extra_named_without_object_name_arm_server",
)
FIELD_CODES = ("PUnI", "PUnT", "PUnP", "PUnJ")
LEDGER_ENTRY_IDS = ("E87", "E89", "E90", "E91", "E92", "E93")
T50_UNCHANGED_FILES = (
    "scratch/t50/out/REPORT.md", "scratch/t50/out/DONE.md",
    "scratch/t50/out/profile_t9.json", "scratch/t50/out/grammar_diff_t9.json",
)


class VerifyFailure(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerifyFailure(message)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_sha256(value: Any) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256(encoded)


def read_json(path: Path) -> Any:
    require(path.is_file(), f"missing JSON: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def read_root_json(relative: str) -> Any:
    return read_json(ROOT / relative)


def verify_snapshot_and_protected(schema: dict[str, Any], markdown: bytes, baseline: dict[str, Any],
                                  baseline_json: bytes, baseline_md: bytes) -> int:
    require(sha256(baseline_json) == V5_JSON_SHA256 and sha256(baseline_md) == V5_MD_SHA256,
            "frozen v5 snapshot SHA mismatch")
    current_json = PUBLIC_JSON.read_bytes()
    require(sha256(current_json) == sha256((json.dumps(schema, ensure_ascii=False, indent=2) + "\n").encode("utf-8")),
            "public JSON is not the parsed v6 schema")
    require(markdown.startswith(baseline_md), "v5 Markdown is not an exact byte prefix")
    require((schema.get("schema_version"), schema.get("generated_by")) == (6, "t54"),
            "schema version metadata mismatch")
    for key in PROTECTED_KEYS:
        require(schema.get(key) == baseline.get(key), f"v5 protected block changed: {key}")
    for key, value in baseline["coverage"].items():
        if not key.startswith("nation_"):
            require(schema["coverage"].get(key) == value, f"club/non-nation coverage changed: {key}")
    require(schema["nation_t9_wire"]["table_9"] == baseline["nation_t9_wire"]["table_9"],
            "v5 table_9 field records changed")
    extra_old = baseline["nation_t9_wire"]["table_extra_9"]
    extra_new = schema["nation_t9_wire"]["table_extra_9"]
    for key in ("rejection_records", "rejected_member_mode_attempts_total",
                "rejected_member_mode_attempts_for_extra_9", "source_discovery_binding",
                "t50_data_side_candidate_profile", "t50_L2_shape_assessment", "t50_not_a_parent_assignment"):
        require(extra_new[key] == extra_old[key], f"v5 table_extra_9 record changed: {key}")
    t50_old = baseline["nation_t9_wire"]["t50_L2_cross_validation"]
    t50_new = schema["nation_t9_wire"]["t50_L2_cross_validation"]
    require(t50_new["adjudication"].startswith(t50_old["adjudication"]),
            "v5 NO WINNER adjudication was not retained verbatim as prefix")
    require(t50_new["source_records_verbatim"] == t50_old["source_records_verbatim"],
            "embedded t50 original source records changed")
    return 1 + len(PROTECTED_KEYS) + len(baseline["coverage"]) + 8


def verify_t50_files(baseline: dict[str, Any], schema: dict[str, Any]) -> int:
    embedded = baseline["nation_t9_wire"]["t50_L2_cross_validation"]["source_records_verbatim"]
    current_node = schema["nation_t9_wire"]["t50_L2_cross_validation"]["source_records_verbatim"]
    require(current_node == embedded, "t50 source record object changed")
    path_keys = {
        "scratch/t50/out/REPORT.md": "REPORT.md",
        "scratch/t50/out/DONE.md": "DONE.md",
        "scratch/t50/out/profile_t9.json": "profile_t9.json",
        "scratch/t50/out/grammar_diff_t9.json": "grammar_diff_t9.json",
    }
    for path, key in path_keys.items():
        raw = (ROOT / path).read_bytes()
        require(raw.decode("utf-8") == embedded[key] if key.endswith(".md") else
                json.loads(raw.decode("utf-8")) == embedded[key], f"t50 source changed: {path}")
    records = {item["path"]: item for item in baseline["incremental_provenance"]["tasks"]["t50"]["source_artifacts"]}
    require(all(path in records for path in T50_UNCHANGED_FILES), "v5 t50 provenance lacks a required source file")
    for path in T50_UNCHANGED_FILES:
        raw = (ROOT / path).read_bytes()
        require(sha256(raw) == records[path]["sha256"] and len(raw) == records[path]["bytes"],
                f"t50 original file hash changed: {path}")
    return len(T50_UNCHANGED_FILES) + 1


def verify_t53_sources_and_cursors(schema: dict[str, Any], baseline: dict[str, Any]) -> int:
    t53 = schema["nation_t9_wire"]["t53_crs_adjudication"]
    discovery = read_root_json("scratch/t53/out/discovery_crs_wire.json")
    stored_sources = {item["path"]: item for item in t53["source_artifacts"]}
    require(set(stored_sources) == set(T53_PATHS), "t53 provenance artifact set mismatch")
    checks = 0
    source_json: dict[str, Any] = {}
    for path in T53_PATHS:
        raw = (ROOT / path).read_bytes()
        digest = sha256(raw)
        require(digest == T53_SHA256[path] and stored_sources[path]["sha256"] == digest and
                stored_sources[path]["bytes"] == len(raw), f"t53 source hash/size mismatch: {path}")
        if path.endswith(".json"):
            source_json[path] = json.loads(raw.decode("utf-8"))
        checks += 1
    require(t53["source_records_verbatim"]["REPORT.md"] ==
            (ROOT / "scratch/t53/out/REPORT.md").read_text(encoding="utf-8") and
            t53["source_records_verbatim"]["DONE.md"] ==
            (ROOT / "scratch/t53/out/DONE.md").read_text(encoding="utf-8"),
            "t53 REPORT/DONE are not preserved verbatim")
    require(t53["source_records_verbatim"]["discovery_crs_wire.json"] == discovery,
            "full t53 discovery artifact is not preserved verbatim")
    require(discovery["L3_fields"] == 0 and discovery["L4"] == 0 and
            t53["evidence_level"] == {"accepted_level": "L2", "L3_fields": 0, "L4": 0},
            "t53 evidence grade boundary mismatch")
    require(t53["acceptance_ledger_entry"] == "E93" and t53["acceptance_ledger_level"] == "L2",
            "t53 E93 provenance grade mismatch")
    require(t53["main_vector"]["member"] == "table_9.dat" and
            t53["main_vector"]["slot"] == "this+0x188" and
            t53["getter_vector"]["member"] == "table_extra_9.dat" and
            t53["getter_vector"]["slot"] == "[this+0xb0]+0x48",
            "t53 TCrs member/slot mapping mismatch")
    require(t53["distinct_vector_slots"] is True and
            t53["no_alias_assertion_scope"]["universal_absence_asserted"] is False,
            "t53 no-alias boundary was broadened")

    def check_main(side: str) -> tuple[int, int]:
        cursor = source_json[f"scratch/t53/out/cursor_crs_main_{side}.json"]
        rowlist = cursor["rows"]
        require(cursor["member"] == "table_9.dat" and len(rowlist) == 251 and
                cursor["mode"] == (0 if side == "client" else 1) and cursor["header"] == 13,
                f"main {side} cursor identity/mode/header")
        require(all(a["end"] == b["start"] for a, b in zip(rowlist, rowlist[1:])),
                f"main {side} row continuity")
        spans = sum(row["end"] - row["start"] for row in rowlist)
        footer = len(bytes.fromhex(cursor["footer"]))
        total = cursor["header"] + spans + footer
        expected = 31956 if side == "client" else 307564
        require(total == expected and cursor["end"] == cursor["header"] + spans and footer == 9,
                f"main {side} EOF equation")
        if side == "client":
            require(cursor["summary"]["skipped"] == 251 and cursor["summary"]["items"] == 0,
                    "main client skip count")
            require(t53["double_eof_closure"]["main_table_9"][side] == f"13 + {spans} + 9 = {total}",
                    "main client stored closure formula")
            return spans, total
        presence = Counter(str(row["presence"]) for row in rowlist)
        vectors = [row["vector"] for row in rowlist if row.get("vector")]
        items = [item for vector in vectors for item in vector["items"]]
        require(dict(presence) == {"0": 166, "1": 85} and len(vectors) == 85 and
                sum(vector["count"] > 0 for vector in vectors) == 85 and len(items) == 2219 and
                all(vector["version"] == 2 for vector in vectors) and
                all(item["tag"] == 3 and len(bytes.fromhex(item["raw"])) == 12 and
                    int.from_bytes(bytes.fromhex(item["raw"])[2:6], "little", signed=True) == -1
                    for item in items), "main server counts/tag/version/PUnP")
        require(t53["main_vector"]["archive_modes"][side]["presence"] == {"0": 166, "1": 85} and
                t53["main_vector"]["archive_modes"][side]["items"] == 2219 and
                t53["double_eof_closure"]["main_table_9"][side] == f"13 + {spans} + 9 = {total}",
                "main server stored counts/formula")
        return spans, total

    def check_extra(side: str) -> tuple[int, int]:
        cursor = source_json[f"scratch/t53/out/cursor_crs_extra_{side}.json"]
        rowlist = cursor["rows"]
        require(cursor["member"] == "table_extra_9.dat" and len(rowlist) == 251 and
                cursor["mode"] == (0 if side == "client" else 1) and cursor["header"] == 12,
                f"extra {side} cursor identity/mode/header")
        require(all(a["end"] == b["start"] for a, b in zip(rowlist, rowlist[1:])),
                f"extra {side} row continuity")
        spans = sum(row["end"] - row["start"] for row in rowlist)
        total = cursor["header"] + spans
        expected = 83927 if side == "client" else 105228
        require(cursor["end"] == total == expected and cursor["footer"] == "",
                f"extra {side} EOF equation")
        if side == "client":
            require(cursor["summary"]["skipped"] == 251 and cursor["summary"]["items"] == 0,
                    "extra client skip count")
            require(t53["double_eof_closure"]["getter_table_extra_9_suffix"][side] ==
                    f"12 + sum(spans={spans}) = {total}", "extra client stored closure formula")
            return spans, total
        presence = Counter(str(row["presence"]) for row in rowlist)
        vectors = [row["vector"] for row in rowlist if row.get("vector")]
        items = [item for vector in vectors for item in vector["items"]]
        require(dict(presence) == {"0": 179, "1": 72} and len(vectors) == 72 and
                sum(vector["count"] == 0 for vector in vectors) == 39 and
                sum(vector["count"] > 0 for vector in vectors) == 33 and len(items) == 76 and
                all(vector["version"] == 2 for vector in vectors) and all(item["tag"] == 3 for item in items),
                "extra server counts/tag/version")
        require(t53["getter_vector"]["archive_modes"][side]["presence"] == {"0": 179, "1": 72} and
                t53["getter_vector"]["archive_modes"][side]["items"] == 76 and
                t53["getter_vector"]["archive_modes"][side]["zero_count_vectors"] == 39 and
                t53["double_eof_closure"]["getter_table_extra_9_suffix"][side] ==
                f"12 + sum(spans={spans}) = {total}", "extra server stored counts/formula")
        return spans, total

    check_main("client")
    check_main("server")
    check_extra("client")
    check_extra("server")
    for code in FIELD_CODES:
        source_field = source_json[f"scratch/t53/out/fields_{code}.json"]
        embedded = t53["field_dispositions"][code]
        require(source_field["grade"] == "held" and embedded["grade"] == "held" and
                embedded["source_record_verbatim"] == source_field,
                f"t53 {code} held record changed")
    trial_list = t53["wrong_mode_trial_groups"]
    require([item["id"] for item in trial_list] == list(TRIAL_IDS) and len(trial_list) == 8,
            "t53 negative trial groups are not individually retained")
    for item in trial_list:
        require(item["source_record"] == discovery["trials"][item["id"]],
                f"t53 trial group changed: {item['id']}")
    extra_rows = source_json["scratch/t53/out/cursor_crs_extra_server.json"]["rows"]
    cross = t53["t50_block_internal_cross_result"]
    require(cross["server_row_2"]["t50_candidate_offsets"] == [867, 875] and
            cross["server_row_2"]["t53_selected_block_start"] == extra_rows[2]["start"] == 875 and
            cross["server_row_82"]["t50_candidate_offsets"] == [39439, 39533] and
            cross["server_row_82"]["t53_selected_block_start"] == extra_rows[82]["start"] == 39533 and
            cross["server_row_82"]["bytes_consumed_after_earlier_candidate"] == 94 and
            cross["t9_table_9_no_winner_unchanged"] is True,
            "t50 candidate cross-result mismatch")
    return checks + 26


def verify_coverage_and_provenance(schema: dict[str, Any], baseline: dict[str, Any]) -> int:
    coverage = schema["coverage"]
    old_coverage = baseline["coverage"]
    require((coverage["nation_L3_occurrences"], coverage["nation_L3_unique_wire_fields"],
             coverage["nation_held_occurrences"], coverage["nation_negative_records"]) == (30, 30, 20, 15),
            "v6 nation coverage totals mismatch")
    require(coverage["nation_t53_negative_trial_groups"] == 8 and
            coverage["nation_negative_record_breakdown"]["t53_wrong_mode_trial_groups"] == 8 and
            len(coverage["nation_negative_record_breakdown"]["t53_wrong_mode_trial_ids"]) == 8 and
            coverage["nation_negative_record_breakdown"]["t53_no_alias_scope_limit_counted_as_failed_trial"] is False,
            "v6 negative record bookkeeping mismatch")
    for key, value in old_coverage.items():
        if key not in ("nation_negative_records", "nation_negative_record_breakdown", "nation_coverage_policy"):
            require(coverage.get(key) == value, f"unexpected v5 nation counter change: {key}")
    old_breakdown = old_coverage["nation_negative_record_breakdown"]
    new_breakdown = coverage["nation_negative_record_breakdown"]
    for key, value in old_breakdown.items():
        require(new_breakdown.get(key) == value, f"old negative record scope changed: {key}")
    require(coverage["nation_negative_records"] ==
            new_breakdown["t49_rejected_member_mode_attempts"] +
            new_breakdown["t51_EDfx_UI_path_with_archive_backing_unbound"] +
            new_breakdown["t53_wrong_mode_trial_groups"],
            "negative total does not equal bounded individual groups")
    require(schema["nation_t9_wire"]["table_extra_9"]["status"] != "unbound_open_negative" and
            schema["nation_t9_wire"]["table_extra_9"]["target_parent_assignment"] ==
            ["nation.xml#nation[64].TCrs getter vector (typed suffix only)"],
            "typed-suffix binding is missing or over-broad")
    require(schema["nation_t9_wire"]["table_extra_9"]["rejected_member_mode_attempts_total"] == 6,
            "the six prior t49 slot19 negative attempts were dropped")

    ledger = read_root_json("scratch/t01/LEDGER.json")
    referenced_entries: dict[str, dict[str, Any]] = {}
    for entry in ledger["entries"]:
        entry_id = entry.get("id")
        if entry_id in LEDGER_ENTRY_IDS:
            require(entry_id not in referenced_entries, f"duplicate referenced ledger entry: {entry_id}")
            referenced_entries[entry_id] = entry
    require(set(referenced_entries) == set(LEDGER_ENTRY_IDS),
            "one or more referenced ledger entries are missing")
    prov = schema["incremental_provenance"]
    expected_entries = prov["acceptance_ledger_entries"]
    baseline_entries = baseline["incremental_provenance"]["acceptance_ledger_entries"]
    for entry_id in LEDGER_ENTRY_IDS:
        actual = referenced_entries[entry_id]
        expected = expected_entries[entry_id]
        require(expected.get("kind") == actual.get("kind") and
                expected.get("level") == actual.get("level") and
                expected.get("claim_sha256") == canonical_sha256(actual["claim"]),
                f"{entry_id} referenced entry identity/claim/grade mismatch")
        if entry_id != "E93":
            require(expected == baseline_entries[entry_id],
                    f"{entry_id} provenance changed from the frozen v5 reference")
    entries = referenced_entries
    for entry_id in ("E91", "E92", "E93"):
        require((entries[entry_id]["kind"], entries[entry_id]["level"]) == ("acceptance", "L2"),
                f"{entry_id} must remain acceptance/L2")
    require(prov["tasks"]["t50"]["acceptance_ledger_entry"] == "E91" and
            prov["tasks"]["t50"]["ledger_status"].startswith("E91 accepts L2 data-side profile only; no L3") and
            prov["tasks"]["t53"]["acceptance_ledger_entry"] == "E93" and
            prov["tasks"]["t53"]["acceptance_ledger_level"] == "L2" and
            prov["tasks"]["t53"]["evidence_level"]["L3_fields"] == 0,
            "t52 fix1 E91@L2-only guard / t53 E93@L2 provenance mismatch")
    t53_record = schema["nation_t9_wire"]["t53_crs_adjudication"]
    require(t53_record["acceptance_ledger_claim_sha256"] == canonical_sha256(entries["E93"]["claim"]),
            "E93 claim hash mismatch")
    snapshot_meta = prov["t54_ledger_snapshot"]
    require(snapshot_meta["entries_used"] == list(LEDGER_ENTRY_IDS) and
            snapshot_meta["t50_acceptance_level"] == "L2" and
            snapshot_meta["t52_acceptance_level"] == "L2" and
            snapshot_meta["t53_acceptance_level"] == "L2",
            "t54 referenced-entry scope/levels mismatch")
    return 20


def selftest() -> None:
    require(sha256(b"") == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "empty SHA-256 selftest")
    require(len(TRIAL_IDS) == 8 and len(FIELD_CODES) == 4 and len(PROTECTED_KEYS) == 5 and
            len(LEDGER_ENTRY_IDS) == 6, "verifier constants selftest")
    sample = {"x": [1, 2], "held": True}
    require(json.loads(json.dumps(sample)) == sample, "JSON structural equality selftest")
    print("t54 verifier selftest PASS")


def verify_all() -> int:
    schema = read_json(PUBLIC_JSON)
    markdown = PUBLIC_MD.read_bytes()
    require(V5_JSON.is_file() and V5_MD.is_file(), "v5 snapshots missing")
    baseline_json, baseline_md = V5_JSON.read_bytes(), V5_MD.read_bytes()
    baseline = json.loads(baseline_json.decode("utf-8"))
    checks = verify_snapshot_and_protected(schema, markdown, baseline, baseline_json, baseline_md)
    checks += verify_t50_files(baseline, schema)
    checks += verify_t53_sources_and_cursors(schema, baseline)
    checks += verify_coverage_and_provenance(schema, baseline)
    print(f"t54 independent verification PASS ({checks} checks/groups)")
    print("v5 snapshots: SHA-pinned; protected tables/club/nation_static_side content unchanged")
    print("TCrs: main 2,219 and getter suffix 76 items; four archive members EOF-closed")
    print("PUnI/PUnT/PUnP/PUnJ held; E93=L2; L3 fields=0; L4=0")
    print("t50 original records and NO WINNER prefix preserved; extra_9 internal cross-result appended")
    print("ledger guard: E87/E89/E90/E91/E92/E93 entry-level only; E94 excluded")
    print("nation coverage: 30/30/20/15; eight t53 trial groups individually retained")
    return checks


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Independently verify t54 v6 against the frozen v5 pair, t53 artifacts, E91/E93 L2 provenance, protected blocks, and EOF closures.")
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--selftest", action="store_true", help="run isolated verifier selftests")
    modes.add_argument("--check", action="store_true", help="verify the public v6 pair and its frozen sources")
    args = parser.parse_args(argv)
    try:
        if args.selftest:
            selftest()
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
