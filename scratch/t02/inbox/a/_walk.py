"""Symbolic reader walker: resolves dest pointers through register copies."""
from __future__ import annotations
import sys, pathlib, json
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _lib import *
import capstone.x86_const as x86


def reader_sites(pe, start, maxbytes=0x600, base_reg="rdi"):
    """Return ordered [{row_off, width, dest_disp, dest_off, width_off, call_off, ok}].

    Tracks `lea REG,[BASE+disp]` then `mov rdx,REG` (or lea rdx,[BASE+disp]) to
    resolve the actual destination address passed to stream `call [rax+0x28]`.
    """
    regs = {}
    out = []
    cum = 0
    pend_width = None
    pend_width_off = None
    pend_reg = None
    pend_disp = None
    pend_dest_off = None
    for i in pe.dis(start, maxbytes):
        if i.mnemonic == "ret":
            break
        if i.mnemonic == "lea" and len(i.operands) == 2 and \
                i.operands[0].type == x86.X86_OP_REG and \
                i.operands[1].type == x86.X86_OP_MEM:
            dst = i.reg_name(i.operands[0].reg)
            mm = i.operands[1].mem
            if i.reg_name(mm.base) == base_reg:
                regs[dst] = mm.disp
            else:
                regs.pop(dst, None)
            if dst == "rdx":
                pend_disp = regs.get("rdx")
                pend_dest_off = pe.off(i.address)
                pend_reg = "rdx"
        elif i.mnemonic == "mov" and len(i.operands) == 2 and \
                i.operands[0].type == x86.X86_OP_REG:
            d = i.reg_name(i.operands[0].reg)
            src = i.operands[1]
            if src.type == x86.X86_OP_REG:
                s = i.reg_name(src.reg)
                if s in regs:
                    regs[d] = regs[s]
                    if d == "rdx":
                        pend_disp = regs["rdx"]
                        pend_dest_off = pe.off(i.address)
                else:
                    regs.pop(d, None)
            elif src.type == x86.X86_OP_IMM and d == "r8d":
                pend_width = src.imm & 0xFFFFFFFF
                pend_width_off = pe.off(i.address)
        elif i.mnemonic == "call" and i.operands and \
                i.operands[0].type == x86.X86_OP_MEM and i.operands[0].mem.disp == 0x28:
            out.append({"row_offset": cum, "width": pend_width,
                        "dest_disp": pend_disp, "dest_off": pend_dest_off,
                        "width_off": pend_width_off, "call_off": pe.off(i.address),
                        "resolved": pend_disp is not None and pend_width is not None})
            if pend_width:
                cum += pend_width
            pend_width = None
            pend_disp = None
            pend_dest_off = None
            pend_width_off = None
    return out
