"""t138_people_pure_py — pure-Python streaming decoder for FM24 people_db.dat.

Goal (prompt zcode_t138_people_pure_py.md): decode ALL 658,011 person rows of the
400,443,970-byte decompressed people_db.dat with ZERO runtime dependencies beyond the
vendored zstandard, using no Unicorn / no IDA at runtime, and NO heuristic
identity-skipping — every branch below mirrors the real editor.exe C grammar.

Grammar source of truth:
  * Hex-Rays decompilations in scratch/t138/out/ida/<funcva>.c (via idalib on
    scratch/t95/editor_work.i64 only — editor_merge_v2.i64 untouched).
  * Read-by-read Unicorn traces in scratch/t120/out/people_unicorn_traces.json
    (slot19 polymorphic readers, real editor.exe factory sub_1410992C0).
  * Oracle walk of the first 3,000 rows in scratch/t126/out/_walk.json
    (end_offset == 1,216,813, per-row off/pt/len/ord).

Wire layout of the decompressed payload:
  raw[0:2]  two zero bytes
  raw[2:6]  u32 LE person count (658,011)
  rows from offset 6:  [u32 ordinal][u8 ptype][body]
  body = exactly the bytes consumed by the ptype's slot19 reader chain.
  footer (28 B, decode_footer): [u32][u32] case-3 table counts (loader-read,
  sub_140F64530 case 3) + 20-byte writer-only commit trailer, closed byte-exact
  (full-walk diff == 0; provenance in decode_footer's docstring).

Runtime constants (from qword_141B60330 / qword_141B6034C / byte_141B5FC2C):
  VERSION = 0x0DF1 (3569), REF8 = HIBYTE(qword_141B6034C) = 1, FC2C = byte_141B5FC2C = 0.

Person type -> slot19 reader:
  1 NON_PLAYER                0x140DC1D30 (a3=1)
  2 PLAYER                    0x140E06EC0 (a3=1)
  3 ACTUAL_PLAYER_AND_NON_PLAYER 0x1415D5110 (PLAYER a3=0 + NON_PLAYER a3=0 + shared tail)
  4 OFFICIAL                  0x1415856B0
  5 RETIRED_PERSON
The a3 flag only gates each subreader's tail chain (DD8520 -> DFB5C0 -> PERSON base);
with a3=0 the tail is skipped and the type3 dispatcher runs the chain exactly once.

Unknown / not-yet-mapped conditional branches raise BranchError carrying the row and
wire offset — the walk stops honestly instead of guessing.
"""
from __future__ import annotations
import sys as _cfg_sys
from pathlib import Path as _cfg_pathlib
_cfg_sys.path.insert(0, str(_cfg_pathlib(__file__).resolve().parent))
import fm24_config as _cfg

import argparse
import io
import json
import sys
import time
from array import array
from heapq import nlargest
from pathlib import Path
from struct import unpack_from, error as struct_error

sys.path.insert(0, str(_cfg.VENDOR_DIR))
import zstandard  # vendored, zero-install

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "scratch/data/people_db.dat"
ORACLE_PATH = ROOT / "scratch/t126/out/_walk.json"
OUT_DIR = ROOT / "scratch/t138/out"
T106_DIR = ROOT / "scratch/t106/out"


def load_name_pools() -> tuple[dict, dict, dict]:
    """t106 name pools: payload_server_name_table_extra_{0,1,2}.bin.

    Each file: 12-byte 'tad.' header with u32 count at +8, then records
    [u32 uid][u32 len][len UTF-8 bytes] (verified closure by t106).
    Returns (first_names, second_names, common_names) as uid->str dicts.
    """
    pools = []
    for idx in (0, 1, 2):
        b = (T106_DIR / f"payload_server_name_table_extra_{idx}.bin").read_bytes()
        cnt = unpack_from("<I", b, 8)[0]
        pos = 12
        mp: dict = {}
        for _ in range(cnt):
            uid, slen = unpack_from("<II", b, pos)
            pos += 8
            mp[uid] = b[pos : pos + slen].decode("utf-8", errors="replace")
            pos += slen
        if pos != len(b):
            raise ValueError(f"name_table_extra_{idx}: closure {pos} != {len(b)}")
        pools.append(mp)
    return pools[0], pools[1], pools[2]


def resolve_person_name(entries: list[dict], pools: tuple[dict, dict, dict]) -> str:
    """t135 convention: common name wins, else 'first second'."""
    first, second, common = (e.get("inline_name") for e in entries)
    ids = (e["id"] for e in entries)
    if first is None:
        fid, sid, cid = ids
        first = pools[0].get(fid & 0xFFFFFFFF, "") if fid >= 0 else ""
        second = pools[1].get(sid & 0xFFFFFFFF, "") if sid >= 0 else ""
        common = pools[2].get(cid & 0xFFFFFFFF, "") if cid >= 0 else ""
    second = second or ""
    common = (common or "").strip()
    return common if common else f"{first} {second}".strip()

VERSION = 0x0DF1  # 3569
REF8 = True       # HIBYTE(qword_141B6034C)
FC2C = False      # byte_141B5FC2C

PTYPE_NAMES = {
    1: "NON_PLAYER",
    2: "PLAYER",
    3: "ACTUAL_PLAYER_AND_NON_PLAYER",
    4: "OFFICIAL",
    5: "RETIRED_PERSON",
}


class BranchError(Exception):
    """A conditional branch whose C grammar is not fully mapped yet."""

    def __init__(self, func: str, detail: str):
        super().__init__(f"{func}: {detail}")
        self.func = func
        self.detail = detail


class Wire:
    """Sequential reader over the decompressed payload (bytes)."""

    __slots__ = ("b", "p", "end")

    def __init__(self, b: bytes, p: int = 0):
        self.b = b
        self.p = p
        self.end = len(b)

    def u8(self) -> int:
        p = self.p
        v = self.b[p]
        self.p = p + 1
        return v

    def u16(self) -> int:
        p = self.p
        v = unpack_from("<H", self.b, p)[0]
        self.p = p + 2
        return v

    def u32(self) -> int:
        p = self.p
        v = unpack_from("<I", self.b, p)[0]
        self.p = p + 4
        return v

    def i32(self) -> int:
        p = self.p
        v = unpack_from("<i", self.b, p)[0]
        self.p = p + 4
        return v

    def take(self, n: int) -> None:
        p = self.p + n
        if p > self.end:
            raise IndexError(f"overread take({n}) at {self.p}")
        self.p = p

    def read(self, n: int) -> bytes:
        """take(n) that also returns the bytes (used by footer verification)."""
        p = self.p + n
        if p > self.end:
            raise IndexError(f"overread take({n}) at {self.p}")
        out = self.b[self.p : p]
        self.p = p
        return out

    def string(self) -> int:
        """[u32 len][len bytes] — returns the length."""
        n = self.u32()
        p = self.p + n
        if p > self.end:
            raise IndexError(f"overread string({n}) at {self.p}")
        self.p = p
        return n


# ----------------------------------------------------------------------------
# Primitive readers (each mirrors one decompiled function)
# ----------------------------------------------------------------------------

def x_date(r: Wire) -> None:
    """sub_143B934A0: [u32][u8 f]; f!=0 -> sub_1410B9440 [u32 len][len][8][2][4][1][1]."""
    r.u32()
    if r.u8() != 0:
        n = r.u32()
        r.take(n)
        r.take(8 + 2 + 4 + 1 + 1)


def x_person_base(r: Wire) -> None:
    """sub_143F2B820 (via 141084540, a3=0): [8][12] — [12] = identity ordinal/dbid/uid."""
    r.take(8)
    r.take(12)


