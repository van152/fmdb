"""Control-flow-aware reader walker (handles if/else diamonds, no loops assumed)."""
from __future__ import annotations
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _lib import *
import capstone.x86_const as x86


def walk_cfg(pe, start, max_ins=400, base_reg="rcx"):
    """Symbolic walk. Returns (sites_in_stream_order, trace, notes).

    Reads are `call [reg+0x28]` with r8d=width and rdx=dest. dest is resolved
    through `lea REG,[<objbase>+disp]` / `mov rdx,REG` chains. Both sides of an
    `if (stream ok)` diamond are explored in target order; a simple heuristic
    joins on the nearest forward block.
    """
    regs = {}          # reg -> disp (object-relative)
    sites = []
    trace = []
    notes = []
    cum = [0]
    visited = set()
    todo = [(start, dict(regs), cum[0])]
    order = []
    while todo:
        pc, regs_in, base_cum = todo.pop(0)
        while True:
            if pc in visited:
                break
            visited.add(pc)
            i = pe.ins(pc)
            if i is None:
                notes.append(f"undecodable at {pc:#x}")
                break
            off = pe.off(i.address)
            text = (i.mnemonic + " " + i.op_str).strip()
            row = {"file_offset": off, "instruction": text, "cum": base_cum}
            if i.mnemonic == "ret":
                trace.append({**row, "note": "ret"})
                break
            if i.mnemonic == "lea" and len(i.operands) == 2 and \
                    i.operands[0].type == x86.X86_OP_REG and \
                    i.operands[1].type == x86.X86_OP_MEM:
                d = i.reg_name(i.operands[0].reg)
                mm = i.operands[1].mem
                if mm.index == 0 and i.reg_name(mm.base) != "rip":
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
                else:
                    regs.pop(d, None)
            elif i.mnemonic == "call" and i.operands and \
                    i.operands[0].type == x86.X86_OP_MEM and \
                    i.operands[0].mem.disp == 0x28:
                w = regs.get("r8d")
                dst = regs.get("rdx")
                site = {"file_offset": off, "cum": base_cum,
                        "width": regs.get("__w"), "dest_disp": dst,
                        "dest_off": regs.get("__dest_off"),
                        "width_off": regs.get("__w_off"),
                        "instruction": text}
                sites.append(site)
                trace.append({**row, "note": "stream-call", "site": site})
                if regs.get("__w"):
                    base_cum += regs["__w"]
                regs["__w"] = None
                regs["__dest_off"] = None
                regs["__w_off"] = None
                pc = pe.off(i.address) + i.size
                continue
            elif i.mnemonic == "mov" and len(i.operands) == 2 and \
                    i.operands[0].type == x86.X86_OP_REG and \
                    i.reg_name(i.operands[0].reg) == "r8d" and \
                    i.operands[1].type == x86.X86_OP_IMM:
                regs["__w"] = i.operands[1].imm & 0xFFFFFFFF
                regs["__w_off"] = off
            if i.mnemonic == "lea" and len(i.operands) == 2 and \
                    i.operands[0].type == x86.X86_OP_REG and \
                    i.reg_name(i.operands[0].reg) == "rdx":
                regs["__dest_off"] = off
            trace.append(row)
            if i.mnemonic.startswith("j") and i.operands and \
                    i.operands[0].type == x86.X86_OP_IMM:
                tgt = pe.off(i.operands[0].imm)
                fall = pe.off(i.address) + i.size
                if i.mnemonic == "jmp":
                    pc = tgt
                    continue
                # conditional: explore fallthrough first, queue target
                todo.append((tgt, dict(regs), base_cum))
                pc = fall
                continue
            pc = pe.off(i.address) + i.size
    return sites, trace, notes
