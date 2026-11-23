import sys, json
from pathlib import Path
import capstone, capstone.x86_const as x86
E=Path('../fm24/input/editor.exe'); data=E.read_bytes()
pe=int.from_bytes(data[0x3C:0x40],'little'); opt=pe+24
base=int.from_bytes(data[opt+24:opt+32],'little')
nsec=int.from_bytes(data[pe+6:pe+8],'little'); tbl=opt+int.from_bytes(data[pe+20:pe+22],'little')
secs=[]
for p in range(tbl,tbl+nsec*40,40):
    nm=data[p:p+8].rstrip(b'\0').decode('ascii','replace')
    vs,rva,rs,raw=__import__('struct').unpack_from('<IIII',data,p+8)
    secs.append((nm,rva,vs,raw,rs))
def va(o):
    for _,rva,_,raw,size in secs:
        if raw<=o<raw+size: return base+rva+o-raw
def off(v):
    for _,rva,_,raw,size in secs:
        d=v-(base+rva)
        if 0<=d<size: return raw+d
md=capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64); md.detail=True
def dump(start, size=0x800, stop_at_ret=True):
    ins=list(md.disasm(data[start:start+size], va(start)))
    out=[]
    for i in ins:
        o=off(i.address)
        t=f"{i.mnemonic} {i.op_str}"
        ann=''
        if i.mnemonic=='mov' and i.operands and i.reg_name(i.operands[0].reg)=='r8d' and i.operands[1].type==x86.X86_OP_IMM:
            ann='   <<WIDTH %d>>'%i.operands[1].imm
        elif i.mnemonic=='lea' and len(i.operands)>1 and i.operands[1].type==x86.X86_OP_MEM:
            mm=i.operands[1].mem
            ann='   <<DEST %s+%#x>>'%(i.reg_name(mm.base),mm.disp)
        elif i.mnemonic=='call':
            if i.operands[0].type==x86.X86_OP_MEM:
                ann='   <<STREAMCALL>>'
            else:
                ann='   -><t>'
        elif i.mnemonic in ('je','jne','jz','jnz','jmp','jb','jae','jbe','ja','jl','jge','jle','jg','js','jns'):
            ann='   -><j>'
        out.append((o,t,ann))
        if stop_at_ret and i.mnemonic in ('ret','retn'): break
    return out
if __name__=='__main__':
    s=int(sys.argv[1],16); sz=int(sys.argv[2],16) if len(sys.argv)>2 else 0x800
    for o,t,a in dump(s,sz): print(f"{o:#09x} {t:60s}{a}")
