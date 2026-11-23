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
cur={(H,0):(None,None)}; hist=[]
for i in range(n):
    new={}
    for (curp,last),(pp,pu) in cur.items():
        for p,u in cands[i]:
            if p<curp or u<=last: continue
            new.setdefault((p+T,u),(p,(curp,last)))
    pruned={}; best=None
    for k in sorted(new):
        if best is not None and k[1]>=best: continue
        pruned[k]=new[k]; best=k[1]
    hist.append(pruned); cur=pruned
fin=[k for k in cur if k[0]==end][0]
path=[]; key=fin
for i in range(n,0,-1):
    p,prev=hist[i-1][key]; path.append((p,key[1],raw[p+12])); key=prev
path.reverse()
lens=[path[i][0]-(H if i==0 else path[i-1][0]+T) for i in range(n)]
def body(i):
    s=H if i==0 else path[i-1][0]+T
    return raw[s:path[i][0]]
# test TEAM layout hypothesis for selector 10
ok=0; bad=[]
cntvals=collections.Counter()
for i in range(n):
    if path[i][2]!=10: continue
    b=body(i)
    c=struct.unpack_from('<H',b,33)[0]
    cntvals[c]+=1
    if len(b)==53+4*c: ok+=1
    elif len(bad)<5: bad.append((i,len(b),c))
print('TEAM rows len==53+4c:',ok,'bad',len(bad),bad[:5])
print('count hist top', cntvals.most_common(5))
# nat rows
nat=[i for i in range(n) if path[i][2]==11]
print('nat rows',len(nat))
for i in nat[:6]:
    b=body(i); print(i,'len',len(b),'c0',struct.unpack_from('<H',b,48)[0], 'first16', b[:16].hex())
# try: len = 49 + item + 53 + 4c
sols=[]
for i in nat:
    b=body(i)
    for itm in range(0,40):
        if len(b) < 49+itm+53: continue
        c=struct.unpack_from('<H',b,49+itm+33)[0]
        if len(b)==49+itm+53+4*c: sols.append((i,itm,c))
print('item size candidates', collections.Counter(s[1] for s in sols))
print(sols[:8])
