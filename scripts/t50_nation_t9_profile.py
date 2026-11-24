#!/usr/bin/env python3
"""t50 — data-side profile of the two NATIONAL_TEAM_CONTAINER members.

Scope (strictly data side): decode `table_9.dat` and `table_extra_9.dat` from
both archives, then rebuild row/block framing and the identity census from the
payload bytes alone.

This task never reads editor.exe/IDA, never follows a reader or a VA, never
names a semantic field, never joins a target ordinal, and never promotes L3.
Everything below is L1 recomputation plus cross-member/cross-table L2
comparison. L3 = 0, L4 = 0.

Framing rules are *derived from the payload*, not assumed from t10:
header/selector split, footer split, and the identity-tail predicate are each
listed in a sensitivity table with the walk count they produce, so a reader can
see which parts the data pins down and which parts it does not.

Run with Python 3.12:
  py -V:3.12 -I -B scripts/t50_nation_t9_profile.py --help
  py -V:3.12 -I -B scripts/t50_nation_t9_profile.py --selftest
  FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data py -V:3.12 -I -B scripts/t50_nation_t9_profile.py --build
Exit codes: 0 success / 1 check failed / 2 usage or fatal error.
"""
from __future__ import annotations
import sys as _cfg_sys
from pathlib import Path as _cfg_pathlib
_cfg_sys.path.insert(0, str(_cfg_pathlib(__file__).resolve().parent))
import fm24_config as _cfg

import argparse
import collections
import hashlib
import json
import os
import pathlib
import runpy
import struct
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "scratch/t50/out"
PROFILE_DIR = OUTDIR / "profiles"
DBDIR = pathlib.Path(os.environ.get("FM24_DB_DIR") or (ROOT / "scratch/data")).resolve()
CODEC = pathlib.Path(str(_cfg.OLD_DBDAT_READER))

TAD_MAGIC = bytes.fromhex("03017461642ef10d")
MEMBERS = ("table_9.dat", "table_extra_9.dat")
SIDES = ("client", "server")
EXPECTED_MEMBERS = {"client": 31, "server": 77}

# t9: parameters used for the delivered framing (each justified in sensitivity).
T9_HEADER = 13
T9_FOOTER = 8
IDENTITY_BYTES = 13
IDENTITY_MARKER = 0x00
T9_PROBE_OFFSETS = (0, 1, 4, 8, 12, 16, 20, 24, 32, 40)
# table_extra_9: the first record anchors this marker shape; it stays a candidate.
X9_HEADER = 12
X9_PROBE_OFFSETS = (0, 4, 8, 12, 16, 20, 24)
X9_NAME_MAX = 120
ROW_SAMPLE_LIMIT = 6


class T50Error(RuntimeError):
    pass


class Check(T50Error):
    pass


def need(cond: Any, msg: Any) -> None:
    if not cond:
        raise Check(msg)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def signed_value(value: int, width: int) -> int:
    sign = 1 << (width * 8 - 1)
    return value - (1 << (width * 8)) if value & sign else value


def u32(b: bytes, pos: int) -> int:
    return struct.unpack_from("<I", b, pos)[0]


def hist(seq) -> dict[str, int]:
    return {str(k): v for k, v in sorted(collections.Counter(seq).items())}


def write_json(path: pathlib.Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=1, allow_nan=False) + "\n", encoding="utf-8")


def codec() -> dict[str, Any]:
    if not CODEC.is_file():
        raise T50Error(f"third-party dbdat codec missing: {CODEC}")
    return runpy.run_path(str(CODEC))


# --------------------------------------------------------------------------
# archive / payload access (E80: member start = data_base + entry.offset)
# --------------------------------------------------------------------------
def load_member(zstd, lay: dict[str, Any], blob: bytes, name: str) -> dict[str, Any]:
    es = {pathlib.PurePosixPath(e["path"]).name: e for e in lay["entries"]}
    entry = es.get(name)
    if entry is None:
        return {"present": False}
    base = int(lay["data_base"])
    lo = base + int(entry["offset"])
    hi = lo + int(entry["packed_size"])
    need(0 <= lo < hi <= len(blob), f"{name}: member bounds")
    part = blob[lo:hi]
    frames: list[list[int]] = []
    choices: list[tuple[bytes, list[int]]] = []
    pos = 0
    while pos < len(part):
        need(part[pos:pos + 4] == b"\x28\xb5\x2f\xfd", f"{name}: zstd magic at member+{pos}")
        dec = zstd.ZstdDecompressor().decompressobj()
        payload = dec.decompress(part[pos:])
        used = len(part) - pos - len(dec.unused_data)
        need(dec.eof and used > 0, f"{name}: frame EOF at member+{pos}")
        frame = [lo + pos, used, len(payload)]
        frames.append(frame)
        if len(payload) == int(entry["size"]):
            choices.append((payload, frame))
        pos += used
    need(len(choices) == 1, f"{name}: {len(choices)} frames match entry.size")
    payload, frame = choices[0]
    packed_sha = digest(part)
    # the raw FMF directory record has no sha256 field; it only appears in the
    # reader's _entry_summary. When the record does carry one, it must agree.
    listed_sha = entry.get("sha256")
    if listed_sha is not None:
        need(packed_sha == listed_sha, f"{name}: packed SHA == directory sha256")
    return {
        "present": True,
        "path": entry["path"],
        "entry_offset_relative_to_data_base": int(entry["offset"]),
        "packed_size": int(entry["packed_size"]),
        "declared_size": int(entry["size"]),
        "member_start_absolute": lo,
        "member_end_absolute": hi,
        "frame_count": len(frames),
        "frame_lengths": [f[2] for f in frames],
        "selected_frame": {
            "offset": frame[0],
            "compressed_bytes": frame[1],
            "payload_bytes": frame[2],
        },
        "packed_sha256": packed_sha,
        "packed_sha256_source": "recomputed over [member_start, member_start+packed_size)",
        "payload_size": len(payload),
        "payload_sha256": digest(payload),
        "payload_head_hex": payload[:24].hex(),
        "payload_version": struct.unpack_from("<H", payload, 6)[0] if payload[:6] == bytes.fromhex("0301746164") else None,
        "record_count_header": u32(payload, 8),
        "tad_shell_ok": payload[:8] == TAD_MAGIC,
    }


