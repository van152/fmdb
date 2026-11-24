#!/usr/bin/env python3
"""t33 batch II: data-side profiles for 7 uncovered STARTING_* server subtables.

Scope (fixed by the task brief):
  * read-only: scratch/data archive copy + in-repo frozen evidence
  * output: scratch/t33/out only
  * no static cursor work, no L3 promotion, no reader_va inference
  * every column claim stays `candidate` / L2

Row boundaries
  * fixed tables   : 14 + n*stride + 8 (also tests 13 + n*stride + 9)
  * variable tables: tail-13 frame  ordinal(u32) | id(u32) | id(u32) | marker(u8)
                     walked forward with strict ordinal arity; exact footer closure

Usage
  py -V:3.12 -I -B scripts/t33_profile_batch.py --help
  py -V:3.12 -I -B scripts/t33_profile_batch.py --selftest
  FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data \
    py -V:3.12 -I -B scripts/t33_profile_batch.py [--only 58,39]
Exit codes 0 ok / 1 check failed / 2 usage or fatal
"""
from __future__ import annotations
import sys as _cfg_sys
from pathlib import Path as _cfg_pathlib
_cfg_sys.path.insert(0, str(_cfg_pathlib(__file__).resolve().parent))
import fm24_config as _cfg

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
OUTDIR = ROOT / "scratch/t33/out"
DBDIR = pathlib.Path(os.environ.get("FM24_DB_DIR", ROOT / "scratch/data")).resolve()
MASTER = ROOT / "evidence/fm24/reports/editor_schema/master.json"
MANIFEST = ROOT / "evidence/MANIFEST.json"
SERVER_CENSUS = ROOT / "evidence/fm24/reports/dbdat_decode/server_tables_census.json"
DAT_HEADERS = ROOT / "evidence/fm24/reports/dbdat_decode/dat_headers.json"
T14_CENSUS = ROOT / "scratch/t14/out/census.json"
STAGE2_MAP = ROOT / "scratch/t14/out/stage2_map.json"
T29_INVENTORY = ROOT / "scratch/t29/out/subtable_inventory.json"

# table -> (label, candidate parents). Parents are schema list 4CC codes.
TABLES: dict[int, dict[str, Any]] = {
    58: {"label": "STARTING_WEEKLY_WAGE_CONTRIBUTION", "parents": ["Cwcl"],
         "rejected": {}},
    39: {"label": "STARTING_AVERAGE_POINTS", "parents": ["csap"],
         "rejected": {"CPsL": "CPsL is club.Player Partnerships (2 person fields); table 39 "
                              "is RTTI-tagged team and its row carries a team-domain id, so a "
                              "player-pair list cannot be the item type"}},
    12: {"label": "STARTING_AWARD_HISTORY", "parents": ["AWsh"],
         "rejected": {"Cafl": "Cafl is club.Current Affiliations (club ref + booleans + fees); "
                              "table 12 is RTTI-tagged awar and its rows carry award-history "
                              "strings/positions",
                      "Calt": "Calt is club.Alternative Stadiums (competition+stadium refs+dates); "
                              "no stadium-domain column exists in table 12"}},
    45: {"label": "STARTING_RECORD", "parents": ["Plhs", "Pnph", "Pacl"], "rejected": {}},
    48: {"label": "STARTING_RECORD", "parents": ["Plhs", "Pnph", "Pacl"], "rejected": {}},
    59: {"label": "STARTING_MEDIA_EXPECTATIONS", "parents": ["Csme"], "rejected": {}},
    73: {"label": "STARTING_ITALIAN_SERIE_A_NON_EU_PLAYER_SIGNED_FOR_RESTRICTED_SLOT",
         "parents": [], "rejected": {}},
}

