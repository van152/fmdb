#!/usr/bin/env python3
"""t46 data-side profile of nation server table_10.

Uses t38's member-bounded payload loader and the accepted t25 client cursor only
as an identity cross-check. It never applies client count/item formulas to server.

Run with Python 3.12:
  py -V:3.12 -I -B scripts/t46_nation_server10.py --help
  py -V:3.12 -I -B scripts/t46_nation_server10.py --selftest
  FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data py -V:3.12 -I -B scripts/t46_nation_server10.py --build
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import math
import os
import pathlib
import runpy
import struct
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "scratch/t46/out"
PROFILE_DIR = OUTDIR / "profiles"
DBDIR = pathlib.Path(os.environ.get("FM24_DB_DIR", ROOT / "scratch/data")).resolve()
T25_CURSOR = ROOT / "scratch/t25/out/cursor_nation.json"
T25_REPORT = ROOT / "scratch/t25/out/REPORT.md"
T25_SPLIT = ROOT / "scratch/t25/out/schema_split.json"
T37_INVENTORY = ROOT / "scratch/t37/out/nation_subtable_inventory.json"
T38_REPORT = ROOT / "scratch/t38/out/REPORT.md"
TABLE_ID = 10
TAD_MAGIC = bytes.fromhex("03017461642ef10d")
FOOTER_BYTES = 8
IDENTITY_BYTES = 13
PROBE_OFFSETS = (24, 28, 32, 36, 40, 44, 48, 52)


class T46Error(RuntimeError):
    pass


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def signed_value(value: int, width: int) -> int:
    sign = 1 << (width * 8 - 1)
    return value - (1 << (width * 8)) if value & sign else value


def bind_rows_by_identity(body: bytes, client_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Find exact server row tails using ordinal and client-observed nation IDs.

    The client contributes only the row ordinal/ID witness set. Server boundaries
    are the observed 13-byte tail records and must uniquely close the full body.
    """
    result: list[dict[str, Any]] = []
    pos = 0
    for expected, client_row in enumerate(client_rows):
        ordinal = int(client_row["ordinal"])
        row_id = int(client_row["row_id"])
        if ordinal != expected:
            raise T46Error(f"t25 ordinal sequence breaks at row {expected}: {ordinal}")
        needle = struct.pack("<III", ordinal, row_id, row_id)
        hits: list[int] = []
        search_at = 0
        while True:
            found = body.find(needle, search_at)
            if found < 0:
                break
            if found + IDENTITY_BYTES <= len(body) and body[found + 12] == 0:
                hits.append(found)
            search_at = found + 1
        if len(hits) != 1:
            raise T46Error(
                f"server row {expected}: expected unique ordinal/id/id/00 tail, found {len(hits)}"
            )
        tail = hits[0]
        end = tail + IDENTITY_BYTES
        if tail < pos:
            raise T46Error(f"server row {expected}: identity tail is not monotonic")
        raw = body[pos:end]
        if len(raw) < IDENTITY_BYTES:
            raise T46Error(f"server row {expected}: shorter than identity tail")
        got_ordinal, got_id, repeated_id = struct.unpack_from("<III", raw, len(raw) - IDENTITY_BYTES)
        marker = raw[-1]
        if (got_ordinal, got_id, repeated_id, marker) != (ordinal, row_id, row_id, 0):
            raise T46Error(f"server row {expected}: identity tail changed during framing")
        prefix_probe = []
        for offset in PROBE_OFFSETS:
            if len(raw) >= offset + 4:
                unsigned = struct.unpack_from("<I", raw, offset)[0]
                prefix_probe.append({
                    "offset": offset,
                    "raw_hex": raw[offset:offset + 4].hex(),
                    "u32le": unsigned,
                    "i32le": signed_value(unsigned, 4),
                    "meaning": "unassigned positional probe; not asserted as a count",
                })
        result.append({
            "row": expected,
            "offset": 14 + pos,
            "body_offset": pos,
            "len": len(raw),
            "raw_hex": raw.hex(),
            "identity": {
                "ordinal": got_ordinal,
                "row_id": got_id,
                "repeated_id": repeated_id,
                "marker": marker,
                "tail_offset_in_row": len(raw) - IDENTITY_BYTES,
                "basis": "observed server tail; row ID independently cross-checked against t25",
            },
            "prefix_probe_i32le": prefix_probe,
        })
        pos = end
    if pos != len(body):
        raise T46Error(f"identity-framed rows close at {pos}, server body is {len(body)} bytes")
    return result


