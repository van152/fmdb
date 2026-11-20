import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
import struct, collections

def rows_media(arch):
    raw=load(arch,7)
    out=[]
    for p in (14,'x'):
        break
    # use known: parse with hypothesis iteratively
    return raw

raw=load('client',7)
# take the 208 boundaries from DP
from _x7 import build_cands
def dp_path(raw,n=208,W=13,header=14,footer=8):
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

rb=dp_path(raw)
print('rows',len(rb))
mids=[]
for i,(s,e) in enumerate(rb[:12]):
    b=raw[s:e]
    nl=struct.unpack_from('<I',b,0)[0]
    name=b[4:4+nl]
    pre=b[4+nl:4+nl+6]
    ul=struct.unpack_from('<I',b,4+nl+6)[0]
    url=b[4+nl+10:4+nl+10+ul]
    mid=b[4+nl+10+ul:e-13]
    print(f'row{i} len={len(b)} nl={nl} name={name!r} pre={pre.hex()} ul={ul} url={url[:28]!r} midlen={len(mid)}')
    print('   mid:',mid.hex(' '))
    mids.append(mid)
EOF=0
