import pathlib,sys,struct,itertools
sys.stdout.reconfigure(encoding='utf-8')
D=pathlib.Path('scratch/t106/out')
b=(D/'payload_server_simple_vars.bin').read_bytes()
N=len(b)
def parse(hdr,kw,lw,le,foot):
    p=hdr; n=0; keys=[]
    end=N-foot
    while p<end:
        if p+kw+lw>end: return None
        key=int.from_bytes(b[p:p+kw],le); L=int.from_bytes(b[p+kw:p+kw+lw],le)
        if L> end-p-kw-lw: return None
        keys.append(key); p+=kw+lw+L; n+=1
        if n>300000: return None
    if p!=end: return None
    return n,keys
for hdr in (12,13,14,15,16):
    for kw in (1,2,4):
        for lw in (1,2,3,4):
            for le in ('little','big'):
                for foot in (0,7,8,9,10):
                    r=parse(hdr,kw,lw,le,foot)
                    if r:
                        n,keys=r
                        uniq=len(set(keys)); mono=all(keys[i]<keys[i+1] for i in range(len(keys)-1))
                        print(f'hdr={hdr} kw={kw} lw={lw} {le} foot={foot} recs={n} uniq={uniq} mono={mono} maxkey={max(keys)}')