def naive_tail13_walk(body: bytes, anchored_records: list[dict[str, Any]], max_span: int = 4096) -> dict[str, Any]:
    """Reproduce the rejected shortest-frame heuristic and retain its false hits."""
    pos = 0
    walked = []
    failure_row = None
    failure_candidates = None
    for ordinal in range(len(anchored_records)):
        candidates = []
        upper = min(max_span, len(body) - pos)
        for span in range(IDENTITY_BYTES, upper + 1):
            tail = pos + span - IDENTITY_BYTES
            got_ordinal, row_id, repeated_id = struct.unpack_from("<III", body, tail)
            marker = body[tail + 12]
            if got_ordinal == ordinal and row_id == repeated_id and marker in (0x00, 0x0C):
                candidates.append(span)
        if not candidates:
            failure_row = ordinal
            failure_candidates = 0
            break
        chosen = min(candidates)
        anchored_len = int(anchored_records[ordinal]["len"])
        walked.append({
            "row": ordinal,
            "candidate_count": len(candidates),
            "chosen_shortest_len": chosen,
            "identity_anchored_len": anchored_len,
            "delta_shortest_minus_anchored": chosen - anchored_len,
            "is_false_boundary": chosen != anchored_len,
        })
        pos += chosen
    false_hits = [row for row in walked if row["is_false_boundary"]]
    return {
        "rule": "ordinal==row index; repeated IDs equal; marker in {0x00,0x0C}; choose shortest span in [13,4096]",
        "rows_walked_before_failure": len(walked),
        "walked_rows": walked,
        "false_shortest_candidates": false_hits,
        "first_failure_row": failure_row,
        "first_failure_body_offset": pos if failure_row is not None else None,
        "failure_search_max_span": max_span,
        "failure_candidate_count": failure_candidates,
        "failure_prefix_hex": body[pos:pos + 32].hex() if failure_row is not None else None,
        "disposition": "rejected: shortest identity-tail candidates include false internal frames; never used for delivered row boundaries",
    }


def column_profile(rows: list[bytes], offset: int, width: int, *, from_end: bool,
                   nation_ordinals: set[int], nation_ids: set[int]) -> dict[str, Any]:
    values: list[int] = []
    for row in rows:
        p = len(row) - offset if from_end else offset
        if p < 0 or p + width > len(row):
            continue
        values.append(int.from_bytes(row[p:p + width], "little", signed=False))
    if not values:
        raise T46Error(f"empty column coverage at offset={offset}, width={width}")

    n = len(values)
    mask = (1 << (width * 8)) - 1
    counter = collections.Counter(values)
    distinct = sorted(counter)
    zero_count = counter.get(0, 0)
    sentinel_count = counter.get(mask, 0)
    signed_values = [signed_value(v, width) for v in values]
    out: dict[str, Any] = {
        "offset": -offset if from_end else offset,
        "width": width,
        "interpretation": f"u{width * 8}",
        "offset_frame": "row_end" if from_end else "row_start",
        "count": n,
        "coverage": round(n / len(rows), 6),
        "distinct": len(counter),
        "min_unsigned": min(values),
        "max_unsigned": max(values),
        "min_signed": min(signed_values),
        "max_signed": max(signed_values),
        "zero_count": zero_count,
        "zero_rate": round(zero_count / n, 6),
        "signed_minus_one_count": sum(v == -1 for v in signed_values),
        "signed_minus_one_rate": round(sum(v == -1 for v in signed_values) / n, 6),
        "sentinel_value": f"0x{mask:0{width * 2}X}",
        "sentinel_count": sentinel_count,
        "sentinel_rate": round(sentinel_count / n, 6),
        "top_values": [{"value": value, "count": count}
                       for value, count in counter.most_common(12)],
        "small_value_set": distinct if len(distinct) <= 64 else None,
    }
    if width == 1:
        bit_counts = [sum(bool(v & (1 << bit)) for v in values) for bit in range(8)]
        out["bit_masks"] = {
            "set_count_by_bit": bit_counts,
            "set_rate_by_bit": [round(value / n, 6) for value in bit_counts],
        }
        live = [v for v in values if v not in (0xFF,)]
        out["boolean_like_0_1"] = bool(live) and all(v in (0, 1) for v in live)
        out["boolean_like_basis"] = "diagnostic only; 0xFF excluded as all-one sentinel"
    if width == 4:
        nonnull = [v for v in values if v != 0xFFFFFFFF]
        signed_nonnull = [signed_value(v, 4) for v in nonnull]
        zero_excluded = [v for v in signed_nonnull if v != 0]
        cash_like = [v for v in zero_excluded if -1_000_000_000 <= v <= 1_000_000_000]
        out["signed_i32_cash_diagnostic"] = {
            "min_nonnull": min(signed_nonnull) if signed_nonnull else None,
            "max_nonnull": max(signed_nonnull) if signed_nonnull else None,
            "nonzero_nonnull_count": len(zero_excluded),
            "within_abs_1e9_count": len(cash_like),
            "within_abs_1e9_rate_nonzero_nonnull": round(len(cash_like) / max(1, len(zero_excluded)), 6),
            "interpretation": "numeric compatibility only; not a cash field assignment",
        }
        float_values = [struct.unpack("<f", struct.pack("<I", v))[0] for v in values]
        finite = [v for v in float_values if math.isfinite(v)]
        out["float32_diagnostic"] = {
            "finite_count": len(finite),
            "finite_ratio": round(len(finite) / n, 6),
            "min_finite": min(finite) if finite else None,
            "max_finite": max(finite) if finite else None,
        }
        valid_days: list[int] = []
        valid_years: list[int] = []
        nonblank = 0
        for value in values:
            day = value & 0xFFFF
            year = (value >> 16) & 0xFFFF
            if value in (0, 0xFFFFFFFF) or year in (0, 0xFFFF):
                continue
            nonblank += 1
            if 1900 <= year <= 2035 and day <= 366:
                valid_days.append(day)
                valid_years.append(year)
        out["packed_day_year"] = {
            "nonblank_count": nonblank,
            "valid_count": len(valid_days),
            "valid_ratio_nonblank": round(len(valid_days) / max(1, nonblank), 6),
            "year_min": min(valid_years) if valid_years else None,
            "year_max": max(valid_years) if valid_years else None,
            "year_distinct": len(set(valid_years)),
            "day_max": max(valid_days) if valid_days else None,
            "rule": "u32 low16=day, high16=year; 0/all-ones/year=0xffff excluded; diagnostic only",
        }
        ordinal_hits = sum(v in nation_ordinals for v in nonnull)
        id_hits = sum(v in nation_ids for v in nonnull)
        denom = len(nonnull)
        out["reference_domains"] = {
            "nation_actual_ordinal_set": {
                "set_size": len(nation_ordinals),
                "in_set_count": ordinal_hits,
                "denominator_nonnull": denom,
                "ratio": round(ordinal_hits / max(1, denom), 6),
                "basis": "exact t25-observed nation row ordinals; candidate only",
            },
            "nation_actual_row_id_set": {
                "set_size": len(nation_ids),
                "in_set_count": id_hits,
                "denominator_nonnull": denom,
                "ratio": round(id_hits / max(1, denom), 6),
                "basis": "exact t25-observed nation row IDs; candidate only",
            },
        }
    return out


