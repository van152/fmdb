#!/usr/bin/env python3
"""Independent verifier for the additive t56 public schema v7 consolidation."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
PUBLIC_JSON = ROOT / "reports" / "club_nation_subtable_schema.json"
PUBLIC_MD = ROOT / "reports" / "club_nation_subtable_schema.md"
V5_JSON = OUT / "club_nation_subtable_schema.v5.json"
V5_MD = OUT / "club_nation_subtable_schema.v5.md"
V6_JSON = OUT / "club_nation_subtable_schema.v6.json"
V6_MD = OUT / "club_nation_subtable_schema.v6.md"
V7_JSON = OUT / "club_nation_subtable_schema.v7.json"
V7_MD = OUT / "club_nation_subtable_schema.v7.md"
V5_JSON_SHA256 = "03967c9157fe0ca46d741e5bd74f9cd4d8df592045ca2dd6c38827f99eb36184"
V5_MD_SHA256 = "4e40595cb7734df534c4ab145b96855fada9da38f711454f27d3cfedf5e6c009"
V6_JSON_SHA256 = "02751ef7c79c60dfcf14bfbad5fe10e2077f15ed753d12e9ebfa1dfbbc010f44"
V6_MD_SHA256 = "a8d6509b090cd16ed7bf3d89c37638e23da120cbcfcc9e80424bd01a82234ac6"
E94_SHA256 = "358243779bba359656ecae6804cea9cea26b1739ffce5bf96a2599d735263c89"
E95_SHA256 = "2632aaae869ee3a5c1020d82e409f1f26ad429d077f06f078d5f7f1058f43eb1"
OLD_GUARDS = ("E87", "E89", "E90", "E91", "E92", "E93")
NEW_GUARDS = {"E94": ("acceptance", "L3", E94_SHA256), "E95": ("acceptance", "L2", E95_SHA256)}
PROTECTED = (
    "tables", "negative_regressions", "v3_baseline", "club_auxiliary_sources",
    "nation_data_side_status", "nation_static_side", "nation_t9_wire",
)
T55_ARTIFACTS = {
    "scratch/t55/out/field_slots.json": "1625560fa99e635cdf60e10c108fedf799c359790adcfba429fc205edcfbcd17",
    "scratch/t55/out/field_map.json": "6828a434cff296af0a63471bff8deeb2edbcb0d2226cd3665955797c373137a4",
    "scratch/t55/out/abc_closure.json": "8fbce6d9ebc32d2d950d45c4c7fb35ca88d8095e26f8f045c564b06f45388153",
    "scratch/t55/out/instructions.part001.json": "32f4c3b017f47b736ddc5de425a7b9725ddd710f9bb008d73d545505d4206a0e",
    "scratch/t55/out/instructions.part002.json": "e50e8d1f2bb779bb13655a44be97296122740308854ec5e3da124880ec1e8de1",
    "scratch/t55/out/instructions.part003.json": "72158705e606f97321720a8ccb5a33037d7ff2277065c5ee4dcc262c4ac5f850",
    "scratch/t55/out/branches.part001.json": "bf7308fd411e23e43429be95090c4a093d862fd3731cbd64e86811346c741b48",
    "scratch/t55/out/verify.py": "fd8775d27dfb48bc71455c80fc33f5d5a32d4244760b69a70522c3d77488e7bf",
    "scratch/t55/out/REPORT.md": "9cbf22d1883cc200ef9f0da699828f71a1b23546381ef63dbb6a644cce058065",
    "scratch/t55/out/DONE.md": "05f3626869bd5daa5593277918f61129d4a91a7af28690f95dc66fcb51e80c50",
    "scripts/t55_natmain_fields.py": "350bf0cfe2fac90e90c4057cd313067e6e0cfaed878a2f5056a26a2ba83be27b",
}
OLD_COVERAGE_EDITABLE = {
    "nation_side", "nation_L3_occurrences", "nation_L3_unique_wire_fields",
    "nation_L3_unique_wire_field_ids", "nation_held_occurrences", "nation_coverage_policy",
}
EXPECTED_GRADES = {
    "L3": 5, "held": 5, "linked_parent_held": 1, "no_main_wire_slot": 1,
    "no_wire_slot": 1, "prior_collection": 5, "prior_identity": 1, "unmapped": 327,
}
EXPECTED_L3 = {"Nnsi": (1, 21, 21), "Ncti": (15, 16, 5), "Nrgi": (16, 17, 19),
               "Ncur": (18, 20, 41), "Nndn": (37, 29, None)}


class CheckFailure(Exception):
    pass


def require(ok: bool, why: str) -> None:
    if not ok:
        raise CheckFailure(why)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_sha(value: Any) -> str:
    return sha(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def load_json(path: Path) -> Any:
    return json.loads(path.read_bytes())


def check_hash(path: Path, expected: str) -> bytes:
    raw = path.read_bytes()
    require(sha(raw) == expected, f"SHA-256 mismatch: {path.relative_to(ROOT)}")
    return raw


def verify_ledger(baseline: dict[str, Any], schema: dict[str, Any]) -> None:
    ledger = load_json(ROOT / "scratch/t01/LEDGER.json")
    wanted = {*OLD_GUARDS, *NEW_GUARDS}
    found: dict[str, dict[str, Any]] = {}
    for entry in ledger["entries"]:
        if entry.get("id") in wanted:
            eid = entry["id"]
            require(eid not in found, f"duplicate live ledger entry {eid}")
            found[eid] = entry
    require(set(found) == wanted, "entry-level ledger guard set incomplete")
    provenance = schema["incremental_provenance"]
    recorded = provenance["acceptance_ledger_entries"]
    old_recorded = baseline["incremental_provenance"]["acceptance_ledger_entries"]
    for eid in OLD_GUARDS:
        actual = found[eid]
        expected = old_recorded[eid]
        require(actual.get("kind") == expected.get("kind") and actual.get("level") == expected.get("level") and
                canonical_sha(actual.get("claim")) == expected.get("claim_sha256"), f"baseline ledger guard {eid}")
        require(recorded[eid] == expected, f"existing schema ledger record changed: {eid}")
    for eid, (kind, level, expected_sha) in NEW_GUARDS.items():
        actual = found[eid]
        require((actual.get("kind"), actual.get("level"), canonical_sha(actual.get("claim"))) ==
                (kind, level, expected_sha), f"new ledger guard {eid}")
        row = recorded[eid]
        require((row.get("kind"), row.get("level"), row.get("claim_sha256")) ==
                (kind, level, expected_sha), f"schema ledger record {eid}")
    snapshot = provenance["t56_ledger_snapshot"]
    require(snapshot["path"] == "scratch/t01/LEDGER.json" and
            snapshot["guarded_entries"] == [*OLD_GUARDS, "E94", "E95"] and
            snapshot["v6_baseline_acceptance_entry"] == "E95" and
            snapshot["v6_baseline_acceptance_level"] == "L2" and
            snapshot["t55_acceptance_entry"] == "E94" and snapshot["t55_acceptance_level"] == "L3" and
            "no live full-file hash" in snapshot["guard_scope"], "entry-only ledger provenance")
    task = provenance["tasks"]["t55"]
    require(task["acceptance_ledger_entry"] == "E94" and task["acceptance_ledger_level"] == "L3" and
            task["ledger_claim_sha256"] == E94_SHA256 and task["evidence_level"] == {"L3_fields": 5, "L4": 0},
            "t55 task provenance")


def verify_sources(section: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    listed = {row["path"]: row for row in section["source_artifacts"]}
    require(set(listed) == set(T55_ARTIFACTS), "t55 artifact manifest path set")
    for rel, expected in T55_ARTIFACTS.items():
        raw = check_hash(ROOT / rel, expected)
        require(listed[rel]["sha256"] == expected and listed[rel]["bytes"] == len(raw),
                f"embedded t55 artifact record {rel}")
    field_slots = load_json(ROOT / "scratch/t55/out/field_slots.json")
    field_map = load_json(ROOT / "scratch/t55/out/field_map.json")
    abc = load_json(ROOT / "scratch/t55/out/abc_closure.json")
    require(section["source_records"]["field_slots"] == field_slots and
            section["source_records"]["field_map"] == field_map, "embedded source records differ")
    require(section["abc_closure_reference"]["source_record"] == abc and
            section["abc_closure_reference"]["segments"] == abc["segments"], "embedded ABC closure differs")
    return field_slots, field_map, abc


def verify_main_row(section: dict[str, Any], field_slots: dict[str, Any], field_map: dict[str, Any], abc: dict[str, Any]) -> None:
    require(section["source_task"] == "t55" and section["acceptance_ledger_entry"] == "E94" and
            section["acceptance_ledger_level"] == "L3" and section["evidence_level"] == {"L3_fields": 5, "L4": 0},
            "main-row section provenance")
    require(field_slots["source"]["entry"] == 17038016 and field_slots["source"]["end_exclusive"] == 17042404 and
            field_slots["source"]["reachable"] == 992 and field_slots["source"]["external_edges"] == [] and
            field_slots["source"]["stream_slot_28_count"] == 40, "main-row source bounds")
    require(field_map["fields_total"] == 346 and field_map["positions_with_unique_XML"] == 15 and
            field_map["grade_counts"] == EXPECTED_GRADES and sum(EXPECTED_GRADES.values()) == 346,
            "main-row field counts")
    records = field_map["fields"]
    require(len(records) == 346 and section["field_census"]["grade_counts"] == EXPECTED_GRADES,
            "complete field map and grade counts")
    record_by_code = {item["code"]: item for item in records}
    slot_by_pos = {item["position"]: item for item in field_slots["slots"]}
    require({code: (record_by_code[code]["slot"], record_by_code[code]["xml_index"],
                    slot_by_pos[record_by_code[code]["slot"]].get("target_table"))
             for code in EXPECTED_L3} == EXPECTED_L3, "five L3 field positions/targets")
    l3_records = [item for item in records if item["grade"] == "L3"]
    section_l3 = {item["code"]: item for item in section["L3_fields"]}
    require(set(section_l3) == set(EXPECTED_L3), "section L3 set")
    for item in l3_records:
        pos, xml_index, target = EXPECTED_L3[item["code"]]
        slot = slot_by_pos[pos]
        projection = section_l3[item["code"]]
        require((projection["xml_index"], projection["wire_position"], projection.get("target_table")) ==
                (xml_index, pos, target), f"L3 projection {item['code']}")
        require(slot["candidate_4cc"] == item["code"], f"slot code {item['code']}")
    require(section["grade_membership"] == {
        grade: [item["code"] for item in records if item["grade"] == grade]
        for grade in EXPECTED_GRADES
    }, "grade membership including held/unmapped")
    require(record_by_code["EDsc"]["grade"] == "held" and record_by_code["TCrs"]["grade"] == "no_main_wire_slot" and
            record_by_code["EDfx"]["grade"] == "no_wire_slot", "source held/no-slot grade distinctions")
    require(field_map["supplemental"]["Npop"]["status"] == "held_out_of_schema", "supplemental Npop scope")
    require(field_map["order"]["status"] == "mismatch" and field_map["order"]["inversions"] == 46 and
            field_map["order"]["first_counterexample"] == {
                "earlier": {"position": 1, "xml_index": 21, "code": "Nnsi"},
                "later": {"position": 15, "xml_index": 16, "code": "Ncti"},
            }, "wire/XML inversion evidence")
    require(section["order"] == field_map["order"] and
            section["ordering_policy"] == "wire 顺序≠XML 顺序，后续映射不得按 XML 序号对齐",
            "wire/XML policy")
    require(abc["status"] == "A_B_C_D_explained_for_both_modes" and
            abc["original_sha256"] == sha((ROOT / abc["original"]).read_bytes()), "ABC source closure identity")
    expected_segments = {
        "A": ("Nlns", 23, 5, 492), "B": ("Nefr", 24, 28, 214),
        "C": ("Nnfr", 25, 28, 63), "D": ("Nagr", 26, 12, 162),
    }
    for label, (parent, position, stride, items) in expected_segments.items():
        segment = abc["segments"][label]
        client, server = segment["profiles"]["client"], segment["profiles"]["server"]
        require((segment["parent"], segment["position"], segment["item_stride"]) ==
                (parent, position, stride), f"ABC identity {label}")
        require(client["rows"] == server["rows"] == 251 and client["items"] == server["items"] == items and
                client["counts"] == server["counts"], f"ABC dual-mode distributions {label}")
        require(segment["original_negative"] is not None, f"ABC original negative retained {label}")


def verify_coverage(baseline: dict[str, Any], schema: dict[str, Any]) -> None:
    old = baseline["coverage"]
    new = schema["coverage"]
    for key, value in old.items():
        if key not in OLD_COVERAGE_EDITABLE:
            require(new.get(key) == value, f"coverage field changed outside nation increment: {key}")
    for key in ("club_L3_occurrences", "club_L3_unique_wire_fields", "club_auxiliary_sources", "club_auxiliary_views"):
        if key in old:
            require(new.get(key) == old[key], f"club coverage changed: {key}")
    require(new["nation_L3_occurrences"] == old["nation_L3_occurrences"] + 5 == 35 and
            new["nation_L3_unique_wire_fields"] == old["nation_L3_unique_wire_fields"] + 5 == 35 and
            new["nation_held_occurrences"] == old["nation_held_occurrences"] + 5 == 25 and
            new["nation_negative_records"] == old["nation_negative_records"] == 15,
            "nation coverage counters")
    ids = old["nation_L3_unique_wire_field_ids"]
    added = ["t10/main/Nnsi", "t10/main/Ncti", "t10/main/Nrgi", "t10/main/Ncur", "t10/main/Nndn"]
    require(new["nation_L3_unique_wire_field_ids"] == [*ids, *added] and len(set(new["nation_L3_unique_wire_field_ids"])) == 35,
            "nation unique IDs appended")
    policy = new["nation_coverage_policy"]
    require(policy.startswith(old["nation_coverage_policy"]) and
            "wire 顺序≠XML 顺序，后续映射不得按 XML 序号对齐" in policy,
            "nation policy additive warning")
    old_side = old["nation_side"]
    new_side = new["nation_side"]
    for key, value in old_side.items():
        require(new_side.get(key) == value, f"previous nation-side coverage changed: {key}")
    row = new_side["t55_main_row_census"]
    require(row["acceptance_ledger_entry"] == "E94" and row["acceptance_ledger_level"] == "L3" and
            row["fields_total"] == 346 and row["positions_with_unique_XML"] == 15 and
            row["L3_fields"] == 5 and row["L4"] == 0 and row["grade_counts"] == EXPECTED_GRADES,
            "additive nation-side t55 summary")


def verify() -> None:
    check_hash(V5_JSON, V5_JSON_SHA256)
    check_hash(V5_MD, V5_MD_SHA256)
    v6_json_raw = check_hash(V6_JSON, V6_JSON_SHA256)
    v6_md_raw = check_hash(V6_MD, V6_MD_SHA256)
    baseline = json.loads(v6_json_raw)
    require(load_json(V5_JSON)["schema_version"] == 5 and baseline["schema_version"] == 6,
            "baseline schema versions")
    public_json = check_hash(PUBLIC_JSON, sha(V7_JSON.read_bytes()))
    public_md = check_hash(PUBLIC_MD, sha(V7_MD.read_bytes()))
    require(public_json == V7_JSON.read_bytes() and public_md == V7_MD.read_bytes(), "public/output pair mismatch")
    schema = json.loads(public_json)
    require(schema["schema_version"] == 7 and schema["generated_by"] == "t56", "public v7 identity")
    require(public_md.startswith(v6_md_raw), "Markdown v6 prefix changed")
    expected_root = set(baseline) | {"nation_main_row_fields"}
    require(set(schema) == expected_root, "schema root keys changed outside additive section")
    for key in PROTECTED:
        require(schema.get(key) == baseline.get(key), f"protected block changed: {key}")
    for key, value in baseline.items():
        if key not in {"schema_version", "generated_by", "coverage", "incremental_provenance"}:
            require(schema.get(key) == value, f"root data changed: {key}")
    section = schema["nation_main_row_fields"]
    field_slots, field_map, abc = verify_sources(section)
    verify_main_row(section, field_slots, field_map, abc)
    verify_coverage(baseline, schema)
    verify_ledger(baseline, schema)
    provenance = schema["incremental_provenance"]
    old_prov = baseline["incremental_provenance"]
    for key, value in old_prov.items():
        if key not in {"acceptance_ledger_entries", "tasks"}:
            require(provenance.get(key) == value, f"prior incremental provenance changed: {key}")
    for key, value in old_prov["tasks"].items():
        require(provenance["tasks"].get(key) == value, f"prior task changed: {key}")
    for key, value in old_prov["acceptance_ledger_entries"].items():
        require(provenance["acceptance_ledger_entries"].get(key) == value, f"prior ledger record changed: {key}")
    appendix = public_md[len(v6_md_raw):].decode("utf-8")
    for token in ("t56 — t55 Nation", "46 个倒置对", "`EDsc=held`", "`TCrs=no_main_wire_slot`",
                  "`EDfx=no_wire_slot`", "A/B/C/D 收口", E94_SHA256, E95_SHA256):
        require(token in appendix, f"Markdown addendum missing {token}")
    report = (OUT / "REPORT.md").read_text(encoding="utf-8")
    done = (OUT / "DONE.md").read_text(encoding="utf-8")
    require(sha(public_json) in report and sha(public_md) in report and
            sha(public_json) in done and sha(public_md) in done, "report/DONE output hashes")
    print("t56 verify PASS: v5/v6 snapshots; entry-level E87-E95 guards; protected blocks; 5 L3; 35/35/25 nation counters; ABC; Markdown prefix")


def selftest() -> None:
    require(len(canonical_sha("t56")) == 64, "canonical SHA helper")
    require(sum(EXPECTED_GRADES.values()) == 346 and len(EXPECTED_L3) == 5, "static census invariants")
    require(set(NEW_GUARDS) == {"E94", "E95"}, "ledger guard set")
    print("t56 verifier selftest PASS")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--check", action="store_true", help="verify public v7 and all pinned sources (default)")
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
