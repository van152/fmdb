import sys, struct, runpy, collections, json
sys.path.insert(0,'D:/tmp2b/fm24/tools/python'); sys.path.insert(0,'scripts')
m=runpy.run_path('scripts/t38_multiframe.py', run_name='p')
codec=m['_codec'](); cache={}
raw=m['load_payload_mf'](codec,'server',24,cache)
n=struct.unpack_from('<I',raw,8)[0]
H=14; F=8; T=13
end=len(raw)-F
cands=collections.defaultdict(list)
for p in range(H, end-(T-1)):
    a,b,c=struct.unpack_from('<III',raw,p)
    if a<n and b==c and b:
        cands[a].append((p,b))
for k in cands: cands[k].sort()
back=[{}]     # back[i][key] = prevkey
states={(H,0)}
for i in range(n):
    cs=cands.get(i,())
    new={}
    for (cur,last) in states:
        for p,u in cs:
            if p<cur or u<=last: continue
            k=(p+T,u)
            if k not in new: new[k]=(cur,last)
    pruned={}; minuid=None
    for k in sorted(new):
        if minuid is not None and k[1]>=minuid: continue
        pruned[k]=new[k]; minuid=k[1]
    back.append(pruned)
    states=set(pruned)
fin=[s for s in states if s[0]==end]
print('final',fin)
key=fin[0]; path=[]
for i in range(n,0,-1):
    prev=back[i][key]
    p=prev[0]; uid=key[1]
    path.append((p,uid))
    key=prev
path.reverse()
assert path[0][0]==H
lens=[path[i][0]-(H if i==0 else path[i-1][0]+T) for i in range(n)]
print('len min/max/mean',min(lens),max(lens),round(sum(lens)/n,3))
sel=collections.Counter(raw[path[i][0]+12] for i in range(n))
print('selector',sel)
def body(i):
    s=H if i==0 else path[i-1][0]+T
    return raw[s:path[i][0]]
print('row0',len(body(0)),body(0).hex())
print('row1',len(body(1)),body(1).hex())
print('row2',len(body(2)),body(2).hex())
nat=[i for i in range(n) if raw[path[i][0]+12]==11]
print('nat',len(nat),nat[:6])
for i in nat[:3]:
    print('nat',i,'len',len(body(i)),body(i).hex())
    print('   pre49?', raw[path[i][0]-49:path[i][0]].hex() if path[i][0]>=49 else None)
json.dump({'lens':lens,'ident':path}, open('scratch/t104/path.json','w'))
