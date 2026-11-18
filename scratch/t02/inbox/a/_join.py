"""Join: getter 4CC -> handler -> object member read ; reader dest -> row offset."""
from __future__ import annotations
import sys, pathlib, json
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _lib import *
from _walk import reader_sites
import capstone.x86_const as x86


def handler_for(pe, cmp_off):
    """Equality-handler start for `cmp reg,imm` at cmp_off (cmp; jcc pattern)."""
    ci = pe.ins(cmp_off)
    nb = cmp_off + ci.size
    br = pe.ins(nb)
    if br is None:
        return None
    if br.mnemonic in ("je", "jz"):
        return pe.off(br.operands[0].imm)
    if br.mnemonic in ("jne", "jnz"):
        return nb + br.size
    return nb + br.size


def handler_reads(pe, start, limit=0x120, base_reg="rdi"):
    """Memory reads/writes [base_reg+disp] up to the first call/jmp/ret."""
    out = []
    for i in pe.dis(start, limit):
        if i.mnemonic in ("ret", "jmp"):
            break
        if i.mnemonic == "call":
            break
        if i.mnemonic in ("cmp", "test", "jne", "je", "jb", "jae", "jbe", "ja"):
            if i.mnemonic in ("jne", "je", "jb", "jae", "jbe", "ja"):
                break
            continue
        for k, o in enumerate(i.operands):
            if o.type != x86.X86_OP_MEM or o.mem.base == 0:
                continue
            if i.reg_name(o.mem.base) != base_reg:
                continue
            is_write = (k == 0 and i.mnemonic in ("mov", "movzx", "movsx", "movsxd", "lea"))
            out.append({"file_offset": hex(pe.off(i.address)),
                        "instruction": (i.mnemonic + " " + i.op_str).strip(),
                        "disp": o.mem.disp, "size": o.size,
                        "is_write": is_write})
    return out


def entity_getters(pe, getter_start, codes, window=0x1800):
    """Scan the getter body for the entity's own 4CC compares."""
    want = {int.from_bytes(c.encode(), "big"): c for c in codes}
    hits = []
    for i in pe.dis(getter_start, window):
        if i.mnemonic == "cmp" and len(i.operands) == 2 and \
                i.operands[1].type == x86.X86_OP_IMM and \
                i.operands[0].type == x86.X86_OP_REG and \
                i.operands[0].size == 4:
            imm = i.operands[1].imm & 0xFFFFFFFF
            if imm in want:
                hits.append({"file_offset": hex(pe.off(i.address)),
                             "code": want[imm],
                             "register": i.reg_name(i.operands[0].reg),
                             "instruction": (i.mnemonic + " " + i.op_str).strip(),
                             "bytes": pe.data[pe.off(i.address):
                                              pe.off(i.address) + i.size].hex(" ")})
    return hits
