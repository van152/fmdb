#!/usr/bin/env python3
"""t82 — table_extra_3.dat remaining member naming, dual-chain static proofs,
CBW*/CBD* -> STARTING_RECORD (table_45.dat) negative proof, and full-archive
vectorized domain validation across all 84,259 x 2 rows.

Write boundary: emits JSON artifacts only under --outdir (default scratch/t82/out).
Read-only inputs: editor.exe, evidence/fm24/*, scratch/t57/t63/t71, scratch/data/*.
L4 = 0 (never launches game/editor/IDA, never touches Z:, no network).
Exit codes: 0 = pass, 1 = verification/check failed, 2 = CLI usage or fatal error.
"""
from __future__ import annotations
import sys as _cfg_sys
from pathlib import Path as _cfg_pathlib
_cfg_sys.path.insert(0, str(_cfg_pathlib(__file__).resolve().parent))
import fm24_config as _cfg

import argparse
import hashlib
import json
import os
import struct
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import numpy as np

TOOLS_PY = str(_cfg.VENDOR_DIR)
if TOOLS_PY not in sys.path:
    sys.path.insert(0, TOOLS_PY)

import capstone  # type: ignore
import pefile  # type: ignore
import zstandard as zstd  # type: ignore

ROOT = Path(str(_cfg.ROOT))
DEFAULT_EXE = Path(str(_cfg.EDITOR_EXE))
DEFAULT_DATA = Path(os.environ.get("FM24_DB_DIR", str(ROOT / "scratch/data")))
DEFAULT_OUT = ROOT / "scratch/t82/out"

TAD_HEAD = bytes.fromhex("03017461642ef10d")
SENTINEL_DATE4 = 0x076C0001  # 1900-01-01 default sentinel

PINNED_SHA256 = {
    "editor.exe": "b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4",
    "evidence/fm24/reports/editor_schema/master.json": "7d57477e144d5359ccde64bb24b3ba7c640ef41738ed196eba8a38e792776eda",
    "evidence/fm24/reports/dbdat_decode/db_tables_big.json": "c57b2b6837a3dcca106bf4363da105eca7665df407b738483839d1b7b6de3ddf",
    "scratch/t57/out/field_map.json": "0b04de7b15c455ccb85212d43221d5cbecb8fd5ccbf830ba71d5f4f3011f3664",
    "scratch/t63/out/field_map_r2.json": "5bdf1fc6e35c6c0cabe666a0e173228f6127a770392b73ca8d23b0a35c24dd46",
    "scratch/t71/out/chain.json": "c001f0d22db79b144760d614c69f21c3812a66de714e3ebeee0f3e35acd09534",
    "scratch/t71/out/field_map_r3.json": "5e5a869acbb4a545ff1f27ef346952547b3d92ce052db6a51ce7390b552dfe75",
    "scratch/t71/out/rows_extra3.json": "df809f45cdd7329f005144d3a90ec316c4ee1ebd7f16e751f9d082d68914ca38",
    "client_db.dat": "5ce7cd91da1031436a55ad47dac04bac446cb0cad807e9c9b24f4885d9b5ecc1",
    "server_db.dat": "99eed00bd26582648c0d3ff51b5c8e37a35b68c296a074e8fb476d1b3ca4a662",
}

T71_L3_INDICES = {
    26, 48, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164,
    165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176,
}


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def check_date4_scalar(u: int) -> tuple[bool, bool]:
    """Validate packed 4-byte FM date (u16 doy_bits, u16 year)."""
    yr = (u >> 16) & 0xFFFF
    doy = u & 0x1FF
    mid = (u >> 9) & 0x7F
    leap = 1 if (yr % 4 == 0 and (yr % 100 != 0 or yr % 400 == 0)) else 0
    valid = (yr >= 1) and (1 <= doy <= 365 + leap) and (mid == 0)
    return valid, (u == SENTINEL_DATE4)