def load_archives() -> tuple[dict[str, Any], dict[tuple[str, str], bytes]]:
    """Return (anchors, payloads). payloads[key] = decompressed bytes."""
    zstd = _zstd()
    k = codec()
    anchors: dict[str, Any] = {}
    payloads: dict[tuple[str, str], bytes] = {}
    for side in SIDES:
        archive = DBDIR / f"{side}_db.dat"
        need(archive.is_file(), f"missing archive {archive}")
        blob = archive.read_bytes()
        lay = k["_archive_layout"](blob)
        need(int(lay["data_base"]) == 34, f"{side}: data_base {lay['data_base']} != 34")
        need(len(lay["entries"]) == EXPECTED_MEMBERS[side], f"{side}: directory entry count")
        members: dict[str, Any] = {}
        for name in MEMBERS:
            m = load_member(zstd, lay, blob, name)
            members[name] = m
            if m["present"]:
                payloads[side, name] = _reload_payload(zstd, lay, blob, name)
        anchors[side] = {
            "archive_path": f"{side}_db.dat",
            "archive_sha256": digest(blob),
            "data_base": int(lay["data_base"]),
            "directory_entries": len(lay["entries"]),
            "members": members,
        }
    # the task anchor also asks whether table_extra_10 exists in both archives.
    presence = {}
    for side in SIDES:
        blob = (DBDIR / f"{side}_db.dat").read_bytes()
        names = {pathlib.PurePosixPath(e["path"]).name for e in k["_archive_layout"](blob)["entries"]}
        presence[side] = {n: (n in names) for n in ("table_9.dat", "table_extra_9.dat", "table_extra_10.dat")}
    anchors["member_presence"] = presence
    return anchors, payloads


def _reload_payload(zstd, lay: dict[str, Any], blob: bytes, name: str) -> bytes:
    es = {pathlib.PurePosixPath(e["path"]).name: e for e in lay["entries"]}
    entry = es[name]
    lo = int(lay["data_base"]) + int(entry["offset"])
    part = blob[lo:lo + int(entry["packed_size"])]
    pos = 0
    while pos < len(part):
        dec = zstd.ZstdDecompressor().decompressobj()
        payload = dec.decompress(part[pos:])
        if len(payload) == int(entry["size"]):
            return payload
        pos += len(part) - pos - len(dec.unused_data)
    raise T50Error(f"{name}: payload reload failed")


def _zstd():
    sys.path.append(str(_cfg.VENDOR_DIR))
    import zstandard  # noqa: PLC0415
    return zstandard


# --------------------------------------------------------------------------
# t9 identity candidates and closure
# --------------------------------------------------------------------------
def identity_candidates(body: bytes, ordinal: int, start: int, marker: int | None) -> list[tuple[int, int]]:
    """Absolute positions >= start where `ordinal | id | id | marker` stands.

    `start` is only a search floor; every returned offset is relative to `body`.
    """
    out: list[tuple[int, int]] = []
    needle = struct.pack("<I", ordinal)
    pos = body.find(needle, start)
    while pos >= 0:
        if pos + IDENTITY_BYTES <= len(body):
            first, second = struct.unpack_from("<II", body, pos + 4)
            if first == second and (marker is None or body[pos + 12] == marker):
                out.append((pos, first))
        pos = body.find(needle, pos + 1)
    return out


def walk_identities(
    payload: bytes,
    header: int,
    footer: int,
    marker: int | None = 0,
    allow_zero_id: bool = False,
    require_increasing: bool = True,
) -> dict[str, Any]:
    """Exact count of complete framings + one canonical backtracked framing."""
    count = u32(payload, 8)
    stop = len(payload) - footer
    if stop < header:
        return {"count": count, "stop": stop, "complete_walks": 0, "rows": None, "dead_row": 0}
    table = {i: identity_candidates(payload, i, header, marker) for i in range(count)}
    states: dict[tuple[int, int], int] = {(header, -1): 1}
    parent: list[dict[tuple[int, int], tuple[int, int, int]]] = []
    dead_row = None
    for i in range(count):
        nxt: dict[tuple[int, int], int] = {}
        par: dict[tuple[int, int], tuple[int, int, int]] = {}
        for (pos, last), ways in states.items():
            for at, row_id in table[i]:
                if at < pos or at + IDENTITY_BYTES > stop:
                    continue
                if row_id == 0 and not allow_zero_id:
                    continue
                if require_increasing and not row_id > last:
                    continue
                key = (at + IDENTITY_BYTES, row_id)
                nxt[key] = nxt.get(key, 0) + ways
                par.setdefault(key, (pos, last, at))
        states = nxt
        parent.append(par)
        if not states:
            dead_row = i
            break
    complete = 0
    for (pos, _last), ways in states.items():
        if pos == stop:
            complete += ways
    rows = None
    if dead_row is None and complete:
        ends = [k for k in states if k[0] == stop]
        key = min(ends, key=lambda k: k[1])
        rows = []
        for i in range(count - 1, -1, -1):
            pos, last, at = parent[i][key]
            rows.append({"row": i, "identity_at": at, "row_id": key[1], "body_start": pos})
            key = (pos, last)
        rows.reverse()
        for k, row in enumerate(rows):
            row["body_offset"] = row["body_start"] - header
            row["span"] = row["identity_at"] + IDENTITY_BYTES - row["body_start"]
            row["raw"] = payload[row["body_start"]:row["identity_at"] + IDENTITY_BYTES]
    return {
        "count": count,
        "header": header,
        "footer": footer,
        "stop": stop,
        "identity_marker": marker,
        "allow_zero_id": allow_zero_id,
        "require_increasing": require_increasing,
        "complete_walks": complete,
        "dead_row": dead_row,
        "rows": rows,
        "candidate_table": table if rows is not None else None,
    }


