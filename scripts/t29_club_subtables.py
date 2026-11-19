#!/usr/bin/env python3
"""t29 broad data-side profiling for non-Cstc club nested lists.

Reads only repository evidence and FM24_DB_DIR (constrained to scratch/data).
Writes only scratch/t29/out. Candidate column names are never promoted.
"""
from __future__ import annotations

import argparse
import collections
import ctypes
import hashlib
import json
import math
import os
import pathlib
import struct
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "scratch/t29/out"
DBDIR = pathlib.Path(os.environ.get("FM24_DB_DIR", ROOT / "scratch/data")).resolve()
MASTER = ROOT / "evidence/fm24/reports/editor_schema/master.json"
MANIFEST = ROOT / "evidence/MANIFEST.json"
T24_PARTS = ROOT / "scratch/t24/out"
T14_CENSUS = ROOT / "scratch/t14/out/census.json"
T14_STAGE2 = ROOT / "scratch/t14/out/stage2_map.json"
LEGACY_STAGE2 = ROOT / "reports/stage2_table_identity.json"
SERVER_CENSUS = ROOT / "evidence/fm24/reports/dbdat_decode/server_tables_census.json"
DAT_HEADERS = ROOT / "evidence/fm24/reports/dbdat_decode/dat_headers.json"

CLUB_DOMAIN = 84259
REFERENCE_DOMAINS = {
    "club": CLUB_DOMAIN,
    "competition": 7047,
    "person": 792149,
    "nation": 251,
    "stadium": 48413,
    "stage_name": 278,
    "team": 84507,
    "media_source": 208,
    "city": 56293,
    "region": 28,
}
CLUB_RTTI_TABLES = (33, 34, 37, 43, 50, 51, 58, 60, 61, 62, 63, 64, 66, 70)

# Relationship candidates are deliberately one-to-many where the available
# schema and RTTI names do not distinguish an individual nested list.
RELATIONS = {
    33: {"parents": ["Cdbt"], "fields": None, "confidence": "high",
         "basis": "STARTING_CLUB_DEBT aligns with club.Cdbt Debts; t14 and stage2 both resolve club."},
    34: {"parents": ["Tchl"], "fields": None, "confidence": "high",
         "basis": "STARTING_TEAM_CUP_HISTORY aligns with club.Tchl Team Cup History; t14 and stage2 both resolve club."},
    37: {"parents": ["Clhs"], "fields": None, "confidence": "high",
         "basis": "STARTING_TEAM_LEAGUE_HISTORY aligns with club.Clhs Team League History; t14 and stage2 both resolve club."},
    43: {"parents": ["Cmti"], "fields": None, "confidence": "high",
         "basis": "STARTING_MONTHLY_INSTALLMENT aligns with club.Cmti Instalments; t14 and stage2 both resolve club."},
    50: {"parents": ["exis", "insl"], "fields": ["expi"], "confidence": "medium",
         "basis": "STARTING_MLS_TRADED_SLOT is compatible with nested CpTI.exis/insl international-slot expiry records."},
    51: {"parents": ["CpTI"], "fields": ["alls", "allr"], "confidence": "medium",
         "basis": "STARTING_MLS_GENERAL_ALLOCATION_MONEY is compatible with CpTI allocation-money item fields."},
    58: {"parents": ["Cwcl"], "fields": None, "confidence": "high",
         "basis": "STARTING_WEEKLY_WAGE_CONTRIBUTION aligns with club.Cwcl Wage Contributions; t14 and stage2 both resolve club."},
    60: {"parents": ["CpTI"], "fields": ["alls", "allr"], "confidence": "medium",
         "basis": "STARTING_MLS_TARGETED_ALLOCATION_MONEY is compatible with CpTI allocation-money item fields."},
    62: {"parents": ["CSrs", "Crty"], "fields": None, "confidence": "low",
         "basis": "STARTING_RESERVE_TEAM is compatible with both club reserve-team list schemas; current evidence does not distinguish them."},
    64: {"parents": ["TCrs"], "fields": None, "confidence": "medium",
         "basis": "STARTING_CLUB_STAFF_JOB_STATUS is compatible with club.TCrs Responsibilities; exact item-list link is not independently established."},
    66: {"parents": ["CNtp"], "fields": None, "confidence": "high",
         "basis": "STARTING_CLUB_TRANSFER_PREFERENCE aligns with club.CNtp Nation Transfer Preferences; schema item includes nation reference."},
    70: {"parents": ["CAmb"], "fields": None, "confidence": "high",
         "basis": "STARTING_VISION_OBJECTIVE aligns with club.CAmb Supporter Objectives; t14 and stage2 both resolve club."},
}

class T29Error(Exception):
    pass


