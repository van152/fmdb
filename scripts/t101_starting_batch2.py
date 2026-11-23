#!/usr/bin/env python3
"""t101 — STARTING_* sub-table batch 2 (tt 49..73, 20 tables) L3 wire schemas.

Derives, from the Hex-Rays ``slot19_read_server`` pseudo-code in
``scratch/t95/funcs/*.c`` (read-only) plus the t101 helper decompilations in
``scratch/t101/ida/*.c``, the exact wire order of every ``STARTING_*`` child
table, then validates each decoder against the live ``server_db/table_<N>.dat``
payload (unpacked with ``scripts/t38_multiframe.py``).

Per table the script emits
  * ordered wire fields (wire offset, width, ``this+0xNN`` mem offset, C source line)
  * the 4CC census reachable from that table's own vtable slots 02/03
  * a full-table decode run: selector histogram, row-length histogram,
    base-identity postcondition (row ordinal == wire ordinal, id == id2),
    closure ``13 + body + 9 == payload_len`` and the 9-byte footer

Wire framing recap
------------------
``03 01 "tad." | u16 version | u32 count | body | 9B footer``.  Every row is
``u8 selector`` followed by the field block read by ``sub_<slot19>``; the last
12 body bytes of a row are the DATABASE_ROW base identity
``u32 row_index, u32 dbid, u32 dbid2`` (``sub_143DCB6F0`` tail read, line 15).

Table families (all confirmed from the C bodies)
------------------------------------------------
* fixed stride, single block: 49 50 51 58 60 61 62 63 64 65 66 67 68 69 70 73
* variable stride, self-closing: 59 (``u32 count`` x 10B entries)
* variable stride, anchor framed: 71 72 (nested sub-records; the row trailer is
  still the 12B identity, so framing is anchored on it and the leftover bytes /
  row-length histogram are reported instead of a hard stride assertion)
* zero rows in server_db, schema-only: 52 57

Usage
-----
  py -V:3.12 -I -B scripts/t101_starting_batch2.py --selftest
  py -V:3.12 -I -B scripts/t101_starting_batch2.py
  py -V:3.12 -I -B scripts/t101_starting_batch2.py --out scratch/t101/out

Exit codes: 0 ok, 1 acceptance/selftest failure, 2 usage or missing input.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import struct
import sys
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

FUNCS = ROOT / "scratch/t95/funcs"
VTABLE = ROOT / "scratch/t95/vtable_index.json"
FOURCC = Path(__file__).resolve().parents[1] / "scratch/t97/out/fourcc_mem_map.json"
DEFAULT_OUT = ROOT / "scratch/t101/out"
DEFAULT_DB = ROOT / "scratch/data/server_db.dat"

SCHEMA = "t101.starting_batch2.v1"
CHUNK = 5

U32 = struct.Struct("<I")
U16 = struct.Struct("<H")


def f(off: int, width: int, mem: int | None, name: str, line: int) -> dict:
    """One wire field: byte offset inside the row body (after the selector)."""
    return {"wire_off": off, "width": width,
            "mem_off": None if mem is None else f"0x{mem:02x}",
            "mem_off_int": mem, "name": name, "src_line": line}


# --------------------------------------------------------------------- specs
# `stride` excludes the 1-byte selector.  `fields` follow the exact read order
# of the C body; the 12B base identity block is listed as one synthetic field.
SPECS: dict[int, dict] = {}


def spec(tt, cls, entity, vtable, reader, reader_lines, reader_file, fields,
         mode="fixed", stride=None, fourcc_mode="own", note=""):
    if stride is None:
        stride = sum(x["width"] for x in fields if isinstance(x["width"], int))
    SPECS[tt] = dict(table_type=tt, cls=cls, entity=entity, vtable_va=vtable,
                     reader_va=reader, reader_file=reader_file,
                     reader_lines=reader_lines, mode=mode, stride=stride,
                     fields=fields, fourcc_mode=fourcc_mode, note=note)


spec(49, "STARTING_PERSON_HISTORY", "pers", "0x1418b6c88", "0x144381b80",
     [23, 33, 37, 43], "144381b80.c",
     [f(0, 4, 0x24, "date_dayyear", 23),
      f(4, 12, 0x18, "block0x18(comp,otel,team)", 33),
      f(16, 7, 0x28, "block0x28(otea,plac,ajob,prom)", 37),
      f(23, 12, 0x08, "base_identity(row,dbid,dbid2)", 43)],
     note="36B fixed; 792,149 rows; date u32 low16=day high16=year")

spec(50, "STARTING_MLS_TRADED_SLOT", "club", "0x141883fe8", "0x144543110",
     [24, 28, 32, 39, 56], "144543110.c",
     [f(0, 4, 0x18, "row_u32_0x18", 24),
      f(4, 4, 0x1c, "row_u32_0x1c", 28),
      f(8, 1, 0x24, "row_u8_0x24", 32),
      f(9, 4, 0x20, "row_u32_0x20", 39),
      f(13, 12, 0x08, "base_identity(row,dbid,dbid2)", 56)])

spec(51, "STARTING_MLS_GENERAL_ALLOCATION_MONEY", "club", "0x141884148",
     "0x1444c31f0", [22, 25, 28, 40], "1444c31f0.c",
     [f(0, 4, 0x18, "row_u32_0x18", 22),
      f(4, 4, 0x1c, "row_u32_0x1c", 25),
      f(8, 2, 0x20, "row_u16_0x20", 28),
      f(10, 12, 0x08, "base_identity(row,dbid,dbid2)", 40)])

spec(52, "STARTING_PLAYER_HAPPINESS", "play", "0x141884828", "0x144543d80",
     [10, 14, 18, 22, 26], "144543d80.c",
     [f(0, 4, 0x18, "row_u32_0x18", 10),
      f(4, 4, 0x20, "row_u32_0x20", 14),
      f(8, 2, 0x2c, "row_u16_0x2c", 18),
      f(10, 1, 0x2e, "row_u8_0x2e", 22),
      f(11, 4, 0x28, "row_u32_0x28", 26),
      f(15, 12, 0x08, "base_identity(row,dbid,dbid2)", 30)],
     note="0 rows in server_db; stride 27+1 derived from Hex-Rays only")

spec(57, "FIXTURE_NAME", "—", "0x1418852e8", "0x143e76470",
     [10, 14, 18, 22, 26], "143e76470.c",
     [f(0, 4, 0x18, "row_u32_0x18", 10),
      f(4, 4, 0x20, "row_u32_0x20", 14),
      f(8, 4, 0x28, "row_u32_0x28", 18),
      f(12, 4, 0x30, "row_u32_0x30", 22),
      f(16, 4, 0x40, "row_u32_0x40", 26),
      f(20, 12, 0x08, "base_identity(row,dbid,dbid2)", 30)],
     note="0 rows in server_db; stride 32+1 derived from Hex-Rays only")

spec(58, "STARTING_WEEKLY_WAGE_CONTRIBUTION", "club", "0x141883bc8",
     "0x1444dd8a0", [31, 44, 57, 70, 77, 90], "1444dd8a0.c",
     [f(0, 8, 0x18, "play_u64(+0x0)", 31),
      f(8, 8, 0x20, "club_u64(+0x4)", 44),
      f(16, 8, 0x28, "icom_u64(+0x8)", 57),
      f(24, 4, 0x30, "wend(+0xc)", 70),
      f(28, 4, 0x34, "wage(+0xd)", 77),
      f(32, 12, 0x08, "base_identity(row,dbid,dbid2)", 90)])

spec(59, "STARTING_MEDIA_EXPECTATIONS", "play", "0x141882fa8", "0x141583ba0",
     [43, 46, 50, 80, 87, 97, 158], "141583ba0.c",
     [f(0, 4, 0x18, "row_u32_0x18", 43),
      f(4, 1, 0x1c, "row_u8_0x1c", 46),
      f(5, "var", None, "count u32 + count*10B {sel,u32,u32,u8}", 50),
      f(None, 12, 0x08, "base_identity(row,dbid,dbid2)", 158)],
     mode="var59",
     note="variable: 22B (count=0) or 32B (count=1) rows; 10B entry = "
          "u8 sel + u32 + u32 + u8")

spec(60, "STARTING_MLS_TARGETED_ALLOCATION_MONEY", "club", "0x1418842a8",
     "0x1444c31f0", [22, 25, 28, 40], "1444c31f0.c",
     [f(0, 4, 0x18, "row_u32_0x18(=Ceta)", 22),
      f(4, 4, 0x1c, "row_u32_0x1c", 25),
      f(8, 2, 0x20, "row_u16_0x20(=Cety)", 28),
      f(10, 12, 0x08, "base_identity(row,dbid,dbid2)", 40)],
     note="shares reader 0x1444c31f0 with tt51/tt73")

spec(61, "STARTING_ITALIAN_SERIE_A_CLUB_THAT_FREED_UP_NON_EU_SLOT", "club",
     "0x141884408", "0x1445437b0", [22, 25, 28, 40], "1445437b0.c",
     [f(0, 4, 0x18, "row_u32_0x18", 22),
      f(4, 1, 0x1c, "row_u8_0x1c", 25),
      f(5, 2, 0x1e, "row_u16_0x1e", 28),
      f(7, 12, 0x08, "base_identity(row,dbid,dbid2)", 40)],
     note="shares reader 0x1445437b0 with tt63")

spec(62, "STARTING_RESERVE_TEAM", "club", "0x141884988", "0x143fc8d30",
     [16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56], "143fc8d30.c",
     [f(0, 1, 0x44, "Ttyp", 16),
      f(1, 4, 0x18, "Cclu/Clri(u64 low)", 20),
      f(5, 4, 0x20, "Cdvi/Tdvi(u64 low)", 24),
      f(9, 4, 0x30, "Tsti(u64 low)", 28),
      f(13, 4, 0x38, "Catd", 32),
      f(17, 4, 0x3c, "Cmxa", 36),
      f(21, 4, 0x40, "Cmna", 40),
      f(25, 1, 0x45, "Twhm", 44),
      f(26, 1, 0x46, "Tmhm", 48),
      f(27, 1, 0x47, "tmno", 52),
      f(28, 1, 0x48, "row_u8_0x48", 56),
      f(29, 12, 0x08, "base_identity(row,dbid,dbid2)", 60)])

spec(63, "STARTING_ITALIAN_SERIE_A_CLUB_NON_EU_SLOTS_NUMBER", "club",
     "0x141884568", "0x1445437b0", [22, 25, 28, 40], "1445437b0.c",
     [f(0, 4, 0x18, "row_u32_0x18", 22),
      f(4, 1, 0x1c, "row_u8_0x1c", 25),
      f(5, 2, 0x1e, "row_u16_0x1e", 28),
      f(7, 12, 0x08, "base_identity(row,dbid,dbid2)", 40)],
     note="shares reader 0x1445437b0 with tt61")

spec(64, "STARTING_CLUB_STAFF_JOB_STATUS", "club", "0x141884b48",
     "0x144540010", [23, 26, 29, 32, 44], "144540010.c",
     [f(0, 4, 0x18, "row_u32_0x18", 23),
      f(4, 2, 0x20, "row_u16_0x20", 26),
      f(6, 1, 0x22, "row_u8_0x22", 29),
      f(7, 1, 0x23, "row_u8_0x23", 32),
      f(8, 12, 0x08, "base_identity(row,dbid,dbid2)", 44)])

for _tt in (65, 67, 68, 69):
    spec(_tt, "STARTING_NEWGEN_PARAMETER", "pers", "0x141884ca8", "0x1444c4820",
         [20, 21, 32, 47], "1444c4820.c",
         [f(0, 4, 0x28, "row_u32_0x28", 20),
          f(4, 14, 0x18, "newgen_block(sub_14475B320)", 21),
          f(18, 12, 0x08, "base_identity(row,dbid,dbid2)", 32)],
         fourcc_mode="own",
         note="nested 14B = u8 ver + u32 + u32 + (ver>=2 ? u32 : u8->float) + u8")

spec(66, "STARTING_CLUB_TRANSFER_PREFERENCE", "club", "0x141884e08",
     "0x1444c39b0", [10, 14, 18, 22, 26], "1444c39b0.c",
     [f(0, 4, 0x18, "row_u32_0x18", 10),
      f(4, 4, 0x1c, "nati", 14),
      f(8, 1, 0x20, "rati", 18),
      f(9, 1, 0x21, "mina", 22),
      f(10, 1, 0x22, "maxa", 26),
      f(11, 12, 0x08, "base_identity(row,dbid,dbid2)", 30)])

spec(70, "STARTING_VISION_OBJECTIVE", "club", "0x141884f68", "0x1443802e0",
     [17, 21, 25, 29, 33, 37, 41, 45, 49, 53, 57, 61], "1443802e0.c",
     [f(0, 4, 0x18, "row_u32_0x18", 17),
      f(4, 4, 0x20, "row_u32_0x20", 21),
      f(8, 4, 0x28, "comp", 25),
      f(12, 4, 0x2c, "nati", 29),
      f(16, 2, 0x30, "wrcl", 33),
      f(18, 2, 0x32, "styr", 37),
      f(20, 2, 0x34, "enyr", 41),
      f(22, 1, 0x36, "type", 45),
      f(23, 1, 0x37, "levl", 49),
      f(24, 1, 0x38, "mage", 53),
      f(25, 1, 0x39, "mlen", 57),
      f(26, 1, 0x3a, "isog", 61),
      f(27, 12, 0x08, "base_identity(row,dbid,dbid2)", 65)])

spec(71, "STARTING_PAST_TRANSFER", "pers", "0x14188df58", "0x141199440",
     [44, 48, 52, 59, 67, 71, 75, 79, 83, 153, 160, 171, 176, 181, 185, 189],
     "141199440.c",
     [f(0, 4, 0x24, "row_u32_0x24", 44),
      f(4, 4, 0x1c, "plyr", 48),
      f(8, 4, 0x20, "row_u32_0x20", 52),
      f(12, 4, 0x28, "row_u32_0x28", 59),
      f(16, 4, 0x54, "row_u32_0x54", 67),
      f(20, 1, 0x2c, "row_u8_0x2c", 71),
      f(21, 1, 0x59, "PPty", 75),
      f(22, 1, 0x5a, "Pmdt", 79),
      f(23, "var", None, "u8 n + n*sub_1411919D0 sub-records", 83),
      f(None, 1, 0x10, "row_u8_0x10", 160),
      f(None, "opt", None, "optional sub-object (build<0xDDD gate)", 171),
      f(None, 12, 0x08, "base_identity(row,dbid,dbid2)", 194)],
     mode="anchor",
     note="nested sub_1411919D0 (0x1411919d0.c) + 48B array + version-gated "
          "sub-object; row trailer = 12B identity")

spec(72, "STARTING_PAST_TRADE", "pers", "0x1418bdb48", "0x1444dff00",
     [9, 13, 16, 18, 20, 22, 24, 27, 30, 33, 36, 39], "1444dff00.c",
     [f(0, 4, 0x18, "row_u32_0x18", 9),
      f(4, 4, 0x20, "row_u32_0x20", 13),
      f(8, "vec", None, "vector A (sub_141726770)", 16),
      f(None, "vec", None, "vector B (sub_141726770)", 18),
      f(None, "vec", None, "vector C (sub_141726770)", 20),
      f(None, "vec", None, "vector D (sub_141726770)", 22),
      f(None, 4, 0x28, "row_u32_0x28 (ref u32)", 24),
      f(None, 4, 0x2c, "row_u32_0x2c", 27),
      f(None, "date4", None, "4x date pair (sub_141541000/141541480)", 30),
      f(None, 12, 0x08, "base_identity(row,dbid,dbid2)", 43)],
     mode="anchor",
     note="4x sub_141726770 vectors + 4x date-pair blocks; row trailer = 12B identity")

spec(73, "STARTING_ITALIAN_SERIE_A_NON_EU_PLAYER_SIGNED_FOR_RESTRICTED_SLOT",
     "play", "0x1418846c8", "0x1444c31f0", [22, 25, 28, 40], "1444c31f0.c",
     [f(0, 4, 0x18, "row_u32_0x18", 22),
      f(4, 4, 0x1c, "row_u32_0x1c", 25),
      f(8, 2, 0x20, "row_u16_0x20", 28),
      f(10, 12, 0x08, "base_identity(row,dbid,dbid2)", 40)],
     note="shares reader 0x1444c31f0 with tt51/tt60")

TARGETS = [49, 50, 51, 52, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69,
           70, 71, 72, 73]


# ------------------------------------------------------------------- decoding
def decode_fixed(body: bytes, count: int, stride: int) -> dict:
    """Fixed-stride pass: selector + identity postcondition for every row."""
    total = count * stride
    ok = len(body) >= total
    sels = Counter()
    ident_bad = []
    dayyear = {"ok": 0, "n": 0}
    for i in range(count if ok else 0):
        row = body[i * stride:(i + 1) * stride]
        sels[row[0]] += 1
        if stride >= 13:
            r, a, b = struct.unpack_from("<III", row, stride - 12)
            if r != i or a != b:
                if len(ident_bad) < 5:
                    ident_bad.append({"row": i, "identity": [r, a, b]})
                continue
        dayyear["n"] += 1
        dayyear["ok"] += 1
    return {"mode": "fixed_stride", "stride_incl_selector": stride,
            "rows": count, "consumed": total, "body_len": len(body),
            "closure": total == len(body), "selectors": dict(sels.most_common(8)),
            "identity_violations": len(ident_bad),
            "identity_violation_samples": ident_bad,
            "date_valid_rows": dayyear["ok"]}


def decode_var59(body: bytes, count: int) -> dict:
    """tt59: u32 + u8 + u32(n) + n*(u8,u32,u32,u8) + 12B identity."""
    pos, lens, sels, cnt_hist, ident_bad, entries = 0, Counter(), Counter(), Counter(), [], 0
    n = len(body)
    day_ok = 0
    for i in range(count):
        if pos + 6 > n:
            return {"mode": "var_59", "error": f"truncated at row {i}", "pos": pos}
        sels[body[pos]] += 1
        p = pos + 1 + 4 + 1
        c = U32.unpack_from(body, p)[0]
        p += 4
        if c > 4096 or p + 10 * c + 12 > n:
            return {"mode": "var_59", "error": f"bad entry count {c} at row {i}",
                    "pos": pos}
        entries += c
        cnt_hist[c] += 1
        p += 10 * c
        r, a, b = struct.unpack_from("<III", body, p)
        if r != i or a != b:
            if len(ident_bad) < 5:
                ident_bad.append({"row": i, "identity": [r, a, b]})
        else:
            day_ok += 1
        p += 12
        lens[p - pos] += 1
        pos = p
    return {"mode": "var_59", "rows": count, "consumed": pos, "body_len": n,
            "closure": pos == n, "row_len_histogram": dict(sorted(lens.items())),
            "entries_total": entries,
            "entries_per_row_histogram": dict(sorted(cnt_hist.items())),
            "selectors": dict(sels.most_common(8)),
            "identity_violations": len(ident_bad),
            "identity_violation_samples": ident_bad}


IDENT_STRUCT = struct.Struct("<III")


def decode_anchor(body: bytes, count: int, first_ordinal: int = 0) -> dict:
    """Variable-stride framing anchored on the 12B base identity trailer.

    The trailer is ``(row_index, dbid, dbid2)`` with ``dbid == dbid2``; rows are
    delimited by the smallest offset ``>= start+margin`` that satisfies it with
    the expected ascending row index.  Leftover bytes are reported verbatim
    instead of being forced into a stride.
    """
    pos, lens, sels, ident_bad = 0, Counter(), Counter(), []
    n = len(body)
    margin = 20
    for k in range(count):
        want = first_ordinal + k
        sels[body[pos]] += 1
        found = None
        j = pos + margin
        while j + 12 <= n:
            if body[j] == (want & 0xFF) and body[j + 1] == ((want >> 8) & 0xFF) \
                    and body[j + 2] == ((want >> 16) & 0xFF) and body[j + 3] == ((want >> 24) & 0xFF):
                a, b = struct.unpack_from("<II", body, j + 4)
                if a == b:
                    found = j
                    break
            j += 1
        if found is None:
            ident_bad.append({"row": k, "why": "anchor not found", "pos": pos})
            break
        lens[found + 12 - pos] += 1
        pos = found + 12
    return {"mode": "anchor_identity", "rows_framed": k + 1 if count else 0,
            "rows_expected": count, "consumed": pos, "body_len": n,
            "leftover_bytes": n - pos,
            "closure": pos == n and len(ident_bad) == 0,
            "row_len_histogram": dict(sorted(lens.items())[:24]),
            "row_len_distinct": len(lens),
            "selectors": dict(sels.most_common(8)),
            "identity_violations": len(ident_bad),
            "identity_violation_samples": ident_bad[:5]}


# ------------------------------------------------------------------ 4CC census
def own_fourccs(vtable_index: dict, tt: int) -> dict:
    for t in vtable_index["tables"]:
        if t["table_type"] == tt:
            out = {}
            for slot in ("slot02_get_prop", "slot03_set_prop"):
                s = t["core"].get(slot, {})
                out[slot] = {"va": s.get("va"), "lines": s.get("lines")}
            return out
    return {}


def fourcc_rows(fourcc_map: dict, tt: int, own_vtable_slots: dict) -> list:
    """4CC rows whose accessor is the table's own slot02/03 body."""
    own_vas = {v.get("va") for v in own_vtable_slots.values() if v.get("va")}
    rows = []
    for t in fourcc_map["tables"]:
        if t["table_type"] != tt:
            continue
        for cc, info in sorted(t["fourccs"].items()):
            if info.get("func_va") not in own_vas:
                continue
            rows.append({"fourcc": cc, "slot": info["slot"],
                         "mem_off": info["primary_off"],
                         "width": info["width"], "kind": info["kind"]})
    return rows


