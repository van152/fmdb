"""Entity field join: reader row slots x getter object offsets."""
from __future__ import annotations
import sys, pathlib, json
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _lib import *
from _walk import reader_sites
from _getter import entity_codes
import capstone.x86_const as x86

TYPE_WIDTH = {
    "real": 4, "integer": 4, "boolean": 1, "enum": 1, "multiple_enum": 4,
    "database_record_unique_id": 4, "unique_id": 4, "date": 4, "cash": 4,
    "string": None, "short": 4, "byte": 1, "float": 4,
}


def getter_window(pe, getter_start, window=0x1C00):
    return pe.dis(getter_start, window)


def scan_entity_compares(pe, getter_start, codes, window=0x1C00):
    want = {int.from_bytes(c.encode(), "big"): c for c in codes}
    hits = []
    for i in getter_window(pe, getter_start, window):
        if i.mnemonic != "cmp" or len(i.operands) != 2:
            continue
        a, b = i.operands
        if a.type == x86.X86_OP_REG and a.size == 4 and b.type == x86.X86_OP_IMM:
            imm = b.imm & 0xFFFFFFFF
            if imm in want:
                hits.append({"code": want[imm], "file_offset": pe.off(i.address),
                             "register": i.reg_name(a.reg),
                             "text": (i.mnemonic + " " + i.op_str).strip(),
                             "size": i.size})
    return hits


def eq_handler(pe, cmp_off):
    ci = pe.ins(cmp_off)
    nb = cmp_off + ci.size
    br = pe.ins(nb)
    if br is None:
        return None
    if br.mnemonic in ("je", "jz") and br.operands[0].type == x86.X86_OP_IMM:
        return pe.off(br.operands[0].imm)
    if br.mnemonic in ("jne", "jnz"):
        return nb + br.size
    return nb + br.size


def obj_reads(pe, start, limit=0x100):
    """Object member access in the equality handler, before the first call/jmp."""
    out = []
    if start is None:
        return out
    prev_cond = False
    for i in pe.dis(start, limit):
        if i.mnemonic in ("ret", "jmp", "call"):
            break
        if i.mnemonic.startswith("j"):
            prev_cond = True
            continue
        if i.mnemonic in ("cmp", "test", "nop", "int3"):
            continue
        for k, o in enumerate(i.operands):
            if o.type != x86.X86_OP_MEM or o.mem.base == 0:
                continue
            out.append({"file_offset": pe.off(i.address),
                        "text": (i.mnemonic + " " + i.op_str).strip(),
                        "base": i.reg_name(o.mem.base), "disp": o.mem.disp,
                        "mem_size": o.size,
                        "kind": "write" if (k == 0 and i.mnemonic in
                                            ("mov", "movzx", "movsx", "movsxd", "lea"))
                                else "read",
                        "opcode": i.mnemonic})
    return out
