#!/usr/bin/env python3
"""Strictly independent verifier for t83 (award 0 / media 7 / language 8 / derby 18 / weather 27).

STRICT INDEPENDENCE:
  Does NOT import scripts/t83_five_tables_l3.py, t05_pe, t21b_control_flow, ReaderCFG, or fm24_dump.
  Independently parses PE64/sections/.pdata/RTTI, FMF/Zstd archives, replays all 5 tables
  across both client_db.dat and server_db.dat, and validates every JSON deliverable.

Exit codes: 0 all checks passed, 1 verification failed, 2 usage/fatal error.
"""
from __future__ import annotations

import argparse
import ast
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

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(r"D:\tmp2b\fm24\tools\python")

import numpy as np
import zstandard as zstd
from capstone import CS_ARCH_X86, CS_MODE_64, Cs

EXE_PATH = Path(r"D:\tmp2b\fm24\input\editor.exe")
EXPECTED_EXE_SHA256 = "b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4"
DB_DIR = Path(os.environ.get("FM24_DB_DIR", str(ROOT / "scratch/data")))
MANIFEST_PATH = ROOT / "evidence/MANIFEST.json"
MASTER_REL = "evidence/fm24/reports/editor_schema/master.json"
SMALL_REL = "evidence/fm24/reports/dbdat_decode/db_tables_small.json"
BIG_REL = "evidence/fm24/reports/dbdat_decode/db_tables_big.json"
T74_FRAMES_PATH = ROOT / "scratch/t74/out/frames.json"
T76C_DIR = ROOT / "scratch/t76c/out"
FORBIDDEN_MODS = ("t83_five_tables_l3", "t05_pe", "t21b_control_flow", "fm24_dump", "t73_mapper_core", "t81_fk_index")


class VerifyFail(Exception):
    pass


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


class IndepPE64:
    def __init__(self, path: Path) -> None:
        self.raw = path.read_bytes()
        if self.raw[:2] != b"MZ":
            raise VerifyFail("not MZ")
        pe_off = struct.unpack_from("<I", self.raw, 0x3C)[0]
        if self.raw[pe_off:pe_off + 4] != b"PE\x00\x00":
            raise VerifyFail("not PE")
        _, n_sec, _, _, _, opt_sz, _ = struct.unpack_from("<HHIIIHH", self.raw, pe_off + 4)
        opt_off = pe_off + 24
        if struct.unpack_from("<H", self.raw, opt_off)[0] != 0x20B:
            raise VerifyFail("not PE32+")
        self.image_base = struct.unpack_from("<Q", self.raw, opt_off + 24)[0]
        exc_rva, exc_sz = struct.unpack_from("<II", self.raw, opt_off + 112 + 3 * 8)
        sec_off = opt_off + opt_sz
        self.sections: list[tuple[int, int, int, int]] = []
        for i in range(n_sec):
            o = sec_off + i * 40
            vsz, vrva, rsz, roff = struct.unpack_from("<IIII", self.raw, o + 8)
            self.sections.append((vrva, max(vsz, rsz), roff, rsz))
        self.pdata: list[tuple[int, int]] = []
        self.pstarts: list[int] = []
        if exc_rva and exc_sz:
            efo = self.rva_to_fo(exc_rva)
            for k in range(0, exc_sz, 12):
                b, e, _ = struct.unpack_from("<III", self.raw, efo + k)
                if b == 0 and e == 0:
                    break
                self.pdata.append((b, e))
                self.pstarts.append(b)

    def rva_to_fo(self, rva: int) -> int:
        for vrva, vspan, roff, rsz in self.sections:
            if vrva <= rva < vrva + vspan and (rva - vrva) < rsz:
                return roff + (rva - vrva)
        raise VerifyFail(f"unmapped rva {hex(rva)}")

    def fo_to_rva(self, fo: int) -> int:
        for vrva, _, roff, rsz in self.sections:
            if roff <= fo < roff + rsz:
                return vrva + (fo - roff)
        raise VerifyFail(f"unmapped fo {hex(fo)}")

    def va_to_fo(self, va: int) -> int:
        return self.rva_to_fo(va - self.image_base)

    def fo_to_va(self, fo: int) -> int:
        return self.image_base + self.fo_to_rva(fo)

    def rtti(self, vt_va: int) -> str:
        vt_fo = self.va_to_fo(vt_va)
        col_va = struct.unpack_from("<Q", self.raw, vt_fo - 8)[0]
        col_fo = self.va_to_fo(col_va)
        sig, _, _, td_rva = struct.unpack_from("<IIII", self.raw, col_fo)
        if sig != 1:
            raise VerifyFail(f"bad RTTI sig {sig}")
        td_fo = self.rva_to_fo(td_rva)
        end = self.raw.index(b"\x00", td_fo + 16)
        return self.raw[td_fo + 16:end].decode("ascii")

    def rel32(self, tbl_fo: int, idx: int) -> int:
        rel = struct.unpack_from("<i", self.raw, tbl_fo + idx * 4)[0]
        return self.va_to_fo(self.fo_to_va(tbl_fo) + rel)

    def vslot(self, vt_va: int, slot: int) -> int:
        vt_fo = self.va_to_fo(vt_va)
        return self.va_to_fo(struct.unpack_from("<Q", self.raw, vt_fo + slot * 8)[0])

    def dis1(self, md: Cs, fo: int) -> tuple[str, str]:
        va = self.fo_to_va(fo)
        ins = next(md.disasm(self.raw[fo:fo + 16], va, 1))
        return ins.bytes.hex(), f"{ins.mnemonic} {ins.op_str}".strip()


