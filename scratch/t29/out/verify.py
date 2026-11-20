#!/usr/bin/env python3
"""Independent verifier for t29 row dumps and candidate-column evidence."""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import math
import pathlib
import struct
import sys
from typing import Any

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
INVENTORY = HERE / "subtable_inventory.json"

class VerifyFailure(Exception):
    pass


def require(ok: bool, message: str) -> None:
    if not ok:
        raise VerifyFailure(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verify_manifest_pin() -> str:
    rel = "evidence/fm24/reports/editor_schema/master.json"
    manifest = json.loads((ROOT / "evidence/MANIFEST.json").read_text(encoding="utf-8"))
    pinned = next((item["sha256"] for item in manifest["files"] if item["path"] == rel), None)
    actual = sha((ROOT / rel).read_bytes())
    require(pinned is not None and actual == pinned, "master.json does not match MANIFEST.json")
    return actual


def load_rows(table: dict[str, Any]) -> list[bytes]:
    rel = pathlib.PurePosixPath(table["full_rows_file"])
    require(not rel.is_absolute() and ".." not in rel.parts, "unsafe row dump path")
    path = (HERE / pathlib.Path(*rel.parts)).resolve()
    require(path.is_relative_to(HERE.resolve()), "row dump escapes output directory")
    file_bytes = path.read_bytes()
    require(sha(file_bytes) == table["full_rows_sha256"], f"table {table['table_type']}: JSONL dump hash mismatch")
    rows: list[bytes] = []
    rows_hash = hashlib.sha256()
    stride = table["row_closure"]["stride"]
    row_start = table["row_closure"]["row_start"]
    with path.open("r", encoding="ascii", newline="") as stream:
        for expected_index, line in enumerate(stream):
            record = json.loads(line)
            require(record["row"] == expected_index, f"table {table['table_type']}: row ordinal gap at {expected_index}")
            require(record["len"] == stride, f"table {table['table_type']}: wrong stride at row {expected_index}")
            require(record["offset"] == row_start + expected_index * stride,
                    f"table {table['table_type']}: wrong row offset at row {expected_index}")
            row = bytes.fromhex(record["raw_hex"])
            require(len(row) == stride, f"table {table['table_type']}: wrong raw row length at {expected_index}")
            rows_hash.update(row)
            rows.append(row)
    closure = table["row_closure"]
    count = closure["count"]
    payload_size = closure["payload_bytes"]
    require(len(rows) == count, f"table {table['table_type']}: dumped count {len(rows)} != {count}")
    require(row_start + count * stride + closure["footer_bytes"] == payload_size,
            f"table {table['table_type']}: arithmetic closure failed")
    require(closure["rows_sha256"] == rows_hash.hexdigest(),
            f"table {table['table_type']}: concatenated row hash mismatch")
    return rows


def column_facts(rows: list[bytes], off: int, width: int) -> dict[str, Any]:
    vals = [int.from_bytes(row[off:off + width], "little") for row in rows]
    sentinel = (1 << (8 * width)) - 1
    counter = collections.Counter(vals)
    distinct = set(vals)
    facts: dict[str, Any] = {
        "count": len(vals),
        "distinct": len(distinct),
        "min_unsigned": min(vals) if vals else None,
        "max_unsigned": max(vals) if vals else None,
        "zero_count": sum(v == 0 for v in vals),
        "zero_rate": round(sum(v == 0 for v in vals) / max(1, len(vals)), 6),
        "sentinel_count": sum(v == sentinel for v in vals),
        "sentinel_rate": round(sum(v == sentinel for v in vals) / max(1, len(vals)), 6),
        "sentinel_value": f"0x{sentinel:0{width * 2}X}",
        "top_values": [{"value": v, "count": n} for v, n in counter.most_common(12)],
        "small_value_set": sorted(distinct) if len(distinct) <= 64 else None,
    }
    if width == 4:
        domains = {"club": 84259, "competition": 7047, "person": 792149,
                   "nation": 251, "stadium": 48413, "stage_name": 278,
                   "team": 84507, "media_source": 208, "city": 56293, "region": 28}
        nonnull = [v for v in vals if v != 0xFFFFFFFF]
        facts["reference_domains"] = {
            entity: {"in_range_count": sum(v < limit for v in nonnull),
                     "denominator_nonnull": len(nonnull),
                     "ratio": round(sum(v < limit for v in nonnull) / max(1, len(nonnull)), 6)}
            for entity, limit in domains.items()
        }
        valid_days = []
        years = []
        date_live = 0
        for v in vals:
            day, year = v & 0xFFFF, v >> 16
            if v in (0, 0xFFFFFFFF) or year in (0, 0xFFFF):
                continue
            date_live += 1
            if 1900 <= year <= 2035 and day <= 366:
                valid_days.append(day)
                years.append(year)
        facts["packed_day_year"] = {
            "nonblank_count": date_live,
            "valid_count": len(valid_days),
            "valid_ratio_nonblank": round(len(valid_days) / max(1, date_live), 6),
            "year_min": min(years) if years else None,
            "year_max": max(years) if years else None,
            "year_distinct": len(set(years)),
            "day_max": max(valid_days) if valid_days else None,
        }
        signed = [v if v < 0x80000000 else v - 0x100000000 for v in nonnull]
        live_signed = [v for v in signed if v != 0]
        good_cash = sum(-1_000_000_000 <= v <= 1_000_000_000 for v in signed)
        facts["signed_i32"] = {
            "min": min(signed) if signed else None,
            "max": max(signed) if signed else None,
            "within_abs_1e9_count": good_cash,
            "within_abs_1e9_rate_nonzero_nonnull": round(good_cash / max(1, len(live_signed)), 6),
        }
        floats = [struct.unpack("<f", row[off:off + 4])[0] for row in rows]
        finite = [v for v in floats if math.isfinite(v)]
        facts["float32"] = {
            "finite_count": len(finite),
            "finite_ratio": round(len(finite) / max(1, len(floats)), 6),
            "min_finite": min(finite) if finite else None,
            "max_finite": max(finite) if finite else None,
            "first_finite_samples": finite[:12],
        }
    return facts


def verify_candidates(doc: dict[str, Any], rows_by_type: dict[int, list[bytes]]) -> int:
    verified = 0
    for parent in doc["parents"]:
        for field in parent["item_field_candidates"]:
            for match in field["matches"]:
                tid = match["table_type"]
                require(tid in rows_by_type, f"candidate references absent table {tid}")
                rows = rows_by_type[tid]
                off, width = match["offset"], match["width"]
                require(0 <= off <= len(rows[0]) - width, f"candidate offset exceeds table {tid} row")
                facts = column_facts(rows, off, width)
                evidence = match["evidence"]
                require(evidence.get("offset") == off and evidence.get("width") == width,
                        f"candidate evidence offset/width mismatch for {parent['parent_4cc']}.{field['field']}")
                for key, value in facts.items():
                    require(evidence.get(key) == value,
                            f"candidate stats mismatch table {tid} +{off} {key}")
                expected_indices = sorted({0, len(rows) // 2, len(rows) - 1})
                require(match["sample_indices"] == expected_indices,
                        f"candidate sample index mismatch table {tid} +{off}")
                expected_samples = [
                    {"row": index, "unsigned": int.from_bytes(rows[index][off:off + width], "little")}
                    for index in expected_indices
                ]
                require(evidence.get("sample_values") == expected_samples,
                        f"candidate sample values mismatch table {tid} +{off}")
                verified += 1
    return verified


def run_selftest() -> None:
    rows = [struct.pack("<I", (2020 << 16) | 1), struct.pack("<I", (2021 << 16) | 365)]
    facts = column_facts(rows, 0, 4)
    assert facts["distinct"] == 2
    assert facts["packed_day_year"]["valid_count"] == 2
    ref_facts = column_facts([struct.pack("<I", 1), struct.pack("<I", 80000)], 0, 4)
    assert ref_facts["reference_domains"]["club"]["ratio"] == 1.0
    print("SELFTEST PASS: independent u32, domain, sentinel, and packed-date statistics")


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify t29 full-row dumps and candidate column statistics.")
    parser.add_argument("--selftest", action="store_true", help="run offline synthetic checks only")
    parser.add_argument("--inventory", type=pathlib.Path, default=INVENTORY, help="inventory JSON path")
    args = parser.parse_args()
    try:
        if args.selftest:
            run_selftest()
            return 0
        if args.inventory.resolve() != INVENTORY.resolve():
            raise VerifyFailure("inventory must be scratch/t29/out/subtable_inventory.json")
        doc = json.loads(INVENTORY.read_text(encoding="utf-8"))
        require(doc.get("status") == "partial_parent_identity_coverage", "unexpected inventory status")
        require(doc["provenance"]["master_sha256"] == verify_manifest_pin(), "inventory master hash mismatch")
        rows_by_type = {}
        for table in doc["tables"]:
            rows_by_type[int(table["table_type"])] = load_rows(table)
        matches = verify_candidates(doc, rows_by_type)
        print(f"PASS: verified {len(rows_by_type)} table row dumps, {matches} candidate column records, and manifest pin")
        return 0
    except VerifyFailure as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    except (OSError, ValueError, KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