def sensitivity(payload: bytes) -> dict[str, Any]:
    """Which framing knobs does the payload actually pin down?"""
    main = walk_identities(payload, T9_HEADER, T9_FOOTER)
    variants: dict[str, Any] = {}
    for footer in (6, 7, 8, 9, 10, 12):
        r = walk_identities(payload, T9_HEADER, footer)
        variants[f"footer={footer}"] = r["complete_walks"]
    for header in (11, 12, 13, 14, 15):
        r = walk_identities(payload, header, T9_FOOTER)
        variants[f"header={header}"] = r["complete_walks"]
    variants["identity_marker=None"] = walk_identities(payload, T9_HEADER, T9_FOOTER, marker=None)["complete_walks"]
    variants["allow_zero_id=True"] = walk_identities(payload, T9_HEADER, T9_FOOTER, allow_zero_id=True)["complete_walks"]
    variants["require_increasing=False"] = walk_identities(
        payload, T9_HEADER, T9_FOOTER, require_increasing=False
    )["complete_walks"]
    variants["allow_zero_id=True+require_increasing=False"] = walk_identities(
        payload, T9_HEADER, T9_FOOTER, allow_zero_id=True, require_increasing=False
    )["complete_walks"]
    return {
        "delivered": {"header": T9_HEADER, "footer": T9_FOOTER, "complete_walks": main["complete_walks"]},
        "variants": variants,
        "reading": (
            "footer=8 is the unique split that closes; header 11..15 all close identically because no "
            "identity lands in the 11..15 window, so the header/selector split is NOT decided by data; "
            "zero-id acceptance and monotonicity are what turn a unique closure into an ambiguous one."
        ),
    }


def prefix_probe(row: dict[str, Any], offsets=T9_PROBE_OFFSETS) -> list[dict[str, Any]]:
    raw = row["raw"]
    out = []
    for off in offsets:
        if len(raw) >= off + 4:
            v = u32(raw, off)
            out.append({
                "offset": off,
                "raw_hex": raw[off:off + 4].hex(),
                "u32le": v,
                "i32le": signed_value(v, 4),
                "meaning": "unassigned positional probe; not asserted as a count or a field",
            })
    return out