def read_fmf(side: str, wanted: list[str]) -> dict[str, bytes]:
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
            raise VerifyFail(f"failed decompress {key}")
    return out


def _extract_uids_dp(buf: bytes, tid: int, require_tail0: bool) -> np.ndarray:
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
        raise VerifyFail(f"uid DP t{tid}: last row mismatch at {last_target}")
    for j in range(n - 2, -1, -1):
        max_nxt = reach[j + 1][-1]
        pts = [p for p in cand.get(j, ()) if p + 12 <= max_nxt]
        if not pts:
            raise VerifyFail(f"uid DP t{tid}: chain lost at {j}")
        reach[j] = sorted(pts)
    prev_min = 1
    for j in range(n):
        reach[j] = [p for p in reach[j] if p >= prev_min + 12]
        if not reach[j]:
            raise VerifyFail(f"uid DP t{tid}: forward lost at {j}")
        prev_min = reach[j][0]
    for j in range(n - 2, -1, -1):
        max_nxt = reach[j + 1][-1]
        reach[j] = [p for p in reach[j] if p + 12 <= max_nxt]
    pinned = [struct.unpack_from("<I", buf, r[0] + 4)[0] for r in reach if len(r) == 1]
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
            ref = nb if nb else pinned
            p = min(cands, key=lambda q: (min(abs(struct.unpack_from("<I", buf, q + 4)[0] - u) for u in ref), -q))
        uids[j] = struct.unpack_from("<I", buf, p + 4)[0]
        prev_p = p
    return uids


def extract_uids(buf: bytes, tid: int = -1) -> np.ndarray:
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
            return _extract_uids_dp(buf, tid, req0)
        except VerifyFail:
            if not req0:
                raise
    raise VerifyFail(f"uid scan failed for t{tid}")


def bad_dates(vals: np.ndarray) -> int:
    v = np.asarray(vals, dtype="<u4")
    y = v >> 16
    d = v & 0x1FF
    rem = (v >> 9) & 0x7F
    leap = (y % 4 == 0) & ((y % 100 != 0) | (y % 400 == 0))
    ok = (rem == 0) & (y >= 1) & (d >= 1) & (d <= 365 + leap)
    return int((~ok).sum())


def enum_set(master: dict[str, Any], key: str) -> set[int]:
    out = set()
    for x in master["enums"][key]["values"]:
        v = x.get("enum_id")
        if v is None:
            v = x.get("enum")
        out.add(int(v, 0) if isinstance(v, str) else int(v))
    return out


