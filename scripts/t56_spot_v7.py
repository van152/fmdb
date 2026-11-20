#!/usr/bin/env python3
"""Independent spot checks for the t56 additive schema v7 release."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "scratch/t56/out"
V5_JSON_SHA = "03967c9157fe0ca46d741e5bd74f9cd4d8df592045ca2dd6c38827f99eb36184"
V5_MD_SHA = "4e40595cb7734df534c4ab145b96855fada9da38f711454f27d3cfedf5e6c009"
V6_JSON_SHA = "02751ef7c79c60dfcf14bfbad5fe10e2077f15ed753d12e9ebfa1dfbbc010f44"
V6_MD_SHA = "a8d6509b090cd16ed7bf3d89c37638e23da120cbcfcc9e80424bd01a82234ac6"
E94_SHA = "358243779bba359656ecae6804cea9cea26b1739ffce5bf96a2599d735263c89"
E95_SHA = "2632aaae869ee3a5c1020d82e409f1f26ad429d077f06f078d5f7f1058f43eb1"
SOURCE_SHA = {
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
PROTECTED = (
    "tables", "negative_regressions", "v3_baseline", "club_auxiliary_sources",
    "nation_data_side_status", "nation_static_side", "nation_t9_wire",
)
GRADES = {"L3": 5, "held": 5, "linked_parent_held": 1, "no_main_wire_slot": 1,
          "no_wire_slot": 1, "prior_collection": 5, "prior_identity": 1, "unmapped": 327}


class SpotFailure(Exception):
    pass


def need(ok: bool, message: str) -> None:
    if not ok:
        raise SpotFailure(message)


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_sha(value: Any) -> str:
    return digest(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def load(path: Path) -> Any:
    return json.loads(path.read_bytes())


def check() -> None:
    checks = 0
    def ok(condition: bool, message: str) -> None:
        nonlocal checks
        need(condition, message)
        checks += 1
        print(f"PASS {checks:02d}: {message}")

    v5j = OUT / "club_nation_subtable_schema.v5.json"
    v5m = OUT / "club_nation_subtable_schema.v5.md"
    v6j = OUT / "club_nation_subtable_schema.v6.json"
    v6m = OUT / "club_nation_subtable_schema.v6.md"
    v7j = OUT / "club_nation_subtable_schema.v7.json"
    v7m = OUT / "club_nation_subtable_schema.v7.md"
    ok(digest(v5j.read_bytes()) == V5_JSON_SHA and digest(v5m.read_bytes()) == V5_MD_SHA, "v5 snapshot pair SHA")
    base_raw = v6j.read_bytes()
    base_md = v6m.read_bytes()
    baseline = json.loads(base_raw)
    ok(digest(base_raw) == V6_JSON_SHA and digest(base_md) == V6_MD_SHA, "v6 snapshot pair SHA")
    raw = (ROOT / "reports/club_nation_subtable_schema.json").read_bytes()
    md = (ROOT / "reports/club_nation_subtable_schema.md").read_bytes()
    schema = json.loads(raw)
    ok(raw == v7j.read_bytes() and md == v7m.read_bytes(), "public pair equals t56 output pair")
    ok(schema["schema_version"] == 7 and schema["generated_by"] == "t56", "public schema is v7/t56")
    ok(md.startswith(base_md), "v6 Markdown retained byte-for-byte as prefix")
    ok(all(schema[key] == baseline[key] for key in PROTECTED), "all protected JSON sections unchanged")
    for rel, expected in SOURCE_SHA.items():
        path = ROOT / rel
        ok(digest(path.read_bytes()) == expected, f"source pinned: {Path(rel).name}")
    field_map = load(ROOT / "scratch/t55/out/field_map.json")
    slots = load(ROOT / "scratch/t55/out/field_slots.json")
    abc = load(ROOT / "scratch/t55/out/abc_closure.json")
    section = schema["nation_main_row_fields"]
    ok(section["source_records"]["field_map"] == field_map and section["source_records"]["field_slots"] == slots,
       "full t55 field map and slot census retained")
    ok(section["field_census"]["grade_counts"] == GRADES and sum(GRADES.values()) == 346,
       "t55 grade counts total 346")
    ok(section["abc_closure_reference"]["source_record"] == abc, "t55 ABC closure record retained")
    for label, parent, position, stride, items in (
        ("A", "Nlns", 23, 5, 492), ("B", "Nefr", 24, 28, 214),
        ("C", "Nnfr", 25, 28, 63), ("D", "Nagr", 26, 12, 162),
    ):
        segment = abc["segments"][label]
        client, server = segment["profiles"]["client"], segment["profiles"]["server"]
        ok(segment["parent"] == parent and segment["position"] == position and segment["item_stride"] == stride and
           client["rows"] == server["rows"] == 251 and client["items"] == server["items"] == items and
           client["counts"] == server["counts"], f"A/B/C/D {label} both-mode profile")
    coverage = schema["coverage"]
    ok((coverage["nation_L3_occurrences"], coverage["nation_L3_unique_wire_fields"],
        coverage["nation_held_occurrences"], coverage["nation_negative_records"]) == (35, 35, 25, 15),
       "nation counters are 35/35/25/15")
    ok(coverage["nation_L3_unique_wire_field_ids"][-5:] ==
       ["t10/main/Nnsi", "t10/main/Ncti", "t10/main/Nrgi", "t10/main/Ncur", "t10/main/Nndn"],
       "five t55 identifiers append without replacing prior IDs")
    records = {row["code"]: row for row in field_map["fields"]}
    ok(records["EDsc"]["grade"] == "held" and records["TCrs"]["grade"] == "no_main_wire_slot" and
       records["EDfx"]["grade"] == "no_wire_slot", "held and no-slot source labels preserved")
    ok(field_map["order"]["inversions"] == 46 and
       field_map["order"]["first_counterexample"]["earlier"]["code"] == "Nnsi" and
       field_map["order"]["first_counterexample"]["later"]["code"] == "Ncti" and
       "wire 顺序≠XML 顺序，后续映射不得按 XML 序号对齐" in coverage["nation_coverage_policy"],
       "wire/XML order warning and first counterexample")
    ledger = load(ROOT / "scratch/t01/LEDGER.json")
    entries = {entry["id"]: entry for entry in ledger["entries"] if entry["id"] in ("E94", "E95")}
    ok(len(entries) == 2 and canonical_sha(entries["E94"]["claim"]) == E94_SHA and
       entries["E94"]["kind"] == "acceptance" and entries["E94"]["level"] == "L3", "E94 t55 L3 entry guard")
    ok(canonical_sha(entries["E95"]["claim"]) == E95_SHA and entries["E95"]["kind"] == "acceptance" and
       entries["E95"]["level"] == "L2", "E95 v6 baseline L2 entry guard")
    ok(schema["incremental_provenance"]["tasks"]["t55"]["acceptance_ledger_entry"] == "E94" and
       schema["incremental_provenance"]["t56_ledger_snapshot"]["v6_baseline_acceptance_entry"] == "E95",
       "task and baseline provenance point to correct entries")
    ok(md[len(base_md):].decode("utf-8").count("A/B/C/D 收口") == 1 and
       "E94 / L3" in md[len(base_md):].decode("utf-8"), "t55 Markdown addendum present")
    report = (OUT / "REPORT.md").read_text(encoding="utf-8")
    done = (OUT / "DONE.md").read_text(encoding="utf-8")
    ok(digest(raw) in report and digest(md) in report and digest(raw) in done and digest(md) in done,
       "REPORT/DONE schema hashes agree")
    print(f"t56 spot checks PASS: {checks}/{checks}")


def selftest() -> None:
    need(len(GRADES) == 8 and sum(GRADES.values()) == 346, "grade census")
    need(len(canonical_sha("test")) == 64, "canonical ledger hash")
    need(set(PROTECTED) >= {"tables", "nation_data_side_status", "nation_t9_wire"}, "protection keys")
    print("t56 spot selftest PASS")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--check", action="store_true", help="run independent release spot checks (default)")
    group.add_argument("--selftest", action="store_true", help="run pure spot-checker tests")
    args = parser.parse_args()
    try:
        selftest() if args.selftest else check()
        return 0
    except SpotFailure as exc:
        print(f"CHECK FAILED: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"FATAL: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
