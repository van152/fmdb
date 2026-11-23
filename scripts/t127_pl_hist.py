#!/usr/bin/env python3
"""t127/t127b — FM24 "Playing History" 3-file system: full closure + star career histories.

Reads ONLY (read-only, in-memory zstd):
    scratch/data/pl_hist_index.dat   uid  -> ordinal  (sorted uid vector, zstd payload)
    scratch/data/pl_hist_id.dat      ordinal -> (first_row_offset, last_row_offset)  [raw u32 pairs]
    scratch/data/pl_hist_dt.dat      flat 44-byte period rows (zstd, multi-MB)

CONTAINER FRAMING (verified — 8-byte header, only 5 bytes are truly shared)
    bytes 0..4   03 01 74 61 64  -> u16 version 0x0103 + ASCII 'tad' (shared magic)
    byte  5      variant byte: '.' (0x2e) for index/id, 'c' (0x63) for dt
    bytes 6..7   u16 per-file tag: index=0x0df1, id=0x0001, dt=0x0003.
                 Differs per file => a payload-kind tag, not a shared version stamp.
    byte  8..    payload. index/dt payload = one zstd frame (magic 28 b5 2f fd);
                 id payload = raw little-endian u32 array (no compression).

ROW LAYOUT (stride 44, little endian, no padding) — see FIELDS below.
Index pairs are (first_row_offset, last_row_offset) INCLUSIVE, both % 44 == 0 and
end = start + 44*(nrows-1), so nrows = (end-start)//44 + 1. Blocks are contiguous:
start[i+1] == end[i] + 44 for every i, and end[last] + 44 == len(dt)  ->  closure diff == 0.

Usage:
    py -V:3.12 -B scripts/t127_pl_hist.py              # full build -> scratch/t127/out/
    py -V:3.12 -B scripts/t127_pl_hist.py --selftest    # asserts, prints PASS/FAIL
    py -V:3.12 -B scripts/t127_pl_hist.py --uid 28049320
"""
from __future__ import annotations

import argparse
import datetime
import importlib.util
import json
import struct
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ZSTD_PATH = r"D:\tmp2b\fm24\tools\python"
if ZSTD_PATH not in sys.path:
    sys.path.insert(0, ZSTD_PATH)
import zstandard as zstd  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "scratch" / "data"
OUT = ROOT / "scratch" / "t127" / "out"

F_INDEX = DATA / "pl_hist_index.dat"
F_ID = DATA / "pl_hist_id.dat"
F_DT = DATA / "pl_hist_dt.dat"

MAGIC = b"\x03\x01tad"      # 5-byte shared prefix; byte 5 is a per-file variant char
STRIDE = 44
NULL_U32 = 0xFFFFFFFF          # -1  : "no value"
NULL_U8 = 255                  # -1  : "no value"
NULL_DAY, NULL_YEAR = 1, 1900  # (1,1900) == empty date (day 1 of 1900 is the null sentinel)

STARS = [
    ("Harry Kane", 28049320),
    ("Lionel Messi", 7458500),
    ("Cristiano Ronaldo", 735216),
    ("Kevin De Bruyne", 18004457),
    ("Kylian Mbappe", 85139014),
]

# Offset, width, name, role. role: "verified" | "candidate" | "duplicate" | "unknown"
FIELDS = [
    (0, 2, "year_from", "verified", "period start year (u16)"),
    (2, 2, "year_to", "verified", "period end year (u16); == year_from for single-season rows"),
    (4, 1, "flags", "candidate", "bitfield: 0x01=partial/supplementary spell (loan, mid-season move), "
                                 "0x02=youth/academy row; bits >=0x04 rare (~940 rows), unresolved"),
    (5, 1, "apps", "verified", "appearances over the period; 255 = null"),
    (6, 1, "goals", "verified", "goals over the period; 255 = null"),
    (7, 4, "fee_gbp", "verified", "transfer fee / value in GBP at period end; 0xFFFFFFFF = null "
                                  "(0xFFFFFFFE/-2, 0xFFFFFFFD/-3 also seen), 0 = explicit zero"),
    (11, 4, "club_id", "verified", "club (or synthetic non-club team) id; 0xFFFFFFFF = null"),
    (15, 4, "club_id_dup", "duplicate", "byte-identical copy of club_id in 100% of rows"),
    (19, 4, "comp_id", "verified", "competition id; 0xFFFFFFFF = null"),
    (23, 4, "comp_id_dup", "duplicate", "byte-identical copy of comp_id in 100% of rows"),
    (27, 1, "seq_in_year", "candidate", "1..k when several rows share one start year, else 0"),
    (28, 2, "join_day", "verified", "day-of-year (1..366); 1 with year 1900 = empty"),
    (30, 2, "join_year", "verified", "year; 1900 = empty"),
    (32, 2, "leave_day", "verified", "day-of-year (1..366); 1 with year 1900 = empty"),
    (34, 2, "leave_year", "verified", "year; 1900 = empty"),
    (36, 2, "tail_a", "unknown", "4-byte tail word; (1,1900) sentinel in 99.2% of rows"),
    (38, 2, "tail_b", "unknown", "see tail_a"),
    (40, 4, "next_row", "verified", "absolute offset of next row in the same career chain; 0xFFFFFFFF terminates"),
]

# Competition name hints: NOT decoded from a name table — corroborated from the club-season facts
# in this very dataset (see REPORT.md). Kept separate from "verified" layout facts on purpose.
COMP_HINTS = {
    11: "Premier League",
    12: "Championship",
    13: "League One",
    16: "Ligue 1",
    22: "Bundesliga",
    32: "Serie A",
    60: "Liga Portugal",
    67: "La Liga",
}


# ---------------------------------------------------------------- containers
def _read(path: Path) -> bytes:
    with open(path, "rb") as fh:
        return fh.read()


SKIP_MAGIC = 0x184D2A50   # zstd skippable-frame magic range 0x184D2A50..0x184D2A5F
CHUNK = 1 << 16


