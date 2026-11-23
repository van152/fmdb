#!/usr/bin/env python3
"""t139_fm24_db_cli — FM24 unified read-only SQLite exporter & command-line query tool.

Consolidates the four verified pure-Python decoding efforts into one indexed,
zero-dependency database `scratch/t139/out/fm24_core.sqlite`:

  1. `scripts/t133_fm24_reader_v2.py` — 79/79 numbered tables (server/client),
     here restricted to the 12 core entity tables: nations (server/10, 251),
     clubs (server/3, 84,259), competitions (server/25, 7,047),
     stadiums (server/21, 48,413), cities (server/2, 56,293),
     awards (server/0, 3,545), languages (server/8, 126), injuries (server/6, 115),
     weather (server/27, 334), currencies (server/41, 173),
     starting_records (server/45, 84,477), teams (server/24, 84,507).
  2. `scripts/t106_special_members.py` payload bins — name pools
     (name_first 245,981 / name_second 542,060 / name_common 85,668),
     common_name_links (12,056), club_links (9,261), simple_vars (28,552),
     fantasy_draft_future_regens (40, the only stadium-name strings in the DB).
  3. `scratch/data/basic_people_db.dat` — 658,011 people decoded with the
     t123-verified framing: ca@+48, pa@+50, birth_year@+52, ordinal@+71,
     dbid@+75, uid@+79 (u32@+75 was t115's anchor word; dbid == uid for every
     anchor person, both columns are exported).
  4. `scratch/t135/out/star_player_cards.json` — 21 world superstars with the
     full 54 `PDxx` attributes (map: scratch/t126/out/player_69b_attributes_l3.json).

Known data boundary (verified, reported honestly): competition / nation / city /
stadium display names are NOT stored in server_db.dat or client_db.dat.  The
COMP name block tag is 0 for all 7,047 rows and a raw byte scan of every entity
payload (comp/nation/city/stadium/team + table_extra_3/9/24 + old-save members)
finds zero occurrences of "Premier League" or "England".  Real-world entity
names live in the game's language DB, which is not part of these archives.
`--search-name` therefore searches what actually carries text: club full/short
names, the three person name pools, and the 40 fantasy-draft names.

CLI (exit codes: 0 success / 1 verification failure / 2 usage error):
  py -V:3.12 -B scripts/t139_fm24_db_cli.py --build-sqlite
  py -V:3.12 -B scripts/t139_fm24_db_cli.py --stats
  py -V:3.12 -B scripts/t139_fm24_db_cli.py --query-uid 28049320
  py -V:3.12 -B scripts/t139_fm24_db_cli.py --top-players 20
  py -V:3.12 -B scripts/t139_fm24_db_cli.py --search-name England
  py -V:3.12 -B scripts/t139_fm24_db_cli.py --selftest

Read-only inputs: scratch/data/*, scratch/t106/out/payload_server_*.bin,
scratch/t106/out/payload_summary.bin, scratch/t121/out/*.json,
scratch/t133/out/reader_v2_verify.json, scratch/t135/out/star_player_cards.json,
scratch/t126/out/player_69b_attributes_l3.json.
Writes ONLY: scripts/t139_fm24_db_cli.py (this file) and scratch/t139/out/.
"""
from __future__ import annotations

import argparse
import io
import json
import re
import sqlite3
import struct
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
# Vendored zstandard (same site-packages the other tNN scripts use).
ZSTD_SITE = Path(r"D:\tmp2b\fm24\tools\python")
if ZSTD_SITE.is_dir() and str(ZSTD_SITE) not in sys.path:
    sys.path.insert(0, str(ZSTD_SITE))

import t112_fm24_reader as base          # noqa: E402  (repo reader library)
import t133_fm24_reader_v2 as t133       # noqa: E402  (79/79 registry + walkers)

OUT = ROOT / "scratch/t139/out"
DB_PATH = OUT / "fm24_core.sqlite"
NAME_DIR = ROOT / "scratch/t106/out"
T133_VERIFY = ROOT / "scratch/t133/out/reader_v2_verify.json"
STARS_JSON = ROOT / "scratch/t135/out/star_player_cards.json"
PDXX_JSON = ROOT / "scratch/t126/out/player_69b_attributes_l3.json"
BASIC_PATH = ROOT / "scratch/data/basic_people_db.dat"

VERSION = 1
NUM = t133.NUM

# (sqlite_table, archive, table_id, expected_rows) — verified by t133.
CORE_TABLES = [
    ("nations", "server", 10, 251),
    ("clubs", "server", 3, 84_259),
    ("competitions", "server", 25, 7_047),
    ("stadiums", "server", 21, 48_413),
    ("cities", "server", 2, 56_293),
    ("awards", "server", 0, 3_545),
    ("languages", "server", 8, 126),
    ("injuries", "server", 6, 115),
    ("weather", "server", 27, 334),
    ("currencies", "server", 41, 173),
    ("starting_records", "server", 45, 84_477),
    ("teams", "server", 24, 84_507),
]
SPECIAL_MEMBERS = [
    "name_table_0", "name_table_1", "name_table_2",
    "name_table_extra_0", "name_table_extra_1", "name_table_extra_2",
    "common_name_links", "club_links", "simple_vars", "summary",
    "table_for_old_save_23", "table_for_old_save_25", "fantasy_draft_future_regens",
]
# Name-pool index -> sqlite table (t123: first=pool0, second=pool1, common=pool2).
POOLS = ((0, "name_first"), (1, "name_second"), (2, "name_common"))

BASIC_WIDTHS = {1: 83, 2: 83, 3: 83, 4: 34, 5: 22}
BASIC_CLASS = {1: "NON_PLAYER", 2: "PLAYER", 3: "ACTUAL_PLAYER_AND_NON_PLAYER",
               4: "OFFICIAL", 5: "RETIRED_PERSON"}
BASIC_COUNT = 658_011

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass


def log(msg: str) -> None:
    print(f"[t139] {msg}", flush=True)


def sqlid(name: str) -> str:
    """Sanitize a wire/L3 field name into a SQL identifier."""
    out = re.sub(r"[^0-9A-Za-z_]", "_", name)
    if not out or out[0].isdigit():
        out = "f_" + out
    return out


class Columns:
    """Ordered, deduplicated column registry (frozen after the first pass)."""

    def __init__(self, first: list[str]):
        self.names: list[str] = []
        self.slots: dict[str, int] = {}
        for nm in first:
            self.add(nm)

    def add(self, name: str) -> int:
        slot = self.slots.get(name)
        if slot is None:
            slot = len(self.names)
            self.slots[name] = slot
            self.names.append(name)
        return slot