def x_c07d00(r: Wire) -> None:
    """sub_143C07D00: [4] + (REF8 && !FC2C ? [13] : [4]) + [2]."""
    r.u32()
    if REF8 and not FC2C:
        r.take(13)
    else:
        r.take(4)
    r.u16()


def x_14009c0(r: Wire) -> None:
    """sub_1414009C0 (0x1442FFBE0): [1][2][1][4] = 8B, unconditional."""
    r.u8()
    r.u16()
    r.u8()
    r.u32()


def x_14141e220(r: Wire) -> None:
    """sub_14141E220 (0x14432A580) at VERSION=0x0DF1 (>=0xDCD):
    [1][2][1][1 b]; b==1 -> [4 @a1] else [8 @a1].  (Verified vs row-1213 trace r45-r94.)"""
    r.u8()
    r.u16()
    r.u8()
    b = r.u8()
    r.take(4 if b == 1 else 8)


def x_1400230(r: Wire) -> None:
    """sub_141400230: [u8 n1][n1!=0: n1*16 merged][i32 n2][n2>0: n2*7][1][1][1]
    [u8 n3][n3 * sub_1414009C0][1 if VERSION>=0xDF0]."""
    n1 = r.u8()
    if n1 != 0:
        r.take(16 * n1)
    n2 = r.i32()
    if n2 > 0:
        r.take(7 * n2)
    r.u8()
    r.u8()
    r.u8()
    n3 = r.u8()
    for _ in range(n3):
        x_14009c0(r)
    r.u8()  # VERSION >= 0xDF0


def x_14156add0(r: Wire) -> None:
    """sub_14156ADD0: [2][4][4][4][2][1][4][4][1][4][1] = 31B."""
    r.u16()
    r.u32()
    r.u32()
    r.u32()
    r.u16()
    r.u8()
    r.u32()
    r.u32()
    r.u8()
    r.u32()
    r.u8()


def x_141727530(r: Wire) -> None:
    """sub_141727530 (0x144749220): [1 v16][2][4] + (v16>=2: [4]) + (v16>=5: [4])
    + (v16<3 ? [1] : [1][1]) + (v16>=4: [1])."""
    v16 = r.u8()
    r.u16()
    r.u32()
    if v16 >= 2:
        r.u32()
    if v16 >= 5:
        r.u32()
    if v16 < 3:
        r.u8()
    else:
        r.u8()
        r.u8()
    if v16 >= 4:
        r.u8()


def x_141727d70(r: Wire) -> None:
    """sub_141727D70: [u32 n][n * sub_14156ADD0]."""
    n = r.u32()
    for _ in range(n):
        x_14156add0(r)


def x_141727c60(r: Wire) -> None:
    """sub_141727C60 (0x14474B9D0): [1][2][8] + sub_141727D70 + [2][8] + sub_141727D70."""
    r.u8()
    r.u16()
    r.take(8)
    x_141727d70(r)
    r.u16()
    r.take(8)
    x_141727d70(r)


def x_14141d290(r: Wire) -> None:
    """sub_14141D290: [u32 n][n * sub_141727530]."""
    n = r.u32()
    for _ in range(n):
        x_141727530(r)


def x_140f80b80(r: Wire) -> None:
    """sub_140F80B80 — only partially mapped (path A [8]; path B [1 v50]...).
    Complex v50!=0 path (sub_140F92E30/140F92AB0) not yet wire-verified."""
    raise BranchError("sub_140F80B80", "complex path not mapped")


def x_141727790(r: Wire) -> None:
    """sub_141727790: [1] + sub_14141D290 + sub_140F80B80."""
    r.u8()
    x_14141d290(r)
    x_140f80b80(r)


def x_141420390(r: Wire) -> None:
    """sub_141420390 (DD8520 v239b loop element) — element shape not yet wire-verified."""
    raise BranchError("sub_141420390", "element grammar not mapped")


# ----------------------------------------------------------------------------
# Career objects (DD8520 v239 loop — dispatcher obj_140EE7C20)
# ----------------------------------------------------------------------------

def x_af70(r: Wire) -> None:
    """sub_14156AF70 (CASE0 v81 loop element): [2][4][10][1][9][4] + queued [1] = 31B."""
    r.u16()
    r.u32()
    r.take(10)
    r.u8()
    r.take(9)
    r.u32()
    r.u8()


def x_c4670(r: Wire) -> None:
    """sub_1414C4670 (EDFB90 n-loop element): [1 b][1][3][8][8][2] + (b>=7 ? [2] : [1][1]) + [4]."""
    b = r.u8()
    r.u8()
    r.take(3)
    r.take(8)
    r.take(8)
    r.u16()
    if b >= 7:
        r.u16()
    else:
        r.u8()
        r.u8()
    r.u32()


def x_edf6c0(r: Wire) -> None:
    """sub_140EDF6C0: [5 (b0=v24, b1=v25)][v25!=0:+1][v25>=2:+1][v25>=3:+1][v25>=4:+1]
    [v25>=5: +1+(v25-5)] + tail [4 if v24>2 else 2] (queued, wire order preserved)."""
    b = r.b[r.p:r.p + 5]
    r.take(5)
    v24 = b[0]
    v25 = b[1]
    n = (1 if v25 != 0 else 0) + (1 if v25 >= 2 else 0) + (1 if v25 >= 3 else 0) + (1 if v25 >= 4 else 0)
    if v25 >= 5:
        n += 1 + (v25 - 5)
    r.take(n)
    r.take(4 if v24 > 2 else 2)


def x_edfb90(r: Wire) -> None:
    """sub_140EDFB90: [12][8][6][u32 n][n * sub_1414C4670][1][4][7][8][4][1] + sub_143C07D00."""
    r.take(12)
    r.take(8)
    r.take(6)
    n = r.u32()
    for _ in range(n):
        x_c4670(r)
    r.u8()
    r.u32()
    r.take(7)
    r.take(8)
    r.u32()
    r.u8()
    x_c07d00(r)


def x_case0(r: Wire) -> None:
    """sub_141421090 (career obj t==0): [1][16][8][1][2][u8 v80][v80>0: 8*v80]
    [u8 v81][v81 * sub_14156AF70][u32 n75][n75*31B][1] + sub_140EDF6C0 + sub_140EDFB90."""
    r.u8()
    r.take(16)
    r.take(8)
    r.u8()
    r.u16()
    v80 = r.u8()
    if v80 > 0:
        r.take(8 * v80)
    v81 = r.u8()
    for _ in range(v81):
        x_af70(r)
    n75 = r.u32()
    for _ in range(n75):
        r.take(31)
    r.u8()
    x_edf6c0(r)
    x_edfb90(r)


def x_141441770(r: Wire) -> None:
    """sub_141441770: [1] + 7 counted groups + [4][1][1][1].
    g1 elem [1][4][1][1]=7B; g2..g5 elem [1][4][1]=6B; g6 elem [1][4][1][4][4]=14B;
    g7 elem sub_14156ADD0 (31B)."""
    r.u8()
    n = r.u8()
    for _ in range(n):
        r.take(7)
    for _ in range(4):
        n = r.u8()
        for _ in range(n):
            r.take(6)
    n = r.u8()
    for _ in range(n):
        r.take(14)
    n = r.u8()
    for _ in range(n):
        x_14156add0(r)
    r.u32()
    r.u8()
    r.u8()
    r.u8()


def x_career_case1(r: Wire) -> None:
    """Career obj t==1: vtable 0x141889138 slot4 = sub_14103B0D0:
    [1 flag][flag!=0: sub_141441770 + [1 n66] + n66*31B] + [1] + [6] + [9] + [4] + [76]
    + sub_140EDFB90."""
    if r.u8() != 0:
        x_141441770(r)
        n66 = r.u8()
        for _ in range(n66):
            r.take(31)
    r.u8()
    r.take(6)
    r.take(9)
    r.u32()
    r.take(76)
    x_edfb90(r)


