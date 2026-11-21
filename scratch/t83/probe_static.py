#!/usr/bin/env python3
"""Scratch probe for t83 static disassembly, schema dump, and db+offset mapping."""
from __future__ import annotations
import json, os, struct, sys
from collections import deque
from pathlib import Path
from capstone import CS_ARCH_X86, CS_MODE_64, Cs
from capstone.x86 import X86_OP_IMM

EXE_PATH = Path(r"D:\tmp2b\fm24\input\editor.exe")
ROOT = Path(r"D:\tmp2b\fm24-db")
OUT = ROOT / "scratch/t83"
OUT.mkdir(parents=True, exist_ok=True)


class MiniPE64:
    def __init__(self, path: Path) -> None:
        self.raw = path.read_bytes()
        pe_off = struct.unpack_from("<I", self.raw, 0x3C)[0]
        _, n_sec, _, _, _, opt_sz, _ = struct.unpack_from("<HHIIIHH", self.raw, pe_off + 4)
        opt_off = pe_off + 24
        self.image_base = struct.unpack_from("<Q", self.raw, opt_off + 24)[0]
        dd_off = opt_off + 112
        exc_rva, exc_sz = struct.unpack_from("<II", self.raw, dd_off + 3 * 8)
        sec_off = opt_off + opt_sz
        self.sections = []
        for i in range(n_sec):
            o = sec_off + i * 40
            vsize, vrva, rsize, roff = struct.unpack_from("<IIII", self.raw, o + 8)
            self.sections.append((vrva, max(vsize, rsize), roff, rsize))
        self.pdata = []
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
        raise ValueError(f"rva {hex(rva)}")

    def fo_to_rva(self, fo: int) -> int:
        for vrva, _, roff, rsize in self.sections:
            if roff <= fo < roff + rsize:
                return vrva + (fo - roff)
        raise ValueError(f"fo {hex(fo)}")

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
        raise ValueError(f"no .pdata for {hex(entry_fo)}")


def follow_thunk(pe: MiniPE64, md: Cs, fo: int) -> int:
    ins = next(md.disasm(pe.raw[fo:fo + 15], pe.fo_to_va(fo), 1))
    if ins.mnemonic == "jmp" and ins.operands and ins.operands[0].type == X86_OP_IMM:
        return pe.va_to_fo(ins.operands[0].imm)
    return fo


def walk_cfg(pe: MiniPE64, md: Cs, entry_fo: int) -> tuple[int, int, int, dict[int, object]]:
    real = follow_thunk(pe, md, entry_fo)
    b_fo, e_fo = pe.func_bounds_fo(real)
    insns = {}
    q = deque([real])
    seen = set()
    while q:
        cur = q.popleft()
        while b_fo <= cur < e_fo and cur not in seen:
            seen.add(cur)
            ins = next(md.disasm(pe.raw[cur:min(cur + 16, e_fo)], pe.fo_to_va(cur), 1), None)
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
    return real, b_fo, e_fo, insns


def disasm_linear_bounds(pe: MiniPE64, md: Cs, entry_fo: int):
    real = follow_thunk(pe, md, entry_fo)
    b_fo, e_fo = pe.func_bounds_fo(real)
    insns = {}
    cur = b_fo
    while cur < e_fo:
        ins = next(md.disasm(pe.raw[cur:min(cur + 16, e_fo)], pe.fo_to_va(cur), 1), None)
        if ins is None:
            cur += 1
            continue
        insns[cur] = ins
        cur += ins.size
    return real, b_fo, e_fo, insns


def dump_fn(pe: MiniPE64, md: Cs, title: str, fo: int, linear: bool = False) -> str:
    real, b_fo, e_fo, insns = (disasm_linear_bounds if linear else walk_cfg)(pe, md, fo)
    lines = [f"\n================ {title} entry={hex(fo)} real={hex(real)} bounds=[{hex(b_fo)},{hex(e_fo)}) n_ins={len(insns)} ================"]
    for f in sorted(insns.keys()):
        ins = insns[f]
        cmt = ""
        if ins.mnemonic in ("call", "jmp") and ins.operands and ins.operands[0].type == X86_OP_IMM:
            tva = ins.operands[0].imm
            try:
                tfo = pe.va_to_fo(tva)
                rfo = follow_thunk(pe, md, tfo)
                cmt = f"  ; -> fo={hex(tfo)}" + (f" real={hex(rfo)}" if rfo != tfo else "")
            except Exception:
                pass
        # Check for 4CC immediates
        if ins.operands:
            for op in ins.operands:
                if op.type == X86_OP_IMM:
                    v = op.imm & 0xFFFFFFFF
                    bs = struct.pack(">I", v)
                    if all(32 <= b < 127 for b in bs) and v > 0x20202020:
                        cmt += f"  ; 4CC='{bs.decode('ascii')}'"
        lines.append(f"  {hex(f):>10}: {ins.mnemonic:8s} {ins.op_str}{cmt}")
    return "\n".join(lines)


