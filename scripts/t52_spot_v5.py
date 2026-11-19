#!/usr/bin/env python3
"""Independent source-backed spot checks for the t52 schema v5 merge."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
V4_JSON = ROOT / "scratch/t52/out/club_nation_subtable_schema.v4.json"
V4_MD = ROOT / "scratch/t52/out/club_nation_subtable_schema.v4.md"
V5_JSON = ROOT / "reports/club_nation_subtable_schema.json"
V4_JSON_SHA256 = "7567606c8082f53296caf9c07088489614c364d214e25ba3d4f6390e17d25932"
V4_MD_SHA256 = "ee47e88a4f7d82ecb996022dc7465975eff51bb153869f99adb987dc46ee3c0c"

T9_PARENTS = ("Nntp", "Nctp", "Nrtp", "NTRv", "NWGv", "NSps", "Nfmp", "NCro")
Ntxr_L3 = {"lowa": 1, "uppa": 5, "capa": 9, "year": 13, "perc": 17, "fram": 21, "leve": 22}


class SpotFailure(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SpotFailure(message)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_json(path: Path) -> Any:
    require(path.is_file(), f"missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def root_json(path: str) -> Any:
    return read_json(ROOT / path)


def root_jsonl(path: str) -> list[dict[str, Any]]:
    p = ROOT / path
    require(p.is_file(), f"missing JSONL: {path}")
    return [json.loads(line) for line in p.read_text(encoding="ascii").splitlines() if line]


def verify_spots() -> tuple[int, int, list[str]]:
    v4_raw = V4_JSON.read_bytes()
    v4_md_raw = V4_MD.read_bytes()
    require(sha256(v4_raw) == V4_JSON_SHA256, "v4 JSON SHA-256 baseline")
    require(sha256(v4_md_raw) == V4_MD_SHA256, "v4 Markdown SHA-256 baseline")
    base, schema = json.loads(v4_raw.decode("utf-8")), read_json(V5_JSON)
    samples: list[str] = []
    row_checks = 0

    for key in ("tables", "negative_regressions", "v3_baseline", "club_auxiliary_sources", "nation_data_side_status"):
        require(schema[key] == base[key], f"protected v4 block {key}")
        samples.append(f"protected:{key}")
    for key, value in base["coverage"].items():
        require(schema["coverage"].get(key) == value, f"v4 coverage key {key}")
        samples.append(f"coverage:{key}")

    t47 = root_json("scratch/t47/out/fields_nation_tax.json")
    stored_t47 = schema["nation_static_side"]["Ntxr"]
    require(stored_t47["source_field_ledger"] == t47, "Ntxr source ledger retained")
    for code, offset in Ntxr_L3.items():
        source = t47["fields"][code]
        stored = next(item for item in stored_t47["fields"] if item["code"] == code)
        require(source["status"] == "L3" and source["accepted_item_offset"] == offset,
                f"Ntxr/{code}: accepted source offset")
        require(stored["grade"] == "L3" and stored["item_relative_offset"] == offset,
                f"Ntxr/{code}: merged item-relative L3 offset")
        samples.append(f"Ntxr/{code}@+{offset}")
    for code in ("ppty", "txty"):
        source = t47["fields"][code]
        stored = next(item for item in stored_t47["fields"] if item["code"] == code)
        require(source["status"] == stored["grade"] == "held", f"Ntxr/{code}: held is preserved")
        samples.append(f"Ntxr/{code}:held")

    total_t49_fields = 0
    for parent in T9_PARENTS:
        source = root_json(f"scratch/t49/out/fields_{parent}.json")
        stored = schema["nation_t9_wire"]["table_9"]["parents"][parent]
        source_items = list(source["fields"].items())
        stored_items = stored["fields"]
        require(source_items and stored_items, f"t49/{parent}: nonempty field ledger")
        first_code, first_record = source_items[0]
        require(stored_items[0]["code"] == first_code and stored_items[0]["grade"] == first_record["grade"],
                f"t49/{parent}: first field and grade")
        samples.append(f"t49/{parent}/first={first_code}:{first_record['grade']}")
        for code, record in source_items:
            merged = next(item for item in stored_items if item["code"] == code)
            require(merged["source_record"] == record and merged["grade"] == record["grade"],
                    f"t49/{parent}/{code}: exact grade/source")
            if record["grade"] == "L3":
                require(merged["accepted_item_offset"] == record["accepted_item_offset"],
                        f"t49/{parent}/{code}: accepted offset")
            total_t49_fields += 1
            samples.append(f"t49/{parent}/{code}:{record['grade']}")
    require(total_t49_fields == 30, "t49 field ledger item count")

    for parent in ("Nrvn", "Nftb", "Calt"):
        source = root_json(f"scratch/t51/out/fields_{parent}.json")
        require(schema["nation_static_side"]["t51_followup"]["field_ledgers"][parent] == source,
                f"t51/{parent}: exact source ledger retained")
        for code, record in source["fields"].items():
            samples.append(f"t51/{parent}/{code}:{record['status']}")

    t50_profile = root_json("scratch/t50/out/profile_t9.json")
    t50_diff = root_json("scratch/t50/out/grammar_diff_t9.json")
    t50_report = (ROOT / "scratch/t50/out/REPORT.md").read_text(encoding="utf-8")
    t50_done = (ROOT / "scratch/t50/out/DONE.md").read_text(encoding="utf-8")
    t50_node = schema["nation_t9_wire"]["t50_L2_cross_validation"]
    require(t50_node["source_records_verbatim"]["REPORT.md"] == t50_report and
            t50_node["source_records_verbatim"]["DONE.md"] == t50_done, "t50 report/DONE text exact")
    require(t50_node["source_records_verbatim"]["profile_t9.json"] == t50_profile and
            t50_node["source_records_verbatim"]["grammar_diff_t9.json"] == t50_diff,
            "t50 profile and grammar diff retained")
    require(t50_profile["evidence_level"]["L3"] == t50_profile["evidence_level"]["L4"] == 0,
            "t50 stays below L3/L4")
    for side, total, stream, footer in (("client", 31956, 31935, 8), ("server", 307564, 307543, 8)):
        closure = t50_profile["members"][f"{side}/table_9.dat"]["closure"]
        require((closure["count"], closure["payload_bytes"], closure["sum_row_lens"], closure["footer_bytes"]) ==
                (251, total, stream, footer), f"t50 {side} table_9 closure values")
        require(13 + stream + footer == total, f"t50 {side} table_9 closure equation")
        samples.append(f"t50/{side}/table9={closure['equation']}")
    for side, total, spans, walks in (("client", 83927, 83915, 1), ("server", 105228, 105216, 4)):
        closure = t50_profile["members"][f"{side}/table_extra_9.dat"]["closure"]
        require((closure["count"], closure["payload_bytes"], closure["sum_block_spans"], closure["block_walks"]) ==
                (251, total, spans, walks), f"t50 {side} extra_9 closure values")
        require(12 + spans == total, f"t50 {side} extra_9 closure equation")
        samples.append(f"t50/{side}/extra9={closure['equation']};walks={walks}")
    require(t50_diff["table_9"]["identity_agrees_row_by_row"] is True and
            t50_diff["table_9"]["identical_row_count"] == 0, "t50 client/server identity/body comparison")
    require(t50_diff["cross_table"]["t9_ids_equal_t10_ids"]["client"] and
            t50_diff["cross_table"]["t9_ids_equal_t10_ids"]["server"], "t50 t9/t10 identity ladder")
    require(t50_node["adjudication"].startswith("NO WINNER"), "t49/t50 framing stays unresolved")
    ledger = root_json("scratch/t01/LEDGER.json")
    e91 = [entry for entry in ledger["entries"] if entry.get("id") == "E91"]
    task50 = schema["incremental_provenance"]["tasks"]["t50"]
    require(len(e91) == 1 and (e91[0].get("kind"), e91[0].get("level")) == ("acceptance", "L2") and
            t50_node["acceptance_ledger_entry"] == task50["acceptance_ledger_entry"] == "E91" and
            "E91 accepts L2 data-side profile only" in task50["ledger_status"] and
            t50_profile["evidence_level"]["L3"] == 0,
            "t50 E91 must remain an L2-only acceptance with no L3 field promotion")
    samples.append("t50/E91:L2; field attribution L3=0")
    shape = schema["nation_t9_wire"]["table_extra_9"]["t50_L2_shape_assessment"]
    require(shape["acceptance_ledger_entry"] == "E91" and shape["target_parent_assignment"] == [],
            "t50 sidecar remains unassigned under E91")
    for location, value in (("nation_static_side", schema["nation_static_side"]),
                            ("nation_t9_wire.table_9", schema["nation_t9_wire"]["table_9"]),
                            ("tables", schema["tables"])):
        stack = [value]
        while stack:
            item = stack.pop()
            if isinstance(item, dict):
                require(item.get("source_task") != "t50" and item.get("field_source_task") != "t50" and
                        item.get("grade_source_task") != "t50" and item.get("acceptance_ledger_entry") != "E91",
                        f"t50 field attribution found in {location}")
                stack.extend(item.values())
            elif isinstance(item, list):
                stack.extend(item)
    require(schema["nation_t9_wire"]["table_9"]["grade_totals"] == {"L3": 17, "held": 13},
            "t49 accepted and held totals")
    require(schema["nation_t9_wire"]["table_extra_9"]["target_parent_assignment"] == [],
            "table_extra_9 remains unassigned")

    for side in ("client", "server"):
        a = root_json(f"scratch/t49/out/cursor_t9_{side}.json")["rows"]
        b = root_json(f"scratch/t51/out/cursor_table_9_{side}.json")["rows"]
        for x, y in zip(a, b):
            require(all(x.get(k) == y.get(k) for k in ("row", "wire13", "legacy14", "end", "identity_at", "length", "identity", "wire_sha256")),
                    f"t49/t51 {side} source cross-walk row {x['row']}")
            row_checks += 1
    a = root_json("scratch/t47/out/cursor_nation_tax.json")["server"]["rows"]
    b = root_json("scratch/t51/out/cursor_table_10_server.json")["rows"]
    for x, y in zip(a, b):
        require(all(x.get(k) == y.get(k) for k in ("row", "wire13", "legacy14", "end", "identity_at", "length", "identity", "wire_sha256")),
                f"t47/t51 t10 source cross-walk row {x['row']}")
        row_checks += 1
    require(row_checks == 753, "all three cross-walks contain 251 rows")
    for side in ("client", "server"):
        old = root_json(f"scratch/t49/out/cursor_t9_{side}.json")["rows"]
        new = root_jsonl(f"scratch/t50/out/profiles/table_{side}_9.rows.jsonl")
        require([r["offset"] - q["wire13"] for q, r in zip(old, new)] == [0] + [1] * 250,
                f"t50 {side}: candidate row starts remain distinct from t49")
        require([r["len"] - q["length"] for q, r in zip(old, new)] == [1] + [0] * 250,
                f"t50 {side}: candidate row lengths remain distinct from t49")
        tail_matches = [r["offset"] + r["identity"]["tail_offset_in_row"] == q["identity_at"]
                        for q, r in zip(old, new)]
        require(len(tail_matches) == 251 and all(tail_matches),
                f"t50 {side}: absolute identity-tail starts differ from t49")
        samples.append(f"t50/{side}: identity-tail starts 251/251; marker/selector boundary unresolved")
    require(schema["coverage"]["nation_L3_occurrences"] == 30 and
            schema["coverage"]["nation_L3_unique_wire_fields"] == 30 and
            schema["coverage"]["nation_held_occurrences"] == 20 and
            schema["coverage"]["nation_negative_records"] == 7, "nation coverage counters")
    require(len(samples) >= 20, f"spot sample too small: {len(samples)}")
    return len(samples), row_checks, samples


def selftest() -> None:
    old = [{"wire13": 13, "length": 4}]
    candidate = [{"offset": 13, "len": 5}]
    require(candidate[0]["offset"] - old[0]["wire13"] == 0, "selftest start")
    require(candidate[0]["len"] - old[0]["length"] == 1, "selftest length")
    require(len(Ntxr_L3) == 7 and len(T9_PARENTS) == 8, "selftest expected scope size")
    require(sha256(b"") == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "selftest SHA")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Source-backed t52-fix1 spot checks for t50 E91 L2 scope, field grades, closures, and row cross-walks.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--selftest", action="store_true", help="run isolated helper tests")
    group.add_argument("--check", action="store_true", help="run source-backed spot checks")
    args = parser.parse_args(argv)
    try:
        if args.selftest:
            selftest()
            print("t52 spot selftest PASS")
            return 0
        sample_count, row_count, samples = verify_spots()
        print(f"t52 spot checks PASS: {sample_count} field/closure/protected samples; {row_count} cross-walk row comparisons")
        for item in samples:
            print(f"SPOT {item}")
        print("SPOT E91 accepts t50 at L2 only; L3 field attribution remains zero, sidecar unassigned, no framing winner")
        return 0
    except SpotFailure as exc:
        print(f"CHECK FAILED: {exc}", file=sys.stderr)
        return 1
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"FATAL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
