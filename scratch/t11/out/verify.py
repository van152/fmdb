from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from collections import Counter
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
SCHEMA = ROOT / "scratch/t05/schema_inventory.json"
LAYOUTS = ROOT / "scratch/t05/layouts.json"
T07 = ROOT / "scratch/t07/out/naming_result.json"
T08 = ROOT / "scratch/t08/out/naming_result.json"
NAMING = OUT / "naming_result.json"
SCHEMA_MAP = OUT / "schema_map.json"
SMALL = OUT / "small_tables.json"
UNIVERSAL = {"duni", "rdui", "NDBC", "FDBC", "dbnm"}
INJURY = {
    "icla": (0x4C, 1), "iscl": (0x4D, 1), "Imnd": (0x34, 2), "Iexd": (0x36, 2),
    "Iiar": (0x58, 1), "Irec": (0x59, 1), "Iocr": (0x30, 4), "Imip": (0x50, 1),
    "Iagr": (0x51, 1), "Icms": (0x52, 1), "Icon": (0x53, 1), "inSr": (0x54, 1),
    "Icdp": (0x56, 1),
}
CITY = {"Clat": (0x48, 4), "Clon": (0x4C, 4), "Cnti": (0x20, 4),
        "Cwea": (0x28, 4), "Clgi": (0x30, 4), "Clri": (0x38, 4)}
SMALL_IDS = {23, 31, 35, 42, 46, 50, 51, 60, 61, 63, 64}


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def code_tokens(field):
    codes = field.get("codes") or []
    if codes:
        return list(codes)
    value = field.get("field")
    return [x for x in re.split(r"[+|]", value) if x] if value else []