# --------------------------------------------------------------------- driver
def run_table(tt: int, payload: bytes, vi: dict, fm: dict) -> dict:
    sp = SPECS[tt]
    version, count = struct.unpack_from("<HI", payload, 6)
    footer = payload[-9:]
    body = payload[13:len(payload) - 9]
    entry = {"table_type": tt, "class": sp["cls"], "entity": sp["entity"],
             "vtable_va": sp["vtable_va"],
             "reader": {"va": sp["reader_va"], "file": f"funcs/{sp['reader_file']}",
                        "lines": sp["reader_lines"]},
             "wire": {"selector_bytes": 1, "field_count": len(sp["fields"]),
                      "max_stride_incl_selector": sp["stride"] + 1,
                      "fields": sp["fields"]},
             "payload": {"len": len(payload), "version": version,
                         "declared_count": count, "body_len": len(body),
                         "footer_hex": footer.hex(),
                         "payload_sha256": hashlib.sha256(payload).hexdigest(),
                         "closure": 13 + count * 0 + len(body) + 9 == len(payload)},
             "fourcc": {"own_vtable_slots": own_fourccs(vi, tt),
                        "own_4cc_rows": fourcc_rows(fm, tt, own_fourccs(vi, tt))},
             "note": sp["note"]}

    if sp["mode"] == "fixed":
        entry["validation"] = decode_fixed(body, count, sp["stride"] + 1)
    elif sp["mode"] == "var59":
        entry["validation"] = decode_var59(body, count)
    else:
        entry["validation"] = decode_anchor(body, count, 0)

    v = entry["validation"]
    entry["status"] = ("closed" if v.get("closure") else
                       ("anchored_partial" if sp["mode"] == "anchor" else "open"))
    if count == 0:
        entry["status"] = "schema_only_zero_rows"
    return entry