def x_career_obj(r: Wire, t: int) -> None:
    """obj_140EE7C20(t) — DD8520 v239 loop career-object dispatch."""
    if t == 0:
        x_case0(r)
    elif t == 1:
        x_career_case1(r)
    elif t in (2, 3, 4):
        x_edfb90(r)
    elif t == 5:
        x_c07d00(r)
    else:
        raise BranchError("obj_140EE7C20", f"career type {t}")


# ----------------------------------------------------------------------------
# sub_140DD8520 / sub_140DFB5C0 (shared tail part 1 + part 2, always a3=0 here)
# ----------------------------------------------------------------------------

def x_dd8520(r: Wire) -> None:
    """sub_140DD8520 (a3=0): [u16][8][u8*4][8][u8][u8 v233 (i8>0: v233*u32)][4]
    [u8 v239: v239*([u8 t]; t!=0xFF -> career obj)][u8 v239b: v239b * sub_141420390]
    [u8 v234: v234*9B][u32 v231: v231 * sub_14141E220][u8 v230!=0: 15B sub_143EB4E80]
    [u16 v228>0: v228*u32] + 36B tail [2][4][1][8][4][4][4][1][8]."""
    r.u16()
    r.take(8)
    r.take(4)
    r.take(8)
    r.u8()
    v233 = r.u8()
    if 0 < v233 < 128:  # signed i8 > 0
        r.take(4 * v233)
    r.u32()
    v239 = r.u8()
    for _ in range(v239):
        t = r.u8()
        if t != 0xFF:
            x_career_obj(r, t)
    v239b = r.u8()
    for _ in range(v239b):
        x_141420390(r)
    v234 = r.u8()
    for _ in range(v234):
        r.take(9)
    v231 = r.u32()
    for _ in range(v231):
        x_14141e220(r)
    if r.u8() != 0:
        r.take(15)  # sub_143EB4E80 [7][4][1][2][1]
    v228 = r.u16()
    for _ in range(v228):
        r.u32()
    r.take(36)


def x_141457830(r: Wire) -> None:
    """sub_141457830: [u8 n][n * ([u8][string][u32])]."""
    n = r.u8()
    for _ in range(n):
        r.u8()
        r.string()
        r.u32()


def x_dfb5c0(r: Wire, name_sink: list | None = None) -> None:
    """sub_140DFB5C0 (a3=0): 3*date + string + [4][5][16][8]
    + [u8 v38!=0: sub_141400230] + [u8 v39!=0: sub_141457830] + [4].

    The three sub_143B934A0 "date" calls are the person NAME-ID reads
    (first / second / common name, pool picked by the caller's a3 via
    qword_141B5FDA8+200/208/216). Each is [i32 id][u8 flag]; flag!=0 makes the
    reader register a fresh pool entry by reading the name string inline
    (sub_1410B9440: [u32 len][len bytes][8][2][4][1][1]).  When name_sink is
    given, the three entries are appended as dicts for Top-20 name resolution.
    """
    for _ in range(3):
        pid = r.i32()
        flag = r.u8()
        entry: dict = {"id": pid, "flag": flag, "inline_name": None}
        if flag != 0:
            n = r.u32()
            if n > (1 << 20):
                raise BranchError("x_dfb5c0", f"implausible inline name length {n}")
            entry["inline_name"] = r.read(n).decode("utf-8", errors="replace")
            r.take(16)
        if name_sink is not None:
            name_sink.append(entry)
    r.string()
    r.take(4)
    r.take(5)
    r.take(16)
    r.take(8)
    if r.u8() != 0:
        x_1400230(r)
    if r.u8() != 0:
        x_141457830(r)
    r.take(4)


# ----------------------------------------------------------------------------
# CONTRACT (sub_14145F800) and its optional subreaders
# ----------------------------------------------------------------------------

def x_1415f6ed0(r: Wire) -> None:
    """sub_1415F6ED0: [u8 b][b>=6 ? 11B : 10B]."""
    b = r.u8()
    r.take(11 if b >= 6 else 10)


def x_14172a440(r: Wire) -> None:
    """sub_14172A440: [1][u8 n][n * ([1 v46][1][2][4][2][4]
    + (v46<2: [4]; v46==2: [2]; v46>=3: [2][4]))]."""
    r.u8()
    n = r.u8()
    for _ in range(n):
        v46 = r.u8()
        r.u8()
        r.u16()
        r.u32()
        r.u16()
        r.u32()
        if v46 < 2:
            r.u32()
        elif v46 == 2:
            r.u16()
        else:
            r.u16()
            r.u32()


def x_1408386a0(r: Wire) -> None:
    """sub_1408386A0 (sub_14145E300 vector element tail) — variant switch not yet mapped."""
    raise BranchError("sub_1408386A0", "variant switch not mapped")


def x_14145e300(r: Wire) -> None:
    """sub_14145E300: [1][u32 n][n * ([1][1][4] + sub_1408386A0)]."""
    r.u8()
    n = r.u32()
    for _ in range(n):
        r.u8()
        r.u8()
        r.u32()
        x_1408386a0(r)


def x_14172a120(r: Wire) -> None:
    """sub_14172A120: [u8 b][3][4][b>=2 ? [1][2] : [1]]."""
    b = r.u8()
    r.take(3)
    r.u32()
    if b >= 2:
        r.u8()
        r.u16()
    else:
        r.u8()


def x_14146e9f0(r: Wire) -> None:
    """sub_14146E9F0: [1 b][1][2][1][2][1][1] + (b>=2: 4*u16)."""
    b = r.u8()
    r.u8()
    r.u16()
    r.u8()
    r.u16()
    r.u8()
    r.u8()
    if b >= 2:
        r.u16()
        r.u16()
        r.u16()
        r.u16()


def x_contract(r: Wire) -> None:
    """sub_14145F800 (CONTRACT): [u8 v57] + sub_1415F6ED0
    + [u8 v58!=0: sub_14172A440] + [u8 v59!=0: sub_14145E300]
    + [u32 n>0: n*([u8][u8])] + [u8 v60!=0: [u8][u32][u8]]
    + [u8 v61!=0: sub_14172A120] + sub_14146E9F0 + [u8]
    + (v57>=7 ? [4][2] : [4][1]) + [2][1][4][1][12]."""
    v57 = r.u8()
    x_1415f6ed0(r)
    if r.u8() != 0:
        x_14172a440(r)
    if r.u8() != 0:
        x_14145e300(r)
    n = r.u32()
    for _ in range(n):
        r.u8()
        r.u8()
    if r.u8() != 0:
        r.u8()
        r.u32()
        r.u8()
    if r.u8() != 0:
        x_14172a120(r)
    x_14146e9f0(r)
    r.u8()
    if v57 >= 7:
        r.u32()
        r.u16()
    else:
        r.u32()
        r.u8()
    r.take(2)
    r.u8()
    r.u32()
    r.u8()
    r.take(12)


# ----------------------------------------------------------------------------
# PLAYER conditional objects
# ----------------------------------------------------------------------------

def x_14144ad70(r: Wire) -> None:
    """sub_14144AD70 (PLAYER f3): fixed 55B — [1][1][4][4][4][1][4][2][2][1][2]
    + sub_140DB8980 [4] + sub_140DB8980 [4] + [1][1][1][4][2][4][4][4]."""
    r.take(55)