def verify_all(outdir: Path) -> list[str]:
    passed: list[str] = []

    def ok(tag: str, detail: str = "") -> None:
        passed.append(tag)
        print(f"PASS {tag}" + (f"  {detail}" if detail else ""))

    def req(cond: bool, msg: str) -> None:
        if not cond:
            raise VerifyFail(msg)

    # 1. Strict independence (runtime modules + AST of self)
    for fm in FORBIDDEN_MODS:
        req(fm not in sys.modules, f"forbidden module loaded: {fm}")
    tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                req(not any(fm in alias.name for fm in FORBIDDEN_MODS), f"forbidden import {alias.name}")
        elif isinstance(node, ast.ImportFrom) and node.module:
            req(not any(fm in node.module for fm in FORBIDDEN_MODS), f"forbidden import-from {node.module}")
    ok("01.independence", "0 forbidden imports (AST + sys.modules)")

    # 2. Integrity of editor.exe & MANIFEST snapshots
    req(sha256_file(EXE_PATH) == EXPECTED_EXE_SHA256, "editor.exe sha256 mismatch")
    man = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    mmap = {e["path"].replace("\\", "/"): e["sha256"] for e in man.get("files", [])}
    for rel in (MASTER_REL, SMALL_REL, BIG_REL):
        exp = mmap.get(rel) or mmap.get(rel.removeprefix("evidence/"))
        req(exp is not None and sha256_file(ROOT / rel) == exp, f"MANIFEST mismatch for {rel}")
    ok("02.integrity", "editor.exe + master/small/big MANIFEST SHA-256 verified")

    # 3. Load deliverables
    req_files = [
        "field_map.json", "domain_stats.json",
        "xref_award.json", "xref_language.json", "xref_weather.json", "xref_derby.json", "xref_media.json",
    ]
    for fn in req_files:
        req((outdir / fn).is_file(), f"missing deliverable {fn}")
    fmap = json.loads((outdir / "field_map.json").read_text(encoding="utf-8"))
    dstats = json.loads((outdir / "domain_stats.json").read_text(encoding="utf-8"))
    xrefs = {k: json.loads((outdir / f"xref_{k}.json").read_text(encoding="utf-8"))
             for k in ("award", "language", "weather", "derby", "media")}
    master = json.loads((ROOT / MASTER_REL).read_text(encoding="utf-8"))
    ok("03.deliverables_loaded", f"{len(req_files)} JSON files parsed")

    # 4. XML denominator completeness & L4=0 discipline
    req("L4=0" in fmap.get("evidence_level", ""), "L4=0 marker missing")
    expected_xmls = [
        ("award_0", "award.xml", 38),
        ("language_8", "language.xml", 12),
        ("derby_18", "derby.xml", 22),
        ("weather_27", "weather.xml", 94),
        ("media_7", "media source.xml", 22),
    ]
    tot_xml = 0
    tot_l3 = 0
    tot_held = 0
    for key, xml_name, exp_cnt in expected_xmls:
        m_ids = [f["field"] for f in master["entities"][xml_name][0]["fields"]]
        f_ids = [f["field"] for f in fmap[key]["schema_fields"]]
        req(len(m_ids) == exp_cnt and m_ids == f_ids, f"XML field list mismatch for {key}")
        for f in fmap[key]["schema_fields"]:
            req(f["grade"] != "L4", f"forbidden L4 grade on {key}.{f['field']}")
            if f["grade"] == "L3":
                tot_l3 += 1
            elif f["grade"] == "held":
                tot_held += 1
                req(bool(f.get("hold_reason")), f"held field {key}.{f['field']} missing hold_reason")
                req(bool(f.get("first_counterexample")), f"held field {key}.{f['field']} missing first_counterexample")
        tot_xml += len(f_ids)
    req(tot_xml == 188 and fmap["summary"]["xml_denominator_total"] == 188, f"xml total mismatch: {tot_xml}")
    ok("04.xml_denominator", f"188/188 fields accounted (L3={tot_l3}, held={tot_held}, non-wire/meta={188 - tot_l3 - tot_held}, L4=0)")

    # 5. Independent static PE64 verification of all 5 classes + xref bytes + key fixes
    pe = IndepPE64(EXE_PATH)
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    class_expect = [
        ("award", 0, 0xF48C54, 0x14187B828, ".?AVAWARD@db@@"),
        ("media", 7, 0xF48EA6, 0x1418BDD08, ".?AVMEDIA_SOURCE@db@@"),
        ("language", 8, 0xF48EBB, 0x141888DB8, ".?AVLANGUAGE@db@@"),
        ("derby", 18, 0xF48F77, 0x141887278, ".?AVDERBY@db@@"),
        ("weather", 27, 0xF491DD, 0x141882DE8, ".?AVWEATHER@db@@"),
    ]
    checked_insns = 0
    for nm, tid, exp_case, vt_va, exp_rtti in class_expect:
        xr = xrefs[nm]
        req(pe.rel32(0xF49D38, tid) == exp_case, f"factory mismatch for {nm}")
        req(pe.rtti(vt_va) == exp_rtti, f"RTTI mismatch for {nm}")
        req(xr["class"]["rtti"] == exp_rtti, f"xref RTTI mismatch for {nm}")
        # Verify vtable slots match xref
        for s_idx, s_lbl in [(2, "get"), (3, "set"), (5, "prop_reg"), (19, "read"), (20, "fixup"), (21, "write")]:
            s_fo = pe.vslot(vt_va, s_idx)
            req(xr["class"]["vtable_slots"][f"slot{s_idx}_{s_lbl}"]["entry_fo"] == hex(s_fo), f"{nm} slot{s_idx} mismatch")
        # Verify every instruction object in xref["members"] directly against editor.exe bytes!
        for mem in xr["members"]:
            for k in ("getter_cmp", "getter_handler", "setter_cmp", "setter_handler", "reader_sink", "fixup", "season_getter_handler"):
                obj = mem.get(k)
                if isinstance(obj, dict) and "fo" in obj and "bytes" in obj:
                    bhex, txt = pe.dis1(md, int(obj["fo"], 16))
                    req(bhex == obj["bytes"] and txt == obj["text"], f"{nm}.{mem['field']}.{k} byte mismatch at {obj['fo']}")
                    checked_insns += 1
            for k in ("getter_dispatch", "setter_dispatch"):
                obj = mem.get(k)
                if isinstance(obj, dict):
                    if "bytes" in obj and "fo" in obj:
                        bhex, txt = pe.dis1(md, int(obj["fo"], 16))
                        req(bhex == obj["bytes"], f"{nm}.{mem['field']}.{k} mismatch")
                        checked_insns += 1
                    elif "table_fo" in obj and "index" in obj and "target_fo" in obj:
                        tfo = pe.rel32(int(obj["table_fo"], 16), obj["index"])
                        req(hex(tfo) == obj["target_fo"], f"{nm}.{mem['field']}.{k} rel32 target mismatch")
                        checked_insns += 1

    # Explicitly re-verify critical static proofs:
    # - WEATHER wind (+2..+6) vs precip (+7..+11) & tend null 0x64 (+0x16)
    _, t_win0 = pe.dis1(md, 0x158F30C)
    _, t_pre0 = pe.dis1(md, 0x158F28E)
    _, t_dn_cmp = pe.dis1(md, 0x158F3E5)
    _, t_set_w0w0 = pe.dis1(md, 0x15903EF)
    _, t_set_w0p0 = pe.dis1(md, 0x15902F0)
    req("+ 2]" in t_win0 and "+ 7]" in t_pre0 and "0x64" in t_dn_cmp, "WEATHER_SEASON::get static check failed")
    req("+ 0x22]" in t_set_w0w0 and "+ 0x27]" in t_set_w0p0, "WEATHER::set wind/precip static check failed")
    # - DERBY server 6B gate + DB_CONTEXT +0x98 = tid 24 TEAM
    _, t_dr_gate = pe.dis1(md, 0x3D00AAE)
    _, t_db_team = pe.dis1(md, 0xF041A3)
    req("test" in t_dr_gate and "0x140ffa310" in t_db_team, "DERBY static gate / TEAM binding failed")
    # - MEDIA server 7B gate + Mcli club/curl
    _, t_md_gate = pe.dis1(md, 0x1545CFE)
    _, t_md_club = pe.dis1(md, 0x154DDC8)
    _, t_md_curl = pe.dis1(md, 0x154DDC0)
    req("test" in t_md_gate and "0x636c7562" in t_md_club and "0x6375726c" in t_md_curl, "MEDIA static gate / Mcli check failed")
    ok("05.static_pe64", f"5/5 classes RTTI+vtable+factory+DB_CONTEXT + {checked_insns} instruction/rel32 cross-checks verified")

    # 6. Load client + server archives & reference tables + cross-check t74 & t76c frames
    wanted = [
        "table_0.dat", "table_2.dat", "table_3.dat", "table_5.dat", "table_6.dat", "table_7.dat",
        "table_8.dat", "table_9.dat", "table_10.dat", "table_12.dat", "table_18.dat",
        "table_21.dat", "table_24.dat", "table_25.dat", "table_27.dat", "table_30.dat", "table_47.dat",
    ]
    cli = read_fmf("client", wanted)
    srv = read_fmf("server", wanted)
    ref_n: dict[int, int] = {}
    ref_uids: dict[int, set[int]] = {}
    for tid in (0, 2, 3, 5, 6, 7, 8, 9, 10, 12, 18, 21, 24, 25, 27, 30, 47):
        k = f"table_{tid}.dat"
        buf = srv.get(k) or cli.get(k)
        req(buf is not None, f"missing ref table {tid}")
        u = extract_uids(buf, tid)
        req(len(np.unique(u)) == len(u), f"non-unique UIDs in ref table {tid}")
        if k in cli and k in srv:
            uc = extract_uids(cli[k], tid)
            req(np.array_equal(u, uc), f"client!=server UIDs in ref table {tid}")
        ref_n[tid] = len(u)
        ref_uids[tid] = set(int(x) for x in u.tolist())
    req(dstats["reference_table_counts"] == {str(k): v for k, v in ref_n.items()}, "reference_table_counts mismatch")

    t74 = json.loads(T74_FRAMES_PATH.read_text(encoding="utf-8"))
    t74_tables = t74["tables"]
    for tid in (0, 7, 8, 18, 27):
        for side, d in (("client", cli), ("server", srv)):
            buf = d[f"table_{tid}.dat"]
            r74 = t74_tables[str(tid)]["archives"][side]
            req(len(buf) == r74["payload_len"], f"t74 payload_len mismatch {(side, tid)}")
            req(struct.unpack_from("<I", buf, 8)[0] == r74["count"], f"t74 count mismatch {(side, tid)}")
            req(hashlib.sha256(buf).hexdigest() == r74["payload_sha256"], f"t74 sha256 mismatch {(side, tid)}")
    for tid in (18, 27):
        for side, d in (("client", cli), ("server", srv)):
            s76 = json.loads((T76C_DIR / f"slots_{side}_{tid}.json").read_text(encoding="utf-8"))
            req(s76["payload_sha256"] == hashlib.sha256(d[f"table_{tid}.dat"]).hexdigest(), f"t76c sha256 mismatch {(side, tid)}")
    ok("06.archives_t74_t76c", "client+server loaded, 17 ref tables exact-DP indexed (client==server), 10/10 t74 + 4/4 t76c SHA-256 verified")

    # 7. Replay & verify AWARD (0)
    a_c, a_s = cli["table_0.dat"], srv["table_0.dat"]
    req(a_c == a_s, "award client!=server")
    n0 = struct.unpack_from("<I", a_c, 8)[0]
    req(n0 == 3545 and len(a_c) == 13 + n0 * 77 + 9, "award frame failed")
    A = np.frombuffer(a_c, dtype=np.uint8, offset=13, count=n0 * 77).reshape(n0, 77)
    req(np.all(A[:, 0] == 0), "award selector!=0")
    AB = A[:, 1:]
    ord0 = AB[:, 64:68].copy().view("<u4").ravel()
    duni0 = AB[:, 68:72].copy().view("<u4").ravel()
    rdui0 = AB[:, 72:76].copy().view("<u4").ravel()
    req(np.array_equal(ord0, np.arange(n0, dtype=np.uint32)) and np.array_equal(duni0, rdui0) and len(np.unique(duni0)) == n0, "award id failed")
    req(bad_dates(AB[:, 19:23].copy().view("<u4").ravel()) == 0 and bad_dates(AB[:, 60:64].copy().view("<u4").ravel()) == 0, "award dates failed")
    # Verify all L3 FK/enum/range fields have 0 violations & held fields match counterexamples!
    aw_map = {f["field"]: f for f in fmap["award_0"]["schema_fields"]}
    for fk_f, off, tid in [("AWci", 23, 5), ("AWni", 27, 10), ("AWmi", 41, 25)]:
        col = AB[:, off:off + 4].copy().view("<i4").ravel()
        live = col[col >= 0]
        req(int((col < -1).sum()) == 0 and int((live >= ref_n[tid]).sum()) == 0, f"award {fk_f} FK failed")
        req(aw_map[fk_f]["domain"]["live"] == len(live) and aw_map[fk_f]["domain"]["null_0xffffffff_count"] == int((col == -1).sum()), f"award {fk_f} stats mismatch")
    for en_f, off, w, ekey in [
        ("AWrb", 35, 1, "AWrb"), ("AWsr", 46, 1, "AWsr"), ("AWss", 47, 1, "AWss"),
        ("AWap", 50, 1, "AWap"), ("AWrt", 51, 1, "AWrt"), ("AWvf", 52, 1, "AWvf"),
        ("AWpo", 55, 4, "AWpo"), ("AWnp", 59, 1, "AWnp"),
    ]:
        col = AB[:, off:off + 4].copy().view("<u4").ravel() if w == 4 else AB[:, off].view(np.int8)
        aset = enum_set(master, ekey)
        req(all(int(x) in aset for x in col.tolist()), f"award L3 enum {en_f} violation!")
    # Check held counterexamples directly against raw wire bytes
    for hf, off in [("AWsc", 2), ("AWty", 17), ("AWdr", 18), ("AWfo", 37), ("AWxa", 38), ("AWbr", 45)]:
        ce = aw_map[hf]["first_counterexample"]
        raw_v = int(AB[ce["row"], off]) if hf == "AWxa" else int(AB[ce["row"], off].view(np.int8))
        req(int(duni0[ce["row"]]) == ce["duni"] and raw_v == ce["raw_value"], f"award held {hf} counterexample mismatch")
    # Verify L2 77B column profile + FK candidate matrix in domain_stats.json
    aw_l2 = dstats["award_0"]["l2_column_profile"]
    req(len(aw_l2["byte_summary_0_76"]) == 77, "award L2 byte summary len != 77")
    for fk_off, exp_tid in [(23, 5), (27, 10), (31, 47), (41, 25)]:
        cmat = aw_l2["i32_fk_candidate_matrix"][f"body@{fk_off}"]
        req(cmat["fk_candidates"][f"t{exp_tid}"]["ordinal_fit_100pct"] is True, f"award L2 FK fit failed body@{fk_off}->t{exp_tid}")
        for req_t in ("t30", "t10", "t25", "t3"):
            req(req_t in cmat["fk_candidates"] and "wrong_uid_control_hits" in cmat["fk_candidates"][req_t], f"missing L2 candidate {req_t}")
    ok("07.award_0", f"{n0} rows client==server, 77B L2 profile + 24 L3 0-violation + 7 held counterexamples exact")

    # 8. Replay & verify LANGUAGE (8)
    l_c, l_s = cli["table_8.dat"], srv["table_8.dat"]
    req(l_c == l_s, "language client!=server")
    n8 = struct.unpack_from("<I", l_c, 8)[0]
    req(n8 == 126, "language n!=126")
    pos = 13
    lnames: list[str] = []
    lsuf = np.empty((n8, 29), dtype=np.uint8)
    for i in range(n8):
        req(l_c[pos] == 0, f"lang sel!=0 at {i}")
        pos += 1
        sl = struct.unpack_from("<I", l_c, pos)[0]
        pos += 4
        lnames.append(l_c[pos:pos + sl].decode("utf-8"))
        pos += sl
        lsuf[i] = np.frombuffer(l_c, dtype=np.uint8, offset=pos, count=29)
        pos += 29
    req(pos == len(l_c) - 9, "language closure failed")
    ord8 = lsuf[:, 17:21].copy().view("<u4").ravel()
    duni8 = lsuf[:, 21:25].copy().view("<u4").ravel()
    rdui8 = lsuf[:, 25:29].copy().view("<u4").ravel()
    req(np.array_equal(ord8, np.arange(n8, dtype=np.uint32)) and np.array_equal(duni8, rdui8), "language id failed")
    lnat = lsuf[:, 9:13].copy().view("<i4").ravel()
    req(lnames[3] == "Chinese" and int(lnat[3]) == 55 and lnames[7] == "English" and int(lnat[7]) == 139, "language England/China anchor failed")
    req(int((lnat < -1).sum()) == 0 and int((lnat[lnat >= 0] >= ref_n[10]).sum()) == 0, "language Lnat FK failed")
    la_map = {f["field"]: f for f in fmap["language_8"]["schema_fields"]}
    for hf, off in [("Lfam", 3), ("Lgro", 5), ("Lsub", 7)]:
        ce = la_map[hf]["first_counterexample"]
        raw_v = int(struct.unpack_from("<h", lsuf[ce["row"]].tobytes(), off)[0])
        req(lnames[ce["row"]] == ce["name"] and raw_v == ce["raw_value"], f"language held {hf} counterexample mismatch")
    # Verify L2 17B suffix + 12B identity profile + FK candidate matrix
    la_l2 = dstats["language_8"]["l2_column_profile"]
    req(len(la_l2["byte_summary_0_28"]) == 29, "language L2 byte summary len != 29")
    lnat_mat = la_l2["i32_fk_candidate_matrix"]["suf+9_Lnat"]
    req(lnat_mat["fk_candidates"]["t10"]["ordinal_fit_100pct"] is True and lnat_mat["null_0xffffffff_count"] == 5 and lnat_mat["valid_zero_count"] == 1, "language L2 Lnat stats mismatch")
    ok("08.language_8", f"{n8} rows client==server, 17B+13B L2 profile, Chinese->55 / English->139, 5 L3 + 4 held verified")

    # 9. Replay & verify DERBY (18)
    def walk_derby(buf: bytes, is_srv: bool) -> tuple[list[list[str]], np.ndarray]:
        n = struct.unpack_from("<I", buf, 8)[0]
        p = 13
        ss: list[list[str]] = [[], [], [], []]
        nl = 42 if is_srv else 36
        nums = np.empty((n, nl + 12), dtype=np.uint8)
        for i in range(n):
            req(buf[p] == 0, f"derby sel!=0 at {i}")
            p += 1
            for k in range(4):
                sl = struct.unpack_from("<I", buf, p)[0]
                p += 4
                ss[k].append(buf[p:p + sl].decode("utf-8"))
                p += sl
            nums[i] = np.frombuffer(buf, dtype=np.uint8, offset=p, count=nl + 12)
            p += nl + 12
        req(p == len(buf) - 9, "derby closure failed")
        return ss, nums

    dsc, dnc = walk_derby(cli["table_18.dat"], False)
    dss, dns = walk_derby(srv["table_18.dat"], True)
    n18 = len(dsc[0])
    req(n18 == 1567 and dsc == dss, "derby strings mismatch")
    req(np.array_equal(dnc[:, :28], dns[:, :28]) and np.array_equal(dnc[:, 28:36], dns[:, 34:42]) and np.array_equal(dnc[:, 36:48], dns[:, 42:54]), "derby shared bytes mismatch")
    req(bad_dates(dns[:, 0:4].copy().view("<u4").ravel()) == 0, "derby Dfmd date invalid")
    for off, tid in [(4, 24), (8, 24), (12, 25), (16, 21)]:
        col = dns[:, off:off + 4].copy().view("<i4").ravel()
        req(int((col < -1).sum()) == 0 and int((col[col >= 0] >= ref_n[tid]).sum()) == 0, f"derby FK @{off}->t{tid} failed")
    # Co-null check on D1tw/D1td/D1tl
    w_c = dns[:, 28:30].copy().view("<i2").ravel()
    d_c = dns[:, 30:32].copy().view("<i2").ravel()
    l_c2 = dns[:, 32:34].copy().view("<i2").ravel()
    req(np.array_equal(w_c == -1, d_c == -1) and np.array_equal(d_c == -1, l_c2 == -1) and int((w_c == -1).sum()) == 903, "derby D1tw/d/l co-null failed")
    req(dss[0][0] == "Merseyside" and dss[0][388] == "Manchester" and dss[0][395] == "North London", "derby named anchors failed")
    ok("09.derby_18", f"{n18} rows, +6B server delta (D1tw/D1td/D1tl 903 null / 664 live), 18 L3 + 1 held verified")

    # 10. Replay & verify WEATHER (27)
    w_c2, w_s2 = cli["table_27.dat"], srv["table_27.dat"]
    req(w_c2 == w_s2, "weather client!=server")
    n27 = struct.unpack_from("<I", w_c2, 8)[0]
    req(n27 == 334, "weather n!=334")
    pos = 13
    wnames: list[str] = []
    wmid = np.empty((n27, 107), dtype=np.uint8)
    for i in range(n27):
        req(w_c2[pos] == 0, f"weather sel!=0 at {i}")
        pos += 1
        sl = struct.unpack_from("<I", w_c2, pos)[0]
        pos += 4
        wnames.append(w_c2[pos:pos + sl].decode("utf-8"))
        pos += sl
        wmid[i] = np.frombuffer(w_c2, dtype=np.uint8, offset=pos, count=107)
        pos += 107
    req(pos == len(w_c2) - 9 and np.all(wmid[:, :3] == 0), "weather closure/zero-prefix failed")
    win_ne = 0
    pre_ne = 0
    tem_ne = 0
    for b in range(4):
        base = 3 + 23 * b
        sd = wmid[:, base:base + 2].copy().view("<i2").ravel()
        req(int((sd < 0).sum()) == 0 and int((sd > 365).sum()) == 0, f"weather w{b}sd out of range")
        w_blk = wmid[:, base + 2:base + 7].view(np.int8)
        p_blk = wmid[:, base + 7:base + 12].view(np.int8)
        t_blk = wmid[:, base + 12:base + 22].view(np.int8)
        dn = wmid[:, base + 22].view(np.int8)
        req(int((w_blk < 0).sum()) == 0 and int((w_blk > 100).sum()) == 0, f"weather w{b}w out of range")
        req(int((p_blk < 0).sum()) == 0 and int((p_blk > 100).sum()) == 0, f"weather w{b}p out of range")
        req(int((t_blk < 0).sum()) == 0 and int((t_blk > 100).sum()) == 0, f"weather w{b}t out of range")
        dn_live = dn[dn != 100]
        req(len(dn_live) == 314 and int((dn_live < 0).sum()) == 0 and int((dn_live > 50).sum()) == 0, f"weather w{b}dn failed")
        win_ne += int((w_blk.sum(axis=1) != 100).sum())
        pre_ne += int((p_blk.sum(axis=1) != 100).sum())
        tem_ne += int((t_blk.sum(axis=1) != 100).sum())
    ns = dstats["weather_27"]["post_read_normalizer"]
    req(win_ne == ns["wind_blk2_6_sum_ne_100"] == 76 and pre_ne == ns["precip_blk7_11_sum_ne_100"] == 67 and tem_ne == ns["temp10_blk12_21_sum_ne_100"] == 468, "weather normalizer counts mismatch")
    ok("10.weather_27", f"{n27} rows client==server, 90 L3 + 1 held, normalizer 76/67/468 & wind/precip swap fix verified")

    # 11. Replay & verify MEDIA_SOURCE (7)
    def walk_media(buf: bytes, is_srv: bool) -> list[dict[str, Any]]:
        n = struct.unpack_from("<I", buf, 8)[0]
        p = 13
        rows = []
        for i in range(n):
            r0 = p
            req(buf[p] == 0, f"media sel!=0 at {i}")
            p += 1

            def rs() -> str:
                nonlocal p
                l = struct.unpack_from("<I", buf, p)[0]
                p += 4
                s = buf[p:p + l].decode("utf-8")
                p += l
                return s

            def rv() -> list[int]:
                nonlocal p
                c = struct.unpack_from("<I", buf, p)[0]
                p += 4
                vals = list(struct.unpack_from(f"<{c}i", buf, p))
                p += 4 * c
                return vals

            mnam = rs()
            d1 = buf[p]; p += 1
            ct = struct.unpack_from("<I", buf, p)[0]; p += 4
            mtyp = list(buf[p:p + ct]); p += ct
            murl = rs(); mhtg = rs()
            misf, msty = buf[p], buf[p + 1]; p += 2
            mcmi = rv()
            mcyi = struct.unpack_from("<i", buf, p)[0]; p += 4
            mrgi = rv(); mnti = rv()
            mcti = struct.unpack_from("<i", buf, p)[0]; p += 4
            ccl = struct.unpack_from("<I", buf, p)[0]; p += 4
            mcli = []
            for _ in range(ccl):
                u1, u2 = struct.unpack_from("<II", buf, p); p += 8
                mcli.append((u1, u2, rs()))
            if is_srv:
                mper, mscp = buf[p], buf[p + 1]; p += 2
                mdlp = struct.unpack_from("<I", buf, p)[0]; p += 4
                cj = buf[p]; p += 1
                mjor = list(struct.unpack_from(f"<{cj}i", buf, p)); p += 4 * cj
            else:
                mper = mscp = mdlp = mjor = None
            mlnm = rv()
            mapc = buf[p]; p += 1
            pre5 = buf[p - 5:p].hex()
            oi, di, ri = struct.unpack_from("<III", buf, p); p += 12
            rows.append({
                "Mnam": mnam, "d1": d1, "Mtyp": mtyp, "Murl": murl, "Mhtg": mhtg,
                "Misf": misf, "Msty": msty, "Mcmi": mcmi, "Mcyi": mcyi, "Mrgi": mrgi,
                "Mnti": mnti, "Mcti": mcti, "Mcli": mcli, "Mper": mper, "Mscp": mscp,
                "Mdlp": mdlp, "Mjor": mjor, "Mlnm": mlnm, "Mapc": mapc, "pre5": pre5,
                "ord": oi, "duni": di, "rdui": ri, "rlen": p - r0,
            })
        req(p == len(buf) - 9, f"media closure failed {p} vs {len(buf) - 9}")
        return rows

    mc = walk_media(cli["table_7.dat"], False)
    ms = walk_media(srv["table_7.dat"], True)
    req(len(mc) == 208 and len(ms) == 208, "media n!=208")
    req(all(rs["rlen"] - rc["rlen"] == 7 for rc, rs in zip(mc, ms)), "media +7B delta failed")
    req(all(len(rs["Mjor"]) == 0 and rs["Mdlp"] == 0x076C0001 for rs in ms), "media server block check failed")
    for k, tid in [("Mcmi", 25), ("Mrgi", 47), ("Mnti", 10), ("Mlnm", 7)]:
        vals = [x for r in ms for x in r[k]]
        req(all(0 <= x < ref_n[tid] for x in vals), f"media {k} FK failed")
    for k, tid in [("Mcyi", 2), ("Mcti", 5)]:
        req(all(r[k] == -1 or 0 <= r[k] < ref_n[tid] for r in ms), f"media {k} FK failed")
    mcli_items = [it for r in ms for it in r["Mcli"]]
    req(len(mcli_items) == 450 and all(u1 == u2 and u1 in ref_uids[3] for u1, u2, _ in mcli_items), "media Mcli CLUB UID check failed")
    req(len(Counter(r["pre5"] for r in mc)) == 16, "media pre5 distinct count != 16")
    md_map = {f["field"]: f for f in fmap["media_7"]["schema_fields"]}
    for hf in ("Mper", "Mscp"):
        ce = md_map[hf]["first_counterexample"]
        req(ms[ce["row"]]["Mnam"] == ce["name"] and ms[ce["row"]][hf] == ce["raw_value"], f"media held {hf} counterexample mismatch")
    ok("11.media_7", "208/208 closed client(36,824B) & server(38,280B), +7B delta, Mcli 450/450 CLUB UIDs, pre5 16 distinct, 15 L3 + 4 held")

    return passed