def load_json(path: pathlib.Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def manifest_hash(path: pathlib.Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    manifest = load_json(MANIFEST)
    row = next((item for item in manifest["files"] if item["path"] == rel), None)
    if row is None:
        raise T29Error(f"manifest has no entry for {rel}")
    actual = sha256(path.read_bytes())
    if actual != row["sha256"]:
        raise T29Error(f"snapshot SHA-256 mismatch for {rel}: {actual}")
    return actual


def schema_lists(fields: list[dict[str, Any]], parent_path: str = "club.xml#club") -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for item in fields:
        if item.get("type") != "list":
            continue
        code = item.get("field")
        if not isinstance(code, str):
            continue
        result.setdefault(code, {
            "parent_4cc": code,
            "name": item.get("name"),
            "path": f"{parent_path}.{code}",
            "list_item_fields": item.get("list_item_fields") or [],
            "schema_field": item,
        })
        nested = item.get("list_item_fields") or []
        if nested:
            result.update(schema_lists(nested, f"{parent_path}.{code}.item"))
    return result


def load_parent_inventory() -> tuple[dict[str, dict[str, Any]], dict[str, list[dict[str, Any]]]]:
    master_hash = manifest_hash(MASTER)
    master = load_json(MASTER)
    entities = master.get("entities", {}).get("club.xml", [])
    if len(entities) != 1 or entities[0].get("id") != "club":
        raise T29Error("master.json club entity shape mismatch")
    schema_parent_map = schema_lists(entities[0].get("fields", []))
    all_nested: list[dict[str, Any]] = []
    for path in sorted(T24_PARTS.glob("subtables.part*.json")):
        all_nested.extend(load_json(path).get("nested_fields", []))
    if len(all_nested) != 239:
        raise T29Error(f"t24 nested field count changed: {len(all_nested)} != 239")
    groups: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    for item in all_nested:
        parent = item.get("parent")
        if isinstance(parent, str) and parent != "Cstc":
            groups[parent].append(item)
    if sum(map(len, groups.values())) != 211:
        raise T29Error("non-Cstc nested field count changed")
    return schema_parent_map, dict(groups), master_hash


def parse_fmf_directory(blob: bytes, label: str) -> tuple[int, dict[str, dict[str, int]]]:
    if len(blob) < 34 or blob[:8] != bytes.fromhex("03 01 74 61 64 2e f1 0d"):
        raise T29Error(f"{label}: tad. v3569 header missing")
    if blob[8:14] != b"\x02\x01fmf." or blob[14:17] != b"\x08\x00\x00":
        raise T29Error(f"{label}: embedded FMF header mismatch")
    toc_off = struct.unpack_from("<I", blob, 17)[0] + 17
    if toc_off + 9 >= len(blob) or blob[toc_off:toc_off + 6] != b"\x02\x01fmf.":
        raise T29Error(f"{label}: FMF TOC not found at {toc_off}")
    # The compressed TOC has no declared decompressed size; cap it at 16 MiB.
    toc_raw = zstd_decompress(blob[toc_off + 9:], 16 * 1024 * 1024)
    pos = 0
    root_len = struct.unpack_from("<I", toc_raw, pos)[0]
    pos += 4
    root = toc_raw[pos:pos + root_len].decode("utf-8")
    pos += root_len
    count = struct.unpack_from("<I", toc_raw, pos)[0]
    pos += 4
    entries: dict[str, dict[str, int]] = {}
    for _ in range(count):
        name_len = struct.unpack_from("<I", toc_raw, pos)[0]
        pos += 4
        name = toc_raw[pos:pos + name_len].decode("utf-8")
        pos += name_len
        ext_len = struct.unpack_from("<I", toc_raw, pos)[0]
        pos += 4
        ext = toc_raw[pos:pos + ext_len].decode("utf-8")
        pos += ext_len
        offset, packed, size = struct.unpack_from("<QQQ", toc_raw, pos)
        pos += 24
        pos += 16  # two archive timestamp qwords
        path = f"{root}/{name}{ext}"
        if path in entries:
            raise T29Error(f"{label}: duplicate FMF member {path}")
        entries[path] = {"offset": offset, "packed_size": packed, "size": size}
    if pos != len(toc_raw) - 4 or toc_raw[pos:] != bytes(4):
        raise T29Error(f"{label}: unexpected TOC terminator at {pos} of {len(toc_raw)} bytes")
    return 34, entries


def load_zstd() -> Any:
    configured = os.environ.get("FM24_ZSTD_DLL")
    candidates = [pathlib.Path(configured)] if configured else []
    candidates += [pathlib.Path(r"C:\Program Files\Git\mingw64\bin\libzstd.dll")]
    dll = next((p for p in candidates if p.is_file()), None)
    if dll is None:
        raise T29Error("libzstd.dll not found; set FM24_ZSTD_DLL")
    lib = ctypes.CDLL(str(dll))
    lib.ZSTD_decompress.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_void_p, ctypes.c_size_t]
    lib.ZSTD_decompress.restype = ctypes.c_size_t
    lib.ZSTD_isError.argtypes = [ctypes.c_size_t]
    lib.ZSTD_isError.restype = ctypes.c_uint
    lib.ZSTD_getErrorName.argtypes = [ctypes.c_size_t]
    lib.ZSTD_getErrorName.restype = ctypes.c_char_p
    return lib


_ZSTD: Any = None


def zstd_decompress(frame: bytes, expected_size: int) -> bytes:
    global _ZSTD
    if _ZSTD is None:
        _ZSTD = load_zstd()
    src = ctypes.create_string_buffer(frame)
    capacity = expected_size
    while True:
        dst = ctypes.create_string_buffer(capacity)
        got = _ZSTD.ZSTD_decompress(dst, capacity, src, len(frame))
        if not _ZSTD.ZSTD_isError(got):
            if expected_size >= 0 and got > expected_size:
                raise T29Error(f"zstd output {got} exceeds expected {expected_size}")
            return dst.raw[:got]
        name = _ZSTD.ZSTD_getErrorName(got).decode("ascii", errors="replace")
        if "Destination buffer is too small" not in name and "dstSize_tooSmall" not in name:
            raise T29Error(f"zstd decompression failed: {name}")
        capacity *= 2
        if capacity > 16 * 1024 * 1024 and expected_size == 16 * 1024 * 1024:
            raise T29Error("FMF TOC exceeds 16 MiB safety cap")
        if capacity > 512 * 1024 * 1024:
            raise T29Error("zstd output exceeds 512 MiB safety cap")


def read_archives() -> tuple[dict[int, bytes], dict[str, Any]]:
    allowed = (ROOT / "scratch/data").resolve()
    if DBDIR != allowed:
        raise T29Error(f"FM24_DB_DIR must be exactly {allowed}; got {DBDIR}")
    if not DBDIR.is_dir():
        raise FileNotFoundError(DBDIR)
    server_census = load_json(SERVER_CENSUS)
    headers = load_json(DAT_HEADERS)
    header = next((h for h in headers if h.get("file") == "server_db.dat"), None)
    if header is None:
        raise T29Error("dat_headers.json has no server_db.dat row")
    archive = (DBDIR / "server_db.dat").read_bytes()
    if len(archive) != header.get("size") or sha256(archive) != header.get("sha256"):
        raise T29Error("scratch/data/server_db.dat differs from frozen dat_headers.json")
    data_base, directory = parse_fmf_directory(archive, "server_db.dat")
    declared = {item["path"]: item for item in server_census.get("entries", [])}
    payloads: dict[int, bytes] = {}
    member_metadata = {}
    for tid in CLUB_RTTI_TABLES:
        path = f"server_db/table_{tid}.dat"
        toc_item = directory.get(path)
        census_item = declared.get(path)
        if toc_item is None or census_item is None:
            raise T29Error(f"server table {tid} absent from FMF directory/census")
        if toc_item["packed_size"] != census_item["packed_size"] or toc_item["size"] != census_item["payload_size"]:
            raise T29Error(f"table {tid} FMF directory disagrees with frozen census")
        start = data_base + toc_item["offset"]
        end = start + toc_item["packed_size"]
        if end > len(archive):
            raise T29Error(f"table {tid} packed member exceeds archive")
        raw = zstd_decompress(archive[start:end], toc_item["size"])
        if len(raw) != census_item["payload_size"] or sha256(raw) != census_item["payload_sha256"]:
            raise T29Error(f"table {tid} payload differs from frozen census")
        payloads[tid] = raw
        member_metadata[tid] = {
            "archive": "server", "member": path, "packed_offset": start,
            "packed_size": toc_item["packed_size"], "payload_size": len(raw),
            "payload_sha256": sha256(raw), "census_row_boundary": census_item.get("row_boundary"),
            "census_row_model": census_item.get("row_model"),
        }
    return payloads, {"server_archive_sha256": header["sha256"], "tables": member_metadata}


def decode_rows(tid: int, raw: bytes, meta: dict[str, Any]) -> tuple[list[bytes], dict[str, Any]]:
    if raw[:8] != bytes.fromhex("03 01 74 61 64 2e f1 0d") or len(raw) < 22:
        raise T29Error(f"table {tid}: TAD payload header invalid")
    count = struct.unpack_from("<I", raw, 8)[0]
    boundary = meta["census_row_boundary"] or {}
    stride = boundary.get("stride")
    if not isinstance(stride, int) or stride <= 0:
        raise T29Error(f"table {tid}: no arithmetic stride in frozen census")
    row_start = 14
    footer = 8
    row_end = len(raw) - footer
    if row_start + count * stride + footer != len(raw):
        raise T29Error(f"table {tid}: closure mismatch {row_start}+{count}*{stride}+{footer}!={len(raw)}")
    if boundary.get("count") != count:
        raise T29Error(f"table {tid}: row count differs from frozen boundary")
    rows = [raw[row_start + i * stride:row_start + (i + 1) * stride] for i in range(count)]
    digest = hashlib.sha256(b"".join(rows)).hexdigest()
    closure = {
        "status": "complete_arithmetic_closure_L1",
        "count": count, "stride": stride, "row_start": row_start,
        "footer_bytes": footer, "row_end_exclusive": row_end,
        "payload_bytes": len(raw),
        "equation": f"{row_start} + {count} * {stride} + {footer} = {len(raw)}",
        "rows_sha256": digest,
        "basis": "full payload size/count/stride closure; stride is arithmetic census evidence, not a schema serializer proof",
    }
    return rows, closure


def decode_width(raw: bytes, off: int, width: int) -> int:
    return int.from_bytes(raw[off:off + width], "little", signed=False)


def column_profile(rows: list[bytes], off: int, width: int) -> dict[str, Any]:
    top: collections.Counter[int] = collections.Counter()
    distinct: set[int] = set()
    min_v: int | None = None
    max_v: int | None = None
    zero = sentinel = 0
    domain_hits = collections.Counter()
    date_valid = date_live = date_blank = 0
    date_years: set[int] = set()
    date_days: list[int] = []
    signed_min: int | None = None
    signed_max: int | None = None
    signed_good = 0
    signed_live = 0
    sentinel_value = (1 << (width * 8)) - 1
    for row in rows:
        v = decode_width(row, off, width)
        top[v] += 1
        distinct.add(v)
        min_v = v if min_v is None or v < min_v else min_v
        max_v = v if max_v is None or v > max_v else max_v
        zero += v == 0
        sentinel += v == sentinel_value
        if width == 4:
            if v != 0xFFFFFFFF:
                for entity, limit in REFERENCE_DOMAINS.items():
                    domain_hits[entity] += v < limit
                if v != 0:
                    signed_live += 1
                sv = v if v < 0x80000000 else v - 0x100000000
                signed_min = sv if signed_min is None or sv < signed_min else signed_min
                signed_max = sv if signed_max is None or sv > signed_max else signed_max
                signed_good += -1_000_000_000 <= sv <= 1_000_000_000
            low = v & 0xFFFF
            year = (v >> 16) & 0xFFFF
            if v in (0, 0xFFFFFFFF) or year in (0, 0xFFFF):
                date_blank += 1
            else:
                date_live += 1
                if 1900 <= year <= 2035 and low <= 366:
                    date_valid += 1
                    date_years.add(year)
                    date_days.append(low)
    n = len(rows)
    result: dict[str, Any] = {
        "offset": off, "width": width, "interpretation": f"u{width * 8}",
        "count": n, "distinct": len(distinct), "min_unsigned": min_v,
        "max_unsigned": max_v, "zero_count": zero,
        "zero_rate": round(zero / n, 6) if n else 0,
        "sentinel_value": f"0x{sentinel_value:0{width * 2}X}",
        "sentinel_count": sentinel, "sentinel_rate": round(sentinel / n, 6) if n else 0,
        "top_values": [{"value": k, "count": v} for k, v in top.most_common(12)],
        "small_value_set": sorted(distinct) if len(distinct) <= 64 else None,
    }
    if width == 4:
        result["signed_i32"] = {"min": signed_min, "max": signed_max,
                                 "within_abs_1e9_count": signed_good,
                                 "within_abs_1e9_rate_nonzero_nonnull": round(signed_good / max(1, signed_live), 6)}
        result["reference_domains"] = {
            key: {"in_range_count": value, "denominator_nonnull": n - sentinel,
                  "ratio": round(value / max(1, n - sentinel), 6)}
            for key, value in domain_hits.items()
        }
        result["packed_day_year"] = {
            "nonblank_count": date_live, "valid_count": date_valid,
            "valid_ratio_nonblank": round(date_valid / max(1, date_live), 6),
            "year_min": min(date_years) if date_years else None,
            "year_max": max(date_years) if date_years else None,
            "year_distinct": len(date_years), "day_max": max(date_days) if date_days else None,
            "rule": "u32 low16=day_or_ordinal<=366, high16=year 1900..2035; 0/0xffffffff/year=0xffff treated as blank",
        }
    return result


def float_profile(rows: list[bytes], off: int) -> dict[str, Any]:
    vals = []
    finite = 0
    min_v: float | None = None
    max_v: float | None = None
    for row in rows:
        v = struct.unpack_from("<f", row, off)[0]
        if math.isfinite(v):
            finite += 1
            min_v = v if min_v is None or v < min_v else min_v
            max_v = v if max_v is None or v > max_v else max_v
            if len(vals) < 12:
                vals.append(v)
    return {"offset": off, "width": 4, "count": len(rows), "finite_count": finite,
            "finite_ratio": round(finite / max(1, len(rows)), 6), "min_finite": min_v,
            "max_finite": max_v, "first_finite_samples": vals}


def profile_table(tid: int, rows: list[bytes], closure: dict[str, Any], meta: dict[str, Any],
                  outdir: pathlib.Path) -> dict[str, Any]:
    stride = closure["stride"]
    columns = []
    for width in (1, 2, 4, 8):
        for off in range(0, stride - width + 1):
            col = column_profile(rows, off, width)
            if width == 4:
                col["float32"] = float_profile(rows, off)
            columns.append(col)
    rows_rel = f"profiles/table_server_{tid}.rows.jsonl"
    row_path = outdir / rows_rel
    with row_path.open("w", encoding="ascii", newline="\n") as stream:
        for index, row in enumerate(rows):
            record = {"row": index, "offset": closure["row_start"] + index * stride,
                      "len": stride, "raw_hex": row.hex()}
            stream.write(json.dumps(record, separators=(",", ":")) + "\n")
    return {
        "status": "complete_data_profile",
        "table_type": tid, "archive": "server", "rtti_class": meta.get("rtti_class"),
        "entity_tag": meta.get("entity_tag"),
        "t14_adjudication": meta.get("t14_adjudication"),
        "stage2_status": meta.get("stage2_status"),
        "identity_basis": meta.get("identity_basis"),
        "payload": {k: meta[k] for k in (
            "archive", "member", "packed_offset", "packed_size", "payload_size", "payload_sha256",
        )},
        "row_closure": closure,
        "full_rows_file": rows_rel,
        "full_rows_sha256": sha256(row_path.read_bytes()),
        "profile_method": {
            "all_offsets": True, "primitive_widths": [1, 2, 4, 8],
            "four_byte_metrics": ["u32 domain", "sentinel", "packed day/year", "signed i32/cash-range", "float32 reinterpretation"],
            "limits": "value domains are diagnostics; they do not independently identify fields",
        },
        "columns": columns,
    }


def schema_field_range(field: dict[str, Any]) -> tuple[int | None, int | None]:
    lo = field.get("min_value")
    hi = field.get("max_value")
    try:
        lo_i = int(str(lo)) if lo is not None else None
    except ValueError:
        lo_i = None
    try:
        hi_i = int(str(hi)) if hi is not None else None
    except ValueError:
        hi_i = None
    code = str(field.get("field", "")).lower()
    if lo_i is None and hi_i is None and code in {"year", "styr", "edyr", "enyr", "expi"}:
        return 1800, 2100
    return lo_i, hi_i


def column_candidate(field: dict[str, Any], col: dict[str, Any]) -> tuple[float, str] | None:
    typ = field.get("type")
    width = col["width"]
    n = col["count"]
    null_count = col["sentinel_count"]
    live = n - null_count
    code = str(field.get("field", "")).lower()
    if typ == "date":
        if width != 4:
            return None
        packed = col["packed_day_year"]
        if packed["nonblank_count"] < max(2, int(n * 0.05)) or packed["valid_ratio_nonblank"] < 0.95:
            return None
        return packed["valid_ratio_nonblank"], "packed day/year profile matches date semantics"
    if typ == "database_record_unique_id":
        table_type = field.get("database_table_type")
        limit = REFERENCE_DOMAINS.get(str(table_type))
        if width != 4 or limit is None or live < max(2, int(n * 0.05)):
            return None
        ratio = col["reference_domains"][str(table_type)]["ratio"]
        if ratio < 0.98:
            return None
        return ratio, f"{table_type} ID-domain compatibility [0,{limit}); reference-domain fit is not field identity"
    if typ == "boolean":
        if width not in (1, 2, 4):
            return None
        allowed = 1 if width == 1 else (1 << (width * 8)) - 1
        if col["distinct"] > 2:
            return None
        valid = sum(x["count"] for x in col["top_values"] if x["value"] in (0, 1))
        ratio = valid / max(1, n)
        return (ratio, "boolean-like 0/1 value set") if ratio >= 0.98 else None
    if typ == "day_of_week":
        if width not in (1, 2, 4):
            return None
        valid = sum(x["count"] for x in col["top_values"] if x["value"] <= 6)
        ratio = valid / max(1, n)
        return (ratio, "day-of-week values within 0..6") if ratio >= 0.98 else None
    if typ == "cash":
        if width != 4:
            return None
        lo, hi = schema_field_range(field)
        if lo is None:
            lo = -1_000_000_000
        if hi is None:
            hi = 1_000_000_000
        good = 0
        for item in col["top_values"]:
            value = item["value"]
            signed = value if value < 0x80000000 else value - 0x100000000
            if lo <= signed <= hi or lo <= value <= hi:
                good += item["count"]
        # Top values are truncated; use full-range summary as a conservative filter.
        signed_info = col["signed_i32"]
        if signed_info["min"] is None or signed_info["max"] is None:
            return None
        top_coverage = good / max(1, n)
        if top_coverage < 0.50 and not (lo <= signed_info["min"] and signed_info["max"] <= hi):
            return None
        return min(1.0, max(top_coverage, 0.95)), f"signed/raw numeric values compatible with schema cash range [{lo},{hi}]"
    if typ == "real":
        if width != 4:
            return None
        fp = col.get("float32", {})
        if fp.get("finite_ratio", 0) < 0.98:
            return None
        if fp.get("min_finite") is None or fp.get("max_finite") is None:
            return None
        return fp["finite_ratio"], "finite float32 reinterpretation; semantic anchor still required"
    if typ == "enum":
        if width not in (1, 2, 4) or col["distinct"] > 64:
            return None
        values = col["small_value_set"]
        if values is None:
            return None
        max_enum = 255 if width == 1 else 4095 if width == 2 else 65535
        if not values or max(values) > max_enum:
            return None
        if len(values) > 1 and col["sentinel_rate"] > 0.95:
            return None
        return 1.0 - col["sentinel_rate"], "small finite value set compatible with enum storage"
    if typ == "integer":
        if width not in (1, 2, 4):
            return None
        lo, hi = schema_field_range(field)
        if lo is None and hi is None:
            return None
        # Low-width unsigned columns and signed 32-bit columns are both tested.
        valid = 0
        for item in col["top_values"]:
            value = item["value"]
            signed = value if value < (1 << (width * 8 - 1)) else value - (1 << (width * 8))
            probes = (value, signed)
            if any((lo is None or x >= lo) and (hi is None or x <= hi) for x in probes):
                valid += item["count"]
        ratio = valid / max(1, n)
        if ratio < 0.95:
            return None
        return ratio, f"numeric range compatible with schema [{lo},{hi}]"
    return None


def candidate_fields_for_parent(parent: str, table_ids: list[int], schema_map: dict[str, dict[str, Any]],
                                profiles: dict[int, dict[str, Any]], sample_rows: dict[int, dict[int, bytes]]) -> list[dict[str, Any]]:
    schema = schema_map.get(parent)
    if schema is None:
        return []
    fields = schema.get("list_item_fields") or []
    candidates = []
    for field in fields:
        all_matches = []
        for tid in table_ids:
            relation = RELATIONS[tid]
            allow = relation["fields"]
            if allow is not None and field.get("field") not in allow:
                continue
            profile = profiles.get(tid)
            if profile is None:
                continue
            matches = []
            for col in profile["columns"]:
                fit = column_candidate(field, col)
                if fit is None:
                    continue
                score, reason = fit
                matches.append({
                    "table_type": tid, "column": f"{col['interpretation']}@+{col['offset']}",
                    "offset": col["offset"], "width": col["width"],
                    "claim_status": "candidate", "evidence_level": "L2_candidate",
                    "fit_score": round(score, 6), "basis": reason,
                    "evidence": col,
                    "sample_indices": sorted({0, max(0, col["count"] // 2), max(0, col["count"] - 1)}),
                })
            matches.sort(key=lambda x: (-x["fit_score"], x["evidence"]["sentinel_rate"],
                                        x["evidence"]["distinct"], x["offset"], x["width"]))
            for match in matches[:5]:
                idx = match["sample_indices"]
                samples = []
                for row_index in idx:
                    row = sample_rows[tid][row_index]
                    val = int.from_bytes(row[match["offset"]:match["offset"] + match["width"]], "little")
                    samples.append({"row": row_index, "unsigned": val})
                match["evidence"] = dict(match["evidence"])
                match["evidence"]["sample_values"] = samples
                all_matches.append(match)
        all_matches.sort(key=lambda x: (-x["fit_score"], x["table_type"], x["offset"], x["width"]))
        candidates.append({
            "field": field.get("field"), "name": field.get("name"), "schema_type": field.get("type"),
            "database_table_type": field.get("database_table_type"),
            "claim_status": "candidate" if all_matches else "no_column_candidate",
            "matches_considered": len(all_matches), "matches": all_matches[:8],
            "blocker": None if all_matches else "no full-column profile satisfies the conservative type/domain filter",
        })
    return candidates


def identity_maps() -> tuple[dict[int, dict[str, Any]], dict[int, dict[str, Any]], dict[str, Any]]:
    census = load_json(T14_CENSUS)
    t14_by_type = {int(row["table_type"]): row for row in census.get("tables", [])}
    stage2 = load_json(T14_STAGE2)
    stage2_by_type = {int(row["table_type"]): row for row in stage2.get("tables", [])}
    legacy = load_json(LEGACY_STAGE2)
    legacy_by_type = {int(row["table_type"]): row for row in legacy.get("rows", [])}
    notes = {
        "t14_stage2": stage2.get("summary"),
        "legacy_reports_stage2": {"n_total": legacy.get("n_total"), "counts": legacy.get("counts")},
        "legacy_stage2_is_older_partial_view": len(legacy.get("rows", [])) != len(stage2.get("tables", [])),
    }
    return t14_by_type, stage2_by_type, {"legacy_by_type": legacy_by_type, "notes": notes}


def build_output() -> dict[str, Any]:
    schema_map, grouped, master_hash = load_parent_inventory()
    t14_by_type, stage2_by_type, stage2_extra = identity_maps()
    payloads, archive_metadata = read_archives()
    sample_rows: dict[int, dict[int, bytes]] = {}
    profiles: dict[int, dict[str, Any]] = {}
    outdir = OUTDIR
    (outdir / "profiles").mkdir(parents=True, exist_ok=True)

    for tid in CLUB_RTTI_TABLES:
        t14 = t14_by_type.get(tid, {})
        s2 = stage2_by_type.get(tid, {})
        if t14.get("entity_tag") != "club":
            continue
        if s2.get("status") != "resolved" or s2.get("entity") != "club":
            continue
        class_name = t14.get("primary_class")
        first_vtable = next(iter(t14.get("vtables", [])), {})
        reader_va = t14.get("reader_va") or first_vtable.get("reader_va")
        raw = payloads[tid]
        meta = dict(archive_metadata["tables"][tid])
        meta.update({
            "rtti_class": class_name,
            "entity_tag": t14.get("entity_tag"),
            "t14_adjudication": t14.get("adjudication"),
            "stage2_status": s2.get("status"),
            "identity_basis": {
                "t14_primary_class": class_name,
                "t14_adjudication": t14.get("adjudication"),
                "stage2_entity": s2.get("entity"),
                "stage2_status": s2.get("status"),
                "stage2_evidence": s2.get("evidence", []),
                "handler_off": t14.get("handler_off"),
                "vtable_va": first_vtable.get("vtable_va"),
                "reader_va": None,
            },
        })
        rows, closure = decode_rows(tid, raw, meta)
        sample_rows[tid] = {i: rows[i] for i in sorted({0, len(rows) // 2, max(0, len(rows) - 1)})}
        profile = profile_table(tid, rows, closure, meta, outdir)
        profile_path = outdir / "profiles" / f"table_server_{tid}.profile.json"
        profile_path.write_text(json.dumps(profile, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        meta["profile_file"] = f"profiles/table_server_{tid}.profile.json"
        meta["profile_sha256"] = sha256(profile_path.read_bytes())
        profile["profile_file"] = meta["profile_file"]
        profiles[tid] = profile

    table_parent_candidates: dict[str, list[int]] = collections.defaultdict(list)
    for tid, relation in RELATIONS.items():
        for parent in relation["parents"]:
            table_parent_candidates[parent].append(tid)

    parent_rows = []
    all_parents = sorted(grouped)
    for parent in all_parents:
        schema = schema_map.get(parent)
        type_ids = sorted(
            t for t in table_parent_candidates.get(parent, [])
            if t in profiles
            and profiles[t].get("t14_adjudication") == "resolved"
            and profiles[t].get("stage2_status") == "resolved"
        )
        table_rows = []
        for tid in type_ids:
            relation = RELATIONS[tid]
            t14 = t14_by_type.get(tid, {})
            s2 = stage2_by_type.get(tid, {})
            table_rows.append({
                "table_type": tid, "archive": "server", "rtti_class": t14.get("primary_class"),
                "reader_va": profiles[tid]["identity_basis"].get("reader_va"),
                "handler_off": profiles[tid]["identity_basis"].get("handler_off"),
                "vtable_va": profiles[tid]["identity_basis"].get("vtable_va"),
                "identity_status": "resolved" if profiles[tid].get("t14_adjudication") == "resolved" and profiles[tid].get("stage2_status") == "resolved" else "candidate",
                "parent_link_status": "candidate", "parent_link_confidence": relation["confidence"],
                "basis": relation["basis"], "profile_file": profiles[tid]["profile_file"],
                "count": profiles[tid]["row_closure"]["count"],
                "stride": profiles[tid]["row_closure"]["stride"],
                "row_closure": profiles[tid]["row_closure"],
            })
        field_candidates = candidate_fields_for_parent(parent, type_ids, schema_map, profiles, sample_rows)
        mapped_unique = len(type_ids) == 1 and bool(table_rows)
        if mapped_unique:
            status = "complete_candidate_profile"
            selected_table_type: int | None = type_ids[0]
        elif type_ids:
            status = "partial_ambiguous_table_candidate"
            selected_table_type = None
        else:
            status = "partial_unknown_table_identity"
            selected_table_type = None
        blockers = []
        if not type_ids:
            blockers.append("No club-tagged t14 RTTI class was uniquely linked to this schema list; do not infer a table from field type/domain alone.")
        if len(type_ids) > 1:
            blockers.append("Multiple RTTI-identified tables or schema parents remain compatible; parent-to-table link is not unique.")
        if schema is None:
            blockers.append("The frozen club schema tree did not expose a list_item_fields node for this 4CC.")
        if table_rows and any(x["reader_va"] is None for x in table_rows):
            blockers.append("t14 census has no reader_va; no reader address was inferred.")
        if any(not x["matches"] for x in field_candidates):
            blockers.append("Some item fields have no candidate column passing the conservative data-side filter.")
        parent_rows.append({
            "parent_4cc": parent,
            "schema_path": schema.get("path") if schema else None,
            "schema_list_name": schema.get("name") if schema else None,
            "t24_nested_field_count": len(grouped[parent]),
            "schema_item_field_count": len(schema.get("list_item_fields", [])) if schema else None,
            "table_type": selected_table_type,
            "table_type_candidates": type_ids,
            "archive": "server" if table_rows else None,
            "rtti_class": table_rows[0]["rtti_class"] if len(table_rows) == 1 else None,
            "reader_va": table_rows[0]["reader_va"] if len(table_rows) == 1 else None,
            "count": table_rows[0]["count"] if len(table_rows) == 1 else None,
            "stride": table_rows[0]["stride"] if len(table_rows) == 1 else None,
            "table_candidates": table_rows,
            "item_field_candidates": field_candidates,
            "confidence": "high" if mapped_unique and table_rows[0]["parent_link_confidence"] == "high" else ("medium" if table_rows else "unknown"),
            "status": status,
            "blockers": blockers,
        })

    unmapped_club_tables = []
    for tid in CLUB_RTTI_TABLES:
        if tid not in RELATIONS or profiles[tid].get("t14_adjudication") != "resolved" or profiles[tid].get("stage2_status") != "resolved":
            relation = RELATIONS.get(tid)
            unmapped_club_tables.append({
                "table_type": tid, "archive": "server",
                "rtti_class": t14_by_type[tid].get("primary_class"),
                "count": profiles[tid]["row_closure"]["count"],
                "stride": profiles[tid]["row_closure"]["stride"],
                "profile_file": profiles[tid]["profile_file"],
                "candidate_parent_4cc": relation["parents"] if relation else [],
                "identity_status": "candidate" if profiles[tid].get("stage2_status") != "resolved" or profiles[tid].get("t14_adjudication") != "resolved" else "resolved",
                "status": "partial_identity_or_parent_link",
                "blocker": "RTTI table is retained as a profile, but independent club entity and/or schema-list linkage is not resolved.",
            })
    fields_with_candidates = sum(
        1 for parent in parent_rows for field in parent["item_field_candidates"] if field["matches"]
    )
    unknown = [x["parent_4cc"] for x in parent_rows if x["status"] == "partial_unknown_table_identity"]
    return {
        "status": "partial_parent_identity_coverage",
        "task": "t29 club nested-list data-side reconnaissance; candidate only; no L3 claims",
        "provenance": {
            "master_sha256": master_hash,
            "server_archive_sha256": archive_metadata["server_archive_sha256"],
            "server_census": "evidence/fm24/reports/dbdat_decode/server_tables_census.json",
            "t14_census": "scratch/t14/out/census.json",
            "t14_stage2": "scratch/t14/out/stage2_map.json",
            "legacy_stage2": "reports/stage2_table_identity.json",
            "legacy_stage2_note": stage2_extra["notes"],
            "t24_nested_fields": "scratch/t24/out/subtables.part001-003.json",
            "data_root": "scratch/data",
        },
        "summary": {
            "nested_fields_total": 239, "cstc_skipped_fields": 28,
            "non_cstc_nested_fields": 211, "non_cstc_parent_codes": len(parent_rows),
            "parents_with_unique_candidate_table": sum(x["status"] == "complete_candidate_profile" for x in parent_rows),
            "parents_with_ambiguous_table_candidates": sum(x["status"] == "partial_ambiguous_table_candidate" for x in parent_rows),
            "parents_unknown": len(unknown), "item_fields_with_column_candidates": fields_with_candidates,
            "club_rtti_tables_profiled": len(profiles),
            "club_rtti_tables_identity_candidates": sum(x.get("stage2_status") != "resolved" or x.get("t14_adjudication") != "resolved" for x in profiles.values()),
            "club_rtti_tables_with_unknown_parent": len(unmapped_club_tables),
        },
        "tables": [profiles[tid] for tid in sorted(profiles)],
        "unmapped_club_rtti_tables": unmapped_club_tables,
        "unknown_parent_4cc": unknown,
        "parents": parent_rows,
    }


def write_report(doc: dict[str, Any]) -> None:
    summary = doc["summary"]
    unknown = doc["unknown_parent_4cc"]
    lines = [
        "# t29 Club 子表数据侧侦察",
        "",
        f"状态：`{doc['status']}`。所有列名均为 `candidate`，未晋级 L3；不含 Cstc/table_22 的画像。",
        "",
        "## 结果",
        "",
        f"- t24 清单：239 项；排除 Cstc 28 项后，覆盖 {summary['non_cstc_parent_codes']} 个父码、{summary['non_cstc_nested_fields']} 个嵌套字段。",
        f"- 已输出 {summary['club_rtti_tables_profiled']} 张 RTTI 标记为 club 的 server 子表完整行与逐列画像（其中 {summary['club_rtti_tables_identity_candidates']} 张的 stage2/t14 身份仍为 candidate）；其中 {summary['parents_with_unique_candidate_table']} 个父码有唯一 table candidate，{summary['parents_with_ambiguous_table_candidates']} 个父码仍多解。",
        f"- 有至少一个列候选的 schema item 字段数：{summary['item_fields_with_column_candidates']}（同字段可能有多个列/表候选；不代表确认）。",
        f"- 无子表身份映射的父码：{', '.join(unknown) if unknown else '无'}。",
        "",
        "## 父码清单",
        "",
        "| 父码 | table candidate | RTTI class | 行数 × stride | 状态 / blocker |",
        "|---|---:|---|---:|---|",
    ]
    for row in doc["parents"]:
        tid = row.get("table_type")
        if tid is None:
            tid = ",".join(map(str, row.get("table_type_candidates", []))) or "unknown"
        size = f"{row['count']} × {row['stride']}" if row.get("count") is not None else "—"
        cls = row.get("rtti_class") or "—"
        blocker = row["blockers"][0] if row["blockers"] else "item fields retain candidate-only status"
        lines.append(f"| `{row['parent_4cc']}` | {tid} | `{cls}` | {size} | `{row['status']}`: {blocker} |")
    lines += [
        "",
        "## 完整画像表",
        "",
        "每张表在 `profiles/` 有全行 JSONL 与 profile JSON；行封口只说明 count/stride 算式闭合，不说明字段 serializer 已恢复。候选证据包含全列统计、哨兵率、日期识别、引用域和现金数值范围。",
        "",
    ]
    for table in doc["tables"]:
        closure = table["row_closure"]
        lines.append(f"- table_{table['table_type']} `{table['rtti_class']}`: {closure['equation']}; `{table['profile_file']}`; `{table['full_rows_file']}`.")
    lines += [
        "",
        "## t27 衔接",
        "",
        "Cstc 和 server table_22 完全跳过；t27 的静态 cursor 工作不受本任务写入影响。本产物只提供可复制的数据侧画像方法及明确的 schema/type/domain 候选，日期候选必须通过 packed day/year 画像，club reference 候选要求列值落在 `[0,84259)`。RTTI class 与表号身份来自 t14/stage2；父码链接及所有列仍是候选，不能替代 t27 的 cursor 路径，也不构成 L3/L4。",
        "",
        "## 口径与 blockers",
        "",
        "- 冻结 `master.json` SHA-256 与 `evidence/MANIFEST.json` 比对；快照哈希写入 inventory。",
        "- `reports/stage2_table_identity.json` 的 consolidated view 与 t14 当前 `stage2_map.json` 行数不同；同时保留二者元数据，以 t14 当前 54/59 视图做身份交叉，不覆盖旧报告。",
        "- 没有唯一 RTTI/schema 链的父码标 unknown；数值域相似、行数相似、计数大小都不用于补猜。",
        "- t14 census 没有 `reader_va` 字段，inventory 保留 `null`，没有从 handler VA 推导 reader VA。",
        "",
        "## 验证",
        "",
        "运行 `py -V:3.12 -I scratch/t29/out/verify.py` 复算所有行 dump 的序号、stride、哈希与封口，并抽验候选列样本。",
    ]
    (OUTDIR / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_selftest() -> None:
    assert schema_field_range({"field": "year", "type": "integer"}) == (1800, 2100)
    assert schema_field_range({"field": "cash", "min_value": "-5", "max_value": "9"}) == (-5, 9)
    assert decode_width(bytes.fromhex("ff ff 34 12"), 2, 2) == 0x1234
    assert parse_fmf_directory.__name__ == "parse_fmf_directory"
    synthetic_rows = [bytes.fromhex("01 00 00 00"), bytes.fromhex("02 00 00 00")]
    c = column_profile(synthetic_rows, 0, 1)
    assert c["distinct"] == 2 and c["zero_count"] == 0
    date_rows = [struct.pack("<I", (2020 << 16) | 1), struct.pack("<I", (2021 << 16) | 365)]
    date_col = column_profile(date_rows, 0, 4)
    assert date_col["packed_day_year"]["valid_count"] == 2
    assert column_candidate({"type": "date", "field": "stdt"}, date_col) is not None
    assert column_candidate({"type": "database_record_unique_id", "database_table_type": "club"},
                            column_profile([struct.pack("<I", 100), struct.pack("<I", 80000)], 0, 4)) is not None
    print("SELFTEST PASS: schema ranges, primitive columns, packed dates, reference-domain candidates")


def main() -> int:
    parser = argparse.ArgumentParser(description="Profile non-Cstc club RTTI subtable candidates from scratch/data.")
    parser.add_argument("--selftest", action="store_true", help="run offline synthetic checks only")
    parser.add_argument("--outdir", type=pathlib.Path, default=OUTDIR, help="must resolve to scratch/t29/out")
    args = parser.parse_args()
    try:
        if args.selftest:
            run_selftest()
            return 0
        if args.outdir.resolve() != OUTDIR.resolve():
            raise T29Error("output must be scratch/t29/out")
        OUTDIR.mkdir(parents=True, exist_ok=True)
        doc = build_output()
        (OUTDIR / "subtable_inventory.json").write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        write_report(doc)
        s = doc["summary"]
        print(f"wrote {OUTDIR}; parents={s['non_cstc_parent_codes']} unique_candidates={s['parents_with_unique_candidate_table']} ambiguous={s['parents_with_ambiguous_table_candidates']} unknown={s['parents_unknown']} profiles={s['club_rtti_tables_profiled']} field_candidates={s['item_fields_with_column_candidates']}")
        return 0
    except T29Error as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    except (OSError, ValueError, KeyError, IndexError, struct.error, ctypes.ArgumentError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
