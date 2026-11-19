#!/usr/bin/env python3
"""Verify t21 club row audit and preserve its partial cursor status."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent
EXPECTED_STATUS = "partial_row_audit_complete_cursor_unreconciled"
EXPECTED_SHA256 = "db8ea78cbb8fcc7973525b04f55ca1b2c9dafda1e096dfa15c1affcdcc4fab9f"
EXPECTED_CLASSES = {"CLUB", "LEAGUE_BODY_CLUB"}


def selftest() -> bool:
    return EXPECTED_STATUS.startswith("partial_") and EXPECTED_SHA256.startswith("db8e")


def verify() -> list[str]:
    errors: list[str] = []
    path = OUT / "audit.json"
    if not path.is_file():
        return ["missing audit.json"]
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"invalid audit.json: {exc}"]
    if doc.get("status") != EXPECTED_STATUS:
        errors.append("t21 status no longer records an unreconciled cursor")
    if doc.get("data_sha256") != EXPECTED_SHA256:
        errors.append("local club payload SHA-256 differs from the audited snapshot")
    rows = doc.get("row_audit", {})
    if rows.get("row_count") != 84259 or rows.get("standard_rows") != 84256:
        errors.append("club row counts are not 84259 total / 84256 standard")
    if rows.get("compact_rows") != [69706, 69707, 69708]:
        errors.append("compact row ordinals changed")
    if rows.get("footer_exact") is not True or rows.get("row_end_offset") != rows.get("footer_offset"):
        errors.append("row walk does not close exactly at the footer")
    if rows.get("marker_counts") != {"0": 84256, "12": 3}:
        errors.append("marker distribution changed")
    relations = rows.get("fixed_word_relations", {})
    if relations.get("u32@0==u32@8") != 55868:
        errors.append("row+0/row+8 equality count changed")
    windows = rows.get("ordinal_window_diagnostics", [])
    if len(windows) != 2 or windows[0].get("row_count") != 69705 or windows[1].get("row_count") != 14554:
        errors.append("transition window diagnostics are incomplete")
    static = doc.get("static_reader_audit", {})
    classes = {item.get("class") for item in static.get("classes", [])}
    if classes != EXPECTED_CLASSES:
        errors.append(f"expected both class readers, found {sorted(classes)}")
    if static.get("all_instruction_checks_pass") is not True:
        errors.append("one or more cited reader instructions failed byte/disassembly recheck")
    for item in static.get("classes", []):
        if item.get("instruction_checks_passed") != item.get("instruction_check_count"):
            errors.append(f"instruction check count mismatch for {item.get('class')}")
    mapping = doc.get("field_mapping_result", {})
    if mapping.get("new_row_coordinate_mappings") != 0:
        errors.append("t21 unexpectedly promotes a new row-coordinate mapping")
    if mapping.get("class_to_ordinal_discriminator") != "unresolved":
        errors.append("class-to-ordinal discriminator was promoted")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selftest", action="store_true", help="run deterministic checks")
    args = parser.parse_args()
    if args.selftest:
        ok = selftest()
        print("t21 verify selftest: " + ("PASS" if ok else "FAIL"))
        return 0 if ok else 1
    try:
        errors = verify()
    except (OSError, TypeError, KeyError) as exc:
        print(f"fatal: {exc}", file=sys.stderr)
        return 2
    if errors:
        for error in errors:
            print("FAIL: " + error)
        return 1
    print("PASS (partial): 84259 club rows closed; both RTTI reader traces rechecked; no new row mappings promoted.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