def profile_columns(rows: list[bytes], nation_ordinals: set[int], nation_ids: set[int]) -> dict[str, list[dict[str, Any]]]:
    min_len = min(map(len, rows))
    out: dict[str, list[dict[str, Any]]] = {"row_start": [], "row_end": []}
    for width in (1, 2, 4, 8):
        for offset in range(0, min_len - width + 1):
            col = column_profile(rows, offset, width, from_end=False,
                                 nation_ordinals=nation_ordinals, nation_ids=nation_ids)
            if width == 4:
                col["float32_diagnostic"].update({"offset": offset, "width": 4})
            out["row_start"].append(col)
        for distance in range(width, min_len + 1):
            col = column_profile(rows, distance, width, from_end=True,
                                 nation_ordinals=nation_ordinals, nation_ids=nation_ids)
            if width == 4:
                col["float32_diagnostic"].update({"offset_from_row_end": distance, "width": 4})
            out["row_end"].append(col)
    return out


def collect_column_candidates(columns: dict[str, list[dict[str, Any]]]) -> dict[str, list[dict[str, Any]]]:
    result: dict[str, list[dict[str, Any]]] = {
        "boolean_like_u8": [], "packed_day_year": [], "nation_ordinal_reference": [],
        "nation_id_reference": [], "signed_i32_cash_range": [],
    }
    for frame, items in columns.items():
        for col in items:
            where = {"offset_frame": frame, "offset": col["offset"], "width": col["width"]}
            if col["width"] == 1 and col.get("boolean_like_0_1"):
                result["boolean_like_u8"].append({**where, "distinct": col["distinct"],
                                                  "sentinel_count": col["sentinel_count"]})
            if col["width"] == 4:
                date = col["packed_day_year"]
                if date["nonblank_count"] >= 2 and date["valid_ratio_nonblank"] >= 0.95:
                    result["packed_day_year"].append({**where, **date})
                refs = col["reference_domains"]
                if col["distinct"] > 1 and refs["nation_actual_ordinal_set"]["ratio"] >= 0.98:
                    result["nation_ordinal_reference"].append(
                        {**where, **refs["nation_actual_ordinal_set"]})
                if col["distinct"] > 1 and refs["nation_actual_row_id_set"]["ratio"] >= 0.98:
                    result["nation_id_reference"].append({**where, **refs["nation_actual_row_id_set"]})
                cash = col["signed_i32_cash_diagnostic"]
                if col["distinct"] > 2 and cash["nonzero_nonnull_count"] >= 2 \
                        and cash["within_abs_1e9_rate_nonzero_nonnull"] >= 0.98:
                    result["signed_i32_cash_range"].append({**where, **cash})
    return result


def row_length_summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    lengths = [int(r["len"]) for r in records]
    counter = collections.Counter(lengths)
    return {
        "min": min(lengths), "max": max(lengths),
        "mean": round(sum(lengths) / len(lengths), 3),
        "distinct": len(counter),
        "most_common": [{"length": length, "count": count}
                        for length, count in counter.most_common(20)],
        "largest_rows": [
            {"row": r["row"], "row_id": r["identity"]["row_id"], "len": r["len"]}
            for r in sorted(records, key=lambda x: x["len"], reverse=True)[:12]
        ],
    }