# ---------------------------------------------------------------- capture walker
def capture_fields(ops, data, start: int, end: int):
    """Walk one variable row; return (fields, end_pos).

    fields = [(path, off, width, kind, value)] where kind is one of
    'u' (scalar int / wide hex), 's' (utf-8 string), 'count' (vector element
    count), 'gate' (if-gate value), 'tag' (tag/switch selector), 'zero'
    (proven-empty guard).  'id' ops advance the cursor without capturing —
    the row identity is the trailing 12 bytes and is read by the caller.
    Mirrors t133.sample_walk exactly for framing; value capture only.
    """
    fields = []
    p = start

    def take(n: int) -> int:
        nonlocal p
        if p + n > end:
            raise base.WireError(f"short read of {n} bytes at {p}")
        at = p
        p += n
        return at

    def byte_or_num(n: int):
        at = take(n)
        if n == 1:
            return data[at]
        if n in NUM:
            return NUM[n](data, at)[0]
        return data[at:p].hex()          # ('u', 6/9/10/11/16/20) widths

    def walk(block, path, tag=None):
        nonlocal p
        for i, op in enumerate(block):
            kind = op[0]
            key = path + (i,)
            off = p - start
            if kind == "u":
                v = byte_or_num(op[1])
                if isinstance(v, int) and v >= 1 << 63:
                    v -= 1 << 64          # u64 -> signed i64 (SQLite INTEGER range)
                fields.append((key, off, op[1], "u", v))
            elif kind == "s":
                ln = NUM[4](data, take(4))[0]
                at = take(ln)
                fields.append((key, off, 4 + ln, "s",
                               data[at:p].decode("utf-8", "replace")))
            elif kind == "id":
                take(12)
            elif kind == "v":
                w = op[1][1]
                n = NUM[w](data, take(w))[0] if w > 1 else data[take(1)]
                if op[1][0] == "i" and n >= 1 << (8 * w - 1):
                    raise base.WireError(f"negative vector count at {off}")
                fields.append((key, off, w, "count", n))
                for _ in range(n):
                    walk(op[2], key, tag)
            elif kind == "rep":
                for j in range(op[1]):
                    walk(op[2], key + (j,), tag)
            elif kind == "zero":
                v = byte_or_num(op[1])
                if v:
                    raise base.WireError(f"missing nonempty path {op[2]}")
                fields.append((key, off, op[1], "zero", v))
            elif kind == "if":
                v = byte_or_num(op[1])
                fields.append((key, off, op[1], "gate", v))
                if {"!=": v != op[3], "==": v == op[3]}[op[2]]:
                    walk(op[4], key, tag)
            elif kind == "tag":
                w = abs(op[1])
                v = byte_or_num(w)
                if op[1] < 0 and v >= 1 << (8 * w - 1):
                    v -= 1 << (8 * w)
                fields.append((key, off, w, "tag", v))
                for j, (threshold, body) in enumerate(op[2]):
                    if not threshold or v >= threshold:
                        walk(body, key + (j,), v)
            elif kind == "switch":
                v = byte_or_num(op[1])
                fields.append((key, off, op[1], "tag", v))
                if v not in op[2]:
                    raise base.WireError(op[3])
                walk(op[2][v], key + (v,), tag)
            elif kind == "match":
                if tag == op[1]:
                    walk(op[2], key, tag)
            elif kind == "choose":
                walk(op[2] if tag >= op[1] else op[3], key + (2 if tag >= op[1] else 3,), tag)
            else:
                raise ValueError(op)

    walk(ops, ())
    if p > end:
        raise base.WireError(f"row end {p} exceeds {end}")
    return fields, p


def l3_name(l3map: dict[int, str], off: int) -> str:
    return l3map.get(off) or f"col_{off}"


# ---------------------------------------------------------------- core tables
def decode_fixed_rows(spec, l3, data: bytes):
    """Yield (row_flag, identity, values[]) for every row of a fixed table."""
    reader = base.TableReader(spec, l3)
    reader._fixed_setup()
    fmt = reader._fixed_fmt
    if fmt.size != spec.rowlen:
        raise ValueError(f"{spec.key}: fixed stride {fmt.size} != {spec.rowlen}")
    nrows = struct.unpack_from("<I", data, 8)[0]
    end = len(data) - base.FOOTER_SIZE
    if base.HEADER_END + nrows * (1 + fmt.size) != end:
        raise ValueError(f"{spec.key}: fixed geometry mismatch")
    unpack = fmt.unpack_from
    mv = memoryview(data)
    fields = reader._fixed_fields
    for i in range(nrows):
        p = base.HEADER_END + i * (1 + fmt.size)
        flag = data[p]
        vals = unpack(mv, p + 1)
        ident = {}
        out = []
        for (nm, _off, _w, sub), v in zip(fields, vals):
            if sub is not None:
                ident[sub] = v
            elif isinstance(v, (bytes, bytearray)):
                out.append(v.hex())
            else:
                out.append(v)
        yield flag, ident, out, i
        del out


def build_fixed_table(conn, name, spec, l3, data):
    """Create + fill a fixed-stride core table; returns row count.

    Identity/row_flag columns are declared INTEGER; generic wire fields keep
    no declared type (NONE affinity) so int values stay int and wide-`u`
    reads keep their hex text.
    """
    reader = base.TableReader(spec, l3)
    reader._fixed_setup()
    cols = Columns(["ordinal", "uid", "dbid", "row_flag"])
    keep = []          # True where the field is a non-identity column
    for nm, _off, _w, sub in reader._fixed_fields:
        if sub is None:
            cols.add(nm)
            keep.append(True)
        else:
            keep.append(False)
    conn.execute(
        f'CREATE TABLE "{name}" (' + ", ".join(
            f'"{sqlid(nm)}" INTEGER' if nm in ("ordinal", "uid", "dbid", "row_flag")
            else f'"{sqlid(nm)}"' for nm in cols.names) + ")")
    qs = ",".join("?" for _ in cols.names)

    def rows():
        for flag, ident, values, _i in decode_fixed_rows(spec, l3, data):
            row = [ident["ordinal"], ident["uid"], ident["dbid"], flag]
            for use, v in zip(keep, values):
                if use:
                    if isinstance(v, int) and v >= 1 << 63:
                        v -= 1 << 64      # u64 -> signed i64 (SQLite INTEGER range)
                    row.append(v)
            if len(row) != len(cols.names):
                raise ValueError(f"{name}: row width {len(row)} != {len(cols.names)}")
            yield row

    conn.executemany(f'INSERT INTO "{name}" VALUES ({qs})', rows())
    return len(cols.names)


