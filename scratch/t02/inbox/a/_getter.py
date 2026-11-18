"""Getter (4CC -> handler -> object member read) and reader (dest/width) extractors."""
from __future__ import annotations
import sys, pathlib, json
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _lib import *
import capstone.x86_const as x86


def entity_codes():
    m = json.loads(MASTER.read_text(encoding="utf-8"))
    out = {}
    for k, v in m["entities"].items():
        for e in v:
            out[e["id"]] = {"xml": k, "fields": [f["field"] for f in e["fields"]],
                            "names": {f["field"]: f.get("name") for f in e["fields"]},
                            "types": {f["field"]: f.get("type") for f in e["fields"]}}
    return out


def cmp_sites(pe):
    d = pe.data
    regs = {0xF8: "eax", 0xF9: "ecx", 0xFA: "edx", 0xFB: "ebx",
            0xFC: "esp", 0xFD: "ebp", 0xFE: "esi", 0xFF: "edi"}
    out = []
    for p in range(len(d) - 8):
        b = d[p]
        if b == 0x81 and d[p + 1] in regs:
            i = pe.ins(p)
            if i is not None and i.mnemonic == "cmp" and i.size == 6:
                out.append((p, int.from_bytes(d[p + 2:p + 6], "little"), regs[d[p + 1]]))
        elif b == 0x3D:
            i = pe.ins(p)
            if i is not None and i.mnemonic == "cmp" and i.size == 5:
                out.append((p, int.from_bytes(d[p + 1:p + 5], "little"), "eax"))
    return out


def branch_after(pe, off):
    i = pe.ins(off)
    return i


def handler_range(pe, cmp_off, limit=0x200):
    """Return (start, end) file offsets of the equality/fallthrough handler block."""
    cmp_ins = pe.ins(cmp_off)
    br = pe.ins(cmp_off + cmp_ins.size)
    nxt = cmp_off + cmp_ins.size
    if br is None:
        return (nxt, nxt + limit)
    m = br.mnemonic
    if m in ("je", "jz"):
        t = pe.off(br.operands[0].imm)
        return (t, t + limit)
    if m in ("jne", "jnz"):
        # fallthrough is the equality handler; runs until next cmp
        return (nxt + br.size, nxt + br.size + limit)
    return (nxt + br.size, nxt + br.size + limit)


def block_reads(pe, start, end):
    """Collect memory reads of form [reg+disp] with a width, in the block."""
    reads = []
    ins = pe.dis(start, end - start)
    for i in ins:
        if i.mnemonic in ("cmp", "jmp", "ret", "call") and i.mnemonic != "cmp":
            if i.mnemonic in ("ret", "jmp"):
                break
        if i.mnemonic == "call":
            break
        if not i.operands:
            continue
        for k, o in enumerate(i.operands):
            if o.type != x86.X86_OP_MEM or o.mem.base == 0:
                continue
            base = i.reg_name(o.mem.base)
            size = o.size
            writes = (k == 0 and i.mnemonic in ("mov", "movzx", "movsx", "movsxd", "lea"))
            reads.append({"file_offset": hex(pe.off(i.address)), "instruction":
                          (i.mnemonic + " " + i.op_str).strip(), "base": base,
                          "disp": o.mem.disp, "size": size, "is_dest": writes})
    return reads


def reader_sites(pe, start, maxbytes=0x800):
    """Walk reader: (order, dest_disp, width, dest_off, width_off, call_off)"""
    out = []
    ins = pe.dis(start, maxbytes)
    pend_width = None
    pend_width_off = None
    pend_dest = None
    pend_dest_off = None
    for i in ins:
        if i.mnemonic == "ret":
            break
        if (i.mnemonic == "mov" and len(i.operands) == 2 and
                i.operands[0].type == x86.X86_OP_REG and
                i.reg_name(i.operands[0].reg) == "r8d" and
                i.operands[1].type == x86.X86_OP_IMM):
            pend_width = i.operands[1].imm
            pend_width_off = pe.off(i.address)
        elif i.mnemonic == "lea" and len(i.operands) == 2 and \
                i.operands[1].type == x86.X86_OP_MEM:
            pend_dest = i.operands[1].mem
            pend_dest_off = pe.off(i.address)
        elif i.mnemonic == "call" and i.operands and \
                i.operands[0].type == x86.X86_OP_MEM and i.operands[0].mem.disp == 0x28:
            out.append({"dest_disp": pend_dest.disp if pend_dest else None,
                        "dest_base": i.reg_name(pend_dest.base) if pend_dest else None,
                        "width": pend_width,
                        "dest_off": pend_dest_off, "width_off": pend_width_off,
                        "call_off": pe.off(i.address)})
            pend_dest = None
    return out