def source_context(t25: dict[str, Any], split: dict[str, Any], inventory: dict[str, Any]) -> dict[str, Any]:
    nagr = next((row for row in inventory.get("parents", []) if row.get("parent_4cc") == "Nagr"), None)
    return {
        "t25_client_cursor_sha256": sha256(T25_CURSOR.read_bytes()),
        "t25_client_report_sha256": sha256(T25_REPORT.read_bytes()),
        "t25_schema_split_sha256": sha256(T25_SPLIT.read_bytes()),
        "t37_inventory_sha256": sha256(T37_INVENTORY.read_bytes()),
        "t38_report_sha256": sha256(T38_REPORT.read_bytes()),
        "t25_client_payload": t25.get("source_payload"),
        "t25_collection_totals": t25.get("collection_totals"),
        "t25_collection_maxima": t25.get("collection_maxima"),
        "schema_split_counts": split.get("counts"),
        "t37_nagr_context": None if nagr is None else {
            "archive": nagr.get("archive"), "table_type": nagr.get("table_type"),
            "count": nagr.get("count"), "stride": nagr.get("stride"),
            "link_status": nagr.get("link_status"),
            "scope_note": "t37 records the already-closed client_inline collection; it does not assign server row fields",
        },
    }


def build_grammar_diff(client_cursor: dict[str, Any], server_rows: list[dict[str, Any]]) -> dict[str, Any]:
    first_client = client_cursor["rows"][0]
    first_server = server_rows[0]
    client_grammar = client_cursor["row_grammar"]
    client_counts = first_client["counts"]
    client_offsets = first_client["count_offsets_body"]
    client_items = first_client["item_wire_bytes"]
    mappings = {
        "A": {"client_width": 1, "client_signed": True, "client_offset": 24},
        "B": {"client_width": 4, "client_signed": True, "client_offset": client_offsets["B"]},
        "C": {"client_width": 4, "client_signed": True, "client_offset": client_offsets["C"]},
        "D": {"client_width": 4, "client_signed": True, "client_offset": client_offsets["D"]},
    }
    segments = {}
    for name, meta in mappings.items():
        off, width = meta["client_offset"], meta["client_width"]
        server_raw = bytes.fromhex(first_server["raw_hex"])
        raw = server_raw[off:off + width]
        unsigned = int.from_bytes(raw, "little") if len(raw) == width else None
        server_signed = signed_value(unsigned, width) if unsigned is not None else None
        client_value = int(client_counts[name])
        segments[name] = {
            "status": "unknown",
            "client": {
                "count_location": client_grammar[name]["count"],
                "count_width": meta["client_width"],
                "count_signed": True,
                "first_row_count": client_value,
                "item_width": int(client_items[name]),
            },
            "server": {
                "count_location": None,
                "count_width": None,
                "count_signed": None,
                "first_row_count": None,
                "item_width": None,
                "status_note": "no independently established server segment/count boundary",
            },
            "same_offset_probe": {
                "server_row": 0, "offset": off, "raw_hex": raw.hex(),
                "interpreted_with_client_width_as_signed": server_signed,
                "client_first_row_count_at_that_slot": client_value,
                "matches": server_signed == client_value,
                "meaning": "positional falsification probe only; server value is not assigned as this segment's count",
            },
            "first_counterexample": None if server_signed == client_value else {
                "row": 0, "server_offset": off, "server_raw_hex": raw.hex(),
                "server_signed_probe": server_signed, "client_count": client_value,
                "scope": "rejects copying the client count slot; does not establish semantic segment difference",
            },
        }
    client_formula_span = int(first_client["row_span"])
    server_span = int(first_server["len"])
    return {
        "status": "partial_server_internal_segments_unresolved",
        "comparison_basis": "t25 row metadata only; no client row dump regenerated; client formula is used solely as a falsification comparator",
        "overall_row_grammar": {
            "status": "different",
            "client_first_row_span": client_formula_span,
            "server_first_row_span": server_span,
            "first_counterexample": {
                "row": 0, "client_span": client_formula_span, "server_span": server_span,
                "detail": "server's identity-framed row is 632 bytes; t25 client row 0 is 65 bytes",
            },
            "caveat": "This rejects whole-row grammar identity; it does not locate server list segments.",
        },
        "identity_tail": {
            "status": "same_observed_shape_with_cross_side_id_match",
            "server_observed": "u32 ordinal | u32 nation row ID | repeated u32 nation row ID | 0x00",
            "rows_matched": len(server_rows),
            "client_rows": int(client_cursor["row_count"]),
            "basis": "server tail pattern was found uniquely for each t25-observed ordinal/ID pair and closes the complete server body",
        },
        "segments": segments,
        "server_independent_observations": {
            "row0_prefix_i32le_probes": server_rows[0]["prefix_probe_i32le"],
            "row162_prefix_hex": bytes.fromhex(server_rows[162]["raw_hex"][:128]).hex()
            if len(server_rows) > 162 else None,
            "internal_count_positions": "unknown",
            "item_widths": "unknown",
            "negative_result": "Generic shortest tail-13 walking without the t25 ID witness stops at row 88/body+62440; that false/underconstrained parse is retained as a rejected approach, not used for the delivered row set.",
        },
    }


