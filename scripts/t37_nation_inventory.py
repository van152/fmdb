#!/usr/bin/env python3
"""Build a conservative data-side inventory of nation list parents.

Only existing repository evidence is read. New artifacts are confined to
scratch/t37/out. Candidate columns remain L2 diagnostics; this script does not
perform static cursor work or promote fields to L3.
"""
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

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "scratch" / "t37" / "out"
PROFILES = OUT / "profiles"
MASTER_REL = "evidence/fm24/reports/editor_schema/master.json"
T28_CODES = ("Nlns", "Nefr", "Nnfr", "Nagr")
T33_PROFILE_IDS = (12, 39, 45, 48, 58, 59, 73)
RTTI_PROBES = {
    "Nntp": "NATION_TRANSFER_PREFERENCE",
    "Ntxr": "TAX_RULE",
    "Nfmp": "FAMOUS_PLAYER",
}
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


class CheckFailure(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckFailure(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_json(rel: str) -> tuple[dict[str, Any], bytes]:
    raw = (ROOT / rel).read_bytes()
    return json.loads(raw.decode("utf-8")), raw


def schema_item(field: dict[str, Any], top_index: int, item_index: int) -> dict[str, Any]:
    return {
        "schema_index": top_index,
        "item_index": item_index,
        "field": field.get("field"),
        "name": field.get("name"),
        "type": field.get("type", "unknown"),
        "database_table_type": field.get("database_table_type"),
        "enum_ref": field.get("enum_ref"),
        "optional": field.get("optional"),
        "min_value": field.get("min_value"),
        "max_value": field.get("max_value"),
    }


def parse_rows(profile: dict[str, Any], rows_path: Path, rows_bytes: bytes) -> list[bytes]:
    closure = profile["row_closure"]
    stride = int(closure["stride"])
    row_start = int(closure["row_start"])
    rows: list[bytes] = []
    digest = hashlib.sha256()
    for i, line in enumerate(rows_bytes.splitlines()):
        record = json.loads(line.decode("ascii"))
        require(record.get("row") == i, f"row ordinal mismatch at {i}")
        require(record.get("offset") == row_start + i * stride, f"row offset mismatch at {i}")
        raw = bytes.fromhex(record["raw_hex"])
        require(record.get("len") == stride and len(raw) == stride, f"row stride mismatch at {i}")
        digest.update(raw)
        rows.append(raw)
    require(len(rows) == closure["count"], "row count differs from source profile")
    require(row_start + len(rows) * stride + closure["footer_bytes"] == closure["payload_bytes"],
            "source profile row-closure equation failed")
    require(digest.hexdigest() == closure["rows_sha256"], "source profile row hash mismatch")
    require(sha(rows_bytes) == profile["full_rows_sha256"], "source JSONL hash mismatch")
    return rows


def column_facts(rows: list[bytes], offset: int, width: int) -> dict[str, Any]:
    values = [int.from_bytes(row[offset:offset + width], "little") for row in rows]
    sentinel = (1 << (8 * width)) - 1
    counts = collections.Counter(values)
    distinct = set(values)
    n = len(values)
    facts: dict[str, Any] = {
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
        "top_values": [{"value": v, "count": c} for v, c in counts.most_common(12)],
        "small_value_set": sorted(distinct) if len(distinct) <= 64 else None,
    }
    if width == 1:
        facts["bit_masks"] = {
            "set_count_by_bit": [sum(bool(v & (1 << bit)) for v in values) for bit in range(8)],
            "set_rate_by_bit": [round(sum(bool(v & (1 << bit)) for v in values) / max(1, n), 6)
                                for bit in range(8)],
        }
    if width == 4:
        nonnull = [v for v in values if v != 0xFFFFFFFF]
        facts["reference_domains"] = {
            entity: {
                "limit_exclusive": limit,
                "in_range_count": sum(v < limit for v in nonnull),
                "denominator_nonnull": len(nonnull),
                "ratio": round(sum(v < limit for v in nonnull) / max(1, len(nonnull)), 6),
            }
            for entity, limit in DOMAINS.items()
        }
        live_days: list[int] = []
        years: list[int] = []
        nonblank = 0
        for value in values:
            day = value & 0xFFFF
            year = value >> 16
            if value in (0, 0xFFFFFFFF) or year in (0, 0xFFFF):
                continue
            nonblank += 1
            if 1900 <= year <= 2035 and day <= 366:
                live_days.append(day)
                years.append(year)
        facts["packed_day_year"] = {
            "nonblank_count": nonblank,
            "valid_count": len(live_days),
            "valid_ratio_nonblank": round(len(live_days) / max(1, nonblank), 6),
            "year_min": min(years) if years else None,
            "year_max": max(years) if years else None,
            "year_distinct": len(set(years)),
            "day_max": max(live_days) if live_days else None,
        }
        signed = [v if v < 0x80000000 else v - 0x100000000 for v in nonnull]
        live_signed = [v for v in signed if v != 0]
        in_cash_range = [v for v in live_signed if -1_000_000_000 <= v <= 1_000_000_000]
        facts["signed_i32_cash_diagnostic"] = {
            "min": min(signed) if signed else None,
            "max": max(signed) if signed else None,
            "nonzero_nonnull_count": len(live_signed),
            "within_abs_1e9_count": len(in_cash_range),
            "within_abs_1e9_rate_nonzero_nonnull": round(len(in_cash_range) / max(1, len(live_signed)), 6),
            "first_nonzero_samples": live_signed[:12],
        }
        floats = [struct.unpack("<f", row[offset:offset + 4])[0] for row in rows]
        finite = [value for value in floats if math.isfinite(value)]
        facts["float32_diagnostic"] = {
            "finite_count": len(finite),
            "finite_ratio": round(len(finite) / max(1, len(floats)), 6),
            "min_finite": min(finite) if finite else None,
            "max_finite": max(finite) if finite else None,
            "first_finite_samples": finite[:12],
        }
    return facts


def compatibility(field: dict[str, Any], column: dict[str, Any]) -> tuple[bool, float, str]:
    kind = field.get("type", "unknown")
    width = column["width"]
    small = column.get("small_value_set")
    if kind == "database_record_unique_id" and width == 4:
        entity = field.get("database_table_type")
        domain = column.get("reference_domains", {}).get(entity, {})
        if entity and domain.get("ratio", 0) >= 0.80:
            score = float(domain["ratio"])
            return True, score, f"{entity}-domain ratio {score:.3f}; full denominator and column stats in profile"
    elif kind == "boolean" and width == 1 and small is not None and len(small) == 2 and set(small) <= {0, 1}:
        return True, 1.0, "observed byte value set is exactly {0,1}"
    elif kind == "day_of_week" and width == 1 and small is not None and 2 <= len(small) <= 8 and set(small) <= set(range(8)):
        return True, 1.0, "observed byte domain is a subset of 0..7"
    elif kind in ("enum", "multiple_enum") and width == 1 and small is not None and 2 <= len(small) <= 32:
        return True, round(1.0 / len(small), 6), f"low-cardinality byte domain ({len(small)} values); weak compatibility only"
    elif kind == "date" and width == 4:
        date = column.get("packed_day_year", {})
        if date.get("nonblank_count", 0) and date.get("valid_ratio_nonblank", 0) >= 0.90:
            score = float(date["valid_ratio_nonblank"])
            return True, score, f"packed day/year diagnostic valid ratio {score:.3f}"
    elif kind == "cash" and width == 4:
        signed = column.get("signed_i32_cash_diagnostic", {})
        if signed.get("within_abs_1e9_rate_nonzero_nonnull", 0) >= 0.90:
            score = float(signed["within_abs_1e9_rate_nonzero_nonnull"])
            return True, score, f"signed i32 cash-range diagnostic {score:.3f}"
    elif kind == "real" and width == 4:
        finite = column.get("float32_diagnostic", {})
        if finite.get("finite_ratio", 0) >= 0.99:
            score = float(finite["finite_ratio"])
            return True, score, "finite float32 reinterpretation; weak diagnostic"
    elif kind == "integer" and width in (1, 2, 4):
        lo, hi = field.get("min_value"), field.get("max_value")
        if lo is not None and hi is not None:
            try:
                low, high = int(lo), int(hi)
            except (TypeError, ValueError):
                return False, 0.0, "schema bounds are not parseable integers"
            if column.get("min_unsigned", low - 1) >= max(0, low) and column.get("max_unsigned", high + 1) <= high:
                return True, 1.0, f"unsigned profile range within schema [{low},{high}]"
    return False, 0.0, "no compatible column diagnostic"


def item_candidates(items: list[dict[str, Any]], columns: list[dict[str, Any]], row_count: int) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    by_key = {column["key"]: column for column in columns}
    samples = sorted({0, row_count // 2, row_count - 1}) if row_count else []
    for item in items:
        matches = []
        for column in columns:
            ok, score, basis = compatibility(item, column)
            if not ok:
                continue
            matches.append({
                "offset": column["offset"],
                "width": column["width"],
                "score": round(score, 6),
                "basis": basis,
                "statistics_ref": {
                    "profile_file": "profiles/table_server_34.profile.json",
                    "column_key": column["key"],
                    "sample_indices": samples,
                    "sample_values": [],
                },
            })
        matches.sort(key=lambda x: (-x["score"], x["width"], x["offset"]))
        candidates.append({
            **item,
            "status": "L2_candidate" if matches else "partial_no_compatible_column_observed",
            "evidence_level": "L2_candidate" if matches else "unresolved",
            "confidence": "low_candidate" if matches else "unknown",
            "column_candidate_count": len(matches),
            "column_candidates": matches,
            "hint_policy": "whole-table type/statistics compatibility only; not a field-to-offset assignment",
            "blocker": "Parent-to-table34 collection/read-sink join is not established; overlapping compatible columns remain ambiguous.",
        })
    return candidates


def add_candidate_samples(candidates: list[dict[str, Any]], rows: list[bytes]) -> None:
    for field in candidates:
        for match in field["column_candidates"]:
            ref = match["statistics_ref"]
            offset, width = match["offset"], match["width"]
            ref["sample_values"] = [
                {"row": index, "unsigned": int.from_bytes(rows[index][offset:offset + width], "little")}
                for index in ref["sample_indices"]
            ]


def normalized_items(items: list[dict[str, Any]]) -> list[tuple[Any, ...]]:
    return [
        (item.get("field"), item.get("name"), item.get("type"), item.get("database_table_type"))
        for item in items
    ]


def build() -> dict[str, Any]:
    manifest, manifest_raw = read_json("evidence/MANIFEST.json")
    master, master_raw = read_json(MASTER_REL)
    master_sha = sha(master_raw)
    pins = {entry["path"]: entry["sha256"] for entry in manifest.get("files", [])}
    require(pins.get(MASTER_REL) == master_sha and master_sha.startswith("7d57477e"),
            "frozen nation schema is not pinned by evidence/MANIFEST.json")
    entity_fields = master["entities"]["nation.xml"][0]["fields"]
    club_fields = master["entities"]["club.xml"][0]["fields"]
    nation_lists = [(i, field) for i, field in enumerate(entity_fields) if field.get("type") == "list"]
    require(len(entity_fields) == 346, f"unexpected nation schema field count {len(entity_fields)}")
    require(len(nation_lists) == 29, f"expected 29 nation list parents, found {len(nation_lists)}")

    census, census_raw = read_json("scratch/t14/out/census.json")
    stage2_map, stage2_map_raw = read_json("scratch/t14/out/stage2_map.json")
    stage2_identity, stage2_identity_raw = read_json("reports/stage2_table_identity.json")
    census_by_type = {row["table_type"]: row for row in census["tables"]}
    stage2_map_by_type = {row["table_type"]: row for row in stage2_map["tables"]}
    stage2_identity_by_type = {row["table_type"]: row for row in stage2_identity["rows"]}

    t28, t28_raw = read_json("scratch/t28/out/cursor_nation_tail.json")
    t28_fields, t28_fields_raw = read_json("scratch/t28/out/fields_nation_client.json")
    t28_collections = t28["collections"]
    t28_by_parent = {entry["parent"]: (label, entry) for label, entry in t28_collections.items()}
    t28_field_rows = {
        code: [field for field in t28_fields["fields"] if field.get("parent") == code]
        for code in T28_CODES
    }
    for code in T28_CODES:
        require(code in t28_by_parent, f"t28 collection missing {code}")
        require(all(field.get("grade") == "L3" for field in t28_field_rows[code]),
                f"t28 existing field ledger is not fully L3 for {code}")

    t29, t29_raw = read_json("scratch/t29/out/subtable_inventory.json")
    t29_profile_rel = "scratch/t29/out/profiles/table_server_34.profile.json"
    t29_rows_rel = "scratch/t29/out/profiles/table_server_34.rows.jsonl"
    source_profile, source_profile_raw = read_json(t29_profile_rel)
    source_rows_raw = (ROOT / t29_rows_rel).read_bytes()
    source_rows_path = ROOT / t29_rows_rel
    require(source_profile.get("status") == "complete_data_profile", "t29 table34 profile is not complete")
    require(source_profile.get("table_type") == 34 and source_profile.get("archive") == "server",
            "t29 profile identity is not server table34")
    rows = parse_rows(source_profile, source_rows_path, source_rows_raw)
    closure = source_profile["row_closure"]
    t14_34 = census_by_type.get(34)
    require(t14_34 is not None and t14_34.get("primary_class") == "STARTING_TEAM_CUP_HISTORY",
            "table34 RTTI class does not match the expected t14 row")
    t29_tchl = next((row for row in t29["parents"] if row.get("parent_4cc") == "Tchl"), None)
    require(t29_tchl is not None and t29_tchl.get("table_type") == 34,
            "t29 has no club Tchl/table34 candidate record")

    # Consume t33 batch-II profiles as explicit negative/near-semantic checks.
    t33_rel = "scratch/t33/out/subtable_candidates.json"
    t33_candidates, t33_candidates_raw = read_json(t33_rel)
    t33_by_type = {row["table_type"]: row for row in t33_candidates["tables"]}
    nation_codes = {field.get("field") for _, field in nation_lists}
    t33_reviews = []
    t33_source_hashes = {t33_rel: sha(t33_candidates_raw)}
    for table_id in T33_PROFILE_IDS:
        profile_rel = f"scratch/t33/out/profiles/table_server_{table_id}.profile.json"
        t33_profile, t33_profile_raw = read_json(profile_rel)
        require(t33_profile.get("status") == "complete_data_profile" and t33_profile.get("table_type") == table_id,
                f"t33 profile identity/status mismatch for table {table_id}")
        t33_entry = t33_by_type.get(table_id)
        require(t33_entry is not None, f"t33 candidate inventory lacks table {table_id}")
        declared_parents = [parent.get("parent_4cc") for parent in t33_entry.get("parents", []) if parent.get("parent_4cc")]
        overlap = sorted(nation_codes.intersection(declared_parents))
        row_closure = t33_profile.get("row_closure", {})
        t33_reviews.append({
            "table_type": table_id,
            "archive": t33_profile.get("archive"),
            "rtti_class": t33_profile.get("rtti_class"),
            "count": row_closure.get("count"),
            "stride": row_closure.get("stride"),
            "profile_status": t33_profile.get("status"),
            "profile_file": profile_rel,
            "profile_sha256": sha(t33_profile_raw),
            "rows_file": f"scratch/t33/out/{t33_profile.get('full_rows_file')}",
            "rows_sha256": t33_profile.get("full_rows_sha256"),
            "declared_parent_codes": declared_parents,
            "nation_parent_code_intersection": overlap,
            "review_status": "partial_semantic_only_not_assigned" if table_id == 58 else "negative_no_exact_nation_parent_code",
            "note": (
                "STARTING_WEEKLY_WAGE_CONTRIBUTION is a near-name check against nation NWGv, but t33 only carries the club-side Cwcl candidate; no nation parent/read-sink join, so table58 is not assigned."
                if table_id == 58 else
                "Existing t33 candidate parents do not establish a nation list-parent link; profile retained as a non-assignment cross-check."
            ),
        })
        t33_source_hashes[profile_rel] = sha(t33_profile_raw)
    require(not any(row["nation_parent_code_intersection"] for row in t33_reviews),
            "t33 currently has an exact nation parent-code overlap; review assignment logic")

    # Recompute every primitive-width column from the existing full row dump.
    columns: list[dict[str, Any]] = []
    for width in (1, 2, 4, 8):
        for offset in range(int(closure["stride"]) - width + 1):
            columns.append(column_facts(rows, offset, width))

    source_tchl = next((field.get("list_item_fields", []) for field in club_fields if field.get("field") == "Tchl"), [])
    nation_tchl = next((field.get("list_item_fields", []) for _, field in nation_lists if field.get("field") == "Tchl"), [])
    require(bool(nation_tchl), "frozen nation schema lacks Tchl item fields")
    require(normalized_items(nation_tchl) == normalized_items(source_tchl),
            "nation and club Tchl item schema signatures differ")
    require(normalized_items(nation_tchl) == normalized_items(t29_tchl.get("schema_item_fields", [])),
            "nation Tchl item signature differs from t29 candidate schema")
    tchl_top_index = next(i for i, field in nation_lists if field.get("field") == "Tchl")
    tchl_items = [schema_item(field, tchl_top_index, j) for j, field in enumerate(nation_tchl)]
    tchl_candidates = item_candidates(tchl_items, columns, len(rows))
    add_candidate_samples(tchl_candidates, rows)

    # Output the reverified data-side profile while retaining t29 as immutable source.
    table34_profile = {
        "status": "complete_data_profile_reverified_L1",
        "table_type": 34,
        "archive": "server",
        "rtti_class": t14_34["primary_class"],
        "entity_tag": t14_34.get("entity_tag"),
        "parent_link_status": "partial_shared_schema_candidate",
        "payload": source_profile["payload"],
        "row_closure": closure,
        "full_rows_file": t29_rows_rel,
        "full_rows_sha256": source_profile["full_rows_sha256"],
        "source_profile": {
            "path": t29_profile_rel,
            "sha256": sha(source_profile_raw),
            "note": "Existing t29 full-data profile; t37 independently recomputed all listed primitive-width column statistics from its full raw rows.",
        },
        "profile_method": {
            "all_offsets": True,
            "widths": [1, 2, 4, 8],
            "statistics": [
                "unsigned range/distinct/top values/zero/sentinel/small value set",
                "u8 bit-mask frequency",
                "u32 reference domains including nation/club/team",
                "packed day/year diagnostics",
                "signed i32 cash-range samples",
                "float32 finite-value diagnostics",
            ],
            "interpretation_limit": "diagnostic compatibility only; no column name or field assignment is established",
            "frame_note": t29["provenance"].get("table34_sampling_note"),
        },
        "columns": columns,
    }
    profile_out = PROFILES / "table_server_34.profile.json"
    PROFILES.mkdir(parents=True, exist_ok=True)
    profile_bytes = (json.dumps(table34_profile, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    profile_out.write_bytes(profile_bytes)
    profile_sha = sha(profile_bytes)

    parents: list[dict[str, Any]] = []
    extra_schema_codes: list[str] = []
    expected_parent_codes = {field.get("field") for _, field in nation_lists}
    baseline_codes = {
        "Nagr", "TCrs", "Nrvn", "Nefr", "Nnfr", "Nntp", "Nctp", "Nrtp", "Nlns",
        "NTRv", "NWGv", "NSps", "NCro", "Ntxr", "Nfmp", "Nftb", "Calt",
        "Nchi", "Nphi", "Tko1", "Tkg1", "Tko2", "Tkg2", "Tko3", "Tkg3",
    }
    extra_schema_codes = sorted(expected_parent_codes - baseline_codes)

    for top_index, parent_field in nation_lists:
        code = parent_field.get("field")
        raw_items = parent_field.get("list_item_fields", [])
        items = [schema_item(item, top_index, j) for j, item in enumerate(raw_items)]
        blockers: list[str] = []
        row: dict[str, Any] = {
            "parent_4cc": code,
            "parent_name": parent_field.get("name"),
            "parent_schema_index": top_index,
            "parent_database_table_type": parent_field.get("database_table_type"),
            "schema_item_field_count": len(items),
            "schema_item_fields": items,
            "table_type": "unknown",
            "archive": "unknown",
            "rtti_class": "unknown",
            "reader_va": None,
            "count": None,
            "stride": None,
            "confidence": "unknown",
            "link_status": "partial_parent_to_table_unknown",
            "item_field_candidates": [],
            "profile": None,
            "blockers": blockers,
        }
        if code in T28_CODES:
            label, coll = t28_by_parent[code]
            count = int(coll["count"]["profile"]["total"])
            wire_stride = int(coll["wire_stride"])
            row.update({
                "table_type": 10,
                "archive": "client_inline",
                "archive_member": "client_db/table_10.dat",
                "rtti_class": census_by_type[10].get("primary_class", "NATION"),
                "t14_handler_off": census_by_type[10].get("handler_off"),
                "count": count,
                "count_semantics": "total inline list items across 251 nation client rows",
                "stride": wire_stride,
                "stride_semantics": "wire item bytes; not an independent table row stride",
                "item_object_stride": coll.get("item_object_stride"),
                "confidence": "existing_t28_closed",
                "link_status": "complete_linked_by_t28",
                "item_field_candidates": [
                    {
                        "field": field.get("code"),
                        "name": field.get("name"),
                        "type": field.get("type"),
                        "database_table_type": field.get("database_table_type"),
                        "status": "linked_by_t28_existing_L3",
                        "evidence_level": "existing_L3_not_promoted_by_t37",
                        "column_candidates": [],
                    }
                    for field in t28_field_rows[code]
                ],
                "blockers": [
                    "Already closed by t28 for the client table_10 inline collection; t37 does not repeat its field mapping or profiling.",
                    "t14 records the NATION handler/class but has no per-item reader_VA field; exact item reader coordinates remain in the accepted t28 evidence.",
                ],
                "t28_collection": {
                    "label": label,
                    "object_off": coll.get("object_off"),
                    "count_row_offset": coll["count"].get("row_offset"),
                    "items_row_offset": coll.get("items_row_offset"),
                    "t28_wire_stride": wire_stride,
                },
            })
        elif code == "Tchl":
            stage2 = stage2_identity_by_type.get(34, {})
            server_map = stage2_map_by_type.get(34, {})
            row.update({
                "table_type": 34,
                "archive": "server",
                "rtti_class": t14_34["primary_class"],
                "t14_handler_off": t14_34.get("handler_off"),
                "count": closure["count"],
                "stride": closure["stride"],
                "confidence": "low_candidate",
                "link_status": "partial_shared_schema_candidate",
                "item_field_candidates": tchl_candidates,
                "profile": {
                    "profile_file": "profiles/table_server_34.profile.json",
                    "profile_sha256": profile_sha,
                    "source_rows_file": t29_rows_rel,
                    "source_rows_sha256": source_profile["full_rows_sha256"],
                    "payload_sha256": source_profile["payload"]["payload_sha256"],
                    "payload_size": closure["payload_bytes"],
                    "packed_offset": source_profile["payload"].get("packed_offset"),
                    "row_start": closure["row_start"],
                    "footer_bytes": closure["footer_bytes"],
                    "equation": closure["equation"],
                },
                "stage2_identity": {
                    "status": stage2.get("status"),
                    "entity": stage2.get("entity"),
                    "level": stage2.get("level"),
                    "note": stage2.get("note"),
                    "stage2_map_status": server_map.get("status"),
                    "stage2_map_entity": server_map.get("entity"),
                },
                "existing_club_side_candidate": {
                    "source_inventory": "scratch/t29/out/subtable_inventory.json",
                    "parent_4cc": "Tchl",
                    "table_type": 34,
                    "reader_va": t29_tchl.get("reader_va"),
                    "scope_note": "t29 is the club-side candidate only; shared item schema does not prove the nation collection-to-table link.",
                },
                "blockers": [
                    "Nation and club Tchl item schemas have identical (field,name,type,database_table_type) signatures; this supports a shared-schema hypothesis only.",
                    "t29 links table_34 as a club-side Tchl candidate; no independent nation collection-to-table_34 reader/sink join is established.",
                    f"stage2_table_identity.json remains {stage2.get('status', 'unknown')} for table_34; do not treat the club entity attribution as nation ownership.",
                    "All column matches are L2 compatibility candidates with full statistics referenced in the profile; no L3 promotion is made.",
                ],
            })
        elif not items:
            row["link_status"] = "partial_zero_item_schema"
            row["confidence"] = "unknown"
            row["blockers"] = [
                "Frozen schema list_item_fields is empty; row shape may be ref-only, embedded, shared, or otherwise unresolved.",
                "No independent child-table identity or count/stride link is established by the consumed evidence.",
            ]
        else:
            row["item_field_candidates"] = [
                {
                    **item,
                    "status": "partial_parent_table_unknown",
                    "evidence_level": "unresolved",
                    "confidence": "unknown",
                    "column_candidate_count": 0,
                    "column_candidates": [],
                    "blocker": "No supported parent-to-table join; type compatibility alone is not used to assign a profile.",
                }
                for item in items
            ]
            row["blockers"] = [
                "No direct parent collection-to-table join is present in the consumed nation/t14/stage2 evidence.",
                "No independent full-row profile was assigned from semantic or value-shape similarity alone.",
            ]
            if code in RTTI_PROBES:
                expected = RTTI_PROBES[code]
                present = any(c.get("primary_class") == expected for c in census["tables"])
                row["rtti_name_probe"] = {
                    "expected_class_candidate": expected,
                    "exact_primary_class_present_in_t14": present,
                    "result": "partial_no_exact_rtti_name_match" if not present else "name_match_unjoined",
                }
                if not present:
                    row["blockers"].append(f"t14's complete 74-type census has no exact primary_class {expected}; parent remains unknown.")
            if code == "Ntxr":
                row["blockers"].append(
                    "t28 notes an Ntxr object container at nation object +0x60, but post-D object整理 is not list-item read evidence; all 9 item fields remain unresolved."
                )

        parents.append(row)

    candidate_fields = sum(
        1 for parent in parents for field in parent["item_field_candidates"]
        if field.get("status") == "L2_candidate"
    )
    candidate_matches = sum(
        len(field.get("column_candidates", []))
        for parent in parents for field in parent["item_field_candidates"]
    )
    table_row = {
        "table_type": 34,
        "archive": "server",
        "parent_candidates": ["Tchl"],
        "rtti_class": t14_34["primary_class"],
        "count": closure["count"],
        "stride": closure["stride"],
        "payload_size": closure["payload_bytes"],
        "payload_sha256": source_profile["payload"]["payload_sha256"],
        "row_closure_equation": closure["equation"],
        "profile_file": "profiles/table_server_34.profile.json",
        "profile_sha256": profile_sha,
        "link_status": "partial_shared_schema_candidate",
        "confidence": "low_candidate",
    }
    sources = {
        MASTER_REL: master_sha,
        "evidence/MANIFEST.json": sha(manifest_raw),
        "scratch/t14/out/census.json": sha(census_raw),
        "scratch/t14/out/stage2_map.json": sha(stage2_map_raw),
        "reports/stage2_table_identity.json": sha(stage2_identity_raw),
        "scratch/t28/out/cursor_nation_tail.json": sha(t28_raw),
        "scratch/t28/out/fields_nation_client.json": sha(t28_fields_raw),
        "scratch/t29/out/subtable_inventory.json": sha(t29_raw),
        t29_profile_rel: sha(source_profile_raw),
        t29_rows_rel: sha(source_rows_raw),
        **t33_source_hashes,
    }
    summary = {
        "nation_schema_fields": len(entity_fields),
        "nation_list_parent_count": len(parents),
        "item_bearing_parent_count": sum(bool(row["schema_item_field_count"]) for row in parents),
        "zero_item_parent_count": sum(not row["schema_item_field_count"] for row in parents),
        "baseline_omitted_schema_lists": extra_schema_codes,
        "linked_by_t28_parent_count": len(T28_CODES),
        "candidate_table_count": 1,
        "candidate_table_types": [34],
        "L2_candidate_item_field_count": candidate_fields,
        "candidate_column_match_count": candidate_matches,
        "unknown_or_partial_parent_count": sum(not row["link_status"].startswith("complete_") for row in parents),
        "new_L3_claims": 0,
        "L4": 0,
    }
    inventory = {
        "status": "partial_nation_parent_identity_coverage",
        "task": "t37 nation subtable data-side inventory; no static cursor and no L3 promotion",
        "generated_on": "2026-11-19",
        "provenance": {
            "schema_path": MASTER_REL,
            "schema_sha256": master_sha,
            "manifest_snapshot_date": manifest.get("snapshot_date"),
            "source_hashes": sources,
            "profile_basis": "Existing complete t29 server table34 full-row dump; t37 independently recomputed row closure and all primitive-width column statistics.",
            "t28_basis": "Existing accepted t28 client table10 evidence only; four linked parents are not redumped or re-promoted.",
            "t33_basis": "All seven t33 batch-II candidate/profile pairs were consumed; exact parent-code intersection with nation.xml is empty. Table58 is retained as a weekly-wage near-name non-assignment, not a nation mapping.",
            "multi_frame_note": t29["provenance"].get("table34_sampling_note"),
            "evidence_policy": "RTTI and table34 schema/value compatibility produce a low-confidence candidate only; no field-to-offset conclusion and no new L3/L4 claims.",
        },
        "summary": summary,
        "tables": [table_row],
        "parents": parents,
        "t33_profile_reviews": t33_reviews,
        "rtti_name_probes": [
            {"parent_4cc": code, **next(p["rtti_name_probe"] for p in parents if p["parent_4cc"] == code)}
            for code in RTTI_PROBES
        ],
        "next_static_handoff": [
            "For Tchl, confirm whether the nation collection reader reaches table_34's STARTING_TEAM_CUP_HISTORY reader/sink; t29 only covers the club-side candidate.",
            "For Nntp/Ntxr/Nfmp and the other unknowns, establish direct parent collection to serialized member/reader links before profiling additional tables.",
            "Keep Nlns/Nefr/Nnfr/Nagr linked_by_t28; do not spend static work duplicating their closed client-tail fields.",
        ],
    }
    inventory_path = OUT / "nation_subtable_inventory.json"
    inventory_path.write_text(json.dumps(inventory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = render_report(inventory)
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")
    done = (
        "# t37 Nation Subtable Inventory\n\n"
        "Status: `partial_nation_parent_identity_coverage`\n\n"
        f"Frozen-schema inventory: {summary['nation_list_parent_count']} list parents, "
        f"{summary['item_bearing_parent_count']} with item fields and {summary['zero_item_parent_count']} with zero item fields.\n\n"
        "One server table (34 / STARTING_TEAM_CUP_HISTORY) is retained as a low-confidence shared-schema candidate for nation Tchl. "
        "Four client inline collections remain linked by the existing t28 evidence. Seven t33 profiles were cross-checked; table58 remains unassigned to nation NWGv. No new L3 or L4 claims were made.\n\n"
        "Verification commands:\n\n"
        "```text\n"
        "py -V:3.12 -I -B scratch/t37/out/verify.py --selftest\n"
        "py -V:3.12 -I -B scratch/t37/out/verify.py\n"
        "py -V:3.12 -I -B scripts/t01_anchors.py\n"
        "```\n\n"
        "See `REPORT.md` for parent-by-parent coverage and blockers.\n"
    )
    (OUT / "DONE.md").write_text(done, encoding="utf-8")
    return inventory


def render_report(inventory: dict[str, Any]) -> str:
    summary = inventory["summary"]
    lines = [
        "# t37 — Nation Subtable Data-Side Inventory",
        "",
        "Status: `partial_nation_parent_identity_coverage`. This is data-side reconnaissance only; no static cursor work, new L3, or L4.",
        "",
        "## Coverage",
        "",
        f"- Frozen nation schema: {summary['nation_schema_fields']} fields and {summary['nation_list_parent_count']} list parents.",
        f"- Item-bearing / zero-item parents: {summary['item_bearing_parent_count']} / {summary['zero_item_parent_count']}.",
        f"- Existing t28 links: {summary['linked_by_t28_parent_count']} parents; new server-table candidate: table 34.",
        f"- L2 candidate fields / column matches: {summary['L2_candidate_item_field_count']} / {summary['candidate_column_match_count']}.",
        "- New L3 claims: 0; L4: 0.",
        "",
        "## Schema Baseline Difference",
        "",
        "The supplied baseline enumerated 17 item-bearing and 8 zero-item parents (25 total). The frozen `nation.xml` schema actually has 20 item-bearing and 9 zero-item list fields (29 total). The additional schema parents included here are `EDfx`, `Tchl`, `EDsc`, and `AXML`; none is silently dropped.",
        "",
        "## Candidate and Existing Links",
        "",
        "- `Tchl` → server table 34 / `STARTING_TEAM_CUP_HISTORY`: low-confidence shared-schema candidate. Nation and club Tchl item signatures match exactly; t29's existing association is club-side, and stage2 entity identity is still candidate. Table 34 closes as `14 + 7115 * 44 + 8 = 313082`. Candidate columns remain ambiguous and are referenced with full statistics in `profiles/table_server_34.profile.json`.",
        "- `Nlns`, `Nefr`, `Nnfr`, `Nagr`: `linked_by_t28`; existing client table_10 inline collections, not redumped here. Counts and wire strides are carried from the t28 collection evidence.",
        "",
        "## Parent Inventory",
        "",
        "| Parent | Items | Table | Archive | Count | Stride | Status |",
        "|---|---:|---:|---|---:|---:|---|",
    ]
    for row in inventory["parents"]:
        table = row["table_type"]
        count = row["count"] if row["count"] is not None else "unknown"
        stride = row["stride"] if row["stride"] is not None else "unknown"
        archive = row["archive"]
        lines.append(
            f"| `{row['parent_4cc']}` | {row['schema_item_field_count']} | `{table}` | {archive} | {count} | {stride} | `{row['link_status']}` |"
        )
    lines.extend([
        "",
        "## Tchl L2 Column Candidates",
        "",
        "Offsets are row-relative diagnostics, not field assignments. Full all-row column statistics, including sentinels, value domains, packed day/year, signed cash-range, float32 and u8 masks, are in the profile JSON. Multiple matching offsets are intentionally retained.",
        "",
    ])
    tchl = next(row for row in inventory["parents"] if row["parent_4cc"] == "Tchl")
    for field in tchl["item_field_candidates"]:
        matches = field["column_candidates"]
        offsets = ", ".join(f"+{m['offset']}/w{m['width']} ({m['score']:.3f})" for m in matches[:8]) or "none observed"
        if len(matches) > 8:
            offsets += f", ... ({len(matches)} total)"
        lines.append(f"- `{field['field']}` ({field['type']}, {field.get('database_table_type') or 'no table type'}): {offsets}.")
    lines.extend([
        "",
        "## T33 Batch-II Cross-Check",
        "",
        "All seven existing t33 profiles were consumed. None of their declared candidate parent codes exactly overlaps a nation list parent. Table 58 (`STARTING_WEEKLY_WAGE_CONTRIBUTION`, 8 rows x 45 bytes) was checked against `NWGv` by name only; t33's candidate is club-side `Cwcl`, so the nation link remains unassigned. Source profile hashes are in inventory provenance.",
        "",
        "## Unknowns and Blockers",
        "",
        "- All non-t28 parents other than Tchl lack an independent parent-to-table join in the consumed evidence. Unknown values stay `unknown`; semantic names, numeric shape and counts are not used as standalone identity proof.",
        "- The t14 census has no exact `NATION_TRANSFER_PREFERENCE`, `TAX_RULE`, or `FAMOUS_PLAYER` primary-class match for Nntp, Ntxr, or Nfmp, respectively.",
        "- Nation Tchl ownership of table 34 is unresolved. The row profile proves data availability and arithmetic closure only, not the schema parent.",
        "- Empty-item parents may be ref-only, embedded, or shared; no storage model is inferred.",
        "",
        "## Static Handoff",
        "",
    ])
    lines.extend(f"- {item}" for item in inventory["next_static_handoff"])
    lines.extend([
        "",
        "## Verification",
        "",
        "Run `py -V:3.12 -I -B scratch/t37/out/verify.py --selftest` and then `py -V:3.12 -I -B scratch/t37/out/verify.py`. The verifier independently recalculates table34 row closure and candidate-column statistics from the source full-row dump.",
        "",
    ])
    return "\n".join(lines)


def selftest() -> None:
    date_rows = [struct.pack("<I", (2020 << 16) | 1), struct.pack("<I", 0xFFFFFFFF), struct.pack("<I", (2021 << 16) | 366)]
    date_facts = column_facts(date_rows, 0, 4)
    assert date_facts["distinct"] == 3 and date_facts["sentinel_count"] == 1
    assert date_facts["packed_day_year"]["valid_count"] == 2
    ref_facts = column_facts([struct.pack("<I", 1), struct.pack("<I", 0xFFFFFFFF), struct.pack("<I", 250)], 0, 4)
    assert ref_facts["reference_domains"]["nation"]["in_range_count"] == 2
    u8 = column_facts([b"\x00", b"\x01", b"\x81"], 0, 1)
    assert u8["small_value_set"] == [0, 1, 129]
    assert u8["bit_masks"]["set_count_by_bit"] == [2, 0, 0, 0, 0, 0, 0, 1]
    field = {"type": "database_record_unique_id", "database_table_type": "nation"}
    assert compatibility(field, ref_facts)[0]
    print("SELFTEST PASS: ranges, sentinels, nation domain, dates, masks, and candidate compatibility")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the t37 nation list-parent data-side inventory.")
    parser.add_argument("--selftest", action="store_true", help="run synthetic checks without reading or writing repository data")
    args = parser.parse_args()
    if args.selftest:
        selftest()
        return 0
    try:
        result = build()
        print(json.dumps(result["summary"], ensure_ascii=False, sort_keys=True))
        print(f"wrote {OUT / 'nation_subtable_inventory.json'}")
        print(f"wrote {OUT / 'profiles/table_server_34.profile.json'}")
        return 0
    except CheckFailure as exc:
        print(f"CHECK FAILED: {exc}", file=sys.stderr)
        return 1
    except (OSError, ValueError, KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
        print(f"FATAL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
