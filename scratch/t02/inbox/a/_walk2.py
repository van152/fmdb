"""Reader walk: object-relative dest disp -> cumulative row offset."""
from __future__ import annotations
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _lib import *
import capstone.x86_const as x86

SKIP_BASES = {"rsp", "rbp", "rip"}


def reader_sites(pe, start, maxbytes=0x800):
    """Walk a reader body, returning ordered stream-site records.

    Each record: {row_offset, width, dest_disp, dest_off, width_off, call_off,
                  instruction}
    A site is `call [REG+0x28]` with r8d=width and rdx=dest. dest is resolved
    from `lea REG,[OBJ+disp]` / `mov rdx,REG`, where OBJ is any register other
    than rsp/rbp/rip. Widths accumulate only along the block actually walked.
    """
    regs = {}     # reg -> object-relative disp
    sites = []
    cum = 0
    w = None
    w_off = None
    for i in pe.dis(start, maxbytes):
        if i.mnemonic == "ret":
            break
        if i.mnemonic == "lea" and len(i.operands) == 2 and \
                i.operands[0].type == x86.X86_OP_REG and \
                i.operands[1].type == x86.X86_OP_MEM:
            d = i.reg_name(i.operands[0].reg)
            mm = i.operands[1].mem
            if mm.index == 0 and i.reg_name(mm.base) not in SKIP_BASES:
                regs[d] = mm.disp
            else:
                regs.pop(d, None)
        elif i.mnemonic == "mov" and len(i.operands) == 2 and \
                i.operands[0].type == x86.X86_OP_REG:
            d = i.reg_name(i.operands[0].reg)
            s = i.operands[1]
            if s.type == x86.X86_OP_REG:
                sn = i.reg_name(s.reg)
                if sn in regs:
                    regs[d] = regs[sn]
                else:
                    regs.pop(d, None)
            elif s.type == x86.X86_OP_IMM and d in ("r8", "r8d"):
                w = s.imm & 0xFFFFFFFF
                w_off = pe.off(i.address)
            else:
                regs.pop(d, None)
        elif i.mnemonic == "call" and i.operands and \
                i.operands[0].type == x86.X86_OP_MEM and \
                i.operands[0].mem.disp == 0x28:
            sites.append({"row_offset": cum, "width": w,
                          "dest_disp": regs.get("rdx"),
                          "dest_off": regs.get("__doff"),
                          "width_off": w_off,
                          "call_off": pe.off(i.address),
                          "instruction": (i.mnemonic + " " + i.op_str).strip()})
            if w:
                cum += w
            w = None
            w_off = None
        if i.mnemonic == "lea" and len(i.operands) == 2 and \
                i.operands[0].type == x86.X86_OP_REG and \
                i.reg_name(i.operands[0].reg) == "rdx":
            regs["__doff"] = pe.off(i.address)
    return sites
