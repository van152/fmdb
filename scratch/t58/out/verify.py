#!/usr/bin/env python3
"""Independent verifier for the additive t58 public schema v8 consolidation."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PUBLIC_JSON = ROOT / "reports" / "club_nation_subtable_schema.json"
PUBLIC_MD = ROOT / "reports" / "club_nation_subtable_schema.md"
V7_JSON = HERE / "club_nation_subtable_schema.v7.json"
V7_MD = HERE / "club_nation_subtable_schema.v7.md"
V8_JSON = HERE / "club_nation_subtable_schema.v8.json"
V8_MD = HERE / "club_nation_subtable_schema.v8.md"
V7_JSON_SHA256 = "d93a5070489c737e5d70fa2b8ffb135f9d4135d70df7ae4b6e2d27a4379ded10"
V7_MD_SHA256 = "f84d265c2ca067794bd98f8ddb15cda026dc2b63bd185bd3db0eab43bd6b83bc"
LEDGER_PATH = ROOT / "scratch" / "t01" / "LEDGER.json"
E96_SHA256 = "8fa14c406df939da7d1024eccdb2ed26e876071f9efef64270a998b9eb74cc92"
E97_SHA256 = "ba5a1079403dd970b30c9304a90c37d5a66f3d28163ee2cf2588fd355129ff32"
OLD_GUARDS = ("E87", "E89", "E90", "E91", "E92", "E93", "E94", "E95")
NEW_GUARDS = ("E96", "E97")
PROTECTED_ROOT_KEYS = (
    "tables", "negative_regressions", "v3_baseline", "club_auxiliary_sources",
    "nation_data_side_status", "nation_static_side", "nation_t9_wire",
    "nation_main_row_fields",
)
EXPECTED_L3 = [
    "duni", "Cext", "Cedp", "Cnti", "Cbni", "Cccn", "Cncl",
    "Ccty", "CIns", "CASt", "Csot", "Ctsi", "CnCV",
]
EXPECTED_NEW_L3 = ["Cext", "Cedp", "Cncl", "CIns", "Ctsi"]
EXPECTED_GRADES = {
    "L3": 13,
    "held": 11,
    "skipped_separate_member": 10,
    "unmapped": 399,
}
T57_ARTIFACTS = {
    "scratch/t57/out/field_slots.json": "da3d3abd76e3d96a4db989c2dec3fcc1d352d1ccaac5267b00ab12731bbd6489",
    "scratch/t57/out/field_map.json": "0b04de7b15c455ccb85212d43221d5cbecb8fd5ccbf830ba71d5f4f3011f3664",
    "scratch/t57/out/instructions.part001.json": "c64bff5a17030f28ee0421ae0b3985b1eefd128deb881e8c0f123a3341d78050",
    "scratch/t57/out/instructions.part002.json": "4337bb0938b35a58cb153337126696819489ca4a36e16c5abc92cc2cf0d50468",
    "scratch/t57/out/instructions.part003.json": "f411ce54f3efa13bd2c5e42ec6d36a2572a6b5142807b94731a03ba311c8b6cd",
    "scratch/t57/out/instructions.part004.json": "462a0be204e0773ef66187d6f48c7d84c052525c5f53b6caca89a96ff6e56e13",
    "scratch/t57/out/instructions.part005.json": "0c31d8463915377c5047bd939a70c5a6c16bd769003ae5e325a37decb8f45430",
    "scratch/t57/out/instructions.part006.json": "b1a0181c75624ed0f718e6b57df419fcb0056341804a2a5210dc3526201f93ef",
    "scratch/t57/out/instructions.part007.json": "92af197f476d2a24ec3da7194d0ce4965b5698440fa322f814c7ca50aa58bc14",
    "scratch/t57/out/instructions.part008.json": "abca0e9f801141ff790b615c65644e961cf9298d5093ee492506499b39dc5697",
    "scratch/t57/out/instructions.part009.json": "a929a281336715b5c2607614fe609bbfbbf0d363102e24d58382251efff5d6b3",
    "scratch/t57/out/branches.part001.json": "078d39d16dedf15bb40f7a71f2eef622e08976fc70b00702a91985feeab931f5",
    "scratch/t57/out/branches.part002.json": "f568689b41f98df396c31ead1af542a243a9e813b006b5a49e2337bb5a830a63",
    "scratch/t57/out/branches.part003.json": "a5f49fb76eb87588e21c70d628c8f80cfcc574dcadfd5467626c26ecbdc8a444",
    "scratch/t57/out/verify.py": "396064544983619d568127432c97e91a685179330e5dec65afcd7e3c4789ed3f",
    "scratch/t57/out/REPORT.md": "8149962abe4a221e48a7880aea0bb81037f89cbc2a14fb9ad8259e04fcddcfb1",
    "scratch/t57/out/DONE.md": "f87808aafb5d40858ac0c0c81030af0738537abc7fd0de9c3f6adf6bd683ca7d",
    "scripts/t57_clubmain_fields.py": "c189ce419f2fedcba172e2d78f5d024dcd5f70c48de424e41c83f4cf6c7be32b",
}


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
    ledger = load_json(LEDGER_PATH)
    wanted = {*OLD_GUARDS, *NEW_GUARDS}
    found: dict[str, dict[str, Any]] = {}
    for entry in ledger["entries"]:
        if entry.get("id") in wanted:
            entry_id = entry["id"]
            require(entry_id not in found, f"duplicate live ledger entry {entry_id}")
            found[entry_id] = entry
    require(set(found) == wanted, "entry-level ledger guard set incomplete")
    baseline_recorded = baseline["incremental_provenance"]["acceptance_ledger_entries"]
    recorded = schema["incremental_provenance"]["acceptance_ledger_entries"]
    for entry_id in OLD_GUARDS:
        actual = found[entry_id]
        expected = baseline_recorded[entry_id]
        require(actual.get("kind") == expected.get("kind") and actual.get("level") == expected.get("level") and
                canonical_sha(actual.get("claim")) == expected.get("claim_sha256"),
                f"baseline ledger guard {entry_id}")
        require(recorded[entry_id] == expected, f"existing schema ledger record changed: {entry_id}")
    for entry_id, expected_sha in (("E96", E96_SHA256), ("E97", E97_SHA256)):
        actual = found[entry_id]
        require((actual.get("kind"), actual.get("level"), canonical_sha(actual.get("claim"))) ==
                ("acceptance", "L3", expected_sha), f"new ledger guard {entry_id}")
        row = recorded[entry_id]
        require((row.get("kind"), row.get("level"), row.get("claim_sha256")) ==
                ("acceptance", "L3", expected_sha), f"schema ledger record {entry_id}")
    snapshot = schema["incremental_provenance"]["t57_ledger_snapshot"]
    require(snapshot["path"] == "scratch/t01/LEDGER.json" and
            snapshot["guarded_entries"] == [*OLD_GUARDS, *NEW_GUARDS] and
            snapshot["t56_acceptance_entry"] == "E96" and snapshot["t56_acceptance_level"] == "L3" and
            snapshot["t57_acceptance_entry"] == "E97" and snapshot["t57_acceptance_level"] == "L3" and
            "no live full-file hash" in snapshot["guard_scope"], "entry-only t57 ledger provenance")


def verify_sources(section: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    listed = {row["path"]: row for row in section["source_artifacts"]}
    require(set(listed) == set(T57_ARTIFACTS), "t57 artifact manifest path set")
    for rel, expected in T57_ARTIFACTS.items():
        raw = check_hash(ROOT / rel, expected)
        require(listed[rel]["sha256"] == expected and listed[rel]["bytes"] == len(raw),
                f"embedded t57 artifact record {rel}")
    field_slots = load_json(ROOT / "scratch/t57/out/field_slots.json")
    field_map = load_json(ROOT / "scratch/t57/out/field_map.json")
    require(section["source_records"]["field_slots"] == field_slots and
            section["source_records"]["field_map"] == field_map,
            "embedded t57 source records differ")
    return field_slots, field_map


def verify_main_row(section: dict[str, Any], field_slots: dict[str, Any], field_map: dict[str, Any]) -> None:
    require(section["source_task"] == "t57" and section["acceptance_ledger_entry"] == "E97" and
            section["acceptance_ledger_level"] == "L3" and section["evidence_level"] == {"L3_fields": 13, "L4": 0},
            "main-row section provenance")
    require(field_slots["status"] == "observed_dual_archive_outer_census_complete_unobserved_dispatch_not_replayed" and
            field_map["fields_total"] == 433 and field_map["fields_with_unique_XML_alignment"] == 18 and
            field_map["domain_pass_L3"] == 13 and field_map["new_L3"] == EXPECTED_NEW_L3 and
            field_map["grade_counts"] == EXPECTED_GRADES and sum(EXPECTED_GRADES.values()) == 433,
            "t57 field counts")
    require(len(field_slots["slots"]) == 34 and [x["position"] for x in field_slots["slots"]] == list(range(34)),
            "t57 logical positions")
    main = field_slots["source"]["runtime_function_extents"]["15050656"]
    reader = section["outer_sequence_closure"]["reader"]
    require((reader["vtable_slot"], reader["file_offset"], reader["file_offset_hex"], reader["reachable_instructions"], reader["conditional_branches"], reader["external_edges"]) ==
            (19, 15050656, "0xe5a7a0", 1412, 167, []) and
            main["end_exclusive"] == reader["extent_end_exclusive"] == 15056842,
            "t57 reader closure")
    require(section["outer_sequence_closure"]["positions"] == 34 and
            section["outer_sequence_closure"]["archive_modes"] == field_slots["envelopes"] and
            section["outer_sequence_closure"]["execution_templates"] == field_slots["execution_templates"],
            "t57 envelope/templates projection")
    env = field_slots["envelopes"]
    require((env["client"]["payload"], env["server"]["payload"], env["client"]["rows"], env["server"]["rows"]) ==
            (6932082, 16595312, 84259, 84259), "t57 payload/row assertions")
    identity = section["identity_framing"]
    require(identity["native_tail_width"] == 12 and identity["layout"] == "ordinal | UID | UID" and
            identity["footer_hex"] == "0000000001e3c03a77" and identity["selector_counts"] == {"0": 84256, "12": 3},
            "t57 identity framing")
    negative = identity["thirteen_byte_first_counterexample"]
    require(negative == {
        "ordinal": 69705, "client_absolute": 5705237, "server_absolute": 14067615,
        "raw": "491001003145d8053145d8050c", "next_selector": "0c",
    }, "t57 13-byte counterexample")
    require(identity["footer_width_sensitivity"] == {"footer_7": 0, "footer_8": 0, "footer_9": 1, "footer_10": 0, "footer_12": 0},
            "t57 footer sensitivity")

    records = field_map["fields"]
    l3_records = [item for item in records if item["grade"] == "L3"]
    projections = section["L3_fields"]
    require([item["code"] for item in l3_records] == EXPECTED_L3 and
            [item["code"] for item in projections] == EXPECTED_L3,
            "t57 L3 field set/order")
    slots_by_pos = {item["position"]: item for item in field_slots["slots"]}
    for record, projection in zip(l3_records, projections, strict=True):
        pos = record["candidate_position"]
        require(projection["source_record"] == record and projection["slot_record"] == slots_by_pos[pos] and
                projection["wire_position"] == pos and projection["accepted_position"] == pos and
                projection["xml_index"] == record["xml_index"] and projection["slot_key"] == slots_by_pos[pos]["key"],
                f"t57 L3 projection {record['code']}")
    membership = {}
    for record in records:
        membership.setdefault(record["grade"], []).append(record["code"])
    require(section["grade_membership"] == membership, "t57 held/unmapped membership")
    require(section["field_census"] == {
        "fields_total": 433,
        "fields_with_unique_XML_alignment": 18,
        "alignment_ratio": field_map["alignment_ratio"],
        "grade_counts": EXPECTED_GRADES,
        "new_L3": EXPECTED_NEW_L3,
    }, "t57 census projection")
    require(section["order"] == field_map["order"] and
            section["ordering_policy"] == "wire 顺序≠XML 顺序，后续映射不得按 XML 序号对齐" and
            section["order"]["inversions"] == 72 and
            section["order"]["first_counterexample"] == [[3, 13, "Cext"], [10, 6, "Cnam"]],
            "t57 inversion projection")
    require(section["source_report_note"]["report_path"] == "scratch/t57/out/REPORT.md" and
            section["source_report_note"]["done_path"] == "scratch/t57/out/DONE.md" and
            "verbatim t57 occurrence ledger" in section["source_report_note"]["held_and_unmapped_records"],
            "t57 preservation note")
    preserved = section["negative_regressions_preserved"]
    require(preserved["E60_original_Cccn_negative"] == field_map["regression"]["original_Cccn_negative"] and
            preserved["true_binding_note"] ==
            "Cccn is bound at +0xf0, the fourth u32 transfer; +0xe8, the third u32 transfer, is Cbni.",
            "E60 negative and true Cccn binding")


def verify_coverage(baseline: dict[str, Any], schema: dict[str, Any]) -> None:
    old = baseline["coverage"]
    new = schema["coverage"]
    for key, value in old.items():
        require(new.get(key) == value, f"existing coverage changed: {key}")
    expected = {
        "club_main_row_occurrences": 433,
        "club_main_row_aligned": 18,
        "club_main_row_L3": 13,
        "club_main_row_held": 11,
        "club_main_row_skipped_separate_member": 10,
        "club_main_row_unmapped": 399,
        "club_main_row_new_L3": 5,
        "club_main_row_order_inversions": 72,
        "club_main_row_L4": 0,
    }
    for key, value in expected.items():
        require(new.get(key) == value, f"club main coverage {key}")
    policy = "Identity-tail and footer widths are table-specific evidence. Derive and verify each table independently; never copy another table's identity or footer width, including the nation 13-byte versus club 12-byte distinction."
    coverage_keys = list(new)
    require(new.get("row_identity_footer_width_policy") == policy and
            coverage_keys.index("row_identity_footer_width_policy") == coverage_keys.index("nation_coverage_policy") + 1,
            "table-specific identity/footer policy placement")
    require(new["club_L3_occurrences"] == 94 and new["club_L3_unique_wire_fields"] == 59 and
            new["held_fields"] == 21 and new["negative_regressions"] == 4,
            "club subtable coverage changed")


def verify() -> None:
    v7_json_raw = check_hash(V7_JSON, V7_JSON_SHA256)
    v7_md_raw = check_hash(V7_MD, V7_MD_SHA256)
    baseline = json.loads(v7_json_raw)
    require(baseline["schema_version"] == 7 and baseline["generated_by"] == "t56", "v7 baseline identity")
    v8_json_raw = V8_JSON.read_bytes()
    v8_md_raw = V8_MD.read_bytes()
    public_json = PUBLIC_JSON.read_bytes()
    public_md = PUBLIC_MD.read_bytes()
    require(public_json == v8_json_raw and public_md == v8_md_raw, "public/output pair mismatch")
    schema = json.loads(public_json)
    require(schema["schema_version"] == 8 and schema["generated_by"] == "t58", "public v8 identity")
    require(public_md.startswith(v7_md_raw), "Markdown v7 prefix changed")
    expected_root = set(baseline) | {"club_main_row_fields"}
    require(set(schema) == expected_root, "schema root keys changed outside additive section")
    for key in PROTECTED_ROOT_KEYS:
        require(schema.get(key) == baseline.get(key), f"protected block changed: {key}")
    for key, value in baseline.items():
        if key not in {"schema_version", "generated_by", "coverage", "incremental_provenance"}:
            require(schema.get(key) == value, f"root data changed: {key}")
    section = schema["club_main_row_fields"]
    field_slots, field_map = verify_sources(section)
    verify_main_row(section, field_slots, field_map)
    appendix = public_md[len(v7_md_raw):].decode("utf-8")
    require(field_map["regression"]["original_Cccn_negative"] in appendix and
            "第四次 u32 transfer" in appendix and "Cccn" in appendix,
            "E60 original negative and true binding appear in Markdown")
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
    report = (HERE / "REPORT.md").read_text(encoding="utf-8")
    done = (HERE / "DONE.md").read_text(encoding="utf-8")
    require(sha(v8_json_raw) in report and sha(v8_md_raw) in report and
            sha(v8_json_raw) in done and sha(v8_md_raw) in done,
            "report/DONE output hashes")
    for token in (
        V7_JSON_SHA256, V7_MD_SHA256, "E97", "1,412", "167", "6,932,082", "16,595,312",
        "84,259", "identity 12 B", "13 L3", "72 inversions", "69705",
        "club_L3_occurrences=94", "Csnm", "CLat/CLon", "Csti", "Cyfn",
    ):
        require(token in report or token in done, f"delivery token missing: {token}")
    print(
        "t58 independent verify PASS: "
        f"v7 snapshot {V7_JSON_SHA256} / {V7_MD_SHA256}; "
        "protected tables/negative/v3/club_auxiliary/nation sections; "
        "84259+84259 rows; identity 12B; 1412 instructions/167 branches; "
        "13 L3/11 held/10 skipped/399 unmapped; 72 inversions; entry guards E87,E89-E97; L4=0"
    )


def selftest() -> None:
    require(len(E96_SHA256) == len(E97_SHA256) == 64, "ledger SHA constants")
    require(sum(EXPECTED_GRADES.values()) == 433 and len(EXPECTED_L3) == 13 and len(EXPECTED_NEW_L3) == 5,
            "static t57 census invariants")
    require(["E87", "E89", "E90", "E91", "E92", "E93", "E94", "E95", "E96", "E97"] ==
            [*OLD_GUARDS, *NEW_GUARDS], "guard chain")
    print("t58 verifier selftest PASS")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--check", action="store_true", help="verify public v8 and pinned sources (default)")
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
