"""t88-fix6: stub map (mov rcx,rdi; mov dl,N; mov r8d,tag; jmp) -> start addr."""
import sys,json,capstone
import sys as _cfg_sys
from pathlib import Path as _cfg_pathlib
_cfg_sys.path.insert(0, str(_cfg_pathlib(__file__).resolve().parent))
import fm24_config as _cfg
EXE=str(_cfg.EDITOR_EXE); BASE=0x140000000
def s4(v):
    b=v.to_bytes(4,'big')
    return b.decode('latin1') if all(32<=c<127 for c in b) else None
def main():
    d=open(EXE,'rb').read()
    md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
    lo,hi=0x11f0000,0x11f5000
    ins=list(md.disasm(d[lo:hi],BASE+lo))
    stubs={}
    for i in range(len(ins)-3):
        a,b,c,e=ins[i],ins[i+1],ins[i+2],ins[i+3]
        if (a.mnemonic=='mov' and a.op_str=='rcx, rdi' and b.mnemonic=='mov' and b.op_str.startswith('dl, ')
            and c.mnemonic=='mov' and c.op_str.startswith('r8d, ') and e.mnemonic=='jmp'):
            try: dl=int(b.op_str.split(', ')[1],16); tg=s4(int(c.op_str.split(', ')[1],16))
            except: continue
            if tg: stubs[a.address-BASE]={'rec_type':dl,'tag':tg,'dl_fo':b.address-BASE,'tag_fo':c.address-BASE,'jmp':e.op_str}
    # 2-instruction variant (rcx already set)
    for i in range(len(ins)-2):
        b,c,e=ins[i],ins[i+1],ins[i+2]
        if (b.mnemonic=='mov' and b.op_str.startswith('dl, ') and c.mnemonic=='mov' and c.op_str.startswith('r8d, ')
            and e.mnemonic=='jmp' and (b.address-BASE) not in stubs):
            try: dl=int(b.op_str.split(', ')[1],16); tg=s4(int(c.op_str.split(', ')[1],16))
            except: continue
            if tg: stubs[b.address-BASE]={'rec_type':dl,'tag':tg,'dl_fo':b.address-BASE,'tag_fo':c.address-BASE,'jmp':e.op_str}
    json.dump({hex(k):v for k,v in sorted(stubs.items())},open('scratch/t88/out3/_stubs.json','w'),indent=0)
    print('stubs',len(stubs))
    for k,v in sorted(stubs.items()): print('  %x rt=%-3s %s'%(k,v['rec_type'],v['tag']))
if __name__=='__main__':
    if '--help' in sys.argv: print('usage: t88_stubs.py'); sys.exit(0)
    main()