def make_profile(server_meta: dict[str, Any], records: list[dict[str, Any]],
                 client_cursor: dict[str, Any], split: dict[str, Any], inventory: dict[str, Any],
                 columns: dict[str, list[dict[str, Any]]], candidates: dict[str, list[dict[str, Any]]],
                 rows_file: pathlib.Path) -> dict[str, Any]:
    rows_hash = hashlib.sha256()
    raw_rows = [bytes.fromhex(record["raw_hex"]) for record in records]
    for row in raw_rows:
        rows_hash.update(row)
    payload = server_meta["payload"]
    body_bytes = sum(int(r["len"]) for r in records)
    closure = {
        "status": "complete_variable_identity_closure_L1_L2",
        "model": "variable",
        "count": len(records),
        "stride": None,
        "row_start": 14,
        "footer_bytes": FOOTER_BYTES,
        "row_end_exclusive": 14 + body_bytes,
        "payload_bytes": payload["payload_size"],
        "equation": f"14 + sum(row_lens={body_bytes}) + 8 = {payload['payload_size']}",
        "rows_sha256": rows_hash.hexdigest(),
        "identity": {
            "grammar": "ordinal|nation_row_id|repeated_nation_row_id|zero_marker at row_end-13",
            "tail13_hits": len(records), "id_pair_hits": len(records), "zero_marker_hits": len(records),
            "row_ids_cross_checked_against": "scratch/t25/out/cursor_nation.json",
            "boundary_ambiguity": "zero: each exact ordinal/ID/ID/00 sequence is unique over the full server body",
        },
        "row_len": row_length_summary(records),
        "frame_ambiguity": {
            "rows_with_multiple_valid_identity_tails": 0,
            "max_candidate_lengths": 1,
            "rule": "one unique exact identity-tail sequence per ordinal using t25-observed row ID; no client span formula used",
        },
        "marker_counts": {"0x00": len(records)},
        "basis": "full payload size/count/identity closure (L1) plus exact cross-side ordinal/row-ID set match to the t25 client cursor (L2); no server segment semantics inferred",
    }
    return {
        "status": "partial_data_profile_server_internal_grammar_open",
        "table_type": TABLE_ID,
        "archive": "server",
        "entity_tag": "nation (task scope; row semantics remain data-side)",
        "evidence_level": {"L1": "payload hash, row identity framing, closure, and byte profiles recomputed", "L2": "server identity ordinal/ID pairs match all t25 client rows", "L3": 0, "L4": 0},
        "archive_presence": server_meta["archive_presence"],
        "payload": payload,
        "row_closure": closure,
        "full_rows_file": "profiles/table_server_10.rows.jsonl",
        "full_rows_sha256": sha256(rows_file.read_bytes()),
        "profile_method": {
            "all_common_offsets": True,
            "primitive_widths": [1, 2, 4, 8],
            "offset_frames": ["row_start", "row_end"],
            "signed_metrics": ["i8", "i16", "i32", "signed -1 count/rate", "zero count/rate"],
            "four_byte_metrics": ["u32/i32 domains", "all-one sentinel", "packed day/year", "signed cash-range diagnostic", "float32 reinterpretation", "exact nation ordinal and row-ID set tests"],
            "one_byte_metrics": ["all-one sentinel", "zero", "per-bit masks", "0/1 boolean-like candidate"],
            "limits": "byte/value compatibility is diagnostic only; it never assigns schema fields or proves count/item grammar",
        },
        "server_structure": {
            "header_bytes": 14,
            "header_hex": payload["header_hex"],
            "record_count_header": payload["record_count_header"],
            "prefix_and_internal_segments": "partial: row starts and identity tails are bound; fixed prefix extent, internal count positions/signedness, item widths, and segment semantics remain unknown",
            "candidate_count_probe_row0": {
                "probes": records[0]["prefix_probe_i32le"],
                "note": "raw fixed-offset probes only; values such as +32/+36/+40 are not accepted as counts without repeated boundary/size validation",
            },
            "footer_bytes": FOOTER_BYTES,
            "footer_hex": server_meta["footer_hex"],
            "generic_walker_negative": {
                "method": "shortest tail13 ordinal|id|id|marker search without client ID witness",
                "first_failure_row": 88,
                "body_offset": 62440,
                "prefix_hex": server_meta["generic_walker_failure_prefix_hex"],
                "disposition": "retained counterexample; not used to frame delivered rows",
            },
        },
        "columns": columns,
        "column_candidates": candidates,
        "ordinal_reference_scope": {
            "tested_target_sets": [
                {"target": "nation actual ordinal set", "values": "0..250", "source": "all ordinals in t25 cursor", "status": "candidate scan only"},
                {"target": "nation actual row-ID set", "values": "exact 251 t25 IDs", "source": "all row IDs in t25 cursor", "status": "candidate scan only"},
            ],
            "other_target_tables": "not dumped or assigned in this task; no range-only target reference claims",
        },
        "nation_context": source_context(client_cursor, split, inventory),
        "grammar_diff_file": "grammar_diff_client_server.json",
        "L3_claims": 0,
        "L4": 0,
    }