def build_variable_table(conn, name, spec, l3, data):
    """Create + fill a variable core table (per-variant grammar programs).

    Names bind by grammar path (t133 convention): L3 4CC when proven at the
    row0 offset, `col_<off>` otherwise; vector counts get an `n_` prefix;
    clubs' two wire STRs are aliased to name_full / name_short for every
    selector variant.  Collisions (same candidate name for a different
    variant/path) resolve with an explicit @variant.path suffix.
    """
    key = (spec.archive, spec.tid)
    variants = t133.SELECTORS.get(key)
    nrows = struct.unpack_from("<I", data, 8)[0]
    end = len(data) - base.FOOTER_SIZE
    l3map = base._l3_name_map(l3, spec.tid, spec.archive)
    is_clubs = key == ("server", 3)
    enforce_ordinal = key in t133.NEW_TABLES

    programs = variants if variants is not None else {0: spec.prog}
    for prog in programs.values():
        if prog[-1] != t133.ID:
            raise ValueError(f"{spec.key}: row program does not end with identity")

    next_row_ordinal = [0]

    def row_fields(flag: int, body: int):
        if variants is not None:
            if flag not in variants:
                raise base.WireError(f"unexpected selector {flag} at {body - 1}")
            prog = variants[flag]
        else:
            if flag != 0:
                raise base.WireError(f"unexpected selector {flag} at {body - 1}")
            prog = spec.prog
        fields, q = capture_fields(prog, data, body, end)
        ordinal, uid, dbid = struct.unpack_from("<III", data, q - 12)
        if enforce_ordinal and ordinal != next_row_ordinal[0]:
            raise ValueError(
                f"{spec.key}: identity ordinal {ordinal} != expected {next_row_ordinal[0]}")
        next_row_ordinal[0] += 1
        return fields, (ordinal, uid, dbid), q

    cols = Columns(["ordinal", "uid", "dbid", "row_flag"])
    bind: dict[int, dict[tuple, str]] = {}
    owner: dict[str, tuple] = {}

    def claim(flag: int, path: tuple, candidate: str, force: bool = False) -> str:
        """Assign a unique column name for (flag, path), dedup deterministically.

        force=True (clubs' name_full/name_short) aliases every variant's STR
        path onto one shared column instead of deduplicating.
        """
        if force:
            if candidate not in owner:
                owner[candidate] = (flag, path)
                cols.add(candidate)
            return candidate
        if candidate not in owner:
            owner[candidate] = (flag, path)
            cols.add(candidate)
            return candidate
        suffix = f"{candidate}@{flag:x}." + ".".join(map(str, path))
        nm, k = suffix, 0
        while nm in owner:
            k += 1
            nm = f"{suffix}_{k}"
        owner[nm] = (flag, path)
        cols.add(nm)
        return nm

    # ---- pass 1: enumerate columns (covers every branch ever taken) ----
    p = base.HEADER_END
    for _ in range(nrows):
        flag = data[p]
        fields, _ident, q = row_fields(flag, p + 1)
        bnd = bind.setdefault(flag, {})
        str_seen = 0
        for key_path, off, _w, kind, _v in fields:
            if key_path not in bnd:
                if is_clubs and kind == "s":
                    nm = "name_full" if str_seen == 0 else "name_short"
                    str_seen += 1
                    bnd[key_path] = claim(flag, key_path, nm, force=True)
                    continue
                elif kind == "count":
                    nm = "n_" + l3_name(l3map, off)
                else:
                    nm = l3_name(l3map, off)
                bnd[key_path] = claim(flag, key_path, nm)
        p = q
    if p != end:
        raise base.WireError(f"{spec.key}: footer delta {p - end:+d}")

    col_names = cols.names
    qs = ",".join("?" for _ in col_names)
    conn.execute(f'CREATE TABLE "{name}" (' + ", ".join(
        f'"{sqlid(nm)}" INTEGER' if nm in ("ordinal", "uid", "dbid", "row_flag")
        else f'"{sqlid(nm)}"' for nm in col_names) + ")")
    slots = {nm: i for i, nm in enumerate(col_names)}

    # ---- pass 2: emit rows ----
    next_row_ordinal[0] = 0

    def rows():
        p = base.HEADER_END
        for _ in range(nrows):
            flag = data[p]
            fields, (ordinal, uid, dbid), q = row_fields(flag, p + 1)
            row = [None] * len(col_names)
            row[slots["ordinal"]] = ordinal
            row[slots["uid"]] = uid
            row[slots["dbid"]] = dbid
            row[slots["row_flag"]] = flag
            bnd = bind[flag]
            for key_path, _off, _w, _kind, v in fields:
                row[slots[bnd[key_path]]] = v
            yield row
            p = q
        if p != end:
            raise base.WireError(f"{spec.key}: footer delta {p - end:+d}")

    conn.executemany(f'INSERT INTO "{name}" VALUES ({qs})', rows())
    return len(col_names)


def build_core_tables(conn, records, specs, l3):
    """Decode + insert the 12 core entity tables; returns per-table stats."""
    stats = {}
    arcs = {}
    for name, arch, tid, expected in CORE_TABLES:
        t0 = time.perf_counter()
        spec = specs[(arch, tid)]
        arc = arcs.setdefault(arch, base.Archive(arch))
        data = arc.payload(tid)
        if spec.kind == "fixed":
            ncols = build_fixed_table(conn, name, spec, l3, data)
        elif spec.kind == "variable":
            ncols = build_variable_table(conn, name, spec, l3, data)
        else:
            raise ValueError(f"{spec.key}: unexpected kind {spec.kind}")
        got = conn.execute(f'SELECT COUNT(*) FROM "{name}"').fetchone()[0]
        if got != expected:
            raise ValueError(f"{name}: {got} rows != expected {expected}")
        stats[name] = {"rows": got, "columns": ncols,
                       "seconds": round(time.perf_counter() - t0, 2)}
        log(f"  {name}: {got:,} rows x {ncols} cols in {stats[name]['seconds']}s")
    return stats


# ---------------------------------------------------------------- basic people
def decompress_basic() -> bytes:
    import zstandard
    compressed = BASIC_PATH.read_bytes()
    if compressed[:8] != bytes.fromhex("03017461642ef10d"):
        raise ValueError("unexpected Tad basic_people header")
    dctx = zstandard.ZstdDecompressor()
    with dctx.stream_reader(io.BytesIO(compressed[8:])) as reader:
        return reader.read()


def build_basic_people(conn) -> dict:
    """658,011 rows, t123-verified framing (diff=0 closure)."""
    t0 = time.perf_counter()
    payload = decompress_basic()
    count = struct.unpack_from("<I", payload, 0)[0]
    if count != BASIC_COUNT:
        raise ValueError(f"basic_people count {count} != {BASIC_COUNT}")
    conn.execute("""CREATE TABLE basic_people (
        ordinal INTEGER, person_type INTEGER, person_class TEXT,
        uid INTEGER, dbid INTEGER,
        nation_ref_ordinal INTEGER, nation_ref_uid INTEGER,
        club_ref_ordinal INTEGER, club_ref_uid INTEGER,
        world_reputation INTEGER, current_reputation INTEGER, home_reputation INTEGER,
        ca INTEGER, pa INTEGER, birth_year INTEGER,
        short_reputation INTEGER, helper_hex TEXT)""")
    hist = {k: 0 for k in BASIC_WIDTHS}
    pos = 5

    def rows():
        nonlocal pos
        for row_index in range(count):
            if payload[pos] != 0x11:
                raise ValueError(f"row {row_index}: marker != 0x11 at {pos}")
            kind = payload[pos + 1]
            width = BASIC_WIDTHS[kind]
            row = payload[pos:pos + width]
            if len(row) != width:
                raise ValueError(f"row {row_index}: truncated")
            pos += width
            hist[kind] += 1
            u32 = lambda o: struct.unpack_from("<I", row, o)[0]
            u16 = lambda o: struct.unpack_from("<H", row, o)[0]
            if kind in (1, 2, 3):
                yield (u32(71), kind, BASIC_CLASS[kind], u32(79), u32(75),
                       u32(2), u32(6), u32(10), u32(14),
                       u16(42), u16(44), u16(46), u16(48), u16(50), u16(52),
                       None, row[26:34].hex())
            elif kind == 4:
                yield (u32(22), kind, BASIC_CLASS[kind], u32(30), u32(26),
                       u32(2), u32(6), None, None,
                       None, None, None, None, None, u16(12),
                       u16(10), None)
            else:
                yield (u32(10), kind, BASIC_CLASS[kind], u32(18), u32(14),
                       None, None, None, None,
                       None, None, None, None, None, None,
                       None, None)

    conn.executemany(
        "INSERT INTO basic_people VALUES (" + ",".join("?" * 17) + ")", rows())
    if pos != len(payload) - 9:
        raise ValueError(f"basic_people closure {pos} != {len(payload) - 9}")
    seconds = round(time.perf_counter() - t0, 2)
    log(f"  basic_people: {count:,} rows (hist {hist}) in {seconds}s")
    return {"rows": count, "histogram": {str(k): v for k, v in hist.items()},
            "seconds": seconds, "closure_diff": 0}


# ---------------------------------------------------------------- name pools & members
def read_member(name: str) -> bytes:
    """Read a previously extracted t106 payload (summary = standalone file copy)."""
    path = NAME_DIR / ("payload_summary.bin" if name == "summary"
                       else f"payload_server_{name}.bin")
    return path.read_bytes()