def x_140f938d0(r: Wire) -> None:
    """sub_140F938D0 (REF8 && !FC2C): [1][2][==0xFFFE ? [4]][2][==0xFFFF ? [4]][4][4]."""
    r.u8()
    if r.u16() == 0xFFFE:
        r.u32()
    if r.u16() == 0xFFFF:
        r.u32()
    r.u32()
    r.u32()


def x_14151d760(r: Wire) -> None:
    """sub_14151D760: [u32 n][n * <element>] — element grammar not yet wire-verified
    (n==0 observed in traces)."""
    n = r.u32()
    if n:
        raise BranchError("sub_14151D760", f"n={n} element grammar not mapped")


def x_14146de90(r: Wire) -> None:
    """sub_14146DE90 (0x14439F1F0): [1][4][4][4][1][1][1][4][1] = 21B."""
    r.u8()
    r.u32()
    r.u32()
    r.u32()
    r.u8()
    r.u8()
    r.u8()
    r.u32()
    r.u8()


def x_14146cfc0(r: Wire) -> None:
    """sub_14146CFC0 (0x14439E0E0): [1][4][4][4][4] = 17B."""
    r.u8()
    r.u32()
    r.u32()
    r.u32()
    r.u32()


def x_14141f7b0(r: Wire) -> None:
    """sub_14141F7B0 (0x14432AD70, with sub_140DB8980 [4] inside):
    [2][4][1][4][4][4][4] = 23B."""
    r.u16()
    r.u32()
    r.u8()
    r.u32()
    r.u32()
    r.u32()
    r.u32()


def x_14146d370(r: Wire) -> None:
    """sub_14146D370 (PLAYER f4): [u16 v81][1][u32 n][n*24B]
    + (v81<=25: [u8 m][m * sub_140F938D0]) + sub_14151D760
    + (v81<=25: sub_140F938D0) + [u8 k][k*[1]]
    + [4][2][1][4] + (v81>=28: [4]) + [4][4][4] + [1][1][1][1] + [4][4]
    + sub_14146DE90 + [u8!=0: sub_14146CFC0] + sub_14141F7B0."""
    v81 = r.u16()
    r.u8()
    n = r.u32()
    for _ in range(n):
        r.take(24)  # [2][1][4][1][4][4][4][4]
    if v81 <= 25:
        m = r.u8()
        for _ in range(m):
            x_140f938d0(r)
    x_14151d760(r)
    if v81 <= 25:
        x_140f938d0(r)
    k = r.u8()
    for _ in range(k):
        r.u8()
    r.u32()
    r.u16()
    r.u8()
    r.u32()
    if v81 >= 28:
        r.u32()
    r.u32()
    r.u32()
    r.u32()
    r.u8()
    r.u8()
    r.u8()
    r.u8()
    r.u32()
    r.u32()
    x_14146de90(r)
    if r.u8() != 0:
        x_14146cfc0(r)
    x_14141f7b0(r)


def x_14145c5a0(r: Wire) -> None:
    """sub_14145C5A0 (0x14438C670): [u32 n][n * ([1][2][1][11][4]) = 19B]."""
    n = r.u32()
    for _ in range(n):
        r.take(19)


def x_14145c700(r: Wire) -> None:
    """sub_14145C700: [u32 n][n * ([1][4]) = 5B]."""
    n = r.u32()
    for _ in range(n):
        r.take(5)


def x_14145ce40(r: Wire) -> None:
    """sub_14145CE40 (0x14438F150): [1][sub_14145C5A0][7 * sub_14145C700]."""
    r.u8()
    x_14145c5a0(r)
    for _ in range(7):
        x_14145c700(r)


def x_140e06080(r: Wire) -> None:
    """sub_140E06080 (=0x143BA6880): [1][sub_14145CE40][4]."""
    r.u8()
    x_14145ce40(r)
    r.u32()


def x_14146ad40(r: Wire) -> None:
    """sub_14146AD40 (PLAYER f2): dispatcher — case readers not yet mapped."""
    b = r.u8()
    raise BranchError("sub_14146AD40", f"case {b} reader not mapped")


def x_career_factory(r: Wire, t: int) -> None:
    """PLAYER n74 career loop — factory sub_1413C40A0(t) temp objects (cases 0-6)."""
    if t == 0:
        r.take(4)                       # 0x1442A4FA0 [2][1][1]
    elif t in (1, 2):
        r.take(6)                       # [2][2][1][1] / 0x1442A7730
    elif t == 3:
        r.take(9)                       # 0x1442A9550 [1][1][1][2][2][1][1]
    elif t in (4, 5):
        r.take(6)                       # 0x1442A8F60 [1][1][2][1][1]
    elif t == 6:
        n = r.u32()                     # 0x1413C4A40 [u32 n][n B][2][1][1]
        r.take(n)
        r.take(4)
    else:
        raise BranchError("sub_1413C40A0", f"career factory case {t}")


def x_14145d260(r: Wire) -> None:
    """sub_14145D260: [8][1][1][4] + sub_1414E57A0 + [2][1][1][1][2][1] = 44B.
    (PLAYER's queued 4@a1-312 flushes inside its prologue — wire order preserved.)"""
    r.take(8)
    r.u8()
    r.u8()
    r.u32()
    x_1414e57a0(r)
    r.u16()
    r.u8()
    r.u8()
    r.u8()
    r.u16()
    r.u8()


def x_1414e57a0(r: Wire) -> None:
    """sub_1414E57A0 (0x14447E060): [u32 n][n * sub_1414E5A30]."""
    n = r.u32()
    for _ in range(n):
        r.take(6)  # sub_1414E5A30 [1][2][1][1][1]


# ----------------------------------------------------------------------------
# Top-level slot19 readers
# ----------------------------------------------------------------------------

def x_player_body(r: Wire) -> None:
    """PLAYER body (sub_140E06EC0 minus a3-gated tail):
    [10][1][4][2][4][8][69][4][1][14 (VERSION>0xDF0)][4][4][1][2][2][4][4][1]
    [u32 n>0: n*u8][4] + CONTRACT + string + [12]
    + [u8 f1!=0: 30B] + [u8 f2!=0: sub_14146AD40] + [u8 f3!=0: sub_14144AD70]
    + [u8 f4!=0: sub_14146D370] + [u8 n74: n74*([u8 t]; t!=0xFF: factory obj)]
    + [u8!=0: sub_140E06080] + [4][4] + sub_14145D260 + [4]."""
    r.take(10)
    r.u8()
    r.u32()
    r.u16()
    r.u32()
    r.take(8)
    r.take(69)
    r.u32()
    r.u8()
    r.take(14)  # VERSION 0x0DF1 > 0xDF0
    r.u32()
    r.u32()
    r.u8()
    r.u16()
    r.u16()
    r.u32()
    r.u32()
    r.u8()
    n = r.u32()
    for _ in range(n):
        r.u8()
    r.u32()
    x_contract(r)
    r.string()
    r.take(12)
    if r.u8() != 0:
        r.take(30)
    if r.u8() != 0:
        x_14146ad40(r)
    if r.u8() != 0:
        x_14144ad70(r)
    if r.u8() != 0:
        x_14146d370(r)
    n74 = r.u8()
    for _ in range(n74):
        t = r.u8()
        if t != 0xFF:
            x_career_factory(r, t)
    if r.u8() != 0:
        x_140e06080(r)
    r.u32()
    r.u32()
    x_14145d260(r)
    r.u32()