def check_date4_vec(arr: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    yr = (arr >> 16) & 0xFFFF
    doy = arr & 0x1FF
    mid = (arr >> 9) & 0x7F
    leap = ((yr % 4 == 0) & ((yr % 100 != 0) | (yr % 400 == 0))).astype(np.uint32)
    valid = (yr >= 1) & (doy >= 1) & (doy <= 365 + leap) & (mid == 0)
    sent = arr == SENTINEL_DATE4
    return valid, sent


def replay_uefa_ring(vals: list[int]) -> tuple[list[int], int]:
    """Exact mirror of 0x39aa1f0 ring-buffer push (capacity 10)."""
    ring = [0] * 10
    head = 0
    cnt = 0
    for v in vals:
        if cnt < 10:
            ring[(head + cnt) % 10] = v
            cnt += 1
        else:
            ring[head] = v
            head = (head + 1) % 10
    ordered = [ring[(head + k) % 10] if k < cnt else 0 for k in range(10)]
    return ordered, head


def open_fmf(path: Path) -> tuple[dict[str, tuple[int, int, int]], bytes]:
    raw = path.read_bytes()
    toc, base = (x + 17 for x in struct.unpack_from("<QQ", raw, 17))
    if base != 34 or raw[8:17] != b"\x02\x01fmf.\x08\x00\x00" or raw[toc:toc + 9] != b"\x02\x01fmf.\x08\x00\x00":
        raise RuntimeError(f"Invalid FMF header/TOC magic in {path}")

    def _frame(buf: bytes) -> tuple[bytes, int]:
        d = zstd.ZstdDecompressor().decompressobj()
        v = d.decompress(buf)
        return v, len(buf) - len(d.unused_data)

    directory, used = _frame(raw[toc + 9:])
    if toc + 9 + used != len(raw):
        raise RuntimeError(f"FMF TOC trailing bytes in {path}")
    pos = 0
    entries: dict[str, tuple[int, int, int]] = {}

    def pull(n: int) -> bytes:
        nonlocal pos
        r = directory[pos:pos + n]
        pos += n
        return r

    def num() -> int:
        return struct.unpack("<I", pull(4))[0]

    def text() -> str:
        return pull(num()).decode("utf-8")

    def node(parent: str) -> None:
        prefix = parent + text() + "/"
        for _ in range(num()):
            name = prefix + text() + text()
            off, size, unpacked, _, _ = struct.unpack("<5Q", pull(40))
            entries[name] = (base + off, base + off + size, unpacked)
        for _ in range(num()):
            node(prefix)

    node("")
    return entries, raw


def extract_fmf_member(raw: bytes, entries: dict[str, tuple[int, int, int]], rel: str) -> bytes:
    lo, hi, unpacked = entries[rel]
    q = lo
    out = None
    while q < hi:
        d = zstd.ZstdDecompressor().decompressobj()
        pl = d.decompress(raw[q:hi])
        w = (hi - q) - len(d.unused_data)
        q += w
        if len(pl) == unpacked:
            out = pl
    if out is None or out[:8] != TAD_HEAD:
        raise RuntimeError(f"Failed to extract valid tad. member {rel}")
    return out


def extract_seq_uids(buf: bytes) -> tuple[dict[int, int], set[int]]:
    """Extract sequential (ordinal, uid, uid) triples from a tad. table stream."""
    cnt = struct.unpack_from("<I", buf, 8)[0]
    ord_to_uid: dict[int, int] = {}
    uid_set: set[int] = set()
    pos = 12
    for k in range(cnt):
        needle = struct.pack("<I", k)
        found = False
        s = pos
        lim = min(len(buf), pos + 450)
        while True:
            idx = buf.find(needle, s, lim)
            if idx == -1:
                break
            if idx + 12 <= len(buf):
                u1, u2 = struct.unpack_from("<II", buf, idx + 4)
                if u1 == u2 and 1 <= u1 <= 2_100_000_000:
                    ord_to_uid[k] = u1
                    uid_set.add(u1)
                    pos = idx + 12
                    found = True
                    break
            s = idx + 1
        if not found:
            raise RuntimeError(f"UID sequential scan stopped at ordinal {k} (pos={pos})")
    return ord_to_uid, uid_set


def verify_manifest_and_inputs(exe_path: Path, data_dir: Path) -> dict[str, str]:
    manifest = json.loads((ROOT / "evidence/MANIFEST.json").read_bytes())
    man_map = {e["path"]: e["sha256"] for e in manifest["files"]}
    checked: dict[str, str] = {}
    for rel, expected in PINNED_SHA256.items():
        if rel == "editor.exe":
            p = exe_path
        elif rel in ("client_db.dat", "server_db.dat"):
            p = data_dir / rel
        else:
            p = ROOT / rel
        if not p.exists():
            raise RuntimeError(f"Missing required input: {p}")
        actual = sha256_file(p)
        if actual != expected:
            raise RuntimeError(f"SHA-256 mismatch for {rel}: got {actual}, expected {expected}")
        if rel in man_map and man_map[rel] != actual:
            raise RuntimeError(f"MANIFEST.json mismatch for {rel}")
        checked[rel] = actual
    return checked


class PEInspector:
    def __init__(self, exe_path: Path):
        self.raw = exe_path.read_bytes()
        self.pe = pefile.PE(data=self.raw, fast_load=True)
        self.ib = self.pe.OPTIONAL_HEADER.ImageBase
        self.md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

    def va(self, fo: int) -> int:
        return self.ib + self.pe.get_rva_from_offset(fo)

    def fo_from_va(self, v: int) -> int:
        return self.pe.get_offset_from_rva(v - self.ib)

    def insn_at(self, fo: int, count: int = 1) -> dict[str, Any]:
        sva = self.va(fo)
        insns = list(self.md.disasm(self.raw[fo:fo + 16 * count], sva))[:count]
        if len(insns) < count:
            raise RuntimeError(f"Disassembly failed at fo=0x{fo:x}")
        tot_len = sum(i.size for i in insns)
        return {
            "file_offset": f"0x{fo:x}",
            "va": f"0x{sva:x}",
            "bytes": self.raw[fo:fo + tot_len].hex(),
            "disasm": "; ".join(f"{i.mnemonic} {i.op_str}".strip() for i in insns),
        }

    def bytes_at(self, fo: int, size: int) -> dict[str, Any]:
        return {
            "file_offset": f"0x{fo:x}",
            "va": f"0x{self.va(fo):x}",
            "bytes": self.raw[fo:fo + size].hex(),
        }

    def rel32_table(self, base_fo: int, count: int) -> list[dict[str, Any]]:
        out = []
        for idx in range(count):
            cfo = base_fo + 4 * idx
            rel = struct.unpack_from("<i", self.raw, cfo)[0]
            tgt = base_fo + rel
            out.append({
                "index": idx,
                "cell_fo": f"0x{cfo:x}",
                "cell_va": f"0x{self.va(cfo):x}",
                "bytes": self.raw[cfo:cfo + 4].hex(),
                "rel32": rel,
                "target_fo": f"0x{tgt:x}",
                "target_va": f"0x{self.va(tgt):x}",
            })
        return out

    def vtable_slots(self, vt_fo: int, n_slots: int = 8) -> dict[str, Any]:
        slots = {}
        for k in range(n_slots):
            off = 8 * k
            ptr = struct.unpack_from("<Q", self.raw, vt_fo + off)[0]
            tfo = self.fo_from_va(ptr)
            slots[f"+0x{off:02x}"] = {"target_fo": f"0x{tfo:x}", "target_va": f"0x{ptr:x}"}
        # COL pointer sits at vt_fo - 8
        col_ptr = struct.unpack_from("<Q", self.raw, vt_fo - 8)[0]
        col_fo = self.fo_from_va(col_ptr)
        td_rva = struct.unpack_from("<I", self.raw, col_fo + 12)[0]
        td_fo = self.pe.get_offset_from_rva(td_rva)
        rtti_end = self.raw.find(b"\x00", td_fo + 16)
        rtti = self.raw[td_fo + 16:rtti_end].decode("ascii", errors="replace")
        return {
            "vtable_fo": f"0x{vt_fo:x}",
            "vtable_va": f"0x{self.va(vt_fo):x}",
            "col_fo": f"0x{col_fo:x}",
            "col_va": f"0x{col_ptr:x}",
            "rtti": rtti,
            "rtti_fo": f"0x{td_fo + 16:x}",
            "slots": slots,
        }


def replay_table_extra_3(buf: bytes, server: bool) -> dict[str, Any]:
    """Byte-exact sequential replay of client_db or server_db table_extra_3.dat."""
    if buf[:8] != TAD_HEAD:
        raise RuntimeError("Bad tad. magic")
    n = struct.unpack_from("<I", buf, 8)[0]
    if n != 84259:
        raise RuntimeError(f"Unexpected row count {n}, expected 84259")

    # Common tail arrays (present on both client and server)
    res: dict[str, Any] = {
        "rows": n,
        "bytes": len(buf),
        "stream_sha256": sha256_bytes(buf),
        "d8": np.empty(n, dtype="<u2"),
        "cc": np.empty(n, dtype="<u4"),
        "base_ac": np.empty(n, dtype="<u2"),
        "base_a0": np.empty(n, dtype="<u4"),
        "base_a8": np.empty(n, dtype="<u4"),
        "tcht_len": np.empty(n, dtype="<u4"),
        "tcht_map": {},
        "tcht_bad_utf8": 0,
        "kit_cnt": np.empty(n, dtype=np.uint8),
        "kit_total": 0,
        "kit_tag_counter": Counter(),
        "kit_buckets": Counter(),
        "kit_bucket_rows": defaultdict(set),
        "kit_years": Counter(),
        "kit_comp_vals": [],
        "common_tail_hash": hashlib.sha256(),
    }

    if server:
        for k, dt in [
            ("Ctlv", "i1"), ("Cmle", "i1"), ("e122", "i1"), ("e18_cnt", "<u2"),
            ("eda_tag", "u1"), ("eda_b1", "u1"), ("eda_b2", "u1"), ("eda_b3", "u1"), ("eda_b4", "u1"),
            ("e123", "i1"), ("Csth", "<i4"), ("edates_flag", "u1"),
            ("ede", "<u2"), ("eb8", "<u4"), ("e125", "i1"), ("e84", "<u4"), ("e80", "<u4"),
            ("elec_flag", "u1"), ("elec_club", "<i4"), ("elec_d1", "<u4"), ("elec_d2", "<u4"),
            ("Cepr", "<i2"), ("Cetl", "i1"), ("Cmtm", "i1"), ("Cect", "i1"), ("Cemn", "i1"), ("Cemx", "i1"),
            ("Cyim", "i1"), ("CScP", "i1"), ("e128", "i1"), ("Cown", "i1"), ("Chti", "i1"),
            ("f8_ver", "u1"), ("f8_CsSF", "<i4"), ("f8_CsSS", "<i2"), ("f8_CsST", "<i2"),
            ("Csly", "i1"), ("Csps", "i1"), ("Cspt", "i1"), ("Csaf", "i1"), ("Cste", "i1"), ("Cspe", "i1"),
            ("p10c_ver", "u1"),
            ("ebc", "<u4"), ("ec4", "<i4"), ("ec8", "<i4"),
            ("Cyfb", "i1"), ("Cytv", "i1"), ("Crcb", "i1"), ("e12e", "i1"), ("e12f", "i1"),
            ("ed0", "<i4"), ("ed4", "<i4"),
            ("e28_cnt", "i1"), ("e20_cnt", "u1"), ("e48_flag", "u1"), ("e48_cnt", "u1"), ("e48_head", "u1"),
            ("e68_cnt", "<u2"), ("edc", "<u2"),
            ("b18_cnt", "<i2"), ("b30_cnt", "i1"),
            ("Cpfr", "i1"), ("C2pf", "i1"), ("Cdfo", "i1"), ("Cafo", "i1"),
            ("Catd", "<i4"), ("Cmna", "<i4"), ("Cmxa", "<i4"),
            ("b0_cnt", "<u2"), ("b48_flag", "u1"), ("b48_cnt", "<u4"),
        ]:
            res[k] = np.full(n, -1 if dt.endswith(("i1", "i2", "i4")) else 0, dtype=dt)
        res["e88_dates"] = np.empty((n, 6), dtype="<u4")
        res["ea0_dates"] = np.empty((n, 6), dtype="<u4")
        res["f8_tail6"] = np.empty((n, 6), dtype="i1")
        res["p10c_raw"] = np.empty((n, 20), dtype="u1")
        res["cuf_raw"] = np.zeros((n, 10), dtype="<i4")
        res["cuf_f32"] = np.zeros((n, 10), dtype=np.float32)
        res["cuf_has"] = np.zeros(n, dtype=bool)
        res["e48_tags"] = Counter()
        res["cscm_items"] = []
        res["cpsl_items"] = []
        res["cspb_items"] = []
        res["cren_items"] = []
        res["tcrs_items"] = []
        res["tcrs_ver"] = Counter()
        res["tcrs_item_ver"] = Counter()
        res["b0_tags"] = Counter()
        res["b0_tag_rows"] = Counter()
        res["csoc_items"] = []
        res["camc_items"] = []
        res["cbbl_items"] = []
        res["pcpt_items"] = []
        res["vtag4_cnt"] = 0
        res["vtag9_cnt"] = 0
        res["vtag16_cnt"] = 0
        res["vtag37_cnt"] = 0

    p = 12
    ct_hash = res["common_tail_hash"]
    for i in range(n):
        ord_val = struct.unpack_from("<I", buf, p)[0]
        if ord_val != i:
            raise RuntimeError(f"Ordinal mismatch at row {i}: got {ord_val} at pos {p}")
        p += 4

        if server:
            res["Ctlv"][i], res["Cmle"][i], res["e122"][i] = struct.unpack_from("<bbb", buf, p)
            p += 3
            c18 = struct.unpack_from("<H", buf, p)[0]
            res["e18_cnt"][i] = c18
            p += 2 + 4 * c18
            res["eda_tag"][i], res["eda_b1"][i], res["eda_b2"][i], res["eda_b3"][i], res["eda_b4"][i] = struct.unpack_from("<5B", buf, p)
            p += 5
            res["e123"][i], res["Csth"][i] = struct.unpack_from("<bi", buf, p)
            p += 5
            res["e88_dates"][i] = struct.unpack_from("<6I", buf, p)
            p += 24
            ef = buf[p]
            res["edates_flag"][i] = ef
            p += 1
            if ef:
                res["ea0_dates"][i] = struct.unpack_from("<6I", buf, p)
                p += 24
            else:
                res["ea0_dates"][i] = SENTINEL_DATE4
            res["ede"][i], res["eb8"][i], res["e125"][i], res["e84"][i], res["e80"][i] = struct.unpack_from("<HIbII", buf, p)
            p += 15
            elf = buf[p]
            res["elec_flag"][i] = elf
            p += 1
            if elf:
                ec, ed1, ed2, cepr, cetl, cmtm, cect, cemn, cemx = struct.unpack_from("<iIIhbbbbb", buf, p)
                p += 19
                res["elec_club"][i] = ec
                res["elec_d1"][i] = ed1
                res["elec_d2"][i] = ed2
                res["Cepr"][i] = cepr
                res["Cetl"][i] = cetl
                res["Cmtm"][i] = cmtm
                res["Cect"][i] = cect
                res["Cemn"][i] = cemn
                res["Cemx"][i] = cemx
            res["Cyim"][i], res["CScP"][i], res["e128"][i], res["Cown"][i], res["Chti"][i] = struct.unpack_from("<5b", buf, p)
            p += 5
            # +0xf8 supporter profile 1 (1B ver=3 + 20B)
            f8v = buf[p]
            res["f8_ver"][i] = f8v
            if f8v != 3:
                raise RuntimeError(f"Unexpected +0xf8 version {f8v} at row {i}")
            p += 1
            vals = struct.unpack_from("<ihh12b", buf, p)
            p += 20
            res["f8_CsSF"][i], res["f8_CsSS"][i], res["f8_CsST"][i] = vals[0], vals[1], vals[2]
            res["Csly"][i], res["Csps"][i], res["Cspt"][i], res["Csaf"][i], res["Cste"][i], res["Cspe"][i] = vals[3:9]
            res["f8_tail6"][i] = vals[9:15]
            # +0x10c supporter profile 2 (1B ver=3 + 20B)
            p10v = buf[p]
            res["p10c_ver"][i] = p10v
            if p10v != 3:
                raise RuntimeError(f"Unexpected +0x10c version {p10v} at row {i}")
            p += 1
            res["p10c_raw"][i] = np.frombuffer(buf, dtype=np.uint8, count=20, offset=p)
            p += 20
            # cnst blocks A (+0xe0) & B (+0xe7) — already promoted in t71, skip structurally
            ta = buf[p]
            p += 1 + (7 if ta > 1 else 6)
            tb = buf[p]
            p += 1 + (12 if tb < 2 else 14 if tb == 2 else 15)
            # +bc, +c4, +c8, +12b..+12f, +d0, +d4 (25B)
            (res["ebc"][i], res["ec4"][i], res["ec8"][i],
             res["Cyfb"][i], res["Cytv"][i], res["Crcb"][i], res["e12e"][i], res["e12f"][i],
             res["ed0"][i], res["ed4"][i]) = struct.unpack_from("<Iiibbbbbii", buf, p)
            p += 25
            # +0x28 (Cscm): i8 cnt x 22B
            c28 = struct.unpack_from("<b", buf, p)[0]
            res["e28_cnt"][i] = c28
            p += 1
            for _ in range(c28):
                ver, co1, co2, stnm, sn1, sn2, tl = struct.unpack_from("<Biibiii", buf, p)
                res["cscm_items"].append((i, ver, co1, co2, stnm, sn1, sn2, tl))
                p += 22
            # +0x20 (INT_DUTY_PLAYER_COUNT): u8 cnt x 10B
            c20 = buf[p]
            res["e20_cnt"][i] = c20
            p += 1 + 10 * c20
            # +0x48 (UEFA coeff ring buffer)
            f48 = buf[p]
            res["e48_flag"][i] = f48
            p += 1
            if f48:
                t48 = struct.unpack_from("<b", buf, p)[0]
                res["e48_tags"][t48] += 1
                p += 1 + (24 if t48 > 0 else 16)
                cnt48 = buf[p]
                res["e48_cnt"][i] = cnt48
                p += 1
                vals48 = list(struct.unpack_from(f"<{cnt48}i", buf, p)) if cnt48 else []
                p += 4 * cnt48
                ordered, head = replay_uefa_ring(vals48)
                res["e48_head"][i] = head
                res["cuf_has"][i] = True
                for s_idx in range(10):
                    res["cuf_raw"][i, s_idx] = ordered[s_idx]
                    res["cuf_f32"][i, s_idx] = np.float32(ordered[s_idx] / 1000.0)
            # +0x30(1B), +0x38(1B), +0x70(1B), +0x50(4B u32) — all 0 in current archive
            if buf[p:p + 7] != b"\x00" * 7:
                raise RuntimeError(f"Non-zero +30/+38/+70/+50 bytes at row {i}: {buf[p:p+7].hex()}")
            p += 7
            # +0x68 (CPsL): u16 cnt x (1B tag + 10B)
            c68 = struct.unpack_from("<H", buf, p)[0]
            res["e68_cnt"][i] = c68
            p += 2
            for _ in range(c68):
                tg, p1, p2, w8 = struct.unpack_from("<BiiH", buf, p)
                res["cpsl_items"].append((i, tg, p1, p2, w8))
                p += 11
            # +0x40 (1B flag == 0) + +0xdc (2B u16)
            if buf[p] != 0:
                raise RuntimeError(f"Non-zero +0x40 flag at row {i}: {buf[p]}")
            p += 1
            res["edc"][i] = struct.unpack_from("<H", buf, p)[0]
            p += 2

        # Common tail (BOTH client and server) — hash exact wire bytes for cross-archive equality proof!
        ct_start = p
        res["d8"][i], res["cc"][i], res["base_ac"][i] = struct.unpack_from("<HIH", buf, p)
        p += 8
        tlen = struct.unpack_from("<I", buf, p)[0]
        res["tcht_len"][i] = tlen
        p += 4
        if tlen:
            sb = buf[p:p + tlen]
            p += tlen
            try:
                res["tcht_map"][i] = sb.decode("utf-8")
            except UnicodeDecodeError:
                res["tcht_bad_utf8"] += 1
        kcnt = buf[p]
        res["kit_cnt"][i] = kcnt
        p += 1
        for _ in range(kcnt):
            ot = buf[p]
            res["kit_tag_counter"][ot] += 1
            if ot != 1:
                raise RuntimeError(f"Unexpected kit tag {ot} at row {i}")
            c18k, c1ck, kyr, b22, b23, b24, b25 = struct.unpack_from("<iiHBBBB", buf, p + 13)
            p += 27
            res["kit_total"] += 1
            bucket = (b22, 1 if b25 else 0)
            res["kit_buckets"][bucket] += 1
            res["kit_bucket_rows"][bucket].add(i)
            res["kit_years"][kyr] += 1
            if c18k > 0:
                res["kit_comp_vals"].append((i, c18k, c1ck))
        # base+0xa0 (ttcl) & base+0xa8 (tbcl): 4B reversed RGBA each
        a3, a2, a1, a0, b3, b2, b1, b0 = buf[p:p + 8]
        p += 8
        res["base_a0"][i] = a0 | (a1 << 8) | (a2 << 16) | (a3 << 24)
        res["base_a8"][i] = b0 | (b1 << 8) | (b2 << 16) | (b3 << 24)
        ct_hash.update(buf[ct_start:p])

        if server:
            # base+0x18 (Cspb): i16 cnt x 20B
            c18b = struct.unpack_from("<h", buf, p)[0]
            res["b18_cnt"][i] = c18b
            p += 2
            for _ in range(c18b):
                ver, cm1, cm2, venu, matc, btype, stdt, endt = struct.unpack_from("<BiibbbII", buf, p)
                res["cspb_items"].append((i, ver, cm1, cm2, venu, matc, btype, stdt, endt))
                p += 20
            # base+0x30 (Cren): i8 cnt x 6B
            c30b = struct.unpack_from("<b", buf, p)[0]
            res["b30_cnt"][i] = c30b
            p += 1
            for _ in range(c30b):
                rsnn, rsnp, rsnr = struct.unpack_from("<bib", buf, p)
                res["cren_items"].append((i, rsnn, rsnp, rsnr))
                p += 6
            # base+0x74..+0x77 (4B) + base+0x68..+0x70 (12B)
            (res["Cpfr"][i], res["C2pf"][i], res["Cdfo"][i], res["Cafo"][i],
             res["Catd"][i], res["Cmna"][i], res["Cmxa"][i]) = struct.unpack_from("<bbbbiii", buf, p)
            p += 16
            # base+0x00 polymorphic virtual dispatch
            cb0 = struct.unpack_from("<H", buf, p)[0]
            res["b0_cnt"][i] = cb0
            p += 2
            seen_tags = set()
            for _ in range(cb0):
                t = buf[p]
                p += 1
                res["b0_tags"][t] += 1
                seen_tags.add(t)
                if t == 4:
                    res["vtag4_cnt"] += 1
                    p += 43
                elif t == 5:
                    p1, p2, club_ord, perc, b20, d18, d1c, b22, b23 = struct.unpack_from("<iiibbiiBB", buf, p)
                    res["csoc_items"].append((i, p1, p2, club_ord, perc, b20, d18, d1c, b22, b23))
                    p += 24
                elif t == 6:
                    p1, p2, club_ord, cash, apps, apfr, ctype = struct.unpack_from("<iiiibbb", buf, p)
                    res["camc_items"].append((i, p1, p2, club_ord, cash, apps, apfr, ctype))
                    p += 19
                elif t == 7:
                    p1, p2, cash, club_ord, bbsd, bbed = struct.unpack_from("<iiiiII", buf, p)
                    res["cbbl_items"].append((i, p1, p2, cash, club_ord, bbsd, bbed))
                    p += 24
                elif t == 9:
                    res["vtag9_cnt"] += 1
                    p += 20
                    for _ in range(4):
                        sl = struct.unpack_from("<I", buf, p)[0]
                        p += 4 + sl
                elif t == 16:
                    res["vtag16_cnt"] += 1
                    c16 = struct.unpack_from("<b", buf, p)[0]
                    p += 1 + 4 * c16
                elif t == 37:
                    res["vtag37_cnt"] += 1
                    p += 27
                elif t == 38:
                    c38 = struct.unpack_from("<I", buf, p)[0]
                    p += 4
                    for _ in range(c38):
                        ver = buf[p]
                        m38 = struct.unpack_from("<I", buf, p + 1)[0]
                        if m38 != 0:
                            raise RuntimeError(f"Non-zero tag38 inner vec count {m38} at row {i}")
                        ptpl, d1, ptly, w3c = struct.unpack_from("<iIIH", buf, p + 5)
                        sl = struct.unpack_from("<I", buf, p + 19)[0]
                        sstr = buf[p + 23:p + 23 + sl]
                        res["pcpt_items"].append((i, ver, ptpl, d1, ptly, w3c, len(sstr)))
                        p += 23 + sl
                else:
                    raise RuntimeError(f"Unknown polymorphic tag {t} at row {i} pos {p - 1}")
            for tg in seen_tags:
                res["b0_tag_rows"][tg] += 1
            # base+0x48 (TCrs)
            f48b = buf[p]
            res["b48_flag"][i] = f48b
            p += 1
            if f48b:
                v48, c48 = struct.unpack_from("<II", buf, p)
                p += 8
                res["tcrs_ver"][v48] += 1
                res["b48_cnt"][i] = c48
                for _ in range(c48):
                    iv = struct.unpack_from("<h", buf, p)[0]
                    p += 2
                    res["tcrs_item_ver"][iv] += 1
                    if iv != 3:
                        raise RuntimeError(f"Unexpected TCrs item ver {iv} at row {i}")
                    pid, pi, pt, pj, b8, b9 = struct.unpack_from("<iBbHBB", buf, p)
                    res["tcrs_items"].append((i, pid, pi, pt, pj, b8, b9))
                    p += 10

    if p != len(buf):
        raise RuntimeError(f"EOF mismatch (server={server}): cursor={p}, len={len(buf)}")
    res["common_tail_sha256"] = ct_hash.hexdigest()
    del res["common_tail_hash"]
    return res


def summarize_int_arr(
    arr: np.ndarray,
    *,
    min_v: int | None = None,
    max_v: int | None = None,
    allowed: set[int] | None = None,
    suppress_val: int | None = None,
    ctor_default: int | None = None,
    mask: np.ndarray | None = None,
) -> dict[str, Any]:
    if mask is not None:
        idxs = np.where(mask)[0]
        sub = arr[idxs]
    else:
        idxs = None
        sub = arr

    vals, cnts = np.unique(sub, return_counts=True)
    hist = {str(int(v)): int(c) for v, c in zip(vals, cnts)} if len(vals) <= 32 else None
    out: dict[str, Any] = {
        "evaluated_rows": int(len(sub)),
        "distinct": int(len(vals)),
        "min": int(vals[0]) if len(vals) else None,
        "max": int(vals[-1]) if len(vals) else None,
        "count_zero": int(np.sum(sub == 0)),
        "count_minus1": int(np.sum(sub == -1)),
        "sha256": sha256_bytes(sub.tobytes()),
    }
    if ctor_default is not None:
        out["ctor_default"] = ctor_default
        out["count_eq_ctor_default"] = int(np.sum(sub == ctor_default))
        out["count_ne_ctor_default"] = int(np.sum(sub != ctor_default))
    if hist is not None:
        out["histogram"] = hist

    # Domain violations
    check_sub = sub
    check_rows = idxs if idxs is not None else np.arange(len(arr))
    if suppress_val is not None:
        live = check_sub != suppress_val
        out["suppressed_value"] = suppress_val
        out["suppressed_rows"] = int(np.sum(~live))
        out["live_rows"] = int(np.sum(live))
        check_sub = check_sub[live]
        check_rows = check_rows[live]

    bad_mask = np.zeros(len(check_sub), dtype=bool)
    if min_v is not None:
        bad_mask |= check_sub < min_v
    if max_v is not None:
        bad_mask |= check_sub > max_v
    if allowed is not None:
        bad_mask |= ~np.isin(check_sub, list(allowed))

    viol_cnt = int(np.sum(bad_mask))
    out["violations"] = viol_cnt
    if viol_cnt:
        first_pos = int(np.argmax(bad_mask))
        out["first_counterexample"] = {
            "row_ordinal": int(check_rows[first_pos]),
            "raw_value": int(check_sub[first_pos]),
            "bad_distinct_values": sorted(int(x) for x in np.unique(check_sub[bad_mask])),
        }
    return out


def build_all(exe_path: Path, data_dir: Path, out_dir: Path) -> int:
    print("[t82] 1/5 Verifying frozen MANIFEST & pinned SHA-256s...")
    pinned_ok = verify_manifest_and_inputs(exe_path, data_dir)

    master = json.loads((ROOT / "evidence/fm24/reports/editor_schema/master.json").read_bytes())
    club_fields = master["entities"]["club.xml"][0]["fields"]
    enums = master["enums"]
    occ_counts = Counter(f["field"] for f in club_fields)

    t57 = json.loads((ROOT / "scratch/t57/out/field_map.json").read_bytes())
    t63 = json.loads((ROOT / "scratch/t63/out/field_map_r2.json").read_bytes())
    t71 = json.loads((ROOT / "scratch/t71/out/field_map_r3.json").read_bytes())

    t57_by_idx = {e["xml_index"]: e for e in t57["fields"] if "xml_index" in e}
    t63_by_idx = {}
    for e in t63["fields"]:
        idx = (e.get("r1_id") or {}).get("xml_index")
        if idx is None and "/" in e.get("id", ""):
            idx = int(e["id"].rsplit("/", 1)[1])
        if idx is not None:
            t63_by_idx[idx] = e
    t71_idx_check = {int(e["id"].rsplit("/", 1)[1]) for e in t71["fields"]}
    if t71_idx_check != T71_L3_INDICES:
        raise RuntimeError(f"t71 L3 indices drift: {sorted(t71_idx_check)}")

    print("[t82] 2/5 Extracting FMF archives & join tables...")
    cli_ent, cli_raw = open_fmf(data_dir / "client_db.dat")
    srv_ent, srv_raw = open_fmf(data_dir / "server_db.dat")

    cli_ex3 = extract_fmf_member(cli_raw, cli_ent, "client_db/table_extra_3.dat")
    srv_ex3 = extract_fmf_member(srv_raw, srv_ent, "server_db/table_extra_3.dat")
    t3_cli = extract_fmf_member(cli_raw, cli_ent, "client_db/table_3.dat")
    t25_cli = extract_fmf_member(cli_raw, cli_ent, "client_db/table_25.dat")
    t23_srv = extract_fmf_member(srv_raw, srv_ent, "server_db/table_23.dat")
    t45_srv = extract_fmf_member(srv_raw, srv_ent, "server_db/table_45.dat")

    club_ord_to_uid, club_uids = extract_seq_uids(t3_cli)
    _, comp_uids = extract_seq_uids(t25_cli)
    _, stage_name_uids = extract_seq_uids(t23_srv)
    t45_count = struct.unpack_from("<I", t45_srv, 8)[0]

    print(f"      table_3={len(club_uids)}, table_25={len(comp_uids)}, table_23={len(stage_name_uids)}, table_45(STARTING_RECORD)={t45_count}")

    print("[t82] 3/5 Full-archive sequential replay & vectorized profiling (84,259 x 2 rows)...")
    cli = replay_table_extra_3(cli_ex3, server=False)
    srv = replay_table_extra_3(srv_ex3, server=True)

    # Assert 100% client == server byte equality across the entire common tail!
    if cli["common_tail_sha256"] != srv["common_tail_sha256"]:
        raise RuntimeError("Client vs server common tail SHA-256 mismatch!")
    if not (
        np.array_equal(cli["d8"], srv["d8"])
        and np.array_equal(cli["cc"], srv["cc"])
        and np.array_equal(cli["base_ac"], srv["base_ac"])
        and np.array_equal(cli["base_a0"], srv["base_a0"])
        and np.array_equal(cli["base_a8"], srv["base_a8"])
        and cli["tcht_map"] == srv["tcht_map"]
        and cli["kit_buckets"] == srv["kit_buckets"]
    ):
        raise RuntimeError("Client vs server common tail field mismatch!")

    print("[t82] 4/5 Collecting PE static witnesses from editor.exe...")
    pei = PEInspector(exe_path)

    # Core structural functions
    core_witnesses = {
        "CLUB_EXTRA_READER": pei.insn_at(0xE5D210, 4),
        "CLUB_EXTRA_MODE_BRANCH": pei.insn_at(0xE5D2B7, 2),
        "CLUB_EXTRA_CTOR": pei.insn_at(0x3AABA20, 4),
        "CLUB_EXTRA_FIXUP": pei.insn_at(0x3AAE490, 4),
        "CLUB_EXTRA_SET": pei.insn_at(0xE57E6F, 3),
        "CLUB_EXTRA_WRITER": pei.insn_at(0xE5F3D0, 4),
        "TC_EXTRA_READER": pei.insn_at(0x11D3200, 4),
        "TC_EXTRA_FIXUP": pei.insn_at(0x3EA1030, 4),
        "TC_EXTRA_SET": pei.insn_at(0x11CF800, 4),
        "TC_EXTRA_WRITER": pei.insn_at(0x11D53F0, 4),
        "CLUB_GET": pei.insn_at(0xE89A00, 4),
        "CLUB_SET": pei.insn_at(0xE82AA0, 4),
        "TC_GET2": pei.insn_at(0x11F0690, 4),
        "TC_SET2": pei.insn_at(0x11F4200, 4),
        "ELECTION_READER": pei.insn_at(0x4342940, 4),
        "ELECTION_GET": pei.insn_at(0xE96F20, 4),
        "ELECTION_SET": pei.insn_at(0x3AEB720, 4),
        "SUPPORTER_READER": pei.insn_at(0x4340450, 4),
        "SUPPORTER_GET": pei.insn_at(0x1520050, 4),
        "SUPPORTER_SET": pei.insn_at(0x43419B0, 4),
        "UEFA_RING_PUSH": pei.insn_at(0x39AA1F0, 4),
        "UEFA_DIV_1000_F64": pei.bytes_at(0x179F810, 8),
        "EXTRA_DA_DECODER": pei.insn_at(0x4348EF0, 4),
        "UID_PACKER_0xfe68b0": pei.insn_at(0xFE68CA, 2),
        "KIT_FILTER_HELPER": pei.insn_at(0x3EC2F60, 4),
        "KIT_FILTER_CMP_B22_B25": pei.insn_at(0x3EC2FE9, 5),
        "CSCM_ITEM_READER": pei.insn_at(0x3AAF9E0, 4),
        "CSCM_ITEM_GET": pei.insn_at(0xEAF720, 4),
        "CSCM_SET": pei.insn_at(0xEAEDB0, 4),
        "CPSL_ITEM_GET": pei.insn_at(0x1524AF0, 4),
        "CPSL_SET": pei.insn_at(0xEAC360, 4),
        "CSPB_ITEM_READER": pei.insn_at(0x3EA5150, 4),
        "CSPB_ITEM_GET": pei.insn_at(0x11F8990, 4),
        "CREN_INLINE_READER": pei.insn_at(0x11D45F0, 4),
        "CREN_ITEM_GET": pei.insn_at(0x3EC49F0, 4),
        "TCRS_READER": pei.insn_at(0x4387AB0, 4),
        "TCRS_SUB_READER": pei.insn_at(0x155C120, 4),
        "TCRS_ITEM_GET": pei.insn_at(0x155A320, 4),
        "POLY_FACTORY": pei.insn_at(0x14CF6D0, 4),
        "POLY_LIST_FILTER": pei.insn_at(0x43462A0, 4),
        "PCPT_ITEM_GET": pei.insn_at(0x42F5660, 4),
        "DERIVED_COLOUR_PARENT": pei.insn_at(0x3AE7420, 4),
        "DERIVED_COLOUR_SEARCH": pei.insn_at(0x11DC460, 4),
        "DERIVED_COLOUR_CONTRAST": pei.insn_at(0x150D300, 4),
    }

    # Verify UEFA divisor constant 1000.0
    if struct.unpack("<d", bytes.fromhex(core_witnesses["UEFA_DIV_1000_F64"]["bytes"]))[0] != 1000.0:
        raise RuntimeError("UEFA divisor at 0x179f810 is not 1000.0!")

    cuf_get_jt = pei.rel32_table(0xE91DB0, 9)
    cuf_set_jt = pei.rel32_table(0xE86B54, 9)

    # Polymorphic base+0x00 vtable & RTTI proofs
    poly_tags_meta = [
        (4, 0x18B86B8, 0x42C8F90, 0x42CBE80, "CCBc (not in club.xml; CLUB_GET 0xe8b3eb / CLUB_EXTRA_SET 0xe57f8d)"),
        (5, 0x18B8768, 0x42D2710, 0x42CF700, "Csoc (club.xml[120], Sell On Clauses)"),
        (6, 0x18B8818, 0x42D6A10, 0x42D6680, "Camc (club.xml[121], Conditional Fees)"),
        (7, 0x18B8608, 0x42C66F0, 0x42C7150, "Cbbl (club.xml[119], Player Buy Back Clauses)"),
        (9, 0x18B9208, 0x42DBA50, None, "Internal/Nation NA*/NG* via 0x3ebcf40 (vt[+0x28]=0xbb0, not in club.xml)"),
        (16, 0x18B9A88, 0x14D7530, None, "Internal club cup points via 0x3ebd740 (vt[+0x28]=0xbb0, not in club.xml)"),
        (37, 0x18B88D8, 0x42D9380, 0x42D83B0, "Internal EPPP clause (vt[+0x38]=0x25!=6, excluded by Camc; not in club.xml)"),
        (38, 0x18B9428, 0x14DA470, 0x42F5660, "pcpt (club.xml[196], Player Testimonial List)"),
    ]
    poly_catalog = []
    for tag, vt_fo, rdr_fo, get_fo, role in poly_tags_meta:
        vt_info = pei.vtable_slots(vt_fo, 8)
        poly_catalog.append({
            "tag": tag,
            "observed_items": int(srv["b0_tags"][tag]),
            "observed_rows": int(srv["b0_tag_rows"][tag]),
            "role": role,
            "vtable": vt_info,
            "reader": pei.insn_at(rdr_fo, 3),
            "item_getter": pei.insn_at(get_fo, 3) if get_fo else None,
        })
    # Add unobserved tag 35 (0x23) for CssT..E
    poly_catalog.append({
        "tag": 35,
        "observed_items": int(srv["b0_tags"][35]),
        "observed_rows": int(srv["b0_tag_rows"][35]),
        "role": "CssT/CssP/CssS/CssE (club.xml[109..112], preserved t63 held; 0 items / 0 rows in archive)",
        "vtable": None,
        "reader": None,
        "item_getter": None,
    })

    # Negative proof: CBW*/CBD* and club.xml[211..327] -> STARTING_RECORD (table_45.dat)
    sr_vt = pei.vtable_slots(0x1881308, 4)
    if "DATABASE_TABLE@VSTARTING_RECORD@db" not in sr_vt["rtti"]:
        raise RuntimeError(f"Unexpected RTTI at 0x1881308: {sr_vt['rtti']}")
    negative_starting_record = {
        "proof_summary": (
            "CBW*/CBD* and all club record 4CCs (club.xml[211..327]) do NOT touch CLUB+0x100 or CLUB+0xb0 "
            "or table_extra_3.dat. TC_GET2 (0x11f0ca7 CBDa / 0x11f0cb6 CBWa -> hub 0x11f2a76) and "
            "CLUB_GET (hub 0xe8f1d9) dispatch via 0x11e8af0 -> TC_RECORD_GET (0x3ebad50), and setters via "
            "0x11e8b40 -> TC_RECORD_SET (0x3ebaf50), which load global DATABASE_TABLE<STARTING_RECORD>* at "
            "VA 0x141b60190 (table type 0x2d = 45 -> server_db/table_45.dat, 84,477 rows), matching "
            "[rec+0x4c]==[CLUB+0xc] and [rec+0x5e]==rec_type before forwarding to RECORD_GET 0x1543ca0."
        ),
        "table_type": 45,
        "table_member": "server_db/table_45.dat",
        "table_45_bytes": len(t45_srv),
        "table_45_rows": int(t45_count),
        "global_table_ptr_va": "0x141b60190",
        "global_table_ptr_fo": "0x1b5f190",
        "database_table_vtable": sr_vt,
        "witnesses": {
            "table_45_init_type_0x2d": pei.insn_at(0xF06C70, 4),
            "tc_get2_cbda_switch": pei.insn_at(0x11F0CA7, 3),
            "tc_get2_cbwa_switch": pei.insn_at(0x11F0CB6, 3),
            "tc_set2_cbda_switch": pei.insn_at(0x11F495B, 3),
            "tc_set2_cbwa_switch": pei.insn_at(0x11F496B, 3),
            "tc_get2_hub_to_11e8af0": pei.insn_at(0x11F2A76, 1),
            "club_get_hub_to_11e8af0": pei.insn_at(0xE8F1D9, 1),
            "tc_record_get_load_global": pei.insn_at(0x3EBAD50, 5),
            "tc_record_get_match_club_and_type": pei.insn_at(0x3EBAD7C, 4),
            "tc_record_set_entry": pei.insn_at(0x3EBAF50, 4),
            "record_get_entry": pei.insn_at(0x1543CA0, 4),
            "record_set_entry": pei.insn_at(0x1544C80, 4),
        },
        "club_xml_indices": list(range(211, 328)),
        "club_xml_count": 117,
        "cbw_cbd_codes": [club_fields[i]["field"] for i in range(211, 221)],
    }

    # --- Compute full-archive domain stats ---
    el_mask = srv["elec_flag"] == 1
    cown_37 = np.isin(srv["Cown"], [3, 7])
    elec_invariants = {
        "elec_present_rows": int(np.sum(el_mask)),
        "elec_absent_rows": int(np.sum(~el_mask)),
        "elec_club_eq_row_ordinal": int(np.sum(srv["elec_club"][el_mask] == np.where(el_mask)[0])),
        "cown_in_3_7_rows": int(np.sum(cown_37)),
        "elec_iff_cown_in_3_7_exact_rows": int(np.sum(el_mask == cown_37)),
        "cown_when_elec1": {str(k): int(v) for k, v in sorted(Counter(srv["Cown"][el_mask].tolist()).items())},
        "cown_when_elec0": {str(k): int(v) for k, v in sorted(Counter(srv["Cown"][~el_mask].tolist()).items())},
        "elec_d2_sentinel_rows": int(np.sum(srv["elec_d2"][el_mask] == SENTINEL_DATE4)),
    }

    # Scalar & enum domain summaries
    pfms_vals = {int(v["enum"]) for v in enums["pfms"]["values"]}
    sfms_vals = {int(v["enum"]) for v in enums["sfms"]["values"]}
    dfms_vals = {int(v["enum"]) for v in enums["dfms"]["values"]}
    afms_vals = {int(v["enum"]) for v in enums["afms"]["values"]}
    ftjn_vals = {int(v["enum"]) for v in enums["ftjn"]["values"]}

    scalar_domains = {
        # CLUB+0x100 direct scalars
        "Ctlv": summarize_int_arr(srv["Ctlv"], min_v=0, max_v=20, ctor_default=0),
        "Cmle": summarize_int_arr(srv["Cmle"], min_v=0, max_v=20, ctor_default=10),
        "Cyim": summarize_int_arr(srv["Cyim"], min_v=-1, max_v=20, ctor_default=0),
        "Cyfb": summarize_int_arr(srv["Cyfb"], min_v=-1, max_v=20, ctor_default=0),
        "Cytv": summarize_int_arr(srv["Cytv"], min_v=-1, max_v=20, ctor_default=10),
        "Crcb": summarize_int_arr(srv["Crcb"], min_v=-1, max_v=20, ctor_default=10),
        "Csth": summarize_int_arr(srv["Csth"], min_v=0, max_v=200000, ctor_default=-1),
        "CScP": summarize_int_arr(srv["CScP"], ctor_default=0),
        "Cown": summarize_int_arr(srv["Cown"], ctor_default=0),
        "Chti": summarize_int_arr(srv["Chti"], ctor_default=1),
        # CLUB+0x100 -> +0x78 election (present rows only)
        "Cetl": summarize_int_arr(srv["Cetl"], min_v=0, max_v=100, mask=el_mask),
        "Cmtm": summarize_int_arr(srv["Cmtm"], min_v=0, max_v=100, mask=el_mask),
        "Cect": summarize_int_arr(srv["Cect"], min_v=0, max_v=100, mask=el_mask),
        "Cemn": summarize_int_arr(srv["Cemn"], min_v=0, max_v=100, mask=el_mask),
        "Cemx": summarize_int_arr(srv["Cemx"], min_v=0, max_v=100, mask=el_mask),
        "Cepr": summarize_int_arr(srv["Cepr"], mask=el_mask),
        # CLUB+0x100 -> +0xf8 supporter profile
        "Csly": summarize_int_arr(srv["Csly"], min_v=0, max_v=20, ctor_default=10),
        "Csps": summarize_int_arr(srv["Csps"], min_v=0, max_v=20, ctor_default=10),
        "Cspt": summarize_int_arr(srv["Cspt"], min_v=0, max_v=20, ctor_default=10),
        "Csaf": summarize_int_arr(srv["Csaf"], min_v=0, max_v=20, ctor_default=10),
        "Cste": summarize_int_arr(srv["Cste"], min_v=0, max_v=20, ctor_default=10),
        "Cspe": summarize_int_arr(srv["Cspe"], min_v=0, max_v=20, ctor_default=10),
        # CLUB+0xb0 server attendance
        "Catd": summarize_int_arr(srv["Catd"], min_v=0, max_v=1000000, ctor_default=10000),
        "Cmna": summarize_int_arr(srv["Cmna"], min_v=0, max_v=1000000, ctor_default=10000),
        "Cmxa": summarize_int_arr(srv["Cmxa"], min_v=0, max_v=1000000, ctor_default=10000),
        # CLUB+0xb0 server formations (getter suppresses 0)
        "Cpfr": summarize_int_arr(srv["Cpfr"], allowed=pfms_vals, suppress_val=0, ctor_default=0),
        "C2pf": summarize_int_arr(srv["C2pf"], allowed=sfms_vals, suppress_val=0, ctor_default=0),
        "Cdfo": summarize_int_arr(srv["Cdfo"], allowed=dfms_vals, suppress_val=0, ctor_default=0),
        "Cafo": summarize_int_arr(srv["Cafo"], allowed=afms_vals, suppress_val=0, ctor_default=0),
    }

    # UEFA coeff ring buffer Cuf1..Cuf9, Cf10
    cuf_codes = [f"Cuf{k}" for k in range(1, 10)] + ["Cf10"]
    cuf_domains: dict[str, Any] = {}
    for k, fc in enumerate(cuf_codes):
        col = srv["cuf_f32"][:, k]
        raw_col = srv["cuf_raw"][:, k]
        present = srv["cuf_has"]
        bad = (col < 0.0) | (col > 50.0) | (~np.isfinite(col))
        cuf_domains[fc] = {
            "ring_slot": k,
            "rows": 84259,
            "present_object_rows": int(np.sum(present)),
            "absent_default_zero_rows": int(np.sum(~present)),
            "nonzero_rows": int(np.sum(raw_col != 0)),
            "min_f32": float(np.min(col)),
            "max_f32": float(np.max(col)),
            "raw_min_milli": int(np.min(raw_col)),
            "raw_max_milli": int(np.max(raw_col)),
            "violations": int(np.sum(bad)),
            "sha256": sha256_bytes(raw_col.tobytes()),
        }

    # Common tail string & colour domains (client+server 100% identical)
    tcht_domain = {
        "scope": "client+server",
        "client_eq_server_rows": 84259,
        "rows": 84259,
        "nonempty_rows": len(srv["tcht_map"]),
        "empty_rows": 84259 - len(srv["tcht_map"]),
        "bad_utf8": int(srv["tcht_bad_utf8"]),
        "max_byte_len": int(np.max(srv["tcht_len"])),
        "violations": int(srv["tcht_bad_utf8"]),
        "sha256": sha256_bytes(json.dumps(sorted(srv["tcht_map"].items()), ensure_ascii=False).encode("utf-8")),
    }
    tcnn_domain = {
        "scope": "conditional_wire_0_populated",
        "gated_by": "CLUB+0xba != 0",
        "populated_rows": 0,
        "rows": 84259,
    }

    def colour_stats(arr: np.ndarray) -> dict[str, Any]:
        nz = arr != 0
        alpha_ff = (arr >> 24) == 0xFF
        return {
            "scope": "client+server",
            "client_eq_server_rows": 84259,
            "rows": 84259,
            "zero_fallback_rows": int(np.sum(~nz)),
            "nonzero_rows": int(np.sum(nz)),
            "nonzero_alpha_0xff_rows": int(np.sum(nz & alpha_ff)),
            "nonzero_other_alpha_rows": int(np.sum(nz & (~alpha_ff))),
            "sha256": sha256_bytes(arr.tobytes()),
        }

    ttcl_domain = colour_stats(srv["base_a0"])
    tbcl_domain = colour_stats(srv["base_a8"])
    ttcl_eq_tbcl_nz = int(np.sum((srv["base_a0"] != 0) & (srv["base_a0"] == srv["base_a8"])))

    # List-field item-level domain audits
    # 1. Cscm (+0x28)
    cscm = srv["cscm_items"]
    cscm_co_miss = [x for x in cscm if x[2] != -1 and x[2] not in comp_uids]
    cscm_stnm_viol = [x for x in cscm if not (0 <= x[4] <= 200)]
    cscm_slsn_zero = [x for x in cscm if x[5] == 0]
    cscm_slsn_nz_miss = [x for x in cscm if x[5] not in (-1, 0) and x[5] not in stage_name_uids]
    cscm_domain = {
        "rows_populated": len({x[0] for x in cscm}),
        "total_items": len(cscm),
        "ver_hist": {str(k): v for k, v in sorted(Counter(x[1] for x in cscm).items())},
        "stco_eq_pair": sum(x[2] == x[3] for x in cscm),
        "stco_table25_miss": len(cscm_co_miss),
        "stnm_min": min(x[4] for x in cscm),
        "stnm_max": max(x[4] for x in cscm),
        "stnm_violations": len(cscm_stnm_viol),
        "slsn_eq_pair": sum(x[5] == x[6] for x in cscm),
        "slsn_zero_not_in_table23": len(cscm_slsn_zero),
        "slsn_nonzero_table23_miss": len(cscm_slsn_nz_miss),
        "tail4_minus1": sum(x[7] == -1 for x in cscm),
        "violations": len(cscm_co_miss) + len(cscm_stnm_viol) + len(cscm_slsn_zero) + len(cscm_slsn_nz_miss),
        "first_counterexample": {
            "row_ordinal": cscm_slsn_zero[0][0],
            "club_uid": club_ord_to_uid[cscm_slsn_zero[0][0]],
            "stco": cscm_slsn_zero[0][2],
            "stnm": cscm_slsn_zero[0][4],
            "slsn": cscm_slsn_zero[0][5],
            "reason": "slsn=0 is passed through by 0xfe68ca (cmp [rcx],0; js null) and does not exist in table_23 STAGE_NAME UIDs (min UID=1)",
        } if cscm_slsn_zero else None,
    }

    # 2. CPsL (+0x68)
    cpsl = srv["cpsl_items"]
    cpsl_bad = [x for x in cpsl if x[1] != 2 or x[2] <= 0 or x[3] <= 0]
    cpsl_domain = {
        "rows_populated": len({x[0] for x in cpsl}),
        "total_items": len(cpsl),
        "tag_hist": {str(k): v for k, v in sorted(Counter(x[1] for x in cpsl).items())},
        "per1_min": min(x[2] for x in cpsl),
        "per1_max": max(x[2] for x in cpsl),
        "per1_nonpositive": sum(x[2] <= 0 for x in cpsl),
        "per2_min": min(x[3] for x in cpsl),
        "per2_max": max(x[3] for x in cpsl),
        "per2_nonpositive": sum(x[3] <= 0 for x in cpsl),
        "w8_hist": {str(k): v for k, v in sorted(Counter(x[4] for x in cpsl).items())},
        "person_uid_note": "All per1/per2 are positive person UIDs; person/PDxx table decode is out-of-scope per AGENTS.md",
        "violations": len(cpsl_bad),
    }

    # 3. Cspb (base+0x18)
    cspb = srv["cspb_items"]
    cspb_co_miss = [x for x in cspb if x[2] != -1 and x[2] not in comp_uids]
    cspb_matc_viol = [x for x in cspb if x[5] != -1 and not (0 <= x[5] <= 127)]
    cspb_d1_bad = [x for x in cspb if not check_date4_scalar(x[7])[0]]
    cspb_d2_bad = [x for x in cspb if not check_date4_scalar(x[8])[0]]
    cspb_domain = {
        "rows_populated": len({x[0] for x in cspb}),
        "total_items": len(cspb),
        "ver_hist": {str(k): v for k, v in sorted(Counter(x[1] for x in cspb).items())},
        "cmid_eq_pair": sum(x[2] == x[3] for x in cspb),
        "cmid_null_minus1": sum(x[2] == -1 for x in cspb),
        "cmid_live": sum(x[2] != -1 for x in cspb),
        "cmid_table25_miss": len(cspb_co_miss),
        "venu_hist": {str(k): v for k, v in sorted(Counter(x[4] for x in cspb).items())},
        "matc_hist": {str(k): v for k, v in sorted(Counter(x[5] for x in cspb).items())},
        "matc_suppressed_minus1": sum(x[5] == -1 for x in cspb),
        "matc_violations": len(cspb_matc_viol),
        "type_hist": {str(k): v for k, v in sorted(Counter(x[6] for x in cspb).items())},
        "stdt_bad": len(cspb_d1_bad),
        "endt_bad": len(cspb_d2_bad),
        "violations": len(cspb_co_miss) + len(cspb_matc_viol) + len(cspb_d1_bad) + len(cspb_d2_bad),
    }

    # 4. Cren (base+0x30)
    cren = srv["cren_items"]
    cren_n_viol = [x for x in cren if not (1 <= x[1] <= 99)]
    cren_p_neg_other = [x for x in cren if x[2] < -1]
    cren_domain = {
        "rows_populated": len({x[0] for x in cren}),
        "total_items": len(cren),
        "rsnn_min": min(x[1] for x in cren),
        "rsnn_max": max(x[1] for x in cren),
        "rsnn_violations": len(cren_n_viol),
        "rsnp_null_minus1": sum(x[2] == -1 for x in cren),
        "rsnp_live_person_ordinal": sum(x[2] >= 0 for x in cren),
        "rsnp_live_min": min(x[2] for x in cren if x[2] >= 0),
        "rsnp_live_max": max(x[2] for x in cren if x[2] >= 0),
        "rsnp_other_neg": len(cren_p_neg_other),
        "rsnr_hist": {str(k): v for k, v in sorted(Counter(x[3] for x in cren).items())},
        "violations": len(cren_n_viol) + len(cren_p_neg_other),
    }

    # 5. TCrs (base+0x48)
    tcrs = srv["tcrs_items"]
    punj_viol = [x for x in tcrs if x[4] != 0 and x[4] not in ftjn_vals]
    tcrs_domain = {
        "flag_1_rows": int(np.sum(srv["b48_flag"] == 1)),
        "rows_with_items": len({x[0] for x in tcrs}),
        "total_items": len(tcrs),
        "container_ver_hist": {str(k): v for k, v in sorted(srv["tcrs_ver"].items())},
        "item_ver_hist": {str(k): v for k, v in sorted(srv["tcrs_item_ver"].items())},
        "PUnI_distinct": len({x[2] for x in tcrs}),
        "PUnI_min": min(x[2] for x in tcrs),
        "PUnI_max": max(x[2] for x in tcrs),
        "PUnT_hist": {str(k): v for k, v in sorted(Counter(x[3] for x in tcrs).items())},
        "PUnJ_zero_suppressed": sum(x[4] == 0 for x in tcrs),
        "PUnJ_ftjn_violations": len(punj_viol),
        "PUnJ_bad_values": sorted({x[4] for x in punj_viol}),
        "PUnP_mode0_uid_items": sum(x[6] == 0 for x in tcrs),
        "PUnP_mode1_ord_null_minus1_items": sum(x[6] == 1 and x[1] == -1 for x in tcrs),
        "violations": len(punj_viol),
        "first_counterexample": {
            "row_ordinal": punj_viol[0][0],
            "club_uid": club_ord_to_uid[punj_viol[0][0]],
            "PUnP": punj_viol[0][1],
            "PUnI": punj_viol[0][2],
            "PUnT": punj_viol[0][3],
            "PUnJ": punj_viol[0][4],
            "reason": "PUnJ outside frozen enums['ftjn'] (and PUnI/PUnT lack scoped enum_ref)",
        },
    }

    # 6. Polymorphic Csoc (tag 5), Camc (tag 6), Cbbl (tag 7), pcpt (tag 38)
    csoc = srv["csoc_items"]
    csoc_club_oob = [x for x in csoc if not (0 <= x[3] < 84259)]
    csoc_perc_viol = [x for x in csoc if not (0 <= x[4] <= 100)]
    csoc_wrong_uid_hits = sum(x[3] in club_uids for x in csoc)
    csoc_domain = {
        "rows_populated": len({x[0] for x in csoc}),
        "total_items": len(csoc),
        "play_eq_pair": sum(x[1] == x[2] for x in csoc),
        "play_min": min(x[1] for x in csoc),
        "play_max": max(x[1] for x in csoc),
        "play_nonpositive": sum(x[1] <= 0 for x in csoc),
        "club_ordinal_in_range": len(csoc) - len(csoc_club_oob),
        "club_ordinal_oob": len(csoc_club_oob),
        "club_wrong_uid_control_hits": csoc_wrong_uid_hits,
        "club_wrong_uid_control_misses": len(csoc) - csoc_wrong_uid_hits,
        "perc_min": min(x[4] for x in csoc),
        "perc_max": max(x[4] for x in csoc),
        "perc_violations": len(csoc_perc_viol),
        "violations": len(csoc_club_oob) + len(csoc_perc_viol) + sum(x[1] <= 0 for x in csoc),
    }

    camc = srv["camc_items"]
    camc_club_oob = [x for x in camc if not (0 <= x[3] < 84259)]
    camc_cash_viol = [x for x in camc if not (0 <= x[4] <= 1_000_000_000)]
    camc_apps_viol = [x for x in camc if not (1 <= x[5] <= 100)]
    camc_apfr_viol = [x for x in camc if not (1 <= x[6] <= 100)]
    camc_wrong_uid_hits = sum(x[3] in club_uids for x in camc)
    camc_domain = {
        "rows_populated": len({x[0] for x in camc}),
        "total_items": len(camc),
        "play_eq_pair": sum(x[1] == x[2] for x in camc),
        "club_ordinal_in_range": len(camc) - len(camc_club_oob),
        "club_wrong_uid_control_hits": camc_wrong_uid_hits,
        "club_wrong_uid_control_misses": len(camc) - camc_wrong_uid_hits,
        "cash_min": min(x[4] for x in camc),
        "cash_max": max(x[4] for x in camc),
        "cash_violations": len(camc_cash_viol),
        "apps_min": min(x[5] for x in camc),
        "apps_max": max(x[5] for x in camc),
        "apps_violations": len(camc_apps_viol),
        "apfr_min": min(x[6] for x in camc),
        "apfr_max": max(x[6] for x in camc),
        "apfr_violations_lt_1": len(camc_apfr_viol),
        "type_hist": {str(k): v for k, v in sorted(Counter(x[7] for x in camc).items())},
        "violations": len(camc_club_oob) + len(camc_cash_viol) + len(camc_apps_viol) + len(camc_apfr_viol),
        "first_counterexample": {
            "row_ordinal": camc_apfr_viol[0][0],
            "club_uid": club_ord_to_uid[camc_apfr_viol[0][0]],
            "play": camc_apfr_viol[0][1],
            "club_ord": camc_apfr_viol[0][3],
            "cash": camc_apfr_viol[0][4],
            "apps": camc_apfr_viol[0][5],
            "apfr": camc_apfr_viol[0][6],
            "type": camc_apfr_viol[0][7],
            "reason": "apfr=0 < frozen min_value=1 (VTAG6_GET 0x42d6759 does not suppress 0) and subfield type lacks scoped enum_ref",
        },
    }

    cbbl = srv["cbbl_items"]
    cbbl_club_oob = [x for x in cbbl if not (0 <= x[4] < 84259)]
    cbbl_cash_viol = [x for x in cbbl if not (0 <= x[3] <= 1_000_000_000)]
    cbbl_d1_bad = [x for x in cbbl if not check_date4_scalar(x[5])[0]]
    cbbl_d2_bad = [x for x in cbbl if not check_date4_scalar(x[6])[0]]
    cbbl_wrong_uid_hits = sum(x[4] in club_uids for x in cbbl)
    cbbl_domain = {
        "rows_populated": len({x[0] for x in cbbl}),
        "total_items": len(cbbl),
        "play_eq_pair": sum(x[1] == x[2] for x in cbbl),
        "play_min": min(x[1] for x in cbbl),
        "play_max": max(x[1] for x in cbbl),
        "play_nonpositive": sum(x[1] <= 0 for x in cbbl),
        "cash_min": min(x[3] for x in cbbl),
        "cash_max": max(x[3] for x in cbbl),
        "cash_violations": len(cbbl_cash_viol),
        "club_ordinal_in_range": len(cbbl) - len(cbbl_club_oob),
        "club_wrong_uid_control_hits": cbbl_wrong_uid_hits,
        "club_wrong_uid_control_misses": len(cbbl) - cbbl_wrong_uid_hits,
        "bbsd_bad": len(cbbl_d1_bad),
        "bbsd_sentinel": sum(x[5] == SENTINEL_DATE4 for x in cbbl),
        "bbed_bad": len(cbbl_d2_bad),
        "bbed_sentinel": sum(x[6] == SENTINEL_DATE4 for x in cbbl),
        "violations": len(cbbl_club_oob) + len(cbbl_cash_viol) + len(cbbl_d1_bad) + len(cbbl_d2_bad) + sum(x[1] <= 0 for x in cbbl),
    }

    pcpt = srv["pcpt_items"]
    pcpt_d1_bad = [x for x in pcpt if not check_date4_scalar(x[3])[0]]
    pcpt_d2_bad = [x for x in pcpt if not check_date4_scalar(x[4])[0]]
    pcpt_domain = {
        "rows_populated": len({x[0] for x in pcpt}),
        "total_items": len(pcpt),
        "ver_hist": {str(k): v for k, v in sorted(Counter(x[1] for x in pcpt).items())},
        "PtPl_min": min(x[2] for x in pcpt),
        "PtPl_max": max(x[2] for x in pcpt),
        "PtPl_nonpositive": sum(x[2] <= 0 for x in pcpt),
        "d1_sentinel": sum(x[3] == SENTINEL_DATE4 for x in pcpt),
        "d1_bad": len(pcpt_d1_bad),
        "PtLy_bad": len(pcpt_d2_bad),
        "PtLy_sentinel": sum(x[4] == SENTINEL_DATE4 for x in pcpt),
        "PtLy_years": sorted({(x[4] >> 16) & 0xFFFF for x in pcpt}),
        "trailing_str_nonempty": sum(x[6] > 0 for x in pcpt),
        "violations": len(pcpt_d1_bad) + len(pcpt_d2_bad) + sum(x[2] <= 0 for x in pcpt),
    }

    # 7. Kits (base+0x78)
    kit_bucket_names = {
        (0, 1): "Tko1", (0, 0): "Tkg1",
        (1, 1): "Tko2", (1, 0): "Tkg2",
        (2, 1): "Tko3", (2, 0): "Tkg3",
    }
    kit_unmapped_buckets = {str(k): v for k, v in srv["kit_buckets"].items() if k not in kit_bucket_names}
    kit_comp_miss = [x for x in srv["kit_comp_vals"] if x[1] not in comp_uids]
    kit_domain = {
        "scope": "client+server",
        "client_eq_server_rows": 84259,
        "total_items": int(srv["kit_total"]),
        "tag_hist": {str(k): v for k, v in sorted(srv["kit_tag_counter"].items())},
        "buckets": {
            kit_bucket_names[b]: {
                "kit_type_b22": b[0],
                "outfield_b25": b[1],
                "items": int(srv["kit_buckets"][b]),
                "rows": len(srv["kit_bucket_rows"][b]),
            }
            for b in [(0, 1), (0, 0), (1, 1), (1, 0), (2, 1), (2, 0)]
        },
        "unmapped_buckets": kit_unmapped_buckets,
        "comp_nonzero_items": len(srv["kit_comp_vals"]),
        "comp_nonzero_table25_miss": len(kit_comp_miss),
    }

    # Unnamed / internal wire slot stats (100% byte accounting)
    p10c_expected = struct.pack("<ihh12b", -1, -1, -1, 10, 10, 10, 10, 10, 10, 0, 0, 0, 0, 0, 0)
    p10c_eq_def = int(np.sum(np.all(srv["p10c_raw"] == np.frombuffer(p10c_expected, dtype=np.uint8), axis=1)))
    internal_slots = {
        "extra_plus_0x18_u16_cnt": {"all_zero": bool(np.all(srv["e18_cnt"] == 0)), "max": int(np.max(srv["e18_cnt"]))},
        "extra_plus_0x20_u8_cnt_INT_DUTY": {"all_zero": bool(np.all(srv["e20_cnt"] == 0)), "max": int(np.max(srv["e20_cnt"]))},
        "extra_plus_0x30_0x38_0x70_0x50_0x40": {"all_zero_84259": True},
        "extra_plus_0xda_5B_bitfield": {
            "tag_all_zero": bool(np.all(srv["eda_tag"] == 0)),
            "b1_max": int(np.max(srv["eda_b1"])), "b1_nz": int(np.sum(srv["eda_b1"] != 0)),
            "b2_max": int(np.max(srv["eda_b2"])), "b2_nz": int(np.sum(srv["eda_b2"] != 0)),
            "b3_max": int(np.max(srv["eda_b3"])), "b3_nz": int(np.sum(srv["eda_b3"] != 0)),
            "b4_max": int(np.max(srv["eda_b4"])), "b4_nz": int(np.sum(srv["eda_b4"] != 0)),
            "getter_setter_hits": 0,
        },
        "extra_plus_0x123_i8": {
            "min": int(np.min(srv["e123"])), "max": int(np.max(srv["e123"])),
            "nonzero_rows": int(np.sum(srv["e123"] != 0)), "getter_setter_hits": 0,
        },
        "extra_plus_0xcc_u32_TCoi": {
            "scope": "client+server",
            "client_0xffffffff_rows": int(np.sum(cli["cc"] == 0xFFFFFFFF)),
            "client_zero_rows": int(np.sum(cli["cc"] == 0)),
            "server_0xffffffff_rows": int(np.sum(srv["cc"] == 0xFFFFFFFF)),
            "server_zero_rows": int(np.sum(srv["cc"] == 0)),
        },
        "extra_dates_sentinel_check": {
            "e80_sentinel_rows": int(np.sum(srv["e80"] == SENTINEL_DATE4)),
            "e84_sentinel_rows": int(np.sum(srv["e84"] == SENTINEL_DATE4)),
            "eb8_sentinel_rows": int(np.sum(srv["eb8"] == SENTINEL_DATE4)),
            "ebc_sentinel_rows": int(np.sum(srv["ebc"] == SENTINEL_DATE4)),
            "e88_6_sentinel_cells": int(np.sum(srv["e88_dates"] == SENTINEL_DATE4)),
            "ea0_flag_1_rows": int(np.sum(srv["edates_flag"] == 1)),
            "ea0_6_sentinel_cells": int(np.sum(srv["ea0_dates"] == SENTINEL_DATE4)),
        },
        "extra_constants": {
            "e122_all_0": bool(np.all(srv["e122"] == 0)),
            "e125_all_0": bool(np.all(srv["e125"] == 0)),
            "e128_all_minus1": bool(np.all(srv["e128"] == -1)),
            "e12e_all_minus2": bool(np.all(srv["e12e"] == -2)),
            "e12f_Cels_all_minus1": bool(np.all(srv["e12f"] == -1)),
            "ec4_all_0": bool(np.all(srv["ec4"] == 0)),
            "ec8_CMwg_all_0": bool(np.all(srv["ec8"] == 0)),
            "ed0_all_minus1": bool(np.all(srv["ed0"] == -1)),
            "ed4_all_0": bool(np.all(srv["ed4"] == 0)),
            "edc_all_1": bool(np.all(srv["edc"] == 1)),
            "ede_all_0": bool(np.all(srv["ede"] == 0)),
            "f8_CsSF_all_minus1": bool(np.all(srv["f8_CsSF"] == -1)),
            "f8_CsSS_all_minus1": bool(np.all(srv["f8_CsSS"] == -1)),
            "f8_CsST_all_minus1": bool(np.all(srv["f8_CsST"] == -1)),
            "f8_tail6_Cfph_Cfpc_all_0": bool(np.all(srv["f8_tail6"] == 0)),
            "p10c_eq_ctor_default_rows": p10c_eq_def,
        },
        "base_plus_0xac_u16": {
            "scope": "client+server",
            "client_eq_server": True,
            "min": int(np.min(srv["base_ac"])), "max": int(np.max(srv["base_ac"])),
            "nonzero_rows": int(np.sum(srv["base_ac"] != 0)),
            "getter_setter_hits": 0,
            "sha256": sha256_bytes(srv["base_ac"].tobytes()),
        },
        "base_plus_0x00_non_clubxml_tags": {
            "tag4_COMPETITION_BONUS_INFO_CCBc": {"items": int(srv["b0_tags"][4]), "rows": int(srv["b0_tag_rows"][4])},
            "tag9_STARTING_PLAYER_RECORD_INFO_NA_NG": {"items": int(srv["b0_tags"][9]), "rows": int(srv["b0_tag_rows"][9])},
            "tag16_CLUB_CUP_POINTS": {"items": int(srv["b0_tags"][16]), "rows": int(srv["b0_tag_rows"][16])},
            "tag37_EPPP_APPEARANCE_MONEY_INFO": {"items": int(srv["b0_tags"][37]), "rows": int(srv["b0_tag_rows"][37])},
        },
    }

    # Known-club L2 anchor witnesses
    l2_anchors = []
    for ord_id, label in [
        (460, "Liverpool"),
        (463, "Manchester City"),
        (464, "Manchester United"),
        (415, "Chelsea"),
        (1297, "Real Madrid"),
        (623, "Bayern Munich"),
        (1282, "Barcelona"),
        (586, "Paris Saint-Germain"),
    ]:
        l2_anchors.append({
            "label": label,
            "row_ordinal": ord_id,
            "club_uid": club_ord_to_uid[ord_id],
            "Cyfn": int(srv["d8"][ord_id]),
            "Ctlv": int(srv["Ctlv"][ord_id]),
            "Cmle": int(srv["Cmle"][ord_id]),
            "Cyim": int(srv["Cyim"][ord_id]),
            "Cyfb": int(srv["Cyfb"][ord_id]),
            "Cytv": int(srv["Cytv"][ord_id]),
            "Crcb": int(srv["Crcb"][ord_id]),
            "Cown": int(srv["Cown"][ord_id]),
            "Csly": int(srv["Csly"][ord_id]),
            "Catd": int(srv["Catd"][ord_id]),
            "Cmna": int(srv["Cmna"][ord_id]),
            "Cmxa": int(srv["Cmxa"][ord_id]),
            "TCht": srv["tcht_map"].get(ord_id, ""),
            "Cuf1_to_Cf10": [round(float(x), 3) for x in srv["cuf_f32"][ord_id].tolist()] if srv["cuf_has"][ord_id] else None,
        })

    # --- Build incremental field_map.json (35 L3 + 40 held + negative_not_extra3) ---
    def make_prior(idx: int) -> dict[str, Any]:
        p57 = t57_by_idx.get(idx, {})
        p63 = t63_by_idx.get(idx, {})
        return {
            "id": f"E97/club.xml#club/{idx:03d}",
            "t57_grade": p57.get("grade"),
            "t63_grade": p63.get("grade"),
            "t63_reason": p63.get("reason") or (p63.get("first_counterexample") or {}).get("reason") if isinstance(p63.get("first_counterexample"), dict) else p63.get("reason"),
        }

    def add_field(
        entries: list[dict[str, Any]],
        *,
        xml_index: int,
        grade: str,
        wire_scope: str,
        obj_path: str,
        wire_type: str,
        getter_fo: int,
        setter_fo: int | None,
        reader_fo: int,
        domain: dict[str, Any],
        ctor_default: Any = None,
        hold_reason: str | None = None,
        first_counterexample: dict[str, Any] | None = None,
        extra_witnesses: dict[str, Any] | None = None,
        subfields: list[dict[str, Any]] | None = None,
    ) -> None:
        if xml_index in T71_L3_INDICES:
            raise RuntimeError(f"Attempted to re-grade t71 L3 index {xml_index}")
        fld = club_fields[xml_index]
        code = fld["field"]
        # Triple-gate safety assertion for L3
        if grade == "L3":
            if occ_counts[code] != 1:
                raise RuntimeError(f"L3 Gate 1 fail (non-unique XML occurrence): {code}")
            if setter_fo is None:
                raise RuntimeError(f"L3 dual-chain missing setter: {code}")
            if fld["type"] in ("enum", "multiple_enum") and not fld.get("enum_ref"):
                raise RuntimeError(f"L3 missing scoped enum_ref: {code}")
            if domain.get("violations", 0) != 0:
                raise RuntimeError(f"L3 non-zero violations on {code}: {domain.get('violations')}")
        elif grade == "held":
            if not hold_reason or not first_counterexample:
                raise RuntimeError(f"held field missing hold_reason or first_counterexample: {code}[{xml_index}]")

        rec: dict[str, Any] = {
            "id": f"E97/club.xml#club/{xml_index:03d}",
            "xml_index": xml_index,
            "code": code,
            "schema_name": fld.get("name"),
            "schema_type": fld.get("type"),
            "schema_min": fld.get("min_value"),
            "schema_max": fld.get("max_value"),
            "enum_ref": fld.get("enum_ref"),
            "xml_occurrence_count": occ_counts[code],
            "prior": make_prior(xml_index),
            "grade": grade,
            "wire_scope": wire_scope,
            "object_path": obj_path,
            "wire_type": wire_type,
            "ctor_default": ctor_default,
            "static_chain": {
                "getter": pei.insn_at(getter_fo, 2),
                "setter": pei.insn_at(setter_fo, 2) if setter_fo is not None else None,
                "reader": pei.insn_at(reader_fo, 2),
            },
            "domain": domain,
        }
        if extra_witnesses:
            rec["static_chain"]["extra"] = extra_witnesses
        if subfields is not None:
            rec["subfields"] = subfields
        if hold_reason:
            rec["hold_reason"] = hold_reason
        if first_counterexample:
            rec["first_counterexample"] = first_counterexample
        entries.append(rec)

    fm_entries: list[dict[str, Any]] = []

    # --- 1. CLUB+0x100 direct scalars (6 L3 + 4 held) ---
    for idx, code, off, gfo, sfo, cdef in [
        (64, "Ctlv", "+0x120", 0xE8A998, 0xE581D1, 0),
        (30, "Cmle", "+0x121", 0xE8C525, 0xE5830F, 10),
        (68, "Cyim", "+0x126", 0xE8B983, 0xE58023, 0),
        (66, "Cyfb", "+0x12b", 0xE8B10C, 0xE58244, 0),
        (65, "Cytv", "+0x12c", 0xE8C3F9, 0xE58030, 10),
        (67, "Crcb", "+0x12d", 0xE8BD74, 0xE58202, 10),
    ]:
        add_field(
            fm_entries, xml_index=idx, grade="L3", wire_scope="server_only",
            obj_path=f"CLUB+0x100 -> {off}", wire_type="i8",
            getter_fo=gfo, setter_fo=sfo, reader_fo=0xE5D210,
            domain=scalar_domains[code], ctor_default=cdef,
        )

    # Csth (held: 3 rows have -1 < min_value=0)
    add_field(
        fm_entries, xml_index=115, grade="held", wire_scope="server_only",
        obj_path="CLUB+0x100 -> +0xc0", wire_type="i32",
        getter_fo=0xE8CEF0, setter_fo=0xE581B7, reader_fo=0xE5D210,
        domain=scalar_domains["Csth"], ctor_default=-1,
        hold_reason="CLUB_GET 0xe8cef0 returns raw i32 without clamp/suppression; 3/84,259 rows equal -1 (0xffffffff) < frozen min_value=0",
        first_counterexample={
            "row_ordinal": scalar_domains["Csth"]["first_counterexample"]["row_ordinal"],
            "club_uid": club_ord_to_uid[scalar_domains["Csth"]["first_counterexample"]["row_ordinal"]],
            "raw_value": -1,
            "raw_hex": "0xffffffff",
            "schema_min": 0,
        },
    )

    # Unscoped enums on CLUB+0x100 (held: no scoped enum_ref, matching t63 Cpfa/Chsd & t79 PLgn)
    for idx, code, off, gfo, sfo, cdef in [
        (34, "CScP", "+0x127", 0xE8ADF3, 0xE580FF, 0),
        (47, "Cown", "+0x129", 0xE8B7F0, 0xE84309, 0),
        (55, "Chti", "+0x12a", 0xE8AD6A, 0xE83A8C, 1),
    ]:
        add_field(
            fm_entries, xml_index=idx, grade="held", wire_scope="server_only",
            obj_path=f"CLUB+0x100 -> {off}", wire_type="i8",
            getter_fo=gfo, setter_fo=sfo, reader_fo=0xE5D210,
            domain=scalar_domains[code], ctor_default=cdef,
            hold_reason="no scoped enum_ref in frozen master.json (preserves t63 Cpfa/Chsd & t79 PLgn discipline)",
            first_counterexample={
                "kind": "schema_gate",
                "xml_index": idx,
                "enum_ref": None,
                "observed_min": scalar_domains[code]["min"],
                "observed_max": scalar_domains[code]["max"],
                "observed_distinct": scalar_domains[code]["distinct"],
            },
        )

    # --- 2. Election sub-object CLUB+0x100 -> +0x78 (5 L3 + 1 held; Cebd already L3 in t71) ---
    for idx, code, off, gfo, sfo in [
        (50, "Cetl", "+0x12", 0xE970A6, 0x3AEB82F),
        (51, "Cmtm", "+0x13", 0xE970B2, 0x3AEB83B),
        (52, "Cect", "+0x14", 0xE9702F, 0x3AEB7F8),
        (53, "Cemn", "+0x15", 0xE9703B, 0x3AEB804),
        (54, "Cemx", "+0x16", 0xE96FA5, 0x3AEB7AD),
    ]:
        add_field(
            fm_entries, xml_index=idx, grade="L3", wire_scope="server_only_conditional_flag_11963",
            obj_path=f"CLUB+0x100 -> +0x78 -> {off}", wire_type="i8",
            getter_fo=gfo, setter_fo=sfo, reader_fo=0x4342940,
            domain=scalar_domains[code], ctor_default=None,
            extra_witnesses={"election_alloc_gate": pei.insn_at(0xE5DC38, 2)},
        )

    add_field(
        fm_entries, xml_index=49, grade="held", wire_scope="server_only_conditional_flag_11963",
        obj_path="CLUB+0x100 -> +0x78 -> +0x10", wire_type="i16_bitmask",
        getter_fo=0xE96FB1, setter_fo=0x3AEB7B9, reader_fo=0x4342940,
        domain=scalar_domains["Cepr"], ctor_default=None,
        hold_reason="multiple_enum with no scoped enum_ref in frozen master.json",
        first_counterexample={
            "kind": "schema_gate",
            "xml_index": 49,
            "enum_ref": None,
            "observed_min": scalar_domains["Cepr"]["min"],
            "observed_max": scalar_domains["Cepr"]["max"],
            "observed_distinct": scalar_domains["Cepr"]["distinct"],
        },
    )

    # --- 3. Supporter profile CLUB+0x100 -> +0xf8 (6 L3) ---
    for idx, code, off, gfo, sfo in [
        (149, "Csly", "+0x08", 0x15202A6, 0x43419CA),
        (150, "Csps", "+0x09", 0x15201A2, 0x43419EB),
        (151, "Cspt", "+0x0a", 0x1520311, 0x43419F3),
        (152, "Csaf", "+0x0b", 0x152029A, 0x43419C2),
        (153, "Cste", "+0x0c", 0x152031D, 0x43419FB),
        (154, "Cspe", "+0x0d", 0x15201AE, 0x43419D2),
    ]:
        add_field(
            fm_entries, xml_index=idx, grade="L3", wire_scope="server_only",
            obj_path=f"CLUB+0x100 -> +0xf8 -> {off}", wire_type="i8",
            getter_fo=gfo, setter_fo=sfo, reader_fo=0x4340450,
            domain=scalar_domains[code], ctor_default=10,
            extra_witnesses={"club_get_forward": pei.insn_at(0xE8C094, 2), "club_extra_set_forward": pei.insn_at(0xE57FEC, 2)},
        )

    # --- 4. UEFA coeff ring buffer CLUB+0x100 -> +0x48 (10 L3) ---
    for k, code in enumerate(cuf_codes):
        idx = 133 + k
        if k < 9:
            gfo = int(cuf_get_jt[k]["target_fo"], 16)
            sfo = int(cuf_set_jt[k]["target_fo"], 16)
            ex_w = {"get_jt_cell": cuf_get_jt[k], "set_jt_cell": cuf_set_jt[k]}
        else:
            gfo = 0xE8C8FB
            sfo = 0xE842D0
            ex_w = {"set_arm": pei.insn_at(0xE8458E, 2)}
        add_field(
            fm_entries, xml_index=idx, grade="L3", wire_scope="server_only_conditional_flag_569",
            obj_path=f"CLUB+0x100 -> +0x48 -> ring[(head+{k})%10] / 1000.0", wire_type="i32_milli_ring_to_f32",
            getter_fo=gfo, setter_fo=sfo, reader_fo=0x39AA1F0,
            domain=cuf_domains[code], ctor_default=0.0,
            extra_witnesses=ex_w,
        )

    # --- 5. CLUB+0xb0 common tail (1 L3 + 15 held) ---
    add_field(
        fm_entries, xml_index=12, grade="L3", wire_scope="client+server",
        obj_path="CLUB+0xb0 -> +0x98", wire_type="u32_len_utf8",
        getter_fo=0x11F0831, setter_fo=0x11CFA3E, reader_fo=0x11D3200,
        domain=tcht_domain, ctor_default="",
        extra_witnesses={"tc_get2_copy_arm": pei.insn_at(0x11F1FD0, 3)},
    )
    add_field(
        fm_entries, xml_index=11, grade="held", wire_scope="conditional_wire_0_populated",
        obj_path="CLUB+0xb0 -> +0x90 (gated by CLUB+0xba != 0)", wire_type="u32_len_utf8",
        getter_fo=0x11F1463, setter_fo=0x11CFA4A, reader_fo=0x11D3200,
        domain=tcnn_domain, ctor_default="",
        hold_reason="gated on CLUB+0xba != 0, which is 0 on all 84,259/84,259 rows in both client and server (0 wire observations)",
        first_counterexample={"kind": "zero_populated", "populated_rows": 0, "total_rows": 84259},
    )
    # Duplicate ttcl [24, 76] & tbcl [25, 77]
    for idx, code, off, gfo, sfo, dom in [
        (24, "ttcl", "+0xa0", 0x11F0C4D, 0x11F4636, ttcl_domain),
        (76, "ttcl", "+0xa0", 0x11F0C4D, 0x11F4636, ttcl_domain),
        (25, "tbcl", "+0xa8", 0x11F171D, 0x11F4620, tbcl_domain),
        (77, "tbcl", "+0xa8", 0x11F171D, 0x11F4620, tbcl_domain),
    ]:
        add_field(
            fm_entries, xml_index=idx, grade="held", wire_scope="client+server",
            obj_path=f"CLUB+0xb0 -> {off}", wire_type="u32_rev_rgba",
            getter_fo=gfo, setter_fo=sfo, reader_fo=0x11D3200,
            domain=dom, ctor_default=0,
            hold_reason=f"fails Gate 1 (duplicate occurrence of {code} in frozen club.xml: 2 occurrences) and 6,586/84,259 rows are 0x00000000 falling back to base+0x78 kits",
            first_counterexample={
                "kind": "duplicate_xml_occurrence_and_zero_fallback",
                "duplicate_indices": [24, 76] if code == "ttcl" else [25, 77],
                "zero_fallback_rows": dom["zero_fallback_rows"],
                "first_zero_row_ordinal": int(np.argmax((srv["base_a0"] if code == "ttcl" else srv["base_a8"]) == 0)),
            },
        )

    # Derived read-only 10 colour getters (1scl..3tbc)
    for idx, code, gfo in [
        (70, "1scl", 0xE8BEBB), (71, "1sbc", 0xE8BEAF),
        (72, "2scl", 0xE8C80A), (73, "2sbc", 0xE89C6C),
        (74, "3scl", 0xE8BF90), (75, "3sbc", 0xE8BF84),
        (78, "2tcl", 0xE8B27A), (79, "2tbc", 0xE8C816),
        (80, "3tcl", 0xE8AC73), (81, "3tbc", 0xE8AC67),
    ]:
        add_field(
            fm_entries, xml_index=idx, grade="held", wire_scope="derived_read_only_from_base78",
            obj_path="derived from CLUB+0xb0 -> +0x78 (parent-club 0x3ae7420 + kit search 0x11dc460 + contrast 0x150d300)",
            wire_type="computed_colour",
            getter_fo=gfo, setter_fo=None, reader_fo=0x11D3200,
            domain={"kit_pool_items": int(srv["kit_total"]), "setter_exists": False},
            hold_reason="read-only derived colour getter (no setter in CLUB_SET/TC_SET2); computes from parent club + base+0x78 kit search + contrast/palette fallback",
            first_counterexample={"kind": "derived_read_only_no_setter", "code": code, "getter_fo": f"0x{gfo:x}"},
        )

    # --- 6. CLUB+0xb0 server attendance (3 L3) & formations (4 held) ---
    for idx, code, off, gfo, sfo in [
        (61, "Catd", "+0x68", 0x11F13A6, 0x11CFA06),
        (62, "Cmna", "+0x6c", 0x11F0E42, 0x11CFA1E),
        (63, "Cmxa", "+0x70", 0x11F0E4E, 0x11CF976),
    ]:
        add_field(
            fm_entries, xml_index=idx, grade="L3", wire_scope="server_only",
            obj_path=f"CLUB+0xb0 -> {off}", wire_type="i32",
            getter_fo=gfo, setter_fo=sfo, reader_fo=0x11D3200,
            domain=scalar_domains[code], ctor_default=10000,
        )

    for idx, code, off, gfo, sfo, eref in [
        (145, "Cpfr", "+0x74", 0xE8BB09, 0x11CF98E, "pfms"),
        (146, "C2pf", "+0x75", 0xE8B848, 0x11CFB55, "sfms"),
        (147, "Cdfo", "+0x76", 0xE8B164, 0x11CFA12, "dfms"),
        (148, "Cafo", "+0x77", 0xE8B4E7, 0x11CFB7D, "afms"),
    ]:
        fcx = scalar_domains[code]["first_counterexample"]
        add_field(
            fm_entries, xml_index=idx, grade="held", wire_scope="server_only",
            obj_path=f"CLUB+0xb0 -> {off}", wire_type="i8_enum",
            getter_fo=gfo, setter_fo=sfo, reader_fo=0x11D3200,
            domain=scalar_domains[code], ctor_default=0,
            hold_reason=f"{scalar_domains[code]['violations']} live non-zero rows outside frozen enums['{eref}'] (0 suppressed by getter)",
            first_counterexample={
                "row_ordinal": fcx["row_ordinal"],
                "club_uid": club_ord_to_uid[fcx["row_ordinal"]],
                "raw_value": fcx["raw_value"],
                "enum_ref": eref,
                "bad_distinct_values": fcx["bad_distinct_values"],
            },
        )

    # --- 7. List & polymorphic vectors (4 L3 + 11 held + 4 preserved t63 held) ---
    # 4 CLEAN L3 lists: Cbbl, Csoc, pcpt, CPsL
    add_field(
        fm_entries, xml_index=119, grade="L3", wire_scope="server_only",
        obj_path="CLUB+0xb0 -> +0x00 polymorphic tag 7 (PLAYER_BUY_BACK_INFO, 24B)",
        wire_type="poly_tag7_24B",
        getter_fo=0xE8AEE9, setter_fo=0xE5829D, reader_fo=0x42C66F0,
        domain=cbbl_domain,
        extra_witnesses={"item_getter": pei.insn_at(0x42C7150, 3), "vtable": pei.vtable_slots(0x18B8608, 4)},
        subfields=[
            {"code": "play", "mem_off": "+0x10", "wire_off": 0, "type": "8B_person_uid_pair"},
            {"code": "cash", "mem_off": "+0x18", "wire_off": 8, "type": "i32_cash"},
            {"code": "club", "mem_off": "+0x20", "wire_off": 12, "type": "i32_club_ordinal_ref:table_3"},
        ],
    )
    add_field(
        fm_entries, xml_index=120, grade="L3", wire_scope="server_only",
        obj_path="CLUB+0xb0 -> +0x00 polymorphic tag 5 (NEXT_SALE_PERCENTAGE_INFO, 24B)",
        wire_type="poly_tag5_24B",
        getter_fo=0xE8B1C0, setter_fo=0xE5835F, reader_fo=0x42D2710,
        domain=csoc_domain,
        extra_witnesses={"item_getter": pei.insn_at(0x42CF700, 3), "vtable": pei.vtable_slots(0x18B8768, 4)},
        subfields=[
            {"code": "play", "mem_off": "+0x08", "wire_off": 0, "type": "8B_person_uid_pair"},
            {"code": "club", "mem_off": "+0x10", "wire_off": 8, "type": "i32_club_ordinal_ref:table_3"},
            {"code": "perc", "mem_off": "+0x21", "wire_off": 12, "type": "i8_percent_0_100"},
        ],
    )
    add_field(
        fm_entries, xml_index=196, grade="L3", wire_scope="server_only",
        obj_path="CLUB+0xb0 -> +0x00 polymorphic tag 38 (TESTIMONIAL_INFO, varlen)",
        wire_type="poly_tag38_varlen",
        getter_fo=0xE8B2D8, setter_fo=0xE583AB, reader_fo=0x14DA470,
        domain=pcpt_domain,
        extra_witnesses={"item_getter": pei.insn_at(0x42F5660, 3), "vtable": pei.vtable_slots(0x18B9428, 4)},
        subfields=[
            {"code": "PtPl", "mem_off": "+0x30", "wire_off": 5, "type": "i32_person_uid"},
            {"code": "PtLy", "mem_off": "+0x38", "wire_off": 13, "type": "u32_date4"},
        ],
    )
    add_field(
        fm_entries, xml_index=197, grade="L3", wire_scope="server_only",
        obj_path="CLUB+0x100 -> +0x68 (u16 cnt x (tag=2 + 10B))",
        wire_type="vec_tag2_11B",
        getter_fo=0xE8B5EE, setter_fo=0xE83303, reader_fo=0xE5D210,
        domain=cpsl_domain,
        extra_witnesses={"item_getter": pei.insn_at(0x1524AF0, 4), "list_setter": pei.insn_at(0xEAC360, 3)},
        subfields=[
            {"code": "per1", "mem_off": "+0x00", "wire_off": 1, "type": "i32_person_uid"},
            {"code": "per2", "mem_off": "+0x04", "wire_off": 5, "type": "i32_person_uid"},
        ],
    )

    # 5 held list fields with subfield violations / missing enum_ref
    add_field(
        fm_entries, xml_index=104, grade="held", wire_scope="server_only",
        obj_path="CLUB+0x100 -> +0x28 (i8 cnt x 22B)", wire_type="vec_22B",
        getter_fo=0xE89E67, setter_fo=0xE83611, reader_fo=0x3AAF9E0,
        domain=cscm_domain,
        extra_witnesses={"item_getter": pei.insn_at(0xEAF720, 3), "list_setter": pei.insn_at(0xEAEDB0, 3)},
        subfields=[
            {"code": "stco", "mem_off": "+0x00", "wire_off": 1, "type": "8B_comp_uid_pair:table_25"},
            {"code": "stnm", "mem_off": "+0x08", "wire_off": 9, "type": "i8_matches_0_200"},
            {"code": "slsn", "mem_off": "+0x0c", "wire_off": 10, "type": "8B_stage_name_uid_pair:table_23"},
        ],
        hold_reason="118/15,360 items have slsn=(0,0) which 0xfe68ca passes through (only <0 is nulled) and does not exist in table_23 STAGE_NAME UIDs (min UID=1)",
        first_counterexample=cscm_domain["first_counterexample"],
    )
    add_field(
        fm_entries, xml_index=86, grade="held", wire_scope="server_only",
        obj_path="CLUB+0xb0 -> +0x18 (i16 cnt x 20B)", wire_type="vec_20B",
        getter_fo=0xE8F522, setter_fo=0xE5836C, reader_fo=0x3EA5150,
        domain=cspb_domain,
        extra_witnesses={"item_getter": pei.insn_at(0x11F8990, 3)},
        subfields=[
            {"code": "cmid", "mem_off": "+0x04", "wire_off": 1, "type": "8B_comp_uid_pair:table_25"},
            {"code": "venu", "mem_off": "+0x00", "wire_off": 9, "type": "i8_enum(enum_ref=None)"},
            {"code": "matc", "mem_off": "+0x01", "wire_off": 10, "type": "i8_matches(-1_suppressed)"},
            {"code": "type", "mem_off": "+0x02", "wire_off": 11, "type": "i8_enum(enum_ref=None)"},
            {"code": "stdt", "mem_off": "+0x0c", "wire_off": 12, "type": "u32_date4"},
            {"code": "endt", "mem_off": "+0x10", "wire_off": 16, "type": "u32_date4"},
        ],
        hold_reason="subfields type and venu have no scoped enum_ref in frozen master.json (cmid/matc/stdt/endt have 0 violations across all 46 items)",
        first_counterexample={"kind": "schema_gate_subfield", "subfields": ["type", "venu"], "enum_ref": None, "observed_type": cspb_domain["type_hist"], "observed_venu": cspb_domain["venu_hist"]},
    )
    add_field(
        fm_entries, xml_index=199, grade="held", wire_scope="server_only",
        obj_path="CLUB+0xb0 -> +0x30 (i8 cnt x 6B)", wire_type="vec_6B",
        getter_fo=0xE8C37D, setter_fo=0x11CFA8D, reader_fo=0x11D45F0,
        domain=cren_domain,
        extra_witnesses={"item_getter": pei.insn_at(0x3EC49F0, 3)},
        subfields=[
            {"code": "rsnn", "mem_off": "+0x08", "wire_off": 0, "type": "i8_squad_num_1_99"},
            {"code": "rsnp", "mem_off": "+0x00", "wire_off": 1, "type": "i32_person_ordinal_or_minus1"},
            {"code": "rsnr", "mem_off": "+0x09", "wire_off": 5, "type": "i8_enum(enum_ref=None)"},
        ],
        hold_reason="subfield rsnr has no scoped enum_ref in frozen master.json (rsnn 1..99 and rsnp have 0 violations across all 1,202 items)",
        first_counterexample={"kind": "schema_gate_subfield", "subfield": "rsnr", "enum_ref": None, "observed_rsnr": cren_domain["rsnr_hist"]},
    )
    add_field(
        fm_entries, xml_index=121, grade="held", wire_scope="server_only",
        obj_path="CLUB+0xb0 -> +0x00 polymorphic tag 6 (APPEARANCE_MONEY_INFO, 19B)",
        wire_type="poly_tag6_19B",
        getter_fo=0xE8B4B1, setter_fo=0xE580C3, reader_fo=0x42D6A10,
        domain=camc_domain,
        extra_witnesses={"item_getter": pei.insn_at(0x42D6680, 3), "vtable": pei.vtable_slots(0x18B8818, 4)},
        subfields=[
            {"code": "play", "mem_off": "+0x08", "wire_off": 0, "type": "8B_person_uid_pair"},
            {"code": "club", "mem_off": "+0x10", "wire_off": 8, "type": "i32_club_ordinal_ref:table_3"},
            {"code": "cash", "mem_off": "+0x18", "wire_off": 12, "type": "i32_cash"},
            {"code": "apps", "mem_off": "+0x1c", "wire_off": 16, "type": "i8_1_100"},
            {"code": "apfr", "mem_off": "+0x1d", "wire_off": 17, "type": "i8_1_100"},
            {"code": "type", "mem_off": "+0x1e", "wire_off": 18, "type": "i8_enum(enum_ref=None)"},
        ],
        hold_reason="973/1,601 items have apfr=0 < frozen min_value=1 (VTAG6_GET 0x42d6759 does not suppress 0) and subfield type lacks scoped enum_ref",
        first_counterexample=camc_domain["first_counterexample"],
    )
    add_field(
        fm_entries, xml_index=201, grade="held", wire_scope="server_only",
        obj_path="CLUB+0xb0 -> +0x48 (flag + ver=2 + cnt x (iv=3 + 10B))",
        wire_type="vec_tcrs_12B",
        getter_fo=0x11F15AB, setter_fo=0x11CFA56, reader_fo=0x4387AB0,
        domain=tcrs_domain,
        extra_witnesses={"item_getter": pei.insn_at(0x155A320, 3), "sub_reader": pei.insn_at(0x155C120, 3)},
        subfields=[
            {"code": "PUnP", "mem_off": "+0x00", "wire_off": 2, "type": "i32_person_uid_or_ord_by_b9"},
            {"code": "PUnI", "mem_off": "+0x04", "wire_off": 6, "type": "u8_enum(enum_ref=None)"},
            {"code": "PUnT", "mem_off": "+0x05", "wire_off": 7, "type": "i8_enum(enum_ref=None)"},
            {"code": "PUnJ", "mem_off": "+0x06", "wire_off": 8, "type": "u16_enum:ftjn"},
        ],
        hold_reason="2,709/23,027 items violate frozen enums['ftjn'] on PUnJ, and PUnI/PUnT lack scoped enum_ref",
        first_counterexample=tcrs_domain["first_counterexample"],
    )

    # 6 kit list containers Tko1..3 / Tkg1..3 (held: no frozen list_item_fields for 27B TEAM_KIT_FOR_YEAR)
    for idx, code, gfo, sfo, ktype, outf in [
        (178, "Tko1", 0x11F06CC, 0x11CFACE, 0, 1),
        (179, "Tkg1", 0x11F0706, 0x11CF9CE, 0, 0),
        (180, "Tko2", 0x11F0730, 0x11CFAC2, 1, 1),
        (181, "Tkg2", 0x11F06C4, 0x11CF9DA, 1, 0),
        (182, "Tko3", 0x11F073C, 0x11CFAB6, 2, 1),
        (183, "Tkg3", 0x11F06D4, 0x11CF9E6, 2, 0),
    ]:
        bstat = kit_domain["buckets"][code]
        add_field(
            fm_entries, xml_index=idx, grade="held", wire_scope="client+server",
            obj_path=f"CLUB+0xb0 -> +0x78 filtered by (kit_type@+0x22=={ktype}, outfield@+0x25=={outf})",
            wire_type="vec_kit_27B",
            getter_fo=gfo, setter_fo=sfo, reader_fo=0x11D3200,
            domain={
                "scope": "client+server",
                "client_eq_server": True,
                "items": bstat["items"],
                "rows": bstat["rows"],
                "kit_type_b22": ktype,
                "outfield_b25": outf,
                "all_405204_items_partitioned": len(kit_unmapped_buckets) == 0,
            },
            extra_witnesses={"filter_helper": pei.insn_at(0x3EC2FE9, 5)},
            hold_reason="container + exact (kit_type, outfield) partition 100% dual-chain & dual-archive proven, but frozen club.xml omits list_item_fields for inner 27B TEAM_KIT_FOR_YEAR struct",
            first_counterexample={
                "kind": "no_frozen_list_item_fields",
                "xml_index": idx,
                "code": code,
                "inner_item_bytes": 27,
            },
        )

    # 4 preserved t63 held: CssT..E (poly tag 35 = 0x23, 0 items / 0 rows in DB)
    for idx, code in [(109, "CssT"), (110, "CssP"), (111, "CssS"), (112, "CssE")]:
        add_field(
            fm_entries, xml_index=idx, grade="held", wire_scope="server_only_poly_tag35_0_populated",
            obj_path="CLUB+0xb0 -> +0x00 polymorphic tag 35 (0x23) — 0 items across 84,259 rows",
            wire_type="poly_tag35_unobserved",
            getter_fo=0xE89A00, setter_fo=None, reader_fo=0x11D3200,
            domain={"observed_items": 0, "observed_rows": 0, "preserved_from": "t63/E106"},
            hold_reason="preserved t63 held verbatim; full-archive scan confirms 0/84,259 rows contain polymorphic tag 35 (0x23) in table_extra_3.dat",
            first_counterexample={"kind": "preserved_t63_held_zero_observed", "tag": 35, "observed_items": 0, "t63_id": f"E97/club.xml#club/{idx:03d}"},
        )

    # Sort entries by xml_index for deterministic output
    fm_entries.sort(key=lambda e: e["xml_index"])

    # Negative / non-extra_3 registry
    other_negatives = [
        (8, "Csxn", "CLUB+0x100 -> +0x00 runtime string zeroed in ctor 0x3aaba20; NOT read from table_extra_3.dat wire", 0xE581C4),
        (9, "Cl3n", "CLUB+0x100 -> +0x08 runtime string zeroed in ctor 0x3aaba20; NOT read from table_extra_3.dat wire", 0xE57E9F),
        (10, "Ca3n", "CLUB+0x100 -> +0x10 runtime string zeroed in ctor 0x3aaba20; NOT read from table_extra_3.dat wire", 0xE580B6),
        (177, "Crkt", "Action/command setter (CLUB_EXTRA_SET 0xe5820f -> 0xe586a0 & TC_EXTRA_SET 0x11cfa99) that randomizes kits; NO getter, NOT a wire boolean", 0xE5820F),
        (129, "C1sq", "CLUB_GET 0xe8d9f0 -> 0xe8f34a -> 0x11f41d0 forwards Tsqi to first TEAM; NOT extra_3", 0xE8D9F0),
        (432, "Cmls", "Preserved t63 held verbatim: 0x3ebf730 reads COMP+0xb0 ([team+0x50]+0xb0), NOT CLUB+0xb0", 0x3EBF730),
        (117, "Cdbt", "0x4343880 scans separate global DATABASE_TABLE, NOT table_extra_3.dat", 0xE5815E),
        (118, "Cffp", "0x4343880 scans separate global DATABASE_TABLE, NOT table_extra_3.dat", 0xE5816B),
        (329, "Clhs", "0x4344a40 scans separate global DATABASE_TABLE (skipped_separate_member in t57), NOT extra_3", 0xE57EAC),
        (330, "CAmb", "0x1449360 scans separate global DATABASE_TABLE, NOT extra_3", 0xE57F80),
        (122, "Cmti", "0x1523b10 scans separate global DATABASE_TABLE, NOT extra_3", 0xE5831C),
        (123, "Cwcl", "0x1523f00 scans separate global DATABASE_TABLE, NOT extra_3", 0xE58237),
        (103, "Coin", "0x3b14af0 reads main CLUB+0x130, NOT extra_3", 0xE581F5),
        (85, "Calt", "0x3ecc060 reads main CLUB+0xa8, NOT extra_3", 0x3ECC060),
    ]
    negative_entries = []
    for idx in range(211, 328):
        fld = club_fields[idx]
        negative_entries.append({
            "id": f"E97/club.xml#club/{idx:03d}",
            "xml_index": idx,
            "code": fld["field"],
            "schema_name": fld.get("name"),
            "grade": "negative_not_extra3",
            "prior": make_prior(idx),
            "target_table": "server_db/table_45.dat (DATABASE_TABLE<STARTING_RECORD>, type 0x2d=45)",
            "reason": "Routes via TC_GET2 (0x11f2a76) / CLUB_GET (0xe8f1d9) -> 0x11e8af0 -> TC_RECORD_GET 0x3ebad50 on global VA 0x141b60190 (table_45.dat); 0 bytes in table_extra_3.dat",
        })
    for idx, code, reason, wfo in other_negatives:
        fld = club_fields[idx]
        negative_entries.append({
            "id": f"E97/club.xml#club/{idx:03d}",
            "xml_index": idx,
            "code": code,
            "schema_name": fld.get("name"),
            "grade": "held" if idx == 432 else "negative_not_extra3",
            "prior": make_prior(idx),
            "reason": reason,
            "witness": pei.insn_at(wfo, 2),
        })

    # Complete wire layout ledger (100% byte accounting for CLUB+0x100 and CLUB+0xb0)
    wire_ledger = {
        "CLUB_plus_0x100_CLUB_IN_GAME_DATA": {
            "object_size": "0x130",
            "reader_fo": "0xe5d210",
            "ctor_fo": "0x3aaba20",
            "fixup_fo": "0x3aae490",
            "writer_fo": "0xe5f3d0",
            "server_prefix_sequence": [
                {"order": 1, "wire_bytes": 1, "mem_off": "+0x120", "type": "i8", "ctor_default": 0, "binding": "Ctlv [64] (L3)"},
                {"order": 2, "wire_bytes": 1, "mem_off": "+0x121", "type": "i8", "ctor_default": 10, "binding": "Cmle [30] (L3)"},
                {"order": 3, "wire_bytes": 1, "mem_off": "+0x122", "type": "i8", "ctor_default": 0, "binding": "internal (all 0)"},
                {"order": 4, "wire_bytes": "2 + 4*cnt", "mem_off": "+0x18", "type": "u16_cnt_vec", "binding": "internal (cnt=0 all 84,259)"},
                {"order": 5, "wire_bytes": 5, "mem_off": "+0xda", "type": "5B_bitfield_via_0x4348ef0", "binding": "internal (0 getter/setter hits)"},
                {"order": 6, "wire_bytes": 1, "mem_off": "+0x123", "type": "i8", "binding": "internal (0..20, 1,970 nz, 0 getter/setter hits)"},
                {"order": 7, "wire_bytes": 4, "mem_off": "+0xc0", "type": "i32", "ctor_default": -1, "binding": "Csth [115] (held: 3 rows=-1 < 0)"},
                {"order": 8, "wire_bytes": 24, "mem_off": "+0x88[0..5]", "type": "6x_date4", "binding": "internal (100% sentinel 0x076c0001)"},
                {"order": 9, "wire_bytes": "1 + 24*flag", "mem_off": "+0xa0[0..5]", "type": "flag(all 1) + 6x_date4", "binding": "internal (100% sentinel 0x076c0001)"},
                {"order": 10, "wire_bytes": 15, "mem_off": "+0xde/+0xb8/+0x125/+0x84/+0x80", "type": "u16+date4+i8+date4+date4", "binding": "internal (all 0 / sentinel)"},
                {"order": 11, "wire_bytes": "1 + 19*flag", "mem_off": "+0x78", "type": "election_19B (11,963 rows)", "binding": "Cebd [48] (t71 L3), Cetl/Cmtm/Cect/Cemn/Cemx (5 L3), Cepr (held); +0x00 club_ord==row_ord, +0x0c sentinel"},
                {"order": 12, "wire_bytes": 5, "mem_off": "+0x126..+0x12a", "type": "5x_i8", "binding": "Cyim [68] (L3), CScP [34] (held), +0x128 internal(-1), Cown [47] (held), Chti [55] (held)"},
                {"order": 13, "wire_bytes": 21, "mem_off": "+0xf8", "type": "ver(3) + 20B supporter profile 1", "binding": "Csly/Csps/Cspt/Csaf/Cste/Cspe [149..154] (6 L3); CsSF/CsSS/CsST(-1) & Cfph..Cfpc(0) internal"},
                {"order": 14, "wire_bytes": 21, "mem_off": "+0x10c", "type": "ver(3) + 20B supporter profile 2", "binding": "internal (100% ctor default across 84,259 rows)"},
                {"order": 15, "wire_bytes": 8, "mem_off": "+0xe0", "type": "tag(2) + 7B cnst block A", "ctor_default": 6, "binding": "t71 L3 (7 cnst fields, excluded from t82)"},
                {"order": 16, "wire_bytes": 16, "mem_off": "+0xe7", "type": "tag(3) + 15B cnst block B", "ctor_default": 6, "binding": "t71 L3 (15 cnst fields, excluded from t82)"},
                {"order": 17, "wire_bytes": 25, "mem_off": "+bc/+c4/+c8/+12b..12f/+d0/+d4", "type": "date4+2i32+5i8+2i32", "binding": "Cyfb/Cytv/Crcb [66,65,67] (3 L3); +bc(sent)/+c4(0)/+c8 CMwg(0)/+12e(-2)/+12f Cels(-1)/+d0(-1)/+d4(0) internal"},
                {"order": 18, "wire_bytes": "1 + 22*cnt", "mem_off": "+0x28", "type": "i8_cnt x 22B (3,972 rows, 15,360 items)", "binding": "Cscm [104] (held: 118 items slsn=0)"},
                {"order": 19, "wire_bytes": "1 + 10*cnt", "mem_off": "+0x20", "type": "u8_cnt x 10B", "binding": "internal INT_DUTY_PLAYER_COUNT (cnt=0 all 84,259)"},
                {"order": 20, "wire_bytes": "1 + 66*flag", "mem_off": "+0x48", "type": "UEFA coeff ring buffer (569 rows)", "binding": "Cuf1..Cuf9, Cf10 [133..142] (10 L3); fixed 24B header internal"},
                {"order": 21, "wire_bytes": 7, "mem_off": "+0x30/+0x38/+0x70/+0x50", "type": "3x_u8_flag + u32_cnt", "binding": "internal (+0x30=CWsc; all 0 across 84,259 rows)"},
                {"order": 22, "wire_bytes": "2 + 11*cnt", "mem_off": "+0x68", "type": "u16_cnt x (tag=2 + 10B) (249 rows, 694 items)", "binding": "CPsL [197] (L3)"},
                {"order": 23, "wire_bytes": 3, "mem_off": "+0x40/+0xdc", "type": "u8_flag(0) + u16(1)", "binding": "internal (all 0 / all 1)"},
            ],
            "common_prefix_client_and_server": [
                {"order": 24, "wire_bytes": 2, "mem_off": "+0xd8", "type": "u16", "binding": "Cyfn [26] (t71 L3, excluded from t82; 100% client==server)"},
                {"order": 25, "wire_bytes": 4, "mem_off": "+0xcc", "type": "u32", "binding": "internal TCoi (84,259/84,259 0xffffffff in BOTH client & server, 0 zeros)"},
            ],
        },
        "CLUB_plus_0xb0_TEAM_CONTAINER_IN_GAME_DATA": {
            "object_size": "0xb0",
            "reader_fo": "0x11d3200",
            "fixup_fo": "0x3ea1030",
            "writer_fo": "0x11d53f0",
            "common_tail_client_and_server_100pct_identical": [
                {"order": 26, "wire_bytes": "0 (skipped: CLUB+0xba==0)", "mem_off": "+0x90", "type": "optional_utf8", "binding": "TCnn [11] (held: 0 populated)"},
                {"order": 27, "wire_bytes": 2, "mem_off": "+0xac", "type": "u16", "binding": "internal (0..127, 2,819 nz, 100% client==server, 0 getter/setter hits)"},
                {"order": 28, "wire_bytes": "4 + len", "mem_off": "+0x98", "type": "u32_len_utf8", "binding": "TCht [12] (L3, 799 non-empty, 100% client==server)"},
                {"order": 29, "wire_bytes": "1 + 27*cnt", "mem_off": "+0x78", "type": "u8_cnt x (tag=1 + 26B TEAM_KIT_FOR_YEAR, 405,204 items)", "binding": "Tko1..3/Tkg1..3 [178..183] (6 held: no frozen list_item_fields) + 1scl..3tbc [70..75,78..81] (10 held: derived read-only)"},
                {"order": 30, "wire_bytes": 4, "mem_off": "+0xa0", "type": "4B_rev_rgba", "binding": "ttcl [24, 76] (held: duplicate XML + 6,586 zero fallbacks)"},
                {"order": 31, "wire_bytes": 4, "mem_off": "+0xa8", "type": "4B_rev_rgba", "binding": "tbcl [25, 77] (held: duplicate XML + 6,586 zero fallbacks)"},
            ],
            "server_only_tail": [
                {"order": 32, "wire_bytes": "2 + 20*cnt", "mem_off": "+0x18", "type": "i16_cnt x 20B (44 rows, 46 items)", "binding": "Cspb [86] (held: type/venu enum_ref=None)"},
                {"order": 33, "wire_bytes": "1 + 6*cnt", "mem_off": "+0x30", "type": "i8_cnt x 6B (903 rows, 1,202 items)", "binding": "Cren [199] (held: rsnr enum_ref=None)"},
                {"order": 34, "wire_bytes": 4, "mem_off": "+0x74..+0x77", "type": "4x_i8_enum", "ctor_default": 0, "binding": "Cpfr/C2pf/Cdfo/Cafo [145..148] (4 held: out-of-domain vs pfms/sfms/dfms/afms)"},
                {"order": 35, "wire_bytes": 12, "mem_off": "+0x68/+0x6c/+0x70", "type": "3x_i32", "ctor_default": 10000, "binding": "Catd/Cmna/Cmxa [61..63] (3 L3)"},
                {"order": 36, "wire_bytes": "2 + varlen_poly", "mem_off": "+0x00", "type": "u16_cnt x polymorphic(factory 0x14cf6d0, 8 observed tags)", "binding": "Csoc(5)/Cbbl(7)/pcpt(38) (3 L3); Camc(6) (held: apfr=0); CssT..E(35) (4 preserved t63 held, 0 items); tags 4/9/16/37 internal/non-club.xml"},
                {"order": 37, "wire_bytes": "1 + (8+12*cnt)*flag", "mem_off": "+0x48", "type": "TCrs (1,836 flag=1, 1,687 non-empty, 23,027 items)", "binding": "TCrs [201] (held: 2,709 PUnJ ftjn violations + PUnI/PUnT enum_ref=None)"},
            ],
        },
    }

    grade_counts = Counter(e["grade"] for e in fm_entries)
    print(f"[t82] 5/5 Writing deliverables to {out_dir} (L3={grade_counts['L3']}, held={grade_counts['held']}, negatives={len(negative_entries)})...")
    out_dir.mkdir(parents=True, exist_ok=True)

    xref_doc = {
        "task": "t82",
        "scope": "table_extra_3.dat remaining members (CLUB+0x100 & CLUB+0xb0), excluding t71 24 L3s",
        "L4": 0,
        "editor": {"path": str(exe_path), "sha256": PINNED_SHA256["editor.exe"]},
        "pinned_inputs": pinned_ok,
        "addressing": "PE file offsets with corresponding VA and exact bytes",
        "wire_ledger": wire_ledger,
        "core_witnesses": core_witnesses,
        "uefa_jump_tables": {"CLUB_GET_0xe91db0": cuf_get_jt, "CLUB_SET_0xe86b54": cuf_set_jt},
        "polymorphic_base0_dispatch": poly_catalog,
        "negative_proof_starting_record": negative_starting_record,
    }

    field_map_doc = {
        "task": "t82",
        "scope": "table_extra_3.dat remaining club.xml occurrences (excludes t71 24 L3s; preserves t57/t63 negatives verbatim)",
        "L4": 0,
        "pinned_inputs": pinned_ok,
        "excluded_t71_L3_indices": sorted(T71_L3_INDICES),
        "excluded_t71_L3_count": len(T71_L3_INDICES),
        "superseded_prior_negatives": [],
        "grade_counts": {
            "L3": int(grade_counts["L3"]),
            "held": int(grade_counts["held"]),
            "negative_not_extra3": sum(1 for e in negative_entries if e["grade"] == "negative_not_extra3"),
            "preserved_t63_held_non_extra3": sum(1 for e in negative_entries if e["grade"] == "held"),
        },
        "new_L3_codes": [e["code"] for e in fm_entries if e["grade"] == "L3"],
        "held_codes": [f"{e['code']}[{e['xml_index']}]" for e in fm_entries if e["grade"] == "held"],
        "fields": fm_entries,
        "negative_not_extra3": negative_entries,
    }

    domain_stats_doc = {
        "task": "t82",
        "L4": 0,
        "archives": {
            "client_extra3": {
                "member": "client_db/table_extra_3.dat",
                "rows": cli["rows"],
                "bytes": cli["bytes"],
                "footer_bytes": 0,
                "stream_sha256": cli["stream_sha256"],
                "common_tail_sha256": cli["common_tail_sha256"],
            },
            "server_extra3": {
                "member": "server_db/table_extra_3.dat",
                "rows": srv["rows"],
                "bytes": srv["bytes"],
                "footer_bytes": 0,
                "stream_sha256": srv["stream_sha256"],
                "common_tail_sha256": srv["common_tail_sha256"],
            },
            "common_tail_client_eq_server_exact": cli["common_tail_sha256"] == srv["common_tail_sha256"],
            "join_tables": {
                "table_3_clubs": len(club_uids),
                "table_25_comps": len(comp_uids),
                "table_23_stage_names": len(stage_name_uids),
                "table_45_starting_records": int(t45_count),
            },
        },
        "scope_separation": {
            "client_only_fields": [],
            "client_and_server_fields": ["TCht", "TCnn(0-populated)", "ttcl", "tbcl", "Tko1..3/Tkg1..3", "Cyfn(t71)", "+0xcc(TCoi internal)", "+0xac(internal)"],
            "server_only_fields": [
                "Ctlv", "Cmle", "Cyim", "Cyfb", "Cytv", "Crcb", "Csth", "CScP", "Cown", "Chti",
                "Cetl", "Cmtm", "Cect", "Cemn", "Cemx", "Cepr", "Cebd(t71)",
                "Csly", "Csps", "Cspt", "Csaf", "Cste", "Cspe",
                "Cuf1..Cuf9", "Cf10", "Cscm", "CPsL",
                "Catd", "Cmna", "Cmxa", "Cpfr", "C2pf", "Cdfo", "Cafo",
                "Cspb", "Cren", "TCrs", "Csoc", "Camc", "Cbbl", "pcpt", "CssT..E(0-populated)",
            ],
        },
        "election_and_cown_invariants": elec_invariants,
        "scalar_and_enum_domains": scalar_domains,
        "uefa_ring_domains": cuf_domains,
        "common_tail_domains": {
            "TCht": tcht_domain,
            "TCnn": tcnn_domain,
            "ttcl": ttcl_domain,
            "tbcl": tbcl_domain,
            "ttcl_eq_tbcl_nonzero_rows": ttcl_eq_tbcl_nz,
            "kits_base78": kit_domain,
        },
        "list_and_poly_domains": {
            "Cscm": cscm_domain,
            "CPsL": cpsl_domain,
            "Cspb": cspb_domain,
            "Cren": cren_domain,
            "TCrs": tcrs_domain,
            "Csoc_tag5": csoc_domain,
            "Camc_tag6": camc_domain,
            "Cbbl_tag7": cbbl_domain,
            "pcpt_tag38": pcpt_domain,
            "CssT_CssP_CssS_CssE_tag35": {"observed_items": 0, "observed_rows": 0},
        },
        "internal_wire_slots": internal_slots,
        "l2_anchor_witnesses": l2_anchors,
    }

    (out_dir / "xref_extra3.json").write_text(json.dumps(xref_doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (out_dir / "field_map.json").write_text(json.dumps(field_map_doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (out_dir / "domain_stats.json").write_text(json.dumps(domain_stats_doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("[t82] Build complete: PASS")
    return 0


def run_selftest() -> int:
    # 1. date4 leap & sentinel
    ok, sent = check_date4_scalar(SENTINEL_DATE4)
    assert ok and sent, "Sentinel 1900-01-01 check failed"
    ok_leap, _ = check_date4_scalar((2024 << 16) | 366)
    ok_nonleap, _ = check_date4_scalar((2023 << 16) | 366)
    assert ok_leap and not ok_nonleap, "Leap-year date4 boundary failed"
    # 2. UEFA ring buffer wraparound
    ordered, head = replay_uefa_ring([1000 * k for k in range(1, 13)])
    assert head == 2 and ordered == [1000 * k for k in range(3, 13)], (ordered, head)
    # 3. Domain validator catches -1 < 0 and allows suppressed 0
    s1 = summarize_int_arr(np.array([0, 10, -1], dtype=np.int32), min_v=0, max_v=100, ctor_default=-1)
    assert s1["violations"] == 1 and s1["first_counterexample"]["row_ordinal"] == 2 and s1["count_minus1"] == 1 and s1["count_zero"] == 1
    s2 = summarize_int_arr(np.array([0, 1, 64], dtype=np.int8), allowed={1, 2}, suppress_val=0)
    assert s2["suppressed_rows"] == 1 and s2["violations"] == 1 and s2["first_counterexample"]["raw_value"] == 64
    print("[t82] selftest PASS")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="t82 builder: table_extra_3.dat remaining member naming, static dual-chain proofs, and full-archive domain stats."
    )
    ap.add_argument("--selftest", action="store_true", help="Run built-in unit self-tests and exit.")
    ap.add_argument("--build", action="store_true", help="Run full build (default when --selftest is not set).")
    ap.add_argument("--exe", type=Path, default=DEFAULT_EXE, help="Path to read-only editor.exe.")
    ap.add_argument("--data-dir", type=Path, default=DEFAULT_DATA, help="Path to scratch/data FMF archive directory.")
    ap.add_argument("--outdir", type=Path, default=DEFAULT_OUT, help="Output directory (default: scratch/t82/out).")
    args = ap.parse_args(argv)

    try:
        if args.selftest:
            rc = run_selftest()
            if not args.build:
                return rc
        return build_all(args.exe, args.data_dir, args.outdir)
    except AssertionError as exc:
        print(f"[t82] FAIL (assertion): {exc}", file=sys.stderr)
        return 1
    except RuntimeError as exc:
        print(f"[t82] FAIL (check): {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"[t82] FATAL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
