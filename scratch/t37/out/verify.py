#!/usr/bin/env python3
"""Independent verification for the t37 nation data-side inventory."""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import math
import struct
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
INVENTORY = HERE / "nation_subtable_inventory.json"
PROFILE = HERE / "profiles" / "table_server_34.profile.json"
T28_CODES = {"Nlns", "Nefr", "Nnfr", "Nagr"}
DOMAINS = {
    "agreement": 6,
    "club": 84259,
    "city": 56293,
    "competition": 7047,
    "continent": 7,
    "language": 126,
    "media_source": 208,
    "nation": 251,
    "person": 792149,
    "region": 28,
    "stage_name": 278,
    "stadium": 48413,
    "team": 84507,
}


class VerifyFailure(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerifyFailure(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_json(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = path.read_bytes()
    return json.loads(raw.decode("utf-8")), raw


def column_facts(rows: list[bytes], offset: int, width: int) -> dict[str, Any]:
    values = [int.from_bytes(row[offset:offset + width], "little") for row in rows]
    sentinel = (1 << (8 * width)) - 1
    counter = collections.Counter(values)
    distinct = set(values)
    n = len(values)
    result: dict[str, Any] = {
        "key": f"u{width * 8}@row+{offset}",
        "offset": offset,
        "width": width,
        "interpretation": f"u{width * 8}",
        "count": n,
        "distinct": len(distinct),
        "min_unsigned": min(values) if values else None,
        "max_unsigned": max(values) if values else None,
        "zero_count": sum(v == 0 for v in values),
        "zero_rate": round(sum(v == 0 for v in values) / max(1, n), 6),
        "sentinel_value": f"0x{sentinel:0{width * 2}X}",
        "sentinel_count": sum(v == sentinel for v in values),
        "sentinel_rate": round(sum(v == sentinel for v in values) / max(1, n), 6),
        "top_values": [{"value": value, "count": count} for value, count in counter.most_common(12)],
        "small_value_set": sorted(distinct) if len(distinct) <= 64 else None,
    }
    if width == 1:
        result["bit_masks"] = {
            "set_count_by_bit": [sum(bool(v & (1 << bit)) for v in values) for bit in range(8)],
            "set_rate_by_bit": [round(sum(bool(v & (1 << bit)) for v in values) / max(1, n), 6)
                                for bit in range(8)],
        }
    if width == 4:
        nonnull = [value for value in values if value != 0xFFFFFFFF]
        result["reference_domains"] = {
            entity: {
                "limit_exclusive": limit,
                "in_range_count": sum(value < limit for value in nonnull),
                "denominator_nonnull": len(nonnull),
                "ratio": round(sum(value < limit for value in nonnull) / max(1, len(nonnull)), 6),
            }
            for entity, limit in DOMAINS.items()
        }
        valid_days: list[int] = []
        valid_years: list[int] = []
        nonblank = 0
        for value in values:
            day, year = value & 0xFFFF, value >> 16
            if value in (0, 0xFFFFFFFF) or year in (0, 0xFFFF):
                continue
            nonblank += 1
            if 1900 <= year <= 2035 and day <= 366:
                valid_days.append(day)
                valid_years.append(year)
        result["packed_day_year"] = {
            "nonblank_count": nonblank,
            "valid_count": len(valid_days),
            "valid_ratio_nonblank": round(len(valid_days) / max(1, nonblank), 6),
            "year_min": min(valid_years) if valid_years else None,
            "year_max": max(valid_years) if valid_years else None,
            "year_distinct": len(set(valid_years)),
            "day_max": max(valid_days) if valid_days else None,
        }
        signed = [value if value < 0x80000000 else value - 0x100000000 for value in nonnull]
        live = [value for value in signed if value != 0]
        cash_like = [value for value in live if -1_000_000_000 <= value <= 1_000_000_000]
        result["signed_i32_cash_diagnostic"] = {
            "min": min(signed) if signed else None,
            "max": max(signed) if signed else None,
            "nonzero_nonnull_count": len(live),
            "within_abs_1e9_count": len(cash_like),
            "within_abs_1e9_rate_nonzero_nonnull": round(len(cash_like) / max(1, len(live)), 6),
            "first_nonzero_samples": live[:12],
        }
        floats = [struct.unpack("<f", row[offset:offset + 4])[0] for row in rows]
        finite = [value for value in floats if math.isfinite(value)]
        result["float32_diagnostic"] = {
            "finite_count": len(finite),
            "finite_ratio": round(len(finite) / max(1, len(floats)), 6),
            "min_finite": min(finite) if finite else None,
            "max_finite": max(finite) if finite else None,
            "first_finite_samples": finite[:12],
        }
    return result


def load_rows(profile: dict[str, Any]) -> list[bytes]:
    relative = Path(*Path(profile["full_rows_file"]).parts)
    require(not relative.is_absolute() and ".." not in relative.parts, "unsafe source row path")
    path = (ROOT / relative).resolve()
    require(path.is_relative_to(ROOT.resolve()), "source row path escapes repository")
    raw_bytes = path.read_bytes()
    require(sha(raw_bytes) == profile["full_rows_sha256"], "source rows JSONL hash mismatch")
    closure = profile["row_closure"]
    stride = int(closure["stride"])
    row_start = int(closure["row_start"])
    rows: list[bytes] = []
    rows_hash = hashlib.sha256()
    for expected, line in enumerate(raw_bytes.splitlines()):
        record = json.loads(line.decode("ascii"))
        require(record.get("row") == expected, f"row ordinal mismatch at {expected}")
        require(record.get("offset") == row_start + expected * stride, f"row offset mismatch at {expected}")
        row = bytes.fromhex(record["raw_hex"])
        require(record.get("len") == stride and len(row) == stride, f"row stride mismatch at {expected}")
        rows_hash.update(row)
        rows.append(row)
    require(len(rows) == closure["count"], "row dump count differs from profile")
    require(row_start + len(rows) * stride + closure["footer_bytes"] == closure["payload_bytes"],
            "row closure equation failed")
    require(rows_hash.hexdigest() == closure["rows_sha256"], "concatenated row hash mismatch")
    return rows


def verify_manifest_pin() -> str:
    manifest_path = ROOT / "evidence/MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    rel = "evidence/fm24/reports/editor_schema/master.json"
    pinned = next((entry["sha256"] for entry in manifest["files"] if entry["path"] == rel), None)
    actual = sha((ROOT / rel).read_bytes())
    require(pinned == actual and actual.startswith("7d57477e"), "frozen master.json manifest pin mismatch")
    return actual


def verify_inventory() -> tuple[int, int]:
    inventory, _ = read_json(INVENTORY)
    profile, profile_raw = read_json(PROFILE)
    require(inventory.get("status") == "partial_nation_parent_identity_coverage", "unexpected inventory status")
    require(inventory["provenance"]["schema_sha256"] == verify_manifest_pin(), "inventory schema pin mismatch")
    require(sha(profile_raw) == inventory["tables"][0]["profile_sha256"], "profile SHA mismatch")
    require(profile.get("table_type") == 34 and profile.get("archive") == "server", "wrong candidate profile identity")
    require(profile.get("status") == "complete_data_profile_reverified_L1", "profile status is not complete/reverified")

    master = json.loads((ROOT / "evidence/fm24/reports/editor_schema/master.json").read_text(encoding="utf-8"))
    schema_fields = master["entities"]["nation.xml"][0]["fields"]
    expected_parents = {field["field"]: field for field in schema_fields if field.get("type") == "list"}
    parents = inventory["parents"]
    require(len(expected_parents) == 29 and len(parents) == 29, "nation list-parent count mismatch")
    actual_by_code = {row["parent_4cc"]: row for row in parents}
    require(set(actual_by_code) == set(expected_parents), "inventory parent-code set differs from schema")
    for code, schema_parent in expected_parents.items():
        row = actual_by_code[code]
        require(row["schema_item_field_count"] == len(schema_parent.get("list_item_fields", [])),
                f"{code}: item-field count mismatch")

    t28 = json.loads((ROOT / "scratch/t28/out/cursor_nation_tail.json").read_text(encoding="utf-8"))
    t28_fields = json.loads((ROOT / "scratch/t28/out/fields_nation_client.json").read_text(encoding="utf-8"))
    for code in T28_CODES:
        row = actual_by_code[code]
        coll = next(value for value in t28["collections"].values() if value["parent"] == code)
        require(row["link_status"] == "complete_linked_by_t28", f"{code}: not marked linked_by_t28")
        require(row["count"] == coll["count"]["profile"]["total"], f"{code}: t28 item count mismatch")
        require(row["stride"] == coll["wire_stride"], f"{code}: t28 wire stride mismatch")
        fields = [field for field in t28_fields["fields"] if field.get("parent") == code]
        require(len(fields) == len(row["item_field_candidates"]), f"{code}: t28 child field count mismatch")
        require(all(field["grade"] == "L3" for field in fields), f"{code}: source t28 ledger field not L3")

    rows = load_rows(profile)
    closure = profile["row_closure"]
    require(closure["equation"] == f"{closure['row_start']} + {closure['count']} * {closure['stride']} + {closure['footer_bytes']} = {closure['payload_bytes']}",
            "profile equation text mismatch")
    require(closure["status"] == "complete_arithmetic_closure_L1", "source closure status mismatch")
    columns = {column["key"]: column for column in profile["columns"]}
    require(len(columns) == len(profile["columns"]), "duplicate profile column keys")
    recomputed = 0
    candidate_fields = 0
    for parent in parents:
        for field in parent["item_field_candidates"]:
            matches = field.get("column_candidates", [])
            if field.get("status") == "L2_candidate":
                candidate_fields += 1
            for match in matches:
                ref = match["statistics_ref"]
                key = ref["column_key"]
                require(key in columns, f"candidate references absent profile column {key}")
                require(ref["profile_file"] == "profiles/table_server_34.profile.json", "candidate profile reference mismatch")
                facts = column_facts(rows, int(match["offset"]), int(match["width"]))
                require(facts == columns[key], f"independent stats mismatch for {key}")
                require(match["offset"] == facts["offset"] and match["width"] == facts["width"],
                        "candidate coordinate differs from profile column")
                expected_indices = sorted({0, len(rows) // 2, len(rows) - 1})
                require(ref["sample_indices"] == expected_indices, "candidate sample indices mismatch")
                expected_samples = [
                    {"row": index, "unsigned": int.from_bytes(rows[index][match["offset"]:match["offset"] + match["width"]], "little")}
                    for index in expected_indices
                ]
                require(ref["sample_values"] == expected_samples, f"candidate sample value mismatch for {key}")
                recomputed += 1
    summary = inventory["summary"]
    require(summary["L2_candidate_item_field_count"] == candidate_fields, "candidate field summary mismatch")
    require(summary["candidate_column_match_count"] == recomputed, "candidate column summary mismatch")
    require(summary["linked_by_t28_parent_count"] == 4, "t28 linkage summary mismatch")
    require(summary["candidate_table_types"] == [34] and summary["candidate_table_count"] == 1,
            "candidate table summary mismatch")
    require(summary["new_L3_claims"] == 0 and summary["L4"] == 0, "t37 evidence-grade policy violated")
    reviews = inventory.get("t33_profile_reviews", [])
    require(len(reviews) == 7, "t33 batch-II profile review count mismatch")
    require(all(not row["nation_parent_code_intersection"] for row in reviews), "t33 exact nation-parent overlap was not resolved")
    table58 = next((row for row in reviews if row["table_type"] == 58), None)
    require(table58 is not None and table58["review_status"] == "partial_semantic_only_not_assigned",
            "table58 weekly-wage near-match must remain unassigned")

    # Source evidence hashes are checked independently of the build script.
    for rel, expected in inventory["provenance"]["source_hashes"].items():
        path = (ROOT / Path(*Path(rel).parts)).resolve()
        require(path.is_relative_to(ROOT.resolve()), f"source hash path escapes repository: {rel}")
        require(sha(path.read_bytes()) == expected, f"source evidence hash mismatch: {rel}")
    return len(rows), recomputed


def selftest() -> None:
    rows = [struct.pack("<I", (2020 << 16) | 1), struct.pack("<I", 0xFFFFFFFF), struct.pack("<I", (2021 << 16) | 366)]
    facts = column_facts(rows, 0, 4)
    assert facts["sentinel_count"] == 1 and facts["packed_day_year"]["valid_count"] == 2
    refs = column_facts([struct.pack("<I", 1), struct.pack("<I", 0xFFFFFFFF), struct.pack("<I", 250)], 0, 4)
    assert refs["reference_domains"]["nation"]["in_range_count"] == 2
    masks = column_facts([b"\x00", b"\x01", b"\x81"], 0, 1)
    assert masks["bit_masks"]["set_count_by_bit"] == [2, 0, 0, 0, 0, 0, 0, 1]
    print("SELFTEST PASS: verifier u32 domains, sentinels, dates, and bit masks")


def main() -> int:
    parser = argparse.ArgumentParser(description="Independently verify t37 nation inventory, row closure, and candidate column statistics.")
    parser.add_argument("--selftest", action="store_true", help="run offline synthetic checks only")
    args = parser.parse_args()
    try:
        if args.selftest:
            selftest()
            return 0
        row_count, candidate_count = verify_inventory()
        print(f"PASS: {row_count} table34 rows closed; {candidate_count} candidate columns independently rechecked; 29 parents, t28 links, and manifest pin verified")
        return 0
    except VerifyFailure as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    except (OSError, ValueError, KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