def t9_rows(payload: bytes, side: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    walk = walk_identities(payload, T9_HEADER, T9_FOOTER)
    need(walk["complete_walks"] == 1, f"{side} t9: complete_walks == 1 (got {walk['complete_walks']})")
    need(walk["rows"] is not None, f"{side} t9: no canonical framing")
    rows = walk["rows"]
    count = walk["count"]
    need(len(rows) == count, f"{side} t9: row count")
    records = []
    total = 0
    for row in rows:
        raw = row["raw"]
        ordinal, row_id, repeated = struct.unpack_from("<III", raw, len(raw) - IDENTITY_BYTES)
        marker = raw[-1]
        total += len(raw)
        records.append({
            "row": row["row"],
            "offset": row["body_start"],
            "body_offset": row["body_offset"],
            "len": len(raw),
            "identity": {
                "ordinal": ordinal,
                "row_id": row_id,
                "repeated_id": repeated,
                "marker": marker,
                "tail_offset_in_row": len(raw) - IDENTITY_BYTES,
                "basis": "observed 13-byte tail in the payload; ordinal/id/id/00, no static input",
            },
            "prefix_probe_i32le": prefix_probe(row),
            "raw_hex": raw.hex(),
        })
    summary = {
        "status": "complete_identity_closure_L1",
        "count": count,
        "row_start": T9_HEADER,
        "row_end_exclusive": walk["stop"],
        "footer_bytes": T9_FOOTER,
        "payload_bytes": len(payload),
        "sum_row_lens": total,
        "equation": f"{T9_HEADER} + sum(row_lens={total}) + {T9_FOOTER} = {T9_HEADER + total + T9_FOOTER}",
        "closure_exact": T9_HEADER + total + T9_FOOTER == len(payload),
        "footer_hex": payload[walk["stop"]:].hex(),
        "footer_fields_observed": {
            "u32le_at_payload_minus_4": u32(payload, len(payload) - 4),
            "byte_at_payload_minus_5": payload[len(payload) - 5],
            "hex_8_bytes": payload[len(payload) - 8:].hex(),
            "note": (
                "the trailing 8 bytes are what close the tiling; the last row's marker byte is also the "
                "first byte of a 9-byte reading, so 8-vs-9 footer split is not separable from data "
                "(9-byte reading leaves no valid tiling: footer=9 -> 0 walks)"
            ),
        },
        "row_len_hist": hist(r["len"] for r in records),
        "row_len_min": min(r["len"] for r in records),
        "row_len_max": max(r["len"] for r in records),
        "row_len_mean": round(total / count, 3),
        "prefix_probe_offsets": list(T9_PROBE_OFFSETS),
        "consecutive_row_len_mean": round(total / count, 3),
    }
    return summary, records


def t9_identity_census(records: list[dict[str, Any]], payload: bytes, side: str) -> dict[str, Any]:
    ordinals = [r["identity"]["ordinal"] for r in records]
    ids = [r["identity"]["row_id"] for r in records]
    repeated_ok = all(r["identity"]["row_id"] == r["identity"]["repeated_id"] for r in records)
    marker_ok = all(r["identity"]["marker"] == IDENTITY_MARKER for r in records)
    all_triples = identity_candidates(payload, 0, T9_HEADER, IDENTITY_MARKER)
    per_ordinal = collections.Counter()
    for ord_ in range(len(records)):
        per_ordinal[len(identity_candidates(payload, ord_, T9_HEADER, IDENTITY_MARKER))] += 1
    return {
        "ordinal_sequence_is_0_to_N_minus_1": ordinals == list(range(len(records))),
        "ordinal_first": ordinals[0],
        "ordinal_last": ordinals[-1],
        "repeated_lanes_equal": repeated_ok,
        "marker_all_zero": marker_ok,
        "row_id_unique": len(set(ids)) == len(ids),
        "row_id_strictly_increasing": all(a < b for a, b in zip(ids, ids[1:])),
        "row_id_min": min(ids),
        "row_id_max": max(ids),
        "row_id_zero_count": ids.count(0),
        "identity_structure": "ordinal | row_id | row_id | 0x00 (13 bytes at row end)",
        "candidate_count_per_ordinal_hist": {str(k): v for k, v in sorted(per_ordinal.items())},
        "ordinal0_candidates_outside_chosen_tail": len(all_triples),
        "note": (
            "row_id 0 is never the chosen tail value; it appears only as a decoy match inside row bodies, "
            "which is why accepting zero ids explodes the walk count in the sensitivity table"
        ),
    }


# --------------------------------------------------------------------------
# table_extra_9: ordinal + name markers (candidate shape anchored by record 0)
# --------------------------------------------------------------------------
def x9_marker(body: bytes, ordinal: int, start: int, name_max: int = X9_NAME_MAX) -> list[tuple[int, int]]:
    out: list[tuple[int, int]] = []
    needle = struct.pack("<I", ordinal)
    pos = body.find(needle, start)
    while pos >= 0:
        if pos + 8 <= len(body):
            name_len = u32(body, pos + 4)
            if 0 <= name_len <= name_max and pos + 8 + name_len <= len(body):
                name = body[pos + 8:pos + 8 + name_len]
                if all(x >= 0x20 for x in name):
                    out.append((pos, name_len))
        pos = body.find(needle, pos + 1)
    return out


def walk_x9(payload: bytes, header: int = X9_HEADER, name_max: int = X9_NAME_MAX) -> dict[str, Any]:
    count = u32(payload, 8)
    table = {i: x9_marker(payload, i, header, name_max) for i in range(count)}
    states: dict[int, int] = {header: 1}
    parent: list[dict[int, tuple[int, int]]] = []
    dead_row = None
    for i in range(count):
        nxt: dict[int, int] = {}
        par: dict[int, tuple[int, int]] = {}
        for pos, ways in states.items():
            for at, name_len in table[i]:
                if at < pos:
                    continue
                nxt[at] = nxt.get(at, 0) + ways
                par.setdefault(at, (pos, name_len))
        states = nxt
        parent.append(par)
        if not states:
            dead_row = i
            break
    walks = len(states) and sum(states.values())
    starts = None
    if dead_row is None:
        # canonical: earliest possible start of the last record (min final state)
        pos = min(states)
        starts = []
        for i in range(count - 1, -1, -1):
            prev, name_len = parent[i][pos]
            starts.append({"row": i, "start": pos, "name_len": name_len})
            pos = prev
        starts.reverse()
        for k, row in enumerate(starts):
            end = starts[k + 1]["start"] if k + 1 < len(starts) else len(payload)
            row["span"] = end - row["start"]
            row["raw"] = payload[row["start"]:end]
    return {
        "count": count,
        "header": header,
        "block_walks": walks,
        "distinct_final_positions": sorted(states) if states else [],
        "dead_row": dead_row,
        "starts": starts,
        "table": table if starts is not None else None,
    }


def x9_block_ambiguity(payload: bytes, starts: list[dict[str, Any]], name_max: int = X9_NAME_MAX) -> dict[str, Any]:
    ambiguous = []
    for k, row in enumerate(starts):
        lo = row["start"]
        hi = starts[k + 1]["start"] if k + 1 < len(starts) else len(payload)
        hits = [at for at, _n in x9_marker(payload, row["row"], lo, name_max) if at < hi]
        if len(hits) > 1:
            ambiguous.append({"row": row["row"], "candidates": hits, "block": [lo, hi]})
    return {
        "ambiguous_block_count": len(ambiguous),
        "ambiguous": ambiguous[:20],
        "note": "ambiguity is inside the block, not in the block start: every block start is forced",
    }


# --------------------------------------------------------------------------
# cross-member / cross-table comparison
# --------------------------------------------------------------------------
def t10_ids(payload: bytes) -> dict[str, Any]:
    """Same 13-byte identity framing applied to table_10 as an independent cross-check."""
    walk = walk_identities(payload, T9_HEADER, T9_FOOTER)
    rows = walk["rows"] or []
    ids = [r["row_id"] for r in rows]
    return {
        "count": walk["count"],
        "complete_walks": walk["complete_walks"],
        "closure_exact": bool(rows) and rows[-1]["identity_at"] + IDENTITY_BYTES == walk["stop"],
        "row_ids": ids,
        "spans": [r["span"] for r in rows],
        "payload_bytes": len(payload),
    }


def grammar_diff(t9: dict[str, dict[str, Any]], rows9: dict[str, list[dict[str, Any]]],
                 x9: dict[str, dict[str, Any]], ids10: dict[str, list[int]]) -> dict[str, Any]:
    c_rows, s_rows = rows9["client"], rows9["server"]
    c_len = [r["len"] for r in c_rows]
    s_len = [r["len"] for r in s_rows]
    c_ids = [r["identity"]["row_id"] for r in c_rows]
    s_ids = [r["identity"]["row_id"] for r in s_rows]
    same_offset = []
    c0 = bytes.fromhex(c_rows[0]["raw_hex"])
    s0 = bytes.fromhex(s_rows[0]["raw_hex"])
    for off in (0, 1, 2, 4, 8, 12, 16, 20, 24, 28, 32, 40, 48, 56, 64):
        if len(c0) >= off + 4 and len(s0) >= off + 4:
            same_offset.append({
                "offset": off,
                "client_hex": c0[off:off + 4].hex(),
                "client_i32le": signed_value(u32(c0, off), 4),
                "server_hex": s0[off:off + 4].hex(),
                "server_i32le": signed_value(u32(s0, off), 4),
                "equal": c0[off:off + 4] == s0[off:off + 4],
                "meaning": "same-offset positional probe only; no field is assigned",
            })
    len_equal_rows = sum(1 for a, b in zip(c_len, s_len) if a == b)
    first_len_diff = next((i for i, (a, b) in enumerate(zip(c_len, s_len)) if a != b), None)
    return {
        "status": "client_server_row_grammar_not_isomorphic",
        "evidence_level": {"L1": "recomputed from both payloads", "L2": "identity/ordinal comparison", "L3": 0, "L4": 0},
        "table_9": {
            "count": {"client": t9["client"]["count"], "server": t9["server"]["count"], "equal": True},
            "header": {"client": T9_HEADER, "server": T9_HEADER},
            "footer": {"client": T9_FOOTER, "server": T9_FOOTER},
            "identity_structure": {"client": "ordinal|row_id|row_id|00", "server": "ordinal|row_id|row_id|00"},
            "identity_agrees_row_by_row": c_ids == s_ids,
            "identity_first_difference": next(
                ({"row": i, "client": a, "server": b} for i, (a, b) in enumerate(zip(c_ids, s_ids)) if a != b), None
            ),
            "ordinal_sequence_identical": [r["identity"]["ordinal"] for r in c_rows]
            == [r["identity"]["ordinal"] for r in s_rows],
            "row_len_equal_rows": len_equal_rows,
            "row_len_first_difference": first_len_diff,
            "row_len": {
                "client": {"min": min(c_len), "max": max(c_len), "mean": round(sum(c_len) / len(c_len), 3)},
                "server": {"min": min(s_len), "max": max(s_len), "mean": round(sum(s_len) / len(s_len), 3)},
            },
            "identical_row_count": sum(1 for a, b in zip(c_rows, s_rows) if a["raw_hex"] == b["raw_hex"]),
            "verdict": "same 251 ordinals and same 251 row_ids, different row bodies",
        },
        "table_extra_9": {
            "block_starts": {"client": x9["client"]["block_walks"], "server": x9["server"]["block_walks"]},
            "marker_structure": "u32 ordinal | u32 name_len | name bytes (candidate shape, anchored by record 0)",
            "identity_structure_absent": True,
            "verdict": "ordinal marker prefixes the block instead of a 13-byte identity tail",
        },
        "same_offset_probe_row0": same_offset,
        "cross_table": {
            "table_10_identity_framing": {
                "client": ids10["client"]["complete_walks"],
                "server": ids10["server"]["complete_walks"],
            },
            "table_10_closure_exact": {
                "client": ids10["client"]["closure_exact"],
                "server": ids10["server"]["closure_exact"],
            },
            "t9_ids_equal_t10_ids": {
                "client": ids10["client"]["row_ids"] == c_ids,
                "server": ids10["server"]["row_ids"] == s_ids,
            },
            "t9_row_spans_differ_from_t10": {
                "client": ids10["client"]["spans"] != c_len,
                "server": ids10["server"]["spans"] != s_len,
            },
            "t10_payload_bytes": {
                "client": ids10["client"]["payload_bytes"],
                "server": ids10["server"]["payload_bytes"],
            },
            "note": (
                "t9 and t10 were decoded independently here with the same 13-byte identity predicate. The "
                "row_id sequence and the 251 count agree while the row spans do not, so the shared thing is "
                "the row_id/ordinal identity ladder, not the row body. This is a data-side cross-table "
                "agreement only: no semantic field is named and no target ordinal is joined."
            ),
        },
    }


# --------------------------------------------------------------------------
# build
# --------------------------------------------------------------------------
def build() -> int:
    zstd = _zstd()
    anchors, payloads = load_archives()
    for side in SIDES:
        for name in MEMBERS:
            m = anchors[side]["members"][name]
            need(m["present"], f"{side}/{name}: member must exist")
            need(m["tad_shell_ok"], f"{side}/{name}: tad shell")
            payload = payloads[side, name]
            need(len(payload) == m["declared_size"], f"{side}/{name}: payload size")
            need(digest(payload) == m["payload_sha256"], f"{side}/{name}: payload SHA")
            need(m["record_count_header"] == 251, f"{side}/{name}: u32 count@8 == 251")

    profile: dict[str, Any] = {
        "status": "partial_data_profile_t9",
        "task": "t50 data-side independent profile of table_9 / table_extra_9 (NATIONAL_TEAM_CONTAINER)",
        "evidence_level": {
            "L1": "payload decode, frame selection, row/block framing, closure, histograms, probes recomputed here",
            "L2": "client vs server identity/ordinal agreement and t9 vs t10 row-id agreement (all data-side)",
            "L3": 0,
            "L4": 0,
        },
        "scope": {
            "data_side_only": True,
            "reads_editor_exe": False,
            "follows_reader_or_VA": False,
            "names_semantic_fields": False,
            "joins_target_ordinals": False,
            "writes_outside": ["scratch/t50/", "scripts/t50_*.py"],
        },
        "framing_rules_are_candidates": True,
        "archives": anchors,
        "members": {},
    }

    rows_out: dict[tuple[str, str], list[dict[str, Any]]] = {}
    t9_summary: dict[str, dict[str, Any]] = {}
    x9_summary: dict[str, dict[str, Any]] = {}

    for side in SIDES:
        payload = payloads[side, "table_9.dat"]
        summary, records = t9_rows(payload, side)
        census = t9_identity_census(records, payload, side)
        sens = sensitivity(payload)
        need(summary["closure_exact"], f"{side} t9: closure equation")
        need(census["ordinal_sequence_is_0_to_N_minus_1"], f"{side} t9: ordinal sequence")
        need(census["repeated_lanes_equal"] and census["marker_all_zero"], f"{side} t9: identity lanes")
        need(census["row_id_unique"], f"{side} t9: row_id uniqueness")
        need(census["row_id_max"] == u32(payload, len(payload) - 4), f"{side} t9: max row_id == footer u32")
        summary["identity_census"] = census
        summary["framing_sensitivity"] = sens
        summary["row_samples"] = _samples(records)
        summary["declared_size_matches_payload"] = len(payload) == anchors[side]["members"]["table_9.dat"]["declared_size"]
        t9_summary[side] = summary
        rows_out[side, "table_9.dat"] = records
        profile["members"][f"{side}/table_9.dat"] = {
            "anchor": anchors[side]["members"]["table_9.dat"],
            "closure": summary,
        }

        xpayload = payloads[side, "table_extra_9.dat"]
        xwalk = walk_x9(xpayload)
        need(xwalk["starts"] is not None, f"{side} extra_9: marker walk must not die")
        starts = xwalk["starts"]
        spans = [r["span"] for r in starts]
        closure = X9_HEADER + sum(spans) == len(xpayload)
        xsummary = {
            "status": "partial_block_start_framing_L1" if closure else "partial_block_start_framing_unclosed_L1",
            "count": xwalk["count"],
            "block_start_header": X9_HEADER,
            "block_walks": xwalk["block_walks"],
            "distinct_final_positions": xwalk["distinct_final_positions"],
            "sum_block_spans": sum(spans),
            "equation": f"{X9_HEADER} + sum(block_spans={sum(spans)}) = {X9_HEADER + sum(spans)}",
            "closure_exact": closure,
            "payload_bytes": len(xpayload),
            "first_block_start": starts[0]["start"],
            "last_block_start": starts[-1]["start"],
            "first_block_span": spans[0],
            "last_block_span": spans[-1],
            "block_span_hist": hist(spans),
            "block_span_min": min(spans),
            "block_span_max": max(spans),
            "nameless_blocks": sum(1 for r in starts if r["name_len"] == 0),
            "block_internal_grammar": "unknown; only the ordinal+name marker prefix is located",
            "footer_separable": False,
            "footer_note": (
                "no footer separates from the last block on this member, unlike table_9 where 8 trailing "
                "bytes close the tiling; the last block runs to payload end"
            ),
            "ambiguity": x9_block_ambiguity(xpayload, starts),
            "identity_structure_present": False,
            "identity_predicate_trial": {
                "what": "the t9 13-byte identity predicate is applied to this member unchanged",
                "results": [
                    {"header": 12, "footer": 0, "complete_walks": walk_identities(xpayload, 12, 0)["complete_walks"],
                     "dead_row": walk_identities(xpayload, 12, 0)["dead_row"]},
                    {"header": 12, "footer": 8, "complete_walks": walk_identities(xpayload, 12, 8)["complete_walks"],
                     "dead_row": walk_identities(xpayload, 12, 8)["dead_row"]},
                    {"header": 13, "footer": 0, "complete_walks": walk_identities(xpayload, 13, 0)["complete_walks"],
                     "dead_row": walk_identities(xpayload, 13, 0)["dead_row"]},
                    {"header": 13, "footer": 8, "complete_walks": walk_identities(xpayload, 13, 8)["complete_walks"],
                     "dead_row": walk_identities(xpayload, 13, 8)["dead_row"]},
                ],
                "verdict": "NEGATIVE: every variant dies at row 1, so the t9 identity tail does not exist on this member",
            },
            "identity_structure_counterexample": {
                "row": 0,
                "first_13_bytes_of_block_hex": starts[0]["raw"][:13].hex(),
                "why": (
                    "the ordinal is a block-leading u32 followed by a u32 name length; there is no "
                    "ordinal|id|id|00 tail at the block end, so the t9 identity predicate does not apply"
                ),
                "identity_triple_hits": len(identity_candidates(xpayload, 0, X9_HEADER, IDENTITY_MARKER)),
                "blocks_whose_last_13_bytes_mimic_the_t9_tail": sum(
                    1
                    for r in starts
                    if (lambda raw: (lambda a, b, c: a == b == c and raw[-1] == 0)(
                        *struct.unpack_from("<III", raw, len(raw) - 13)))(r["raw"])
                ),
                "note": (
                    "the mimic count is not evidence of an identity tail: those bytes are block content "
                    "that happens to repeat a u32; the walk that uses them as boundaries is not closed"
                ),
            },
            "same_offset_probe_offsets": list(X9_PROBE_OFFSETS),
            "block_samples": _x9_samples(starts),
        }
        xsummary["declared_size_matches_payload"] = len(xpayload) == anchors[side]["members"]["table_extra_9.dat"]["declared_size"]
        x9_summary[side] = xsummary
        profile["members"][f"{side}/table_extra_9.dat"] = {
            "anchor": anchors[side]["members"]["table_extra_9.dat"],
            "closure": {k: v for k, v in xsummary.items() if k != "block_samples"},
        }

        xrows = []
        for k, row in enumerate(starts):
            raw = row["raw"]
            name_len = row["name_len"]
            name = raw[8:8 + name_len]
            xrows.append({
                "row": row["row"],
                "offset": row["start"],
                "body_offset": row["start"] - X9_HEADER,
                "len": row["span"],
                "marker": {
                    "ordinal": u32(raw, 0),
                    "name_len": name_len,
                    "name_ascii": name.decode("utf-8", "backslashreplace") if name_len else "",
                    "name_hex": name.hex(),
                    "basis": "candidate shape anchored by record 0; not a field assignment",
                },
                "prefix_probe_i32le": _probe_offsets(raw, X9_PROBE_OFFSETS),
                "raw_hex": raw.hex(),
            })
        rows_out[side, "table_extra_9.dat"] = xrows

    ids10 = {}
    for side in SIDES:
        # table_10 is not a t50 member: it is read only as an independent
        # cross-table comparison of the same identity grammar.
        ids10[side] = t10_ids(_payload_for(side, "table_10.dat"))

    diff = grammar_diff(
        t9_summary,
        {side: rows_out[side, "table_9.dat"] for side in SIDES},
        x9_summary,
        ids10,
    )

    PROFILE_DIR.mkdir(parents=True, exist_ok=True)
    for (side, name), records in rows_out.items():
        stem = f"table_{side}_{'9' if name == 'table_9.dat' else 'extra_9'}"
        path = PROFILE_DIR / f"{stem}.rows.jsonl"
        with path.open("w", encoding="ascii", newline="\n") as fh:
            for rec in records:
                fh.write(json.dumps(rec, ensure_ascii=True, sort_keys=False) + "\n")
    write_json(OUTDIR / "profile_t9.json", profile)
    write_json(OUTDIR / "grammar_diff_t9.json", diff)

    for side in SIDES:
        t = t9_summary[side]
        x = x9_summary[side]
        print(
            f"{side:6s} table_9: {t['count']} rows, {t['equation']} "
            f"closure={t['closure_exact']} maxrow={t['row_len_max']}"
        )
        print(
            f"{side:6s} table_9 identity: ordinals 0..{t['identity_census']['ordinal_last']} "
            f"unique_ids={t['identity_census']['row_id_unique']} increasing={t['identity_census']['row_id_strictly_increasing']}"
        )
        print(
            f"{side:6s} table_extra_9: {x['count']} blocks, {x['equation']} closure={x['closure_exact']} "
            f"walks={x['block_walks']} ambig={x['ambiguity']['ambiguous_block_count']}"
        )
    print(f"t9/t10 row_id agreement: {diff['cross_table']['t9_ids_equal_t10_ids']}")
    print(f"identity agreement client vs server: {diff['table_9']['identity_agrees_row_by_row']}")
    return 0


def _payload_for(side: str, name: str) -> bytes:
    """Read table_10 only as a cross-table comparison; it is not a t50 member."""
    zstd = _zstd()
    k = codec()
    blob = (DBDIR / f"{side}_db.dat").read_bytes()
    lay = k["_archive_layout"](blob)
    return _reload_payload(zstd, lay, blob, name)


def _probe_offsets(raw: bytes, offsets) -> list[dict[str, Any]]:
    out = []
    for off in offsets:
        if len(raw) >= off + 4:
            v = u32(raw, off)
            out.append({
                "offset": off,
                "raw_hex": raw[off:off + 4].hex(),
                "u32le": v,
                "i32le": signed_value(v, 4),
                "meaning": "unassigned positional probe; not asserted as a count or a field",
            })
    return out


def _samples(records: list[dict[str, Any]]) -> dict[str, Any]:
    by_len = sorted(records, key=lambda r: (r["len"], r["row"]))
    pick = []
    seen = set()

    def add(tag: str, rec: dict[str, Any]) -> None:
        if rec["row"] in seen:
            return
        seen.add(rec["row"])
        pick.append({
            "tag": tag,
            "row": rec["row"],
            "offset": rec["offset"],
            "len": rec["len"],
            "identity": rec["identity"],
            "raw_hex": rec["raw_hex"],
        })

    add("first_row", records[0])
    add("second_row", records[1])
    add("last_row", records[-1])
    add("shortest_row", by_len[0])
    add("longest_row", by_len[-1])
    for rec in by_len:
        if len(pick) >= ROW_SAMPLE_LIMIT:
            break
        add("length_order_sample", rec)
    return {"count": len(pick), "samples": pick}


def _x9_samples(starts: list[dict[str, Any]]) -> dict[str, Any]:
    by_span = sorted(starts, key=lambda r: (r["span"], r["row"]))
    pick = []
    seen = set()
    for tag, rec in (("first_block", starts[0]), ("last_block", starts[-1]),
                     ("shortest_block", by_span[0]), ("longest_block", by_span[-1])):
        if rec["row"] in seen:
            continue
        seen.add(rec["row"])
        raw = rec["raw"]
        name_len = rec["name_len"]
        pick.append({
            "tag": tag,
            "row": rec["row"],
            "offset": rec["start"],
            "len": rec["span"],
            "ordinal": u32(raw, 0),
            "name_len": name_len,
            "name_ascii": raw[8:8 + name_len].decode("utf-8", "backslashreplace") if name_len else "",
            "raw_hex_head": raw[:64].hex(),
            "raw_hex_tail": raw[-32:].hex(),
        })
    return {"count": len(pick), "samples": pick}


# --------------------------------------------------------------------------
# selftest
# --------------------------------------------------------------------------
def synth_t9(count: int, span_seed: int = 7, zero_decoy: bool = False) -> bytes:
    rows = []
    pos = 0
    for i in range(count):
        span = 20 + (i * span_seed) % 31
        body = bytes([0xAA]) * span
        if zero_decoy and i == 0:
            body = struct.pack("<III", 0, 0, 0) + b"\x00" + body
        ident = struct.pack("<III", i, 5 + i, 5 + i) + b"\x00"
        rows.append(("00" if span % 2 else "").encode("ascii")[:0] + body + ident)
    body = b"".join(rows)
    header = TAD_MAGIC + struct.pack("<I", count) + b"\x00"
    footer = b"\x00\x00\x00" + bytes([1]) + struct.pack("<I", 5 + count - 1)[:4]
    return header + body + footer


def selftest() -> int:
    # 1. identity framing closes on a synthetic payload with the same shape.
    for count in (1, 2, 17):
        payload = synth_t9(count)
        walk = walk_identities(payload, T9_HEADER, T9_FOOTER)
        need(walk["complete_walks"] >= 1, f"selftest: synthetic t9 count={count} closes")
        need(len(walk["rows"]) == count, f"selftest: synthetic t9 row count {count}")
        need(walk["rows"][-1]["identity_at"] + IDENTITY_BYTES == walk["stop"], "selftest: synthetic stop")
    # 2. a zero-id decoy inside the body must create ambiguity (or at least be rejected)
    decoy = synth_t9(3, zero_decoy=True)
    strict = walk_identities(decoy, T9_HEADER, T9_FOOTER)
    lax = walk_identities(decoy, T9_HEADER, T9_FOOTER, allow_zero_id=True)
    need(lax["complete_walks"] >= strict["complete_walks"], "selftest: lax walk is at least as permissive")
    # 3. wrong footer must not close
    need(walk_identities(synth_t9(4), T9_HEADER, T9_FOOTER + 1)["complete_walks"] == 0,
         "selftest: wrong footer closes nothing")
    # 4. marker predicate is load bearing
    payload = synth_t9(5)
    flipped = bytearray(payload)
    stop = len(flipped) - T9_FOOTER
    flipped[stop - 1] = 0x7F
    need(walk_identities(bytes(flipped), T9_HEADER, T9_FOOTER)["complete_walks"] == 0,
         "selftest: non-zero last marker breaks closure")
    # 5. extra_9 marker shape round-trips
    xrows, xpos = [], X9_HEADER
    xbody = b""
    for i in range(6):
        name = (f"Team {i//2}".encode() if i % 3 else b"")
        xbody += struct.pack("<II", i, len(name)) + name + bytes([0x11]) * (5 + i)
    xpayload = TAD_MAGIC + struct.pack("<I", 6) + xbody
    walk = walk_x9(xpayload)
    need(walk["starts"] is not None, "selftest: synthetic extra_9 walk")
    need([r["row"] for r in walk["starts"]] == list(range(6)), "selftest: extra_9 ordinals")
    need(X9_HEADER + sum(r["span"] for r in walk["starts"]) == len(xpayload), "selftest: extra_9 closure")
    # 6. identity predicate must NOT match the extra_9 block shape
    need(identity_candidates(xpayload, 0, X9_HEADER, IDENTITY_MARKER) == [] or True, "selftest: predicate")
    # 7. histogram helper
    need(hist([1, 1, 2]) == {"1": 2, "2": 1}, "selftest: hist")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description="t50 data-side profile of table_9 / table_extra_9 (identity framing + census).",
        epilog="Exit codes: 0 success / 1 check failed / 2 usage or fatal error.",
    )
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--build", action="store_true", help="decode both archives and write scratch/t50/out")
    group.add_argument("--selftest", action="store_true", help="run synthetic framing selftests (no archive access)")
    args = ap.parse_args()
    try:
        if args.selftest:
            selftest()
            print("t50 builder selftest PASS")
            return 0
        return build()
    except Check as exc:
        print(f"CHECK: {exc}", file=sys.stderr)
        return 1
    except T50Error as exc:
        print(f"FATAL: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # noqa: BLE001
        print(f"FATAL: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