def x_nonplayer_body(r: Wire) -> None:
    """NON_PLAYER body (sub_140DC1D30 minus a3-gated tail):
    [u16 n>0: n*([u8][u16])][15][u8 v118][v118<10 ? 51B : 52B][4][16][8]
    [6 (VERSION>0xDCB)][8] + flags:
    [u8 f1!=0: VERSION>=0xDC9 ? sub_1413F90A0 : sub_1413F97A0]
    [u8 f2!=0: sub_1413FE0E0] [u8 f3!=0: sub_1413FE6B0] [u8 f4!=0: sub_1413FECE0]
    [u8 f5!=0: sub_14141F7B0 (23B)] [VERSION>=0xDC1: u8 f6!=0: sub_1413FF240]
    [VERSION>=0xDD0: 7B]."""
    n = r.u16()
    for _ in range(n):
        r.u8()
        r.u16()
    r.take(15)
    v118 = r.u8()
    r.take(51 if v118 < 10 else 52)
    r.u32()
    r.take(16)
    r.take(8)
    r.take(6)   # VERSION > 0xDCB
    r.take(8)
    if r.u8() != 0:
        if VERSION >= 0xDC9:
            x_1413f90a0(r)
        else:
            x_1413f97a0(r)
    if r.u8() != 0:
        x_1413fe0e0(r)
    if r.u8() != 0:
        x_1413fe6b0(r)
    if r.u8() != 0:
        x_1413fece0(r)
    if r.u8() != 0:
        x_14141f7b0(r)
    if VERSION >= 0xDC1:
        if r.u8() != 0:
            x_1413ff240(r)
    if VERSION >= 0xDD0:
        r.take(7)


def x_1413f90a0(r: Wire) -> None:
    """sub_1413F90A0: [1][u16 n][n * sub_1413F94B0 (20B)]."""
    r.u8()
    n = r.u16()
    for _ in range(n):
        r.take(20)  # [1][1][1][4][4][4][4][1]


def x_1413f97a0(r: Wire) -> None:
    """sub_1413F97A0: [u16 n][n * sub_1413F94B0 (20B)]."""
    n = r.u16()
    for _ in range(n):
        r.take(20)


def x_1413fe0e0(r: Wire) -> None:
    """sub_1413FE0E0: [u8 n][n * vtable 0x1418B5BB8 slot3 object] — slot target not mapped."""
    n = r.u8()
    if n:
        raise BranchError("sub_1413FE0E0", f"n={n} vtable-slot object not mapped")


def x_1413fe6b0(r: Wire) -> None:
    """sub_1413FE6B0: [1][u16 n][n * ([1][1][1])]."""
    r.u8()
    n = r.u16()
    for _ in range(n):
        r.take(3)


def x_1413fece0(r: Wire) -> None:
    """sub_1413FECE0: [u8 n][n * ([1][1])]."""
    n = r.u8()
    for _ in range(n):
        r.take(2)


def x_1413ff240(r: Wire) -> None:
    """sub_1413FF240: [u32 n][n * ([u8 v38][v38<=1: 47*u8][v38>=3: 47*u8]
    [v38==2: state machine ~39 reads][4][4])] — v38==2 path not yet mapped."""
    n = r.u32()
    for _ in range(n):
        v38 = r.u8()
        if v38 == 2:
            raise BranchError("sub_1413FF240", "v38==2 state machine not mapped")
        r.take(47)
        r.take(4)
        r.take(4)


def x_official(r: Wire) -> None:
    """OFFICIAL (sub_1415856B0): [8][u16*3][u8*9][u8 v51: v51*24B]
    + sub_14096BA90 *2 ([u32 n][n*u32]) + [u32][u8] + sub_140DFB5C0 + PERSON base."""
    r.take(8)
    r.u16()
    r.u16()
    r.u16()
    r.take(9)
    v51 = r.u8()
    for _ in range(v51):
        r.take(24)  # (u8,u8,u8,u8,u32,u8,u8,u32,u8,u8,u32,u32)
    for _ in range(2):
        n = r.u32()
        for _ in range(n):
            r.u32()
    r.u32()
    r.u8()
    x_dfb5c0(r)
    x_person_base(r)


def decode_row(r: Wire, ptype: int, name_sink: list | None = None) -> None:
    """Dispatch one person row body by type. Each branch ends with the shared tail
    chain DD8520 -> DFB5C0 -> PERSON base (exactly once per row)."""
    if ptype == 1:
        x_nonplayer_body(r)
        x_dd8520(r)
        x_dfb5c0(r, name_sink)
        x_person_base(r)
    elif ptype == 2:
        x_player_body(r)
        x_dd8520(r)
        x_dfb5c0(r, name_sink)
        x_person_base(r)
    elif ptype == 3:
        x_player_body(r)
        x_nonplayer_body(r)
        x_dd8520(r)
        x_dfb5c0(r, name_sink)
        x_person_base(r)
    elif ptype == 4:
        x_official(r)
    elif ptype == 5:
        r.string()
        r.string()
        x_person_base(r)
    else:
        raise BranchError("dispatch", f"unknown person type {ptype}")


# ----------------------------------------------------------------------------
# Walk driver
# ----------------------------------------------------------------------------

class WalkStats:
    __slots__ = ("histo", "minlen", "maxlen", "ca_rows", "body_off", "ptype_of")

    def __init__(self):
        self.histo = {}
        self.minlen = {}
        self.maxlen = {}
        self.ca_rows = []       # (ca, row_idx) for ptype 2/3
        self.body_off = array("q")
        self.ptype_of = bytearray()


def decode_footer(r: "Wire") -> dict:
    """people_db payload footer: 28 bytes after the last row body.

    Loader-read part (C: sub_140F64530 case 3; also proven by emulating the real
    stage machine on the real payload bytes -- it consumes exactly 8 bytes after
    the last row, then the stage-4 cleanup runs with no further stream reads):
      [u32] case-3 table pass-1 count   (sub_141438DB0 elements, type id 14)
      [u32] case-3 table pass-2 count   (sub_141454370 elements, type id 44)
    Nonzero counts would mean element reads follow -> BranchError (no skipping).

    Writer-only commit trailer (the remaining 20 bytes). No loader path consumes
    them, proven four ways:
      (a) the stage machine returns true at stage 4 after exactly those 8 bytes;
      (b) the same "tad." family walker tail (sub_140F2FE70 -> sub_140FFAFD0:
          [u32 n] + n*12 UID-index entries, then [u8] flags + [u32] value) is
          empirically confirmed on basic_people_db.dat, whose final 9 bytes are
          [4]=0 [1]=01 [4]=last-uid -- the same shape as the t92 table_9 footer
          `00 00 00 00 01 ec 7a e4 04`;
      (c) in people_db that 9-byte shape fits only at footer offset 19
          (index_n=0, flags=01, value=0);
      (d) footer bytes 8..18 ([u32 0x100][7 zero bytes]) are commit-layer
          residue referenced by no reader (all people_db loader callers have
          zero stream reads after the stage machine).
    Consumed here with byte-exact assertions; any deviation raises BranchError.
    """
    c1 = r.u32()
    c2 = r.u32()
    if c1 or c2:
        raise BranchError(
            "footer",
            f"nonzero case-3 table counts ({c1},{c2}) - element reads would follow",
        )
    out: dict = {"case3_count1": c1, "case3_count2": c2}
    residue = r.read(11)
    if residue != b"\x00\x01" + b"\x00" * 9:
        raise BranchError("footer", f"commit trailer residue mismatch: {residue.hex()}")
    idx_n = r.u32()
    flags = r.u8()
    value = r.u32()
    if idx_n or flags != 1 or value:
        raise BranchError(
            "footer",
            f"family tail mismatch: index_n={idx_n} flags={flags} value={value}",
        )
    out["commit_residue_hex"] = residue.hex()
    out["family_tail"] = {"index_n": idx_n, "flags": flags, "value": value}
    return out