def main():
    # 1. Schema dump
    m = json.loads((ROOT / "evidence/fm24/reports/editor_schema/master.json").read_text(encoding="utf-8"))
    s_out = []
    for ek in ["award.xml", "language.xml", "weather.xml", "derby.xml", "media source.xml"]:
        e = m["entities"][ek]
        if isinstance(e, list) and e and isinstance(e[0], dict) and "fields" in e[0]:
            flds = [x for blk in e for x in blk.get("fields", [])]
        elif isinstance(e, list):
            flds = e
        else:
            flds = e.get("fields", [])
        s_out.append(f"=== {ek} ({len(flds)} fields) ===")
        for i, fl in enumerate(flds):
            fc = fl.get("field") or fl.get("id") or fl.get("code")
            extra = {k: v for k, v in fl.items() if k not in ("field", "name", "type")}
            s_out.append(f"  [{i:2d}] {str(fc):6s} type={str(fl.get('type')):26s} name={fl.get('name')!r} extra={extra}")
            eid = fl.get("enum_id") or fl.get("enum") or fc
            if eid in m.get("enums", {}):
                s_out.append(f"        ENUM[{eid}]: {m['enums'][eid]}")
            elif fc in m.get("enums", {}):
                s_out.append(f"        ENUM[{fc}]: {m['enums'][fc]}")
    (OUT / "schema_5tables.txt").write_text("\n".join(s_out), encoding="utf-8")
    print("schema_5tables.txt:", len(s_out), "lines")

    # 2. Upstream small/big notes
    u_out = []
    for rel in ["evidence/fm24/reports/dbdat_decode/db_tables_small.json", "evidence/fm24/reports/dbdat_decode/db_tables_big.json"]:
        d = json.loads((ROOT / rel).read_text(encoding="utf-8"))
        u_out.append(f"=== {rel} ===")
        for k, v in (d.get("tables") or {}).items():
            if v.get("table_id") in (0, 7, 8, 18, 27):
                u_out.append(f"  {k} tid={v.get('table_id')}:")
                for sub in ("negative_results", "notes", "caveats", "row_boundary", "identity", "anchors"):
                    if sub in v:
                        u_out.append(f"    {sub}: {json.dumps(v[sub], ensure_ascii=False)}")
    (OUT / "upstream_notes.txt").write_text("\n".join(u_out), encoding="utf-8")
    print("upstream_notes.txt:", len(u_out), "lines")

    # 3. PE disassembly
    pe = MiniPE64(EXE_PATH)
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True

    targets = [
        ("AWARD::read", 0xe483b0),
        ("AWARD::fixup", 0xe488a0),
        ("AWARD::write", 0xe48940),
        ("LANGUAGE::read", 0x10376d0),
        ("LANGUAGE::fixup", 0x10385f0),
        ("LANGUAGE::write", 0x1038620),
        ("DERBY::read", 0xffe510),
        ("DERBY::fixup", 0xffe810),
        ("DERBY::write", 0xffea80),
        ("WEATHER::read", 0x158b970),
        ("WEATHER::write", 0x158be80),
        ("MEDIA_SOURCE::read", 0x15457c0),
        ("MEDIA_SOURCE::fixup", 0x1545f80),
        ("MEDIA_SOURCE::write", 0x1546220),
    ]
    r_chunks = [dump_fn(pe, md, t, fo) for t, fo in targets]
    (OUT / "dis_rw_fixup.txt").write_text("\n".join(r_chunks), encoding="utf-8")
    print("dis_rw_fixup.txt:", sum(c.count("\n") for c in r_chunks), "lines")

    # 4. Getters and setters (linear bounds so jump-table targets aren't missed!)
    gs_targets = [
        ("AWARD::get", 0xe49a70),
        ("AWARD::set", 0xe4c240),
        ("LANGUAGE::get", 0x1038a00),
        ("LANGUAGE::set", 0x1039110),
        ("DERBY::get", 0xffd1b0),
        ("DERBY::set", 0xffdf50),
        ("WEATHER::get", 0x158e6b0),
        ("WEATHER::set", 0x15901a0),
        ("MEDIA_SOURCE::get", 0x1546e60),
        ("MEDIA_SOURCE::set", 0x154a980),
    ]
    for name, fo in gs_targets:
        slug = name.lower().replace("::", "_")
        txt = dump_fn(pe, md, name, fo, linear=True)
        (OUT / f"dis_{slug}.txt").write_text(txt, encoding="utf-8")
        print(f"dis_{slug}.txt:", txt.count("\n"), "lines")

    # 5. DATABASE context table registrations in 0xf026c0
    real, b_fo, e_fo, insns = walk_cfg(pe, md, 0xf026c0)
    ins_list = sorted(insns.items())
    db_lines = [f"=== DATABASE context registrations in 0xf026c0 [{hex(b_fo)},{hex(e_fo)}) ==="]
    for idx, (f, ins) in enumerate(ins_list):
        if ins.mnemonic == "mov" and ins.op_str.startswith("qword ptr [r14") and ins.op_str.endswith(", rdi"):
            # Look back for table name / table_id
            back = []
            for k in range(max(0, idx - 40), idx):
                bf, bi = ins_list[k]
                if bi.mnemonic in ("mov", "lea", "call"):
                    s = f"{hex(bf)}:{bi.mnemonic} {bi.op_str}"
                    # Check if lea references ascii string
                    if bi.mnemonic == "lea" and "[rip +" in bi.op_str:
                        disp = bi.operands[1].mem.disp
                        tva = bi.address + bi.size + disp
                        try:
                            tfo = pe.va_to_fo(tva)
                            raws = pe.raw[tfo:tfo+40]
                            nul = raws.find(b"\x00")
                            if 2 <= nul <= 36 and all(32 <= c < 127 for c in raws[:nul]):
                                s += f" '{raws[:nul].decode()}'"
                        except Exception:
                            pass
                    back.append(s)
            db_lines.append(f"  {hex(f)}: {ins.mnemonic} {ins.op_str}")
            for b in back[-8:]:
                db_lines.append(f"      {b}")
    (OUT / "db_context_map.txt").write_text("\n".join(db_lines), encoding="utf-8")
    print("db_context_map.txt:", len(db_lines), "lines")


if __name__ == "__main__":
    main()
