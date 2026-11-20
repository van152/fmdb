#!/usr/bin/env python3
"""Independent verifier for the additive t60 public schema v9 consolidation."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PUBLIC_JSON = ROOT / "reports" / "club_nation_subtable_schema.json"
PUBLIC_MD = ROOT / "reports" / "club_nation_subtable_schema.md"
V8_JSON = HERE / "club_nation_subtable_schema.v8.json"
V8_MD = HERE / "club_nation_subtable_schema.v8.md"
V9_JSON = HERE / "club_nation_subtable_schema.v9.json"
V9_MD = HERE / "club_nation_subtable_schema.v9.md"
LEDGER_PATH = ROOT / "scratch" / "t01" / "LEDGER.json"
V8_JSON_SHA256 = "76da94d4376613a9e649a32d3bfc415f19596d4c7fb1c7c861d60b5951770cbf"
V8_MD_SHA256 = "5067502eadd489fac0e9842c6ece45e8402ff656e43d41e721522714308737f6"
E98_SHA256 = "57a2384c170c3effc159a98012b866ab174849da8849269abc118b8e7fe4f150"
E99_SHA256 = "e13990af22d739ba1f6a61e9adc2211febb051821845a48358e30306d452b16b"
GUARDED_IDS = tuple(f"E{i}" for i in range(84, 100))
EXPECTED_NEW_4CC = [
    "LAUC", "cext", "cusn", "culn", "Pcsp", "Pcsk", "Pcsf", "Pcsr", "Pcsb", "Pcsh", "Pcsy",
    "Pcjm", "Pcja", "Pcjc", "Pcji", "Pcjg", "Pcsc", "Pcjy", "Pcdf", "Pctd", "Pchd", "Pcda",
    "Pcss", "Pcdr", "Pcjs", "Pcjp",
]
EXPECTED_COUNTS = {"L3": 49, "held": 10, "unmapped": 196}
EXPECTED_COVERAGE = {
    "comp_main_row_occurrences": 255,
    "comp_main_row_aligned": 54,
    "comp_main_row_L3": 49,
    "comp_main_row_held": 10,
    "comp_main_row_unmapped": 196,
    "comp_main_row_order_inversions": 818,
}
EXPECTED_REFERENCE_JOINS = [
    {"field": "ccti", "target": "table_5 continent", "live": 6981, "null": 66, "miss": 0},
    {"field": "cnti", "target": "table_10 nation", "live": 6769, "null": 278, "miss": 0},
    {"field": "cpcm", "target": "table_25 competition self-reference", "live": 3506, "null": 3541, "miss": 0},
    {"field": "cnor", "target": "table_2 city", "live": 680, "null": 6367, "miss": 0},
    {"field": "csou", "target": "table_2 city", "live": 671, "null": 6376, "miss": 0},
    {"field": "cwes", "target": "table_2 city", "live": 642, "null": 6405, "miss": 0},
    {"field": "ceas", "target": "table_2 city", "live": 641, "null": 6406, "miss": 0},
]
T59_ARTIFACTS = {
    "scratch/t59/out/field_slots.json": "c408afe0b29231e2fcb152259fbe9f54d50abbdb38db1b15cb43ab6c16f92fe0",
    "scratch/t59/out/field_map.json": "fdbcb6120cf87b1f7987d50bc2b2283e8a25d23594060f4b348defbfc546d168",
    "scratch/t59/out/REPORT.md": "4049fbb767effd8b6fbc56d9512e12d1e72d9f4bb7fdb4987526f5854bbc15af",
    "scratch/t59/out/DONE.md": "a8f525266d8dddce2bcaf148e6a0c4cb6616b54c4575591238764fb4f631046a",
    "scratch/t59/out/verify.py": "ca328232f46a196c4fc707c15374a83fdc50e4297f710399015f0155c20022da",
    "scratch/t59/out/instructions.part01.json": "147daaaddfc93ca5d798cc0c5866c4ea4aeba96e0f3e58009a48b42f75f6580a",
    "scratch/t59/out/instructions.part02.json": "95667e8864d3802cd0d4d2829b796aac3f7d1a78455226dcb92b8bedd63362c1",
    "scratch/t59/out/instructions.part03.json": "61cb61917365a29bfce9cfff5cfa8278a6c64b0445fd9b563b527b01cd60f4a9",
    "scratch/t59/out/instructions.part04.json": "bba78f63989568be5010925379d5b3c73f61c91c0497720a0f4e902782b91ea8",
    "scratch/t59/out/instructions.part05.json": "4b64ec45d86b2cd1339bbf452fb4315d8877b5ec2146f80beb9433a9fdbd5716",
    "scratch/t59/out/instructions.part06.json": "251e59792bf7069d600d68fa08ccd496aa95ed8983898932368b5d793b9ff0af",
    "scratch/t59/out/instructions.part07.json": "d60e06781a97d15b4d1b2771130d53f3a33e9bb972f9b60974aa7e27a9e0d0c8",
    "scratch/t59/out/branches.part01.json": "e66e280b3ec346bff1a07d2d76cc215dbaa7a69ac9884a2ed9653790def3c377",
    "scratch/t59/out/branches.part02.json": "eada3cef8d2b1bd9cf9dd98341dbf252c656a77f57e69dfe90cb08e4e74d6150",
    "scratch/t59/out/branches.part03.json": "c99ebb958b286f3a0988813672ce955775d1b04694141e4679c4b6d1cdd7ce7e",
}


class CheckFailure(Exception):
    pass


def require(ok: bool, why: str) -> None:
    if not ok:
        raise CheckFailure(why)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_sha(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha(raw)


def read_json(path: Path) -> Any:
    return json.loads(path.read_bytes())


def check_t59_artifacts() -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    artifact_rows = []
    for rel, expected in T59_ARTIFACTS.items():
        raw = (ROOT / rel).read_bytes()
        require(sha(raw) == expected, f"t59 artifact SHA-256 mismatch: {rel}")
        artifact_rows.append({"path": rel, "sha256": expected, "bytes": len(raw)})
    slots = read_json(ROOT / "scratch/t59/out/field_slots.json")
    field_map = read_json(ROOT / "scratch/t59/out/field_map.json")
    return slots, field_map, artifact_rows


def verify_ledger(schema: dict[str, Any]) -> None:
    ledger = read_json(LEDGER_PATH)
    found: dict[str, dict[str, Any]] = {}
    for entry in ledger["entries"]:
        entry_id = entry.get("id")
        if entry_id in GUARDED_IDS:
            require(entry_id not in found, f"duplicate live ledger entry {entry_id}")
            found[entry_id] = entry
    require(set(found) == set(GUARDED_IDS), "live ledger guard set incomplete")
    guards = []
    for entry_id in GUARDED_IDS:
        item = found[entry_id]
        guards.append({
            "id": entry_id,
            "kind": item["kind"],
            "level": item["level"],
            "claim_sha256": canonical_sha(item["claim"]),
        })
    snapshot = schema["incremental_provenance"]["t60_ledger_snapshot"]
    require(snapshot["path"] == "scratch/t01/LEDGER.json" and
            snapshot["guarded_entries"] == list(GUARDED_IDS) and snapshot["entries"] == guards,
            "entry-level guard snapshot E84-E99")
    require(snapshot["v8_baseline_acceptance_entry"] == "E98" and
            snapshot["v8_baseline_acceptance_level"] == "L3" and
            snapshot["t59_acceptance_entry"] == "E99" and
            snapshot["t59_acceptance_level"] == "L3" and
            "no live full-file hash" in snapshot["guard_scope"], "ledger guard scope / task levels")
    recorded = schema["incremental_provenance"]["acceptance_ledger_entries"]
    for entry_id in GUARDED_IDS:
        live = found[entry_id]
        row = recorded[entry_id]
        require((row.get("kind"), row.get("level"), row.get("claim_sha256")) ==
                (live["kind"], live["level"], canonical_sha(live["claim"])),
                f"schema acceptance ledger record {entry_id}")
    require(canonical_sha(found["E98"]["claim"]) == E98_SHA256 and
            canonical_sha(found["E99"]["claim"]) == E99_SHA256 and
            found["E98"]["level"] == found["E99"]["level"] == "L3",
            "E98/E99 fixed acceptance claims")
    print("PASS ledger: entry-level id/kind/level/canonical claim SHA guards E84-E99")


def verify_protected_sections(baseline: dict[str, Any], schema: dict[str, Any]) -> None:
    protected = {"tables", "negative_regressions", "v3_baseline", "club_auxiliary_sources", "club_main_row_fields"}
    protected.update(key for key in baseline if key.startswith("nation_"))
    for key in protected:
        require(schema.get(key) == baseline.get(key), f"protected section changed: {key}")
    for key, value in baseline.items():
        if key not in {"schema_version", "generated_by", "coverage", "incremental_provenance"}:
            require(schema.get(key) == value, f"non-additive root changed: {key}")
    require(set(schema) == set(baseline) | {"comp_main_row_fields"}, "unexpected root key")
    for key, value in baseline["coverage"].items():
        require(schema["coverage"].get(key) == value, f"pre-existing coverage changed: {key}")
    old_prov = baseline["incremental_provenance"]
    new_prov = schema["incremental_provenance"]
    for key, value in old_prov.items():
        if key not in {"acceptance_ledger_entries", "tasks"}:
            require(new_prov.get(key) == value, f"pre-existing provenance changed: {key}")
    for key, value in old_prov["tasks"].items():
        require(new_prov["tasks"].get(key) == value, f"pre-existing task changed: {key}")
    for key, value in old_prov["acceptance_ledger_entries"].items():
        require(new_prov["acceptance_ledger_entries"].get(key) == value,
                f"pre-existing ledger record changed: {key}")
    print("PASS protected sections: tables, regressions, v3, club auxiliary/main, all nation_* and old counters")


def verify_t59_section(section: dict[str, Any], slots: dict[str, Any], field_map: dict[str, Any],
                       artifact_rows: list[dict[str, Any]]) -> None:
    require(section["source_task"] == "t59" and section["acceptance_ledger_entry"] == "E99" and
            section["acceptance_ledger_level"] == "L3" and section["status"] == "partial_schema_join" and
            section["scope"] == "comp.xml#comp top level only" and
            section["evidence_level"] == {"L3_fields": 49, "L4": 0}, "t59 section provenance")
    require(field_map["count"] == 255 and field_map["aligned"] == 54 and field_map["summary"] == EXPECTED_COUNTS and
            len(field_map["new_L3"]) == 26 and field_map["new_L3"] == EXPECTED_NEW_4CC and
            len(field_map["inversions"]) == 818, "t59 numeric census")
    require(section["source_records"]["field_slots"] == slots and
            section["source_records"]["field_map"] == field_map, "verbatim embedded t59 records")
    records = field_map["fields"]
    require(section["L3_fields"] == [row for row in records if row["status"] == "L3"] and
            section["held_records"] == [row for row in records if row["status"] == "held"] and
            section["unmapped_records"] == [row for row in records if row["status"] == "unmapped"],
            "source-identical L3/held/unmapped records")
    require(len(section["held_records"]) == 10 and len(section["unmapped_records"]) == 196,
            "held/unmapped record counts")
    env = section["row_framing"]["archives"]
    require((env["client"]["header"], env["client"]["rows"], env["client"]["footer"],
             env["client"]["payload"]) == (13, 894969, 9, 894991) and
            env["client"]["row_width_histogram"] == {"127": 7047} and
            (env["server"]["header"], env["server"]["rows"], env["server"]["footer"],
             env["server"]["payload"]) == (13, 1533950, 9, 1533972) and
            env["client"]["count"] == env["server"]["count"] == 7047 and
            section["row_framing"]["client_row_width_bytes"] == 127 and
            section["row_framing"]["client_row_width_histogram"] == {"127": 7047},
            "client/server payload closure, row counts and fixed client width")
    framing = section["row_framing"]
    identity = next(row for row in slots["slots"] if row["key"] == "identity")
    require(framing["identity_width"] == identity["nominal_width"] == 12 and
            framing["identity_layout"] == "dsha ordinal | duni UID | saved rdui UID (observed equal to duni)" and
            framing["footer_width"] == 9 and framing["footer_hex"] == "00000000014ec43a77" and
            framing["footer_parts"] == ["00000000", "01", "4ec43a77"], "identity/footer assertion")
    reader = section["reader_and_factory"]
    require((reader["vtable_slot"], reader["reader_file_offset_hex"], reader["reader_VA"],
             reader["reachable_instructions"], reader["conditional_branches"], reader["external_edges"]) ==
            (19, "0xeb7000", "0x140eb7a00", 837, 114, []), "COMP slot19 reader assertion")
    require(reader["comp_object_vtable"] == "0x14187dcb8" and
            reader["database_table_comp_vtable"] == "0x14187f6d8" and
            reader["object_shapes_are_distinct"], "factory case25 object shapes remain distinct")
    outer = section["outer_sequence_closure"]
    require((outer["observed_positions"], outer["static_untriggered_positions"],
             outer["field_slot_records"], outer["client_sites_per_row"], outer["server_templates"],
             outer["server_sites_per_template"]) ==
            (82, ["obj_a8", "obj_e0"], 84, 51, 25, {"min": 77, "max": 82}),
            "82 observed sites plus two static untriggered")
    census = section["field_census"]
    require((census["occurrences"], census["aligned"], census["grade_counts"], census["new_4CC_count"], census["new_4CC"], census["L4"]) ==
            (255, 54, EXPECTED_COUNTS, 26, EXPECTED_NEW_4CC, 0), "field census projection")
    require(section["order"]["inversions"] == 818 and
            section["order"]["first_counterexample"] == {
                "xml_pair": [1, 12], "codes": ["duni", "cfcl"], "execution_pair": [81, 4],
            } and section["order"]["all_pairs"] == field_map["inversions"], "full inversion ledger")
    require(section["reference_joins"] == EXPECTED_REFERENCE_JOINS and
            section["reference_join_violations"] == 0, "reference-domain joins/zero violations")
    require(section["source_artifacts"] == artifact_rows, "t59 source artifact manifest")
    print("PASS t59 assertions: 894991/1533972 bytes, 7047 rows, client 127B, 12B identity, 9B footer, 49 L3, 26 new 4CC, 818 inversions, 82 observed sites")
    print("PASS t59 record preservation: all 10 held and 196 unmapped rows match source objects")


def verify_coverage(baseline: dict[str, Any], schema: dict[str, Any]) -> None:
    for key, expected in EXPECTED_COVERAGE.items():
        require(schema["coverage"].get(key) == expected, f"comp coverage {key}")
    for key in baseline["coverage"]:
        if key.startswith("club_") or key.startswith("nation_") or key in {
            "held_fields", "negative_regressions", "L4", "row_identity_footer_width_policy",
        }:
            require(schema["coverage"].get(key) == baseline["coverage"][key],
                    f"club/nation/pre-existing coverage changed: {key}")
    require(schema["coverage"]["comp_identity_footer_width_note"] == (
        "Third independently evidenced row-frame example: comp/table_25 has a 12-byte identity and 9-byte footer, "
        "alongside nation 13-byte and club 12-byte identity tails. Derive and verify each table independently; do not copy widths."
    ), "additive comp row identity note")
    print("PASS coverage: six comp_main_row counters added; all prior club/nation counters unchanged")


def verify() -> None:
    v8_json_raw = V8_JSON.read_bytes()
    v8_md_raw = V8_MD.read_bytes()
    require(sha(v8_json_raw) == V8_JSON_SHA256 and sha(v8_md_raw) == V8_MD_SHA256,
            "v8 snapshot SHA-256")
    baseline = json.loads(v8_json_raw)
    require(baseline["schema_version"] == 8 and baseline["generated_by"] == "t58", "v8 snapshot identity")
    print(f"PASS v8 snapshot SHA: JSON {V8_JSON_SHA256}; Markdown {V8_MD_SHA256}")

    public_json = PUBLIC_JSON.read_bytes()
    public_md = PUBLIC_MD.read_bytes()
    require(public_json == V9_JSON.read_bytes() and public_md == V9_MD.read_bytes(),
            "public schema/output snapshot mismatch")
    schema = json.loads(public_json)
    require(schema["schema_version"] == 9 and schema["generated_by"] == "t60", "public schema v9 identity")
    require(public_md.startswith(v8_md_raw), "Markdown v8 prefix changed")
    require(public_md.endswith(b"\n"), "Markdown final newline")
    verify_protected_sections(baseline, schema)

    slots, field_map, artifact_rows = check_t59_artifacts()
    verify_t59_section(schema["comp_main_row_fields"], slots, field_map, artifact_rows)
    verify_coverage(baseline, schema)
    verify_ledger(schema)

    provenance = schema["incremental_provenance"]
    old_task_ids = set(baseline["incremental_provenance"]["tasks"])
    require(set(provenance["tasks"]) == old_task_ids | {"t59"}, "provenance task set")
    task = provenance["tasks"]["t59"]
    require(task["acceptance_ledger_entry"] == "E99" and task["acceptance_ledger_level"] == "L3" and
            task["ledger_claim_sha256"] == E99_SHA256 and task["evidence_level"] == {"L3_fields": 49, "L4": 0} and
            task["held_records_preserved"] and task["unmapped_records_preserved"], "t59 task provenance")

    report = (HERE / "REPORT.md").read_text(encoding="utf-8")
    done = (HERE / "DONE.md").read_text(encoding="utf-8")
    public_json_sha, public_md_sha = sha(public_json), sha(public_md)
    require(public_json_sha in report and public_md_sha in report and
            public_json_sha in done and public_md_sha in done, "report/DONE public output hashes")
    for token in ("894,991", "1,533,972", "7,047", "12 B", "9 B", "49 L3", "26", "818", "82"):
        require(token in report or token in done, f"delivery report token missing: {token}")
    anchors_log = (HERE / "spot_t01_anchors.log").read_text(encoding="utf-8")
    require("7/7 checks passed" in anchors_log, "t01 anchors 7/7 validation log")
    print("PASS anchors: t01 regression log records 7/7")
    print(f"PASS public v9 pair and Markdown v8 verbatim prefix; JSON {public_json_sha}; Markdown {public_md_sha}")
    print("t60 independent verify PASS")


def selftest() -> None:
    require(len(E98_SHA256) == len(E99_SHA256) == 64 and len(GUARDED_IDS) == 16,
            "static guard constants")
    require(sum(EXPECTED_COUNTS.values()) == 255 and len(EXPECTED_NEW_4CC) == 26 and
            EXPECTED_COVERAGE["comp_main_row_order_inversions"] == 818,
            "static t59 census constants")
    require(GUARDED_IDS[0] == "E84" and GUARDED_IDS[-1] == "E99", "guard range")
    print("t60 verifier selftest PASS")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--check", action="store_true", help="verify public v9 and pinned sources (default)")
    group.add_argument("--selftest", action="store_true", help="run pure verifier tests")
    args = parser.parse_args()
    try:
        selftest() if args.selftest else verify()
        return 0
    except CheckFailure as exc:
        print(f"CHECK FAILED: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"FATAL: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
