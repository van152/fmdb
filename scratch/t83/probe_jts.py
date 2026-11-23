#!/usr/bin/env python3
"""Decode all switch jump tables and inspect WEATHER season sub-get/set, AWARD get/set, MEDIA get/set."""
from __future__ import annotations
import struct, sys
from pathlib import Path
from capstone import CS_ARCH_X86, CS_MODE_64, Cs
from capstone.x86 import X86_OP_IMM, X86_OP_MEM

sys.path.insert(0, str(Path(__file__).resolve().parent))
from probe_static import MiniPE64, dump_fn, follow_thunk, disasm_linear_bounds, EXE_PATH, OUT

pe = MiniPE64(EXE_PATH)
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True


def decode_jump_tables_in(fn_fo: int, name: str) -> str:
    real, b_fo, e_fo, insns = disasm_linear_bounds(pe, md, fn_fo)
    fs = sorted(insns.keys())
    lines = [f"=== Jump tables in {name} (real={hex(real)}) ==="]
    for idx, f in enumerate(fs):
        ins = insns[f]
        if ins.mnemonic == "jmp" and ins.op_str in ("rax", "rcx", "rdx", "r8", "r9"):
            # Look back for lea reg, [rip+disp], cmp eax, N, lea eax, [r - base] / sub eax, base
            tbl_fo = None
            max_idx = None
            base_4cc = None
            for k in range(max(0, idx - 12), idx):
                bi = insns[fs[k]]
                if bi.mnemonic == "lea" and "[rip +" in bi.op_str:
                    disp = bi.operands[1].mem.disp
                    tbl_va = bi.address + bi.size + disp
                    try:
                        tbl_fo = pe.va_to_fo(tbl_va)
                    except Exception:
                        pass
                if bi.mnemonic == "cmp" and len(bi.operands) == 2 and bi.operands[1].type == X86_OP_IMM:
                    max_idx = bi.operands[1].imm
                if bi.mnemonic == "lea" and len(bi.operands) == 2 and bi.operands[1].type == X86_OP_MEM and bi.operands[1].mem.disp < 0:
                    base_4cc = (-bi.operands[1].mem.disp) & 0xFFFFFFFF
                if bi.mnemonic in ("sub", "add") and len(bi.operands) == 2 and bi.operands[1].type == X86_OP_IMM:
                    if bi.mnemonic == "sub":
                        base_4cc = bi.operands[1].imm & 0xFFFFFFFF
                    elif bi.operands[1].imm < 0:
                        base_4cc = (-bi.operands[1].imm) & 0xFFFFFFFF
            if tbl_fo is not None and max_idx is not None and max_idx < 256:
                lines.append(f"  switch@{hex(f)} tbl_fo={hex(tbl_fo)} max={max_idx} base={hex(base_4cc) if base_4cc else None}")
                # find default target (most frequent)
                targets = []
                for j in range(max_idx + 1):
                    rel = struct.unpack_from("<i", pe.raw, tbl_fo + j * 4)[0]
                    tva = pe.fo_to_va(tbl_fo) + rel
                    tfo = pe.va_to_fo(tva)
                    targets.append(tfo)
                from collections import Counter
                cnt = Counter(targets)
                default_tfo = cnt.most_common(1)[0][0] if len(cnt) > 1 and cnt.most_common(1)[0][1] > 2 else None
                for j, tfo in enumerate(targets):
                    if tfo == default_tfo:
                        continue
                    code = (base_4cc + j) & 0xFFFFFFFF if base_4cc else j
                    bs = struct.pack(">I", code)
                    cstr = bs.decode("ascii") if all(32 <= b < 127 for b in bs) else hex(code)
                    lines.append(f"    [{j:2d}] '{cstr}' ({hex(code)}) -> {hex(tfo)}")
                if default_tfo is not None:
                    lines.append(f"    (default -> {hex(default_tfo)}, count={cnt[default_tfo]})")
    return "\n".join(lines)


def main():
    chunks = []
    # Check WEATHER sub-get and find sub-set from WEATHER::set
    chunks.append(dump_fn(pe, md, "WEATHER_SEASON::get", 0x158f1d0, linear=True))
    # Scan WEATHER::set for external jumps/calls
    real, b_fo, e_fo, insns = disasm_linear_bounds(pe, md, 0x15901a0)
    ext_targets = set()
    for f, ins in sorted(insns.items()):
        if ins.mnemonic in ("call", "jmp") and ins.operands and ins.operands[0].type == X86_OP_IMM:
            try:
                tfo = pe.va_to_fo(ins.operands[0].imm)
            except ValueError:
                continue
            if not (b_fo <= tfo < e_fo) and 0x1580000 <= tfo <= 0x1595000:
                ext_targets.add(tfo)
    print("WEATHER::set local targets:", [hex(x) for x in sorted(ext_targets)])
    for tfo in sorted(ext_targets):
        chunks.append(dump_fn(pe, md, f"WEATHER_sub_{hex(tfo)}", tfo, linear=True))
    (OUT / "dis_weather_sub.txt").write_text("\n".join(chunks), encoding="utf-8")
    print("dis_weather_sub.txt:", sum(c.count("\n") for c in chunks), "lines")

    # Decode all jump tables across the 5 get/set functions + WEATHER_SEASON
    jt_targets = [
        ("AWARD::get", 0xe49a70),
        ("AWARD::set", 0xe4c240),
        ("LANGUAGE::get", 0x1038a00),
        ("LANGUAGE::set", 0x1039110),
        ("DERBY::get", 0xffd1b0),
        ("DERBY::set", 0xffdf50),
        ("WEATHER::get", 0x158e6b0),
        ("WEATHER::set", 0x15901a0),
        ("WEATHER_SEASON::get", 0x158f1d0),
        ("MEDIA_SOURCE::get", 0x1546e60),
        ("MEDIA_SOURCE::set", 0x154a980),
    ]
    for tfo in sorted(ext_targets):
        jt_targets.append((f"WEATHER_sub_{hex(tfo)}", tfo))
    jt_out = [decode_jump_tables_in(fo, n) for n, fo in jt_targets]
    (OUT / "jump_tables.txt").write_text("\n\n".join(jt_out), encoding="utf-8")
    print("jump_tables.txt:", sum(c.count("\n") for c in jt_out), "lines")


if __name__ == "__main__":
    main()
