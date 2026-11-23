import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
from _dp import dp_walk
import struct, difflib, collections

def rows_of(arch,tid,n):
    raw=load(arch,tid)
    p,b,_,_ = dp_walk(raw,f'{arch}{tid}',14,len(raw)-8,n)
    return raw, [(s,e) for s,e,u in b]

for tid,n in ((7,208),(18,1567)):
    r1,rc=rows_of('client',tid,n); r2,rs=rows_of('server',tid,n)
    print(f'=== t{tid}')
    gaps=collections.Counter()
    for i in range(min(6,n)):
        a=r1[rc[i][0]:rc[i][1]]; b=r2[rs[i][0]:rs[i][1]]
        sm=difflib.SequenceMatcher(None,a,b,autojunk=False)
        ops=[(t,i1,i2,j1,j2) for t,i1,i2,j1,j2 in sm.get_opcodes() if t!='equal']
        print(f' row{i} c={len(a)} s={len(b)} ops={[(t,i1,i2,a[i1:i2].hex(),b[j1:j2].hex()) for t,i1,i2,j1,j2 in ops]}')
    # full-scan: is diff always at the same position?
    poss=collections.Counter()
    for i in range(n):
        a=r1[rc[i][0]:rc[i][1]]; b=r2[rs[i][0]:rs[i][1]]
        sm=difflib.SequenceMatcher(None,a,b,autojunk=False)
        for t,i1,i2,j1,j2 in sm.get_opcodes():
            if t!='equal':
                poss[(i1,i2,j1,j2)]+=1
    print(' distinct diff opcodes:', len(poss), 'top:', poss.most_common(4))
