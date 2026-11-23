import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
from _x7 import build_cands
import struct, collections

def dp_path(raw,n,W=13,header=14,footer=8):
    end=len(raw)-footer
    cands,_=build_cands(raw,header,end,W,None,True)
    layers=[sorted(cands.get(i,[])) for i in range(n)]
    sols=[]
    def dfs(i,pos,lu,acc):
        if sols: return
        if i==n:
            if pos==end: sols.append(list(acc))
            return
        for pk,uid in layers[i]:
            if pk<pos: continue
            if uid<=lu: continue
            acc.append(pk); dfs(i+1,pk+W,uid,acc); acc.pop()
            if sols: return
    dfs(0,header,0,[])
    b=[header]+[p+W for p in sols[0]]
    return [(b[i],b[i+1]) for i in range(len(b)-1)]

def analyze(arch,tid,n):
    raw=load(arch,tid)
    rows=dp_path(raw,n)
    print(f'=== {arch} t{tid}: {len(rows)} rows, payload {len(raw)}')
    resid=collections.Counter(); names=[]
    for i,(s,e) in enumerate(rows):
        b=raw[s:e]
        nl=struct.unpack_from('<I',b,0)[0]
        name=b[4:4+nl]
        names.append((nl,name))
        resid[len(b)-(4+nl)-13]+=1
    print('  residual after name+before 13B identity hist:', dict(sorted(resid.items())))
    print('  name len range', min(x[0] for x in names), max(x[0] for x in names))
    print('  first names', [x[1][:24] for x in names[:4]])
    return raw, rows

for arch,tid,n in [('client',8,126),('server',8,126),('client',27,334),('server',27,334),
                   ('client',18,1567),('server',18,1567),('client',7,208),('server',7,208)]:
    analyze(arch,tid,n)
    print()