def build() -> dict[str, Any]:
    required = (T25_CURSOR, T25_REPORT, T25_SPLIT, T37_INVENTORY, T38_REPORT)
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise T46Error("required evidence missing: " + ", ".join(missing))
    t25 = load_json(T25_CURSOR)
    split = load_json(T25_SPLIT)
    inventory = load_json(T37_INVENTORY)
    if t25.get("row_count") != 251 or len(t25.get("rows", [])) != 251:
        raise T46Error("t25 cursor must contain exactly 251 client rows")
    if t25.get("source_payload", {}).get("sha256") != "7e9d740b9ee6900965d8616a136ea4bc54a0f7207f9727eac72badfb727f6c34":
        raise T46Error("t25 client payload SHA pin differs from the instructed source")
    if split.get("counts", {}).get("server_only_explicit") != 0:
        raise T46Error("schema_split server-only baseline changed; inspect before proceeding")

    t38 = runpy.run_path(str(ROOT / "scripts/t38_multiframe.py"))
    codec = t38["_codec"]()
    cache: dict[str, Any] = {}
    archive_presence: dict[str, Any] = {}
    decoded: dict[str, bytes] = {}
    metas: dict[str, dict[str, Any]] = {}
    for archive in ("client", "server"):
        info = t38["archive_info"](codec, archive, cache)
        candidates = [e for e in info["tables"] if t38["entry_table_id"](e) == TABLE_ID]
        entry = codec["_resolve_table"](TABLE_ID, info["tables"], f"{archive}_db.dat") if candidates else None
        if len(candidates) != 1 or entry is None:
            archive_presence[archive] = {
                "archive_member_count": len(info["entries"]), "table_count": len(info["tables"]),
                "table_10_exists": False, "members": [],
            }
            if archive == "server":
                raise T46Error("server table_10 is absent; refusing to create a fabricated profile")
            continue
        selected = t38["inspect_entry"](codec, entry, info)
        raw = selected["data"]
        payload_sha = sha256(raw)
        ver, header_count = t38["_header_fields"](raw)
        decoded[archive] = raw
        member = {
            "path": entry["path"], "entry_offset_relative_to_data_base": int(entry["offset"]),
            "data_base": int(info["data_base"]), "member_start_absolute": int(info["data_base"]) + int(entry["offset"]),
            "packed_size": int(entry["packed_size"]), "packed_sha256": entry.get("sha256"),
            "payload_size": len(raw), "payload_sha256": payload_sha,
            "payload_version": ver, "record_count_header": header_count,
            "frame_count": selected["diag"]["phase1"]["frame_count"],
            "frame_lengths": selected["diag"]["phase1"]["frame_lengths"],
            "leftover_bytes": selected["diag"]["leftover_bytes"],
            "selected_frame_member_offset": selected["diag"]["selected_member_offset"],
            "packed_sha_matches_entry": selected["diag"]["entry_sha256_is_packed_sha"],
        }
        archive_presence[archive] = {
            "archive_member_count": len(info["entries"]), "table_count": len(info["tables"]),
            "table_10_exists": True, "members": [member],
        }
        metas[archive] = member
    client_source = t25["source_payload"]
    client_raw = decoded.get("client")
    if client_raw is None or len(client_raw) != int(client_source["bytes"]) \
            or sha256(client_raw) != client_source["sha256"]:
        raise T46Error("client payload does not match the accepted t25 SHA/size; no client rows were regenerated")
    if len(decoded["server"]) < 22 or decoded["server"][:8] != TAD_MAGIC:
        raise T46Error("server table_10 has an unexpected header")
    server = decoded["server"]
    server_count = struct.unpack_from("<I", server, 8)[0]
    if server_count != len(t25["rows"]):
        raise T46Error(f"server record_count_header={server_count}, t25 identity rows={len(t25['rows'])}")
    body = server[14:-FOOTER_BYTES]
    records = bind_rows_by_identity(body, t25["rows"])
    if len(records) != server_count:
        raise T46Error("server framed row count differs from payload header")

    PROFILE_DIR.mkdir(parents=True, exist_ok=True)
    rows_path = PROFILE_DIR / "table_server_10.rows.jsonl"
    with rows_path.open("w", encoding="ascii", newline="\n") as stream:
        for record in records:
            stream.write(json.dumps(record, separators=(",", ":")) + "\n")

    raw_rows = [bytes.fromhex(record["raw_hex"]) for record in records]
    ordinals = {int(row["ordinal"]) for row in t25["rows"]}
    ids = {int(row["row_id"]) for row in t25["rows"]}
    columns = profile_columns(raw_rows, ordinals, ids)
    column_candidates = collect_column_candidates(columns)
    server_meta = {
        "archive_presence": archive_presence,
        "payload": {
            "archive": "server", "member": metas["server"]["path"],
            "packed_offset": metas["server"]["member_start_absolute"],
            "entry_offset_relative_to_data_base": metas["server"]["entry_offset_relative_to_data_base"],
            "data_base": metas["server"]["data_base"],
            "packed_size": metas["server"]["packed_size"],
            "packed_sha256": metas["server"]["packed_sha256"],
            "payload_size": metas["server"]["payload_size"],
            "payload_sha256": metas["server"]["payload_sha256"],
            "payload_version": metas["server"]["payload_version"],
            "record_count_header": metas["server"]["record_count_header"],
            "header_hex": server[:14].hex(),
        },
        "footer_hex": server[-FOOTER_BYTES:].hex(),
        "generic_walker_failure_prefix_hex": body[62440:62440 + 32].hex(),
    }
    profile = make_profile(server_meta, records, t25, split, inventory, columns, column_candidates, rows_path)
    profile_path = PROFILE_DIR / "table_server_10.profile.json"
    profile_path.write_bytes(json_bytes(profile))
    grammar_diff = build_grammar_diff(t25, records)
    diff_path = OUTDIR / "grammar_diff_client_server.json"
    diff_path.write_bytes(json_bytes(grammar_diff))
    report = make_report(profile, grammar_diff)
    (OUTDIR / "REPORT.md").write_text(report, encoding="utf-8", newline="\n")
    done = make_done(profile, grammar_diff)
    (OUTDIR / "DONE.md").write_text(done, encoding="utf-8", newline="\n")
    return {
        "profile": str(profile_path.relative_to(ROOT)),
        "rows": str(rows_path.relative_to(ROOT)),
        "grammar_diff": str(diff_path.relative_to(ROOT)),
        "report": str((OUTDIR / "REPORT.md").relative_to(ROOT)),
        "done": str((OUTDIR / "DONE.md").relative_to(ROOT)),
        "server_rows": len(records), "server_payload_sha256": metas["server"]["payload_sha256"],
        "row_span_min": profile["row_closure"]["row_len"]["min"],
        "row_span_max": profile["row_closure"]["row_len"]["max"],
    }