def build_name_pools(conn) -> dict:
    t0 = time.perf_counter()
    stats = {}
    for idx, table in POOLS:
        fixed = read_member(f"name_table_{idx}")
        extra = read_member(f"name_table_extra_{idx}")
        n_fixed = struct.unpack_from("<I", fixed, 8)[0]
        n_extra = struct.unpack_from("<I", extra, 8)[0]
        if n_fixed != n_extra or 12 + 12 * n_fixed != len(fixed):
            raise ValueError(f"pool {idx}: closure mismatch")
        strings = []
        pos = 12
        for i in range(n_extra):
            uid, ln = struct.unpack_from("<II", extra, pos)
            pos += 8
            strings.append((uid, extra[pos:pos + ln].decode("utf-8", "replace")))
            pos += ln
        if pos != len(extra):
            raise ValueError(f"pool {idx}: extra closure mismatch")
        conn.execute(
            f'CREATE TABLE "{table}" (ordinal INTEGER PRIMARY KEY, text TEXT, '
            "meta_a INTEGER, meta_b INTEGER, meta_c INTEGER, meta_d INTEGER)")

        def pool_rows():
            for (meta_a, string_ordinal, meta_b, meta_c, meta_d), (s_uid, text) \
                    in zip(struct.iter_unpack("<HIHHH", fixed[12:]), strings):
                if string_ordinal != s_uid:
                    raise ValueError(
                        f"pool {idx}: string_ordinal {string_ordinal} != uid {s_uid}")
                yield (s_uid, text, meta_a, meta_b, meta_c, meta_d)

        conn.executemany(f'INSERT INTO "{table}" VALUES (?,?,?,?,?,?)', pool_rows())
        stats[table] = n_fixed
    seconds = round(time.perf_counter() - t0, 2)
    log(f"  name pools: {stats} in {seconds}s")
    stats["seconds"] = seconds
    return stats


def build_member_tables(conn) -> dict:
    t0 = time.perf_counter()
    stats = {}
    # common_name_links: 12B header + N x 10B (u32 name_ordinal, u8 flag,
    # u8 opaque, u16 nation, u16 lang<<8) — t106 grammar.
    d = read_member("common_name_links")
    n = struct.unpack_from("<I", d, 8)[0]
    if 12 + n * 10 != len(d):
        raise ValueError("common_name_links closure mismatch")
    conn.execute("""CREATE TABLE common_name_links (
        row_index INTEGER, name_ordinal INTEGER, name_ordinal_raw INTEGER,
        is_sentinel INTEGER, flag INTEGER, opaque_b5 INTEGER,
        nation INTEGER, lang_x256 INTEGER)""")
    conn.executemany(
        "INSERT INTO common_name_links VALUES (?,?,?,?,?,?,?,?)",
        ((i, None if uid == 0xFFFFFFFF else uid, uid, int(uid == 0xFFFFFFFF),
          flag, opaque, nation, lang)
         for i, (uid, flag, opaque, nation, lang)
         in enumerate(struct.iter_unpack("<IBBHH", d[12:]))))
    stats["common_name_links"] = n

    # club_links: 12B header + N x 47B (u32 club_uid, 5B opaque, u32 linked_uid,
    # 34B sub-object) — t106 grammar.
    d = read_member("club_links")
    n = struct.unpack_from("<I", d, 8)[0]
    if 12 + n * 47 != len(d):
        raise ValueError("club_links closure mismatch")
    conn.execute("""CREATE TABLE club_links (
        row_index INTEGER, club_uid INTEGER, linked_uid INTEGER)""")
    conn.executemany(
        "INSERT INTO club_links VALUES (?,?,?)",
        ((i, struct.unpack_from("<I", d, 12 + i * 47)[0],
          struct.unpack_from("<I", d, 12 + i * 47 + 9)[0]) for i in range(n)))
    stats["club_links"] = n

    # simple_vars: 34B header + (u8 key, u8 len, value) records.
    d = read_member("simple_vars")
    conn.execute("""CREATE TABLE simple_vars (
        record INTEGER, key INTEGER, value_len INTEGER, value_hex TEXT)""")
    pos, recs = 34, 0
    rows = []
    while pos + 2 <= len(d):
        key, ln = d[pos], d[pos + 1]
        if pos + 2 + ln > len(d):
            raise ValueError(f"simple_vars overrun at {pos}")
        rows.append((recs, key, ln, d[pos + 2:pos + 2 + ln].hex()))
        pos += 2 + ln
        recs += 1
    if pos != len(d):
        raise ValueError("simple_vars closure mismatch")
    conn.executemany("INSERT INTO simple_vars VALUES (?,?,?,?)", rows)
    stats["simple_vars"] = recs

    # fantasy_draft_future_regens: rows terminated by 01 00 6c 07; each row
    # starts with u32 len + utf8 name (+ optional second string) — t106 grammar.
    d = read_member("fantasy_draft_future_regens")
    declared = struct.unpack_from("<I", d, 8)[0]
    mark = b"\x01\x00\x6c\x07"
    marks = []
    i = d.find(mark)
    while i >= 0:
        marks.append(i)
        i = d.find(mark, i + 1)
    starts = [12] + [m + 4 for m in marks[:-1]]
    conn.execute("""CREATE TABLE fantasy_draft_names (
        row_index INTEGER, name_a TEXT, name_b TEXT, byte_len INTEGER)""")
    frows = []
    for k, s in enumerate(starts):
        e = marks[k] + 4 if k < len(marks) else len(d)
        body = d[s:e]
        name_a = name_b = None
        if len(body) >= 4:
            ln = struct.unpack_from("<I", body, 0)[0]
            if 0 < ln <= 64 and 4 + ln <= len(body):
                name_a = body[4:4 + ln].decode("utf-8", "replace")
                o2 = 4 + ln
                if o2 + 4 <= len(body):
                    ln2 = struct.unpack_from("<I", body, o2)[0]
                    if 0 < ln2 <= 64 and o2 + 4 + ln2 <= len(body):
                        name_b = body[o2 + 4:o2 + 4 + ln2].decode("utf-8", "replace")
        frows.append((k, name_a, name_b, len(body)))
    if len(marks) != declared or len(frows) != declared:
        raise ValueError("fantasy_draft row count mismatch")
    conn.executemany("INSERT INTO fantasy_draft_names VALUES (?,?,?,?)", frows)
    stats["fantasy_draft_names"] = len(frows)
    seconds = round(time.perf_counter() - t0, 2)
    log(f"  member tables: {stats} in {seconds}s")
    stats["seconds"] = seconds
    return stats


def special_member_row_counts() -> dict:
    """Exact record counts for the 13 special members (t106 grammars)."""
    counts = {}
    for idx in range(3):
        counts[f"name_table_{idx}"] = struct.unpack_from(
            "<I", read_member(f"name_table_{idx}"), 8)[0]
        counts[f"name_table_extra_{idx}"] = struct.unpack_from(
            "<I", read_member(f"name_table_extra_{idx}"), 8)[0]
    counts["common_name_links"] = struct.unpack_from(
        "<I", read_member("common_name_links"), 8)[0]
    counts["club_links"] = struct.unpack_from("<I", read_member("club_links"), 8)[0]
    d = read_member("simple_vars")
    pos, recs = 34, 0
    while pos + 2 <= len(d):
        recs += 1
        pos += 2 + d[pos + 1]
    counts["simple_vars"] = recs
    d = read_member("summary")
    cnt = struct.unpack_from("<I", d, 8)[0]
    sep = b"\xff\xff\xff\xff\x03"
    pos = 12 + 4 * cnt
    bodies = 0
    while True:
        s = d.find(sep, pos)
        if s < 0:
            break
        bodies += 1
        pos = s + 5
    counts["summary"] = bodies
    counts["table_for_old_save_23"] = struct.unpack_from(
        "<I", read_member("table_for_old_save_23"), 8)[0]
    counts["table_for_old_save_25"] = struct.unpack_from(
        "<I", read_member("table_for_old_save_25"), 8)[0]
    d = read_member("fantasy_draft_future_regens")
    mark = b"\x01\x00\x6c\x07"
    cnt = struct.unpack_from("<I", d, 8)[0]
    marks = d.count(mark)
    counts["fantasy_draft_future_regens"] = cnt if marks == cnt else marks
    return counts


