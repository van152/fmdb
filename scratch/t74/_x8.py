import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
from _x7 import build_cands
import struct

def enumerate_paths(raw, header, footer, n, W, align=None, require_marker=False, strict_uid=True, limit=20):
    end = len(raw)-footer
    cands, ncand = build_cands(raw, header, end, W, align, require_marker)
    layers = [sorted(cands.get(i, [])) for i in range(n)]
    # dfs with memo of paths
    sols=[]
    def dfs(i, pos, lu, acc):
        if len(sols)>limit: return
        if i==n:
            if pos==end: sols.append(list(acc))
            return
        for pk,uid in layers[i]:
            if pk<pos: continue
            e=pk+W
            if e>end: continue
            if strict_uid and uid<=lu: continue
            acc.append((pk,e,i,uid))
            dfs(i+1,e,uid,acc)
            acc.pop()
    dfs(0,header,0,[])
    return sols, layers, ncand

raw=load('client',27)
sols,layers,ncand = enumerate_paths(raw,14,8,334,13,None,True)
print('n paths',len(sols),'ncand',ncand)
for s in sols:
    lens=[s[i][0]-(s[i-1][1] if i else 14) for i in range(len(s))]
    print('path rowlens min/max',min(lens),max(lens),'first5',lens[:5],'last3',lens[-3:])
sols2,_,_ = enumerate_paths(raw,14,8,334,13,None,False)
print('marker-free paths', len(sols2))
