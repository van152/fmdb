#!/usr/bin/env python3
"""Validate the t20 table_22 cursor, named-slot ledger, and fixed-stride closure."""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
EXPECTED_WIDTHS = [4, 4, 4, 4, 1, 4, 1, 4, 4, 4, 4, 4, 1, 4, 1, 1, 1, 4, 12]
LINEAR_CANDIDATES = {"Salt": 17, "Scam": 43, "Scpm": 21, "Slhm": 42}


def selftest() -> bool:
    cursor = 0
    offsets = {}
    for i, width in enumerate(EXPECTED_WIDTHS):
        offsets[i] = cursor
        cursor += width
    return cursor == 66 and 66 + 13 == 79 and {
        "Salt": offsets[5], "Scam": offsets[13], "Scpm": offsets[6], "Slhm": offsets[12]
    } == LINEAR_CANDIDATES


def verify() -> list[str]:
    errors: list[str] = []
    cursor_path = OUT / "cursor_t22.json"
    fields_path = OUT / "fields_t22.json"
    if not cursor_path.is_file() or not fields_path.is_file():
        return ["missing cursor_t22.json or fields_t22.json"]
    cursor = json.loads(cursor_path.read_text(encoding="utf-8"))
    fields = json.loads(fields_path.read_text(encoding="utf-8"))
    steps = cursor.get("steps", [])
    if cursor.get("status") != "partial_cursor_t22_branch_paths_unreconciled":
        errors.append("cursor status does not preserve the unresolved branch-path result")
    if cursor.get("table_type") != 22 or cursor.get("entity") != "club":
        errors.append("table identity metadata mismatch")
    if [x.get("width") for x in steps] != EXPECTED_WIDTHS:
        errors.append("19 cursor widths differ from the accepted type-22 window")
    at = 0
    for i, step in enumerate(steps):
        if step.get("slot") != i or step.get("row_offset_candidate") != at:
            errors.append(f"slot {i} has a non-cumulative linear candidate offset")
            break
        if step.get("row_offset") is not None:
            errors.append(f"slot {i} incorrectly promotes an unverified row offset")
            break
        at += int(step["width"])
    if at != 66:
        errors.append(f"business cursor ends at {at}, not 66")
    closure = cursor.get("stride_closure", {})
    if closure.get("stride") != 79 or closure.get("business_width_candidate") != 66 or closure.get("trailer_width") != 13:
        errors.append("stride fields do not state 66+13=79")
    if closure.get("byte_budget_pass") is not True or closure.get("field_cursor_closed") is not False:
        errors.append("partial byte-budget/field-cursor status is inconsistent")
    if closure.get("payload_equation") != "14 + 449*79 + 8 = 35493":
        errors.append("payload boundary equation changed")
    if cursor.get("serializer_locator", {}).get("slot19_walk_function_file_off") != "0x1537800":
        errors.append("slot-19 walk locator changed")
    if cursor.get("cursor_method", {}).get("branch_path_closed") is not False or cursor.get("serializer_locator", {}).get("slot19_events_with_member_sink") != 18:
        errors.append("expected a branch-unclosed 18-event walk plus one 12-byte bulk call")
    for code, offset in LINEAR_CANDIDATES.items():
        step = next((x for x in steps if x.get("field_code_candidate") == code), None)
        if step is None or step.get("row_offset_candidate") != offset or step.get("row_offset") is not None:
            errors.append(f"E56 code {code} candidate is missing or wrongly promoted")

    if fields.get("fields_named") != 0 or fields.get("candidate_names_unique_within_club_Cstc") != 15 or len(fields.get("fields", [])) != 19:
        errors.append("field ledger must preserve 19 candidates, with zero promoted row names and 15 unplaced name candidates")
    if fields.get("business_width") != 66 or fields.get("stride") != 79:
        errors.append("field ledger dimensions mismatch")
    if len(steps) != len(fields.get("fields", [])):
        errors.append("cursor and field ledger slot counts differ")
    if any(a.get("row_offset_candidate") != b.get("row_offset_candidate") or
           a.get("row_offset") != b.get("row_offset") or a.get("width") != b.get("width")
           for a, b in zip(steps, fields.get("fields", []))):
        errors.append("cursor and field-ledger candidate coordinates differ")
    for i in (1, 2):
        if fields["fields"][i].get("grade") != "L3_code_only":
            errors.append(f"duplicate code slot {i} was promoted beyond code-only")
    if fields["fields"][18].get("field") is not None or fields["fields"][18].get("row_offset") is not None or fields["fields"][18].get("width") != 12:
        errors.append("12-byte bulk sink must remain unnamed and unplaced")
    if len(closure.get("data_shape_conflicts", [])) < 3:
        errors.append("independent packed-date conflicts were not retained")

    csv_path = ROOT / "scratch" / "t13d" / "out" / "t22.csv"
    if not csv_path.is_file():
        errors.append("source t22.csv missing")
    else:
        with csv_path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        if len(rows) != 449:
            errors.append(f"source row count is {len(rows)}, not 449")
        for i, row in enumerate(rows):
            if int(row["offset"]) != 14 + i * 79 or int(row["len"]) != 79 or len(bytes.fromhex(row["raw_hex"])) != 79:
                errors.append(f"source CSV row {i} is not contiguous 79-byte data")
                break
    return errors


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--selftest", action="store_true", help="run deterministic cursor/anchor arithmetic checks")
    args = ap.parse_args()
    if args.selftest:
        ok = selftest()
        print("t20 verify selftest: " + ("PASS" if ok else "FAIL"))
        return 0 if ok else 1
    try:
        errors = verify()
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(f"fatal: {exc}", file=sys.stderr)
        return 2
    if errors:
        for error in errors:
            print("FAIL: " + error)
        return 1
    print("PASS (partial): 66B candidate budget + 13B trailer = stride 79; 449 rows; E56 identity 4/4; row coordinates remain unpromoted.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