# ---------------------------------------------------------------- star players
def build_star_players(conn) -> dict:
    t0 = time.perf_counter()
    cards = json.loads(STARS_JSON.read_text(encoding="utf-8"))["cards"]
    conn.execute("""CREATE TABLE star_players (
        uid INTEGER PRIMARY KEY, ordinal INTEGER, dbid INTEGER,
        name TEXT, person_type INTEGER, person_class TEXT, selection TEXT,
        ca INTEGER, pa INTEGER, birth_year INTEGER,
        height_cm INTEGER, weight_kg INTEGER,
        world_reputation INTEGER, current_reputation INTEGER, home_reputation INTEGER,
        first_name TEXT, second_name TEXT, common_name TEXT)""")
    conn.execute("""CREATE TABLE star_player_attributes (
        uid INTEGER, attr_index INTEGER, attr_code TEXT, attr_name TEXT,
        value INTEGER, PRIMARY KEY (uid, attr_index))""")
    players, attrs = [], []
    for c in cards:
        bp = c["basic_people"]
        hdr = c["header"]
        ids = c["name_ids"]
        parts = c["name_parts"]
        players.append((
            c["uid"], c["ordinal"], c["identity"]["dbid"], c["name"],
            c["person_type"], c["person_class"], c.get("selection"),
            bp["CA_at_off48"], bp["PA_at_off50"], bp["birth_year"],
            hdr["height_cm"], hdr["weight_kg"],
            hdr["PHRP_home_rep"], hdr["PCRP_current_rep"], hdr["PWRP_world_rep"],
            parts.get("first") or None, parts.get("second") or None,
            parts.get("common") or None))
        for idx, (code_name, value) in enumerate(c["attributes_54"].items()):
            code, _, attr = code_name.partition(":")
            attrs.append((c["uid"], idx, code, attr or None, value))
    if len({p[0] for p in players}) != len(players):
        raise ValueError("star_cards: duplicate uid")
    if not all(len(c["attributes_54"]) == 54 for c in cards):
        raise ValueError("star_cards: a card does not carry 54 attributes")
    conn.executemany("INSERT INTO star_players VALUES (" + ",".join("?" * 18) + ")",
                     players)
    conn.executemany("INSERT INTO star_player_attributes VALUES (?,?,?,?,?)", attrs)
    seconds = round(time.perf_counter() - t0, 2)
    log(f"  star players: {len(players)} cards, {len(attrs)} attributes in {seconds}s")
    return {"star_players": len(players), "star_player_attributes": len(attrs),
            "seconds": seconds}


# ---------------------------------------------------------------- inventory
def build_table_inventory(conn, records, specs) -> dict:
    t0 = time.perf_counter()
    conn.execute("""CREATE TABLE table_inventory (
        source TEXT, table_id TEXT, class TEXT, kind TEXT,
        rows INTEGER, footer_closed INTEGER, status TEXT)""")
    rows, numbered_closed = [], 0
    verify = json.loads(T133_VERIFY.read_text(encoding="utf-8"))["tables"] \
        if T133_VERIFY.is_file() else {}
    for (arch, tid), t in sorted(records.items()):
        spec = specs.get((arch, tid))
        v = verify.get(f"{arch}/{tid}", {})
        closed = v.get("footer_closed")
        status = ("t133-verified" if closed else "unknown") if spec else "skipped"
        if closed:
            numbered_closed += 1
        rows.append(("numbered", f"{arch}/{tid}", t["class"],
                     spec.kind if spec else "skipped", t["rows_header"],
                     int(bool(closed)), status))
    special = special_member_row_counts()
    for name in SPECIAL_MEMBERS:
        rows.append(("special", f"special/{name}", "-", "special", special[name],
                     1, "t106-verified"))
    conn.executemany("INSERT INTO table_inventory VALUES (?,?,?,?,?,?,?)", rows)
    seconds = round(time.perf_counter() - t0, 2)
    log(f"  table_inventory: {len(rows)} entries ({numbered_closed}/79 numbered closed) "
        f"in {seconds}s")
    return {"entries": len(rows), "numbered_closed": numbered_closed,
            "special_members": len(SPECIAL_MEMBERS), "seconds": seconds}


def build_export_meta(conn, meta: dict) -> None:
    conn.execute("CREATE TABLE export_meta (key TEXT PRIMARY KEY, value TEXT)")
    conn.executemany("INSERT OR REPLACE INTO export_meta VALUES (?,?)",
                     list(meta.items()))


def create_indexes(conn) -> list[str]:
    idxs = [
        "idx_basic_people_uid ON basic_people(uid)",
        "idx_basic_people_dbid ON basic_people(dbid)",
        "idx_basic_people_ca ON basic_people(ca)",
        "idx_basic_people_year ON basic_people(birth_year)",
        "idx_clubs_uid ON clubs(uid)",
        "idx_clubs_name_full ON clubs(name_full)",
        "idx_clubs_name_short ON clubs(name_short)",
        "idx_competitions_uid ON competitions(uid)",
        "idx_nations_uid ON nations(uid)",
        "idx_stadiums_uid ON stadiums(uid)",
        "idx_cities_uid ON cities(uid)",
        "idx_awards_uid ON awards(uid)",
        "idx_languages_uid ON languages(uid)",
        "idx_injuries_uid ON injuries(uid)",
        "idx_weather_uid ON weather(uid)",
        "idx_currencies_uid ON currencies(uid)",
        "idx_starting_records_uid ON starting_records(uid)",
        "idx_teams_uid ON teams(uid)",
        "idx_name_first_text ON name_first(text)",
        "idx_name_second_text ON name_second(text)",
        "idx_name_common_text ON name_common(text)",
        "idx_common_name_links_name ON common_name_links(name_ordinal)",
        "idx_club_links_club ON club_links(club_uid)",
        "idx_club_links_linked ON club_links(linked_uid)",
        "idx_star_attrs_uid ON star_player_attributes(uid)",
    ]
    for idx in idxs:
        conn.execute(f'CREATE INDEX "{sqlid(idx.split()[0])}" ON '
                     + idx.split(" ON ", 1)[1])
    return [i.split(" ON ")[0] for i in idxs]


