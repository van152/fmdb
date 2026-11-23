import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
from _x7 import build_cands
import struct, difflib

def rows_of(arch,tid,n,W=13,mk=True):
    raw=load(arch,tid)
    end=len(raw)-8
    cands,nc = build_cands(raw,14,end,W,None,mk)
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
            acc.append((pk,pk+W)); 
            dfs(i+1,pk+W,uid,acc)
            acc.pop()
            if sols: return
    dfs(0,14,0,[])
    s=sols[0]
    bounds=[14]+[b for a,b in s]
    return raw, [ (bounds[i],bounds[i+1]) for i in range(n)]

rc, rc_r = rows_of('client',7,208)
rs, rs_r = rows_of('server',7,208)
print('client rows',len(rc_r),'server rows',len(rs_r))
for i in range(4):
    a=rc[rc_r[i][0]:rc_r[i][1]]
    b=rs[rs_r[i][0]:rs_r[i][1]]
    print(f'row{i} client len {len(a)} server len {len(b)} diff {len(b)-len(a)}')
    print('  client:',a.hex())
    print('  server:',b.hex())
print()
diffs=[ (rs_r[i][1]-rs_r[i][0]) - (rc_r[i][1]-rc_r[i][0]) for i in range(208)]
import collections
print('per-row length diff hist', collections.Counter(diffs))
