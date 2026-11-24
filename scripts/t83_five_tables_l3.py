#!/usr/bin/env python3
"""t83 — L3 static + full-archive vectorized harvest for 5 FM24 tables:
  award(0), media(7), language(8), derby(18), weather(27).

Generates in --outdir (default: scratch/t83/out):
  - field_map.json
  - xref_award.json, xref_language.json, xref_weather.json, xref_derby.json, xref_media.json
  - domain_stats.json

Exit codes: 0 success, 1 check/selftest failed, 2 usage or fatal error.
"""
from __future__ import annotations
import sys as _cfg_sys
from pathlib import Path as _cfg_pathlib
_cfg_sys.path.insert(0, str(_cfg_pathlib(__file__).resolve().parent))
import fm24_config as _cfg

import argparse
import bisect
import hashlib
import json
import os
import struct
import sys
from collections import Counter
from pathlib import Path
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(_cfg.VENDOR_DIR))

import numpy as np
import zstandard as zstd
from capstone import CS_ARCH_X86, CS_MODE_64, Cs

EXE_PATH = Path(str(_cfg.EDITOR_EXE))
EXPECTED_EXE_SHA256 = "b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4"
DB_DIR = Path(os.environ.get("FM24_DB_DIR", str(ROOT / "scratch/data")))
MANIFEST_PATH = ROOT / "evidence/MANIFEST.json"
MASTER_REL = "evidence/fm24/reports/editor_schema/master.json"
SMALL_REL = "evidence/fm24/reports/dbdat_decode/db_tables_small.json"
BIG_REL = "evidence/fm24/reports/dbdat_decode/db_tables_big.json"
T74_FRAMES_PATH = ROOT / "scratch/t74/out/frames.json"
T76C_DIR = ROOT / "scratch/t76c/out"


# ---------------------------------------------------------------------------
# PE64 + Capstone helpers
# ---------------------------------------------------------------------------
class MiniPE64:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.raw = path.read_bytes()
        if self.raw[:2] != b"MZ":
            raise ValueError("not MZ")
        pe_off = struct.unpack_from("<I", self.raw, 0x3C)[0]
        if self.raw[pe_off:pe_off + 4] != b"PE\x00\x00":
            raise ValueError("not PE")
        _, n_sec, _, _, _, opt_sz, _ = struct.unpack_from("<HHIIIHH", self.raw, pe_off + 4)
        opt_off = pe_off + 24
        if struct.unpack_from("<H", self.raw, opt_off)[0] != 0x20B:
            raise ValueError("not PE32+")
        self.image_base = struct.unpack_from("<Q", self.raw, opt_off + 24)[0]
        exc_rva, exc_sz = struct.unpack_from("<II", self.raw, opt_off + 112 + 3 * 8)
        sec_off = opt_off + opt_sz
        self.sections: list[tuple[int, int, int, int]] = []
        for i in range(n_sec):
            o = sec_off + i * 40
            vsize, vrva, rsize, roff = struct.unpack_from("<IIII", self.raw, o + 8)
            self.sections.append((vrva, max(vsize, rsize), roff, rsize))
        self.pdata: list[tuple[int, int]] = []
        self.pdata_starts: list[int] = []
        if exc_rva and exc_sz:
            exc_fo = self.rva_to_fo(exc_rva)
            for k in range(0, exc_sz, 12):
                b, e, _ = struct.unpack_from("<III", self.raw, exc_fo + k)
                if b == 0 and e == 0:
                    break
                self.pdata.append((b, e))
                self.pdata_starts.append(b)

    def rva_to_fo(self, rva: int) -> int:
        for vrva, vspan, roff, rsize in self.sections:
            if vrva <= rva < vrva + vspan:
                d = rva - vrva
                if d < rsize:
                    return roff + d
        raise ValueError(f"rva {hex(rva)} not mapped")

    def fo_to_rva(self, fo: int) -> int:
        for vrva, _, roff, rsize in self.sections:
            if roff <= fo < roff + rsize:
                return vrva + (fo - roff)
        raise ValueError(f"fo {hex(fo)} not mapped")

    def va_to_fo(self, va: int) -> int:
        return self.rva_to_fo(va - self.image_base)

    def fo_to_va(self, fo: int) -> int:
        return self.image_base + self.fo_to_rva(fo)

    def func_bounds_fo(self, entry_fo: int) -> tuple[int, int]:
        rva = self.fo_to_rva(entry_fo)
        idx = bisect.bisect_right(self.pdata_starts, rva) - 1
        if idx >= 0:
            b, e = self.pdata[idx]
            if b <= rva < e:
                return self.rva_to_fo(b), self.rva_to_fo(e)
        raise ValueError(f"no .pdata entry for {hex(entry_fo)}")

    def rtti_name(self, vtable_va: int) -> str:
        vt_fo = self.va_to_fo(vtable_va)
        col_va = struct.unpack_from("<Q", self.raw, vt_fo - 8)[0]
        col_fo = self.va_to_fo(col_va)
        sig, _, _, td_rva = struct.unpack_from("<IIII", self.raw, col_fo)
        if sig != 1:
            raise ValueError(f"bad RTTI sig {sig}")
        td_fo = self.rva_to_fo(td_rva)
        end = self.raw.index(b"\x00", td_fo + 16)
        return self.raw[td_fo + 16:end].decode("ascii")

    def rel32_target_fo(self, table_fo: int, idx: int) -> int:
        rel = struct.unpack_from("<i", self.raw, table_fo + idx * 4)[0]
        return self.va_to_fo(self.fo_to_va(table_fo) + rel)

    def vtable_slot_fo(self, vtable_va: int, slot: int) -> int:
        vt_fo = self.va_to_fo(vtable_va)
        fn_va = struct.unpack_from("<Q", self.raw, vt_fo + slot * 8)[0]
        return self.va_to_fo(fn_va)

    def unwrap_thunk(self, md: Cs, fo: int) -> int:
        ins = next(md.disasm(self.raw[fo:fo + 16], self.fo_to_va(fo), 1))
        if ins.mnemonic == "jmp" and ins.op_str.startswith("0x"):
            return self.va_to_fo(int(ins.op_str, 16))
        return fo

    def dis_one(self, md: Cs, fo: int) -> dict[str, Any]:
        va = self.fo_to_va(fo)
        ins = next(md.disasm(self.raw[fo:fo + 16], va, 1))
        return {
            "fo": hex(fo),
            "va": hex(va),
            "bytes": ins.bytes.hex(),
            "text": f"{ins.mnemonic} {ins.op_str}".strip(),
        }

    def dis_n(self, md: Cs, fo: int, n: int) -> list[dict[str, Any]]:
        va0 = self.fo_to_va(fo)
        out: list[dict[str, Any]] = []
        for ins in md.disasm(self.raw[fo:fo + n * 16], va0, n):
            ifo = fo + (ins.address - va0)
            out.append({
                "fo": hex(ifo),
                "va": hex(ins.address),
                "bytes": ins.bytes.hex(),
                "text": f"{ins.mnemonic} {ins.op_str}".strip(),
            })
        return out


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_integrity() -> dict[str, Any]:
    exe_sha = sha256_file(EXE_PATH)
    if exe_sha != EXPECTED_EXE_SHA256:
        raise RuntimeError(f"editor.exe SHA-256 mismatch: {exe_sha}")
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    man_map = {e["path"].replace("\\", "/"): e["sha256"] for e in manifest.get("files", [])}
    out: dict[str, Any] = {
        "editor.exe": {"path": str(EXE_PATH), "sha256": exe_sha, "verified": True},
    }
    for rel in (MASTER_REL, SMALL_REL, BIG_REL):
        actual = sha256_file(ROOT / rel)
        exp = man_map.get(rel) or man_map.get(rel.removeprefix("evidence/"))
        if exp is None or actual != exp:
            raise RuntimeError(f"MANIFEST mismatch for {rel}: actual={actual} exp={exp}")
        out[rel] = {"sha256": actual, "manifest_match": True}
    return out


# ---------------------------------------------------------------------------
# FMF / Zstd loader + generic helpers
# ---------------------------------------------------------------------------
def load_fmf(side: str, wanted: list[str]) -> dict[str, bytes]:
    raw = (DB_DIR / f"{side}_db.dat").read_bytes()
    toc_off, base_off = (x + 17 for x in struct.unpack_from("<QQ", raw, 17))
    toc = zstd.ZstdDecompressor().decompressobj().decompress(raw[toc_off + 9:])
    pos = [0]
    entries: dict[str, tuple[int, int, int]] = {}

    def take(n: int) -> bytes:
        a = pos[0]
        pos[0] += n
        return toc[a:a + n]

    def u32() -> int:
        return struct.unpack("<I", take(4))[0]

    def s() -> str:
        return take(u32()).decode("utf-8")

    def walk(pfx: str) -> None:
        cur = pfx + s() + "/"
        for _ in range(u32()):
            nm = cur + s() + s()
            off, csz, usz, _, _ = struct.unpack("<5Q", take(40))
            entries[nm] = (base_off + off, base_off + off + csz, usz)
        for _ in range(u32()):
            walk(cur)

    walk("")
    out: dict[str, bytes] = {}
    for w in wanted:
        key = f"{side}_db/{w}"
        if key not in entries:
            continue
        lo, hi, usz = entries[key]
        q = lo
        while q < hi:
            dec = zstd.ZstdDecompressor().decompressobj()
            pl = dec.decompress(raw[q:hi])
            used = (hi - q) - len(dec.unused_data)
            if len(pl) == usz:
                out[w] = pl
                break
            q += used
        if w not in out:
            raise RuntimeError(f"failed decompress {key}")
    return out


def _scan_uids_dp_once(buf: bytes, tid: int, require_tail0: bool) -> np.ndarray:
    n = struct.unpack_from("<I", buf, 8)[0]
    L = len(buf)
    arr_u8 = np.frombuffer(buf, dtype=np.uint8)
    cand: dict[int, list[int]] = {}
    for r in range(4):
        m_cnt = (L - 9 - r - 12) // 4 + 1
        if m_cnt <= 0:
            continue
        o = arr_u8[r:r + 4 * m_cnt].view("<u4")
        a = arr_u8[r + 4:r + 4 + 4 * m_cnt].view("<u4")
        b = arr_u8[r + 8:r + 8 + 4 * m_cnt].view("<u4")
        mask = (a == b) & (a != 0) & (a != 0xFFFFFFFF) & (o < n)
        idx = np.nonzero(mask)[0]
        if idx.size == 0:
            continue
        pos_all = r + 4 * idx
        keep = (pos_all >= 13) & (pos_all + 12 <= L - 9)
        if require_tail0:
            keep = keep & (arr_u8[pos_all + 12] == 0)
        idx = idx[keep]
        pos_all = pos_all[keep]
        for p, v in zip(pos_all.tolist(), o[idx].tolist()):
            cand.setdefault(v, []).append(p)
    reach: list[list[int]] = [[] for _ in range(n)]
    last_target = L - 9 - 12
    reach[n - 1] = [p for p in cand.get(n - 1, ()) if p == last_target]
    if not reach[n - 1]:
        raise RuntimeError(f"scan_uids t{tid}: last row does not close at {last_target}")
    for j in range(n - 2, -1, -1):
        max_nxt = reach[j + 1][-1]
        pts = [p for p in cand.get(j, ()) if p + 12 <= max_nxt]
        if not pts:
            raise RuntimeError(f"scan_uids t{tid}: chain lost at row {j}")
        reach[j] = sorted(pts)
    prev_min = 1
    for j in range(n):
        reach[j] = [p for p in reach[j] if p >= prev_min + 12]
        if not reach[j]:
            raise RuntimeError(f"scan_uids t{tid}: forward lost at row {j}")
        prev_min = reach[j][0]
    for j in range(n - 2, -1, -1):
        max_nxt = reach[j + 1][-1]
        reach[j] = [p for p in reach[j] if p + 12 <= max_nxt]
    pinned_uids = [struct.unpack_from("<I", buf, r[0] + 4)[0] for r in reach if len(r) == 1]
    uids = np.empty(n, dtype=np.uint32)
    prev_p = 1
    for j in range(n):
        cands = [p for p in reach[j] if p >= prev_p + 12]
        if len(cands) == 1:
            p = cands[0]
        else:
            nb = [
                struct.unpack_from("<I", buf, reach[k][0] + 4)[0]
                for k in range(max(0, j - 10), min(n, j + 11))
                if k != j and len(reach[k]) == 1
            ]
            ref = nb if nb else pinned_uids
            p = min(cands, key=lambda q: (min(abs(struct.unpack_from("<I", buf, q + 4)[0] - u) for u in ref), -q))
        uids[j] = struct.unpack_from("<I", buf, p + 4)[0]
        prev_p = p
    return uids


def scan_uids(buf: bytes, tid: int = -1) -> np.ndarray:
    n = struct.unpack_from("<I", buf, 8)[0]
    if n == 0:
        return np.empty(0, dtype=np.uint32)
    if (len(buf) - 22) % n == 0:
        st = (len(buf) - 22) // n
        arr = np.frombuffer(buf, dtype=np.uint8, offset=13, count=n * st).reshape(n, st)
        if np.array_equal(arr[:, st - 12:st - 8].copy().view("<u4").ravel(), np.arange(n, dtype=np.uint32)):
            u1 = arr[:, st - 8:st - 4].copy().view("<u4").ravel()
            u2 = arr[:, st - 4:st].copy().view("<u4").ravel()
            if np.array_equal(u1, u2) and np.all(u1 != 0):
                return u1
    for req0 in ((False,) if tid == 24 else (True, False)):
        try:
            return _scan_uids_dp_once(buf, tid, req0)
        except RuntimeError:
            if not req0:
                raise
    raise RuntimeError(f"scan_uids failed for t{tid}")


def l2_fk_candidate_matrix(
    vals: np.ndarray,
    ref_n: dict[int, int],
    ref_uids: dict[int, set[int]],
    candidate_tids: tuple[int, ...] = (5, 6, 10, 47, 25, 30, 3),
) -> dict[str, Any]:
    """Vectorized L2 FK candidate scan across reference tables (ordinal vs wrong-UID control)."""
    v = np.asarray(vals, dtype=np.int32)
    null_m1 = int((v == -1).sum())
    other_neg = int(((v < 0) & (v != -1)).sum())
    valid_zero = int((v == 0).sum())
    live = v[v >= 0]
    n_live = int(len(live))
    live_min = int(live.min()) if n_live else None
    live_max = int(live.max()) if n_live else None
    cands: dict[str, Any] = {}
    live_list = live.tolist()
    for tid in candidate_tids:
        nt = ref_n[tid]
        in_ord = int((live < nt).sum()) if n_live else 0
        uset = ref_uids[tid]
        uid_hits = sum(1 for x in live_list if x in uset)
        cands[f"t{tid}"] = {
            "target_rows": nt,
            "ordinal_in_range": in_ord,
            "ordinal_miss": n_live - in_ord,
            "ordinal_fit_100pct": (other_neg == 0 and in_ord == n_live),
            "top_over_N": round(live_max / nt, 4) if (n_live and nt) else None,
            "wrong_uid_control_hits": uid_hits,
            "wrong_uid_control_misses": n_live - uid_hits,
        }
    return {
        "rows": int(len(v)),
        "null_0xffffffff_count": null_m1,
        "valid_zero_count": valid_zero,
        "other_neg": other_neg,
        "live": n_live,
        "live_min": live_min,
        "live_max": live_max,
        "distinct_live": int(len(np.unique(live))) if n_live else 0,
        "fk_candidates": cands,
    }


def check_dates_vec(vals: np.ndarray) -> dict[str, Any]:
    v = np.asarray(vals, dtype="<u4")
    y = v >> 16
    d = v & 0x1FF
    rem = (v >> 9) & 0x7F
    leap = (y % 4 == 0) & ((y % 100 != 0) | (y % 400 == 0))
    ok = (rem == 0) & (y >= 1) & (d >= 1) & (d <= 365 + leap)
    inv = int((~ok).sum())
    return {
        "n": int(len(v)),
        "valid_gregorian": int(ok.sum()),
        "invalid": inv,
        "year_min": int(y[ok].min()) if ok.any() else None,
        "year_max": int(y[ok].max()) if ok.any() else None,
        "default_1900_01_01_count": int((v == 0x076C0001).sum()),
        "violations": inv,
    }


def fk_stats_vec(vals: np.ndarray, tid: int, ref_n: dict[int, int], ref_uids: dict[int, set[int]]) -> dict[str, Any]:
    v = np.asarray(vals, dtype=np.int32)
    n = int(len(v))
    null_m1 = int((v == -1).sum())
    other_neg = int(((v < 0) & (v != -1)).sum())
    valid_zero = int((v == 0).sum())
    live = v[v >= 0]
    n_live = int(len(live))
    in_range = int((live < ref_n[tid]).sum())
    miss = n_live - in_range
    uset = ref_uids[tid]
    wrong_uid_hits = sum(1 for x in live.tolist() if x in uset)
    return {
        "rows_or_items": n,
        "target_table": tid,
        "target_rows": ref_n[tid],
        "live": n_live,
        "valid_zero_count": valid_zero,
        "null_0xffffffff_count": null_m1,
        "other_neg": other_neg,
        "ordinal_in_range": in_range,
        "ordinal_miss": miss,
        "wrong_uid_control_hits": wrong_uid_hits,
        "wrong_uid_control_misses": n_live - wrong_uid_hits,
        "live_min": int(live.min()) if n_live else None,
        "live_max": int(live.max()) if n_live else None,
        "violations": other_neg + miss,
    }


def parse_enum_ids(master: dict[str, Any], key: str) -> list[int]:
    em = master["enums"][key]
    out: list[int] = []
    for x in em.get("values", []):
        v = x.get("enum_id")
        if v is None:
            v = x.get("enum")
        if v is None:
            v = x.get("id")
        out.append(int(v, 0) if isinstance(v, str) else int(v))
    return sorted(set(out))


def enum_stats_vec(
    vals: np.ndarray,
    allowed: list[int],
    dunis: np.ndarray,
    names: list[str] | None = None,
) -> tuple[dict[str, Any], dict[str, Any] | None]:
    v = np.asarray(vals, dtype=np.int64)
    aset = set(allowed)
    u, cnt = np.unique(v, return_counts=True)
    hist = {str(int(k)): int(c) for k, c in zip(u, cnt)}
    bad_mask = np.array([int(x) not in aset for x in v.tolist()], dtype=bool)
    n_bad = int(bad_mask.sum())
    bad_vals: dict[str, int] = {}
    first_ce: dict[str, Any] | None = None
    if n_bad:
        bi = np.nonzero(bad_mask)[0]
        bu, bc = np.unique(v[bi], return_counts=True)
        bad_vals = {str(int(k)): int(c) for k, c in zip(bu, bc)}
        r0 = int(bi[0])
        first_ce = {
            "row": r0,
            "duni": int(dunis[r0]),
            "raw_value": int(v[r0]),
        }
        if names is not None:
            first_ce["name"] = names[r0]
    dom = {
        "rows": int(len(v)),
        "allowed_enum": allowed,
        "raw_histogram": hist,
        "in_enum": int(len(v) - n_bad),
        "violations": n_bad,
    }
    if n_bad:
        dom["out_of_enum_histogram"] = bad_vals
    return dom, first_ce