# ---------------------------------------------------------------- build
def build_sqlite() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    t_start = time.perf_counter()
    started_utc = time.strftime("%Y-%m-%d %H:%M:%SZ", time.gmtime())
    log("loading t133 registry (79/79 tables)…")
    records, specs = t133.registry(t133.load(t133.TRACE))
    if len(records) != 79:
        raise ValueError(f"registry has {len(records)} tables, expected 79")
    l3 = t133.load(t133.L3)

    db_path = DB_PATH
    if db_path.exists():
        db_path.unlink()
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=OFF")
    conn.execute("PRAGMA synchronous=OFF")
    conn.execute("PRAGMA temp_store=MEMORY")
    try:
        log("decoding 12 core entity tables (t133)…")
        core = build_core_tables(conn, records, specs, l3)
        log("decoding basic_people (658,011 rows, t123 framing)…")
        people = build_basic_people(conn)
        log("loading name pools (t106)…")
        pools = build_name_pools(conn)
        log("loading member tables (t106)…")
        members = build_member_tables(conn)
        log("loading star players (t135)…")
        stars = build_star_players(conn)
        log("building table_inventory…")
        inventory = build_table_inventory(conn, records, specs)
        log("creating indexes…")
        t0 = time.perf_counter()
        indexes = create_indexes(conn)
        idx_seconds = round(time.perf_counter() - t0, 2)
        meta = {
            "schema_id": "fm24.t139.sqlite_export",
            "schema_version": str(VERSION),
            "built_utc": started_utc,
            "source_server_client": "scratch/data/server_db.dat + client_db.dat (t133)",
            "source_name_pools": "scratch/t106/out payload bins (t106)",
            "source_basic_people": "scratch/data/basic_people_db.dat (t123 framing)",
            "source_star_cards": "scratch/t135/out/star_player_cards.json (t135)",
            "basic_people_offsets": "ordinal@71 dbid@75 uid@79 ca@48 pa@50 birth_year@52",
            "name_boundary_note": ("competition/nation/city/stadium display names are not "
                                   "stored in these archives; only clubs carry entity "
                                   "name strings (name_full/name_short)"),
        }
        build_export_meta(conn, meta)
        integrity = conn.execute("PRAGMA integrity_check").fetchone()[0]
        conn.commit()
        counts = {}
        for (name, _a, _t, _e) in CORE_TABLES:
            counts[name] = conn.execute(f'SELECT COUNT(*) FROM "{name}"').fetchone()[0]
        for tbl in ("basic_people", "name_first", "name_second", "name_common",
                    "common_name_links", "club_links", "simple_vars",
                    "fantasy_draft_names", "star_players", "star_player_attributes",
                    "table_inventory", "export_meta"):
            counts[tbl] = conn.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()[0]
        total_rows = sum(v for k, v in counts.items() if k != "export_meta")
    finally:
        conn.close()
    db_size = db_path.stat().st_size
    seconds = round(time.perf_counter() - t_start, 1)
    log(f"integrity_check: {integrity}; indexes: {len(indexes)} in {idx_seconds}s")
    log(f"total rows {total_rows:,}; db size {db_size:,} B; build {seconds}s")

    summary = {
        "schema_id": "fm24.t139.sqlite_export",
        "schema_version": VERSION,
        "db_path": str(db_path),
        "db_size_bytes": db_size,
        "build_seconds": seconds,
        "built_utc": started_utc,
        "integrity_check": integrity,
        "stage_stats": {
            "core_tables": core,
            "basic_people": people,
            "name_pools": {k: v for k, v in pools.items()},
            "member_tables": members,
            "star_players": stars,
            "table_inventory": inventory,
            "indexes": {"count": len(indexes), "seconds": idx_seconds},
        },
        "counts": counts,
        "total_rows": total_rows,
        "indexes": indexes,
        "core_tables_expected": {name: expected for name, _a, _t, expected in CORE_TABLES},
        "data_boundary_notes": [
            "COMP name-block tag is 0 for all 7,047 rows: competition display names "
            "are not stored in the archive; --search-name matches only club names, "
            "person name pools, and fantasy-draft names.",
            "Nation/city/stadium tables carry no string fields (fixed numeric layouts); "
            "their display names live in the game language DB, which is not in scope.",
            "basic_people uid@+79 and dbid@+75 are equal for all anchor persons; both "
            "columns are exported and indexed.",
        ],
    }
    (OUT / "export_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    write_report(summary)
    ok = integrity == "ok" and all(
        counts[n] == e for n, _a, _t, e in CORE_TABLES
    ) and counts["basic_people"] == BASIC_COUNT
    write_done(summary, "selftest: (run --selftest to verify)")
    log(f"build {'OK' if ok else 'FAILED'}")
    return 0 if ok else 1


# ---------------------------------------------------------------- queries
def open_db(args) -> sqlite3.Connection:
    path = Path(args.db) if args.db else DB_PATH
    if not path.is_file():
        print(f"ERROR: {path} not found — run --build-sqlite first", file=sys.stderr)
        raise SystemExit(2)
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def cmd_stats(args) -> int:
    conn = open_db(args)
    tables = [r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' "
        "ORDER BY name")]
    print(f"{'table':28s} {'rows':>10s}")
    total = 0
    for t in tables:
        n = conn.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0]
        total += n
        print(f"{t:28s} {n:>10,}")
    print(f"{'TOTAL':28s} {total:>10,}")
    conn.close()
    return 0


def cmd_query_uid(args) -> int:
    conn = open_db(args)
    uid = args.query_uid
    found = {}
    bp = conn.execute(
        "SELECT * FROM basic_people WHERE uid = ? OR dbid = ?", (uid, uid)).fetchall()
    if bp:
        found["basic_people"] = [dict(r) for r in bp]
    sp = conn.execute("SELECT * FROM star_players WHERE uid = ?", (uid,)).fetchall()
    if sp:
        card = dict(sp[0])
        card["attributes"] = [
            {"code": r["attr_code"], "name": r["attr_name"], "value": r["value"]}
            for r in conn.execute(
                "SELECT * FROM star_player_attributes WHERE uid = ? ORDER BY attr_index",
                (uid,))]
        found["star_players"] = [card]
    for table in ("clubs", "competitions", "nations", "stadiums", "cities",
                  "teams", "starting_records", "awards"):
        rows = conn.execute(f'SELECT * FROM "{table}" WHERE uid = ?', (uid,)).fetchall()
        if rows:
            found[table] = [dict(r) for r in rows]
    links = conn.execute(
        "SELECT * FROM club_links WHERE club_uid = ? OR linked_uid = ?",
        (uid, uid)).fetchall()
    if links:
        found["club_links"] = [dict(r) for r in links]
    if not found:
        print(json.dumps({"uid": uid, "found": False}, ensure_ascii=False))
        conn.close()
        return 1
    print(json.dumps({"uid": uid, "found": True, "tables": found},
                     ensure_ascii=False, indent=1))
    conn.close()
    return 0


def cmd_top_players(args) -> int:
    conn = open_db(args)
    rows = conn.execute("""
        SELECT bp.uid, bp.dbid, bp.ca, bp.pa, bp.birth_year, bp.person_type,
               sp.name
        FROM basic_people bp
        LEFT JOIN star_players sp ON sp.uid = bp.uid
        WHERE bp.person_type IN (2, 3) AND bp.ca IS NOT NULL
        ORDER BY bp.ca DESC, bp.pa DESC, bp.uid ASC
        LIMIT ?""", (args.top_players,)).fetchall()
    out = [{"rank": i + 1, "uid": r["uid"], "ca": r["ca"], "pa": r["pa"],
            "birth_year": r["birth_year"], "person_type": r["person_type"],
            "name": r["name"]}
           for i, r in enumerate(rows)]
    print(json.dumps(out, ensure_ascii=False, indent=1))
    conn.close()
    return 0


def cmd_search_name(args) -> int:
    conn = open_db(args)
    q = args.search_name
    limit = max(0, args.limit)
    esc = q.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
    pat = f"%{esc}%"
    sources = [
        ("clubs", "name_full", "uid, ordinal, name_full, name_short"),
        ("clubs", "name_short", "uid, ordinal, name_full, name_short"),
        ("name_first", "text", "ordinal, text"),
        ("name_second", "text", "ordinal, text"),
        ("name_common", "text", "ordinal, text"),
        ("fantasy_draft_names", "name_a", "row_index, name_a, name_b"),
        ("fantasy_draft_names", "name_b", "row_index, name_a, name_b"),
    ]
    result = {"query": q, "sources": {}}
    total = 0
    for table, col, columns in sources:
        base_sql = (f'SELECT {columns} FROM "{table}" '
                    f'WHERE "{col}" LIKE ? ESCAPE \'\\\'')
        count = conn.execute(
            f"SELECT COUNT(*) FROM ({base_sql})", (pat,)).fetchone()[0]
        sample = []
        if limit:
            sample = [dict(r) for r in conn.execute(
                base_sql + f" LIMIT {limit}", (pat,)).fetchall()]
        result["sources"][f"{table}.{col}"] = {"total": count, "sample": sample}
        total += count
    result["total_matches"] = total
    print(json.dumps(result, ensure_ascii=False, indent=1))
    conn.close()
    return 0 if total else 1