def walk(raw: bytes, row_limit: int | None, stats: WalkStats | None):
    """Decode rows [u32 ordinal][u8 ptype][body] from offset 6.

    Returns (rows_decoded, end_pos, count_from_header, row_end, footer) where
    row_end is the offset just past the last decoded row body.  When every row
    of the header count is decoded, the 28-byte payload footer is consumed as
    well and end_pos == len(raw) (exact EOF closure).
    """
    b = raw
    total = len(b)
    count = unpack_from("<I", b, 2)[0]
    limit = count if row_limit is None else min(row_limit, count)
    p = 6
    decoded = 0
    for i in range(limit):
        ordinal = unpack_from("<I", b, p)[0]
        pt = b[p + 4]
        body_start = p + 5
        r = Wire(b, body_start)
        try:
            decode_row(r, pt)
        except BranchError as exc:
            exc.row_idx = i                      # type: ignore[attr-defined]
            exc.off_abs = p                      # type: ignore[attr-defined]
            exc.body_rel = r.p - body_start      # type: ignore[attr-defined]
            exc.ptype = pt                       # type: ignore[attr-defined]
            exc.ordinal = ordinal                # type: ignore[attr-defined]
            raise
        except (IndexError, struct_error) as exc:
            err = BranchError("Wire", f"overread/desync: {exc}")
            err.row_idx = i                      # type: ignore[attr-defined]
            err.off_abs = p                      # type: ignore[attr-defined]
            err.body_rel = r.p - body_start      # type: ignore[attr-defined]
            err.ptype = pt                       # type: ignore[attr-defined]
            err.ordinal = ordinal                # type: ignore[attr-defined]
            raise err from exc
        end = r.p
        if stats is not None:
            stats.histo[pt] = stats.histo.get(pt, 0) + 1
            if pt not in stats.minlen or end - body_start < stats.minlen[pt]:
                stats.minlen[pt] = end - body_start
            if pt not in stats.maxlen or end - body_start > stats.maxlen[pt]:
                stats.maxlen[pt] = end - body_start
            stats.body_off.append(body_start)
            stats.ptype_of.append(pt)
            if pt in (2, 3) and end - body_start >= 10:
                stats.ca_rows.append((unpack_from("<H", b, body_start + 6)[0], i))
        p = end
        decoded += 1
    row_end = p
    footer = None
    if decoded == count:
        fr = Wire(b, p)
        footer = decode_footer(fr)
        p = fr.p
    return decoded, p, count, row_end, footer


def decompress_people_db() -> bytes:
    """people_db.dat = 8-byte envelope (03 01 'tad.' + u16 VERSION 0x0DF1) + zstd frame."""
    data = DATA_PATH.read_bytes()
    if data[8:12] != b"\x28\xb5\x2f\xfd":
        raise ValueError(f"unexpected people_db.dat envelope: {data[:8].hex()}")
    dctx = zstandard.ZstdDecompressor()
    with dctx.stream_reader(io.BytesIO(data[8:])) as rdr:
        raw = rdr.read()
    return raw


def load_oracle():
    if not ORACLE_PATH.exists():
        return None
    d = json.loads(ORACLE_PATH.read_text(encoding="utf-8"))
    return d


def check_oracle(my_rows, oracle_rows):
    """my_rows: list of (i, off, pt, len, ord). Returns list of mismatch dicts."""
    bad = []
    for i, (off, pt, blen, ordinal) in enumerate(my_rows):
        if i >= len(oracle_rows):
            break
        o = oracle_rows[i]
        if (o["off"], o["pt"], o["len"], o["ord"]) != (off, pt, blen, ordinal):
            bad.append({
                "i": i,
                "oracle": [o["off"], o["pt"], o["len"], o["ord"]],
                "mine": [off, pt, blen, ordinal],
            })
    return bad


# ----------------------------------------------------------------------------
# Selftest — synthetic rows built FROM the grammar, decoded back, must close exactly
# ----------------------------------------------------------------------------

def _s(b: bytes) -> bytes:
    return len(b).to_bytes(4, "little") + b


def _build_dd8520() -> bytes:
    o = bytearray()
    o += (0).to_bytes(2, "little")            # u16 count = 0
    o += b"\xa1" * 8                          # [8]
    o += b"\x00\x11\x22\x33"                  # u8*4
    o += b"\x44" * 8                          # [8]
    o += b"\x55"                              # u8
    o += (0).to_bytes(1, "little")            # v233 = 0
    o += (0x01234567).to_bytes(4, "little")   # [4]
    o += (1).to_bytes(1, "little")            # v239 = 1
    o += (5).to_bytes(1, "little")            # t=5 -> C07D00
    o += (0x89ABCDEF).to_bytes(4, "little")   # C07D00 [4]
    o += b"\x66" * 13                         # C07D00 [13] (REF8 && !FC2C)
    o += (7).to_bytes(2, "little")            # C07D00 [2]
    o += (0).to_bytes(1, "little")            # v239b = 0
    o += (1).to_bytes(1, "little")            # v234 = 1
    o += b"\x77" * 9                          # 9B block
    o += (2).to_bytes(4, "little")            # v231 = 2
    # element 1: [1][2][1][1 b!=1] + [8] = 13B
    o += b"\x01\x02\x03\x00\x00" + b"\xaa" * 8
    # element 2: [1][2][1][1 b==1] + [4] = 9B
    o += b"\x04\x05\x06\x00\x01" + b"\xbb" * 4
    o += (1).to_bytes(1, "little")            # v230 = 1 -> 15B
    o += b"\x88" * 15
    o += (1).to_bytes(2, "little")            # v228 = 1
    o += (0x55667788).to_bytes(4, "little")   # u32 element
    o += b"\x99" * 36                         # tail
    return bytes(o)


def _build_dfb5c0() -> bytes:
    o = bytearray()
    for _ in range(3):                        # dates, f=0
        o += (1234).to_bytes(4, "little")
        o += (0).to_bytes(1, "little")
    o += _s(b"DFB")                           # string
    o += b"\x00" * 4                          # [4]
    o += b"\x00" * 5                          # [5]
    o += b"\x00" * 16                         # [16]
    o += b"\x00" * 8                          # [8]
    o += (1).to_bytes(1, "little")            # v38 = 1 -> sub_141400230
    o += (1).to_bytes(1, "little")            # n1 = 1
    o += b"\xcc" * 16                         # 16B merged
    o += (1).to_bytes(4, "little", signed=True)   # n2 = 1
    o += b"\xdd" * 7                          # 7B
    o += b"\x00\x00\x00"                      # [1][1][1]
    o += (1).to_bytes(1, "little")            # n3 = 1
    # sub_1414009C0: [1][2][1][4] = 8B
    o += (1).to_bytes(1, "little") + (2).to_bytes(2, "little") + (3).to_bytes(1, "little") + (9).to_bytes(4, "little")
    o += (1).to_bytes(1, "little")            # VERSION>=0xDF0 byte
    o += (1).to_bytes(1, "little")            # v39 = 1 -> sub_141457830
    o += (1).to_bytes(1, "little")            # n = 1
    o += (9).to_bytes(1, "little")            # elem [u8]
    o += _s(b"ab")                            # elem string
    o += (3).to_bytes(4, "little")            # elem u32
    o += (0xBEAF).to_bytes(4, "little")       # [4]
    return bytes(o)


def _build_person_base() -> bytes:
    return b"\x11" * 8 + (1).to_bytes(4, "little") + (2).to_bytes(4, "little") + (3).to_bytes(4, "little")