def load_pe():
    spec = importlib.util.spec_from_file_location("t11_verify_pe", ROOT / "scripts/t05_pe.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load scripts/t05_pe.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.default()


def normalized(text):
    return " ".join(text.lower().split())


def selftest():
    assert code_tokens({"field": "A+B", "codes": ["A", "B"]}) == ["A", "B"]
    assert code_tokens({"field": "A|B"}) == ["A", "B"]
    assert "duni" in UNIVERSAL and len(INJURY) == 13 and len(CITY) == 6
    print("verify.py selftest: OK")
    return 0


def check():
    failures = []
    schema = load(SCHEMA)["entities"]
    layouts = {x["type_id"]: x for x in load(LAYOUTS)["layouts"]}
    baseline = load(T07)
    t08 = load(T08)
    naming = load(NAMING)
    mapping = load(SCHEMA_MAP)
    small = load(SMALL)
    schema_by_type = {x["type_id"]: x.get("schema_entity") for x in mapping.get("entities", [])}
    out_by_type = {x["type_id"]: x for x in naming.get("results", [])}

    if not str(naming.get("status", "")).startswith("complete_"):
        failures.append(f"naming status incomplete: {naming.get('status')!r}")
    if not str(mapping.get("status", "")).startswith("complete_"):
        failures.append(f"schema_map status incomplete: {mapping.get('status')!r}")
    if not str(small.get("status", "")).startswith("complete_"):
        failures.append(f"small_tables status incomplete: {small.get('status')!r}")

    # Hard allow-list: derive each schema field set live; do not encode the known bad-name list.
    named_total = 0
    illegal = []
    for entity in naming.get("results", []):
        tid = entity["type_id"]
        schema_name = schema_by_type.get(tid)
        if schema_name not in schema:
            if any(f.get("field") is not None for a in entity.get("archives", {}).values()
                   for f in a.get("fields", [])):
                failures.append(f"type {tid} has named fields but no schema mapping")
            continue
        allowed = {f.get("code") for f in schema[schema_name].get("fields", []) if f.get("code")} | UNIVERSAL
        for archive, spec in entity.get("archives", {}).items():
            for field in spec.get("fields", []):
                if field.get("field") is None:
                    continue
                named_total += 1
                for code in code_tokens(field):
                    if code not in allowed:
                        illegal.append((tid, archive, field.get("idx"), code, schema_name))
    if illegal:
        failures.append(f"schema-illegal field codes remain: {illegal}")

    # t07 zero-regression: compare the 45 pre-existing names at exact (type, archive, idx).
    old_names = {}
    for entity in baseline.get("results", []):
        for archive, spec in entity.get("archives", {}).items():
            for field in spec.get("fields", []):
                if field.get("field") is not None:
                    old_names[(entity["type_id"], archive, field["idx"])] = field["field"]
    preserved = 0
    for key, old_name in old_names.items():
        tid, archive, idx = key
        current_entity = out_by_type.get(tid, {})
        current_spec = current_entity.get("archives", {}).get(archive, {})
        current = next((f for f in current_spec.get("fields", []) if f.get("idx") == idx), None)
        if current is None or current.get("field") != old_name:
            failures.append(f"t07 baseline changed at {key}: {old_name!r} -> {current.get('field') if current else None!r}")
        else:
            preserved += 1
    if len(old_names) != 45 or preserved != 45:
        failures.append(f"t07 named-slot preservation {preserved}/{len(old_names)}, expected 45/45")

    def calibration_hit(code, expected):
        for entity in naming.get("results", []):
            for spec in entity.get("archives", {}).values():
                for field in spec.get("fields", []):
                    for access in field.get("accesses", []):
                        if access.get("code") == code and (access.get("object_off"), access.get("size")) == expected:
                            return True
                    if code in field.get("codes", []) and (field.get("object_off"), field.get("width")) == expected:
                        return True
        return False

    injury_ok = sum(calibration_hit(code, expected) for code, expected in INJURY.items())
    city_ok = sum(calibration_hit(code, expected) for code, expected in CITY.items())
    if injury_ok != 13:
        failures.append(f"injury calibration {injury_ok}/13")
    if city_ok != 6:
        failures.append(f"city calibration {city_ok}/6")

    # Independently re-disassemble all 84 original t08 chain_unique access records at their VA.
    pe = load_pe()
    from capstone import CS_ARCH_X86, CS_MODE_64, Cs
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    source_accesses = [access
        for entity in t08.get("results", [])
        for spec in entity.get("archives", {}).values()
        for field in spec.get("fields", [])
        if field.get("confidence") == "chain_unique"
        for access in field.get("accesses", [])]
    instruction_ok = 0
    for access in source_accesses:
        try:
            va = int(access["access_va"], 16)
            file_off = pe.va2f(va)
            actual = next(iter(md.disasm(pe.raw[file_off:file_off + 16], va)), None) if file_off is not None else None
            declared = access.get("instruction", "")
            if actual and actual.address == va and normalized(f"{actual.mnemonic} {actual.op_str}") == normalized(declared):
                instruction_ok += 1
            else:
                failures.append(f"VA instruction mismatch at {access.get('access_va')}: declared={declared!r}, actual={actual}")
        except Exception as exc:
            failures.append(f"cannot verify access {access}: {exc}")
    if len(source_accesses) != 84 or instruction_ok != 84:
        failures.append(f"t08 access audit {instruction_ok}/{len(source_accesses)}, expected 84/84")

    # Required ref_ptr anchors use reader width, not the qword getter's 8B width.
    anchor_expect = {"Sold": (32, 4, 4), "Snew": (40, 4, 8), "Salt": (72, 4, 17)}
    type22 = out_by_type.get(22, {})
    anchor_ok = 0
    for code, (off, width, row_off) in anchor_expect.items():
        found = False
        for archive, spec in type22.get("archives", {}).items():
            for field in spec.get("fields", []):
                if (field.get("field") == code and field.get("object_off") == off and
                        field.get("width") == width and field.get("row_off") == row_off and
                        field.get("confidence") == "ref_pair" and
                        any(a.get("code") == code and a.get("kind") == "ref_ptr" and
                            a.get("object_off") == off and a.get("size") == width
                            for a in field.get("accesses", []))):
                    found = True
        anchor_ok += found
        if not found:
            failures.append(f"ref_ptr anchor missing/bad: {code} obj={off} row+{row_off}/w{width}")
    if anchor_ok != 3:
        failures.append(f"Sold/Snew/Salt ref_ptr anchors {anchor_ok}/3")

    # Immutable layout closure and row offsets/widths.
    for tid, layout in layouts.items():
        current_entity = out_by_type.get(tid)
        if not current_entity:
            failures.append(f"type {tid} missing from naming result")
            continue
        for archive, source in layout.get("archives", {}).items():
            current = current_entity.get("archives", {}).get(archive)
            if not current:
                failures.append(f"type {tid} missing archive {archive}")
                continue
            src_fields = source.get("fields", [])
            out_fields = current.get("fields", [])
            if len(src_fields) != len(out_fields):
                failures.append(f"type {tid}/{archive} field count changed")
                continue
            for before, after in zip(src_fields, out_fields):
                if (before.get("idx"), before.get("row_off"), before.get("width")) != (
                        after.get("idx"), after.get("row_off"), after.get("width")):
                    failures.append(f"type {tid}/{archive}/idx {before.get('idx')} row_off/width changed")
            actual = sum(f.get("width", 0) for f in out_fields)
            if actual != source.get("business_width") or actual != current.get("business_width"):
                failures.append(f"type {tid}/{archive} sum(width)={actual}, business_width={source.get('business_width')}")

    # Every requested small table has an explicit unique/ambiguous/no_instance result.
    small_by_type = {x["type_id"]: x for x in small.get("tables", [])}
    if set(small_by_type) != SMALL_IDS:
        failures.append(f"small table coverage mismatch: {sorted(small_by_type)}")
    for tid, row in small_by_type.items():
        if row.get("status") not in {"unique_solution", "ambiguous", "no_instance"}:
            failures.append(f"type {tid} has no explicit solution classification")
        if row.get("status") == "no_instance" and not row.get("no_instance_numeric", {}).get("intersection_empty"):
            failures.append(f"type {tid} no_instance lacks empty offset intersection proof")

    # Acceptance thresholds beyond the mandatory regression checks.
    if named_total < 138:
        failures.append(f"named slots {named_total}/240 < required 138")
    checked_unique = sum(1 for row in small.get("tables", [])
                         if row.get("status") == "unique_solution" and
                         row.get("data_side_verification", {}).get("status") == "supported")
    if checked_unique < 2:
        failures.append(f"unique small tables with supported data-side checks {checked_unique}/2")

    print(f"schema-illegal=0; t07={preserved}/45; injury={injury_ok}/13; city={city_ok}/6; "
          f"VA instructions={instruction_ok}/{len(source_accesses)}; ref_ptr={anchor_ok}/3; "
          f"named={named_total}/240; data-verified unique tables={checked_unique}/2")
    if failures:
        for failure in failures:
            print("FAIL:", failure)
        return 1
    print("PASS: schema constraints, regression anchors, ref_ptr, layout closure, and acceptance thresholds")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Verify t11 schema naming and regression/acceptance gates.")
    ap.add_argument("--selftest", action="store_true", help="run pure helper tests")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    try:
        return check()
    except Exception as exc:
        print(f"FATAL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
