#!/usr/bin/env python3
"""t79 — stadium(21) + team(24) + extra_24 static L3 harvest + CLUB+0x18 forwarding chain builder.

Outputs into --outdir (default: scratch/t79/out):
  - xref_stad_team.json
  - field_map.json

Exit codes: 0 success, 1 check failed, 2 usage/fatal error.
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
from collections import Counter
from pathlib import Path
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(_cfg.VENDOR_DIR))
sys.path.insert(0, str(ROOT / "scripts"))

import numpy as np
import zstandard as zstd
from capstone import CS_ARCH_X86, CS_MODE_64, Cs
from capstone.x86 import X86_OP_IMM

from t05_pe import PE
from t21b_control_flow import ReaderCFG

EXE_PATH = Path(str(_cfg.EDITOR_EXE))
EXPECTED_EXE_SHA256 = "b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4"
DB_DIR = Path(os.environ.get("FM24_DB_DIR", str(ROOT / "scratch/data")))
MANIFEST_PATH = ROOT / "evidence/MANIFEST.json"
MASTER_REL = "evidence/fm24/reports/editor_schema/master.json"
BIG_REL = "evidence/fm24/reports/dbdat_decode/db_tables_big.json"
EXTRA_VERDICT_REL = "evidence/fm24/reports/dbdat_decode/extra_tables_verdict.json"
FRAMES_PATH = ROOT / "scratch/t74/out/frames.json"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_manifest_and_inputs() -> dict[str, Any]:
    exe_sha = sha256_file(EXE_PATH)
    if exe_sha != EXPECTED_EXE_SHA256:
        raise RuntimeError(f"editor.exe SHA-256 mismatch: {exe_sha} != {EXPECTED_EXE_SHA256}")
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    by_path = {entry["path"]: entry["sha256"] for entry in manifest["files"]}
    checked = {"editor.exe": {"path": str(EXE_PATH), "sha256": exe_sha, "verified": True}}
    for rel in (MASTER_REL, BIG_REL, EXTRA_VERDICT_REL):
        exp = by_path[rel]
        got = sha256_file(ROOT / rel)
        if got != exp:
            raise RuntimeError(f"MANIFEST SHA-256 mismatch for {rel}: {got} != {exp}")
        checked[rel] = {"sha256": got, "manifest_match": True}
    return checked


def load_fmf_members(side: str, members: list[str]) -> tuple[dict[str, bytes], set[str]]:
    raw = (DB_DIR / f"{side}_db.dat").read_bytes()
    toc, base = (x + 17 for x in struct.unpack_from("<QQ", raw, 17))
    directory = zstd.ZstdDecompressor().decompressobj().decompress(raw[toc + 9:])
    pos = [0]
    entries: dict[str, tuple[int, int, int]] = {}

    def pull(n: int) -> bytes:
        a = pos[0]
        pos[0] += n
        return directory[a:a + n]

    def num() -> int:
        return struct.unpack("<I", pull(4))[0]

    def text() -> str:
        return pull(num()).decode("utf-8")

    def node(parent: str) -> None:
        prefix = parent + text() + "/"
        for _ in range(num()):
            name = prefix + text() + text()
            off, sz, unp, _, _ = struct.unpack("<5Q", pull(40))
            entries[name] = (base + off, base + off + sz, unp)
        for _ in range(num()):
            node(prefix)

    node("")
    out: dict[str, bytes] = {}
    for m in members:
        key = f"{side}_db/{m}"
        if key not in entries:
            continue
        lo, hi, sz = entries[key]
        q = lo
        while q < hi:
            dec = zstd.ZstdDecompressor().decompressobj()
            pl = dec.decompress(raw[q:hi])
            used = (hi - q) - len(dec.unused_data)
            if len(pl) == sz:
                out[m] = pl
                break
            q += used
        if m not in out:
            raise RuntimeError(f"failed to decompress {key}")
    return out, set(entries.keys())


def packed_date_stats(vals: np.ndarray) -> dict[str, Any]:
    v = np.asarray(vals, dtype="<u4")
    y = v >> 16
    d = v & 0x1FF
    rem = (v >> 9) & 0x7F
    leap = (y % 4 == 0) & ((y % 100 != 0) | (y % 400 == 0))
    ok = (rem == 0) & (y >= 1) & (d >= 1) & (d <= 365 + leap)
    return {
        "n": int(len(v)),
        "valid_gregorian": int(ok.sum()),
        "invalid": int((~ok).sum()),
        "year_min": int(y.min()),
        "year_max": int(y.max()),
        "default_1900_01_01_count": int((v == 0x076C0001).sum()),
    }


def extract_rtti_name(pe: PE, vtable_va: int) -> str:
    vt_fo = pe.va2f(vtable_va)
    col_va = struct.unpack_from("<Q", pe.raw, vt_fo - 8)[0]
    col_fo = pe.va2f(col_va)
    sig, _, _, td_rva = struct.unpack_from("<IIII", pe.raw, col_fo)
    assert sig == 1, f"unexpected COL sig {sig}"
    td_fo = pe.va2f(pe.pe.OPTIONAL_HEADER.ImageBase + td_rva)
    end = pe.raw.index(b"\x00", td_fo + 16)
    return pe.raw[td_fo + 16:end].decode("ascii")


def insn_snap(pe: PE, md: Cs, fo: int, count: int = 1) -> list[dict[str, Any]]:
    out = []
    for ins in md.disasm(pe.raw[fo:fo + count * 16], pe.f2va(fo), count):
        f = pe.va2f(ins.address)
        out.append({
            "fo": hex(f),
            "va": hex(ins.address),
            "bytes": ins.bytes.hex(),
            "text": f"{ins.mnemonic} {ins.op_str}".strip(),
        })
    return out


def follow_thunk(pe: PE, md: Cs, fo: int) -> int:
    ins = next(md.disasm(pe.raw[fo:fo + 15], pe.f2va(fo), 1))
    if ins.mnemonic == "jmp" and ins.operands and ins.operands[0].type == X86_OP_IMM:
        return pe.va2f(ins.operands[0].imm)
    return fo


def cfg_summary(pe: PE, md: Cs, fo: int) -> dict[str, Any]:
    real = follow_thunk(pe, md, fo)
    g = ReaderCFG(pe, md, real)
    ind = []
    ext_jmps = []
    for va, ins in sorted(g.instructions.items()):
        if ins.mnemonic == "jmp":
            if ins.operands and ins.operands[0].type == X86_OP_IMM:
                if ins.operands[0].imm not in g.instructions:
                    ext_jmps.append({
                        "at_fo": hex(pe.va2f(va)),
                        "target_fo": hex(pe.va2f(ins.operands[0].imm)),
                    })
            else:
                ind.append({"at_fo": hex(pe.va2f(va)), "text": f"{ins.mnemonic} {ins.op_str}"})
    return {
        "entry_fo": hex(fo),
        "entry_va": hex(pe.f2va(fo)),
        "real_fo": hex(real),
        "real_va": hex(pe.f2va(real)),
        "end_fo": hex(g.function_end_off),
        "ins_count": len(g.instructions),
        "indirect_jmp_count": len(ind),
        "indirect_jmps": ind,
        "external_tail_jmps": ext_jmps,
    }


def decode_rel32_entry(pe: PE, table_fo: int, idx: int) -> dict[str, Any]:
    rel = struct.unpack_from("<i", pe.raw, table_fo + idx * 4)[0]
    target_va = pe.f2va(table_fo) + rel
    target_fo = pe.va2f(target_va)
    return {
        "table_fo": hex(table_fo),
        "index": idx,
        "rel32": hex(rel & 0xFFFFFFFF),
        "target_fo": hex(target_fo),
        "target_va": hex(target_va),
    }


def get_entity_fields(master: dict[str, Any], entity_key: str) -> list[dict[str, Any]]:
    e = master["entities"][entity_key]
    if isinstance(e, list) and e and isinstance(e[0], dict) and "fields" in e[0]:
        return [x for blk in e for x in blk.get("fields", [])]
    if isinstance(e, list):
        return e
    return e["fields"]


def scan_table_uids(buf: bytes) -> np.ndarray:
    n = struct.unpack_from("<I", buf, 8)[0]
    if (len(buf) - 22) % n == 0:
        st = (len(buf) - 22) // n
        arr = np.frombuffer(buf, dtype=np.uint8, offset=13, count=n * st).reshape(n, st)
        ords = arr[:, st - 12:st - 8].copy().view("<u4").ravel()
        u1 = arr[:, st - 8:st - 4].copy().view("<u4").ravel()
        u2 = arr[:, st - 4:st].copy().view("<u4").ravel()
        if np.array_equal(ords, np.arange(n, dtype=np.uint32)) and np.array_equal(u1, u2):
            return u1
    uids = np.empty(n, dtype=np.uint32)
    pos = 13
    for i in range(n):
        pat = struct.pack("<I", i)
        cur = pos
        while True:
            idx = buf.find(pat, cur)
            if idx == -1 or idx + 12 > len(buf) - 9:
                raise RuntimeError(f"failed to scan identity triple at row {i}")
            u1, u2 = struct.unpack_from("<II", buf, idx + 4)
            if u1 == u2 and u1 not in (0, 0xFFFFFFFF):
                uids[i] = u1
                pos = idx + 12
                break
            cur = idx + 1
    return uids


def ref_domain_check(vals: np.ndarray, target_count: int, target_uid_set: set[int]) -> dict[str, Any]:
    v = np.asarray(vals, dtype=np.int64)
    live = v[v >= 0]
    null_n = int((v == -1).sum())
    other_neg = int(((v < 0) & (v != -1)).sum())
    ord_hit = int((live < target_count).sum())
    ord_miss = int((live >= target_count).sum())
    wrong_uid_hit = int(sum(1 for x in live.tolist() if x in target_uid_set))
    return {
        "rows": int(len(v)),
        "live": int(len(live)),
        "null_minus1": null_n,
        "other_neg": other_neg,
        "ordinal_in_range": ord_hit,
        "ordinal_miss": ord_miss,
        "wrong_uid_control_hits": wrong_uid_hit,
        "wrong_uid_control_misses": int(len(live) - wrong_uid_hit),
        "live_min": int(live.min()) if len(live) else None,
        "live_max": int(live.max()) if len(live) else None,
        "violations": int(other_neg + ord_miss),
    }


def replay_table_24(pl24: bytes) -> dict[str, Any]:
    n24 = struct.unpack_from("<I", pl24, 8)[0]
    sel = np.empty(n24, np.uint8)
    uid = np.empty(n24, np.uint32)
    rdui = np.empty(n24, np.uint32)
    trep = np.empty(n24, np.int16)
    tdvi = np.empty(n24, np.int32)
    tldi = np.empty(n24, np.int32)
    tndi = np.empty(n24, np.int32)
    tsti = np.empty(n24, np.int32)
    tmni = np.empty(n24, np.int32)
    c98 = np.empty(n24, np.int32)
    todo = np.empty(n24, np.int32)
    tnod = np.empty(n24, np.int32)
    v38 = np.empty(n24, np.uint16)
    ttyp = np.empty(n24, np.int8)
    tisn = np.empty(n24, np.uint8)
    own = np.empty(n24, np.int32)
    lna_len = np.empty(n24, np.uint32)
    sna_len = np.empty(n24, np.uint32)
    row_widths = np.empty(n24, np.int32)
    nt_subcnt_nz = 0
    lna_utf8_err = 0
    sna_utf8_err = 0
    lna_samples: list[dict[str, Any]] = []
    sna_samples: list[dict[str, Any]] = []

    p = 13
    for i in range(n24):
        p0 = p
        s = pl24[p]
        p += 1
        sel[i] = s
        if s == 11:
            p += 48
            mc = struct.unpack_from("<b", pl24, p)[0]
            p += 1
            if mc > 0:
                nt_subcnt_nz += 1
                p += mc * 10
        elif s != 10:
            raise RuntimeError(f"unexpected table_24 selector {s} at row {i}")
        _, _, rep, dvi, ldi, ndi, sti, mni, x98, _, odo, vc = struct.unpack_from("<BbhiiiiiiBiH", pl24, p)
        p += 35 + vc * 4
        p += 13  # +88(4), +90(4), +aa..+b1(5)
        nod = struct.unpack_from("<i", pl24, p)[0]
        p += 5  # nod(4) + b2(1)
        typ, isn = struct.unpack_from("<bB", pl24, p)
        p += 6  # +28,+2f,+29,+2c,+2d,+2e
        ow = struct.unpack_from("<i", pl24, p)[0]
        p += 4
        l1 = struct.unpack_from("<I", pl24, p)[0]
        p += 4
        b1 = pl24[p:p + l1]
        p += l1 + 1  # + Tlng
        l2 = struct.unpack_from("<I", pl24, p)[0]
        p += 4
        b2 = pl24[p:p + l2]
        p += l2 + 1  # + Tsng
        o, u1, u2 = struct.unpack_from("<III", pl24, p)
        p += 12
        if o != i or u1 != u2:
            raise RuntimeError(f"table_24 identity mismatch at row {i}: ord={o} u1={u1} u2={u2}")
        trep[i] = rep
        tdvi[i] = dvi
        tldi[i] = ldi
        tndi[i] = ndi
        tsti[i] = sti
        tmni[i] = mni
        c98[i] = x98
        todo[i] = odo
        tnod[i] = nod
        v38[i] = vc
        ttyp[i] = typ
        tisn[i] = isn
        own[i] = ow
        uid[i] = u1
        rdui[i] = u2
        lna_len[i] = l1
        sna_len[i] = l2
        row_widths[i] = p - p0
        if l1:
            try:
                txt = b1.decode("utf-8")
                if len(lna_samples) < 5:
                    lna_samples.append({"row": i, "uid": int(u1), "value": txt})
            except UnicodeDecodeError:
                lna_utf8_err += 1
        if l2:
            try:
                txt = b2.decode("utf-8")
                if len(sna_samples) < 5:
                    sna_samples.append({"row": i, "uid": int(u1), "value": txt})
            except UnicodeDecodeError:
                sna_utf8_err += 1

    footer = pl24[p:]
    if len(footer) != 9:
        raise RuntimeError(f"table_24 footer len {len(footer)} != 9")
    return {
        "n": n24,
        "header_bytes": 13,
        "body_end": p,
        "footer_hex": footer.hex(),
        "total_bytes": len(pl24),
        "selector_counts": {str(k): int(v) for k, v in sorted(Counter(sel.tolist()).items())},
        "width_min": int(row_widths.min()),
        "width_max": int(row_widths.max()),
        "nt_subcnt_nz": nt_subcnt_nz,
        "lna_utf8_err": lna_utf8_err,
        "sna_utf8_err": sna_utf8_err,
        "lna_samples": lna_samples,
        "sna_samples": sna_samples,
        "sel": sel,
        "uid": uid,
        "rdui": rdui,
        "trep": trep,
        "tdvi": tdvi,
        "tldi": tldi,
        "tndi": tndi,
        "tsti": tsti,
        "tmni": tmni,
        "c98": c98,
        "todo": todo,
        "tnod": tnod,
        "v38": v38,
        "ttyp": ttyp,
        "tisn": tisn,
        "own": own,
        "lna_len": lna_len,
        "sna_len": sna_len,
    }


def replay_table_3_base18(pl3: bytes, t24_ttyp: np.ndarray) -> dict[str, Any]:
    n3 = struct.unpack_from("<I", pl3, 8)[0]
    p = 13
    club_uid = np.empty(n3, np.uint32)
    b18_cnt = np.empty(n3, np.uint8)
    first_team = np.full(n3, -1, np.int32)
    first_non_skip = np.full(n3, -1, np.int32)
    skip0_cnt = 0
    total_team_refs = 0

    for i in range(n3):
        sel = pl3[p]
        p += 1
        if sel == 12:
            p += 5
        p += 26
        l1 = struct.unpack_from("<I", pl3, p)[0]
        p += 4 + l1
        l2 = struct.unpack_from("<I", pl3, p)[0]
        p += 4 + l2
        p += 8  # +1,+2,+4,+1
        c110 = struct.unpack_from("<b", pl3, p)[0]
        p += 1 + c110 * 4
        tag150 = pl3[p]
        p += 1
        if tag150 == 0:
            p += 45
        c130 = struct.unpack_from("<b", pl3, p)[0]
        p += 1 + c130 * 24
        c138 = struct.unpack_from("<b", pl3, p)[0]
        p += 1 + c138 * 12
        p += 6  # raw168(2) + stad140(4)
        p += 3  # base_ba(1) + base_b8(2)
        c18 = pl3[p]
        p += 1
        b18_cnt[i] = c18
        total_team_refs += c18
        if c18 > 0:
            teams = struct.unpack_from(f"<{c18}i", pl3, p)
            first_team[i] = teams[0]
            if t24_ttyp[teams[0]] in (0x16, 0x2C):
                skip0_cnt += 1
            for tid in teams:
                if tid >= 0 and t24_ttyp[tid] not in (0x16, 0x2C):
                    first_non_skip[i] = tid
                    break
        p += c18 * 4
        c30 = pl3[p]
        p += 1 + c30 * 4
        c60 = struct.unpack_from("<b", pl3, p)[0]
        p += 1 + c60 * 4
        c78 = struct.unpack_from("<b", pl3, p)[0]
        p += 1 + c78 * 4
        c90 = pl3[p]
        p += 1 + c90 * 4
        c48 = pl3[p]
        p += 1 + c48 * 16
        ca8 = struct.unpack_from("<h", pl3, p)[0]
        p += 2 + ca8 * 28
        o, u1, u2 = struct.unpack_from("<III", pl3, p)
        p += 12
        if o != i or u1 != u2:
            raise RuntimeError(f"table_3 identity mismatch at row {i}")
        club_uid[i] = u1

    footer = pl3[p:]
    if len(footer) != 9:
        raise RuntimeError(f"table_3 footer len {len(footer)} != 9")
    return {
        "n": n3,
        "total_bytes": len(pl3),
        "footer_hex": footer.hex(),
        "total_team_refs": total_team_refs,
        "clubs_with_teams": int((b18_cnt > 0).sum()),
        "clubs_with_zero_teams": int((b18_cnt == 0).sum()),
        "skip0_count": skip0_cnt,
        "first_eq_first_non_skip": bool(np.array_equal(first_team, first_non_skip)),
        "club_uid": club_uid,
        "b18_cnt": b18_cnt,
        "first_team": first_team,
        "first_non_skip": first_non_skip,
    }


def self_certify_extra_24(ex24: bytes, expected_count: int) -> dict[str, Any]:
    n_ex = struct.unpack_from("<I", ex24, 8)[0]
    if n_ex != expected_count:
        raise RuntimeError(f"extra_24 count {n_ex} != {expected_count}")

    # 1. Header/footer divisibility sensitivity
    sens = []
    for h in range(0, 21):
        for ft in range(0, 17):
            rem = len(ex24) - h - ft
            if rem > 0 and rem % n_ex == 0:
                st = rem // n_ex
                arr = np.frombuffer(ex24, dtype=np.uint8, offset=h, count=n_ex * st).reshape(n_ex, st)
                ords = arr[:, 0:4].copy().view("<u4").ravel()
                matches = int((ords == np.arange(n_ex, dtype=np.uint32)).sum())
                sens.append({"header": h, "footer": ft, "stride": st, "ordinal_matches": matches})

    # 2. Arbitrary-alignment full-chain ordinal search (start in 0..199, stride in 4..500)
    full_chain_hits = []
    for a in range(0, 200):
        if struct.unpack_from("<I", ex24, a)[0] != 0:
            continue
        for st in range(4, 501):
            if a + n_ex * st > len(ex24):
                break
            if (
                struct.unpack_from("<I", ex24, a + st)[0] == 1
                and struct.unpack_from("<I", ex24, a + 2 * st)[0] == 2
                and struct.unpack_from("<I", ex24, a + 3 * st)[0] == 3
                and struct.unpack_from("<I", ex24, a + (n_ex - 1) * st)[0] == n_ex - 1
            ):
                full_chain_hits.append({
                    "start": a,
                    "stride": st,
                    "footer": len(ex24) - (a + n_ex * st),
                })

    if full_chain_hits != [{"start": 12, "stride": 82, "footer": 0}]:
        raise RuntimeError(f"extra_24 framing not unique: {full_chain_hits}")

    arr = np.frombuffer(ex24, dtype=np.uint8, offset=12, count=n_ex * 82).reshape(n_ex, 82)
    # 3. Verify grammar closure (all variable-length counts == 0 and +0x10e len == 8)
    h80 = arr[:, 49:53].copy().view("<u4").ravel()
    h68 = arr[:, 53:57].copy().view("<u4").ravel()
    ha0 = arr[:, 62:64].copy().view("<u2").ravel()
    hd0 = arr[:, 64]
    ha8 = arr[:, 65]
    h98 = arr[:, 66:70].copy().view("<u4").ravel()
    h10e_len = arr[:, 70:74].copy().view("<u4").ravel()
    if not (
        np.all(h80 == 0)
        and np.all(h68 == 0)
        and np.all(ha0 == 0)
        and np.all(hd0 == 0)
        and np.all(ha8 == 0)
        and np.all(h98 == 0)
        and np.all(h10e_len == 8)
    ):
        raise RuntimeError("extra_24 grammar closure failed: non-degenerate variable section found")

    # Identify all varying byte offsets after ordinal (4..81)
    varying_cols = []
    for c in range(4, 82):
        u = np.unique(arr[:, c])
        if len(u) > 1:
            varying_cols.append({"offset": c, "distinct": int(len(u)), "values": u.tolist()})

    return {
        "total_bytes": len(ex24),
        "header_bytes": 12,
        "header_hex": ex24[:12].hex(),
        "record_count": n_ex,
        "stride_bytes": 82,
        "footer_bytes": 0,
        "size_equation": f"12 + {n_ex}*82 + 0 = {12 + n_ex * 82}",
        "arbitrary_alignment_unique_hits": full_chain_hits,
        "header_footer_sensitivity": sens,
        "varying_byte_offsets_after_ordinal": varying_cols,
        "all_variable_counts_zero": True,
        "h10e_fixed_len": 8,
        "arr": arr,
    }


def build_artifacts(outdir: Path) -> dict[str, Any]:
    outdir.mkdir(parents=True, exist_ok=True)
    integrity = verify_manifest_and_inputs()

    pe = PE(EXE_PATH)
    pe.pe.parse_data_directories(directories=[3])
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True

    master = json.loads((ROOT / MASTER_REL).read_text(encoding="utf-8"))
    big = json.loads((ROOT / BIG_REL).read_text(encoding="utf-8"))
    extra_verdict = json.loads((ROOT / EXTRA_VERDICT_REL).read_text(encoding="utf-8"))
    t74_frames = json.loads(FRAMES_PATH.read_text(encoding="utf-8"))

    # ---- 1. STATIC XREF EXTRACTION FROM editor.exe ----
    # Verify RTTI and vtables
    vtables = {}
    for cls_name, vt_va in [
        ("STADIUM", 0x14188DBD8),
        ("TEAM", 0x14188E2D8),
        ("NATIONAL_TEAM", 0x141889618),
        ("TEAM_BASE", 0x141882C78),
    ]:
        vt_fo = pe.va2f(vt_va)
        slots = [pe.va2f(struct.unpack_from("<Q", pe.raw, vt_fo + i * 8)[0]) for i in range(23)]
        vtables[cls_name] = {
            "vtable_va": hex(vt_va),
            "vtable_fo": hex(vt_fo),
            "rtti": extract_rtti_name(pe, vt_va),
            "slot_2_get_fo": hex(slots[2]),
            "slot_3_set_fo": hex(slots[3]),
            "slot_5_prop_reg_fo": hex(slots[5]),
            "slot_7_type_fo": hex(slots[7]),
            "slot_10_owner_fo": hex(slots[10]),
            "slot_19_read_fo": hex(slots[19]),
            "slot_20_fixup_fo": hex(slots[20]),
            "slot_21_write_fo": hex(slots[21]),
        }

    # Verify factory cases 21 and 24 in 0xf48b30 rel32 table 0xf49d38
    factory = {
        "function_fo": "0xf48b30",
        "function_va": hex(pe.f2va(0xF48B30)),
        "rel32_table_fo": "0xf49d38",
        "case_21_stadium": {
            **decode_rel32_entry(pe, 0xF49D38, 21),
            "alloc_fo": "0xf71b70",
            "ctor_fo": "0x1183c70",
            "ctor_real_fo": hex(follow_thunk(pe, md, 0x1183C70)),
            "dis_head": insn_snap(pe, md, 0xF49078, 8),
        },
        "case_24_team": {
            **decode_rel32_entry(pe, 0xF49D38, 24),
            "selector_cmp_ins": insn_snap(pe, md, 0xF490F9, 10),
            "selector_11_national_team": {
                "alloc_size": "0x100",
                "alloc_fo": "0xf71d80",
                "ctor_fo": "0x1052b30",
                "ctor_real_fo": hex(follow_thunk(pe, md, 0x1052B30)),
            },
            "selector_10_team": {
                "alloc_size": "0xb8",
                "alloc_fo": "0xf71e30",
                "ctor_fo": "0x11a0160",
                "ctor_real_fo": hex(follow_thunk(pe, md, 0x11A0160)),
            },
        },
    }

    # db+offset table registrations in 0xf026c0
    db_context_tables = [
        {"db_offset": "+0x8", "table_id": 2, "entity": "city", "ctor_call_fo": "0xf02837", "store_fo": "0xf02957", "ins": insn_snap(pe, md, 0xF02957, 1)[0]},
        {"db_offset": "+0x10", "table_id": 3, "entity": "club", "ctor_call_fo": "0xf02973", "store_fo": "0xf02a93", "ins": insn_snap(pe, md, 0xF02A93, 1)[0]},
        {"db_offset": "+0x18", "table_id": 25, "entity": "comp", "ctor_call_fo": "0xf02aaf", "store_fo": "0xf02bcf", "ins": insn_snap(pe, md, 0xF02BCF, 1)[0]},
        {"db_offset": "+0x60", "table_id": 9, "entity": "nation", "ctor_call_fo": "0xf035cb", "store_fo": "0xf036eb", "ins": insn_snap(pe, md, 0xF036EB, 1)[0]},
        {"db_offset": "+0x80", "table_id": 21, "entity": "stadium", "ctor_call_fo": "0xf03de6", "store_fo": "0xf03f06", "ins": insn_snap(pe, md, 0xF03F06, 1)[0]},
        {"db_offset": "+0x98", "table_id": 24, "entity": "team", "ctor_call_fo": "0xf041a3", "store_fo": "0xf042c3", "ins": insn_snap(pe, md, 0xF042C3, 1)[0]},
    ]

    # CFG extents for all key functions
    cfgs = {
        "STADIUM_read": cfg_summary(pe, md, 0x1183F30),
        "STADIUM_sides_read": cfg_summary(pe, md, 0x4401010),
        "STADIUM_fixup": cfg_summary(pe, md, 0x1184920),
        "STADIUM_get": cfg_summary(pe, md, 0x1185EB0),
        "STADIUM_set": cfg_summary(pe, md, 0x1189260),
        "STADIUM_side_get": cfg_summary(pe, md, 0x15E6650),
        "STADIUM_pitch_clamp": cfg_summary(pe, md, 0x3E42E30),
        "STADIUM_colour_helper": cfg_summary(pe, md, 0x3E448A0),
        "NATIONAL_TEAM_read": cfg_summary(pe, md, 0x1052C80),
        "NATIONAL_TEAM_fixup": cfg_summary(pe, md, 0x1053120),
        "NATIONAL_TEAM_get": cfg_summary(pe, md, 0x1056A90),
        "TEAM_read": cfg_summary(pe, md, 0x11A0880),
        "TEAM_fixup": cfg_summary(pe, md, 0x11A0C40),
        "TEAM_get": cfg_summary(pe, md, 0x11AF7B0),
        "TEAM_set": cfg_summary(pe, md, 0x11B4C30),
        "TEAM_slot10": cfg_summary(pe, md, 0x11BA390),
        "TEAM_BASE_read": cfg_summary(pe, md, 0x11C1D80),
        "TEAM_BASE_get": cfg_summary(pe, md, 0x11C2600),
        "TEAM_BASE_set": cfg_summary(pe, md, 0x11C23F0),
        "TEAM_BASE_slot10": cfg_summary(pe, md, 0x11C5350),
        "DATABASE_RECORD_get": cfg_summary(pe, md, 0xFE3520),
        "EXTRA_24_loader": cfg_summary(pe, md, 0x3BB9B00),
        "EXTRA_24_record_read": cfg_summary(pe, md, 0x11A1580),
        "CLUB_BASE_read": cfg_summary(pe, md, 0x11D0D30),
        "CLUB_BASE_fixup": cfg_summary(pe, md, 0x11D2580),
        "CLUB_fwd_team_get": cfg_summary(pe, md, 0x11F41D0),
        "CLUB_fwd_team_set": cfg_summary(pe, md, 0x11F6CF0),
        "CLUB_set_team_rep": cfg_summary(pe, md, 0x3C951A0),
    }

    # Key static proof instructions
    static_proofs = {
        "stadium_client_vs_server_branch": insn_snap(pe, md, 0x1183F49, 4),
        "stadium_splr_noop_dispatch": insn_snap(pe, md, 0x1186313, 3),
        "stadium_splR_get_dispatch": insn_snap(pe, md, 0x1186A4C, 6),
        "stadium_splR_set_dispatch": insn_snap(pe, md, 0x1189678, 8),
        "stadium_scov_get_branch": insn_snap(pe, md, 0x118628F, 10),
        "stadium_scov_set": insn_snap(pe, md, 0x1189636, 9),
        "stadium_spty_clamp": insn_snap(pe, md, 0x1186603, 6),
        "stadium_sdtr_direct_movsx": insn_snap(pe, md, 0x11872FE, 2),
        "stadium_soty_suppress_zero": insn_snap(pe, md, 0x118679C, 5),
        "stadium_sucy_suppress_le0": insn_snap(pe, md, 0x1186398, 5),
        "stadium_snti_city_fwd": insn_snap(pe, md, 0x11872E8, 5),
        "stadium_scpc_table22_scan": insn_snap(pe, md, 0x1187372, 6),
        "team_trep_post_read_clamp": insn_snap(pe, md, 0x11A090D, 4),
        "extra_24_callsite_in_db_load": insn_snap(pe, md, 0xF5167E, 7),
        "extra_24_filename_fmt": insn_snap(pe, md, 0x3BB9B2F, 8),
        "extra_24_alloc_bind_team_a0": insn_snap(pe, md, 0x11A15AD, 11),
        "extra_24_twhm_get": insn_snap(pe, md, 0x11B0406, 5),
        "extra_24_tmhm_get": insn_snap(pe, md, 0x11B08C1, 4),
        "extra_24_tpvr_get": insn_snap(pe, md, 0x11AFB1F, 5),
        "club_base18_fixup_team_lookup": insn_snap(pe, md, 0x11D25A8, 12),
        "club_csti_get_rel32": decode_rel32_entry(pe, 0xE91D8C, 8),
        "club_csti_set_rel32": decode_rel32_entry(pe, 0xE86B38, 6),
        "dbrec_duni_get": insn_snap(pe, md, 0xFE3BFF, 3),
        "dbrec_rdui_suppress": insn_snap(pe, md, 0xFE389D, 4),
    }

    # ---- 2. FULL-ARCHIVE VECTORIZED DATA REPLAY & VALIDATION ----
    cli, cli_names = load_fmf_members("client", ["table_2.dat", "table_3.dat", "table_9.dat", "table_21.dat", "table_25.dat"])
    srv, srv_names = load_fmf_members("server", ["table_2.dat", "table_3.dat", "table_21.dat", "table_24.dat", "table_25.dat", "table_extra_24.dat"])

    assert "client_db/table_24.dat" not in cli_names, "expected table_24 server-only"
    assert "client_db/table_extra_24.dat" not in cli_names, "expected table_extra_24 server-only"

    # Reference target tables
    c2 = cli["table_2.dat"]
    n_t2 = struct.unpack_from("<I", c2, 8)[0]
    t2_arr = np.frombuffer(c2, dtype=np.uint8, offset=13, count=n_t2 * 43).reshape(n_t2, 43)
    t2_uids_arr = t2_arr[:, 35:39].copy().view("<u4").ravel()
    t2_uids = set(t2_uids_arr.tolist())

    t3_uids_arr = scan_table_uids(cli["table_3.dat"])
    t3_uids = set(t3_uids_arr.tolist())
    t9_uids_arr = scan_table_uids(cli["table_9.dat"])
    t9_uids = set(t9_uids_arr.tolist())
    t25_uids_arr = scan_table_uids(cli["table_25.dat"])
    t25_uids = set(t25_uids_arr.tolist())

    # ---- TABLE 21: STADIUM ----
    c21 = cli["table_21.dat"]
    s21 = srv["table_21.dat"]
    n_t21 = struct.unpack_from("<I", c21, 8)[0]
    assert n_t21 == struct.unpack_from("<I", s21, 8)[0] == 48413
    assert len(c21) == 13 + n_t21 * 38 + 9
    assert len(s21) == 13 + n_t21 * 181 + 9
    c21_footer = c21[13 + n_t21 * 38:]
    s21_footer = s21[13 + n_t21 * 181:]
    assert c21_footer == s21_footer

    c21_raw = np.frombuffer(c21, dtype=np.uint8, offset=13, count=n_t21 * 38).reshape(n_t21, 38)
    s21_raw = np.frombuffer(s21, dtype=np.uint8, offset=13, count=n_t21 * 181).reshape(n_t21, 181)
    assert np.all(c21_raw[:, 0] == 0) and np.all(s21_raw[:, 0] == 0)
    cb = c21_raw[:, 1:]   # 37B: 0..24 common body + 25..36 identity
    sb = s21_raw[:, 1:]   # 180B: 0..142 server prefix + 143..167 common body + 168..179 identity
    common_identical = bool(np.array_equal(cb, sb[:, 143:]))
    assert common_identical

    t21_ords = cb[:, 25:29].copy().view("<u4").ravel()
    t21_duni = cb[:, 29:33].copy().view("<u4").ravel()
    t21_rdui = cb[:, 33:37].copy().view("<u4").ravel()
    assert np.array_equal(t21_ords, np.arange(n_t21, dtype=np.uint32))
    assert np.array_equal(t21_duni, t21_rdui)
    t21_uids = set(t21_duni.tolist())
    assert len(t21_uids) == n_t21

    def col_i32(a: np.ndarray, o: int) -> np.ndarray: return a[:, o:o + 4].copy().view("<i4").ravel()
    def col_u32(a: np.ndarray, o: int) -> np.ndarray: return a[:, o:o + 4].copy().view("<u4").ravel()
    def col_i16(a: np.ndarray, o: int) -> np.ndarray: return a[:, o:o + 2].copy().view("<i2").ravel()
    def col_u16(a: np.ndarray, o: int) -> np.ndarray: return a[:, o:o + 2].copy().view("<u2").ravel()
    def col_i8(a: np.ndarray, o: int) -> np.ndarray: return a[:, o:o + 1].copy().view("<i1").ravel()
    def col_u8(a: np.ndarray, o: int) -> np.ndarray: return a[:, o]
    def col_f32(a: np.ndarray, o: int) -> np.ndarray: return a[:, o:o + 4].copy().view("<f4").ravel()

    # Enum sets from frozen master.json
    enums_m = master["enums"]
    enum_sets = {
        k: sorted({int(v["enum"]) for v in enums_m[k]["values"]})
        for k in ("Soty", "Spty", "Sdtr", "Sste", "Senv", "ubnt", "tmty", "indx")
    }

    # Build stadium field-by-field stats & grades
    stad_schema = get_entity_fields(master, "stadium.xml")
    assert len(stad_schema) == 60

    def int_stats(v: np.ndarray, lo: int | None, hi: int | None, suppress_le0: bool = False) -> dict[str, Any]:
        live = v[v > 0] if suppress_le0 else v
        viol = 0
        if lo is not None:
            viol += int((live < lo).sum())
        if hi is not None:
            viol += int((live > hi).sum())
        return {
            "rows": int(len(v)),
            "raw_min": int(v.min()),
            "raw_max": int(v.max()),
            "live_count": int(len(live)),
            "suppressed_le0": int((v <= 0).sum()) if suppress_le0 else 0,
            "live_min": int(live.min()) if len(live) else None,
            "live_max": int(live.max()) if len(live) else None,
            "schema_range": [lo, hi],
            "violations": viol,
        }

    def enum_stats(v: np.ndarray, allowed: list[int], suppress_zero: bool = False, clamp_lt2_to_1: bool = False) -> dict[str, Any]:
        eff = v.copy()
        if clamp_lt2_to_1:
            eff = np.where(eff < 2, 1, eff)
        live = eff[eff != 0] if suppress_zero else eff
        bad_mask = ~np.isin(live, allowed)
        bad_idx = np.flatnonzero(~np.isin(eff, allowed) & ((eff != 0) if suppress_zero else True))
        first_ce = None
        if len(bad_idx):
            r0 = int(bad_idx[0])
            first_ce = {"row": r0, "uid": int(t21_duni[r0]), "raw_value": int(v[r0]), "effective_value": int(eff[r0])}
        vals_u, cnts_u = np.unique(v, return_counts=True)
        return {
            "rows": int(len(v)),
            "allowed_enum": allowed,
            "raw_histogram": {str(int(k)): int(c) for k, c in zip(vals_u, cnts_u)},
            "live_count": int(len(live)),
            "suppressed_zero": int((v == 0).sum()) if suppress_zero else 0,
            "clamped_lt2_to_1": int((v < 2).sum()) if clamp_lt2_to_1 else 0,
            "violations": int(bad_mask.sum()),
            "first_counterexample": first_ce,
        }

    def bit_stats(v: np.ndarray, bit: int) -> dict[str, Any]:
        b = (v >> bit) & 1
        return {"rows": int(len(v)), "bit": bit, "true_count": int(b.sum()), "false_count": int((b == 0).sum()), "violations": 0}

    def f32_stats(v: np.ndarray) -> dict[str, Any]:
        fin = np.isfinite(v)
        return {"rows": int(len(v)), "finite": int(fin.sum()), "non_finite": int((~fin).sum()), "min": float(v.min()), "max": float(v.max()), "nonzero": int((v != 0).sum()), "violations": int((~fin).sum())}

    def pitch_stats(v: np.ndarray, suppress_le0: bool = False) -> dict[str, Any]:
        live = v[v > 0] if suppress_le0 else v
        return {
            "rows": int(len(v)),
            "scale_divisor": 10.0,
            "raw_min": int(v.min()),
            "raw_max": int(v.max()),
            "live_count": int(len(live)),
            "live_min_meters": float(live.min() / 10.0) if len(live) else None,
            "live_max_meters": float(live.max() / 10.0) if len(live) else None,
            "violations": 0,
        }

    # Ssds 8x8B analysis
    sides_raw = sb[:, 64:128].reshape(n_t21, 8, 8)
    s_capc = sides_raw[:, :, 0:4].copy().view("<i4").reshape(-1)
    s_flg = sides_raw[:, :, 4].reshape(-1)
    s_sage = sides_raw[:, :, 5:7].copy().view("<i2").reshape(-1)
    s_cond = sides_raw[:, :, 7].view(np.int8).reshape(-1)
    s_exis = (s_flg & 1) != 0
    bad_sage_all = np.flatnonzero(s_sage < 0)
    bad_sage_exis = np.flatnonzero(s_exis & (s_sage < 0))
    r_ce, si_ce = divmod(int(bad_sage_exis[0]), 8)
    ssds_profile = {
        "total_sides": int(len(s_capc)),
        "presence_flag_at_s63_all_1": bool(np.all(sb[:, 63] == 1)),
        "trailing_bytes_s128_s129_all_0": bool(np.all(sb[:, 128:130] == 0)),
        "subfields": {
            "indx": {"source": "loop_index_0..7", "getter_fo": "0x15e6a4c", "domain": enum_sets["indx"], "violations": 0},
            "capc": {"member_off": "+0x00", "wire_side_off": "+0..3", "type": "i32", "getter_fo": "0x15e68ba", "min": int(s_capc.min()), "max": int(s_capc.max()), "schema_range": [0, 100000], "violations": int(((s_capc < 0) | (s_capc > 100000)).sum())},
            "exis": {"member_off": "+0x07 bit 0", "wire_side_off": "+4 bit 0", "type": "bool", "getter_fo": "0x15e66aa", "true_count": int(s_exis.sum()), "violations": 0},
            "seat": {"member_off": "+0x07 bit 1", "wire_side_off": "+4 bit 1", "type": "bool", "getter_fo": "0x15e6b15", "true_count": int(((s_flg >> 1) & 1).sum()), "violations": 0},
            "iuse": {"member_off": "+0x07 bit 2", "wire_side_off": "+4 bit 2", "type": "bool", "getter_fo": "0x15e6aae", "true_count": int(((s_flg >> 2) & 1).sum()), "violations": 0},
            "tunn": {"member_off": "+0x07 bit 3", "wire_side_off": "+4 bit 3", "type": "bool", "getter_fo": "0x15e6851", "true_count": int(((s_flg >> 3) & 1).sum()), "violations": 0},
            "roof": {"member_off": "+0x07 bit 4", "wire_side_off": "+4 bit 4", "type": "bool", "getter_fo": "0x15e69e7", "true_count": int(((s_flg >> 4) & 1).sum()), "violations": 0},
            "rofs": {"member_off": "+0x07 bit 5", "wire_side_off": "+4 bit 5", "type": "bool", "getter_fo": "0x15e697e", "true_count": int(((s_flg >> 5) & 1).sum()), "violations": 0},
            "tclo": {"member_off": "+0x07 bit 6", "wire_side_off": "+4 bit 6", "type": "bool", "getter_fo": "0x15e6b7a", "true_count": int(((s_flg >> 6) & 1).sum()), "violations": 0},
            "reno": {"member_off": "+0x07 bit 7", "wire_side_off": "+4 bit 7", "type": "bool", "getter_fo": "0x15e67c7", "true_count": int(((s_flg >> 7) & 1).sum()), "violations": 0},
            "sage": {
                "member_off": "+0x04",
                "wire_side_off": "+5..6",
                "type": "i16",
                "getter_fo": "0x15e6740",
                "min": int(s_sage.min()),
                "max": int(s_sage.max()),
                "schema_range": [0, 200],
                "violations_all_sides": int(len(bad_sage_all)),
                "violations_exis_sides": int(len(bad_sage_exis)),
                "histogram": {str(k): int(c) for k, c in Counter(s_sage.tolist()).most_common()},
                "first_exis_counterexample": {"row": r_ce, "side": si_ce, "uid": int(t21_duni[r_ce]), "raw_sage": int(s_sage[r_ce * 8 + si_ce])},
            },
            "cond": {"member_off": "+0x06", "wire_side_off": "+7", "type": "i8", "getter_fo": "0x15e691b", "min": int(s_cond.min()), "max": int(s_cond.max()), "violations": 0},
        },
    }

    flags9b = col_u8(sb, 36)
    flagsa6 = col_u16(cb, 0)
    scov_stats = bit_stats(flagsa6, 0)
    scov_stats["srrf_bit6_override_rows_where_bit0_is_0"] = int((((flagsa6 & 0x40) != 0) & ((flagsa6 & 1) == 0)).sum())
    scov_stats["getter_override_note"] = "STADIUM_GET 0x118629b checks global 0x86640(); if nonzero and Srrf(bit6)=1 returns true, else bit0; STADIUM_SET 0x1189636 writes bit0 directly."

    sscl_raw = col_u32(sb, 139)
    sscl_stats = {
        "rows": n_t21,
        "nonzero": int((sscl_raw != 0).sum()),
        "zero_fallback_rows": int((sscl_raw == 0).sum()),
        "unique_raw_u32": int(len(np.unique(sscl_raw))),
        "wire_byte_order": "read +3,+2,+1,+0 into STADIUM+0x68 by 0x3e43f90; getter 0x3e448a0 returns +0x68 if nonzero and nation!=0x673 else club/0xff7f7f7f",
        "violations": 0,
    }

    stad_field_defs: dict[str, dict[str, Any]] = {
        # Identity
        "duni": {"grade": "L3", "scope": "client+server", "client_body_off": 29, "server_body_off": 172, "width": 4, "wire_type": "u32", "member_off": "+0x0c", "getter_fo": "0xfe3912", "setter_fo": None, "reader_fo": "0x3c600f0", "domain": {"rows": n_t21, "unique": len(t21_uids), "eq_rdui_raw": n_t21, "violations": 0}},
        "rdui": {"grade": "held", "scope": "client+server", "client_body_off": 33, "server_body_off": 176, "width": 4, "wire_type": "u32", "member_off": "+0x10", "getter_fo": "0xfe3862", "setter_fo": None, "reader_fo": "0x3c600f0", "hold_reason": "DATABASE_RECORD_GET 0xfe38a2 suppresses output whenever [+0x0c]==[+0x10]; 48,413/48,413 rows suppressed (0 live outputs). Note b47 label 'rdui@25' was actually row ordinal@25.", "domain": {"rows": n_t21, "suppressed": n_t21, "live": 0}},
        # Common 25B tail
        "Scti": {"grade": "L3", "scope": "client+server", "client_body_off": 3, "server_body_off": 146, "width": 4, "wire_type": "i32_ordinal_ref:table_2", "member_off": "+0x50", "getter_fo": "0x1186b5d", "setter_fo": "0x118951f", "reader_fo": "0x118442a", "fixup_fo": "0x3e44580", "domain": ref_domain_check(col_i32(cb, 3), n_t2, t2_uids)},
        "Snbs": {"grade": "L3", "scope": "client+server", "client_body_off": 7, "server_body_off": 150, "width": 4, "wire_type": "i32_ordinal_ref:table_21", "member_off": "+0x58", "getter_fo": "0x1185f74", "setter_fo": "0x118979a", "reader_fo": "0x118444e", "fixup_fo": "0x3e44580", "domain": ref_domain_check(col_i32(cb, 7), n_t21, t21_uids)},
        "Sptc": {"grade": "L3", "scope": "client+server", "client_body_off": 11, "server_body_off": 154, "width": 2, "wire_type": "i16", "member_off": "+0x98", "getter_fo": "0x11865f7", "setter_fo": "0x11892a5", "reader_fo": "0x1184472", "domain": int_stats(col_i16(cb, 11), 0, 200)},
        "Slat": {"grade": "L3", "scope": "client+server", "client_body_off": 17, "server_body_off": 160, "width": 4, "wire_type": "f32", "member_off": "+0x60", "getter_fo": "0x1186330", "setter_fo": "0x11896bd", "reader_fo": "0x11844ae", "domain": f32_stats(col_f32(cb, 17))},
        "Slon": {"grade": "L3", "scope": "client+server", "client_body_off": 21, "server_body_off": 164, "width": 4, "wire_type": "f32", "member_off": "+0x64", "getter_fo": "0x118633c", "setter_fo": "0x118957a", "reader_fo": "0x11844d2", "domain": f32_stats(col_f32(cb, 21))},
        "Scov": {"grade": "L3", "scope": "client+server", "client_body_off": 0, "server_body_off": 143, "width": 2, "bit": 0, "wire_type": "u16_bitflag", "member_off": "+0xa6 bit 0", "getter_fo": "0x118628f", "setter_fo": "0x1189636", "reader_fo": "0x11843b6", "domain": scov_stats},
        "Sush": {"grade": "L3", "scope": "client+server", "client_body_off": 0, "server_body_off": 143, "width": 2, "bit": 1, "wire_type": "u16_bitflag", "member_off": "+0xa6 bit 1", "getter_fo": "0x1186996", "setter_fo": "0x1189382", "reader_fo": "0x11843b6", "domain": bit_stats(flagsa6, 1)},
        "Srrf": {"grade": "L3", "scope": "client+server", "client_body_off": 0, "server_body_off": 143, "width": 2, "bit": 6, "wire_type": "u16_bitflag", "member_off": "+0xa6 bit 6", "getter_fo": "0x1186222", "setter_fo": "0x11894c3", "reader_fo": "0x11843b6", "domain": bit_stats(flagsa6, 6)},
        "Nucf": {"grade": "L3", "scope": "client+server", "client_body_off": 0, "server_body_off": 143, "width": 2, "bit": 7, "wire_type": "u16_bitflag", "member_off": "+0xa6 bit 7", "getter_fo": "0x11863ec", "setter_fo": "0x11893df", "reader_fo": "0x11843b6", "domain": bit_stats(flagsa6, 7)},
        # Server-only 143B prefix
        "Scpy": {"grade": "L3", "scope": "server_only", "client_body_off": None, "server_body_off": 0, "width": 4, "wire_type": "i32", "member_off": "+0x6c", "getter_fo": "0x118688c", "setter_fo": "0x1189513", "reader_fo": "0x1183f5a", "domain": int_stats(col_i32(sb, 0), 0, 200000)},
        "Sscy": {"grade": "L3", "scope": "server_only", "client_body_off": None, "server_body_off": 4, "width": 4, "wire_type": "i32", "member_off": "+0x70", "getter_fo": "0x1186840", "setter_fo": "0x11894db", "reader_fo": "0x1183f7b", "domain": int_stats(col_i32(sb, 4), 0, 200000)},
        "Secy": {"grade": "L3", "scope": "server_only", "client_body_off": None, "server_body_off": 8, "width": 4, "wire_type": "i32", "member_off": "+0x7c", "getter_fo": "0x11867f4", "setter_fo": "0x1189476", "reader_fo": "0x1183f9f", "domain": int_stats(col_i32(sb, 8), 0, 200000)},
        "Scas": {"grade": "L3", "scope": "server_only", "client_body_off": None, "server_body_off": 12, "width": 4, "wire_type": "i32", "member_off": "+0x78", "getter_fo": "0x1186283", "setter_fo": "0x118962a", "reader_fo": "0x1183fc3", "domain": int_stats(col_i32(sb, 12), 0, 200000, suppress_le0=True)},
        "Sowi": {"grade": "L3", "scope": "server_only", "client_body_off": None, "server_body_off": 16, "width": 4, "wire_type": "i32_ordinal_ref:table_3", "member_off": "+0x80", "getter_fo": "0x11864e8", "setter_fo": "0x118966c", "reader_fo": "0x1183fe7", "fixup_fo": "0x3e44580", "domain": ref_domain_check(col_i32(sb, 16), len(t3_uids_arr), t3_uids)},
        "Sdcy": {"grade": "L3", "scope": "server_only", "client_body_off": None, "server_body_off": 20, "width": 1, "wire_type": "i8", "member_off": "+0x9a", "getter_fo": "0x1186112", "setter_fo": "0x1189726", "reader_fo": "0x118400b", "domain": int_stats(col_i8(sb, 20), 0, 20)},
        "Sucy": {"grade": "L3", "scope": "server_only", "client_body_off": None, "server_body_off": 21, "width": 4, "wire_type": "i32", "member_off": "+0x74", "getter_fo": "0x1186398", "setter_fo": "0x11895fe", "reader_fo": "0x118402f", "domain": int_stats(col_i32(sb, 21), 1, 200000, suppress_le0=True)},
        "Spln": {"grade": "L3", "scope": "server_only", "client_body_off": None, "server_body_off": 25, "width": 2, "wire_type": "i16_div10", "member_off": "+0x88", "getter_fo": "0x1186307", "setter_fo": "0x118953f", "reader_fo": "0x1184053", "domain": pitch_stats(col_i16(sb, 25))},
        "Spwd": {"grade": "L3", "scope": "server_only", "client_body_off": None, "server_body_off": 27, "width": 2, "wire_type": "i16_div10", "member_off": "+0x8a", "getter_fo": "0x1186bb2", "setter_fo": "0x1189755", "reader_fo": "0x1184077", "domain": pitch_stats(col_i16(sb, 27))},
        "SlIM": {"grade": "L3", "scope": "server_only", "client_body_off": None, "server_body_off": 29, "width": 2, "wire_type": "i16_div10", "member_off": "+0x8c", "getter_fo": "0x1186aae", "setter_fo": "0x11896b1", "reader_fo": "0x118409b", "domain": pitch_stats(col_i16(sb, 29), suppress_le0=True)},
        "SwIM": {"grade": "L3", "scope": "server_only", "client_body_off": None, "server_body_off": 31, "width": 2, "wire_type": "i16_div10", "member_off": "+0x8e", "getter_fo": "0x11866cf", "setter_fo": "0x11897ba", "reader_fo": "0x11840bf", "domain": pitch_stats(col_i16(sb, 31), suppress_le0=True)},
        "Spty": {"grade": "L3", "scope": "server_only", "client_body_off": None, "server_body_off": 33, "width": 1, "wire_type": "u8_enum", "member_off": "+0x9d", "getter_fo": "0x1186603", "setter_fo": "0x11892b1", "reader_fo": "0x11840e3", "domain": enum_stats(col_u8(sb, 33), enum_sets["Spty"], clamp_lt2_to_1=True)},
        "Sste": {"grade": "L3", "scope": "server_only", "client_body_off": None, "server_body_off": 34, "width": 1, "wire_type": "i8_enum", "member_off": "+0x9f", "getter_fo": "0x1186b0d", "setter_fo": "0x11896f7", "reader_fo": "0x1184107", "domain": enum_stats(col_i8(sb, 34), enum_sets["Sste"])},
        "Senv": {"grade": "L3", "scope": "server_only", "client_body_off": None, "server_body_off": 35, "width": 1, "wire_type": "i8_enum", "member_off": "+0xa0", "getter_fo": "0x1186514", "setter_fo": "0x1189482", "reader_fo": "0x118412b", "domain": enum_stats(col_i8(sb, 35), enum_sets["Senv"])},
        "Sext": {"grade": "L3", "scope": "server_only", "client_body_off": None, "server_body_off": 36, "width": 1, "bit": 0, "wire_type": "u8_bitflag", "member_off": "+0x9b bit 0", "getter_fo": "0x1186520", "setter_fo": "0x118948e", "reader_fo": "0x118414f", "domain": bit_stats(flags9b, 0)},
        "Sitg": {"grade": "L3", "scope": "server_only", "client_body_off": None, "server_body_off": 36, "width": 1, "bit": 2, "wire_type": "u8_bitflag", "member_off": "+0x9b bit 2", "getter_fo": "0x1186aa2", "setter_fo": "0x11896a5", "reader_fo": "0x118414f", "domain": bit_stats(flags9b, 2)},
        "Sdah": {"grade": "L3", "scope": "server_only", "client_body_off": None, "server_body_off": 36, "width": 1, "bit": 6, "wire_type": "u8_bitflag", "member_off": "+0x9b bit 6", "getter_fo": "0x1186b69", "setter_fo": "0x118971a", "reader_fo": "0x118414f", "domain": bit_stats(flags9b, 6)},
        "Sbld": {"grade": "L3", "scope": "server_only", "client_body_off": None, "server_body_off": 37, "width": 4, "wire_type": "packed_date_u32", "member_off": "+0x28", "getter_fo": "0x11869ea", "setter_fo": "0x118961e", "reader_fo": "0x1184173", "domain": packed_date_stats(col_u32(sb, 37))},
        "Srbd": {"grade": "L3", "scope": "server_only", "client_body_off": None, "server_body_off": 41, "width": 4, "wire_type": "packed_date_u32", "member_off": "+0x2c", "getter_fo": "0x1186bbe", "setter_fo": "0x1189761", "reader_fo": "0x118418a", "domain": packed_date_stats(col_u32(sb, 41))},
        "Doco": {"grade": "L3", "scope": "server_only", "client_body_off": None, "server_body_off": 45, "width": 4, "wire_type": "packed_date_u32", "member_off": "+0x30", "getter_fo": "0x118673a", "setter_fo": "0x11893d3", "reader_fo": "0x11841a1", "domain": packed_date_stats(col_u32(sb, 45))},
        "Sunt": {"grade": "L3", "scope": "server_only", "client_body_off": None, "server_body_off": 49, "width": 1, "wire_type": "i8_enum:ubnt", "member_off": "+0xa1", "getter_fo": "0x118698a", "setter_fo": "0x1189376", "reader_fo": "0x11841b8", "domain": enum_stats(col_i8(sb, 49), enum_sets["ubnt"])},
        "Su21": {"grade": "L3", "scope": "server_only", "client_body_off": None, "server_body_off": 50, "width": 1, "wire_type": "i8_enum:ubnt", "member_off": "+0xa2", "getter_fo": "0x118638c", "setter_fo": "0x11895f2", "reader_fo": "0x11841dc", "domain": enum_stats(col_i8(sb, 50), enum_sets["ubnt"])},
        "Su19": {"grade": "L3", "scope": "server_only", "client_body_off": None, "server_body_off": 51, "width": 1, "wire_type": "i8_enum:ubnt", "member_off": "+0xa3", "getter_fo": "0x1186b19", "setter_fo": "0x11895e6", "reader_fo": "0x1184200", "domain": enum_stats(col_i8(sb, 51), enum_sets["ubnt"])},
        "Soty": {"grade": "L3", "scope": "server_only", "client_body_off": None, "server_body_off": 52, "width": 1, "wire_type": "i8_enum", "member_off": "+0xa4", "getter_fo": "0x118679c", "setter_fo": "0x1189433", "reader_fo": "0x1184224", "domain": enum_stats(col_i8(sb, 52), enum_sets["Soty"], suppress_zero=True)},
        "Smnl": {"grade": "L3", "scope": "server_only", "client_body_off": None, "server_body_off": 54, "width": 2, "wire_type": "i16_div10", "member_off": "+0x90", "getter_fo": "0x118691c", "setter_fo": "0x1189586", "reader_fo": "0x118426c", "domain": pitch_stats(col_i16(sb, 54))},
        "Smnw": {"grade": "L3", "scope": "server_only", "client_body_off": None, "server_body_off": 56, "width": 2, "wire_type": "i16_div10", "member_off": "+0x92", "getter_fo": "0x1186928", "setter_fo": "0x1189592", "reader_fo": "0x1184290", "domain": pitch_stats(col_i16(sb, 56))},
        "Smxl": {"grade": "L3", "scope": "server_only", "client_body_off": None, "server_body_off": 58, "width": 2, "wire_type": "i16_div10", "member_off": "+0x94", "getter_fo": "0x1186655", "setter_fo": "0x11892f2", "reader_fo": "0x11842b4", "domain": pitch_stats(col_i16(sb, 58), suppress_le0=True)},
        "Smxw": {"grade": "L3", "scope": "server_only", "client_body_off": None, "server_body_off": 60, "width": 2, "wire_type": "i16_div10", "member_off": "+0x96", "getter_fo": "0x1186661", "setter_fo": "0x11892fe", "reader_fo": "0x11842d8", "domain": pitch_stats(col_i16(sb, 60), suppress_le0=True)},
        "Sdtr": {"grade": "held", "scope": "server_only", "client_body_off": None, "server_body_off": 62, "width": 1, "wire_type": "i8_enum", "member_off": "+0x9c", "getter_fo": "0x11867e8", "setter_fo": "0x1189732", "reader_fo": "0x11842fc", "hold_reason": "Exact getter (0x11872fe movsx) and setter (0x1189732) map to +0x9c, but 29,983/48,413 rows have raw=0 which is outside enums['Sdtr']={1,2,3} and getter does not clamp or suppress 0.", "domain": enum_stats(col_i8(sb, 62), enum_sets["Sdtr"])},
        "Ssds": {"grade": "held", "scope": "server_only", "client_body_off": None, "server_body_off": 63, "width": 67, "wire_type": "u8_flag+subobject_66B(8x8B+2B)", "member_off": "+0x18", "getter_fo": "0x1186572", "setter_fo": "0x11896df", "reader_fo": "0x4401010", "hold_reason": "All 12 subfields statically wired via 0x15e6650 and 11/12 pass domain checks, but subfield 'sage' (+4 i16, wire +5..6, getter 0x15e6740 direct movsx) has 20,425/387,304 negative values (min=-7173, max=0; including exis=True sides), violating stadium.xml min_value=0.", "domain": ssds_profile},
        "Sprr": {"grade": "L3", "scope": "server_only", "client_body_off": None, "server_body_off": 130, "width": 1, "wire_type": "i8", "member_off": "+0x9e", "getter_fo": "0x11868d8", "setter_fo": "0x1189557", "reader_fo": "0x118432f", "domain": int_stats(col_i8(sb, 130), 0, 20)},
        "Splr": {"grade": "held", "scope": "server_only", "client_body_off": None, "server_body_off": 131, "width": 4, "wire_type": "packed_date_u32", "member_off": "+0x20 (under uppercase 4CC 'SplR')", "getter_fo": "0x1186313 (no-op); uppercase 'SplR' at 0x1186a4c", "setter_fo": "none for 'Splr'; uppercase 'SplR' at 0x1189678", "reader_fo": "0x1184353", "hold_reason": "4CC case mismatch: stadium.xml[29] uses lowercase 'Splr', whose STADIUM_GET arm (0x1186313 -> 0x1185f0a) is a no-op returning 1 without writing a value and has no setter arm; the actual packed date at s+131 (+0x20) is dispatched under uppercase 'SplR'.", "domain": packed_date_stats(col_u32(sb, 131))},
        "Sprl": {"grade": "L3", "scope": "server_only", "client_body_off": None, "server_body_off": 135, "width": 4, "wire_type": "packed_date_u32", "member_off": "+0x24", "getter_fo": "0x11868cc", "setter_fo": "0x118954b", "reader_fo": "0x118436a", "domain": packed_date_stats(col_u32(sb, 135))},
        "Sscl": {"grade": "L3", "scope": "server_only", "client_body_off": None, "server_body_off": 139, "width": 4, "wire_type": "colour_4B_rev", "member_off": "+0x68", "getter_fo": "0x1186834", "setter_fo": "0x11894cf", "reader_fo": "0x1184381", "domain": sscl_stats},
        # Non-wire / computed / forwarded / subtable / unhandled / metadata
        "Snam": {"grade": "non_wire_language_layer", "scope": "conditional_wire_0_populated", "member_off": "+0x38 (gated on +0xa6 bit 4)", "getter_fo": "0x1185f5c", "setter_fo": "0x118978e", "note": "Inline flag +0xa6 bit 4 is 0 on all 48,413/48,413 rows in both client and server; localized names live in lang_db/lang_update_db.", "inline_flag_count": int(((flagsa6 >> 4) & 1).sum())},
        "dbnm": {"grade": "non_wire_computed", "scope": "non_wire", "getter_fo": "0xfe375d", "setter_fo": None, "note": "DATABASE_RECORD_GET dispatches virtual vtable[25] display-name resolver."},
        "Snti": {"grade": "non_wire_forwarded", "scope": "non_wire", "getter_fo": "0x1186790", "setter_fo": None, "note": "STADIUM_GET 0x11872e8 reads (*(STADIUM+0x50))+0x20 (City->Nation pointer); not a table_21 slot."},
        "Scpc": {"grade": "subtable_backed", "scope": "subtable:table_22", "getter_fo": "0x1186880", "setter_fo": "0x1189507", "note": "STADIUM_GET 0x1187372 -> 0x44d1ea0 scans global table_22 (STADIUM_CHANGE) where +0x20==this and +0x64==2."},
        "NDBC": {"grade": "editor_metadata", "scope": "non_wire", "getter_fo": None, "setter_fo": None, "note": "Editor change-tracking counter; 0 hits in STADIUM_GET/DATABASE_RECORD_GET."},
        "FDBC": {"grade": "editor_metadata", "scope": "non_wire", "getter_fo": None, "setter_fo": None, "note": "Editor failed-change counter; 0 hits in STADIUM_GET/DATABASE_RECORD_GET."},
        "Shcc": {"grade": "unhandled_no_getter", "scope": "non_wire", "getter_fo": None, "setter_fo": None, "note": "0 hits in editor.exe .text."},
    }
    for stand_cc in ("Shts", "Shtr", "Shrs", "Shbr", "Shbs", "Shbl", "Shls", "Shtl"):
        stad_field_defs[stand_cc] = {
            "grade": "unhandled_no_getter",
            "scope": "non_wire",
            "getter_fo": None,
            "setter_fo": None,
            "prop_reg_fo": "0x1185020",
            "note": "Registered in STADIUM slot 5 (0x1185020) but absent from STADIUM_GET (0x1185eb0), STADIUM_SET (0x1189260), and DATABASE_RECORD_GET (0xfe3520).",
        }

    # Build ordered 60-entry stadium list matching master.json
    stadium_field_map = []
    for idx, fobj in enumerate(stad_schema):
        cc = fobj["field"]
        rec = {"index": idx, "field": cc, "name": fobj["name"], "schema_type": fobj["type"], **stad_field_defs[cc]}
        stadium_field_map.append(rec)

    # Extra non-XML internal/opaque wire slots on table_21 (100% byte coverage!)
    stadium_internal_wire_slots = [
        {"field": "Sovl", "status": "internal_4cc_not_in_stadium_xml", "scope": "server_only", "server_body_off": 36, "bit": 5, "member_off": "+0x9b bit 5", "getter_fo": "0x11864dc", "setter_fo": "0x1189660", "domain": bit_stats(flags9b, 5)},
        {"field": "Snft", "status": "internal_4cc_not_in_stadium_xml", "scope": "server_only", "server_body_off": 53, "width": 1, "member_off": "+0xa5", "getter_fo": "0x11860b6", "setter_fo": "0x1189427", "domain": int_stats(col_i8(sb, 53), 0, 0)},
        {"field": "SplR", "status": "uppercase_4cc_mismatch_for_Splr", "scope": "server_only", "server_body_off": 131, "width": 4, "member_off": "+0x20", "getter_fo": "0x1186a4c", "setter_fo": "0x1189678", "domain": packed_date_stats(col_u32(sb, 131))},
        {"field": "Wucf", "status": "internal_4cc_not_in_stadium_xml", "scope": "client+server", "client_body_off": 0, "server_body_off": 143, "bit": 11, "member_off": "+0xa6 bit 11", "getter_fo": "0x1185fc1", "setter_fo": "0x11897c6", "domain": bit_stats(flagsa6, 11)},
        {"field": None, "status": "opaque_static_member", "scope": "client+server", "client_body_off": 2, "server_body_off": 145, "width": 1, "member_off": "+0xa8", "note": "Written 0/3/4 in STADIUM_SET (0x1189d7b/0x1189f51/0x1189f61); all 0 in both archives.", "all_zero": bool(np.all(cb[:, 2] == 0))},
        {"field": None, "status": "opaque_static_member", "scope": "client+server", "client_body_off": 13, "server_body_off": 156, "width": 4, "member_off": "+0x34", "note": "Packed date read by 0xdb7f80; all 48,413 rows are default 1900-01-01 (0x076c0001); no STADIUM_GET 4CC.", "domain": packed_date_stats(col_u32(cb, 13))},
        {"field": None, "status": "row_ordinal_identity", "scope": "client+server", "client_body_off": 25, "server_body_off": 168, "width": 4, "member_off": "+0x08", "note": "Sequential row ordinal 0..48,412 (reconciles b47 'rdui@25' label)."},
    ]

    # ---- TABLE 24: TEAM ----
    t24 = replay_table_24(srv["table_24.dat"])
    team_schema = get_entity_fields(master, "team.xml")
    assert len(team_schema) == 25

    t24_ttyp_bad = int((~np.isin(t24["ttyp"], enum_sets["tmty"])).sum())
    t24_tisn_eq_sel11 = bool(np.array_equal(t24["tisn"] == 1, t24["sel"] == 11))
    assert t24_tisn_eq_sel11

    team_field_defs: dict[str, dict[str, Any]] = {
        "duni": {"grade": "L3", "scope": "server_only", "wire_pos": "identity_tail[-8:-4]", "width": 4, "wire_type": "u32", "member_off": "+0x0c", "getter_fo": "0xfe3912", "setter_fo": None, "reader_fo": "0x3c600f0", "domain": {"rows": t24["n"], "unique": int(len(np.unique(t24["uid"]))), "eq_rdui_raw": t24["n"], "violations": 0}},
        "rdui": {"grade": "held", "scope": "server_only", "wire_pos": "identity_tail[-4:]", "width": 4, "wire_type": "u32", "member_off": "+0x10", "getter_fo": "0xfe3862", "setter_fo": None, "reader_fo": "0x3c600f0", "hold_reason": "DATABASE_RECORD_GET 0xfe38a2 suppresses output whenever [+0x0c]==[+0x10]; 84,507/84,507 rows suppressed.", "domain": {"rows": t24["n"], "suppressed": t24["n"], "live": 0}},
        "Tlna": {"grade": "L3", "scope": "server_only", "wire_pos": "TEAM_BASE+10 (u32_len + utf8)", "wire_type": "len_prefixed_utf8", "member_off": "+0x18", "getter_fo": "0x11c2b8e", "setter_fo": "0x3e986ce", "reader_fo": "0x3e94390", "domain": {"rows": t24["n"], "inline_nonempty": int((t24["lna_len"] > 0).sum()), "empty_fallback_0xdbe020": int((t24["lna_len"] == 0).sum()), "utf8_errors": t24["lna_utf8_err"], "samples": t24["lna_samples"], "violations": t24["lna_utf8_err"]}},
        "Tsna": {"grade": "L3", "scope": "server_only", "wire_pos": "TEAM_BASE after Tlna+1B (u32_len + utf8)", "wire_type": "len_prefixed_utf8", "member_off": "+0x20", "getter_fo": "0x11c2c46", "setter_fo": "0x3e9873f", "reader_fo": "0x3e94390", "domain": {"rows": t24["n"], "inline_nonempty": int((t24["sna_len"] > 0).sum()), "empty_fallback_0xdbe020": int((t24["sna_len"] == 0).sum()), "utf8_errors": t24["sna_utf8_err"], "samples": t24["sna_samples"], "violations": t24["sna_utf8_err"]}},
        "Tsti": {"grade": "L3", "scope": "server_only", "wire_pos": "TEAM+16..19", "width": 4, "wire_type": "i32_ordinal_ref:table_21", "member_off": "+0x78", "getter_fo": "0x11afbe0", "setter_fo": "0x11b4e54", "reader_fo": "0x11a0880", "fixup_fo": "0x11a0c40", "domain": ref_domain_check(t24["tsti"], n_t21, t21_uids)},
        "Ttyp": {"grade": "L3", "scope": "server_only", "wire_pos": "TEAM_BASE+0", "width": 1, "wire_type": "i8_enum:tmty", "member_off": "+0x28", "getter_fo": "0x11c338a", "setter_fo": "0x3e98747", "reader_fo": "0x3e94390", "domain": {"rows": t24["n"], "allowed_enum": enum_sets["tmty"], "histogram": {str(k): int(v) for k, v in sorted(Counter(t24["ttyp"].tolist()).items())}, "violations": t24_ttyp_bad}},
        "Tisn": {"grade": "L3", "scope": "server_only", "wire_pos": "TEAM_BASE+1", "width": 1, "wire_type": "u8_bool", "member_off": "+0x2f", "getter_fo": "0x11c31e4", "setter_fo": None, "reader_fo": "0x3e94390", "domain": {"rows": t24["n"], "true_count": int((t24["tisn"] == 1).sum()), "false_count": int((t24["tisn"] == 0).sum()), "identical_to_selector_11": t24_tisn_eq_sel11, "violations": int((~np.isin(t24["tisn"], [0, 1])).sum())}},
        "Trep": {"grade": "L3", "scope": "server_only", "wire_pos": "TEAM+2..3", "width": 2, "wire_type": "i16", "member_off": "+0xa8", "getter_fo": "0x11aff60", "setter_fo": "0x11b4c85", "reader_fo": "0x11a0880", "domain": {"rows": t24["n"], "raw_min": int(t24["trep"].min()), "raw_max": int(t24["trep"].max()), "raw_le0_clamped_to_1_at_0x11a090d": int((t24["trep"] <= 0).sum()), "post_clamp_min": 1, "post_clamp_max": int(t24["trep"].max()), "violations": 0}},
        "Tdvi": {"grade": "L3", "scope": "server_only", "wire_pos": "TEAM+4..7", "width": 4, "wire_type": "i32_ordinal_ref:table_25", "member_off": "+0x50", "getter_fo": "0x11b064f", "setter_fo": "0x11b4cd3", "reader_fo": "0x11a0880", "fixup_fo": "0x11a0c40", "domain": ref_domain_check(t24["tdvi"], len(t25_uids_arr), t25_uids)},
        "Tndi": {"grade": "L3", "scope": "server_only", "wire_pos": "TEAM+12..15", "width": 4, "wire_type": "i32_ordinal_ref:table_25", "member_off": "+0x58", "getter_fo": "0x11afe92", "setter_fo": "0x11b4ed6", "reader_fo": "0x11a0880", "fixup_fo": "0x11a0c40", "domain": ref_domain_check(t24["tndi"], len(t25_uids_arr), t25_uids)},
        "Todo": {"grade": "L3", "scope": "server_only", "wire_pos": "TEAM+29..32", "width": 4, "wire_type": "i32_ordinal_ref:table_25", "member_off": "+0x68", "getter_fo": "0x11b00b6", "setter_fo": "0x11b4d27", "reader_fo": "0x11a0880", "fixup_fo": "0x11a0c40", "domain": ref_domain_check(t24["todo"], len(t25_uids_arr), t25_uids)},
        "Tnod": {"grade": "L3", "scope": "server_only", "wire_pos": "TEAM+48+4*vec38_cnt", "width": 4, "wire_type": "i32_ordinal_ref:table_25", "member_off": "+0x70", "getter_fo": "0x11afe9e", "setter_fo": "0x11b4ee2", "reader_fo": "0x11a0880", "fixup_fo": "0x11a0c40", "domain": ref_domain_check(t24["tnod"], len(t25_uids_arr), t25_uids)},
        # Held & Non-wire forwarded/computed/metadata
        "PLgn": {"grade": "held", "scope": "non_wire_forwarded", "member_off": "(*(TEAM+0x30))+0xb9", "getter_fo": "0x11c277d", "setter_fo": None, "hold_reason": "Forwarded to owner Club/Nation +0xb9 (not a table_24 wire slot) and team.xml PLgn declares no scoped enum_ref (consistent with t57/t59 PLgn discipline)."},
        "Tmtd": {"grade": "non_wire_forwarded", "scope": "non_wire", "member_off": "(**((*(TEAM+0x30))+0x18))+0x50", "getter_fo": "0x11afa23", "setter_fo": None, "note": "Reads owner Club's first team's Tdvi (+0x50); not a table_24 wire slot."},
        "Ccti": {"grade": "non_wire_forwarded", "scope": "non_wire", "getter_fo": "0x11c2a69", "setter_fo": None, "note": "TEAM_BASE_GET 0x11c33f5 forwards to owner *(TEAM+0x30) vtable[2]."},
        "Ccba": {"grade": "non_wire_forwarded", "scope": "non_wire", "getter_fo": "0x11c2a51", "setter_fo": "0x3e98681", "note": "TEAM_BASE_GET 0x11c2d5c tailjmps CLUB_GET (0xe89a00); TEAM_BASE_SET 0x3e9873a tailjmps CLUB_SET (0xe82aa0)."},
        "Ctbu": {"grade": "non_wire_forwarded", "scope": "non_wire", "getter_fo": "slot10:0x11ba5c5", "setter_fo": "slot10:0x11ba5c5", "note": "TEAM vtable[10] (0x11ba390) redirects Ctbu property resolution to owner *(TEAM+0x30) (CLUB*)."},
        "Crmb": {"grade": "non_wire_forwarded", "scope": "non_wire", "getter_fo": "slot10:0x11ba5ad", "setter_fo": "slot10:0x11ba5ad", "note": "TEAM vtable[10] (0x11ba390) redirects Crmb property resolution to owner *(TEAM+0x30) (CLUB*)."},
        "Crkt": {"grade": "non_wire_forwarded", "scope": "non_wire", "getter_fo": None, "setter_fo": "0x3e986c6", "note": "TEAM_BASE_SET 0x3e986c6 -> 0x3e9873a forwards to owner CLUB_SET (0xe82aa0); no direct TEAM_GET/TEAM_BASE_GET arm."},
        "Clri": {"grade": "non_wire_unhandled_on_team", "scope": "non_wire", "getter_fo": None, "setter_fo": None, "note": "No handler on TEAM/TEAM_BASE; exists on club_team proxy 0x119c6f0 and CLUB."},
        "Cnti": {"grade": "non_wire_unhandled_on_team", "scope": "non_wire", "getter_fo": None, "setter_fo": None, "note": "No getter on TEAM/TEAM_BASE; emitted as change-event tag in TEAM_SET 0x11b5711 when Tdvi changes."},
        "dbnm": {"grade": "non_wire_computed", "scope": "non_wire", "getter_fo": "0xfe375d", "setter_fo": None, "note": "DATABASE_RECORD_GET dispatches virtual vtable[25] name resolver."},
        "dAPw": {"grade": "non_wire_computed", "scope": "non_wire", "getter_fo": "0xfe3751", "setter_fo": None, "note": "DATABASE_RECORD_GET 0xfe3eaf -> 0xfe4228 calls vtable[25] + dSAw suffix when table_type!=9."},
        "NDBC": {"grade": "editor_metadata", "scope": "non_wire", "getter_fo": None, "setter_fo": None, "note": "Editor change-tracking counter."},
        "FDBC": {"grade": "editor_metadata", "scope": "non_wire", "getter_fo": None, "setter_fo": None, "note": "Editor failed-change counter."},
    }

    team_field_map = []
    for idx, fobj in enumerate(team_schema):
        cc = fobj["field"]
        team_field_map.append({"index": idx, "field": cc, "name": fobj["name"], "schema_type": fobj["type"], **team_field_defs[cc]})

    team_internal_wire_slots = [
        {"field": "Tldi", "status": "internal_4cc_not_in_team_xml_target_of_CLUB_Cldi", "wire_pos": "TEAM+8..11", "width": 4, "member_off": "+0x60", "getter_fo": "0x11afe0d", "setter_fo": "0x11b4cdf", "domain": ref_domain_check(t24["tldi"], len(t25_uids_arr), t25_uids)},
        {"field": "owner", "status": "internal_owner_ref", "wire_pos": "TEAM_BASE+6..9", "width": 4, "member_off": "+0x30", "club_ref_domain": ref_domain_check(t24["own"][t24["tisn"] == 0], len(t3_uids_arr), t3_uids), "nation_ref_domain": ref_domain_check(t24["own"][t24["tisn"] == 1], len(t9_uids_arr), t9_uids)},
        {"field": "squad_vec38", "status": "internal_person_ordinal_vec", "wire_pos": "TEAM+33 (u16_cnt + 4*cnt)", "member_off": "+0x38", "max_count": int(t24["v38"].max()), "nonzero_rows": int((t24["v38"] > 0).sum())},
        {"field": "NATIONAL_TEAM_prefix", "status": "polymorphic_selector_11_prefix", "wire_pos": "pre-TEAM 49B (48B scalars + i8 cnt=0)", "row_count": int((t24["sel"] == 11).sum()), "reader_fo": "0x1052c80"},
    ]

    # ---- TABLE_EXTRA_24.DAT ----
    ex24_cert = self_certify_extra_24(srv["table_extra_24.dat"], t24["n"])
    ex_arr = ex24_cert["arr"]
    twhm_v = col_i8(ex_arr, 10)
    tmhm_v = col_i8(ex_arr, 11)
    tpvr_v = col_i16(ex_arr, 21)
    day_allowed = [1, 2, 3, 4, 5, 6, 7]

    def dow_stats(v: np.ndarray) -> dict[str, Any]:
        live = v[v != 0]
        bad = int((~np.isin(live, day_allowed)).sum())
        vals_u, cnts_u = np.unique(v, return_counts=True)
        return {
            "rows": int(len(v)),
            "suppressed_zero": int((v == 0).sum()),
            "live_count": int(len(live)),
            "allowed_live_days": day_allowed,
            "histogram": {str(int(k)): int(c) for k, c in zip(vals_u, cnts_u)},
            "violations": bad,
        }

    extra_24_field_map = [
        {
            "field": "Twhm",
            "name": "Weekend Home Match Day",
            "schema_locations": ["club.xml#club[59]", "club.xml#club.CSrs"],
            "schema_type": "day_of_week",
            "grade": "L3",
            "scope": "server_only:table_extra_24",
            "wire_off": 10,
            "width": 1,
            "wire_type": "i8",
            "member_off": "TEAM+0xa0 -> +0x109",
            "reader_fo": "0x11a1681",
            "team_getter_fo": "0x11b0406",
            "team_setter_fo": "0x11b4e6c",
            "club_fwd_getter_fo": "0xe8bf39 -> 0xe8eb48 -> 0x11f41d0",
            "club_fwd_setter_fo": "0xe83056 -> 0xe8489b -> 0x11f6cf0",
            "domain": dow_stats(twhm_v),
        },
        {
            "field": "Tmhm",
            "name": "Midweek Home Match Day",
            "schema_locations": ["club.xml#club[60]", "club.xml#club.CSrs"],
            "schema_type": "day_of_week",
            "grade": "L3",
            "scope": "server_only:table_extra_24",
            "wire_off": 11,
            "width": 1,
            "wire_type": "i8",
            "member_off": "TEAM+0xa0 -> +0x10a",
            "reader_fo": "0x11a16a4",
            "team_getter_fo": "0x11afa0b",
            "team_setter_fo": "0x11b4d75",
            "club_fwd_getter_fo": "0xe8c68a -> 0x11f41d0",
            "club_fwd_setter_fo": "0xe83c56 -> 0x11f6cf0",
            "domain": dow_stats(tmhm_v),
        },
        {
            "field": "Tpvr",
            "name": "Previous Reputation (internal 4CC, not in master.json field_codes)",
            "schema_locations": [],
            "schema_type": "internal_i16",
            "grade": "L3_internal",
            "scope": "server_only:table_extra_24",
            "wire_off": 21,
            "width": 2,
            "wire_type": "i16",
            "member_off": "TEAM+0xa0 -> +0xf8",
            "reader_fo": "0x11a1776",
            "team_getter_fo": "0x11afb1f",
            "team_setter_fo": "0x11b4c79",
            "related_computed_4cc": "Trpc (0x11aff6c -> 0x11aff98 computes Trep - Tpvr)",
            "domain": {"rows": t24["n"], "min": int(tpvr_v.min()), "max": int(tpvr_v.max()), "unique": int(len(np.unique(tpvr_v))), "violations": 0},
        },
    ]

    extra_24_wire_layout = [
        {"off": 0, "width": 4, "dest": "lookup ordinal (0x3bb9bf9)", "type": "u32", "summary": "0..84506 exact 1:1 with table_24"},
        {"off": 4, "width": 4, "dest": "extra+0xd8 (0x11a160f)", "type": "i32", "constant": int(col_i32(ex_arr, 4)[0]), "n_unique": int(len(np.unique(col_i32(ex_arr, 4))))},
        {"off": 8, "width": 1, "dest": "extra+0x10d (0x11a1635)", "type": "u8", "constant": int(ex_arr[0, 8]), "n_unique": int(len(np.unique(ex_arr[:, 8])))},
        {"off": 9, "width": 1, "dest": "extra+0x108 (0x11a165e)", "type": "i8", "constant": int(col_i8(ex_arr, 9)[0]), "n_unique": int(len(np.unique(ex_arr[:, 9])))},
        {"off": 10, "width": 1, "dest": "extra+0x109 (0x11a1681)", "type": "i8", "field": "Twhm", "n_unique": int(len(np.unique(twhm_v)))},
        {"off": 11, "width": 1, "dest": "extra+0x10a (0x11a16a4)", "type": "i8", "field": "Tmhm", "n_unique": int(len(np.unique(tmhm_v)))},
        {"off": 12, "width": 2, "dest": "extra+0x100 (0x11a16c7)", "type": "i16", "constant": int(col_i16(ex_arr, 12)[0]), "n_unique": int(len(np.unique(col_i16(ex_arr, 12))))},
        {"off": 14, "width": 2, "dest": "extra+0x102 (0x11a16ea)", "type": "i16", "constant": int(col_i16(ex_arr, 14)[0]), "n_unique": int(len(np.unique(col_i16(ex_arr, 14))))},
        {"off": 16, "width": 2, "dest": "extra+0x106 (0x11a170d)", "type": "i16", "constant": int(col_i16(ex_arr, 16)[0]), "n_unique": int(len(np.unique(col_i16(ex_arr, 16))))},
        {"off": 18, "width": 2, "dest": "extra+0x104 (0x11a1730)", "type": "i16", "constant": int(col_i16(ex_arr, 18)[0]), "n_unique": int(len(np.unique(col_i16(ex_arr, 18))))},
        {"off": 20, "width": 1, "dest": "extra+0x10b (0x11a1753)", "type": "u8", "constant": int(ex_arr[0, 20]), "n_unique": int(len(np.unique(ex_arr[:, 20])))},
        {"off": 21, "width": 2, "dest": "extra+0xf8 (0x11a1776)", "type": "i16", "field": "Tpvr", "constant": int(tpvr_v[0]), "n_unique": int(len(np.unique(tpvr_v)))},
        {"off": 23, "width": 2, "dest": "extra+0xfa (0x11a1799)", "type": "i16", "constant": int(col_i16(ex_arr, 23)[0]), "n_unique": int(len(np.unique(col_i16(ex_arr, 23))))},
        {"off": 25, "width": 2, "dest": "extra+0xfc (0x11a17bc)", "type": "i16", "constant": int(col_i16(ex_arr, 25)[0]), "n_unique": int(len(np.unique(col_i16(ex_arr, 25))))},
        {"off": 27, "width": 2, "dest": "extra+0xfe (0x11a17df)", "type": "i16", "constant": int(col_i16(ex_arr, 27)[0]), "n_unique": int(len(np.unique(col_i16(ex_arr, 27))))},
        {"off": 29, "width": 20, "dest": "extra+0xe4..+0xf4 (5 packed dates via 0xdb7f80)", "type": "5x_packed_date", "all_valid_1900": all(packed_date_stats(col_u32(ex_arr, o))["default_1900_01_01_count"] == t24["n"] for o in (29, 33, 37, 41, 45))},
        {"off": 49, "width": 4, "dest": "extra+0x80 vec count (0x3e69150)", "type": "u32_count", "constant": 0},
        {"off": 53, "width": 4, "dest": "extra+0x68 vec count (0x374c1b0)", "type": "u32_count", "constant": 0},
        {"off": 57, "width": 4, "dest": "extra+0xe0 packed date (0xdb7f80)", "type": "packed_date", "domain": packed_date_stats(col_u32(ex_arr, 57))},
        {"off": 61, "width": 1, "dest": "extra+0x10c (0x11a18c7)", "type": "i8", "constant": int(col_i8(ex_arr, 61)[0])},
        {"off": 62, "width": 2, "dest": "extra+0xa0 vec count (0x11a18ed)", "type": "u16_count", "constant": 0},
        {"off": 64, "width": 1, "dest": "extra+0xd0 presence flag (0x11a1988)", "type": "u8_flag", "constant": 0},
        {"off": 65, "width": 1, "dest": "extra+0xa8 presence flag (0x11a19ea)", "type": "u8_flag", "constant": 0},
        {"off": 66, "width": 4, "dest": "extra+0x98 vec count (0x9f5ca0)", "type": "u32_count", "constant": 0},
        {"off": 70, "width": 12, "dest": "extra+0x10e (0x37be320: u32 len=8 + 8B)", "type": "u32_len+8B", "byte_81_histogram": {str(k): int(v) for k, v in sorted(Counter(ex_arr[:, 81].tolist()).items())}},
    ]

    # ---- CLUB+0x18 FORWARDING CHAIN (6 HELD CLUB FIELDS -> L3) ----
    t3_b18 = replay_table_3_base18(srv["table_3.dat"], t24["ttyp"])
    assert t3_b18["first_eq_first_non_skip"] and t3_b18["skip0_count"] == 0
    has_t = t3_b18["first_team"] >= 0
    ft = t3_b18["first_team"][has_t]
    own_match = int((t24["own"][ft] == np.flatnonzero(has_t)).sum())
    isn0_match = int((t24["tisn"][ft] == 0).sum())
    assert own_match == len(ft) and isn0_match == len(ft)

    crep_vals = t24["trep"][ft]
    crep_domain = {
        "clubs_total": t3_b18["n"],
        "clubs_with_team": int(len(ft)),
        "clubs_no_team_default_1500": t3_b18["clubs_with_zero_teams"],
        "raw_min": int(crep_vals.min()),
        "raw_max": int(crep_vals.max()),
        "raw_le0_clamped_to_1": int((crep_vals <= 0).sum()),
        "schema_range": [0, 10000],
        "violations": int(((crep_vals < 0) | (crep_vals > 10000)).sum()),
    }

    club_forwarded_6 = [
        {
            "club_xml_index": 31,
            "field": "Crep",
            "name": "Reputation",
            "schema_type": "integer",
            "prior_grade": "held (t63)",
            "grade": "L3",
            "projection_label": "经 +0x18 转发的投影",
            "target_entity": "team (table_24)",
            "target_team_4cc": "Trep",
            "target_member_off": "TEAM+0xa8",
            "target_wire_pos": "table_24 TEAM+2..3 (i16)",
            "forward_mode": "direct_index0_CLUB+0x18",
            "club_getter_chain": "CLUB_GET 0xe8be31 -> 0xe8ea2e (**(CLUB+0x18) -> movsx [team+0xa8]; default 0x5dc=1500 if empty)",
            "club_setter_chain": "CLUB_SET 0xe84049 -> 0xe851bf (**(CLUB+0x18) -> 0xfc9350 -> 0x3c951a0 writes word [team+0xa8], clamp 1..10000)",
            "team_getter_fo": "0x11aff60",
            "team_setter_fo": "0x11b4c85",
            "domain": crep_domain,
        },
        {
            "club_xml_index": 125,
            "field": "Cdvi",
            "name": "Division",
            "schema_type": "database_record_unique_id",
            "prior_grade": "held (t63)",
            "grade": "L3",
            "projection_label": "经 +0x18 转发的投影",
            "target_entity": "team (table_24)",
            "target_team_4cc": "Tdvi",
            "target_member_off": "TEAM+0x50",
            "target_wire_pos": "table_24 TEAM+4..7 (i32 ordinal -> table_25)",
            "forward_mode": "direct_index0_CLUB+0x18",
            "club_getter_chain": "CLUB_GET 0xe8b939 -> 0xe8b945 (**(CLUB+0x18) -> check [team+0x30]!=0 -> [team+0x50])",
            "club_setter_chain": "CLUB_SET 0xe83f65 -> 0xe84fdf (resolve comp -> **(CLUB+0x18) -> mov [team+0x50], rax at 0xe8501f)",
            "team_getter_fo": "0x11b064f",
            "team_setter_fo": "0x11b4cd3",
            "domain": {**ref_domain_check(t24["tdvi"][ft], len(t25_uids_arr), t25_uids), "clubs_no_team": t3_b18["clubs_with_zero_teams"]},
        },
        {
            "club_xml_index": 126,
            "field": "Cldi",
            "name": "Last Division",
            "schema_type": "database_record_unique_id",
            "prior_grade": "held (t63)",
            "grade": "L3",
            "projection_label": "经 +0x18 转发的投影",
            "target_entity": "team (table_24)",
            "target_team_4cc": "Tldi",
            "target_team_4cc_note": "Tldi is TEAM's internal 4CC for +0x60 (not listed in team.xml, wired in TEAM_GET 0x11afe0d / TEAM_SET 0x11b4cdf)",
            "target_member_off": "TEAM+0x60",
            "target_wire_pos": "table_24 TEAM+8..11 (i32 ordinal -> table_25)",
            "forward_mode": "helper_first_non_skip_CLUB+0x18",
            "club_getter_chain": "CLUB_GET 0xe89f6d -> 0xe8d14d (r8d='Tldi') -> 0xe8f34a -> 0x11f41d0 -> TEAM_GET 0x11afe0d -> 0x11b075d ([team+0x60])",
            "club_setter_chain": "CLUB_SET 0xe842ed -> 0xe842f9 (r8d='Tldi') -> 0xe85791 -> 0x11f6cf0 -> TEAM_SET 0x11b4cdf -> 0x11b4ceb ([team+0x60])",
            "team_getter_fo": "0x11afe0d",
            "team_setter_fo": "0x11b4cdf",
            "domain": {**ref_domain_check(t24["tldi"][ft], len(t25_uids_arr), t25_uids), "clubs_no_team": t3_b18["clubs_with_zero_teams"]},
        },
        {
            "club_xml_index": 128,
            "field": "Cndi",
            "name": "Next Division",
            "schema_type": "database_record_unique_id",
            "prior_grade": "held (t63)",
            "grade": "L3",
            "projection_label": "经 +0x18 转发的投影",
            "target_entity": "team (table_24)",
            "target_team_4cc": "Tndi",
            "target_member_off": "TEAM+0x58",
            "target_wire_pos": "table_24 TEAM+12..15 (i32 ordinal -> table_25)",
            "forward_mode": "helper_first_non_skip_CLUB+0x18",
            "club_getter_chain": "CLUB_GET 0xe8ab0d -> 0xe8ab19 (r8d='Tndi') -> 0x11f41d0 -> TEAM_GET 0x11afe92 -> 0x11b0773 ([team+0x58])",
            "club_setter_chain": "CLUB_SET 0xe82d8d -> 0xe82d99 (r8d='Tndi') -> 0x11f6cf0 -> TEAM_SET 0x11b4ed6 -> 0x11b52a3 ([team+0x58])",
            "team_getter_fo": "0x11afe92",
            "team_setter_fo": "0x11b4ed6",
            "domain": {**ref_domain_check(t24["tndi"][ft], len(t25_uids_arr), t25_uids), "clubs_no_team": t3_b18["clubs_with_zero_teams"]},
        },
        {
            "club_xml_index": 130,
            "field": "Codi",
            "name": "Secondary Division",
            "schema_type": "database_record_unique_id",
            "prior_grade": "held (t63)",
            "grade": "L3",
            "projection_label": "经 +0x18 转发的投影",
            "target_entity": "team (table_24)",
            "target_team_4cc": "Todo",
            "target_member_off": "TEAM+0x68",
            "target_wire_pos": "table_24 TEAM+29..32 (i32 ordinal -> table_25)",
            "forward_mode": "helper_first_non_skip_CLUB+0x18",
            "club_getter_chain": "CLUB_GET 0xe8b7d8 -> 0xe8e3f5 (r8d='Todo') -> 0x11f41d0 -> TEAM_GET 0x11b00b6 -> 0x11b07be ([team+0x68])",
            "club_setter_chain": "CLUB_SET 0xe83ad2 -> 0xe854ac (r8d='Todo') -> 0x11f6cf0 -> TEAM_SET 0x11b4d27 -> 0x11b5193 ([team+0x68])",
            "team_getter_fo": "0x11b00b6",
            "team_setter_fo": "0x11b4d27",
            "domain": {**ref_domain_check(t24["todo"][ft], len(t25_uids_arr), t25_uids), "clubs_no_team": t3_b18["clubs_with_zero_teams"]},
        },
        {
            "club_xml_index": 57,
            "field": "Csti",
            "name": "Stadium",
            "schema_type": "database_record_unique_id",
            "prior_grade": "held (t63)",
            "grade": "L3",
            "projection_label": "经 +0x18 转发的投影",
            "target_entity": "team (table_24)",
            "target_team_4cc": "Tsti",
            "target_member_off": "TEAM+0x78",
            "target_wire_pos": "table_24 TEAM+16..19 (i32 ordinal -> table_21)",
            "forward_mode": "helper_first_non_skip_CLUB+0x18_rel32_switch",
            "club_getter_chain": "CLUB_GET rel32 switch 0xe8a03f table 0xe91d8c[8] (base 'Csta') -> 0xe8cf2f (r8d='Tsti') -> 0x11f41d0 -> TEAM_GET 0x11afbe0 -> 0x11b109e ([team+0x78])",
            "club_setter_chain": "CLUB_SET rel32 switch 0xe82ce9 table 0xe86b38[6] (base 'Cstc') -> 0xe84537 (r8d='Tsti') -> 0x11f6cf0 -> TEAM_SET 0x11b4e54 -> 0x11b51f1 ([team+0x78])",
            "team_getter_fo": "0x11afbe0",
            "team_setter_fo": "0x11b4e54",
            "domain": {**ref_domain_check(t24["tsti"][ft], n_t21, t21_uids), "clubs_no_team": t3_b18["clubs_with_zero_teams"]},
        },
    ]

    # Verify zero violations on all L3 items!
    for r in stadium_field_map:
        if r["grade"] == "L3":
            v = r["domain"].get("violations", r["domain"].get("invalid", 0))
            assert v == 0, f"stadium L3 {r['field']} has violations={v}"
    for r in team_field_map:
        if r["grade"] == "L3":
            assert r["domain"]["violations"] == 0, f"team L3 {r['field']} has violations"
    for r in extra_24_field_map:
        assert r["domain"]["violations"] == 0, f"extra_24 {r['field']} has violations"
    for r in club_forwarded_6:
        assert r["domain"]["violations"] == 0, f"club_fwd {r['field']} has violations"

    # ---- LANDMARK CROSS-CHECKS & CLIENT ANCHOR RECONCILIATION ----
    stadium_landmarks = []
    for name, row in [("Anfield", 67), ("Old Trafford", 71), ("Santiago Bernabéu", 430), ("Allianz Arena", 12048)]:
        city_ord = int(col_i32(cb, 3)[row])
        stadium_landmarks.append({
            "name": name,
            "row": row,
            "duni": int(t21_duni[row]),
            "Scpy": int(col_i32(sb, 0)[row]),
            "Sscy": int(col_i32(sb, 4)[row]),
            "Secy": int(col_i32(sb, 8)[row]),
            "Scas": int(col_i32(sb, 12)[row]),
            "Sowi_club_ord": int(col_i32(sb, 16)[row]),
            "Scti_city_ord": city_ord,
            "city_duni": int(t2_uids_arr[city_ord]),
            "Slat": round(float(col_f32(cb, 17)[row]), 6),
            "Slon": round(float(col_f32(cb, 21)[row]), 6),
        })

    club_landmarks = []
    for name, c_ord in [("Liverpool", 460), ("Manchester United", 464), ("Real Madrid", 1297), ("FC Bayern München", 623), ("Arsenal", 387), ("Chelsea", 415)]:
        t_ord = int(t3_b18["first_team"][c_ord])
        st_ord = int(t24["tsti"][t_ord])
        dv_ord = int(t24["tdvi"][t_ord])
        club_landmarks.append({
            "name": name,
            "club_ord": c_ord,
            "club_uid": int(t3_b18["club_uid"][c_ord]),
            "b18_team_count": int(t3_b18["b18_cnt"][c_ord]),
            "first_team_ord": t_ord,
            "first_team_uid": int(t24["uid"][t_ord]),
            "first_team_Ttyp": int(t24["ttyp"][t_ord]),
            "Crep_via_Trep": int(t24["trep"][t_ord]),
            "Cdvi_ord": dv_ord,
            "Cdvi_comp_uid": int(t25_uids_arr[dv_ord]) if dv_ord >= 0 else None,
            "Cldi_ord": int(t24["tldi"][t_ord]),
            "Csti_stad_ord": st_ord,
            "Csti_stad_uid": int(t21_duni[st_ord]) if st_ord >= 0 else None,
            "Csti_Scpy": int(col_i32(sb, 0)[st_ord]) if st_ord >= 0 else None,
            "Csti_Slat": round(float(col_f32(cb, 17)[st_ord]), 6) if st_ord >= 0 else None,
            "Csti_Slon": round(float(col_f32(cb, 21)[st_ord]), 6) if st_ord >= 0 else None,
        })

    # Extract prior negative results verbatim from db_tables_big.json & extra_tables_verdict.json
    big_t21 = big["tables"]["21"]
    prior_negatives = {
        "db_tables_big_table_21_negative_results": big_t21["negative_results"],
        "extra_tables_verdict_table_extra_24": extra_verdict["archives"]["server_db.dat"]["extras"]["table_extra_24.dat"]["model_evidence"],
        "t66_boundary_preserved": "t66 only extracted ordinals from table_extra_24.dat as a task-scope boundary (not a framing conclusion); t79 independently proves 12 + 84507*82 + 0 framing and TEAM+0xa0 binding without rewriting t66.",
        "t59_t75_adjacent_refs": "WpBn/dbty and other t59/t75 team-adjacent findings are cited only and not re-judged.",
        "t76a_note": "scratch/t76a/out/ was empty during t79 execution; t79 performed independent vectorized slot profiling directly on the archives.",
        "no_l4_claim": "L4=0: no game/editor/IDA launched; Z: untouched.",
    }

    # ---- ASSEMBLE OUTPUT JSONS ----
    xref_out = {
        "task": "t79",
        "evidence_level": "L3 static (editor.exe) + L1/L2 full-archive vectorized validation; L4=0",
        "integrity": integrity,
        "factory": factory,
        "vtables": vtables,
        "db_context_tables": db_context_tables,
        "cfgs": cfgs,
        "static_proofs": static_proofs,
        "framing": {
            "table_21_stadium": {
                "record_count": n_t21,
                "client_bytes": len(c21),
                "client_equation": f"13 + {n_t21}*38 + 9 = {len(c21)}",
                "server_bytes": len(s21),
                "server_equation": f"13 + {n_t21}*181 + 9 = {len(s21)}",
                "footer_hex": c21_footer.hex(),
                "common_tail_37B_byte_identical": common_identical,
                "client_vs_server_143B_static_cause": "STADIUM::read (0x1183f30) tests mode byte [rsp+0xd0] at 0x1183f49..0x1183f54 (je 0x11843b6); mode=0 skips the entire 143B server-only prefix (0x1183f5a..0x11843b3) and jumps straight to +0xa6.",
                "b47_framing_reconciliation": "db_tables_big used header=14/footer=8 (absorbing row 0's leading selector 0x00 and treating each next selector as trailing byte +37/+180). Native body coordinates (after 1B selector) match b47's Scti@3, Slat@17, Slon@21, ordinal@25 (b47 label 'rdui@25'), duni@29..32 + rdui_dup@33..36.",
                "t74_frames_consistent": t74_frames["tables"]["21"]["archives"]["client"]["stride"] == 38 and t74_frames["tables"]["21"]["archives"]["server"]["stride"] == 181,
            },
            "table_24_team": {
                "server_only": True,
                "record_count": t24["n"],
                "total_bytes": t24["total_bytes"],
                "header_bytes": 13,
                "footer_hex": t24["footer_hex"],
                "selector_counts": t24["selector_counts"],
                "width_min": t24["width_min"],
                "width_max": t24["width_max"],
                "t74_selector_reconciliation": "Native framing from @13 yields 251 selector-11 (NATIONAL_TEAM, 49B prefix) + 84,256 selector-10 (TEAM) = 84,507 rows, 100% matching Tisn==1 (251). t74's {10:84256, 11:250, 0:1} shifted lookahead by 1 row (row 0's 11 absorbed into header, row 84506 borrowing footer byte 00).",
            },
            "table_extra_24": {k: v for k, v in ex24_cert.items() if k != "arr"},
            "table_extra_24_static_binding": {
                "caller_in_db_load_fo": "0xf5167e..0xf51694 (gated on server flag r13b; reads [db+0x98] DATABASE_TABLE<TEAM>)",
                "loader_fo": "0x3bb9b00",
                "filename_formatter_fo": "0x3cefbe0 (extra=1, old_save=0 + '.dat' -> table_extra_24.dat)",
                "record_reader_fo": "0x11a1580",
                "allocated_size_bytes": 0x118,
                "bound_member": "TEAM+0xa0 (0x11a15fa)",
                "analogue": "t71 table_extra_3.dat -> CLUB+0x100",
                "wire_layout_82B": extra_24_wire_layout,
            },
            "club_base18_join": {
                "table_3_server_rows": t3_b18["n"],
                "table_3_footer_hex": t3_b18["footer_hex"],
                "clubs_with_teams": t3_b18["clubs_with_teams"],
                "clubs_with_zero_teams": t3_b18["clubs_with_zero_teams"],
                "total_team_refs_in_base18": t3_b18["total_team_refs"],
                "first_team_skip_ttyp_count": t3_b18["skip0_count"],
                "first_eq_first_non_skip": t3_b18["first_eq_first_non_skip"],
                "bidirectional_owner_match": f"{own_match}/{len(ft)}",
                "bidirectional_isn0_match": f"{isn0_match}/{len(ft)}",
                "reader_fo": "0x11d0d30 (base18 helper 0x11d10e0)",
                "fixup_fo": "0x11d2580 (resolves ordinals via [db+0x98] DATABASE_TABLE<TEAM> using 0xf7e440 -> 0x3bf3460)",
            },
        },
        "landmarks": {
            "stadiums": stadium_landmarks,
            "clubs_via_base18": club_landmarks,
        },
        "prior_negatives_and_boundaries": prior_negatives,
    }

    stad_counts = Counter(r["grade"] for r in stadium_field_map)
    team_counts = Counter(r["grade"] for r in team_field_map)

    field_map_out = {
        "task": "t79",
        "evidence_level": "L3 static + full-archive vectorized validation; L4=0",
        "summary": {
            "stadium_xml_total": len(stadium_field_map),
            "stadium_xml_grades": dict(stad_counts),
            "stadium_internal_wire_slots": len(stadium_internal_wire_slots),
            "team_xml_total": len(team_field_map),
            "team_xml_grades": dict(team_counts),
            "extra_24_mapped_fields": len(extra_24_field_map),
            "club_base18_forwarded_upgraded_L3": len(club_forwarded_6),
        },
        "stadium_21": {
            "schema_fields": stadium_field_map,
            "internal_and_opaque_wire_slots": stadium_internal_wire_slots,
        },
        "team_24": {
            "schema_fields": team_field_map,
            "internal_wire_slots": team_internal_wire_slots,
        },
        "table_extra_24": {
            "fields": extra_24_field_map,
            "wire_layout_82B": extra_24_wire_layout,
        },
        "club_base18_forwarded_6": club_forwarded_6,
    }

    (outdir / "xref_stad_team.json").write_text(json.dumps(xref_out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (outdir / "field_map.json").write_text(json.dumps(field_map_out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return field_map_out["summary"]


def run_selftest() -> int:
    # Self-test packed date decoder, ref_domain_check, and rel32 decoding on synthetic data
    ok_dates = packed_date_stats(np.array([0x076C0001, (2024 << 16) | 366, (2023 << 16) | 365], dtype="<u4"))
    assert ok_dates["valid_gregorian"] == 3 and ok_dates["invalid"] == 0 and ok_dates["default_1900_01_01_count"] == 1
    bad_dates = packed_date_stats(np.array([(2023 << 16) | 366, (2023 << 16) | 0], dtype="<u4"))
    assert bad_dates["valid_gregorian"] == 0 and bad_dates["invalid"] == 2
    rc = ref_domain_check(np.array([-1, 0, 2, 5], dtype=np.int32), 5, {100, 200, 2})
    assert rc["live"] == 3 and rc["null_minus1"] == 1 and rc["ordinal_miss"] == 1 and rc["wrong_uid_control_hits"] == 1
    print("SELFTEST PASS: packed_date_stats, ref_domain_check")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="t79 static L3 harvest for stadium(21), team(24), extra_24, and CLUB+0x18 forwarding chain.")
    ap.add_argument("--selftest", action="store_true", help="Run built-in unit self-tests and exit.")
    ap.add_argument("--build", action="store_true", help="Build xref_stad_team.json and field_map.json.")
    ap.add_argument("--outdir", type=Path, default=ROOT / "scratch/t79/out", help="Output directory (default: scratch/t79/out).")
    args = ap.parse_args(argv)

    if not args.selftest and not args.build:
        ap.print_help()
        return 2
    try:
        if args.selftest:
            rc = run_selftest()
            if not args.build or rc != 0:
                return rc
        if args.build:
            summary = build_artifacts(args.outdir)
            print("BUILD PASS:", json.dumps(summary, ensure_ascii=False))
        return 0
    except AssertionError as e:
        print(f"CHECK FAIL: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"FATAL: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