def _build_nonplayer_body() -> bytes:
    o = bytearray()
    o += (0).to_bytes(2, "little")            # u16 count = 0
    o += b"\xa2" * 15                         # [15]
    o += (0).to_bytes(1, "little")            # v118 = 0 -> 51B
    o += b"\xb2" * 51
    o += (0x11223344).to_bytes(4, "little")   # [4]
    o += b"\xc2" * 16                         # [16]
    o += b"\xd2" * 8                          # [8]
    o += b"\xe2" * 6                          # [6] VERSION>0xDCB
    o += b"\xf2" * 8                          # [8]
    o += (1).to_bytes(1, "little")            # f1 = 1 -> sub_1413F90A0 (VERSION>=0xDC9)
    o += (1).to_bytes(1, "little")            # its [1]
    o += (1).to_bytes(2, "little")            # u16 n = 1
    o += b"\x01\x01\x01" + b"\x33" * 16 + b"\x02"   # 20B element
    o += (0).to_bytes(1, "little")            # f2 = 0
    o += (1).to_bytes(1, "little")            # f3 = 1 -> sub_1413FE6B0
    o += (1).to_bytes(1, "little")            # its [1]
    o += (2).to_bytes(2, "little")            # u16 n = 2
    o += b"\x00" * 6                          # 2 * 3B
    o += (0).to_bytes(1, "little")            # f4 = 0
    o += (1).to_bytes(1, "little")            # f5 = 1 -> sub_14141F7B0
    o += (1).to_bytes(2, "little") + (2).to_bytes(4, "little") + (3).to_bytes(1, "little")
    o += (4).to_bytes(4, "little") + (5).to_bytes(4, "little") + (6).to_bytes(4, "little") + (7).to_bytes(4, "little")
    o += (0).to_bytes(1, "little")            # f6 = 0 (VERSION>=0xDC1)
    o += b"\x05" * 7                          # [7] VERSION>=0xDD0
    return bytes(o)


def _build_player_body() -> bytes:
    o = bytearray()
    o += b"\x10" * 10                         # [10]
    o += (1).to_bytes(1, "little")            # [1]
    o += (0x11223344).to_bytes(4, "little")   # [4]
    o += (2).to_bytes(2, "little")            # [2]
    o += (3).to_bytes(4, "little")            # [4]
    o += b"\x20" * 8                          # [8]
    o += b"\x30" * 69                         # [69]
    o += (4).to_bytes(4, "little")            # [4]
    o += (5).to_bytes(1, "little")            # [1]
    o += b"\x40" * 14                         # [14] (VERSION>0xDF0)
    o += (6).to_bytes(4, "little")            # [4]
    o += (7).to_bytes(4, "little")            # [4]
    o += (8).to_bytes(1, "little")            # [1]
    o += (9).to_bytes(2, "little")            # [2]
    o += (10).to_bytes(2, "little")           # [2]
    o += (11).to_bytes(4, "little")           # [4]
    o += (12).to_bytes(4, "little")           # [4]
    o += (13).to_bytes(1, "little")           # [1]
    o += (1).to_bytes(4, "little")            # u32 n = 1
    o += (99).to_bytes(1, "little")           # u8 element
    o += (14).to_bytes(4, "little")           # [4]
    # CONTRACT (v57 = 7)
    o += (7).to_bytes(1, "little")            # v57 = 7
    o += (5).to_bytes(1, "little")            # 1415F6ED0 b=5 -> 10B
    o += b"\x50" * 10
    o += (1).to_bytes(1, "little")            # v58 = 1 -> sub_14172A440
    o += (0).to_bytes(1, "little")            # its [1]
    o += (1).to_bytes(1, "little")            # n = 1
    o += (1).to_bytes(1, "little")            # v46 = 1 (<2 -> +[4])
    o += (1).to_bytes(1, "little") + (2).to_bytes(2, "little") + (3).to_bytes(4, "little")
    o += (4).to_bytes(2, "little") + (5).to_bytes(4, "little") + (6).to_bytes(4, "little")
    o += (0).to_bytes(1, "little")            # v59 = 0
    o += (1).to_bytes(4, "little")            # n = 1 -> [u8][u8]
    o += (1).to_bytes(1, "little") + (2).to_bytes(1, "little")
    o += (1).to_bytes(1, "little")            # v60 = 1
    o += (1).to_bytes(1, "little") + (2).to_bytes(4, "little") + (3).to_bytes(1, "little")
    o += (1).to_bytes(1, "little")            # v61 = 1 -> sub_14172A120
    o += (1).to_bytes(1, "little")            # b=1 (<2 -> [1])
    o += b"\x60" * 3                          # [3]
    o += (1).to_bytes(4, "little")            # [4]
    o += (1).to_bytes(1, "little")            # [1]
    o += (3).to_bytes(1, "little")            # 14146E9F0 b=3 (>=2 -> 4*u16)
    o += (1).to_bytes(1, "little") + (2).to_bytes(2, "little") + (3).to_bytes(1, "little")
    o += (4).to_bytes(2, "little") + (5).to_bytes(1, "little") + (6).to_bytes(1, "little")
    o += (1).to_bytes(2, "little") + (2).to_bytes(2, "little") + (3).to_bytes(2, "little") + (4).to_bytes(2, "little")
    o += (0).to_bytes(1, "little")            # [u8] after 14146E9F0
    o += (1).to_bytes(4, "little")            # v57>=7 -> [4]
    o += (1).to_bytes(2, "little")            # [2]
    o += (1).to_bytes(2, "little")            # [2]
    o += (1).to_bytes(1, "little")            # [1]
    o += (1).to_bytes(4, "little")            # [4]
    o += (1).to_bytes(1, "little")            # [1]
    o += b"\x70" * 12                         # [12]
    o += _s(b"PL")                            # string
    o += b"\x80" * 12                         # [12]
    o += (1).to_bytes(1, "little")            # f1 = 1 -> 30B
    o += b"\x90" * 30
    o += (0).to_bytes(1, "little")            # f2 = 0
    o += (1).to_bytes(1, "little")            # f3 = 1 -> sub_14144AD70 (55B)
    o += b"\xa0" * 55
    o += (0).to_bytes(1, "little")            # f4 = 0
    o += (1).to_bytes(1, "little")            # n74 = 1
    o += (3).to_bytes(1, "little")            # t = 3 -> 9B factory obj
    o += b"\xb0" * 9
    o += (0).to_bytes(1, "little")            # fe = 0
    o += (1).to_bytes(4, "little")            # [4]
    o += (2).to_bytes(4, "little")            # [4]
    # sub_14145D260
    o += b"\xc0" * 8                          # [8]
    o += (1).to_bytes(1, "little")            # [1]
    o += (2).to_bytes(1, "little")            # [1]
    o += (3).to_bytes(4, "little")            # [4]
    o += (2).to_bytes(4, "little")            # 1414E57A0 n = 2
    o += b"\xd0" * 6 + b"\xd1" * 6            # 2 * 6B
    o += (1).to_bytes(2, "little")            # [2]
    o += (1).to_bytes(1, "little")            # [1]
    o += (2).to_bytes(1, "little")            # [1]
    o += (3).to_bytes(1, "little")            # [1]
    o += (4).to_bytes(2, "little")            # [2]
    o += (5).to_bytes(1, "little")            # [1]
    o += (15).to_bytes(4, "little")           # [4]
    return bytes(o)


def _build_official() -> bytes:
    o = bytearray()
    o += b"\xe0" * 8                          # [8]
    o += (1).to_bytes(2, "little") + (2).to_bytes(2, "little") + (3).to_bytes(2, "little")
    o += b"\xf0" * 9                          # u8*9
    o += (1).to_bytes(1, "little")            # v51 = 1
    o += b"\x0a" * 24                         # 24B element
    o += (1).to_bytes(4, "little")            # 14096BA90 n = 1
    o += (77).to_bytes(4, "little")           # u32 element
    o += (0).to_bytes(4, "little")            # 14096BA90 n = 0
    o += (8).to_bytes(4, "little")            # [u32]
    o += (9).to_bytes(1, "little")            # [u8]
    o += _build_dfb5c0()
    o += _build_person_base()
    return bytes(o)


