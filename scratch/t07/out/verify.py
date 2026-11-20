from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
LAYOUTS = ROOT / "scratch/t05/layouts.json"
TABLE = OUT / "4cc_table.json"
NAMING = OUT / "naming_result.json"

# Fixed acceptance expectations from the task brief; generation itself does not use these values.
INJURY = {
    "icla": (0x4C, 1), "iscl": (0x4D, 1), "Imnd": (0x34, 2), "Iexd": (0x36, 2),
    "Iiar": (0x58, 1), "Irec": (0x59, 1), "Iocr": (0x30, 4), "Imip": (0x50, 1),
    "Iagr": (0x51, 1), "Icms": (0x52, 1), "Icon": (0x53, 1), "inSr": (0x54, 1),
    "Icdp": (0x56, 1),
}
CITY = {"Clat": 0x48, "Clon": 0x4C, "Cnti": 0x20, "Cwea": 0x28, "Clgi": 0x30, "Clri": 0x38}


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def selftest():
    assert len(INJURY) == 13 and len(CITY) == 6
    assert all(off >= 0x20 and size in (1, 2, 4) for off, size in INJURY.values())
    assert all(off >= 0x20 for off in CITY.values())
    print("verify.py selftest: OK")
    return 0


def check():
    failures = []
    layouts = load(LAYOUTS)
    table = load(TABLE)
    naming = load(NAMING)
    if not str(table.get("status", "")).startswith("complete_"):
        failures.append(f"4cc_table.status not complete: {table.get('status')!r}")
    codes = table.get("codes", {})
    for code, (off, size) in INJURY.items():
        matches = [r for r in codes.get(code, []) if r.get("object_off") == off and r.get("size") == size]
        if not matches:
            failures.append(f"injury missing {code} off={off:#x} size={size}")
    injury_ok = sum(bool([r for r in codes.get(code, []) if r.get("object_off") == off and r.get("size") == size])
                    for code, (off, size) in INJURY.items())
    for code, off in CITY.items():
        matches = [r for r in codes.get(code, []) if r.get("object_off") == off and r.get("size") == 4]
        if not matches:
            failures.append(f"city missing {code} off={off:#x} size=4")
    city_ok = sum(bool([r for r in codes.get(code, []) if r.get("object_off") == off and r.get("size") == 4])
                  for code, off in CITY.items())

    expected_layouts = {x["type_id"]: x for x in layouts.get("layouts", [])}
    named_layouts = {x["type_id"]: x for x in naming.get("results", [])}
    if set(expected_layouts) != set(named_layouts):
        failures.append(f"entity coverage mismatch: layouts={len(expected_layouts)}, naming={len(named_layouts)}")
    for tid, layout in expected_layouts.items():
        named = named_layouts.get(tid)
        if not named:
            continue
        for archive, spec in layout.get("archives", {}).items():
            other = named.get("archives", {}).get(archive)
            if not other:
                failures.append(f"type {tid} missing archive {archive}")
                continue
            original_fields = spec.get("fields", [])
            named_fields = other.get("fields", [])
            if len(original_fields) != len(named_fields):
                failures.append(f"type {tid}/{archive} field count changed")
                continue
            for i, (original, slot) in enumerate(zip(original_fields, named_fields)):
                if (original.get("idx"), original.get("row_off"), original.get("width")) != (
                        slot.get("idx"), slot.get("row_off"), slot.get("width")):
                    failures.append(f"type {tid}/{archive}/field {i} row_off/width/idx changed")
                if slot.get("confidence") == "unresolved":
                    continue
                accesses = slot.get("accesses", [])
                if not accesses:
                    failures.append(f"type {tid}/{archive}/field {i} named without access evidence")
                    continue
                width = original["width"]
                sizes = {a.get("size") for a in accesses}
                if width == 8 and all(s == 4 for s in sizes) and len(accesses) >= 2:
                    # The only packed-size exception is a pair of 4-byte getters spanning the 8-byte slot.
                    starts = {a.get("object_off") for a in accesses}
                    base = slot.get("object_off")
                    if not isinstance(base, int) or not {base, base + 4}.issubset(starts):
                        failures.append(f"type {tid}/{archive}/field {i} invalid 4+4 packed mapping")
                elif sizes != {width}:
                    failures.append(f"type {tid}/{archive}/field {i} evidence sizes {sorted(sizes)} != width {width}")

    # Explicitly ensure the reference-backed city candidates retain 4-byte field widths.
    for code in ("Cnti", "Cwea", "Clgi", "Clri"):
        if not any(r.get("kind") == "ref_only" and r.get("size") == 4
                   for r in codes.get(code, [])):
            failures.append(f"city {code} must be labeled ref_only, size 4")

    print(f"injury {injury_ok}/13; city {city_ok}/6; entities {len(named_layouts)}/26")
    if failures:
        for f in failures:
            print("FAIL:", f)
        return 1
    print("PASS: calibration, evidence widths, and untouched row_off/width verified")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Verify t07 4CC mappings against fixed calibration and layouts.")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        return selftest()
    try:
        return check()
    except Exception as exc:
        print(f"FATAL: {exc}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