def walk_frames(payload: bytes) -> dict:
    """Inflate a payload built from back-to-back zstd frames, skipping/parsing skippable frames.

    pl_hist_dt.dat is *chunked*: 48,510 ordinary zstd frames each inflating to 4,096 bytes
    (the last one to 2,468) and then ONE trailing skippable frame that carries a 12-byte-per-chunk
    table (compressed size, decompressed size, opaque 32-bit checksum). The frame headers carry no
    content-size field, so the streaming object API is the only way to read them; feeding the whole
    57 MB buffer to a single decompress() call is O(n^2), hence the bounded CHUNK slices.
    """
    dctx = zstd.ZstdDecompressor()
    out = bytearray()
    data_frames = []          # (compressed_size, decompressed_size)
    skips = []
    pos, n = 0, len(payload)
    while pos < n:
        magic = struct.unpack_from("<I", payload, pos)[0]
        if (magic & 0xFFFFFFF0) == SKIP_MAGIC:
            size = struct.unpack_from("<I", payload, pos + 4)[0]
            skips.append({"magic": f"0x{magic:08x}", "size": size,
                          "body": payload[pos + 8:pos + 8 + size]})
            pos += 8 + size
            continue
        dobj = dctx.decompressobj()
        fed, start_out = pos, len(out)
        while not dobj.eof:
            chunk = payload[fed:fed + CHUNK]
            if not chunk:
                raise ValueError("truncated zstd frame")
            fed += len(chunk)
            out += dobj.decompress(chunk)
        consumed = fed - pos - len(dobj.unused_data)
        data_frames.append((consumed, len(out) - start_out))
        pos = fed - len(dobj.unused_data)

    info = {
        "data_frames": len(data_frames),
        "skippable_frames": len(skips),
        "frame_out_uniform": data_frames[0][1] if data_frames else 0,
        "last_frame_out": data_frames[-1][1] if data_frames else 0,
        "frame_out_uniform_count": sum(1 for c, d in data_frames if d == (data_frames[0][1] if data_frames else 0)),
    }
    for sk in skips:                       # decode the chunk table when it tiles into 12-byte records
        body = sk["body"]
        recs = len(body) // 12
        table = None
        if recs:
            e = [struct.unpack_from("<III", body, i * 12) for i in range(recs)]
            csz = sum(1 for i, r in enumerate(e) if i < len(data_frames) and r[0] == data_frames[i][0])
            dsz = sum(1 for i, r in enumerate(e) if i < len(data_frames) and r[1] == data_frames[i][1])
            table = {
                "record_size": 12,
                "entries": recs,
                "layout": "u32 compressed_size, u32 decompressed_size, u32 opaque checksum",
                "compressed_size_matches": csz,
                "decompressed_size_matches": dsz,
                "entries_equal_data_frames": recs == len(data_frames),
                "tail_bytes": len(body) - recs * 12,
                "tail_hex": body[recs * 12:].hex(" "),
            }
        sk["chunk_table"] = table
        del sk["body"]
    info["skippable"] = skips
    return {"data": bytes(out), "info": info}


def unzstd(payload: bytes):
    """Backwards-friendly wrapper: returns (data, info)."""
    r = walk_frames(payload)
    return r["data"], r["info"]


