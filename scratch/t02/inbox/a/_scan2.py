import sys
sys.path.insert(0,str(__import__('pathlib').Path(__file__).resolve().parent))
from _lib import *

def scan_raw(pe, start, end):
    d=pe.data; regs={0xF8:'eax',0xF9:'ecx',0xFA:'edx',0xFB:'ebx',0xFC:'esp',0xFD:'ebp',0xFE:'esi',0xFF:'edi'}
    hits=[]
    for p in range(start,end):
        if d[p]==0x81 and p+6<=end and d[p+1] in regs:
            imm=int.from_bytes(d[p+2:p+6],'little')
            hits.append((p,regs[d[p+1]],imm))
        elif d[p]==0x3D and p+5<=end:
            hits.append((p,'eax',int.from_bytes(d[p+1:p+5],'little')))
        elif d[p]==0x41 and p+7<=end and d[p+1]==0x81 and d[p+2] in regs:
            hits.append((p,'r'+regs[d[p+2]],int.from_bytes(d[p+3:p+7],'little')))
    return hits

if __name__=='__main__':
    pe=PE(EDITOR.read_bytes())
    s=int(sys.argv[1],16); e=int(sys.argv[2],16)
    for p,r,imm in scan_raw(pe,s,e):
        ab=imm.to_bytes(4,'big')
        txt=''.join(chr(c) if 32<=c<127 else '.' for c in ab)
        i=pe.ins(p)
        ok = i is not None and i.mnemonic=='cmp' and i.size in (5,6,7)
        print(f"{p:#x} {r:4s} {imm:#010x} '{ab.decode('latin1')}' {'decoded' if ok else 'RAW'}")