# reference id domains (same table used by t29; diagnostics only, never identity)
REFERENCE_DOMAINS = {
    "club": 84259,
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

ZSTD_MAGIC = bytes.fromhex("28b52ffd")
TAD_MAGIC = bytes.fromhex("03017461642ef10d")
TAIL13 = 13
MARKERS = (0x00, 0x0C)


class T33Error(Exception):
    pass


# ---------------------------------------------------------------- utilities
def load_json(path: pathlib.Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def manifest_hash(path: pathlib.Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    manifest = load_json(MANIFEST)
    row = next((item for item in manifest["files"] if item["path"] == rel), None)
    if row is None:
        raise T33Error(f"manifest has no entry for {rel}")
    actual = sha256(path.read_bytes())
    if actual != row["sha256"]:
        raise T33Error(f"snapshot SHA-256 mismatch for {rel}: {actual}")
    return actual


_ZSTD: Any = None


def load_zstd() -> Any:
    configured = os.environ.get("FM24_ZSTD_DLL")
    cands = [pathlib.Path(configured)] if configured else []
    cands += [pathlib.Path(str(_cfg.MINGW_ZSTD_DLL))]
    dll = next((p for p in cands if p.is_file()), None)
    if dll is None:
        raise T33Error("libzstd.dll not found; set FM24_ZSTD_DLL")
    lib = ctypes.CDLL(str(dll))
    lib.ZSTD_decompress.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_void_p, ctypes.c_size_t]
    lib.ZSTD_decompress.restype = ctypes.c_size_t
    lib.ZSTD_isError.argtypes = [ctypes.c_size_t]
    lib.ZSTD_isError.restype = ctypes.c_uint
    lib.ZSTD_getErrorName.argtypes = [ctypes.c_size_t]
    lib.ZSTD_getErrorName.restype = ctypes.c_char_p
    return lib


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
                raise T33Error(f"zstd output {got} exceeds expected {expected_size}")
            return dst.raw[:got]
        name = _ZSTD.ZSTD_getErrorName(got).decode("ascii", errors="replace")
        if "Destination buffer is too small" not in name and "dstSize_tooSmall" not in name:
            raise T33Error(f"zstd decompression failed: {name}")
        capacity *= 2
        if capacity > 512 * 1024 * 1024:
            raise T33Error("zstd output exceeds 512 MiB safety cap")


def parse_fmf_directory(blob: bytes, label: str) -> tuple[int, dict[str, dict[str, int]]]:
    if len(blob) < 34 or blob[:8] != bytes.fromhex("03 01 74 61 64 2e f1 0d"):
        raise T33Error(f"{label}: tad. v3569 header missing")
    toc_off = struct.unpack_from("<I", blob, 17)[0] + 17
    if toc_off + 9 >= len(blob) or blob[toc_off:toc_off + 6] != b"\x02\x01fmf.":
        raise T33Error(f"{label}: FMF TOC not found at {toc_off}")
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
        pos += 24 + 16
        entries[f"{root}/{name}{ext}"] = {"offset": offset, "packed_size": packed, "size": size}
    return 34, entries


def load_server_tables(table_ids: list[int]) -> tuple[dict[int, bytes], dict[int, dict[str, Any]], dict[str, Any]]:
    """Resolve + decompress the requested server members from the read-only copy."""
    allowed = (ROOT / "scratch/data").resolve()
    if DBDIR != allowed:
        raise T33Error(f"FM24_DB_DIR must be exactly {allowed}; got {DBDIR}")
    header = next((h for h in load_json(DAT_HEADERS) if h.get("file") == "server_db.dat"), None)
    if header is None:
        raise T33Error("dat_headers.json has no server_db.dat row")
    archive = (DBDIR / "server_db.dat").read_bytes()
    if len(archive) != header.get("size") or sha256(archive) != header.get("sha256"):
        raise T33Error("scratch/data/server_db.dat differs from frozen dat_headers.json")
    data_base, directory = parse_fmf_directory(archive, "server_db.dat")
    census = {item["path"]: item for item in load_json(SERVER_CENSUS).get("entries", [])}
    payloads: dict[int, bytes] = {}
    meta: dict[int, dict[str, Any]] = {}
    notes: dict[str, Any] = {"server_archive_sha256": header["sha256"], "e66_frame_scan": {}}
    for tid in table_ids:
        path = f"server_db/table_{tid}.dat"
        toc_item, cen = directory.get(path), census.get(path)
        if toc_item is None or cen is None:
            raise T33Error(f"server table {tid} absent from FMF directory/census")
        start = data_base + toc_item["offset"]
        end = start + toc_item["packed_size"]
        if end > len(archive):
            raise T33Error(f"table {tid} packed member exceeds archive")
        member = archive[start:end]
        expect = toc_item["size"]
        # E66 caveat: a member may open with an empty zstd stub frame. Walk the
        # magic candidates and pick the first frame whose output matches the
        # frozen census payload size (never "first magic wins").
        candidates = []
        search = 0
        while True:
            rel = member.find(ZSTD_MAGIC, search)
            if rel < 0 or len(candidates) > 8:
                break
            candidates.append(rel)
            search = rel + 4
        chosen = None
        for rel in candidates:
            try:
                raw = zstd_decompress(member[rel:], expect)
            except T33Error:
                continue
            if len(raw) == cen["payload_size"] and sha256(raw) == cen["payload_sha256"]:
                chosen = (rel, raw)
                break
        if chosen is None:
            raise T33Error(f"table {tid}: no frame reproduces the frozen census payload")
        rel, raw = chosen
        if rel != candidates[0]:
            notes["e66_frame_scan"][str(tid)] = {
                "first_magic_offset": candidates[0], "used_magic_offset": rel,
                "decompressed_size": len(raw),
            }
        payloads[tid] = raw
        meta[tid] = {
            "archive": "server", "member": path, "packed_offset": start + rel,
            "packed_size": toc_item["packed_size"], "payload_size": len(raw),
            "payload_sha256": sha256(raw),
            "census_row_boundary": cen.get("row_boundary"),
            "census_row_model": cen.get("row_model"),
        }
    return payloads, meta, notes


# --------------------------------------------------------------- row decode
def decode_fixed(raw: bytes, count_hint: int | None = None) -> dict[str, Any]:
    """Try the two payload conventions and require exact closure + tail identity."""
    if raw[:8] != TAD_MAGIC:
        raise T33Error("TAD payload header invalid")
    count = struct.unpack_from("<I", raw, 8)[0]
    if count_hint is not None and count != count_hint:
        raise T33Error(f"header count {count} != census count {count_hint}")
    tried = []
    for header, footer in ((14, 8), (13, 9)):
        body_len = len(raw) - header - footer
        if body_len <= 0:
            continue
        for stride in range(1, 400):
            if count * stride != body_len:
                continue
            body = raw[header:header + body_len]
            rows = [body[i * stride:(i + 1) * stride] for i in range(count)]
            ident = identity_score(rows, tail13=False)
            tried.append({"header": header, "footer": footer, "stride": stride,
                          "equation": f"{header} + {count} * {stride} + {footer} = {len(raw)}",
                          "rdui_tail_hits": ident["tail13_hits"],
                          "id_pair_hits": ident["id_pair_hits"]})
            if ident["tail13_hits"] == count:
                return {"model": "fixed", "count": count, "stride": stride,
                        "row_start": header, "footer_bytes": footer, "rows": rows,
                        "equation": tried[-1]["equation"], "identity": ident,
                        "conventions_tried": tried}
    if not tried:
        raise T33Error(f"no fixed stride closes {len(raw)} bytes for count {count}")
    best = max(tried, key=lambda x: x["rdui_tail_hits"])
    raise T33Error(f"fixed stride closes arithmetically but fails tail identity: {best}")


def identity_score(rows: list[bytes], tail13: bool = True) -> dict[str, Any]:
    tail_hits = pair_hits = 0
    for i, row in enumerate(rows):
        if len(row) < 13:
            continue
        o, a, b = struct.unpack_from("<III", row, len(row) - 13)
        if o == i and row[len(row) - 1] in MARKERS:
            tail_hits += 1
        if a == b:
            pair_hits += 1
    return {"tail13_hits": tail_hits, "id_pair_hits": pair_hits,
            "rows": len(rows), "grammar": "ordinal|id|id|marker at row_end-13"}


def walk_variable(body: bytes, count: int, max_span: int = 2048) -> dict[str, Any]:
    """Strict forward walk of the tail-13 frame; returns rows and closure.

    The first length that satisfies the frame is taken; how often more than one
    length would have satisfied it is reported as frame_ambiguity so the caller
    can see the residual risk instead of it being hidden.
    """
    pos, rows, span = 0, [], []
    ambiguous_rows = 0
    max_candidates = 1
    for i in range(count):
        hit = None
        extra = 0
        for length in range(13, min(max_span, len(body) - pos) + 1):
            t = pos + length - 13
            if t < pos:
                continue
            if t + 13 > len(body):
                break
            o, a, b = struct.unpack_from("<III", body, t)
            if o == i and a == b and body[t + 12] in MARKERS:
                if hit is None:
                    hit = length
                else:
                    extra += 1
                    if extra > 3:
                        break
        if hit is None:
            raise T33Error(f"variable walk stuck at row {i}, pos {pos}")
        if extra:
            ambiguous_rows += 1
            max_candidates = max(max_candidates, extra + 1)
        rows.append(body[pos:pos + hit])
        span.append(hit)
        pos += hit
    if pos != len(body):
        raise T33Error(f"variable walk closed {pos} != body {len(body)}")
    markers = collections.Counter(row[-1] for row in rows)
    return {"model": "variable", "count": count, "stride": None,
            "row_start": 14, "footer_bytes": 8, "rows": rows,
            "equation": (f"14 + sum(row_lens={sum(span)}) + 8 = {len(body) + 22}"),
            "identity": {"grammar": "ordinal|id|id|marker at row_end-13",
                         "tail13_hits": count, "id_pair_hits": count},
            "row_len": {"min": min(span), "max": max(span),
                        "mean": round(sum(span) / count, 3),
                        "distinct": len(set(span))},
            "frame_ambiguity": {"rows_with_multiple_valid_lengths": ambiguous_rows,
                                "max_candidate_lengths": max_candidates,
                                "rule": "first (shortest) valid frame length is used"},
            "marker_counts": {f"0x{k:02X}": v for k, v in sorted(markers.items())}}


# ------------------------------------------------------------ column profile
def _w(row: bytes, off: int, width: int, from_end: bool) -> int | None:
    p = (len(row) - off) if from_end else off
    if from_end:
        p = len(row) - off
        if p < 0 or p + width > len(row):
            return None
    else:
        if p + width > len(row):
            return None
    return int.from_bytes(row[p:p + width], "little", signed=False)


def column_profile(rows: list[bytes], off: int, width: int, from_end: bool = False) -> dict[str, Any]:
    top: collections.Counter[int] = collections.Counter()
    distinct: set[int] = set()
    mn = mx = None
    zero = sentinel = covered = 0
    domain_hits = collections.Counter()
    date_valid = date_live = date_blank = 0
    date_years: set[int] = set()
    date_days: list[int] = []
    smin = smax = None
    signed_good = signed_live = 0
    sentinel_value = (1 << (width * 8)) - 1
    for row in rows:
        v = _w(row, off, width, from_end)
        if v is None:
            continue
        covered += 1
        top[v] += 1
        distinct.add(v)
        mn = v if mn is None or v < mn else mn
        mx = v if mx is None or v > mx else mx
        zero += v == 0
        sentinel += v == sentinel_value
        if width == 4:
            if v != 0xFFFFFFFF:
                for entity, limit in REFERENCE_DOMAINS.items():
                    domain_hits[entity] += v < limit
                if v != 0:
                    signed_live += 1
                sv = v if v < 0x80000000 else v - 0x100000000
                smin = sv if smin is None or sv < smin else smin
                smax = sv if smax is None or sv > smax else smax
                signed_good += -1_000_000_000 <= sv <= 1_000_000_000
            low, year = v & 0xFFFF, (v >> 16) & 0xFFFF
            if v in (0, 0xFFFFFFFF) or year in (0, 0xFFFF):
                date_blank += 1
            else:
                date_live += 1
                if 1900 <= year <= 2035 and low <= 366:
                    date_valid += 1
                    date_years.add(year)
                    date_days.append(low)
    n = len(rows)
    out: dict[str, Any] = {
        "offset": (-off if from_end else off), "width": width,
        "interpretation": f"u{width * 8}",
        "offset_frame": "row_end" if from_end else "row_start",
        "count": covered, "coverage": round(covered / n, 6) if n else 0,
        "distinct": len(distinct), "min_unsigned": mn, "max_unsigned": mx,
        "zero_count": zero, "zero_rate": round(zero / covered, 6) if covered else 0,
        "sentinel_value": f"0x{sentinel_value:0{width * 2}X}",
        "sentinel_count": sentinel,
        "sentinel_rate": round(sentinel / covered, 6) if covered else 0,
        "top_values": [{"value": k, "count": v} for k, v in top.most_common(12)],
        "small_value_set": sorted(distinct) if len(distinct) <= 64 else None,
    }
    if width == 4:
        out["signed_i32"] = {"min": smin, "max": smax,
                             "within_abs_1e9_count": signed_good,
                             "within_abs_1e9_rate_nonzero_nonnull":
                                 round(signed_good / max(1, signed_live), 6)}
        out["reference_domains"] = {
            key: {"in_range_count": value, "denominator_nonnull": covered - sentinel,
                  "ratio": round(value / max(1, covered - sentinel), 6)}
            for key, value in domain_hits.items()}
        out["packed_day_year"] = {
            "nonblank_count": date_live, "valid_count": date_valid,
            "valid_ratio_nonblank": round(date_valid / max(1, date_live), 6),
            "year_min": min(date_years) if date_years else None,
            "year_max": max(date_years) if date_years else None,
            "year_distinct": len(date_years),
            "day_max": max(date_days) if date_days else None,
            "rule": ("u32 low16=day_or_ordinal<=366, high16=year 1900..2035; "
                     "0/0xffffffff/year=0xffff treated as blank"),
        }
    return out


def float_profile(rows: list[bytes], off: int) -> dict[str, Any]:
    vals, finite = [], 0
    mn = mx = None
    for row in rows:
        if off + 4 > len(row):
            continue
        v = struct.unpack_from("<f", row, off)[0]
        if math.isfinite(v):
            finite += 1
            mn = v if mn is None or v < mn else mn
            mx = v if mx is None or v > mx else mx
            if len(vals) < 12:
                vals.append(round(v, 6))
    return {"offset": off, "width": 4, "count": len(rows), "finite_count": finite,
            "finite_ratio": round(finite / max(1, len(rows)), 6),
            "min_finite": mn, "max_finite": mx, "first_finite_samples": vals}


def structural_notes(decode: dict[str, Any]) -> dict[str, Any]:
    """Cheap row-body structure diagnostics for variable-length tables.

    Only reports what is directly observable: where a u32 length prefix is
    followed by exactly that many printable ASCII bytes, and the leading u32.
    Nothing here is a field name.
    """
    rows = decode["rows"]
    if decode["stride"] is not None:
        return {}
    prefix = collections.Counter()
    str_at = collections.Counter()
    str_lens: list[int] = []
    sample_names: list[str] = []
    for row in rows:
        if len(row) >= 4:
            prefix[struct.unpack_from("<I", row, 0)[0] & 0xFF] += 1
        found = False
        for p in range(4, min(len(row) - 5, 64)):
            n = struct.unpack_from("<I", row, p)[0]
            if not 1 <= n <= 40 or p + 4 + n > len(row):
                continue
            chunk = row[p + 4:p + 4 + n]
            if all(0x20 <= b < 0x7F for b in chunk):
                str_at[p] += 1
                str_lens.append(n)
                if len(sample_names) < 6:
                    sample_names.append(chunk.decode("ascii"))
                found = True
                break
        if not found:
            str_at[None] += 1
    n_rows = len(rows)
    best = str_at.most_common(3)
    return {
        "rows_with_length_prefixed_ascii": n_rows - str_at[None],
        "rows_without": str_at[None],
        "length_prefix_offsets_top": [{"offset": k, "count": v}
                                      for k, v in best if k is not None],
        "string_len_min": min(str_lens) if str_lens else None,
        "string_len_max": max(str_lens) if str_lens else None,
        "sample_ascii": sample_names,
        "leading_u32_low_byte_top": [{"low_byte": k, "count": v}
                                     for k, v in prefix.most_common(6)],
        "caveat": ("length-prefixed ASCII presence is a layout observation, not a "
                   "schema field; no item field is named from it"),
    }


def profile_columns(decode: dict[str, Any]) -> dict[str, Any]:
    rows = decode["rows"]
    stride = decode.get("stride")
    out: dict[str, Any] = {"row_start": [], "row_end": []}
    if stride:
        for width in (1, 2, 4, 8):
            for off in range(0, stride - width + 1):
                col = column_profile(rows, off, width)
                if width == 4:
                    col["float32"] = float_profile(rows, off)
                out["row_start"].append(col)
        return out
    min_len = min(len(r) for r in rows)
    for width in (1, 2, 4, 8):
        for off in range(0, max(1, min_len - width + 1)):
            col = column_profile(rows, off, width)
            if width == 4:
                col["float32"] = float_profile(rows, off)
            out["row_start"].append(col)
    for off in range(1, min_len + 1):
        for width in (1, 2, 4):
            if width > 1 and off < width:
                continue
            out["row_end"].append(column_profile(rows, off, width, from_end=True))
    return out


# ------------------------------------------------------- schema/item mapping
def schema_list_nodes() -> dict[str, list[dict[str, Any]]]:
    """code -> list of {entity_file, entity_id, node} for every list node."""
    master = load_json(MASTER)
    found: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)

    def walk(fields: list[dict[str, Any]], entity_file: str, entity_id: str) -> None:
        for f in fields:
            if f.get("type") == "list" and isinstance(f.get("field"), str):
                found[f["field"]].append({"entity_file": entity_file, "entity_id": entity_id,
                                          "node": f})
            if f.get("list_item_fields"):
                walk(f["list_item_fields"], entity_file, entity_id)

    for entity_file, ents in master.get("entities", {}).items():
        for ent in ents:
            walk(ent.get("fields", []), entity_file, str(ent.get("id")))
    return dict(found)


def schema_range(field: dict[str, Any]) -> tuple[int | None, int | None]:
    def as_int(x: Any) -> int | None:
        try:
            return int(str(x)) if x is not None else None
        except ValueError:
            return None

    lo, hi = as_int(field.get("min_value")), as_int(field.get("max_value"))
    code = str(field.get("field", "")).lower()
    if lo is None and hi is None and code in {"year", "styr", "edyr", "enyr", "expi", "ahye"}:
        return 1800, 2100
    return lo, hi


def is_frame_column(col: dict[str, Any]) -> bool:
    """True for the walker's own tail-13 identity frame or an all-zero column.

    Those bytes are boundary machinery, not item payload; letting them match a
    schema field would manufacture evidence.
    """
    if col["offset_frame"] == "row_end" and 1 <= abs(col["offset"]) <= TAIL13:
        return True
    return col["distinct"] <= 1


def column_fit(field: dict[str, Any], col: dict[str, Any]) -> tuple[float, str] | None:
    """Conservative type/domain filter copied in spirit from t29 (candidate only)."""
    typ, width, n = field.get("type"), col["width"], col["count"]
    nulls = col["sentinel_count"]
    live = n - nulls
    if is_frame_column(col):
        return None
    if typ == "date":
        if width != 4:
            return None
        packed = col["packed_day_year"]
        if packed["nonblank_count"] < max(2, int(n * 0.05)) or packed["valid_ratio_nonblank"] < 0.95:
            return None
        return packed["valid_ratio_nonblank"], "packed day/year profile matches date semantics"
    if typ == "database_record_unique_id":
        limit = REFERENCE_DOMAINS.get(str(field.get("database_table_type")))
        if width != 4 or limit is None or live < max(2, int(n * 0.05)):
            return None
        # An identifier column must actually vary across rows: ids are per-row
        # values, not a handful of small ordinals that merely sit under the limit.
        if col["distinct"] < max(4, int(n * 0.5)):
            return None
        if col["max_unsigned"] < 32:
            return None
        ratio = col["reference_domains"][str(field.get("database_table_type"))]["ratio"]
        if ratio < 0.98:
            return None
        return ratio, (f"{field.get('database_table_type')} ID-domain compatibility "
                       f"[0,{limit}); domain fit is not field identity")
    if typ == "boolean":
        if width not in (1, 2, 4) or col["distinct"] > 2:
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
        lo, hi = schema_range(field)
        lo = -1_000_000_000 if lo is None else lo
        hi = 1_000_000_000 if hi is None else hi
        info = col["signed_i32"]
        if info["min"] is None or info["max"] is None:
            return None
        if lo <= info["min"] and info["max"] <= hi:
            return 1.0, f"all values inside schema cash range [{lo},{hi}]"
        # full-column min/max already failed: demand the whole column still fit.
        return None
    if typ == "real":
        if width != 4:
            return None
        fp = col.get("float32", {})
        if fp.get("finite_ratio", 0) < 0.98 or fp.get("min_finite") is None:
            return None
        return fp["finite_ratio"], "finite float32 reinterpretation; semantic anchor still required"
    if typ == "enum":
        if width not in (1, 2, 4) or col["distinct"] > 64 or col["small_value_set"] is None:
            return None
        max_enum = 255 if width == 1 else 4095 if width == 2 else 65535
        if not col["small_value_set"] or max(col["small_value_set"]) > max_enum:
            return None
        if len(col["small_value_set"]) > 1 and col["sentinel_rate"] > 0.95:
            return None
        return 1.0 - col["sentinel_rate"], "small finite value set compatible with enum storage"
    if typ == "integer":
        if width not in (1, 2, 4):
            return None
        lo, hi = schema_range(field)
        if lo is None and hi is None:
            return None
        valid = 0
        for item in col["top_values"]:
            v = item["value"]
            sv = v if v < (1 << (width * 8 - 1)) else v - (1 << (width * 8))
            if any((lo is None or x >= lo) and (hi is None or x <= hi) for x in (v, sv)):
                valid += item["count"]
        ratio = valid / max(1, n)
        if ratio < 0.95:
            return None
        # A bound like 0..127 is satisfied by hundreds of byte offsets; only
        # keep it when the column really uses a range, not two flag values.
        if col["distinct"] <= 2 and lo is not None and hi is not None and (hi - lo) > 64:
            return None
        if col["distinct"] > 64 and col["distinct"] > n * 0.9:
            return None
        return ratio, f"numeric range compatible with schema [{lo},{hi}]"
    return None


def item_field_candidates(node: dict[str, Any], columns: dict[str, Any],
                          min_coverage: float) -> list[dict[str, Any]]:
    fields = node.get("list_item_fields") or []
    pool = [c for c in columns["row_start"] if c["coverage"] >= min_coverage]
    pool += [c for c in columns["row_end"] if c["coverage"] >= min_coverage]
    out = []
    for field in fields:
        matches = []
        for col in pool:
            fit = column_fit(field, col)
            if fit is None:
                continue
            score, reason = fit
            matches.append({
                "column": f"{col['interpretation']}@{col['offset_frame']}"
                          f"{col['offset']:+d}",
                "offset": col["offset"], "offset_frame": col["offset_frame"],
                "width": col["width"], "fit_score": round(score, 6),
                "coverage": col["coverage"], "distinct": col["distinct"],
                "basis": reason,
                "evidence_level": "L2_candidate", "claim_status": "candidate",
            })
        matches.sort(key=lambda x: (-x["fit_score"], -x["distinct"], -x["coverage"],
                                    x["offset_frame"], x["offset"]))
        out.append({
            "field": field.get("field"), "name": field.get("name"),
            "schema_type": field.get("type"),
            "database_table_type": field.get("database_table_type"),
            "claim_status": "candidate" if matches else "no_column_candidate",
            "matches_considered": len(matches), "matches": matches[:6],
            "ambiguous": len(matches) > 8,
            "blocker": None if matches else
            "no column passing the conservative type/domain filter",
        })
    return out


# ---------------------------------------------------------------- profiling
def build_table_profile(tid: int, raw: bytes, meta: dict[str, Any], node_map: dict[str, list],
                        ident: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    count_hint = (meta.get("census_row_boundary") or {}).get("count")
    model = (meta.get("census_row_model") or "").lower()
    decode = None
    if model == "fixed_stride":
        try:
            decode = decode_fixed(raw, count_hint)
        except T33Error as exc:
            ident.setdefault("decode_notes", []).append(f"fixed decode failed: {exc}")
    if decode is None:
        if raw[:8] != TAD_MAGIC:
            raise T33Error(f"table {tid}: TAD header invalid")
        count = struct.unpack_from("<I", raw, 8)[0]
        body = raw[14:len(raw) - 8]
        decode = walk_variable(body, count)
    rows = decode["rows"]
    columns = profile_columns(decode)
    profiles_dir = OUTDIR / "profiles"
    profiles_dir.mkdir(parents=True, exist_ok=True)
    rows_rel = f"profiles/table_server_{tid}.rows.jsonl"
    rows_path = OUTDIR / rows_rel
    with rows_path.open("w", encoding="ascii", newline="\n") as stream:
        base = decode["row_start"]
        cursor = 0
        for i, row in enumerate(rows):
            stream.write(json.dumps({"row": i, "offset": base + cursor, "len": len(row),
                                     "raw_hex": row.hex()}, separators=(",", ":")) + "\n")
            cursor += len(row)
    closure = {
        "status": "complete_arithmetic_closure_L1",
        "model": decode["model"], "count": decode["count"], "stride": decode["stride"],
        "row_start": decode["row_start"], "footer_bytes": decode["footer_bytes"],
        "row_end_exclusive": decode["row_start"] + sum(len(r) for r in rows),
        "payload_bytes": len(raw),
        "equation": decode["equation"],
        "rows_sha256": sha256(b"".join(rows)),
        "conventions_tried": decode.get("conventions_tried"),
        "identity": decode["identity"],
        "row_len": decode.get("row_len"), "marker_counts": decode.get("marker_counts"),
        "frame_ambiguity": decode.get("frame_ambiguity"),
        "basis": ("payload size/count/stride closure plus per-row tail identity; "
                  "stride is arithmetic + framing evidence, not a schema serializer proof"),
    }
    t14 = ident["t14"].get(tid, {})
    s2 = ident["stage2"].get(tid, {})
    profile = {
        "status": "complete_data_profile",
        "table_type": tid, "archive": "server",
        "rtti_class": t14.get("primary_class") or TABLES[tid]["label"],
        "entity_tag": t14.get("entity_tag"),
        "t14_adjudication": t14.get("adjudication"),
        "stage2_status": s2.get("status"), "stage2_entity": s2.get("entity"),
        "identity_basis": {
            "t14_primary_class": t14.get("primary_class"),
            "t14_adjudication": t14.get("adjudication"),
            "t14_entity_tag": t14.get("entity_tag"),
            "handler_off": t14.get("handler_off"),
            "vtable_va": next((v.get("vtable_va") for v in t14.get("vtables", [])), None),
            "stage2_entity": s2.get("entity"), "stage2_status": s2.get("status"),
            "stage2_conflicts": s2.get("conflicts", []),
            "reader_va": None,
            "note": "identity from t14 RTTI census / stage2 map only; no reader_va inferred",
        },
        "payload": {k: meta[k] for k in ("archive", "member", "packed_offset", "packed_size",
                                         "payload_size", "payload_sha256")},
        "row_closure": closure,
        "full_rows_file": rows_rel,
        "full_rows_sha256": sha256(rows_path.read_bytes()),
        "profile_method": {
            "all_offsets": True, "primitive_widths": [1, 2, 4, 8],
            "offset_frames": ["row_start", "row_end"] if decode["stride"] is None else ["row_start"],
            "four_byte_metrics": ["u32 domain", "sentinel", "packed day/year",
                                  "signed i32/cash-range", "float32 reinterpretation"],
            "limits": "value domains are diagnostics; they never identify fields on their own",
        },
        "columns": columns,
        "structural_notes": structural_notes({
            "rows": rows, "stride": decode["stride"]}),
    }
    parent_map = {}
    min_cov = 1.0 if decode["stride"] else 0.9
    for code in TABLES[tid]["parents"]:
        for entry in node_map.get(code, []):
            parent_map[code] = {
                "entity_file": entry["entity_file"], "entity_id": entry["entity_id"],
                "schema_list_name": entry["node"].get("name"),
                "item_field_count": len(entry["node"].get("list_item_fields") or []),
                "item_field_candidates": item_field_candidates(entry["node"], columns, min_cov),
            }
            break
    profile["schema_parent_candidates"] = parent_map
    return profile, {"decode": decode}


def relationship_entries(tid: int, profile: dict[str, Any]) -> dict[str, Any]:
    """Honest parent<->table candidate judgement for this batch."""
    closure = profile["row_closure"]
    n, stride = closure["count"], closure["stride"]
    parents = []
    for code, info in profile["schema_parent_candidates"].items():
        matched = [f for f in info["item_field_candidates"] if f["matches"]]
        parents.append({
            "parent_4cc": code,
            "schema_path": f"{info['entity_file']}#{info['entity_id']}.{code}",
            "schema_list_name": info["schema_list_name"],
            "item_field_count": info["item_field_count"],
            "item_fields_with_column_candidate": len(matched),
            "item_fields": matched,
            "link_status": "candidate",
            "confidence": "candidate",
        })
    return {
        "table_type": tid, "archive": "server", "rtti_class": profile["rtti_class"],
        "entity_tag": profile["entity_tag"],
        "t14_adjudication": profile["t14_adjudication"],
        "stage2_status": profile["stage2_status"],
        "count": n, "stride": stride, "row_model": closure["model"],
        "parents": parents,
        "rejected_parents": [
            {"parent_4cc": code, "reason": reason, "claim_status": "rejected"}
            for code, reason in TABLES[tid].get("rejected", {}).items()],
        "profile_file": f"profiles/table_server_{tid}.profile.json",
        "confidence": ("candidate" if parents else "unknown"),
        "blockers": [
            "no reader/collection join was performed; RTTI class + data shape are not a join",
            "no L3/L4 evidence in this task (L4=0 by instruction)",
        ] + ([] if parents else [
            "no schema list node in the frozen master.json matches this class",
        ]),
    }


def attach_judgement(tid: int, profile: dict[str, Any], rel: dict[str, Any]) -> None:
    """Fill per-table confidence + blockers, keeping every uncertainty explicit."""
    table = profile["table_type"]
    n, stride = profile["row_closure"]["count"], profile["row_closure"]["stride"]
    budget = {
        58: dict(conf="candidate", parents=["Cwcl"],
                 why=("row framing (45 B, 8 rows) is consistent with a small per-club "
                      "contribution list, but two u32 pairs + u16 year + u32 value do not "
                      "reproduce the 5-field Cwcl item list; no reader join"),
                 blockers=["5-field item list (icom/play/club/wage/wend) is not reproducible "
                           "from the 45-byte row with a single admissible layout",
                           "only 8 rows: too few to separate sender/player/club id columns"]),
        39: dict(conf="unknown", parents=["csap"],
                 why=("entity team is resolved by RTTI+stage2, but the 42-byte row shows the "
                      "same u32 at +4 and +8 in all 117 rows and only 3 u16 value slots, "
                      "which does not line up with team+6 integer csap items"),
                 blockers=["constant u32 at +4/+8 in every row is unexplained",
                           "csap item needs 6 numeric slots; only 3 u16 slots admit the "
                           "integer filter",
                           "csap lives on comp.xml, table_39 entity is team: ownership "
                           "direction (comp->team vs team->comp) is unresolved"]),
        12: dict(conf="candidate", parents=["AWsh"],
                 why=("rows carry length-prefixed person-name strings plus u32 id pairs and "
                      "packed dates, matching an award-history item (AH1n/First Placed Name "
                      "etc.), but only a subset of the 26 AWsh items is reachable"),
                 blockers=["variable rows 31..203 B do not expose one fixed slot per AWsh item",
                           "no reader join from table 12 to award.AWsh collection"]),
        45: dict(conf="unknown", parents=["Plhs"],
                 why=("person names + packed dates + a repeated u32 pair appear in every row, "
                      "consistent with a per-person career record; entity pers is only the "
                      "stage2 adjudication (t14 keeps the entity tag null)"),
                 blockers=["t14 adjudication for table 45 is `candidate`, entity_tag null",
                           "three schema lists (Plhs/Pnph/Pacl) remain compatible",
                           "row body is variable (80..122 B) and contains an unexplained "
                           "person-name string copy"]),
        48: dict(conf="unknown", parents=["Plhs", "Pnph"],
                 why=("same RTTI class/handler/vtable as table 45, so the two tables are the "
                      "same C++ type; which schema list each one instantiates is undetermined"),
                 blockers=["identical RTTI identity to table 45 forbids a unique list claim",
                           "rows 79..130 B, u32 pairs + u16 year + person-name string",
                           "no reader join; entity resolution rests on the older stage2 note"]),
        59: dict(conf="candidate", parents=["Csme"],
                 why=("9,079 short rows (19..32 B) of small integers match the 2-field Csme "
                      "item (media source id + predicted finish <= 127)"),
                 blockers=["tail id pair in every row equals 0x01000000, not a plausible "
                           "media_source id; column semantics stay unresolved",
                           "row body length varies 19/22/25/32 so no single 2-field layout "
                           "holds for all rows"]),
        73: dict(conf="unknown", parents=[],
                 why=("single 23-byte row; u16 year 2023 and one u32 in the club id domain, "
                      "which fits the Italian non-EU slot event, but the frozen master.json "
                      "exposes no matching schema list and one row cannot support a column map"),
                 blockers=["no schema list node in the frozen master.json",
                           "count=1: every column statistic is degenerate",
                           "u32 at +0 (80,864,099) is outside the person reference domain"]),
    }[table]
    rel["confidence"] = budget["conf"]
    rel["confidence_basis"] = budget["why"]
    rel["blockers"] = budget["blockers"] + rel["blockers"]
    for parent in rel["parents"]:
        if parent["parent_4cc"] in budget["parents"]:
            parent["confidence"] = budget["conf"]
        else:
            parent["confidence"] = "unknown"
            parent["link_status"] = "rejected_for_this_table"
        parent["judged_confidence"] = parent["confidence"]


def write_progress(lines: list[str]) -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    path = OUTDIR / "PROGRESS.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(only: list[int] | None) -> int:
    table_ids = [t for t in sorted(TABLES) if not only or t in only]
    ident = {
        "t14": {int(r["table_type"]): r for r in load_json(T14_CENSUS).get("tables", [])},
        "stage2": {int(r["table_type"]): r for r in load_json(STAGE2_MAP).get("tables", [])},
    }
    node_map = schema_list_nodes()
    master_sha = manifest_hash(MASTER)
    payloads, metas, notes = load_server_tables(table_ids)
    OUTDIR.mkdir(parents=True, exist_ok=True)
    (OUTDIR / "profiles").mkdir(exist_ok=True)
    progress = ["# t33 batch II progress", "",
                f"master.json sha256 `{master_sha}`; server archive sha256 "
                f"`{notes['server_archive_sha256']}`", ""]
    results = []
    for tid in table_ids:
        profile, extra = build_table_profile(tid, payloads[tid], metas[tid], node_map, ident)
        rel = relationship_entries(tid, profile)
        attach_judgement(tid, profile, rel)
        profile_path = OUTDIR / "profiles" / f"table_server_{tid}.profile.json"
        profile_path.write_text(json.dumps(profile, ensure_ascii=False, indent=1) + "\n",
                                encoding="utf-8")
        rel["profile_sha256"] = sha256(profile_path.read_bytes())
        rel["rows_sha256"] = profile["row_closure"]["rows_sha256"]
        results.append(rel)
        c = profile["row_closure"]
        progress.append(
            f"- [x] table_{tid} `{profile['rtti_class']}`: {c['equation']}; "
            f"model={c['model']}; rows={c['count']}; conf={rel['confidence']}")
        write_progress(progress)
        print(f"table_{tid}: model={c['model']} count={c['count']} stride={c['stride']} "
              f"conf={rel['confidence']}")
    doc = {
        "status": "batch_ii_data_side_profiles",
        "task": "t33 club/team subtable data-side profiling batch II; candidates only, no L3",
        "generated_on": "2026-11-19",
        "provenance": {
            "master_sha256": master_sha,
            "server_archive_sha256": notes["server_archive_sha256"],
            "server_census": "evidence/fm24/reports/dbdat_decode/server_tables_census.json",
            "t14_census": "scratch/t14/out/census.json",
            "stage2_map": "scratch/t14/out/stage2_map.json",
            "t29_inventory": "scratch/t29/out/subtable_inventory.json",
            "data_root": "scratch/data",
            "manifest_snapshot": "evidence/MANIFEST.json",
            "e66_frame_scan": notes["e66_frame_scan"] or "no member needed a frame-offset retry",
        },
        "summary": {
            "tables_profiled": len(results),
            "confidence": {k: sum(1 for r in results if r["confidence"] == k)
                           for k in ("candidate", "unknown")},
            "L3_claims": 0, "L4_claims": 0,
            "row_models": {str(r["table_type"]): r["row_model"] for r in results},
        },
        "tables": results,
    }
    (OUTDIR / "subtable_candidates.json").write_text(
        json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    write_report(doc)
    write_done(doc)
    progress.append("")
    progress.append(f"done: {len(results)}/{len(TABLES)} tables")
    write_progress(progress)
    bad = [r["table_type"] for r in results
           if r["profile_file"] and not (OUTDIR / r["profile_file"]).is_file()]
    return 1 if bad else 0


# ---------------------------------------------------------------- selftest
def write_report(doc: dict[str, Any]) -> None:
    s = doc["summary"]
    lines = [
        "# t33 — club/team 子表数据侧画像 batch II",
        "",
        f"状态：`{doc['status']}`。本批 7 张 server 子表全部获得完整行 dump 与逐字节列画像；"
        f"**parent↔table 连接全部停留在 candidate/unknown，L3=0、L4=0**，不做静态 cursor。",
        "",
        "## 行封口(独立算术 + 每行尾锚)",
        "",
        "| table | RTTI | model | count | stride | 封口方程 | rows_sha256 前 16 |",
        "|---:|---|---|---:|---:|---|---|",
    ]
    for t in doc["tables"]:
        prof = load_json(OUTDIR / t["profile_file"])
        c = prof["row_closure"]
        lines.append(
            f"| {t['table_type']} | `{t['rtti_class'][:44]}` | {c['model']} | {c['count']} | "
            f"{c['stride'] if c['stride'] else '—'} | {c['equation']} | "
            f"`{c['rows_sha256'][:16]}` |")
    lines += [
        "",
        "固定表同时试过 `14+n*s+8` 与 `13+n*s+9` 两种约定；只有通过逐行尾锚"
        "(`ordinal|id|id|marker`) 的那一种被采用，另一种的算术结果保留在 "
        "`row_closure.conventions_tried` 里备查。变长表用 tail-13 帧前向走查，"
        "每行 ordinal 严格等于行号、相邻两个 u32 相等、末字节为 0x00/0x0C，"
        "并要求 `14 + Σrow + 8 == payload_len` 精确闭合。",
        "",
        "### 帧歧义(E66 相邻问题)",
        "",
        "变长走查取**最短可行帧长**；若同一行还有更长的长度也满足帧条件，计入 "
        "`frame_ambiguity`：",
        "",
    ]
    for t in doc["tables"]:
        prof = load_json(OUTDIR / t["profile_file"])
        fa = prof["row_closure"].get("frame_ambiguity")
        if fa:
            lines.append(f"- table_{t['table_type']}: 多解行 {fa['rows_with_multiple_valid_lengths']}"
                         f" / {prof['row_closure']['count']}，最多 {fa['max_candidate_lengths']} 个候选长度")
    lines += [
        "",
        "## parent↔table 连接判断",
        "",
        "| table | 候选父码 | confidence | 主要 blocker |",
        "|---:|---|---|---|",
    ]
    for t in doc["tables"]:
        parents = ", ".join(f"`{p['parent_4cc']}`" for p in t["parents"]) or "—"
        lines.append(f"| {t['table_type']} | {parents} | **{t['confidence']}** | "
                     f"{t['blockers'][0][:96]} |")
    lines += [
        "",
        "### 逐表理由",
        "",
    ]
    for t in doc["tables"]:
        lines.append(f"- **table_{t['table_type']}** `{t['rtti_class']}` — {t['confidence']}")
        lines.append(f"  - 依据：{t['confidence_basis']}")
        for b in t["blockers"]:
            lines.append(f"  - blocker：{b}")
        for r in t["rejected_parents"]:
            lines.append(f"  - 已排除 `{r['parent_4cc']}`：{r['reason']}")
        for p in t["parents"]:
            lines.append(f"  - schema `{p['schema_path']}` item 字段 "
                         f"{p['item_fields_with_column_candidate']}/{p['item_field_count']} "
                         f"有列候选")
    lines += [
        "",
        "## 列候选方法",
        "",
        "- 列画像覆盖每个 byte offset × {u8,u16,u32,u64}，固定表用 `row_start` 帧，"
        "变长表同时用 `row_start` 与 `row_end` 帧；u32 额外算 signed i32、引用域"
        "命中率、packed day/year 有效率、float32 重解释。",
        "- 走查器自身的尾锚字节(`row_end-1..-13`)与常量列在匹配前被剔除"
        "(`is_frame_column`)，否则边界机器码会被当成字段证据。",
        "- 引用域候选要求列值真分散(≥50% distinct 且 max≥32)，只落在"
        "`[0,domain)` 不算证据。整数候选要求列真有范围，不是两值旗标。",
        "- 所有匹配一律 `evidence_level=L2_candidate` / `claim_status=candidate`；"
        "域相似性从不单独决定字段身份。",
        "",
        "## 口径与限制",
        "",
        "- 只读 `scratch/data`(与冻结 `dat_headers.json` 的 size/SHA-256 校验一致)与仓内证据；"
        "未读写 Z:，未启动游戏/编辑器/IDA，L4=0。",
        "- `master.json` 快照 SHA-256 与 `evidence/MANIFEST.json` 比对通过，写入 provenance。",
        "- t14 census 无 `reader_va` 字段，本批一律记 `null`，未从 handler VA 推导。",
        "- t14 `entity_tag` 为 null 的表(45/48)保留 null，不借 stage2 的 pers 结论改写 RTTI 身份。",
        "- 负结果保留：table_73 在冻结 schema 中找不到对应 list 节点，标 unknown 而非猜。",
        "",
        "## 验证",
        "",
        "```",
        "py -V:3.12 -I -B scratch/t33/out/verify.py",
        "```",
        "",
        "独立重读 archive、重新走查行边界、复算 payload/rows SHA-256、复核列统计抽样。",
    ]
    (OUTDIR / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_done(doc: dict[str, Any]) -> None:
    parts = []
    for t in doc["tables"]:
        prof = load_json(OUTDIR / t["profile_file"])
        c = prof["row_closure"]
        parts.append(f"t{t['table_type']}={c['count']}x"
                     f"{c['stride'] if c['stride'] else 'var'}")
    cand = [f"t{t['table_type']}->{p['parent_4cc']}" for t in doc["tables"]
            for p in t["parents"]]
    text = (
        f"DONE: 完成 {len(doc['tables'])}/7 表画像(" + ", ".join(parts) + ").\n"
        f"新连接候选: {', '.join(cand) or '无'} (全部 candidate/unknown, L3=0, L4=0)。\n"
        "交付: profiles/*.profile.json + *.rows.jsonl, subtable_candidates.json, "
        "REPORT.md, verify.py, scripts/t33_profile_batch.py。\n"
    )
    (OUTDIR / "DONE.md").write_text(text, encoding="utf-8")


def run_selftest() -> None:
    rows = [struct.pack("<III", (2020 << 16) | 1, 0, 0), struct.pack("<III", (2021 << 16) | 365, 0, 0)]
    col = column_profile(rows, 0, 4)
    assert col["packed_day_year"]["valid_count"] == 2, col["packed_day_year"]
    assert column_fit({"type": "date", "field": "stdt"}, col) is not None
    # signed cash
    cash = column_profile([struct.pack("<i", -500), struct.pack("<i", 250)], 0, 4)
    assert column_fit({"type": "cash", "field": "wage", "min_value": 0,
                       "max_value": 1_000_000_000}, cash) is None
    assert column_fit({"type": "cash", "field": "wage", "min_value": -1_000,
                       "max_value": 1_000}, cash) is not None
    # boolean / enum
    flags = column_profile([b"\x00", b"\x01", b"\x01"], 0, 1)
    assert column_fit({"type": "boolean", "field": "ismc"}, flags) is not None
    # domain: ids must vary across rows
    ids = column_profile([struct.pack("<I", v) for v in (100, 80_000, 4_321, 39_004)], 0, 4)
    assert column_fit({"type": "database_record_unique_id", "field": "affl",
                       "database_table_type": "club"}, ids) is not None
    tiny = column_profile([struct.pack("<I", v) for v in (1, 2, 1, 2)], 0, 4)
    assert column_fit({"type": "database_record_unique_id", "field": "affl",
                       "database_table_type": "club"}, tiny) is None
    # variable walker: build 3 rows with the tail-13 frame
    blobs = []
    for i, extra in enumerate((b"", b"\xaa\xbb\xcc\xdd", b"\x01\x02")):
        body = extra + struct.pack("<I", i) + struct.pack("<I", 7) + struct.pack("<I", 7) + b"\x00"
        blobs.append(body)
    raw = TAD_MAGIC + struct.pack("<I", 3) + b"\x00\x00" + b"".join(blobs) + b"\x00" * 8
    dec = walk_variable(raw[14:len(raw) - 8], 3)
    assert dec["count"] == 3 and [len(r) for r in dec["rows"]] == [13, 17, 15]
    assert dec["marker_counts"] == {"0x00": 3}
    # fixed closure on both conventions
    body = b"".join(struct.pack("<I", i) + struct.pack("<II", 9, 9) + b"\x00" for i in range(4))
    fixed_raw = TAD_MAGIC + struct.pack("<I", 4) + b"\x00\x00" + body + b"\x00" * 8
    dec2 = decode_fixed(fixed_raw, 4)
    assert dec2["stride"] == 13 and dec2["row_start"] == 14
    # suffix column
    suf = column_profile([b"abc\x01\x00", b"de\x02\x00"], 2, 2, from_end=True)
    assert suf["coverage"] == 1.0 and suf["offset_frame"] == "row_end"
    print("SELFTEST PASS: packed dates, cash/boolean/domain filters, tail-13 walker, "
          "fixed closure, suffix columns")


def main() -> int:
    ap = argparse.ArgumentParser(description="t33 batch II data-side subtable profiling.")
    ap.add_argument("--selftest", action="store_true", help="offline synthetic checks only")
    ap.add_argument("--only", default="", help="comma list of table ids to profile")
    ap.add_argument("--outdir", type=pathlib.Path, default=OUTDIR,
                    help="must resolve to scratch/t33/out")
    args = ap.parse_args()
    try:
        if args.selftest:
            run_selftest()
            return 0
        if args.outdir.resolve() != OUTDIR.resolve():
            raise T33Error("output must be scratch/t33/out")
        only = [int(x) for x in args.only.split(",") if x.strip()] if args.only else None
        return run(only)
    except T33Error as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    except (OSError, ValueError, KeyError, IndexError, struct.error, ctypes.ArgumentError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