def _build_type1_row() -> bytes:
    return _build_nonplayer_body() + _build_dd8520() + _build_dfb5c0() + _build_person_base()


def _build_type2_row() -> bytes:
    return _build_player_body() + _build_dd8520() + _build_dfb5c0() + _build_person_base()


def _build_type3_row() -> bytes:
    return _build_player_body() + _build_nonplayer_body() + _build_dd8520() + _build_dfb5c0() + _build_person_base()


def selftest() -> dict:
    """Build synthetic rows from the grammar, decode them, require exact closure."""
    cases = []
    # type 5
    body = _s(b"ret-one") + _s(b"ret-two-longer") + b"\x00" * 8 + b"\x22" * 12
    cases.append((5, body))
    cases.append((1, _build_type1_row()))
    cases.append((2, _build_type2_row()))
    cases.append((3, _build_type3_row()))
    cases.append((4, _build_official()))
    results = []
    ok = True
    for pt, body in cases:
        frame = (657483).to_bytes(4, "little") + bytes([pt]) + body
        r = Wire(frame, 5)
        decode_row(r, pt)
        consumed = r.p - 5
        exact = consumed == len(body)
        ok = ok and exact
        results.append({"ptype": pt, "body_len": len(body), "consumed": consumed, "exact": exact})
    # targeted reader checks
    r = Wire(b"\x04\x05\x06\x00\x01" + b"\xbb" * 4)
    x_14141e220(r)
    ok = ok and r.p == 9
    r = Wire(b"\x01\x02\x03\x00\x00" + b"\xaa" * 8)
    x_14141e220(r)
    ok = ok and r.p == 13
    return {"pass": ok, "cases": results}


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description="pure-Python people_db.dat decoder (t138)")
    ap.add_argument("--limit", type=int, default=0, help="decode only the first N rows")
    ap.add_argument("--verify-full", action="store_true", help="walk every row to EOF closure")
    ap.add_argument("--selftest", action="store_true", help="synthetic grammar round-trip")
    ap.add_argument("--out", default="people_pure_py_verify.json")
    args = ap.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    if args.selftest:
        res = selftest()
        print(json.dumps(res, indent=2))
        print("SELFTEST:", "PASS" if res["pass"] else "FAIL")
        (OUT_DIR / "people_pure_py_selftest.json").write_text(
            json.dumps(res, indent=2), encoding="utf-8")
        return 0 if res["pass"] else 1

    t0 = time.time()
    raw = decompress_people_db()
    t_dec = time.time() - t0
    print(f"decompressed {len(raw):,} bytes in {t_dec:.1f}s", flush=True)

    oracle = load_oracle()
    stats = WalkStats()
    limit = args.limit if args.limit > 0 else (None if args.verify_full else 3000)

    t1 = time.time()
    try:
        decoded, end_pos, count, row_end, footer = walk(raw, limit, stats)
    except BranchError as exc:
        info = {
            "error": "BranchError",
            "func": exc.func,
            "detail": exc.detail,
            "row_idx": getattr(exc, "row_idx", None),
            "off_abs": getattr(exc, "off_abs", None),
            "body_rel": getattr(exc, "body_rel", None),
            "ptype": getattr(exc, "ptype", None),
            "ordinal": getattr(exc, "ordinal", None),
        }
        ra = getattr(exc, "off_abs", None)
        if ra is not None:
            lo = max(0, ra - 16)
            info["hex_ctx_16_before"] = raw[lo:ra].hex()
            info["hex_ctx_at"] = raw[ra:ra + 32].hex()
        print("WALK FAILED:", json.dumps(info, indent=2), flush=True)
        (OUT_DIR / "people_pure_py_error.json").write_text(
            json.dumps(info, indent=2), encoding="utf-8")
        return 2
    t_walk = time.time() - t1

    diff = len(raw) - end_pos
    result = {
        "rows_decoded": decoded,
        "count_from_header": count,
        "total_bytes": len(raw),
        "end_offset": end_pos,
        "row_end_offset": row_end,
        "diff": diff,
        "footer": footer,
        "footer_closed": end_pos == len(raw),
        "decompress_sec": round(t_dec, 2),
        "walk_sec": round(t_walk, 2),
        "elapsed_sec": round(time.time() - t0, 2),
    }

    if oracle is not None:
        # rebuild per-row tuples for the oracle window
        orows = oracle["rows"]
        n_check = min(decoded, len(orows))
        # walk again cheaply? no — we did not store per-row lens in limit mode.
        # Re-derive from stats when available, else re-walk.
        if stats is not None:
            tuples = []
            for i in range(n_check):
                bo = stats.body_off[i]
                pt = stats.ptype_of[i]
                if i + 1 < decoded:
                    blen = stats.body_off[i + 1] - bo - 5
                else:
                    blen = row_end - bo
                tuples.append((bo - 5, pt, blen, unpack_from("<I", raw, bo - 5)[0]))
            bad = check_oracle(tuples, orows)
        else:
            bad = [{"error": "no stats in limit mode; rerun with --verify-full or implement stats"}]
        result["oracle_rows_checked"] = n_check
        result["oracle_mismatches"] = len(bad)
        result["oracle_end_expected"] = oracle.get("end")
        # only comparable in limit mode (full mode consumes the 28-byte footer,
        # so end_pos is the payload EOF, not the oracle's mid-file end)
        result["oracle_end_match"] = (
            (end_pos == oracle.get("end")) if (n_check >= len(orows) and footer is None) else None
        )
        if bad:
            result["first_mismatches"] = bad[:10]
        print(f"oracle: checked {n_check} rows, mismatches={len(bad)}", flush=True)

    if stats is not None:
        result["histogram"] = {str(k): v for k, v in sorted(stats.histo.items())}
        result["body_len_min"] = {str(k): v for k, v in sorted(stats.minlen.items())}
        result["body_len_max"] = {str(k): v for k, v in sorted(stats.maxlen.items())}
        top = nlargest(20, stats.ca_rows)
        pools = load_name_pools()
        top_out = []
        for ca, idx in top:
            bo = stats.body_off[idx]
            # body ends 5 bytes before the next row header (or at row_end for
            # the final row)
            nxt = stats.body_off[idx + 1] - 5 if idx + 1 < decoded else row_end
            body = raw[bo:nxt]
            ident = unpack_from("<III", body, len(body) - 12)
            # re-decode the exact body (walk is byte-exact per row, so a
            # standalone decode of [bo:nxt] consumes precisely the body)
            pt = stats.ptype_of[idx]
            sink: list = []
            rr = Wire(raw, bo)
            decode_row(rr, pt, name_sink=sink)
            if rr.p != nxt:
                raise BranchError("top20", f"row {idx}: re-decode ended at {rr.p}, body end {nxt}")
            top_out.append({
                "row_idx": idx,
                "ptype": pt,
                "ca": ca,
                "name": resolve_person_name(sink, pools),
                "name_ids": [e["id"] for e in sink],
                "ordinal": ident[0],
                "dbid": ident[1],
                "uid": ident[2],
                "pdxx_hex": body[44:98].hex(),
            })
        result["top20_by_ca"] = top_out

    out_path = OUT_DIR / args.out
    out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "top20_by_ca"}, indent=2), flush=True)
    if stats is not None:
        print("top CA:", [(t["ca"], t["uid"]) for t in result.get("top20_by_ca", [])[:5]], flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