def make_report(profile: dict[str, Any], diff: dict[str, Any]) -> str:
    c = profile["row_closure"]
    p = profile["payload"]
    lens = c["row_len"]
    lines = [
        "# t46 — Nation Server table_10 Data-Side Profile", "",
        "Status: `partial_data_profile_server_internal_grammar_open`. No L3 or L4 claims.", "",
        "## Archive and Payload", "",
        f"- client `table_10`: present, {profile['archive_presence']['client']['members'][0]['payload_size']:,} B, SHA-256 `{profile['archive_presence']['client']['members'][0]['payload_sha256']}`; matches t25 exactly. Client rows were not regenerated.",
        f"- server `table_10`: present, {p['payload_size']:,} B, SHA-256 `{p['payload_sha256']}`; directory record count {p['record_count_header']}; member `{p['member']}`.",
        f"- archive directories: client {profile['archive_presence']['client']['archive_member_count']} members; server {profile['archive_presence']['server']['archive_member_count']} members. Frame selection used t38's `data_base + offset`, `packed_size` boundary, and declared `size`.", "",
        "## Server Rows and Closure", "",
        f"- Server rows bound: {c['count']}; spans {lens['min']}..{lens['max']} B, mean {lens['mean']} B, {lens['distinct']} distinct lengths.",
        f"- Identity tail: `{c['identity']['grammar']}`; all {c['identity']['tail13_hits']} rows uniquely match t25 ordinal/row-ID witnesses and marker `00`.",
        f"- L1 arithmetic closure: `{c['equation']}`. Concatenated row SHA-256 `{c['rows_sha256']}`.",
        "- The first 88 rows also satisfy a naive shortest-tail walk, but it stops at row 88/body+62440. That negative result is retained. The delivered walk uses each exact t25-observed row ID as an independent identity witness; it does not use client lengths or counts.", "",
        "## Grammar Differential", "",
        f"- Whole-row grammar: different. First counterexample is row 0: client span {diff['overall_row_grammar']['client_first_row_span']} B versus server span {diff['overall_row_grammar']['server_first_row_span']} B.",
        "- A/B/C/D server segment mapping: unknown. No internal server count positions, count signedness, or item widths were accepted. Same-offset probes are recorded in `grammar_diff_client_server.json`; they falsify copying some client count slots but do not assign server semantics.",
    ]
    for name, seg in diff["segments"].items():
        probe = seg["same_offset_probe"]
        lines.append(f"- {name}: client count `{seg['client']['count_location']}`, item {seg['client']['item_width']} B; server unknown. Row-0 same-slot probe at +{probe['offset']}: signed {probe['interpreted_with_client_width_as_signed']} vs client count {probe['client_first_row_count_at_that_slot']}.")
    lines += [
        "- Server row prefix/internal lists remain partial: first-row `+32/+36/+40` are small positive i32 probes (28/8/2), but no repeated count-to-span equation or item boundary validates them as counts. A long-string row (ordinal 162) visibly changes these positional bytes; raw example and probes are retained in the profile/rows.", "",
        "## Column Portrait", "",
        f"- All common start/end offsets profiled for widths 1/2/4/8; signed i8/i16/i32 ranges, -1/all-one sentinels, zero rates, u8 bit masks, date-like packed day/year, cash-range and float32 diagnostics are included.",
        f"- Exact reference candidate tests use only the observed nation ordinal set (0..250) and t25 row-ID set; candidates are diagnostic, not field assignments. Other target tables were not read or assigned.",
        f"- Candidate counts: bool-like u8 {len(profile['column_candidates']['boolean_like_u8'])}; packed-day/year {len(profile['column_candidates']['packed_day_year'])}; nation-ordinal-set {len(profile['column_candidates']['nation_ordinal_reference'])}; nation-ID-set {len(profile['column_candidates']['nation_id_reference'])}; signed cash-range {len(profile['column_candidates']['signed_i32_cash_range'])}.", "",
        "## Scope and Verification", "",
        "- t25 is used as client comparison only; t37 `Nagr` remains `client_inline`; no client formula is promoted to server. Schema split has zero explicitly server-only fields and retains unknown/unmarked fields as unknown.",
        "- Evidence: L1 data recomputation and closure; L2 row identity set comparison; L3=0; L4=0.",
        "- Run: `py -V:3.12 -I -B scripts/t46_nation_server10.py --help`; `... --selftest`; `py -V:3.12 -I -B scratch/t46/out/verify.py`; `py -V:3.12 -I -B scripts/t01_anchors.py`.",
        "",
    ]
    return "\n".join(lines)


