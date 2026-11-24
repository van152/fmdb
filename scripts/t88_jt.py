"""t88-fix6: decode range-dispatch jump tables.
 lea eax,[rsi-K] ; cmp eax,N ; jbe/ja ; [lea rcx,[rip+D]] ; movsxd rax,[rcx+rax*4] ; add rax,rcx ; jmp rax
 code = s4(K+i)
usage: t88_jt.py
"""
import sys,json,struct
import sys as _cfg_sys
from pathlib import Path as _cfg_pathlib
_cfg_sys.path.insert(0, str(_cfg_pathlib(__file__).resolve().parent))
import fm24_config as _cfg
EXE=str(_cfg.EDITOR_EXE)
JBE1=b'\x76'; JA1=b'\x77'; JBE2=b'\x0f\x86'; JA2=b'\x0f\x87'
def s4(v):
    b=v.to_bytes(4,'big')
    return b.decode('latin1') if all(32<=c<127 for c in b) else None
def main():
    d=open(EXE,'rb').read()
    lo,hi=0x11f0000,0x11f6000
    tabs=[]
    for fo in range(lo,hi-16):
        if d[fo:fo+2]!=b'\x8d\x86': continue
        k=(-struct.unpack_from('<i',d,fo+2)[0])&0xffffffff
        p=fo+6; n=None
        if d[p]==0x3d:
            n=struct.unpack_from('<I',d,p+1)[0]; p+=5
        elif d[p:p+2]==b'\x83\xf8':
            n=d[p+2]; p+=3
        if n is None or n>0x40: continue
        if d[p:p+1] in (JBE1,JA1): guard='jbe' if d[p:p+1]==JBE1 else 'ja'; p+=1
        elif d[p:p+2] in (JBE2,JA2): guard='jbe' if d[p:p+2]==JBE2 else 'ja'; p+=2
        else: continue
        tb=None
        for q in range(p,p+40):
            if d[q:q+3]==b'\x48\x8d\x0d':
                dd=struct.unpack_from('<i',d,q+3)[0]; tb=q+7+dd
                if 0<=tb<len(d): break
        if tb is None: continue
        try: offs=[struct.unpack_from('<i',d,tb+x*4)[0] for x in range(n+1)]
        except Exception: continue
        ent=[{'code':s4(k+x),'off':k+x,'tgt':tb+o} for x,o in enumerate(offs)]
        tabs.append({'lea_fo':fo,'base':s4(k),'k':k,'n':n,'table_fo':tb,'guard':guard,'entries':ent})
    json.dump(tabs,open('scratch/t88/out3/_jt.json','w'),indent=0)
    tot=0
    for t in tabs:
        good=[e for e in t['entries'] if e['code']]
        tot+=len(good)
        print(' lea=%x base=%-5s n=%-3d %-3s tb=%x codes=%d'%(t['lea_fo'],t['base'],t['n'],t['guard'],t['table_fo'],len(good)))
    print('tables',len(tabs),'code slots',tot)
if __name__=='__main__':
    if '--help' in sys.argv: print(__doc__); sys.exit(0)
    main()
