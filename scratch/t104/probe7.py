import sys, struct, runpy, collections, json
sys.path.insert(0,'D:/tmp2b/fm24/tools/python'); sys.path.insert(0,'scripts')
m=runpy.run_path('scripts/t38_multiframe.py', run_name='p')
codec=m['_codec'](); cache={}
raw=m['load_payload_mf'](codec,'server',24,cache)
n=struct.unpack_from('<I',raw,8)[0]
H=14; F=8; T=13; end=len(raw)-F
ALLOW=(0,10,11)
cands=collections.defaultdict(list)
for p in range(H, end-(T-1)):
    if raw[p+12] not in ALLOW: continue
    a,b,c=struct.unpack_from('<III',raw,p)
    if a<n and b==c and b: cands[a].append((p,b))
for k in cands: cands[k].sort()
cur={(H,0):(None,None)}; hist=[]
for i in range(n):
    new={}
    for (curp,last) in cur:
        for p,u in cands[i]:
            if p<curp or u<=last: continue
            new.setdefault((p+T,u),(p,(curp,last)))
    pruned={}; best=None
    for k in sorted(new):
        if best is not None and k[1]>=best: continue
        pruned[k]=new[k]; best=k[1]
    hist.append(pruned); cur=set(pruned)
fin=[k for k in cur if k[0]==end][0]
path=[]; key=fin
for i in range(n,0,-1):
    p,prev=hist[i-1][key]; path.append((p,key[1],raw[p+12])); key=prev
path.reverse()
lens=[path[i][0]-(H if i==0 else path[i-1][0]+T) for i in range(n)]
def body(i):
    s=H if i==0 else path[i-1][0]+T
    return raw[s:path[i][0]]
json.dump({'lens':lens,'ident':[[p,u,s] for p,u,s in path]}, open('scratch/t104/path.json','w'))
sel=collections.Counter(x[2] for x in path)
nat=[i for i in range(n) if path[i][2]==11]
print('nat rows',len(nat),'lens',collections.Counter(lens[i] for i in nat).most_common(10))
# check 49B prefix parse: u32 x12? inspect first 49 bytes of nat rows
b=body(nat[0]); print('nat0 49B', b[:49].hex())
for i in nat[:8]:
    bb=body(i)
    print(i, lens[i], bb[:49].hex(), 'c@48', bb[48])
