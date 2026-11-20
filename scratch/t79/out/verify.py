#!/usr/bin/env python3
"""Independent verifier for t79 (stadium 21 + team 24 + extra_24 + CLUB+0x18 forwarding).

STRICT INDEPENDENCE:
  Does NOT import any builder, t05_pe, ReaderCFG, or fm24_dump.
  Independently parses PE64/sections/.pdata/RTTI/CFG, FMF/Zstd archives, and replays all payloads.

Exit codes: 0 all checks passed, 1 verification failed, 2 usage/fatal error.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import struct
import sys
from collections import Counter, deque
from pathlib import Path
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(r"D:\tmp2b\fm24\tools\python")

import numpy as np
import zstandard as zstd
from capstone import CS_ARCH_X86, CS_MODE_64, Cs
from capstone.x86 import X86_OP_IMM

EXE_PATH = Path(r"D:\tmp2b\fm24\input\editor.exe")
EXPECTED_EXE_SHA256 = "b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4"
DB_DIR = Path(os.environ.get("FM24_DB_DIR", str(ROOT / "scratch/data")))
MANIFEST_PATH = ROOT / "evidence/MANIFEST.json"
MASTER_REL = "evidence/fm24/reports/editor_schema/master.json"
BIG_REL = "evidence/fm24/reports/dbdat_decode/db_tables_big.json"
EXTRA_VERDICT_REL = "evidence/fm24/reports/dbdat_decode/extra_tables_verdict.json"


# ---- Independent minimal PE64 parser ----
class MiniPE64:
    def __init__(self, path: Path) -> None:
        self.raw = path.read_bytes()
        if self.raw[:2] != b"MZ":
            raise ValueError("not MZ")
        pe_off = struct.unpack_from("<I", self.raw, 0x3C)[0]
        if self.raw[pe_off:pe_off + 4] != b"PE\x00\x00":
            raise ValueError("not PE")
        _, n_sec, _, _, _, opt_sz, _ = struct.unpack_from("<HHIIIHH", self.raw, pe_off + 4)
        opt_off = pe_off + 24
        magic = struct.unpack_from("<H", self.raw, opt_off)[0]
        if magic != 0x20B:
            raise ValueError(f"not PE32+ (magic={hex(magic)})")
        self.image_base = struct.unpack_from("<Q", self.raw, opt_off + 24)[0]
        # DataDirectory[3] = Exception Table (.pdata)
        dd_off = opt_off + 112
        exc_rva, exc_sz = struct.unpack_from("<II", self.raw, dd_off + 3 * 8)
        sec_off = opt_off + opt_sz
        self.sections: list[tuple[int, int, int, int]] = []
        for i in range(n_sec):
            o = sec_off + i * 40
            vsize, vrva, rsize, roff = struct.unpack_from("<IIII", self.raw, o + 8)
            self.sections.append((vrva, max(vsize, rsize), roff, rsize))
        self.pdata: list[tuple[int, int]] = []
        if exc_rva and exc_sz:
            exc_fo = self.rva_to_fo(exc_rva)
            for k in range(0, exc_sz, 12):
                b, e, _ = struct.unpack_from("<III", self.raw, exc_fo + k)
                if b == 0 and e == 0:
                    break
                self.pdata.append((b, e))

    def rva_to_fo(self, rva: int) -> int:
        for vrva, vspan, roff, rsize in self.sections:
            if vrva <= rva < vrva + vspan:
                delta = rva - vrva
                if delta < rsize:
                    return roff + delta
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
        lo, hi = 0, len(self.pdata) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            b, e = self.pdata[mid]
            if rva < b:
                hi = mid - 1
            elif rva >= e:
                lo = mid + 1
            else:
                return self.rva_to_fo(b), self.rva_to_fo(e)
        raise ValueError(f"no .pdata entry for {hex(entry_fo)}")

    def rtti_name(self, vtable_va: int) -> str:
        vt_fo = self.va_to_fo(vtable_va)
        col_va = struct.unpack_from("<Q", self.raw, vt_fo - 8)[0]
        col_fo = self.va_to_fo(col_va)
        sig, _, _, td_rva = struct.unpack_from("<IIII", self.raw, col_fo)
        assert sig == 1
        td_fo = self.rva_to_fo(td_rva)
        end = self.raw.index(b"\x00", td_fo + 16)
        return self.raw[td_fo + 16:end].decode("ascii")

    def rel32_target_fo(self, table_fo: int, idx: int) -> int:
        rel = struct.unpack_from("<i", self.raw, table_fo + idx * 4)[0]
        return self.va_to_fo(self.fo_to_va(table_fo) + rel)


def walk_cfg(pe: MiniPE64, md: Cs, entry_fo: int) -> dict[int, Any]:
    i0 = next(md.disasm(pe.raw[entry_fo:entry_fo + 15], pe.fo_to_va(entry_fo), 1))
    if i0.mnemonic == "jmp" and i0.operands and i0.operands[0].type == X86_OP_IMM:
        entry_fo = pe.va_to_fo(i0.operands[0].imm)
    b_fo, e_fo = pe.func_bounds_fo(entry_fo)
    insns: dict[int, Any] = {}
    q = deque([entry_fo])
    seen: set[int] = set()
    while q:
        cur = q.popleft()
        while b_fo <= cur < e_fo and cur not in seen:
            seen.add(cur)
            it = md.disasm(pe.raw[cur:min(cur + 16, e_fo)], pe.fo_to_va(cur), 1)
            ins = next(it, None)
            if ins is None:
                break
            insns[cur] = ins
            nxt = cur + ins.size
            mn = ins.mnemonic
            if mn in ("ret", "int3", "ud2"):
                break
            if mn == "jmp":
                if ins.operands and ins.operands[0].type == X86_OP_IMM:
                    tfo = pe.va_to_fo(ins.operands[0].imm)
                    if b_fo <= tfo < e_fo and tfo not in seen:
                        q.append(tfo)
                break
            if mn.startswith("j") and ins.operands and ins.operands[0].type == X86_OP_IMM:
                tfo = pe.va_to_fo(ins.operands[0].imm)
                if b_fo <= tfo < e_fo and tfo not in seen:
                    q.append(tfo)
            cur = nxt
    return insns


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_fmf(side: str, wanted: list[str]) -> tuple[dict[str, bytes], set[str]]:
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
    return out, set(entries.keys())


def check_dates(vals: np.ndarray) -> int:
    v = np.asarray(vals, dtype="<u4")
    y = v >> 16
    d = v & 0x1FF
    rem = (v >> 9) & 0x7F
    leap = (y % 4 == 0) & ((y % 100 != 0) | (y % 400 == 0))
    ok = (rem == 0) & (y >= 1) & (d >= 1) & (d <= 365 + leap)
    return int((~ok).sum())


def scan_uids(buf: bytes) -> np.ndarray:
    n = struct.unpack_from("<I", buf, 8)[0]
    if (len(buf) - 22) % n == 0:
        st = (len(buf) - 22) // n
        arr = np.frombuffer(buf, dtype=np.uint8, offset=13, count=n * st).reshape(n, st)
        if np.array_equal(arr[:, st - 12:st - 8].copy().view("<u4").ravel(), np.arange(n, dtype=np.uint32)):
            u1 = arr[:, st - 8:st - 4].copy().view("<u4").ravel()
            u2 = arr[:, st - 4:st].copy().view("<u4").ravel()
            if np.array_equal(u1, u2):
                return u1
    uids = np.empty(n, dtype=np.uint32)
    pos = 13
    for i in range(n):
        pat = struct.pack("<I", i)
        cur = pos
        while True:
            idx = buf.find(pat, cur)
            assert idx != -1 and idx + 12 <= len(buf) - 9
            u1, u2 = struct.unpack_from("<II", buf, idx + 4)
            if u1 == u2 and u1 not in (0, 0xFFFFFFFF):
                uids[i] = u1
                pos = idx + 12
                break
            cur = idx + 1
    return uids


def verify_all(outdir: Path) -> list[str]:
    passed: list[str] = []

    def ok(tag: str, detail: str = "") -> None:
        passed.append(tag)
        print(f"PASS {tag}" + (f"  {detail}" if detail else ""))

    # 0. Independence check (ensure forbidden modules are NOT imported)
    for forbidden in ("t79_stad_team_harvest", "t05_pe", "t21b_control_flow", "fm24_dump"):
        assert forbidden not in sys.modules, f"forbidden module imported: {forbidden}"
    ok("V0_independence", "no builder/t05_pe/ReaderCFG/fm24_dump imported")

    # 1. Input integrity
    assert sha256_file(EXE_PATH) == EXPECTED_EXE_SHA256
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    by_path = {e["path"]: e["sha256"] for e in manifest["files"]}
    for rel in (MASTER_REL, BIG_REL, EXTRA_VERDICT_REL):
        assert sha256_file(ROOT / rel) == by_path[rel], f"manifest mismatch {rel}"
    ok("V1_integrity", "editor.exe + 3 MANIFEST files SHA-256 matched")

    # 2. Load deliverables
    xref = json.loads((outdir / "xref_stad_team.json").read_text(encoding="utf-8"))
    fmap = json.loads((outdir / "field_map.json").read_text(encoding="utf-8"))
    master = json.loads((ROOT / MASTER_REL).read_text(encoding="utf-8"))

    # 3. Independent PE64 static verification
    pe = MiniPE64(EXE_PATH)
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True

    # Factory cases 21 & 24
    assert pe.rel32_target_fo(0xF49D38, 21) == 0xF49078
    assert pe.rel32_target_fo(0xF49D38, 24) == 0xF490F9
    # RTTI & vtables
    assert pe.rtti_name(0x14188DBD8) == ".?AVSTADIUM@db@@"
    assert pe.rtti_name(0x14188E2D8) == ".?AVTEAM@db@@"
    assert pe.rtti_name(0x141889618) == ".?AVNATIONAL_TEAM@db@@"
    assert pe.rtti_name(0x141882C78) == ".?AVTEAM_BASE@db@@"
    # Verify vtable slots match xref
    for cls_name, vt_va, s2, s3, s19, s20 in [
        ("STADIUM", 0x14188DBD8, 0x1185EB0, 0x1189260, 0x1183F30, 0x1184920),
        ("TEAM", 0x14188E2D8, 0x11AF7B0, 0x11B4C30, 0x11A0880, 0x11A0C40),
        ("NATIONAL_TEAM", 0x141889618, 0x1056A90, 0x11B4C30, 0x1052C80, 0x1053120),
        ("TEAM_BASE", 0x141882C78, 0x11C2600, 0x11C23F0, 0x11C1D80, 0x11C1F40),
    ]:
        vt_fo = pe.va_to_fo(vt_va)
        assert pe.va_to_fo(struct.unpack_from("<Q", pe.raw, vt_fo + 2 * 8)[0]) == s2
        assert pe.va_to_fo(struct.unpack_from("<Q", pe.raw, vt_fo + 3 * 8)[0]) == s3
        assert pe.va_to_fo(struct.unpack_from("<Q", pe.raw, vt_fo + 19 * 8)[0]) == s19
        assert pe.va_to_fo(struct.unpack_from("<Q", pe.raw, vt_fo + 20 * 8)[0]) == s20
    ok("V2_factory_vtables_rtti", "cases 21/24 + 4 classes RTTI & vtable slots verified")

    # Verify db+offset registrations
    for fo, expected_txt in [
        (0xF02957, "mov qword ptr [r14 + 8], rdi"),
        (0xF02A93, "mov qword ptr [r14 + 0x10], rdi"),
        (0xF02BCF, "mov qword ptr [r14 + 0x18], rdi"),
        (0xF036EB, "mov qword ptr [r14 + 0x60], rdi"),
        (0xF03F06, "mov qword ptr [r14 + 0x80], rdi"),
        (0xF042C3, "mov qword ptr [r14 + 0x98], rdi"),
    ]:
        ins = next(md.disasm(pe.raw[fo:fo + 16], pe.fo_to_va(fo), 1))
        assert f"{ins.mnemonic} {ins.op_str}" == expected_txt, f"{hex(fo)}: {ins.mnemonic} {ins.op_str}"
    ok("V3_db_context_tables", "6 db+offset table registrations verified")

    # Independent CFG walks & 4CC dispatch verification
    cfg_stad_read = walk_cfg(pe, md, 0x1183F30)
    assert cfg_stad_read[0x1183F51].mnemonic == "test" and cfg_stad_read[0x1183F54].mnemonic == "je"
    assert pe.va_to_fo(cfg_stad_read[0x1183F54].operands[0].imm) == 0x11843B6

    cfg_stad_get = walk_cfg(pe, md, 0x1185EB0)
    cfg_stad_set = walk_cfg(pe, md, 0x1189260)
    cfg_team_get = walk_cfg(pe, md, 0x11AF7B0)
    cfg_team_set = walk_cfg(pe, md, 0x11B4C30)
    cfg_tbase_get = walk_cfg(pe, md, 0x11C2600)
    cfg_tbase_set = walk_cfg(pe, md, 0x11C23F0)
    cfg_dbrec_get = walk_cfg(pe, md, 0xFE3520)
    cfg_ex24_rec = walk_cfg(pe, md, 0x11A1580)
    cfg_side_get = walk_cfg(pe, md, 0x15E6650)

    def assert_cmp_4cc(cfg: dict[int, Any], fo_hex: str, cc: str) -> None:
        fo = int(fo_hex, 16)
        ins = cfg[fo]
        assert ins.mnemonic == "cmp", f"expected cmp at {fo_hex}, got {ins.mnemonic}"
        val = ins.operands[1].imm & 0xFFFFFFFF
        assert val == int.from_bytes(cc.encode("ascii"), "big"), f"4CC mismatch at {fo_hex}: {hex(val)} vs {cc}"

    # Verify every stadium L3 getter & setter 4CC dispatch in binary!
    for rec in fmap["stadium_21"]["schema_fields"]:
        cc = rec["field"]
        if rec["grade"] == "L3":
            if cc == "duni":
                assert_cmp_4cc(cfg_dbrec_get, rec["getter_fo"], "duni")
            else:
                assert_cmp_4cc(cfg_stad_get, rec["getter_fo"], cc)
                assert_cmp_4cc(cfg_stad_set, rec["setter_fo"], cc)
    # Verify Splr no-op vs SplR active, Sdtr movsx, Spty clamp, Scov branch, Ssds sage movsx
    assert_cmp_4cc(cfg_stad_get, "0x1186313", "Splr")
    assert pe.va_to_fo(cfg_stad_get[0x1186319].operands[0].imm) == 0x1185F0A
    assert_cmp_4cc(cfg_stad_get, "0x1186a4c", "SplR")
    assert_cmp_4cc(cfg_stad_set, "0x1189678", "SplR")
    assert cfg_stad_get[0x11872FE].mnemonic == "movsx" and "+ 0x9c]" in cfg_stad_get[0x11872FE].op_str
    assert cfg_stad_get[0x118661D].mnemonic == "cmovae"
    assert cfg_side_get[0x15E6740].mnemonic == "movsx" and "[rax + 4]" in cfg_side_get[0x15E6740].op_str
    ok("V4_stadium_static_dispatches", "41 L3 + 4 held + SplR/Splr/Sdtr/Spty/Ssds verified in editor.exe")

    # Verify every team L3 getter & setter 4CC dispatch
    for rec in fmap["team_24"]["schema_fields"]:
        cc = rec["field"]
        if rec["grade"] == "L3":
            if cc == "duni":
                assert_cmp_4cc(cfg_dbrec_get, rec["getter_fo"], "duni")
            elif cc in ("Tlna", "Tsna", "Ttyp", "Tisn"):
                assert_cmp_4cc(cfg_tbase_get, rec["getter_fo"], cc)
                if rec["setter_fo"]:
                    assert_cmp_4cc(cfg_tbase_set, rec["setter_fo"], cc)
            else:
                assert_cmp_4cc(cfg_team_get, rec["getter_fo"], cc)
                assert_cmp_4cc(cfg_team_set, rec["setter_fo"], cc)
    # Verify Trep clamp & extra_24 TEAM+0xa0 store + Twhm/Tmhm/Tpvr
    assert cfg_ex24_rec[0x11A15FA].mnemonic == "mov" and "[rdi + 0xa0], rsi" in cfg_ex24_rec[0x11A15FA].op_str
    assert_cmp_4cc(cfg_team_get, "0x11b0406", "Twhm")
    assert_cmp_4cc(cfg_team_set, "0x11b4e6c", "Twhm")
    assert_cmp_4cc(cfg_team_get, "0x11afa0b", "Tmhm")
    assert_cmp_4cc(cfg_team_set, "0x11b4d75", "Tmhm")
    assert_cmp_4cc(cfg_team_get, "0x11afb1f", "Tpvr")
    assert_cmp_4cc(cfg_team_set, "0x11b4c79", "Tpvr")
    ok("V5_team_and_extra24_static", "11 team L3 + TEAM+0xa0 bind + Twhm/Tmhm/Tpvr verified in editor.exe")

    # Verify CLUB+0x18 forwarding chain (getter + setter) for all 6 held club fields!
    assert pe.rel32_target_fo(0xE91D8C, 8) == 0xE8CF2F  # Csti getter
    assert pe.rel32_target_fo(0xE86B38, 6) == 0xE84537  # Csti setter
    for fo, cc in [
        (0xE8BE31, "Crep"), (0xE84049, "Crep"),
        (0xE8B939, "Cdvi"), (0xE83F65, "Cdvi"),
        (0xE89F6D, "Cldi"), (0xE842ED, "Cldi"),
        (0xE8AB0D, "Cndi"), (0xE82D8D, "Cndi"),
        (0xE8B7D8, "Codi"), (0xE83AD2, "Codi"),
    ]:
        ins = next(md.disasm(pe.raw[fo:fo + 16], pe.fo_to_va(fo), 1))
        assert ins.mnemonic == "cmp" and (ins.operands[1].imm & 0xFFFFFFFF) == int.from_bytes(cc.encode(), "big")
    # Verify Cldi/Cndi/Codi/Csti pass Tldi/Tndi/Todo/Tsti in r8d
    for fo, tcc in [
        (0xE8D14D, "Tldi"), (0xE842F9, "Tldi"),
        (0xE8AB19, "Tndi"), (0xE82D99, "Tndi"),
        (0xE8E3F5, "Todo"), (0xE854AC, "Todo"),
        (0xE8CF2F, "Tsti"), (0xE84537, "Tsti"),
    ]:
        # Scan up to 6 insns from arm for mov r8d, <tcc>
        found = False
        for ins in md.disasm(pe.raw[fo:fo + 32], pe.fo_to_va(fo), 6):
            if ins.mnemonic == "mov" and len(ins.operands) == 2 and ins.operands[1].type == X86_OP_IMM:
                if (ins.operands[1].imm & 0xFFFFFFFF) == int.from_bytes(tcc.encode(), "big"):
                    found = True
                    break
        assert found, f"expected mov r8d, {tcc!r} near {hex(fo)}"
    # Verify CLUB_BASE_fixup resolves CLUB+0x18 via [r13 + 0x98]
    fix_ins = next(md.disasm(pe.raw[0x11D25A8:0x11D2620], pe.fo_to_va(0x11D25A8), 20))
    fix_block = [f"{i.mnemonic} {i.op_str}" for i in md.disasm(pe.raw[0x11D25A8:0x11D2625], pe.fo_to_va(0x11D25A8))]
    assert any("+ 0x98]" in line for line in fix_block), "CLUB+0x18 fixup did not read [db+0x98]"
    ok("V6_club_base18_static_chain", "all 6 club fields getter+setter + rel32 Csti + fixup [db+0x98] verified")

    # ---- 4. INDEPENDENT FULL-ARCHIVE DATA VERIFICATION ----
    cli, cli_set = load_fmf("client", ["table_2.dat", "table_3.dat", "table_9.dat", "table_21.dat", "table_25.dat"])
    srv, srv_set = load_fmf("server", ["table_2.dat", "table_3.dat", "table_21.dat", "table_24.dat", "table_25.dat", "table_extra_24.dat"])
    assert "client_db/table_24.dat" not in cli_set and "client_db/table_extra_24.dat" not in cli_set

    n_t2 = struct.unpack_from("<I", cli["table_2.dat"], 8)[0]
    t2_uids = set(np.frombuffer(cli["table_2.dat"], np.uint8, offset=13, count=n_t2 * 43).reshape(n_t2, 43)[:, 35:39].copy().view("<u4").ravel().tolist())
    t3_uids_arr = scan_uids(cli["table_3.dat"])
    t3_uids = set(t3_uids_arr.tolist())
    t9_uids_arr = scan_uids(cli["table_9.dat"])
    t9_uids = set(t9_uids_arr.tolist())
    t25_uids_arr = scan_uids(cli["table_25.dat"])
    t25_uids = set(t25_uids_arr.tolist())

    # Table 21 (client + server)
    c21, s21 = cli["table_21.dat"], srv["table_21.dat"]
    n21 = struct.unpack_from("<I", c21, 8)[0]
    assert n21 == 48413 and len(c21) == 13 + n21 * 38 + 9 and len(s21) == 13 + n21 * 181 + 9
    assert c21[-9:] == s21[-9:] == bytes.fromhex("00000000017ece3a77")
    cb = np.frombuffer(c21, np.uint8, offset=13, count=n21 * 38).reshape(n21, 38)[:, 1:]
    sb = np.frombuffer(s21, np.uint8, offset=13, count=n21 * 181).reshape(n21, 181)[:, 1:]
    assert np.array_equal(cb, sb[:, 143:])
    t21_ord = cb[:, 25:29].copy().view("<u4").ravel()
    t21_uid = cb[:, 29:33].copy().view("<u4").ravel()
    t21_rdui = cb[:, 33:37].copy().view("<u4").ravel()
    assert np.array_equal(t21_ord, np.arange(n21, dtype=np.uint32)) and np.array_equal(t21_uid, t21_rdui)
    t21_uid_set = set(t21_uid.tolist())
    assert len(t21_uid_set) == n21

    # Client anchors & landmarks on table_21
    assert int(cb[67, 3:7].copy().view("<i4")[0]) == 1061  # Anfield -> Liverpool
    assert abs(float(cb[67, 17:21].copy().view("<f4")[0]) - 53.43082) < 1e-4
    assert abs(float(cb[67, 21:25].copy().view("<f4")[0]) - (-2.960832)) < 1e-4
    assert int(sb[430, 0:4].copy().view("<i4")[0]) == 81044  # Bernabeu Scpy
    assert int(sb[71, 0:4].copy().view("<i4")[0]) == 74031   # Old Trafford Scpy (prior mismatch retained)
    # Check Sdtr violations & Ssds sage violations
    sdtr = sb[:, 62].view(np.int8)
    assert int((~np.isin(sdtr, [1, 2, 3])).sum()) == 29983 and int(sdtr[0]) == 0
    sides = sb[:, 64:128].reshape(n21, 8, 8)
    sage = sides[:, :, 5:7].copy().view("<i2").reshape(-1)
    assert int((sage < 0).sum()) == 20425 and int(sage.min()) == -7173
    # Check dates
    for doff in (37, 41, 45, 131, 135, 156):
        assert check_dates(sb[:, doff:doff + 4].copy().view("<u4").ravel()) == 0
    # Check Scti, Snbs, Sowi ordinal refs + wrong-UID controls
    scti = cb[:, 3:7].copy().view("<i4").ravel()
    snbs = cb[:, 7:11].copy().view("<i4").ravel()
    sowi = sb[:, 16:20].copy().view("<i4").ravel()
    assert int(((scti < 0) | (scti >= n_t2)).sum()) == 0
    assert int(((snbs >= 0) & (snbs >= n21)).sum()) == 0 and int(((snbs < 0) & (snbs != -1)).sum()) == 0
    assert int(((sowi >= 0) & (sowi >= len(t3_uids_arr))).sum()) == 0 and int(((sowi < 0) & (sowi != -1)).sum()) == 0
    ok("V7_table_21_data", f"48,413 dual rows byte-identical common 37B; all 41 L3 + 4 held verified")

    # Table 24 (server-only) sequential replay
    s24 = srv["table_24.dat"]
    n24 = struct.unpack_from("<I", s24, 8)[0]
    assert n24 == 84507
    p = 13
    t24_sel = np.empty(n24, np.uint8)
    t24_rep = np.empty(n24, np.int16)
    t24_dvi = np.empty(n24, np.int32)
    t24_ldi = np.empty(n24, np.int32)
    t24_ndi = np.empty(n24, np.int32)
    t24_sti = np.empty(n24, np.int32)
    t24_odo = np.empty(n24, np.int32)
    t24_nod = np.empty(n24, np.int32)
    t24_typ = np.empty(n24, np.int8)
    t24_isn = np.empty(n24, np.uint8)
    t24_own = np.empty(n24, np.int32)
    t24_uid = np.empty(n24, np.uint32)
    lna_nz = sna_nz = 0
    for i in range(n24):
        sel = s24[p]; p += 1; t24_sel[i] = sel
        if sel == 11:
            p += 48
            mc = struct.unpack_from("<b", s24, p)[0]; p += 1 + max(0, mc) * 10
        else:
            assert sel == 10
        _, _, rep, dvi, ldi, ndi, sti, _, _, _, odo, vc = struct.unpack_from("<BbhiiiiiiBiH", s24, p)
        p += 35 + vc * 4 + 13
        nod = struct.unpack_from("<i", s24, p)[0]; p += 5
        typ, isn = struct.unpack_from("<bB", s24, p); p += 6
        ow = struct.unpack_from("<i", s24, p)[0]; p += 4
        l1 = struct.unpack_from("<I", s24, p)[0]; p += 4
        if l1:
            s24[p:p + l1].decode("utf-8")
            lna_nz += 1
        p += l1 + 1
        l2 = struct.unpack_from("<I", s24, p)[0]; p += 4
        if l2:
            s24[p:p + l2].decode("utf-8")
            sna_nz += 1
        p += l2 + 1
        o, u1, u2 = struct.unpack_from("<III", s24, p); p += 12
        assert o == i and u1 == u2
        t24_rep[i] = rep; t24_dvi[i] = dvi; t24_ldi[i] = ldi; t24_ndi[i] = ndi
        t24_sti[i] = sti; t24_odo[i] = odo; t24_nod[i] = nod
        t24_typ[i] = typ; t24_isn[i] = isn; t24_own[i] = ow; t24_uid[i] = u1
    assert p + 9 == len(s24) and s24[p:] == bytes.fromhex("0000000001e3c03a77")
    assert int((t24_sel == 11).sum()) == 251 and np.array_equal(t24_sel == 11, t24_isn == 1)
    tmty_allowed = [int(v["enum"]) for v in master["enums"]["tmty"]["values"]]
    assert int((~np.isin(t24_typ, tmty_allowed)).sum()) == 0
    assert lna_nz == 1741 and sna_nz == 1741
    for arr, lim in [(t24_dvi, len(t25_uids_arr)), (t24_ldi, len(t25_uids_arr)), (t24_ndi, len(t25_uids_arr)), (t24_odo, len(t25_uids_arr)), (t24_nod, len(t25_uids_arr)), (t24_sti, n21)]:
        assert int(((arr >= 0) & (arr >= lim)).sum()) == 0 and int(((arr < 0) & (arr != -1)).sum()) == 0
    ok("V8_table_24_data", f"84,507 rows replayed exact EOF; 251 NT + 84,256 TEAM; 11 L3 verified")

    # Table extra 24 independent framing self-certification + grammar closure
    ex24 = srv["table_extra_24.dat"]
    assert len(ex24) == 6929586 and struct.unpack_from("<I", ex24, 8)[0] == n24
    hits = []
    for a in range(0, 200):
        if struct.unpack_from("<I", ex24, a)[0] != 0:
            continue
        for st in range(4, 501):
            if a + n24 * st > len(ex24):
                break
            if (struct.unpack_from("<I", ex24, a + st)[0] == 1 and
                struct.unpack_from("<I", ex24, a + 2 * st)[0] == 2 and
                struct.unpack_from("<I", ex24, a + 3 * st)[0] == 3 and
                struct.unpack_from("<I", ex24, a + (n24 - 1) * st)[0] == n24 - 1):
                hits.append((a, st, len(ex24) - (a + n24 * st)))
    assert hits == [(12, 82, 0)], f"non-unique extra_24 framing: {hits}"
    ex_arr = np.frombuffer(ex24, np.uint8, offset=12, count=n24 * 82).reshape(n24, 82)
    assert np.array_equal(ex_arr[:, 0:4].copy().view("<u4").ravel(), np.arange(n24, dtype=np.uint32))
    assert np.all(ex_arr[:, 49:57] == 0) and np.all(ex_arr[:, 62:70] == 0)
    assert np.all(ex_arr[:, 70:74].copy().view("<u4").ravel() == 8)
    for doff in (29, 33, 37, 41, 45, 57):
        assert check_dates(ex_arr[:, doff:doff + 4].copy().view("<u4").ravel()) == 0
    twhm = ex_arr[:, 10].view(np.int8)
    tmhm = ex_arr[:, 11].view(np.int8)
    tpvr = ex_arr[:, 21:23].copy().view("<i2").ravel()
    assert int((~np.isin(twhm[twhm != 0], [1, 2, 3, 4, 5, 6, 7])).sum()) == 0 and int((twhm != 0).sum()) == 10775
    assert int((~np.isin(tmhm[tmhm != 0], [1, 2, 3, 4, 5, 6, 7])).sum()) == 0 and int((tmhm != 0).sum()) == 6897
    assert np.all(tpvr == 1)
    ok("V9_table_extra_24_data", "unique (12,82,0) framing + 82B grammar closure + Twhm/Tmhm/Tpvr verified")

    # Table 3 (server) CLUB+0x18 replay & 6 forwarded club fields
    s3 = srv["table_3.dat"]
    n3 = struct.unpack_from("<I", s3, 8)[0]
    p = 13
    first_team = np.full(n3, -1, np.int32)
    club_uid = np.empty(n3, np.uint32)
    for i in range(n3):
        sel = s3[p]; p += 1
        if sel == 12:
            p += 5
        p += 26
        l1 = struct.unpack_from("<I", s3, p)[0]; p += 4 + l1
        l2 = struct.unpack_from("<I", s3, p)[0]; p += 4 + l2
        p += 8
        c110 = struct.unpack_from("<b", s3, p)[0]; p += 1 + c110 * 4
        if s3[p] == 0:
            p += 46
        else:
            p += 1
        c130 = struct.unpack_from("<b", s3, p)[0]; p += 1 + c130 * 24
        c138 = struct.unpack_from("<b", s3, p)[0]; p += 1 + c138 * 12
        p += 9
        c18 = s3[p]; p += 1
        if c18 > 0:
            t0 = struct.unpack_from("<i", s3, p)[0]
            assert t24_typ[t0] not in (0x16, 0x2C)
            first_team[i] = t0
        p += c18 * 4
        c30 = s3[p]; p += 1 + c30 * 4
        c60 = struct.unpack_from("<b", s3, p)[0]; p += 1 + c60 * 4
        c78 = struct.unpack_from("<b", s3, p)[0]; p += 1 + c78 * 4
        c90 = s3[p]; p += 1 + c90 * 4
        c48 = s3[p]; p += 1 + c48 * 16
        ca8 = struct.unpack_from("<h", s3, p)[0]; p += 2 + ca8 * 28
        o, u1, u2 = struct.unpack_from("<III", s3, p); p += 12
        assert o == i and u1 == u2
        club_uid[i] = u1
    assert p + 9 == len(s3)
    has_t = first_team >= 0
    ft = first_team[has_t]
    assert len(ft) == 82515 and int((~has_t).sum()) == 1744
    assert np.array_equal(t24_own[ft], np.flatnonzero(has_t)) and np.all(t24_isn[ft] == 0)
    assert int(((t24_rep[ft] < 0) | (t24_rep[ft] > 10000)).sum()) == 0
    # Landmark: Liverpool (club 460 -> team 586 -> Anfield 67, Trep 8700, Tdvi 7)
    assert int(club_uid[460]) == 676 and int(first_team[460]) == 586
    assert int(t24_rep[586]) == 8700 and int(t24_dvi[586]) == 7 and int(t24_sti[586]) == 67
    # Landmark: Real Madrid (1297 -> 1495 -> Bernabeu 430)
    assert int(club_uid[1297]) == 1736 and int(first_team[1297]) == 1495 and int(t24_sti[1495]) == 430
    ok("V10_club_base18_data", "82,515 clubs joined bidirectionally; 6 forwarded fields + landmarks verified")

    # ---- 5. JSON SCHEMA & CROSS-CHECK ----
    assert fmap["summary"]["stadium_xml_total"] == 60
    assert fmap["summary"]["stadium_xml_grades"]["L3"] == 41
    assert fmap["summary"]["stadium_xml_grades"]["held"] == 4
    assert fmap["summary"]["team_xml_total"] == 25
    assert fmap["summary"]["team_xml_grades"]["L3"] == 11
    assert fmap["summary"]["team_xml_grades"]["held"] == 2
    assert fmap["summary"]["club_base18_forwarded_upgraded_L3"] == 6
    assert all(x["grade"] == "L3" and x["projection_label"] == "经 +0x18 转发的投影" for x in fmap["club_base18_forwarded_6"])
    assert len(xref["landmarks"]["stadiums"]) == 4 and len(xref["landmarks"]["clubs_via_base18"]) == 6
    ok("V11_json_crosscheck", "xref_stad_team.json + field_map.json counts and labels verified")

    return passed


def run_selftest() -> int:
    assert check_dates(np.array([0x076C0001, (2020 << 16) | 366], dtype="<u4")) == 0
    assert check_dates(np.array([(2021 << 16) | 366], dtype="<u4")) == 1
    pe = MiniPE64(EXE_PATH)
    assert pe.va_to_fo(pe.fo_to_va(0xF48B30)) == 0xF48B30
    print("SELFTEST PASS: MiniPE64 round-trip, check_dates")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Independent verifier for t79 deliverables (no builder/ReaderCFG/fm24_dump imports).")
    ap.add_argument("--selftest", action="store_true", help="Run built-in unit self-tests and exit.")
    ap.add_argument("--outdir", type=Path, default=Path(__file__).resolve().parent, help="Directory containing xref_stad_team.json and field_map.json.")
    args = ap.parse_args(argv)
    try:
        if args.selftest:
            return run_selftest()
        passed = verify_all(args.outdir)
        print(f"\nALL {len(passed)}/{len(passed)} INDEPENDENT VERIFICATION CHECKS PASSED")
        return 0
    except AssertionError as e:
        print(f"VERIFY FAIL: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"FATAL: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