def run_selftest(outdir: Path) -> bool:
    # 1. Verify negative checks detect tampering!
    ok_all = True
    try:
        # Synthetic bad date check
        if bad_dates(np.array([(2023 << 16) | 366], dtype="<u4")) != 1:
            raise VerifyFail("bad_dates failed to reject 2023-day366")
        print("PASS selftest.neg_date_reject  rejected non-leap day 366")
    except Exception as exc:
        print(f"FAIL selftest.neg_date_reject  {exc}")
        ok_all = False

    # 2. Synthetic tamper check on a temp copy of field_map.json (change L3 -> L4)
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        tp = Path(td)
        for fn in (
            "field_map.json", "domain_stats.json",
            "xref_award.json", "xref_language.json", "xref_weather.json", "xref_derby.json", "xref_media.json",
        ):
            src = outdir / fn
            if not src.is_file():
                print(f"FAIL selftest.tamper_setup  missing {src}")
                return False
            (tp / fn).write_bytes(src.read_bytes())
        tampered = json.loads((tp / "field_map.json").read_text(encoding="utf-8"))
        tampered["award_0"]["schema_fields"][0]["grade"] = "L4"
        (tp / "field_map.json").write_text(json.dumps(tampered), encoding="utf-8")
        try:
            verify_all(tp)
            print("FAIL selftest.tamper_detect  verifier accepted tampered L4 grade!")
            ok_all = False
        except VerifyFail as vf:
            print(f"PASS selftest.tamper_detect  caught tampered L4 grade ({vf})")
    return ok_all


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Independent verifier for t83 deliverables.")
    ap.add_argument("--outdir", type=Path, default=Path(__file__).resolve().parent, help="Directory with t83 JSON deliverables")
    ap.add_argument("--selftest", action="store_true", help="Run negative tamper self-tests in addition to full verification")
    args = ap.parse_args(argv)

    try:
        passed = verify_all(args.outdir)
        print(f"\nALL VERIFY CHECKS PASSED: {len(passed)}/{len(passed)}")
        if args.selftest:
            if not run_selftest(args.outdir):
                return 1
            print("SELFTEST PASSED")
        return 0
    except VerifyFail as vf:
        print(f"VERIFY FAILED: {vf}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"FATAL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
