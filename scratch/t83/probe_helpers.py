#!/usr/bin/env python3
"""Disassemble helper functions and extract db+offset table IDs cleanly."""
from __future__ import annotations
import struct, sys
from pathlib import Path
from capstone import CS_ARCH_X86, CS_MODE_64, Cs
from capstone.x86 import X86_OP_IMM

sys.path.insert(0, str(Path(__file__).resolve().parent))
from probe_static import MiniPE64, dump_fn, follow_thunk, walk_cfg, EXE_PATH, OUT

pe = MiniPE64(EXE_PATH)
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True

helpers = [
    ("AWARD_helper_18_read", 0x4330ce0),
    ("AWARD_ref_50_read", 0xf920b0),
    ("AWARD_ref_60_read", 0xf92430),
    ("AWARD_ref_68_read", 0xf92b40),
    ("AWARD_ref_58_read", 0xf80180),
    ("FIXUP_3bf4a90", 0x3bf4a90),
    ("FIXUP_3bf5e90", 0x3bf5e90),
    ("FIXUP_3bf6ec0", 0x3bf6ec0),
    ("FIXUP_3bf5fd0", 0x3bf5fd0),
    ("FIXUP_3bf9220", 0x3bf9220),
    ("MEDIA_item_read_3cd4360", 0x3cd4360),
    ("WEATHER_post_43e7e10", 0x43e7e10),
    ("LANG_post_1037880", 0x1037880),
    ("AWARD_slot5_prop_reg", 0xe49090),
    ("LANG_slot5_prop_reg", 0x10387a0),
    ("DERBY_slot5_prop_reg", 0xffcc30),
    ("WEATHER_slot5_prop_reg", 0x158cab0),
    ("MEDIA_slot5_prop_reg", 0x15468e0),
]

chunks = []
for name, fo in helpers:
    try:
        chunks.append(dump_fn(pe, md, name, fo))
    except ValueError:
        real = follow_thunk(pe, md, fo)
        lines = [f"\n================ {name} (leaf) entry={hex(fo)} real={hex(real)} ================"]
        for ins in md.disasm(pe.raw[real:real+256], pe.fo_to_va(real)):
            lines.append(f"  {hex(pe.va_to_fo(ins.address)):>10}: {ins.mnemonic:8s} {ins.op_str}")
            if ins.mnemonic == "ret":
                break
        chunks.append("\n".join(lines))
(OUT / "dis_helpers.txt").write_text("\n".join(chunks), encoding="utf-8")
print("dis_helpers.txt:", sum(c.count("\n") for c in chunks), "lines")

# Also parse db_context_map cleanly from 0xf026c0 by finding every store to [r14+off] and table_id passed to ctor
real, b_fo, e_fo, insns = walk_cfg(pe, md, 0xf026c0)
ins_list = sorted(insns.items())
out = ["=== Clean db+offset -> table_id table ==="]
for idx, (f, ins) in enumerate(ins_list):
    if ins.mnemonic == "mov" and ins.op_str.startswith("qword ptr [r14") and ins.op_str.endswith(", rdi"):
        # Look back for mov r9d, <imm> or mov edx, <imm> right before table ctor
        tids = []
        for k in range(max(0, idx - 35), idx):
            bf, bi = ins_list[k]
            if bi.mnemonic in ("mov", "xor") and any(bi.op_str.startswith(r) for r in ("edx, ", "r8d, ", "r9d, ", "r9d, r9d", "edx, edx")):
                tids.append(f"{hex(bf)}:{bi.mnemonic} {bi.op_str}")
            if bi.mnemonic == "lea" and "[rip +" in bi.op_str:
                disp = bi.operands[1].mem.disp
                tva = bi.address + bi.size + disp
                try:
                    tfo = pe.va_to_fo(tva)
                    col_va = struct.unpack_from("<Q", pe.raw, tfo - 8)[0]
                    col_fo = pe.va_to_fo(col_va)
                    sig, _, _, td_rva = struct.unpack_from("<IIII", pe.raw, col_fo)
                    if sig == 1:
                        td_fo = pe.rva_to_fo(td_rva)
                        end = pe.raw.index(b"\x00", td_fo + 16)
                        tids.append(f"RTTI={pe.raw[td_fo+16:end].decode('ascii')}")
                except Exception:
                    pass
        out.append(f"  {hex(f)}: {ins.op_str:30s} | {tids[-5:]}")
(OUT / "db_context_clean.txt").write_text("\n".join(out), encoding="utf-8")
print("db_context_clean.txt:", len(out), "lines")
