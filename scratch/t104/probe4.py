import sys, struct, runpy, collections, json
sys.path.insert(0,'D:/tmp2b/fm24/tools/python'); sys.path.insert(0,'scripts')
m=runpy.run_path('scripts/t38_multiframe.py', run_name='p')
codec=m['_codec'](); cache={}
raw=m['load_payload_mf'](codec,'server',24,cache)
n=struct.unpack_from('<I',raw,8)[0]
H=14; F=8; T=13
end=len(raw)-F
ALLOW=(0,10,11)
cands=collections.defaultdict(list)
for p in range(H, end-(T-1)):
    if raw[p+12] not in ALLOW: continue
    a,b,c=struct.unpack_from('<III',raw,p)
    if a<n and b==c and b: cands[a].append((p,b))
for k in cands: cands[k].sort()
# DP over rows: state = (cursor_after, uid) -> (p, prev_state)
cur={(H,0):(None,None)}
hist=[]
for i in range(n):
    new={}
    for (curp,last),(pp,pu) in cur.items():
        for p,u in cands[i]:
            if p<curp or u<=last: continue
            k=(p+T,u)
            if k not in new: new[k]=(p,(curp,last))
    # dominance prune
    keys=sorted(new, key=lambda k:(k[0],k[1]))
    pruned={}; best=None
    for k in keys:
        if best is not None and k[1]>=best: continue
        pruned[k]=new[k]; best=k[1]
    hist.append(pruned); cur=pruned
fin=[k for k in cur if k[0]==end]
print('final states',fin)
assert len(fin)==1
key=fin[0]; path=[]
for i in range(n,0,-1):
    p,prev=hist[i-1][key]
    path.append((p,key[1],raw[p+12]))
    key=prev
path.reverse()
lens=[path[i][0]-(H if i==0 else path[i-1][0]+T) for i in range(n)]
print('closure', H+sum(lens)+T*n+F==len(raw), 'lens', min(lens), max(lens), round(sum(lens)/n,3))
print('sel', collections.Counter(x[2] for x in path))
def body(i):
    s=H if i==0 else path[i-1][0]+T
    return raw[s:path[i][0]]
print('row0',lens[0],body(0).hex())
print('row1',lens[1],body(1).hex())
json.dump({'lens':lens,'ident':[[p,u,s] for p,u,s in path]}, open('scratch/t104/path.json','w'))
