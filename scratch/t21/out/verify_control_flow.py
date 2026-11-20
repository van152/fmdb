#!/usr/bin/env python3
"""Verify t21b's PE-bounded control-flow audit and count scopes."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent
EXPECTED_STATUS = "partial_control_flow_audit_complete_row_cursor_unreconciled"
EXPECTED_EDITOR_SHA = "b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4"


def selftest() -> bool:
    return EXPECTED_STATUS.startswith("partial_control_flow_") and len(EXPECTED_EDITOR_SHA) == 64


def verify() -> list[str]:
    errors: list[str] = []
    path = OUT / "control_flow.json"
    if not path.is_file():
        return ["missing control_flow.json"]
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"invalid control_flow.json: {exc}"]
    if doc.get("status") != EXPECTED_STATUS:
        errors.append("control-flow status no longer preserves the unreconciled cursor")
    if doc.get("editor_sha256") != EXPECTED_EDITOR_SHA:
        errors.append("editor.exe SHA-256 differs from the frozen audit")
    comparison = doc.get("linear_scan_comparison", {})
    expected_counts = {
        "t05_window_stream_call_count": 41,
        "t01h_reported_stream_call_count": 21,
        "t01h_stream_call_site_records": 8,
        "t01h_stream_call_sites_matching_cfg_transfer_sites": 8,
        "t01h_stream_call_sites_not_matching_cfg": 0,
        "club_cfg_reachable_stream_transfer_count": 41,
    }
    for key, expected in expected_counts.items():
        if comparison.get(key) != expected:
            errors.append(f"{key}={comparison.get(key)!r}, expected {expected!r}")
    if comparison.get("t05_window_byte_span") != "0x2000":
        errors.append("t05 scan window is not 0x2000 bytes")
    if comparison.get("t05_scan_end_exclusive") != "0xe5c7a0":
        errors.append("t05 scan end does not match the recorded 0x2000-byte window")
    classes = {item.get("class"): item for item in doc.get("classes", [])}
    if set(classes) != {"CLUB", "LEAGUE_BODY_CLUB"}:
        errors.append(f"unexpected reader classes: {sorted(classes)}")
    bounds = {
        "CLUB": ("0xe5a7a0", "0xe5bfca", 41, 167, 35),
        "LEAGUE_BODY_CLUB": ("0x43beba0", "0x43bec73", 2, 3, 1),
    }
    for name, (begin, end, transfers, branches, backedges) in bounds.items():
        cfg = classes[name].get("cfg", {})
        extent = cfg.get("function_extent", {})
        if extent.get("begin_file_offset") != begin or extent.get("end_file_offset_exclusive") != end:
            errors.append(f"{name} PE runtime-function extent changed")
        for key, expected in (("reachable_stream_transfer_count", transfers),
                              ("conditional_branch_count", branches),
                              ("backedge_count", backedges)):
            if cfg.get(key) != expected:
                errors.append(f"{name} {key}={cfg.get(key)!r}, expected {expected!r}")
        if len(cfg.get("stream_transfers", [])) != transfers:
            errors.append(f"{name} transfer record count does not match summary")
    if doc.get("row_class_discriminator", {}).get("status") != "negative_not_established":
        errors.append("row class discriminator was promoted")
    if doc.get("row_class_discriminator", {}).get("row_coordinate_mapping_count") != 0:
        errors.append("t21b unexpectedly reports row-coordinate mappings")
    if doc.get("Cccn", {}).get("status") != "unpromoted":
        errors.append("Cccn was promoted")
    for item in classes.values():
        for transfer in item.get("cfg", {}).get("stream_transfers", []):
            if transfer.get("width_source") == "same_basic_block_mov_r8d" and transfer.get("width_before_call") is None:
                errors.append(f"local width source has null width at {transfer.get('file_offset')}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selftest", action="store_true", help="run deterministic checks")
    args = parser.parse_args()
    if args.selftest:
        ok = selftest()
        print("t21b verify selftest: " + ("PASS" if ok else "FAIL"))
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
    print("PASS (partial): PE-bounded CFG counts and count scopes verified; row cursor remains unreconciled.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