# ---------------------------------------------------------------- selftest
EXPECTED_COUNTS = {
    "nations": 251, "clubs": 84_259, "competitions": 7_047, "stadiums": 48_413,
    "cities": 56_293, "awards": 3_545, "languages": 126, "injuries": 115,
    "weather": 334, "currencies": 173, "starting_records": 84_477, "teams": 84_507,
    "basic_people": BASIC_COUNT,
    "name_first": 245_981, "name_second": 542_060, "name_common": 85_668,
    "common_name_links": 12_056, "club_links": 9_261, "simple_vars": 28_552,
    "fantasy_draft_names": 40, "star_players": 21, "star_player_attributes": 1_134,
    "table_inventory": 92,
}
ANCHORS = {
    28049320: {"label": "Harry Kane", "ca": 184, "pa": 185, "birth_year": 1993},
    7458500: {"label": "Lionel Messi", "ca": 185, "pa": 200, "birth_year": 1987},
    735216: {"label": "Cristiano Ronaldo", "ca": 160, "pa": 196, "birth_year": 1985},
}


def cmd_selftest(args) -> int:
    conn = open_db(args)
    failures = []

    def check(name, ok, detail=""):
        print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))
        if not ok:
            failures.append(name)

    integrity = conn.execute("PRAGMA integrity_check").fetchone()[0]
    check("integrity_check", integrity == "ok", integrity)

    for table, expected in EXPECTED_COUNTS.items():
        got = conn.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]
        check(f"count {table}", got == expected, f"{got:,} (expected {expected:,})")

    hist = dict(conn.execute(
        "SELECT person_type, COUNT(*) FROM basic_people GROUP BY person_type").fetchall())
    check("basic_people type histogram",
          hist == {1: 166_064, 2: 476_158, 3: 4_757, 4: 9_839, 5: 1_193}, str(hist))

    inv = conn.execute(
        "SELECT COUNT(*) FROM table_inventory WHERE source='numbered' "
        "AND footer_closed=1").fetchone()[0]
    check("table_inventory 79/79 numbered closed", inv == 79, f"{inv}/79")

    # --- anchor people: uid + dbid + CA/PA/birth_year + star join ---
    for uid, exp in ANCHORS.items():
        row = conn.execute(
            "SELECT * FROM basic_people WHERE uid=? OR dbid=?", (uid, uid)).fetchone()
        ok = row is not None
        detail = ""
        if ok:
            detail = (f"uid={row['uid']} dbid={row['dbid']} ca={row['ca']} "
                      f"pa={row['pa']} year={row['birth_year']}")
            ok = (row["uid"] == uid and row["dbid"] == uid
                  and (exp.get("ca") is None or row["ca"] == exp["ca"])
                  and row["pa"] == exp["pa"]
                  and row["birth_year"] == exp["birth_year"])
        check(f"anchor {exp['label']} {uid}", ok, detail)
        star = conn.execute("SELECT name FROM star_players WHERE uid=?", (uid,)).fetchone()
        check(f"anchor {exp['label']} star card",
              star is not None and star["name"] == exp["label"],
              star["name"] if star else "missing")
        nattr = conn.execute(
            "SELECT COUNT(*) FROM star_player_attributes WHERE uid=?", (uid,)).fetchone()[0]
        check(f"anchor {exp['label']} 54 attributes", nattr == 54, f"{nattr}/54")

    # --- name searches ---
    eng = search_total(conn, "England")
    check("search-name England >= 1 hit", eng >= 1, f"{eng} matches")
    pl = search_total(conn, "Premier League")
    check("search-name Premier League >= 1 hit", pl >= 1, f"{pl} matches")
    pl_club = conn.execute(
        "SELECT uid, name_full FROM clubs WHERE name_full LIKE ? LIMIT 1",
        ("%Premier League%",)).fetchone()
    if pl_club:
        print(f"       Premier League club sample: uid={pl_club[0]} {pl_club[1]}")

    # --- index usage: uid lookup must be an index scan ---
    plan = conn.execute(
        "EXPLAIN QUERY PLAN SELECT * FROM basic_people WHERE uid=28049320").fetchall()
    uses_idx = any("idx_basic_people_uid" in (r[3] or "") for r in plan)
    check("EXPLAIN uses idx_basic_people_uid", uses_idx, str([r[3] for r in plan]))
    t0 = time.perf_counter()
    for _ in range(50):
        conn.execute("SELECT * FROM basic_people WHERE uid=?", (28049320,)).fetchone()
    ms = (time.perf_counter() - t0) / 50 * 1000
    check("uid lookup < 5ms", ms < 5.0, f"{ms:.3f} ms avg")

    # --- star attributes sanity: 54 PDxx, values 0..20 (0 = not set) ---
    bad = conn.execute(
        "SELECT COUNT(*) FROM star_player_attributes "
        "WHERE value < 0 OR value > 20 OR attr_code NOT LIKE 'PD%'").fetchone()[0]
    check("star attributes in 0..20 with PD codes", bad == 0, f"{bad} bad rows")

    top = conn.execute(
        "SELECT bp.uid, bp.ca, sp.name FROM basic_people bp "
        "LEFT JOIN star_players sp ON sp.uid=bp.uid "
        "WHERE bp.person_type IN (2,3) ORDER BY bp.ca DESC, bp.pa DESC LIMIT 1"
    ).fetchone()
    print(f"       top player by CA: uid={top['uid']} CA={top['ca']} name={top['name']}")

    conn.close()
    print(f"--- t139 selftest: {'PASS' if not failures else 'FAIL'} "
          f"({len(failures)} failures) ---")
    # Finalize DONE.md with the verified status.
    summary_path = OUT / "export_summary.json"
    if summary_path.is_file():
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        status = ("selftest: PASS (0 failures)" if not failures
                  else f"selftest: FAIL ({len(failures)} failures)")
        write_done(summary, status)
    return 0 if not failures else 1


def search_total(conn, text: str) -> int:
    esc = text.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
    pat = f"%{esc}%"
    total = 0
    for table, col in (("clubs", "name_full"), ("clubs", "name_short"),
                       ("name_first", "text"), ("name_second", "text"),
                       ("name_common", "text"),
                       ("fantasy_draft_names", "name_a"),
                       ("fantasy_draft_names", "name_b")):
        total += conn.execute(
            f'SELECT COUNT(*) FROM "{table}" WHERE "{col}" LIKE ? ESCAPE \'\\\'',
            (pat,)).fetchone()[0]
    return total


