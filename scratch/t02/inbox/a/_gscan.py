import sys, pathlib, json
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _lib import *
import capstone.x86_const as x86

def scan_region(pe, start, size):
    """All cmp r32, imm32 with printable ASCII imm (potential 4CC) in a region."""
    out=[]
    for i in pe.dis(start, size):
        if i.mnemonic=='cmp' and len(i.operands)==2 and i.operands[1].type==x86.X86_OP_IMM and i.operands[0].type==x86.X86_OP_REG and i.operands[0].size==4:
            imm=i.operands[1].imm & 0xFFFFFFFF
            b=imm.to_bytes(4,'big')
            if all(32<=c<127 for c in b):
                out.append((pe.off(i.address), b.decode(), i.reg_name(i.operands[0].reg)))
    return out

if __name__=='__main__':
    pe=PE(EDITOR.read_bytes())
    s=int(sys.argv[1],16); n=int(sys.argv[2],16)
    for o,c,r in scan_region(pe,s,n):
        print(f"{o:#x} {r:4s} {c}")
