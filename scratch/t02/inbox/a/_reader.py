import sys, json
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
from _dis import data, va, off, md
import capstone.x86_const as x86


def resolve(o, depth=0):
    while depth < 12:
        i = next(md.disasm(data[o:o + 15], va(o)), None)
        if i is None:
            return o
        if i.mnemonic == 'jmp' and i.operands[0].type == x86.X86_OP_IMM:
            t = off(i.operands[0].imm)
            if t is None:
                return o
            o = t
            depth += 1
            continue
        return o
    return o


def walk(start, maxbytes=0x4000):
    return list(md.disasm(data[start:start + maxbytes], va(start)))


def width_sites(ins_list):
    """mov r8d,imm followed (within a few insns) by lea dest + call [reg+0x28]."""
    out = []
    for k, i in enumerate(ins_list):
        if (i.mnemonic == 'mov' and len(i.operands) == 2 and
                i.operands[0].type == x86.X86_OP_REG and
                i.reg_name(i.operands[0].reg) == 'r8d' and
                i.operands[1].type == x86.X86_OP_IMM):
            dest = None
            call = None
            for j in range(k, min(k + 14, len(ins_list))):
                jj = ins_list[j]
                if (jj.mnemonic == 'lea' and len(jj.operands) == 2 and
                        jj.operands[1].type == x86.X86_OP_MEM):
                    dest = jj
                if jj.mnemonic == 'call':
                    call = jj
                    break
            out.append((off(i.address), i.operands[1].imm, dest, call))
    return out