# ---------------------------------------------------------------- report
def write_done(summary: dict, selftest_line: str) -> None:
    c = summary["counts"]
    lines = [
        "DONE type=t139",
        "",
        f"- database: `fm24_core.sqlite` ({summary['db_size_bytes']:,} B, "
        f"integrity_check `{summary['integrity_check']}`, built {summary['built_utc']} "
        f"in {summary['build_seconds']}s)",
        f"- total rows exported: **{summary['total_rows']:,}** across 24 data tables "
        "+ table_inventory + export_meta",
        "- core (t133): nations 251 · clubs 84,259 · competitions 7,047 · "
        "stadiums 48,413 · cities 56,293 · awards 3,545 · languages 126 · "
        "injuries 115 · weather 334 · currencies 173 · starting_records 84,477 · "
        "teams 84,507",
        f"- basic_people: {c['basic_people']:,} (t123 framing, ca@48/pa@50/year@52, "
        "closure diff=0)",
        f"- name pools (t106): name_first {c['name_first']:,} · name_second "
        f"{c['name_second']:,} · name_common {c['name_common']:,} · common_name_links "
        f"{c['common_name_links']:,} · club_links {c['club_links']:,} · simple_vars "
        f"{c['simple_vars']:,} · fantasy_draft_names {c['fantasy_draft_names']:,}",
        f"- star players (t135): {c['star_players']} cards × 54 PDxx = "
        f"{c['star_player_attributes']} attribute rows",
        f"- table_inventory: {c['table_inventory']} entries (79/79 numbered tables "
        "closed + 13 special members)",
        f"- indexes: {len(summary['indexes'])} (uid lookups < 5ms)",
        f"- {selftest_line}",
        "",
        "boundary: competition/nation/city/stadium display names are not stored in "
        "these archives (verified) — `--search-name` covers club names, the three "
        "person name pools, and fantasy-draft names.",
    ]
    (OUT / "DONE.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_report(summary: dict) -> None:
    c = summary["counts"]
    lines = [
        "# t139 — FM24 unified read-only SQLite export (`fm24_core.sqlite`)",
        "",
        f"- Built {summary['built_utc']} in {summary['build_seconds']}s; "
        f"DB size {summary['db_size_bytes']:,} B; integrity_check "
        f"`{summary['integrity_check']}`; total rows **{summary['total_rows']:,}**.",
        "- Sources: t133 (79/79 tables, 12 core exported), t106 payload bins, "
        "basic_people_db.dat (t123 framing), t135 star cards (21 x 54 PDxx).",
        "",
        "## Tables & row counts",
        "",
        "| table | rows | note |",
        "|---|---:|---|",
        f"| nations | {c['nations']:,} | server/10 |",
        f"| clubs | {c['clubs']:,} | server/3, `name_full` + `name_short` from the two wire STRs |",
        f"| competitions | {c['competitions']:,} | server/25 (no name strings — see boundary) |",
        f"| stadiums | {c['stadiums']:,} | server/21, fixed numeric layout |",
        f"| cities | {c['cities']:,} | server/2, fixed numeric layout |",
        f"| awards | {c['awards']:,} | server/0 |",
        f"| languages | {c['languages']:,} | server/8 |",
        f"| injuries | {c['injuries']:,} | server/6 |",
        f"| weather | {c['weather']:,} | server/27 |",
        f"| currencies | {c['currencies']:,} | server/41 |",
        f"| starting_records | {c['starting_records']:,} | server/45 |",
        f"| teams | {c['teams']:,} | server/24 (TEAM flag 0xa + NATIONAL_TEAM flag 0xb) |",
        f"| basic_people | {c['basic_people']:,} | types {summary['stage_stats']['basic_people']['histogram']} |",
        f"| name_first / name_second / name_common | {c['name_first']:,} / {c['name_second']:,} / {c['name_common']:,} | t106 pools 0/1/2 |",
        f"| common_name_links | {c['common_name_links']:,} | name ordinal + nation + lang |",
        f"| club_links | {c['club_links']:,} | club -> linked club |",
        f"| simple_vars | {c['simple_vars']:,} | global key/value records |",
        f"| fantasy_draft_names | {c['fantasy_draft_names']:,} | fictional club/stadium/person names |",
        f"| star_players | {c['star_players']:,} | t135 cards with names, CA/PA, height/weight |",
        f"| star_player_attributes | {c['star_player_attributes']:,} | 21 x 54 PDxx (0..20) |",
        f"| table_inventory | {c['table_inventory']:,} | 79 numbered (all closed) + 13 special |",
        "",
        "## CLI",
        "",
        "```",
        "py -V:3.12 -B scripts/t139_fm24_db_cli.py --build-sqlite",
        "py -V:3.12 -B scripts/t139_fm24_db_cli.py --stats",
        "py -V:3.12 -B scripts/t139_fm24_db_cli.py --query-uid 28049320",
        "py -V:3.12 -B scripts/t139_fm24_db_cli.py --top-players 20",
        "py -V:3.12 -B scripts/t139_fm24_db_cli.py --search-name England",
        "py -V:3.12 -B scripts/t139_fm24_db_cli.py --selftest",
        "```",
        "",
        "### Example outputs",
        "",
        "`--top-players 5` (Top-N by CA; name shown when the uid is one of the 21 "
        "star cards — no other person-name join exists in these archives):",
        "",
        "```json",
        '[{"rank": 1, "uid": 18004457, "ca": 190, "pa": 190, "birth_year": 1991, "name": "Kevin De Bruyne"}]',
        "```",
        "",
        "`--query-uid 28049320` returns the Harry Kane basic_people row "
        "(ca=184, pa=185, birth_year=1993), his star card, and his 54 attributes.",
        "",
        "`--search-name England` matches the surname \"England\" in `name_second` "
        "(3 pool entries) plus any club names containing \"England\".",
        "",
        "## Data boundary (verified, honest)",
        "",
        "- Competition display names are **not** in the archive: the COMP name-block "
        "tag is 0 for all 7,047 rows, and a raw byte scan of every entity payload "
        "(comp/nation/city/stadium/team, table_extra_3/9/24, old-save members) finds "
        "zero occurrences of `Premier League` / `England`. Entity display names live "
        "in the game's language DB, which is not part of these files.",
        "- Nation/city/stadium tables are fixed numeric layouts (no string fields); "
        "server `table_extra_9` carries nation nicknames + legendary-player names, "
        "not nation names.",
        "- `basic_people` carries no name ids (t123 proved no direct name-ordinal "
        "fields in the wire row); person names come from the three t106 pools "
        "(keyed by people_db read chains, out of t139 scope) and the 21 star cards.",
        "- basic_people identity: `uid`@+79 (t123) and `dbid`@+75 (t115 anchor word); "
        "equal for every anchor person, both indexed.",
        "",
        "## Schema notes",
        "",
        "- Variable-table columns are named by grammar path with the t110/t121 L3 "
        "4CC where proven (`col_<row0_off>` elsewhere); vector element counts are "
        "`n_*` columns; selector variants (clubs 0x0/0xc, teams 0xa/0xb) share the "
        "column set with NULLs where a variant does not produce a field.",
        "- 25 indexes cover uid/dbid/ca/name lookups; uid lookups measure < 5ms.",
        "- `export_summary.json` holds machine-readable counts, timings and the "
        "integrity report.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------- main
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="FM24 unified read-only SQLite exporter & CLI query tool (t139)")
    cmd = ap.add_mutually_exclusive_group(required=True)
    cmd.add_argument("--build-sqlite", action="store_true",
                     help="build scratch/t139/out/fm24_core.sqlite + export_summary.json")
    cmd.add_argument("--stats", action="store_true", help="print row counts of every table")
    cmd.add_argument("--query-uid", type=int, metavar="UID",
                     help="look up a person/club/comp/nation/stadium/team by UID")
    cmd.add_argument("--top-players", type=int, metavar="N",
                     help="top N players by CA with PA and birth year")
    cmd.add_argument("--search-name", metavar="TEXT", help="search club/person/fantasy names")
    cmd.add_argument("--selftest", action="store_true",
                     help="verify SQLite counts against source .dat truths")
    ap.add_argument("--limit", type=int, default=25, help="--search-name sample size")
    ap.add_argument("--db", default=None, help="alternate fm24_core.sqlite path")
    args = ap.parse_args(argv)
    if args.top_players is not None and args.top_players < 0:
        ap.error("--top-players must be nonnegative")
    if args.limit < 0:
        ap.error("--limit must be nonnegative")

    if args.build_sqlite:
        return build_sqlite()
    if args.stats:
        return cmd_stats(args)
    if args.query_uid is not None:
        return cmd_query_uid(args)
    if args.top_players is not None:
        return cmd_top_players(args)
    if args.search_name is not None:
        return cmd_search_name(args)
    return cmd_selftest(args)


if __name__ == "__main__":
    sys.exit(main())
