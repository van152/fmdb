#!/usr/bin/env python3
"""Verify t19 club/nation cursor artifacts using only frozen workspace inputs."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def checks():
    results = []
    def add(name, ok, detail):
        results.append({"check": name, "status": "pass" if ok else "fail", "detail": detail})

    club = load(OUT / "cursor_club.json")
    nation = load(OUT / "cursor_nation.json")
    club_src = load(ROOT / "scratch/t02/inbox/club_v2/output.json")
    nation_src = load(ROOT / "scratch/t01/inbox/t01g/output.json")
    widths = load(ROOT / "scratch/t05/reader_widths.json")

    boundary = club["boundary_evidence"]
    end = int(boundary["row_body_end_member_offset"], 16)
    member_len = boundary["member_length"]
    footer_off = int(boundary["footer_offset"], 16)
    add("club_footer_seal", boundary["footer_exact"] and end == footer_off and end + 8 == member_len,
        f"body_end={end:#x}, footer={footer_off:#x}, member={member_len}")
    add("club_row_count", boundary["count"] == 84259 and boundary["standard_layout_rows"] + boundary["compact_rows"] == 84259,
        f"standard={boundary['standard_layout_rows']} compact={boundary['compact_rows']} total={boundary['count']}")

    sample_rows = []
    partition = club_src["class_partition"]
    for key in ("CLUB_samples", "LEAGUE_BODY_CLUB_samples"):
        sample_rows.extend(partition.get(key, []))
    for variant in club_src["variants"]:
        for key in ("sample_rows_before_transition", "sample_rows_after_transition"):
            sample_rows.extend(variant.get(key, []))
    sample_rows = [x for x in sample_rows if x.get("full_name") is not None and x.get("short_name") is not None]
    formula_ok = bool(sample_rows)
    formula_detail = []
    for row in sample_rows:
        n = len(row["full_name"].encode("utf-8"))
        m = len(row["short_name"].encode("utf-8"))
        expected = 50 + n + m
        formula_ok &= row["row_length"] == expected
        formula_detail.append({"row": row["row"], "observed": row["row_length"], "expected": expected})
    add("club_sample_name_length_recompute", formula_ok, formula_detail[:8])
    compact = partition["compact_rows_inside_LEAGUE_BODY_CLUB_segment"]
    add("club_compact_identity_frame", len(compact) == 3 and all(x in (69706, 69707, 69708) for x in compact), compact)

    reader10 = next(x for x in widths["results"] if x["type_id"] == 10)
    prefix = nation_src["row_codec"]["cursor_layout"]
    expected_prefix_widths = [x["width"] for x in prefix]
    expected_prefix_objects = [int(x["object_offset"], 16) if x.get("object_offset") else None for x in prefix]
    widths_match = reader10["seq"][15:25] == expected_prefix_widths
    objects_match = reader10["obj_seq"][15:24] == expected_prefix_objects[:9]
    scratch_divergence = reader10["obj_seq"][24] == 68 and expected_prefix_objects[9] is None
    add("nation_prefix_widths", widths_match and sum(expected_prefix_widths) == 25,
        {"widths": expected_prefix_widths, "sum": sum(expected_prefix_widths)})
    add("nation_prefix_object_sinks", objects_match and scratch_divergence,
        {"first_nine_match": objects_match, "call24_object_offset": reader10["obj_seq"][24],
         "t01g_call24_sink": "stack scratch byte"})

    prefix_cursor = 0
    for step in prefix:
        if step["row_offset_in_body"] != prefix_cursor:
            raise ValueError(f"nation prefix cursor discontinuity at {step['step']}")
        prefix_cursor += step["width"]
    add("nation_prefix_cursor_accumulation", prefix_cursor == 25, f"cursor_end={prefix_cursor}")

    for code, mapping in nation_src["row_offset_map"].items():
        if code not in {"Ngct", "Ncti", "Nrgi", "Ncur", "Nsod", "Necf", "Nygn"}:
            continue
        dest = bytes.fromhex(mapping["serializer"]["destination"]["bytes"])
        transfer = bytes.fromhex(mapping["serializer"]["width_instruction"]["bytes"])
        displacement = int.from_bytes(dest[3:7], "little")
        width = int.from_bytes(transfer[-4:], "little")
        getter = bytes.fromhex(mapping["field_getter_link"]["compare"]["bytes"])
        getter_code = getter[-4:][::-1].decode("ascii")
        add(f"nation_instruction_recompute_{code}", displacement == int(mapping["object_offset"], 16)
            and width == mapping["width"] and getter_code == code,
            {"object_offset": hex(displacement), "width": width, "getter_code": getter_code,
             "row_offset": mapping["row_offset"]})

    env = nation["payload_envelope"]
    add("nation_payload_envelope", env["header_bytes"] + env["data_bytes"] + env["footer_bytes"] == env["payload_size"],
        env["equation"])

    ledgers = {}
    for entity in ("club", "nation"):
        manifest = load(OUT / f"fields_{entity}.json")
        fields = []
        for shard in manifest["shards"]:
            fields.extend(load(OUT / shard)["fields"])
        ledgers[entity] = (manifest, fields)
    club_manifest, club_fields = ledgers["club"]
    nation_manifest, nation_fields = ledgers["nation"]
    old_club_fields = [x for p in sorted((ROOT / "scratch/t18/out").glob("fields_club.part*.json"))
                       for x in load(p)["fields"] if x.get("grade") != "unnamed"]
    old_nation_fields = [x for p in sorted((ROOT / "scratch/t18/out").glob("fields_nati.part*.json"))
                         for x in load(p)["fields"] if x.get("grade") != "unnamed"]
    baseline_club = len(old_club_fields)
    baseline_nation = len(old_nation_fields)
    add("club_schema_ledger_and_baseline", len(club_fields) == 672 and club_manifest["top_level_fields"] == 433
        and baseline_club == 14 and club_manifest["named_fields"] == 15,
        {"total": len(club_fields), "top_level": club_manifest["top_level_fields"],
         "t18_named": baseline_club, "t19_named": club_manifest["named_fields"]})
    add("nation_schema_ledger_and_baseline", len(nation_fields) == 441 and nation_manifest["top_level_fields"] == 346
        and baseline_nation == 0 and nation_manifest["named_fields"] == 7,
        {"total": len(nation_fields), "top_level": nation_manifest["top_level_fields"],
         "t18_named": baseline_nation, "t19_named": nation_manifest["named_fields"]})
    club_by_code = {x["field"]: x for x in club_fields if x.get("parent") is None}
    club_offsets_match = all(club_by_code[x["field"]]["row_offset"] == x.get("offset")
        and club_by_code[x["field"]]["width"] == x.get("width")
        and club_by_code[x["field"]]["grade"] == x.get("grade") for x in old_club_fields)
    add("club_baseline_field_offset_compare", club_offsets_match,
        {"compared": len(old_club_fields), "fields": [x["field"] for x in old_club_fields]})
    nation_by_code = {x["field"]: x for x in nation_fields if x.get("parent") is None}
    nation_offsets_match = all(nation_by_code[code]["row_offset"] == mapping["row_offset"]
        and nation_by_code[code]["width"] == mapping["width"]
        for code, mapping in nation_src["row_offset_map"].items()
        if code in {"Ngct", "Ncti", "Nrgi", "Ncur", "Nsod", "Necf", "Nygn"})
    add("nation_prefix_field_offset_compare", nation_offsets_match,
        {"compared": 7, "fields": ["Ngct", "Ncti", "Nrgi", "Ncur", "Nsod", "Necf", "Nygn"]})

    cccn = next(x for x in club_fields if x["field"] == "Cccn" and x.get("parent") is None)
    ev = cccn["evidence"]
    dest = bytes.fromhex(ev["reader_destination"].split(": ", 1)[1])
    transfer = bytes.fromhex(ev["width_instruction"].split(": ", 1)[1])
    getter = bytes.fromhex(ev["getter_cmp"].split(": ", 1)[1])
    object_off = int.from_bytes(dest[3:7], "little")
    transfer_width = int.from_bytes(transfer[-4:], "little")
    getter_code = getter[2:6][::-1].decode("ascii")
    add("club_Cccn_instruction_recompute", cccn["row_offset"] == 8 and cccn["width"] == 4
        and cccn["grade"] == "L3_inherited" and object_off == 0xF0 and transfer_width == 4
        and getter_code == "Cccn"
        and ev["status"] == "inherited_low_confidence_candidate_not_revalidated",
        {"row_offset_candidate": cccn["row_offset"], "object_offset": hex(object_off),
         "transfer_width": transfer_width, "getter_code": getter_code, "status": ev["status"]})

    blockers = ["club reader transfer trace is not aligned to row-frame cursor",
                "nation counted-loop body widths and per-row closure remain unresolved"]
    return {"status": "partial" if all(x["status"] == "pass" for x in results) else "failed",
            "checks": results, "blockers": blockers,
            "complete_cursor": False}


def selftest():
    result = checks()
    failed = [x for x in result["checks"] if x["status"] != "pass"]
    if failed:
        raise AssertionError(f"artifact selftest failed: {failed}")
    assert 50 + len("Klubi i Futbollit Albpetrol Patos".encode()) + len("KF Albpetrol".encode()) == 95
    assert 14 + 24710 + 8 == 24732
    print("t19 verify selftest: PASS (cursor completion remains intentionally partial)")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selftest", action="store_true", help="run all reproducible checks; unresolved completion gates are reported separately")
    parser.add_argument("--json", action="store_true", help="print machine-readable check results")
    args = parser.parse_args()
    try:
        if args.selftest:
            selftest()
            return 0
        result = checks()
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            for item in result["checks"]:
                print(f"{item['status'].upper():4} {item['check']}: {item['detail']}")
            print("BLOCKED: " + "; ".join(result["blockers"]))
        failed = any(x["status"] != "pass" for x in result["checks"])
        return 1 if failed or not result["complete_cursor"] else 0
    except (OSError, KeyError, ValueError, StopIteration, AssertionError) as exc:
        print(f"fatal: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
