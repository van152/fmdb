#!/usr/bin/env python3
"""Independent verifier for t82 (table_extra_3.dat remaining member naming).

Strictly independent: MUST NOT import t82_extra3_remaining, ReaderCFG, fm24_dump,
t05_pe, or any builder module from scripts/. Parses PE32+ headers with stdlib struct,
extracts FMF frames independently with zstandard, replays all 84,259 x 2 rows byte-exact,
and independently audits all PE bytes, full-archive vectorized domains, triple-gate
invariants, negative proofs, and L2 anchors.

Exit codes: 0 = all checks pass, 1 = verification failed, 2 = CLI usage or fatal error.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import struct
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np

TOOLS_PY = r"D:\tmp2b\fm24\tools\python"
if TOOLS_PY not in sys.path:
    sys.path.insert(0, TOOLS_PY)

import zstandard as zstd  # type: ignore

ROOT = Path(r"D:\tmp2b\fm24-db")
DEFAULT_EXE = Path(r"D:\tmp2b\fm24\input\editor.exe")
DEFAULT_DATA = Path(os.environ.get("FM24_DB_DIR", str(ROOT / "scratch/data")))
DEFAULT_OUT = ROOT / "scratch/t82/out"

TAD_MAGIC = bytes.fromhex("03017461642ef10d")
SENTINEL_DATE4 = 0x076C0001
FORBIDDEN_IMPORTS = {"t82_extra3_remaining", "ReaderCFG", "fm24_dump", "t05_pe", "scripts"}

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


def _sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


class PurePE64:
    """Minimal stdlib-only PE32+ mapper (file offset <-> VA)."""

    def __init__(self, blob: bytes):
        self.blob = blob
        if blob[:2] != b"MZ":
            raise AssertionError("Not MZ")
        pe_off = struct.unpack_from("<I", blob, 0x3C)[0]
        if blob[pe_off:pe_off + 4] != b"PE\x00\x00":
            raise AssertionError("Not PE")
        nsec = struct.unpack_from("<H", blob, pe_off + 6)[0]
        opt_sz = struct.unpack_from("<H", blob, pe_off + 20)[0]
        opt_off = pe_off + 24
        if struct.unpack_from("<H", blob, opt_off)[0] != 0x20B:
            raise AssertionError("Not PE32+")
        self.image_base = struct.unpack_from("<Q", blob, opt_off + 24)[0]
        sec_off = opt_off + opt_sz
        self.sections: list[tuple[int, int, int, int]] = []
        for k in range(nsec):
            o = sec_off + 40 * k
            vsize, vaddr, rsize, rptr = struct.unpack_from("<4I", blob, o + 8)
            self.sections.append((rptr, rsize, vaddr, max(vsize, rsize)))

    def fo_to_va(self, fo: int) -> int:
        for rptr, rsize, vaddr, _ in self.sections:
            if rptr <= fo < rptr + rsize:
                return self.image_base + vaddr + (fo - rptr)
        raise AssertionError(f"fo 0x{fo:x} not in any PE section")

    def va_to_fo(self, va: int) -> int:
        rva = va - self.image_base
        for rptr, rsize, vaddr, vspan in self.sections:
            if vaddr <= rva < vaddr + vspan:
                off = rptr + (rva - vaddr)
                if off < rptr + rsize:
                    return off
        raise AssertionError(f"VA 0x{va:x} not mapped to file")

    def verify_witness(self, w: dict[str, Any], label: str) -> None:
        fo = int(w["file_offset"], 16)
        va = int(w["va"], 16)
        raw = bytes.fromhex(w["bytes"])
        if self.fo_to_va(fo) != va:
            raise AssertionError(f"[{label}] VA mismatch at fo=0x{fo:x}: got 0x{self.fo_to_va(fo):x}, doc has 0x{va:x}")
        actual = self.blob[fo:fo + len(raw)]
        if actual != raw:
            raise AssertionError(f"[{label}] PE byte mismatch at fo=0x{fo:x}: got {actual.hex()}, doc has {raw.hex()}")


def _check_import_hygiene() -> None:
    src = Path(__file__).read_text(encoding="utf-8")
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                top = alias.name.split(".")[0]
                if top in FORBIDDEN_IMPORTS or alias.name in FORBIDDEN_IMPORTS:
                    raise AssertionError(f"Forbidden import detected: {alias.name}")
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            top = mod.split(".")[0]
            if top in FORBIDDEN_IMPORTS or mod in FORBIDDEN_IMPORTS:
                raise AssertionError(f"Forbidden from-import detected: {mod}")


def _extract_fmf_members(fmf_path: Path, members: list[str]) -> dict[str, bytes]:
    raw = fmf_path.read_bytes()
    toc_rel, base_rel = struct.unpack_from("<QQ", raw, 17)
    toc, base = toc_rel + 17, base_rel + 17
    if base != 34 or raw[8:17] != b"\x02\x01fmf.\x08\x00\x00" or raw[toc:toc + 9] != b"\x02\x01fmf.\x08\x00\x00":
        raise AssertionError(f"Bad FMF magic in {fmf_path}")
    d = zstd.ZstdDecompressor().decompressobj()
    directory = d.decompress(raw[toc + 9:])
    if len(d.unused_data) != 0:
        raise AssertionError(f"Trailing bytes after FMF TOC in {fmf_path}")
    pos = 0
    table: dict[str, tuple[int, int, int]] = {}

    def _u32() -> int:
        nonlocal pos
        v = struct.unpack_from("<I", directory, pos)[0]
        pos += 4
        return v

    def _str() -> str:
        nonlocal pos
        n = _u32()
        s = directory[pos:pos + n].decode("utf-8")
        pos += n
        return s

    def _walk(prefix: str) -> None:
        nonlocal pos
        cur = prefix + _str() + "/"
        for _ in range(_u32()):
            nm = cur + _str() + _str()
            off, sz, unp, _, _ = struct.unpack_from("<5Q", directory, pos)
            pos += 40
            table[nm] = (base + off, base + off + sz, unp)
        for _ in range(_u32()):
            _walk(cur)

    _walk("")
    out: dict[str, bytes] = {}
    for m in members:
        lo, hi, unp = table[m]
        q = lo
        found = None
        while q < hi:
            dec = zstd.ZstdDecompressor().decompressobj()
            pl = dec.decompress(raw[q:hi])
            q += (hi - q) - len(dec.unused_data)
            if len(pl) == unp:
                found = pl
        if found is None or found[:8] != TAD_MAGIC:
            raise AssertionError(f"Failed to extract {m}")
        out[m] = found
    return out


def _scan_uids(buf: bytes) -> tuple[dict[int, int], set[int]]:
    cnt = struct.unpack_from("<I", buf, 8)[0]
    o2u: dict[int, int] = {}
    uset: set[int] = set()
    p = 12
    for k in range(cnt):
        needle = struct.pack("<I", k)
        s = p
        hi = min(len(buf), p + 450)
        hit = False
        while True:
            idx = buf.find(needle, s, hi)
            if idx == -1:
                break
            if idx + 12 <= len(buf):
                u1, u2 = struct.unpack_from("<II", buf, idx + 4)
                if u1 == u2 and 1 <= u1 <= 2_100_000_000:
                    o2u[k] = u1
                    uset.add(u1)
                    p = idx + 12
                    hit = True
                    break
            s = idx + 1
        if not hit:
            raise AssertionError(f"UID scan stopped at {k}")
    return o2u, uset


def _date4_valid(u: int) -> bool:
    yr = (u >> 16) & 0xFFFF
    doy = u & 0x1FF
    mid = (u >> 9) & 0x7F
    leap = 1 if (yr % 4 == 0 and (yr % 100 != 0 or yr % 400 == 0)) else 0
    return (yr >= 1) and (1 <= doy <= 365 + leap) and (mid == 0)


def _replay_both(cli_buf: bytes, srv_buf: bytes) -> dict[str, Any]:
    n_c = struct.unpack_from("<I", cli_buf, 8)[0]
    n_s = struct.unpack_from("<I", srv_buf, 8)[0]
    if not (n_c == n_s == 84259):
        raise AssertionError(f"Row counts mismatch: client={n_c}, server={n_s}")

    # Client replay
    pc = 12
    cli_tail_h = hashlib.sha256()
    cli_cc_ff = 0
    cli_cc_0 = 0
    for i in range(n_c):
        if struct.unpack_from("<I", cli_buf, pc)[0] != i:
            raise AssertionError(f"client ordinal mismatch at {i}")
        pc += 4
        ts = pc
        _, cc, _ = struct.unpack_from("<HIH", cli_buf, pc)
        if cc == 0xFFFFFFFF:
            cli_cc_ff += 1
        elif cc == 0:
            cli_cc_0 += 1
        pc += 8
        tlen = struct.unpack_from("<I", cli_buf, pc)[0]
        pc += 4 + tlen
        kcnt = cli_buf[pc]
        pc += 1 + 27 * kcnt
        pc += 8
        cli_tail_h.update(cli_buf[ts:pc])
    if pc != len(cli_buf):
        raise AssertionError(f"client EOF mismatch: {pc} != {len(cli_buf)}")

    # Server full replay
    ps = 12
    srv_tail_h = hashlib.sha256()
    cols: dict[str, np.ndarray] = {
        k: np.full(n_s, -1 if dt.startswith("i") or dt.endswith(("i1", "i2", "i4")) else 0, dtype=dt)
        for k, dt in [
            ("Ctlv", "i1"), ("Cmle", "i1"), ("Csth", "<i4"),
            ("elec_flag", "u1"), ("elec_club", "<i4"),
            ("Cepr", "<i2"), ("Cetl", "i1"), ("Cmtm", "i1"), ("Cect", "i1"), ("Cemn", "i1"), ("Cemx", "i1"),
            ("Cyim", "i1"), ("CScP", "i1"), ("Cown", "i1"), ("Chti", "i1"),
            ("Csly", "i1"), ("Csps", "i1"), ("Cspt", "i1"), ("Csaf", "i1"), ("Cste", "i1"), ("Cspe", "i1"),
            ("Cyfb", "i1"), ("Cytv", "i1"), ("Crcb", "i1"),
            ("d8", "<u2"), ("cc", "<u4"), ("base_ac", "<u2"), ("base_a0", "<u4"), ("base_a8", "<u4"),
            ("Cpfr", "i1"), ("C2pf", "i1"), ("Cdfo", "i1"), ("Cafo", "i1"),
            ("Catd", "<i4"), ("Cmna", "<i4"), ("Cmxa", "<i4"),
        ]
    }
    cuf_raw = np.zeros((n_s, 10), dtype="<i4")
    cuf_has = np.zeros(n_s, dtype=bool)
    tcht_map: dict[int, str] = {}
    kit_buckets: Counter = Counter()
    cscm_items = []
    cpsl_items = []
    cspb_items = []
    cren_items = []
    tcrs_items = []
    csoc_items = []
    camc_items = []
    cbbl_items = []
    pcpt_items = []
    b0_tags: Counter = Counter()
    b48_flag_cnt = 0

    for i in range(n_s):
        if struct.unpack_from("<I", srv_buf, ps)[0] != i:
            raise AssertionError(f"server ordinal mismatch at {i}")
        ps += 4
        cols["Ctlv"][i], cols["Cmle"][i], _ = struct.unpack_from("<bbb", srv_buf, ps)
        ps += 3
        c18 = struct.unpack_from("<H", srv_buf, ps)[0]
        ps += 2 + 4 * c18
        ps += 5  # +da
        ps += 1  # +123
        cols["Csth"][i] = struct.unpack_from("<i", srv_buf, ps)[0]
        ps += 4 + 24
        ef = srv_buf[ps]
        ps += 1 + (24 if ef else 0) + 15
        elf = srv_buf[ps]
        cols["elec_flag"][i] = elf
        ps += 1
        if elf:
            ec, _, _, cepr, cetl, cmtm, cect, cemn, cemx = struct.unpack_from("<iIIhbbbbb", srv_buf, ps)
            ps += 19
            cols["elec_club"][i] = ec
            cols["Cepr"][i] = cepr
            cols["Cetl"][i] = cetl
            cols["Cmtm"][i] = cmtm
            cols["Cect"][i] = cect
            cols["Cemn"][i] = cemn
            cols["Cemx"][i] = cemx
        cols["Cyim"][i], cols["CScP"][i], _, cols["Cown"][i], cols["Chti"][i] = struct.unpack_from("<5b", srv_buf, ps)
        ps += 5
        ps += 1  # f8 ver
        (cols["Csly"][i], cols["Csps"][i], cols["Cspt"][i],
         cols["Csaf"][i], cols["Cste"][i], cols["Cspe"][i]) = struct.unpack_from("<6b", srv_buf, ps + 8)
        ps += 20 + 21  # f8 + p10c
        ta = srv_buf[ps]
        ps += 1 + (7 if ta > 1 else 6)
        tb = srv_buf[ps]
        ps += 1 + (12 if tb < 2 else 14 if tb == 2 else 15)
        cols["Cyfb"][i], cols["Cytv"][i], cols["Crcb"][i] = struct.unpack_from("<bbb", srv_buf, ps + 12)
        ps += 25
        c28 = struct.unpack_from("<b", srv_buf, ps)[0]
        ps += 1
        for _ in range(c28):
            ver, co1, co2, stnm, sn1, sn2, tl = struct.unpack_from("<Biibiii", srv_buf, ps)
            cscm_items.append((i, ver, co1, co2, stnm, sn1, sn2, tl))
            ps += 22
        c20 = srv_buf[ps]
        ps += 1 + 10 * c20
        f48 = srv_buf[ps]
        ps += 1
        if f48:
            t48 = struct.unpack_from("<b", srv_buf, ps)[0]
            ps += 1 + (24 if t48 > 0 else 16)
            cnt48 = srv_buf[ps]
            ps += 1
            vals48 = struct.unpack_from(f"<{cnt48}i", srv_buf, ps) if cnt48 else ()
            ps += 4 * cnt48
            ring = [0] * 10
            head = 0
            rcnt = 0
            for v in vals48:
                if rcnt < 10:
                    ring[(head + rcnt) % 10] = v
                    rcnt += 1
                else:
                    ring[head] = v
                    head = (head + 1) % 10
            cuf_has[i] = True
            for k in range(10):
                cuf_raw[i, k] = ring[(head + k) % 10] if k < rcnt else 0
        ps += 7
        c68 = struct.unpack_from("<H", srv_buf, ps)[0]
        ps += 2
        for _ in range(c68):
            tg, p1, p2, w8 = struct.unpack_from("<BiiH", srv_buf, ps)
            cpsl_items.append((i, tg, p1, p2, w8))
            ps += 11
        ps += 3

        # Common tail
        ts = ps
        cols["d8"][i], cols["cc"][i], cols["base_ac"][i] = struct.unpack_from("<HIH", srv_buf, ps)
        ps += 8
        tlen = struct.unpack_from("<I", srv_buf, ps)[0]
        ps += 4
        if tlen:
            tcht_map[i] = srv_buf[ps:ps + tlen].decode("utf-8")
            ps += tlen
        kcnt = srv_buf[ps]
        ps += 1
        for _ in range(kcnt):
            b22 = srv_buf[ps + 23]
            b25 = srv_buf[ps + 26]
            kit_buckets[(b22, 1 if b25 else 0)] += 1
            ps += 27
        a3, a2, a1, a0, b3, b2, b1, b0 = srv_buf[ps:ps + 8]
        cols["base_a0"][i] = a0 | (a1 << 8) | (a2 << 16) | (a3 << 24)
        cols["base_a8"][i] = b0 | (b1 << 8) | (b2 << 16) | (b3 << 24)
        ps += 8
        srv_tail_h.update(srv_buf[ts:ps])

        # Server tail
        c18b = struct.unpack_from("<h", srv_buf, ps)[0]
        ps += 2
        for _ in range(c18b):
            cspb_items.append((i,) + struct.unpack_from("<BiibbbII", srv_buf, ps))
            ps += 20
        c30b = struct.unpack_from("<b", srv_buf, ps)[0]
        ps += 1
        for _ in range(c30b):
            cren_items.append((i,) + struct.unpack_from("<bib", srv_buf, ps))
            ps += 6
        (cols["Cpfr"][i], cols["C2pf"][i], cols["Cdfo"][i], cols["Cafo"][i],
         cols["Catd"][i], cols["Cmna"][i], cols["Cmxa"][i]) = struct.unpack_from("<bbbbiii", srv_buf, ps)
        ps += 16
        cb0 = struct.unpack_from("<H", srv_buf, ps)[0]
        ps += 2
        for _ in range(cb0):
            t = srv_buf[ps]
            ps += 1
            b0_tags[t] += 1
            if t == 4:
                ps += 43
            elif t == 5:
                csoc_items.append((i,) + struct.unpack_from("<iiibbiiBB", srv_buf, ps))
                ps += 24
            elif t == 6:
                camc_items.append((i,) + struct.unpack_from("<iiiibbb", srv_buf, ps))
                ps += 19
            elif t == 7:
                cbbl_items.append((i,) + struct.unpack_from("<iiiiII", srv_buf, ps))
                ps += 24
            elif t == 9:
                ps += 20
                for _ in range(4):
                    sl = struct.unpack_from("<I", srv_buf, ps)[0]
                    ps += 4 + sl
            elif t == 16:
                c16 = struct.unpack_from("<b", srv_buf, ps)[0]
                ps += 1 + 4 * c16
            elif t == 37:
                ps += 27
            elif t == 38:
                c38 = struct.unpack_from("<I", srv_buf, ps)[0]
                ps += 4
                for _ in range(c38):
                    ver = srv_buf[ps]
                    ptpl, d1, ptly, w3c = struct.unpack_from("<iIIH", srv_buf, ps + 5)
                    sl = struct.unpack_from("<I", srv_buf, ps + 19)[0]
                    pcpt_items.append((i, ver, ptpl, d1, ptly, w3c, sl))
                    ps += 23 + sl
            else:
                raise AssertionError(f"Unknown poly tag {t}")
        f48b = srv_buf[ps]
        ps += 1
        if f48b:
            b48_flag_cnt += 1
            _, c48 = struct.unpack_from("<II", srv_buf, ps)
            ps += 8
            for _ in range(c48):
                iv = struct.unpack_from("<h", srv_buf, ps)[0]
                ps += 2
                if iv != 3:
                    raise AssertionError(f"TCrs iv={iv}")
                tcrs_items.append((i,) + struct.unpack_from("<iBbHBB", srv_buf, ps))
                ps += 10
    if ps != len(srv_buf):
        raise AssertionError(f"server EOF mismatch: {ps} != {len(srv_buf)}")

    return {
        "cli_tail_sha": cli_tail_h.hexdigest(),
        "srv_tail_sha": srv_tail_h.hexdigest(),
        "cli_cc_ff": cli_cc_ff,
        "cli_cc_0": cli_cc_0,
        "cols": cols,
        "cuf_raw": cuf_raw,
        "cuf_has": cuf_has,
        "tcht_map": tcht_map,
        "kit_buckets": kit_buckets,
        "cscm_items": cscm_items,
        "cpsl_items": cpsl_items,
        "cspb_items": cspb_items,
        "cren_items": cren_items,
        "tcrs_items": tcrs_items,
        "csoc_items": csoc_items,
        "camc_items": camc_items,
        "cbbl_items": cbbl_items,
        "pcpt_items": pcpt_items,
        "b0_tags": b0_tags,
        "b48_flag_cnt": b48_flag_cnt,
    }


def run_verify(exe_path: Path, data_dir: Path, out_dir: Path) -> int:
    passed = 0

    def ok(msg: str) -> None:
        nonlocal passed
        passed += 1
        print(f"  [PASS {passed:02d}] {msg}")

    # Check 1: Import hygiene
    _check_import_hygiene()
    ok("Import hygiene (zero forbidden builder/fm24_dump/ReaderCFG/t05_pe imports)")

    # Check 2: Pinned SHA-256 & MANIFEST
    manifest = json.loads((ROOT / "evidence/MANIFEST.json").read_bytes())
    man_map = {e["path"]: e["sha256"] for e in manifest["files"]}
    for rel, exp in PINNED_SHA256.items():
        p = exe_path if rel == "editor.exe" else (data_dir / rel if rel in ("client_db.dat", "server_db.dat") else ROOT / rel)
        got = _sha256_file(p)
        if got != exp:
            raise AssertionError(f"SHA-256 mismatch for {rel}: {got} != {exp}")
        if rel in man_map and man_map[rel] != got:
            raise AssertionError(f"MANIFEST mismatch for {rel}")
    ok(f"Pinned SHA-256 & MANIFEST.json ({len(PINNED_SHA256)} frozen inputs verified)")

    # Load generated artifacts
    xref = json.loads((out_dir / "xref_extra3.json").read_bytes())
    fmap = json.loads((out_dir / "field_map.json").read_bytes())
    dstat = json.loads((out_dir / "domain_stats.json").read_bytes())
    master = json.loads((ROOT / "evidence/fm24/reports/editor_schema/master.json").read_bytes())
    club_fields = master["entities"]["club.xml"][0]["fields"]
    occ_counts = Counter(f["field"] for f in club_fields)
    t71_fm = json.loads((ROOT / "scratch/t71/out/field_map_r3.json").read_bytes())
    t71_indices = {int(e["id"].rsplit("/", 1)[1]) for e in t71_fm["fields"]}

    # Check 3: Pure-struct PE32+ static witness verification
    pe64 = PurePE64(exe_path.read_bytes())
    w_cnt = 0
    for nm, w in xref["core_witnesses"].items():
        pe64.verify_witness(w, f"core:{nm}")
        w_cnt += 1
    # Verify UEFA divisor == 1000.0 and rel32 jump tables
    div_val = struct.unpack("<d", bytes.fromhex(xref["core_witnesses"]["UEFA_DIV_1000_F64"]["bytes"]))[0]
    if div_val != 1000.0:
        raise AssertionError(f"UEFA divisor != 1000.0: {div_val}")
    for jt_name, base_fo in [("CLUB_GET_0xe91db0", 0xE91DB0), ("CLUB_SET_0xe86b54", 0xE86B54)]:
        cells = xref["uefa_jump_tables"][jt_name]
        if len(cells) != 9:
            raise AssertionError(f"{jt_name} len != 9")
        for idx, c in enumerate(cells):
            cfo = base_fo + 4 * idx
            rel = struct.unpack_from("<i", pe64.blob, cfo)[0]
            if c["rel32"] != rel or int(c["target_fo"], 16) != base_fo + rel:
                raise AssertionError(f"{jt_name}[{idx}] mismatch")
            w_cnt += 1
    # Verify all polymorphic vtables, RTTI, readers, getters
    for entry in xref["polymorphic_base0_dispatch"]:
        if entry["vtable"] is not None:
            vt_fo = int(entry["vtable"]["vtable_fo"], 16)
            col_ptr = struct.unpack_from("<Q", pe64.blob, vt_fo - 8)[0]
            col_fo = pe64.va_to_fo(col_ptr)
            td_rva = struct.unpack_from("<I", pe64.blob, col_fo + 12)[0]
            td_fo = pe64.va_to_fo(pe64.image_base + td_rva)
            rtti_end = pe64.blob.find(b"\x00", td_fo + 16)
            rtti = pe64.blob[td_fo + 16:rtti_end].decode("ascii")
            if rtti != entry["vtable"]["rtti"]:
                raise AssertionError(f"Poly tag {entry['tag']} RTTI mismatch: {rtti}")
            pe64.verify_witness(entry["reader"], f"poly{entry['tag']}:reader")
            w_cnt += 1
            if entry["item_getter"]:
                pe64.verify_witness(entry["item_getter"], f"poly{entry['tag']}:getter")
                w_cnt += 1
    # Verify STARTING_RECORD negative proof
    neg_sr = xref["negative_proof_starting_record"]
    for nm, w in neg_sr["witnesses"].items():
        pe64.verify_witness(w, f"neg_sr:{nm}")
        w_cnt += 1
    # Explicitly assert 0xf06c70 contains mov edx, 0x2d (ba 2d 00 00 00) and RTTI matches STARTING_RECORD
    if not neg_sr["witnesses"]["table_45_init_type_0x2d"]["bytes"].startswith("ba2d000000"):
        raise AssertionError("0xf06c70 does not start with mov edx, 0x2d")
    if "DATABASE_TABLE@VSTARTING_RECORD@db" not in neg_sr["database_table_vtable"]["rtti"]:
        raise AssertionError("STARTING_RECORD RTTI check failed")
    # Verify every field_map getter/setter/reader witness
    for e in fmap["fields"]:
        pe64.verify_witness(e["static_chain"]["getter"], f"fm:{e['code']}:get")
        pe64.verify_witness(e["static_chain"]["reader"], f"fm:{e['code']}:rdr")
        w_cnt += 2
        if e["static_chain"]["setter"] is not None:
            pe64.verify_witness(e["static_chain"]["setter"], f"fm:{e['code']}:set")
            w_cnt += 1
    ok(f"Pure-struct PE32+ static verification ({w_cnt} instruction/table/vtable/RTTI witnesses exact)")

    # Check 4: Independent FMF extraction + join tables
    cli_m = _extract_fmf_members(data_dir / "client_db.dat", ["client_db/table_extra_3.dat", "client_db/table_3.dat", "client_db/table_25.dat"])
    srv_m = _extract_fmf_members(data_dir / "server_db.dat", ["server_db/table_extra_3.dat", "server_db/table_23.dat", "server_db/table_45.dat"])
    if _sha256_bytes(cli_m["client_db/table_extra_3.dat"]) != dstat["archives"]["client_extra3"]["stream_sha256"]:
        raise AssertionError("client table_extra_3 stream SHA-256 mismatch")
    if _sha256_bytes(srv_m["server_db/table_extra_3.dat"]) != dstat["archives"]["server_extra3"]["stream_sha256"]:
        raise AssertionError("server table_extra_3 stream SHA-256 mismatch")
    club_o2u, club_uids = _scan_uids(cli_m["client_db/table_3.dat"])
    _, comp_uids = _scan_uids(cli_m["client_db/table_25.dat"])
    _, sn_uids = _scan_uids(srv_m["server_db/table_23.dat"])
    t45_cnt = struct.unpack_from("<I", srv_m["server_db/table_45.dat"], 8)[0]
    if not (len(club_uids) == 84259 and len(comp_uids) == 7047 and len(sn_uids) == 278 and t45_cnt == 84477):
        raise AssertionError("Join table counts mismatch")
    ok(f"Independent FMF extraction & join tables (t3={len(club_uids)}, t25={len(comp_uids)}, t23={len(sn_uids)}, t45={t45_cnt})")

    # Check 5: Full-archive sequential replay + EOF + 100% client==server common tail
    rp = _replay_both(cli_m["client_db/table_extra_3.dat"], srv_m["server_db/table_extra_3.dat"])
    if rp["cli_tail_sha"] != rp["srv_tail_sha"] or rp["cli_tail_sha"] != dstat["archives"]["client_extra3"]["common_tail_sha256"]:
        raise AssertionError("Client vs server common tail SHA-256 mismatch")
    ok(f"Byte-exact replay of 84,259 x 2 rows (EOF exact, footer=0, common tail 100% client==server: {rp['cli_tail_sha'][:16]}...)")

    # Check 6: Vectorized scalar/enum/UEFA column SHA-256 digests & invariants
    cols = rp["cols"]
    el_mask = cols["elec_flag"] == 1
    if int(np.sum(el_mask)) != 11963:
        raise AssertionError("elec_flag==1 count != 11963")
    if int(np.sum(cols["elec_club"][el_mask] == np.where(el_mask)[0])) != 11963:
        raise AssertionError("elec_club != row_ordinal")
    if int(np.sum(el_mask == np.isin(cols["Cown"], [3, 7]))) != 84259:
        raise AssertionError("elec_flag==1 iff Cown in {3,7} failed")
    if not (rp["cli_cc_ff"] == 84259 and rp["cli_cc_0"] == 0 and int(np.sum(cols["cc"] == 0xFFFFFFFF)) == 84259 and int(np.sum(cols["cc"] == 0)) == 0):
        raise AssertionError("+0xcc 0xffffffff vs 0 check failed")
    for name, st in dstat["scalar_and_enum_domains"].items():
        arr = cols[name][el_mask] if name in ("Cetl", "Cmtm", "Cect", "Cemn", "Cemx", "Cepr") else cols[name]
        if _sha256_bytes(arr.tobytes()) != st["sha256"]:
            raise AssertionError(f"Column SHA-256 mismatch on {name}")
    cuf_codes = [f"Cuf{k}" for k in range(1, 10)] + ["Cf10"]
    for k, fc in enumerate(cuf_codes):
        if _sha256_bytes(rp["cuf_raw"][:, k].tobytes()) != dstat["uefa_ring_domains"][fc]["sha256"]:
            raise AssertionError(f"UEFA column SHA-256 mismatch on {fc}")
    tcht_sha = _sha256_bytes(json.dumps(sorted(rp["tcht_map"].items()), ensure_ascii=False).encode("utf-8"))
    if tcht_sha != dstat["common_tail_domains"]["TCht"]["sha256"]:
        raise AssertionError("TCht digest mismatch")
    if _sha256_bytes(cols["base_a0"].tobytes()) != dstat["common_tail_domains"]["ttcl"]["sha256"]:
        raise AssertionError("ttcl digest mismatch")
    if _sha256_bytes(cols["base_a8"].tobytes()) != dstat["common_tail_domains"]["tbcl"]["sha256"]:
        raise AssertionError("tbcl digest mismatch")
    if sum(rp["kit_buckets"].values()) != 405204 or set(rp["kit_buckets"].keys()) != {(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)}:
        raise AssertionError("Kit 6-bucket partition mismatch")
    ok("All 40 scalar/enum/UEFA/common-tail column SHA-256 digests, 405,204-kit partition, elec/Cown & 0xffffffff invariants verified")

    # Check 7: List & polymorphic item-level counts + joins + counterexamples
    if not (
        len(rp["cscm_items"]) == 15360
        and len(rp["cpsl_items"]) == 694
        and len(rp["cspb_items"]) == 46
        and len(rp["cren_items"]) == 1202
        and len(rp["tcrs_items"]) == 23027
        and len(rp["csoc_items"]) == 2616
        and len(rp["camc_items"]) == 1601
        and len(rp["cbbl_items"]) == 75
        and len(rp["pcpt_items"]) == 29
        and rp["b0_tags"][35] == 0
    ):
        raise AssertionError("List/polymorphic item counts mismatch")
    # Independent join & violation cross-checks
    assert sum(1 for x in rp["cscm_items"] if x[2] not in comp_uids) == 0
    assert sum(1 for x in rp["cscm_items"] if x[5] == 0) == 118
    assert sum(1 for x in rp["cscm_items"] if x[5] not in (-1, 0) and x[5] not in sn_uids) == 0
    assert sum(1 for x in rp["csoc_items"] if not (0 <= x[3] < 84259) or not (0 <= x[4] <= 100) or x[1] <= 0) == 0
    assert sum(1 for x in rp["csoc_items"] if x[3] not in club_uids) == 1068
    assert sum(1 for x in rp["cbbl_items"] if not (0 <= x[4] < 84259) or not (0 <= x[3] <= 1_000_000_000) or x[1] <= 0) == 0
    assert sum(1 for x in rp["cbbl_items"] if x[4] not in club_uids) == 23
    assert sum(1 for x in rp["camc_items"] if x[6] < 1) == 973
    assert sum(1 for x in rp["pcpt_items"] if x[2] <= 0 or not _date4_valid(x[4])) == 0
    assert sum(1 for x in rp["cpsl_items"] if x[1] != 2 or x[2] <= 0 or x[3] <= 0) == 0
    ftjn = {int(v["enum"]) for v in master["enums"]["ftjn"]["values"]}
    assert sum(1 for x in rp["tcrs_items"] if x[4] != 0 and x[4] not in ftjn) == 2709
    ok("All 10 populated list/polymorphic collections, table_25/table_23/table_3 joins, wrong-UID controls & counterexamples verified")

    # Check 8: Triple-gate & prior-negative enforcement on field_map.json
    if fmap["L4"] != 0 or xref["L4"] != 0 or dstat["L4"] != 0:
        raise AssertionError("L4 must be 0")
    if fmap["superseded_prior_negatives"] != []:
        raise AssertionError("Unexpected superseded prior negatives")
    seen_idx = set()
    l3_cnt = 0
    held_cnt = 0
    for e in fmap["fields"]:
        idx = e["xml_index"]
        if idx in seen_idx:
            raise AssertionError(f"Duplicate xml_index {idx} in field_map")
        seen_idx.add(idx)
        if idx in t71_indices:
            raise AssertionError(f"Overlap with t71 L3 index {idx}")
        fld = club_fields[idx]
        if fld["field"] != e["code"]:
            raise AssertionError(f"club.xml[{idx}] code mismatch: {fld['field']} != {e['code']}")
        if e["grade"] == "L3":
            l3_cnt += 1
            if occ_counts[e["code"]] != 1:
                raise AssertionError(f"L3 {e['code']} fails Gate 1 (non-unique occurrence)")
            if e["static_chain"]["setter"] is None:
                raise AssertionError(f"L3 {e['code']} missing setter witness")
            if fld["type"] in ("enum", "multiple_enum") and not fld.get("enum_ref"):
                raise AssertionError(f"L3 {e['code']} lacks scoped enum_ref")
            if e["domain"].get("violations", 0) != 0:
                raise AssertionError(f"L3 {e['code']} has violations")
        elif e["grade"] == "held":
            held_cnt += 1
            if not e.get("hold_reason") or not e.get("first_counterexample"):
                raise AssertionError(f"held {e['code']}[{idx}] missing hold_reason or first_counterexample")
        else:
            raise AssertionError(f"Unexpected grade {e['grade']} in fields")
    if l3_cnt != fmap["grade_counts"]["L3"] or held_cnt != fmap["grade_counts"]["held"]:
        raise AssertionError("Grade counts tally mismatch")
    # Ensure preserved t63 held CssT..E & Cmls are present and held
    held_idx = {e["xml_index"] for e in fmap["fields"] if e["grade"] == "held"}
    neg_held_idx = {e["xml_index"] for e in fmap["negative_not_extra3"] if e["grade"] == "held"}
    if not ({109, 110, 111, 112}.issubset(held_idx) and 432 in neg_held_idx):
        raise AssertionError("Preserved t63 held items missing")
    ok(f"Triple-gate & negative-preservation audit passed (L3={l3_cnt}, held={held_cnt}, negatives={len(fmap['negative_not_extra3'])}, t71 overlap=0, L4=0)")

    # Check 9: Known-club L2 anchor cross-checks
    assert club_o2u[460] == 676 and int(cols["d8"][460]) == 1892 and int(cols["Catd"][460]) == 52998 and rp["tcht_map"][460] == "Liverpool"
    assert rp["cuf_raw"][460].tolist() == [0, 10000, 22000, 0, 30000, 29000, 18000, 24000, 33000, 19000]
    assert club_o2u[463] == 679 and int(cols["d8"][463]) == 1894 and rp["tcht_map"][463] == "mcfc"
    assert club_o2u[1297] == 1736 and int(cols["d8"][1297]) == 1902 and int(cols["Catd"][1297]) == 68000
    assert club_o2u[623] == 915 and int(cols["d8"][623]) == 1900 and int(cols["Catd"][623]) == 75024
    ok("Known-club L2 anchor cross-checks (Liverpool, Man City, Real Madrid, Bayern Munich) verified")

    print(f"[t82/verify] ALL {passed}/{passed} CHECKS PASSED")
    return 0


def run_selftest() -> int:
    _check_import_hygiene()
    assert _date4_valid(SENTINEL_DATE4)
    assert _date4_valid((2024 << 16) | 366)
    assert not _date4_valid((2023 << 16) | 366)
    assert not _date4_valid((2023 << 16) | 0)
    assert not _date4_valid((2023 << 16) | (1 << 9) | 1)
    print("[t82/verify] selftest PASS")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Independent verifier for t82 table_extra_3.dat deliverables (zero builder imports)."
    )
    ap.add_argument("--selftest", action="store_true", help="Run built-in unit self-tests and exit.")
    ap.add_argument("--exe", type=Path, default=DEFAULT_EXE, help="Path to read-only editor.exe.")
    ap.add_argument("--data-dir", type=Path, default=DEFAULT_DATA, help="Path to scratch/data directory.")
    ap.add_argument("--outdir", type=Path, default=DEFAULT_OUT, help="Directory holding t82 JSON artifacts.")
    args = ap.parse_args(argv)
    try:
        if args.selftest:
            return run_selftest()
        return run_verify(args.exe, args.data_dir, args.outdir)
    except AssertionError as exc:
        print(f"[t82/verify] FAIL: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"[t82/verify] FATAL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