def load_inputs():
    import t38_multiframe as mf  # noqa: E402  (read-only helper module)
    vi = json.loads(VTABLE.read_text(encoding="utf-8"))
    fm = json.loads(FOURCC.read_text(encoding="utf-8"))
    return mf, vi, fm


def selftest() -> int:
    print("t101 selftest")
    ok = True
    for path, label in ((FUNCS, "t95 funcs"), (VTABLE, "vtable_index"),
                        (FOURCC, "fourcc map"), (DEFAULT_DB, "server_db")):
        state = "ok" if path.exists() else "MISS"
        print(f"  {label:14s} {state:4s} {path}")
        ok &= path.exists()
    missing = []
    for tt in TARGETS:
        sp = SPECS.get(tt)
        if sp is None:
            missing.append(tt)
            continue
        if not (FUNCS / sp["reader_file"]).exists():
            print(f"  reader file missing for tt{tt}: {sp['reader_file']}")
            ok = False
    if missing:
        print(f"  specs missing for {missing}")
        ok = False
    if len(TARGETS) != 21:
        print(f"  target count {len(TARGETS)} != 21")
        ok = False
    payload_16 = b"\x03\x01tad." + struct.pack("<HI", 3569, 2) + b"\x00" * 2
    try:
        print(f"  struct sanity  {struct.unpack_from('<HI', payload_16, 6)}")
    except Exception as exc:  # pragma: no cover
        print(f"  struct sanity failed: {exc}")
        ok = False
    print("  RESULT", "ok" if ok else "FAIL")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(
        description="STARTING_* batch-2 (tt 49..73) L3 wire schemas + live validation.")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT, help="output directory")
    ap.add_argument("--db", type=Path, default=DEFAULT_DB, help="server_db archive (read-only)")
    ap.add_argument("--selftest", action="store_true", help="check inputs only, no decode")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    if args.selftest:
        return selftest()
    if not VTABLE.exists() or not FUNCS.exists() or not args.db.exists():
        print("missing input (vtable_index / funcs / server_db)", file=sys.stderr)
        return 2
    if not DEFAULT_OUT.parent.exists():
        print("scratch/t101 missing", file=sys.stderr)
        return 2

    mf, vi, fm = load_inputs()
    codec = mf._codec()
    cache: dict = {}
    args.out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    tables: dict[str, dict] = {}
    doc = {"schema": SCHEMA, "status": "partial", "generated_by": "t101",
           "outdir": str(args.out.relative_to(ROOT)).replace("\\", "/"),
           "targets": TARGETS, "tables": tables}

    for idx, tt in enumerate(TARGETS, 1):
        payload = mf.load_payload_mf(codec, "server", tt, cache)
        entry = run_table(tt, payload, vi, fm)
        tables[str(tt)] = entry
        v = entry["validation"]
        print(f"[{idx:2d}/{len(TARGETS)}] tt{tt:<3d} {entry['class'][:44]:44s} "
              f"n={entry['payload']['declared_count']:>7d} "
              f"mode={v['mode']:16s} closure={v.get('closure')} status={entry['status']}")
        if idx % CHUNK == 0 or idx == len(TARGETS):
            doc["completed_tables"] = idx
            doc["elapsed_sec"] = round(time.time() - t0, 1)
            (args.out / "batch2_schemas.json").write_text(
                json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
            print(f"        -> flushed batch2_schemas.json ({idx} tables)")

    # ---- summary
    closed = [t for t in tables.values() if t["status"] == "closed"]
    anchored = [t for t in tables.values() if t["status"] == "anchored_partial"]
    schema_only = [t for t in tables.values() if t["status"] == "schema_only_zero_rows"]
    open_ = [t for t in tables.values() if t["status"] == "open"]
    rows_total = sum(t["payload"]["declared_count"] for t in tables.values())
    (args.out / "batch2_schemas.json").write_text(
        json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")

    summary = {
        "tables": len(tables), "closed": len(closed),
        "anchored_partial": len(anchored), "schema_only": len(schema_only),
        "open": len(open_), "rows_total": rows_total,
        "rows_closed": sum(t["payload"]["declared_count"] for t in closed),
        "bytes_validated": sum(t["payload"]["len"] for t in tables.values()),
        "elapsed_sec": round(time.time() - t0, 1),
    }
    print("\nsummary:", json.dumps(summary, ensure_ascii=False))
    return 0 if not open_ else 1


if __name__ == "__main__":
    raise SystemExit(main())