def int_range_stats_vec(
    vals: np.ndarray,
    mn: int,
    mx: int,
    dunis: np.ndarray,
    null_cond: str | None = None,
    names: list[str] | None = None,
) -> tuple[dict[str, Any], dict[str, Any] | None]:
    v = np.asarray(vals, dtype=np.int64)
    if null_cond == "le0":
        sup = v <= 0
    elif null_cond == "eq0":
        sup = v == 0
    elif null_cond == "lt0":
        sup = v < 0
    elif null_cond == "eq100":
        sup = v == 100
    else:
        sup = np.zeros(len(v), dtype=bool)
    live_mask = ~sup
    live = v[live_mask]
    bad_mask = live_mask & ((v < mn) | (v > mx))
    n_bad = int(bad_mask.sum())
    first_ce: dict[str, Any] | None = None
    if n_bad:
        r0 = int(np.nonzero(bad_mask)[0][0])
        first_ce = {"row": r0, "duni": int(dunis[r0]), "raw_value": int(v[r0]), "expected": f"[{mn}..{mx}]"}
        if names is not None:
            first_ce["name"] = names[r0]
    dom = {
        "rows": int(len(v)),
        "schema_range": [mn, mx],
        "null_rule": null_cond,
        "suppressed_null": int(sup.sum()),
        "live": int(live_mask.sum()),
        "valid_zero_count": int((live == 0).sum()) if len(live) else 0,
        "live_min": int(live.min()) if len(live) else None,
        "live_max": int(live.max()) if len(live) else None,
        "violations": n_bad,
    }
    return dom, first_ce


# ---------------------------------------------------------------------------
# Static verification of class headers, DB_CONTEXT, and per-field instructions
# ---------------------------------------------------------------------------
FACTORY_FO = 0xF48B30
FACTORY_REL32_FO = 0xF49D38
DB_CONTEXT_FO = 0xF026C0

DB_CONTEXT_BINDINGS = [
    (0x00, 0, "AWARD", 0xF026F5, 0xF0281C),
    (0x08, 2, "CITY", 0xF02837, 0xF02957),
    (0x10, 3, "CLUB", 0xF02973, 0xF02A93),
    (0x18, 25, "COMP", 0xF02AAF, 0xF02BCF),
    (0x20, 5, "CONTINENT", 0xF02BEB, 0xF02D0B),
    (0x28, 10, "NATION", 0xF02D27, 0xF02E47),
    (0x48, 7, "MEDIA_SOURCE", 0xF03217, 0xF03337),
    (0x50, 8, "LANGUAGE", 0xF03353, 0xF03473),
    (0x58, 47, "LOCAL_REGION", 0xF0348F, 0xF035AF),
    (0x60, 9, "NATION_T9", 0xF035CB, 0xF036EB),
    (0x68, 1, "PERSON", 0xF03707, 0xF03827),
    (0x80, 21, "STADIUM", 0xF03DE6, 0xF03F06),
    (0x90, 23, "STAGE_NAME", 0xF04064, 0xF04184),
    (0x98, 24, "TEAM", 0xF041A3, 0xF042C3),
    (0xA0, 27, "WEATHER", 0xF042E2, 0xF04402),
    (0xB0, 18, "DERBY", 0xF03B6B, 0xF03C8B),
]

CLASS_META = {
    0: {
        "key": "award_0",
        "xml": "award.xml",
        "entity_code": "awar",
        "rtti": ".?AVAWARD@db@@",
        "factory_case_fo": 0xF48C54,
        "vtable_va": 0x14187B828,
    },
    7: {
        "key": "media_7",
        "xml": "media source.xml",
        "entity_code": "mdso",
        "rtti": ".?AVMEDIA_SOURCE@db@@",
        "factory_case_fo": 0xF48EA6,
        "vtable_va": 0x1418BDD08,
    },
    8: {
        "key": "language_8",
        "xml": "language.xml",
        "entity_code": "lang",
        "rtti": ".?AVLANGUAGE@db@@",
        "factory_case_fo": 0xF48EBB,
        "vtable_va": 0x141888DB8,
    },
    18: {
        "key": "derby_18",
        "xml": "derby.xml",
        "entity_code": "drbr",
        "rtti": ".?AVDERBY@db@@",
        "factory_case_fo": 0xF48F77,
        "vtable_va": 0x141887278,
    },
    27: {
        "key": "weather_27",
        "xml": "weather.xml",
        "entity_code": "weat",
        "rtti": ".?AVWEATHER@db@@",
        "factory_case_fo": 0xF491DD,
        "vtable_va": 0x141882DE8,
    },
}


def verify_class_static(pe: MiniPE64, md: Cs, tid: int) -> dict[str, Any]:
    cm = CLASS_META[tid]
    case_fo = pe.rel32_target_fo(FACTORY_REL32_FO, tid)
    if case_fo != cm["factory_case_fo"]:
        raise RuntimeError(f"tid {tid} factory case mismatch: {hex(case_fo)} vs {hex(cm['factory_case_fo'])}")
    rtti = pe.rtti_name(cm["vtable_va"])
    if rtti != cm["rtti"]:
        raise RuntimeError(f"tid {tid} RTTI mismatch: {rtti} vs {cm['rtti']}")
    slots = {}
    for s_idx, s_name in [(2, "get"), (3, "set"), (5, "prop_reg"), (19, "read"), (20, "fixup"), (21, "write")]:
        s_fo = pe.vtable_slot_fo(cm["vtable_va"], s_idx)
        real_fo = pe.unwrap_thunk(md, s_fo)
        slots[f"slot{s_idx}_{s_name}"] = {
            "entry_fo": hex(s_fo),
            "entry_va": hex(pe.fo_to_va(s_fo)),
            "real_fo": hex(real_fo),
            "real_va": hex(pe.fo_to_va(real_fo)),
        }
    return {
        "table_id": tid,
        "xml": cm["xml"],
        "entity_code": cm["entity_code"],
        "rtti": rtti,
        "factory": {
            "function_fo": hex(FACTORY_FO),
            "function_va": hex(pe.fo_to_va(FACTORY_FO)),
            "rel32_table_fo": hex(FACTORY_REL32_FO),
            "case_fo": hex(case_fo),
            "case_va": hex(pe.fo_to_va(case_fo)),
            "dis_head": pe.dis_n(md, case_fo, 6),
        },
        "vtable_va": hex(cm["vtable_va"]),
        "vtable_fo": hex(pe.va_to_fo(cm["vtable_va"])),
        "vtable_slots": slots,
    }


def verify_db_context(pe: MiniPE64, md: Cs) -> list[dict[str, Any]]:
    rows = []
    for off, tid, name, ctor_fo, store_fo in DB_CONTEXT_BINDINGS:
        c_ins = pe.dis_one(md, ctor_fo)
        s_ins = pe.dis_one(md, store_fo)
        if "call 0x140ffa310" not in c_ins["text"]:
            raise RuntimeError(f"DB_CONTEXT ctor check failed at {hex(ctor_fo)}: {c_ins}")
        if "[r14" not in s_ins["text"] or not s_ins["text"].endswith(", rdi"):
            raise RuntimeError(f"DB_CONTEXT store check failed at {hex(store_fo)}: {s_ins}")
        rows.append({
            "db_off": f"+0x{off:02x}",
            "table_id": tid,
            "name": name,
            "ctor_call": c_ins,
            "store_ins": s_ins,
        })
    return rows


def check_4cc_at(pe: MiniPE64, md: Cs, fo: int, expected_cc: str) -> dict[str, Any]:
    info = pe.dis_one(md, fo)
    imm_hex = hex(struct.unpack(">I", expected_cc.encode("ascii"))[0])
    if imm_hex not in info["text"]:
        raise RuntimeError(f"4CC '{expected_cc}' ({imm_hex}) not found at {hex(fo)}: {info['text']}")
    return info


def check_ins_contains(pe: MiniPE64, md: Cs, fo: int, substr: str) -> dict[str, Any]:
    info = pe.dis_one(md, fo)
    if substr not in info["text"]:
        raise RuntimeError(f"Expected '{substr}' at {hex(fo)}, got: {info['text']}")
    return info


def decode_switch_targets(pe: MiniPE64, tbl_fo: int, base_4cc: str, indices: list[int]) -> dict[str, dict[str, Any]]:
    base_val = struct.unpack(">I", base_4cc.encode("ascii"))[0]
    out: dict[str, dict[str, Any]] = {}
    for idx in indices:
        cc = struct.pack(">I", base_val + idx).decode("ascii")
        tfo = pe.rel32_target_fo(tbl_fo, idx)
        out[cc] = {
            "table_fo": hex(tbl_fo),
            "entry_fo": hex(tbl_fo + idx * 4),
            "index": idx,
            "target_fo": hex(tfo),
            "target_va": hex(pe.fo_to_va(tfo)),
        }
    return out