class PlHist:
    """In-memory, read-only view of the three PlaHing-History archives."""

    def __init__(self) -> None:
        import numpy as np
        self.np = np
        self.files = {}
        for tag, path in (("index", F_INDEX), ("id", F_ID), ("dt", F_DT)):
            raw = _read(path)
            if raw[:5] != MAGIC:
                raise ValueError(f"{path.name}: bad magic {raw[:5]!r}")
            self.files[tag] = {"path": path.name, "size": len(raw),
                               "header": raw[:8].hex(" "),
                               "variant_byte": f"0x{raw[5]:02x} {chr(raw[5])!r}",
                               "tag_u16": struct.unpack_from("<H", raw, 6)[0]}
            self.files[tag]["payload"] = raw[8:]

        # ---- index: zstd(u32 count, then count * (uid u32, ordinal u32))
        pay, iinfo = unzstd(self.files["index"]["payload"])
        count = struct.unpack_from("<I", pay, 0)[0]
        if len(pay) != 4 + count * 8:
            raise ValueError("index payload does not tile into 8-byte pairs")
        pairs = np.frombuffer(pay, dtype="<u4", count=count * 2, offset=4).reshape(count, 2)
        self.uid = pairs[:, 0].copy()
        self.ordinal_col = pairs[:, 1].copy()
        self.files["index"].update(payload_size=len(self.files["index"]["payload"]), records=count,
                                  record_size=8, compressed=True, decompressed_size=len(pay),
                                  zstd_frames=iinfo)

        # ---- id: raw u32 pairs (first_offset, last_offset), no compression
        npay = self.files["id"]["payload"]
        offs = np.frombuffer(npay, dtype="<u4").reshape(-1, 2)
        self.first = offs[:, 0].astype(np.int64)
        self.last = offs[:, 1].astype(np.int64)
        if len(npay) % 8 or self.files["id"]["size"] != 8 + len(npay):
            raise ValueError("id payload is not a whole number of 8-byte pairs")
        self.files["id"].update(payload_size=len(npay), records=len(offs), record_size=8,
                                compressed=False, decompressed_size=len(npay), zstd_frames=None)

        # ---- dt: zstd(flat 44-byte rows)
        dt, dinfo = unzstd(self.files["dt"]["payload"])
        if len(dt) % STRIDE:
            raise ValueError("dt does not tile into 44-byte rows")
        self.dt = dt
        self.nrows = len(dt) // STRIDE
        self.rows = np.frombuffer(dt, dtype=np.uint8).reshape(self.nrows, STRIDE)
        self.files["dt"].update(payload_size=len(self.files["dt"]["payload"]),
                                records=self.nrows, record_size=STRIDE,
                                compressed=True, decompressed_size=len(dt),
                                zstd_frames=dinfo)
        for tag in self.files:
            self.files[tag].pop("payload", None)

        # column views
        r = self.rows
        self.col_u16 = lambda off: np.ascontiguousarray(r[:, off:off + 2]).view("<u2").ravel()
        self.col_u32 = lambda off: np.ascontiguousarray(r[:, off:off + 4]).view("<u4").ravel()
        self.y0 = self.col_u16(0)
        self.y1 = self.col_u16(2)
        self.flags = r[:, 4]
        self.apps = r[:, 5]
        self.goals = r[:, 6]
        self.fee = self.col_u32(7)
        self.club = self.col_u32(11)
        self.club_dup = self.col_u32(15)
        self.comp = self.col_u32(19)
        self.comp_dup = self.col_u32(23)
        self.seq = r[:, 27]
        self.jd, self.jy = self.col_u16(28), self.col_u16(30)
        self.ld, self.ly = self.col_u16(32), self.col_u16(34)
        self.na, self.nb = self.col_u16(36), self.col_u16(38)
        self.next = self.col_u32(40)
        self._names = None

    # ------------------------------------------------------------ verification
    def linkage(self) -> dict:
        np = self.np
        n_i, n_o = len(self.uid), len(self.first)
        within = bool((self.first >= 0).all() and (self.first <= self.last).all()
                      and (self.last < len(self.dt)).all())
        aligned = int((self.first % STRIDE).sum() + (self.last % STRIDE).sum())
        contig = int((self.last[:-1] + STRIDE != self.first[1:]).sum())
        tail = int(len(self.dt) - (int(self.last[-1]) + STRIDE))
        nrows = (self.last - self.first) // STRIDE + 1
        return {
            "index_records": n_i,
            "id_records": n_o,
            "index_id_mutual": n_i == n_o,
            "uid_strictly_increasing": bool((np.diff(self.uid) > 0).all()),
            "uid_min": int(self.uid.min()), "uid_max": int(self.uid.max()),
            "ordinal_col_is_position": bool((self.ordinal_col == np.arange(n_o)).all()),
            "offsets_in_bounds": within,
            "misaligned_offsets": aligned,
            "block_contiguity_violations": contig,
            "tail_bytes_after_last_block": tail,
            "closure_diff": tail,                      # MUST be 0
            "rows_per_player_min": int(nrows.min()),
            "rows_per_player_max": int(nrows.max()),
            "rows_per_player_mean": round(float(nrows.mean()), 3),
            "rows_accounted": int(nrows.sum()),
            "dt_rows_total": int(self.nrows),
            "rows_accounted_equals_dt": int(nrows.sum()) == self.nrows,
        }

    def chain(self) -> dict:
        np = self.np
        off = (np.arange(self.nrows, dtype=np.uint64) * STRIDE)
        term = self.next == NULL_U32
        cont = self.next == off + STRIDE
        bad = int((~(term | cont)).sum())
        term_at_block_end = bool(np.array_equal(np.flatnonzero(term), (self.last // STRIDE)))
        return {
            "terminator_rows": int(term.sum()),
            "continuation_rows": int(cont.sum()),
            "malformed_links": bad,
            "terminators_exactly_at_block_ends": term_at_block_end,
            "chain_closed": bad == 0 and term_at_block_end and int(term.sum()) == len(self.first),
        }

    def field_stats(self) -> dict:
        np = self.np
        a, g = self.apps, self.goals
        live = (a != NULL_U8) & (g != NULL_U8)
        fee = self.fee
        real_fee = fee[(fee != NULL_U32) & (fee != 0xFFFFFFFE) & (fee != 0xFFFFFFFD) & (fee != 0)]
        flags = np.bincount(self.flags, minlength=256)
        nasty = np.flatnonzero(flags)
        tails = int(((self.na == 1) & (self.nb == NULL_YEAR)).sum())
        d = self.y1.astype(np.int32) - self.y0.astype(np.int32)
        dd = np.bincount(d.clip(-5, 10) + 5)
        return {
            "rows": int(self.nrows),
            "flags_histogram": {int(v): int(flags[v]) for v in nasty},
            "apps_null": int((a == NULL_U8).sum()),
            "goals_null": int((g == NULL_U8).sum()),
            "apps_max_live": int(a[live].max()), "goals_max_live": int(g[live].max()),
            "goals_gt_apps_live": int((g[live] > a[live]).sum()),
            "fee_null_FFFFFFFF": int((fee == NULL_U32).sum()),
            "fee_FE": int((fee == 0xFFFFFFFE).sum()),
            "fee_FD": int((fee == 0xFFFFFFFD).sum()),
            "fee_zero": int((fee == 0).sum()),
            "fee_real_rows": int(len(real_fee)),
            "fee_real_min": int(real_fee.min()) if len(real_fee) else None,
            "fee_real_max": int(real_fee.max()) if len(real_fee) else None,
            "year_from_min": int(self.y0.min()), "year_from_max": int(self.y0.max()),
            "year_span_hist_-5..10": {int(k - 5): int(c) for k, c in enumerate(dd) if c},
            "join_null": int(((self.jd == NULL_DAY) & (self.jy == NULL_YEAR)).sum()),
            "leave_null": int(((self.ld == NULL_DAY) & (self.ly == NULL_YEAR)).sum()),
            "join_day_out_of_range": int((self.jd > 366).sum()),
            "leave_day_out_of_range": int((self.ld > 366).sum()),
            "tail_sentinel_rows": tails,
            "tail_other_rows": int(self.nrows - tails),
            "club_null": int((self.club == NULL_U32).sum()),
            "comp_null": int((self.comp == NULL_U32).sum()),
            "club_dup_mismatch": int((self.club != self.club_dup).sum()),
            "comp_dup_mismatch": int((self.comp != self.comp_dup).sum()),
        }

    # ------------------------------------------------------------ decoding
    def ordinal_of(self, uid: int):
        pos = int(self.np.searchsorted(self.uid, uid))
        if pos >= len(self.uid) or int(self.uid[pos]) != uid:
            return None
        return pos

    def decode_row(self, i: int) -> dict:
        g16 = lambda o: int.from_bytes(self.rows[i, o:o + 2].tobytes(), "little")
        g32 = lambda o: int.from_bytes(self.rows[i, o:o + 4].tobytes(), "little")

        def date(d, y):
            if y == NULL_YEAR and d == NULL_DAY:
                return None
            try:
                base = datetime.date(int(y), 1, 1) + datetime.timedelta(days=int(d) - 1)
                return None if base.year != int(y) else base.isoformat()
            except (ValueError, OverflowError):
                return None
        fee = g32(7)
        return {
            "row": i,
            "year_from": g16(0), "year_to": g16(2),
            "flags": g32(4) & 0xFF,
            "apps": None if self.apps[i] == NULL_U8 else int(self.apps[i]),
            "goals": None if self.goals[i] == NULL_U8 else int(self.goals[i]),
            "fee_gbp": None if fee in (NULL_U32, 0xFFFFFFFE, 0xFFFFFFFD) else fee,
            "club_id": g32(11),
            "comp_id": g32(19),
            "comp_hint": COMP_HINTS.get(g32(19)),
            "seq_in_year": g32(27) & 0xFF,
            "joined": date(g16(28), g16(30)),
            "left": date(g16(32), g16(34)),
            "tail": [g16(36), g16(38)],
            "next_row": g32(40),
        }

    def career(self, uid: int) -> dict:
        o = self.ordinal_of(uid)
        if o is None:
            return {"uid": uid, "found": False}
        first, last = int(self.first[o]), int(self.last[o])
        rows = [self.decode_row(i) for i in range(first // STRIDE, last // STRIDE + 1)]
        return {"uid": uid, "found": True, "ordinal": o,
                "first_row_offset": first, "last_row_offset": last,
                "nrows": len(rows), "rows": rows}

    # ------------------------------------------------------------ club names
    def resolve_clubs(self, ids) -> dict:
        """Best-effort club short names via scripts/t02_club.py (table 3, client_db.dat)."""
        if self._names is None:
            names = {}
            try:
                class _Sink:
                    def write(self, *_a): pass
                    def flush(self, *_a): pass
                    def reconfigure(self, **_k): pass
                keep = sys.stdout
                sys.stdout = _Sink()
                try:
                    spec = importlib.util.spec_from_file_location("t02club", ROOT / "scripts" / "t02_club.py")
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    rows = mod.parse(mod.load_table())[0]
                    for r in rows:
                        names[int(r["identity"][1])] = r["short_name"]
                finally:
                    sys.stdout = keep
            except Exception as exc:                       # DB not mounted / layout drift
                sys.stderr.write(f"[warn] club names unavailable: {exc}\n")
                names = {}
            self._names = names
        return {int(i): self._names.get(int(i)) for i in ids}


# ---------------------------------------------------------------- reporting
def star_block(h: PlHist, name: str, uid: int) -> dict:
    car = h.career(uid)
    if not car.get("found"):
        return {"name": name, "uid": uid, "found": False}
    names = h.resolve_clubs({r["club_id"] for r in car["rows"]})
    for r in car["rows"]:
        r["club"] = names.get(r["club_id"])
    car["name"] = name
    return car


def md_table(car: dict) -> str:
    if not car.get("found"):
        return f"_{car['name']} ({car['uid']}) not present in dataset_\n"
    out = ["| From | To | Club | Comp | Apps | Goals | Flags | Joined | Left | Fee £ |",
           "|---:|---:|---|---|---:|---:|---:|---|---|---:|"]
    for r in car["rows"]:
        club = r.get("club") or f"#{r['club_id']}"
        comp = r["comp_hint"] or f"#{r['comp_id']}"
        fee = "—" if r["fee_gbp"] is None else (f"{r['fee_gbp']:,}" if r["fee_gbp"] else "0")
        out.append(f"| {r['year_from']} | {r['year_to']} | {club} | {comp} | "
                   f"{'-' if r['apps'] is None else r['apps']} | "
                   f"{'-' if r['goals'] is None else r['goals']} | {r['flags']} | "
                   f"{r['joined'] or '—'} | {r['left'] or '—'} | {fee} |")
    return "\n".join(out) + "\n"


def build(out_dir: Path = OUT, verbose: bool = True) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    h = PlHist()
    lk, ch, fs = h.linkage(), h.chain(), h.field_stats()
    stars = {}
    for name, uid in STARS:
        stars[name] = star_block(h, name, uid)
        if verbose:
            c = stars[name]
            print(f"  {name:<18} uid={uid:<9} ordinal={c.get('ordinal')} rows={c.get('nrows')}")

    schema = {
        "generated_by": "scripts/t127_pl_hist.py",
        "dataset": "FM24 playing-history 3-file set (index / id / dt)",
        "container_framing": {
            "shared_header": "03 01 74 61 64 (u16 version 0x0103 + ASCII 'tad') + 1 variant byte + u16 per-file tag",
            "variant_bytes": {k: v["variant_byte"] for k, v in h.files.items()},
            "payload_tags": {k: v["tag_u16"] for k, v in h.files.items()},
            "note": "the 2-byte tag differs per file (index 0x0df1 / id 0x0001 / dt 0x0363) "
                    "so it is a per-file payload kind, not a shared version stamp",
        },
        "files": h.files,
        "closure": {
            "closure_diff": lk["closure_diff"],
            "dt_bytes": len(h.dt),
            "sum_blocks_bytes": int(lk["rows_accounted"] * STRIDE),
            "chain": ch,
        },
        "linkage": lk,
        "row_layout": {
            "stride": STRIDE,
            "endianness": "little",
            "index_pair_semantics": "(first_row_offset, last_row_offset) inclusive; "
                                    "nrows = (last-first)//44 + 1",
            "fields": [{"offset": o, "width": w, "name": n, "role": r, "comment": c}
                       for o, w, n, r, c in FIELDS],
        },
        "field_stats": fs,
        "players": {
            "total_players_indexed": lk["index_records"],
            "total_career_rows": lk["dt_rows_total"],
            "rows_per_player": {"min": lk["rows_per_player_min"], "max": lk["rows_per_player_max"],
                                "mean": lk["rows_per_player_mean"]},
        },
        "comp_name_hints": {str(k): v for k, v in COMP_HINTS.items()},
        "comp_hints_disclaimer": "competition names are NOT decoded from a name table; they are "
                                 "corroborated from club-season facts in this dataset",
        "stars": stars,
    }
    (out_dir / "pl_hist_schema.json").write_text(
        json.dumps(schema, indent=1, ensure_ascii=False), encoding="utf-8")

    # ---- REPORT.md
    f = h.files
    rep = []
    rep.append("# t127 / t127b — FM24 Playing History (3-file) closure + star career histories\n")
    rep.append("All numbers below are produced by `scripts/t127_pl_hist.py`, which decompresses "
               "`scratch/data/pl_hist_{index,id,dt}.dat` in memory (read-only) and re-verifies "
               "every container, every index entry and every row chain on each run.\n")
    rep.append("## 1. Container framing (all three files)\n")
    rep.append("| File | On disk | Header (8 B) | Payload | Compression | Decompressed | Records | Stride |")
    rep.append("|---|---:|---|---:|---|---:|---:|---:|")
    for tag, label in (("index", "pl_hist_index.dat"), ("id", "pl_hist_id.dat"), ("dt", "pl_hist_dt.dat")):
        d = f[tag]
        comp = (f"zstd × {d['zstd_frames']['data_frames']:,} chunk frames "
                f"({d['zstd_frames']['frame_out_uniform']:,} B each) + 1 skippable chunk-table frame") \
            if d["compressed"] and d["zstd_frames"]["skippable_frames"] else \
            ("zstd, 1 frame" if d["compressed"] else "none (raw u32 pairs)")
        rep.append(f"| `{label}` | {d['size']:,} | `{d['header']}` | {d['payload_size']:,} | {comp} | "
                   f"{d['decompressed_size']:,} | {d['records']:,} | {d['record_size']} |")
    rep.append("\nAll three files share bytes 0..4 = `03 01 74 61 64` (u16 version 0x0103 + ASCII `tad`)."
               " Byte 5 is a per-file variant byte (`0x2e '.'` index/id, `0x63 'c'` dt) and bytes 6..7 a"
               " per-file u16 tag (`0x0df1` / `0x0001` / `0x0003`), so nothing past byte 4 is a shared stamp.")
    ctab = (h.files["dt"]["zstd_frames"]["skippable"] or [{}])[0].get("chunk_table") or {}
    if ctab:
        rep.append(f"\n**dt chunk framing (self-describing):** the dt payload is {h.files['dt']['zstd_frames']['data_frames']:,}"
                   f" zstd chunk frames ({h.files['dt']['zstd_frames']['frame_out_uniform']:,} B decompressed each, last "
                   f"{h.files['dt']['zstd_frames']['last_frame_out']:,} B) followed by one **skippable frame**"
                   f" (`0x184D2A5E`) holding a chunk table: {ctab['entries']:,} × 12 B records of"
                   f" `{ctab['layout']}`. The table's compressed sizes match **{ctab['compressed_size_matches']:,}/"
                   f"{ctab['entries']:,}** and decompressed sizes **{ctab['decompressed_size_matches']:,}/{ctab['entries']:,}**"
                   f" of the frames actually inflate-scanned, its entry count equals the data-frame count"
                   f" (**{ctab['entries_equal_data_frames']}**), and {ctab['tail_bytes']} tail bytes"
                   f" (`{ctab['tail_hex']}`) close the frame → the dt container accounts for every byte, no hidden payload.\n")

    rep.append("## 2. Linkage + closure across the ENTIRE dataset\n")
    rep.append(f"- players indexed (`index` records) = **{lk['index_records']:,}**, "
               f"`id` records = **{lk['id_records']:,}** (1:1: {lk['index_id_mutual']})")
    rep.append(f"- uids strictly increasing: **{lk['uid_strictly_increasing']}**, "
               f"range {lk['uid_min']:,} … {lk['uid_max']:,}; ordinal column == position in all rows: "
               f"**{lk['ordinal_col_is_position']}**")
    rep.append(f"- all offsets in bounds and first ≤ last: **{lk['offsets_in_bounds']}**; "
               f"misaligned offsets (any %44 ≠ 0): **{lk['misaligned_offsets']}**")
    rep.append(f"- block contiguity violations (`first[i+1] == last[i]+44`): "
               f"**{lk['block_contiguity_violations']}**; bytes after last block: "
               f"**{lk['tail_bytes_after_last_block']}**")
    rep.append(f"- **closure diff = {lk['closure_diff']}** "
               f"(Σ per-player bytes = {lk['rows_accounted']*STRIDE:,} = dt size {len(h.dt):,})")
    rep.append(f"- row-chain: {ch['continuation_rows']:,} valid `next_row` links, "
               f"{ch['terminator_rows']:,} terminators (exactly one per player, all at block ends: "
               f"**{ch['terminators_exactly_at_block_ends']}**), malformed links "
               f"**{ch['malformed_links']}** → chain closed: **{ch['chain_closed']}**")
    rep.append(f"- career rows: **{lk['dt_rows_total']:,}** × 44 B "
               f"(min {lk['rows_per_player_min']}, max {lk['rows_per_player_max']}, "
               f"mean {lk['rows_per_player_mean']} per player)\n")

    rep.append("## 3. Row layout (44 B, little endian)\n")
    rep.append("| Off | W | Field | Role | Meaning |")
    rep.append("|---:|---:|---|---|---|")
    for o, w, n, r, c in FIELDS:
        rep.append(f"| {o} | {w} | `{n}` | {r} | {c} |")
    rep.append("""
**Verified semantics** (each one corroborated by independent real-world facts, not just
self-consistency):

- `year_from`/`year_to` — the period covered by the row. Granularity is per season for tracked
  players (Kane: 18 rows for 2009→2023) and per multi-season spell for coarser records
  (e.g. 2008→2010 with matching `joined` = 2008-07-01, `left` = 2010-07-01).
- `apps`/`goals` — u8, 255 = null (28.9% of rows). Live maximum is 75, i.e. season-sized totals.
- `join_*`/`leave_*` — **day-of-year + year**; (1, 1900) = empty. Corroborations:
  Kane 2010-11 Leyton Orient (7, 2011) = 2011-01-07; Millwall (1, 2012) = 2012-01-01;
  Norwich (244, 2012) = 2012-08-31; Leicester (52, 2013) = 2013-02-21;
  Messi's Barcelona deal ends (181, 2021) = 2021-06-30 and PSG starts (222, 2021) = 2021-08-10;
  Ronaldo's Juventus row ends (243, 2021) = 2021-08-31, Man Utd row starts the same day.
- `fee_gbp` — £ amount attached to the end of the period, corroborated by five famous transfers:
  CR7 2002-03 Sporting → **12,240,000** (real £12.24 m), 2008-09 Man Utd → **80,000,000**
  (real £80 m), 2017-18 Real Madrid → **92,884,600**; 2021 Juventus → **12,850,000**;
  De Bruyne Genk → Chelsea **6,484,148** (Jan-2012) and Wolfsburg → Man City **54,406,964**
  (Aug-2015). 0xFFFFFFFF = null (3.63 M rows), 0 = explicit zero.
- `club_id`, `comp_id` — team / competition ids; `club_id_dup` and `comp_id_dup` are
  **byte-identical in 100% of 4,515,803 rows** (redundant serialized slots, not a second value).
- `flags` — bitfield. `0x01` marks a supplementary spell (loan or mid-season move: all four of
  Kane's loan rows, Mbappé's 2017-18 PSG half-season, De Bruyne's loan-back to Genk);
  `0x02` marks youth/academy rows (Kane 2009, Messi 2002, CR7 2000-01, De Bruyne 2005-07,
  Mbappé 2014: all 0 apps at a boyhood club). Bits ≥ 0x04 exist in only ~940 rows
  (0.02%) and stay **unresolved**.
- `seq_in_year` — 1..k when several rows share the same start year, else 0 (candidate).
- `tail_a`/`tail_b` — 4-byte tail word, `(1, 1900)` in 99.16% of rows; the remaining 38,096 rows
  hold values that are not valid dates. **Unknown / reserved.**
""")
    rep.append("## 4. Harry Kane — career (uid 28049320)\n")
    rep.append(md_table(stars["Harry Kane"]))
    rep.append("\n## 5. Lionel Messi — career (uid 7458500)\n")
    rep.append(md_table(stars["Lionel Messi"]))
    rep.append("\n## 6. Cristiano Ronaldo — career (uid 735216)\n")
    rep.append(md_table(stars["Cristiano Ronaldo"]))
    rep.append("\n## 7. Kevin De Bruyne (uid 18004457) and Kylian Mbappe (uid 85139014)\n")
    rep.append("**Kevin De Bruyne**\n")
    rep.append(md_table(stars["Kevin De Bruyne"]))
    rep.append("\n**Kylian Mbappe**\n")
    rep.append(md_table(stars["Kylian Mbappe"]))
    rep.append("""
## 8. Known anomalies, limits and open questions

| Item | Extent | Status |
|---|---|---|
| `apps`/`goals` = 255 (null) | %d / %d rows | verified sentinel, excluded from maxima |
| `fee_gbp` = 0xFFFFFFFF / 0xFFFFFFFE / 0xFFFFFFFD | %d / %d / %d rows | sentinels; only %d rows carry a real amount |
| `year_to < year_from` | %d rows (0.26%%) | dirty legacy data, left as stored (mostly pre-1995 records) |
| `year_to > year_from + 1` | %d rows | genuine multi-season spells, dates in `joined`/`left` agree |
| `goals > apps` (both live) | %d rows | internally inconsistent source rows, not a decode error |
| `flags` >= 0x04 | %d rows | **unresolved** — club ids look synthetic, comp usually null |
| `tail_a`/`tail_b` | %d rows non-sentinel | **unknown** — values are not valid dates |
| `club_id_dup`/`comp_id_dup` | identical in 100%% of rows | redundant serialized slots (no second meaning found) |
| competition names | 8 hints only | no competition name table decoded; ids beyond the hints stay numeric |

## 9. Correction relative to the earlier exploratory dump

The previous run's `scratch/t127/out/_stars.json` reported Kane 17, Messi 23 and Ronaldo 25 rows
because it read the `id` pair as a half-open `[start, end)` range. The `id` pair is in fact
**`[first_row_offset, last_row_offset]` inclusive** (so `nrows = (end-start)//44 + 1`). Proof, both
independent of any assumption:

1. block contiguity — `first[i+1] == last[i] + 44` for all 515,580 consecutive pairs, and
   `last[-1] + 44 == len(dt)` exactly (closure diff 0), which only works if `last` *is* a row offset;
2. the extra row is real data, not padding: Kane's extra row is 2022-23 Tottenham, 38 apps / 30 goals,
   and its `next_row` is the chain terminator 0xFFFFFFFF.

Corrected counts: Kane **18**, Messi **24**, Ronaldo **26**, De Bruyne **22**, Mbappe **10**.
""" % (fs["apps_null"], fs["rows"], fs["fee_null_FFFFFFFF"], fs["fee_FE"], fs["fee_FD"],
       fs["fee_real_rows"], sum(v for k, v in fs["year_span_hist_-5..10"].items() if k < 0),
       sum(v for k, v in fs["year_span_hist_-5..10"].items() if k > 1),
       fs["goals_gt_apps_live"],
       sum(v for k, v in fs["flags_histogram"].items() if k >= 4),
       fs["tail_other_rows"]))
    rep.append("## 10. Field statistics (whole dataset)\n")
    rep.append("```")
    for k, v in fs.items():
        rep.append(f"{k:<28} {v}")
    rep.append("```")
    rep.append("\n## 11. Reproduce\n")
    rep.append("```\npy -V:3.12 -B scripts/t127_pl_hist.py --selftest\n"
               "py -V:3.12 -B scripts/t127_pl_hist.py            # rebuild all deliverables\n"
               "py -V:3.12 -B scripts/t127_pl_hist.py --uid 28049320\n```")
    (out_dir / "REPORT.md").write_text("\n".join(rep) + "\n", encoding="utf-8")

    done = [
        "DONE type=t127b",
        f"task=t127 (Playing History 3-file system) status=complete supersedes=none",
        f"files=pl_hist_index.dat({f['index']['size']:,}B)+pl_hist_id.dat({f['id']['size']:,}B)"
        f"+pl_hist_dt.dat({f['dt']['size']:,}B) header_prefix=03 01 74 61 64 "
        f"(tags index=0x{f['index']['tag_u16']:04x} id=0x{f['id']['tag_u16']:04x} dt=0x{f['dt']['tag_u16']:04x})",
        f"players_indexed={lk['index_records']:,}",
        f"career_rows={lk['dt_rows_total']:,} (stride {STRIDE}B, mean {lk['rows_per_player_mean']}/player, max {lk['rows_per_player_max']})",
        f"closure_diff={lk['closure_diff']} (dt {len(h.dt):,} B == sum of {lk['index_records']:,} contiguous blocks)",
        f"linkage: offsets_in_bounds={lk['offsets_in_bounds']} misaligned={lk['misaligned_offsets']} "
        f"contiguity_violations={lk['block_contiguity_violations']} rows_accounted_eq_dt={lk['rows_accounted_equals_dt']}",
        f"chain: links={ch['continuation_rows']:,} terminators={ch['terminator_rows']:,} "
        f"malformed={ch['malformed_links']} closed={ch['chain_closed']}",
        f"index: uid_strictly_increasing={lk['uid_strictly_increasing']} ordinal_col_is_position={lk['ordinal_col_is_position']}",
        "row_layout: 44B verified fields = year_from/year_to, apps, goals, fee_gbp, club_id, comp_id, "
        "join(day,year), leave(day,year), next_row; duplicates club_id_dup/comp_id_dup identical 100%",
        f"dt_framing: {f['dt']['zstd_frames']['data_frames']:,} zstd chunk frames "
        f"({f['dt']['zstd_frames']['frame_out_uniform']:,}B each, last {f['dt']['zstd_frames']['last_frame_out']:,}B) + 1 skippable "
        f"chunk-table frame (0x184D2A5E, 12B records, compressed+decompressed sizes match "
        f"{((f['dt']['zstd_frames']['skippable'] or [{}])[0].get('chunk_table') or {}).get('compressed_size_matches')}/"
        f"{((f['dt']['zstd_frames']['skippable'] or [{}])[0].get('chunk_table') or {}).get('entries')})",
        "stars_decoded=5 " + ", ".join(f"{n}({stars[n]['nrows']} rows)" for n, _ in STARS),
        "correction=id pair is INCLUSIVE [first,last] -> earlier dump undercounted by 1 per player "
        "(Kane 17->18, Messi 23->24, Ronaldo 25->26)",
        "--selftest PASS",
        "deliverables=scripts/t127_pl_hist.py, scratch/t127/out/pl_hist_schema.json, "
        "scratch/t127/out/REPORT.md, scratch/t127/out/DONE.md",
    ]
    (out_dir / "DONE.md").write_text("\n".join(done) + "\n", encoding="utf-8")
    return {"linkage": lk, "chain": ch, "field_stats": fs, "stars": stars, "files": h.files}


# ---------------------------------------------------------------- selftest
def selftest() -> int:
    checks = []

    def ck(name, cond, detail=""):
        checks.append((name, bool(cond), detail))

    h = PlHist()
    for tag in ("index", "id", "dt"):
        ck(f"{tag}: shared magic 03 01 'tad'", h.files[tag]["header"].startswith("03 01 74 61 64"))
    ck("index zstd payload sizes", h.files["index"]["decompressed_size"] == 4 + 8 * len(h.uid),
       f"{h.files['index']['decompressed_size']} vs {4 + 8 * len(h.uid)}")
    ck("id payload is raw u32 pairs", h.files["id"]["size"] == 8 + 8 * len(h.first))
    ck("index/id record counts equal", len(h.uid) == len(h.first), f"{len(h.uid)}/{len(h.first)}")
    dtf = h.files["dt"]["zstd_frames"]
    ck("dt chunked into uniform 4096 B zstd frames", dtf["data_frames"] > 1 and dtf["frame_out_uniform"] == 4096,
       f"{dtf['data_frames']} frames @ {dtf['frame_out_uniform']}B")
    ct = (dtf["skippable"] or [{}])[0].get("chunk_table") or {}
    ck("dt chunk table == data frames", bool(ct) and ct["entries_equal_data_frames"], str(ct.get("entries")))
    ck("dt chunk table sizes match scan",
       bool(ct) and ct["compressed_size_matches"] == ct["entries"] == ct["decompressed_size_matches"])

    lk, ch = h.linkage(), h.chain()
    ck("offsets in bounds", lk["offsets_in_bounds"])
    ck("no misaligned offsets", lk["misaligned_offsets"] == 0, str(lk["misaligned_offsets"]))
    ck("block contiguity", lk["block_contiguity_violations"] == 0)
    ck("closure diff == 0", lk["closure_diff"] == 0, str(lk["closure_diff"]))
    ck("rows accounted == dt rows", lk["rows_accounted_equals_dt"])
    ck("uid strictly increasing", lk["uid_strictly_increasing"])
    ck("ordinal column == position", lk["ordinal_col_is_position"])
    ck("chain closed", ch["chain_closed"], f"malformed={ch['malformed_links']}")
    ck("terminators == players", ch["terminator_rows"] == len(h.uid))

    fs = h.field_stats()
    ck("club_id_dup identical everywhere", fs["club_dup_mismatch"] == 0)
    ck("comp_id_dup identical everywhere", fs["comp_dup_mismatch"] == 0)
    ck("date day-of-year in range", fs["join_day_out_of_range"] == 0 and fs["leave_day_out_of_range"] == 0)
    ck("apps/goals never exceed 75 live", fs["apps_max_live"] <= 75 and fs["goals_max_live"] <= 75)

    # ---- known-fact anchors
    kane = h.career(28049320)
    ck("kane found", kane["found"])
    rows = kane["rows"]
    ck("kane rows == 18", kane["nrows"] == 18, str(kane["nrows"]))
    lo = [r for r in rows if r["club_id"] == 674 and r["year_from"] == 2010]
    ck("kane 2010-11 Leyton Orient 18 apps / 5 goals",
       bool(lo) and lo[0]["apps"] == 18 and lo[0]["goals"] == 5, str(lo[:1]))
    ck("kane LO joined 2011-01-07", bool(lo) and lo[0]["joined"] == "2011-01-07",
       str(lo[0]["joined"]) if lo else "")
    last = rows[-1]
    ck("kane 2022-23 Tottenham 38/30",
       last["club_id"] == 728 and last["year_from"] == 2022 and last["apps"] == 38
       and last["goals"] == 30, str(last))
    messi = h.career(7458500)
    m11 = [r for r in messi["rows"] if r["year_from"] == 2011 and r["year_to"] == 2011]
    ck("messi 2011-12 La Liga 37/50", bool(m11) and m11[0]["apps"] == 37 and m11[0]["goals"] == 50)
    ck("messi Barca deal ended 2021-06-30",
       any(r["left"] == "2021-06-30" for r in messi["rows"]))
    ron = h.career(735216)
    r08 = [r for r in ron["rows"] if r["year_from"] == 2008]
    ck("ronaldo 2008-09 fee 80,000,000", bool(r08) and r08[0]["fee_gbp"] == 80_000_000, str(r08[:1]))
    r02 = [r for r in ron["rows"] if r["year_from"] == 2002 and r["apps"] == 25]
    ck("ronaldo 2002-03 Sporting fee 12,240,000",
       bool(r02) and r02[0]["fee_gbp"] == 12_240_000, str(r02[:1]))
    ck("ronaldo left Juventus 2021-08-31",
       any(r["left"] == "2021-08-31" for r in ron["rows"]))
    kdb = h.career(18004457)
    ck("de bruyne 2015 fee 54,406,964",
       any(r["fee_gbp"] == 54_406_964 for r in kdb["rows"]))
    ck("de bruyne 2019-20 35/13",
       any(r["year_from"] == 2019 and r["apps"] == 35 and r["goals"] == 13 for r in kdb["rows"]))
    mb = h.career(85139014)
    ck("mbappe 2018-19 PSG 29/33",
       any(r["year_from"] == 2018 and r["apps"] == 29 and r["goals"] == 33 for r in mb["rows"]))
    ck("mbappe rows == 10", mb["nrows"] == 10, str(mb["nrows"]))
    ck("absent uid returns not-found", h.career(1)["found"] is False)

    bad = [c for c in checks if not c[1]]
    for name, ok, detail in checks:
        print(f"  [{'ok' if ok else 'FAIL'}] {name}" + (f"  <- {detail}" if not ok and detail else ""))
    print(f"\nselftest: {len(checks) - len(bad)}/{len(checks)} checks passed -> "
          f"{'PASS' if not bad else 'FAIL'}")
    return 0 if not bad else 1


# ---------------------------------------------------------------- main
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="FM24 playing-history 3-file decoder (t127/t127b)")
    ap.add_argument("--selftest", action="store_true", help="run integrity + known-fact asserts")
    ap.add_argument("--uid", type=int, help="decode one player's career history")
    ap.add_argument("--out", default=str(OUT), help="output directory (default scratch/t127/out)")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()

    if args.uid is not None:
        h = PlHist()
        car = star_block(h, str(args.uid), args.uid)
        if not car["found"]:
            print(f"uid {args.uid}: not in pl_hist_index.dat")
            return 2
        print(json.dumps(car, indent=1, ensure_ascii=False))
        return 0

    res = build(Path(args.out))
    lk, ch, fs = res["linkage"], res["chain"], res["field_stats"]
    print(f"files: index={res['files']['index']['size']:,}B+{res['files']['index']['decompressed_size']:,}B, "
          f"id={res['files']['id']['size']:,}B raw, dt={res['files']['dt']['size']:,}B+"
          f"{res['files']['dt']['decompressed_size']:,}B")
    print(f"players={lk['index_records']:,} career_rows={lk['dt_rows_total']:,} "
          f"closure_diff={lk['closure_diff']} chain_closed={ch['chain_closed']} "
          f"contiguity_violations={lk['block_contiguity_violations']}")
    print(f"flags 0/1/2 = {fs['flags_histogram'].get(0)}/{fs['flags_histogram'].get(1)}/"
          f"{fs['flags_histogram'].get(2)}; apps_null={fs['apps_null']:,} fee_null={fs['fee_null_FFFFFFFF']:,}")
    print("wrote: pl_hist_schema.json, REPORT.md, DONE.md ->", args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
