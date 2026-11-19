#!/usr/bin/env python3
"""Independent t46 verifier for server nation table_10 outputs.

Run with Python 3.12:
  py -V:3.12 -I -B scratch/t46/out/verify.py --help
  py -V:3.12 -I -B scratch/t46/out/verify.py --selftest
  FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data py -V:3.12 -I -B scratch/t46/out/verify.py
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

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = pathlib.Path(__file__).resolve().parent
PROFILE_PATH = OUT / "profiles/table_server_10.profile.json"
ROWS_PATH = OUT / "profiles/table_server_10.rows.jsonl"
DIFF_PATH = OUT / "grammar_diff_client_server.json"
T25_CURSOR = ROOT / "scratch/t25/out/cursor_nation.json"
T38_PATH = ROOT / "scripts/t38_multiframe.py"
DBDIR = pathlib.Path(os.environ.get("FM24_DB_DIR", ROOT / "scratch/data")).resolve()
MAGIC = bytes.fromhex("03017461642ef10d")


class VerifyError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerifyError(message)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def signed(value: int, width: int) -> int:
    sign = 1 << (width * 8 - 1)
    return value - (1 << (width * 8)) if value & sign else value


def read_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_rows(path: pathlib.Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="ascii").splitlines() if line]


def expected_column(rows: list[bytes], column: dict[str, Any], ordinals: set[int], ids: set[int]) -> dict[str, Any]:
    width = int(column["width"])
    frame = column["offset_frame"]
    offset = int(column["offset"])
    values = []
    for row in rows:
        p = offset if frame == "row_start" else len(row) + offset
        require(0 <= p and p + width <= len(row), f"column points outside row: {column}")
        values.append(int.from_bytes(row[p:p + width], "little"))
    counts = collections.Counter(values)
    mask = (1 << (width * 8)) - 1
    signed_values = [signed(value, width) for value in values]
    result = {
        "count": len(values), "coverage": round(len(values) / len(rows), 6),
        "distinct": len(counts), "min_unsigned": min(values), "max_unsigned": max(values),
        "min_signed": min(signed_values), "max_signed": max(signed_values),
        "zero_count": counts.get(0, 0),
        "signed_minus_one_count": sum(value == -1 for value in signed_values),
        "sentinel_count": counts.get(mask, 0),
        "top_values": [{"value": value, "count": count} for value, count in counts.most_common(12)],
        "small_value_set": sorted(counts) if len(counts) <= 64 else None,
    }
    if width == 1:
        bit_counts = [sum(bool(value & (1 << bit)) for value in values) for bit in range(8)]
        live = [value for value in values if value != 0xFF]
        result["bit_masks"] = {
            "set_count_by_bit": bit_counts,
            "set_rate_by_bit": [round(value / len(values), 6) for value in bit_counts],
        }
        result["boolean_like_0_1"] = bool(live) and all(value in (0, 1) for value in live)
    if width == 4:
        nonnull = [value for value in values if value != 0xFFFFFFFF]
        signed_nonnull = [signed(value, 4) for value in nonnull]
        nonzero = [value for value in signed_nonnull if value != 0]
        cash = [value for value in nonzero if -1_000_000_000 <= value <= 1_000_000_000]
        result["signed_i32_cash_diagnostic"] = {
            "min_nonnull": min(signed_nonnull) if signed_nonnull else None,
            "max_nonnull": max(signed_nonnull) if signed_nonnull else None,
            "nonzero_nonnull_count": len(nonzero),
            "within_abs_1e9_count": len(cash),
            "within_abs_1e9_rate_nonzero_nonnull": round(len(cash) / max(1, len(nonzero)), 6),
            "interpretation": "numeric compatibility only; not a cash field assignment",
        }
        floats = [struct.unpack("<f", struct.pack("<I", value))[0] for value in values]
        finite = [value for value in floats if math.isfinite(value)]
        result["float32_diagnostic"] = {
            "finite_count": len(finite), "finite_ratio": round(len(finite) / len(values), 6),
            "min_finite": min(finite) if finite else None, "max_finite": max(finite) if finite else None,
        }
        if frame == "row_start":
            result["float32_diagnostic"].update({"offset": offset, "width": 4})
        else:
            result["float32_diagnostic"].update({"offset_from_row_end": -offset, "width": 4})
        days, years, nonblank = [], [], 0
        for value in values:
            day, year = value & 0xFFFF, (value >> 16) & 0xFFFF
            if value in (0, 0xFFFFFFFF) or year in (0, 0xFFFF):
                continue
            nonblank += 1
            if 1900 <= year <= 2035 and day <= 366:
                days.append(day)
                years.append(year)
        result["packed_day_year"] = {
            "nonblank_count": nonblank, "valid_count": len(days),
            "valid_ratio_nonblank": round(len(days) / max(1, nonblank), 6),
            "year_min": min(years) if years else None, "year_max": max(years) if years else None,
            "year_distinct": len(set(years)), "day_max": max(days) if days else None,
            "rule": "u32 low16=day, high16=year; 0/all-ones/year=0xffff excluded; diagnostic only",
        }
        result["reference_domains"] = {
            "nation_actual_ordinal_set": {
                "set_size": len(ordinals), "in_set_count": sum(value in ordinals for value in nonnull),
                "denominator_nonnull": len(nonnull),
                "ratio": round(sum(value in ordinals for value in nonnull) / max(1, len(nonnull)), 6),
                "basis": "exact t25-observed nation row ordinals; candidate only",
            },
            "nation_actual_row_id_set": {
                "set_size": len(ids), "in_set_count": sum(value in ids for value in nonnull),
                "denominator_nonnull": len(nonnull),
                "ratio": round(sum(value in ids for value in nonnull) / max(1, len(nonnull)), 6),
                "basis": "exact t25-observed nation row IDs; candidate only",
            },
        }
    return result


def derive_candidates(columns: dict[str, list[dict[str, Any]]]) -> dict[str, list[dict[str, Any]]]:
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
                    result["nation_ordinal_reference"].append({**where, **refs["nation_actual_ordinal_set"]})
                if col["distinct"] > 1 and refs["nation_actual_row_id_set"]["ratio"] >= 0.98:
                    result["nation_id_reference"].append({**where, **refs["nation_actual_row_id_set"]})
                cash = col["signed_i32_cash_diagnostic"]
                if col["distinct"] > 2 and cash["nonzero_nonnull_count"] >= 2 \
                        and cash["within_abs_1e9_rate_nonzero_nonnull"] >= 0.98:
                    result["signed_i32_cash_range"].append({**where, **cash})
    return result


def verify_columns(profile: dict[str, Any], raw_rows: list[bytes], cursor: dict[str, Any]) -> int:
    ordinals = {int(row["ordinal"]) for row in cursor["rows"]}
    ids = {int(row["row_id"]) for row in cursor["rows"]}
    checked = 0
    min_len = min(map(len, raw_rows))
    for frame in ("row_start", "row_end"):
        columns = profile["columns"][frame]
        expected_offsets = set()
        for width in (1, 2, 4, 8):
            distances = (range(0, min_len - width + 1) if frame == "row_start"
                         else range(width, min_len + 1))
            expected_offsets.update((width, offset if frame == "row_start" else -offset)
                                    for offset in distances)
        actual_offsets = {(int(col["width"]), int(col["offset"])) for col in columns}
        require(actual_offsets == expected_offsets, f"incomplete or extra {frame} offset coverage")
        for col in columns:
            expected = expected_column(raw_rows, col, ordinals, ids)
            for key, value in expected.items():
                require(col.get(key) == value,
                        f"column mismatch {frame} offset={col['offset']} width={col['width']} key={key}")
            require(col.get("coverage") == 1.0, f"incomplete common-offset coverage: {col}")
            checked += 1
    return checked


def verify() -> dict[str, Any]:
    for path in (PROFILE_PATH, ROWS_PATH, DIFF_PATH, OUT / "REPORT.md", OUT / "DONE.md", T25_CURSOR, T38_PATH):
        require(path.is_file(), f"missing required file: {path}")
    profile = read_json(PROFILE_PATH)
    diff = read_json(DIFF_PATH)
    cursor = read_json(T25_CURSOR)
    records = read_rows(ROWS_PATH)
    require(len(records) == 251 == cursor["row_count"], "row count mismatch")
    require(sha256(ROWS_PATH.read_bytes()) == profile["full_rows_sha256"], "rows JSONL SHA mismatch")
    require(diff["status"] == "partial_server_internal_segments_unresolved", "grammar diff status changed")
    require(diff["overall_row_grammar"]["status"] == "different", "whole-row grammar differential missing")
    require(all(diff["segments"][name]["status"] == "unknown" for name in "ABCD"),
            "unresolved server segment status was promoted")
    require({int(row["ordinal"]) for row in cursor["rows"]} == set(range(251)),
            "t25 nation ordinal set is not the expected observed 0..250 set")

    t38 = runpy.run_path(str(T38_PATH))
    codec = t38["_codec"]()
    cache: dict[str, Any] = {}
    payloads = {}
    archive_data = {}
    for archive in ("client", "server"):
        info = t38["archive_info"](codec, archive, cache)
        entry = codec["_resolve_table"](10, info["tables"], f"{archive}_db.dat")
        selected = t38["inspect_entry"](codec, entry, info)
        payloads[archive] = selected["data"]
        archive_data[archive] = (info, entry, selected["diag"])
        presence = profile["archive_presence"][archive]
        require(presence["table_10_exists"] is True, f"{archive} table_10 presence mismatch")
        require(presence["archive_member_count"] == len(info["entries"]), f"{archive} archive member count mismatch")
        require(presence["table_count"] == len(info["tables"]), f"{archive} table count mismatch")
        member = presence["members"][0]
        diag = selected["diag"]
        require(member["path"] == entry["path"], f"{archive} member path mismatch")
        require(member["entry_offset_relative_to_data_base"] == int(entry["offset"]), f"{archive} entry offset mismatch")
        require(member["data_base"] == info["data_base"] and member["member_start_absolute"] == diag["member_start"],
                f"{archive} data-base coordinate mismatch")
        require(member["packed_size"] == int(entry["packed_size"]) and member["payload_size"] == int(entry["size"]),
                f"{archive} member size mismatch")
        require(member["payload_sha256"] == sha256(selected["data"]), f"{archive} payload hash mismatch")
        require(member["packed_sha_matches_entry"] == diag["entry_sha256_is_packed_sha"],
                f"{archive} packed hash verification mismatch")
        require(member["frame_count"] == diag["phase1"]["frame_count"]
                and member["frame_lengths"] == diag["phase1"]["frame_lengths"],
                f"{archive} frame enumeration mismatch")
    client_sha = sha256(payloads["client"])
    require(client_sha == cursor["source_payload"]["sha256"], "client t25 source payload mismatch")
    server = payloads["server"]
    server_sha = sha256(server)
    require(server_sha == profile["payload"]["payload_sha256"], "server payload SHA mismatch")
    require(len(server) == profile["payload"]["payload_size"], "server payload size mismatch")
    require(server[:8] == MAGIC and server[:14].hex() == profile["payload"]["header_hex"], "server header mismatch")
    require(struct.unpack_from("<I", server, 8)[0] == len(records), "payload record count mismatch")
    footer_bytes = int(profile["row_closure"]["footer_bytes"])
    require(server[-footer_bytes:].hex() == profile["server_structure"]["footer_hex"], "footer mismatch")

    body = server[14:-footer_bytes]
    pos = 0
    raw_rows: list[bytes] = []
    concatenated = hashlib.sha256()
    for expected, (record, client_row) in enumerate(zip(records, cursor["rows"], strict=True)):
        ordinal, row_id = int(client_row["ordinal"]), int(client_row["row_id"])
        needle = struct.pack("<III", ordinal, row_id, row_id)
        hits = []
        at = 0
        while True:
            found = body.find(needle, at)
            if found < 0:
                break
            if found + 13 <= len(body) and body[found + 12] == 0:
                hits.append(found)
            at = found + 1
        require(len(hits) == 1, f"identity not unique at row {expected}: {len(hits)} hits")
        tail = hits[0]
        end = tail + 13
        require(tail >= pos, f"identity order regressed at row {expected}")
        raw = body[pos:end]
        require(record["row"] == expected, f"rows file ordinal mismatch at {expected}")
        require(record["offset"] == 14 + pos and record["body_offset"] == pos,
                f"rows file offset mismatch at row {expected}")
        require(record["len"] == len(raw), f"rows file length mismatch at row {expected}")
        require(bytes.fromhex(record["raw_hex"]) == raw, f"rows file bytes mismatch at row {expected}")
        got = struct.unpack_from("<III", raw, len(raw) - 13)
        require(got == (ordinal, row_id, row_id) and raw[-1] == 0,
                f"identity tail mismatch at row {expected}")
        expected_identity = record["identity"]
        require(expected_identity == {
            "ordinal": ordinal, "row_id": row_id, "repeated_id": row_id, "marker": 0,
            "tail_offset_in_row": len(raw) - 13,
            "basis": "observed server tail; row ID independently cross-checked against t25",
        }, f"identity metadata mismatch at row {expected}")
        raw_rows.append(raw)
        concatenated.update(raw)
        pos = end
    require(pos == len(body), f"rows end at {pos}, body ends at {len(body)}")
    closure = profile["row_closure"]
    require(closure["rows_sha256"] == concatenated.hexdigest(), "concatenated row SHA mismatch")
    require(closure["equation"] == f"14 + sum(row_lens={len(body)}) + 8 = {len(server)}",
            "closure equation mismatch")
    lengths = [len(row) for row in raw_rows]
    summary = closure["row_len"]
    require(summary["min"] == min(lengths) and summary["max"] == max(lengths), "row span range mismatch")
    require(summary["distinct"] == len(set(lengths)), "row span distinct-count mismatch")
    require(summary["mean"] == round(sum(lengths) / len(lengths), 3), "row span mean mismatch")
    identity = closure["identity"]
    require(identity["tail13_hits"] == len(raw_rows)
            and identity["id_pair_hits"] == len(raw_rows)
            and identity["zero_marker_hits"] == len(raw_rows), "identity closure counters mismatch")
    cols_checked = verify_columns(profile, raw_rows, cursor)
    require(profile["column_candidates"] == derive_candidates(profile["columns"]),
            "column candidate lists do not match verified column statistics")

    return {
        "status": "PASS",
        "server_payload_sha256": server_sha,
        "client_payload_sha256_matches_t25": client_sha,
        "rows": len(raw_rows), "body_bytes": len(body),
        "row_span_min": min(lengths), "row_span_max": max(lengths),
        "identity_unique_and_ordered": len(raw_rows),
        "profile_columns_recomputed": cols_checked,
        "L3": 0, "L4": 0,
    }


def selftest() -> int:
    rows = [b"\x00\xff\x00\x00", b"\x01\x00\x00\x00"]
    col = {
        "offset": 0, "width": 1, "offset_frame": "row_start",
    }
    out = expected_column(rows, col, {0, 1}, {5, 6})
    require(out["count"] == 2 and out["zero_count"] == 1 and out["distinct"] == 2,
            "synthetic column profile failed")
    print("PASS independent column-stat recomputation")
    print("1/1 selftest checks passed")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Independently verify t46 server table_10 outputs.")
    parser.add_argument("--selftest", action="store_true", help="run isolated verifier tests")
    args = parser.parse_args()
    if sys.version_info[:2] != (3, 12):
        print("FATAL: requires py -V:3.12 -I -B", file=sys.stderr)
        return 2
    try:
        result = selftest() if args.selftest else verify()
    except Exception as exc:  # noqa: BLE001
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    if isinstance(result, dict):
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