# ---------------------------------------------------------------------------
# Table 0 — AWARD (38 XML fields, 3,545 rows, 77B fixed, client==server)
# ---------------------------------------------------------------------------
def build_award(
    pe: MiniPE64,
    md: Cs,
    master: dict[str, Any],
    cli: dict[str, bytes],
    srv: dict[str, bytes],
    ref_n: dict[int, int],
    ref_uids: dict[int, set[int]],
    code_occ: Counter[str],
    db_ctx: list[dict[str, Any]],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    buf_c, buf_s = cli["table_0.dat"], srv["table_0.dat"]
    if buf_c != buf_s:
        raise RuntimeError("table_0 client != server")
    n = struct.unpack_from("<I", buf_c, 8)[0]
    if len(buf_c) != 13 + n * 77 + 9:
        raise RuntimeError("table_0 framing mismatch")
    A = np.frombuffer(buf_c, dtype=np.uint8, offset=13, count=n * 77).reshape(n, 77)
    if not np.all(A[:, 0] == 0):
        raise RuntimeError("table_0 non-zero selector")
    AB = A[:, 1:]  # body@0..63, id@64..75
    ords = AB[:, 64:68].copy().view("<u4").ravel()
    dunis = AB[:, 68:72].copy().view("<u4").ravel()
    rduis = AB[:, 72:76].copy().view("<u4").ravel()
    if not np.array_equal(ords, np.arange(n, dtype=np.uint32)):
        raise RuntimeError("table_0 ordinal != arange")
    if len(np.unique(dunis)) != n or not np.array_equal(dunis, rduis):
        raise RuntimeError("table_0 duni/rdui invariant failed")

    # Verify comp 0x5f5e117 fixup edge case
    buf25 = cli["table_25.dat"]
    n25 = struct.unpack_from("<I", buf25, 8)[0]
    st25 = (len(buf25) - 22) // n25
    u25 = np.frombuffer(buf25, dtype=np.uint8, offset=13, count=n25 * st25).reshape(n25, st25)[:, st25 - 8:st25 - 4].copy().view("<u4").ravel()
    comp_special_ord = int(np.nonzero(u25 == 0x5F5E117)[0][0])
    awmi_col = AB[:, 41:45].copy().view("<i4").ravel()
    special_rows = [int(r) for r in np.nonzero(awmi_col == comp_special_ord)[0].tolist()]

    # Static jump tables for AWsc/AWsh/AWsn/AWsr/AWss in AWARD::get & AWARD::set
    jt_get = decode_switch_targets(pe, 0xE4C1F4, "AWsc", [0, 5, 11, 15, 16])
    jt_set = decode_switch_targets(pe, 0xE4CCBC, "AWsc", [0, 5, 11, 15, 16])

    # Static map for wire fields: (body_off, width, wire_type, mem_off, get_cmp_or_jt, get_handler, set_cmp_or_jt, set_handler, reader_fo, fixup_fo, ins_check_get, ins_check_read)
    AW_STATIC: dict[str, dict[str, Any]] = {
        "AWci": {"off": 23, "w": 4, "wt": "i32_ordinal_ref:table_5", "mem": "+0x50", "gcmp": 0xE4A134, "gh": 0xE4AD85, "scmp": 0xE4C3ED, "sh": 0xE4C707, "rd": 0xE484BD, "fx": 0x3BF4A90, "gchk": "+ 0x50", "rchk": "+ 0x50", "fk": 5},
        "AWni": {"off": 27, "w": 4, "wt": "i32_ordinal_ref:table_10", "mem": "+0x60", "gcmp": 0xE4A1F7, "gh": 0xE4A203, "scmp": 0xE4C4C8, "sh": 0xE4C4D4, "rd": 0xE484ED, "fx": 0xF7F030, "gchk": "+ 0x60", "rchk": "+ 0x60", "fk": 10},
        "AWmi": {"off": 41, "w": 4, "wt": "i32_ordinal_ref:table_25", "mem": "+0x58", "gcmp": 0xE4A00A, "gh": 0xE4A016, "scmp": 0xE4C56E, "sh": 0xE4C57A, "rd": 0xE48634, "fx": 0xF7E610, "gchk": "+ 0x58", "rchk": "+ 0x58", "fk": 25},
        "AWre": {"off": 15, "w": 2, "wt": "i16", "mem": "+0x7c", "gcmp": 0xE49F04, "gh": 0xE4AE23, "scmp": 0xE4C3C0, "sh": 0xE4C3C0, "rd": 0xE4843C, "fx": None, "gchk": "+ 0x7c", "rchk": "+ 0x7c", "rng": (0, 20, None)},
        "AWwh": {"off": 39, "w": 1, "wt": "u8_optional_0_null", "mem": "+0x91", "gcmp": 0xE49AD7, "gh": 0xE4A9DD, "scmp": 0xE4C481, "sh": 0xE4C737, "rd": 0xE485ED, "fx": None, "gchk": "+ 0x91", "rchk": "+ 0x91", "rng": (1, 200, "eq0")},
        "AWwr": {"off": 40, "w": 1, "wt": "u8_optional_0_null", "mem": "+0x92", "gcmp": 0xE49AE3, "gh": 0xE49AEF, "scmp": 0xE4C48D, "sh": 0xE4C499, "rd": 0xE4860C, "fx": None, "gchk": "+ 0x92", "rchk": "+ 0x92", "rng": (1, 200, "eq0")},
        "AWfc": {"off": 4, "w": 2, "wt": "u16_rgb555", "mem": "+0x18", "gcmp": 0xE49B60, "gh": 0xE4AAA8, "scmp": 0xE4C5B6, "sh": 0xE4C5C2, "rd": 0xE48425, "fx": None, "gchk": "+ 0x18", "rchk": "+ 0x18", "color": True},
        "AWbc": {"off": 6, "w": 2, "wt": "u16_rgb555", "mem": "+0x1c", "gcmp": 0xE49F81, "gh": 0xE4A93C, "scmp": 0xE4C504, "sh": 0xE4C76D, "rd": 0xE48425, "fx": None, "gchk": "+ 0x1c", "rchk": "+ 0x18", "color": True},
        "AWtc": {"off": 8, "w": 2, "wt": "u16_rgb555", "mem": "+0x20", "gcmp": 0xE4A220, "gh": 0xE4A251, "scmp": 0xE4C31E, "sh": 0xE4C6D9, "rd": 0xE48425, "fx": None, "gchk": "+ 0x20", "rchk": "+ 0x18", "color": True},
        "AWrt": {"off": 51, "w": 1, "wt": "i8_enum", "mem": "+0x89", "gcmp": 0xE49F10, "gh": 0xE49F1C, "scmp": 0xE4C831, "sh": 0xE4C839, "rd": 0xE48779, "fx": None, "gchk": "+ 0x89", "rchk": "+ 0x89", "enum": "AWrt"},
        "AWty": {"off": 17, "w": 1, "wt": "i8_enum", "mem": "+0x81", "gcmp": 0xE4A033, "gh": 0xE4ACA7, "scmp": 0xE4C32A, "sh": 0xE4C32A, "rd": 0xE4845C, "fx": None, "gchk": "+ 0x81", "rchk": "+ 0x81", "enum": "AWty"},
        "AWdr": {"off": 18, "w": 1, "wt": "i8_enum", "mem": "+0x82", "gcmp": 0xE49B54, "gh": 0xE4ABDD, "scmp": 0xE4C5AA, "sh": 0xE4C7D8, "rd": 0xE4847F, "fx": None, "gchk": "+ 0x82", "rchk": "+ 0x82", "enum": "AWdr"},
        "AWda": {"off": 19, "w": 4, "wt": "u32_packed_date", "mem": "+0x48", "gcmp": 0xE4A140, "gh": 0xE4A171, "scmp": 0xE4C3F9, "sh": 0xE4C405, "rd": 0xE4849F, "fx": None, "gchk": "+ 0x48", "rchk": "+ 0x48", "date": True},
        "AWad": {"off": 60, "w": 4, "wt": "u32_packed_date", "mem": "+0x4c", "gcmp": 0xE49E15, "gh": 0xE4A4D3, "scmp": 0xE4C2D7, "sh": 0xE4C669, "rd": 0xE48845, "fx": None, "gchk": "+ 0x4c", "rchk": "+ 0x4c", "date": True},
        "AWnp": {"off": 59, "w": 1, "wt": "i8_enum", "mem": "+0x8b", "gcmp": 0xE49C85, "gh": 0xE4AC42, "scmp": 0xE4C5FD, "sh": 0xE4C81A, "rd": 0xE48825, "fx": None, "gchk": "+ 0x8b", "rchk": "+ 0x8b", "enum": "AWnp"},
        "AWma": {"off": 54, "w": 1, "wt": "u8_optional_le0_null", "mem": "+0x90", "gcmp": 0xE49EAA, "gh": 0xE49EB6, "scmp": 0xE4C371, "sh": 0xE4C37D, "rd": 0xE487E2, "fx": None, "gchk": "+ 0x90", "rchk": "+ 0x90", "rng": (10, 99, "le0")},
        "AWxa": {"off": 38, "w": 1, "wt": "u8_optional_le0_null", "mem": "+0x8f", "gcmp": 0xE4A0B3, "gh": 0xE4AD0C, "scmp": 0xE4C5D9, "sh": 0xE4C7EF, "rd": 0xE485CA, "fx": None, "gchk": "+ 0x8f", "rchk": "+ 0x8f", "rng": (10, 99, "le0")},
        "AWpo": {"off": 55, "w": 4, "wt": "u32_enum", "mem": "+0x78", "gcmp": 0xE49C9D, "gh": 0xE49CA9, "scmp": 0xE4C3A8, "sh": 0xE4C63E, "rd": 0xE48805, "fx": None, "gchk": "+ 0x78", "rchk": "+ 0x78", "enum": "AWpo"},
        "AWsr": {"off": 46, "w": 1, "wt": "i8_enum", "mem": "+0x84", "gcmp": None, "gh": 0xE4A315, "scmp": None, "sh": 0xE4C97C, "rd": 0xE48666, "fx": None, "gchk": "+ 0x84", "rchk": "+ 0x84", "enum": "AWsr", "jt": True},
        "AWfo": {"off": 37, "w": 1, "wt": "i8_enum", "mem": "+0x8e", "gcmp": 0xE49B6C, "gh": 0xE49B78, "scmp": 0xE4C365, "sh": 0xE4C6F0, "rd": 0xE485B1, "fx": None, "gchk": "+ 0x8e", "rchk": "+ 0x8e", "enum": "foms"},
        "AWus": {"off": 49, "w": 1, "wt": "u8_bit0_bool", "mem": "+0x8d:bit0", "gcmp": 0xE4A03F, "gh": 0xE4A04B, "scmp": 0xE4C533, "sh": 0xE4C784, "rd": 0xE48733, "fx": None, "gchk": "+ 0x8d", "rchk": "+ 0x8d", "bit": 0},
        "AWsc": {"off": 2, "w": 1, "wt": "i8_enum", "mem": "+0x80", "gcmp": None, "gh": 0xE49C08, "scmp": None, "sh": 0xE4C29C, "rd": 0xE48405, "fx": None, "gchk": "+ 0x80", "rchk": "+ 0x80", "enum": "AWsc", "jt": True},
        "AWvf": {"off": 52, "w": 1, "wt": "i8_enum", "mem": "+0x8a", "gcmp": 0xE49ACB, "gh": 0xE4AB71, "scmp": 0xE4C53F, "sh": 0xE4C54B, "rd": 0xE4879C, "fx": None, "gchk": "+ 0x8a", "rchk": "+ 0x8a", "enum": "AWvf"},
        "AWop": {"off": 49, "w": 1, "wt": "u8_bit1_bool", "mem": "+0x8d:bit1", "gcmp": 0xE49C91, "gh": 0xE4AB07, "scmp": 0xE4C609, "sh": 0xE4C615, "rd": 0xE48733, "fx": None, "gchk": "+ 0x8d", "rchk": "+ 0x8d", "bit": 1},
        "AWrb": {"off": 35, "w": 1, "wt": "i8_enum", "mem": "+0x85", "gcmp": 0xE49EF8, "gh": 0xE4AE85, "scmp": 0xE4C3B4, "sh": 0xE4C652, "rd": 0xE4855F, "fx": None, "gchk": "+ 0x85", "rchk": "+ 0x85", "enum": "AWrb"},
        "AWbr": {"off": 45, "w": 1, "wt": "i8_enum", "mem": "+0x83", "gcmp": 0xE49F8D, "gh": 0xE49F99, "scmp": 0xE4C510, "sh": 0xE4C51C, "rd": 0xE48647, "fx": None, "gchk": "+ 0x83", "rchk": "+ 0x83", "enum": "AWbr"},
        "AWss": {"off": 47, "w": 1, "wt": "i8_enum", "mem": "+0x87", "gcmp": None, "gh": 0xE4A2B0, "scmp": None, "sh": 0xE4C993, "rd": 0xE486ED, "fx": None, "gchk": "+ 0x87", "rchk": "+ 0x87", "enum": "AWss", "jt": True},
        "AWap": {"off": 50, "w": 1, "wt": "i8_enum", "mem": "+0x88", "gcmp": 0xE49E21, "gh": 0xE49E2D, "scmp": 0xE4C2E3, "sh": 0xE4C2EF, "rd": 0xE48756, "fx": None, "gchk": "+ 0x88", "rchk": "+ 0x88", "enum": "AWap"},
        "AWmg": {"off": 53, "w": 1, "wt": "u8_optional_le0_null", "mem": "+0x93", "gcmp": 0xE49FFE, "gh": 0xE4A99B, "scmp": 0xE4C562, "sh": 0xE4C7AD, "rd": 0xE487BF, "fx": None, "gchk": "+ 0x93", "rchk": "+ 0x93", "rng": (1, 100, "le0")},
    }

    xml_fields = master["entities"]["award.xml"][0]["fields"]
    schema_out: list[dict[str, Any]] = []
    xref_members: list[dict[str, Any]] = []
    dom_out: dict[str, Any] = {}

    for idx, f in enumerate(xml_fields):
        fid = f["field"]
        rec: dict[str, Any] = {
            "index": idx,
            "field": fid,
            "name": f.get("name"),
            "schema_type": f.get("type"),
            "master_occ": code_occ[fid],
            "prior_refs": ["t74/E115", "t76b(absorbed)"],
        }
        if fid == "duni":
            g_ins = check_4cc_at(pe, md, 0xFE3912, "duni")
            rec.update({
                "grade": "L3", "scope": "client+server",
                "client_body_off": 68, "server_body_off": 68, "width": 4, "wire_type": "u32",
                "member_off": "+0x0c", "getter_fo": "0xfe3912", "setter_fo": None, "reader_fo": "0x3c600f0",
                "prior_refs": ["t74/E115", "fm24_dump:award.duni@68"],
                "domain": {"rows": n, "unique": n, "eq_rdui_raw": n, "violations": 0},
            })
            xref_members.append({"field": fid, "member_off": "+0x0c", "getter_cmp": g_ins, "reader": pe.dis_one(md, 0x3C600F0)})
            dom_out[fid] = rec["domain"]
        elif fid == "rdui":
            g_ins = check_4cc_at(pe, md, 0xFE3862, "rdui")
            rec.update({
                "grade": "held", "scope": "client+server",
                "client_body_off": 72, "server_body_off": 72, "width": 4, "wire_type": "u32",
                "member_off": "+0x10", "getter_fo": "0xfe3862", "setter_fo": None, "reader_fo": "0x3c600f0",
                "prior_refs": ["t74/E115", "t79/E117", "fm24_dump:award.rdui@64(actually row_ordinal@64)"],
                "hold_reason": "DATABASE_RECORD::get 0xfe38a2 suppresses output whenever [+0x0c]==[+0x10]; 3,545/3,545 rows suppressed (0 live outputs). Note fm24_dump label 'rdui@64' is row ordinal@64..67.",
                "first_counterexample": {"row": 0, "duni": int(dunis[0]), "rdui_raw": int(rduis[0]), "reason": "suppressed_eq_duni"},
                "domain": {"rows": n, "suppressed": n, "live": 0},
            })
            xref_members.append({"field": fid, "member_off": "+0x10", "getter_cmp": g_ins, "reader": pe.dis_one(md, 0x3C600F0)})
            dom_out[fid] = rec["domain"]
        elif fid in ("NDBC", "FDBC"):
            rec.update({"grade": "editor_metadata", "scope": "non_wire", "getter_fo": None, "setter_fo": None,
                        "note": "Editor change-tracking counter; 0 hits in AWARD::get/DATABASE_RECORD::get."})
        elif fid in ("dbnm", "dAPw"):
            gfo = 0xFE375D if fid == "dbnm" else 0xFE3751
            g_ins = check_4cc_at(pe, md, gfo, fid)
            rec.update({"grade": "non_wire_computed", "scope": "non_wire", "getter_fo": hex(gfo), "setter_fo": None,
                        "note": f"DATABASE_RECORD::get {hex(gfo)} computed display/parent string; not a table_0 wire slot."})
            xref_members.append({"field": fid, "getter_cmp": g_ins, "classification": "non_wire_computed"})
        elif fid in ("AWna", "AWsn"):
            gfo = 0xE4ADA2 if fid == "AWna" else 0xE4A3DC
            sfo = 0xE4C74E if fid == "AWna" else 0xE4C91B
            mem = "+0x30" if fid == "AWna" else "+0x38"
            check_ins_contains(pe, md, gfo, mem.lstrip("+"))
            rec.update({"grade": "non_wire_language_layer", "scope": "non_wire", "member_off": mem,
                        "getter_fo": hex(gfo), "setter_fo": hex(sfo),
                        "note": f"AWARD::read 0xe483b0 never reads {mem}; localized award strings live in lang_db."})
            xref_members.append({"field": fid, "member_off": mem, "getter_handler": pe.dis_one(md, gfo), "setter_handler": pe.dis_one(md, sfo), "classification": "non_wire_language_layer"})
        elif fid == "AWsh":
            g_ins = check_ins_contains(pe, md, 0xE4A381, "0x14151d370")
            s_ins = pe.dis_one(md, 0xE4C865)
            h_ins = check_ins_contains(pe, md, 0x4338105, "+ 0x18")
            rec.update({"grade": "subtable_backed", "scope": "subtable:table_12",
                        "getter_fo": "0xe4a37a", "setter_fo": "0xe4c865", "helper_fo": "0x4338030",
                        "note": f"Subtable-backed: AWARD::get 0xe4a37a calls 0x4338030 scanning AWARD_HISTORY (table_12, {ref_n[12]} rows) where [rec+0x18]==award_ptr."})
            xref_members.append({"field": fid, "getter_call": g_ins, "setter_head": s_ins, "helper_cmp": h_ins, "target_table": 12})
        elif fid in AW_STATIC:
            st = AW_STATIC[fid]
            g_cmp = check_4cc_at(pe, md, st["gcmp"], fid) if st["gcmp"] else jt_get[fid]
            s_cmp = check_4cc_at(pe, md, st["scmp"], fid) if st["scmp"] else jt_set[fid]
            g_h = check_ins_contains(pe, md, st["gh"], st["gchk"])
            s_h = pe.dis_one(md, st["sh"])
            r_ins = check_ins_contains(pe, md, st["rd"], st["rchk"])
            fx_ins = pe.dis_one(md, st["fx"]) if st["fx"] else None

            off, w = st["off"], st["w"]
            first_ce = None
            hold_reason = None
            if "fk" in st:
                col = AB[:, off:off + 4].copy().view("<i4").ravel()
                dom = fk_stats_vec(col, st["fk"], ref_n, ref_uids)
                grade = "L3" if dom["violations"] == 0 else "held"
            elif "enum" in st:
                col = AB[:, off:off + 4].copy().view("<u4").ravel() if w == 4 else AB[:, off].view(np.int8)
                allowed = parse_enum_ids(master, st["enum"])
                dom, first_ce = enum_stats_vec(col, allowed, dunis)
                if dom["violations"] == 0:
                    grade = "L3"
                else:
                    grade = "held"
                    hold_reason = (
                        f"Exact getter ({hex(st['gh'])}) and setter ({hex(st['sh'])}) map to {st['mem']} (wire @{off}), "
                        f"but {dom['violations']}/{n} rows fall outside master.enums['{st['enum']}'] "
                        f"(out-of-enum: {dom['out_of_enum_histogram']}); getter passes raw value without suppression/clamping."
                    )
            elif "rng" in st:
                mn, mx, ncond = st["rng"]
                col = AB[:, off:off + 2].copy().view("<i2").ravel() if w == 2 else AB[:, off]
                dom, first_ce = int_range_stats_vec(col, mn, mx, dunis, ncond)
                if dom["violations"] == 0:
                    grade = "L3"
                else:
                    grade = "held"
                    hold_reason = (
                        f"Exact getter ({hex(st['gh'])}) and setter ({hex(st['sh'])}) map to {st['mem']} (wire @{off}), "
                        f"but {dom['violations']}/{dom['live']} live rows fall outside schema [{mn}..{mx}] "
                        f"(first: row={first_ce['row']}, duni={first_ce['duni']}, raw={first_ce['raw_value']}); getter suppresses <=0 only and does not clamp."
                    )
            elif st.get("date"):
                col = AB[:, off:off + 4].copy().view("<u4").ravel()
                dom = check_dates_vec(col)
                grade = "L3" if dom["violations"] == 0 else "held"
            elif st.get("color"):
                col = AB[:, off:off + 2].copy().view("<u2").ravel()
                bit15 = int(((col & 0x8000) != 0).sum())
                dom = {"rows": n, "min": int(col.min()), "max": int(col.max()), "unique": int(len(np.unique(col))), "bit15_nonzero": bit15, "violations": bit15}
                grade = "L3" if bit15 == 0 else "held"
            elif "bit" in st:
                b = st["bit"]
                bits = (AB[:, off] >> b) & 1
                dom = {"rows": n, "bit": b, "true_count": int((bits == 1).sum()), "false_count": int((bits == 0).sum()), "violations": 0}
                grade = "L3"
            else:
                raise RuntimeError(f"unhandled award spec {fid}")

            if fid in ("AWbr", "AWrt"):
                dom["post_fixup_note"] = (
                    f"AWARD::fixup (0x3a96273/0xf50de3) mutates AWbr->6 and AWrt(8->7) when AWmi points to comp UID 0x5f5e117 "
                    f"(table_25 ord {comp_special_ord}, {len(special_rows)} rows: {special_rows}). Wire bytes reported above."
                )

            rec.update({
                "grade": grade, "scope": "client+server",
                "client_body_off": off, "server_body_off": off, "width": w, "wire_type": st["wt"],
                "member_off": st["mem"],
                "getter_fo": hex(st["gh"]), "setter_fo": hex(st["sh"]), "reader_fo": hex(st["rd"]),
                "fixup_fo": hex(st["fx"]) if st["fx"] else None,
                "domain": dom,
            })
            if hold_reason:
                rec["hold_reason"] = hold_reason
                rec["first_counterexample"] = first_ce
            xref_members.append({
                "field": fid, "grade": grade, "wire_off": off, "width": w, "member_off": st["mem"],
                "getter_dispatch": g_cmp, "getter_handler": g_h,
                "setter_dispatch": s_cmp, "setter_handler": s_h,
                "reader_sink": r_ins, "fixup": fx_ins,
            })
            dom_out[fid] = dom
        else:
            raise RuntimeError(f"missing award field {fid}")
        schema_out.append(rec)

    # Internal wire slots (0 uncovered bytes across 64B body + 12B id + 1B sel = 77B)
    int_68_fk = fk_stats_vec(AB[:, 31:35].copy().view("<i4").ravel(), 47, ref_n, ref_uids)
    internal_slots = [
        {"body_off": 0, "width": 1, "member_off": "+0x7e", "reader_fo": "0xe483d5", "values": {"const": 0, "rows": n}},
        {"body_off": 1, "width": 1, "member_off": "+0x7f", "reader_fo": "0xe483e5", "values": {"const": 0, "rows": n}},
        {"body_off": 3, "width": 1, "member_off": "colour_block_ver(discarded)", "reader_fo": "0x4330ce0", "values": {"const": 1, "rows": n}},
        {"body_off": 10, "width": 2, "member_off": "+0x24", "reader_fo": "0x4330ce0", "values": {"const": 0, "rows": n}},
        {"body_off": 12, "width": 2, "member_off": "+0x28", "reader_fo": "0x4330ce0", "values": {"const": 0, "rows": n}},
        {"body_off": 14, "width": 1, "member_off": "+0x2c", "reader_fo": "0x4330ce0", "values": {"const": 1, "rows": n}},
        {"body_off": 31, "width": 4, "member_off": "+0x68", "reader_fo": "0xe4852c", "fixup_fo": "0x3bf5e90", "note": "ver>=0xdce LOCAL_REGION ordinal ref (not in award.xml)", "domain": int_68_fk},
        {"body_off": 36, "width": 1, "member_off": "+0x86", "internal_4cc": "dSAw", "getter_fo": "0xe4aa1e", "reader_fo": "0xe48591", "values": {"const": 0, "rows": n}},
        {"body_off": 48, "width": 1, "member_off": "+0x8c", "reader_fo": "0xe48710", "values": {"min": int(AB[:, 48].min()), "max": int(AB[:, 48].max()), "nonzero": int((AB[:, 48] != 0).sum())}},
        {"body_off": 64, "width": 4, "member_off": "+0x08", "reader_fo": "0x3c600f0", "note": "row ordinal (0..3544); fm24_dump label 'rdui@64' points here"},
    ]

    fm_tbl = {
        "table_id": 0,
        "xml": "award.xml",
        "rows": n,
        "client_eq_server": True,
        "frame": {"native": f"13 + {n}*77 + 9 = {len(buf_c)}", "t74": f"14 + {n}*77 + 8 = {len(buf_c)}", "body_bytes": 64, "identity_bytes": 12, "selector_bytes": 1},
        "schema_fields": schema_out,
        "internal_wire_slots": internal_slots,
    }
    xref_tbl = {
        "task": "t83",
        "class": verify_class_static(pe, md, 0),
        "db_context_refs": [r for r in db_ctx if r["table_id"] in (0, 5, 10, 25, 47)],
        "helpers": {
            "colour_block_reader": {"thunk_fo": "0x150ec50", "real_fo": "0x4330ce0", "dis_head": pe.dis_n(md, 0x4330ce0, 6)},
            "date_reader": {"thunk_fo": "0xdb7f80", "real_fo": "0x39dd7b0", "dis_head": pe.dis_n(md, 0x39DD7B0, 5)},
            "identity_reader": {"thunk_fo": "0xfae340", "real_fo": "0x3c600f0", "dis_head": pe.dis_n(md, 0x3C600F0, 5)},
            "awsh_history_scan": {"thunk_fo": "0x151c970", "real_fo": "0x4338030", "dis_head": pe.dis_n(md, 0x4338030, 6)},
            "inline_fixup_loop": {"fo": "0xf50d58", "va": hex(pe.fo_to_va(0xF50D58)), "special_comp_uid_check": pe.dis_one(md, 0xF50DE3)},
        },
        "members": xref_members,
        "internal_wire_slots": internal_slots,
    }
    # L2 vectorized column-by-column profile over all 77B (selector + 64B body + 12B identity)
    aw_byte_profile = []
    for b in range(77):
        col_b = A[:, b]
        aw_byte_profile.append({
            "row_off": b,
            "body_off": None if b == 0 else b - 1,
            "min": int(col_b.min()),
            "max": int(col_b.max()),
            "distinct": int(len(np.unique(col_b))),
            "zero_count": int((col_b == 0).sum()),
            "ff_count": int((col_b == 0xFF).sum()),
        })
    aw_l2_fk_cols = {
        f"body@{off}": l2_fk_candidate_matrix(AB[:, off:off + 4].copy().view("<i4").ravel(), ref_n, ref_uids)
        for off in (23, 27, 31, 41)
    }

    dom_tbl = {
        "rows": n,
        "client_payload_bytes": len(buf_c),
        "server_payload_bytes": len(buf_s),
        "client_eq_server": True,
        "l2_column_profile": {
            "row_stride_bytes": 77,
            "byte_summary_0_76": aw_byte_profile,
            "i32_fk_candidate_matrix": aw_l2_fk_cols,
            "ref_table_note": "t6=INJURY(115), t30=STARTING_INJURY(72,473), t5=CONTINENT(7), t10=NATION(251), t47=LOCAL_REGION(2,488), t25=COMP(7,047), t3=CLUB(84,259).",
        },
        "fields": dom_out,
        "internal_plus68_lcrg": int_68_fk,
    }
    return fm_tbl, xref_tbl, dom_tbl


# ---------------------------------------------------------------------------
# Table 8 — LANGUAGE (12 XML fields, 126 rows, lstr + 17B suf + 12B id + 1B sel)
# ---------------------------------------------------------------------------
def build_language(
    pe: MiniPE64,
    md: Cs,
    master: dict[str, Any],
    cli: dict[str, bytes],
    srv: dict[str, bytes],
    ref_n: dict[int, int],
    ref_uids: dict[int, set[int]],
    code_occ: Counter[str],
    db_ctx: list[dict[str, Any]],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    buf_c, buf_s = cli["table_8.dat"], srv["table_8.dat"]
    if buf_c != buf_s:
        raise RuntimeError("table_8 client != server")
    n = struct.unpack_from("<I", buf_c, 8)[0]
    pos = 13
    names: list[str] = []
    suf = np.empty((n, 29), dtype=np.uint8)
    for i in range(n):
        if buf_c[pos] != 0:
            raise RuntimeError(f"table_8 non-zero selector at row {i}")
        pos += 1
        sl = struct.unpack_from("<I", buf_c, pos)[0]
        pos += 4
        names.append(buf_c[pos:pos + sl].decode("utf-8"))
        pos += sl
        suf[i] = np.frombuffer(buf_c, dtype=np.uint8, offset=pos, count=29)
        pos += 29
    if pos != len(buf_c) - 9:
        raise RuntimeError(f"table_8 closure mismatch {pos} vs {len(buf_c) - 9}")
    ords = suf[:, 17:21].copy().view("<u4").ravel()
    dunis = suf[:, 21:25].copy().view("<u4").ravel()
    rduis = suf[:, 25:29].copy().view("<u4").ravel()
    if not np.array_equal(ords, np.arange(n, dtype=np.uint32)) or not np.array_equal(dunis, rduis):
        raise RuntimeError("table_8 identity check failed")

    LA_STATIC = {
        "Lnam": {"loc": "lstr@0", "w": None, "wt": "u32_len+utf8", "mem": "+0x18", "gcmp": 0x1038BBF, "gh": 0x1038BCB, "scmp": 0x103917C, "sh": 0x1039188, "rd": 0x3D546E4, "fx": None, "gchk": "0x18", "rchk": "+ 0x18", "str": True},
        "Linf": {"loc": "suf+1", "off": 1, "w": 1, "wt": "i8", "mem": "+0x3b", "gcmp": 0x1038BB3, "gh": 0x1038DA1, "scmp": 0x1039170, "sh": 0x10392E2, "rd": 0x3D54721, "fx": None, "gchk": "+ 0x3b", "rchk": "+ 0x3b", "rng": (0, 20, None)},
        "Ldff": {"loc": "suf+2", "off": 2, "w": 1, "wt": "i8", "mem": "+0x3c", "gcmp": 0x1038B48, "gh": 0x1038B54, "scmp": 0x1039143, "sh": 0x103914F, "rd": 0x3D54742, "fx": None, "gchk": "+ 0x3c", "rchk": "+ 0x3c", "rng": (0, 20, None)},
        "Lnat": {"loc": "suf+9", "off": 9, "w": 4, "wt": "i32_ordinal_ref:table_10", "mem": "+0x28", "gcmp": 0x1038A37, "gh": 0x1038CC1, "scmp": 0x103921F, "sh": 0x103930D, "rd": 0x3D547B6, "fx": 0x3D550A0, "gchk": "+ 0x28", "rchk": "+ 0x28", "fk": 10},
        "Lfam": {"loc": "suf+3", "off": 3, "w": 2, "wt": "i16_enum", "mem": "+0x34", "gcmp": 0x1038C4A, "gh": 0x1038DFD, "scmp": 0x10391F1, "sh": 0x10392F7, "rd": 0x3D5475F, "fx": None, "gchk": "+ 0x34", "rchk": "+ 0x34", "enum": "Lfam"},
        "Lgro": {"loc": "suf+5", "off": 5, "w": 2, "wt": "i16_enum", "mem": "+0x36", "gcmp": 0x1038C56, "gh": 0x1038C62, "scmp": 0x10391FD, "sh": 0x1039209, "rd": 0x3D5477C, "fx": None, "gchk": "+ 0x36", "rchk": "+ 0x36", "enum": "Lgro"},
        "Lsub": {"loc": "suf+7", "off": 7, "w": 2, "wt": "i16_enum", "mem": "+0x38", "gcmp": 0x1038A43, "gh": 0x1038CDE, "scmp": 0x103922B, "sh": 0x1039237, "rd": 0x3D54799, "fx": None, "gchk": "+ 0x38", "rchk": "+ 0x38", "enum": "Lsub"},
    }

    xml_fields = master["entities"]["language.xml"][0]["fields"]
    schema_out: list[dict[str, Any]] = []
    xref_members: list[dict[str, Any]] = []
    dom_out: dict[str, Any] = {}

    for idx, f in enumerate(xml_fields):
        fid = f["field"]
        rec: dict[str, Any] = {
            "index": idx, "field": fid, "name": f.get("name"), "schema_type": f.get("type"),
            "master_occ": code_occ[fid], "prior_refs": ["t74/E115", "t76b(absorbed)"],
        }
        if fid == "duni":
            g_ins = check_4cc_at(pe, md, 0xFE3912, "duni")
            rec.update({
                "grade": "L3", "scope": "client+server", "wire_loc": "suf+21..24", "width": 4, "wire_type": "u32",
                "member_off": "+0x0c", "getter_fo": "0xfe3912", "setter_fo": None, "reader_fo": "0x3c600f0",
                "domain": {"rows": n, "unique": n, "eq_rdui_raw": n, "violations": 0},
            })
            xref_members.append({"field": fid, "member_off": "+0x0c", "getter_cmp": g_ins, "reader": pe.dis_one(md, 0x3C600F0)})
            dom_out[fid] = rec["domain"]
        elif fid == "rdui":
            g_ins = check_4cc_at(pe, md, 0xFE3862, "rdui")
            rec.update({
                "grade": "held", "scope": "client+server", "wire_loc": "suf+25..28", "width": 4, "wire_type": "u32",
                "member_off": "+0x10", "getter_fo": "0xfe3862", "setter_fo": None, "reader_fo": "0x3c600f0",
                "prior_refs": ["t74/E115", "fm24_dump:language.rdui_suffix@17(actually row_ordinal@suf+17)"],
                "hold_reason": "DATABASE_RECORD::get 0xfe38a2 suppresses output whenever [+0x0c]==[+0x10]; 126/126 rows suppressed. Note fm24_dump 'rdui_suffix@17' is row ordinal@suf+17..20.",
                "first_counterexample": {"row": 0, "name": names[0], "duni": int(dunis[0]), "rdui_raw": int(rduis[0]), "reason": "suppressed_eq_duni"},
                "domain": {"rows": n, "suppressed": n, "live": 0},
            })
            xref_members.append({"field": fid, "member_off": "+0x10", "getter_cmp": g_ins, "reader": pe.dis_one(md, 0x3C600F0)})
            dom_out[fid] = rec["domain"]
        elif fid in ("NDBC", "FDBC"):
            rec.update({"grade": "editor_metadata", "scope": "non_wire", "getter_fo": None, "setter_fo": None,
                        "note": "Editor change-tracking counter; 0 hits in LANGUAGE::get/DATABASE_RECORD::get."})
        elif fid == "dbnm":
            g_ins = check_4cc_at(pe, md, 0x1038A4F, "dbnm")
            rec.update({"grade": "non_wire_computed", "scope": "non_wire", "getter_fo": "0x1038a5b", "setter_fo": None,
                        "note": "LANGUAGE::get 0x1038a5b returns +0x18 (Lnam) with special fallback check on +0x30 in {0xf4241, 0xf4244}."})
            xref_members.append({"field": fid, "getter_cmp": g_ins, "getter_handler": pe.dis_one(md, 0x1038A5B), "classification": "non_wire_computed"})
        elif fid in LA_STATIC:
            st = LA_STATIC[fid]
            g_cmp = check_4cc_at(pe, md, st["gcmp"], fid)
            s_cmp = check_4cc_at(pe, md, st["scmp"], fid)
            g_h = check_ins_contains(pe, md, st["gh"], st["gchk"])
            s_h = pe.dis_one(md, st["sh"])
            r_ins = check_ins_contains(pe, md, st["rd"], st["rchk"])
            fx_ins = pe.dis_one(md, st["fx"]) if st["fx"] else None

            first_ce = None
            hold_reason = None
            if st.get("str"):
                dom = {
                    "rows": n, "non_empty": sum(1 for x in names if x), "utf8_errors": 0,
                    "min_len": min(len(x.encode("utf-8")) for x in names),
                    "max_len": max(len(x.encode("utf-8")) for x in names),
                    "samples": [{"row": i, "duni": int(dunis[i]), "value": names[i]} for i in (0, 3, 7)],
                    "violations": 0,
                }
                grade = "L3"
            elif "fk" in st:
                col = suf[:, st["off"]:st["off"] + 4].copy().view("<i4").ravel()
                dom = fk_stats_vec(col, st["fk"], ref_n, ref_uids)
                # Named cross-checks: English (row 7) -> 139, Chinese (row 3) -> 55
                dom["named_anchors"] = {
                    "Chinese_row3_Lnat": int(col[3]),
                    "English_row7_Lnat": int(col[7]),
                }
                grade = "L3" if dom["violations"] == 0 else "held"
            elif "rng" in st:
                mn, mx, ncond = st["rng"]
                col = suf[:, st["off"]].view(np.int8)
                dom, first_ce = int_range_stats_vec(col, mn, mx, dunis, ncond, names)
                grade = "L3" if dom["violations"] == 0 else "held"
            elif "enum" in st:
                col = suf[:, st["off"]:st["off"] + 2].copy().view("<i2").ravel()
                allowed = parse_enum_ids(master, st["enum"])
                dom, first_ce = enum_stats_vec(col, allowed, dunis, names)
                if dom["violations"] == 0:
                    grade = "L3"
                else:
                    grade = "held"
                    hold_reason = (
                        f"Exact getter ({hex(st['gh'])} movsx) and setter ({hex(st['sh'])}) map to {st['mem']} ({st['loc']}), "
                        f"but {dom['violations']}/{n} rows fall outside master.enums['{st['enum']}'] "
                        f"(out-of-enum: {dom['out_of_enum_histogram']}); getter performs no suppression/clamping."
                    )
            else:
                raise RuntimeError(f"unhandled lang {fid}")

            rec.update({
                "grade": grade, "scope": "client+server",
                "wire_loc": st["loc"], "width": st["w"], "wire_type": st["wt"],
                "member_off": st["mem"],
                "getter_fo": hex(st["gh"]), "setter_fo": hex(st["sh"]), "reader_fo": hex(st["rd"]),
                "fixup_fo": hex(st["fx"]) if st["fx"] else None,
                "domain": dom,
            })
            if fid in ("Lnam", "Lnat"):
                rec["gate1_note"] = "Code appears in 2 master.json entities (language.xml & local region.xml); uniquely scoped via LANGUAGE vtable 0x141888db8."
            if hold_reason:
                rec["hold_reason"] = hold_reason
                rec["first_counterexample"] = first_ce
            xref_members.append({
                "field": fid, "grade": grade, "wire_loc": st["loc"], "width": st["w"], "member_off": st["mem"],
                "getter_cmp": g_cmp, "getter_handler": g_h,
                "setter_cmp": s_cmp, "setter_handler": s_h,
                "reader_sink": r_ins, "fixup": fx_ins,
            })
            dom_out[fid] = dom
        schema_out.append(rec)

    i30 = suf[:, 13:17].copy().view("<i4").ravel()
    diff_30 = [{"row": i, "name": names[i], "plus30": int(i30[i]), "duni": int(dunis[i])} for i in range(n) if int(i30[i]) != int(dunis[i])]
    internal_slots = [
        {"wire_loc": "suf+0", "width": 1, "member_off": "+0x3a", "reader_fo": "0x3d54700", "values": {"const": 0, "rows": n}},
        {"wire_loc": "suf+13..16", "width": 4, "member_off": "+0x30", "reader_fo": "0x3d547ee", "note": "ver>=0xde7 legacy language ID passed to 0x1037880; equals duni on 121/126 rows, differs on 5 late-added languages", "diff_from_duni": diff_30},
        {"wire_loc": "suf+17..20", "width": 4, "member_off": "+0x08", "reader_fo": "0x3c600f0", "note": "row ordinal (0..125); fm24_dump label 'rdui_suffix@17' points here"},
    ]
    fm_tbl = {
        "table_id": 8, "xml": "language.xml", "rows": n, "client_eq_server": True,
        "frame": {"native": f"13 + {len(buf_c) - 22} + 9 = {len(buf_c)}", "grammar": "1B sel + lstr(Lnam) + 17B suffix + 12B identity"},
        "schema_fields": schema_out,
        "internal_wire_slots": internal_slots,
    }
    xref_tbl = {
        "task": "t83",
        "class": verify_class_static(pe, md, 8),
        "db_context_refs": [r for r in db_ctx if r["table_id"] in (8, 10)],
        "helpers": {
            "lstr_reader": {"thunk_fo": "0x814110", "real_fo": hex(pe.unwrap_thunk(md, 0x814110))},
            "post_read_lang_id_map": {"fo": "0x1037880", "va": hex(pe.fo_to_va(0x1037880))},
            "identity_reader": {"thunk_fo": "0xfae340", "real_fo": "0x3c600f0"},
        },
        "members": xref_members,
        "internal_wire_slots": internal_slots,
    }
    # L2 vectorized profile over 17B suffix + 12B identity (+ trailing 1B marker/next-selector = 30B)
    la_suf_byte_profile = []
    for b in range(29):
        col_b = suf[:, b]
        la_suf_byte_profile.append({
            "suf_off": b,
            "region": "suffix_17B" if b < 17 else "identity_12B",
            "min": int(col_b.min()),
            "max": int(col_b.max()),
            "distinct": int(len(np.unique(col_b))),
            "zero_count": int((col_b == 0).sum()),
            "ff_count": int((col_b == 0xFF).sum()),
        })
    la_l2_fk_cols = {
        "suf+9_Lnat": l2_fk_candidate_matrix(suf[:, 9:13].copy().view("<i4").ravel(), ref_n, ref_uids),
        "suf+13_int_plus30": l2_fk_candidate_matrix(suf[:, 13:17].copy().view("<i4").ravel(), ref_n, ref_uids),
    }

    dom_tbl = {
        "rows": n, "client_payload_bytes": len(buf_c), "server_payload_bytes": len(buf_s),
        "client_eq_server": True,
        "l2_column_profile": {
            "suffix_plus_identity_bytes": 29,
            "trailing_selector_or_footer0_all_zero": True,
            "byte_summary_0_28": la_suf_byte_profile,
            "i32_fk_candidate_matrix": la_l2_fk_cols,
        },
        "fields": dom_out, "internal_plus30_diffs": diff_30,
    }
    return fm_tbl, xref_tbl, dom_tbl


# ---------------------------------------------------------------------------
# Table 18 — DERBY (22 XML fields, 1,567 rows, 4 lstr + 36B/42B num + 12B id)
# ---------------------------------------------------------------------------
def build_derby(
    pe: MiniPE64,
    md: Cs,
    master: dict[str, Any],
    cli: dict[str, bytes],
    srv: dict[str, bytes],
    ref_n: dict[int, int],
    ref_uids: dict[int, set[int]],
    code_occ: Counter[str],
    db_ctx: list[dict[str, Any]],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    def parse_side(buf: bytes, is_srv: bool) -> tuple[list[list[str]], np.ndarray]:
        n = struct.unpack_from("<I", buf, 8)[0]
        pos = 13
        strs: list[list[str]] = [[], [], [], []]
        nlen = 42 if is_srv else 36
        nums = np.empty((n, nlen + 12), dtype=np.uint8)
        for i in range(n):
            if buf[pos] != 0:
                raise RuntimeError(f"derby sel!=0 at row {i}")
            pos += 1
            for k in range(4):
                sl = struct.unpack_from("<I", buf, pos)[0]
                pos += 4
                strs[k].append(buf[pos:pos + sl].decode("utf-8"))
                pos += sl
            nums[i] = np.frombuffer(buf, dtype=np.uint8, offset=pos, count=nlen + 12)
            pos += nlen + 12
        if pos != len(buf) - 9:
            raise RuntimeError(f"derby closure failed {pos} vs {len(buf) - 9}")
        return strs, nums

    str_c, num_c = parse_side(cli["table_18.dat"], False)
    str_s, num_s = parse_side(srv["table_18.dat"], True)
    n = len(str_c[0])
    if str_c != str_s:
        raise RuntimeError("derby strings client!=server")
    if not np.array_equal(num_c[:, :28], num_s[:, :28]):
        raise RuntimeError("derby num[0:28] client!=server")
    if not np.array_equal(num_c[:, 28:36], num_s[:, 34:42]):
        raise RuntimeError("derby num tail client!=server")
    if not np.array_equal(num_c[:, 36:48], num_s[:, 42:54]):
        raise RuntimeError("derby id client!=server")

    ords = num_s[:, 42:46].copy().view("<u4").ravel()
    dunis = num_s[:, 46:50].copy().view("<u4").ravel()
    rduis = num_s[:, 50:54].copy().view("<u4").ravel()
    if not np.array_equal(ords, np.arange(n, dtype=np.uint32)) or not np.array_equal(dunis, rduis):
        raise RuntimeError("derby id invariant failed")

    # Verify server-only 6B gate instruction at 0x3d00aae
    srv_gate_ins = check_ins_contains(pe, md, 0x3D00AAE, "test")

    jt_get = decode_switch_targets(pe, 0xFFDF00, "Dfma", [0, 2, 3, 18])
    jt_set = decode_switch_targets(pe, 0xFFE4BC, "Dfma", [0, 2, 3, 18])

    DR_STATIC: dict[str, dict[str, Any]] = {
        "Dnam": {"scope": "client+server", "loc": "str0", "c_off": None, "s_off": None, "w": None, "wt": "u32_len+utf8", "mem": "+0x18", "gcmp": 0xFFD2B3, "gh": 0xFFD613, "scmp": 0xFFE173, "sh": 0xFFE17F, "rd": 0x3D00966, "fx": None, "gchk": "0x18", "rchk": "+ 0x18", "str_idx": 0},
        "Dsnm": {"scope": "client+server", "loc": "str1", "c_off": None, "s_off": None, "w": None, "wt": "u32_len+utf8", "mem": "+0x20", "gcmp": 0xFFD42C, "gh": 0xFFD6C1, "scmp": 0xFFE107, "sh": 0xFFE113, "rd": 0x3D00982, "fx": None, "gchk": "0x20", "rchk": "+ 0x20", "str_idx": 1},
        "Dasn": {"scope": "client+server", "loc": "str2", "c_off": None, "s_off": None, "w": None, "wt": "u32_len+utf8", "mem": "+0x28", "gcmp": 0xFFD20D, "gh": 0xFFD219, "scmp": 0xFFE06F, "sh": 0xFFE07B, "rd": 0x3D0099E, "fx": None, "gchk": "0x28", "rchk": "+ 0x28", "str_idx": 2},
        "Danm": {"scope": "client+server", "loc": "str3", "c_off": None, "s_off": None, "w": None, "wt": "u32_len+utf8", "mem": "+0x30", "gcmp": 0xFFD201, "gh": 0xFFD556, "scmp": 0xFFE063, "sh": 0xFFE312, "rd": 0x3D009BA, "fx": None, "gchk": "0x30", "rchk": "+ 0x30", "str_idx": 3},
        "Dfmd": {"scope": "client+server", "loc": "num@0..3", "c_off": 0, "s_off": 0, "w": 4, "wt": "u32_packed_date", "mem": "+0x60", "gcmp": None, "gh": 0xFFD860, "scmp": None, "sh": 0xFFE1D0, "rd": 0x3D009D3, "fx": None, "gchk": "+ 0x60", "rchk": "+ 0x60", "date": True, "jt": True},
        "Dtm1": {"scope": "client+server", "loc": "num@4..7", "c_off": 4, "s_off": 4, "w": 4, "wt": "i32_ordinal_ref:table_24", "mem": "+0x40", "gcmp": 0xFFD438, "gh": 0xFFD444, "scmp": 0xFFE01F, "sh": 0xFFE2B0, "rd": 0x3D009EA, "fx": 0x3D00FC0, "gchk": "+ 0x40", "rchk": "+ 0x40", "fk": 24},
        "Dtm2": {"scope": "client+server", "loc": "num@8..11", "c_off": 8, "s_off": 8, "w": 4, "wt": "i32_ordinal_ref:table_24", "mem": "+0x48", "gcmp": 0xFFD378, "gh": 0xFFD695, "scmp": 0xFFE02B, "sh": 0xFFE2E1, "rd": 0x3D00A0B, "fx": 0x3D00FC0, "gchk": "+ 0x48", "rchk": "+ 0x48", "fk": 24},
        "Dfmc": {"scope": "client+server", "loc": "num@12..15", "c_off": 12, "s_off": 12, "w": 4, "wt": "i32_ordinal_ref:table_25", "mem": "+0x50", "gcmp": None, "gh": 0xFFD81E, "scmp": None, "sh": 0xFFE19F, "rd": 0x3D00A28, "fx": 0x3D00FC0, "gchk": "+ 0x50", "rchk": "+ 0x50", "fk": 25, "jt": True},
        "Dfms": {"scope": "client+server", "loc": "num@16..19", "c_off": 16, "s_off": 16, "w": 4, "wt": "i32_ordinal_ref:table_21", "mem": "+0x58", "gcmp": None, "gh": 0xFFD8D9, "scmp": None, "sh": 0xFFE242, "rd": 0x3D00A45, "fx": 0x3BF6EC0, "gchk": "+ 0x58", "rchk": "+ 0x58", "fk": 21, "jt": True},
        "Dfma": {"scope": "client+server", "loc": "num@20..23", "c_off": 20, "s_off": 20, "w": 4, "wt": "i32_optional_lt0_null", "mem": "+0x64", "gcmp": None, "gh": 0xFFD34C, "scmp": None, "sh": 0xFFDF92, "rd": 0x3D00A62, "fx": None, "gchk": "+ 0x64", "rchk": "+ 0x64", "rng": (0, 200000, "lt0"), "jt": True},
        "D1tw": {"scope": "server_only", "loc": "s@28..29", "c_off": None, "s_off": 28, "w": 2, "wt": "i16_optional_lt0_null", "mem": "+0x70", "gcmp": 0xFFD1F5, "gh": 0xFFD534, "scmp": 0xFFE09B, "sh": 0xFFE379, "rd": 0x3D00AB6, "fx": None, "gchk": "+ 0x70", "rchk": "+ 0x70", "rng": (0, 10000, "lt0")},
        "D1td": {"scope": "server_only", "loc": "s@30..31", "c_off": None, "s_off": 30, "w": 2, "wt": "i16_optional_lt0_null", "mem": "+0x72", "gcmp": 0xFFD3F2, "gh": 0xFFD5D8, "scmp": 0xFFDFD2, "sh": 0xFFE287, "rd": 0x3D00AD3, "fx": None, "gchk": "+ 0x72", "rchk": "+ 0x72", "rng": (0, 10000, "lt0")},
        "D1tl": {"scope": "server_only", "loc": "s@32..33", "c_off": None, "s_off": 32, "w": 2, "wt": "i16_optional_lt0_null", "mem": "+0x74", "gcmp": 0xFFD3FE, "gh": 0xFFD40A, "scmp": 0xFFDFDE, "sh": 0xFFDFEA, "rd": 0x3D00AF0, "fx": None, "gchk": "+ 0x74", "rchk": "+ 0x74", "rng": (0, 10000, "lt0")},
        "Dfg1": {"scope": "client+server", "loc": "c@28/s@34", "c_off": 28, "s_off": 34, "w": 1, "wt": "i8_optional_lt0_null", "mem": "+0x76", "gcmp": 0xFFD4FA, "gh": 0xFFD8F6, "scmp": 0xFFE133, "sh": 0xFFE3B6, "rd": 0x3D00B0D, "fx": None, "gchk": "+ 0x76", "rchk": "+ 0x76", "rng": (0, 100, "lt0")},
        "Dfg2": {"scope": "client+server", "loc": "c@29/s@35", "c_off": 29, "s_off": 35, "w": 1, "wt": "i8_optional_lt0_null", "mem": "+0x77", "gcmp": 0xFFD506, "gh": 0xFFD512, "scmp": 0xFFE13F, "sh": 0xFFE14B, "rd": 0x3D00B2E, "fx": None, "gchk": "+ 0x77", "rchk": "+ 0x77", "rng": (0, 100, "lt0")},
        "Dwdr": {"scope": "client+server", "loc": "c@34/s@40", "c_off": 34, "s_off": 40, "w": 1, "wt": "u8", "mem": "+0x7c", "gcmp": 0xFFD384, "gh": 0xFFD390, "scmp": 0xFFE037, "sh": 0xFFE043, "rd": 0x3D00BD3, "fx": None, "gchk": "+ 0x7c", "rchk": "+ 0x7c", "rng": (0, 200, None)},
        "Dntr": {"scope": "client+server", "loc": "c@35/s@41", "c_off": 35, "s_off": 41, "w": 1, "wt": "u8", "mem": "+0x7d", "gcmp": 0xFFD2BF, "gh": 0xFFD2CB, "scmp": 0xFFE0FB, "sh": 0xFFE3A2, "rd": 0x3D00BF4, "fx": None, "gchk": "+ 0x7d", "rchk": "+ 0x7d", "rng": (0, 200, None)},
    }

    xml_fields = master["entities"]["derby.xml"][0]["fields"]
    schema_out: list[dict[str, Any]] = []
    xref_members: list[dict[str, Any]] = []
    dom_out: dict[str, Any] = {}

    for idx, f in enumerate(xml_fields):
        fid = f["field"]
        rec: dict[str, Any] = {
            "index": idx, "field": fid, "name": f.get("name"), "schema_type": f.get("type"),
            "master_occ": code_occ[fid], "prior_refs": ["t74/E115", "t76c/E118"],
        }
        if fid == "duni":
            g_ins = check_4cc_at(pe, md, 0xFE3912, "duni")
            rec.update({
                "grade": "L3", "scope": "client+server", "client_num_off": 40, "server_num_off": 46, "width": 4, "wire_type": "u32",
                "member_off": "+0x0c", "getter_fo": "0xfe3912", "setter_fo": None, "reader_fo": "0x3c600f0",
                "domain": {"rows": n, "unique": n, "eq_rdui_raw": n, "violations": 0},
            })
            xref_members.append({"field": fid, "member_off": "+0x0c", "getter_cmp": g_ins, "reader": pe.dis_one(md, 0x3C600F0)})
            dom_out[fid] = rec["domain"]
        elif fid == "rdui":
            g_ins = check_4cc_at(pe, md, 0xFE3862, "rdui")
            rec.update({
                "grade": "held", "scope": "client+server", "client_num_off": 44, "server_num_off": 50, "width": 4, "wire_type": "u32",
                "member_off": "+0x10", "getter_fo": "0xfe3862", "setter_fo": None, "reader_fo": "0x3c600f0",
                "hold_reason": "DATABASE_RECORD::get 0xfe38a2 suppresses output whenever [+0x0c]==[+0x10]; 1,567/1,567 rows suppressed (0 live outputs).",
                "first_counterexample": {"row": 0, "name": str_s[0][0], "duni": int(dunis[0]), "rdui_raw": int(rduis[0]), "reason": "suppressed_eq_duni"},
                "domain": {"rows": n, "suppressed": n, "live": 0},
            })
            xref_members.append({"field": fid, "member_off": "+0x10", "getter_cmp": g_ins, "reader": pe.dis_one(md, 0x3C600F0)})
            dom_out[fid] = rec["domain"]
        elif fid in ("NDBC", "FDBC"):
            rec.update({"grade": "editor_metadata", "scope": "non_wire", "getter_fo": None, "setter_fo": None,
                        "note": "Editor change-tracking counter; 0 hits in DERBY::get/DATABASE_RECORD::get."})
        elif fid == "dbnm":
            g_ins = check_4cc_at(pe, md, 0xFFD46C, "dbnm")
            rec.update({"grade": "non_wire_computed", "scope": "non_wire", "getter_fo": "0xffd478", "setter_fo": None,
                        "note": "DERBY::get 0xffd478 returns +0x18 (Dnam)."})
            xref_members.append({"field": fid, "getter_cmp": g_ins, "getter_handler": pe.dis_one(md, 0xFFD478), "classification": "non_wire_computed"})
        elif fid in DR_STATIC:
            st = DR_STATIC[fid]
            g_cmp = check_4cc_at(pe, md, st["gcmp"], fid) if st["gcmp"] else jt_get[fid]
            s_cmp = check_4cc_at(pe, md, st["scmp"], fid) if st["scmp"] else jt_set[fid]
            g_h = check_ins_contains(pe, md, st["gh"], st["gchk"])
            s_h = pe.dis_one(md, st["sh"])
            r_ins = check_ins_contains(pe, md, st["rd"], st["rchk"])
            fx_ins = pe.dis_one(md, st["fx"]) if st["fx"] else None

            if "str_idx" in st:
                svec = str_s[st["str_idx"]]
                dom = {
                    "rows": n, "non_empty": sum(1 for x in svec if x), "empty": sum(1 for x in svec if not x),
                    "utf8_errors": 0, "violations": 0,
                    "samples": [{"row": i, "duni": int(dunis[i]), "value": svec[i]} for i in (0, 85, 388, 395, 694) if svec[i]][:4],
                }
                grade = "L3"
            elif st.get("date"):
                col = num_s[:, st["s_off"]:st["s_off"] + 4].copy().view("<u4").ravel()
                dom = check_dates_vec(col)
                grade = "L3" if dom["violations"] == 0 else "held"
            elif "fk" in st:
                col = num_s[:, st["s_off"]:st["s_off"] + 4].copy().view("<i4").ravel()
                dom = fk_stats_vec(col, st["fk"], ref_n, ref_uids)
                grade = "L3" if dom["violations"] == 0 else "held"
            elif "rng" in st:
                mn, mx, ncond = st["rng"]
                so, w = st["s_off"], st["w"]
                if w == 4:
                    col = num_s[:, so:so + 4].copy().view("<i4").ravel()
                elif w == 2:
                    col = num_s[:, so:so + 2].copy().view("<i2").ravel()
                else:
                    col = num_s[:, so].view(np.int8) if ncond == "lt0" else num_s[:, so]
                dom, _ = int_range_stats_vec(col, mn, mx, dunis, ncond, str_s[0])
                grade = "L3" if dom["violations"] == 0 else "held"
            else:
                raise RuntimeError(f"unhandled derby {fid}")

            rec.update({
                "grade": grade, "scope": st["scope"],
                "wire_loc": st["loc"], "client_num_off": st["c_off"], "server_num_off": st["s_off"],
                "width": st["w"], "wire_type": st["wt"], "member_off": st["mem"],
                "getter_fo": hex(st["gh"]), "setter_fo": hex(st["sh"]), "reader_fo": hex(st["rd"]),
                "fixup_fo": hex(st["fx"]) if st["fx"] else None,
                "domain": dom,
            })
            if fid in ("Dtm1", "Dtm2"):
                rec["t76c_reconciliation"] = "t76c L2 fitted club(84,259) ordinals; L3 static proves DERBY::fixup (0x3d00fc0 -> 0x3bf3460) binds [db+0x98] = table_24 TEAM (84,507 rows) and DERBY::get emits 4CC 'Ttea'."
            elif fid in ("D1tw", "D1td", "D1tl"):
                rec["t76c_reconciliation"] = "t76c E118 established 6B server-only delta = {D1tw,D1td,D1tl} as unordered group; L3 static proves exact order D1tw@s28(+0x70), D1td@s30(+0x72), D1tl@s32(+0x74) gated by test bpl,bpl at 0x3d00aae."
            elif fid in ("Dwdr", "Dntr"):
                rec["t76c_reconciliation"] = "t76c REPORT noted client@34..35 (slots_client_18.json had off-by-2 typo '36'); L3 static proves Dwdr@c34/s40(+0x7c), Dntr@c35/s41(+0x7d)."
            elif fid in ("Dasn", "Danm"):
                rec["t74_reconciliation"] = "DERBY::read ALWAYS reads 4 lstrings in exact wire order Dnam, Dsnm, Dasn, Danm (Dasn precedes Danm); t74 k in {2,4} arose from empty len=0 strings on 1,446/1,567 rows."

            xref_members.append({
                "field": fid, "grade": grade, "scope": st["scope"], "wire_loc": st["loc"], "width": st["w"], "member_off": st["mem"],
                "getter_dispatch": g_cmp, "getter_handler": g_h,
                "setter_dispatch": s_cmp, "setter_handler": s_h,
                "reader_sink": r_ins, "fixup": fx_ins,
            })
            dom_out[fid] = dom
        schema_out.append(rec)

    rpdr_col = num_s[:, 24:28].copy().view("<i4").ravel()
    internal_slots = [
        {"wire_loc": "num@24..27", "width": 4, "member_off": "+0x68", "internal_4cc": "rpdr", "getter_fo": "0xffd743", "reader_fo": "0x3d00a7f", "fixup_target": "table_25(COMP)", "values": {"const": -1, "rows": n}},
        {"wire_loc": "c@30..33/s@36..39", "width": 4, "member_off": "+0x78..+0x7b", "reader_fo": "0x3d00b4f", "values": {"const": 0, "rows": n}},
        {"wire_loc": "c@36..39/s@42..45", "width": 4, "member_off": "+0x08", "reader_fo": "0x3c600f0", "note": "row ordinal (0..1566)"},
    ]
    fm_tbl = {
        "table_id": 18, "xml": "derby.xml", "rows": n, "client_eq_server": False,
        "server_delta": {"bytes_per_row": 6, "gate_fo": "0x3d00aae", "fields": ["D1tw@s28", "D1td@s30", "D1tl@s32"]},
        "frame": {
            "client_bytes": len(cli["table_18.dat"]), "server_bytes": len(srv["table_18.dat"]),
            "delta_total_bytes": len(srv["table_18.dat"]) - len(cli["table_18.dat"]),
            "grammar": "1B sel + 4 lstr(Dnam,Dsnm,Dasn,Danm) + 36B(client)/42B(server) num + 12B identity",
        },
        "schema_fields": schema_out,
        "internal_wire_slots": internal_slots,
    }
    xref_tbl = {
        "task": "t83",
        "class": verify_class_static(pe, md, 18),
        "db_context_refs": [r for r in db_ctx if r["table_id"] in (18, 21, 24, 25)],
        "server_6b_gate": srv_gate_ins,
        "members": xref_members,
        "internal_wire_slots": internal_slots,
    }
    dom_tbl = {
        "rows": n, "client_payload_bytes": len(cli["table_18.dat"]), "server_payload_bytes": len(srv["table_18.dat"]),
        "shared_bytes_identical": True, "server_only_delta_bytes": 6,
        "rpdr_all_minus1": bool(np.all(rpdr_col == -1)),
        "fields": dom_out,
    }
    return fm_tbl, xref_tbl, dom_tbl


# ---------------------------------------------------------------------------
# Table 27 — WEATHER (94 XML fields, 334 rows, lstr + 3B + 4*23B + 12B id)
# ---------------------------------------------------------------------------
def build_weather(
    pe: MiniPE64,
    md: Cs,
    master: dict[str, Any],
    cli: dict[str, bytes],
    srv: dict[str, bytes],
    code_occ: Counter[str],
    db_ctx: list[dict[str, Any]],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    buf_c, buf_s = cli["table_27.dat"], srv["table_27.dat"]
    if buf_c != buf_s:
        raise RuntimeError("table_27 client != server")
    n = struct.unpack_from("<I", buf_c, 8)[0]
    pos = 13
    names: list[str] = []
    mid = np.empty((n, 107), dtype=np.uint8)
    for i in range(n):
        if buf_c[pos] != 0:
            raise RuntimeError(f"weather sel!=0 at row {i}")
        pos += 1
        sl = struct.unpack_from("<I", buf_c, pos)[0]
        pos += 4
        names.append(buf_c[pos:pos + sl].decode("utf-8"))
        pos += sl
        mid[i] = np.frombuffer(buf_c, dtype=np.uint8, offset=pos, count=107)
        pos += 107
    if pos != len(buf_c) - 9:
        raise RuntimeError(f"weather closure failed {pos} vs {len(buf_c) - 9}")
    if not np.all(mid[:, :3] == 0):
        raise RuntimeError("weather mid[0:3] not all zero")
    ords = mid[:, 95:99].copy().view("<u4").ravel()
    dunis = mid[:, 99:103].copy().view("<u4").ravel()
    rduis = mid[:, 103:107].copy().view("<u4").ravel()
    if not np.array_equal(ords, np.arange(n, dtype=np.uint32)) or not np.array_equal(dunis, rduis):
        raise RuntimeError("weather identity check failed")

    # Decode WEATHER::get & WEATHER::set & WEATHER_SEASON::get jump tables directly from PE!
    w_get_jts: dict[str, dict[str, Any]] = {}
    for tbl_fo, base_cc, idxs in [
        (0x158ECCC, "w0t0", [0, 1, 2, 3, 4, 5, 6, 7, 53, 70]),
        (0x158EE10, "w1t0", [0, 1, 2, 3, 4, 5, 6, 7, 53, 70]),
        (0x158EF54, "w2t0", [0, 1, 2, 3, 4, 5, 6, 7, 53, 70]),
        (0x158F098, "w3t0", [0, 1, 2, 3, 4, 5, 6, 7, 53, 70]),
        (0x158ECB8, "w0p0", [0, 1, 2, 3, 4]),
        (0x158EDFC, "w1p0", [0, 1, 2, 3, 4]),
        (0x158EF40, "w2p0", [0, 1, 2, 3, 4]),
        (0x158F084, "w3p0", [0, 1, 2, 3, 4]),
        (0x158EDE8, "w0w0", [0, 1, 2, 3, 4]),
        (0x158EF2C, "w1w0", [0, 1, 2, 3, 4]),
        (0x158F070, "w2w0", [0, 1, 2, 3, 4]),
        (0x158F1B4, "w3w0", [0, 1, 2, 3, 4]),
    ]:
        w_get_jts.update(decode_switch_targets(pe, tbl_fo, base_cc, idxs))

    w_set_jts: dict[str, dict[str, Any]] = {}
    for tbl_fo, base_cc, idxs in [
        (0x1590B98, "w0t0", [0, 1, 2, 3, 4, 5, 6, 7, 53, 70]),
        (0x1590CDC, "w1t0", [0, 1, 2, 3, 4, 5, 6, 7, 53, 70]),
        (0x1590E20, "w2t0", [0, 1, 2, 3, 4, 5, 6, 7, 53, 70]),
        (0x1590F64, "w3t0", [0, 1, 2, 3, 4, 5, 6, 7, 53, 70]),
        (0x1590B84, "w0p0", [0, 1, 2, 3, 4]),
        (0x1590CC8, "w1p0", [0, 1, 2, 3, 4]),
        (0x1590E0C, "w2p0", [0, 1, 2, 3, 4]),
        (0x1590F50, "w3p0", [0, 1, 2, 3, 4]),
        (0x1590CB4, "w0w0", [0, 1, 2, 3, 4]),
        (0x1590DF8, "w1w0", [0, 1, 2, 3, 4]),
        (0x1590F3C, "w2w0", [0, 1, 2, 3, 4]),
        (0x1591080, "w3w0", [0, 1, 2, 3, 4]),
    ]:
        w_set_jts.update(decode_switch_targets(pe, tbl_fo, base_cc, idxs))

    # WEATHER_SEASON::get (0x158f1d0) inner 4CC -> (season_rel_off, wire_rel_off, width, inner_handler_fo, reader_lea_fo)
    SEASON_SUB = {
        "sd": (0x00, 0, 2, "stdy", 0x158F377, 0x158BA27),
        "w0": (0x02, 2, 1, "win0", 0x158F30C, 0x158BA47),
        "w1": (0x03, 3, 1, "win1", 0x158F8FC, 0x158BA64),
        "w2": (0x04, 4, 1, "win2", 0x158F95B, 0x158BA81),
        "w3": (0x05, 5, 1, "win3", 0x158F9BA, 0x158BAA2),
        "w4": (0x06, 6, 1, "win4", 0x158FA19, 0x158BAC3),
        "p0": (0x07, 7, 1, "pre0", 0x158F28E, 0x158BAE4),
        "p1": (0x08, 8, 1, "pre1", 0x158F780, 0x158BB05),
        "p2": (0x09, 9, 1, "pre2", 0x158F7DF, 0x158BB26),
        "p3": (0x0A, 10, 1, "pre3", 0x158F83E, 0x158BB47),
        "p4": (0x0B, 11, 1, "pre4", 0x158F89D, 0x158BB68),
        "te": (0x0C, 12, 1, "teme", 0x158F6C2, 0x158BB89),
        "tv": (0x0D, 13, 1, "temv", 0x158F721, 0x158BBAA),
        "t0": (0x0E, 14, 1, "tem0", 0x158F210, 0x158BBCB),
        "t1": (0x0F, 15, 1, "tem1", 0x158F429, 0x158BBEC),
        "t2": (0x10, 16, 1, "tem2", 0x158F488, 0x158BC0D),
        "t3": (0x11, 17, 1, "tem3", 0x158F4E7, 0x158BC2E),
        "t4": (0x12, 18, 1, "tem4", 0x158F546, 0x158BC4F),
        "t5": (0x13, 19, 1, "tem5", 0x158F5A5, 0x158BC70),
        "t6": (0x14, 20, 1, "tem6", 0x158F604, 0x158BC91),
        "t7": (0x15, 21, 1, "tem7", 0x158F663, 0x158BCB2),
        "dn": (0x16, 22, 1, "tend", 0x158F3E1, 0x158BCD3),
    }

    SCALAR_GET_CMP = {
        "w0sd": (0x158E91C, 0x158E922), "w1sd": (0x158E958, 0x158E95E),
        "w2sd": (0x158E93A, 0x158E940), "w3sd": (0x158E8FE, 0x158E904),
        "w0dn": (0x158E910, 0x158EBEE), "w1dn": (0x158E94C, 0x158EBFA),
        "w2dn": (0x158E92E, 0x158EBF4), "w3dn": (0x158E8F2, 0x158EBE8),
    }
    SCALAR_SET_CMP = {
        "w0sd": (0x15905DD, 0x15905E9), "w1sd": (0x15904DA, 0x15904E6),
        "w2sd": (0x1590507, 0x1590513), "w3sd": (0x15904AD, 0x15904B9),
        "w0dn": (0x1590469, 0x1590475), "w1dn": (0x15904CE, 0x1590A38),
        "w2dn": (0x15904FB, 0x1590A64), "w3dn": (0x15904A1, 0x1590A0C),
    }

    # Verify every WEATHER_SEASON::get handler reads the exact expected offset!
    for suf_key, (s_rel, _, w, inner_cc, inner_fo, rd_fo) in SEASON_SUB.items():
        if s_rel == 0:
            check_ins_contains(pe, md, inner_fo, "[rcx]")
        else:
            check_ins_contains(pe, md, inner_fo, f"+ {hex(s_rel)}" if s_rel >= 10 else f"+ {s_rel}")
        r_off = 0x20 + s_rel
        check_ins_contains(pe, md, rd_fo, f"+ {hex(r_off)}")

    xml_fields = master["entities"]["weather.xml"][0]["fields"]
    schema_out: list[dict[str, Any]] = []
    xref_members: list[dict[str, Any]] = []
    dom_out: dict[str, Any] = {}

    for idx, f in enumerate(xml_fields):
        fid = f["field"]
        rec: dict[str, Any] = {
            "index": idx, "field": fid, "name": f.get("name"), "schema_type": f.get("type"),
            "master_occ": code_occ[fid], "prior_refs": ["t01l/E27", "t74/E115", "t76c/E118"],
        }
        if fid == "duni":
            g_ins = check_4cc_at(pe, md, 0xFE3912, "duni")
            rec.update({
                "grade": "L3", "scope": "client+server", "wire_loc": "mid+99..102", "width": 4, "wire_type": "u32",
                "member_off": "+0x0c", "getter_fo": "0xfe3912", "setter_fo": None, "reader_fo": "0x3c600f0",
                "domain": {"rows": n, "unique": n, "eq_rdui_raw": n, "violations": 0},
            })
            xref_members.append({"field": fid, "member_off": "+0x0c", "getter_cmp": g_ins, "reader": pe.dis_one(md, 0x3C600F0)})
            dom_out[fid] = rec["domain"]
        elif fid == "rdui":
            g_ins = check_4cc_at(pe, md, 0xFE3862, "rdui")
            rec.update({
                "grade": "held", "scope": "client+server", "wire_loc": "mid+103..106", "width": 4, "wire_type": "u32",
                "member_off": "+0x10", "getter_fo": "0xfe3862", "setter_fo": None, "reader_fo": "0x3c600f0",
                "hold_reason": "DATABASE_RECORD::get 0xfe38a2 suppresses output whenever [+0x0c]==[+0x10]; 334/334 rows suppressed (0 live outputs).",
                "first_counterexample": {"row": 0, "name": names[0], "duni": int(dunis[0]), "rdui_raw": int(rduis[0]), "reason": "suppressed_eq_duni"},
                "domain": {"rows": n, "suppressed": n, "live": 0},
            })
            xref_members.append({"field": fid, "member_off": "+0x10", "getter_cmp": g_ins, "reader": pe.dis_one(md, 0x3C600F0)})
            dom_out[fid] = rec["domain"]
        elif fid in ("NDBC", "FDBC"):
            rec.update({"grade": "editor_metadata", "scope": "non_wire", "getter_fo": None, "setter_fo": None,
                        "note": "Editor change-tracking counter; 0 hits in WEATHER::get/DATABASE_RECORD::get."})
        elif fid == "dbnm":
            g_ins = check_4cc_at(pe, md, 0xFE375D, "dbnm")
            rec.update({"grade": "non_wire_computed", "scope": "non_wire", "getter_fo": "0xfe375d", "setter_fo": None,
                        "note": "DATABASE_RECORD::get 0xfe375d dispatches virtual display-name resolver (returns wnam)."})
            xref_members.append({"field": fid, "getter_cmp": g_ins, "classification": "non_wire_computed"})
        elif fid == "wnam":
            g_cmp = check_4cc_at(pe, md, 0x158E971, "wnam")
            s_cmp = check_4cc_at(pe, md, 0x1590585, "wnam")
            r_ins = check_ins_contains(pe, md, 0x158B98C, "+ 0x18")
            dom = {
                "rows": n, "non_empty": sum(1 for x in names if x), "utf8_errors": 0,
                "min_len": min(len(x.encode("utf-8")) for x in names),
                "max_len": max(len(x.encode("utf-8")) for x in names),
                "samples": [{"row": i, "duni": int(dunis[i]), "value": names[i]} for i in (0, 1, 2, 139, 333)],
                "violations": 0,
            }
            rec.update({
                "grade": "L3", "scope": "client+server", "wire_loc": "lstr@0", "width": None, "wire_type": "u32_len+utf8",
                "member_off": "+0x18", "getter_fo": "0x158e979", "setter_fo": "0x1590591", "reader_fo": "0x158b98c",
                "domain": dom,
            })
            xref_members.append({"field": fid, "grade": "L3", "member_off": "+0x18", "getter_cmp": g_cmp, "setter_cmp": s_cmp, "reader_sink": r_ins})
            dom_out[fid] = dom
        else:
            # w{b}{suf}
            b = int(fid[1])
            suf_key = fid[2:]
            s_rel, w_rel, w, inner_cc, inner_fo, rd_fo = SEASON_SUB[suf_key]
            mid_off = 3 + 23 * b + w_rel
            mem_off = 0x20 + 0x18 * b + s_rel

            if fid in SCALAR_GET_CMP:
                g_cmp = check_4cc_at(pe, md, SCALAR_GET_CMP[fid][0], fid)
                g_outer_fo = SCALAR_GET_CMP[fid][1]
                s_cmp = check_4cc_at(pe, md, SCALAR_SET_CMP[fid][0], fid)
                s_h_fo = SCALAR_SET_CMP[fid][1]
            else:
                g_cmp = w_get_jts[fid]
                g_outer_fo = int(g_cmp["target_fo"], 16)
                s_cmp = w_set_jts[fid]
                s_h_fo = int(s_cmp["target_fo"], 16)

            # Verify setter writes EXACT mem_off!
            s_insns = pe.dis_n(md, s_h_fo, 8)
            expected_mem = f"+ {hex(mem_off)}"
            if not any(expected_mem in x["text"] for x in s_insns):
                raise RuntimeError(f"WEATHER::set {fid} at {hex(s_h_fo)} does not write {expected_mem}: {s_insns}")

            if suf_key == "sd":
                col = mid[:, mid_off:mid_off + 2].copy().view("<i2").ravel()
                dom, _ = int_range_stats_vec(col, 0, 365, dunis, None, names)
                wt = "i16"
            elif suf_key == "dn":
                col = mid[:, mid_off].view(np.int8)
                dom, _ = int_range_stats_vec(col, 0, 50, dunis, "eq100", names)
                dom["sentinel_0x64_null_count"] = int((col == 100).sum())
                wt = "i8_optional_0x64_null"
            else:
                col = mid[:, mid_off].view(np.int8)
                dom, _ = int_range_stats_vec(col, 0, 100, dunis, None, names)
                wt = "i8"

            grade = "L3" if dom["violations"] == 0 else "held"
            rec.update({
                "grade": grade, "scope": "client+server",
                "wire_loc": f"mid+{mid_off}" + (f"..{mid_off + 1}" if w == 2 else ""),
                "mid_off": mid_off, "width": w, "wire_type": wt,
                "member_off": f"+0x{mem_off:02x}",
                "getter_fo": f"{hex(g_outer_fo)}->{hex(inner_fo)}({inner_cc})",
                "setter_fo": hex(s_h_fo),
                "reader_fo": hex(rd_fo),
                "domain": dom,
            })
            if suf_key == "sd":
                rec["t76c_reconciliation"] = "t76c L2 read blk+0 as u8 and assigned blk+1 ({0,1}) to w{b}dn; L3 static proves blk+0..1 is a 2B i16 w{b}sd (0..359)."
            elif suf_key == "dn":
                rec["t76c_reconciliation"] = "t76c L2 left blk+22 ({0,100}) unassigned; L3 static proves blk+22 (+0x16) IS w{b}dn ('tend') with 0x64(100) as explicit NULL sentinel (WEATHER_SEASON::get 0x158f3e5, WEATHER::set 0x1590498/a2f/a5b/a87)."
            elif suf_key[0] in ("w", "p"):
                rec["reconciliation_correction"] = "CORRECTS wind/precip swap in BOTH t01l(E27) and t76c(E118): blk+2..6 (+0x02..+0x06) = w{b}w0..w4 (WIND) and blk+7..11 (+0x07..+0x0b) = w{b}p0..p4 (PRECIPITATION), quadruple-confirmed by WEATHER::read + WEATHER::get + WEATHER_SEASON::get + WEATHER::set."

            xref_members.append({
                "field": fid, "grade": grade, "mid_off": mid_off, "width": w, "member_off": f"+0x{mem_off:02x}",
                "getter_dispatch": g_cmp, "season_inner_4cc": inner_cc, "season_getter_handler": pe.dis_one(md, inner_fo),
                "setter_dispatch": s_cmp, "setter_store_seq": [x for x in s_insns if expected_mem in x["text"] or "0x64" in x["text"]],
                "reader_sink": pe.dis_one(md, rd_fo),
            })
            dom_out[fid] = dom
        schema_out.append(rec)

    # Compute exact post-read normalizer statistics (0x43e7e10 & 0x158bd07)
    sds = np.column_stack([mid[:, 3 + 23 * b:3 + 23 * b + 2].copy().view("<i2").ravel() for b in range(4)])
    all_sd_eq = int(((sds[:, 0] == sds[:, 1]) & (sds[:, 1] == sds[:, 2]) & (sds[:, 2] == sds[:, 3])).sum())
    win_ne100 = sum(int((mid[:, 3 + 23 * b + 2:3 + 23 * b + 7].view(np.int8).sum(axis=1) != 100).sum()) for b in range(4))
    pre_ne100 = sum(int((mid[:, 3 + 23 * b + 7:3 + 23 * b + 12].view(np.int8).sum(axis=1) != 100).sum()) for b in range(4))
    tem10_ne100 = sum(int((mid[:, 3 + 23 * b + 12:3 + 23 * b + 22].view(np.int8).sum(axis=1) != 100).sum()) for b in range(4))
    norm_stats = {
        "total_season_blocks": 4 * n,
        "wind_blk2_6_sum_ne_100": win_ne100,
        "precip_blk7_11_sum_ne_100": pre_ne100,
        "temp10_blk12_21_sum_ne_100": tem10_ne100,
        "all_4_sd_equal_rows_reset_to_55_145_230_300": all_sd_eq,
        "normalizer_fo": "0x43e7e10",
        "sd_reset_fo": "0x158bd07",
    }

    internal_slots = [
        {"wire_loc": "mid+0..2", "width": 3, "member_off": "+0x80..+0x82", "reader_fo": "0x158b9a4", "values": {"const": 0, "rows": n}},
        {"wire_loc": "mid+95..98", "width": 4, "member_off": "+0x08", "reader_fo": "0x3c600f0", "note": "row ordinal (0..333)"},
    ]
    fm_tbl = {
        "table_id": 27, "xml": "weather.xml", "rows": n, "client_eq_server": True,
        "frame": {"native": f"13 + {len(buf_c) - 22} + 9 = {len(buf_c)}", "grammar": "1B sel + lstr(wnam) + 3B zero + 4*23B season + 12B identity"},
        "post_read_normalizer": norm_stats,
        "schema_fields": schema_out,
        "internal_wire_slots": internal_slots,
    }
    xref_tbl = {
        "task": "t83",
        "class": verify_class_static(pe, md, 27),
        "db_context_refs": [r for r in db_ctx if r["table_id"] == 27],
        "helpers": {
            "weather_season_get": {"fo": "0x158f1d0", "va": hex(pe.fo_to_va(0x158F1D0)), "tend_null_cmp": pe.dis_one(md, 0x158F3E5)},
            "post_read_normalizer": {"thunk_fo": "0x158bd70", "real_fo": "0x43e7e10", "wind_fix": pe.dis_one(md, 0x43E7E40), "precip_fix": pe.dis_one(md, 0x43E7E7C), "temp_fix": pe.dis_one(md, 0x43E7EF5)},
            "sd_equal_reset": {"fo": "0x158bd07", "dis_head": pe.dis_n(md, 0x158BD07, 10)},
        },
        "members": xref_members,
        "internal_wire_slots": internal_slots,
    }
    dom_tbl = {
        "rows": n, "client_payload_bytes": len(buf_c), "server_payload_bytes": len(buf_s),
        "client_eq_server": True, "post_read_normalizer": norm_stats, "fields": dom_out,
    }
    return fm_tbl, xref_tbl, dom_tbl


# ---------------------------------------------------------------------------
# Table 7 — MEDIA_SOURCE (22 XML fields, 208 rows, variable + 7B server delta)
# ---------------------------------------------------------------------------
def parse_media_archive(buf: bytes, is_server: bool) -> list[dict[str, Any]]:
    n = struct.unpack_from("<I", buf, 8)[0]
    pos = 13
    rows: list[dict[str, Any]] = []
    for i in range(n):
        row_start = pos
        sel = buf[pos]
        if sel != 0:
            raise RuntimeError(f"media sel!=0 at row {i}")
        pos += 1

        def rd_lstr() -> str:
            nonlocal pos
            l = struct.unpack_from("<I", buf, pos)[0]
            pos += 4
            s = buf[pos:pos + l].decode("utf-8")
            pos += l
            return s

        def rd_u8() -> int:
            nonlocal pos
            v = buf[pos]
            pos += 1
            return v

        def rd_i32() -> int:
            nonlocal pos
            v = struct.unpack_from("<i", buf, pos)[0]
            pos += 4
            return v

        def rd_u32() -> int:
            nonlocal pos
            v = struct.unpack_from("<I", buf, pos)[0]
            pos += 4
            return v

        def rd_vec() -> list[int]:
            c = rd_u32()
            return [rd_i32() for _ in range(c)]

        Mnam = rd_lstr()
        int_d1 = rd_u8()
        cnt_t = rd_u32()
        Mtyp = [rd_u8() for _ in range(cnt_t)]
        Murl = rd_lstr()
        Mhtg = rd_lstr()
        Misf = rd_u8()
        Msty = rd_u8()
        Mcmi = rd_vec()
        Mcyi = rd_i32()
        Mrgi = rd_vec()
        Mnti = rd_vec()
        Mcti = rd_i32()
        cnt_cl = rd_u32()
        Mcli = []
        for _ in range(cnt_cl):
            u1 = rd_u32()
            u2 = rd_u32()
            cu = rd_lstr()
            Mcli.append((u1, u2, cu))
        if is_server:
            s0 = pos
            Mper = rd_u8()
            Mscp = rd_u8()
            Mdlp = rd_u32()
            cnt_j = rd_u8()
            Mjor = [rd_i32() for _ in range(cnt_j)]
            srv_len = pos - s0
        else:
            Mper = Mscp = Mdlp = None
            Mjor = None
            srv_len = 0
        Mlnm = rd_vec()
        Mapc = rd_u8()
        pre5_hex = buf[pos - 5:pos].hex()
        ord_i = rd_u32()
        duni_i = rd_u32()
        rdui_i = rd_u32()
        rows.append({
            "Mnam": Mnam, "int_d1": int_d1, "Mtyp": Mtyp, "Murl": Murl, "Mhtg": Mhtg,
            "Misf": Misf, "Msty": Msty, "Mcmi": Mcmi, "Mcyi": Mcyi, "Mrgi": Mrgi,
            "Mnti": Mnti, "Mcti": Mcti, "Mcli": Mcli, "Mper": Mper, "Mscp": Mscp,
            "Mdlp": Mdlp, "Mjor": Mjor, "Mlnm": Mlnm, "Mapc": Mapc, "pre5": pre5_hex,
            "ord": ord_i, "duni": duni_i, "rdui": rdui_i,
            "row_len": pos - row_start, "srv_len": srv_len,
        })
    if pos != len(buf) - 9:
        raise RuntimeError(f"media closure failed {pos} vs {len(buf) - 9}")
    return rows


def build_media(
    pe: MiniPE64,
    md: Cs,
    master: dict[str, Any],
    cli: dict[str, bytes],
    srv: dict[str, bytes],
    ref_n: dict[int, int],
    ref_uids: dict[int, set[int]],
    code_occ: Counter[str],
    db_ctx: list[dict[str, Any]],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    m_cli = parse_media_archive(cli["table_7.dat"], False)
    m_srv = parse_media_archive(srv["table_7.dat"], True)
    n = len(m_srv)
    shared_keys = ["Mnam", "int_d1", "Mtyp", "Murl", "Mhtg", "Misf", "Msty", "Mcmi", "Mcyi", "Mrgi", "Mnti", "Mcti", "Mcli", "Mlnm", "Mapc", "ord", "duni", "rdui"]
    if not all(all(rc[k] == rs[k] for k in shared_keys) for rc, rs in zip(m_cli, m_srv)):
        raise RuntimeError("media shared fields client != server")
    if any(rs["row_len"] - rc["row_len"] != 7 for rc, rs in zip(m_cli, m_srv)):
        raise RuntimeError("media server delta != 7")
    if [r["ord"] for r in m_srv] != list(range(n)) or any(r["duni"] != r["rdui"] for r in m_srv):
        raise RuntimeError("media identity check failed")

    names = [r["Mnam"] for r in m_srv]
    dunis = np.array([r["duni"] for r in m_srv], dtype=np.uint32)
    rduis = np.array([r["rdui"] for r in m_srv], dtype=np.uint32)

    # Verify server gate & helper instructions
    srv_gate_ins = check_ins_contains(pe, md, 0x1545CFE, "test")
    mcli_club_ins = check_4cc_at(pe, md, 0x154DDC8, "club")
    mcli_curl_ins = check_4cc_at(pe, md, 0x154DDC0, "curl")
    mtyp_item_ins = check_4cc_at(pe, md, 0x4381950, "Mtyp")

    MD_STATIC: dict[str, dict[str, Any]] = {
        "Mnam": {"scope": "client+server", "seq": 1, "wt": "u32_len+utf8", "mem": "+0x18", "gcmp": 0x15470E6, "gh": 0x15470F2, "scmp": 0x154AAA0, "sh": 0x154AAAC, "rd": 0x15457DC, "fx": None, "gchk": "0x18", "rchk": "+ 0x18"},
        "Mtyp": {"scope": "client+server", "seq": 3, "wt": "u32_cnt+u8_vec_enum", "mem": "+0x30..+0x40", "gcmp": 0x154763A, "gh": 0x1547646, "scmp": 0x154AA15, "sh": 0x154AD20, "rd": 0x15458B2, "fx": None, "gchk": "rbp", "rchk": "+ 0x30"},
        "Murl": {"scope": "client+server", "seq": 4, "wt": "u32_len+utf8", "mem": "+0x20", "gcmp": 0x1546ED3, "gh": 0x15487D7, "scmp": 0x154AA21, "sh": 0x154AA2D, "rd": 0x1545904, "fx": None, "gchk": "0x20", "rchk": "+ 0x20"},
        "Mhtg": {"scope": "client+server", "seq": 5, "wt": "u32_len+utf8", "mem": "+0x28", "gcmp": 0x15474B0, "gh": 0x1547D74, "scmp": 0x154A9C2, "sh": 0x154AC9F, "rd": 0x1545921, "fx": None, "gchk": "0x28", "rchk": "+ 0x28"},
        "Misf": {"scope": "client+server", "seq": 6, "wt": "u8_bool", "mem": "+0xd2", "gcmp": 0x15474BC, "gh": 0x1548454, "scmp": 0x154A9CE, "sh": 0x154A9DA, "rd": 0x154593E, "fx": None, "gchk": "+ 0xd2", "rchk": "+ 0xd2"},
        "Msty": {"scope": "client+server", "seq": 7, "wt": "i8_enum", "mem": "+0xd0", "gcmp": 0x154762E, "gh": 0x15484B7, "scmp": 0x154AA09, "sh": 0x154AD09, "rd": 0x1545962, "fx": None, "gchk": "+ 0xd0", "rchk": "+ 0xd0"},
        "Mcmi": {"scope": "client+server", "seq": 8, "wt": "u32_cnt+i32_ordinal_vec:table_25", "mem": "+0x48..+0x58", "gcmp": 0x154735A, "gh": 0x1547B5A, "scmp": 0x154AB53, "sh": 0x154AB5F, "rd": 0x15459A4, "fx": 0x437A490, "gchk": "r12", "rchk": "+ 0x48"},
        "Mcyi": {"scope": "client+server", "seq": 9, "wt": "i32_ordinal_ref:table_2", "mem": "+0xc0", "gcmp": 0x154717E, "gh": 0x1547AD7, "scmp": 0x154AAD8, "sh": 0x154AAE4, "rd": 0x1545AFD, "fx": 0x437A490, "gchk": "+ 0xc0", "rchk": "+ 0xc0"},
        "Mrgi": {"scope": "client+server", "seq": 10, "wt": "u32_cnt+i32_ordinal_vec:table_47", "mem": "+0x78..+0x88", "gcmp": 0x1547298, "gh": 0x154809E, "scmp": 0x154AB18, "sh": 0x154AF0E, "rd": 0x1545B3F, "fx": 0x3BF5E90, "gchk": "r12", "rchk": "+ 0x78"},
        "Mnti": {"scope": "client+server", "seq": 11, "wt": "u32_cnt+i32_ordinal_vec:table_10", "mem": "+0x60..+0x70", "gcmp": 0x15473B6, "gh": 0x15473C2, "scmp": 0x154ABEA, "sh": 0x154B00A, "rd": 0x1545BBF, "fx": 0x437A490, "gchk": "rbp", "rchk": "+ 0x60"},
        "Mcti": {"scope": "client+server", "seq": 12, "wt": "i32_ordinal_ref:table_5", "mem": "+0xc8", "gcmp": 0x1547372, "gh": 0x154737E, "scmp": 0x154AACC, "sh": 0x154AEDA, "rd": 0x1545C1D, "fx": 0x3BF4A90, "gchk": "+ 0xc8", "rchk": "+ 0xc8"},
        "Mcli": {"scope": "client+server", "seq": 13, "wt": "u32_cnt+(u32_uid+u32_rdui+lstr)_vec:table_3_uid", "mem": "+0xa8..+0xb8", "gcmp": 0x1546FB6, "gh": 0x1546FC2, "scmp": 0x154AB47, "sh": 0x154AF8A, "rd": 0x1545C6A, "fx": None, "gchk": "rbp", "rchk": "+ 0xa8"},
        "Mper": {"scope": "server_only", "seq": 14, "wt": "i8_enum", "mem": "+0xf0", "gcmp": 0x154728C, "gh": 0x1547AF7, "scmp": 0x154ABF6, "sh": 0x154AC02, "rd": 0x1545D0B, "fx": None, "gchk": "+ 0xf0", "rchk": "+ 0xf0"},
        "Mscp": {"scope": "server_only", "seq": 15, "wt": "i8_enum", "mem": "+0xf1", "gcmp": 0x1547622, "gh": 0x1547DF4, "scmp": 0x154AB24, "sh": 0x154AB30, "rd": 0x1545D2F, "fx": None, "gchk": "+ 0xf1", "rchk": "+ 0xf1"},
        "Mdlp": {"scope": "server_only", "seq": 16, "wt": "u32_packed_date", "mem": "+0xd4", "gcmp": 0x154718A, "gh": 0x154803D, "scmp": 0x154A9B6, "sh": 0x154AC19, "rd": 0x1545D4F, "fx": None, "gchk": "+ 0xd6", "rchk": "+ 0xd4"},
        "Mlnm": {"scope": "client+server", "seq": 18, "wt": "u32_cnt+i32_ordinal_vec:table_7", "mem": "+0x90..+0xa0", "gcmp": 0x15470DA, "gh": 0x1547F49, "scmp": 0x154AA94, "sh": 0x154AE59, "rd": 0x1545E0D, "fx": 0x3BF5FD0, "gchk": "r12", "rchk": "+ 0x90"},
        "Mapc": {"scope": "client+server", "seq": 19, "wt": "u8_bool", "mem": "+0xd3", "gcmp": 0x1546F9E, "gh": 0x1547940, "scmp": 0x154AA65, "sh": 0x154AA71, "rd": 0x1545E72, "fx": None, "gchk": "+ 0xd3", "rchk": "+ 0xd3"},
    }

    xml_fields = master["entities"]["media source.xml"][0]["fields"]
    schema_out: list[dict[str, Any]] = []
    xref_members: list[dict[str, Any]] = []
    dom_out: dict[str, Any] = {}

    for idx, f in enumerate(xml_fields):
        fid = f["field"]
        rec: dict[str, Any] = {
            "index": idx, "field": fid, "name": f.get("name"), "schema_type": f.get("type"),
            "master_occ": code_occ[fid], "prior_refs": ["t74/E115", "t76b(absorbed)"],
        }
        if fid == "duni":
            g_ins = check_4cc_at(pe, md, 0xFE3912, "duni")
            rec.update({
                "grade": "L3", "scope": "client+server", "wire_loc": "trailer+4..7", "width": 4, "wire_type": "u32",
                "member_off": "+0x0c", "getter_fo": "0xfe3912", "setter_fo": None, "reader_fo": "0x3c600f0",
                "domain": {"rows": n, "unique": n, "eq_rdui_raw": n, "violations": 0},
            })
            xref_members.append({"field": fid, "member_off": "+0x0c", "getter_cmp": g_ins, "reader": pe.dis_one(md, 0x3C600F0)})
            dom_out[fid] = rec["domain"]
        elif fid == "rdui":
            g_ins = check_4cc_at(pe, md, 0xFE3862, "rdui")
            rec.update({
                "grade": "held", "scope": "client+server", "wire_loc": "trailer+8..11", "width": 4, "wire_type": "u32",
                "member_off": "+0x10", "getter_fo": "0xfe3862", "setter_fo": None, "reader_fo": "0x3c600f0",
                "hold_reason": "DATABASE_RECORD::get 0xfe38a2 suppresses output whenever [+0x0c]==[+0x10]; 208/208 rows suppressed (0 live outputs).",
                "first_counterexample": {"row": 0, "name": names[0], "duni": int(dunis[0]), "rdui_raw": int(rduis[0]), "reason": "suppressed_eq_duni"},
                "domain": {"rows": n, "suppressed": n, "live": 0},
            })
            xref_members.append({"field": fid, "member_off": "+0x10", "getter_cmp": g_ins, "reader": pe.dis_one(md, 0x3C600F0)})
            dom_out[fid] = rec["domain"]
        elif fid in ("NDBC", "FDBC"):
            rec.update({"grade": "editor_metadata", "scope": "non_wire", "getter_fo": None, "setter_fo": None,
                        "note": "Editor change-tracking counter; 0 hits in MEDIA_SOURCE::get/DATABASE_RECORD::get."})
        elif fid == "dbnm":
            g_ins = check_4cc_at(pe, md, 0xFE375D, "dbnm")
            rec.update({"grade": "non_wire_computed", "scope": "non_wire", "getter_fo": "0xfe375d", "setter_fo": None,
                        "note": "DATABASE_RECORD::get 0xfe375d dispatches virtual display-name resolver (returns Mnam)."})
            xref_members.append({"field": fid, "getter_cmp": g_ins, "classification": "non_wire_computed"})
        elif fid in MD_STATIC:
            st = MD_STATIC[fid]
            g_cmp = check_4cc_at(pe, md, st["gcmp"], fid)
            s_cmp = check_4cc_at(pe, md, st["scmp"], fid)
            g_h = check_ins_contains(pe, md, st["gh"], st["gchk"])
            s_h = pe.dis_one(md, st["sh"])
            r_ins = check_ins_contains(pe, md, st["rd"], st["rchk"])
            fx_ins = pe.dis_one(md, st["fx"]) if st["fx"] else None

            first_ce = None
            hold_reason = None
            if fid in ("Mnam", "Murl", "Mhtg"):
                sv = [r[fid] for r in m_srv]
                dom = {
                    "rows": n, "non_empty": sum(1 for x in sv if x), "empty": sum(1 for x in sv if not x),
                    "utf8_errors": 0, "violations": 0,
                    "samples": [{"row": i, "duni": int(dunis[i]), "value": sv[i]} for i in range(min(5, n)) if sv[i]][:3],
                }
                if fid == "Mhtg":
                    dom["note"] = "All 208/208 rows store len=0 empty string ''; getter 0x1547d74 emits live empty string without suppression."
                grade = "L3"
            elif fid in ("Misf", "Mapc"):
                col = np.array([r[fid] for r in m_srv], dtype=np.uint8)
                bad = int(((col != 0) & (col != 1)).sum())
                dom = {"rows": n, "true_count": int((col == 1).sum()), "false_count": int((col == 0).sum()), "violations": bad}
                if fid == "Misf":
                    dom["note"] = "All 208/208 rows store 0 (False); getter 0x1548454 emits live boolean without suppression."
                grade = "L3" if bad == 0 else "held"
            elif fid == "Mtyp":
                allowed = parse_enum_ids(master, "Mtyp")
                flat = np.array([x for r in m_srv for x in r["Mtyp"]], dtype=np.int64)
                flat_dunis = np.array([r["duni"] for r in m_srv for _ in r["Mtyp"]], dtype=np.uint32)
                dom, first_ce = enum_stats_vec(flat, allowed, flat_dunis)
                dom["rows"] = n
                dom["total_items"] = int(len(flat))
                dom["list_len_histogram"] = {str(k): int(v) for k, v in sorted(Counter(len(r["Mtyp"]) for r in m_srv).items())}
                grade = "L3" if dom["violations"] == 0 else "held"
            elif fid in ("Msty", "Mper", "Mscp"):
                col = np.array([r[fid] for r in m_srv], dtype=np.int8)
                allowed = parse_enum_ids(master, fid)
                dom, first_ce = enum_stats_vec(col, allowed, dunis, names)
                if dom["violations"] == 0:
                    grade = "L3"
                else:
                    grade = "held"
                    hold_reason = (
                        f"Exact getter ({hex(st['gh'])} movsx) and setter ({hex(st['sh'])}) map to {st['mem']} ({st['scope']}), "
                        f"but {dom['violations']}/{n} rows have raw=0 outside master.enums['{fid}'] ({allowed}); getter does not suppress 0."
                    )
            elif fid == "Mdlp":
                col = np.array([r["Mdlp"] for r in m_srv], dtype="<u4")
                dom = check_dates_vec(col)
                dom["suppressed_1900_01_01"] = dom["default_1900_01_01_count"]
                dom["live"] = n - dom["suppressed_1900_01_01"]
                grade = "held"
                hold_reason = (
                    "Exact getter (0x154803d), setter (0x154a9b6 -> 0x154ac19; unset writes 0x76c0001 at 0x154b5c8), and server-only reader (0x1545d4f) map to +0xd4; "
                    "getter suppresses 1900-01-01 (0x076c0001) and all 208/208 rows store 1900-01-01 (0 live outputs)."
                )
                first_ce = {"row": 0, "name": names[0], "duni": int(dunis[0]), "raw_value": "0x076c0001 (1900-01-01)", "reason": "suppressed_default_date_0_live"}
            elif fid in ("Mcmi", "Mrgi", "Mnti", "Mlnm"):
                tid_map = {"Mcmi": 25, "Mrgi": 47, "Mnti": 10, "Mlnm": 7}
                flat = np.array([x for r in m_srv for x in r[fid]], dtype=np.int32)
                dom = fk_stats_vec(flat, tid_map[fid], ref_n, ref_uids)
                dom["rows_non_empty"] = sum(1 for r in m_srv if r[fid])
                dom["list_len_histogram"] = {str(k): int(v) for k, v in sorted(Counter(len(r[fid]) for r in m_srv).items())}
                grade = "L3" if dom["violations"] == 0 else "held"
            elif fid in ("Mcyi", "Mcti"):
                tid_map = {"Mcyi": 2, "Mcti": 5}
                col = np.array([r[fid] for r in m_srv], dtype=np.int32)
                dom = fk_stats_vec(col, tid_map[fid], ref_n, ref_uids)
                grade = "L3" if dom["violations"] == 0 else "held"
            elif fid == "Mcli":
                items = [it for r in m_srv for it in r["Mcli"]]
                u1s = [it[0] for it in items]
                u2s = [it[1] for it in items]
                curls = [it[2] for it in items]
                club_uids = ref_uids[3]
                in_uid = sum(1 for u in u1s if u in club_uids)
                wrong_ord_hits = sum(1 for u in u1s if u < ref_n[3])
                miss = len(items) - in_uid
                dom = {
                    "rows": n, "rows_non_empty": sum(1 for r in m_srv if r["Mcli"]),
                    "total_items": len(items),
                    "u1_eq_u2": sum(1 for a, b in zip(u1s, u2s) if a == b),
                    "target_table": 3, "target_key_kind": "UID_pair_not_ordinal",
                    "uid_hits": in_uid, "uid_misses": miss,
                    "wrong_ordinal_control_hits": wrong_ord_hits,
                    "wrong_ordinal_control_misses": len(items) - wrong_ord_hits,
                    "curl_non_empty": sum(1 for c in curls if c),
                    "curl_utf8_errors": 0,
                    "samples": [{"club_uid": it[0], "curl": it[2]} for it in items[:5]],
                    "violations": miss,
                }
                grade = "L3" if miss == 0 else "held"
            else:
                raise RuntimeError(f"unhandled media {fid}")

            rec.update({
                "grade": grade, "scope": st["scope"], "wire_seq": st["seq"], "wire_type": st["wt"],
                "member_off": st["mem"],
                "getter_fo": hex(st["gh"]), "setter_fo": hex(st["sh"]), "reader_fo": hex(st["rd"]),
                "fixup_fo": hex(st["fx"]) if st["fx"] else None,
                "domain": dom,
            })
            if hold_reason:
                rec["hold_reason"] = hold_reason
                rec["first_counterexample"] = first_ce
            xref_members.append({
                "field": fid, "grade": grade, "scope": st["scope"], "wire_seq": st["seq"], "member_off": st["mem"],
                "getter_cmp": g_cmp, "getter_handler": g_h,
                "setter_cmp": s_cmp, "setter_handler": s_h,
                "reader_sink": r_ins, "fixup": fx_ins,
            })
            dom_out[fid] = dom
        schema_out.append(rec)

    pre5_counts = Counter(r["pre5"] for r in m_cli)
    pre5_explanation = {
        "distinct_5b_values_before_identity": len(pre5_counts),
        "rows_with_Mlnm_len_0": sum(1 for r in m_cli if len(r["Mlnm"]) == 0),
        "rows_with_Mlnm_len_gt_0": sum(1 for r in m_cli if len(r["Mlnm"]) > 0),
        "exact_decomposition": "Last 5B before 12B identity are u32(cnt_lnm=0)+u8(Mapc) on 192 rows ('0000000001' x161, '0000000000' x31) and u32(last Mlnm ordinal)+u8(Mapc) on 16 rows with cnt_lnm>0 (14 distinct patterns, incl. '4000000001' x3), total 2+14 = 16.",
        "histogram": dict(pre5_counts.most_common()),
    }
    internal_slots = [
        {"wire_seq": 2, "width": 1, "member_off": "+0xd1", "reader_fo": "0x15457f9", "values": {"const": 0, "rows": n}},
        {"wire_seq": 17, "scope": "server_only", "width": "1 + 4*cnt", "member_off": "+0xd8..+0xe8", "internal_4cc": "Mjor", "getter_fo": "0x15474d4", "reader_fo": "0x1545d88", "fixup_fo": "0x3bf9220", "values": {"cnt_all_0": True, "rows": n}},
        {"wire_seq": 20, "width": 4, "member_off": "+0x08", "reader_fo": "0x3c600f0", "note": "row ordinal (0..207)"},
    ]
    fm_tbl = {
        "table_id": 7, "xml": "media source.xml", "rows": n, "client_eq_server": False,
        "server_delta": {
            "bytes_per_row": 7, "gate_fo": "0x1545cfe",
            "grammar": "1B Mper(+0xf0) + 1B Mscp(+0xf1) + 4B Mdlp(+0xd4) + u8 cnt_jor(=0 on 208/208) + cnt_jor*4B Mjor(+0xd8)",
            "explains_t74_7b_delta": True,
        },
        "pre5_before_identity": pre5_explanation,
        "frame": {
            "client_bytes": len(cli["table_7.dat"]), "server_bytes": len(srv["table_7.dat"]),
            "delta_total_bytes": len(srv["table_7.dat"]) - len(cli["table_7.dat"]),
            "t74_mid_block_solved": True,
        },
        "schema_fields": schema_out,
        "internal_wire_slots": internal_slots,
    }
    xref_tbl = {
        "task": "t83",
        "class": verify_class_static(pe, md, 7),
        "db_context_refs": [r for r in db_ctx if r["table_id"] in (2, 3, 5, 7, 10, 25, 47)],
        "server_7b_gate": srv_gate_ins,
        "helpers": {
            "mtyp_list_builder": {"thunk_fo": "0x1732970", "real_fo": "0x45f25b0"},
            "mtyp_item_get": {"fo": "0x4381840", "cmp_4cc": mtyp_item_ins},
            "mcli_item_get": {"fo": "0x154dc00", "cmp_club": mcli_club_ins, "cmp_curl": mcli_curl_ins, "uid_lookup_call": pe.dis_one(md, 0x154DDDF)},
            "mcli_uid_pair_reader": {"thunk_fo": "0xfe96c0", "real_fo": "0x3cd4360"},
            "mdlp_null_suppress": {"fo": "0x154803d", "dis_head": pe.dis_n(md, 0x154803D, 6)},
        },
        "members": xref_members,
        "internal_wire_slots": internal_slots,
    }
    dom_tbl = {
        "rows": n, "client_payload_bytes": len(cli["table_7.dat"]), "server_payload_bytes": len(srv["table_7.dat"]),
        "shared_fields_identical": True, "server_only_delta_bytes_all_208": 7,
        "pre5_before_identity": pre5_explanation,
        "fields": dom_out,
    }
    return fm_tbl, xref_tbl, dom_tbl


# ---------------------------------------------------------------------------
# Cross-check against frozen t74 / t76c foundations & build outputs
# ---------------------------------------------------------------------------
def build_all(outdir: Path) -> dict[str, Any]:
    integrity = verify_integrity()
    pe = MiniPE64(EXE_PATH)
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    master = json.loads((ROOT / MASTER_REL).read_text(encoding="utf-8"))

    code_occ: Counter[str] = Counter()
    for recs in master["entities"].values():
        for rec in recs:
            for f in rec.get("fields", []):
                code_occ[f["field"]] += 1

    db_ctx = verify_db_context(pe, md)

    wanted = [
        "table_0.dat", "table_2.dat", "table_3.dat", "table_5.dat", "table_6.dat", "table_7.dat",
        "table_8.dat", "table_9.dat", "table_10.dat", "table_12.dat", "table_18.dat",
        "table_21.dat", "table_24.dat", "table_25.dat", "table_27.dat", "table_30.dat", "table_47.dat",
    ]
    cli = load_fmf("client", wanted)
    srv = load_fmf("server", wanted)

    ref_n: dict[int, int] = {}
    ref_uids: dict[int, set[int]] = {}
    for tid in (0, 2, 3, 5, 6, 7, 8, 9, 10, 12, 18, 21, 24, 25, 27, 30, 47):
        k = f"table_{tid}.dat"
        buf = srv.get(k) or cli.get(k)
        if buf is None:
            continue
        u = scan_uids(buf, tid)
        if k in cli and k in srv:
            uc = scan_uids(cli[k], tid)
            if not np.array_equal(u, uc):
                raise RuntimeError(f"UID mismatch between client and server for table_{tid}")
        ref_n[tid] = int(len(u))
        ref_uids[tid] = set(int(x) for x in u.tolist())

    # Cross-check payload lengths, row counts, and SHA-256 against frozen t74 frames.json
    t74 = json.loads(T74_FRAMES_PATH.read_text(encoding="utf-8"))
    t74_tables = t74["tables"]
    for tid in (0, 7, 8, 18, 27):
        for side, d in (("client", cli), ("server", srv)):
            r74 = t74_tables[str(tid)]["archives"][side]
            buf = d[f"table_{tid}.dat"]
            if r74["payload_len"] != len(buf):
                raise RuntimeError(f"t74 payload_len mismatch for {(side, tid)}: {len(buf)} vs {r74['payload_len']}")
            n_hdr = struct.unpack_from("<I", buf, 8)[0]
            if r74["count"] != n_hdr:
                raise RuntimeError(f"t74 count mismatch for {(side, tid)}: {n_hdr} vs {r74['count']}")
            sha = hashlib.sha256(buf).hexdigest()
            if r74["payload_sha256"] != sha:
                raise RuntimeError(f"t74 payload_sha256 mismatch for {(side, tid)}: {sha} vs {r74['payload_sha256']}")

    aw_fm, aw_xr, aw_dm = build_award(pe, md, master, cli, srv, ref_n, ref_uids, code_occ, db_ctx)
    la_fm, la_xr, la_dm = build_language(pe, md, master, cli, srv, ref_n, ref_uids, code_occ, db_ctx)
    dr_fm, dr_xr, dr_dm = build_derby(pe, md, master, cli, srv, ref_n, ref_uids, code_occ, db_ctx)
    we_fm, we_xr, we_dm = build_weather(pe, md, master, cli, srv, code_occ, db_ctx)
    md_fm, md_xr, md_dm = build_media(pe, md, master, cli, srv, ref_n, ref_uids, code_occ, db_ctx)

    def grade_counts(tbl: dict[str, Any]) -> dict[str, int]:
        c = Counter(f["grade"] for f in tbl["schema_fields"])
        return dict(sorted(c.items()))

    all_tbls = [aw_fm, la_fm, dr_fm, we_fm, md_fm]
    tot_grades: Counter[str] = Counter()
    for t in all_tbls:
        for f in t["schema_fields"]:
            tot_grades[f["grade"]] += 1

    field_map = {
        "task": "t83",
        "evidence_level": "L3 static (editor.exe) + L1/L2 full-archive vectorized validation; L4=0",
        "address_convention": "PE file offsets in field_map.json (matching t79); exact VAs, raw instruction bytes, and Capstone disassembly for every gate/handler/sink/fixup are recorded in xref_{award,language,weather,derby,media}.json.",
        "integrity": integrity,
        "summary": {
            "xml_denominator_total": sum(len(t["schema_fields"]) for t in all_tbls),
            "xml_denominator_source": MASTER_REL,
            "xml_denominator_note": "reports/xml_denominator_coverage.json covers club/comp/nation (1,034 occ) only; these 5 tables' 188-field XML denominator is counted directly from MANIFEST-verified master.json.",
            "total_grades": dict(sorted(tot_grades.items())),
            "award_0": {"xml_total": len(aw_fm["schema_fields"]), "grades": grade_counts(aw_fm), "internal_wire_slots": len(aw_fm["internal_wire_slots"])},
            "language_8": {"xml_total": len(la_fm["schema_fields"]), "grades": grade_counts(la_fm), "internal_wire_slots": len(la_fm["internal_wire_slots"])},
            "derby_18": {"xml_total": len(dr_fm["schema_fields"]), "grades": grade_counts(dr_fm), "internal_wire_slots": len(dr_fm["internal_wire_slots"])},
            "weather_27": {"xml_total": len(we_fm["schema_fields"]), "grades": grade_counts(we_fm), "internal_wire_slots": len(we_fm["internal_wire_slots"])},
            "media_7": {"xml_total": len(md_fm["schema_fields"]), "grades": grade_counts(md_fm), "internal_wire_slots": len(md_fm["internal_wire_slots"])},
        },
        "reconciliations": [
            {
                "id": "R1_weather_wind_precip_swap",
                "prior_refs": ["t01l/E27", "t76c/E118"],
                "finding": "BOTH t01l(E27) and t76c(E118) swapped precipitation and wind blocks in weather(27). Quadruple static proof (WEATHER::read 0x158ba47..0x158bb79, WEATHER::get 0x158e7d1..0x158ec90, WEATHER_SEASON::get 0x158f28e/30c/780..a19, WEATHER::set 0x15902c5..0x1590b77) proves blk+2..6 (+0x02..+0x06) = w{b}w0..w4 (WIND) and blk+7..11 (+0x07..+0x0b) = w{b}p0..p4 (PRECIPITATION). Normalizer 0x43e7e10 fixes +0x02 (76 non-100 blocks = wind) and +0x07 (67 non-100 blocks = precip).",
            },
            {
                "id": "R2_weather_sd_i16_and_dn_blk22",
                "prior_refs": ["t76c/E118"],
                "finding": "t76c L2 split blk+0..1 into 1B w{b}sd + 1B w{b}dn ({0,1}) and left blk+22 ({0,100}) unassigned. L3 static proves blk+0..1 (+0x00) is a 2B i16 w{b}sd (0..359) and blk+22 (+0x16) is w{b}dn ('tend') with 0x64 (100) as explicit NULL sentinel (WEATHER_SEASON::get 0x158f3e5, WEATHER::set 0x1590498/a2f/a5b/a87).",
            },
            {
                "id": "R3_derby_team_fk_and_server_6b_order",
                "prior_refs": ["t74/E115", "t76c/E118"],
                "finding": "DERBY::read (0x3d00950) always reads 4 lstrings (Dnam, Dsnm, Dasn, Danm); Dtm1/Dtm2 bind [db+0x98]=table_24 TEAM (not table_3 CLUB) via 0x3bf3460 and emit 'Ttea'; server-only 6B block gated at 0x3d00aae is D1tw@s28, D1td@s30, D1tl@s32; trailing pairs are Dfg1@c28/s34, Dfg2@c29/s35, Dwdr@c34/s40, Dntr@c35/s41 (correcting off-by-2 '36' typo in slots_client_18.json).",
            },
            {
                "id": "R4_media_full_grammar_and_7b_delta",
                "prior_refs": ["t74/E115", "t76b(absorbed)"],
                "finding": "MEDIA_SOURCE::read (0x15457c0) closes 208/208 rows on BOTH client (36,824B) and server (38,280B). Server-only block at 0x1545cfe = 1B Mper + 1B Mscp + 4B Mdlp + u8 cnt_jor(=0) = exactly +7B/row. Mcli stores 8B CLUB (duni,rdui) UID pairs (450/450 in table_3 UIDs) + lstr curl. t74's 16 distinct 5B-before-identity prefixes = u32(cnt_lnm=0 or last Mlnm ordinal) + u8(Mapc).",
            },
            {
                "id": "R5_rdui_ordinal_label_disambiguation",
                "prior_refs": ["t01f/E20", "t79/E117", "t76a/E120", "fm24_dump"],
                "finding": "Consistent with E20/E117/E120: fm24_dump 'award.rdui@64' and 'language.rdui_suffix@17' point to row ordinal (+0x08), whereas native rdui (+0x10) sits at @72 / suf+25 (equal to duni on 100% of rows and suppressed by DATABASE_RECORD::get 0xfe38a2 -> held).",
            },
        ],
        "preserved_negatives": [
            "t57/t63 negative results on club/comp/nation main rows untouched (out of t83 scope).",
            "17 xml fields across the 5 tables remain held with explicit first_counterexample (rdui x5, AWty/AWdr/AWxa/AWfo/AWsc/AWbr, Lfam/Lgro/Lsub, Mper/Mscp/Mdlp); candidates/violations are never promoted to L3.",
            "AWna/AWsn (award language layer) are non-wire in table_0.dat; AWsh is subtable-backed in table_12.dat.",
            "L4 = 0 (no game/editor launch).",
        ],
        "award_0": aw_fm,
        "language_8": la_fm,
        "derby_18": dr_fm,
        "weather_27": we_fm,
        "media_7": md_fm,
    }

    domain_stats = {
        "task": "t83",
        "evidence_level": "L1/L2 full-archive vectorized validation (no sampling); L4=0",
        "reference_table_counts": ref_n,
        "award_0": aw_dm,
        "language_8": la_dm,
        "derby_18": dr_dm,
        "weather_27": we_dm,
        "media_7": md_dm,
    }

    outdir.mkdir(parents=True, exist_ok=True)
    for fname, obj in [
        ("field_map.json", field_map),
        ("xref_award.json", aw_xr),
        ("xref_language.json", la_xr),
        ("xref_weather.json", we_xr),
        ("xref_derby.json", dr_xr),
        ("xref_media.json", md_xr),
        ("domain_stats.json", domain_stats),
    ]:
        (outdir / fname).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    return field_map["summary"]


# ---------------------------------------------------------------------------
# Self-test (unit + negative controls)
# ---------------------------------------------------------------------------
def run_selftest() -> bool:
    checks: list[tuple[str, bool, str]] = []

    # 1. Date validator positive & negative controls
    ok_dates = np.array([0x076C0001, (2024 << 16) | 366, (2023 << 16) | 365], dtype="<u4")
    bad_dates = np.array([(2023 << 16) | 366, (2024 << 16) | 0, (2024 << 16) | (1 << 9) | 1], dtype="<u4")
    c_ok = check_dates_vec(ok_dates)
    c_bad = check_dates_vec(bad_dates)
    checks.append(("date_pos_neg", c_ok["invalid"] == 0 and c_bad["invalid"] == 3, f"ok_inv={c_ok['invalid']} bad_inv={c_bad['invalid']}"))

    # 2. Enum validator catches out-of-enum and records first_counterexample
    dom_e, ce_e = enum_stats_vec(np.array([1, 2, 0, 9], dtype=np.int64), [1, 2, 3], np.array([10, 20, 30, 40], dtype=np.uint32))
    checks.append(("enum_neg_ce", dom_e["violations"] == 2 and ce_e is not None and ce_e["row"] == 2 and ce_e["raw_value"] == 0, str(ce_e)))

    # 3. Range validator respects eq100 (w{b}dn) and catches le0/out-of-range (AWxa)
    dom_dn, _ = int_range_stats_vec(np.array([0, 100, 50, 100], dtype=np.int64), 0, 50, np.arange(4, dtype=np.uint32), "eq100")
    dom_xa, ce_xa = int_range_stats_vec(np.array([0, 21, 7, 100], dtype=np.int64), 10, 99, np.array([1, 2, 3, 4], dtype=np.uint32), "le0")
    checks.append(("range_dn_xa", dom_dn["violations"] == 0 and dom_dn["suppressed_null"] == 2 and dom_xa["violations"] == 2 and ce_xa["row"] == 2, f"dn={dom_dn['violations']} xa={ce_xa}"))

    # 4. FK validator separates 0xffffffff (-1) vs valid 0 and computes wrong-UID control
    fk_d = fk_stats_vec(np.array([-1, 0, 2, 5], dtype=np.int32), 99, {99: 5}, {99: {100, 0}})
    checks.append(("fk_sep_and_miss", fk_d["null_0xffffffff_count"] == 1 and fk_d["valid_zero_count"] == 1 and fk_d["ordinal_miss"] == 1 and fk_d["wrong_uid_control_hits"] == 1, str(fk_d)))

    # 5. Live PE sanity on editor.exe (RTTI + weather wind/precip check)
    pe = MiniPE64(EXE_PATH)
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    rtti_ok = all(pe.rtti_name(cm["vtable_va"]) == cm["rtti"] for cm in CLASS_META.values())
    win0_ins = pe.dis_one(md, 0x158F30C)["text"]
    pre0_ins = pe.dis_one(md, 0x158F28E)["text"]
    checks.append(("pe_rtti_and_weather_win_pre", rtti_ok and "+ 2]" in win0_ins and "+ 7]" in pre0_ins, f"win0={win0_ins} | pre0={pre0_ins}"))

    all_ok = True
    for name, ok, detail in checks:
        print(f"{'PASS' if ok else 'FAIL'} selftest.{name}  {detail}")
        if not ok:
            all_ok = False
    return all_ok


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="t83 5-table L3 static + vectorized builder (award/language/weather/derby/media).")
    ap.add_argument("--outdir", type=Path, default=ROOT / "scratch/t83/out", help="Output directory (default: scratch/t83/out)")
    ap.add_argument("--selftest", action="store_true", help="Run self-tests and exit (does not build unless --build also given)")
    ap.add_argument("--build", action="store_true", help="Build all JSON deliverables into --outdir")
    args = ap.parse_args(argv)

    try:
        if args.selftest:
            if not run_selftest():
                return 1
            if not args.build:
                return 0
        summary = build_all(args.outdir)
        print(f"BUILT t83 -> {args.outdir}")
        print(json.dumps(summary, indent=2, ensure_ascii=False))
        return 0
    except Exception as exc:
        print(f"FATAL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