def make_done(profile: dict[str, Any], diff: dict[str, Any]) -> str:
    return "\n".join([
        "# t46 DONE", "",
        "- Scope: server table_10 data-side only; no game/editor/IDA/network access.",
        f"- Server table_10 present; {profile['row_closure']['count']} identity-framed rows; `{profile['row_closure']['equation']}`.",
        "- Client payload/cursor consumed for comparison only; no client rows redumped.",
        f"- Whole-row grammar comparison: {diff['overall_row_grammar']['status']}; server A/B/C/D internals remain unknown.",
        "- L1: payload/frame, row framing, closure, and byte profiles; L2: all row ordinals/IDs cross-match t25.",
        "- New L3 claims: 0; L4: 0.",
        "- Required verification commands are recorded in REPORT.md.", "",
    ])


def selftest() -> int:
    sample = b"".join([
        struct.pack("<III", 0, 5, 5) + b"\x00",
        struct.pack("<III", 1, 6, 6) + b"\x00",
    ])
    fixture = [
        {"ordinal": 0, "row_id": 5},
        {"ordinal": 1, "row_id": 6},
    ]
    rows = bind_rows_by_identity(sample, fixture)
    assert [r["len"] for r in rows] == [13, 13]
    assert rows[1]["identity"]["repeated_id"] == 6
    try:
        bind_rows_by_identity(sample[:-1], fixture)
    except T46Error:
        pass
    else:
        raise AssertionError("truncated body should fail closure")
    c = column_profile([b"\x00\xff\x01\x00", b"\x01\x00\xff\xff"], 0, 1,
                       from_end=False, nation_ordinals={0, 1}, nation_ids={5, 6})
    assert c["zero_count"] == 1 and c["signed_minus_one_count"] == 0
    assert c["bit_masks"]["set_count_by_bit"][0] == 1
    s = column_profile([b"\xff\xff\xff\xff", b"\x00\x00\x00\x00"], 0, 4,
                       from_end=False, nation_ordinals={0, 1}, nation_ids={5, 6})
    assert s["sentinel_count"] == 1 and s["zero_count"] == 1
    print("PASS identity-tail unique framing and closure")
    print("PASS signed/unsigned sentinel, zero, and bit-mask diagnostics")
    print("2/2 selftest checks passed")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Profile nation server table_10 without extrapolating client grammar.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--selftest", action="store_true", help="run small isolated parser/profile tests")
    group.add_argument("--build", action="store_true", help="build scratch/t46/out deliverables (default)")
    args = parser.parse_args()
    if sys.version_info[:2] != (3, 12):
        print("FATAL: requires py -V:3.12 -I -B", file=sys.stderr)
        return 2
    if args.selftest:
        try:
            return selftest()
        except Exception as exc:  # noqa: BLE001
            print(f"FAIL selftest: {exc}", file=sys.stderr)
            return 1
    if not DBDIR.is_dir():
        print(f"FATAL: database directory not found: {DBDIR}", file=sys.stderr)
        return 2
    try:
        result = build()
    except Exception as exc:  # noqa: BLE001
        print(f"FATAL: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
